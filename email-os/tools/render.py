"""Render a campaign into one HTML email (plus a plain-text version) per market.

    python3 tools/render.py <campaign-id>

Inputs (all inside campaigns/<id>/): layout.yaml (designer), images.yaml (image director),
copy/<locale>.yaml (copywriter / localizer). Prices, links and photos come from
data/facts/<market>.json, never from copy: copy uses tokens such as {offer_price:<handle>},
{from_offer_price:<collection group>}, {money:25} and {code}. Optimised, hosted images come
from images.lock.yaml (tools/images.py). Writes out/<market>.html, .txt and .meta.json.
"""
import html as htmllib
import json
import re
import sys
from decimal import ROUND_HALF_UP, Decimal
from urllib.parse import urlencode

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup

from common import CAMPAIGNS, DATA, ROOT, calendar_rows, campaign_markets, config, load

TOKEN = re.compile(r"\{(\w+)(?::([^{}]+))?\}")
# Display width of each image slot; images.py makes 2x JPEGs from these.
SLOT_WIDTH = {"hero": 600, "image": 600, "product": 240, "tile": 176, "tile2": 268}


class RenderError(Exception):
    pass


def fmt_money(amount, market):
    amount = Decimal(str(amount))
    s = f"{amount:.2f}"
    if s.endswith(".00") and market.get("drop_zero_cents", True):
        s = s[:-3]
    if market.get("decimal") == ",":
        s = s.replace(".", ",")
    return market["price_format"].format(amount=s)


def offer_price(price, offer):
    pct = Decimal(str(offer.get("discount_pct", 0)))
    return (Decimal(str(price)) * (100 - pct) / 100).quantize(Decimal("0.01"), ROUND_HALF_UP)


def minify(html):
    html = re.sub(r">\s+<", "><", html)
    return re.sub(r"[ \t]*\n[ \t]*", "\n", html).strip() + "\n"


