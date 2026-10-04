#!/usr/bin/env python3
"""v2: distinct layout per designed email, sparing #C2371A accent, no warranty claims."""
import base64, re, os, concurrent.futures as cf
import gen_bfcm26 as g
from gen_bfcm26 import (img, strip, bar, ttl, ph, msh, card, grid, spec, timer, cta, ulink,
                        case_strip, setrow, listrow, tiles, foot, P, sale, eur, price_html, PRE, LIVE, CW)

# ---------------------------------------------------------------- shared tweaks
def icons():
    return ('<div class="icons"><span>Waterproof</span><span>316L stainless steel</span>'
            '<span>Adjustable fit</span></div>')

def proof(big=False):
    q = ('<blockquote class="quote">“Paste one verified 5-star Trustpilot quote here, '
         'ideally about wearing it every day.”</blockquote>')
    return (f'<div class="proof{" big" if big else ""}"><div class="score"><b>4.5</b><span>/ 5</span></div>'
            f'<p class="small">2,179 reviews on Trustpilot</p>{q}</div>')

def rstrip(text):
    return f'<div class="strip red">{text}</div>'

def poster(head, sub, label, pos='upper', ratio='600/760', wm_right=False):
    wm = '<p class="pk r">Cavaier</p>' if wm_right else ''
    return (f'<div class="poster {pos}">{ph(label, cls="full", style=f"aspect-ratio:{ratio}")}'
            f'<div class="pt">{"" if wm_right else "<p class=pk>Cavaier</p>"}<h2>{head}</h2><p class="ps">{sub}</p></div>{wm}</div>')

def bigtimer(parts, label, fallback):
    cells = ''.join(f'<div><b>{n}</b><span class="lab">{u}</span></div>' for n, u in parts)
    return (f'<div class="btimer"><span class="lab">{label}</span><div class="bt">{cells}</div>'
            f'<p class="small mute">{fallback}</p></div>')

# ---------------------------------------------------------------- 01 · invitation (white, centred, no nav)
def e01(v):
    W = v == 'W'
    picks = ([card('crystalN', 'crystal-necklace__4'), card('braid', 'braid-armband-1__7'), card('cuff', 'minimal-cuff-1__0')]
             if W else
             [card('set3', '3x-minimal-stack-set__0'), card('cuff', 'minimal-cuff__0'), card('braid', 'braid-armband__0')])
    return ''.join([
        strip(PRE),
        '<div class="invite"><p class="wm">Cavaier</p><span class="lab">For subscribers · Nov 23 – 26</span>'
        '<h2>Once a year,<br>you go first.</h2></div>',
        ph(f'Hero · portrait · {"silver on skin, soft daylight" if W else "black on wrist, high contrast"} · 472×590', cls='portrait'),
        '<p class="letter">From today until Friday, everything is 30% off for you, before the public sale. '
        'It comes off at checkout. No code.</p>',
        spec([('Everything', '30% off'), ('Any Set', 'Jewelry case included'),
              ('Any two pieces', 'Jewelry case included'), ('Open to everyone', 'Fri Nov 27')]),
        '<div class="sec">', msh('Where to start', '03 pieces'), grid(picks, 3), '</div>',
        icons(),
        cta('Shop early access', 'Early access ends when the sale opens to everyone, Fri Nov 27 at 07:00 CET.'),
        foot()])

# ---------------------------------------------------------------- 02 · editorial split (fog)
def e02(v):
    W = v == 'W'
    big_img, pair = (('3x-minimal-stack-set-1__2', [card('cubanN', 'cuban-necklace-1__1', ratio='tall'), card('crystalB', 'bracelet__3', ratio='tall')])
                     if W else
                     ('3x-minimal-stack-set__1', [card('set2', '2x-duo-minimal-set__0', ratio='tall'), card('cuff', 'minimal-cuff__3', ratio='tall')]))
    return ''.join([
        strip(PRE), bar(v),
        '<div class="split">', ph(f'Hero · {"W" if W else "M"} · 3:4 · 264×352', cls='sp'),
        '<div class="st"><span class="lab">Early access · 2 days left</span><h2>Choose once.<br>Wear it every day.</h2>'
        '<p class="small">Our most-worn pieces, 30% off before the public sale on Friday.</p>'
        '<div class="vt"><div><b>01</b><span class="lab">Days</span></div><div><b>21</b><span class="lab">Hours</span></div></div>'
        '<p class="small mute">Public sale opens Fri Nov 27, 07:00 CET</p>'
        '<a class="ulink" href="#">Shop early access <span>→</span></a></div></div>',
        f'<div class="feature"><img src="{img(big_img)}" alt="3x Minimal Set worn"><div class="fc">'
        '<div><span class="lab">The best value</span><h3>3x Minimal Set</h3><p class="small mute">Three bracelets, worn together or apart. Jewelry case included.</p></div>'
        f'{price_html("set3")}</div></div>',
        '<div class="sec">', msh('Or pair two', 'Case included'), grid(pair, 2), '</div>',
        case_strip('Any Set, or any two pieces, comes with the jewelry case. Ready to keep or give.'),
        cta('Shop early access'),
        foot()])

