#!/usr/bin/env python3
"""Generates the Cavaier BFCM26 campaign mock-up page (14 sends, W/M versions)."""
import base64, io, json, os, re, urllib.request, concurrent.futures as cf
from html import escape
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
URLS = json.load(open(os.path.join(HERE, 'img2urls.json')))
CACHE = os.path.join(HERE, 'imgcache26')
os.makedirs(CACHE, exist_ok=True)

# ---------------------------------------------------------------- products
def sale(p):
    return round(p * 0.7 + 1e-9, 2)

def eur(x):
    return f"€{x:,.2f}"

P = {  # name, regular EUR price (converted from the store's SEK list)
    'set3':     ('3x Minimal Set', 94.95),
    'set4':     ('4x Stacked Set', 89.95),
    'set2':     ('2x Duo Minimal Set', 59.95),
    'cuff':     ('Minimal Cuff', 34.90),
    'crystalN': ('Crystal Necklace', 89.95),
    'crystalB': ('Crystal Bracelet', 39.95),
    'braid':    ('Braid Bracelet', 39.95),
    'roleP':    ('Role Pendant Necklace', 39.95),
    'ropeP':    ('Rope Pendant Necklace', 39.95),
    'cubeP':    ('Cube Pendant Necklace', 39.95),
    'cubanN':   ('Cuban Necklace', 34.90),
    'ropeB':    ('Rope Bracelet', 29.95),
    'cubeB':    ('Cube Bracelet', 29.95),
    'roleB':    ('Role Bracelet', 29.95),
    'cubanB':   ('Cuban Bracelet', 29.95),
}

USED = set()

def img(key):
    USED.add(key)
    return '{{IMG:' + key + '}}'

# ---------------------------------------------------------------- modules
def strip(text):
    return f'<div class="strip">{text}</div>'

def bar(v):
    nav = ['Women', 'Necklaces', 'Bracelets'] if v == 'W' else ['Men', 'Bracelets', 'Sets']
    return ('<div class="mbar"><p class="wm">Cavaier</p><nav>' +
            ''.join(f'<span>{n}</span>' for n in nav) + '</nav></div>')

def ttl(label, h, copy, center=False):
    if center:
        return (f'<div class="mttl c"><span class="lab">{label}</span><h2>{h}</h2>'
                f'<p class="small">{copy}</p></div>')
    return (f'<div class="mttl"><div><span class="lab">{label}</span><h2>{h}</h2></div>'
            f'<p class="small">{copy}</p></div>')

def ph(label, cls='mhero', style=''):
    st = f' style="{style}"' if style else ''
    return f'<div class="ph {cls}"{st}><span>{label}</span></div>'

def msh(title, right=''):
    return f'<div class="msh"><h3>{title}</h3><span class="lab">{right}</span></div>'

def price_html(key, full=False):
    name, p = P[key]
    if full:
        return f'<div class="price"><span>{eur(p)}</span></div>'
    return f'<div class="price"><s>{eur(p)}</s><span>{eur(sale(p))}</span></div>'

def card(key, image, note='', ratio='sq'):
    name, p = P[key]
    n = f'<p class="small mute">{note}</p>' if note else ''
    return (f'<a class="mcard {ratio}" href="#"><img src="{img(image)}" alt="{name}">'
            f'<h4>{name}</h4>{n}{price_html(key)}</a>')

def grid(cards, cols=2):
    return f'<div class="grid g{cols}">' + ''.join(cards) + '</div>'

def spec(rows):
    return '<div class="spec">' + ''.join(f'<div><span>{a}</span><span>{b}</span></div>' for a, b in rows) + '</div>'

def icons():
    return ('<div class="icons"><span>Waterproof</span><span>316L stainless steel</span>'
            '<span>Lifetime warranty</span></div>')

def proof(big=False):
    q = ('<blockquote class="quote">“Paste one verified 5-star Trustpilot quote here, '
         'ideally about wearing it every day.”</blockquote>')
    cls = 'proof big' if big else 'proof'
    return (f'<div class="{cls}"><div class="score"><b>4.5</b><span>/ 5</span></div>'
            f'<p class="small">2,179 reviews on Trustpilot · Lifetime warranty on every piece</p>{q}</div>')

def timer(label, parts, fallback):
    cells = ''.join(f'<b>{n}<small>{u}</small></b>' for n, u in parts)
    return (f'<div class="timer"><span class="lab">{label}</span><div class="t">{cells}</div></div>'
            f'<p class="tfb">{fallback}</p>')