class Market:
    def __init__(self, campaign_id, market_id, cfg, row):
        self.id, self.cfg, self.row = market_id, cfg, row
        self.m = cfg["markets"]["markets"][market_id]
        self.campaign_id = campaign_id
        self.dir = CAMPAIGNS / campaign_id
        self.offer = row.get("offer") or {}
        self.facts = load(DATA / "facts" / f"{market_id}.json")
        if self.facts is None:
            raise RenderError(f"{market_id}: no facts, run tools/facts.py {market_id}")
        self.copy = load(self.dir / "copy" / f"{self.m['locale']}.yaml")
        if self.copy is None:
            raise RenderError(f"{market_id}: missing copy/{self.m['locale']}.yaml")
        self.images = (load(self.dir / "images.yaml") or {}).get("images", {})
        self.lock = (load(self.dir / "images.lock.yaml") or {}).get("images", {})
        self.base = f"https://{self.m['domain']}{self.m.get('path_prefix', '')}"
        self.utm = urlencode({"utm_source": "klaviyo", "utm_medium": "email", "utm_campaign": campaign_id})
        self.meta = {"market": market_id, "locale": self.m["locale"], "buttons": [], "images": [],
                     "products": [], "reviews": [], "strings_used": [], "tokens": [],
                     "facts_fetched_at": self.facts["fetched_at"]}

    # -- money and tokens -----------------------------------------------------
    def product(self, handle):
        f = self.facts["products"].get(handle)
        if not f or f.get("missing"):
            raise RenderError(f"{self.id}: product {handle} is not in facts or not sold here "
                              "(add it to config/products.yaml and run tools/facts.py)")
        return f

    def group(self, name):
        g = (self.facts.get("collections") or {}).get(name)
        if not g or g.get("min_price") is None:
            raise RenderError(f"{self.id}: collection group '{name}' has no live price "
                              "(config/collections.yaml + tools/facts.py)")
        return g

    def token(self, match):
        name, arg = match.group(1), match.group(2)
        self.meta["tokens"].append(match.group(0))
        if name == "offer_price":
            f = self.product(arg)
            return fmt_money(offer_price(f["price"], self.offer), self.m)
        if name == "price":
            return fmt_money(self.product(arg)["price"], self.m)
        if name == "from_offer_price":
            return fmt_money(offer_price(self.group(arg)["min_price"], self.offer), self.m)
        if name == "from_price":
            return fmt_money(self.group(arg)["min_price"], self.m)
        if name == "money":
            return fmt_money(arg, self.m)
        if name == "code":
            if not self.offer.get("code"):
                raise RenderError("{code} used but the calendar offer has no code")
            return self.offer["code"]
        if name == "pct":
            return f"{self.offer['discount_pct']}%"
        raise RenderError(f"unknown token {match.group(0)}")

    def fill(self, text):
        return TOKEN.sub(self.token, text) if text else text

    def s(self, key):
        if key is None:
            return None
        self.meta["strings_used"].append(key)
        strings = self.copy.get("strings", {})
        if key not in strings:
            raise RenderError(f"{self.id}: copy/{self.m['locale']}.yaml has no string '{key}'")
        return self.fill(strings[key])

    def lines(self, key):
        """A string whose newlines become <br> (escaped first)."""
        v = self.s(key)
        return None if v is None else Markup("<br>".join(htmllib.escape(x) for x in v.split("\n")))

    # -- links, buttons, images ---------------------------------------------
    def product_href(self, handle):
        return f"{self.base}/products/{handle}?{self.utm}"

    def link(self, spec):
        spec = spec or {"path": "/"}
        if "url" in spec:
            return spec["url"]
        if "product" in spec:
            return self.product_href(spec["product"])
        if "collection" in spec:
            path = self.cfg["collections"][spec["collection"]]["path"]
            return f"{self.base}{path}?{self.utm}"
        if "path" in spec:
            path = spec["path"]
            sep = "&" if "?" in path else "?"
            return f"{self.base}{path}{sep}{self.utm}"
        raise RenderError(f"link needs url, product, collection or path: {spec}")

    def button(self, spec, product=None, style="solid"):
        product = spec.get("product", product)
        href = self.link(spec) if {"path", "url", "collection"} & spec.keys() else \
            (self.product_href(product) if product else self.link(spec))
        btn = {"label": self.s(spec["label"]), "href": href, "product": product,
               "style": spec.get("style", style)}
        self.meta["buttons"].append(btn)
        return btn

    def image(self, img_id, product=None, slot="image"):
        if img_id is None and product:
            img_id = f"product:{product}"
            spec = {"source": "shopify", "product": product, "index": 0}
        else:
            spec = self.images.get(img_id)
            if spec is None:
                raise RenderError(f"image '{img_id}' is not in images.yaml")
        src = self.source_url(spec)
        hosted = (self.lock.get(img_id) or {})
        alt = self.s(spec["alt"]) if spec.get("alt") else (self.product(product)["title"] if product else None)
        img = {"id": img_id, "src": hosted.get("url") or src, "source_url": src, "alt": alt,
               "hosted": bool(hosted.get("url")) and hosted.get("source_url") == src,
               "bytes": hosted.get("bytes"), "source": spec.get("source"),
               "width": SLOT_WIDTH.get(slot, 600)}
        if hosted.get("url") and hosted.get("source_url") != src:
            img["src"], img["hosted"] = src, False  # source changed since it was optimised
        self.meta["images"].append(img)
        return img

    def source_url(self, spec):
        if spec.get("source") == "shopify":
            f = self.product(spec["product"])
            imgs = f.get("images") or []
            idx = spec.get("index", 0)
            if idx >= len(imgs):
                raise RenderError(f"{spec['product']} has no image #{idx} in {self.id}")
            return imgs[idx]
        return spec.get("src")

    # -- blocks ---------------------------------------------------------------
    def block(self, raw):
        t = raw["type"]
        b = {"type": t, "align": raw.get("align", "left"), "bg": raw.get("bg")}
        if t == "hero":
            b.update(label=self.s(raw.get("label")), headline=self.lines(raw["headline"]),
                     body=self.s(raw.get("body")), image=self.image(raw["image"], slot="hero"),
                     href=self.link(raw.get("link")))
            b["button"] = self.button(raw["button"]) if raw.get("button") else None
        elif t == "image":
            b.update(image=self.image(raw["image"], slot="image"), href=self.link(raw.get("link")))
        elif t in ("text", "offer_card", "section_header", "strip", "note", "heading"):
            for k in ("label", "title", "body", "note", "text"):
                b[k] = self.lines(raw.get(k)) if k in ("title", "body", "text") else self.s(raw.get(k))
            if raw.get("button"):
                b["button"] = self.button(raw["button"], style=raw["button"].get("style", "solid"))
        elif t == "ticket":
            b["cells"] = [{"label": self.s(c["label"]), "value": self.s(c["value"]),
                           "note": self.s(c.get("note")), "accent": c.get("accent", False)}
                          for c in raw["cells"]]
        elif t == "timeline":
            b.update(left=self.s(raw["left"]), right=self.s(raw["right"]))
        elif t == "tiles":
            b["tiles"] = []
            for tile in raw["tiles"]:
                b["tiles"].append({"image": self.image(tile.get("image"), product=tile.get("product"),
                                                       slot="tile" if len(raw["tiles"]) > 2 else "tile2"),
                                   "label": self.s(tile["label"]), "sub": self.s(tile.get("sub")),
                                   "href": self.link(tile["link"])})
                self.meta["buttons"].append({"label": b["tiles"][-1]["label"], "href": b["tiles"][-1]["href"],
                                             "product": tile["link"].get("product"), "style": "tile"})
        elif t == "product":
            handles = raw["product"] if isinstance(raw["product"], list) else [raw["product"]]
            handle = handles[0]
            f = self.product(handle)
            self.meta["products"].append({"handles": handles, "available": f.get("available", False),
                                          "compare_at": f.get("compare_at")})
            price = Decimal(f["price"])
            if self.offer.get("discount_pct") and (not f.get("compare_at") or self.offer.get("apply_on_compare_at")):
                b["was"], b["now"] = fmt_money(price, self.m), fmt_money(offer_price(price, self.offer), self.m)
            elif f.get("compare_at"):
                b["was"], b["now"] = fmt_money(f["compare_at"], self.m), fmt_money(price, self.m)
            else:
                b["was"], b["now"] = None, fmt_money(price, self.m)
            b.update(name=self.s(raw["name"]) if raw.get("name") else f["title"], body=self.s(raw.get("body")),
                     image=self.image(raw.get("image"), product=handle, slot="product"),
                     href=self.product_href(handle))
            b["button"] = self.button(raw["button"], product=handle)
        elif t == "review":
            reviews = {r["id"]: r for r in (load(DATA / "reviews.yaml") or {}).get("reviews", [])}
            r = reviews.get(raw["review"])
            if r is None:
                raise RenderError(f"review '{raw['review']}' is not in data/reviews.yaml")
            self.meta["reviews"].append({"id": r["id"], "text": r["text"]})
            b.update(text=r["text"], author=r["author"], rating=r.get("rating", 5), platform=r.get("platform", ""))
        elif t == "button":
            b["button"] = self.button(raw["button"], style=raw["button"].get("style", "solid"))
        elif t == "para":
            b["text"] = self.lines(raw["text"])
        elif t == "link":
            b["button"] = self.button(raw["button"], style="link")
        elif t == "footer":
            b.update(links=[self.button(l, style="footer") for l in raw.get("links", [])],
                     text=self.s(raw.get("text")), unsubscribe=self.s(raw["unsubscribe"]),
                     preferences=self.s(raw.get("preferences")))
        elif t in ("logo", "trust", "divider", "spacer"):
            b["size"] = raw.get("size", 24)
        else:
            raise RenderError(f"unknown block type '{t}'")
        for k in ("button", "label", "title", "body", "note", "text", "href"):
            b.setdefault(k, None)
        return b

    def render(self, layout):
        self.meta["subject"] = self.fill(self.copy.get("subject"))
        self.meta["preview"] = self.fill(self.copy.get("preview"))
        blocks = [self.block(raw) for raw in layout["blocks"]]
        style = layout.get("style", "designed")
        env = Environment(loader=FileSystemLoader(ROOT / "templates"), undefined=StrictUndefined, autoescape=True)
        tpl = "plain.html.j2" if style == "plain" else "email.html.j2"
        html = minify(env.get_template(tpl).render(
            brand=self.cfg["brand"], blocks=blocks, locale=self.m["locale"],
            subject=self.meta["subject"], preview=self.meta["preview"]))
        hrefs = {b["href"] for b in self.meta["buttons"]} | {b["href"] for b in blocks if b.get("href")}
        self.meta["links"] = sorted(hrefs)
        self.meta["html_bytes"] = len(html.encode())
        return html, plain_text(blocks, self.meta)


