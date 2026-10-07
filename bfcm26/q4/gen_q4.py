#!/usr/bin/env python3
"""Cavaier Q4 2026 flows mock-up: python3 gen_q4.py -> cavaier-q4-flows.html

Specs live in q4_specs.py (flows, emails as module lists). This file renders them.
Text values: str | phase map {"pre": .., "bf cw": ..} | gender map {"W": .., "M": ..}.
Any module may carry "phases": [...] and/or "gender": "W"|"M".
Seeds the shared page once; after that the published artifact is the master.
"""
import base64, io, json, os, html as H
from PIL import Image, ImageOps
from q4_specs import FLOWS, PAGE

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'cavaier-q4-flows.html')

# ---------------------------------------------------------------- images
LF = ['m_3x_set', 'm_beach_arm', 'm_bw_fist', 'm_hand_hair', 'm_hand_rock', 'm_linen_chest', 'm_linen_chin', 'm_wrist_close',
      'w_3x_set', 'w_black_bracelet', 'w_black_top', 'w_chair', 'w_crossed', 'w_face_wet', 'w_wet_swim']
P = {
    'p_set_m': '3x-minimal-stack-set__0', 'p_set_m_silver': '3x-minimal-stack-set__2', 'p_set_w': '3x-minimal-stack-set-1__0',
    'p_set_w_gold': '3x-minimal-stack-set-1__1', 'p_duo': '2x-duo-minimal-set__0', 'p_stacked': 'stacked-set__0',
    'p_braid_black': 'braid-armband__0', 'p_braid_silver': 'braid-armband-1__7', 'p_crystal_br': 'bracelet__0',
    'p_crystal_neck': 'crystal-necklace__0', 'p_crystal_neck_silver': 'crystal-necklace__4', 'p_crystal_neck_worn': 'crystal-necklace__1',
    'p_cuban_neck': 'cuban-necklace-1__0', 'p_cuban_neck_worn': 'cuban-necklace-1__1', 'p_cube_pend': 'cube-necklace-1__0',
    'p_cube_pend_worn': 'cube-necklace__1', 'p_role_pend': 'role-necklace__0', 'p_role_pend_worn': 'role-necklace-1__2',
    'p_rope_br': 'rope-bracelet-2__1', 'p_rope_neck_worn': 'rope-necklace__3', 'p_cuff_black': 'minimal-cuff-1__0',
    'p_cuff_worn': 'minimal-cuff__3', 'p_case': 'jewelry-case__0', 'p_case_open': 'jewelry-case__1', 'p_giftcard': 'cavaier-gift-card__0',
    'p_cube_br_m': 'cube-bracelet__1', 'p_cube_br_w': 'cube-bracelet-1__1',
}
USED = set()

def enc(path, w, bw):
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    if bw: im = im.convert('L').convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=74, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def load_img(k):
    if k.startswith('lf_'):
        n = k[3:]; bwp = os.path.join(B, f'imgcache26bw/fig_{n}.jpg')
        return enc(bwp if os.path.exists(bwp) else os.path.join(B, f'figimg/{n}.png'), 1000, True)
    return enc(os.path.join(B, f'imgcache26/{P[k]}.jpg'), 640, False)

def img(k, alt='', style='', cls=''):
    if isinstance(k, dict):
        return f'<span class="gW">{img(k["W"], alt, style, cls)}</span><span class="gM">{img(k["M"], alt, style, cls)}</span>'
    if k != 'logo':
        assert k.startswith('lf_') and k[3:] in LF or k in P, f'unknown image {k}'
    USED.add(k)
    return f'<img data-k="{k}" alt="{H.escape(alt)}"' + (f' class="{cls}"' if cls else '') + (f' style="{style}"' if style else '') + '>'

# ---------------------------------------------------------------- phases / text
PH = ['pre', 'ea', 'bf', 'cw', 'xmas', 'late', 'post']
PC = {'pre': 'phP', 'ea': 'phE', 'bf': 'phB', 'cw': 'phC', 'xmas': 'phX', 'late': 'phL', 'post': 'phO'}
PNAME = {'pre': 'Pre-sale', 'ea': 'Early access', 'bf': 'Black Friday', 'cw': 'Cyber Week', 'xmas': 'Christmas', 'late': 'Last minute', 'post': 'After Christmas'}

