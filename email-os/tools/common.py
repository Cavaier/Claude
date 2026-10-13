"""Shared paths, loaders and hashing for the email system."""
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config"
CALENDAR = ROOT / "calendar"
CAMPAIGNS = ROOT / "campaigns"
DATA = ROOT / "data"
LEDGER = ROOT / "approvals" / "ledger.jsonl"
GATES = ["calendar", "copy", "layout", "final"]


def load(path):
    path = Path(path)
    if not path.exists():
        return None
    text = path.read_text()
    return json.loads(text) if path.suffix == ".json" else yaml.safe_load(text)


def config():
    return {
        "brand": load(CONFIG / "brand.yaml"),
        "markets": load(CONFIG / "markets.yaml"),
        "products": load(CONFIG / "products.yaml"),
        "collections": load(CONFIG / "collections.yaml") or {},
        "rules": load(CONFIG / "rules.yaml"),
    }


def calendar_rows():
    """All calendar rows across months, keyed by campaign id."""
    rows = {}
    for f in sorted(CALENDAR.glob("*.yaml")):
        for row in (load(f) or {}).get("rows", []):
            row["_file"] = f.name
            rows[row["id"]] = row
    return rows


def campaign_markets(row, cfg):
    markets = cfg["markets"]["markets"]
    return [m for m in row.get("markets", []) if markets.get(m, {}).get("active")]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def canonical(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode()


def gate_hash(campaign_id, gate, cfg=None):
    """Fingerprint of exactly what a gate approves. None if there is nothing to approve yet.

    An approval is tied to this hash: if the content changes afterwards the approval
    goes stale and has to be given again.
    """
    cfg = cfg or config()
    d = CAMPAIGNS / campaign_id
    if gate == "calendar":
        row = calendar_rows().get(campaign_id)
        if row is None:
            return None
        return sha(canonical({k: v for k, v in row.items() if k != "_file"}))
    if gate == "copy":
        f = d / "copy" / f"{cfg['markets']['master_locale']}.yaml"
        return sha(f.read_bytes()) if f.exists() else None
    if gate == "layout":
        files = [d / "layout.yaml", d / "images.yaml"]
        if not files[0].exists():
            return None
        return sha(b"".join(f.read_bytes() for f in files if f.exists()))
    if gate == "final":
        # Everything a recipient gets: HTML, plain text, subject and preview, per market.
        # (Not the facts timestamp: refreshing identical prices doesn't unapprove anything.)
        outs = sorted((d / "out").glob("*.html"))
        if not outs:
            return None
        parts = []
        for f in outs:
            meta = load(f.with_suffix(".meta.json")) or {}
            txt = f.with_suffix(".txt")
            parts += [f.name.encode(), f.read_bytes(), txt.read_bytes() if txt.exists() else b"",
                      canonical([meta.get("subject"), meta.get("preview")])]
        return sha(b"".join(parts))
    raise ValueError(f"unknown gate {gate}")


def ledger_entries():
    if not LEDGER.exists():
        return []
    return [json.loads(line) for line in LEDGER.read_text().splitlines() if line.strip()]


def approval_state(campaign_id, gate, cfg=None):
    """'approved' | 'stale' | 'none', plus the latest ledger entry for this gate."""
    latest = None
    for e in ledger_entries():
        if e["campaign"] == campaign_id and e["gate"] == gate:
            latest = e
    if latest is None or latest["action"] != "approve":
        return "none", latest
    current = gate_hash(campaign_id, gate, cfg)
    return ("approved" if current == latest["hash"] else "stale"), latest
