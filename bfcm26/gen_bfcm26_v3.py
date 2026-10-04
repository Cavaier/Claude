#!/usr/bin/env python3
"""v3: one unisex version per email, caps hero overlays in the style of Cavaier's past emails,
B&W photography, sparing #C2371A, no warranty claims."""
import base64, io, os, re, concurrent.futures as cf, urllib.request
from html import escape
from PIL import Image, ImageOps
import gen_bfcm26 as g
import gen_bfcm26_v2 as v2
from gen_bfcm26 import (img, strip, spec, timer, cta, P, sale, eur, price_html, listrow, foot, PRE, LIVE, CW)

RED = '#C2371A'

# ---------------------------------------------------------------- modules (from past Cavaier emails)
def hero(head, sub, label, btn=None, tone='white', pos='bottom', ratio='600/720', top=None, align='left'):
    t = f'<div class="htop">{top}</div>' if top else ''
    b = f'<a class="hbtn" href="#">{btn}</a>' if btn else ''
    return (f'<div class="hero {tone} {pos} {align}"><div class="ph hph" style="aspect-ratio:{ratio}"><span>{label}</span></div>'
            f'{t}<p class="hlogo">Cavaier</p><div class="hcopy"><h2>{head}</h2><p class="hsub">{sub}</p>{b}</div></div>')

def logobar(right=''):
    r = f'<span class="lab">{right}</span>' if right else '<nav><span>Bracelets</span><span>Necklaces</span><span>Sets</span></nav>'
    return f'<div class="mbar"><p class="wm">Cavaier</p>{r}</div>'

def capttl(label, head, copy='', center=True):
    c = f'<p class="small">{copy}</p>' if copy else ''
    return f'<div class="cttl{" c" if center else ""}"><span class="lab">{label}</span><h2>{head}</h2>{c}</div>'

def quote(text, name):
    return (f'<div class="vq"><p>“{text}”</p><span>— {name} <i>✓</i> verified buyer</span></div>')

def review(title, text, name):
    return (f'<div class="rcard"><span class="stars">★★★★★</span><h4>{title}</h4><p class="small">{text}</p>'
            f'<span class="rn">– {name}</span></div>')

def trust():
    return ('<div class="trust"><div class="tp"><span class="stars">★★★★★</span><span class="lab">Trustpilot</span></div>'
            '<b>4.5</b><p class="lab">2,179 reviews · trusted worldwide</p></div>')

def casecard(title, sub, btn):
    return (f'<div class="ccard"><h3>{title}</h3><p class="small">{sub}</p>'
            f'<img src="{img("jewelry-case__1")}" alt="Cavaier jewelry case"><a class="solid" href="#">{btn}</a></div>')

def crafted(items, title=None, sub=None, btn=None):
    h = (f'<div class="cttl c"><h2 class="sm">{title}</h2>' + (f'<p class="small">{sub}</p>' if sub else '') + '</div>') if title else ''
    cells = ''.join(f'<a class="pk" href="#"><img src="{img(i)}" alt="{P[k][0]}"><span class="pn">{P[k][0]}</span>{price_html(k)}</a>'
                    for k, i in items)
    b = cta(btn) if btn else ''
    return f'{h}<div class="pkgrid{" g3" if len(items) == 3 else ""}">{cells}</div>{b}'

def mosaic(pk1, pk2, tall, wide, text):
    (k1, i1), (k2, i2) = pk1, pk2
    return (f'<div class="mosaic">'
            f'<a class="m pk1" href="#"><img src="{img(i1)}" alt=""><span class="pn">{P[k1][0]}</span>{price_html(k1)}</a>'
            f'<div class="m txt"><p>{text}</p></div>'
            f'<a class="m pk2" href="#"><img src="{img(i2)}" alt=""><span class="pn">{P[k2][0]}</span>{price_html(k2)}</a>'
            f'<div class="m tall"><img src="{img(tall)}" alt=""></div>'
            f'<div class="m wide"><img src="{img(wide)}" alt=""><a class="gbtn" href="#">Shop now</a></div></div>')

