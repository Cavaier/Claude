#!/usr/bin/env python3
"""Builds the first version of the BFCM26 flows master page (Version A, as briefed).

python3 gen_flows.py  ->  cavaier-bfcm26-flows.html

Run it ONCE to seed the shared page. After that the published artifact is the master:
edit the live page (Artifact read -> edit -> republish), never regenerate from here,
or Katrina's edits are lost.

Source: Cavaier_BFCM_2026_Flows_Simple_Brief.docx (14 emails, W + M) and the kickoff rules.
Each email row can carry several states (pre-sale / early access / live / Dec 6); the page
shows one state at a time (bar switch), and every state + W/M pair becomes its own Figma frame.
"""
import base64, io, json, os
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'cavaier-bfcm26-flows.html')

# ---------------------------------------------------------------- images
def src(name):
    for p in (f'imgcache26bw/{name}.jpg', f'imgcache26/{name}.jpg', f'figimg/{name}.png'):
        if os.path.exists(os.path.join(B, p)):
            return os.path.join(B, p)
    raise FileNotFoundError(name)

IMGS = {
    # heroes / lifestyle
    'hero_f0_M': 'fig_m_3x_set', 'hero_f0_W': 'fig_w_3x_set',
    'hero_f1_M': 'fig_m_wrist_close', 'hero_f1_W': 'fig_w_crossed',
    'hero_f13_M': 'fig_m_linen_chin', 'hero_f13_W': 'fig_w_black_top',
    'hero_f14_M': '3x-minimal-stack-set__1', 'hero_f14_W': '3x-minimal-stack-set-1__1',
    # products
    'set_M_black': '3x-minimal-stack-set__0', 'set_M_silver': '3x-minimal-stack-set__2',
    'set_W_black': '3x-minimal-stack-set-1__0', 'set_W_silver': '3x-minimal-stack-set-1__2',
    'set_M_cart': '3x-minimal-stack-set__3',
    'rope': 'rope-bracelet-2__3',
    'crystal_neck': 'crystal-necklace__1', 'cube_pend': 'cube-necklace__1',
    'cube_M': 'cube-bracelet__1', 'cube_W': 'cube-bracelet-1__1',
    'crystal_br': 'bracelet__1', 'braid_M': 'braid-armband__3', 'braid_W': 'braid-armband-1__3',
    'cuban_M': 'cuban-bracelet__1',
    'case': 'jewelry-case__0',
}
# Dynamic slots show what Klaviyo actually pulls: the Shopify product image, in colour
COLOR = {
    'dz_set_W': '3x-minimal-stack-set-1__0', 'dz_set_M': '3x-minimal-stack-set__0',
    'dz_crystal_neck': 'crystal-necklace__0', 'dz_braid_M': 'braid-armband__0', 'dz_braid_W': 'braid-armband-1__7',
    'dz_case': 'jewelry-case__0',
    'fd_W1': 'bracelet__0', 'fd_W2': 'braid-armband-1__7', 'fd_W3': 'crystal-necklace__4',
    'fd_M1': 'braid-armband__0', 'fd_M2': 'cuban-necklace-1__0', 'fd_M3': 'cube-necklace-1__0',
}
WIDE = {k for k in IMGS if k.startswith('hero')}

def enc(path, wide, color=False):
    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert('RGB')
    if not color: im = im.convert('L').convert('RGB')  # black and white, like the campaign
    w = 1000 if wide else 640
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=74, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()

def logo(i):
    return 'data:image/png;base64,' + base64.b64encode(open(os.path.join(HERE, f'logo{i}.png'), 'rb').read()).decode()

IMGDATA = {k: enc(src(v), k in WIDE) for k, v in IMGS.items()}
IMGDATA.update({k: enc(os.path.join(B, f'imgcache26/{v}.jpg'), False, True) for k, v in COLOR.items()})
IMGDATA['logo'] = logo(0)

def img(k, alt='', style='', cls=''):
    return f'<img data-k="{k}" alt="{alt}"' + (f' class="{cls}"' if cls else '') + (f' style="{style}"' if style else '') + '>'

def gimg(k, alt='', style='', cls=''):
    """W/M image pair: key k has _W and _M variants."""
    return (f'<span class="gW">{img(k+"_W", alt, style, cls)}</span>'
            f'<span class="gM">{img(k+"_M", alt, style, cls)}</span>')

# ---------------------------------------------------------------- copy helpers
STATES = ['pre', 'ea', 'live', 'd6']
SC = {'pre': 'sP', 'ea': 'sE', 'live': 'sL', 'd6': 'sD'}
SNAME = {'pre': 'Pre-sale', 'ea': 'Early access', 'live': 'Live', 'd6': 'Dec 6'}

def st(m, tag='span', cls=''):
    """m: {'pre': html, 'ea': html, 'live': html} -> one element per state. Keys may be 'ea live'."""
    out = []
    for k, v in m.items():
        c = ' '.join(SC[x] for x in k.split())
        out.append(f'<{tag} class="st {c}{" " + cls if cls else ""}">{v}</{tag}>')
    return ''.join(out)

def g(w, m, tag='span'):
    return f'<{tag} class="gW">{w}</{tag}><{tag} class="gM">{m}</{tag}>'

RED = 'var(--red)'
PROOF = '★★★★★ &nbsp;Rated 4.5 on Trustpilot · 3,000+ reviews'

# Static cards carry no fixed price: shoppers see prices in their own currency and the 30% only comes off
# at checkout, so a hard-coded € sale price would be wrong for most of the list. Dynamic blocks print the
# price Klaviyo receives. Sample figures below are Shopify's live EUR prices.
P = {
    'set': ('€94.95', '€66.47'), 'rope': ('€29.95', '€20.97'), 'cube': ('€29.95', '€20.97'),
    'crystal_br': ('€39.95', '€27.97'), 'braid': ('€39.95', '€27.97'), 'cuban': ('€29.95', '€20.97'),
    'crystal_neck': ('€89.95', '€62.97'), 'cube_pend': ('€39.95', '€27.97'),
}
def price(p=None, hide_pre=False):
    pr = '<span class="go red">30% off at checkout</span>'
    if hide_pre:
        return st({'pre': '<span class="go">From Nov 23 · 30% off</span>', 'ea live d6': pr})
    return pr

# ---------------------------------------------------------------- email modules
STRIP = {
    'pre': '<span class="rs">Early access</span> · Opens Nov 23',
    'ea': '<span class="rs">Early access</span> · 30% off is open',
    'live': '<span class="rs">30% off site-wide</span> · Until Dec 6',
    'd6': '<span class="rs">30% off site-wide</span> · Until Dec 6',
}
def strip(states):
    return '<div class="strip">' + st({k: STRIP[k] for k in states}) + '</div>'

def top():
    return f'<div class="etop">{img("logo", "Cavaier", "width:84px;height:14px", "logo")}</div>'

