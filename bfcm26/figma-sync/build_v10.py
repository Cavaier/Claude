"""Build the v10 master: 20 sends (picks only) from the current A–J page + the v10 brief."""
import re, html as H
SRC = 'v10_base.html'; OUT = 'master_v10.html'
h = open(SRC).read()

# ---------- helpers: find articles and resolve shared images ----------
def sec_span(eid):
    s = h.find(f'<section class="entry" id="{eid}"'); e = h.find('<section', s + 10)
    return s, (len(h) if e < 0 else e)
def article(eid, ver):
    s, e = sec_span(eid)
    k = h.find(f'data-ver="{ver}"', s, e); a = h.find('<article', k, e); b = h.find('</article>', a) + 10
    return h[a:b]
def imgs_of(eid):
    s, e = sec_span(eid); a = h.find('<article', s, e); b = h.find('</article>', a); A = h[a:b]; out = []
    for m in re.finditer(r'<img([^>]*)>', A):
        c = re.search(r'class="([^"]*)"', m.group(1))
        if c and 'logo' in c.group(1).split(): continue
        out.append(re.search(r'src="([^"]+)"', m.group(1)).group(1))
    return out
_cache = {}
def src(ref):
    eid, n = ref.split(':')
    if eid not in _cache: _cache[eid] = imgs_of(eid)
    return _cache[eid][int(n)]
s01, e01 = sec_span('e01'); A01 = h[h.find('<article', s01):h.find('</article>', h.find('<article', s01))]
FOOT = re.search(r'<footer class="foot".*?</footer>', A01, re.S).group(0)
LOGO = re.search(r'<img class="logo" src="([^"]+)"', FOOT).group(1)
LOGOW = re.search(r'<img class="logo" src="([^"]+)"', A01).group(1)  # white logo in the 01-A hero
def resolve(a):
    a = re.sub(r'data-img="(e\d\d:\d+)"', lambda m: f'src="{src(m.group(1))}"', a)
    a = a.replace('data-logo="w"', f'src="{LOGOW}"').replace('data-logo', f'src="{LOGO}"')
    a = a.replace('<footer class="foot" data-foot></footer>', FOOT)
    return a
def rep(a, pairs):
    for old, new in pairs:
        assert a.count(old) == 1, ('not unique/absent', old[:80], a.count(old))
        a = a.replace(old, new)
    return a
LAB = 'font:500 10px/1.4 var(--body);letter-spacing:.2em;text-transform:uppercase'
def strip(red, rest):
    return f'<div class="strip" style="background:#0B0B0B;color:#FFFFFF;border-bottom:0"><span class="rs" style="color:#FFFFFF">{red}</span> · {rest}</div>'
def top(): return f'<div class="cx-top"><img class="logo" src="{LOGO}" alt="Cavaier" style="width:80px!important;height:13.4px"></div>'
def line(left, right):
    return (f'<div style="display:flex;align-items:center;gap:12px;margin:30px 24px 0;font:500 10px/1 var(--body);letter-spacing:.18em;text-transform:uppercase">'
            f'<span style="color:#0B0B0B">{left}</span><span style="flex:1;height:1px;background:linear-gradient(to right,#0B0B0B,#CFCFCC)"></span>'
            f'<span style="width:9px;height:9px;border-radius:50%;background:var(--red);flex:none"></span><span style="color:#8B8B88">{right}</span></div>')
def card(ref, name, was, now, extra=''):
    return f'<a class="bx-p" href="#"><img src="{src(ref)}" alt="{name}"><h4>{name}</h4><span class="price "><s>{was}</s><span>{now}</span></span>{extra}</a>'
def hdr(t, r='30% off'): return f'<div class="bx-h"><h3>{t}</h3><span class="lab">{r}</span></div>'
USP = '<p class="mproof">Water-friendly · Stainless steel<br>★★★★★ &nbsp;Rated 4.5 on Trustpilot · 3,000+ reviews</p>'
def text_email(n, paras):
    body = ''.join(f'<p>{p}</p>' for p in paras)
    return (f'<article class="em txt" aria-label="Email {n:02d}, text only"><div class="tx"><div class="txhead"><b>Eli at Cavaier</b> &lt;eli@cavaier.com&gt;</div>'
            f'<p>Hi {{{{ first_name|default:"there" }}}},</p>{body}<p>— Eli</p></div></article>')

# ---------- the 20 sends ----------
S = []  # dicts: n, date, time, phase, urg, heat, versions=[(ver, tag, meta, article)]
def meta(email, fmt, subj, prev, banner, aud, angle, note, clickup):
    return (f'<dl class="meta"><dt>Email</dt><dd><b>{email}</b> · {fmt}</dd><dt>Subject</dt><dd>{subj}</dd><dt>Preview</dt><dd>{prev}</dd>'
            f'<dt>Banner</dt><dd>{banner}</dd><dt>Audience</dt><dd>{aud}</dd><dt>Angle</dt><dd>{angle}</dd><dt>Note</dt><dd>{note}</dd><dt>ClickUp</dt><dd class="mono">{clickup}</dd></dl>')
def add(n, date, time, phase, urg, heat, versions): S.append(dict(n=n, date=date, time=time, phase=phase, urg=urg, heat=heat, versions=versions))

# 1 · Nov 11 · early access by code (01-J)
a = article('e01', 'J')
a = rep(a, [
 ('<span class="rs" style="color:#FFFFFF">Members only</span> · Nov 23 – 27', '<span class="rs" style="color:#FFFFFF">Early access</span> · 30% off with your code'),
 ('<h2>Black Friday is open.<br>For you, first.</h2>', '<h2>Black Friday is open.<br>For you, first.</h2><p class="small" style="max-width:380px;color:var(--ink2)">Two days before everyone else: use your code for the same 30% off as Black Friday.</p>'),
 ('<div><span class="lab">Code</span><b>None</b><span>taken off at checkout</span></div>', '<div><span class="lab">Your code</span><b style="font-size:20px;letter-spacing:.04em">[[EARLY_ACCESS_CODE]]</b><span>works until Thu midnight</span></div>'),
 ('<div><span class="lab">Public on</span><b>Fri 27</b><span>November</span></div>', '<div><span class="lab">Open to everyone</span><b>Fri 13</b><span>November</span></div>'),
 ('Use my early access</a>', 'Use my code</a>'),
 ('Today · First pick</span>', 'Today · Your head start</span>'),
 ('Fri 27 · Everyone</span>', 'Fri 13 · Everyone</span>'),
 ('<span class="lab">Start with your finish</span>', '<span class="lab">Start here</span>'),
 ('<p class="small" style="color:var(--ink2)">Tap your finish. Everything inside is 30% off until Friday.</p>', '<p class="small" style="color:var(--ink2)">Tap where you want to start. Everything is 30% off with your code.</p>'),
 ('<span class="mproof">', '<span class="mproof">') if False else ('Taken off at checkout, no code · Case with 2+ pieces', 'Your code works Wed Nov 11 – Thu Nov 12 · Free shipping · Case included with 2+ pieces<br>Water-friendly · Stainless steel'),
])
# finish picker -> category picker (no finish names), black-first highlight kept on the first tile
def ctile(ref, name, sub, on=False):
    sm = ' style="padding-top:10px"' if on else ''
    return f'<a href="#"><img data-img="{ref}" alt="{name}"><span>{name} <em style="font-style:normal">→</em></span><small{sm}>{sub}</small></a>'