def is_g(v): return isinstance(v, dict) and set(v) <= {'W', 'M'} and v
def is_p(v): return isinstance(v, dict) and not is_g(v)

def t(v, tag='span'):
    """Render a text value (str | phase map | gender map). Strings are trusted HTML-lite."""
    if v is None: return ''
    if isinstance(v, str): return v
    if is_g(v):
        return f'<{tag} class="gW">{t(v.get("W",""), tag)}</{tag}><{tag} class="gM">{t(v.get("M",""), tag)}</{tag}>'
    out = []
    for k, val in v.items():
        cls = ' '.join(PC[x] for x in k.split())
        out.append(f'<{tag} class="st {cls}">{t(val, tag)}</{tag}>')
    return ''.join(out)

def wrap(m, h):
    if m.get('gender'): h = f'<div class="g{m["gender"]}">{h}</div>'
    if m.get('phases'): h = f'<div class="st {" ".join(PC[p] for p in m["phases"])}">{h}</div>'
    return h

PROOF = '★★★★★ &nbsp;Rated 4.5 on Trustpilot · 3,000+ reviews'

# ---------------------------------------------------------------- modules
def m_headline(m):
    cls = 'm-head' + (' left' if m.get('align') == 'left' else '') + (' ' + m['size'] if m.get('size') in ('xl', 'm') else '')
    o = f'<div class="{cls}">'
    if m.get('kicker'): o += f'<span class="lab red">{t(m["kicker"])}</span>'
    o += f'<h2>{t(m["title"])}</h2>'
    if m.get('sub'): o += f'<p class="sub">{t(m["sub"])}</p>'
    if m.get('cta'): o += f'<a class="solid" href="#">{t(m["cta"])}</a>'
    return o + '</div>'

def m_big_type(m):
    o = '<div class="m-big">'
    if m.get('kicker'): o += f'<span class="lab red">{t(m["kicker"])}</span>'
    o += f'<p class="big">{t(m["big"])}</p>'
    if m.get('title'): o += f'<h3>{t(m["title"])}</h3>'
    if m.get('sub'): o += f'<p class="sub">{t(m["sub"])}</p>'
    return o + '</div>'

def m_hero_photo(m):
    shape = m.get('shape', 'inset')
    cls = 'm-photo' + ('' if shape == 'inset' else ' full ' + shape)
    o = f'<div class="{cls}">{img(m["img"], "")}'
    if m.get('caption'): o += f'<p class="cap">{t(m["caption"])}</p>'
    return o + '</div>'

def m_split(m):
    o = f'<div class="m-split{" rev" if m.get("reverse") else ""}">{img(m["img"], "")}<div class="t">'
    if m.get('kicker'): o += f'<span class="lab red">{t(m["kicker"])}</span>'
    o += f'<h4>{t(m["title"])}</h4><p>{t(m["body"])}</p>'
    if m.get('cta'): o += f'<a class="go" href="#">{t(m["cta"])} →</a>'
    return o + '</div></div>'

def m_cta(m):
    o = f'<div class="m-cta"><a class="solid" href="#">{t(m["label"])}</a>'
    if m.get('note'): o += f'<p class="small">{t(m["note"])}</p>'
    if m.get('proof'): o += f'<p class="mproof">{PROOF}</p>'
    return o + '</div>'

def m_text(m):
    cls = 'm-text' + (' left' if m.get('align') == 'left' else '') + (' ' + m['size'] if m.get('size') in ('s', 'l') else '')
    return f'<p class="{cls}">{t(m["body"])}</p>'

def m_promise(m): return f'<p class="m-promise">{t(m["text"])}</p>'

def m_timeline(m):
    o = '<div class="m-tl">'
    pts = m['points']
    for i, p in enumerate(pts):
        s = p.get('state', 'next')
        if i: o += '<i></i>'
        if i or s != 'now':
            o += f'<b class="{s}">●</b>'
        o += f'<span class="{s}">{t(p["label"])}</span>'
    return o + '</div>'