def foot():
    return ('<footer class="foot"><div class="soc">'
            '<a href="#" aria-label="Instagram"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".9" fill="currentColor" stroke="none"/></svg></a>'
            '<a href="#" aria-label="TikTok"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M14 3v11.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 3c.4 2.6 2.2 4.4 5 4.7"/></svg></a>'
            '<a href="#" aria-label="Facebook"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M14.5 21v-8h2.7l.4-3.1h-3.1V8c0-.9.3-1.5 1.6-1.5h1.6V3.7a21 21 0 0 0-2.4-.1c-2.4 0-4 1.4-4 4.1v2.2H8.6V13h2.7v8"/></svg></a></div>'
            '<div class="fnav"><a class="fb on" href="#">Shop all</a><a class="fb" href="#">Men</a><a class="fb" href="#">Women</a><a class="fb" href="#">Men’s Sets</a><a class="fb" href="#">Women’s Sets</a></div>'
            f'<p class="fwm">{img("logo", "Cavaier", "width:64px;height:10.7px", "logo")}</p>'
            '<p class="copy2">© Copyright 2026 Cavaier</p><div class="legal"><span>Manage preferences</span><span>Unsubscribe</span></div></footer>')

def lead(h, sub=None, lab=None, cta=None, center=True, big=False):
    c = ' c' if center else ''
    o = f'<div class="lead{c}">'
    if lab: o += f'<span class="lab red">{lab}</span>'
    o += ('<h2 class="xl">' if big else '<h2>') + f'{h}</h2>'
    if sub: o += f'<p class="copy sub">{sub}</p>'
    if cta: o += f'<a class="solid" href="#">{cta}</a>'
    return o + '</div>'

def cta(label, note=None, proof=False):
    o = f'<div class="mcta"><a class="solid" href="#">{label}</a>'
    if note: o += f'<p class="small mute">{note}</p>'
    if proof: o += f'<p class="mproof">{PROOF}</p>'
    return o + '</div>'

def line(left, right, mid=None):
    """Slim timeline: 'Today · x ——— ● date · y'. No countdowns."""
    o = '<div class="tline">' + f'<span class="a">{left}</span><i></i>'
    if mid:
        o += f'<b>●</b><span class="m">{mid}</span><i></i>'
    o += f'<b class="r">●</b><span class="z">{right}</span></div>'
    return o

def hdr(title, label):
    return f'<div class="sh"><h3>{title}</h3><span class="lab">{label}</span></div>'

def usps(*items):
    return '<div class="usp">' + ''.join(f'<span>{x}</span>' for x in items) + '</div>'

def offer_full(ends=True):
    rows = [('30% off site-wide', 'Applied at checkout, no code'),
            ('Shipping', 'Free on every order'),
            ('Two or more pieces', 'Jewelry case included')]
    if ends: rows.append(('Ends', 'Sun Dec 6, midnight'))
    return '<div class="spec offer">' + ''.join(f'<div><span>{a}</span><span>{b}</span></div>' for a, b in rows) + '</div>'

def offer_compact():
    return '<div class="obar"><span>30% off site-wide</span><span>No code</span><span>Case with 2+ pieces</span></div>'

def card(k, name, p, hide_pre=False, link='Shop', finish=None, gendered=False):
    im = gimg(k, name) if gendered else img(k, name)
    f = ''
    if finish:
        f = '<span class="fin">' + ''.join(f'<i class="{c}"></i>' for c in finish) + '</span>'
    return f'<a class="pc" href="#">{im}<h4>{name}</h4>{f}{price(p, hide_pre)}</a>'

def dyn(W, M, note, big=True):
    """Dynamic product block, drawn with a sample product. W/M = (image key, name, variant or '', price as Klaviyo prints it)."""
    cls = 'dyn big' if big else 'dyn'
    def side(x):
        k, n, v, pr = x
        return (f'<h4>{n}</h4>' + (f'<span class="small mute">{v}</span>' if v else '')
                + f'<span class="dp">{pr}</span><span class="go red">30% off at checkout</span>')
    return (f'<div class="{cls}"><a href="#" class="dimg">{g(img(W[0], W[1]), img(M[0], M[1]))}</a>'
            f'<div class="dt">{g(side(W), side(M), "div")}</div>'
            f'<p class="stand">{note}</p></div>')

def feed():
    """Klaviyo product block on a recommendation feed: catalog title + image, no prices (catalog is EUR only)."""
    def c(k, n): return f'<a class="pc" href="#">{img(k, n)}<h4>{n}</h4><span class="go red">30% off</span></a>'
    w = c('fd_W1', 'Crystal Bracelet') + c('fd_W2', 'Braid Bracelet') + c('fd_W3', 'Crystal Necklace')
    m = c('fd_M1', 'Braid Bracelet') + c('fd_M2', 'Cuban Necklace') + c('fd_M3', 'Cube Pendant Necklace')
    return '<div class="cards c3">' + g(w, m, 'div') + '</div>'


def quote(n=1, who=None):
    q = ('<div class="quote"><span class="bx-stars">★★★★★</span>'
         '<p>[Verified Trustpilot review, Katrina to pull]</p>'
         f'<span class="who">{who or "Name · Trustpilot"}</span></div>')
    return q * n

def order(compact=False):
    """Klaviyo table block repeating over event.extra.line_items. Sample cart in EUR; prices print in the shopper's currency.
    Line prices arrive before discounts; the 30% and the case show up in Total Discounts, and $value is the total."""
    def row(k, name, var, pr):
        return (f'<div class="or">{img(k, name)}<div><h4>{name}</h4><span class="small mute">{var} · Qty 1</span></div>'
                f'<span class="op">{pr}</span></div>')
    case = row('dz_case', 'Jewelry Case', 'Black', 'Included')
    w = row('dz_crystal_neck', 'Crystal Necklace', 'Black / 55 cm', '€89.90') + row('dz_braid_W', 'Braid Bracelet', 'Silver / Medium', '€39.90') + case
    m = row('dz_set_M', '3x Minimal Set', 'Black / Medium', '€94.90') + row('dz_braid_M', 'Braid Bracelet', 'Black / Medium', '€39.90') + case
    tot = (g('<div class="ot"><span>30% off + jewelry case</span><span class="red">−€58.84</span></div>',
             '<div class="ot"><span>30% off + jewelry case</span><span class="red">−€60.34</span></div>', 'div')
           + '<div class="ot"><span>Shipping</span><span>Free</span></div>'
           + g('<div class="ot tt"><span>Total</span><b>€90.86</b></div>',
               '<div class="ot tt"><span>Total</span><b>€94.36</b></div>', 'div'))
    return (f'<div class="order{" c" if compact else ""}"><div class="oh"><span>Your order</span><span class="lab">Saved</span></div>'
            + g(w, m, 'div') + tot + '<p class="stand">Dynamic: Checkout Started line items, discounts and total, in the shopper’s currency</p></div>')

def em(body, fog=False):
    return f'<article class="em{" fog" if fog else ""}">{body}{foot()}</article>'

# ---------------------------------------------------------------- the 14 emails (Version A, as briefed)
E = []

def entry(no, flow, email, timing, live, wave, states, brief, html, angle):
    E.append(dict(no=no, flow=flow, email=email, timing=timing, live=live, wave=wave,
                  states=states, brief=brief, html=html, angle=angle))

