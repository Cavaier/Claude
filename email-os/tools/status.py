"""Pipeline board: every calendar row, its stage, its gates and its lint result.

    python3 tools/status.py [month]      e.g. 2026-11
"""
import sys

from common import CAMPAIGNS, GATES, approval_state, calendar_rows, config, load

MARK = {"approved": "✓", "stale": "~", "none": "·"}


def stage(cid, cfg):
    d = CAMPAIGNS / cid
    master = cfg["markets"]["master_locale"]
    steps = [("brief", d / "brief.yaml"), ("copy", d / "copy" / f"{master}.yaml"), ("layout", d / "layout.yaml"),
             ("images", d / "images.yaml"), ("rendered", d / "out"), ("hosted", d / "images.lock.yaml"),
             ("built", d / "build.yaml")]
    done = [name for name, p in steps if p.exists()]
    if "built" in done:
        markets = (load(d / "build.yaml") or {}).get("markets") or {}
        ok = [m for m, b in markets.items() if b.get("verified")]
        return f"verified:{','.join(ok)}" if ok and len(ok) == len(markets) else "built (unverified)"
    return done[-1] if done else "planned"


def main(month=None):
    cfg = config()
    rows = sorted(calendar_rows().values(), key=lambda r: str(r["date"]))
    if month:
        rows = [r for r in rows if str(r["date"]).startswith(month)]
    print(f"{'date':10}  {'campaign':34} {'stage':18} " + " ".join(f"{g[:5]:5}" for g in GATES) + "  lint")
    for r in rows:
        cid = r["id"]
        gates = " ".join(f"{MARK[approval_state(cid, g, cfg)[0]]:5}" for g in GATES)
        lint = load(CAMPAIGNS / cid / "lint.json")
        lint_s = "–" if not lint else ("pass" if lint["ok"] else f"{lint['errors']} err") + \
            (f" {lint['warnings']} warn" if lint and lint["warnings"] else "")
        print(f"{str(r['date']):10}  {cid:34} {stage(cid, cfg):18} {gates}  {lint_s}"
              + ("  (built outside Email OS)" if r.get("managed") is False else ""))
    print("\n✓ approved   ~ changed since approval (approve again)   · not approved")


if __name__ == "__main__":
    main(*(sys.argv[1:2]))
