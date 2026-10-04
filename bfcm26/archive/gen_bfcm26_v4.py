#!/usr/bin/env python3
"""v4: Matte Cuff as a proper drop, static deadlines instead of countdown timers."""
import base64, os, re, concurrent.futures as cf
import gen_bfcm26 as g
import gen_bfcm26_v2 as v2
import gen_bfcm26_v3 as v3
from gen_bfcm26 import img, strip, spec, cta, P, sale, eur, price_html, listrow, foot, PRE, LIVE, CW
from gen_bfcm26_v3 import hero, logobar, capttl, quote, review, casecard, crafted, msh

def deadline(label, big, sub):
    """Static deadline row: correct on the day it's sent, no live timer needed."""
    return (f'<div class="dl"><span class="lab">{label}</span><b>{big}</b></div>'
            f'<p class="tfb">{sub}</p>')

# ---------------------------------------------------------------- 02 · split, static "days left"
def e02():
    html = v3.e02()
    html = re.sub(r'<div class="vt">.*?</div></div>',
                  '<div class="vt"><div><b>2 days</b><span class="lab">until the public sale</span></div></div>', html, count=1, flags=re.S)
    return html.replace('Public sale opens Fri Nov 27, 07:00 CET', 'Early access ends Fri Nov 27, 07:00 CET')

# ---------------------------------------------------------------- 06 · THE DROP
def e06():
    details = [('01', 'Finish', 'Matte'), ('02', 'Material', '316L stainless steel'),
               ('03', 'Fit', 'Adjustable, one size'), ('04', 'Wear it', 'Water, gym, sleep')]
    return ''.join([
        '<div class="strip red">New drop · limited first batch · live now</div>',
        '<div class="tease"><span class="lab">One more thing</span><h2>You asked for it.</h2>'
        '<p class="copy">All year, one request kept coming back: the Minimal Cuff, without the shine. It’s here.</p></div>',
        hero('The Matte Cuff', 'Limited first batch · live now', 'Hero · B&W · Matte Cuff on wrist, dramatic side light · 600×800',
             btn='Get yours first', ratio='600/800', top='<span class="new">Drop 01</span> · Sat Nov 28'),
        '<div class="limited"><span class="lab red">Limited first batch</span>'
        '<p>We made one small run. When it’s gone, it’s gone until the next batch in [CEO to confirm: restock month].</p></div>',
        '<div class="dropgrid">'
        + g.ph('Matte Cuff · packshot on white', cls='dg1')
        + g.ph('Matte Cuff · macro of the matte surface', cls='dg2')
        + g.ph('Matte Cuff · worn, with a Set', cls='dg3') + '</div>',
        '<div class="details" style="margin-top:36px">' + ''.join(
            f'<div><span class="num">{n}</span><span class="lab">{a}</span><p>{b}</p></div>' for n, a, b in details) + '</div>',
        '<div class="dropprice"><span class="lab">The Matte Cuff</span><b>€39.95</b>'
        '<span class="small mute">New, so it’s full price. Not part of the Black Friday offer.</span>'
        '<a class="solid" href="#">Get yours first</a></div>',
        quote('Minimalistic but luxurious. Compliments every single day.', 'Nicole A'),
        msh('Make it two', '30% off'),
        g.grid([g.card('braid', 'braid-armband__3', ratio='tall'), g.card('ropeB', 'rope-bracelet-2__3', ratio='tall')], 2),
        '<div class="sec"></div>',
        casecard('The case is on us', 'Add any piece at 30% off to your Matte Cuff, and the jewelry case comes with it.', 'Get yours first'),
        '<p class="small mute center" style="padding:28px 40px 0">Ships with the rest of your Black Friday order.</p>',
        '<div style="height:44px"></div>', foot()])

# ---------------------------------------------------------------- 08 · static "7 days left"
def e08():
    html = v3.e08()
    return re.sub(r'<div class="timer">.*?</p>',
                  deadline('Cyber Week', '7 days left', 'Ends Sunday, Dec 6 at 23:59 CET'), html, count=1, flags=re.S)

# ---------------------------------------------------------------- 12 · the deadline is the hero
def e12():
    html = v3.e12()
    big = ('<div class="bigdl"><span class="lab">Final weekend</span><b>2 days left</b>'
           '<p class="small mute">The sale ends Sunday, Dec 6 at 23:59 CET. After that, it’s full price.</p></div>')
    html = re.sub(r'<div class="btimer">.*?</p></div>', big, html, count=1, flags=re.S)
    return html.replace('Full price, €39.95. Pairs with everything above, and counts toward the case.',
                        'Limited first batch, full price €39.95. Pairs with everything above and counts toward the case.')

# ---------------------------------------------------------------- 13 · static "ends tonight"
def e13():
    html = v3.e13()
    return re.sub(r'<div class="timer">.*?</p>',
                  deadline('Last day', 'Ends tonight', 'Sunday, Dec 6 at 23:59 CET'), html, count=1, flags=re.S)