def split(label, head, sub, parts, fallback, link, phlabel):
    cells = ''.join(f'<div><b>{n}</b><span class="lab">{u}</span></div>' for n, u in parts)
    return (f'<div class="split">{g.ph(phlabel, cls="sp")}<div class="st"><span class="lab">{label}</span><h2>{head}</h2>'
            f'<p class="small">{sub}</p><div class="vt">{cells}</div><p class="small mute">{fallback}</p>'
            f'<a class="ulink" href="#">{link} <span>→</span></a></div></div>')

def msh(t, r=''):
    return g.msh(t, r)

# ---------------------------------------------------------------- the 10 designed emails (unisex)
def e01():
    return ''.join([
        strip(PRE),
        hero('Once a year,<br>you go first', 'Early access · 30% off everything', 'Hero · B&W · close portrait, pendant across the face · 600×720',
             btn='Shop early access', align='center'),
        quote('Minimal yet eye-catching. Great value and fast delivery.', 'Adam P.'),
        '<p class="letter">From today until Friday, everything is 30% off for subscribers, before the public sale. It comes off at checkout. No code.</p>',
        spec([('Everything', '30% off'), ('Any Set', 'Jewelry case included'), ('Any two pieces', 'Jewelry case included'), ('Open to everyone', 'Fri Nov 27')]),
        '<div class="sec"></div>',
        crafted([('crystalN', 'crystal-necklace__4'), ('cuff', 'minimal-cuff__0'), ('braid', 'braid-armband__0')],
                'Where to start', 'Three pieces people never take off.', 'Shop early access'),
        '<p class="small mute center">Early access ends when the sale opens to everyone, Fri Nov 27 at 07:00 CET.</p><div style="height:40px"></div>',
        foot()])

def e02():
    return ''.join([
        strip(PRE), logobar(),
        split('Early access · 2 days left', 'Choose once.<br>Wear it every day.', 'Our most-worn pieces, 30% off before the public sale on Friday.',
              [('01', 'Days'), ('21', 'Hours')], 'Public sale opens Fri Nov 27, 07:00 CET', 'Shop early access', 'Hero · B&W · 3:4 · 264×352'),
        f'<div class="feature"><img src="{img("3x-minimal-stack-set__1")}" alt="3x Minimal Set worn"><div class="fc">'
        '<div><span class="lab">The best value</span><h3>3x Minimal Set</h3><p class="small mute">Three bracelets, worn together or apart. Jewelry case included.</p></div>'
        f'{price_html("set3")}</div></div>',
        '<div class="sec">', msh('Or pair two', 'Case included'),
        g.grid([g.card('cubanN', 'cuban-necklace-1__1', ratio='tall'), g.card('set2', '2x-duo-minimal-set__0', ratio='tall')], 2), '</div>',
        '<div class="sec"></div>',
        casecard('The jewelry case', 'Any Set, or any two pieces. The case comes with it.', 'Shop early access'),
        '<div style="height:52px"></div>', foot()])

def e03():
    return ''.join([
        hero('Black Friday', '30% off everything', 'Hero · B&W · editorial close crop, Set on forearm · 600×760', btn='Shop the sale',
             tone='red', pos='upper', ratio='600/760', top='Black Friday · 30% off sitewide · Nov 27 – Dec 6'),
        '<div class="under"><p class="copy">Once a year. Everything is 30% off until Dec 6, applied at checkout. No code.</p></div>',
        spec([('Everything', '30% off'), ('Any Set or two pieces', 'Jewelry case included'), ('Shipping', 'Free on every order'), ('Gift cards', 'Not included')]),
        '<div class="sec"></div>',
        mosaic(('ropeP', 'rope-necklace__7'), ('cuff', 'minimal-cuff-1__2'), 'role-necklace-1__2', '3x-minimal-stack-set__2', 'Thirty<br>percent.<br>Once<br>a year.'),
        '<div class="sec"></div>',
        review('Loved for their simplicity', 'Minimalistic but luxurious. The way these bracelets elevate an outfit is unbelievable. Compliments every single day.', 'Nicole A'),
        cta('Shop Black Friday'), foot()])

