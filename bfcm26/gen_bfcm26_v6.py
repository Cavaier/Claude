#!/usr/bin/env python3
"""v6: real photography from the Cavaier Figma (Static Ads 1 + 2), 3x Minimal Sets as the lead,
'almost sold out' scarcity, free shipping in the offer."""
import base64, io, os, re, concurrent.futures as cf
from PIL import Image, ImageOps
import gen_bfcm26 as g
import gen_bfcm26_v3 as v3
import gen_bfcm26_v4 as v4
import gen_bfcm26_v5 as v5
from gen_bfcm26 import img, strip, eur, sale, foot
from gen_bfcm26_v3 import logobar, capttl, casecard

FIG = os.path.join(g.HERE, 'figimg')
PACKSHOTS = {'crystal-necklace__0', 'crystal-necklace__4', 'minimal-cuff__0', 'minimal-cuff__2', 'minimal-cuff-1__0',
             'minimal-cuff-1__2', 'braid-armband__0', 'braid-armband-1__0', 'braid-armband-1__7', 'jewelry-case__0',
             'jewelry-case__1', 'cavaier-gift-card__0', '2x-duo-minimal-set__1', '2x-duo-minimal-set__2', 'stacked-set__1', 'stacked-set__2'}

def fimg(name):
    return img('fig_' + name)

COLOUR_FIG = {'fig_m_3x_set', 'fig_w_3x_set'}   # first image of the 3x Minimal Set products

def fetch(key):
    if key in COLOUR_FIG:
        path = os.path.join(g.HERE, 'imgcache26bw', key + '_c.jpg')
        if not os.path.exists(path):
            im = Image.open(os.path.join(FIG, key[4:] + '.png')).convert('RGB')
            im.thumbnail((700, 1000))
            b = io.BytesIO(); im.save(b, 'JPEG', quality=72, optimize=True, progressive=True)
            open(path, 'wb').write(b.getvalue())
        return key, open(path, 'rb').read()
    if key.startswith('fighk_'):
        path = os.path.join(g.HERE, 'imgcache26bw', key + '.jpg')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            im = Image.open(os.path.join(FIG, key[6:] + '.png')).convert('L')
            im = ImageOps.autocontrast(im, cutoff=0.5)
            im = im.point(lambda v: int(96 + v * 0.62)).convert('RGB')   # high-key, like the reference board
            im.thumbnail((700, 1000))
            b = io.BytesIO(); im.save(b, 'JPEG', quality=72, optimize=True, progressive=True)
            open(path, 'wb').write(b.getvalue())
        return key, open(path, 'rb').read()
    if key.startswith('fig_'):
        path = os.path.join(g.HERE, 'imgcache26bw', key + '.jpg')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            im = Image.open(os.path.join(FIG, key[4:] + '.png')).convert('L')
            im = ImageOps.autocontrast(im, cutoff=0.5).convert('RGB')
            im.thumbnail((700, 1000))
            b = io.BytesIO(); im.save(b, 'JPEG', quality=70, optimize=True, progressive=True)
            open(path, 'wb').write(b.getvalue())
        return key, open(path, 'rb').read()
    if key in PACKSHOTS or key.endswith('__0'):   # product-only shots + first product image
        return g.fetch(key)      # product-only shots stay in colour
    return v3.fetch_bw(key)      # worn / lifestyle shots in black and white

def swap_ph(html, label_part, src, pos=None):
    """Replace the first placeholder whose label contains label_part with a real image."""
    pat = re.compile(r'<div class="ph ([^"]*)"( style="[^"]*")?><span>([^<]*)</span></div>')
    for m in pat.finditer(html):
        if label_part in m.group(3):
            style = (m.group(2) or ' style=""')[:-1] + (f';object-position:{pos}' if pos else '') + '"'
            new = f'<img class="phimg {m.group(1)}"{style} src="{src}" alt="">'
            return html[:m.start()] + new + html[m.end():]
    raise KeyError(label_part)