men = ctile('e08:3', 'Bracelets', 'From €20.97', True) + ctile('e01:1', 'Sets', 'From €41.97') + ctile('e03:3', 'Necklaces', 'From €24.43')
wom = ctile('e01:4', 'Bracelets', 'From €20.97', True) + ctile('e01:2', 'Sets', 'From €41.97') + ctile('e08:4', 'Necklaces', 'From €27.97')
blocks = re.findall(r'<div class="cx-choice" style="margin-top:16px">.*?</a></div>', a, re.S)
assert len(blocks) == 2
a = a.replace(blocks[0], f'<div class="cx-choice" style="margin-top:16px">{men}</div>', 1).replace(blocks[1], f'<div class="cx-choice" style="margin-top:16px">{wom}</div>', 1)
a = a.replace('<h3>Men</h3>', '<h3>For him</h3>').replace('<h3>Women</h3>', '<h3>For her</h3>').replace('<span class="lab">30% off</span>', '<span class="lab">With your code</span>')
a = rep(a, [('One of each: the 3x Set · €66.47', 'Not sure? The 3x Minimal Set · €66.47')])
add(1, 'Wed Nov 11', '10:00 local', 'Early access', 2, 'BIG send · code', [('A', 'Pick · from 01-J',
  meta('Early Access 1 (code)', 'Designed', 'You’re in early.', 'Your code: 30% off everything.', 'EARLY ACCESS · 30% OFF WITH YOUR CODE', 'Full list minus inactive 180+ days (BIG)', 'Head start, by code',
       'Lead on the head start, never a better price. Every link → [[EARLY_ACCESS_URL]], code applied automatically if possible. No finish names in copy or alt text. No Matte Cuff yet.', 'KA_W46_Nov11_EARLY_ACCESS_1 (CODE)'), resolve(a))])

# 2 · Nov 12 · last day of the code (02-D)
a = article('e02', 'D')
a = rep(a, [
 ('<span class="lab red">Early access</span></div>', '<span class="lab red">Last day for your code</span></div>'),
 ('<span class="lab">Your head start</span><h2>Two days left before everyone gets in.</h2>', '<span class="lab">Your head start</span><h2>Tomorrow, everyone gets in.</h2><p class="small" style="color:var(--ink2);max-width:420px">Your early-access code works until midnight tonight. Here’s what members picked first.</p>'),
 ('<i style="width:60%"></i>', '<i style="width:50%"></i>'),
 ('<span>Mon 23 · opened</span><b>Today, day 3 of 5</b><span>Fri 27 · public</span>', '<span>Wed Nov 11 · opened</span><b>Today · last day</b><span>Fri Nov 13 · everyone</span>'),
 ('<small>Members’ #1 · case included</small>', '<small>Members’ pick · case included</small>'),
 ('<small>Members’ #2 · case included</small>', '<small>Members’ pick · case included</small>'),
 ('<a class="solid" href="#">Use my head start</a><p class="small mute">Picks to confirm from Shopify, Nov 23 – 24.</p>',
  '<p style="margin:0 0 4px;font:500 10px/1.4 var(--body);letter-spacing:.2em;text-transform:uppercase;color:var(--grey)">Your code · <b style="color:var(--black)">[[EARLY_ACCESS_CODE]]</b></p><a class="solid" href="#">Use my code</a><p class="small mute">30% off with your code until midnight tonight. From Fri Nov 13 it’s open to everyone, no code.</p><p class="mproof">Free shipping · Case included with 2+ pieces · Water-friendly · Stainless steel<br>★★★★★ &nbsp;Rated 4.5 on Trustpilot · 3,000+ reviews</p>'),
])
add(2, 'Thu Nov 12', '10:00 local', 'Early access', 4, 'Engaged 30 · code', [('A', 'Pick · from 02-D',
  meta('Early Access 2 (code)', 'Designed', 'Your code ends tonight.', 'Use it before midnight.', 'EARLY ACCESS · LAST DAY FOR YOUR CODE', 'Engaged last 30 days', 'Last day of the code',
       'The urgency is the head start ending, not the price: 30% continues for everyone from Nov 13. Members’ picks: Katrina to pull the real top sellers from Nov 11 in Shopify. Links → [[EARLY_ACCESS_URL]].', 'KA_W46_Nov12_EARLY_ACCESS_2 (CODE)'), resolve(a))])

# 3 · Nov 13 · sale live (new)
a = (f'<article class="em cx " aria-label="Email 03">{strip("BFCM", "30% off site-wide · until Dec 6")}{top()}'
 f'<div style="padding:42px 24px 0;display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px"><span style="{LAB};color:var(--red)">Open to everyone</span>'
 f'<h2 style="margin:0;font:200 66px/.92 var(--disp);letter-spacing:-.045em">30% off.<br>Now for everyone.</h2>'
 f'<p class="copy" style="max-width:380px;color:var(--ink2);font-size:15px">The Black Friday sale is live: every piece, taken off at checkout, through Sun Dec 6.</p>'
 f'<a class="solid" href="#" style="margin-top:6px">Shop the sale</a></div>'
 + line('Today · 30% off for all', 'Sun Dec 6 · Ends') +
 f'<img src="{src("e01:0")}" alt="" style="display:block;width:100%;aspect-ratio:600/460;object-fit:cover;object-position:center 35%;margin-top:30px">'
 f'<div class="obar" style="margin-top:0"><span>30% off everything</span><span>Case included with 2+ pieces</span><span>Free shipping</span></div>'
 + hdr('Where to start') +
 f'<div class="bx-g c2" style="padding:18px 24px 0">{card("e01:1","3x Minimal Set","€94.95","€66.47")}{card("e01:3","Rope Bracelet","€29.95","€20.97")}{card("e01:4","Cube Bracelet","€29.95","€20.97")}{card("e03:2","Minimal Cuff","€34.90","€24.43")}</div>'
 f'<div class="cx-cta"><a class="solid" href="#">Find your piece</a>{USP}</div>{FOOT}</article>')
