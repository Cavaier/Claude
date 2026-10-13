"""End-to-end tests on a throwaway copy of email-os/ (no network: facts are faked).

    python3 -m pytest email-os/tests -q      or      python3 email-os/tests/test_system.py
"""
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import yaml

SRC = Path(__file__).resolve().parents[1]
CID = "2026-11-27-bf-public"
FACTS = {"3x-minimal-stack-set-for-him": ("3x Minimal Stack Set", "94.90"),
         "3x-minimal-stack-set-for-her": ("3x Minimal Stack Set", "94.90"),
         "2x-duo-minimal-set-for-him": ("2x Duo Minimal Set", "59.90"),
         "jewelry-case": ("Jewelry Case", "19.90")}


class Sandbox:
    def __init__(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "email-os"
        shutil.copytree(SRC, self.root, ignore=shutil.ignore_patterns("out", "lint.json", "build.yaml",
                                                                       "ledger.jsonl", "reports", "__pycache__"))
        (self.root / "approvals").mkdir(exist_ok=True)
        for m, dom in (("eu", "cavaier.com"), ("us", "us.cavaier.com"), ("de", "cavaier.com")):
            prods = {h: {"title": t, "price": p, "compare_at": None, "available": True,
                         "image": f"https://cdn.example/{h}.png", "images": [f"https://cdn.example/{h}-{i}.png" for i in range(3)],
                         "url": f"https://{dom}/products/{h}"} for h, (t, p) in FACTS.items()}
            (self.root / "data/facts" / f"{m}.json").write_text(json.dumps(
                {"market": m, "currency": "EUR", "fetched_at": int(time.time()), "products": prods}))

    def run(self, tool, *args, stdin=None):
        return subprocess.run([sys.executable, str(self.root / "tools" / tool), *args], input=stdin,
                              capture_output=True, text=True, cwd=self.root / "tools")

    def lint(self, *flags):
        self.run("lint.py", CID, *flags)
        return json.loads((self.root / "campaigns" / CID / "lint.json").read_text())

    def rules_hit(self, *flags):
        return {f["rule"] for f in self.lint(*flags)["findings"] if f["severity"] == "error"}

    def edit_yaml(self, rel, fn):
        p = self.root / rel
        data = yaml.safe_load(p.read_text())
        fn(data)
        p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))

    def prompt(self, text):
        out = self.run("gate.py", "prompt", stdin=json.dumps({"prompt": text, "session_id": "t"})).stdout
        return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out.strip() else ""

    def pretool(self, tool, inp):
        out = self.run("gate.py", "pretool", stdin=json.dumps({"tool_name": tool, "tool_input": inp,
                                                              "cwd": str(self.root)})).stdout
        return json.loads(out)["hookSpecificOutput"] if out.strip() else None


COPY = f"campaigns/{CID}/copy/en.yaml"
LAYOUT = f"campaigns/{CID}/layout.yaml"


def test_example_campaign_passes():
    assert Sandbox().lint()["ok"]


def test_typed_price_and_wrong_percent_are_caught():
    s = Sandbox()
    s.edit_yaml(COPY, lambda c: c["strings"].update({"hero.body": "Now only €66.43, that's 40% off."}))
    assert "R05" in s.rules_hit()


def test_banned_phrase_is_caught():
    s = Sandbox()
    s.edit_yaml(COPY, lambda c: c["strings"].update({"offer.title": "Free case with every set"}))
    assert "R06" in s.rules_hit()


def test_button_must_name_its_product():
    s = Sandbox()
    s.edit_yaml(COPY, lambda c: c["strings"].update({"p2.cta": "Shop now"}))
    assert "R02" in s.rules_hit()


def test_two_products_in_one_row_is_caught():
    s = Sandbox()
    s.edit_yaml(LAYOUT, lambda l: l["blocks"][3].update(
        {"product": ["3x-minimal-stack-set-for-him", "2x-duo-minimal-set-for-him"]}))
    assert "R03" in s.rules_hit()