# ---------------------------------------------------------------- 03 · poster launch (red overlay)
def e03(v):
    W = v == 'W'
    best = ([card('crystalN', 'crystal-necklace__5', ratio='tall'), card('roleP', 'role-necklace-1__2', ratio='tall'),
             card('cubeB', 'cube-bracelet-1__1', ratio='tall'), card('cuff', 'minimal-cuff-1__3', ratio='tall')]
            if W else
            [card('set3', '3x-minimal-stack-set__2', ratio='tall'), card('cuff', 'minimal-cuff__1', ratio='tall'),
             card('roleB', 'role-bracelet__1', ratio='tall'), card('ropeP', 'rope-necklace__1', ratio='tall')])
    return ''.join([
        rstrip(LIVE),
        poster('Black Friday', '30% off',
               f'Hero · B&W · {"portrait, pendant across the face" if W else "close crop, Set on forearm"} · 600×760'),
        '<div class="under"><p class="copy">Everything, Nov 27 – Dec 6. Applied at checkout, no code.</p></div>',
        cta('Shop the sale'),
        spec([('Everything', '30% off'), ('Any Set or two pieces', 'Jewelry case included'), ('Gift cards', 'Not included')]),
        '<div class="sec">', msh('Best sellers', '04 pieces'), grid(best, 2), '</div>',
        proof(),
        cta('Shop Black Friday'),
        foot()])

# ---------------------------------------------------------------- 04 · the ledger (white)
def e04(v):
    W = v == 'W'
    rows = ([('3x Minimal Set', '3x-minimal-stack-set-1__1', 94.95), ('Crystal Necklace + Bracelet', 'crystal-necklace__1', 129.90),
             ('Cuban Necklace + Braid Bracelet', 'braid-armband-1__4', 74.85)] if W else
            [('3x Minimal Set', '3x-minimal-stack-set__3', 94.95), ('4x Stacked Set', 'stacked-set__0', 89.95),
             ('2x Duo Minimal Set', '2x-duo-minimal-set__1', 59.95)])
    led = '<div class="ledger"><div class="lh"><span>Set</span><span>Now</span><span>You save</span></div>'
    for name, image, reg in rows:
        s = sale(reg)
        led += (f'<a class="lr" href="#"><img src="{img(image)}" alt="{name}"><div><h4>{name}</h4>'
                f'<p class="small mute"><s>{eur(reg)}</s> · case included</p></div>'
                f'<span class="now">{eur(s)}</span><span class="sv">{eur(round(reg - s, 2))}</span></a>')
    led += '</div>'
    duo = ([img('3x-minimal-stack-set-1__0'), img('crystal-necklace__5')] if W else
           [img('3x-minimal-stack-set__5'), img('stacked-set__1')])
    return ''.join([
        strip(LIVE), bar(v),
        ttl('Black Friday · the Sets', 'Buy the Set once.',
            'The biggest saving is in the Sets. 30% off, and the jewelry case comes with every one.'),
        led,
        f'<div class="pair">{"".join(f"<img src={chr(34)}{d}{chr(34)} alt=>" for d in duo)}</div>',
        '<div class="casebox"><img src="' + img('jewelry-case__0') + '" alt="Jewelry case"><div>'
        '<span class="lab">Included with every Set</span><h4>The jewelry case</h4>'
        '<p class="small mute">€19.95 value. Soft, structured, snaps shut.</p></div></div>',
        cta('Shop the Sets', 'Or add any two pieces and the case is included too.'),
        foot()])