add(3, 'Fri Nov 13', '10:00 local', 'Sale live', 3, 'BIG send', [('A', 'New',
  meta('Sale live · launch', 'Designed', 'It’s open to everyone.', '30% off everything. No code.', 'BFCM · 30% OFF SITE-WIDE · UNTIL DEC 6', 'Full list minus inactive 180+ days, excl. BFCM purchasers (BIG)', 'Limited time: the sale opens',
       'Same day the ads and site theme go live: swap in the launch-ad headline and hero once final. The line under the button carries the campaign’s red dot: today → the Dec 6 end.', 'KA_W46_Nov13_BFCM_SALE_LIVE'), a)])

# 4 · Nov 15 · best sellers (new)
def rank(i, ref, name, sub, was, now):
    return (f'<li><a href="#"><span class="n">{i:02d}</span><img src="{src(ref)}" alt="{name}"><div><h4>{name}</h4><p class="small">{sub}</p>'
            f'<span class="price"><s>{was}</s><span>{now}</span></span></div><span class="arr">→</span></a></li>')
a = (f'<article class="em cx " aria-label="Email 04">{strip("BFCM", "30% off site-wide · until Dec 6")}'
 f'<div class="cx-top l"><img class="logo" src="{LOGO}" alt="Cavaier" style="width:80px!important;height:13.4px"><span class="lab red">Best sellers</span></div>'
 f'<div style="padding:40px 24px 26px;display:flex;flex-direction:column;gap:12px"><span style="{LAB};color:var(--grey)">This week, so far</span>'
 f'<h2 style="margin:0;font:200 58px/.95 var(--disp);letter-spacing:-.04em">What’s selling<br>first.</h2>'
 f'<p class="copy" style="max-width:400px;color:var(--ink2);font-size:15px">The pieces people picked first this week, all 30% off through Dec 6.</p></div>'
 f'<ol class="bx-rank">{rank(1,"e01:1","3x Minimal Set · Men","Three bracelets, case included","€94.95","€66.47")}{rank(2,"e01:2","3x Minimal Set · Women","Three bracelets, case included","€94.95","€66.47")}{rank(3,"e01:3","Rope Bracelet","The everyday one","€29.95","€20.97")}{rank(4,"e01:4","Cube Bracelet","Thin, goes with everything","€29.95","€20.97")}</ol>'
 f'<p class="stand">Ranking to confirm: Katrina to pull the real top sellers from Nov 11 – 14 in Shopify.</p>'
 f'<div class="obar" style="margin-top:28px"><span>30% off everything</span><span>Case included with 2+ pieces</span><span>Free shipping</span></div>'
 f'<div class="cx-cta"><a class="solid" href="#">Shop the best sellers</a>{USP}</div>{FOOT}</article>')
add(4, 'Sun Nov 15', '10:00 local', 'Sale live', 2, 'Engaged 30', [('A', 'New',
  meta('Sale · best sellers', 'Designed', 'What’s selling first.', 'Real picks from this week.', 'BFCM · 30% OFF SITE-WIDE · UNTIL DEC 6', 'Engaged last 30 days, excl. BFCM purchasers', 'Best sellers',
       '“Selling first” must reflect real Shopify data (Nov 11 – 14). Numbered ranking so the order itself is the proof.', 'KA_W46_Nov15_BFCM_SALE_BESTSELLERS'), a)])

# 5 · Nov 17 · lifestyle / real-world wear (new)
def moment(ref, t, sub):
    return (f'<div style="display:flex;flex-direction:column;gap:8px;min-width:0"><img src="{src(ref)}" alt="" style="aspect-ratio:3/4;object-fit:cover">'
            f'<span style="font:500 10px/1.3 var(--body);letter-spacing:.18em;text-transform:uppercase">{t}</span><span class="small" style="color:var(--ink2)">{sub}</span></div>')
a = (f'<article class="em cx " aria-label="Email 05">{strip("BFCM", "30% off site-wide · until Dec 6")}{top()}'
 f'<div style="padding:40px 24px 0;display:flex;flex-direction:column;gap:14px"><span style="{LAB};color:var(--red)">Shower · gym · sleep · repeat</span>'
 f'<h2 style="margin:0;font:200 60px/.93 var(--disp);letter-spacing:-.045em">Wear it through<br>everything.</h2>'
 f'<p class="copy" style="max-width:420px;color:var(--ink2);font-size:15px">Water-friendly, sweat-resistant, made for every day. 30% off through Dec 6.</p></div>'
 f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;padding:30px 24px 0">{moment("e06:5","In the water","Stays on when wet")}{moment("e08:3","Every day","Stainless steel")}{moment("e10:6","By the sea","Made to stay on")}</div>'
 f'<div style="padding:26px 24px 0"><a class="solid" href="#">Shop the sale</a></div>'
 + hdr('Made to stay on') +
 f'<div class="bx-g c3" style="padding:18px 24px 0">{card("e01:3","Rope Bracelet","€29.95","€20.97")}{card("e01:4","Cube Bracelet","€29.95","€20.97")}{card("e03:2","Minimal Cuff","€34.90","€24.43")}</div>'
 f'<div class="obar" style="margin-top:34px"><span>30% off everything</span><span>Case included with 2+ pieces</span><span>Free shipping</span></div>'
 f'<div class="cx-cta"><a class="solid" href="#">Find your everyday piece</a>{USP}</div>{FOOT}</article>')
