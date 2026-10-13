"""Close the loop: compare the calendar with what is actually in each Klaviyo account.

    python3 tools/reconcile.py <klaviyo-export.json> [--market eu] [--from 2026-11-01] [--to 2026-11-30] [--today 2026-11-20]

The export is the raw JSON from the Klaviyo connector's get_campaigns (email channel,
include campaign-messages): one response or a list of pages. Prints a Slack-ready report
and writes reports/reconcile-<market>-<date>.json. Exit 1 if anything is wrong.

Catches: calendar sends missing from Klaviyo, wrong date or time, no recipients, approved
but not scheduled, scheduled but never approved, subject differs from approved copy,
cancelled sends, and scheduled Klaviyo sends that aren't on the calendar.
"""
import argparse
import datetime as dt
import json
import sys
from zoneinfo import ZoneInfo

from common import CAMPAIGNS, ROOT, approval_state, calendar_rows, config, load

BAD_STATUS = ("Cancelled", "Queued without Recipients")


def parse_export(raw):
    pages = raw if isinstance(raw, list) else [raw]
    campaigns, messages = {}, {}
    for page in pages:
        page = page.get("result", page)
        for inc in page.get("included", []) or []:
            if inc.get("type") == "campaign-message":
                messages[inc["id"]] = inc
        for c in page.get("data", []):
            campaigns[c["id"]] = c
    out = []
    for c in campaigns.values():
        a = c["attributes"]
        subject = None
        for m in (c.get("relationships", {}).get("campaign-messages", {}) or {}).get("data", []):
            msg = messages.get(m["id"], m)
            subject = (((msg.get("attributes") or {}).get("definition") or {}).get("content") or {}).get("subject")
        when = a.get("send_time") or (a.get("send_strategy") or {}).get("datetime") or a.get("scheduled_at")
        out.append({"id": c["id"], "name": a.get("name"), "status": a.get("status"), "send_time": when,
                    "scheduled": a.get("scheduled_at") is not None,
                    "audiences": (a.get("audiences") or {}).get("included") or [], "subject": subject})
    return out


def local(ts, tz):
    return dt.datetime.fromisoformat(ts).astimezone(ZoneInfo(tz)) if ts else None


def reconcile(export, market_id, start, end, today):
    cfg = config()
    market = cfg["markets"]["markets"][market_id]
    tz = market["timezone"]
    kl = parse_export(export)
    by_name = {}
    for c in kl:
        by_name.setdefault(c["name"], []).append(c)
    issues, ok = [], []

    rows = [r for r in calendar_rows().values()
            if market_id in r.get("markets", []) and start <= str(r["date"]) <= end]
    planned_names = set()
    for row in sorted(rows, key=lambda r: str(r["date"])):
        name = (row.get("klaviyo_name") or {}).get(market_id) if isinstance(row.get("klaviyo_name"), dict) \
            else row.get("klaviyo_name")
        planned_names.add(name)
        label = f"{row['date']} {row['id']}"
        found = by_name.get(name, [])
        days_left = (dt.date.fromisoformat(str(row["date"])) - today).days
        if not found:
            if days_left <= 3:
                issues.append(("error", label, f"not in Klaviyo (expected '{name}'), sends in {days_left} days"))
            continue
        if len(found) > 1:
            issues.append(("warn", label, f"{len(found)} Klaviyo campaigns named '{name}'"))
        c = found[0]
        when = local(c["send_time"], tz)
        problems = []
        if c["status"] and c["status"].startswith(BAD_STATUS):
            problems.append(("error", f"status '{c['status']}'"))
        if not c["audiences"]:
            problems.append(("error", "no recipients (no list or segment included)"))
        if when and str(when.date()) != str(row["date"]):
            problems.append(("error", f"date is {when.date()} in Klaviyo, calendar says {row['date']}"))
        if when and row.get("time") and when.strftime("%H:%M") != str(row["time"]):
            problems.append(("warn", f"time is {when:%H:%M} {tz}, calendar says {row['time']}"))
        final_state, _ = approval_state(row["id"], "final", cfg)
        if c["scheduled"] and final_state != "approved":
            problems.append(("error", f"scheduled in Klaviyo but final approval is {final_state}"))
        if not c["scheduled"] and c["status"] == "Draft" and final_state == "approved" and days_left <= 1:
            problems.append(("error", "approved but never scheduled"))
        copy = load(CAMPAIGNS / row["id"] / "copy" / f"{market['locale']}.yaml") or {}
        if copy.get("subject") and c["subject"] and copy["subject"] != c["subject"]:
            problems.append(("warn", f"subject in Klaviyo '{c['subject']}' ≠ approved '{copy['subject']}'"))
        issues += [(sev, label, msg) for sev, msg in problems]
        if not problems:
            ok.append(f"{label}: {c['status']}{' ' + when.strftime('%a %d %b %H:%M') if when else ''}")

    for c in kl:
        when = local(c["send_time"], tz)
        if c["scheduled"] and c["name"] not in planned_names and when and start <= str(when.date()) <= end:
            issues.append(("warn", f"{when.date()} {c['name']}", "scheduled in Klaviyo but not on the calendar"))
    return issues, ok


def slack_text(market_id, issues, ok, today):
    lines = [f"*Email check · {market_id.upper()} · {today}*"]
    errors = [i for i in issues if i[0] == "error"]
    lines.append(f"{'🔴' if errors else '🟢'} {len(errors)} problems, "
                 f"{len(issues) - len(errors)} warnings, {len(ok)} on track")
    for sev, label, msg in issues:
        lines.append(f"{'🔴' if sev == 'error' else '🟡'} {label}: {msg}")
    for line in ok:
        lines.append(f"✅ {line}")
    return "\n".join(lines)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("export")
    ap.add_argument("--market", default="eu")
    ap.add_argument("--from", dest="start")
    ap.add_argument("--to", dest="end")
    ap.add_argument("--today")
    a = ap.parse_args(argv)
    today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
    start = a.start or str(today)
    end = a.end or str(today + dt.timedelta(days=30))
    issues, ok = reconcile(json.loads(open(a.export).read()), a.market, start, end, today)
    print(slack_text(a.market, issues, ok, today))
    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / f"reconcile-{a.market}-{today}.json").write_text(json.dumps(
        {"market": a.market, "today": str(today), "issues": issues, "ok": ok}, indent=2, ensure_ascii=False))
    return 1 if any(i[0] == "error" for i in issues) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