def swap_src(html, old_key, src):
    return html.replace('{{IMG:' + old_key + '}}', src, 1)

def offer_free_ship(html):
    html = html.replace('<span>No code needed</span></div>', '<span>Free shipping</span></div>')
    return html

TAG = '<span class="hot">Almost sold out</span>'

# ---------------------------------------------------------------- emails
def e01():
    h = v5.E['01']()
    h = swap_ph(h, 'Hero', fimg('m_hand_hair'), 'center 30%')
    # lead "Where to start" with the two best-sellers
    h = h.replace('<div class="pkgrid g3">', '<div class="pkgrid g3">'
                  f'<a class="pk" href="#"><img src="{fimg("m_3x_set")}" alt="3x Minimal Set"><span class="pn">3x Minimal Set · Men</span>{g.price_html("set3")}</a>'
                  f'<a class="pk" href="#"><img src="{fimg("w_3x_set")}" alt="3x Minimal Set"><span class="pn">3x Minimal Set · Women</span>{g.price_html("set3")}</a>', 1)
    h = h.replace('<div class="pkgrid g3">', '<div class="pkgrid">', 1)
    h = re.sub(r'<a class="pk" href="#"><img src="\{\{IMG:braid-armband__0\}\}".*?</a>', '', h, count=1, flags=re.S)
    h = h.replace('Three pieces people never take off.', 'Our two best-sellers first. Then the pieces people never take off.')
    return h

def e02():
    h = v5.E['02']()
    h = swap_ph(h, 'Hero', fimg('w_face_wet'))
    h = swap_src(h, '3x-minimal-stack-set__1', fimg('m_3x_set'))
    h = h.replace('<span class="lab">The best value</span>', f'<span class="lab">Best-seller</span>{TAG}', 1)
    return offer_free_ship(h)

def e03():
    h = v5.E['03']()
    h = swap_ph(h, 'Hero', img('fighk_m_bw_fist'), 'center 40%')
    h = swap_src(h, '3x-minimal-stack-set__2', fimg('w_3x_set'))
    return offer_free_ship(h)

def e04():
    rows = [('3x Minimal Set · Men', 'fig_m_3x_set', 94.95, True), ('3x Minimal Set · Women', 'fig_w_3x_set', 94.95, True),
            ('4x Stacked Set', 'stacked-set__0', 89.95, False), ('2x Duo Minimal Set', '2x-duo-minimal-set__1', 59.95, False)]
    led = '<div class="ledger"><div class="lh"><span>Set</span><span>Now</span><span>You save</span></div>'
    for name, key, reg, hot in rows:
        s = sale(reg)
        led += (f'<a class="lr" href="#"><img src="{img(key)}" alt="{name}"><div><h4>{name}{TAG if hot else ""}</h4>'
                f'<p class="small mute"><s>{eur(reg)}</s> · case included</p></div>'
                f'<span class="now">{eur(s)}</span><span class="sv">{eur(round(reg - s, 2))}</span></a>')
    led += '</div>'
    return ''.join([
        strip('Black Friday · 30% off sitewide · free shipping'), logobar(),
        capttl('Black Friday · the Sets', 'Buy the Set once',
               'Our best-sellers are the 3x Minimal Sets, and they’re going fast. 30% off, and the jewelry case comes with every Set.', center=False),
        '<div class="mcta tight"><a class="solid" href="#">Shop the Sets</a>' + v5.PROOF + '</div>',
        led,
        f'<div class="pair" style="padding-top:30px"><img src="{fimg("w_chair")}" alt=""><img src="{fimg("m_wrist_close")}" alt=""></div>',
        '<div class="sec"></div>',
        casecard('Included with every Set', 'The jewelry case. €19.95 value, yours with any Set or any two pieces.', 'Shop the Sets'),
        '<div style="height:52px"></div>', foot()])