# ---------------------------------------------------------------- 05 · proof first (fog)
def e05(v):
    W = v == 'W'
    picks = ([card('ropeP', 'rope-necklace-1__3'), card('braid', 'braid-armband-1__3'), card('cubanN', 'cuban-necklace-1__3')] if W else
             [card('roleB', 'role-bracelet__3'), card('cubeP', 'cube-necklace__3'), card('cubanB', 'cuban-bracelet__1')])
    return ''.join([
        strip(LIVE), bar(v),
        '<div class="bigproof"><span class="lab">Black Friday · day one</span><b>4.5</b>'
        '<p class="small">out of 5, from 2,179 reviews on Trustpilot</p>'
        '<blockquote class="quote">“Paste one verified 5-star Trustpilot quote here, ideally about wearing it every day.”</blockquote></div>',
        ph(f'Hero · full bleed · {"W · close-up, pendant on skin" if W else "M · close-up, bracelet on wrist"} · 600×400', cls='full', style='aspect-ratio:600/400'),
        ttl('The ones they keep on', 'Never taken off.', 'Worn in the shower, at the gym, to sleep. Now 30% off.'),
        '<div class="sec" style="padding-top:10px">', msh('Most loved', '03 pieces'), grid(picks, 3), '</div>',
        icons(),
        cta('Shop most loved', '30% off until Dec 6 · Jewelry case with any Set or two pieces'),
        foot()])

# ---------------------------------------------------------------- 06 · product launch (white, red "new")
def e06(v):
    W = v == 'W'
    pair = ([card('crystalB', 'bracelet__5', ratio='tall'), card('ropeB', 'rope-bracelet-2__3', ratio='tall')] if W else
            [card('braid', 'braid-armband__3', ratio='tall'), card('roleB', 'role-bracelet__5', ratio='tall')])
    details = [('01', 'Finish', 'Matte'), ('02', 'Material', '316L stainless steel'), ('03', 'Fit', 'Adjustable'), ('04', 'Wear it', 'Water, gym, sleep')]
    return ''.join([
        strip('Black Friday weekend · 30% off everything else'), bar(v),
        '<div class="launch"><span class="lab red">New · Nov 28</span><h2>The Matte Cuff.</h2>'
        '<p class="copy">Our Minimal Cuff, in a matte finish. Same fit, softer light.</p></div>',
        '<div class="stage">' + ph(f'Matte Cuff · packshot on fog · {"W" if W else "M"} · 440×440', cls='prod') + '</div>',
        '<div class="details">' + ''.join(f'<div><span class="num">{n}</span><span class="lab">{a}</span><p>{b}</p></div>' for n, a, b in details) + '</div>',
        '<div class="launchp"><span class="pr">€39.95</span><span class="small mute">New arrival, full price. Not part of the Black Friday offer.</span></div>',
        cta('Shop the Matte Cuff'),
        ph(f'Matte Cuff · worn · {"on skin, daylight" if W else "on wrist, high contrast"} · 600×400', cls='full', style='aspect-ratio:600/400'),
        '<div class="sec">', msh('Wear it with', '30% off'), grid(pair, 2), '</div>',
        case_strip('Matte Cuff plus any other piece makes two, so the jewelry case is included.'),
        ulink('Shop Black Friday weekend', 'center'),
        '<div style="height:52px"></div>',
        foot()])

# ---------------------------------------------------------------- 08 · cyber poster (lower-left red type)
def e08(v):
    W = v == 'W'
    t = ([('Bracelets', 'cube-bracelet-1__3', 'from €20.97'), ('Necklaces', 'role-necklace-1__1', 'from €24.43'),
          ('Cuffs', 'minimal-cuff-1__5', 'from €24.43'), ('Sets', '3x-minimal-stack-set-1__0', 'from €66.47')] if W else
         [('Bracelets', 'cube-bracelet__1', 'from €20.97'), ('Necklaces', 'role-necklace__3', 'from €24.43'),
          ('Cuffs', 'minimal-cuff__5', 'from €24.43'), ('Sets', 'stacked-set__0', 'from €41.97')])
    return ''.join([
        strip(CW), bar(v),
        poster('Cyber Week', '30% off · 7 days left',
               f'Hero · B&W · {"W · necklace, profile" if W else "M · Set on wrist, side light"} · 600×640', pos='lower', ratio='600/640', wm_right=True),
        '<div class="sec" style="padding-top:30px"></div>',
        timer('Sale ends in', [('06', 'D'), ('16', 'H'), ('59', 'M')], 'Ends Sun Dec 6, 23:59 CET'),
        '<div class="sec">', msh('Shop by category', '30% off'), tiles(t), '</div>',
        cta('Shop Cyber Week', 'Jewelry case included with any Set or two pieces.'),
        foot()])

