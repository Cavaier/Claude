#!/usr/bin/env python3
"""v5: conversion pass, informed by Cavaier's BFCM 2025 Klaviyo results."""
import base64, os, re, concurrent.futures as cf
import gen_bfcm26 as g
import gen_bfcm26_v2 as v2
import gen_bfcm26_v3 as v3
import gen_bfcm26_v4 as v4

PROOF = '<p class="mproof">★★★★★ &nbsp;4.5 on Trustpilot · 2,179 reviews</p>'
OFFER_BAR = ('<div class="obar"><span>30% off everything</span><span>Case with any Set or 2 pieces</span>'
             '<span>No code needed</span></div>')

def with_cta_proof(html):
    """Add the proof micro-line under the first primary button block."""
    return re.sub(r'(<div class="mcta">\s*<a class="solid"[^>]*>[^<]*</a>)', lambda m: m.group(1) + PROOF, html, count=1)

def wrap(fn, *steps):
    def inner():
        h = fn()
        for s in steps:
            h = s(h)
        return h
    return inner

def strip_text(new):
    return lambda h: re.sub(r'<div class="strip">[^<]*</div>', f'<div class="strip">{new}</div>', h, count=1)

def after_first(marker, add):
    return lambda h: h.replace(marker, marker + add, 1)

# ---------------------------------------------------------------- per-email upgrades
E = {
    # 01: offer in the strip; button right under the hero is already there; proof by the CTA
    '01': wrap(v3.e01, strip_text('Early access · 30% off everything · Nov 23 – 26'), with_cta_proof),
    # 02: offer strip + offer bar under the split hero
    '02': wrap(v4.e02, strip_text('Early access · 30% off everything · ends Fri 07:00'),
               after_first('</a></div></div>', OFFER_BAR), with_cta_proof),
    # 03: offer bar straight under the poster, proof by the CTA
    '03': wrap(v3.e03, lambda h: h.replace('<div class="under">', OFFER_BAR + '<div class="under">', 1), with_cta_proof),
    # 04: a button above the fold, before the ledger
    '04': wrap(v3.e04, lambda h: re.sub(r'(<div class="cttl">.*?</div>)', r'\1<div class="mcta tight"><a class="solid" href="#">Shop the Sets</a>' + PROOF + '</div>', h, count=1, flags=re.S)),
    # 05: button straight after the score
    '05': wrap(v3.e05, after_first('trusted worldwide</p></div>', '<div class="mcta tight"><a class="solid" href="#">Shop most loved</a></div>')),
    '06': wrap(v4.e06),
    '08': wrap(v4.e08, lambda h: h.replace('<div class="sec" style="padding-top:30px"></div>', OFFER_BAR, 1), with_cta_proof),
    # 10: link under the title so the first screen has an action
    '10': wrap(v3.e10, lambda h: re.sub(r'(<div class="cttl c">.*?</div>)', r'\1<div class="mgo center" style="padding:0 24px 22px"><a class="ulink" href="#">Shop all gifts <span>→</span></a></div>', h, count=1, flags=re.S), with_cta_proof),
    '12': wrap(v4.e12, with_cta_proof),
    '13': wrap(v4.e13, with_cta_proof),
}

# ---------------------------------------------------------------- text-only: link early, P.S. at the end
def ps(text, link):
    return f'P.S. {text} {g.L(link)}'

t07 = g.textmail([
    'Hi {first name},',
    f'A quick note from me, not a campaign. Everything on cavaier.com is 30% off until Sunday, December 6. {g.L("Shop the sale →")}',
    'If I had to pick three:',
    f'– The 3x Minimal Set. Three bracelets, worn together or apart, and the jewelry case is included. Our best value. {g.L("See the Set")}<br>'
    f'– The Minimal Cuff. The one I never take off. €24.43 this week. {g.L("See the Cuff")}<br>'
    f'– The new Matte Cuff. We dropped it yesterday, and the first batch is small. {g.L("See the Matte Cuff")}',
    'Everything is waterproof and made from 316L stainless steel. Shower, gym, sleep: it stays on.',
    'Eli<br>Cavaier',
    ps('Add any two pieces and the jewelry case comes with your order.', 'Start with two →')])

