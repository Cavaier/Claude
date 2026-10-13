"""Check that what is in Klaviyo is exactly what was approved, and record the build.

    python3 tools/verify_build.py <campaign-id> <market> <template.json> <message.json>
    python3 tools/verify_build.py <campaign-id> <market> --fetch <campaign-message-id>
        (reads Klaviyo directly with KLAVIYO_API_KEY: no agent retypes anything)

The builder saves two raw connector responses after building the draft:
  template.json  get_email_template(id) with fields html, text, name
  message.json   get_campaign_message(id, include campaign) with subject, preview, the
                 campaign's name, audiences, send_strategy and status

Klaviyo rewrites HTML when it saves a template (inlines CSS, sorts attributes, turns
entities into characters, drops <link> tags), so the HTML is compared by what a reader gets:
the visible text, every link and every image (src and alt), in order.

Checks: template content and text part equal out/<market>.html/.txt; the template read back
is the one assigned to the message; subject and preview equal the rendered ones; campaign name, audiences and send time equal the calendar row; status Draft.
Writes campaigns/<id>/build.yaml with verified: true/false. The send gate only lets a
campaign through when verified is true for the version that got final approval.
"""
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

import yaml

from common import CAMPAIGNS, calendar_rows, config, gate_hash, load


# A trial build next to the real one: "EOS TEST · <calendar name>". Verified like any build,
# but the send gate refuses it, always.
TEST_PREFIX = "EOS TEST · "


INVISIBLE = dict.fromkeys(map(ord, "\u034f\u200c\u200b\ufeff"), None)


class Fingerprint(HTMLParser):
    """What a reader gets from an email: text, links and images, in order."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text, self.links, self.images, self.skip = [], [], [], 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("style", "script", "head"):
            self.skip += tag != "head"
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.images.append((a.get("src"), a.get("alt")))

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)

    @classmethod
    def of(cls, html):
        fp = cls()
        fp.feed(html or "")
        words = " ".join(fp.text).translate(INVISIBLE).replace("\xa0", " ")
        return {"text": re.sub(r"\s+", " ", words).strip(), "links": fp.links, "images": fp.images}


def norm(text):
    return re.sub(r"\s+", " ", (text or "").translate(INVISIBLE).replace("\xa0", " ")).strip()


def first_diff(a, b):
    i = next((n for n in range(min(len(a), len(b))) if a[n] != b[n]), min(len(a), len(b)))
    return f"…{a[max(0, i - 50):i + 50]!r}… vs approved …{b[max(0, i - 50):i + 50]!r}…"


def fetch(path):
    req = urllib.request.Request(f"https://a.klaviyo.com/api/{path}", headers={
        "Authorization": f"Klaviyo-API-Key {os.environ['KLAVIYO_API_KEY']}",
        "revision": "2024-10-15", "accept": "application/vnd.api+json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


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


def campaign_of(msg):
    """The campaign resource, wherever this response shape puts it."""
    inc = next((i for i in msg.get("included", []) if i.get("type") == "campaign"), None)
    if inc:
        return inc
    rel = first(msg, "data.relationships.campaign.data") or {}
    return rel if rel.get("attributes") else {}


def verify(campaign_id, market, template_json, message_json):
    cfg = config()
    row = calendar_rows()[campaign_id]
    d = CAMPAIGNS / campaign_id
    out_html = (d / "out" / f"{market}.html").read_text()
    out_txt_path = d / "out" / f"{market}.txt"
    meta = load(d / "out" / f"{market}.meta.json")
    if template_json == "--fetch":  # direct read, no transcription
        msg = fetch(f"campaign-messages/{message_json}?include=campaign,template")
        tid = first(msg, "data.relationships.template.data.id")
        tpl = fetch(f"templates/{tid}")
    else:
        tpl = unwrap(json.loads(Path(template_json).read_text()))
        msg = unwrap(json.loads(Path(message_json).read_text()))

    tdata = tpl.get("data", tpl)
    t_attr = tdata.get("attributes", {})
    m_attr = msg.get("data", {}).get("attributes", {})
    campaign = campaign_of(msg)
    c_attr = campaign.get("attributes", {})
    content = first(m_attr, "definition.content") or {}

    problems = []

    def check(name, got, want):
        if got != want:
            problems.append(f"{name}: Klaviyo has {got!r}, approved is {want!r}")

    assigned = first(msg, "data.relationships.template.data.id")
    if assigned and tdata.get("id") and assigned != tdata.get("id"):
        problems.append(f"read back template {tdata.get('id')}, but the message uses {assigned} "
                        "(Klaviyo clones a template when it's assigned: read the assigned one)")
    got, want = Fingerprint.of(t_attr.get("html")), Fingerprint.of(out_html)
    if got["text"] != want["text"]:
        problems.append(f"text in Klaviyo's template differs: {first_diff(got['text'], want['text'])}")
    if got["links"] != want["links"]:
        bad = next((f"{a} ≠ {b}" for a, b in zip(got["links"], want["links"]) if a != b),
                   f"{len(got['links'])} links vs {len(want['links'])}")
        problems.append(f"links in Klaviyo's template differ: {bad}")
    if got["images"] != want["images"]:
        bad = next((f"{a} ≠ {b}" for a, b in zip(got["images"], want["images"]) if a != b),
                   f"{len(got['images'])} images vs {len(want['images'])}")
        problems.append(f"images in Klaviyo's template differ: {bad}")
    if out_txt_path.exists():
        if t_attr.get("text") is None:
            problems.append("Klaviyo's template has no plain-text part")
        elif norm(t_attr["text"]) != norm(out_txt_path.read_text()):
            problems.append(f"plain-text part differs: {first_diff(norm(t_attr['text']), norm(out_txt_path.read_text()))}")
    check("subject", content.get("subject"), meta["subject"])
    check("preview", content.get("preview_text"), meta["preview"])
    want_name = per_market(row.get("klaviyo_name"), market)
    is_test = (c_attr.get("name") or "").startswith(TEST_PREFIX)
    check("campaign name", c_attr.get("name"), (TEST_PREFIX + want_name) if is_test else want_name)
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
        "test": is_test,
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
