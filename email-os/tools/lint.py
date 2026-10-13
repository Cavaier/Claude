"""Check a campaign against the testable rules in config/rules.yaml.

    python3 tools/lint.py <campaign-id> [--final]

Renders first, then checks every active market. Writes campaigns/<id>/lint.json.
Exit 0 = no errors (warnings allowed), 1 = errors. --final adds the checks that only
apply right before the final approval (fresh facts, generated images checked).
"""
import json
import re
import sys
import time

from common import CAMPAIGNS, DATA, calendar_rows, campaign_markets, config, load
from render import RenderError, render

HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
PERCENT = re.compile(r"(\d+(?:[.,]\d+)?)\s?%")
PRICE = re.compile(r"[€$£]\s?\d|\d\s?[€$£]|\b\d+[.,]\d{2}\b|\b(?:EUR|USD|SEK|GBP)\b")
PLACEHOLDER = re.compile(r"\[[^\]]*\]|\bXX+\b|\{\{|\}\}|TBD|TK\b")


def norm_hex(h):
    h = h.upper()
    return "#" + "".join(c * 2 for c in h[1:]) if len(h) == 4 else h


def flatten_copy(copy):
    yield "subject", copy.get("subject") or ""
    yield "preview", copy.get("preview") or ""
    for k, v in (copy.get("strings") or {}).items():
        yield k, v if isinstance(v, str) else ""