def e04():
    rows = [('3x Minimal Set', '3x-minimal-stack-set__3', 94.95), ('4x Stacked Set', 'stacked-set__0', 89.95),
            ('2x Duo Minimal Set', '2x-duo-minimal-set__1', 59.95), ('Crystal Necklace + Bracelet', 'crystal-necklace__1', 129.90)]
    led = '<div class="ledger"><div class="lh"><span>Set</span><span>Now</span><span>You save</span></div>'
    for name, image, reg in rows:
        s = sale(reg)
        led += (f'<a class="lr" href="#"><img src="{img(image)}" alt="{name}"><div><h4>{name}</h4>'
                f'<p class="small mute"><s>{eur(reg)}</s> · case included</p></div>'
                f'<span class="now">{eur(s)}</span><span class="sv">{eur(round(reg - s, 2))}</span></a>')
    led += '</div>'
    return ''.join([
        strip(LIVE), logobar(),
        capttl('Black Friday · the Sets', 'Buy the Set once', 'The biggest saving is in the Sets: 30% off, and the jewelry case comes with every one.', center=False),
        led,
        f'<div class="pair" style="padding-top:30px"><img src="{img("stacked-set__1")}" alt=""><img src="{img("3x-minimal-stack-set-1__0")}" alt=""></div>',
        '<div class="sec"></div>',
        casecard('Included with every Set', 'The jewelry case. €19.95 value, yours with any Set or any two pieces.', 'Shop the Sets'),
        '<div style="height:52px"></div>', foot()])

def e05():
    return ''.join([
        strip(LIVE), logobar(),
        trust(),
        review('Hard wearing and stylish', 'This is my second purchase from Cavaier. The jewellery is so delicate but also hard wearing. Holds its colour, doesn’t tarnish, and looks brilliant. Love it.', 'Maxwell S'),
        quote('Same outfit, different person. I didn’t expect that.', 'Hana G.'),
        hero('Never taken off', 'Worn in the shower, at the gym, to sleep', 'Hero · B&W · wet skin, bracelet on wrist · 600×560', btn='Shop most loved',
             ratio='600/560', align='center'),
        '<div class="sec"></div>',
        crafted([('ropeB', 'rope-bracelet-2__3'), ('cubanN', 'cuban-necklace-1__1'), ('cubeB', 'cube-bracelet-1__1'), ('crystalB', 'bracelet__1')],
                'Most loved', '30% off until Dec 6.', 'Shop most loved'),
        foot()])

def e06():
    details = [('01', 'Finish', 'Matte'), ('02', 'Material', '316L stainless steel'), ('03', 'Fit', 'Adjustable'), ('04', 'Wear it', 'Water, gym, sleep')]
    return ''.join([
        strip('Black Friday weekend · 30% off everything else'),
        hero('The Matte Cuff', 'Same fit, softer light', 'Hero · B&W · Matte Cuff on wrist, side light · 600×700', btn='Discover it',
             ratio='600/700', top='<span class="new">New</span> · Nov 28'),
        '<div class="details" style="margin-top:44px">' + ''.join(f'<div><span class="num">{n}</span><span class="lab">{a}</span><p>{b}</p></div>' for n, a, b in details) + '</div>',
        '<div class="launchp"><span class="pr">€39.95</span><span class="small mute">New arrival, full price. Not part of the Black Friday offer.</span></div>',
        '<div class="stage" style="margin-top:36px">' + g.ph('Matte Cuff · packshot on white · 440×440', cls='prod') + '</div>',
        cta('Shop the Matte Cuff'),
        '<div class="sec" style="padding-top:0"></div>', msh('Wear it with', '30% off'),
        g.grid([g.card('braid', 'braid-armband__3', ratio='tall'), g.card('crystalB', 'bracelet__5', ratio='tall')], 2),
        '<div class="sec"></div>',
        casecard('Make it two', 'Matte Cuff plus any other piece, and the jewelry case is included.', 'Shop the weekend'),
        '<div style="height:52px"></div>', foot()])