def plain_text(blocks, meta):
    """The text/plain part: same words and links, no layout."""
    out = []

    def add(x):
        if x:
            out.append(re.sub(r"<br>", "\n", str(x)))
    for b in blocks:
        for k in ("strip", "label", "headline", "title", "text", "body", "note"):
            add(b.get(k))
        for c in b.get("cells") or []:
            add(" ".join(x for x in (c["label"], c["value"], c["note"]) if x))
        if b.get("left"):
            add(f"{b['left']} → {b['right']}")
        for tile in b.get("tiles") or []:
            add(f"{tile['label']} {tile['sub'] or ''}: {tile['href']}")
        if b.get("name"):
            add(f"{b['name']}  {b['now']}" + (f" (was {b['was']})" if b.get("was") else ""))
        if b.get("button"):
            add(f"{b['button']['label']}: {b['button']['href']}")
    text = "\n\n".join(htmllib.unescape(x) for x in out)
    return text + "\n\n{% unsubscribe_url %}\n"


def render(campaign_id):
    cfg = config()
    row = calendar_rows().get(campaign_id)
    if row is None:
        raise RenderError(f"{campaign_id} is not on the calendar")
    layout = load(CAMPAIGNS / campaign_id / "layout.yaml")
    if layout is None:
        raise RenderError(f"{campaign_id}: no layout.yaml")
    out = CAMPAIGNS / campaign_id / "out"
    out.mkdir(exist_ok=True)
    markets = campaign_markets(row, cfg)
    for stale in out.glob("*"):
        if stale.name.split(".")[0] not in markets:
            stale.unlink()
    for m in markets:
        html, text = (mk := Market(campaign_id, m, cfg, row)).render(layout)
        (out / f"{m}.html").write_text(html)
        (out / f"{m}.txt").write_text(text)
        (out / f"{m}.meta.json").write_text(json.dumps(mk.meta, indent=2, ensure_ascii=False) + "\n")
        print(f"rendered {campaign_id}/out/{m}.html ({mk.meta['html_bytes'] // 1024} KB)")


if __name__ == "__main__":
    try:
        render(sys.argv[1])
    except RenderError as e:
        sys.exit(f"render failed: {e}")