t09 = g.textmail([
    'Hi {first name},',
    f'If you’re shopping for someone else this week, here’s everything you need, in 30 seconds. {g.L("Shop gifts →")}',
    '<b>Size.</b> Every bracelet and cuff adjusts, and necklaces have an extension chain. You don’t need their size.<br>'
    '<b>Wrapping.</b> Any Set, or any two pieces, comes with our jewelry case. Ready to give.<br>'
    '<b>Can’t decide?</b> Gift cards go from €10 to €100, arrive by email and last 3 months. (Not part of the 30% off.)<br>'
    '<b>Delivery.</b> [CEO to confirm: order by [date] for delivery before Christmas]',
    'Eli<br>Cavaier',
    ps('Gifts start at €20.97 this week.', 'See the gift guide →')])

t11 = g.textmail([
    'Hi {first name},',
    'The question we get most: “Can I really wear it all the time?”',
    'Yes. That’s the whole point. Every piece is 316L stainless steel, so it’s waterproof, sweat-proof and heat-proof. '
    'Shower, swim, train, sleep. It stays on, and it doesn’t tarnish.',
    'And every bracelet, cuff and necklace adjusts, so it fits you, not just a size chart.',
    '“This is my second purchase from Cavaier. The jewellery is so delicate but also hard wearing. Holds its colour, doesn’t tarnish.” – Maxwell S, verified buyer',
    f'Three days left at 30% off. {g.L("Shop the sale →")}',
    'Eli<br>Cavaier',
    ps('4.5 out of 5 from 2,179 reviews on Trustpilot.', 'See what people kept on →')])

t14 = g.textmail([
    'Hi {first name},',
    f'Four hours left. {g.L("Shop the last hours →")}',
    'At 23:59 CET tonight, 30% off ends and prices go back to normal. The jewelry case with any Set or two pieces ends with it.',
    'If something’s been sitting in your cart, now’s the time.',
    'Eli<br>Cavaier',
    ps('This is the last email about the sale.', 'Shop before midnight →')])

ENGAGED = 'ALL – Engaged 2 Years — big blasts'
POPUP = 'Newsletter Sign-Up (Pop Up)'
NOBUY = 'excl. placed order since Nov 23'

UPD = {
    '01': dict(time='19:00', subj=('Your early access is open', 'You go first this year'),
               pre='30% off everything, before anyone else. No code.', aud=f'{ENGAGED} + early-access pop-up sign-ups'),
    '02': dict(time='19:00', subj=('Early access ends Friday', 'Pick your Set before Friday'),
               pre='30% off now, before the public sale opens.', aud=f'{ENGAGED}, {NOBUY}'),
    '03': dict(subj=('Black Friday: 30% off everything', 'It’s here. 30% off, once a year.'),
               pre='No code. Ends Dec 6.', aud=f'{ENGAGED} + {POPUP}'),
    '04': dict(subj=('Save €28 on the 3x Minimal Set', 'The Sets, 30% off, case included'),
               pre='The biggest saving of Black Friday is in the Sets.', aud=f'{ENGAGED}, excl. placed order today'),
    '05': dict(subj=('The pieces people never take off', 'Rated 4.5/5 by 2,179 people'),
               pre='Now 30% off until Dec 6.', aud=f'{ENGAGED}, excl. placed order today'),
    '06': dict(aud=f'{ENGAGED} + {POPUP}, including Black Friday buyers: the drop is the reason to buy again'),
    '07': dict(time='19:00', aud=f'{ENGAGED}, {NOBUY}'),
    '08': dict(subj=('Cyber Week starts now: 7 days left', 'Still 30% off everything'),
               pre='Ends Sunday at midnight. No code.', aud=f'{ENGAGED} + {POPUP}, {NOBUY}'),
    '09': dict(time='19:00', aud=f'{ENGAGED}, {NOBUY}'),
    '10': dict(time='19:00', subj=('Gifts from €20.97', 'The gift guide, by price'), aud=f'{ENGAGED}'),
    '11': dict(time='19:00', aud=f'Clicked a BFCM email but no order, {NOBUY}'),
    '12': dict(time='19:00', subj=('2 days left at 30% off', 'Some sizes are almost gone [only if true]'),
               pre='Ends Sunday, 23:59 CET. Then it’s full price.', aud=f'{ENGAGED} + {POPUP}, {NOBUY}'),
    '13': dict(subj=('Last day: 30% off ends tonight', 'Once it ends, it ends'),
               pre='At 23:59 CET, prices go back to normal.', aud=f'{ENGAGED} + {POPUP}, {NOBUY}'),
    '14': dict(aud='Clicked any BFCM email in the last 14 days, no order'),
}

for s in g.SENDS:
    if s['n'] in E:
        s['fn'] = E[s['n']]
    if s['n'] in UPD:
        s.update(UPD[s['n']])
    s['text'] = {'07': t07, '09': t09, '11': t11, '14': t14}.get(s['n'], s.get('text'))
    if s['text'] is None:
        s.pop('text')