add(5, 'Tue Nov 17', '10:00 local', 'Sale live', 1, 'Engaged 30 + 90', [('A', 'New',
  meta('Sale · real-world wear', 'Designed', 'Shower, gym, sleep, repeat.', 'It stays on when wet.', 'BFCM · 30% OFF SITE-WIDE · UNTIL DEC 6', 'Engaged 30 + 31–90 days, excl. BFCM purchasers', 'Lifestyle / real-world wear',
       'Real on-wrist shots in daily moments. Swap in a gym or sleeve shot if Katrina has one; the three captions follow the photos.', 'KA_W46_Nov17_BFCM_SALE_1'), a)])

# 6 · Nov 19 · text, gifting (new)
a = text_email(6, ['If you have people to shop for this year, now is the easy time. Everything is 30% off, shipping is on us, and orders of 2 or more pieces arrive in a jewelry case, ready to give. <a href="#">Shop gifts →</a>',
                   'Not sure what they’d like? The Sets are the easiest pick → <a href="#">Men’s Sets</a> · <a href="#">Women’s Sets</a>'])
add(6, 'Thu Nov 19', '10:00 local', 'Sale live', 1, 'Engaged 30 · text', [('A', 'New · text only',
  meta('Sale · gift list', 'Text only', 'Gift list, sorted early.', 'Skip the December rush.', '— (text only)', 'Engaged last 30 days, excl. BFCM purchasers', 'Gifting',
       'Gifting is allowed again: this is a sale email, not an early-access email.', 'EXTRA_KA_W46_Nov19_BFCM_SALE_2_TEXT ONLY'), a)])

# 7 · Nov 22 · versatile (new)
def look(ref, t):
    return (f'<div style="position:relative;min-width:0"><img src="{src(ref)}" alt="" style="aspect-ratio:4/5;object-fit:cover">'
            f'<span style="position:absolute;left:10px;bottom:10px;background:#FFFFFF;padding:7px 10px;font:500 9.5px/1 var(--body);letter-spacing:.16em;text-transform:uppercase">{t}</span></div>')
def lrow(ref, name, was, now):
    return (f'<a class="lrow" href="#"><img src="{src(ref)}" alt="{name}"><div><h4>{name}</h4><div class="price"><s>{was}</s><span>{now}</span></div></div><span class="arr">→</span></a>')
a = (f'<article class="em cx " aria-label="Email 07">{strip("BFCM", "30% off site-wide · until Dec 6")}{top()}'
 f'<div style="padding:40px 24px 0;display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px"><span style="{LAB};color:var(--grey)">Goes with everything</span>'
 f'<h2 style="margin:0;font:200 60px/.93 var(--disp);letter-spacing:-.045em">One piece.<br>Every outfit.</h2>'
 f'<p class="copy" style="max-width:400px;color:var(--ink2);font-size:15px">Our best sellers, made to go with everything you wear. 30% off through Dec 6.</p>'
 f'<a class="solid" href="#" style="margin-top:6px">Shop the sale</a></div>'
 f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:32px 24px 0">{look("e06:3","White shirt")}{look("e10:0","Black top")}{look("e08:0","Linen")}{look("e12:0","Knit")}</div>'
 + hdr('The ones that go with everything') +
 f'<div style="margin-top:6px">{lrow("e01:3","Rope Bracelet","€29.95","€20.97")}{lrow("e01:4","Cube Bracelet","€29.95","€20.97")}{lrow("e03:2","Minimal Cuff","€34.90","€24.43")}{lrow("e12:2","Crystal Necklace","€89.95","€62.97")}{lrow("e01:1","3x Minimal Set","€94.95","€66.47")}</div>'
 f'<div class="cx-cta"><a class="solid" href="#">Shop the best sellers</a><p class="small mute">Case included with 2+ pieces · Free shipping on every order</p>{USP}</div>{FOOT}</article>')
add(7, 'Sun Nov 22', '10:00 local', 'Sale live', 1, 'Engaged 30 + 90', [('A', 'New',
  meta('Sale · versatile', 'Designed', 'Goes with everything.', 'Matches everything you own.', 'BFCM · 30% OFF SITE-WIDE · UNTIL DEC 6', 'Engaged 30 + 31–90 days, excl. BFCM purchasers', 'Versatile',
       'Four outfits, one idea: the same quiet pieces go with all of them. Outfit labels follow the photos; change them if the shots change.', 'KA_W48_Nov22_BFCM_SALE_3'), a)])

# 8 · Nov 24 · text, the case (new)
a = text_email(8, ['A small detail people ask about: pick 2 or more pieces and your order arrives in a Cavaier jewelry case, included and added automatically. Useful for travel, better for gifting.',
                   'Everything is still 30% off, through Sun Dec 6. <a href="#">Pick your two →</a>'])
a = a.replace('<p>— Eli</p>', '<p>— Eli</p><p>P.S. The Sets make it easy → <a href="#">Sets</a></p>')
add(8, 'Tue Nov 24', '10:00 local', 'Sale live', 2, 'Engaged 30 · text', [('A', 'New · text only',
  meta('Sale · about the case', 'Text only', 'About the case.', 'Pick two pieces, it’s included.', '— (text only)', 'Engaged last 30 days, excl. BFCM purchasers', 'Bonus: the case',
       'Never write “free” for the case in subject, preview or headline.', 'EXTRA_KA_W48_Nov24_BFCM_SALE_4_TEXT ONLY'), a)])

# 9 · Nov 26 · anticipation, split hero (new)
a = (f'<article class="em cx " aria-label="Email 09">{strip("BFCM", "30% off site-wide · until Dec 6")}{top()}'
 f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px"><img src="{src("e01:1")}" alt="" style="aspect-ratio:3/4;object-fit:cover"><img src="{src("e01:2")}" alt="" style="aspect-ratio:3/4;object-fit:cover"></div>'
 f'<div style="padding:40px 24px 0;display:flex;flex-direction:column;align-items:center;text-align:center;gap:14px"><span style="{LAB};color:var(--red)">Thursday · the day before</span>'
 f'<h2 style="margin:0;font:200 58px/.93 var(--disp);letter-spacing:-.045em">Tomorrow is<br>Black Friday.</h2>'
 f'<p class="copy" style="max-width:400px;color:var(--ink2);font-size:15px">Everything stays 30% off through Dec 6, and on Saturday, something new arrives.</p>'
 f'<a class="solid" href="#" style="margin-top:6px">Shop the sale</a></div>'
 + line('Today · 30% off', 'Sat 28 · Something new') + hdr('Before Black Friday') +
 f'<div class="bx-g c3" style="padding:18px 24px 0">{card("e10:8","3x Minimal Set","€94.95","€66.47")}{card("e01:3","Rope Bracelet","€29.95","€20.97")}{card("e04:2","2x Duo Minimal Set","€59.95","€41.97")}</div>'
 f'<div class="obar" style="margin-top:34px"><span>30% off everything</span><span>Case included with 2+ pieces</span><span>Free shipping</span></div>'
 f'<div class="cx-cta"><a class="solid" href="#">Shop before Black Friday</a>{USP}</div>{FOOT}</article>')