# --- e01 · Flow 0 · You're In
entry('01', '0 · VIP Confirmation', '#1 You’re In', 'Immediately, on pre-sale pop-up submit', 'Oct 27 – Nov 26', 1, ['pre', 'ea'],
 [('Trigger', 'Pre-sale pop-up submit, new or existing subscribers'),
  ('Subject', st({'pre': 'You’re on the list.', 'ea': 'You’re on the list.'})),
  ('Preview', st({'pre': 'First access: Monday, Nov 23.', 'ea': 'Early access is open now.'})),
  ('Banner', st({'pre': 'EARLY ACCESS · OPENS NOV 23', 'ea': 'EARLY ACCESS · 30% OFF IS OPEN'})),
  ('Audience', 'W + M versions; neutral if gender unknown'),
  ('Goal', 'Confirm the spot, save the date. The calm one: no sale styling.'),
  ('Note', 'Signups during Nov 23–26 get the Early access state. One hero image, no product grid. No countdown: a timeline line instead. Preview text in the early-access state is ours (brief gives none): check it.')],
 em(strip(['pre', 'ea']) + top()
    + lead(st({'pre': 'You’re In.', 'ea': 'You’re In.<br>Access Is Open.'}),
           st({'pre': 'Early access opens Monday, Nov 23 — before the public sale.',
               'ea': 'You can shop now — before the public sale on Friday.'}), lab='Early access')
    + f'<div class="pic">{gimg("hero_f0", "3x Minimal Set on the wrist", "aspect-ratio:552/440;object-position:center 40%")}</div>'
    + st({'pre': line('Today · On the list', 'Fri 27 · Everyone', 'Mon 23 · You'),
          'ea': line('Today · You’re in', 'Fri 27 · Everyone')}, 'div')
    + '<div class="ticket"><div><span class="lab">Opens</span><b>'
    + st({'pre': 'Mon 23', 'ea': 'Now'}) + '</b><span>November</span></div>'
      '<div><span class="lab">Your price</span><b class="r">30% off</b><span>site-wide</span></div>'
      '<div><span class="lab">Code</span><b>None</b><span>applied at checkout</span></div></div>'
    + cta(st({'pre': 'Save the date', 'ea': 'Shop early access'}),
          st({'pre': 'Adds Mon Nov 23 to your calendar.', 'ea': 'Early access ends when the sale opens to everyone on Fri Nov 27.'}))
    + '<div class="steps"><div><b>01</b><p>' + st({'pre': 'We email you when it opens.', 'ea': 'Access is open now.'})
    + '</p></div><div><b>02</b><p>You shop first, before the public sale.</p></div><div><b>03</b><p>Same 30% off, first pick.</p></div></div>'
    + '<p class="perks">Free shipping on every order · Jewelry case included with 2 or more pieces</p>'
    + '<div class="tlink"><a class="ulink" href="#">Browse the Sets <span>→</span></a></div>'
    + f'<p class="mproof c">{PROOF}</p><div style="height:36px"></div>'),
 'Early Access')

# --- e02 · Flow 1 · #1 Why Cavaier
F1_STATES = ['pre', 'ea', 'live']
entry('02', '1 · Welcome', '#1 Why Cavaier', '1 hour after signup', 'Oct 27 – Dec 6', 1, F1_STATES,
 [('Trigger', 'New subscribers via the BFCM pop-up · exits on Placed Order'),
  ('Subject', 'Jewelry that stays on.'), ('Preview', 'Shower, gym, sleep. Still on.'),
  ('Banner', st({'pre': 'EARLY ACCESS · OPENS NOV 23', 'ea': 'EARLY ACCESS · 30% OFF IS OPEN', 'live': '30% OFF SITE-WIDE · UNTIL DEC 6'})),
  ('Audience', 'W + M (M: black on-wrist · W: silver, soft daylight)'),
  ('Goal', 'Make them care before the sale: the daily-wear promise.'),
  ('Note', 'Module swap by date: pre-sale shows the promise line; early access and live show the full offer. Lifetime warranty removed from the icon row.')],
 em(strip(F1_STATES) + top()
    + f'<div class="pic full">{gimg("hero_f1", "Worn every day", "aspect-ratio:600/620;object-position:center 45%")}</div>'
    + lead('Put It On Once.<br>Live In It.', 'Minimal pieces made for real life — and never taken off.',
           cta=st({'pre': 'Discover the collection', 'ea live': 'Shop 30% off'}))
    + usps('100% waterproof', 'Stainless steel', 'Hypoallergenic')
    + '<div style="height:44px"></div>' + hdr('Start here', st({'pre': 'From Nov 23 · 30% off', 'ea live': '30% off'}))
    + '<div class="cards c2">' + card('set', '3x Minimal Set', 'set', True, gendered=True).replace('data-k="set_W"', 'data-k="set_W_silver"').replace('data-k="set_M"', 'data-k="set_M_black"')
    + card('rope', 'Rope Bracelet', 'rope', True) + '</div>'
    + st({'pre': '<p class="promise">You’ll get early access to 30% off on Nov 23.</p>',
          'ea live': offer_full()}, 'div')
    + f'<p class="mproof c" style="margin-top:28px">{PROOF}</p>'
    + cta(st({'pre': 'See the Sets', 'ea live': 'Shop the sale'}))),
 'Minimal Jewelry')

# --- e03 · Flow 1 · #2 The Set Line-Up
def finish_grid():
    return ('<div class="cards c2">'
            + f'<a class="pc" href="#">{gimg("set", "3x Minimal Set, black").replace("set_W", "set_W_black").replace("set_M", "set_M_black")}<h4>3x Minimal Set</h4><span class="fin"><i class="k on"></i><i class="s"></i><span>Black</span></span>{price("set", True)}</a>'
            + f'<a class="pc" href="#">{gimg("set", "3x Minimal Set, silver").replace("set_W", "set_W_silver").replace("set_M", "set_M_silver")}<h4>3x Minimal Set</h4><span class="fin"><i class="k"></i><i class="s on"></i><span>Silver</span></span>{price("set", True)}</a>'
            + f'<a class="pc" href="#">{img("rope", "Rope Bracelet")}<h4>Rope Bracelet</h4><span class="fin"><i class="k on"></i><i class="s"></i><span>Black</span></span>{price("rope", True)}</a>'
            + '<span class="gW">' + f'<a class="pc" href="#">{img("crystal_neck", "Crystal Necklace")}<h4>Crystal Necklace</h4><span class="fin"><i class="k on"></i><i class="s"></i><span>Black</span></span>{price("crystal_neck", True)}</a></span>'
            + '<span class="gM">' + f'<a class="pc" href="#">{img("cube_pend", "Cube Pendant Necklace")}<h4>Cube Pendant Necklace</h4><span class="fin"><i class="k on"></i><i class="s"></i><span>Black</span></span>{price("cube_pend", True)}</a></span>'
            + '</div>')