def cta(label, note=''):
    n = f'<p class="small mute">{note}</p>' if note else ''
    return f'<div class="mcta"><a class="solid" href="#">{label}</a>{n}</div>'

def ulink(label, align='end'):
    return f'<div class="mgo {align}"><a class="ulink" href="#">{label} <span>→</span></a></div>'

def offer_lock(label, sub):
    return (f'<div class="lock"><span class="lab">{label}</span>'
            f'<div class="big30"><b>30%</b><span>off<br>everything</span></div>'
            f'<p class="small">{sub}</p></div>')

def case_strip(text):
    return (f'<div class="casestrip"><img src="{img("jewelry-case__1")}" alt="Cavaier jewelry case">'
            f'<div><span class="lab">The jewelry case</span><p class="copy">{text}</p></div></div>')

def setrow(name, image, desc, regular, note):
    s = round(regular * 0.7 + 1e-9, 2)
    save = round(regular - s, 2)
    return (f'<div class="srow"><img src="{img(image)}" alt="{name}"><div class="t">'
            f'<h4>{name}</h4><p class="small mute">{desc}</p>'
            f'<div class="price"><s>{eur(regular)}</s><span>{eur(s)}</span></div>'
            f'<p class="save">You save {eur(save)} · {note}</p></div></div>')

def listrow(key, image, note=''):
    name, p = P[key]
    n = f'<p class="small mute">{note}</p>' if note else ''
    return (f'<a class="lrow" href="#"><img src="{img(image)}" alt="{name}"><div><h4>{name}</h4>{n}'
            f'{price_html(key)}</div><span class="arr">→</span></a>')

def tiles(items):
    out = '<div class="tiles">'
    for label, image, frm in items:
        out += (f'<a class="tile" href="#"><img src="{img(image)}" alt="{label}">'
                f'<div><h4>{label}</h4><span class="small mute">{frm}</span></div></a>')
    return out + '</div>'

def foot():
    ig = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="18" rx="5"/>'
          '<circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".9" fill="currentColor" stroke="none"/></svg>')
    tt = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round">'
          '<path d="M14 3v11.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 3c.4 2.6 2.2 4.4 5 4.7"/></svg>')
    fb = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round">'
          '<path d="M14.5 21v-8h2.7l.4-3.1h-3.1V8c0-.9.3-1.5 1.6-1.5h1.6V3.7a21 21 0 0 0-2.4-.1c-2.4 0-4 1.4-4 4.1v2.2H8.6V13h2.7v8"/></svg>')
    return (f'<footer class="foot"><div class="soc"><a href="#" aria-label="Instagram">{ig}</a>'
            f'<a href="#" aria-label="TikTok">{tt}</a><a href="#" aria-label="Facebook">{fb}</a></div>'
            '<a class="fb on" href="#">Shop all</a><a class="fb" href="#">Bracelets</a><a class="fb" href="#">Necklaces</a>'
            '<p class="fwm">Cavaier</p><p class="copy2">© Copyright 2026 Cavaier</p>'
            '<div class="legal"><span>Manage preferences</span><span>Unsubscribe</span></div></footer>')

PRE = 'Early access · BFCM26'
LIVE = 'Black Friday · 30% off sitewide'
CW = 'Cyber Week · 30% off sitewide'

# ---------------------------------------------------------------- designed emails
def e01(v):
    W = v == 'W'
    picks = ([card('crystalN', 'crystal-necklace__4'), card('braid', 'braid-armband-1__7'), card('cuff', 'minimal-cuff-1__0')]
             if W else
             [card('set3', '3x-minimal-stack-set__0'), card('cuff', 'minimal-cuff__0'), card('braid', 'braid-armband__0')])
    return ''.join([
        strip(PRE), bar(v),
        ttl('Subscribers only · Nov 23 – 26', 'Once a year, you go first.',
            '30% off everything, before the public sale. It comes off at checkout, no code needed.', center=True),
        ph(f'Hero · {"silver on skin, soft daylight" if W else "black on wrist, high contrast"} · 552×360'),
        spec([('Everything', '30% off'), ('Any Set', 'Jewelry case included'),
              ('Any two pieces', 'Jewelry case included'), ('Open to everyone', 'Fri Nov 27')]),
        '<div class="sec">', msh('Where to start', '03 pieces'), grid(picks, 3), '</div>',
        icons(),
        cta('Shop early access', 'Early access ends when the sale opens to everyone, Fri Nov 27 at 07:00 CET.'),
        foot()])