add(9, 'Thu Nov 26', '10:00 local', 'Sale live', 3, 'Engaged 30 + 90', [('A', 'New',
  meta('Sale · anticipation', 'Designed', 'Black Friday is tomorrow.', 'Plus something new Saturday.', 'BFCM · 30% OFF SITE-WIDE · UNTIL DEC 6', 'Engaged 30 + 31–90 days, excl. BFCM purchasers', 'Anticipation',
       'The sale has been live since Nov 13: no “opens to everyone” or price-ending urgency. The Saturday tease is text only, no Matte Cuff imagery until Nov 28.', 'KA_W48_Nov26_BFCM_SALE_5'), a)])

# 10 · Nov 27 10:00 · Black Friday send 1 (03-A)
a = article('e03', 'A')
a = rep(a, [
 ('<span class="rs">Black Friday</span> · 30% off sitewide · Nov 27 – Dec 6', '<span class="rs">Black Friday</span> · 30% off site-wide · until Dec 6'),
 ('<a class="hbtn" href="#">Shop the sale</a>', '<a class="hbtn" href="#">Shop 30% off</a>'),
 ('<span>Case with any Set or 2 pieces</span>', '<span>Case included with 2+ pieces</span>'),
 ('<p class="copy">Once a year. Everything is 30% off until Dec 6, applied at checkout. No code.</p>', '<p class="copy">Everything is 30% off until Dec 6, applied at checkout. No code.</p><a class="solid" href="#" style="margin-top:4px">Shop 30% off</a>'),
 ('Waterproof · Stainless steel<br>', 'Water-friendly · Stainless steel<br>'),
])
add(10, 'Fri Nov 27', '10:00 local', 'Black Friday', 4, 'BIG send · 1 of 3', [('A', 'Pick · from 03-A',
  meta('BFCM V1 · Black Friday', 'Designed', 'Black Friday is here.', 'Your everyday piece, 30% off.', 'BLACK FRIDAY · 30% OFF SITE-WIDE · UNTIL DEC 6', 'Full list minus inactive 180+ days, excl. BFCM purchasers (BIG)', 'Limited time: Black Friday',
       '“is here”, not “is open”: the sale has been live since Nov 13. “Once a year.” removed until confirmed true.', 'KA_W46_Nov27_BFCM_V1'), a)])

# 11 · Nov 27 14:00 · Black Friday send 2 (04-B)
a = article('e04', 'B')
a = rep(a, [
 ('<a class="solid" href="#">Find yours at 30% off</a><p class="small mute">Two or more pieces and the jewelry case is included. Shipping on every order is on us.</p>',
  '<a class="solid" href="#">Get the best seller</a><p class="small mute">30% off, applied at checkout · Case included with 2+ pieces · Shipping on us</p><p class="mproof">Water-friendly · Stainless steel</p>'),
])
add(11, 'Fri Nov 27', '14:00 local', 'Black Friday', 4, 'Engaged 30 · 2 of 3', [('A', 'Pick · from 04-B',
  meta('BFCM V2 · best sellers + reviews', 'Designed', 'Rated 4.5 by 3,000+', 'See what they bought.', 'BLACK FRIDAY · 30% OFF SITE-WIDE', 'Engaged last 30 days, excl. BFCM purchasers', 'Best sellers + reviews',
       'New hero and layout from Send 1, so it never feels like a repeat. Katrina to pull 2 verified Trustpilot reviews. Klaviyo: Smart Sending OFF.', 'KA_W46_Nov27_BFCM_V2'), resolve(a))])

# 12 · Nov 27 19:00 · Black Friday send 3 (05-B)
a = article('e05', 'B')
a = rep(a, [
 ('<a class="solid" href="#">Shop all gifts</a><p class="mproof">Adjustable to fit any wrist · Waterproof<br>', '<a class="solid" href="#">Shop the gift edit</a><p class="mproof">Sized however you want · Water-friendly · Case included with 2+ pieces<br>'),
 ('<h4>Role Pendant</h4>', '<h4>Rope Pendant</h4>'),
 ('alt="Role Pendant"', 'alt="Rope Pendant"'),
])
add(12, 'Fri Nov 27', '19:00 local', 'Black Friday', 4, 'Engaged 30 · 3 of 3', [('A', 'Pick · from 05-B',
  meta('BFCM V3 · gifting', 'Designed', 'Gifts under €25', 'And a few worth more.', 'BLACK FRIDAY · GIFTS AT 30% OFF', 'Engaged last 30 days, excl. BFCM purchasers', 'Gifting',
       'All prices: CEO to confirm. Klaviyo: Smart Sending OFF.', 'KA_W46_Nov27_BFCM_V3'), resolve(a))])