def e05():
    h = v5.E['05']()
    return swap_ph(h, 'Hero', fimg('w_wet_swim'), 'center 45%')

def e06():
    h = v5.E['06']()
    h = swap_ph(h, 'Hero', img('minimal-cuff__3'), 'center 60%')
    h = swap_ph(h, 'packshot on white', img('minimal-cuff__0'))
    h = swap_ph(h, 'macro', img('minimal-cuff-1__2'))
    h = swap_ph(h, 'worn, with a Set', fimg('m_linen_chest'))
    h = h.replace('<div class="limited">', '<p class="stand">Stand-in photos (Minimal Cuff) until the Matte Cuff shoot is in.</p><div class="limited">', 1)
    return h

def e08():
    h = v5.E['08']()
    h = swap_ph(h, 'Hero', img('fighk_m_linen_chin'), 'center 35%')
    h = h.replace('<div class="sec" style="padding-top:30px"></div>', '', 1)
    h = h.replace('<div class="obar">', '<div class="mcta tight" style="padding-top:28px"><a class="solid" href="#">Shop Cyber Week</a></div><div class="obar">', 1)
    h = h.replace('<h4>Sets</h4>', f'<h4>Sets</h4>', 1)
    return offer_free_ship(h)

def e10():
    h = v5.E['10']()
    return swap_ph(h, 'Hero', fimg('w_black_top'))

def e12():
    h = v5.E['12']()
    h = swap_ph(h, 'Hero', fimg('w_crossed'), 'center 40%')
    h = h.replace('<p class="hsub">At 30% off this year</p>', '<p class="hsub">At 30% off this year</p><a class="hbtn" href="#">Shop the last weekend</a>', 1)
    h = swap_ph(h, 'Matte Cuff', img('minimal-cuff__0'))
    h = swap_src(h, '3x-minimal-stack-set__1', fimg('m_3x_set'))
    h = h.replace('Jewelry case included</p>', 'Jewelry case included · <b class="hotx">almost sold out</b></p>', 1)
    h = h.replace('<span class="lab">Final weekend</span><b>2 days left</b>',
                  '<span class="lab">Final weekend · almost sold out</span><b>2 days left</b>', 1)
    return h

def e13():
    h = v5.E['13']()
    h = swap_ph(h, 'Hero', img('fighk_m_beach_arm'), 'center 40%')
    h = swap_src(h, '3x-minimal-stack-set__0', fimg('m_3x_set'))
    h = swap_src(h, 'crystal-necklace__5', fimg('w_3x_set'))
    h = swap_src(h, 'minimal-cuff__3', fimg('w_face_wet'))
    h = h.replace('<span class="lab">The one to get</span>', f'<span class="lab">The one to get</span>{TAG}', 1)
    h = h.replace('30% off everything until 23:59 CET tonight.', 'The 3x Minimal Sets are almost sold out. 30% off everything until 23:59 CET tonight.', 1)
    return h

FN = {'01': e01, '02': e02, '03': e03, '04': e04, '05': e05, '06': e06, '08': e08, '10': e10, '12': e12, '13': e13}
for s in g.SENDS:
    if s['n'] in FN:
        s['fn'] = FN[s['n']]
    if s['n'] == '04':
        s['subj'] = ('Our best-seller is almost sold out', 'Save €28 on the 3x Minimal Set')
        s['pre'] = 'The 3x Minimal Sets, 30% off, case included.'
    if s['n'] == '12':
        s['subj'] = ('Almost sold out: 2 days left at 30%', '2 days left at 30% off')
        s['pre'] = 'The 3x Minimal Sets are going fast. Ends Sunday, 23:59 CET.'
        s['job'] = 'Last year’s best performer was “almost sold out”. Lead with it, plus the real deadline.'
    if s['n'] == '13':
        s['pre'] = 'The 3x Minimal Sets are almost gone. 30% off ends at 23:59 CET.'