def e02(v):
    W = v == 'W'
    if W:
        feature = setrow('3x Minimal Set', '3x-minimal-stack-set-1__2', 'Three bracelets, worn together or apart.', 94.95, 'case included')
        pair = [card('cubanN', 'cuban-necklace-1__1', ratio='tall'), card('crystalB', 'bracelet__3', ratio='tall')]
    else:
        feature = setrow('3x Minimal Set', '3x-minimal-stack-set__1', 'Three bracelets, worn together or apart.', 94.95, 'case included')
        pair = [card('set2', '2x-duo-minimal-set__0', ratio='tall'), card('cuff', 'minimal-cuff__3', ratio='tall')]
    return ''.join([
        strip(PRE), bar(v),
        ttl('Early access · 2 days left', 'Choose once. Wear it every day.',
            'Our most-worn pieces, 30% off before the public sale on Friday.'),
        ph(f'Hero · full bleed · {"necklace and bracelet worn together" if W else "Set on wrist, coastal light"} · 600×440', cls='full'),
        timer('Early access ends in', [('01', 'D'), ('21', 'H'), ('59', 'M')], 'Public sale opens Fri Nov 27, 07:00 CET'),
        '<div class="sec">', msh('The Set', 'Best value'), feature, '</div>',
        '<div class="sec">', msh('Or pair two', 'Case included'), grid(pair, 2), '</div>',
        case_strip('Any Set, or any two pieces, comes with the jewelry case. Ready to keep or give.'),
        cta('Shop early access'),
        foot()])

def e03(v):
    W = v == 'W'
    best = ([card('crystalN', 'crystal-necklace__5', ratio='tall'), card('roleP', 'role-necklace-1__2', ratio='tall'),
             card('cubeB', 'cube-bracelet-1__1', ratio='tall'), card('cuff', 'minimal-cuff-1__3', ratio='tall')]
            if W else
            [card('set3', '3x-minimal-stack-set__2', ratio='tall'), card('cuff', 'minimal-cuff__1', ratio='tall'),
             card('roleB', 'role-bracelet__1', ratio='tall'), card('ropeP', 'rope-necklace__1', ratio='tall')])
    return ''.join([
        strip(LIVE), bar(v),
        ph(f'Hero · full bleed · {"editorial portrait, silver necklace" if W else "editorial, black Set on wrist"} · 600×520', cls='full tallh'),
        offer_lock('Black Friday · Nov 27 – Dec 6', 'Once a year. Applied automatically at checkout, no code needed.'),
        cta('Shop the sale'),
        spec([('Everything', '30% off'), ('Any Set or two pieces', 'Jewelry case included'), ('Gift cards', 'Not included')]),
        '<div class="sec">', msh('Best sellers', '04 pieces'), grid(best, 2), '</div>',
        proof(),
        cta('Shop Black Friday'),
        foot()])

def e04(v):
    W = v == 'W'
    if W:
        rows = [setrow('3x Minimal Set', '3x-minimal-stack-set-1__1', 'Three bracelets in one.', 94.95, 'case included'),
                setrow('Crystal Necklace + Crystal Bracelet', 'crystal-necklace__1', 'Make your own Set: any two pieces.', 129.90, 'case included'),
                setrow('Cuban Necklace + Braid Bracelet', 'braid-armband-1__4', 'Make your own Set: any two pieces.', 74.85, 'case included')]
        hero = 'Hero · W · Set and necklace layered on skin'
    else:
        rows = [setrow('3x Minimal Set', '3x-minimal-stack-set__3', 'Three bracelets, worn together or apart.', 94.95, 'case included'),
                setrow('4x Stacked Set', 'stacked-set__0', 'Four bracelets, one stack.', 89.95, 'case included'),
                setrow('2x Duo Minimal Set', '2x-duo-minimal-set__1', 'Two bracelets. The easy start.', 59.95, 'case included')]
        hero = 'Hero · M · three Sets side by side, black'
    return ''.join([
        strip(LIVE), bar(v),
        ttl('Black Friday · the Sets', 'Buy the Set once.',
            'The biggest saving is in the Sets: 30% off, and every Set comes with the jewelry case.'),
        ph(hero + ' · 552×360'),
        ulink('Shop the Sets'),
        '<div class="sec">', msh('The Sets', '30% off + case'), *rows, '</div>',
        '<div class="casebox"><img src="' + img('jewelry-case__0') + '" alt="Jewelry case"><div>'
        '<span class="lab">Included with every Set</span><h4>The jewelry case</h4>'
        '<p class="small mute">€19.95 value. Soft, structured, snaps shut.</p></div></div>',
        cta('Shop the Sets', 'Or add any two pieces and the case is included too.'),
        foot()])