def m_ticket(m):
    cells = m['cells']
    o = f'<div class="m-ticket" style="grid-template-columns:repeat({len(cells)},1fr)">'
    for c in cells:
        rc = ' class="r"' if c.get('red') else ''
        o += f'<div><span class="lab">{t(c["label"])}</span><b{rc}>{t(c["value"])}</b>'
        if c.get('sub'): o += f'<span class="s">{t(c["sub"])}</span>'
        o += '</div>'
    return o + '</div>'

def m_offer_list(m):
    return (f'<div class="m-spec{" fr" if m.get("first_red", True) else ""}">'
            + ''.join(f'<div><span>{t(a)}</span><span>{t(b)}</span></div>' for a, b in m['rows']) + '</div>')

def m_offer_bar(m): return '<div class="m-bar offer">' + ''.join(f'<span>{t(x)}</span>' for x in m['items']) + '</div>'
def m_usp_bar(m): return '<div class="m-bar">' + ''.join(f'<span>{t(x)}</span>' for x in m['items']) + '</div>'

def m_section_header(m):
    return f'<div class="m-sh"><h3>{t(m["title"])}</h3>' + (f'<span class="lab">{t(m["label"])}</span>' if m.get('label') else '') + '</div>'

FIN = {'k': 'Black', 's': 'Silver', 'g': 'Gold'}
def pcard(it):
    o = f'<a class="pc" href="#">{img(it["img"], "")}<h4>{t(it["name"])}</h4>'
    if it.get('finish'):
        o += '<span class="fin">' + ''.join(f'<i class="{f}"></i>' for f in it['finish']) + f'<span>{" · ".join(FIN[f] for f in it["finish"])}</span></span>'
    if it.get('tag'): o += f'<span class="tag">{t(it["tag"])}</span>'
    return o + '</a>'

def m_product_grid(m):
    o = f'<div class="grid c{m.get("cols", 2)}">'
    for it in m['items']:
        c = pcard(it)
        o += f'<div class="g{it["gender"]}">{c}</div>' if it.get('gender') else c
    return o + '</div>'

def m_gift_guide(m):
    o = '<div class="tiles">'
    for tl in m['tiles']:
        o += (f'<a class="tile" href="#">{img(tl["img"], "")}<div><b>{t(tl["label"])}</b>'
              + (f'<span>{t(tl["sub"])}</span>' if tl.get('sub') else '<span>→</span>') + '</div></a>')
    return o + '</div>'

DYN = {
    'viewed': ({'W': 'p_set_w', 'M': 'p_set_m'}, {'W': '3x Minimal Set', 'M': '3x Minimal Set'}, None, '€94.90',
               'Dynamic · Viewed Product: name, image, price in the shopper’s currency'),
    'cart': ({'W': 'p_crystal_neck', 'M': 'p_braid_black'}, {'W': 'Crystal Necklace', 'M': 'Braid Bracelet'},
             {'W': 'Black / 55 cm', 'M': 'Black / Medium'}, {'W': '€89.90', 'M': '€39.90'},
             'Dynamic · Added to Cart: name, finish/size, image, price in the shopper’s currency'),
    'bis': ({'W': 'p_crystal_neck', 'M': 'p_set_m'}, {'W': 'Crystal Necklace', 'M': '3x Minimal Set'}, None, {'W': '€89.90', 'M': '€94.90'},
            'Dynamic · Back in Stock event: name, image, price in the shopper’s currency'),
}
def m_dynamic_product(m):
    im, nm, var, pr, note = DYN[m['source']]
    under = {'pre post': '', 'ea': '<span class="red">Members save 30%</span>', 'bf cw': '<span class="red">30% off at checkout</span>',
             'xmas': '<span class="red">Order by [cut-off] for Christmas</span>', 'late': '<span class="red">Or send a gift card</span>'}
    o = f'<div class="m-dyn{" side" if m.get("size") == "side" else ""}"><a href="#">{img(im, "")}</a><div class="dt"><h4>{t(nm)}</h4>'
    if var: o += f'<span class="small mute">{t(var)}</span>'
    o += f'<span class="dp">{t(pr)}</span>{t(under)}</div><p class="stand">{note}</p></div>'
    return o