# ---------------------------------------------------------------- 10 · gift guide (fog, numbered)
def e10(v):
    W = v == 'W'
    html = g.e10(v)
    old = re.search(r'<div class="ph mhero"[^>]*><span>[^<]*</span></div>', html).group(0)
    new = (f'<div class="duo2" style="margin-top:0">{ph("Hero · gift moment, case in hand", cls="dhero")}'
           f'<img src="{img("jewelry-case__1")}" alt="Jewelry case"></div>')
    return html.replace(old, new, 1)

# ---------------------------------------------------------------- 12 · the countdown is the hero (white)
def e12(v):
    W = v == 'W'
    rows = ([listrow('crystalN', 'crystal-necklace__4'), listrow('roleP', 'role-necklace-1__1'),
             listrow('crystalB', 'bracelet__5'), listrow('set3', '3x-minimal-stack-set-1__2', 'Jewelry case included')] if W else
            [listrow('set3', '3x-minimal-stack-set__1', 'Jewelry case included'), listrow('set4', 'stacked-set__0', 'Jewelry case included'),
             listrow('cuff', 'minimal-cuff__0'), listrow('roleP', 'role-necklace__1')])
    return ''.join([
        strip('Final weekend · 30% off ends Sun 23:59 CET'), bar(v),
        bigtimer([('02', 'Days'), ('05', 'Hours'), ('59', 'Minutes')], 'Final weekend · the sale ends in',
                 'Sunday Dec 6, 23:59 CET. After that, it’s full price.'),
        cta('Shop before Sunday'),
        ph(f'Hero · full bleed · {"W · layered necklaces, warm light" if W else "M · stacked wrist, warm light"} · 600×440', cls='full'),
        '<div class="sec">', msh('Still on your list?', '30% off'), ''.join(rows), '</div>',
        f'<div class="newcard">{ph("Matte Cuff", cls="nc")}<div><span class="lab">New this week</span><h4>The Matte Cuff</h4>'
        '<p class="small mute">Full price, €39.95. Pairs with everything above, and counts toward the case.</p></div></div>',
        cta('Shop before Sunday'),
        foot()])

# ---------------------------------------------------------------- 13 · last day poster (red type, right)
def e13(v):
    W = v == 'W'
    key, image = ('crystalN', 'crystal-necklace__0') if W else ('set3', '3x-minimal-stack-set__0')
    name, p = P[key]
    pair = ([img('crystal-necklace__5'), img('cuban-necklace-1__1')] if W else
            [img('3x-minimal-stack-set__1'), img('minimal-cuff__3')])
    return ''.join([
        rstrip('Last day · 30% off ends 23:59 CET'),
        poster('Last day', '30% off ends tonight',
               f'Hero · B&W · {"W · necklace close-up" if W else "M · Set close-up"} · 600×700', pos='mid', ratio='600/700'),
        timer('Time left', [('13', 'H'), ('59', 'M'), ('00', 'S')], 'Ends tonight, Sun Dec 6, 23:59 CET'),
        '<div class="under"><h3 class="close">Once it ends, it ends.</h3>'
        '<p class="copy">30% off everything until 23:59 CET tonight. Tomorrow, prices go back to normal.</p></div>',
        cta('Shop the last day'),
        f'<div class="one"><img src="{img(image)}" alt="{name}"><div><span class="lab">The one to get</span>'
        f'<h3>{name}</h3><p class="small">Waterproof, adjustable, 316L stainless steel.</p>'
        f'{price_html(key)}<p class="save">You save {eur(round(p - sale(p), 2))}{" · case included" if not W else ""}</p></div></div>',
        f'<div class="pair"><img src="{pair[0]}" alt=""><img src="{pair[1]}" alt=""></div>',
        spec([('Everything', '30% off'), ('Any Set or two pieces', 'Jewelry case included'), ('Ends', 'Tonight, 23:59 CET')]),
        cta('Shop the last day'),
        foot()])

# ---------------------------------------------------------------- text-only fixes
t07 = g.textmail([
    'Hi {first name},',
    'A quick note from me, not a campaign.',
    'Everything on cavaier.com is 30% off until Sunday, December 6. It comes off at checkout, no code.',
    'If I had to pick three:',
    f'– The 3x Minimal Set. Three bracelets, worn together or apart. With the jewelry case included, it’s the best value we have. {g.L("See the Set")}<br>'
    f'– The Minimal Cuff. The one I never take off. €24.43 this week. {g.L("See the Cuff")}<br>'
    f'– The new Matte Cuff. It launched yesterday at full price, and it goes with everything. {g.L("See the Matte Cuff")}',
    'Everything is waterproof and made from 316L stainless steel. Shower, gym, sleep: it stays on.',
    g.L('Shop the sale →'),
    'Eli<br>Cavaier'])