def e05(v):
    W = v == 'W'
    if W:
        two = img('cube-necklace-1__3'); hero = 'Hero · W · close-up, pendant on skin'
        picks = [card('ropeP', 'rope-necklace-1__3'), card('braid', 'braid-armband-1__3'), card('cubanN', 'cuban-necklace-1__3')]
    else:
        two = img('braid-armband__1'); hero = 'Hero · M · close-up, bracelet on wrist'
        picks = [card('roleB', 'role-bracelet__3'), card('cubeP', 'cube-necklace__3'), card('cubanB', 'cuban-bracelet__1')]
    return ''.join([
        strip(LIVE), bar(v),
        ttl('Black Friday · day one', 'The pieces people never take off.',
            'Worn in the shower, at the gym, to sleep. Now 30% off.', center=True),
        proof(big=True),
        f'<div class="duo2">{ph(hero, cls="dhero")}<img src="{two}" alt="Worn every day"></div>',
        '<div class="sec">', msh('Most loved', '03 pieces'), grid(picks, 3), '</div>',
        icons(),
        cta('Shop most loved', '30% off until Dec 6 · Jewelry case with any Set or two pieces'),
        foot()])

def e06(v):
    W = v == 'W'
    pair = ([card('crystalB', 'bracelet__5', ratio='tall'), card('ropeB', 'rope-bracelet-2__3', ratio='tall')] if W else
            [card('braid', 'braid-armband__3', ratio='tall'), card('roleB', 'role-bracelet__5', ratio='tall')])
    return ''.join([
        strip('New · the Matte Cuff &nbsp;·&nbsp; 30% off everything else'), bar(v),
        ph(f'Hero · Matte Cuff macro · {"on skin, daylight" if W else "on wrist, high contrast"} · 600×600', cls='full sqh'),
        ttl('New · Nov 28', 'The Matte Cuff.', 'Our Minimal Cuff, in a matte finish. Same fit, softer light.'),
        spec([('Finish', 'Matte'), ('Material', '316L stainless steel'), ('Size', 'Adjustable'),
              ('Wear it', 'Water, gym, sleep'), ('Price', '€39.95')]),
        cta('Shop the Matte Cuff', 'New arrival at full price. Not part of the Black Friday offer.'),
        f'<div class="duo2 pad">{ph("Matte Cuff · packshot", cls="dhero sq")}{ph("Matte Cuff · worn", cls="dhero sq")}</div>',
        '<div class="sec">', msh('Wear it with', '30% off'), grid(pair, 2), '</div>',
        case_strip('Matte Cuff plus any other piece makes two, so the jewelry case is included.'),
        ulink('Shop Black Friday weekend', 'center'),
        '<div style="height:52px"></div>',
        foot()])

def e08(v):
    W = v == 'W'
    t = ([('Bracelets', 'cube-bracelet-1__3', 'from €20.97'), ('Necklaces', 'role-necklace-1__1', 'from €24.43'),
          ('Cuffs', 'minimal-cuff-1__5', 'from €24.43'), ('Sets', '3x-minimal-stack-set-1__0', 'from €66.47')] if W else
         [('Bracelets', 'cube-bracelet__1', 'from €20.97'), ('Necklaces', 'role-necklace__3', 'from €24.43'),
          ('Cuffs', 'minimal-cuff__5', 'from €24.43'), ('Sets', 'stacked-set__0', 'from €41.97')])
    return ''.join([
        strip(CW), bar(v),
        ttl('Cyber Week · Nov 30 – Dec 6', 'Cyber Week. Seven days left.',
            'Still 30% off everything. On Sunday at midnight, prices go back to normal.'),
        timer('Sale ends in', [('06', 'D'), ('16', 'H'), ('59', 'M')], 'Ends Sun Dec 6, 23:59 CET'),
        ph(f'Hero · {"W · necklace, Cyber Week mood" if W else "M · wrist, Cyber Week mood"} · 552×360', style='margin-top:26px'),
        ulink('Shop Cyber Week'),
        '<div class="sec">', msh('Shop by category', '30% off'), tiles(t), '</div>',
        cta('Shop Cyber Week', 'Jewelry case included with any Set or two pieces.'),
        foot()])