# 13 · Nov 28 · Matte Cuff drop (06-C) + buyer version
base = article('e06', 'C')
common = [
 ('<span class="rs" style="color:#FFFFFF">Just dropped</span> · the Matte Cuff', '<span class="rs" style="color:#FFFFFF">New</span> · The Matte Cuff · 30% off'),
 ('Stainless steel, 100% waterproof, adjustable. Jewelry case included.', 'Stainless steel, water-friendly, adjustable. Jewelry case included.'),
 ('<tr><td>Waterproof</td>', '<tr><td>Water-friendly</td>'),
 ('<span>Waterproof</span>', '<span>Water-friendly</span>'),
]
a = rep(base, common + [
 ('<p class="cx-sub" style="color:var(--ink2)">The Matte Cuff, the one you kept asking for. Our first matte finish, made to wear next to the original glossy cuff.</p>',
  '<p class="cx-sub" style="color:var(--ink2)">The Matte Cuff: our first matte finish, made to wear next to the original cuff. 30% off.</p>'),
 ('<div class="cx-cta"><a class="solid" href="#">Shop glossy + matte</a>', '<div class="cx-cta"><a class="solid" href="#">Get it first</a>'),
])
b = rep(base, common + [
 ('<span class="lab red">You asked. We made it.</span><p class="cx-h" style="font-size:56px">It’s here.</p>', '<span class="lab red">For Black Friday buyers</span><p class="cx-h" style="font-size:46px">You got the classic.<br>Now meet the new one.</p>'),
 ('<p class="cx-sub" style="color:var(--ink2)">The Matte Cuff, the one you kept asking for. Our first matte finish, made to wear next to the original glossy cuff.</p><span class="price lg"><s>€74.85</s><span>€52.40</span></span><a class="solid" href="#" style="margin-top:6px">Shop glossy + matte</a>',
  '<p class="cx-sub" style="color:var(--ink2)">The Matte Cuff just landed, and it pairs with what you ordered. Still 30% off.</p><span class="price lg"><s>€39.95</s><span>€27.97</span></span><a class="solid" href="#" style="margin-top:6px">Add the Matte Cuff</a>'),
 ('<div class="cx-cta"><a class="solid" href="#">Shop glossy + matte</a>', '<div class="cx-cta"><a class="solid" href="#">Add the Matte Cuff</a>'),
])
b = b.replace('aria-label="Email 06, version C"', 'aria-label="Email 13, buyer version"')
add(13, 'Sat Nov 28', '10:00 local', 'BF weekend + drop', 3, 'Engaged 30 + 90 · buyers', [
 ('A', 'Pick · from 06-C · sale version',
  meta('BF weekend · Matte Cuff drop', 'Designed', 'We made it matte.', 'No shine. All presence.', 'NEW · THE MATTE CUFF · 30% OFF', 'Engaged 30 + 31–90 days, not purchased', 'Product spotlight: Matte Cuff',
       'Glossy + Matte bundle at €52.40: CEO to confirm the bundle exists at this price. Stand-in photos until the Matte Cuff shoot is in.', 'KA_W47_Nov28_BF WEEKEND + MATTE CUFF DROP'), resolve(a)),
 ('B', 'Buyer version',
  meta('BF weekend · Matte Cuff · buyers', 'Designed', 'Meet the new one.', 'It pairs with yours.', 'NEW · THE MATTE CUFF · 30% OFF', 'Everyone who bought during BFCM (from Nov 11)', 'Second purchase: pairs with yours',
       'Hero should show the Matte Cuff worn next to a best seller (photo to come). Goal: “oh, I want this new one too.”', 'KA_W47_Nov28_BF WEEKEND + MATTE CUFF DROP · buyers'), resolve(b))])

# 14 · Nov 29 · note from Eli (07-C)
a = article('e07', 'C')
a = rep(a, [
 ('<p>Black Friday pricing is still on today: 30% off everything, taken off at checkout.</p>', '<p>A quick one. Black Friday pricing is still on today: 30% off everything, applied automatically.</p>'),
 ('<p>And if you missed it yesterday, we launched the Matte Cuff, our first matte finish. I think it’s the best thing we’ve made this year.</p>', '<p>Tomorrow, Cyber Week opens and runs through Sunday, Dec 6. And if you missed it yesterday: the Matte Cuff is here, our first matte finish.</p>'),
 ('<p class="small mute">Tomorrow it becomes Cyber Week, through Sun Dec 6.</p>', '<p class="small mute">Every link goes to the sale · 30% off through Sun Dec 6</p>'),
])
add(14, 'Sun Nov 29', '10:00 local', 'BF weekend', 2, 'Engaged 30', [('A', 'Pick · from 07-C',
  meta('BF weekend · a note from Eli', 'Designed letter', 'A note from Eli', 'Plus the new one.', '— (designed letter)', 'Engaged last 30 days, excl. BFCM purchasers', 'Curiosity',
       'Designed letter, kept light. The Matte Cuff card links to the sale page, so every link is one action.', 'EXTRA_KA_W47_Nov29_BF WEEKEND_TEXT ONLY'), resolve(a))])

# 15 · Nov 30 10:00 · Cyber Monday send 1 (08-E)
a = article('e08', 'E')
a = rep(a, [
 ('<span class="lab red">Until Nov 3</span>', '<span class="lab red">Cyber Week · until Dec 6</span>'),
 ('<s>Black Friday</s><b>Cyber Monday</b>', '<s style="text-decoration:none;color:var(--grey)">Black Friday didn’t end.</s><b>It got a week.</b>'),
 ('Same 30% off everything, for seven more days. Including the new Matte Cuff.', 'Same 30% off everything, for seven more days, including the new Matte Cuff.'),
 ('<h2>The Matte Cuff</h2>', '<span class="hot" style="margin:0 auto">New</span><h2>The Matte Cuff</h2>'),
 ('<a class="solid" href="#">Get it at 30% off</a><p class="small mute">Everything else is 30% off too · <a href="#">shop all</a></p>', '<a class="solid" href="#">Shop before Dec 6</a><p class="small mute">30% off everything through Sun Dec 6 at midnight, your local time</p>' + USP),
])
add(15, 'Mon Nov 30', '10:00 local', 'Cyber Monday', 4, 'BIG send · 1 of 3', [('A', 'Pick · from 08-E',
  meta('Cyber Monday V1', 'Designed', 'Cyber Week is open.', 'Cyber Week starts now.', 'CYBER WEEK · 30% OFF UNTIL DEC 6', 'Full list minus inactive 180+ days, excl. BFCM purchasers (BIG)', 'Limited time: Cyber Monday',
       'Every link → the Cyber Week page (one action). Matte Cuff first with a “New” tag.', 'KA_W47_Nov30_CYBERMONDAY_V1'), resolve(a))])

# 16 · Nov 30 14:00 · text, materials (11-A)
a = text_email(16, ['The short version: stainless steel, so it doesn’t rust, fade or turn your skin green. Hypoallergenic. Clasps and weight that feel deliberate, not light and cheap. That’s why people wear one for months. <a href="#">See the collection →</a>',
                    'It’s Cyber Monday, and everything is still 30% off, through Sunday, Dec 6.'])