def e08():
    t = [('Bracelets', 'cube-bracelet__1', 'from €20.97'), ('Necklaces', 'role-necklace-1__1', 'from €24.43'),
         ('Cuffs', 'minimal-cuff-1__5', 'from €24.43'), ('Sets', 'stacked-set__0', 'from €41.97')]
    return ''.join([
        hero('Cyber Week', '30% off · seven days left', 'Hero · B&W · profile, necklace, hard side light · 600×640', btn='Shop Cyber Week',
             tone='red', pos='bottom', ratio='600/640', top='Cyber Week · Nov 30 – Dec 6'),
        '<div class="sec" style="padding-top:30px"></div>',
        timer('Sale ends in', [('06', 'D'), ('16', 'H'), ('59', 'M')], 'Ends Sun Dec 6, 23:59 CET'),
        '<div class="sec">', msh('Shop by category', '30% off'), g.tiles(t), '</div>',
        cta('Shop Cyber Week', 'Jewelry case included with any Set or two pieces.'),
        foot()])

def e10():
    def sec(n, t, items):
        return (f'<div class="sec"><div class="sh"><span class="num">{n}</span><span class="t">{t}</span></div>'
                + g.grid([g.card(k, i) for k, i in items], 3) + '</div>')
    return ''.join([
        strip(CW), logobar(),
        capttl('Cyber Week · gift guide', 'Gifts, by price', 'Prices shown with 30% already off. Every piece adjusts, so size is never a guess.'),
        f'<div class="duo2" style="margin-top:0">{g.ph("Hero · B&W · gift moment, case in hand", cls="dhero")}<img src="{img("jewelry-case__0")}" alt="Jewelry case"></div>',
        sec('01', 'Under €25', [('cubanN', 'cuban-necklace-1__5'), ('cuff', 'minimal-cuff__5'), ('ropeB', 'rope-bracelet-2__1')]),
        sec('02', 'Under €30', [('roleP', 'role-necklace-1__6'), ('braid', 'braid-armband__5'), ('cubeP', 'cube-necklace__1')]),
        '<div class="sec"><div class="sh"><span class="num">03</span><span class="t">The big one</span></div>'
        + g.setrow('3x Minimal Set', '3x-minimal-stack-set__4', 'The full Set, case included.', 94.95, 'case included') + '</div>',
        '<div class="giftrow"><img src="' + img('cavaier-gift-card__0') + '" alt=""><div><span class="lab">Still not sure?</span>'
        '<h4>The gift card</h4><p class="small mute">€10 to €100, sent by email, valid 3 months. Not discounted.</p></div></div>',
        cta('Find a gift'), foot()])

def e12():
    rows = [listrow('set3', '3x-minimal-stack-set__1', 'Jewelry case included'), listrow('crystalN', 'crystal-necklace__4'),
            listrow('cuff', 'minimal-cuff__0'), listrow('roleP', 'role-necklace-1__1')]
    return ''.join([
        strip('Final weekend · 30% off ends Sun 23:59 CET'), logobar(),
        v2.bigtimer([('02', 'Days'), ('05', 'Hours'), ('59', 'Minutes')], 'Final weekend · the sale ends in', 'Sunday Dec 6, 23:59 CET. After that, it’s full price.'),
        cta('Shop before Sunday'),
        hero('The last weekend', 'At 30% off this year', 'Hero · B&W · layered pieces, warm light · 600×440', ratio='600/440', align='center'),
        '<div class="sec">', msh('Still on your list?', '30% off'), ''.join(rows), '</div>',
        f'<div class="newcard">{g.ph("Matte Cuff", cls="nc")}<div><span class="lab red">New this week</span><h4>The Matte Cuff</h4>'
        '<p class="small mute">Full price, €39.95. Pairs with everything above, and counts toward the case.</p></div></div>',
        cta('Shop before Sunday'), foot()])