entry('03', '1 · Welcome', '#2 The Set Line-Up', '12 hours after Email 1', 'Oct 27 – Dec 6', 1, F1_STATES,
 [('Trigger', 'As Email 1'), ('Subject', 'Pick your Set first.'), ('Preview', 'Your Black Friday shortlist, sorted.'),
  ('Banner', st({'pre': 'EARLY ACCESS · OPENS NOV 23', 'ea': 'EARLY ACCESS · 30% OFF IS OPEN', 'live': '30% OFF SITE-WIDE · UNTIL DEC 6'})),
  ('Audience', 'W + M · W: Black Crystal Necklace / M: Cube Pendant Necklace as the 4th card'),
  ('Goal', 'Help them pick before access opens.'),
  ('Note', 'Pre-sale: no % in the hero, one line under the grid. From Nov 28 the last card becomes the Matte Cuff (“New”); no Matte Cuff photos yet. Say “Set”, never “Stack”.')],
 em(strip(F1_STATES) + top()
    + lead('Pick What Fits You.', 'Our best-selling Sets — ready to wear, ready to gift.', center=False,
           cta=st({'pre': 'See the Sets', 'ea live': 'Shop the Sets'}))
    + hdr('Best sellers', 'Black first') + finish_grid()
    + st({'pre': '<p class="promise">All of these are 30% off from Nov 23.</p>', 'ea live': ''}, 'div')
    + f'<div class="gift">{img("case", "Jewelry case")}<div><span class="lab red">Ready to gift</span><h4>Jewelry case included</h4><p class="small">With 2 or more pieces. Added at checkout.</p></div></div>'
    + cta('Shop the Sets', proof=True), fog=True),
 'Best Sellers — Sets')

# --- e04 · Flow 1 · #3 Access Open / Sale Live
entry('04', '1 · Welcome', '#3 Access Open / Sale Live', '1 day after Email 2', 'Oct 27 – Dec 6', 1, F1_STATES,
 [('Trigger', 'As Email 1'),
  ('Subject', st({'pre': 'Access opens Nov 23.', 'ea': 'Early access is open.', 'live': '30% off is live.'})),
  ('Preview', st({'pre': 'Mark it. You’re first in.', 'ea': 'Shop before the public sale.', 'live': 'Applied automatically at checkout.'})),
  ('Banner', st({'pre': 'EARLY ACCESS · OPENS NOV 23', 'ea': 'EARLY ACCESS · 30% OFF IS OPEN', 'live': '30% OFF SITE-WIDE · UNTIL DEC 6'})),
  ('Audience', 'W + M'), ('Goal', 'The loudest Welcome email: get the first order.'),
  ('Note', 'Three states. Pre-sale is new: the old copy said “open” to people signing up weeks early. Pre-sale cards carry no prices. From Nov 28 include the Matte Cuff.')],
 em(strip(F1_STATES) + top()
    + st({'pre': '<div class="lock"><span class="lab red">Early access</span><p class="big">Nov 23.</p><h2>You’re First.</h2>'
                 '<p class="copy sub">Early access opens Monday, Nov 23 — before everyone else.</p></div>',
          'ea': '<div class="lock"><span class="lab red">Early access</span><p class="big">30% Off.</p><h2>You’re First.</h2>'
                '<p class="copy sub">Members shop before the public sale on Friday.</p></div>',
          'live': '<div class="lock"><span class="lab red">Black Friday · Cyber Week</span><p class="big">30% Off</p><h2>Site-Wide.</h2>'
                  '<p class="copy sub">Every piece, every finish — until Sunday, Dec 6.</p></div>'}, 'div')
    + cta(st({'pre': 'Save the date', 'ea': 'Shop early access', 'live': 'Shop the sale'}))
    + f'<div class="pic full">{gimg("hero_f13", "", "aspect-ratio:600/480;object-position:center 35%")}</div>'
    + st({'pre': line('Today', 'Fri 27 · Everyone', 'Mon 23 · You'),
          'ea': line('Today · Members first', 'Fri 27 · Everyone'),
          'live': line('Today · 30% off', 'Sun Dec 6 · Midnight')}, 'div')
    + offer_full()
    + '<div style="height:44px"></div>' + hdr('Where to start', st({'pre': 'From Nov 23', 'ea live': '30% off · no code'}))
    + '<div class="cards c3">' + card('set', '3x Minimal Set', 'set', True, gendered=True).replace('set_W"', 'set_W_black"').replace('set_M"', 'set_M_black"')
    + card('rope', 'Rope Bracelet', 'rope', True)
    + g(card('crystal_neck', 'Crystal Necklace', 'crystal_neck', True), card('cube_pend', 'Cube Pendant Necklace', 'cube_pend', True)) + '</div>'
    + cta(st({'pre': 'Save the date', 'ea': 'Shop early access', 'live': 'Shop the sale'}), proof=True)),
 'Limited Time')

# --- e05 · Flow 1 · #4 Last Call
entry('05', '1 · Welcome', '#4 Last Call', '3 days after Email 3', 'Oct 27 – Dec 6', 1, F1_STATES,
 [('Trigger', 'As Email 1'),
  ('Subject', st({'pre': 'Your access opens soon.', 'ea': 'Early access ends Friday.', 'live': 'Last call: 30% off.'})),
  ('Preview', st({'pre': 'Nov 23. Shop before everyone.', 'ea': 'Then it opens to everyone.', 'live': 'Ends Sunday, Dec 6.'})),
  ('Banner', st({'pre': 'EARLY ACCESS · OPENS NOV 23', 'ea': 'EARLY ACCESS · 30% OFF IS OPEN', 'live': '30% OFF SITE-WIDE · UNTIL DEC 6'})),
  ('Audience', 'W + M'), ('Goal', 'Final push on a real deadline.'),
  ('Note', '“Sale of the year” and “neither will your size” removed: unprovable. Deadline always in live text. From Nov 28: Matte Cuff option as the hero product (no photos yet).')],
 em(strip(F1_STATES) + top()
    + lead(st({'pre': 'Almost Time.', 'ea': 'Last Call for<br>Early Access.', 'live': 'Last Call.'}),
           st({'pre': 'Early access opens Monday, Nov 23. Your list is ready.', 'ea': 'On Friday it opens to everyone.',
               'live': '30% off site-wide ends Sunday, Dec 6 at midnight.'}), big=True)
    + f'<div class="ovl">{gimg("hero_f14", "3x Minimal Set", "aspect-ratio:600/560;object-position:center 50%")}'
      f'<a class="ovc" href="#"><span class="lab red">Best seller</span><h4>3x Minimal Set</h4>{price("set", True)}'
      '<span class="fin"><i class="k on"></i><i class="s"></i><span>Black · Silver</span></span></a></div>'
    + '<div class="dlx">' + st({'pre': '<span>Opens</span><b>Mon Nov 23</b>', 'ea': '<span>Early access ends</span><b>Fri Nov 27</b>',
                                'live': '<span>Ends</span><b>Sun Dec 6, midnight</b>'}) + '</div>'
    + cta(st({'pre': 'See the Sets', 'ea': 'Shop before Friday', 'live': 'Shop before it ends'}))
    + quote() + offer_full(ends=False)
    + cta(st({'pre': 'See the Sets', 'ea': 'Shop before Friday', 'live': 'Shop before it ends'}), proof=True)),
 'Real deadline')