def e10(v):
    W = v == 'W'
    if W:
        u25 = [card('cubanN', 'cuban-necklace-1__5'), card('cuff', 'minimal-cuff-1__5'), card('ropeB', 'rope-bracelet-2__1')]
        u30 = [card('roleP', 'role-necklace-1__6'), card('braid', 'braid-armband-1__4'), card('crystalB', 'bracelet__1')]
        big = setrow('Crystal Necklace', 'crystal-necklace__1', '55 cm, our statement piece.', 89.95, 'add any piece for the case')
    else:
        u25 = [card('cuff', 'minimal-cuff__5'), card('cubanB', 'cuban-bracelet__3'), card('roleB', 'role-bracelet__3')]
        u30 = [card('ropeP', 'rope-necklace__3'), card('cubeP', 'cube-necklace__1'), card('braid', 'braid-armband__5')]
        big = setrow('3x Minimal Set', '3x-minimal-stack-set__4', 'The full Set, case included.', 94.95, 'case included')
    def sec(n, t, cards):
        return (f'<div class="sec"><div class="sh"><span class="num">{n}</span><span class="t">{t}</span></div>'
                + grid(cards, 3) + '</div>')
    return ''.join([
        strip(CW), bar(v),
        ttl('Cyber Week · gift guide', 'Gifts, by price.', 'Prices shown with 30% already taken off. Every piece is adjustable, so size is never a guess.'),
        ph(f'Hero · gift moment, case in hand · {"W" if W else "M"} · 552×260', style='aspect-ratio:552/260'),
        sec('01', 'Under €25', u25),
        sec('02', 'Under €30', u30),
        f'<div class="sec"><div class="sh"><span class="num">03</span><span class="t">The big one</span></div>{big}</div>',
        '<div class="giftrow"><img src="' + img('jewelry-case__0') + '" alt=""><div><span class="lab">Still not sure?</span>'
        '<h4>The gift card</h4><p class="small mute">€10 to €100, sent by email, valid 3 months. Not discounted.</p></div></div>',
        cta('Find a gift'),
        foot()])

def e12(v):
    W = v == 'W'
    rows = ([listrow('crystalN', 'crystal-necklace__4'), listrow('roleP', 'role-necklace-1__1'),
             listrow('crystalB', 'bracelet__5'), listrow('set3', '3x-minimal-stack-set-1__2', 'Jewelry case included')] if W else
            [listrow('set3', '3x-minimal-stack-set__1', 'Jewelry case included'), listrow('set4', 'stacked-set__0', 'Jewelry case included'),
             listrow('cuff', 'minimal-cuff__0'), listrow('roleP', 'role-necklace__1')])
    return ''.join([
        strip('Final weekend · 30% off ends Sun 23:59 CET'), bar(v),
        ttl('Final weekend', 'The last weekend at 30%.',
            'The sale ends Sunday at midnight. After that, it’s full price.', center=True),
        timer('Sale ends in', [('02', 'D'), ('05', 'H'), ('59', 'M')], 'Ends Sun Dec 6, 23:59 CET'),
        ph(f'Hero · full bleed · {"W · layered necklaces, warm light" if W else "M · stacked wrist, warm light"} · 600×440', cls='full', style='margin-top:26px'),
        '<div class="sec">', msh('Still on your list?', '30% off'), ''.join(rows), '</div>',
        f'<div class="newcard">{ph("Matte Cuff", cls="nc")}<div><span class="lab">New this week</span><h4>The Matte Cuff</h4>'
        '<p class="small mute">Full price, €39.95. Pairs with everything above, and counts toward the free case.</p></div></div>',
        cta('Shop before Sunday'),
        foot()])

def e13(v):
    W = v == 'W'
    key, image = ('crystalN', 'crystal-necklace__0') if W else ('set3', '3x-minimal-stack-set__0')
    name, p = P[key]
    pair = ([img('crystal-necklace__5'), img('cuban-necklace-1__1')] if W else
            [img('3x-minimal-stack-set__1'), img('minimal-cuff__3')])
    return ''.join([
        strip('Last day · 30% off ends 23:59 CET'), bar(v),
        ttl('Last day · Dec 6', 'Once it ends, it ends.',
            '30% off everything until 23:59 CET tonight. Tomorrow, prices go back to normal.'),
        timer('Time left', [('13', 'H'), ('59', 'M'), ('00', 'S')], 'Ends tonight, Sun Dec 6, 23:59 CET'),
        ph(f'Hero · {"W · necklace close-up" if W else "M · Set close-up"} · 552×360', style='margin-top:26px'),
        f'<div class="one"><img src="{img(image)}" alt="{name}"><div><span class="lab">The one to get</span>'
        f'<h3>{name}</h3><p class="small">Waterproof, 316L stainless steel, lifetime warranty.</p>'
        f'{price_html(key)}<p class="save">You save {eur(round(p - sale(p), 2))}{" · case included" if not W else ""}</p></div></div>',
        f'<div class="pair"><img src="{pair[0]}" alt=""><img src="{pair[1]}" alt=""></div>',
        spec([('Everything', '30% off'), ('Any Set or two pieces', 'Jewelry case included'), ('Ends', 'Tonight, 23:59 CET')]),
        cta('Shop the last day'),
        foot()])