def e13():
    return ''.join([
        hero('Last day', '30% off ends tonight', 'Hero · B&W · close-up, Set on wrist · 600×700', btn='Shop the last day',
             tone='red', pos='mid', ratio='600/700', top='Last day · ends 23:59 CET'),
        '<div class="sec" style="padding-top:30px"></div>',
        timer('Time left', [('13', 'H'), ('59', 'M'), ('00', 'S')], 'Ends tonight, Sun Dec 6, 23:59 CET'),
        capttl('Dec 6', 'Once it ends, it ends', '30% off everything until 23:59 CET tonight. Tomorrow, prices go back to normal.'),
        f'<div class="one"><img src="{img("3x-minimal-stack-set__0")}" alt="3x Minimal Set"><div><span class="lab">The one to get</span>'
        '<h3>3x Minimal Set</h3><p class="small">Waterproof, adjustable, 316L stainless steel.</p>'
        f'{price_html("set3")}<p class="save">You save {eur(round(94.95 - sale(94.95), 2))} · case included</p></div></div>',
        f'<div class="pair"><img src="{img("crystal-necklace__5")}" alt=""><img src="{img("minimal-cuff__3")}" alt=""></div>',
        spec([('Everything', '30% off'), ('Any Set or two pieces', 'Jewelry case included'), ('Ends', 'Tonight, 23:59 CET')]),
        cta('Shop the last day'), foot()])

FN = {'01': e01, '02': e02, '03': e03, '04': e04, '05': e05, '06': e06, '08': e08, '10': e10, '12': e12, '13': e13}
for s in g.SENDS:
    if s['n'] in FN: s['fn'] = FN[s['n']]
    if s['n'] == '07': s['text'] = v2.t07
    if s['n'] == '11': s['text'] = v2.t11; s['job'] = v2.FN and 'Answer the quality doubt directly: material, waterproofing, fit and reviews.'

# unisex audiences
for s in g.SENDS:
    s['aud'] = s['aud']

def build():
    rows, entries = [], []
    for s in g.SENDS:
        rows.append(f'<tr><td><a href="#e{s["n"]}">{s["n"]}</a></td><td>{s["date"]}<span class="tm">{s["time"]}</span></td>'
                    f'<td>{s["phase"]}</td><td>{s["name"]}</td><td>{s["fmt"]}</td><td>{g.pips(s["heat"])}</td>'
                    f'<td class="sj">{escape(s["subj"][0])}</td></tr>')
        body = (f'<article class="em" aria-label="Email {s["n"]}">{s["fn"]()}</article>' if 'fn' in s else
                f'<article class="em txt" aria-label="Email {s["n"]}, text only">{s["text"]}</article>')
        entries.append(f'''
<section class="entry" id="e{s["n"]}">
  <div class="rail"><span class="no">{s["n"]}</span><p class="d">{s["date"]}</p><p class="tm2">{s["time"]} CET</p>
    <p class="ph2">{s["phase"]}</p>{g.pips(s["heat"])}<p class="heat">{g.HEAT[s["heat"]]}</p></div>
  <div class="main">
    <dl class="meta">
      <dt>Email</dt><dd><b>{s["name"]}</b> · {s["fmt"]}</dd>
      <dt>Subject A</dt><dd>{escape(s["subj"][0])}</dd><dt>Subject B</dt><dd>{escape(s["subj"][1])}</dd>
      <dt>Preheader</dt><dd>{escape(s["pre"])}</dd><dt>Audience</dt><dd>{s["aud"]}</dd>
      <dt>Job</dt><dd>{s["job"]}</dd><dt>ClickUp</dt><dd class="mono">{s["task"]}</dd>
    </dl>
    {body}
  </div>
</section>''')
    tpl = open(os.path.join(g.HERE, 'bfcm26.tpl.html')).read()
    return tpl.replace('%%ROWS%%', ''.join(rows)).replace('%%ENTRIES%%', ''.join(entries))

def fetch_bw(key):
    path = os.path.join(g.HERE, 'imgcache26bw', key + '.jpg')
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path): return key, open(path, 'rb').read()
    _, data = g.fetch(key)
    im = Image.open(io.BytesIO(data)).convert('L')
    im = ImageOps.autocontrast(im, cutoff=0.5).convert('RGB')
    b = io.BytesIO(); im.save(b, 'JPEG', quality=66, optimize=True, progressive=True)
    open(path, 'wb').write(b.getvalue()); return key, b.getvalue()