FEED = {'W': [('p_crystal_br', 'Crystal Bracelet'), ('p_braid_silver', 'Braid Bracelet'), ('p_crystal_neck_silver', 'Crystal Necklace')],
        'M': [('p_braid_black', 'Braid Bracelet'), ('p_cuban_neck', 'Cuban Necklace'), ('p_cube_pend', 'Cube Pendant Necklace')]}
FEEDNOTE = {'recommended': 'Dynamic · Klaviyo product block, “Recommended for you” feed (catalog title + image, no price)',
            'viewed_together': 'Dynamic · Klaviyo product block, “Viewed together” feed for the product in the event',
            'bestsellers': 'Dynamic · Klaviyo product block, best-sellers feed (catalog title + image, no price)'}
def m_product_feed(m):
    tag = {'pre post': 'Best seller', 'ea': 'Members 30% off', 'bf cw': '30% off', 'xmas': 'Gift pick', 'late': 'Gift pick'}
    def side(g):
        return ''.join(f'<a class="pc" href="#">{img(k, n)}<h4>{n}</h4><span class="tag">{t(tag)}</span></a>' for k, n in FEED[g][:m.get('count', 3)])
    return (f'<div class="grid c3"><div class="gW">{side("W")}</div><div class="gM">{side("M")}</div></div>'
            f'<p class="m-note">{FEEDNOTE[m.get("source", "recommended")]}</p>')

def m_order_table(m):
    def row(k, name, var, pr):
        return (f'<div class="or">{img(k, name)}<div><h4>{name}</h4><span class="small mute">{var} · Qty 1</span></div>'
                f'<span class="op">{pr}</span></div>')
    case = row('p_case', 'Jewelry Case', 'Black', 'Included')
    w = row('p_crystal_neck', 'Crystal Necklace', 'Black / 55 cm', '€89.90') + row('p_braid_silver', 'Braid Bracelet', 'Silver / Medium', '€39.90') + case
    mm = row('p_set_m', '3x Minimal Set', 'Black / Medium', '€94.90') + row('p_braid_black', 'Braid Bracelet', 'Black / Medium', '€39.90') + case
    disc = {'bf cw': ('30% off + jewelry case', {'W': '−€58.84', 'M': '−€60.34'}, {'W': '€90.86', 'M': '€94.36'}),
            'pre ea xmas late post': ('Jewelry case (2+ pieces)', {'W': '−€19.90', 'M': '−€19.90'}, {'W': '€129.80', 'M': '€134.80'})}
    tot = ''
    for k, (lab, d, tt) in disc.items():
        cls = ' '.join(PC[x] for x in k.split())
        tot += (f'<div class="st {cls}"><div class="ot"><span>{lab}</span><span class="red">{t(d)}</span></div>'
                f'<div class="ot"><span>Shipping</span><span>{"Free" if k == "bf cw" else "[shipping offer to confirm]"}</span></div>'
                f'<div class="ot tt"><span>Total</span><b>{t(tt)}</b></div></div>')
    return (f'<div class="m-order{" c" if m.get("compact") else ""}"><div class="oh"><span>Your order</span><span class="lab">Saved</span></div>'
            f'<div class="gW">{w}</div><div class="gM">{mm}</div>{tot}'
            '<p class="stand">Dynamic · Checkout Started line items, discounts and total, in the shopper’s currency (sample cart in EUR)</p></div>')

def m_deadline(m): return f'<div class="m-dl"><span>{t(m["label"])}</span><b>{t(m["value"])}</b></div>'

def m_shipping_calendar(m):
    rows = m.get('rows') or [['Netherlands & EU', '[cut-off date]'], ['United Kingdom', '[cut-off date]'], ['US, Canada, Australia', '[cut-off date]'], ['Rest of world', '[cut-off date]']]
    return (f'<div class="m-cal"><div class="ch"><b>{t(m.get("title", "Order by, for Christmas"))}</b><span class="lab">Standard delivery</span></div>'
            + ''.join(f'<div class="cr"><span>{t(a)}</span><span>{t(b)}</span></div>' for a, b in rows) + '</div>')