# ---------------------------------------------------------------- text-only emails
def textmail(paras):
    body = ''.join(f'<p>{p}</p>' for p in paras)
    return f'<div class="tx"><div class="txhead"><b>Eli at Cavaier</b> &lt;eli@cavaier.com&gt;</div>{body}</div>'

L = lambda t: f'<a href="#">{t}</a>'

t07 = textmail([
    'Hi {first name},',
    'A quick note from me, not a campaign.',
    'Everything on cavaier.com is 30% off until Sunday, December 6. It comes off at checkout, no code.',
    'If I had to pick three:',
    f'– The 3x Minimal Set. Three bracelets, worn together or apart. With the jewelry case included, it’s the best value we have. {L("See the Set")}<br>'
    f'– The Minimal Cuff. The one I never take off. €24.43 this week. {L("See the Cuff")}<br>'
    f'– The new Matte Cuff. It launched yesterday at full price, and it goes with everything. {L("See the Matte Cuff")}',
    'Everything is waterproof, made from 316L stainless steel and covered by our lifetime warranty. Shower, gym, sleep: it stays on.',
    L('Shop the sale →'),
    'Eli<br>Cavaier'])

t09 = textmail([
    'Hi {first name},',
    'If you’re shopping for someone else this week, here’s what you need to know:',
    '<b>Size.</b> Every bracelet and cuff is adjustable, and necklaces have an extension chain. You don’t need to know their size.<br>'
    '<b>Wrapping.</b> Any Set, or any two pieces, comes with our jewelry case. It’s ready to give.<br>'
    '<b>Can’t decide?</b> Gift cards go from €10 to €100, arrive by email and are valid for 3 months. (They’re not part of the 30% off.)<br>'
    '<b>Delivery.</b> [CEO to confirm: holiday delivery cut-off]',
    f'30% off everything runs until Sunday at midnight. {L("Find a gift →")}',
    'Eli<br>Cavaier'])

t11 = textmail([
    'Hi {first name},',
    'The question we get most: “Can I really wear it all the time?”',
    'Yes. That’s the whole point. We make every piece from 316L stainless steel, so it’s waterproof, sweat-proof and heat-proof. '
    'Shower, swim, train, sleep. It stays on, and it doesn’t tarnish.',
    'If anything goes wrong, our lifetime warranty covers it.',
    '2,179 people have reviewed us on Trustpilot. The average is 4.5 out of 5.',
    f'You have three days left at 30% off. {L("Shop the sale →")}',
    'Eli<br>Cavaier'])

t14 = textmail([
    'Hi {first name},',
    'Four hours left.',
    'At 23:59 CET tonight, 30% off ends and prices go back to normal. The jewelry case with any Set or two pieces ends with it.',
    f'If something’s been sitting in your cart, now’s the time. {L("Shop the last hours →")}',
    'Eli<br>Cavaier'])