V5_CSS = """
/* ---- v5: conversion pass ---- */
.mproof{margin:2px 0 0;font:400 11px/1.4 var(--body);letter-spacing:.06em;color:var(--ink2)}
.mcta.tight{padding:4px 24px 26px}
.obar{display:flex;margin:24px 24px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.obar span{flex:1;text-align:center;padding:12px 6px;font:500 9.5px/1.35 var(--body);letter-spacing:.14em;text-transform:uppercase}
.obar span+span{border-left:1px solid var(--line)}
.data{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--canvas-line)}
.data div{padding:14px 12px 4px 0;display:flex;flex-direction:column;gap:4px;min-width:0}
.data div+div{padding-left:12px;border-left:1px solid var(--canvas-line)}
.data b{font:300 26px/1 var(--disp);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.data span{font-size:12.5px;line-height:1.45;color:var(--canvas-muted)}
.levers{margin:0;padding-left:18px;font-size:14px;line-height:1.6;max-width:680px}
.levers li+li{margin-top:6px}
@media (max-width:720px){.data{grid-template-columns:1fr 1fr}.data div:nth-child(3){padding-left:0;border-left:0}}
@media (max-width:480px){.obar{flex-direction:column}.obar span+span{border-left:0;border-top:1px solid var(--line)}}
"""

DATA_CARD = """
  <section class="card">
    <span class="kicker">What BFCM 2025 told us · Klaviyo, Nov 10 – Dec 7 2025</span>
    <h2>Clicks are the bottleneck, not opens.</h2>
    <div class="data">
      <div><b>50–59%</b><span>open rate on the engaged segment</span></div>
      <div><b>0.4–2.1%</b><span>click rate. Most opens never reached the site</span></div>
      <div><b>€0.071</b><span>best revenue per recipient: “BF almost sold out”, Nov 19</span></div>
      <div><b>€57</b><span>average order value across the sends</span></div>
    </div>
    <p>The same design was cloned about ten times, and unsubscribes climbed from 0.3% to 0.9%. The pop-up list opened at about 30% and earned less per send than the engaged segment.</p>
    <span class="kicker">What changes in every email this year</span>
    <ul class="levers">
      <li><b>A button in the first screen</b> of every designed email, plus product tiles that click straight through.</li>
      <li><b>The offer is stated the same way everywhere</b> (30% off everything · case with any Set or 2 pieces · no code), so nobody has to work it out.</li>
      <li><b>Proof sits next to the button:</b> 4.5 on Trustpilot from 2,179 reviews.</li>
      <li><b>Order value above €57:</b> the 3x Minimal Set (€66.47 with the case) leads the Sets email, and every email pushes the second piece for the case.</li>
      <li><b>A new design every send,</b> so it never feels like the same email again.</li>
      <li><b>Audiences:</b> the engaged 2-year segment carries the sequence. The pop-up list only gets the big moments (launch, Cyber Monday, final weekend, last day), and buyers are excluded from push emails but get the Matte Cuff drop.</li>
      <li><b>Scarcity, but only if true:</b> it was last year’s best performer. Email 12 has an “almost gone” subject B to use only if stock really is low.</li>
      <li><b>Text emails</b> now put the link in the first lines and end with a P.S. link.</li>
    </ul>
  </section>
"""

if __name__ == '__main__':
    tp = os.path.join(g.HERE, 'bfcm26.tpl.html')
    tpl = open(tp).read()
    if '/* ---- v5:' not in tpl:
        tpl = tpl.replace('</style>', V5_CSS + '</style>', 1)
    if 'What BFCM 2025 told us' not in tpl:
        tpl = tpl.replace('  <div class="tbl">', DATA_CARD + '\n  <div class="tbl">', 1)
    open(tp, 'w').write(tpl)
    html = v3.build()
    with cf.ThreadPoolExecutor(10) as ex:
        data = dict(ex.map(v3.fetch_bw, sorted(g.USED)))
    uri = {k: 'data:image/jpeg;base64,' + base64.b64encode(v).decode() for k, v in data.items()}
    html = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: uri[m.group(1)], html)
    assert 'warrant' not in html.lower()
    assert 'class="timer"' not in html
    open(os.path.join(g.HERE, 'cavaier-bfcm26-sequence.html'), 'w').write(html)
    print(len(g.USED), 'images,', len(html) // 1024, 'KB')