def test_same_family_may_share_a_row():
    s = Sandbox()
    s.edit_yaml(LAYOUT, lambda l: l["blocks"][3].update(
        {"product": ["3x-minimal-stack-set-for-him", "3x-minimal-stack-set-for-her"]}))
    assert "R03" not in s.rules_hit()


def test_second_accent_colour_is_caught():
    s = Sandbox()
    t = s.root / "templates/email.html.j2"
    t.write_text(t.read_text().replace("color:{{ N[6] }};text-decoration:line-through", "color:#FFCC00;text-decoration:line-through"))
    assert "R01" in s.rules_hit()


def test_edited_review_is_caught():
    s = Sandbox()
    (s.root / "data/reviews.yaml").write_text(yaml.safe_dump({"reviews": [
        {"id": "rv-1", "text": "Exact words.", "author": "A", "rating": 5, "platform": "Trustpilot",
         "source_url": "https://www.trustpilot.com/reviews/x"}]}))
    s.edit_yaml(LAYOUT, lambda l: l["blocks"].insert(6, {"type": "review", "review": "rv-1"}))
    assert s.lint()["ok"]
    meta = s.root / f"campaigns/{CID}/out/eu.meta.json"
    m = json.loads(meta.read_text())
    m["reviews"][0]["text"] = "Exact words!"  # what a 'helpful' agent edit would look like
    meta.write_text(json.dumps(m))
    linter = s.run("lint.py", CID)  # re-renders from the ledger, so the edit can't survive
    assert "PASS" in linter.stdout


def test_localization_missing_key_and_overflow():
    s = Sandbox()
    cfg = s.root / "config/markets.yaml"
    c = yaml.safe_load(cfg.read_text()); c["markets"]["de"]["active"] = True
    cfg.write_text(yaml.safe_dump(c))
    s.edit_yaml("calendar/2026-11.yaml", lambda cal: cal["rows"][1]["markets"].append("de"))
    en = yaml.safe_load((s.root / COPY).read_text())
    de = json.loads(json.dumps(en))
    de["strings"] = {k: v + " (DE)" for k, v in en["strings"].items()}
    de["strings"]["hero.headline"] = "30% Rabatt auf wirklich absolut alles."
    del de["strings"]["p1.body"]
    (s.root / f"campaigns/{CID}/copy/de.yaml").write_text(yaml.safe_dump(de, allow_unicode=True))
    findings = s.lint()["findings"]
    assert any(f["rule"] == "R07" and "missing key 'p1.body'" in f["msg"] for f in findings)
    assert any(f["rule"] == "R07" and f["severity"] == "warn" and "hero.headline" in f["msg"] for f in findings)


def test_links_must_stay_on_market_domain():
    s = Sandbox()
    s.edit_yaml(LAYOUT, lambda l: l["blocks"][6]["button"].update({"url": "https://evil.example/x"}))
    assert "R10" in s.rules_hit()
    s.edit_yaml(LAYOUT, lambda l: l["blocks"][6]["button"].update({"url": "https://www.trustpilot.com/review/cavaier.com"}))
    assert "R10" not in s.rules_hit()


def test_gates_in_order_and_only_from_human_prompt():
    s = Sandbox()
    assert "approve calendar first" in s.prompt(f"APPROVE {CID} copy")
    assert "✓" in s.prompt(f"APPROVE {CID} calendar")
    assert "✓" in s.prompt(f"looks good\nAPPROVE {CID} copy,layout")
    # an agent trying to write the ledger directly
    d = s.pretool("Write", {"file_path": str(s.root / "approvals/ledger.jsonl"), "content": "{}"})
    assert d["permissionDecision"] == "deny"
    d = s.pretool("Bash", {"command": "echo '{}' >> email-os/approvals/ledger.jsonl"})
    assert d["permissionDecision"] == "deny"
    assert s.pretool("Bash", {"command": "tail -5 email-os/approvals/ledger.jsonl"}) is None
    for cmd in ("rm email-os/approvals/ledger.jsonl", "sed -i 1d approvals/ledger.jsonl",
                "cat x | tee -a approvals/ledger.jsonl", "echo '{}' > \"approvals/ledger.jsonl\""):
        assert s.pretool("Bash", {"command": cmd})["permissionDecision"] == "deny", cmd
    readme = "cat > README.md <<'EOF'\nApprovals live in approvals/ledger.jsonl\nEOF"
    assert s.pretool("Bash", {"command": readme}) is None