t11 = g.textmail([
    'Hi {first name},',
    'The question we get most: “Can I really wear it all the time?”',
    'Yes. That’s the whole point. We make every piece from 316L stainless steel, so it’s waterproof, sweat-proof and heat-proof. '
    'Shower, swim, train, sleep. It stays on, and it doesn’t tarnish.',
    'And every bracelet, cuff and necklace adjusts, so it sits right on you, not just on the size chart.',
    '2,179 people have reviewed us on Trustpilot. The average is 4.5 out of 5.',
    f'You have three days left at 30% off. {g.L("Shop the sale →")}',
    'Eli<br>Cavaier'])

FN = {'01': e01, '02': e02, '03': e03, '04': e04, '05': e05, '06': e06, '08': e08, '10': e10, '12': e12, '13': e13}
for s in g.SENDS:
    if s['n'] in FN:
        s['fn'] = FN[s['n']]
    if s['n'] == '07':
        s['text'] = t07
    if s['n'] == '11':
        s['text'] = t11
        s['job'] = 'Answer the quality doubt directly: material, waterproofing, fit and reviews.'

EXTRA_CSS = """
/* ---- v2: accent + distinct layouts ---- */
:root{--red:#C2371A}
.strip.red{color:var(--red)}
.lab.red{color:var(--red)}
.poster{position:relative}
.poster .ph{background:repeating-linear-gradient(135deg,#D9D9D7 0 12px,#CFCFCD 12px 24px)}
.poster .pt{position:absolute;left:30px;top:22%;color:var(--red);display:flex;flex-direction:column;gap:2px;pointer-events:none}
.poster.lower .pt{top:auto;bottom:16%}
.poster.mid .pt{top:auto;bottom:34%;left:36px}
.poster .pk{margin:0 0 14px;font:400 12px/1 var(--wm);letter-spacing:.08em;text-transform:uppercase}
.poster .pk.r{position:absolute;right:30px;bottom:calc(16% + 6px);color:var(--red);margin:0}
.poster h2{margin:0;font:500 46px/1 var(--body);letter-spacing:.02em;text-transform:uppercase}
.poster .ps{margin:2px 0 0;font:300 30px/1.1 var(--body);letter-spacing:.03em;text-transform:uppercase}
.under{padding:30px 40px 0;text-align:center;display:flex;flex-direction:column;gap:12px;align-items:center}
.under .copy{max-width:380px}
.under .close{margin:0;font:300 30px/1.1 var(--disp);letter-spacing:-.02em}
.poster + .timer{margin-top:24px}

.invite{padding:44px 24px 30px;display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center}
.invite .wm{font-size:24px;margin-bottom:14px}
.invite h2{margin:0;font:300 38px/1.08 var(--disp);letter-spacing:-.02em}
.ph.portrait{aspect-ratio:4/5;margin:0 64px}
.letter{margin:30px auto 0;max-width:380px;text-align:center;font:300 15px/1.65 var(--body);padding:0 24px}

.split{display:grid;grid-template-columns:264px 1fr;gap:24px;padding:30px 24px 0;align-items:stretch}
.split .sp{aspect-ratio:3/4}
.split .st{display:flex;flex-direction:column;gap:12px;justify-content:center;min-width:0}
.split h2{margin:0;font:300 28px/1.08 var(--disp);letter-spacing:-.02em}
.vt{display:flex;gap:22px;margin-top:6px}
.vt div{display:flex;flex-direction:column;gap:4px}
.vt b{font:300 40px/1 var(--disp);font-variant-numeric:tabular-nums}
.split .ulink{margin-top:6px}
.feature{margin-top:44px}
.feature img{aspect-ratio:600/480}
.feature .fc{display:flex;justify-content:space-between;align-items:flex-end;gap:16px;padding:16px 24px 0}
.feature .fc div{display:flex;flex-direction:column;gap:6px}
.feature h3{margin:0;font:300 24px/1.1 var(--disp);letter-spacing:-.02em}

.ledger{margin:6px 24px 0}
.ledger .lh{display:grid;grid-template-columns:1fr 84px 84px;gap:12px;padding:0 0 10px 88px;border-bottom:1px solid var(--black);font:500 9.5px/1.4 var(--body);letter-spacing:.18em;text-transform:uppercase;color:var(--grey)}
.ledger .lh span:not(:first-child){text-align:right}
.ledger .lr{display:grid;grid-template-columns:76px 1fr 84px 84px;gap:12px;align-items:center;padding:14px 0;border-bottom:1px solid var(--line);text-decoration:none}
.ledger .lr img{aspect-ratio:1/1}
.ledger h4{margin:0 0 4px;font:400 13.5px/1.3 var(--body)}
.ledger .now{text-align:right;font:400 14px/1 var(--body);font-variant-numeric:tabular-nums}
.ledger .sv{text-align:right;font:300 22px/1 var(--disp);font-variant-numeric:tabular-nums;letter-spacing:-.01em}
.ledger + .pair{padding-top:30px}

.bigproof{padding:48px 24px 40px;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center}
.bigproof b{font:300 112px/.9 var(--disp);letter-spacing:-.05em}

.launch{padding:48px 24px 30px;text-align:center;display:flex;flex-direction:column;gap:12px;align-items:center}
.launch h2{margin:0;font:300 44px/1.02 var(--disp);letter-spacing:-.03em}
.launch .copy{max-width:340px}
.stage{background:var(--fog);padding:40px 0}
.stage .prod{aspect-ratio:1/1;margin:0 80px;background:repeating-linear-gradient(135deg,#E3E3E1 0 12px,#DADAD8 12px 24px)}
.details{display:grid;grid-template-columns:1fr 1fr;margin:0 24px;border-bottom:1px solid var(--line)}
.details div{padding:18px 0 16px;border-top:1px solid var(--line);display:flex;flex-direction:column;gap:4px}
.details div:nth-child(even){padding-left:18px;border-left:1px solid var(--line)}
.details .num{font:300 12px/1 var(--disp);color:var(--grey)}
.details p{margin:0;font:300 16px/1.3 var(--disp)}
.launchp{display:flex;flex-direction:column;align-items:center;gap:8px;padding:30px 24px 0;text-align:center}
.launchp .pr{font:300 30px/1 var(--disp);letter-spacing:-.01em}
.launchp + .mcta{padding-top:22px}

.btimer{padding:48px 24px 0;display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center}
.btimer .bt{display:flex;gap:30px}
.btimer .bt div{display:flex;flex-direction:column;gap:6px;align-items:center}
.btimer .bt b{font:300 76px/.9 var(--disp);letter-spacing:-.03em;color:var(--red);font-variant-numeric:tabular-nums}
.btimer + .mcta{padding-top:28px;padding-bottom:40px}
@media (max-width:480px){
  .poster h2{font-size:34px}.poster .ps{font-size:22px}
  .split{grid-template-columns:1fr}
  .ph.portrait{margin:0 24px}
  .ledger .lh{display:none}.ledger .lr{grid-template-columns:64px 1fr auto}.ledger .sv{display:none}
  .stage .prod{margin:0 40px}
  .btimer .bt b{font-size:56px}
}
"""