def m_gift_box(m):
    return f'<div class="m-gift">{img(m.get("img", "p_case"), "")}<div><span class="lab red">{t(m["kicker"])}</span><h4>{t(m["title"])}</h4><p>{t(m["text"])}</p></div></div>'

def m_gift_card(m):
    return (f'<div class="m-gc"><div class="card">{img("logo", "Cavaier", "width:84px;height:14px", "logo")}<span class="amt">Gift card · any amount</span></div>'
            f'<h4>{t(m["title"])}</h4><p>{t(m["text"])}</p><a class="solid" href="#">{t(m["cta"])}</a></div>')

def m_steps(m): return '<div class="m-steps">' + ''.join(f'<div><b>0{i+1}</b><p>{t(x)}</p></div>' for i, x in enumerate(m['items'])) + '</div>'
def m_checklist(m): return '<div class="m-check">' + ''.join(f'<div><i>✓</i><span>{t(x)}</span></div>' for x in m['items']) + '</div>'

def m_quote(m):
    who = m.get('who') or 'Name · Trustpilot'
    q = f'<div class="m-quote"><span class="stars">★★★★★</span><p>[Verified Trustpilot review — to pull]</p><span class="who">{t(who)}</span></div>'
    return q * m.get('count', 1)

def m_score(m): return '<div class="m-score"><span class="stars">★★★★★</span><b>4.5</b><span class="lab">Trustpilot · 3,000+ reviews</span></div>'
def m_faq(m): return '<div class="m-faq">' + ''.join(f'<div><b>{t(q)}</b><p>{t(a)}</p></div>' for q, a in m['items']) + '</div>'
def m_note(m): return f'<p class="m-note">{t(m["text"])}</p>'
def m_spacer(m): return f'<div style="height:{m.get("h", 32)}px"></div>'

RENDER = {k[2:]: v for k, v in globals().items() if k.startswith('m_')}

def strip(banner):
    def one(s):
        if ' · ' in s:
            a, b = s.split(' · ', 1); return f'<span class="rs">{a}</span> · {b}'
        return f'<span class="rs">{s}</span>'
    if isinstance(banner, str): return f'<div class="strip">{one(banner)}</div>'
    return '<div class="strip">' + t({k: one(v) for k, v in banner.items()}) + '</div>'

def foot():
    return ('<footer class="foot"><div class="soc">'
            '<a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".9" fill="currentColor" stroke="none"/></svg></a>'
            '<a href="#" aria-label="TikTok"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M14 3v11.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 3c.4 2.6 2.2 4.4 5 4.7"/></svg></a>'
            '<a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M14.5 21v-8h2.7l.4-3.1h-3.1V8c0-.9.3-1.5 1.6-1.5h1.6V3.7a21 21 0 0 0-2.4-.1c-2.4 0-4 1.4-4 4.1v2.2H8.6V13h2.7v8"/></svg></a></div>'
            '<div class="fnav"><a class="fb on" href="#">Shop all</a><a class="fb" href="#">Men</a><a class="fb" href="#">Women</a><a class="fb" href="#">Men’s Sets</a><a class="fb" href="#">Women’s Sets</a></div>'
            f'<p class="fwm">{img("logo", "Cavaier", "width:64px;height:10.7px", "logo")}</p>'
            '<p class="copy2">© Copyright 2026 Cavaier</p><div class="legal"><span>Manage preferences</span><span>Unsubscribe</span></div></footer>')

def email_html(e):
    body = strip(e['banner']) + f'<div class="etop">{img("logo", "Cavaier", "width:84px;height:14px", "logo")}</div>'
    for m in e['modules']:
        body += wrap(m, RENDER[m['type']](m))
    return f'<article class="em{" fog" if e.get("bg") == "fog" else ""}" aria-label="{e["id"]}">{body}{foot()}</article>'

# ---------------------------------------------------------------- page
def phase_names(ps): return ' · '.join(PNAME[p] for p in ps)

