"""Pull live product facts (title, price, stock, image, url) per market from the storefront.

    python3 tools/facts.py            # all active markets, all products in config/products.yaml
    python3 tools/facts.py eu         # one market

Copy never contains prices. The renderer reads them from data/facts/<market>.json, so every
market shows its own live price in its own currency.
"""
import json
import sys
import time
import urllib.request

from common import DATA, config


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "cavaier-email-os/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def money(cents):
    return None if cents in (None, 0) else f"{cents / 100:.2f}"


def market_facts(market_id, market, products):
    out = {"market": market_id, "currency": market["currency"], "fetched_at": int(time.time()), "products": {}}
    base = f"https://{market['domain']}{market.get('path_prefix', '')}"
    for handle in products:
        # ?country= pins presentment pricing to the market instead of the caller's location.
        url = f"https://{market['domain']}/products/{handle}.js?country={market['country']}"
        try:
            p = fetch(url)
        except Exception as e:  # missing in this store: recorded, and the linter refuses to feature it
            out["products"][handle] = {"missing": True, "error": str(e)}
            continue
        img = p.get("featured_image") or ""
        out["products"][handle] = {
            "title": p["title"],
            "price": money(p["price"]),
            "compare_at": money(p.get("compare_at_price")),
            "available": p["available"],
            "image": ("https:" + img if img.startswith("//") else img) + ("&" if "?" in img else "?") + "width=1200",
            "images": ["https:" + i if i.startswith("//") else i for i in p.get("images", [])],
            "url": f"{base}/products/{handle}",
        }
    return out


def main(argv):
    cfg = config()
    markets = cfg["markets"]["markets"]
    wanted = argv or [m for m, v in markets.items() if v.get("active")]
    for m in wanted:
        facts = market_facts(m, markets[m], cfg["products"])
        path = DATA / "facts" / f"{m}.json"
        path.write_text(json.dumps(facts, indent=2, ensure_ascii=False) + "\n")
        summary = ", ".join(f"{h}={v.get('price', 'MISSING')}" for h, v in facts["products"].items())
        print(f"{m} ({markets[m]['currency']}): {summary}")


if __name__ == "__main__":
    main(sys.argv[1:])