# ---------------------------------------------------------------- schedule
SENDS = [
    dict(n='01', date='Mon Nov 23', time='09:00', phase='Pre-sale', name='Early Access 1', fmt='Designed', heat=1,
         task='KA_W46_Nov23_EARLY_ACCESS_1', subj=('You go first this year', 'Early access starts now'),
         pre='30% off everything, three days before anyone else.', aud='Engaged 90 days + early-access pop-up list',
         job='Make subscribers feel first. Lead with access and the brand promise, not the sale.', fn=e01),
    dict(n='02', date='Wed Nov 25', time='09:00', phase='Pre-sale', name='Early Access 2', fmt='Designed', heat=2,
         task='KA_W46_Nov25_EARLY_ACCESS_2', subj=('Pick your Set before Friday', 'Two days before everyone else'),
         pre='Early access ends when the public sale opens.', aud='Engaged 90 days, not purchased since Nov 23',
         job='Help them choose. Introduce the Sets and the case, with the first real deadline.', fn=e02),
    dict(n='03', date='Fri Nov 27', time='07:00', phase='Black Friday', name='BFCM V1 · Launch', fmt='Designed', heat=3,
         task='KA_W46_Nov27_BFCM_V1', subj=('Black Friday: 30% off everything', 'It’s here. 30% off, once a year.'),
         pre='Applied at checkout. No code needed.', aud='Full list, engaged 180 days',
         job='The loudest email. The offer is unmissable, set in type, with best sellers right under it.', fn=e03),
    dict(n='04', date='Fri Nov 27', time='13:00', phase='Black Friday', name='BFCM V2 · The Sets', fmt='Designed', heat=3,
         task='KA_W46_Nov27_BFCM_V2', subj=('The Sets, 30% off, case included', 'Where you save the most today'),
         pre='The biggest saving of Black Friday is in the Sets.', aud='Engaged 180 days, not purchased today',
         job='Raise the order value. Show the saving in euros and the case.', fn=e04),
    dict(n='05', date='Fri Nov 27', time='20:00', phase='Black Friday', name='BFCM V3 · Most loved', fmt='Designed', heat=3,
         task='KA_W46_Nov27_BFCM_V3', subj=('The pieces people never take off', 'Rated 4.5/5. Now 30% off.'),
         pre='2,179 reviews on Trustpilot. 30% off until Dec 6.', aud='Engaged 90 days, not purchased today',
         job='Proof for the hesitant. Reviews and most-loved pieces close day one.', fn=e05),
    dict(n='06', date='Sat Nov 28', time='10:00', phase='BF weekend', name='Matte Cuff drop', fmt='Designed', heat=3,
         task='KA_W47_Nov28_BF WEEKEND + MATTE CUFF DROP', subj=('New: the Matte Cuff', 'Just landed: the Matte Cuff'),
         pre='Plus 30% off everything else, all weekend.', aud='Full list, engaged 180 days',
         job='A reason to open that isn’t the discount. Novelty lifts the weekend, and the case nudges a second piece.', fn=e06),
    dict(n='07', date='Sun Nov 29', time='11:00', phase='BF weekend', name='BF Weekend · from Eli', fmt='Text only', heat=3,
         task='EXTRA_KA_W47_Nov29_BF WEEKEND_TEXT ONLY', subj=('What I’d buy this weekend', 'a quick note'),
         pre='30% off runs until Dec 6. Here are my three picks.', aud='Engaged 60 days, not purchased since Nov 23',
         job='Personal, founder voice. Lands in Primary and breaks the pattern of designed sends.', text=t07),
    dict(n='08', date='Mon Nov 30', time='07:00', phase='Cyber Week', name='Cyber Week launch', fmt='Designed', heat=4,
         task='KA_W47_Nov30_CYBERWEEK_LAUNCH (CYBER MONDAY)', subj=('Cyber Week starts now', 'Seven days left at 30%'),
         pre='Still 30% off everything. Ends Sunday at midnight.', aud='Full list, engaged 180 days',
         job='Second launch. Reset attention with the real end date and fast category shopping.', fn=e08),
    dict(n='09', date='Tue Dec 1', time='11:00', phase='Cyber Week', name='Cyber Week 2 · gifting', fmt='Text only', heat=4,
         task='EXTRA_KA_W47_Dec01_CYBERWEEK_2_TEXT ONLY', subj=('Buying for someone? Read this first', 'gift questions, answered'),
         pre='Sizing, wrapping and gift cards, in 30 seconds.', aud='Engaged 60 days, not purchased since Nov 23',
         job='Remove gift friction: size, wrapping, gift card, delivery.', text=t09),
    dict(n='10', date='Wed Dec 2', time='09:00', phase='Cyber Week', name='Cyber Week 3 · gift guide', fmt='Designed', heat=4,
         task='KA_W47_Dec02_CYBERWEEK_3', subj=('Gifts from €20.97', 'The gift guide, by price'),
         pre='Sale prices, 30% already off. Every piece adjustable.', aud='Engaged 120 days',
         job='Make choosing easy. Price brackets turn browsing into a quick decision.', fn=e10),
    dict(n='11', date='Thu Dec 3', time='11:00', phase='Cyber Week', name='Cyber Week 4 · why it lasts', fmt='Text only', heat=4,
         task='EXTRA_KA_W47_Dec03_CYBERWEEK_4_TEXT ONLY', subj=('Shower, gym, sleep. It stays on.', 'the question we get most'),
         pre='Why we make it this way, and three days left at 30%.', aud='Engaged 60 days, clicked but not purchased',
         job='Answer the quality doubt directly, with the warranty and reviews.', text=t11),
    dict(n='12', date='Fri Dec 4', time='09:00', phase='Cyber Week', name='Cyber Week 5 · final weekend', fmt='Designed', heat=5,
         task='KA_W47_Dec04_CYBERWEEK_5', subj=('The last weekend at 30%', 'Ends Sunday at midnight'),
         pre='After Sunday, it’s full price.', aud='Engaged 120 days, not purchased since Nov 23',
         job='Turn the deadline on. Countdown in the hero area and a short list of top pieces.', fn=e12),
    dict(n='13', date='Sun Dec 6', time='09:00', phase='Last chance', name='Last Chance', fmt='Designed', heat=5,
         task='KA_W47_Dec06_LAST CHANCE', subj=('Last day: 30% off ends tonight', 'Once it ends, it ends'),
         pre='At 23:59 CET, prices go back to normal.', aud='Full list, engaged 180 days, not purchased since Nov 23',
         job='The close. One message, one product, one deadline.', fn=e13),
    dict(n='14', date='Sun Dec 6', time='20:00', phase='Last chance', name='Last Chance · from Eli', fmt='Text only', heat=5,
         task='EXTRA_KA_W47_Dec06_LAST CHANCE_TEXT ONLY', subj=('4 hours left', 'closing tonight'),
         pre='Then 30% off is gone.', aud='Clicked in the last 14 days, not purchased',
         job='Final nudge to the warmest non-buyers. Short and plain.', text=t14),
]