V6_CSS = """
/* ---- v6: real photos + scarcity ---- */
.phimg{display:block;width:100%;object-fit:cover;max-width:100%}
.hero .phimg{margin:0}
.split .phimg.sp{aspect-ratio:3/4}
.duo2 .phimg{aspect-ratio:3/4}
.dropgrid .phimg.dg1{grid-row:span 2;height:100%;min-height:420px}
.dropgrid .phimg.dg2,.dropgrid .phimg.dg3{aspect-ratio:1/1}
.stage .phimg.prod{aspect-ratio:1/1;margin:0 80px;width:auto}
.newcard .phimg.nc{aspect-ratio:1/1;padding:0}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.18) 0%,rgba(0,0,0,0) 35%,rgba(0,0,0,0) 55%,rgba(0,0,0,.35) 100%);pointer-events:none}
.hero.red::after{background:linear-gradient(180deg,rgba(255,255,255,.35) 0%,rgba(255,255,255,0) 45%,rgba(0,0,0,0) 70%,rgba(0,0,0,.25) 100%)}
.hero .htop,.hero .hlogo,.hero .hcopy{z-index:1}
.hot{display:inline-block;margin-left:8px;padding:3px 6px;border:1px solid var(--red);color:var(--red);font:500 8.5px/1 var(--body);letter-spacing:.14em;text-transform:uppercase;vertical-align:middle}
.hotx{color:var(--red);font-weight:500}
.stand{margin:14px 24px 0;text-align:center;font:300 italic 11px/1.4 var(--body);color:var(--grey)}
"""

def red_strip(html):
    def f(m):
        cls, txt = m.group(1), m.group(2)
        parts = txt.split(' · ', 1)
        if cls.strip() == 'strip red':
            return m.group(0)
        head = f'<span class="rs">{parts[0]}</span>'
        return f'<div class="{cls}">' + head + (' · ' + parts[1] if len(parts) > 1 else '') + '</div>'
    html = re.sub(r'<div class="(strip[^"]*)">([^<]*)</div>', f, html)
    html = re.sub(r'<div class="htop">([^<·]+?) · ', lambda m: f'<div class="htop"><span class="rs">{m.group(1)}</span> · ', html)
    return html

if __name__ == '__main__':
    tp = os.path.join(g.HERE, 'bfcm26.tpl.html')
    tpl = open(tp).read()
    if '/* ---- v6:' not in tpl:
        tpl = tpl.replace('</style>', V6_CSS + '</style>', 1)
    tpl = tpl.replace('Striped boxes are hero placeholders for campaign photography; everything else is real Cavaier product photography from cavaier.com.',
                      'Photography comes from the Cavaier Figma shoots (Static Ads 1 and 2) and cavaier.com, shown in black and white. Swap any image in Figma.')
    tpl = tpl.replace('<li>Matte Cuff: “limited first batch” only if the run really is limited, and the restock month needs filling in.</li>',
                      '<li>Matte Cuff: the photos are Minimal Cuff stand-ins until the Matte Cuff shoot is in. The restock month still needs filling in.</li>')
    open(tp, 'w').write(tpl)
    html = v3.build()
    with cf.ThreadPoolExecutor(10) as ex:
        data = dict(ex.map(fetch, sorted(g.USED)))
    uri = {k: 'data:image/jpeg;base64,' + base64.b64encode(v).decode() for k, v in data.items()}
    html = red_strip(html)
    html = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: uri[m.group(1)], html)
    assert 'warrant' not in html.lower()
    left = re.findall(r'<div class="ph [^"]*"[^>]*><span>([^<]*)</span>', html)
    print('placeholders left:', left)
    open(os.path.join(g.HERE, 'cavaier-bfcm26-sequence.html'), 'w').write(html)
    print(len(g.USED), 'images,', len(html) // 1024, 'KB')
