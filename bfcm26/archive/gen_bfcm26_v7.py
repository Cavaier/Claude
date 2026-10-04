#!/usr/bin/env python3
"""v7: conversion audit pass on top of v6 (same look, more revenue)."""
import base64, os, re, concurrent.futures as cf
import gen_bfcm26 as g
import gen_bfcm26_v3 as v3
import gen_bfcm26_v6 as v6
from gen_bfcm26 import img, price_html

CASE_VAL = 'Case (€19.95 value) with any Set or 2 pieces'
XMAS = '<p class="xmas"><span class="rs">Christmas delivery</span> · order by [CEO to confirm date] to have it under the tree</p>'
TAG = v6.TAG

def common(h):
    h = h.replace('<span>Case with any Set or 2 pieces</span>', f'<span>{CASE_VAL}</span>')
    h = h.replace('<div><span>Any Set or two pieces</span><span>Jewelry case included</span></div>',
                  '<div><span>Any Set or two pieces</span><span>Jewelry case included (€19.95 value)</span></div>')
    return h

def add_ship_row(h):
    if '<span>Shipping</span>' in h:
        return h
    return re.sub(r'(<div class="spec">(?:<div><span>[^<]*</span><span>[^<]*</span></div>)+)', r'\1<div><span>Shipping</span><span>Free on every order</span></div>', h, count=1)

def e01():
    h = common(v6.e01())
    # best-sellers straight after the quote, the letter and offer details after them
    m = re.search(r'<div class="sec"></div><div class="cttl c"><h2 class="sm">Where to start.*?<div class="mcta">.*?</div>', h, re.S)
    block = m.group(0); h = h.replace(block, '', 1)
    h = h.replace('<p class="letter">', block + '<p class="letter">', 1)
    h = h.replace('<h2 class="sm">Where to start</h2>', '<h2 class="sm">Where to start</h2>', 1)
    h = h.replace('<span class="pn">3x Minimal Set · Men</span>', f'<span class="pn">3x Minimal Set · Men</span>', 1)
    h = add_ship_row(h)
    h = h.replace('<p class="small mute center">Early access ends', '<div class="mcta tight" style="padding-top:30px"><a class="solid" href="#">Shop early access</a></div><p class="small mute center">Early access ends', 1)
    return h

def e02():
    return common(v6.e02())

def e03():
    h = common(v6.e03())
    h = h.replace('<a class="gbtn" href="#">Shop now</a>', '<a class="gbtn" href="#">3x Minimal Set · €66.47</a>', 1)
    return h

def e04():
    return common(v6.e04())

def e05():
    return common(v6.e05())

def e06():
    return common(v6.e06())

def e08():
    h = common(v6.e08())
    best = ('<div class="sec">' + g.msh('Best-sellers', 'Almost sold out') +
            '<div class="grid g2">'
            f'<a class="mcard" href="#"><img src="{img("fig_m_3x_set")}" alt="3x Minimal Set, men"><h4>3x Minimal Set · Men</h4>{price_html("set3")}</a>'
            f'<a class="mcard" href="#"><img src="{img("fig_w_3x_set")}" alt="3x Minimal Set, women"><h4>3x Minimal Set · Women</h4>{price_html("set3")}</a>'
            '</div></div>')
    h = h.replace('<div class="sec"><div class="msh"><h3>Shop by category</h3>', best + '<div class="sec"><div class="msh"><h3>Shop by category</h3>', 1)
    h = re.sub(r'(<div class="dl">.*?</p>)', r'\1' + XMAS, h, count=1, flags=re.S)
    return h

def e10():
    h = common(v6.e10())
    return h.replace('<div class="duo2"', XMAS + '<div class="duo2"', 1)

def e12():
    h = common(v6.e12())
    return h.replace('<div class="mcta"><a class="solid" href="#">Shop before Sunday</a>', XMAS + '<div class="mcta"><a class="solid" href="#">Shop before Sunday</a>', 1)

def e13():
    return add_ship_row(common(v6.e13()))

FN = {'01': e01, '02': e02, '03': e03, '04': e04, '05': e05, '06': e06, '08': e08, '10': e10, '12': e12, '13': e13}
for s in g.SENDS:
    if s['n'] in FN:
        s['fn'] = FN[s['n']]

V7_CSS = """
/* ---- v7: conversion audit ---- */
.xmas{margin:14px 24px 0;text-align:center;font:400 11px/1.5 var(--body);letter-spacing:.06em;color:var(--ink2)}
.xmas .rs{color:var(--red);font-weight:600;letter-spacing:.14em;text-transform:uppercase;font-size:10px}
.gbtn{white-space:nowrap}
@media (max-width:480px){
  .em .solid{display:block;width:100%;text-align:center}
  .hero .hbtn{min-width:0;width:100%}
}
"""

if __name__ == '__main__':
    tp = os.path.join(g.HERE, 'bfcm26.tpl.html')
    tpl = open(tp).read()
    if '/* ---- v7:' not in tpl:
        tpl = tpl.replace('</style>', V7_CSS + '</style>', 1)
    open(tp, 'w').write(tpl)
    html = v3.build()
    with cf.ThreadPoolExecutor(10) as ex:
        data = dict(ex.map(v6.fetch, sorted(g.USED)))
    uri = {k: 'data:image/jpeg;base64,' + base64.b64encode(v).decode() for k, v in data.items()}
    html = v6.red_strip(html)
    html = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: uri[m.group(1)], html)
    assert 'warrant' not in html.lower()
    open(os.path.join(g.HERE, 'cavaier-bfcm26-sequence.html'), 'w').write(html)
    print(len(g.USED), 'images,', len(html) // 1024, 'KB')