# --- Flow 2 · Browse
LIVE = ['live']
VIEW_W = ('dz_set_W', '3x Minimal Set', '', '€94.90')
VIEW_M = ('dz_set_M', '3x Minimal Set', '', '€94.90')
def dyn_view(big=True):
    return dyn(VIEW_W, VIEW_M, 'Dynamic: Viewed Product name, image and price (shopper’s currency)', big)

entry('06', '2 · Browse', '#1 Still Looking?', '4 hours after viewed product', 'Nov 27 – Dec 6', 2, LIVE,
 [('Trigger', 'Viewed product, no add to cart · exits: Added to Cart, Started Checkout, Placed Order'),
  ('Subject', 'Still thinking about it?'), ('Preview', 'It’s 30% off right now.'), ('Banner', '30% OFF SITE-WIDE · UNTIL DEC 6'),
  ('Audience', 'W + M, driven by the viewed product'), ('Goal', 'Bring them back to the piece. Lightest touch, no scarcity.'),
  ('Note', 'From Nov 28 the Matte Cuff can be one of the 3 related pieces.')],
 em(strip(LIVE) + top() + lead('Made to Stay On.', 'The piece you looked at is 30% off — shower, gym, all of it.')
    + dyn_view() + cta('See it at 30% off')
    + usps('100% waterproof', 'Stainless steel', 'Rated 4.5 on Trustpilot') + offer_compact()
    + '<div style="height:44px"></div>' + hdr('You might also like', '30% off')
    + feed()
    + '<p class="stand">Dynamic: Klaviyo product block on a recommendation feed, 3 items</p>'
    + '<div class="tlink" style="padding-bottom:48px"><a class="ulink" href="#">Take another look <span>→</span></a></div>'),
 'Product Spotlight')

entry('07', '2 · Browse', '#2 Worth It', '1 day after Email 1', 'Nov 27 – Dec 6', 2, LIVE,
 [('Trigger', 'As Email 1'), ('Subject', 'Worth a second look.'), ('Preview', 'Rated 4.5 on Trustpilot.'),
  ('Banner', '30% OFF SITE-WIDE · UNTIL DEC 6'), ('Audience', 'W + M'), ('Goal', 'Reassure with proof, give a reason to act during the sale.'),
  ('Note', 'Lifetime warranty removed from the icon row. Quote: verified Trustpilot only.')],
 em(strip(LIVE) + top()
    + '<div class="score"><span class="bx-stars">★★★★★</span><b>4.5</b><span class="lab">Trustpilot · 3,000+ reviews</span></div>'
    + lead('Worth It. Ask Them.', 'Rated 4.5 on Trustpilot from 3,000+ reviews — and still 30% off.')
    + dyn_view(big=False) + quote()
    + usps('Waterproof', 'Hypoallergenic', 'Adjustable size')
    + '<div class="dlx"><span>30% off ends</span><b>Sun Dec 6, midnight</b></div>'
    + '<p class="perks">Free shipping on every order</p>'
    + cta('Get it at 30% off')
    + '<div class="tlink" style="padding-bottom:48px"><a class="ulink" href="#">Back to your piece <span>→</span></a></div>', fog=True),
 'Customer Stories')

# --- Flow 3 · Add to cart
CART_W = ('dz_crystal_neck', 'Crystal Necklace', 'Black / 55 cm', '€89.90')
CART_M = ('dz_braid_M', 'Braid Bracelet', 'Black / Medium', '€39.90')
def dyn_cart(big=True):
    return dyn(CART_W, CART_M, 'Dynamic: Added to Cart name, finish/size, image and price (shopper’s currency)', big)

entry('08', '3 · Add to Cart', '#1 Saved For You', '2 hours after added to cart', 'Nov 27 – Dec 6', 2, LIVE,
 [('Trigger', 'Added to cart, no checkout · exits: Started Checkout, Placed Order'),
  ('Subject', 'Still in your cart.'), ('Preview', '30% off already applied.'), ('Banner', '30% OFF SITE-WIDE · UNTIL DEC 6'),
  ('Audience', 'W + M, driven by the cart item'), ('Goal', 'One tap back to the cart.'), ('Note', 'Short email.')],
 em(strip(LIVE) + top() + lead('Still Yours.', 'We saved your pick — 30% comes off automatically at checkout.')
    + dyn_cart() + cta('Return to cart') + offer_compact() + '<div style="height:48px"></div>'),
 'Reminder')

entry('09', '3 · Add to Cart', '#2 Why It Lasts', '12 hours after Email 1', 'Nov 27 – Dec 6', 2, LIVE,
 [('Trigger', 'As Email 1'), ('Subject', 'Made to stay on.'), ('Preview', 'Waterproof. Adjustable. Worn daily.'),
  ('Banner', '30% OFF SITE-WIDE · UNTIL DEC 6'), ('Audience', 'W + M'), ('Goal', 'Answer the doubts: quality, fit, delivery.'),
  ('Note', '“Lifetime warranty” and the unconfirmed “Easy exchanges” tiles replaced with product-page facts.')],
 em(strip(LIVE) + top()
    + lead('Why It Lasts.', 'Stainless steel, 100% waterproof and hypoallergenic — made to be worn, not stored.', center=False)
    + dyn_cart(big=False)
    + '<div class="tiles3"><div><b>01</b><h4>Free shipping</h4><p>On every order.</p></div><div><b>02</b><h4>Adjustable size</h4><p>Fits your wrist.</p></div><div><b>03</b><h4>100% waterproof</h4><p>Shower, sea, gym.</p></div></div>'
    + quote() + cta('Back to my cart')
    + '<div class="tlink" style="padding-bottom:48px"><a class="ulink" href="#">Check out at 30% off <span>→</span></a></div>'),
 'Materials & Craft')

entry('10', '3 · Add to Cart', '#3 Before It Ends', '1 day after Email 2', 'Nov 27 – Dec 6', 2, LIVE,
 [('Trigger', 'As Email 1'), ('Subject', 'Your cart, 30% off.'), ('Preview', 'Until Sunday, Dec 6, midnight.'),
  ('Banner', '30% OFF SITE-WIDE · UNTIL DEC 6'), ('Audience', 'W + M'), ('Goal', 'Last call on the real sale deadline.'),
  ('Note', '“Black Friday ends soon” removed: the sale runs through Cyber Week to Dec 6. Deadline in live text, hero position.')],
 em(strip(LIVE) + top()
    + '<div class="lock"><span class="lab red">Your cart · 30% off</span><p class="big">Sun Dec 6</p><h2>Before It Ends.</h2>'
      '<p class="copy sub">Your cart is 30% off until Sunday, Dec 6 at midnight. After that, full price.</p></div>'
    + line('Today · 30% off', 'Sun Dec 6 · Midnight') + dyn_cart() + offer_full(ends=False)
    + cta('Check out now') , fog=True),
 'Limited Time')

# --- Flow 4 · Checkout
entry('11', '4 · Checkout', '#1 Finish Your Order', '1 h 15 min after started checkout', 'Nov 27 – Dec 6', 2, LIVE,
 [('Trigger', 'Started checkout, no order · exits: Placed Order'), ('Subject', 'One step left.'), ('Preview', 'Your 30% is already applied.'),
  ('Banner', '30% OFF SITE-WIDE · UNTIL DEC 6'), ('Audience', 'W + M'), ('Goal', 'Back to checkout in one tap.'),
  ('Note', 'Minimal. No product recommendations. CTA uses the Shopify recovery URL.')],
 em(strip(LIVE) + top() + lead('One Step Left.', 'Your order is saved, with 30% off already applied.')
    + order() + cta('Complete my order') + '<div style="height:12px"></div>'),
 'Direct reminder')