a = a.replace('<p>— Eli</p>', '<p>— Eli</p><p>P.S. The Sets are the easiest way in → <a href="#">Shop the Sets</a></p>')
add(16, 'Mon Nov 30', '14:00 local', 'Cyber Monday', 3, 'Engaged 30 · text · 2 of 3', [('A', 'Pick · from 11-A',
  meta('Cyber Monday V2 · materials', 'Text only', 'Won’t turn you green.', 'What it’s actually made of.', '— (text only)', 'Engaged last 30 days, excl. BFCM purchasers', 'Materials & craft',
       'Moved from Thu Dec 3. Klaviyo: Smart Sending OFF.', 'EXTRA_KA_W47_Nov30_CYBERMONDAY_V2_TEXT ONLY'), a)])

# 17 · Nov 30 19:00 · text, water-friendly (09-A)
a = text_email(17, ['Most jewelry asks you to take it off: before the shower, the gym, the sea. Ours doesn’t. Stainless steel, water-friendly, tarnish-resistant. Put it on once and leave it. <a href="#">Shop the pieces that stay on →</a>',
                    'It’s Cyber Monday: 30% off everything, through Sunday, Dec 6.'])
a = a.replace('<p>— Eli</p>', '<p>— Eli</p><p>P.S. Most people start with the Rope Bracelet → <a href="#">See it</a></p>')
add(17, 'Mon Nov 30', '19:00 local', 'Cyber Monday', 3, 'Engaged 30 · text · 3 of 3', [('A', 'Pick · from 09-A',
  meta('Cyber Monday V3 · water-friendly', 'Text only', 'Still wearing yours?', 'Shower, gym, sea. Still on.', '— (text only)', 'Engaged last 30 days, excl. BFCM purchasers', 'Water-friendly',
       'Moved from Tue Dec 1. Klaviyo: Smart Sending OFF.', 'EXTRA_KA_W47_Nov30_CYBERMONDAY_V3_TEXT ONLY'), a)])

# 18 · Dec 2 · Sets (10-B)
a = article('e10', 'B')
a = rep(a, [('<a class="solid" href="#">Shop the Sets</a>', '<a class="solid" href="#">Shop the Sets</a>')])
a = a.replace('<div class="strip">', '<div class="strip">', 1)
a = re.sub(r'<div class="strip"><span class="rs">Cyber Week</span> · the Sets</div>', '<div class="strip"><span class="rs">Cyber Week</span> · 30% off until Dec 6</div>', a)
newcard = (f'<a class="bx-inline" href="#"><img src="{src("e08:1")}" alt="Matte Cuff"><div><span class="lab red">New · the new anchor</span>'
           f'<h4 style="margin:0;font:400 12px/1.3 var(--body);letter-spacing:.14em;text-transform:uppercase">The Matte Cuff</h4><span class="small" style="color:var(--ink2)">Our first matte finish. Wear it with any Set.</span><span class="price"><s>€39.95</s><span>€27.97</span></span></div></a>')
k = a.find('<div class="mcta">') if '<div class="mcta">' in a else a.find('<div class="cx-cta">')
i_cta = a.rfind('<a class="solid" href="#">Shop the Sets</a>')
blk = a.rfind('<div', 0, i_cta)
a = a[:blk] + newcard + a[blk:]
a = a.replace('<p class="mproof">★★★★★ &nbsp;Rated 4.5 on Trustpilot · 3,000+ reviews</p>', '<p class="mproof">Sized however you want · Water-friendly<br>★★★★★ &nbsp;Rated 4.5 on Trustpilot · 3,000+ reviews</p>', 1)
add(18, 'Wed Dec 2', '10:00 local', 'Cyber Week', 3, 'Engaged 30 + 90', [('A', 'Pick · from 10-B',
  meta('Cyber Week · the Sets', 'Designed', '€66.47 for three', 'Case and shipping included.', 'CYBER WEEK · 30% OFF UNTIL DEC 6', 'Engaged 30 + 31–90 days, excl. BFCM purchasers', 'Versatile: Sets',
       'Receipt layout. Prices: CEO to confirm. Say “Set”, never “Stack”. Matte Cuff added as the new anchor.', 'KA_W47_Dec02_CYBERWEEK_3'), resolve(a))])

# 19 · Dec 4 · in their words (12-C)
a = article('e12', 'C')
a = rep(a, [
 ('<span class="lab" style="color:#fff">Ends Sunday</span>', '<span class="lab" style="color:#fff">Cyber Week · ends Sun Dec 6</span>'),
 ('<span class="lab" style="color:#fff">Nicole A · verified buyer</span>', '<span class="lab" style="color:#fff">Nicole A · verified buyer</span><p class="small" style="color:#fff;max-width:380px;margin:6px 0 4px">Real reviews from people who never take theirs off. Cyber Week ends Sunday.</p>'),
 ('<h4>Role Pendant Necklace</h4>', '<h4>Rope Pendant Necklace</h4>'),
 ('30% off until Sun Dec 6 at midnight, your local time · Free shipping on every order', '30% off until Sun Dec 6 at midnight, your local time · Free shipping on every order · Order by Sun Dec 6 for holiday delivery'),
])
add(19, 'Fri Dec 4', '10:00 local', 'Cyber Week', 4, 'Engaged 30 + 90', [('A', 'Pick · from 12-C',
  meta('Cyber Week · in their words', 'Designed', 'Worn by 3,000+', 'In their words. Ends Sunday.', 'CYBER WEEK · ENDS SUNDAY, DEC 6', 'Engaged 30 + 31–90 days, excl. BFCM purchasers', 'Customer stories',
       'Headline is a short line from a verified Trustpilot review (fallback: “In their words.”). Matte Cuff as the final “New this week” card.', 'KA_W47_Dec04_CYBERWEEK_5'), resolve(a))])

# 20 · Dec 6 · last call (13-A)
a = article('e13', 'A')
a = rep(a, [
 ('· 30% off ends at midnight</span>', '· 30% off ends tonight</span>'),
 ('Shop before midnight</a></div>', 'Shop before midnight</a><p class="small" style="margin:-8px 0 0;color:var(--ink2)">Ends tonight at midnight.</p></div>'),
])
add(20, 'Sun Dec 6', '10:00 local', 'Last call', 5, 'BIG send · last email', [('A', 'Pick · from 13-A',
  meta('Last chance', 'Designed', 'Today’s the last day.', 'Tonight, prices go back.', 'LAST DAY · 30% OFF ENDS TONIGHT', 'Full list minus inactive 180+ days, excl. BFCM purchasers (BIG)', 'Limited time: last day',
       'End time in live text next to the CTA. No countdown timer (sends are recipient-local).', 'KA_W47_Dec06_LAST CHANCE'), a)])

