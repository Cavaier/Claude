"""Check that what is in Klaviyo is exactly what was approved, and record the build.

    python3 tools/verify_build.py <campaign-id> <market> <template.json> <message.json>

The builder saves two raw connector responses after building the draft:
  template.json  get_email_template(id) with fields html, text, name
  message.json   get_campaign_message(id, include campaign) with subject, preview, the
                 campaign's name, audiences, send_strategy and status

Checks: template HTML and text equal out/<market>.html/.txt; subject and preview equal the
rendered ones; campaign name, audiences and send time equal the calendar row; status Draft.
Writes campaigns/<id>/build.yaml with verified: true/false. The send gate only lets a
campaign through when verified is true for the version that got final approval.
"""
import datetime as dt
import json
import re
import sys
import time
from pathlib import Path

import yaml

from common import CAMPAIGNS, calendar_rows, config, gate_hash, load


def norm(html):
    return re.sub(r"\s+", " ", re.sub(r">\s+<", "><", html or "")).strip()


def first(obj, *keys):
    """Find the first value at any of the given dotted paths in a JSON:API response."""
    for path in keys:
        cur = obj
        for k in path.split("."):
            cur = cur.get(k) if isinstance(cur, dict) else None
            if cur is None:
                break
        if cur is not None:
            return cur
    return None


def unwrap(obj):
    obj = obj.get("result", obj)
    return obj


def per_market(value, market):
    return value.get(market) if isinstance(value, dict) else value


def expected_send(row, market_cfg):
    """(iso-ish local time string, is_local) the calendar asks for."""
    return f"{row['date']}T{row.get('time', '10:00')}", True


def verify(campaign_id, market, template_json, message_json):
    cfg = config()
    row = calendar_rows()[campaign_id]
    d = CAMPAIGNS / campaign_id
    out_html = (d / "out" / f"{market}.html").read_text()
    out_txt_path = d / "out" / f"{market}.txt"
    meta = load(d / "out" / f"{market}.meta.json")
    tpl = unwrap(json.loads(Path(template_json).read_text()))
    msg = unwrap(json.loads(Path(message_json).read_text()))

    tdata = tpl.get("data", tpl)
    t_attr = tdata.get("attributes", {})
    m_attr = msg.get("data", {}).get("attributes", {})
    campaign = next((i for i in msg.get("included", []) if i.get("type") == "campaign"), {})
    c_attr = campaign.get("attributes", {})
    content = first(m_attr, "definition.content") or {}

    problems = []

    def check(name, got, want):
        if got != want:
            problems.append(f"{name}: Klaviyo has {got!r}, approved is {want!r}")

    if norm(t_attr.get("html")) != norm(out_html):
        a, b = norm(t_attr.get("html")), norm(out_html)
        i = next((n for n in range(min(len(a), len(b))) if a[n] != b[n]), min(len(a), len(b)))
        problems.append(f"template HTML differs from out/{market}.html at char {i}: "
                        f"Klaviyo …{a[max(0, i - 40):i + 40]!r}… vs approved …{b[max(0, i - 40):i + 40]!r}…")
    if out_txt_path.exists() and t_attr.get("text") is not None and norm(t_attr["text"]) != norm(out_txt_path.read_text()):
        problems.append("template plain-text part differs from out/<market>.txt")
    check("subject", content.get("subject"), meta["subject"])
    check("preview", content.get("preview_text"), meta["preview"])
    check("campaign name", c_attr.get("name"), per_market(row.get("klaviyo_name"), market))
    want_aud = per_market(row.get("audience_ids") or {}, market) or {}
    got_aud = c_attr.get("audiences") or {}
    check("audiences included", sorted(got_aud.get("included") or []), sorted(want_aud.get("include") or []))
    check("audiences excluded", sorted(got_aud.get("excluded") or []), sorted(want_aud.get("exclude") or []))
    strat = c_attr.get("send_strategy") or {}
    want_local, _ = expected_send(row, cfg["markets"]["markets"][market])
    got_dt = strat.get("datetime")
    if not got_dt:
        problems.append("no send time set in Klaviyo")
    else:
        got = dt.datetime.fromisoformat(got_dt)
        if (strat.get("options") or {}).get("is_local"):
            got_local = got.strftime("%Y-%m-%dT%H:%M")  # local sends store wall-clock time as UTC
        else:
            tz = cfg["markets"]["markets"][market]["timezone"]
            from zoneinfo import ZoneInfo
            got_local = got.astimezone(ZoneInfo(tz)).strftime("%Y-%m-%dT%H:%M")
        check("send time (local)", got_local, want_local)
    check("status", c_attr.get("status"), "Draft")

    final = gate_hash(campaign_id, "final")
    path = d / "build.yaml"
    build = load(path) or {"campaign": campaign_id, "markets": {}}
    build["markets"][market] = {
        "klaviyo_campaign_id": campaign.get("id") or first(msg, "data.relationships.campaign.data.id"),
        "message_id": msg.get("data", {}).get("id"),
        "template_id": tdata.get("id"),
        "final_hash": final,
        "verified": not problems,
        "problems": problems,
        "verified_at": int(time.time()),
    }
    path.write_text(yaml.safe_dump(build, sort_keys=False, allow_unicode=True))
    if problems:
        print(f"NOT VERIFIED {campaign_id} [{market}]:")
        for p in problems:
            print(f"  ✗ {p}")
        return 1
    print(f"verified {campaign_id} [{market}] → Klaviyo {build['markets'][market]['klaviyo_campaign_id']} (hash {final})")
    return 0


if __name__ == "__main__":
    sys.exit(verify(*sys.argv[1:5]))