entry('12', '4 · Checkout', '#2 Delivery', '6 hours after Email 1', 'Nov 27 – Dec 6', 2, LIVE,
 [('Trigger', 'As Email 1'), ('Subject', 'Arrives before the holidays.'), ('Preview', 'Shipping’s on us. Always.'),
  ('Banner', '30% OFF SITE-WIDE · UNTIL DEC 6'), ('Audience', 'W + M'), ('Goal', 'Kill cost and delivery doubts.'),
  ('Note', 'No FREE in subject lines. Holiday delivery claim (“orders by Dec 6 arrive in time”) is unverified: CEO to confirm the cut-off before this goes live.')],
 em(strip(LIVE) + top()
    + lead('No Surprises<br>at Checkout.', 'Shipping is on us, and orders placed by Dec 6 arrive in time for the holidays.')
    + '<div class="spec"><div><span>Shipping</span><span>Free on every order</span></div><div><span>Holidays</span><span>Order by Dec 6</span></div><div><span>Checkout</span><span>Secure</span></div></div>'
    + '<p class="stand">To confirm: holiday delivery cut-off [CEO]</p>'
    + order(compact=True) + cta('Complete my order')),
 'Reassurance')

entry('13', '4 · Checkout', '#3 Loved by 3,000+', '1 day after Email 2', 'Nov 27 – Dec 6', 2, LIVE,
 [('Trigger', 'As Email 1'), ('Subject', 'Why they kept theirs.'), ('Preview', 'Rated 4.5 on Trustpilot.'),
  ('Banner', '30% OFF SITE-WIDE · UNTIL DEC 6'), ('Audience', 'W + M · testimonials gender-matched'), ('Goal', 'Trust: proof.'),
  ('Note', 'Renamed from “Loved by 2,000+”. Trustpilot badge replaces the old warranty badge.')],
 em(strip(LIVE) + top() + lead('Loved, Then<br>Worn Daily.', 'Rated 4.5 on Trustpilot from 3,000+ reviews.')
    + g(quote(2, 'Her name · Trustpilot'), quote(2, 'His name · Trustpilot'), 'div')
    + '<div class="score sm"><span class="bx-stars">★★★★★</span><b>4.5</b><span class="lab">Trustpilot · 3,000+ reviews</span></div>'
    + order(compact=True) + cta('Complete my order')),
 'Customer Stories')

entry('14', '4 · Checkout', '#4 Final Hours', '2 days after Email 3', 'Nov 27 – Dec 6', 2, ['live', 'd6'],
 [('Trigger', 'As Email 1 · suppress if the sale has ended'),
  ('Subject', st({'live': 'Your order’s still saved.', 'd6': 'Final hours at 30%.'})),
  ('Preview', st({'live': '30% off until Dec 6.', 'd6': 'Ends tonight at midnight.'})),
  ('Banner', '30% OFF SITE-WIDE · UNTIL DEC 6'), ('Audience', 'W + M'), ('Goal', 'The real deadline; last email before full price.'),
  ('Note', 'Two versions, split by send date in Klaviyo. “After tonight, full price” is only true on Dec 6. Switch the bar to “Dec 6” to see it.')],
 em(strip(['live', 'd6']) + top()
    + lead(st({'live': 'Still Saved<br>for You.', 'd6': 'Final Hours.'}),
           st({'live': 'Your 30% stays applied until Sunday, Dec 6.', 'd6': 'After tonight, it’s full price.'}), big=True)
    + '<div class="dlx">' + st({'live': '<span>30% off until</span><b>Sun Dec 6, midnight</b>', 'd6': '<span>Ends</span><b>Tonight, midnight</b>'}) + '</div>'
    + order(compact=True) + cta('Complete my order', 'Questions? Reply to this email.')),
 'Limited Time')


# ---------------------------------------------------------------- how each email is built in Klaviyo
C = lambda t: f'<code>{t}</code>'
DATE = 'Date modules switch by themselves: ' + C("{% today '%Y-%m-%d' as d %}") + ' (before 2026-11-23 pre-sale, before 2026-11-27 early access, then live).'
GEN = 'W/M: show/hide on ' + C("person|lookup:'Gender'") + ' (“Men” → M, else W).'
SET = C("|find_replace:'Stack Set|Set'")
VIEW = ('Trigger: Viewed Product (metric HtsYBH) · filter: no Added to Cart, Checkout Started or Placed Order since. '
        'Block fields: ' + C('event.ProductName') + SET + ', ' + C('event.ImageURL') + ', ' + C('event.Price') +
        ' (already text in the shopper’s currency), ' + C('event.URL') + '.')
CART = ('Trigger: Shopify “Added to Cart” (WBpdcS), not the API metric of the same name (silent since Sep 2) · filter: no Checkout Started or Placed Order since. '
        'Fields: ' + C("event|lookup:'Product Name'") + SET + ', ' + C('event.ImageURL') + ', ' + C("event|lookup:'Variant Name'") + ', ' +
        C('event.Price') + ' + ' + C("event|lookup:'$currency'") + '. One item: the one they added.')
CHK = ('Trigger: Shopify “Checkout Started” (LrhH24), not the API “Started Checkout” (no names or images) · filter: no Placed Order since. '
       'Table block repeating over ' + C('event.extra.line_items') + ': ' + C('item.product.variant.images.0.src') + ', ' + C('item.title') + SET + ', ' +
       C('item.variant_title') + ', ' + C('item.quantity') + ', ' + C('item.line_price') + ' + ' + C('event.extra.presentment_currency') +
       '; the Jewelry Case row prints “Included”. Discount row ' + C("event|lookup:'Total Discounts'") + ', total ' + C("event|lookup:'$value'") +
       ', button ' + C('event.extra.responsive_checkout_url') + '.')
WEL = 'Trigger: added to the BFCM pop-up list (form SyHM2E, source POPUP26) · exits on Placed Order. ' + DATE + ' ' + GEN + ' Product cards are static images and links, no prices.'
KB = {
 '01': 'Trigger: added to the BFCM pop-up list (form SyHM2E, source POPUP26), send immediately. ' + DATE.replace(', then live', '') + ' ' + GEN + ' Save the date: add-to-calendar link. No product data.',
 '02': WEL, '03': WEL, '04': WEL, '05': WEL,
 '06': VIEW + ' “You might also like”: product block on a recommendation feed filtered to ' + C('event.Categories') + ', 3 items, title and image only.',
 '07': VIEW, '08': CART, '09': CART, '10': CART,
 '11': CHK, '12': CHK + ' Compact table.', '13': CHK + ' Compact table. ' + GEN + ' for the two quotes.',
 '14': CHK + ' Compact table. Dec 6 copy: ' + C("{% if d == '2026-12-06' %}") + ', other days “Still Saved”. Turn the flow off on Dec 7 so nothing sends after the sale.',
}
for e in E: e['brief'].append(('Klaviyo', KB[e['no']]))