def entry_html(f, e):
    meta = [('Email', f'<b>{e["id"]} · {e["name"]}</b>'), ('Send', e['delay']), ('Runs in', phase_names(e['phases'])),
            ('Subject', t(e['subject'])), ('Preview', t(e['preview'])), ('Job', e['goal']), ('Urgency', e.get('urgency', '')),
            ('Klaviyo', e['klaviyo'])]
    if e.get('notes'): meta.append(('Notes', e['notes']))
    dl = '<dl class="meta">' + ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in meta if b) + '</dl>'
    rail = (f'<div class="rail"><span class="no">{e["id"]}</span><p class="d">{e["name"]}</p><p class="tm2">{e["delay"]}</p>'
            f'<p class="heat">{phase_names(e["phases"])}</p><p class="showing" aria-live="polite"></p></div>')
    return (f'<section class="entry" id="{e["id"]}" data-states="{" ".join(e["phases"])}" data-s="{e["phases"][0]}">'
            f'{rail}<div class="mainc">{email_html(e)}</div><div class="side">{dl}</div></section>\n')

def flow_html(f):
    rows = [('Replaces', f['replaces']), ('Trigger', f['trigger']), ('Filters', f['filters']), ('Exits', f['exits']),
            ('Live', f['live']), ('Why', f['why'])]
    o = (f'<section class="flowhead" id="{f["id"]}"><span class="fid">{f["id"]}</span><div><span class="kicker">{len(f["emails"])} emails</span>'
         f'<h2>{f["name"]}</h2><dl>' + ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in rows) + '</dl></div></section>\n')
    for e in f['emails']:
        o += entry_html(f, e)
    return o

flows_html = ''.join(flow_html(f) for f in FLOWS)
n_emails = sum(len(f['emails']) for f in FLOWS)
map_rows = ''.join(
    f'<tr><td><a href="#{f["id"]}">{f["id"]}</a></td><td>{f["name"]}</td><td>{f["trigger_short"]}</td><td class="n">{len(f["emails"])}</td>'
    f'<td>{" → ".join(e["delay_short"] for e in f["emails"])}</td><td>{f["replaces"]}</td></tr>' for f in FLOWS)

IMGDATA = {k: load_img(k) for k in sorted(USED - {'logo'})}
IMGDATA['logo'] = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(HERE, 'logo0.png'), 'rb').read()).decode()

CSS = open(os.path.join(HERE, 'q4.css')).read() + '\n' + open(os.path.join(HERE, 'live_css.css')).read()
LIVE_JS = open(os.path.join(HERE, 'live_script.js')).read().replace("/^e\\d\\d$/.test(w)?'on '+w.slice(1)", "/^F\\dE\\d$/.test(w)?'on '+w")

phase_btns = ''.join(f'<button type="button" data-s="{p}" aria-pressed="{str(p == "bf").lower()}">{PNAME[p]}</button>' for p in PH)