if __name__ == '__main__':
    tpl_path = os.path.join(g.HERE, 'bfcm26.tpl.html')
    tpl = open(tpl_path).read()
    if '/* ---- v2:' not in tpl:
        tpl = tpl.replace('</style>', EXTRA_CSS + '</style>', 1)
    tpl = tpl.replace('The discount never grows. The pressure does: deadlines appear, subject lines get shorter, the audience gets warmer and Eli starts writing in person.',
                      'The discount never grows. The pressure does: deadlines appear, subject lines get shorter, the audience gets warmer and Eli starts writing in person. Every designed email has its own layout, and the red (#C2371A) appears only where the holiday needs to be seen: the poster headlines, the launch label and the final countdown.')
    open(tpl_path, 'w').write(tpl)
    html = g.build()
    with cf.ThreadPoolExecutor(10) as ex:
        data = dict(ex.map(g.fetch, sorted(g.USED)))
    uri = {k: 'data:image/jpeg;base64,' + base64.b64encode(v).decode() for k, v in data.items()}
    html = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: uri[m.group(1)], html)
    assert 'warrant' not in html.lower(), 'warranty mention left'
    out = os.path.join(g.HERE, 'cavaier-bfcm26-sequence.html')
    open(out, 'w').write(html)
    print(len(g.USED), 'images,', len(html) // 1024, 'KB')