# ---------------------------------------------------------------- page
def rail(e):
    states = ' · '.join(SNAME[s] for s in e['states'])
    return (f'<div class="rail"><span class="no">{e["no"]}</span><p class="fl">Flow {e["flow"]}</p><p class="d">{e["email"]}</p>'
            f'<p class="tm2">{e["timing"]}</p><p class="ph2">Wave {e["wave"]} · {e["live"]}</p>'
            f'<p class="heat">States: {states}</p><p class="showing" aria-live="polite"></p></div>')

def brief_dl(e):
    rows = [('Flow', f'<b>Flow {e["flow"]} · {e["email"]}</b>'), ('Timing', e['timing']), ('Live', f'{e["live"]} · Wave {e["wave"]}'),
            ('Angle', e['angle'])] + e['brief']
    return '<dl class="meta">' + ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in rows) + '</dl>'

entries_html = ''
for e in E:
    entries_html += (f'<section class="entry" id="e{e["no"]}" data-states="{" ".join(e["states"])}" data-s="{e["states"][0]}">'
                     + rail(e) + '<div class="vtrack"><div class="main" data-ver="A">'
                     + '<div class="vtag"><b>Version A</b><span>as briefed</span></div>'
                     + brief_dl(e) + e['html'].replace('<article class="em', f'<article aria-label="Email {e["no"]}" class="em', 1)
                     + '</div></div></section>\n')

maprows = ''.join(f'<tr><td><a href="#e{e["no"]}">{e["no"]}</a></td><td>{e["flow"]}</td><td>{e["email"]}</td><td>{e["timing"]}</td>'
                  f'<td>{e["angle"]}</td><td>{e["live"]}</td><td>{e["wave"]}</td></tr>' for e in E)

PAGE_CSS = open(os.path.join(HERE, 'flows.css')).read()
LIVE_CSS = open(os.path.join(HERE, 'live_css.css')).read()
LIVE_JS = open(os.path.join(HERE, 'live_script.js')).read().replace("/^e\\d\\d$/.test(w)?'on '+w.slice(1)", "/^e\\d\\d$/.test(w)?'on '+w.slice(1)")

