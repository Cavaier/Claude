"""Human gates, enforced by Claude Code hooks (wired in .claude/settings.json).

    gate.py prompt    UserPromptSubmit: records approvals typed by the human
    gate.py pretool   PreToolUse: protects the ledger, blocks unapproved sends

Approvals can only come from a line the human typed into the prompt:

    APPROVE <campaign-id> <gate>[,<gate>...]      gates: calendar, copy, layout, final
    REVOKE  <campaign-id> <gate>

Subagents never trigger UserPromptSubmit, so an agent can't approve, and a relayed
"Eli said it's fine" records nothing. Each approval stores the hash of exactly what was
approved; if that content changes afterwards the approval goes stale.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

from common import CAMPAIGNS, GATES, LEDGER, ROOT, approval_state, canonical, gate_hash, ledger_entries, load, sha

CMD = re.compile(r"^\s*(APPROVE|REVOKE)\s+(\S+)\s+([a-z,]+)\s*$", re.M)
REQUIRES = {"calendar": [], "copy": ["calendar"], "layout": ["calendar", "copy"],
            "final": ["calendar", "copy", "layout"]}


def approver():
    if os.environ.get("EMAIL_OS_APPROVER"):
        return os.environ["EMAIL_OS_APPROVER"]
    try:
        return subprocess.run(["git", "config", "user.email"], capture_output=True, text=True,
                              cwd=ROOT).stdout.strip() or "owner"
    except OSError:
        return "owner"


def append(entry):
    entries = ledger_entries()
    entry["seq"] = len(entries) + 1
    entry["prev"] = entries[-1]["entry_hash"] if entries else ""
    entry["entry_hash"] = sha(canonical(entry))
    LEDGER.parent.mkdir(exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def verify_chain():
    prev = ""
    for e in ledger_entries():
        body = {k: v for k, v in e.items() if k != "entry_hash"}
        if e["prev"] != prev or sha(canonical(body)) != e["entry_hash"]:
            return f"ledger entry {e.get('seq')} was edited or removed outside the hook"
        prev = e["entry_hash"]
    return None


def approve(campaign_id, gate, session):
    if not (CAMPAIGNS / campaign_id).exists() and gate != "calendar":
        return f"✗ {campaign_id}: no such campaign folder"
    missing = [g for g in REQUIRES[gate] if approval_state(campaign_id, g)[0] != "approved"]
    if missing:
        return f"✗ {campaign_id} {gate}: approve {', '.join(missing)} first (missing or changed since approval)"
    if gate == "final":
        import contextlib
        import io

        from lint import Linter
        with contextlib.redirect_stdout(io.StringIO()):  # hook stdout must stay pure JSON
            result = Linter(campaign_id, final=True).run()  # renders, so 'final' is what's on disk now
        if not result["ok"]:
            first = "; ".join(f["msg"] for f in result["findings"] if f["severity"] == "error")[:400]
            return f"✗ {campaign_id} final: lint has {result['errors']} errors, not recorded. {first}"
    h = gate_hash(campaign_id, gate)
    if h is None:
        return f"✗ {campaign_id} {gate}: nothing to approve yet"
    append({"action": "approve", "campaign": campaign_id, "gate": gate, "hash": h,
            "by": approver(), "via": "human-prompt", "session": session, "at": int(time.time())})
    return f"✓ {campaign_id} {gate} approved (hash {h})"


def revoke(campaign_id, gate, session):
    append({"action": "revoke", "campaign": campaign_id, "gate": gate, "hash": None,
            "by": approver(), "via": "human-prompt", "session": session, "at": int(time.time())})
    return f"✓ {campaign_id} {gate} revoked"


def on_prompt(event):
    lines = []
    for action, cid, gates in CMD.findall(event.get("prompt", "")):
        for gate in gates.split(","):
            if gate not in GATES:
                lines.append(f"✗ unknown gate '{gate}' (use {', '.join(GATES)})")
                continue
            fn = approve if action == "APPROVE" else revoke
            lines.append(fn(cid, gate, event.get("session_id")))
    if not lines:
        return None
    text = ("Email gate ledger (written by the hook from the human's own message; do not "
            "write approvals yourself):\n" + "\n".join(lines))
    return {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": text}}


def decision(kind, reason):
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": kind,
                                   "permissionDecisionReason": reason}}


# A write whose target is the approvals folder: redirect, tee, in-place edit, or file command.
# Text that merely mentions the path (a heredoc README, a grep) passes; the hash chain catches
# anything that slips through.
LEDGER_WRITE = re.compile(
    r"(>>?|\btee\s+(-a\s+)?)\s*['\"]?[^\s|;&'\"]*approvals/"
    r"|\b(rm|mv|cp|truncate|dd|sed\s+-i|git\s+(checkout|restore|rm))\b[^|;&\n]*approvals/")


def campaign_for_klaviyo_id(kid):
    for build in CAMPAIGNS.glob("*/build.yaml"):
        data = load(build) or {}
        for market, info in (data.get("markets") or {}).items():
            if (info or {}).get("klaviyo_campaign_id") == kid:
                return build.parent.name, market
    return None, None


def on_pretool(event):
    tool, inp = event.get("tool_name", ""), event.get("tool_input") or {}
    approvals_dir = (ROOT / "approvals").resolve()

    if tool in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
        path = inp.get("file_path") or inp.get("notebook_path") or ""
        p = Path(path) if os.path.isabs(path) else Path(event.get("cwd", ".")) / path
        if approvals_dir in p.resolve().parents or p.resolve() == approvals_dir:
            return decision("deny", "The approval ledger is written only by the hook from the human's "
                                    "own 'APPROVE <campaign> <gate>' message. Agents never approve.")
    elif tool == "Bash":
        cmd = inp.get("command", "")
        if LEDGER_WRITE.search(cmd):
            return decision("deny", "Commands that could change the approval ledger are blocked. "
                                    "Read it with cat/tail, or run tools/status.py.")
    elif tool.endswith("__send_campaign"):
        kid = ((inp.get("body") or {}).get("data") or {}).get("id")
        cid, market = campaign_for_klaviyo_id(kid)
        if cid is None:
            return decision("deny", f"Klaviyo campaign {kid} is not in any campaigns/*/build.yaml. "
                                    "Only campaigns built by this system can be scheduled.")
        broken = verify_chain()
        if broken:
            return decision("deny", broken)
        for gate in GATES:
            state, _ = approval_state(cid, gate)
            if state != "approved":
                return decision("deny", f"{cid}: gate '{gate}' is {state}. The human must type "
                                        f"'APPROVE {cid} {gate}' after reviewing the current version.")
        build = ((load(CAMPAIGNS / cid / "build.yaml") or {}).get("markets") or {}).get(market) or {}
        if not build.get("verified"):
            return decision("deny", f"{cid} [{market}]: the Klaviyo draft isn't verified against the approved "
                                    f"version (tools/verify_build.py). {'; '.join(build.get('problems') or [])}")
        if build.get("final_hash") != approval_state(cid, "final")[1]["hash"]:
            return decision("deny", f"{cid} [{market}]: the Klaviyo draft was verified against a different "
                                    "version than the one approved. Rebuild and verify, or get final approval again.")
        return None  # approved: fall through to the normal permission prompt
    elif tool.endswith("__create_template_preview_send_job"):
        return decision("ask", "Test send. Only if someone asked for it (no unasked messages).")
    elif re.search(r"__(delete_\w+|cancel_campaign_send)$", tool):
        return decision("ask", "Destructive Klaviyo change. Confirm a backup exists (rule H02).")
    return None


def main():
    mode = sys.argv[1]
    event = json.load(sys.stdin)
    try:
        out = on_prompt(event) if mode == "prompt" else on_pretool(event)
    except Exception as e:  # fail closed on sends, open on everything else
        tool = event.get("tool_name", "")
        if tool.endswith("__send_campaign"):
            out = decision("deny", f"gate check crashed ({e}); refusing to send")
        else:
            print(f"email-os gate: {e}", file=sys.stderr)
            return 0
    if out:
        print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
