"""Render a campaign into one HTML email per market.

    python3 tools/render.py <campaign-id>

Inputs (all inside campaigns/<id>/): layout.yaml (designer), images.yaml (image director),
copy/<locale>.yaml (copywriter / localizer). Prices and product links come from
data/facts/<market>.json, never from copy. Writes out/<market>.html and out/<market>.meta.json;
the linter checks the meta file and the HTML.
"""
import json
import sys
from decimal import ROUND_HALF_UP, Decimal
from urllib.parse import urlencode

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from common import CAMPAIGNS, DATA, ROOT, calendar_rows, campaign_markets, config, load


class RenderError(Exception):
    pass


def fmt_money(amount, market):
    s = f"{amount:.2f}"
    if market.get("decimal") == ",":
        s = s.replace(".", ",")
    return market["price_format"].format(amount=s)


def offer_price(price, offer):
    pct = Decimal(str(offer.get("discount_pct", 0)))
    return (Decimal(price) * (100 - pct) / 100).quantize(Decimal("0.01"), ROUND_HALF_UP)


def render_market(campaign_id, market_id, cfg, row):
    d = CAMPAIGNS / campaign_id
    market = cfg["markets"]["markets"][market_id]
    layout = load(d / "layout.yaml")
    images = (load(d / "images.yaml") or {}).get("images", {})
    copy = load(d / "copy" / f"{market['locale']}.yaml")
    facts = load(DATA / "facts" / f"{market_id}.json")
    if layout is None or copy is None:
        raise RenderError(f"{market_id}: missing layout.yaml or copy/{market['locale']}.yaml")
    if facts is None:
        raise RenderError(f"{market_id}: no facts, run tools/facts.py {market_id}")
    strings = copy.get("strings", {})
    offer = row.get("offer") or {}
    utm = urlencode({"utm_source": "klaviyo", "utm_medium": "email", "utm_campaign": campaign_id})
    base = f"https://{market['domain']}{market.get('path_prefix', '')}"
    meta = {"market": market_id, "locale": market["locale"], "subject": copy.get("subject"),
            "preview": copy.get("preview"), "buttons": [], "images": [], "products": [], "reviews": [],
            "strings_used": [], "facts_fetched_at": facts["fetched_at"]}

    def s(key):
        if key is None:
            return None
        meta["strings_used"].append(key)
        if key not in strings:
            raise RenderError(f"{market_id}: copy/{market['locale']}.yaml has no string '{key}'")
        return strings[key]

    def product_href(handle):
        return f"{base}/products/{handle}?{utm}"

    def link(spec):
        if "url" in spec:  # external (e.g. Trustpilot); the linter checks it against the allowlist
            return spec["url"]
        if "product" in spec:
            return product_href(spec["product"])
        return f"{base}{spec.get('path', '/')}?{utm}"

    def button(spec, product=None):
        product = spec.get("product", product)
        href = product_href(product) if product and not ({"path", "url"} & spec.keys()) else link(spec)
        btn = {"label": s(spec["label"]), "href": href, "product": product}
        meta["buttons"].append(btn)
        return btn

    def image(img_id, product=None):
        if img_id is None and product:
            f = facts["products"].get(product, {})
            img = {"id": f"facts:{product}", "src": f.get("image"), "alt_key": None,
                   "alt": f.get("title"), "source": "shopify"}
        else:
            spec = images.get(img_id)
            if spec is None:
                raise RenderError(f"image '{img_id}' is not in images.yaml")
            src = spec.get("src")
            if spec.get("source") == "shopify" and spec.get("product"):
                f = facts["products"].get(spec["product"], {})
                idx = spec.get("index", 0)
                src = (f.get("images") or [None])[idx] if idx < len(f.get("images") or []) else None
                src = src and src + ("&" if "?" in src else "?") + "width=1200"
            img = {"id": img_id, "src": src, "alt_key": spec.get("alt"), "alt": s(spec.get("alt")),
                   "source": spec.get("source")}
        meta["images"].append(img)
        return img

    reviews = {r["id"]: r for r in (load(DATA / "reviews.yaml") or {}).get("reviews", [])}
    blocks = []
    for raw in layout["blocks"]:
        b = {"type": raw["type"]}
        t = raw["type"]
        if t == "hero":
            b.update(label=s(raw.get("label")), headline=s(raw["headline"]), body=s(raw.get("body")),
                     image=image(raw["image"]), href=link(raw.get("link", {"path": "/"})))
            b["button"] = button(raw["button"]) if raw.get("button") else None
        elif t in ("text", "offer_card", "section_header"):
            for k in ("label", "title", "body", "note"):
                b[k] = s(raw.get(k))
        elif t == "product":
            handles = raw["product"] if isinstance(raw["product"], list) else [raw["product"]]
            handle = handles[0]
            f = facts["products"].get(handle) or {"missing": True}
            meta["products"].append({"handles": handles, "available": f.get("available", False),
                                     "missing": f.get("missing", False), "compare_at": f.get("compare_at")})
            if f.get("missing"):
                raise RenderError(f"{market_id}: product {handle} is not sold in this market")
            price = Decimal(f["price"])
            if offer.get("discount_pct") and (not f.get("compare_at") or offer.get("apply_on_compare_at")):
                b["was"], b["now"] = fmt_money(price, market), fmt_money(offer_price(price, offer), market)
            elif f.get("compare_at"):
                b["was"], b["now"] = fmt_money(Decimal(f["compare_at"]), market), fmt_money(price, market)
            else:
                b["was"], b["now"] = None, fmt_money(price, market)
            b.update(name=s(raw["name"]) if raw.get("name") else f["title"], body=s(raw.get("body")),
                     image=image(raw.get("image"), product=handle), href=product_href(handle))
            b["button"] = button(raw["button"], product=handle)
        elif t == "review":
            r = reviews.get(raw["review"])
            if r is None:
                raise RenderError(f"review '{raw['review']}' is not in data/reviews.yaml")
            meta["reviews"].append({"id": r["id"], "text": r["text"]})
            b.update(text=r["text"], author=r["author"], rating=r.get("rating", 5), platform=r.get("platform", ""))
        elif t == "button":
            b["button"] = button(raw["button"])
        elif t == "footer":
            b.update(text=s(raw["text"]), unsubscribe=s(raw["unsubscribe"]))
        blocks.append(b)

    env = Environment(loader=FileSystemLoader(ROOT / "templates"), undefined=StrictUndefined, autoescape=True)
    html = env.get_template("email.html.j2").render(
        brand=cfg["brand"], blocks=blocks, locale=market["locale"],
        subject=meta["subject"], preview=meta["preview"])
    meta["links"] = sorted({b["href"] for b in meta["buttons"]} | {b["href"] for b in blocks if b.get("href")})
    return html, meta


def render(campaign_id):
    cfg = config()
    row = calendar_rows().get(campaign_id)
    if row is None:
        raise RenderError(f"{campaign_id} is not on the calendar")
    out = CAMPAIGNS / campaign_id / "out"
    out.mkdir(exist_ok=True)
    markets = campaign_markets(row, cfg)
    for stale in out.glob("*"):
        if stale.stem.split(".")[0] not in markets:
            stale.unlink()
    for m in markets:
        html, meta = render_market(campaign_id, m, cfg, row)
        (out / f"{m}.html").write_text(html)
        (out / f"{m}.meta.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n")
        print(f"rendered {campaign_id}/out/{m}.html")


if __name__ == "__main__":
    try:
        render(sys.argv[1])
    except RenderError as e:
        sys.exit(f"render failed: {e}")