HEAT = {1: 'Warm-up', 2: 'Build', 3: 'Offer', 4: 'Push', 5: 'Final'}

# ---------------------------------------------------------------- page
def pips(h):
    return '<span class="pips" aria-label="Urgency ' + str(h) + ' of 5">' + ''.join(
        f'<i class="{"on" if i < h else ""}"></i>' for i in range(5)) + '</span>'

def build():
    rows, entries = [], []
    for s in SENDS:
        rows.append(f'<tr><td><a href="#e{s["n"]}">{s["n"]}</a></td><td>{s["date"]}<span class="tm">{s["time"]}</span></td>'
                    f'<td>{s["phase"]}</td><td>{s["name"]}</td><td>{s["fmt"]}</td><td>{pips(s["heat"])}</td>'
                    f'<td class="sj">{escape(s["subj"][0])}</td></tr>')
        if 'fn' in s:
            body = (f'<article class="em vW" aria-label="Email {s["n"]}, women">{s["fn"]("W")}</article>'
                    f'<article class="em vM" aria-label="Email {s["n"]}, men">{s["fn"]("M")}</article>')
        else:
            body = f'<article class="em txt" aria-label="Email {s["n"]}, text only">{s["text"]}</article>'
        entries.append(f'''
<section class="entry" id="e{s["n"]}">
  <div class="rail">
    <span class="no">{s["n"]}</span>
    <p class="d">{s["date"]}</p><p class="tm2">{s["time"]} CET</p>
    <p class="ph2">{s["phase"]}</p>
    {pips(s["heat"])}<p class="heat">{HEAT[s["heat"]]}</p>
  </div>
  <div class="main">
    <dl class="meta">
      <dt>Email</dt><dd><b>{s["name"]}</b> · {s["fmt"]}{" · W + M" if "fn" in s else ""}</dd>
      <dt>Subject A</dt><dd>{escape(s["subj"][0])}</dd>
      <dt>Subject B</dt><dd>{escape(s["subj"][1])}</dd>
      <dt>Preheader</dt><dd>{escape(s["pre"])}</dd>
      <dt>Audience</dt><dd>{s["aud"]}</dd>
      <dt>Job</dt><dd>{s["job"]}</dd>
      <dt>ClickUp</dt><dd class="mono">{s["task"]}</dd>
    </dl>
    {body}
  </div>
</section>''')
    tpl = open(os.path.join(HERE, 'bfcm26.tpl.html')).read()
    html = tpl.replace('%%ROWS%%', ''.join(rows)).replace('%%ENTRIES%%', ''.join(entries))
    return html

def fetch(key):
    path = os.path.join(CACHE, key + '.jpg')
    if os.path.exists(path):
        return key, open(path, 'rb').read()
    data = urllib.request.urlopen(URLS[key] + '&width=900', timeout=60).read()
    im = Image.open(io.BytesIO(data)).convert('RGB')
    im.thumbnail((640, 860))
    b = io.BytesIO(); im.save(b, 'JPEG', quality=64, optimize=True, progressive=True)
    open(path, 'wb').write(b.getvalue())
    return key, b.getvalue()

if __name__ == '__main__':
    html = build()
    with cf.ThreadPoolExecutor(10) as ex:
        data = dict(ex.map(fetch, sorted(USED)))
    uri = {k: 'data:image/jpeg;base64,' + base64.b64encode(v).decode() for k, v in data.items()}
    html = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: uri[m.group(1)], html)
    out = os.path.join(HERE, 'cavaier-bfcm26-sequence.html')
    open(out, 'w').write(html)
    print(len(USED), 'images,', len(html) // 1024, 'KB ->', out)