html = f'''<title>Cavaier BFCM26 Flows</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400&family=Figtree:wght@300;400;500&display=swap">
<style>
{PAGE_CSS}
{LIVE_CSS}
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
    <p class="hint">Everyone who has this page open shows up in the bar above, with the email they’re looking at. When anyone saves a change, this page reloads to it. Claude posts here when it starts and finishes a change, and says what changed where.</p>
    <form id="lvForm" autocomplete="off">
      <select id="lvKind" aria-label="Type"><option value="working">I’m working on</option><option value="waiting">Waiting for Claude</option><option value="note">Note</option></select>
      <input id="lvText" maxlength="200" placeholder="e.g. Email 06 related pieces" aria-label="What">
      <button class="pb" type="submit">Post</button>
      <button class="pb ghost" type="button" id="lvClear">Clear my status</button>
    </form>
    <ol id="lvLog"><li><time></time><span class="hint">No activity yet.</span></li></ol>
  </div>
</div>
<div class="wrap" id="root" data-g="W">
  <header class="intro">
    <span class="kicker">BFCM26 · Klaviyo flows · Oct 27 – Dec 6</span>
    <h1>Cavaier BFCM26 flows</h1>
    <p>Five flows, 14 emails, each in a women’s (W) and a men’s (M) version, written to the BFCM 2026 Flows brief. One row per email: the brief card, then the email at 600px. Use the bar to switch W / M and the date state (pre-sale, early access, live, Dec 6): emails that change with the date show that state, the rest show the only state they run in. Version A is the brief as written, drawn the way Klaviyo will render it: dynamic blocks show sample products from the real Shopify events, and each brief card has a “Klaviyo” line with the trigger, fields and logic. More versions go to the right of A. Static photography from the campaign shoots, in black and white.</p>
  </header>

  <section class="card">
    <span class="kicker">How the flows run</span>
    <div class="arc">
      <div><b>Pre-sale</b><span>Oct 27 – Nov 22</span><span>VIP Confirmation · Welcome (pre-sale state) · regular Browse / Cart / Checkout · pre-sale pop-up</span></div>
      <div><b>Early access</b><span>Nov 23 – Nov 26</span><span>VIP Confirmation · Welcome (early access state) · regular abandonment flows · pre-sale pop-up (signups get instant access)</span></div>
      <div><b>Live</b><span>Nov 27 – Dec 6, midnight</span><span>Welcome (live state) · BFCM Browse / Cart / Checkout (regular ones set to Manual) · on-sale pop-up</span></div>
      <div><b>After</b><span>From Dec 7</span><span>Regular flows back on (clear Needs Review first) · BFCM flows off</span></div>
    </div>
    <p class="notes">Wave 1 (Flows 0–1 + pre-sale pop-up): ready Tue Oct 20, live Tue Oct 27. Wave 2 (Flows 2–4 + on-sale pop-up): ready Fri Nov 20, live Fri Nov 27. Offer: 30% off site-wide, automatic, no code · free shipping on every order · jewelry case included with 2+ pieces · ends Sun Dec 6 at midnight, recipient-local.</p>
  </section>

  <div class="tbl"><table><thead><tr><th>#</th><th>Flow</th><th>Email</th><th>Timing</th><th>Angle</th><th>Live</th><th>Wave</th></tr></thead><tbody>{maprows}</tbody></table></div>

  <section class="card">
    <span class="kicker">Rules for every flow email</span>
    <div class="rules">
      <div><b>Copy</b>Subject lines 3–4 words, previews 4–5 words. Never “FREE” in subjects, previews, banners or headlines; the case is “included”. Say “Set”, never “Stack”.</div>
      <div><b>Claims</b>No lifetime warranty anywhere. Rating line: “Rated 4.5 on Trustpilot · 3,000+ reviews” (re-check on build day). Testimonials: verified Trustpilot only.</div>
      <div><b>Deadlines</b>No countdown timers: sends are recipient-local and the sale ends at each subscriber’s midnight. The deadline goes in live text, with a slim timeline line.</div>
      <div><b>Look</b>White and fog, Figtree, black only on buttons, thin hairlines, red only on the banner label, sale prices and dots. No dark sections, no text over photos.</div>
      <div><b>Build</b>600px, mobile-first, 16px body, live text for offer, dates, names, prices and CTAs, bulletproof buttons, dark-mode logo, under ~90KB.</div>
      <div><b>Footer</b>Logo · Men / Women / Men’s Sets / Women’s Sets / Shop All · social · copyright · unsubscribe.</div>
    </div>
  </section>

  <section class="card" id="build">
    <span class="kicker">Built for Klaviyo</span>
    <ul class="levers">
      <li><b>Checked on your Klaviyo account</b> (test template rendered, then deleted): the <code>today</code> tag for the date switch, <code>find_replace</code> to print “3x Minimal Set” instead of Shopify’s “3x Minimal Stack Set”, the loop over checkout line items, and the <code>Gender</code> profile lookup.</li>
      <li><b>Triggers.</b> Browse: Viewed Product. Cart: Shopify “Added to Cart” (the API one stopped on Sep 2). Checkout: Shopify “Checkout Started” (the API “Started Checkout” has no names or images). Each email’s Klaviyo line lists the exact fields.</li>
      <li><b>Prices.</b> No fixed prices in static cards: shoppers see their own currency (recent events: EUR, AUD, QAR, SGD) and the 30% comes off at checkout. Dynamic blocks print the price Klaviyo receives with “30% off at checkout” under it; checkout emails show the real discount line and total.</li>
      <li><b>Images.</b> Dynamic slots show the Shopify product image (colour), as Klaviyo will. Static sections use the campaign photos, uploaded to Klaviyo.</li>
      <li><b>Email-safe.</b> No overlapping layers, gradients or shadows; the timeline is a hairline with glyph dots; buttons are bulletproof table buttons. Figtree loads in Apple Mail; Gmail and Outlook fall back to Helvetica/Arial.</li>
      <li><b>W/M.</b> Profiles carry <code>Gender</code> = Women / Men from the pop-up; when it’s missing the email falls back to W.</li>
    </ul>
  </section>

  <section class="card" id="open">
    <span class="kicker">Open items</span>
    <ul class="levers">
      <li><b>Date switch timezone.</b> Check in a Klaviyo preview which timezone the <code>today</code> tag uses (account vs recipient) before Nov 23.</li>
      <li><b>Testimonials.</b> Every quote is a placeholder until Katrina pulls verified Trustpilot reviews (Emails 05, 07, 09, 13).</li>
      <li><b>Holiday delivery.</b> Email 12 says orders by Dec 6 arrive for the holidays: CEO to confirm the cut-off.</li>
      <li><b>Matte Cuff.</b> “From Nov 28” swaps (Emails 03, 04, 05, 06) are noted in the brief cards, not drawn: there are no Matte Cuff photos yet and it isn’t in the store.</li>
      <li><b>Neutral version.</b> Flow 0 asks for a neutral version when gender is unknown. Not drawn yet: W is the fallback for now.</li>
      <li><b>Black-led palette.</b> Read as the jewelry and photography being black-led, not black backgrounds (no dark sections). Red sits on the banner label, prices and dots only.</li>
      <li><b>Pop-ups.</b> The two pop-ups (Task 15) are already on Figma’s “Email Flow” page; not on this page yet.</li>
    </ul>
  </section>

  <div class="bar2">
    <div class="ctl">
      <div class="seg" role="group" aria-label="Women or men"><button type="button" data-g="W" aria-pressed="true">W</button><button type="button" data-g="M" aria-pressed="false">M</button></div>
      <div class="seg" role="group" aria-label="Date state"><button type="button" data-s="pre" aria-pressed="true">Pre-sale</button><button type="button" data-s="ea" aria-pressed="false">Early access</button><button type="button" data-s="live" aria-pressed="false">Live</button><button type="button" data-s="d6" aria-pressed="false">Dec 6</button></div>
    </div>
    <div class="ctl">
      <div class="seg vpick" role="group" aria-label="Show versions"><span class="lbl">Show</span><button type="button" data-v="A" aria-pressed="true">A</button></div>
      <select class="jump" id="jump" aria-label="Jump to email"><option value="">Jump to…</option></select>
    </div>
  </div>

{entries_html}
</div>
<script type="application/json" id="imgs">{json.dumps(IMGDATA)}</script>
<script>
(function(){{
  var I=JSON.parse(document.getElementById('imgs').textContent);
  document.querySelectorAll('img[data-k]').forEach(function(im){{var s=I[im.getAttribute('data-k')];if(s)im.src=s}});
  var root=document.getElementById('root');
  var NAME={{pre:'Pre-sale',ea:'Early access',live:'Live',d6:'Dec 6'}};
  var g='W',s='pre',on=['A'];
  try{{g=localStorage.getItem('flows-g')||g;s=localStorage.getItem('flows-s')||s;var v=JSON.parse(localStorage.getItem('flows-v')||'null');if(Array.isArray(v)&&v.length)on=v}}catch(e){{}}
  function eff(states,want){{
    if(states.indexOf(want)>=0)return want;
    if(want==='d6'&&states.indexOf('live')>=0)return 'live';
    if((want==='live'||want==='d6')&&states.indexOf('ea')>=0)return 'ea';
    if((want==='pre'||want==='ea')&&states.indexOf('live')>=0)return 'live';
    return states[0];
  }}
  function apply(){{
    root.setAttribute('data-g',g);
    document.querySelectorAll('.entry').forEach(function(e){{
      var states=e.getAttribute('data-states').split(' '),x=eff(states,s);e.setAttribute('data-s',x);
      var p=e.querySelector('.showing');p.textContent='Showing: '+NAME[x]+(x!==s?' (runs '+states.map(function(k){{return NAME[k]}}).join(' / ')+' only)':'');
    }});
    document.querySelectorAll('[data-g][aria-pressed]').forEach(function(b){{b.setAttribute('aria-pressed',String(b.getAttribute('data-g')===g))}});
    document.querySelectorAll('button[data-s]').forEach(function(b){{b.setAttribute('aria-pressed',String(b.getAttribute('data-s')===s))}});
    document.querySelectorAll('.vtrack>[data-ver]').forEach(function(c){{c.hidden=on.indexOf(c.getAttribute('data-ver'))<0}});
    document.querySelectorAll('.vpick button').forEach(function(b){{b.setAttribute('aria-pressed',String(on.indexOf(b.getAttribute('data-v'))>=0))}});
    try{{localStorage.setItem('flows-g',g);localStorage.setItem('flows-s',s);localStorage.setItem('flows-v',JSON.stringify(on))}}catch(e){{}}
  }}
  document.querySelectorAll('button[data-g]').forEach(function(b){{b.addEventListener('click',function(){{g=b.getAttribute('data-g');apply()}})}});
  document.querySelectorAll('button[data-s]').forEach(function(b){{b.addEventListener('click',function(){{s=b.getAttribute('data-s');apply()}})}});
  document.querySelectorAll('.vpick button').forEach(function(b){{b.addEventListener('click',function(){{
    var v=b.getAttribute('data-v'),i=on.indexOf(v);if(i>=0){{if(on.length>1)on.splice(i,1)}}else{{on.push(v);on.sort()}}apply()}})}});
  var j=document.getElementById('jump');
  document.querySelectorAll('.entry').forEach(function(e){{var o=document.createElement('option');o.value=e.id;
    o.textContent=e.querySelector('.no').textContent+' · Flow '+e.querySelector('.fl').textContent.replace('Flow ','')+' · '+e.querySelector('.d').textContent;j.appendChild(o)}});
  j.addEventListener('change',function(){{if(j.value){{document.getElementById(j.value).scrollIntoView();j.value=''}}}});
  window.flowsView=function(G,S){{g=G;s=S;apply()}};
  apply();
}})();
</script>
<script>{LIVE_JS}</script>
'''
open(OUT, 'w').write(html)
print('wrote', OUT, len(html) // 1024, 'KB,', len(E), 'emails')
