"""End-to-end tests on a throwaway copy of email-os/ with a fixture campaign (no network).

    python3 email-os/tests/test_system.py      (or pytest)
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
FIX = Path(__file__).resolve().parent / "fixtures"
CID = "2026-11-27-bf-public"
COPY = f"campaigns/{CID}/copy/en.yaml"
LAYOUT = f"campaigns/{CID}/layout.yaml"
PRODUCTS = {"3x-minimal-stack-set-for-him": ("3x Minimal Stack Set", "94.90"),
            "3x-minimal-stack-set-for-her": ("3x Minimal Stack Set", "94.90"),
            "2x-duo-minimal-set-for-him": ("2x Duo Minimal Set", "59.90"),
            "cuban-bracelet-for-him": ("Cuban Bracelet", "29.90"),
            "jewelry-case": ("Jewelry Case", "19.90")}
GROUPS = {"him-bracelets": "29.90", "him-sets": "59.90", "all": "19.90", "her-sets": "94.90"}


class Sandbox:
    def __init__(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "email-os"
        shutil.copytree(SRC, self.root, ignore=shutil.ignore_patterns(
            "out", "lint.json", "build.yaml", "ledger.jsonl", "reports", "__pycache__", "img", "tests"))
        for f in (self.root / "calendar").glob("*.yaml"):
            f.unlink()
        for d in (self.root / "campaigns").iterdir():
            shutil.rmtree(d)
        shutil.copy(FIX / "calendar.yaml", self.root / "calendar/2026-11.yaml")
        shutil.copytree(FIX / "campaign", self.root / "campaigns" / CID)
        (self.root / "approvals").mkdir(exist_ok=True)
        for m, dom, cur in (("eu", "cavaier.com", "EUR"), ("us", "us.cavaier.com", "USD"), ("de", "cavaier.com", "EUR")):
            prods = {h: {"title": t, "price": p, "compare_at": None, "available": True,
                         "images": [f"https://cdn.example/{h}-{i}.png" for i in range(3)],
                         "url": f"https://{dom}/products/{h}"} for h, (t, p) in PRODUCTS.items()}
            cols = {g: {"min_price": p, "path": "/collections/x"} for g, p in GROUPS.items()}
            (self.root / "data/facts" / f"{m}.json").write_text(json.dumps(
                {"market": m, "currency": cur, "fetched_at": int(time.time()), "products": prods, "collections": cols}))

    def run(self, tool, *args, stdin=None):
        return subprocess.run([sys.executable, str(self.root / "tools" / tool), *args], input=stdin,
                              capture_output=True, text=True, cwd=self.root / "tools")

    def lint(self, *flags):
        self.run("lint.py", CID, *flags)
        return json.loads((self.root / "campaigns" / CID / "lint.json").read_text())

    def errors(self, *flags):
        return {f["rule"] for f in self.lint(*flags)["findings"] if f["severity"] == "error"}

    def findings(self, *flags):
        return self.lint(*flags)["findings"]

    def edit_yaml(self, rel, fn):
        p = self.root / rel
        data = yaml.safe_load(p.read_text())
        fn(data)
        p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True))

    def meta(self, market="eu"):
        return json.loads((self.root / f"campaigns/{CID}/out/{market}.meta.json").read_text())

    def host_images(self):
        """Pretend tools/images.py prepared and hosted every image."""
        self.run("render.py", CID)
        lock = {"images": {}}
        for m in ("eu", "us"):
            for img in self.meta(m)["images"]:
                lock["images"][img["id"]] = {"source_url": img["source_url"], "file": "eos-x.jpg",
                                             "bytes": 120_000, "url": f"https://cdn.shopify.com/eos-{abs(hash(img['id']))}.jpg"}
        (self.root / f"campaigns/{CID}/images.lock.yaml").write_text(yaml.safe_dump(lock))

    def prompt(self, text):
        out = self.run("gate.py", "prompt", stdin=json.dumps({"prompt": text, "session_id": "t"})).stdout
        return json.loads(out)["hookSpecificOutput"]["additionalContext"] if out.strip() else ""

    def pretool(self, tool, inp):
        out = self.run("gate.py", "pretool", stdin=json.dumps({"tool_name": tool, "tool_input": inp,
                                                              "cwd": str(self.root)})).stdout
        return json.loads(out)["hookSpecificOutput"] if out.strip() else None

    def klaviyo_dumps(self, market="eu", **override):
        """Connector responses as the builder would save them, matching the rendered email."""
        d = self.root / f"campaigns/{CID}/out"
        meta = self.meta(market)
        tpl = {"data": {"type": "template", "id": "T1", "attributes": {
            "html": override.get("html", (d / f"{market}.html").read_text()),
            "text": (d / f"{market}.txt").read_text()}}}
        msg = {"data": {"type": "campaign-message", "id": "M1", "attributes": {"definition": {"content": {
            "subject": override.get("subject", meta["subject"]), "preview_text": meta["preview"]}}}},
            "included": [{"type": "campaign", "id": "K1", "attributes": {
                "name": "KA_W48_Nov27_T01", "status": "Draft",
                "audiences": {"included": override.get("audiences", ["VSrsMu"]), "excluded": []},
                "send_strategy": {"method": "static", "datetime": override.get("datetime", "2026-11-27T10:00:00+00:00"),
                                  "options": {"is_local": True}}}}]}
        tp, mp = self.tmp / "tpl.json", self.tmp / "msg.json"
        tp.write_text(json.dumps(tpl))
        mp.write_text(json.dumps(msg))
        return str(tp), str(mp)


# -- rendering and rules ------------------------------------------------------------

def test_fixture_passes():
    assert Sandbox().lint()["ok"]


def test_tokens_fill_live_prices_per_market():
    s = Sandbox()
    s.lint()
    assert s.meta("eu")["preview"] == "The 3x Set for €66.43. No code needed."
    assert s.meta("us")["preview"] == "The 3x Set for $66.43. No code needed."
    html = (s.root / f"campaigns/{CID}/out/eu.html").read_text()
    assert "From €20.93" in html and "From €41.93" in html  # 29.90 and 59.90 at 30% off


def test_typed_price_and_wrong_percent_are_caught():
    s = Sandbox()
    s.edit_yaml(COPY, lambda c: c["strings"].update({"hero.body": "Now only €66.43, that's 40% off."}))
    assert "R05" in s.errors()


def test_discount_codes_must_match_the_offer():
    s = Sandbox()
    s.edit_yaml("calendar/2026-11.yaml", lambda cal: cal["rows"][0]["offer"].update({"code": "BF26"}))
    msgs = [f["msg"] for f in s.findings() if f["rule"] == "R05"]
    assert any("never gives it" in m for m in msgs)
    s.edit_yaml(COPY, lambda c: c["strings"].update({"hero.body": "Use code BF25 at checkout."}))
    assert any("BF25" in f["msg"] for f in s.findings() if f["rule"] == "R05")
    s.edit_yaml(COPY, lambda c: c["strings"].update({"hero.body": "Use code {code} at checkout."}))
    assert "R05" not in s.errors()
    s.lint()
    assert "Use code BF26 at checkout." in (s.root / f"campaigns/{CID}/out/eu.html").read_text()


def test_banned_phrase_is_caught():
    s = Sandbox()
    s.edit_yaml(COPY, lambda c: c["strings"].update({"section.title": "Free case with every set"}))
    assert "R06" in s.errors()


def test_button_must_name_its_product():
    s = Sandbox()
    s.edit_yaml(COPY, lambda c: c["strings"].update({"p2.cta": "Shop now"}))
    assert "R02" in s.errors()


def test_two_products_in_one_row_is_caught_but_same_family_is_fine():
    s = Sandbox()
    s.edit_yaml(LAYOUT, lambda l: l["blocks"][3].update(
        {"product": ["3x-minimal-stack-set-for-him", "2x-duo-minimal-set-for-him"]}))
    assert "R03" in s.errors()
    s.edit_yaml(LAYOUT, lambda l: l["blocks"][3].update(
        {"product": ["3x-minimal-stack-set-for-him", "3x-minimal-stack-set-for-her"]}))
    assert "R03" not in s.errors()


def test_second_accent_colour_is_caught():
    s = Sandbox()
    t = s.root / "templates/email.html.j2"
    t.write_text(t.read_text().replace("text-decoration:line-through", "text-decoration:line-through;color:#FFCC00"))
    assert "R01" in s.errors()


def test_reviews_render_word_for_word_from_the_ledger():
    s = Sandbox()
    (s.root / "data/reviews.yaml").write_text(yaml.safe_dump({"reviews": [
        {"id": "rv-1", "text": "Exact words.", "author": "A", "rating": 5, "platform": "Trustpilot",
         "source_url": "https://www.trustpilot.com/reviews/x"}]}))
    s.edit_yaml(LAYOUT, lambda l: l["blocks"].insert(6, {"type": "review", "review": "rv-1"}))
    assert s.lint()["ok"]
    assert "Exact words." in (s.root / f"campaigns/{CID}/out/eu.html").read_text()
    s.edit_yaml("data/reviews.yaml", lambda r: r["reviews"][0].pop("source_url"))
    assert "R04" in s.errors()


def test_localization_missing_key_and_overflow():
    s = Sandbox()
    s.edit_yaml("config/markets.yaml", lambda c: c["markets"]["de"].update({"active": True}))
    s.edit_yaml("calendar/2026-11.yaml", lambda cal: cal["rows"][0]["markets"].append("de"))
    en = yaml.safe_load((s.root / COPY).read_text())
    de = json.loads(json.dumps(en))
    de["strings"] = {k: v + " (DE)" for k, v in en["strings"].items()}
    de["strings"]["hero.headline"] = "30% Rabatt auf wirklich absolut alles."
    del de["strings"]["p1.body"]
    (s.root / f"campaigns/{CID}/copy/de.yaml").write_text(yaml.safe_dump(de, allow_unicode=True))
    f = s.findings()
    assert any(x["rule"] == "R07" and "missing key 'p1.body'" in x["msg"] for x in f)
    assert any(x["rule"] == "R07" and x["severity"] == "warn" and "hero.headline" in x["msg"] for x in f)


def test_links_must_stay_on_market_domain():
    s = Sandbox()
    s.edit_yaml(LAYOUT, lambda l: l["blocks"][6]["button"].update({"url": "https://evil.example/x"}))
    assert "R10" in s.errors()
    s.edit_yaml(LAYOUT, lambda l: l["blocks"][6]["button"].update({"url": "https://www.trustpilot.com/review/cavaier.com"}))
    assert "R10" not in s.errors()


def test_near_copy_of_a_recent_layout_is_flagged():
    s = Sandbox()
    s.edit_yaml("calendar/2026-11.yaml", lambda cal: cal["rows"].append(
        {**cal["rows"][0], "id": "2026-11-28-next", "date": "2026-11-28"}))
    shutil.copytree(s.root / f"campaigns/{CID}", s.root / "campaigns/2026-11-28-next")
    s.edit_yaml("campaigns/2026-11-28-next/layout.yaml", lambda l: l["blocks"].insert(3, {"type": "divider"}))
    r = subprocess.run([sys.executable, str(s.root / "tools/lint.py"), "2026-11-28-next"], capture_output=True, text=True)
    assert "R11" in r.stdout and "the same as" in r.stdout


def test_plain_text_send():
    s = Sandbox()
    (s.root / LAYOUT).write_text(yaml.safe_dump({"style": "plain", "blocks": [
        {"type": "para", "text": "p.hi"}, {"type": "para", "text": "p.body"},
        {"type": "link", "button": {"label": "p.link", "collection": "all"}},
        {"type": "para", "text": "p.sign"},
        {"type": "footer", "unsubscribe": "footer.unsubscribe"}]}))
    s.edit_yaml(COPY, lambda c: c["strings"].update({"p.hi": "Hi,", "p.body": "Quick one: the case comes with every set.",
                                                     "p.link": "See the sets", "p.sign": "Eli"}))
    assert s.lint()["ok"]
    html = (s.root / f"campaigns/{CID}/out/eu.html").read_text()
    assert "<img" not in html and "See the sets" in html


def test_weight_rule_images_must_be_hosted_for_final():
    s = Sandbox()
    assert any(f["rule"] == "R16" and f["severity"] == "warn" for f in s.findings())
    assert "R16" in s.errors("--final")
    s.host_images()
    assert "R16" not in s.errors("--final")
    assert "cdn.shopify.com/eos-" in (s.root / f"campaigns/{CID}/out/eu.html").read_text()


def test_html_stays_under_gmail_clip():
    s = Sandbox()
    s.lint()
    assert s.meta()["html_bytes"] < 90_000


# -- gates --------------------------------------------------------------------------

def test_gates_in_order_and_only_from_human_prompt():
    s = Sandbox()
    assert "approve calendar first" in s.prompt(f"APPROVE {CID} copy")
    assert "✓" in s.prompt(f"APPROVE {CID} calendar")
    assert "✓" in s.prompt(f"looks good\nAPPROVE {CID} copy,layout")
    d = s.pretool("Write", {"file_path": str(s.root / "approvals/ledger.jsonl"), "content": "{}"})
    assert d["permissionDecision"] == "deny"
    for cmd in ("rm email-os/approvals/ledger.jsonl", "sed -i 1d approvals/ledger.jsonl",
                "cat x | tee -a approvals/ledger.jsonl", "echo '{}' > \"approvals/ledger.jsonl\""):
        assert s.pretool("Bash", {"command": cmd})["permissionDecision"] == "deny", cmd
    assert s.pretool("Bash", {"command": "tail -5 email-os/approvals/ledger.jsonl"}) is None
    assert s.pretool("Bash", {"command": "cat > README.md <<'EOF'\nsee approvals/ledger.jsonl\nEOF"}) is None


def test_changed_copy_makes_approval_stale():
    s = Sandbox()
    s.prompt(f"APPROVE {CID} calendar,copy")
    s.edit_yaml(COPY, lambda c: c.update({"subject": "Black Friday: 30% off it all"}))
    assert "approve copy first" in s.prompt(f"APPROVE {CID} layout")


def test_final_refused_when_lint_fails():
    s = Sandbox()
    s.host_images()
    s.prompt(f"APPROVE {CID} calendar,copy")
    s.edit_yaml(LAYOUT, lambda l: l["blocks"][3].update({"product": ["3x-minimal-stack-set-for-him", "jewelry-case"]}))
    s.prompt(f"APPROVE {CID} layout")
    assert "lint has" in s.prompt(f"APPROVE {CID} final")


def test_verify_build_catches_klaviyo_drift():
    s = Sandbox()
    s.host_images()
    s.lint("--final")
    assert s.run("verify_build.py", CID, "eu", *s.klaviyo_dumps()).returncode == 0
    for bad, word in ((dict(subject="Black Friday: 30% off"), "subject"),
                      (dict(audiences=["SxyYP7"]), "audiences"),
                      (dict(datetime="2026-11-27T09:00:00+00:00"), "send time"),
                      (dict(html=(s.root / f"campaigns/{CID}/out/eu.html").read_text().replace("€66.43", "€66.47")), "HTML")):
        r = s.run("verify_build.py", CID, "eu", *s.klaviyo_dumps(**bad))
        assert r.returncode == 1 and word in r.stdout, (word, r.stdout)


def test_send_gate_end_to_end():
    s = Sandbox()
    send = lambda kid: s.pretool("mcp__Klaviyo__send_campaign", {"body": {"data": {"type": "campaign-send-job", "id": kid}}})
    assert send("UNKNOWN")["permissionDecision"] == "deny"
    s.host_images()
    s.lint("--final")
    s.run("verify_build.py", CID, "eu", *s.klaviyo_dumps())
    assert "gate 'calendar' is none" in send("K1")["permissionDecisionReason"]
    assert "✓" in s.prompt(f"APPROVE {CID} calendar,copy,layout,final").splitlines()[-1]
    assert send("K1") is None  # approved and verified: falls through to the normal confirmation
    # Klaviyo drifts (someone edits the subject in the UI) → re-verify fails → blocked
    s.run("verify_build.py", CID, "eu", *s.klaviyo_dumps(subject="Changed in Klaviyo"))
    assert "isn't verified" in send("K1")["permissionDecisionReason"]
    s.run("verify_build.py", CID, "eu", *s.klaviyo_dumps())
    assert send("K1") is None
    # copy changes after approval → re-rendered → approval stale
    s.edit_yaml(COPY, lambda c: c["strings"].update({"hero.body": "No code. It comes off at checkout."}))
    s.lint()
    assert send("K1")["permissionDecision"] == "deny"
    # tampering with the ledger is detected
    s.prompt(f"APPROVE {CID} copy,layout,final")
    s.run("verify_build.py", CID, "eu", *s.klaviyo_dumps())
    assert send("K1") is None
    led = s.root / "approvals/ledger.jsonl"
    lines = led.read_text().splitlines()
    led.write_text("\n".join(lines[:2] + lines[3:]) + "\n")
    assert "edited or removed" in send("K1")["permissionDecisionReason"]


def test_trial_builds_are_never_sent():
    s = Sandbox()
    s.host_images()
    s.lint("--final")
    tp, mp = s.klaviyo_dumps()
    msg = json.loads(Path(mp).read_text())
    msg["included"][0]["attributes"]["name"] = "EOS TEST · KA_W48_Nov27_T01"
    Path(mp).write_text(json.dumps(msg))
    assert s.run("verify_build.py", CID, "eu", tp, mp).returncode == 0
    s.prompt(f"APPROVE {CID} calendar,copy,layout,final")
    d = s.pretool("mcp__Klaviyo__send_campaign", {"body": {"data": {"type": "campaign-send-job", "id": "K1"}}})
    assert d["permissionDecision"] == "deny" and "never sent" in d["permissionDecisionReason"]


def test_test_sends_ask():
    s = Sandbox()
    assert s.pretool("mcp__Klaviyo__create_template_preview_send_job", {})["permissionDecision"] == "ask"


# -- daily check ----------------------------------------------------------------------

def camp(cid, name, status, when, audiences, scheduled, subject="x"):
    return {"type": "campaign", "id": cid, "attributes": {
        "name": name, "status": status, "scheduled_at": "2026-11-20T10:00:00+00:00" if scheduled else None,
        "send_time": when if scheduled else None, "audiences": {"included": audiences, "excluded": []},
        "send_strategy": {"method": "static", "datetime": when, "options": {"is_local": True}}},
        "relationships": {"campaign-messages": {"data": [{"type": "campaign-message", "id": "m" + cid,
                                                          "attributes": {"definition": {"content": {"subject": subject}}}}]}}}


def reconcile(s, export, today="2026-11-20"):
    f = s.tmp / "export.json"
    f.write_text(json.dumps(export))
    return s.run("reconcile.py", str(f), "--market", "eu", "--from", "2026-11-01", "--to", "2026-11-30", "--today", today)


def test_reconcile_catches_wrong_date_audience_and_unapproved():
    s = Sandbox()
    r = reconcile(s, {"data": [
        camp("b", "KA_W48_Nov27_T01", "Scheduled", "2026-11-28T10:00:00+00:00", ["SxyYP7"], True),
        camp("c", "Something else", "Scheduled", "2026-11-25T10:00:00+00:00", ["VSrsMu"], True)]})
    assert r.returncode == 1
    for word in ("date is 2026-11-28", "audience is ['SxyYP7']", "final approval is none", "not on the calendar"):
        assert word in r.stdout, word


def test_reconcile_matches_renamed_drafts_by_slot():
    s = Sandbox()
    s.edit_yaml("calendar/2026-11.yaml", lambda cal: cal["rows"][0].update({"managed": False, "subject_plan": "Plan."}))
    r = reconcile(s, {"data": [camp("a", "01-J · Renamed", "Draft", "2026-11-27T10:00:00+00:00", [], False, "Other.")]})
    assert "named '01-J · Renamed' in Klaviyo" in r.stdout
    assert "no recipients" in r.stdout
    assert "≠ plan 'Plan.'" in r.stdout


def test_reconcile_warns_when_a_send_is_missing():
    s = Sandbox()
    assert "not in Klaviyo yet" in reconcile(s, {"data": []}, today="2026-11-26").stdout


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"ok   {name}")
            except Exception as e:
                fails += 1
                print(f"FAIL {name}: {e!r}")
    sys.exit(1 if fails else 0)