class Linter:
    def __init__(self, campaign_id, final=False):
        self.id = campaign_id
        self.final = final
        self.cfg = config()
        self.rules = self.cfg["rules"]["rules"]
        self.dir = CAMPAIGNS / campaign_id
        self.row = calendar_rows().get(campaign_id)
        self.findings = []

    def add(self, rule, msg, market=None, severity=None):
        self.findings.append({"rule": rule, "severity": severity or self.rules[rule]["severity"],
                              "market": market, "msg": msg})

    # -- campaign-level rules -------------------------------------------------
    def r12_why(self):
        why = (self.row or {}).get("why") or {}
        ref = why.get("ref", "")
        if not ref or not why.get("note"):
            self.add("R12", "calendar row needs why.ref and why.note")
            return
        if ref.startswith("perf:"):
            month, _, row_id = ref[5:].partition("#")
            perf = load(DATA / "performance" / f"{month}.yaml") or {}
            if row_id not in {r.get("id") for r in perf.get("rows", [])}:
                self.add("R12", f"why.ref {ref} not found in data/performance/{month}.yaml")
        elif not ref.startswith(("plan:", "http")):
            self.add("R12", f"why.ref must be perf:<month>#<row>, plan:<url> or a URL, got '{ref}'")

    def r11_novelty(self):
        layout = load(self.dir / "layout.yaml")
        if not layout:
            return
        seq = [b["type"] for b in layout["blocks"]]
        others = []
        for cid, row in calendar_rows().items():
            other = load(CAMPAIGNS / cid / "layout.yaml")
            if cid != self.id and other and str(row["date"]) < str(self.row["date"]):
                others.append((str(row["date"]), cid, [b["type"] for b in other["blocks"]]))
        for _, cid, other_seq in sorted(others)[-3:]:
            if other_seq == seq:
                self.add("R11", f"same block sequence as {cid}: pick a different structure")

    def r03_one_product_per_row(self):
        layout = load(self.dir / "layout.yaml") or {"blocks": []}
        for i, b in enumerate(layout["blocks"]):
            if b["type"] != "product":
                continue
            handles = b["product"] if isinstance(b["product"], list) else [b["product"]]
            families = {self.cfg["products"].get(h, {}).get("family", h) for h in handles}
            unknown = [h for h in handles if h not in self.cfg["products"]]
            if unknown:
                self.add("R03", f"block {i}: {unknown} not in config/products.yaml")
            if len(families) > 1:
                self.add("R03", f"block {i}: {len(handles)} different products in one row {handles}")

    def r07_locales(self):
        master_locale = self.cfg["markets"]["master_locale"]
        master = load(self.dir / "copy" / f"{master_locale}.yaml")
        if master is None:
            self.add("R07", f"no master copy copy/{master_locale}.yaml")
            return
        mkeys = dict(flatten_copy(master))
        keep = set((master.get("keep_untranslated") or []))
        limits = master.get("max_len") or {}
        locales = {self.cfg["markets"]["markets"][m]["locale"] for m in campaign_markets(self.row, self.cfg)}
        for loc in sorted(locales):
            copy = load(self.dir / "copy" / f"{loc}.yaml")
            if copy is None:
                self.add("R07", f"copy/{loc}.yaml missing", market=loc)
                continue
            keys = dict(flatten_copy(copy))
            for k in mkeys.keys() - keys.keys():
                self.add("R07", f"{loc}: missing key '{k}'", market=loc)
            for k in keys.keys() - mkeys.keys():
                self.add("R07", f"{loc}: extra key '{k}' not in master", market=loc)
            for k, v in keys.items():
                if k not in mkeys:
                    continue
                if not v.strip():
                    self.add("R07", f"{loc}: '{k}' is empty", market=loc)
                limit = limits.get(k)
                if limit and len(v) > limit:
                    self.add("R07", f"{loc}: '{k}' is {len(v)} chars, slot fits {limit}: flag for layout, don't rewrite",
                             market=loc, severity="warn")
                elif loc != master_locale and len(v) > 1.4 * max(len(mkeys[k]), 10):
                    self.add("R07", f"{loc}: '{k}' is {len(v)} vs {len(mkeys[k])} chars in master: check it fits",
                             market=loc, severity="warn")
                if loc != master_locale and v == mkeys[k] and k not in keep and len(v) > 3:
                    self.add("R07", f"{loc}: '{k}' is identical to master (untranslated?)", market=loc, severity="warn")

    def copy_rules(self):
        """R05, R06, R08 and placeholders over every copy file."""
        offer = (self.row or {}).get("offer") or {}
        allowed_pct = {float(offer["discount_pct"])} if offer.get("discount_pct") else set()
        banned = self.cfg["brand"].get("banned_phrases") or {}
        for f in sorted((self.dir / "copy").glob("*.yaml")):
            loc = f.stem
            copy = load(f) or {}
            for k, v in flatten_copy(copy):
                for m in PERCENT.findall(v):
                    if float(m.replace(",", ".")) not in allowed_pct:
                        self.add("R05", f"{loc}:{k}: '{m}%' doesn't match the offer ({allowed_pct or 'no offer'})", market=loc)
                if PRICE.search(v):
                    self.add("R05", f"{loc}:{k}: looks like a typed price/currency: '{v}'. Prices come from facts", market=loc)
                low = v.lower()
                for phrase, why in banned.items():
                    if phrase in low:
                        self.add("R06", f"{loc}:{k}: banned phrase '{phrase}' ({why})", market=loc)
                if PLACEHOLDER.search(v):
                    self.add("R06", f"{loc}:{k}: unresolved placeholder in '{v}'", market=loc)
            subj, prev = copy.get("subject") or "", copy.get("preview") or ""
            if not 15 <= len(subj) <= 60:
                self.add("R08", f"{loc}: subject is {len(subj)} chars (15-60)", market=loc)
            if not 30 <= len(prev) <= 110:
                self.add("R08", f"{loc}: preview is {len(prev)} chars (30-110)", market=loc)

    def r13_generated_images(self):
        images = (load(self.dir / "images.yaml") or {}).get("images", {})
        for img_id, spec in images.items():
            if spec.get("source") != "generated":
                continue
            if not spec.get("reference_product"):
                self.add("R13", f"image '{img_id}' is generated but names no reference_product")
            qa = spec.get("qa") or {}
            if not qa.get("checked_against_real"):
                self.add("R13", f"image '{img_id}' not yet checked side by side against the real product",
                         severity="error" if self.final else "warn")

    # -- per-market rules on the rendered output -------------------------------
    def market_rules(self, m):
        market = self.cfg["markets"]["markets"][m]
        out = self.dir / "out"
        html = (out / f"{m}.html").read_text()
        meta = load(out / f"{m}.meta.json")
        brand = self.cfg["brand"]

        neutrals = {norm_hex(c) for c in brand["colors"]["neutrals"]}
        accents = {norm_hex(h) for h in HEX.findall(html)} - neutrals
        if len(accents) > brand.get("max_accents", 1):
            self.add("R01", f"{len(accents)} accent colours {sorted(accents)}", market=m)

        products = self.cfg["products"]
        named = 0
        for b in meta["buttons"]:
            if b.get("product"):
                short = (products.get(b["product"], {}).get("short_name") or {}).get(market["locale"], "")
                if short and short.lower() in b["label"].lower():
                    named += 1
                else:
                    self.add("R02", f"button '{b['label']}' links {b['product']} but doesn't say '{short}'", market=m)
        if len(meta["buttons"]) < 2 or named < 2:
            self.add("R02", f"{len(meta['buttons'])} buttons, {named} named after a product (need 2+)", market=m)

        ledger = {r["id"]: r for r in (load(DATA / "reviews.yaml") or {}).get("reviews", [])}
        for r in meta["reviews"]:
            src = ledger.get(r["id"])
            if not src or src["text"] != r["text"]:
                self.add("R04", f"review {r['id']} is not word for word from data/reviews.yaml", market=m)
            elif not src.get("source_url"):
                self.add("R04", f"review {r['id']} has no source_url logged", market=m)

        for img in meta["images"]:
            if not img.get("src") or not str(img["src"]).startswith("https://"):
                self.add("R09", f"image {img['id']} has no https source ({img.get('src')})", market=m)
            if not (img.get("alt") or "").strip():
                self.add("R09", f"image {img['id']} has no alt text", market=m)

        domain = f"https://{market['domain']}/"
        external = tuple(f"https://{d}/" for d in brand.get("allowed_external_domains") or [])
        for href in meta["links"]:
            if href.startswith(external):
                continue
            if not href.startswith(domain):
                self.add("R10", f"link to another domain: {href}", market=m)
            if f"utm_campaign={self.id}" not in href:
                self.add("R10", f"link without utm_campaign={self.id}: {href}", market=m)

        for p in meta["products"]:
            if not p["available"]:
                self.add("R14", f"{p['handles'][0]} is sold out in {m}", market=m)
            if p.get("compare_at") and (self.row.get("offer") or {}).get("discount_pct") \
                    and not self.row["offer"].get("apply_on_compare_at"):
                self.add("R15", f"{p['handles'][0]} is already reduced; offer not shown on top", market=m)
        age_h = (time.time() - meta["facts_fetched_at"]) / 3600
        if self.final and age_h > 24:
            self.add("R14", f"facts are {age_h:.0f}h old, run tools/facts.py {m}", market=m)

    def run(self):
        if self.row is None:
            self.add("R12", f"{self.id} is not on the calendar")
            return self.report()
        self.r12_why()
        self.r11_novelty()
        self.r03_one_product_per_row()
        self.r07_locales()
        self.copy_rules()
        self.r13_generated_images()
        try:
            render(self.id)
        except RenderError as e:
            self.findings.append({"rule": "RENDER", "severity": "error", "market": None, "msg": str(e)})
            return self.report()
        for m in campaign_markets(self.row, self.cfg):
            self.market_rules(m)
        return self.report()

    def report(self):
        errors = [f for f in self.findings if f["severity"] == "error"]
        result = {"campaign": self.id, "final": self.final, "at": int(time.time()),
                  "ok": not errors, "errors": len(errors),
                  "warnings": len(self.findings) - len(errors), "findings": self.findings}
        if self.dir.exists():
            (self.dir / "lint.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        return result


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    result = Linter(args[0], final="--final" in argv).run()
    for f in result["findings"]:
        where = f" [{f['market']}]" if f["market"] else ""
        print(f"{f['severity'].upper():5} {f['rule']}{where}: {f['msg']}")
    print(f"{'PASS' if result['ok'] else 'FAIL'}: {result['errors']} errors, {result['warnings']} warnings")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