def test_changed_copy_makes_approval_stale():
    s = Sandbox()
    s.prompt(f"APPROVE {CID} calendar,copy")
    s.edit_yaml(COPY, lambda c: c.update({"subject": "Black Friday: 30% off it all"}))
    assert "approve copy first" in s.prompt(f"APPROVE {CID} layout")


def test_final_refused_when_lint_fails():
    s = Sandbox()
    s.prompt(f"APPROVE {CID} calendar,copy")
    s.edit_yaml(LAYOUT, lambda l: l["blocks"][3].update({"product": ["3x-minimal-stack-set-for-him", "jewelry-case"]}))
    s.prompt(f"APPROVE {CID} layout")
    assert "lint has" in s.prompt(f"APPROVE {CID} final")


def test_send_gate():
    s = Sandbox()
    send = lambda kid: s.pretool("mcp__Klaviyo__send_campaign", {"body": {"data": {"type": "campaign-send-job", "id": kid}}})
    assert send("UNKNOWN")["permissionDecision"] == "deny"
    s.lint()
    s.run("record_build.py", CID, "eu", "K1", "T1")
    assert "gate 'calendar' is none" in send("K1")["permissionDecisionReason"]
    s.prompt(f"APPROVE {CID} calendar,copy,layout,final")
    assert send("K1") is None  # approved: falls through to the normal confirmation
    # copy changes after approval → re-rendered → no longer the approved version
    s.edit_yaml(COPY, lambda c: c["strings"].update({"hero.body": "No code. It comes off at checkout."}))
    s.lint()
    assert send("K1")["permissionDecision"] == "deny"
    # tampering with the ledger is detected
    s.prompt(f"APPROVE {CID} copy,layout,final")
    s.run("record_build.py", CID, "eu", "K1", "T1")
    assert send("K1") is None
    led = s.root / "approvals/ledger.jsonl"
    lines = led.read_text().splitlines()
    led.write_text("\n".join(lines[:2] + lines[3:]) + "\n")
    assert "edited or removed" in send("K1")["permissionDecisionReason"]


def test_test_sends_ask():
    s = Sandbox()
    assert s.pretool("mcp__Klaviyo__create_template_preview_send_job", {})["permissionDecision"] == "ask"


def test_reconcile_catches_the_article_failures():
    s = Sandbox()
    s.prompt(f"APPROVE {CID} calendar")

    def camp(cid, name, status, when, audiences, scheduled):
        return {"type": "campaign", "id": cid, "attributes": {
            "name": name, "status": status, "scheduled_at": "2026-11-20T10:00:00+00:00" if scheduled else None,
            "send_time": when if scheduled else None, "audiences": {"included": audiences, "excluded": []},
            "send_strategy": {"method": "static", "datetime": when}}}

    export = {"data": [
        camp("a", "KA_W48_Nov23_T01", "Scheduled", "2026-11-24T08:00:00+00:00", [], True),   # no recipients + wrong date
        camp("b", "KA_W48_Nov27_T01", "Scheduled", "2026-11-27T08:00:00+00:00", ["VSrsMu"], True),  # never final-approved
        camp("c", "KA_W48_Nov25_X", "Scheduled", "2026-11-25T08:00:00+00:00", ["VSrsMu"], True),  # not on calendar
    ]}
    f = s.tmp / "export.json"
    f.write_text(json.dumps(export))
    r = s.run("reconcile.py", str(f), "--market", "eu", "--from", "2026-11-01", "--to", "2026-11-30", "--today", "2026-11-20")
    assert r.returncode == 1
    out = r.stdout
    assert "no recipients" in out
    assert "date is 2026-11-24" in out
    assert "final approval is none" in out
    assert "not on the calendar" in out


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print(f"ok   {name}")
            except Exception as e:
                fails += 1; print(f"FAIL {name}: {e!r}")
    sys.exit(1 if fails else 0)
