"""Pull live product and collection facts per market from the storefront.

    python3 tools/facts.py            # all active markets
    python3 tools/facts.py eu         # one market

Products (config/products.yaml): title, price, compare-at, stock, photos, url.
Collection groups (config/collections.yaml): cheapest in-stock price, for "from" tokens.
Copy never contains prices; the renderer reads them from data/facts/<market>.json.
"""
import json
import sys
import time
import urllib.request

from common import DATA, config


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "cavaier-email-os/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def money(cents):
    return None if cents in (None, 0) else f"{cents / 100:.2f}"


def https(u):
    return "https:" + u if u and u.startswith("//") else u


def product_facts(market, handle):
    # ?country= pins presentment pricing to the market instead of the caller's location.
    p = fetch(f"https://{market['domain']}/products/{handle}.js?country={market['country']}")
    return {
        "title": p["title"],
        "type": p.get("type"),
        "price": money(p["price"]),
        "compare_at": money(p.get("compare_at_price")),
        "available": p["available"],
        "images": [https(i) for i in p.get("images", [])],
        "url": f"https://{market['domain']}{market.get('path_prefix', '')}/products/{handle}",
    }


def collection_facts(market, spec):
    data = fetch(f"https://{market['domain']}/collections/{spec['collection']}/products.json"
                 f"?limit=250&country={market['country']}")
    types = spec.get("types")
    best = None
    count = 0
    for p in data.get("products", []):
        if types and p.get("product_type") not in types:
            continue
        count += 1
        for v in p["variants"]:
            if v.get("available") and (best is None or float(v["price"]) < best[0]):
                best = (float(v["price"]), p["handle"])
    return {"min_price": f"{best[0]:.2f}" if best else None, "min_handle": best[1] if best else None,
            "products": count, "path": spec["path"]}


def market_facts(market_id, market, cfg):
    out = {"market": market_id, "currency": market["currency"], "fetched_at": int(time.time()),
           "products": {}, "collections": {}}
    for handle in cfg["products"]:
        try:
            out["products"][handle] = product_facts(market, handle)
        except Exception as e:  # not sold here: recorded, the renderer refuses to feature it
            out["products"][handle] = {"missing": True, "error": str(e)}
    for name, spec in cfg["collections"].items():
        try:
            out["collections"][name] = collection_facts(market, spec)
        except Exception as e:
            out["collections"][name] = {"min_price": None, "error": str(e)}
    return out


def main(argv):
    cfg = config()
    markets = cfg["markets"]["markets"]
    for m in argv or [m for m, v in markets.items() if v.get("active")]:
        facts = market_facts(m, markets[m], cfg)
        (DATA / "facts" / f"{m}.json").write_text(json.dumps(facts, indent=2, ensure_ascii=False) + "\n")
        prods = ", ".join(f"{h}={v.get('price', 'MISSING')}" for h, v in facts["products"].items())
        cols = ", ".join(f"{n}≥{v.get('min_price')}" for n, v in facts["collections"].items())
        print(f"{m} ({markets[m]['currency']})\n  products: {prods}\n  from: {cols}")


if __name__ == "__main__":
    main(sys.argv[1:])