page = f'''<title>Cavaier Q4 Flows</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400&family=Figtree:wght@200;300;400;500;600&display=swap">
<style>
{CSS}
</style>
<div class="live" id="live" role="region" aria-label="Live status">
  <div class="lv-in">
    <span class="dot" id="lvDot" aria-hidden="true"></span>
    <div class="who" id="lvWho"><span>Connecting…</span></div>
    <div class="cl" id="lvClaude" title="What Claude is doing on this page"></div>
    <button type="button" id="lvBtn" aria-expanded="false" aria-controls="lvPanel">Activity</button>
  </div>
</div>
<div class="lvpanel" id="lvPanel" hidden>
  <div class="in">
    <h3>Live on this page</h3>
    <p class="hint">Everyone who has this page open shows up in the bar above, with the email they’re looking at. Claude posts here when it starts and finishes a change, and says what changed where.</p>
    <form id="lvForm" autocomplete="off">
      <select id="lvKind" aria-label="Type"><option value="working">I’m working on</option><option value="waiting">Waiting for Claude</option><option value="note">Note</option></select>
      <input id="lvText" maxlength="200" placeholder="e.g. F4E2 product feed" aria-label="What">
      <button class="pb" type="submit">Post</button>
      <button class="pb ghost" type="button" id="lvClear">Clear my status</button>
    </form>
    <ol id="lvLog"><li><time></time><span class="hint">No activity yet.</span></li></ol>
  </div>
</div>
<div class="wrap" id="root" data-g="W">
{PAGE['intro'].format(n_flows=len(FLOWS), n_emails=n_emails)}
{PAGE['top']}
  <div class="tbl narrow"><table><thead><tr><th>Flow</th><th>Name</th><th>Trigger</th><th>Emails</th><th>Timing</th><th>Replaces</th></tr></thead><tbody>{map_rows}</tbody></table></div>
{PAGE['bottom']}
  <div class="bar2">
    <div class="ctl">
      <div class="seg" role="group" aria-label="Women or men"><button type="button" data-g="W" aria-pressed="true">W</button><button type="button" data-g="M" aria-pressed="false">M</button></div>
      <div class="seg" role="group" aria-label="Q4 phase">{phase_btns}</div>
    </div>
    <select class="jump" id="jump" aria-label="Jump to"><option value="">Jump to…</option></select>
  </div>
{flows_html}
</div>
<script type="application/json" id="imgs">{json.dumps(IMGDATA)}</script>
<script>
(function(){{
  var I=JSON.parse(document.getElementById('imgs').textContent);
  document.querySelectorAll('img[data-k]').forEach(function(im){{var s=I[im.getAttribute('data-k')];if(s)im.src=s}});
  var root=document.getElementById('root');
  var ORDER=['pre','ea','bf','cw','xmas','late','post'];
  var NAME={json.dumps(PNAME)};
  var g='W',s='bf';
  try{{g=localStorage.getItem('q4-g')||g;s=localStorage.getItem('q4-s')||s}}catch(e){{}}
  function eff(states,want){{
    if(states.indexOf(want)>=0)return want;
    var wi=ORDER.indexOf(want),best=states[0],bd=99;
    states.forEach(function(x){{var d=Math.abs(ORDER.indexOf(x)-wi);if(d<bd){{bd=d;best=x}}}});
    return best;
  }}
  function apply(){{
    root.setAttribute('data-g',g);
    document.querySelectorAll('.entry').forEach(function(e){{
      var states=e.getAttribute('data-states').split(' '),x=eff(states,s);e.setAttribute('data-s',x);
      e.querySelector('.showing').textContent='Showing: '+NAME[x]+(x!==s?' (doesn’t send in '+NAME[s]+')':'');
    }});
    document.querySelectorAll('button[data-g]').forEach(function(b){{b.setAttribute('aria-pressed',String(b.getAttribute('data-g')===g))}});
    document.querySelectorAll('button[data-s]').forEach(function(b){{b.setAttribute('aria-pressed',String(b.getAttribute('data-s')===s))}});
    try{{localStorage.setItem('q4-g',g);localStorage.setItem('q4-s',s)}}catch(e){{}}
  }}
  document.querySelectorAll('button[data-g]').forEach(function(b){{b.addEventListener('click',function(){{g=b.getAttribute('data-g');apply()}})}});
  document.querySelectorAll('button[data-s]').forEach(function(b){{b.addEventListener('click',function(){{s=b.getAttribute('data-s');apply()}})}});
  var j=document.getElementById('jump');
  document.querySelectorAll('.flowhead,.entry').forEach(function(e){{var o=document.createElement('option');o.value=e.id;
    o.textContent=e.classList.contains('flowhead')?e.id+' · '+e.querySelector('h2').textContent:'   '+e.id+' · '+e.querySelector('.d').textContent;j.appendChild(o)}});
  j.addEventListener('change',function(){{if(j.value){{document.getElementById(j.value).scrollIntoView();j.value=''}}}});
  window.q4View=function(G,S){{g=G;s=S;apply()}};
  apply();
}})();
</script>
<script>{LIVE_JS}</script>
'''
open(OUT, 'w').write(page)
print('wrote', OUT, len(page) // 1024, 'KB ·', len(FLOWS), 'flows ·', n_emails, 'emails ·', len(IMGDATA), 'images')