# ---------- assemble ----------
def pips(n): return ''.join(f'<i class="{"on" if i < n else ""}"></i>' for i in range(5))
entries = []
for s in S:
    mains = ''.join(f'<div class="main" data-ver="{v}"><div class="vtag"><b>{"Send " + str(s["n"]) if v == "A" else "Buyer version"}</b><i>{tag}</i></div>{m}{art}</div>' for v, tag, m, art in s['versions'])
    entries.append(f'''
<section class="entry" id="s{s["n"]:02d}">
  <div class="rail"><span class="no">{s["n"]:02d}</span><p class="d">{s["date"]}</p><p class="tm2">{s["time"]}</p>
    <p class="ph2">{s["phase"]}</p><span class="pips" aria-label="Urgency {s["urg"]} of 5">{pips(s["urg"])}</span><p class="heat">{s["heat"]}</p></div>
  <div class="vtrack">{mains}</div>
</section>''')
rows = ''.join(f'<tr><td><a href="#s{s["n"]:02d}">{s["n"]:02d}</a></td><td>{s["date"]}<span class="tm">{s["time"].replace(" local","")}</span></td><td>{s["phase"]}</td><td>{re.search(r"<b>(.*?)</b>", s["versions"][0][2]).group(1)}</td><td>{re.search(r"· ([^<]*)</dd><dt>Subject", s["versions"][0][2]).group(1)}</td><td><span class="pips">{pips(s["urg"])}</span></td><td class="sj">{re.search(r"<dt>Subject</dt><dd>(.*?)</dd>", s["versions"][0][2]).group(1)}</td><td class="sj">{s["heat"]}</td></tr>' for s in S)
intro = f'''<header class="intro">
    <span class="kicker">BFCM26 · Nov 11 – Dec 6 · 20 sends · brief v10</span>
    <h1>Cavaier BFCM26 sequence</h1>
    <p>The v10 plan: 20 emails (15 designed, 5 text only), each showing the picked design with its copy aligned to the v10 brief. Picks come from the Figma “Selected” column; the 8 sends that had no email yet are new. All sends 10:00 recipient-local, with Black Friday and Cyber Monday at 10:00 / 14:00 / 19:00. Main store only. The earlier A–J page is archived in the repo (bfcm26/archive).</p>
  </header>
  <section class="card">
    <span class="kicker">The red line</span>
    <h2>“The one you never take off.”</h2>
    <p>One idea runs through all 20 sends: Cavaier is the piece you put on once and leave on, and this is when it’s 30% off. It opens as a head start (two days early, by code), opens to everyone, builds proof (best sellers, real-world wear, reviews), gets something new (the Matte Cuff, with a buyer version), and closes on a real deadline. The discount never changes; the reason to buy today does. A slim line with a red dot marks the next date that matters (Fri 13 · Everyone, Sat 28 · Something new, Dec 6 · Ends).</p>
    <div class="arc">
      <div><b>Early access</b><span>Nov 11 – 12 · 30% by code [[EARLY_ACCESS_CODE]], two days before everyone.</span></div>
      <div><b>Sale live</b><span>Nov 13 – 26 · Open to everyone, then best sellers, real-world wear, gifting, versatile, the case, the eve.</span></div>
      <div><b>Black Friday</b><span>Nov 27 · Three sends: launch, best sellers + reviews, gifts by budget.</span></div>
      <div><b>Drop + weekend</b><span>Nov 28 – 29 · Matte Cuff (sale + buyer version), then a note from Eli.</span></div>
      <div><b>Cyber Week</b><span>Nov 30 – Dec 6 · Cyber Monday ×3, Sets, reviews, last day.</span></div>
    </div>
    <div class="rules">
      <div><b>Offer</b>30% off site-wide: by code Nov 11 – 12, then automatic for everyone from Nov 13 until Sun Dec 6 at midnight, recipient’s local time.</div>
      <div><b>Case &amp; shipping</b>Jewelry case included with 2 or more pieces. Free shipping on every order. Order by Dec 6 for holiday delivery.</div>
      <div><b>Matte Cuff</b>Launches Sat Nov 28 (buyer version for BFCM buyers), then appears in every designed Cyber Week email.</div>
      <div><b>Never</b>“Free” in a subject, preview, banner or headline · “waterproof” (say water-friendly) · a lifetime warranty · “Stack” (always “Set”) · finish names in early access.</div>
    </div>
  </section>
  <div class="tbl">
    <table>
      <thead><tr><th>#</th><th>Send (local)</th><th>Phase</th><th>Email</th><th>Format</th><th>Urgency</th><th>Subject</th><th>Audience</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
  <div class="notes">
    <strong>To confirm before build</strong>
    <ul>
      <li>Katrina: real top sellers from Nov 11 (send 2) and Nov 11 – 14 (send 4); 2 verified Trustpilot reviews (send 11); the review line used as the headline (send 19).</li>
      <li>CEO: gift prices (send 12), the Glossy + Matte bundle at €52.40 (send 13), Set prices (send 18).</li>
      <li>Launch-ad headline and hero for send 3, once final. Matte Cuff photos are stand-ins until the shoot is in.</li>
      <li>Shopify: the early-access code must expire at midnight Nov 12 and not combine with the automatic 30%; end the automatic 30% at midnight in the last time zone the store sells to.</li>
      <li>Klaviyo: Smart Sending off for sends 11, 12, 16 and 17.</li>
    </ul>
  </div>'''
# splice into the page
p0 = h.find('<header class="intro">'); p1 = h.find('<div class="bar2">')
p2 = h.find('<section class="entry"'); p3 = h.find('<script>', h.rfind('</section>'))
bar = h[p1:p2]
bar = re.sub(r'<div class="vpick".*?</div>', '', bar, flags=re.S)
tail_end = h.rfind('</section>') + len('</section>')
out = h[:p0] + intro + '\n\n  ' + bar + ''.join(entries) + '\n' + h[tail_end:]
for a, b in [('<span class="lab red">New · the new anchor</span>', '<span class="lab red">New this week</span>'),
             ('<a class="solid" href="#">Shop before Black Friday</a>', '<a class="solid" href="#">Shop the sale</a>')]:
    assert out.count(a) == 1, a
    out = out.replace(a, b)
open(OUT, 'w').write(out)
print('sends', len(S), 'size', len(out))