t07 = g.textmail([
    'Hi {first name},',
    'A quick note from me, not a campaign.',
    'Everything on cavaier.com is 30% off until Sunday, December 6. It comes off at checkout, no code.',
    'If I had to pick three:',
    f'– The 3x Minimal Set. Three bracelets, worn together or apart. With the jewelry case included, it’s the best value we have. {g.L("See the Set")}<br>'
    f'– The Minimal Cuff. The one I never take off. €24.43 this week. {g.L("See the Cuff")}<br>'
    f'– The new Matte Cuff. We dropped it yesterday, and the first batch is small. If you want one, don’t wait. {g.L("See the Matte Cuff")}',
    'Everything is waterproof and made from 316L stainless steel. Shower, gym, sleep: it stays on.',
    g.L('Shop the sale →'),
    'Eli<br>Cavaier'])

FN = {'02': e02, '06': e06, '08': e08, '12': e12, '13': e13}
for s in g.SENDS:
    if s['n'] in FN:
        s['fn'] = FN[s['n']]
    if s['n'] == '06':
        s['subj'] = ('You asked for this one', 'One more thing')
        s['pre'] = 'The Matte Cuff. Limited first batch, live now.'
        s['job'] = ('A second launch the day after Black Friday. Budgets are spent, so it sells newness and scarcity, '
                    'not a discount: something they haven’t seen, in a small first batch.')
    if s['n'] == '07':
        s['text'] = t07
    if s['n'] == '12':
        s['job'] = 'Turn the deadline on: “2 days left” is the hero, then a short list of top pieces.'

V4_CSS = """
/* ---- v4: drop + static deadlines ---- */
.dl{display:flex;justify-content:space-between;align-items:baseline;margin:0 24px;padding:14px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.dl b{font:300 24px/1 var(--disp);letter-spacing:-.01em}
.bigdl{padding:52px 24px 0;display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center}
.bigdl b{font:300 64px/.95 var(--disp);letter-spacing:-.03em;color:var(--red)}
.bigdl + .mcta{padding-top:28px;padding-bottom:40px}
.vt b{font:300 40px/1 var(--disp);letter-spacing:-.02em}
.tease{padding:52px 32px 40px;text-align:center;display:flex;flex-direction:column;gap:14px;align-items:center}
.tease h2{margin:0;font:300 40px/1.05 var(--disp);letter-spacing:.04em;text-transform:uppercase}
.tease .copy{max-width:360px}
.limited{margin:36px 24px 0;padding:22px 24px;border:1px solid var(--red);display:flex;flex-direction:column;gap:8px;text-align:center;align-items:center}
.limited p{margin:0;font:300 14px/1.55 var(--body);max-width:400px}
.dropgrid{display:grid;grid-template-columns:1.3fr 1fr;grid-template-rows:auto auto;gap:6px;margin:36px 24px 0}
.dropgrid .dg1{grid-row:span 2;aspect-ratio:auto;min-height:420px}
.dropgrid .dg2,.dropgrid .dg3{aspect-ratio:1/1}
.dropprice{padding:40px 24px 8px;display:flex;flex-direction:column;align-items:center;gap:10px;text-align:center}
.dropprice b{font:300 44px/1 var(--disp);letter-spacing:-.02em}
.dropprice .solid{margin-top:12px}
@media (max-width:480px){.tease h2{font-size:30px}.bigdl b{font-size:48px}.dropgrid{grid-template-columns:1fr}.dropgrid .dg1{min-height:0;aspect-ratio:1/1}}
"""

if __name__ == '__main__':
    tp = os.path.join(g.HERE, 'bfcm26.tpl.html')
    tpl = open(tp).read()
    dup = (' Every designed email has its own layout, and the red (#C2371A) appears only where the holiday needs to be seen: '
           'the poster headlines, the launch label and the final countdown.')
    while tpl.count(dup) > 1:
        tpl = tpl.replace(dup, '', 1)
    tpl = tpl.replace('the poster headlines, the launch label and the final countdown.',
                      'the poster headlines, the drop label and the final deadline.')
    tpl = tpl.replace('<li>All send times are CET',
                      '<li>No live countdown timers: each email states the deadline as fixed text (“2 days left”, “Ends tonight”) that is true on its send day. If you want live timers later, Sendtric or MotionMail GIFs drop into a Klaviyo image block.</li>\n      <li>Matte Cuff: “limited first batch” only if the run really is limited, and the restock month needs filling in.</li>\n      <li>All send times are CET', 1)
    if '/* ---- v4:' not in tpl:
        tpl = tpl.replace('</style>', V4_CSS + '</style>', 1)
    open(tp, 'w').write(tpl)
    html = v3.build()
    with cf.ThreadPoolExecutor(10) as ex:
        data = dict(ex.map(v3.fetch_bw, sorted(g.USED)))
    uri = {k: 'data:image/jpeg;base64,' + base64.b64encode(v).decode() for k, v in data.items()}
    html = re.sub(r'\{\{IMG:([^}]+)\}\}', lambda m: uri[m.group(1)], html)
    assert 'warrant' not in html.lower()
    assert 'class="timer"' not in html and 'class="btimer"' not in html, 'live-timer block left'
    open(os.path.join(g.HERE, 'cavaier-bfcm26-sequence.html'), 'w').write(html)
    print(len(g.USED), 'images,', len(html) // 1024, 'KB')