V3_CSS = """
/* ---- v3: past-email modules, caps heroes, B&W ---- */
.hero{position:relative;color:var(--white)}
.hero .hph{background:repeating-linear-gradient(135deg,#8E8E8C 0 12px,#858583 12px 24px);margin:0;align-items:flex-end;justify-content:flex-end}
.hero .hph span{background:rgba(255,255,255,.92)}
.hero .htop{position:absolute;left:24px;right:24px;top:18px;padding:9px 12px;background:rgba(255,255,255,.14);text-align:center;font:400 10px/1.4 var(--body);letter-spacing:.18em;text-transform:uppercase;color:var(--white)}
.hero .htop .new{color:var(--red);font-weight:500}
.hero .hlogo{position:absolute;left:30px;top:66px;margin:0;font:400 17px/1 var(--wm);letter-spacing:.06em;text-transform:uppercase}
.hero .hcopy{position:absolute;left:30px;right:30px;bottom:56px;display:flex;flex-direction:column;gap:4px;align-items:flex-start}
.hero.center .hcopy{align-items:center;text-align:center}
.hero.upper .hcopy{top:30%;bottom:auto}
.hero.mid .hcopy{bottom:24%}
.hero h2{margin:0;font:300 30px/1.12 var(--disp);letter-spacing:.08em;text-transform:uppercase}
.hero .hsub{margin:0;font:300 15px/1.4 var(--disp);letter-spacing:.1em;text-transform:uppercase;opacity:.92}
.hero .hbtn{margin-top:18px;display:block;min-width:234px;text-align:center;padding:14px 22px;background:rgba(255,255,255,.88);color:var(--black);text-decoration:none;font:400 10.5px/1 var(--body);letter-spacing:.22em;text-transform:uppercase}
.hero.red{color:var(--red)}
.hero.red h2{font-weight:500;font-family:var(--body);font-size:46px;letter-spacing:.02em;line-height:1}
.hero.red .hsub{font-family:var(--body);font-size:28px;letter-spacing:.03em;line-height:1.1;opacity:1}
.hero.red .hlogo{color:var(--red)}
.hero.red .htop{color:var(--white)}
.vq{padding:52px 40px 44px;text-align:center;display:flex;flex-direction:column;gap:12px;align-items:center}
.vq p{margin:0;font:300 19px/1.4 var(--disp);max-width:400px}
.vq span{font:300 italic 11.5px/1 var(--body);color:var(--grey)}
.vq i{font-style:normal;display:inline-grid;place-items:center;width:13px;height:13px;border-radius:50%;background:#3A3A38;color:var(--white);font-size:8px;margin:0 2px}
.rcard{margin:0 40px;border:1px solid #BDBDBA;padding:24px 26px;display:flex;flex-direction:column;gap:10px}
.rcard .stars{letter-spacing:.2em;font-size:13px}
.rcard h4{margin:0;font:500 11px/1.3 var(--body);letter-spacing:.16em;text-transform:uppercase}
.rcard .rn{font:500 12px/1 var(--body)}
.trust{padding:48px 24px 30px;display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center}
.trust .tp{display:flex;gap:10px;align-items:center}
.trust .stars{letter-spacing:.2em;font-size:13px}
.trust b{font:300 96px/.9 var(--disp);letter-spacing:-.05em}
.ccard{margin:0 24px;background:var(--fog);border-radius:10px;padding:40px 24px 44px;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center}
#e02 .ccard,#e05 .ccard,#e08 .ccard,#e10 .ccard,#e13 .ccard{background:var(--white)}
.ccard h3{margin:0;font:400 15px/1.3 var(--body);letter-spacing:.16em;text-transform:uppercase}
.ccard img{width:70%;aspect-ratio:4/3;object-fit:contain;background:transparent;mix-blend-mode:multiply;margin:10px 0 16px}
.cttl{padding:44px 24px 24px;display:flex;flex-direction:column;gap:10px}
.cttl.c{align-items:center;text-align:center}
.cttl h2{margin:0;font:300 26px/1.15 var(--disp);letter-spacing:.08em;text-transform:uppercase}
.cttl h2.sm{font-size:17px;letter-spacing:.16em;font-weight:400}
.cttl .small{max-width:420px;color:var(--ink2)}
.pkgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;padding:0 24px}
.pkgrid.g3{grid-template-columns:repeat(3,1fr)}
.pk{display:flex;flex-direction:column;align-items:center;gap:6px;text-decoration:none;background:var(--fog);padding-bottom:18px;text-align:center}
#e02 .pk,#e05 .pk,#e08 .pk,#e10 .pk,#e13 .pk{background:var(--white)}
.pk img{aspect-ratio:1/1;mix-blend-mode:multiply;background:transparent}
.pn{font:400 9.5px/1.4 var(--body);letter-spacing:.22em;text-transform:uppercase;margin-top:6px}
.pk .price,.mosaic .price{font-size:12px}
.pkgrid + .mcta{padding-top:30px}
.mosaic{display:grid;grid-template-columns:1fr 1fr;gap:4px;padding:0 24px}
.mosaic .m{position:relative;min-width:0}
.mosaic .pk1,.mosaic .pk2{background:#F4F4F3;display:flex;flex-direction:column;align-items:center;gap:6px;padding-bottom:16px;text-decoration:none}
.mosaic .pk1 img,.mosaic .pk2 img{aspect-ratio:1/1;mix-blend-mode:multiply;background:transparent}
.mosaic .txt{background:#F4F4F3;display:flex;align-items:flex-start;justify-content:flex-end;padding:28px 20px}
.mosaic .txt p{margin:0;text-align:right;font:300 22px/1.25 var(--disp);letter-spacing:.1em;text-transform:uppercase;color:#3A3A38}
.mosaic .tall{grid-row:span 2}
.mosaic .tall img{height:100%;aspect-ratio:auto}
.mosaic .pk2{grid-column:1}
.mosaic .wide{grid-column:1/-1}
.mosaic .wide img{aspect-ratio:552/300}
.gbtn{position:absolute;right:16px;bottom:22px;padding:10px 40px;background:rgba(255,255,255,.3);border:1px solid rgba(255,255,255,.6);color:var(--white)!important;text-decoration:none;font:400 10px/1 var(--body);letter-spacing:.22em;text-transform:uppercase}
.center{text-align:center}
.mcard h4{font:400 9.5px/1.4 var(--body)!important;letter-spacing:.2em;text-transform:uppercase}
.mbar nav{text-transform:none}
@media (max-width:480px){.hero h2{font-size:22px}.hero.red h2{font-size:34px}.hero.red .hsub{font-size:20px}.rcard{margin:0 24px}.mosaic .txt p{font-size:16px}}
"""

if __name__ == '__main__':
    tp = os.path.join(g.HERE, 'bfcm26.tpl.html')
    tpl = open(tp).read()
    if '/* ---- v3:' not in tpl:
        tpl = tpl.replace('</style>', V3_CSS + '</style>', 1)
    # unisex: drop the W/M switch and its copy
    tpl = re.sub(r'<div class="seg".*?</div>\s*', '', tpl, count=1, flags=re.S)
    tpl = tpl.replace('Designed emails have a Women and a Men version (switch at the top of the timeline). ',
                      'One version per email, sent to everyone, mixing women’s and men’s pieces. Photography is black and white, as in your past campaigns. ')
    open(tp, 'w').write(tpl)
    html = build()
    with cf.ThreadPoolExecutor(10) as ex:
        data = dict(ex.map(fetch_bw, sorted(g.USED)))
    uri = {k: 'data:image/jpeg;base64,' + base64.b64encode(v).decode() for k, v in data.items()}
    html = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: uri[m.group(1)], html)
    assert 'warrant' not in html.lower()
    open(os.path.join(g.HERE, 'cavaier-bfcm26-sequence.html'), 'w').write(html)
    print(len(g.USED), 'images,', len(html) // 1024, 'KB')
