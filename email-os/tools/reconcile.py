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
                    "is_local": ((a.get("send_strategy") or {}).get("options") or {}).get("is_local", False),
                    "audiences": (a.get("audiences") or {}).get("included") or [], "subject": subject})
    return out


def local(ts, tz):
    return dt.datetime.fromisoformat(ts).astimezone(ZoneInfo(tz)) if ts else None


def local_naive(c, tz):
    """Klaviyo local-time sends store wall-clock time as UTC; static sends are real UTC."""
    if not c["send_time"]:
        return None
    t = dt.datetime.fromisoformat(c["send_time"])
    return t.replace(tzinfo=None) if c.get("is_local") else t.astimezone(ZoneInfo(tz)).replace(tzinfo=None)


def reconcile(export, market_id, start, end, today):
    cfg = config()
    market = cfg["markets"]["markets"][market_id]
    tz = market["timezone"]
    kl = parse_export(export)
    by_name = {}
    for c in kl:
        by_name.setdefault(c["name"], []).append(c)
    issues, ok = [], []
    matched = set()

    rows = [r for r in calendar_rows().values()
            if market_id in r.get("markets", []) and start <= str(r["date"]) <= end]
    for row in sorted(rows, key=lambda r: (str(r["date"]), str(r.get("time", "")))):
        name = row.get("klaviyo_name")
        name = name.get(market_id) if isinstance(name, dict) else name
        label = f"{row['date']} {row.get('time', '')} {row['id']}"
        want = f"{row['date']}T{row.get('time', '10:00')}"
        days_left = (dt.date.fromisoformat(str(row["date"])) - today).days
        found = by_name.get(name, [])
        problems = []
        if not found:  # fall back to the slot: same local date and time
            found = [c for c in kl if c["id"] not in matched and local_naive(c, tz)
                     and local_naive(c, tz).strftime("%Y-%m-%dT%H:%M") == want]
            if found:
                problems.append(("warn", f"named '{found[0]['name']}' in Klaviyo, calendar says '{name}'"))
        if not found:
            if days_left <= 7:
                issues.append(("error" if days_left <= 2 else "warn", label,
                               f"not in Klaviyo yet (expected '{name}'), sends in {days_left} days"))
            continue
        if len(found) > 1:
            problems.append(("warn", f"{len(found)} Klaviyo campaigns for this slot: "
                                     + ", ".join(f"'{c['name']}' ({c['status']})" for c in found)))
        c = found[0]
        matched.add(c["id"])
        when = local_naive(c, tz)
        if c["status"] and c["status"].startswith(BAD_STATUS):
            problems.append(("error", f"status '{c['status']}'"))
        if not c["audiences"]:
            problems.append(("error", "no recipients (no list or segment included)"))
        want_aud = row.get("audience_ids") or {}
        want_aud = want_aud.get(market_id) if isinstance(want_aud, dict) and market_id in want_aud else None
        if want_aud is not None and sorted(c["audiences"]) != sorted(want_aud.get("include") or []):
            problems.append(("error", f"audience is {c['audiences']} in Klaviyo, calendar says {want_aud.get('include')}"))
        elif want_aud is None and row.get("audience"):
            problems.append(("warn", f"calendar audience '{row['audience']}' has no Klaviyo ids yet; "
                                     f"Klaviyo uses {c['audiences']}"))
        if when and str(when.date()) != str(row["date"]):
            problems.append(("error", f"date is {when.date()} in Klaviyo, calendar says {row['date']}"))
        elif when and row.get("time") and when.strftime("%H:%M") != str(row["time"]):
            problems.append(("error", f"time is {when:%H:%M} in Klaviyo, calendar says {row['time']}"))
        if row.get("managed", True):
            final_state, _ = approval_state(row["id"], "final", cfg)
            if c["scheduled"] and final_state != "approved":
                problems.append(("error", f"scheduled in Klaviyo but final approval is {final_state}"))
            if not c["scheduled"] and c["status"] == "Draft" and final_state == "approved" and days_left <= 1:
                problems.append(("error", "approved but never scheduled"))
            copy = load(CAMPAIGNS / row["id"] / "copy" / f"{market['locale']}.yaml") or {}
            meta = load(CAMPAIGNS / row["id"] / "out" / f"{market_id}.meta.json") or {}
            subject = meta.get("subject") or copy.get("subject")
            if subject and c["subject"] and subject != c["subject"]:
                problems.append(("warn", f"subject in Klaviyo '{c['subject']}' ≠ approved '{subject}'"))
        else:
            if not c["scheduled"] and days_left <= 1:
                problems.append(("error", "still a draft, sends tomorrow or today"))
            plan = row.get("subject_plan")
            if plan and c["subject"] and plan.strip() != c["subject"].strip():
                problems.append(("warn", f"subject in Klaviyo '{c['subject']}' ≠ plan '{plan}'"))
        issues += [(sev, label, msg) for sev, msg in problems]
        if not [p for p in problems if p[0] == "error"]:
            ok.append(f"{label}: {c['status']}{' ' + when.strftime('%a %d %b %H:%M') if when else ''}")

    planned = {(r.get("klaviyo_name") or {}).get(market_id) if isinstance(r.get("klaviyo_name"), dict)
               else r.get("klaviyo_name") for r in rows}
    for c in kl:
        when = local_naive(c, tz)
        if c["id"] in matched or c["name"] in planned or not when or not (start <= str(when.date()) <= end):
            continue
        if c["scheduled"] or c["status"] in ("Sending", "Scheduled"):
            issues.append(("error", f"{when:%Y-%m-%d %H:%M} {c['name']}", "scheduled in Klaviyo but not on the calendar"))
    dupes = [n for n, cs in by_name.items() if len(cs) > 1 and n not in planned]
    for n in dupes:
        issues.append(("warn", n, f"{len(by_name[n])} Klaviyo campaigns share this name: "
                                  + ", ".join(f"{c['status']} {c['send_time'] or ''}" for c in by_name[n])))
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
