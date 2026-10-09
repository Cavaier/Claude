"""Cavaier Q4 2026 flows: every flow and email as data. Rendered by gen_q4.py.

Phases: pre (Oct 27–Nov 10) · ea (Nov 11–12, code BF26) · bf (Nov 13–30, incl. Black Friday Nov 27 and Cyber Monday) · cw (Dec 1–6) ·
xmas (Dec 7–10, cut-off Thu Dec 10) · late (Dec 11–24) · post (Dec 25–Jan 10).
Rules: 3–4 word subjects, 4–5 word previews, no FREE in subject/preview/banner/headline, no countdown timers,
no fixed prices in static content, Set not Stack, placeholders in [brackets].
"""

ALL = ['pre', 'ea', 'bf', 'cw', 'xmas', 'late', 'post']

def M(type, **kw):
    kw['type'] = type
    return kw

# ---------------------------------------------------------------- shared copy
B_WEL = {'pre': 'Early access · Opens Wed Nov 11', 'ea': '«ban» · 30% off is open',
         'bf cw': '«ban» · 30% off everything',
         'xmas': '«ban» · Order by Dec 10 for delivery', 'late': '«ban» · Gift cards arrive instantly',
         'post': 'New year · Made to stay on'}
B_REC = {'pre post': 'Jewelry case included · With 2+ pieces', 'ea': '«ban» · Members shop 30% off now',
         'bf cw': '«ban» · 30% off everything',
         'xmas': '«ban» · Order by Dec 10 for delivery', 'late': '«ban» · Gift cards arrive instantly'}
TAG = {'pre': 'From Nov 11 · 30% off', 'ea': 'Members 30% off', 'bf cw': '30% off', 'xmas': 'Gift pick',
       'late': 'Gift pick', 'post': 'Best seller'}
TAGR = {'pre post': 'Case with 2+', 'ea': 'Members 30% off', 'bf cw': '30% off', 'xmas': 'Gift picks', 'late': 'For next time'}
WHO = {'W': 'Nicole A · verified buyer', 'M': 'Maxwell S · verified buyer'}
# verified Trustpilot reviews, the same ones the campaigns use (send 11 / 04-B): first per gender, the second is Adam P for both
QUOTES = [{'W': 'Minimalistic but luxurious. Compliments every single day.', 'M': 'Holds its colour, doesn’t tarnish, and looks brilliant.'},
          {'W': 'Minimal yet eye-catching. Great value and fast delivery.', 'M': 'Minimal yet eye-catching. Great value and fast delivery.'}]
WHO2 = 'Adam P · verified buyer'
USP = M('usp_bar', items=['Water-friendly', 'Stainless steel', 'Hypoallergenic'])
OFFER = M('offer_bar', phases=['ea', 'bf', 'cw'], items=['30% off everything', {'ea': 'Code BF26', 'bf cw': 'No code'}, 'Case with 2+ pieces'])
CAL = M('shipping_calendar', phases=['xmas'])
def GC(title='Gift card, sent in minutes.', text='Pick an amount from €10, add a note, choose when it lands. They choose the piece.', cta='Send a gift card', phases=('late',)):
    return M('gift_card', phases=list(phases), title=title, text=text, cta=cta)
CASE = M('gift_box', img='p_case', kicker='Included', title='Jewelry case with 2+ pieces',
         text='Added at checkout automatically. Ready to give, or to keep.')
TICKET = M('ticket', phases=['pre', 'ea', 'bf', 'cw'], cells=[
    dict(label='Your price', value='30% off', sub='everything', red=True),
    dict(label='Code', value={'pre': 'Nov 11', 'ea': 'BF26', 'bf cw': 'None'}, sub={'pre': 'sent by email', 'ea': 'enter at checkout', 'bf cw': 'already on every price'}),
    dict(label={'pre': 'Opens', 'ea bf cw': '«endl»'}, value={'pre': 'Wed 11', 'ea bf cw': '«endv»'},
         sub={'pre': 'November', 'ea bf cw': '«ends»'})])
def TL_SALE():
    return [M('timeline', phases=['pre'], points=[dict(label='Today · On the list', state='now'), dict(label='Wed 11 · You shop first', state='next'), dict(label='Fri 13 · Everyone', state='end')]),
            M('timeline', phases=['ea'], points=[dict(label='Today · Members', state='now'), dict(label='Fri 13 · Everyone', state='end')]),
            M('timeline', phases=['xmas'], points=[dict(label='Today', state='now'), dict(label='Thu 10 · Last order', state='end'), dict(label='Fri 25 · Christmas', state='next')])]
DEADLINE = M('deadline', phases=['ea', 'bf', 'cw', 'xmas'], label='«endl»', value='«dl»')
SALE_LIST = M('offer_list', phases=['bf', 'cw'], rows=[['30% off everything', 'Already on every price, no code'], ['Two or more pieces', 'Jewelry case included'],
                                                        ['Shipping', 'Free on every order'], ['«endl»', '«dl»']])

C = lambda s: f'<code>{s}</code>'
TODAY = ('Today line: the «tokens» (kicker, big word, headline, line, subject, preview, button, deadline row) come from one saved block, “Q4 · Today”: ' +
         C("{% today '%Y-%m-%d' as d %}{% if d == '2026-11-13' %}…{% elif %}…") + ' — one line per sale day (see Plan → Urgency). Same chain in the subject and preview fields; check both in a test send before launch. Dates run on the account time zone.')
DATE = ('Phase blocks switch inside one template: ' + C("{% today '%Y-%m-%d' as d %}") +
        ' — pre &lt; 2026-11-11 ≤ ea &lt; 11-13 ≤ bf &lt; 12-01 ≤ cw &lt; 12-07 ≤ xmas &lt; Dec 10 ≤ late &lt; 12-25 ≤ post.')
GEN = 'W/M: show/hide on ' + C("person|lookup:'Gender'") + ' (“Men” → M, else W).'
SET = C("|find_replace:'Stack Set|Set'")
VIEW = ('Fields: ' + C('event.ProductName') + SET + ', ' + C('event.ImageURL') + ', ' + C('event.Price') + ' (text, shopper’s currency), ' +
        C('event.URL') + '; feed blocks filter on ' + C('event.Categories') + '.')
CART = ('Fields: ' + C("event|lookup:'Product Name'") + SET + ', ' + C('event.ImageURL') + ', ' + C("event|lookup:'Variant Name'") + ', ' +
        C('event.Price') + ' + ' + C("event|lookup:'$currency'") + ', ' + C('event.URL') + '.')
CHK = ('Table over ' + C('event.extra.line_items') + ' (image, title' + SET + ', variant_title, quantity, line_price + presentment_currency; '
       'Jewelry Case row prints “Included”); discount ' + C("event|lookup:'Total Discounts'") + '; total ' + C("event|lookup:'$value'") +
       '; button ' + C('event.extra.responsive_checkout_url') + '.')

# ================================================================= F1 Welcome
F1 = dict(id='F1', name='Q4 Welcome · Early Access', trigger_short='Joined list (pop-up)',
  replaces='Welcome Series (QVmUhV) → Manual on Oct 27',
  trigger='Added to List: BFCM pop-up / newsletter list (form SyHM2E, source POPUP26)',
  filters='Never been in this flow · smart sending on except E1', exits='Placed Order → moves into Post-purchase (F6)',
  live='Oct 27 → Jan 10 · all seven phases, copy switches by date',
  why='Sign-ups spike in Q4 and decide fast. One welcome that is a members’ pass before Nov 11, a 30%-off welcome in the sale, a gifting welcome in December and a gift-card welcome after the cut-off. No welcome flow sent in Q4 2025.',
  emails=[])

F1['emails'].append(dict(id='F1E1', name='The pass', delay='Immediately', delay_short='0', phases=ALL, bg='white', banner=B_WEL,
  subject={'pre': 'You’re on the list.', 'ea': 'Your access is open.', 'bf cw': 'Your 30% is waiting.',
           'xmas': 'Welcome. Gifts, sorted.', 'late': 'Welcome. Gift in minutes.', 'post': 'Welcome to Cavaier.'},
  preview={'pre': 'First access: Wednesday, Nov 11.', 'ea bf cw': '«prev»', 'xmas': 'Order by Dec 10 for Christmas.', 'late': 'Digital gift cards, sent instantly.',
           'post': 'Jewelry made to stay on.'},
  goal='One job per phase: save the date (pre), shop first (ea), shop 30% (bf/cw), shop gifts before the cut-off (xmas), send a gift card (late).',
  urgency='Today line (kicker, sub, button, ticket): the reason to act today, from the send date. The end date only shows when it’s close.',
  klaviyo='Trigger: Added to List. Send immediately, smart sending off. ' + TODAY + ' ' + DATE + ' ' + GEN + ' Product cards static (no prices).',
  modules=[
    M('big_type', kicker={'pre': 'Early access · Member', 'ea bf cw': '«kick»',
                          'xmas late post': 'Welcome to Cavaier'},
      big={'pre ea': 'You’re in.', 'bf cw': '30%', 'xmas': 'Gifts.', 'late': 'Minutes.', 'post': 'Welcome.'},
      title={'pre': 'First pick, Wednesday Nov 11.', 'ea': '30% off with BF26. Before everyone.', 'bf cw': 'off everything. No code.',
             'xmas': 'They’ll never take them off.', 'late': 'That’s how fast a gift card arrives.', 'post': 'Jewelry you never take off.'},
      sub={'pre': 'Members shop 30% off everything before the public sale. We’ll email you the moment it opens.',
           'ea bf cw': '«line»',
           'xmas': 'Water-friendly stainless steel, made to be worn every day. Order by Dec 10 for Christmas delivery.',
           'late': 'Too late for shipping, not for a gift. Pick an amount and it lands in their inbox.',
           'post': 'Minimal pieces made for real life: shower, sea, gym, sleep.'}),
    TICKET, *TL_SALE()[:2],
    M('cta', label={'pre': 'Save the date', 'ea bf cw': '«cta»', 'xmas': 'Shop the gifts',
                    'late': 'Send a gift card', 'post': 'Shop best sellers'},
      note={'pre': 'Adds Wed Nov 11 to your calendar.', 'ea': 'Code BF26. Members only until Friday, Nov 13.'}),
    M('hero_photo', img={'W': 'lf_w_3x_set', 'M': 'lf_m_3x_set'}, shape='wide'),
    CAL, GC(),
    M('section_header', title={'pre': 'Start here', 'ea bf cw': 'Start here', 'xmas': 'Gift picks', 'late': 'For yourself', 'post': 'Best sellers'},
      label={'pre': 'From Nov 11 · 30% off', 'ea bf': '30% off', 'cw': 'Gifts · 30% off', 'xmas late post': 'Case included with 2+'}),
    M('product_grid', cols=2, items=[
        dict(gender='W', img='p_set_w', name='3x Minimal Set', finish=['k', 'g'], tag=TAG),
        dict(gender='W', img='p_crystal_neck_worn', name='Crystal Necklace', finish=['k', 's', 'g'], tag=TAG),
        dict(gender='M', img='p_set_m', name='3x Minimal Set', finish=['k', 's', 'g'], tag=TAG),
        dict(gender='M', img='p_cube_pend_worn', name='Cube Pendant Necklace', finish=['k', 's', 'g'], tag=TAG)]),
    CASE, USP,
    M('cta', label={'pre': 'See the Sets', 'ea': 'Shop early access', 'bf cw': 'Shop the sale', 'xmas': 'Shop the gifts', 'late': 'Send a gift card',
                    'post': 'Shop all'}, proof=True)]))

F1['emails'].append(dict(id='F1E2', name='The Set', delay='+1 day', delay_short='+1d', phases=ALL, bg='fog', banner=B_WEL,
  subject={'pre': 'Pick your Set first.', 'ea': 'Your Set, 30% off.', 'bf cw': 'The Sets, 30% off.', 'xmas': 'The gift: a Set.',
           'late': 'Gift cards, sent instantly.', 'post': 'Start with a Set.'},
  preview={'pre': 'Shortlist now. Shop Nov 11.', 'ea': 'Best sellers, members first.', 'bf cw': 'Three pieces, one tap.',
           'xmas': 'Ready to give, case included.', 'late': 'They choose. You look good.', 'post': 'The pieces worn every day.'},
  goal='Sell the Set: the highest-value piece, and three pieces trigger the jewelry case.',
  urgency='Phase deadline under the grid; members-first in ea; cut-off line in xmas.',
  klaviyo='Smart sending on. ' + DATE + ' ' + GEN,
  modules=[
    M('headline', align='left', size='xl', title='Three pieces. One decision.',
      sub='Our best-selling Sets: matched, ready to wear, ready to give. Black first.',
      cta={'pre': 'See the Sets', 'ea bf cw post': 'Shop the Sets', 'xmas': 'Shop gift Sets', 'late': 'Send a gift card'}),
    M('split', img={'W': 'p_set_w_gold', 'M': 'p_set_m'}, kicker='Best seller', title='3x Minimal Set',
      body='Black, silver or gold. Three stainless-steel bracelets made to stack, and to stay on in the shower, the sea and the gym.', cta='Shop the Set'),
    M('section_header', title='Pick your finish', label='Black first'),
    M('product_grid', cols=3, items=[
        dict(gender='W', img='p_set_w', name='3x Minimal Set', finish=['k'], tag=TAG),
        dict(gender='W', img='p_set_w_gold', name='3x Minimal Set', finish=['g'], tag=TAG),
        dict(gender='W', img='p_braid_silver', name='Braid Bracelet', finish=['s'], tag=TAG),
        dict(gender='M', img='p_set_m', name='3x Minimal Set', finish=['k'], tag=TAG),
        dict(gender='M', img='p_set_m_silver', name='3x Minimal Set', finish=['s'], tag=TAG),
        dict(gender='M', img='p_stacked', name='4x Stacked Set', finish=['k'], tag=TAG)]),
    M('offer_list', phases=['ea', 'bf', 'cw'], rows=[['30% off', {'ea': 'Code BF26 at checkout', 'bf cw': 'Already on every price, no code'}], ['Two or more pieces', 'Jewelry case included'],
                                                    ['Shipping', 'Free on every order'], ['«endl»', '«dl»']]),
    M('promise', phases=['pre'], text='Every Set here is 30% off for members from Wednesday, Nov 11, with the code we email you that morning.'),
    M('promise', phases=['xmas'], text='A Set is three gifts in one box. Order by Dec 10 for Christmas.'),
    M('promise', phases=['post'], text='Three pieces, worn every day. Start there.'),
    GC(title='Can’t ship in time? Give the choice.', text='A digital gift card lands in their inbox in minutes. From €10.'),
    M('quote', count=1, who=WHO),
    M('cta', label={'pre': 'See the Sets', 'ea': '«cta»', 'bf cw': 'Shop the Sets at 30% off', 'xmas': 'Shop gift Sets',
                    'late': 'Send a gift card', 'post': 'Shop the Sets'}, proof=True)]))

F1['emails'].append(dict(id='F1E3', name='Made to stay on', delay='+2 days', delay_short='+2d', phases=ALL, bg='white', banner=B_WEL,
  subject={'pre': 'Shower. Gym. Sleep.', 'ea': 'Made to stay on.', 'bf cw': 'Worn daily. 30% off.', 'xmas': 'A gift worn daily.',
           'late': 'Worn daily, gifted instantly.', 'post': 'Made to stay on.'},
  preview={'pre': 'Why nobody takes them off.', 'ea': 'And members save 30%.', 'bf cw': 'Rated 4.5 on Trustpilot.',
           'xmas': 'Water-friendly steel, case included.', 'late': 'Gift cards arrive in minutes.', 'post': 'Rated 4.5 on Trustpilot.'},
  goal='Kill the doubts (tarnish, water, skin, fit) with product facts and proof, then sell.',
  urgency='Deadline row in ea/bf/cw/xmas.', klaviyo='Smart sending on. ' + DATE + ' ' + GEN,
  modules=[
    M('hero_photo', img={'W': 'lf_w_wet_swim', 'M': 'lf_m_bw_fist'}, shape='tall'),
    M('headline', title='Put it on once. Live in it.', sub='Shower, sea, gym, sleep. Stainless steel that doesn’t rust, tarnish or come off.'),
    M('checklist', items=['Water-friendly, sweat- and heat-resistant', 'Recycled 316L stainless steel', 'Hypoallergenic, kind to skin',
                          'Adjustable with the extension chain']),
    M('score'), M('quote', count=2, who=WHO),
    M('section_header', title='The ones people keep on', label=TAG),
    M('product_grid', cols=3, items=[
        dict(gender='W', img='p_crystal_br', name='Crystal Bracelet', tag=TAG), dict(gender='W', img='p_braid_silver', name='Braid Bracelet', tag=TAG),
        dict(gender='W', img='p_cube_br_w', name='Cube Bracelet', tag=TAG), dict(gender='M', img='p_braid_black', name='Braid Bracelet', tag=TAG),
        dict(gender='M', img='p_cube_br_m', name='Cube Bracelet', tag=TAG), dict(gender='M', img='p_cuff_worn', name='Minimal Cuff', tag=TAG)]),
    DEADLINE, GC(),
    M('cta', label={'pre': 'Find your piece', 'ea': 'Shop early access', 'bf cw': 'Shop 30% off', 'xmas': 'Shop the gifts', 'late': 'Send a gift card',
                    'post': 'Find your piece'})]))

F1['emails'].append(dict(id='F1E4', name='The push', delay='+3 days', delay_short='+3d', phases=ALL, bg='white', banner=B_WEL,
  subject={'pre': 'Nov 11. You’re first.', 'ea bf cw xmas late': '«subj»', 'post': 'Your first piece.'},
  preview={'pre': 'Members shop 30% off first.', 'ea bf cw xmas late': '«prev»', 'post': 'Case included with two pieces.'},
  goal='The loudest welcome email: today’s reason, huge, and one button.',
  urgency='Giant today word (“Today.”, “New.”, “Tomorrow.”, “Tonight.”) + today line; the end date only when it’s 3 days away or less.', klaviyo='Smart sending on. ' + TODAY + ' ' + DATE + ' ' + GEN,
  modules=[
    M('big_type', kicker={'pre': 'Early access', 'ea bf cw xmas late': '«kick»', 'post': 'New year'},
      big={'pre': 'Nov 11', 'ea bf cw xmas late': '«big»', 'post': '2027.'},
      title={'pre': 'You shop first.', 'ea bf cw xmas late': '«head»', 'post': 'Something you’ll wear every day.'},
      sub={'pre': 'Members get 30% off everything on Nov 11 and 12 with a code we email that morning, before the public sale on Friday, Nov 13.',
           'ea bf cw xmas late': '«line»',
           'post': 'Start the year with a piece made to stay on.'}),
    M('cta', label={'pre': 'Add to calendar', 'ea bf cw xmas late': '«cta»', 'post': 'Shop best sellers'}),
    *TL_SALE(),
    M('hero_photo', img={'W': 'lf_w_black_top', 'M': 'lf_m_linen_chin'}, shape='wide'),
    OFFER, CAL, GC(),
    M('section_header', title='Best sellers', label=TAG),
    M('product_feed', source='bestsellers', count=3),
    M('cta', label={'pre': 'See the Sets', 'ea bf cw xmas late': '«cta»', 'post': 'Shop best sellers'}, proof=True)]))

F1['emails'].append(dict(id='F1E5', name='The Set', delay='+4 days', delay_short='+4d', phases=['ea', 'bf', 'cw', 'xmas'], bg='fog', banner=B_WEL,
  subject='«subj»', preview='«prev»',
  goal='Close the welcome on today’s reason; the real deadline only once it’s close.',
  urgency='Today headline + today row + single hero product.',
  klaviyo='Live Nov 11 → Dec 10 only; set to Manual outside (no date-based skip exists in a flow). ' + TODAY + ' ' + DATE + ' ' + GEN,
  notes='Doesn’t send in pre, late or post.',
  modules=[
    M('headline', size='xl', kicker='«kick»', title='«head»', sub='«line»'),
    M('deadline', label='«endl»', value='«dl»'),
    M('split', reverse=True, img={'W': 'p_set_w', 'M': 'p_set_m_silver'}, kicker='Best seller', title='3x Minimal Set',
      body='If you get one thing, get the Set. Three pieces, and the jewelry case comes with it.', cta='Shop the Set'),
    M('quote', count=1, who=WHO),
    M('offer_list', phases=['ea', 'bf', 'cw'], rows=[['30% off', {'ea': 'Code BF26 at checkout', 'bf cw': 'Already on every price, no code'}], ['Two or more pieces', 'Jewelry case included'],
                                                    ['Shipping', 'Free on every order']]),
    M('offer_list', phases=['xmas'], rows=[['Christmas delivery', 'Order by Dec 10'], ['Two or more pieces', 'Jewelry case included'],
                                         ['Shipping', 'Free on every order']]),
    M('cta', label='«cta»', proof=True)]))

# ================================================================= F2 Browse
F2 = dict(id='F2', name='Q4 Browse Abandonment', trigger_short='Viewed Product', replaces='Browse Abandonment (RkFCNW) → Manual on Oct 27',
  trigger='Viewed Product (HtsYBH)',
  filters='No Added to Cart, Checkout Started or Placed Order since starting · not in this flow in the last 3 days · smart sending on',
  exits='Added to Cart / Checkout Started / Placed Order', live='Oct 27 → Jan 10',
  why='The biggest audience of any flow (20,138 recipients in Q4 2025) at only €0.35 per recipient. Faster first touch, the product front and centre, a real reason to act in each phase, and a third email in the sale and Christmas windows.',
  emails=[])

F2['emails'].append(dict(id='F2E1', name='Still looking?', delay='2 hours after viewing', delay_short='2h', phases=ALL, bg='white', banner=B_REC,
  subject={'pre post': 'Still thinking about it?', 'ea': 'Your code takes 30% off this.', 'bf cw': 'It’s 30% off now.', 'xmas': 'Gift it by Christmas.', 'late': 'Too late to ship?'},
  preview={'pre post': 'It’s still here for you.', 'ea': 'Code BF26, until Thursday.', 'bf cw': '«prev»',
           'xmas': 'Order by Thu Dec 10.', 'late': 'Send a gift card instead.'},
  goal='Bring them back to the exact piece with the phase’s reason to buy now.',
  urgency='bf/cw: 30% now + today line in the preview; xmas: cut-off; ea: join to unlock. Pre/post: no sale talk (don’t make October shoppers wait).',
  klaviyo='Trigger Viewed Product. ' + VIEW + ' ' + TODAY + ' ' + DATE,
  modules=[
    M('headline', title={'pre post': 'Made to stay on.', 'ea': 'Members save 30% on this.', 'bf cw': 'It’s 30% off right now.',
                         'xmas': 'Give it before Christmas.', 'late': 'Too late to ship. Not to give.'},
      sub={'pre post': 'The piece you looked at: water-friendly stainless steel, made to be worn every day.',
           'ea': 'Early access is open. Your code BF26 takes 30% off this until Thursday, before Friday’s public sale.',
           'bf cw': 'The piece you looked at is 30% off right now. No code needed.',
           'xmas': 'Order by Thu Dec 10 and it arrives before Christmas.',
           'late': 'Christmas shipping has closed. A gift card lands in their inbox in minutes.'}),
    M('dynamic_product', source='viewed', size='big'),
    M('cta', label={'pre post': 'Take another look', 'ea': 'Use code BF26', 'bf cw': 'Get it at 30% off', 'xmas': 'Order for Christmas', 'late': 'Send a gift card'}),
    M('usp_bar', items=['Water-friendly', 'Stainless steel', 'Rated 4.5 on Trustpilot']),
    GC(),
    M('section_header', title='You might also like', label=TAGR),
    M('product_feed', source='viewed_together', count=3)]))

F2['emails'].append(dict(id='F2E2', name='Worth it', delay='+1 day', delay_short='+1d', phases=ALL, bg='fog', banner=B_REC,
  subject={'pre post': 'Worth a second look.', 'ea': 'Still 30% for members.', 'bf cw': 'Still 30% off.', 'xmas': 'The gift they’ll wear.', 'late': 'A gift, in minutes.'},
  preview={'pre post': 'Rated 4.5 on Trustpilot.', 'ea': 'Code BF26, until Thursday.', 'bf cw': '«prev»',
           'xmas': 'Case included with two pieces.', 'late': 'Digital gift card, sent instantly.'},
  goal='Proof and reassurance for the piece they viewed.', urgency='Today row in ea/bf/cw/xmas.',
  klaviyo='As F2E1. ' + VIEW,
  modules=[
    M('score'),
    M('headline', title='Worth it. Ask them.',
      sub={'pre post': 'Rated 4.5 on Trustpilot from 3,000+ reviews.', 'ea': 'Rated 4.5 on Trustpilot, and 30% off for members now.',
           'bf cw': 'Rated 4.5 on Trustpilot from 3,000+ reviews, and still 30% off.', 'xmas': 'Rated 4.5 on Trustpilot. A gift they’ll actually wear.',
           'late': 'Rated 4.5 on Trustpilot. Let them choose with a gift card.'}),
    M('dynamic_product', source='viewed', size='side'),
    M('quote', count=1, who=WHO),
    M('checklist', items=['Water-friendly: shower, sea, gym', 'Hypoallergenic stainless steel', 'Adjustable size']),
    dict(CASE, phases=['pre', 'xmas', 'post']), DEADLINE, GC(),
    M('cta', label={'pre post': 'Back to your piece', 'ea': 'Use code BF26', 'bf cw': 'Get it at 30% off', 'xmas': 'Order for Christmas', 'late': 'Send a gift card'})]))

F2['emails'].append(dict(id='F2E3', name='Why today', delay='+2 days', delay_short='+2d', phases=['bf', 'cw', 'xmas'], bg='white', banner=B_REC,
  subject='«subj»', preview='«prev»',
  goal='One reason to buy it today, with the product. The end date only when it’s close.', urgency='Giant today word + today line.',
  klaviyo='Live Nov 13 → Dec 10; Manual outside. ' + VIEW + ' ' + TODAY + ' ' + DATE, notes='Doesn’t send in pre, ea, late or post.',
  modules=[
    M('big_type', kicker='«kick»', big='«big»', title='«head»', sub='«line»'),
    M('timeline', phases=['xmas'], points=[dict(label='Today', state='now'), dict(label='Thu 10 · Last order', state='end')]),
    M('dynamic_product', source='viewed', size='big'),
    dict(OFFER, phases=['bf', 'cw']), CAL,
    M('cta', label='«cta»', proof=True)]))

# ================================================================= F3 Collection / search
F3 = dict(id='F3', name='Q4 Collection Browse', trigger_short='Viewed Collection', replaces='NEW',
  trigger='Viewed Collection (Shopify, TK8Zdc)',
  filters='No Viewed Product since starting (F2 takes over) · no Added to Cart or Placed Order · not in this flow in 7 days',
  exits='Viewed Product / Added to Cart / Placed Order', live='Oct 27 → Jan 10',
  why='People who browse collections or search but never open a product get nothing today. In gifting season they are the biggest undecided group: a gift guide sorts them by who they’re buying for.',
  emails=[])

GUIDE = M('gift_guide', tiles=[dict(img='lf_w_crossed', label='For her'), dict(img='lf_m_linen_chest', label='For him'),
                                dict(img='p_set_m_silver', label='The Sets', sub='3 pieces'), dict(img='p_giftcard', label='Gift card', sub='Instant · full price')])
F3['emails'].append(dict(id='F3E1', name='The gift guide', delay='3 hours after', delay_short='3h', phases=ALL, bg='white', banner=B_REC,
  subject={'pre post': 'Find their piece.', 'ea': 'Your 30% gift guide.', 'bf cw': 'Gift guide: 30% off.', 'xmas': 'The Christmas gift guide.', 'late': 'Gifts that arrive instantly.'},
  preview={'pre post': 'For her, him, or you.', 'ea': 'Members shop first, 30% off.', 'bf cw': 'Every piece, no code needed.',
           'xmas': 'Order by Thu Dec 10.', 'late': 'Send a gift card now.'},
  goal='Sort an undecided browser by recipient, then into a product page.', urgency='Phase offer bar / cut-off calendar.',
  klaviyo='Trigger Viewed Collection. ' + DATE + ' Feed blocks: best sellers.',
  notes='Viewed Collection event fields not checked yet: add the collection name to the headline once confirmed.',
  modules=[
    M('headline', kicker={'pre post': 'Gift guide', 'ea': 'Early access · Gift guide', 'bf cw': '30% off · Gift guide', 'xmas': 'Christmas gift guide',
                          'late': 'Last-minute gifts'}, title='Who are you shopping for?', sub='Start with who it’s for. We’ll take it from there.'),
    GUIDE, OFFER, CAL, GC(),
    M('section_header', title='Best sellers', label=TAGR), M('product_feed', source='bestsellers', count=3),
    M('cta', label={'pre post': 'Shop the gift guide', 'ea': 'Shop with code BF26', 'bf cw': 'Shop the gift guide', 'xmas': 'Shop for Christmas',
                    'late': 'Send a gift card'}, proof=True)]))

F3['emails'].append(dict(id='F3E2', name='Start here', delay='+1 day', delay_short='+1d', phases=ALL, bg='fog', banner=B_REC,
  subject={'pre post': 'Our best sellers.', 'ea bf cw': 'Best sellers, 30% off.', 'xmas': 'Our best-selling gifts.', 'late': 'Best gift: the choice.'},
  preview={'pre post': 'Start with the Set.', 'ea bf cw': '«prev»',
           'xmas': 'Order by Thu Dec 10.', 'late': 'Gift cards arrive in minutes.'},
  goal='Hand the undecided the safest first pick.', urgency='Today row.', klaviyo='As F3E1. ' + TODAY,
  modules=[
    M('hero_photo', img={'W': 'lf_w_black_bracelet', 'M': 'lf_m_wrist_close'}, shape='tall'),
    M('headline', align='left', title='Start here.', sub='The pieces most people choose first, and keep on.'),
    M('product_feed', source='bestsellers', count=3),
    M('split', img={'W': 'p_set_w', 'M': 'p_set_m'}, kicker='Best seller', title='3x Minimal Set',
      body='Three pieces, one decision, and the jewelry case comes with it.', cta='Shop the Set'),
    DEADLINE, GC(),
    M('cta', label={'pre post': 'Shop best sellers', 'ea': 'Use code BF26', 'bf cw': 'Shop 30% off', 'xmas': 'Shop for Christmas', 'late': 'Send a gift card'})]))

# ================================================================= F4 Cart
F4 = dict(id='F4', name='Q4 Add to Cart', trigger_short='Added to Cart', replaces='Add to Cart Abandoned (Syiqdb) → Manual on Oct 27',
  trigger='Added to Cart (Shopify, WBpdcS) — not the API metric, silent since Sep 2',
  filters='No Checkout Started or Placed Order since starting · not in this flow in 3 days · smart sending on',
  exits='Checkout Started / Placed Order', live='Oct 27 → Jan 10',
  why='€8,643 at €0.86 per recipient in Q4 2025. Faster first touch, a pair-and-case push to lift order value, and a real-deadline third email.',
  emails=[])

F4['emails'].append(dict(id='F4E1', name='Still yours', delay='1 hour after', delay_short='1h', phases=ALL, bg='white', banner=B_REC,
  subject={'pre post': 'Still in your cart.', 'ea': 'Your cart, 30% off?', 'bf cw': 'Your cart, 30% off.', 'xmas': 'Your gift is waiting.', 'late': 'Too late? Gift card.'},
  preview={'pre post': 'We saved it for you.', 'ea': 'Code BF26, until Thursday.', 'bf cw': 'Already on every price.',
           'xmas': 'Order by Thu Dec 10.', 'late': 'Arrives in their inbox instantly.'},
  goal='One tap back to the cart.', urgency='Phase line under the product.', klaviyo='Trigger Shopify Added to Cart. ' + CART + ' ' + DATE,
  modules=[
    M('headline', size='xl', title='Still yours.',
      sub={'pre post': 'We saved your pick. Two pieces or more and the jewelry case comes with it.',
           'ea': 'Code BF26 takes 30% off this at checkout, until Thursday.',
           'bf cw': 'We saved your pick, and it’s already 30% off.',
           'xmas': 'We saved your pick. Order by Dec 10 for Christmas delivery.',
           'late': 'Shipping won’t make Christmas now. A gift card will.'}),
    M('dynamic_product', source='cart', size='big'),
    M('cta', label={'pre post': 'Return to cart', 'ea': 'Check out with BF26', 'bf cw': 'Check out at 30% off', 'xmas': 'Check out for Christmas', 'late': 'Send a gift card'}),
    M('gift_box', phases=['pre', 'ea', 'bf', 'cw', 'xmas', 'post'], img='p_case', kicker='Add one more', title='Two pieces, case included',
      text='Add a second piece and the jewelry case is added at checkout.'),
    GC(), OFFER]))

F4['emails'].append(dict(id='F4E2', name='Better in pairs', delay='+6 hours', delay_short='+6h', phases=ALL, bg='fog', banner=B_REC,
  subject={'pre post': 'Make it a pair.', 'ea': 'Pair it, save 30%.', 'bf cw': 'Pair it at 30%.', 'xmas': 'Make it a set.', 'late': 'Or a gift card.'},
  preview={'pre post': 'Two pieces, case included.', 'ea': 'Members shop first, 30% off.', 'bf cw': 'Two pieces, case included.',
           'xmas': 'Two gifts, one case.', 'late': 'Arrives in minutes, by email.'},
  goal='Lift order value: the cart item plus a second piece, case included.', urgency='Sale list / deadline row.',
  klaviyo='As F4E1. Feed: “Viewed together” for ' + C('event.ProductID') + '.',
  modules=[
    M('headline', align='left', title='Better in pairs.', sub='What you picked, plus a piece that goes with it. Two pieces and the jewelry case comes with them.'),
    M('dynamic_product', source='cart', size='side'),
    M('section_header', title='Goes with it', label='Case included with 2+'),
    M('product_feed', source='viewed_together', count=3),
    M('gift_box', img='p_case_open', kicker='Included', title='Jewelry case', text='Two pieces or more and it’s in the box. Ready to give.'),
    SALE_LIST, dict(DEADLINE, phases=['ea', 'xmas']), GC(),
    M('cta', label={'pre post': 'Complete the pair', 'ea': 'Use code BF26', 'bf cw': 'Pair it at 30% off', 'xmas': 'Order for Christmas', 'late': 'Send a gift card'})]))

F4['emails'].append(dict(id='F4E3', name='Why today', delay='+1 day', delay_short='+1d', phases=['pre', 'ea', 'bf', 'cw', 'xmas', 'post'], bg='white', banner=B_REC,
  subject={'pre post': 'Last reminder: your cart.', 'ea bf cw xmas': '«subj»'},
  preview={'pre post': 'Water-friendly steel, made to stay.', 'ea xmas': '«prev»', 'bf cw': 'Your cart, still 30% off.'},
  goal='Close the cart today: the day’s reason, the end date only when it’s close.', urgency='Giant today word + today row.', klaviyo='As F4E1. ' + TODAY, notes='Doesn’t send in late (F4E1 already offers the gift card).',
  modules=[
    M('big_type', kicker={'pre post': 'Your cart', 'ea bf cw xmas': '«kick»'},
      big={'pre post': 'Still here.', 'ea bf cw xmas': '«big»'},
      title={'pre post': 'Your pick is waiting.', 'ea bf cw xmas': '«head»'}),
    dict(DEADLINE, phases=['ea', 'bf', 'cw', 'xmas']),
    M('dynamic_product', source='cart', size='big'),
    M('quote', count=1, who=WHO),
    M('cta', label={'pre post': 'Return to cart', 'ea xmas': '«cta»', 'bf cw': 'Check out at 30% off'}, proof=True)]))

# ================================================================= F5 Checkout
F5 = dict(id='F5', name='Q4 Checkout Recovery', trigger_short='Checkout Started', replaces='Checkout Abandoned (Ub2mSt) → Manual on Oct 27',
  trigger='Checkout Started (Shopify, LrhH24) — not the API “Started Checkout”', filters='No Placed Order since starting · smart sending off for E1',
  exits='Placed Order', live='Oct 27 → Jan 10',
  why='The top earner: €10,886 at €1.37 per recipient in Q4 2025, and the first email did most of it (€1.90–2.02 per recipient). Keep the fast first touch, show the real cart and total, then delivery certainty and proof, and end on the real deadline.',
  emails=[])

F5['emails'].append(dict(id='F5E1', name='One step left', delay='45 minutes after', delay_short='45m', phases=ALL, bg='white', banner=B_REC,
  subject={'pre ea bf cw post': 'One step left.', 'xmas': 'One step to Christmas.', 'late': 'Your order is saved.'},
  preview={'pre post': 'Your order is saved.', 'ea': 'Finish before the public sale.', 'bf cw': 'Your 30% is already applied.',
           'xmas': 'Order by Thu Dec 10.', 'late': 'Or send a gift card.'},
  goal='Back to checkout in one tap, with the real total.', urgency='Today row in ea/bf/cw/xmas.',
  klaviyo='Trigger Shopify Checkout Started. ' + CHK + ' ' + TODAY + ' ' + DATE,
  modules=[
    M('headline', title={'pre ea bf cw post': 'One step left.', 'xmas': 'One step to Christmas.', 'late': 'Your order is saved.'},
      sub={'pre post': 'Everything you picked is saved. Finish in one tap.', 'ea': 'Enter code BF26 at checkout: 30% off, until Thursday.', 'bf cw': 'Your order is saved, with 30% off already applied.',
           'xmas': 'Finish by Thu Dec 10 and it arrives before Christmas.',
           'late': 'Christmas delivery has closed. Finish it for yourself, or send a gift card.'}),
    M('order_table'),
    M('cta', label='Complete my order', note='Questions? Reply to this email.'),
    DEADLINE, GC(text='A digital gift card lands in their inbox in minutes. From €10.')]))

F5['emails'].append(dict(id='F5E2', name='No surprises', delay='+4 hours', delay_short='+4h', phases=ALL, bg='fog', banner=B_REC,
  subject={'pre ea post': 'No surprises at checkout.', 'bf cw': 'Shipping is on us.', 'xmas': 'Arrives before Christmas.', 'late': 'Need it by Christmas?'},
  preview={'pre ea post': 'Here’s exactly what to expect.', 'bf cw': 'Included on every order.', 'xmas': 'Delivery dates, by country.',
           'late': 'A gift card arrives instantly.'},
  goal='Kill cost and delivery doubts.', urgency='Cut-off calendar in xmas.', klaviyo='As F5E1. Compact table.',
  modules=[
    M('headline', title='No surprises.', sub={'pre ea post': 'Here’s exactly what happens when you finish.', 'bf cw': 'Shipping is on us, and 30% is already off.',
                                             'xmas': 'Order by your country’s date below and it arrives before Christmas.',
                                             'late': 'Christmas delivery has closed. Here’s what still works.'}),
    M('offer_list', phases=['bf', 'cw'], rows=[['Shipping', 'Free on every order'], ['30% off', 'Already applied'], ['Two or more pieces', 'Jewelry case included'], ['Checkout', 'Secure']]),
    M('offer_list', phases=['pre', 'ea', 'xmas', 'late', 'post'], rows=[['Shipping', 'Free on every order'], ['Two or more pieces', 'Jewelry case included'], ['Checkout', 'Secure']]),
    CAL, GC(),
    M('order_table', compact=True),
    M('faq', items=[['When will it arrive?', 'Delivery times for your country are shown at checkout, before you pay.'], ['Will it tarnish or rust?', 'No. 316L stainless steel, water-friendly.'],
                    ['Will it fit?', 'Every bracelet adjusts with an extension chain.']]),
    M('cta', label='Complete my order')]))

F5['emails'].append(dict(id='F5E3', name='Loved, then worn daily', delay='+1 day', delay_short='+1d', phases=ALL, bg='white', banner=B_REC,
  subject='Why they kept theirs.', preview='Rated 4.5 on Trustpilot.',
  goal='Trust: proof, then the cart.', urgency='Today row.', klaviyo='As F5E1. Compact table. ' + GEN + ' for the two quotes.',
  modules=[
    M('score'), M('headline', title='Loved, then worn daily.', sub='Rated 4.5 on Trustpilot from 3,000+ reviews.'),
    M('quote', count=2, who=WHO),
    M('hero_photo', img={'W': 'lf_w_chair', 'M': 'lf_m_hand_rock'}, shape='inset'),
    M('order_table', compact=True), DEADLINE,
    M('cta', label='Complete my order')]))

F5['emails'].append(dict(id='F5E4', name='Finish today', delay='+2 days', delay_short='+2d', phases=['bf', 'cw', 'xmas'], bg='white', banner=B_REC,
  subject='«subj»', preview='«prev»',
  goal='Last checkout email: today’s reason to finish now; the real deadline once it’s close.', urgency='Today headline + today row.',
  klaviyo='Live Nov 13 → Dec 10; Manual outside. As F5E1. ' + TODAY,
  notes='Doesn’t send in pre, ea, late or post.',
  modules=[
    M('headline', size='xl', kicker='«kick»', title='«head»',
      sub={'bf cw': 'Your order is saved, with 30% already applied.', 'xmas': '«line»'}),
    M('deadline', label='«endl»', value='«dl»'),
    M('order_table', compact=True),
    M('cta', label='Complete my order', note='Questions? Reply to this email.')]))

# ================================================================= F6 Post-purchase
F6 = dict(id='F6', name='Q4 Post-Purchase · Gifting', trigger_short='Placed Order', replaces='new · runs next to Trustpilot Review (Tu9nLm)',
  trigger='Placed Order (Shopify, M8VZY5)', filters='Not in this flow in 14 days · smart sending on except E1', exits='E3 skips if they ordered again',
  live='Oct 27 → Jan 10 · Trustpilot review flow stays live alongside',
  why='There is no post-purchase flow. A Black Friday buyer is the warmest Christmas customer there is: confirm and reassure, then turn them into the gift-giver while 30% and Christmas delivery still apply.',
  emails=[])

F6['emails'].append(dict(id='F6E1', name='Thank you', delay='1 hour after', delay_short='1h', phases=ALL, bg='white', banner=B_WEL,
  subject='Thank you. Truly.',
  preview={'pre post': 'Here’s what happens next.', 'ea bf cw': 'Gifts too? Still 30% off.', 'xmas': 'More gifts? Order by Dec 10.', 'late': 'Gift cards arrive instantly.'},
  goal='Confirm, set expectations, and open the gift list while the offer lasts.', urgency='Today row in bf/cw/xmas.',
  klaviyo='Trigger Placed Order. Smart sending off. ' + DATE + ' ' + GEN,
  modules=[
    M('headline', title='Thank you.', sub='Your order is confirmed. Here’s what happens next.'),
    M('steps', items=['We pack it, with the jewelry case if your order has a Set or 2+ pieces.', 'It ships within 24 hours, with tracking.', 'Put it on. Leave it on.']),
    M('section_header', title={'pre post': 'Complete the look', 'ea bf cw': 'While it’s 30% off', 'xmas': 'Their gift, sorted', 'late': 'Last-minute gifts'},
      label={'pre post': 'Case with 2+', 'ea bf': '30% off', 'cw': 'Gifts · 30% off', 'xmas': 'Order by Dec 10', 'late': 'Gift cards'}),
    GUIDE,
    M('deadline', phases=['bf', 'cw', 'xmas'], label='«endl»', value='«dl»'),
    M('cta', label={'pre post': 'Shop the collection', 'ea': 'Shop early access', 'bf cw': 'Shop gifts at 30% off', 'xmas': 'Shop gifts for Christmas', 'late': 'Send a gift card'}),
    M('text', size='s', body='Questions about your order? Reply to this email.')]))

F6['emails'].append(dict(id='F6E2', name='How to wear it', delay='+4 days', delay_short='+4d', phases=ALL, bg='fog', banner=B_WEL,
  subject='How to wear it.', preview='Layer it, pair it, leave it on.',
  goal='Delight, then cross-sell the piece that completes theirs.', urgency='Offer bar in the sale.',
  klaviyo='Smart sending on. Feed: “Recommended for you” (based on what they bought). ' + DATE + ' ' + GEN,
  modules=[
    M('hero_photo', img={'W': 'lf_w_crossed', 'M': 'lf_m_hand_hair'}, shape='tall'),
    M('headline', title='Layer it. Pair it. Leave it on.'),
    M('steps', items=['Start with one. Add a second in another texture.', 'Layer necklaces at two lengths.', 'Pull the extension chain for a close fit.']),
    M('split', img={'W': 'p_braid_silver', 'M': 'p_braid_black'}, kicker='Pairs well', title='Braid Bracelet',
      body='The texture that makes a Set look considered.', cta='Shop the Braid'),
    M('section_header', title='Best sellers', label=TAGR), M('product_feed', source='recommended', count=3),
    dict(OFFER, phases=['bf', 'cw']),
    M('cta', label={'pre post': 'Shop the collection', 'ea': 'Shop early access', 'bf cw': 'Shop 30% off', 'xmas': 'Shop for Christmas', 'late': 'Send a gift card'})]))

F6['emails'].append(dict(id='F6E3', name='One for them', delay='+8 days', delay_short='+8d', phases=['ea', 'bf', 'cw', 'xmas', 'late'], bg='white', banner=B_WEL,
  subject={'ea bf cw': 'One for them?', 'xmas': 'Their gift, sorted.', 'late': 'A gift in minutes.'},
  preview={'ea bf cw xmas late': '«prev»'},
  goal='Turn a happy buyer into the gift-giver.', urgency='Today line + today row.',
  klaviyo='Filter: no Placed Order in the last 7 days. Live Nov 11 → Dec 24; Manual outside. ' + DATE + ' ' + GEN, notes='Doesn’t send in pre or post.',
  modules=[
    M('big_type', kicker='You love yours', big={'ea bf cw': '30%', 'xmas': 'Gifts.', 'late': 'Now.'},
      title={'ea bf cw': 'off their gift, too.', 'xmas': 'Give what you wear.', 'late': 'Send a gift card.'},
      sub='«line»'),
    dict(GUIDE, phases=['ea', 'bf', 'cw', 'xmas']), dict(CASE, phases=['ea', 'bf', 'cw', 'xmas']), GC(),
    DEADLINE,
    M('cta', label={'ea': 'Shop early access', 'bf cw': 'Shop gifts at 30% off', 'xmas': 'Shop for Christmas', 'late': 'Send a gift card'}, proof=True)]))

# ================================================================= F7 Winback
F7 = dict(id='F7', name='Q4 Winback · Customers First', trigger_short='Lapsed 120+ days', replaces='Customer Winback (VipiiT) → Manual on Oct 27',
  trigger='Segment entry: customers whose last order was 120+ days ago (+ a one-off launch campaign to everyone already in it)',
  filters='No order in the last 120 days · subscribed to email', exits='Placed Order', live='Oct 27 → Jan 10',
  why='The current winback made €231 from 11,172 sends in Q4 2025 (€0.02 per recipient). Lapsed customers already trust the product: early access and 30% are the reason to come back.',
  emails=[])

F7['emails'].append(dict(id='F7E1', name='Customers first', delay='On entry', delay_short='0', phases=ALL, bg='white', banner=B_WEL,
  subject={'pre': 'Early access, for you.', 'ea': 'Your access is open.', 'bf cw': 'Come back to 30%.', 'xmas': 'Back for Christmas?',
           'late': 'Gift cards, sent instantly.', 'post': 'Ready for another?'},
  preview={'pre': 'Customers shop first, Nov 11.', 'ea': 'Code BF26, before Friday.', 'bf cw': 'Everything, already on every price.',
           'xmas': 'Order by Thu Dec 10.', 'late': 'Choose an amount, send now.', 'post': 'Case included with two pieces.'},
  goal='Give a lapsed customer a reason to return: first access, then 30%.', urgency='Pass ticket + timeline.',
  klaviyo='Trigger: segment. Lapsed customers must be in the early-access audience for the pre/ea promise. Feed: “Recommended for you”. ' + DATE + ' ' + GEN,
  modules=[
    M('headline', kicker='For customers',
      title={'pre': 'You’re on the early-access list.', 'ea': 'Your early access is open.', 'bf cw': '30% off. Everything.', 'xmas': 'Back for Christmas?',
             'late': 'Too late to ship? Give the choice.', 'post': 'Ready for the next one?'},
      sub={'pre': 'As a customer you shop 30% off everything from Wednesday, Nov 11, with a code we email you, before the public sale.',
           'ea': 'Shop 30% off now with code BF26, before it opens to everyone on Friday.', 'bf cw': 'Every piece, every finish. No code. «line»',
           'xmas': 'Order by Thu Dec 10 for delivery before Christmas.', 'late': 'A gift card lands in their inbox in minutes.',
           'post': 'Two pieces or more and the jewelry case comes with them.'}),
    TICKET, *TL_SALE()[:2],
    M('hero_photo', img={'W': 'lf_w_face_wet', 'M': 'lf_m_beach_arm'}, shape='wide'),
    M('section_header', title='Best sellers', label=TAG), M('product_feed', source='recommended', count=3),
    CAL, GC(),
    M('cta', label={'pre': 'Add to calendar', 'ea': 'Shop early access', 'bf cw': 'Shop 30% off', 'xmas': 'Shop for Christmas', 'late': 'Send a gift card',
                    'post': 'Shop what’s new'}, proof=True)]))

F7['emails'].append(dict(id='F7E2', name='What’s new', delay='+3 days', delay_short='+3d', phases=ALL, bg='fog', banner=B_WEL,
  subject={'pre post': 'What’s new at Cavaier.', 'ea': 'Members’ 30% is open.', 'bf': '30% off, everything.', 'cw': 'New: the Matte Cuff.',
           'xmas': 'The gift guide.', 'late': 'Gift cards, sent instantly.'},
  preview={'pre post': 'Sets, cuffs and the classics.', 'ea': 'Code BF26, before Friday.', 'bf': 'Already on every price.',
           'cw': '«prev»', 'xmas': 'Order by Thu Dec 10.', 'late': 'They choose. You look good.'},
  goal='Show what changed since their last order.', urgency='Offer bar in the sale.',
  klaviyo='As F7E1. Matte Cuff block only from 2026-11-28.', notes='Matte Cuff product photo from the campaign shoot.',
  modules=[
    M('headline', align='left', title={'pre post': 'What’s new.', 'ea': 'Members first.', 'bf': '30% off. Everything.', 'cw': 'New: the Matte Cuff.',
                                       'xmas': 'Gifts, sorted.', 'late': 'Give the choice.'}),
    M('split', phases=['cw'], img='p_cuff_black', kicker='New · from Nov 28', title='The Matte Cuff',
      body='Our cuff, in a matte finish. 30% off, with everything else.', cta='Shop the Matte Cuff'),
    M('split', phases=['pre', 'ea', 'bf', 'xmas', 'post'], img={'W': 'p_set_w_gold', 'M': 'p_set_m_silver'}, kicker='Best seller', title='3x Minimal Set',
      body='Black, silver or gold. The one most people start with.', cta='Shop the Set'),
    M('product_grid', cols=3, items=[
        dict(gender='W', img='p_role_pend_worn', name='Rope Pendant Necklace', tag=TAG), dict(gender='W', img='p_cuban_neck_worn', name='Cuban Necklace', tag=TAG),
        dict(gender='W', img='p_crystal_br', name='Crystal Bracelet', tag=TAG), dict(gender='M', img='p_rope_neck_worn', name='Rope Pendant Necklace', tag=TAG),
        dict(gender='M', img='p_cube_br_m', name='Cube Bracelet', tag=TAG), dict(gender='M', img='p_cuff_worn', name='Minimal Cuff', tag=TAG)]),
    dict(OFFER, phases=['ea', 'bf', 'cw']), GC(),
    M('cta', label={'pre post': 'Shop what’s new', 'ea': 'Shop early access', 'bf': 'Shop 30% off', 'cw': 'Shop the Matte Cuff', 'xmas': 'Shop the gift guide',
                    'late': 'Send a gift card'})]))

F7['emails'].append(dict(id='F7E3', name='Why today', delay='+4 days', delay_short='+4d', phases=['ea', 'bf', 'cw', 'xmas'], bg='white', banner=B_WEL,
  subject='«subj»', preview='«prev»',
  goal='Close on today’s reason; the real deadline once it’s close.', urgency='Giant today word + today row.',
  klaviyo='Live Nov 11 → Dec 10; Manual outside. As F7E1. ' + TODAY, notes='Doesn’t send in pre, late or post.',
  modules=[
    M('big_type', kicker='«kick»', big='«big»', title='«head»', sub='«line»'),
    DEADLINE, M('product_feed', source='recommended', count=3), M('quote', count=1, who=WHO),
    M('cta', label='«cta»', proof=True)]))

# ================================================================= F8 Sunset
F8 = dict(id='F8', name='Pre-Black Friday Sunset', trigger_short='Unengaged 180 days', replaces='Sunset Flow (YiWP9H) → Manual on Oct 19',
  trigger='Bulk add: subscribed, no click, real open, visit or order in 180 days', filters='Runs Oct 19 → Nov 1 only', exits='Clicked any email (stays on the list)',
  live='Oct 19 → Nov 1, then suppress non-clickers Nov 2–9',
  why='Inbox placement decides Black Friday. Sending the sale to people who never open drags every send towards spam. Ask once, keep the ones who answer, suppress the rest before Nov 11.',
  emails=[])

F8['emails'].append(dict(id='F8E1', name='Stay for Black Friday?', delay='On entry', delay_short='0', phases=['pre'], bg='white', banner={'pre': 'Early access · Opens Wed Nov 11'},
  subject='Still want early access?', preview='One tap keeps you listed.',
  goal='A click that proves they want to stay.', urgency='Nov 1 cut-off for staying on the list.',
  klaviyo='Trigger: segment. Any click = engaged → leaves the sunset segment. ' + GEN,
  modules=[
    M('headline', size='xl', title='Stay for Black Friday?', sub='Members shop 30% off everything first, from Wednesday, Nov 11. Tap below and you stay on the list.'),
    M('cta', label='Keep me on the list'), TICKET,
    M('hero_photo', img={'W': 'lf_w_chair', 'M': 'lf_m_linen_chest'}, shape='inset'),
    M('text', size='s', body='Not for you anymore? No hard feelings. Do nothing and we’ll stop emailing you after Nov 1.')]))

F8['emails'].append(dict(id='F8E2', name='Last email?', delay='+5 days', delay_short='+5d', phases=['pre'], bg='fog', banner={'pre': 'Early access · Opens Wed Nov 11'},
  subject='Last email from us?', preview='Unless you tap below.',
  goal='Final chance to stay before suppression.', urgency='The list closes Nov 1.', klaviyo='As F8E1.',
  modules=[
    M('big_type', big='Last one.', title='Unless you want early access.', sub='Tap once and you’re on the list for 30% off everything from Wednesday, Nov 11.'),
    M('cta', label='Yes, keep me on'),
    M('text', size='s', body='Do nothing and this is the last email you’ll get from us.')]))

# ================================================================= F9 Back in stock
F9 = dict(id='F9', name='Selling Fast', trigger_short='Viewed Product, didn’t buy', replaces='Back in Stock (no API trigger)',
  trigger='Viewed Product (HtsYBH) · once per person', filters='No Placed Order since viewing · never been in this flow',
  exits='Placed Order', live='Oct 27 → Jan 10',
  why='Pieces sell out in the 30% weeks. A second look 4 days after F2 has finished, once per person, built by API (no hand-built Back in Stock flow).',
  emails=[])

F9['emails'].append(dict(id='F9E1', name='Selling fast', delay='4 days after viewing', delay_short='4d', phases=ALL, bg='white', banner=B_REC,
  subject={'pre ea post late': 'Still on your mind?', 'bf cw': 'Selling fast. Now 30% off.', 'xmas': 'Still in time for Christmas.'},
  preview={'pre ea post late': 'The one you looked at.', 'bf cw': 'Sizes go quickly in the sale.', 'xmas': 'Order by Thu Dec 10.'},
  goal='One more look at the exact piece, once per person, after the browse flow is done.',
  urgency='Real: pieces sell out in the sale weeks (no stock numbers claimed). Today row in ea/bf/cw/xmas.',
  klaviyo='Viewed Product event fields (name, image, URL, price) in the product block. ' + DATE,
  notes='No invented stock levels: the copy says pieces sell out in the sale, never that this one is low.',
  modules=[
    M('headline', size='xl', title={'pre ea post late': 'Still on your mind?', 'bf cw': 'Selling fast.', 'xmas': 'Still in time.'},
      sub={'pre ea post late': 'The piece you looked at is still here.', 'bf cw': 'Pieces sell out in the sale. The one you looked at is 30% off right now.',
           'xmas': 'Order by Thu Dec 10 and it arrives before Christmas.'}),
    M('dynamic_product', source='viewed', size='big'),
    M('cta', label={'pre ea post late': 'Shop it now', 'bf cw': 'Get it at 30% off', 'xmas': 'Order for Christmas'}),
    USP,
    M('quote', count=1, who=WHO)]))

# ================================================================= F10 Sale is live (for recent browsers)
F10 = dict(id='F10', name='Sale Live · Recent Browsers', trigger_short='Browsed, didn’t buy (60 days)', replaces='NEW',
  trigger='Added to List “Q4 · Sale live”: on Sat Nov 14, 09:00 add the segment “Viewed Product or Added to Cart in the last 60 days, no order since” (a day without a campaign)',
  filters='No Placed Order in the last 30 days · subscribed to email · smart sending on', exits='Placed Order',
  live='Nov 14 → Dec 6',
  why='People who looked in the last 60 days and didn’t buy are the warmest audience once the sale is open. Three emails, on days without a campaign where possible. (The accounts have no Klaviyo product catalog, so the emails show the most-picked pieces, not each person’s own views.)',
  emails=[])

F10['emails'].append(dict(id='F10E1', name='It’s 30% off now', delay='On entry (Sat Nov 14, 09:00)', delay_short='0', phases=['bf'], bg='white', banner=B_REC,
  subject='You were looking. It’s 30% off now.', preview='«prev»',
  goal='Bring back people who browsed in the last 60 days and didn’t buy, the day after the sale opens, with the pieces people pick first.', urgency='Today line: the Black Friday sale is on.',
  klaviyo='Trigger: Added to List. Feed block “Recently viewed” (Klaviyo catalog). ' + TODAY + ' ' + GEN,
  modules=[
    M('headline', kicker='«kick»', title='It’s 30% off now.', sub='You were on the site lately. Everything is already 30% off, no code. These are the pieces people pick first.'),
    M('section_header', title='Most picked', label='30% off'),
    M('product_feed', source='bestsellers', count=3),
    M('cta', label='«cta»'),
    OFFER, M('quote', count=1, who=WHO),
    M('cta', label='Shop 30% off', proof=True)]))

F10['emails'].append(dict(id='F10E2', name='Still 30% off', delay='+2 days', delay_short='+2d', phases=['bf', 'cw'], bg='fog', banner=B_REC,
  subject='«subj»', preview='Still 30% off, no code.',
  goal='Second push with the day’s reason, and the pair-and-case idea to lift order value.', urgency='Today line.',
  klaviyo='As F10E1. ' + TODAY,
  modules=[
    M('big_type', kicker='«kick»', big='«big»', title='«head»', sub='«line»'),
    M('section_header', title='Most picked', label='30% off'),
    M('product_feed', source='bestsellers', count=3),
    CASE, DEADLINE,
    M('cta', label='«cta»', proof=True)]))

F10['emails'].append(dict(id='F10E3', name='30% ends tomorrow', delay='Wait until Sat Dec 5, 09:00', delay_short='Dec 5', phases=['cw'], bg='white', banner=B_REC,
  subject='30% ends tomorrow.', preview='Sunday midnight, then full price.',
  goal='The real deadline, once, when it’s close: the day before 30% ends.', urgency='Ends tomorrow, Sunday midnight.',
  klaviyo='Wait until Sat Dec 5, 09:00 (account time zone). Exits on Placed Order. ' + GEN,
  modules=[
    M('big_type', kicker='Ends tomorrow', big='Tomorrow.', title='30% ends tomorrow.', sub='Sunday at midnight, everything goes back to full price.'),
    M('product_feed', source='bestsellers', count=3),
    M('deadline', label='30% off ends', value='Tomorrow, midnight'),
    M('cta', label='Shop before tomorrow', proof=True)]))

# ================================================================= F11 Second purchase
F11 = dict(id='F11', name='Second Purchase · Customers', trigger_short='1 order, 30–119 days ago', replaces='NEW',
  trigger='Segment entry: exactly 1 Placed Order, last order 30–119 days ago (F7 Winback takes over at 120)',
  filters='Subscribed to email · not in this flow in 60 days · smart sending on', exits='Placed Order',
  live='Oct 27 → Jan 10',
  why='One-time buyers are the gap between post-purchase (ends day 8) and winback (starts day 120). They already trust the product, and in Q4 they buy for themselves and for others. Nothing reaches them today.',
  emails=[])

F11['emails'].append(dict(id='F11E1', name='It goes with yours', delay='On entry', delay_short='0', phases=ALL, bg='white', banner=B_WEL,
  subject={'pre post': 'It goes with yours.', 'ea': 'Customers shop first.', 'bf cw': 'Next piece, 30% off.', 'xmas': 'One for them?', 'late': 'A gift in minutes.'},
  preview={'pre': 'Customers shop first, Nov 11.', 'ea bf cw xmas late': '«prev»', 'post': 'Two pieces, case included.'},
  goal='Sell the piece that completes what they bought.', urgency='Customers’ early access (pre/ea), today line in the sale.',
  klaviyo='Trigger: segment. Feed “Recommended for you” (based on their order). Customers must be in the early-access audience. ' + TODAY + ' ' + DATE + ' ' + GEN,
  modules=[
    M('headline', kicker='For customers', title='It goes with yours.',
      sub={'pre': 'As a customer you shop 30% off everything from Wednesday, Nov 11, with a code we email you, before the public sale.', 'ea bf cw': '«line»',
           'xmas': 'Order by Thu Dec 10 for Christmas delivery.', 'late': 'Too late to ship. A gift card lands in their inbox in minutes.',
           'post': 'Two pieces or more and the jewelry case comes with them.'}),
    M('section_header', title='Most loved', label=TAG), M('product_feed', source='recommended', count=3),
    TICKET, CASE, GC(),
    M('cta', label={'pre': 'See what matches', 'ea bf cw xmas late': '«cta»', 'post': 'Shop what matches'}, proof=True)]))

F11['emails'].append(dict(id='F11E2', name='Their turn', delay='+4 days', delay_short='+4d', phases=ALL, bg='fog', banner=B_WEL,
  subject={'pre post': 'Still wearing yours?', 'ea bf cw': 'Gifts, 30% off.', 'xmas': 'Their gift, sorted.', 'late': 'Gift cards, sent instantly.'},
  preview={'pre post': 'Most people buy a second.', 'ea bf cw xmas': '«prev»', 'late': 'In their inbox instantly.'},
  goal='Turn a happy customer into the gift-giver.', urgency='Today row.',
  klaviyo='As F11E1. ' + TODAY,
  notes='“Most people buy a second” needs checking against Shopify repeat-rate before launch; else use “Made to be given, too.”',
  modules=[
    M('hero_photo', img={'W': 'lf_w_crossed', 'M': 'lf_m_linen_chest'}, shape='wide'),
    M('headline', title='The gift you already know works.', sub='You wear yours every day. Give them the same.'),
    GUIDE, dict(CASE, phases=['pre', 'ea', 'bf', 'cw', 'xmas', 'post']), DEADLINE, GC(),
    M('cta', label={'pre post': 'Shop gifts', 'ea bf cw xmas late': '«cta»'})]))

F11['emails'].append(dict(id='F11E3', name='Why today', delay='+5 days', delay_short='+5d', phases=['ea', 'bf', 'cw', 'xmas'], bg='white', banner=B_WEL,
  subject='«subj»', preview='«prev»',
  goal='Close on the day’s reason.', urgency='Giant today word + today row.',
  klaviyo='Live Nov 11 → Dec 10; Manual outside. As F11E1. ' + TODAY,
  notes='Doesn’t send in pre, late or post.',
  modules=[
    M('big_type', kicker='«kick»', big='«big»', title='«head»', sub='«line»'),
    M('product_feed', source='recommended', count=3), DEADLINE,
    M('cta', label='«cta»', proof=True)]))

# ================================================================= F12 Site abandonment
F12 = dict(id='F12', name='Site Visit · No Product', trigger_short='Active on Site', replaces='NEW',
  trigger='Active on Site (Klaviyo onsite, KHDq43)',
  filters='No Viewed Product, Viewed Collection, Added to Cart or Placed Order since starting (F2, F3, F4 take over) · not in this flow in 14 days · smart sending on',
  exits='Viewed Product / Added to Cart / Placed Order', live='Oct 27 → Jan 10',
  why='Known visitors who land and leave without opening a product. The lowest intent of the recovery flows, so it’s short: a guide in, then best sellers.',
  emails=[])

F12['emails'].append(dict(id='F12E1', name='Start here', delay='2 hours after', delay_short='2h', phases=ALL, bg='white', banner=B_REC,
  subject={'pre post': 'Find your piece.', 'ea': 'Early access is open.', 'bf cw': '30% off everything.', 'xmas': 'Gifts, sorted.', 'late': 'Too late to ship?'},
  preview={'pre post': 'Start with our best sellers.', 'ea bf cw': '«prev»', 'xmas': 'Order by Thu Dec 10.', 'late': 'Send a gift card instead.'},
  goal='Turn a bounce into a product view.', urgency='Phase offer bar / cut-off calendar.',
  klaviyo='Trigger Active on Site. ' + TODAY + ' ' + DATE,
  modules=[
    M('headline', kicker={'pre post': 'Start here', 'ea bf cw': '«kick»', 'xmas': 'Christmas gift guide', 'late': 'Last-minute gifts'},
      title='Who are you shopping for?', sub='Pick who it’s for. We’ll take it from there.'),
    GUIDE, OFFER, CAL, GC(),
    M('cta', label={'pre post': 'Shop best sellers', 'ea bf cw': '«cta»', 'xmas': 'Shop for Christmas', 'late': 'Send a gift card'}, proof=True)]))

F12['emails'].append(dict(id='F12E2', name='Best sellers', delay='+1 day', delay_short='+1d', phases=ALL, bg='fog', banner=B_REC,
  subject={'pre post': 'Our best sellers.', 'ea bf cw xmas': '«subj»', 'late': 'A gift in minutes.'},
  preview={'pre post': 'The ones people keep on.', 'ea bf cw xmas': '«prev»', 'late': 'In their inbox instantly.'},
  goal='The safest first pick, with proof.', urgency='Today row.', klaviyo='As F12E1.',
  modules=[
    M('hero_photo', img={'W': 'lf_w_wet_swim', 'M': 'lf_m_beach_arm'}, shape='wide'),
    M('headline', align='left', title='The ones people keep on.', sub='Rated 4.5 on Trustpilot from 3,000+ reviews.'),
    M('product_feed', source='bestsellers', count=3), DEADLINE, GC(),
    M('cta', label={'pre post': 'Shop best sellers', 'ea bf cw xmas': '«cta»', 'late': 'Send a gift card'}, proof=True)]))

# ================================================================= F13 Gift card buyers
F13 = dict(id='F13', name='Gift Card Buyers', trigger_short='Bought a gift card', replaces='NEW',
  trigger='Placed Order where Items contains “Gift Card”', filters='Smart sending off for E1', exits='E2: Placed Order since',
  live='Nov 11 → Jan 10',
  why='Last-minute buyers want to know the gift arrives. Then, in January, the person who sorted everyone else gets a reason to treat themselves.',
  emails=[])

F13['emails'].append(dict(id='F13E1', name='How to give it', delay='15 minutes after', delay_short='15m', phases=['ea', 'bf', 'cw', 'xmas', 'late', 'post'], bg='white', banner=B_WEL,
  subject='Your gift card is ready.', preview='Here’s how to give it.',
  goal='Reassure: the gift arrives, and how to make it feel like a gift.', urgency='None: service email.',
  klaviyo='Trigger Placed Order, filter Items contains “Gift Card”. Shopify sends the card itself; this email is the how-to. ' + GEN,
  notes='Check how the store’s gift card app delivers to the recipient (date picker or not) and match step 1.',
  modules=[
    M('headline', title='Your gift card is ready.', sub='Here’s how to make it feel like a gift.'),
    M('steps', items=['The gift card code is in your order email: forward it, print it, or write it in a card.', 'Add a note: it shows above the card.',
                      'They pick the piece. Made to stay on, like yours.']),
    M('gift_card', title='Any amount, any piece.', text='The card works on everything, including Sets and the Matte Cuff.', cta='Send another'),
    M('text', size='s', body='Questions? Reply to this email.')]))

F13['emails'].append(dict(id='F13E2', name='One for you', delay='Wait until Sat Jan 2, 09:00', delay_short='Jan 2', phases=['post'], bg='fog', banner=B_WEL,
  subject='One for you, too?', preview='You sorted everyone else.',
  goal='Turn the gift-giver into a buyer for themselves.', urgency='None: new year.',
  klaviyo='Wait until Sat Jan 2, 09:00. Filter: no Placed Order since the gift card. Feed “Recommended for you”. ' + GEN,
  modules=[
    M('hero_photo', img={'W': 'lf_w_face_wet', 'M': 'lf_m_hand_rock'}, shape='tall'),
    M('headline', title='You sorted everyone else.', sub='Start the year with a piece made to stay on.'),
    M('product_feed', source='recommended', count=3), CASE,
    M('cta', label='Shop for yourself', proof=True)]))

# ================================================================= sign-up pop-up (feeds F1 and the W/M blocks)
POPUP = dict(
  kick={'pre': 'Early access · Opens Wed Nov 11', 'ea bf cw': '«kick»', 'xmas': 'Christmas', 'late': 'Last minute', 'post': 'Cavaier'},
  head={'pre': 'Shop Black Friday first.', 'ea': 'Members are shopping now.', 'bf cw': 'Get the gift guide.', 'xmas': 'Christmas, sorted.',
        'late': 'Too late to ship?', 'post': 'Made to stay on.'},
  sub={'pre': 'Members shop 30% off everything on Nov 11 and 12 with a members’ code. Two days before everyone else.',
       'ea': 'Join and get your code: 30% off everything until Thursday. On Friday it opens to everyone.',
       'bf cw': '30% off everything is live. Join for the gift guide, sorted by who it’s for, and a heads-up before it ends.',
       'xmas': 'Join for the gift guide and the last order date for Christmas delivery.',
       'late': 'Join and we’ll send the gift card link. It lands in their inbox in a minute.',
       'post': 'Join for new pieces and first access to the next sale.'},
  cta={'pre': 'Get early access', 'ea': 'Join & shop 30% off', 'bf cw': 'Send me the guide', 'xmas': 'Send me the dates', 'late': 'Send me the link',
       'post': 'Join the list'},
  done_head={'pre': 'You’re in.', 'ea': 'You’re in. Shop now.', 'bf cw xmas late': 'Check your inbox.', 'post': 'Welcome to Cavaier.'},
  done_sub={'pre': 'Early access opens Wednesday, Nov 11 at 09:00. We’ll email you your code that morning.',
            'ea': 'Your code: BF26. 30% off everything until Thursday at midnight.',
            'bf cw': 'The gift guide is on its way. 30% off everything, already on every price.',
            'xmas': 'Your gift guide and the delivery dates are on their way.', 'late': 'The gift card link is on its way.',
            'post': 'Your welcome email is on its way.'},
  done_cta={'pre': 'Add Nov 11 to my calendar', 'ea': 'Shop early access', 'bf cw xmas post': 'Keep shopping', 'late': 'Send a gift card'},
  teaser={'pre': 'Early access', 'ea': 'Early access is open', 'bf cw': 'Gift guide', 'xmas': 'Christmas dates', 'late': 'Gift card', 'post': 'Join Cavaier'},
  brief=[
    ('Why full screen', 'Agreed on desktop: a full-screen form converts best and the page behind is still one click away. On mobile, a full-screen form the moment someone lands from Google is penalised in search ranking (intrusive interstitials), so on mobile it opens after 10 seconds or on the second page view, never on landing, and the close button is always visible.'),
    ('Klaviyo form', 'Type: Full screen. Step 1 email → step 2 “Who do you shop for?” → success. Adds to the BFCM pop-up list that triggers F1, with hidden property <code>source = POPUP26</code>.'),
    ('Step 2 = W/M', 'Women / Men / Both buttons write the profile property <code>Gender</code> = “Women”, “Men” or “Both”. Every email shows the men’s version for “Men” and the women’s version otherwise, so this one tap is what makes the W/M blocks right.'),
    ('Show rules', 'Desktop: after 5 seconds or on exit intent. Mobile: after 10 seconds or on the 2nd page view. Not on cart, checkout or the back-in-stock form. Hide from anyone already subscribed. Closed → show again after 3 days. Teaser tab bottom-left stays after closing.'),
    ('Copy by date', 'Klaviyo forms don’t switch copy by date: publish the next version on Nov 11 09:00, Nov 13 08:00, Dec 7, Dec 11 and Dec 25 (one draft per phase, ready in advance).'),
    ('No fake urgency', 'No countdowns, no “only today”. The early-access dates (Nov 11–12, code BF26) and the sale itself are the reason.'),
  ])

# ================================================================= today lines (urgency from the send date)
# Every «token» in the copy is filled from the row for the day the email sends. Far from a deadline, the reason to act is
# today’s moment (Black Friday is today, Matte Cuff launches today, order today and it ships Monday). The end date
# (Sun Dec 6, the Christmas cut-off) only leads once it’s 3 days away or less. No invented scarcity.
KEYS = ['ban', 'kick', 'big', 'head', 'line', 'subj', 'prev', 'cta', 'endl', 'endv', 'ends', 'dl']
def D(id, phase, label, ban, kick, big, head, line, subj, prev, cta, endl, endv, ends, dl, default=False):
    return dict(id=id, phase=phase, label=label, default=default, ban=ban, kick=kick, big=big, head=head, line=line, subj=subj, prev=prev,
                cta=cta, endl=endl, endv=endv, ends=ends, dl=dl)
DAYS = [
  D('pre', 'pre', 'Oct 27 – Nov 10', *[''] * 12),
  D('2026-11-11', 'ea', 'Wed 11', 'Early access', 'Early access · opens today', 'Today.', 'Early access opens today.',
    'Members shop 30% off everything with code BF26. Everyone else waits until Friday.', 'Early access is open.', 'Code BF26: 30% off, today.',
    'Shop early access', 'Head start', '2 days', 'then everyone', '2 days, then everyone', True),
  D('2026-11-12', 'ea', 'Thu 12', 'Early access', 'Early access · last day', 'Last day.', 'Last members-only day.',
    'Code BF26 works until midnight. Tomorrow the sale opens to everyone.', 'Last day for code BF26.', 'Tomorrow, everyone gets in.',
    'Shop before tomorrow', 'Head start', 'Last day', 'everyone tomorrow', 'Ends tonight'),
  D('2026-11-13', 'bf', 'Fri 13', 'Black Friday sale', 'The Black Friday sale · open now', 'Open.', 'The Black Friday sale is open.',
    '30% off everything, already on every price. No code.', 'The Black Friday sale is open.', '30% off everything, no code.',
    'Shop Black Friday', 'Black Friday', 'Open now', '30% off everything', 'Black Friday, 30% off'),
  D('b1', 'bf', 'Nov 14 – 25', 'Black Friday', 'Black Friday sale', '30%.', '30% off everything.',
    'The Black Friday sale is on: 30% off everything, already on every price. No code.', 'Black Friday: 30% off.', 'Everything, no code needed.',
    'Shop 30% off', 'Black Friday', '30% off', 'everything', '30% off everything', True),
  D('2026-11-26', 'bf', 'Thu 26', 'Black Friday tomorrow', 'Black Friday is tomorrow', 'Tomorrow.', 'Black Friday is tomorrow.',
    'The sale is already on: 30% off everything, no code. Tomorrow is the big day.', 'Tomorrow: Black Friday.', '30% off already, no code.',
    'Shop 30% off', 'Black Friday', 'Tomorrow', '30% off already', 'Black Friday tomorrow'),
  D('2026-11-27', 'bf', 'Fri 27', 'Black Friday', '30% off everything · Black Friday', 'Today.', 'It’s Black Friday.',
    '30% off everything, already on every price. No code.', 'It’s Black Friday.', 'Black Friday: 30% off everything.',
    'Shop Black Friday', 'Today', 'Black Friday', '30% off everything', 'Black Friday, 30% off'),
  D('2026-11-28', 'bf', 'Sat 28', 'New today', 'New today · Matte Cuff', 'New.', 'The Matte Cuff is here.',
    'It launches today, at 30% off with everything else.', 'New today: Matte Cuff.', 'Launch day, at 30% off.',
    'Shop 30% off', 'New today', 'Matte Cuff', 'launch day', 'Matte Cuff, 30% off'),
  D('2026-11-29', 'bf', 'Sun 29', 'Black Friday weekend', 'Black Friday weekend · Sunday', 'Sets.', 'Sunday is for Sets.',
    'Three pieces in one tap, the jewelry case included, and 30% off.', 'Sunday, 30% off Sets.', 'Three pieces, case included.',
    'Shop the Sets', 'Today', 'Sets', 'case included', 'Sets, 30% off + case'),
  D('2026-11-30', 'bf', 'Mon 30', 'Cyber Monday', 'Cyber Monday · today', 'Today.', 'It’s Cyber Monday.',
    '30% off everything, already on every price. No code.', 'It’s Cyber Monday.', 'Cyber Monday: 30% off everything.',
    'Shop Cyber Monday', 'Today', 'Cyber Monday', '30% off everything', 'Cyber Monday, 30% off'),
  D('2026-12-01', 'cw', 'Tue 1', 'Cyber Week', 'Cyber Week · starts today', 'This week.', '30% off. This week only.',
    'Cyber Week: 30% off everything, Christmas gifts included. Ends Sun Dec 6, then full price.', 'This week only.', '30% off everything, still.',
    'Shop 30% off', 'Cyber Week', 'This week', 'last stretch', 'Christmas gifts, 30% off', True),
  D('2026-12-02', 'cw', 'Wed 2', 'Cyber Week', 'Cyber Week · gift early', 'Gifts.', 'Christmas gifts, at 30% off.',
    'Get the Christmas gifts done now, at 30% off. After Sunday, full price.', 'Christmas gifts, 30% off.', 'Gift now, before full price.',
    'Shop gifts at 30% off', 'Gifts', '30% off', 'until Sunday', 'Christmas gifts, 30% off'),
  D('2026-12-03', 'cw', 'Thu 3', 'Ends this Sunday', 'Ends this Sunday', 'Sunday.', '30% ends this Sunday.',
    'Four days left at 30% off. Then everything goes back to full price.', 'Ends this Sunday.', 'Four days left at 30%.',
    'Shop 30% off', '30% off ends', 'Sunday', 'at midnight', 'This Sunday, midnight'),
  D('2026-12-04', 'cw', 'Fri 4', 'Last weekend', 'The last weekend', 'Weekend.', 'The last weekend at 30%.',
    'It ends Sunday at midnight. Then full price.', 'Last weekend at 30%.', 'Ends Sunday at midnight.',
    'Shop this weekend', '30% off ends', 'Sunday', 'at midnight', 'Sunday, midnight'),
  D('2026-12-05', 'cw', 'Sat 5', 'Ends tomorrow', 'Ends tomorrow', 'Tomorrow.', '30% ends tomorrow.',
    'Sunday at midnight, everything goes back to full price.', '30% ends tomorrow.', 'Then back to full price.',
    'Shop before tomorrow', '30% off ends', 'Tomorrow', 'at midnight', 'Tomorrow, midnight'),
  D('2026-12-06', 'cw', 'Sun 6', 'Ends tonight', 'Final hours', 'Tonight.', 'It ends tonight.',
    'Last chance at 30% off. At midnight it’s full price.', 'Final hours: 30% off.', 'Midnight, then full price.',
    'Shop before midnight', '30% off ends', 'Tonight', 'at midnight', 'Tonight, midnight'),
  D('x1', 'xmas', 'Mon 7 – Tue 8', 'Christmas', 'Christmas', 'In time.', 'Order now, it’s there for Christmas.',
    'Order by Thu Dec 10 and it arrives before Christmas.', 'Gifts, in good time.', 'Order by Thu Dec 10.',
    'Order for Christmas', 'Christmas delivery', 'Thu Dec 10', 'last order day', 'Order by Thu Dec 10', True),
  D('2026-12-09', 'xmas', 'Wed 9', '2 days left', '2 days for Christmas', '2 days', 'Two days left for Christmas delivery.',
    'Order by Thursday, Dec 10 and it arrives before Christmas.', '2 days for Christmas.', 'Order by Thursday.',
    'Order for Christmas', 'Christmas delivery', '2 days', 'left to order', '2 days left to order'),
  D('2026-12-10', 'xmas', 'Thu 10 · last day', 'Last day', 'Last day for delivery', 'Today.', 'Last day for Christmas delivery.',
    'Order today and it arrives before Christmas.', 'Last day for Christmas.', 'Order today, there in time.',
    'Order today', 'Last order', 'Today', 'last order day', 'Today is the last day'),
  D('l1', 'late', 'Fri 11 – Wed 23', 'Last minute', 'Too late to ship?', 'Instant.', 'A gift card, there in a minute.',
    'Pick an amount, add a note. It lands in their inbox.', 'Still time: gift cards.', 'In their inbox instantly.',
    'Send a gift card', 'Gift card', 'Instant', 'by email', 'In their inbox instantly', True),
  D('2026-12-24', 'late', 'Thu 24', 'Christmas Eve', 'Christmas Eve', 'Tonight.', 'Christmas Eve. Still sorted.',
    'A digital gift card lands in their inbox in a minute.', 'Christmas Eve, sorted.', 'A gift card, sent now.',
    'Send a gift card', 'Christmas Eve', 'Instant', 'still in time', 'In their inbox instantly'),
  D('post', 'post', 'Dec 25 – Jan 10', *[''] * 12),
]


# ================================================================= SMS (Klaviyo SMS, both accounts)
# SMS goes out only at the highest-intent moments. Texts: plain GSM-7 characters only (straight ' and ", no – ’ … €),
# "Cavaier:" first, one shortened link, Klaviyo appends the opt-out line. One text = 160 characters, so every SMS
# below is checked to stay one segment with the link and the opt-out line counted.
SMS_KL = ('SMS block in the same flow. Conditional split before it: <code>Can receive SMS marketing</code> = true. '
          'SMS smart sending 24 h (one text a day at most). Quiet hours on: nothing between 20:00 and 10:00 recipient-local, texts wait until 10:00. '
          'Link: Klaviyo shortens it (counted as 23 characters). Opt-out line added by Klaviyo.')
def T(id, name, delay, delay_short, phases, text, goal, klaviyo='', notes='', product=None):
    return dict(kind='sms', id=id, name=name, delay=delay, delay_short=delay_short, phases=list(phases), text=text, goal=goal,
                klaviyo=(klaviyo + ' ' + SMS_KL).strip(), notes=notes, product=product)

def _after(flow, eid, entry):
    i = [e['id'] for e in flow['emails']].index(eid); flow['emails'].insert(i + 1, entry)

_after(F2, 'F2E1', T('F2T1', 'Browse text', '+3 hours', '+3h', ['ea', 'bf', 'cw'],
  {'ea': "Cavaier: The {product} you looked at is 30% off for members today with code BF26: {link}",
   'bf cw': "Cavaier: The {product} you looked at is 30% off today. No code needed: {link}"},
  goal='One text, only while 30% is on: browse texts outside the sale cost more than they make.',
  klaviyo='Filter: no Added to Cart, Checkout Started or Placed Order since the trigger. Product name from <code>event.ProductName</code>.',
  product={'W': 'Braid Bracelet', 'M': '3x Minimal Set'}))
_after(F4, 'F4E1', T('F4T1', 'Cart text', '+2 hours', '+2h', ALL,
  {'pre post': "Cavaier: Your {product} is still in your cart. Water-friendly, made to stay on: {link}",
   'ea': "Cavaier: Your cart is saved. Code BF26 takes 30% off, members only until Friday: {link}",
   'bf cw': "Cavaier: Your cart is saved and it's already 30% off. No code needed: {link}",
   'xmas': "Cavaier: Your cart is saved. Order by Dec 10 for Christmas delivery: {link}",
   'late': "Cavaier: Your cart won't arrive by Christmas, a gift card will. Sent in a minute: {link}"},
  goal='Second touch on a cart, three hours after it was left, while the email sits unopened.',
  klaviyo='Filter: no Checkout Started or Placed Order since the trigger. Link: the cart URL from the event.',
  product={'W': 'Braid Bracelet', 'M': '3x Minimal Set'}))
_after(F5, 'F5E1', T('F5T1', 'Checkout text', '+1 hour', '+1h', ALL,
  {'pre post': "Cavaier: One step left. Your checkout is saved, shipping included: {link}",
   'ea': "Cavaier: One step left. Enter code BF26 at checkout for 30% off: {link}",
   'bf cw': "Cavaier: One step left. Your 30% off is already in the price: {link}",
   'xmas': "Cavaier: One step left. Order by Dec 10 and it arrives for Christmas: {link}",
   'late': "Cavaier: Too late to ship this one. A gift card arrives in a minute instead: {link}"},
  goal='The highest-value text in the system: a started checkout, 1 h 45 min old, one tap from done.',
  klaviyo='Filter: no Placed Order since the trigger. Link: <code>event.extra.responsive_checkout_url</code>. Smart sending off for this text.'))
_after(F7, 'F7E1', T('F7T1', 'Customers-first text', '+3 hours', '+3h', ['ea', 'xmas'],
  {'ea': "Cavaier: Customers first. You shop 30% off everything before Black Friday. Code BF26: {link}",
   'xmas': "Cavaier: Christmas gifts, sorted by who they're for. Order by Dec 10 for delivery: {link}"},
  goal='Past customers with a phone number get the early-access news by text the day they enter.',
  klaviyo='Filter: no Placed Order since entering.'))
_after(F9, 'F9E1', T('F9T1', 'Selling fast text', '+2 hours', '+2h', ALL,
  {'pre ea xmas late post': "Cavaier: Still thinking about the {product}? It's here when you're ready: {link}",
   'bf cw': "Cavaier: Selling fast. The {product} you looked at is 30% off, and pieces go quickly in the sale: {link}"},
  goal='The text follows the email by 2 hours for anyone who can get texts.',
  klaviyo='Product name and URL from the Viewed Product event.',
  product={'W': 'Crystal Necklace', 'M': 'Cuban Necklace'}))

# ---- SMS-only flows, the SMS campaigns, and the gender flows (their own band, not split by women / men)
S1 = dict(id='S1', name='SMS Welcome', trigger_short='Subscribed to SMS', replaces='copy changes by period: see S1 · every period',
  trigger='Subscribed to Text Messaging Marketing (any source: pop-up step 2, checkout, back-in-stock form)',
  filters='Never been in this flow', exits='Placed Order',
  live='Oct 27 → Jan 10', sms=True,
  why='The EU account already collects about 1,000 phone numbers a month through the current pop-up and sends them almost nothing. A welcome text right after sign-up is the most-read message they will ever get from Cavaier.',
  emails=[
    T('S1T1', 'You\'re on the text list', 'Immediately', '0', ALL,
      {'pre': "Cavaier: You're on the text list. Early access opens Wed Nov 11 and the code comes here first: {link}",
       'ea': "Cavaier: You're in. Members shop 30% off everything now with code BF26, before Black Friday: {link}",
       'bf cw': "Cavaier: You're in. 30% off everything is live, already on every price. Start with the gift guide: {link}",
       'xmas': "Cavaier: You're in. Order by Dec 10 for Christmas delivery. Gifts sorted by who they're for: {link}",
       'late': "Cavaier: Too late to ship? Send a digital gift card. It lands in their inbox in a minute: {link}",
       'post': "Cavaier: Welcome. Jewelry made to stay on: water-friendly steel, every day. Start here: {link}"},
      goal='Confirm the sign-up and hand over the one link that matters this week.',
      klaviyo='Sends straight away (quiet hours still apply). Smart sending off.'),
    T('S1T2', 'Still deciding?', '+2 days', '+2d', ['ea', 'bf', 'cw', 'xmas'],
      {'ea': "Cavaier: Early access ends Thursday. Your 30% off is still waiting with code BF26: {link}",
       'bf cw': "Cavaier: Still deciding? Sets are 30% off and come with the jewelry case: {link}",
       'xmas': "Cavaier: Christmas cut-off is Dec 10. Best sellers, ready to gift: {link}"},
      goal='One nudge in the sale weeks for sign-ups who haven\'t ordered. Nothing in pre-sale or after Christmas.',
      klaviyo='Filter: no Placed Order since entering.')])

S2 = dict(id='S2', name='SMS Campaigns · Sale Moments', trigger_short='SMS subscribers, scheduled', replaces='NEW · campaigns, not a flow',
  trigger='Eight campaigns to the segment “Can receive SMS marketing”, scheduled now for the dates below',
  filters='Exclude: Placed Order in the last 2 days · got any SMS in the last 20 hours · Unengaged sunset group',
  exits='—', live='Nov 11 → Dec 22', sms=True, campaign=True,
  why='Date moments (early access opens, Black Friday, Cyber Monday, last hours, the Christmas cut-off) are the same for everyone, so they are campaigns, not flows. A flow with “wait until date” steps would send yesterday\'s alert to anyone who joins late. Eight texts across six weeks, never two in a day.',
  emails=[
    T('S2C1', 'Early access opens', 'Wed Nov 11, 09:00', 'Wed Nov 11, 09:00', ['ea'],
      "Cavaier: Early access is open. 30% off everything for members with code BF26, until Thursday: {link}",
      goal='The biggest text of the season: the first hour of early access.', klaviyo='Campaign. Send 09:00 in each recipient\'s time zone (Klaviyo local time).'),
    T('S2C2', 'Black Friday opens', 'Fri Nov 13, 08:00', 'Fri Nov 13, 08:00', ['bf'],
      "Cavaier: The Black Friday sale is open. 30% off everything, no code, case with 2+ pieces: {link}",
      goal='The Black Friday sale opens for everyone (the website switches the same morning).', klaviyo='Campaign, recipient-local time. US: not before 08:00 local.'),
    T('S2C7', 'Black Friday', 'Fri Nov 27, 19:00', 'Fri Nov 27, 19:00', ['bf'],
      "Cavaier: It's Black Friday. 30% off everything, case included with 2+ pieces. Tonight's the night: {link}",
      goal='The biggest day of the sale gets one text, in the evening, when phones are in hand.', klaviyo='Campaign, recipient-local time.'),
    T('S2C8', 'Matte Cuff launch', 'Sat Nov 28, 10:00', 'Sat Nov 28, 10:00', ['bf'],
      "Cavaier: New today: the Matte Cuff, our first matte finish. 30% off with everything else: {link}",
      goal='The launch day of the only new product of the season.', klaviyo='Campaign, recipient-local time.'),
    T('S2C3', 'Cyber Monday', 'Mon Nov 30, 12:00', 'Mon Nov 30, 12:00', ['bf'],
      "Cavaier: Cyber Monday ends at midnight. 30% off everything, no code needed: {link}",
      goal='Second-biggest day. Midday, when phones are in hand.', klaviyo='Campaign, recipient-local time.'),
    T('S2C4', 'Last hours', 'Sun Dec 6, 18:00', 'Sun Dec 6, 18:00', ['cw'],
      "Cavaier: Last hours. 30% off ends tonight at midnight, then full price: {link}",
      goal='The real deadline, once, six hours before it.', klaviyo='Campaign, recipient-local time.'),
    T('S2C5', 'Christmas cut-off', 'Thu Dec 10, 12:00', 'Thu Dec 10, 12:00', ['xmas'],
      "Cavaier: Today is the last day to order for Christmas delivery. Gifts by who they're for: {link}",
      goal='The cut-off is a real deadline and texts get read the same hour.', klaviyo='Campaign. One per region if the cut-off dates differ.'),
    T('S2C6', 'Gift card, last minute', 'Tue Dec 22, 10:00', 'Tue Dec 22, 10:00', ['late'],
      "Cavaier: Too late to ship? A Cavaier gift card lands in their inbox in a minute: {link}",
      goal='Saves the last-minute buyer who thinks it\'s too late.', klaviyo='Campaign, recipient-local time.')])

def STEP(id, kind, title, rows, delay_short=None):
    return dict(kind='step', id=id, step=kind, title=title, rows=rows, delay_short=delay_short, phases=ALL)
MEN_CATS = ['For Him', "Men's Sets", 'Men Necklace', 'You may also like - Men - Necklace', 'Für Ihn', 'Herrensets', 'Halskette für Herren',
            'Pour Lui', 'Ensembles pour hommes', 'Collier pour homme', 'Para Él', 'Conjuntos para Hombres', 'Collar para hombre', 'Per Lui',
            'Set da uomo', 'Collana da uomo', 'Voor Hem', 'Heren Sets', 'Herenketting', 'Dla niego', 'Zestawy męskie', 'Naszyjnik męski',
            'För honom', 'Herrset', 'Halsband med manmotiv', 'For ham', 'Herresett', 'Menn Halskjede', 'Conjuntos Masculinos', 'בשבילו',
            'סטים לגברים', 'مجموعات الرجال', '給他', '男士套裝', '男士項鍊']
WOMEN_CATS = ['For Her', "Women's Sets", 'Women Necklace', 'You may also like - Women - Necklace', 'Für Sie', 'Damen-Sets', 'Damenhalskette',
              'Pour Elle', 'Ensembles pour femmes', 'Collier pour femmes', 'Para Ella', 'Conjuntos de Mujer', 'Collar para mujer', 'Per Lei',
              'Completi da donna', 'Collana da donna', 'Voor haar', 'Damessets', 'Damesketting', 'Dla Niej', 'Zestawy damskie', 'För henne',
              'Damset', 'Halsband för kvinnor', 'For henne', 'Kvinnesmykke', 'Para Ela', 'Conjuntos de Mulher', 'בשבילה', 'סטים לנשים',
              'مجموعات النساء', '為她', '女裝套裝', '女士項鍊']
G1 = dict(id='G1', name='Gender from Orders', trigger_short='Ordered Product', replaces='NEW',
  trigger='Ordered Product · profile filter: <code>Gender</code> is not set',
  filters='Never overwrites: anyone with a Gender (pop-up answer or an earlier match) is filtered out at the trigger',
  exits='—', live='Oct 27 → for good (keep it after Q4)', util=True,
  why='Without a Gender, people get the women\'s version. Both stores name every women\'s product with a spaced hyphen and no men\'s product has one (“Cube - Bracelet” is women\'s, “Cube Bracelet” is men\'s, in every language), so the product <code>Name</code> on the order decides it. Jewelry Case, Gift Card, Lifetime Warranty and “Featured Product” count for neither. One-off backfill on push: Claude sets Gender for every existing customer from their order history the same way.',
  emails=[
    STEP('G1a', 'Split', 'What have they ordered, ever? (Name contains “ - ” = women\'s)',
         [['Only men\'s pieces', '→ Gender = Men'], ['Only women\'s pieces', '→ Gender = Women'], ['Both', '→ Gender = Both']]),
    STEP('G1b', 'Update profile', 'Write it down',
         [['Gender', 'Men · Women · Both'], ['Gender source', 'order'], ['Gender set on', 'today']]),
  ])
G2 = dict(id='G2', name='Gender from Browsing', trigger_short='Viewed Product', replaces='NEW',
  trigger='Viewed Product · profile filter: <code>Gender</code> is not set',
  filters='Never overwrites a pop-up answer or an order match · re-checks on every view until it can decide',
  exits='—', live='Oct 27 → for good', util=True,
  why='Most sign-ups haven\'t ordered yet. Two or more product views on one side and none on the other is a clear signal. Mixed browsing (common in gift season) sets nothing, so they keep the women\'s default until an order or the pop-up answers it.',
  emails=[
    STEP('G2a', 'Wait', '1 hour', [['Let the visit finish', 'so one session counts as a whole']], delay_short=None),
    STEP('G2b', 'Split', 'Product views in the last 14 days (Name contains “ - ” = women\'s)',
         [['2+ men\'s, no women\'s', '→ Gender = Men'], ['2+ women\'s, no men\'s', '→ Gender = Women'], ['2+ of each', '→ Gender = Both'], ['Only 1 view', '→ nothing yet']]),
    STEP('G2c', 'Update profile', 'Write it down',
         [['Gender', 'Men · Women'], ['Gender source', 'browsing'], ['Gender set on', 'today']]),
  ])
SFLOWS = [S1, S2, G1, G2]

# ---- winback, second purchase and sunset: bulk-add the whole segment instead of waiting for people to cross the line
F7.update(trigger_short='Last order 120+ days · bulk add',
  trigger='Added to List “Q4 · Winback”. Mon Nov 16, 09:00: add everyone in the segment “last order 120+ days ago” (a day without a campaign). Mon Dec 7, 09:00: add the people who crossed 120 days since. “Never been in this flow” stops repeats.',
  live='Nov 16 → Jan 10',
  why='A segment trigger only fires on the day someone crosses 120 days, so in a six-week sale it would reach a handful of people. The lapsed customers worth reaching are already in the segment: thousands of them, from earlier in 2026 and before. Adding the whole segment to a list on the first quiet day of the sale sends every one of them the flow. The current winback made €231 from 11,172 sends in Q4 2025 (€0.02 per recipient).')
F7['emails'][0].update(delay='On entry (Nov 16 or Dec 7, 09:00)', delay_short='0')
F11.update(trigger_short='1 order, 30–119 days ago · bulk add',
  trigger='Added to List “Q4 · Second purchase”. Mon Nov 9, 09:00: add everyone in the segment “exactly 1 order, last order 30–119 days ago”. Mon Dec 7, 09:00: add the people who entered the segment since. F7 takes over at 120 days.',
  live='Nov 9 → Jan 10',
  why='Same reason as F7: a segment trigger would only catch people on the day they cross 30 days. Adding the whole segment on Nov 9 means every one-time buyer gets “early access Wednesday”, then the sale. They already trust the product, and in Q4 they buy for themselves and for others.')
F11['emails'][0].update(delay='On entry (Mon Nov 9, 09:00; top-up Dec 7)', delay_short='0')
F8.update(trigger_short='Unengaged 180 days · bulk add',
  trigger='Added to List “Q4 · Sunset”. Mon Oct 19, 09:00: add everyone in the segment “subscribed 90+ days, no click, no real open (Apple Mail’s automatic opens don’t count), no site visit and no order in 180 days”. Recent openers and browsers stay in the Black Friday audience.',
  why='Inbox placement decides Black Friday. A segment trigger would only catch people the day they hit 120 days; the problem is everyone already past it. Ask them all once, keep the ones who click, suppress the rest before Nov 11.')

# ---- pop-up: phone number becomes step 2 (the current EU form already collects about 1,000 a month)
POPUP.update(
  sms_head={'pre': 'Get the early access text.', 'ea bf cw': 'Get the sale texts.', 'xmas': 'Get the cut-off text.',
            'late': 'Get the gift card by text.', 'post': 'Get first access by text.'},
  sms_sub={'pre': 'We text you the code the moment early access opens on Nov 11. A few texts a season, never more than one a day.',
           'ea': 'A few texts a season, never more than one a day.',
           'bf cw': 'A few texts a season, never more than one a day.',
           'xmas': 'We text you on the last order day for Christmas delivery.',
           'late': 'The gift card link, straight to your phone. It’s sent in a minute.',
           'post': 'New pieces and the next sale, by text, before anyone else.'},
  sms_fine='By tapping “Text me” you agree to receive recurring automated marketing texts from Cavaier at this number. Consent is not a condition of purchase. Msg & data rates may apply. Opt out any time: reply STOP (US/CA) or tap the link in any text. HELP for help. Privacy Policy.')
POPUP['brief'][1] = ('Klaviyo form', 'Type: Full screen. Step 1 email → step 2 phone number (SMS consent, skippable) → step 3 “Who do you shop for?” → success. Email adds to the BFCM pop-up list that triggers F1 (hidden property <code>source = POPUP26</code>); the phone number adds SMS consent, which triggers S1.')
POPUP['brief'].insert(2, ('Step 2 = SMS', 'Phone number with a country picker defaulting to the visitor’s country. Klaviyo shows the legal consent text under the button; keep it. The current EU form (SyHM2E) already collects about 1,000 numbers a month, so leaving the phone step out would cost about a thousand SMS subscribers a month in the busiest season.'))
POPUP['brief'][3] = ('Step 3 = W/M', POPUP['brief'][3][1])

# ---- what each period's sign-ups get next (journey card at the end of each pop-up row)
JOURNEY = {
  'pre': ['F1 welcome, pre-sale versions: E1–E4 over four days', 'The early-access code arrives by campaign on Nov 11', 'Phone → S1T1 now, then the SMS campaigns'],
  'ea': ['F1 welcome, early-access versions (code BF26): E1–E5, one a day', 'Campaigns carry the big moments (code on Nov 11, sale open on Nov 13)', 'Phone → S1T1 now, S1T2 two days later'],
  'bf': ['F1 welcome, 30% versions: E1–E5, one a day', 'Last-hours email and text before Dec 6 midnight', 'Phone → S1T1 now, S1T2 two days later'],
  'xmas': ['F1 welcome, Christmas versions with the cut-off: E1–E5', 'Cut-off campaign on the last order day', 'Phone → S1T1 now, S1T2 two days later'],
  'late': ['F1 welcome, gift-card versions: E1–E4', 'Gift card link in every message', 'Phone → S1T1 with the gift card link'],
  'post': ['F1 welcome, after-Christmas versions: E1–E4', 'Back to the evergreen welcome on Jan 10', 'Phone → S1T1 now'],
}

FLOWS = [F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13]

# ================================================================= page copy
PAGE = {}
PAGE['sms'] = '''  <section class="card narrow">
    <span class="kicker">SMS · the system</span>
    <h2>Texts only where a minute matters.</h2>
    <p class="notes" style="color:inherit;font-size:14px">Both Klaviyo accounts can send SMS. The EU account collects about 1,000 phone numbers a month through the current pop-up and has sent them almost nothing; the US account has a few hundred. A text costs real money per message and gets read within minutes, so it goes only where speed decides the sale: a checkout or cart left behind, a restock, a sign-up, and the five date moments everyone shares.</p>
    <div class="tbl" style="border:0"><table style="min-width:0"><thead><tr><th>Where</th><th>Text</th><th>When</th><th>Why a text</th></tr></thead><tbody>
      <tr><td class="n"><b>Pop-up step 2</b></td><td>Phone number + consent</td><td>After the email</td><td>Keeps the ~1,000 numbers a month the current form already collects.</td></tr>
      <tr><td class="n"><b>S1</b></td><td>SMS welcome · T1, T2</td><td>Now · +2 days in the sale weeks</td><td>The most-read message they will get from Cavaier.</td></tr>
      <tr><td class="n"><b>F5</b></td><td>Checkout text</td><td>1 h 45 min after checkout</td><td>One tap from done. The highest-value text in the system.</td></tr>
      <tr><td class="n"><b>F4</b></td><td>Cart text</td><td>3 hours after the cart</td><td>Lands while the email sits unopened.</td></tr>
      <tr><td class="n"><b>F9</b></td><td>Back in stock text</td><td>On restock, with the email</td><td>Restocks sell out again within hours.</td></tr>
      <tr><td class="n"><b>F2</b></td><td>Browse text</td><td>5 hours after the view, sale weeks only</td><td>Pays only while 30% is on.</td></tr>
      <tr><td class="n"><b>F7</b></td><td>Customers-first text</td><td>3 hours after the bulk add</td><td>Past customers hear about early access the same day.</td></tr>
      <tr><td class="n"><b>S2</b></td><td>Eight campaigns</td><td>Nov 11 · 13 · 27 · 28 · 30 · Dec 6 · 10 · 22</td><td>Date moments are the same for everyone, so they are campaigns.</td></tr>
    </tbody></table></div>
    <ul class="levers">
      <li><b>Never more than one text a day:</b> SMS smart sending 24 h on every flow text; campaigns exclude anyone texted in the last 20 hours and anyone who ordered in the last 2 days.</li>
      <li><b>Quiet hours</b> 20:00–10:00 recipient-local for flow texts. Campaigns go out at the times listed, in each recipient’s time zone; in the US never before 08:00 or after 21:00 local.</li>
      <li><b>One segment per text:</b> plain characters only (no curly quotes, dashes or emoji, which halve the length to 70), “Cavaier:” first, one link, Klaviyo’s opt-out line. Every text on this page shows its count.</li>
      <li><b>Consent:</b> only profiles with SMS consent get texts. The pop-up keeps Klaviyo’s legal line under the button. EU and UK numbers get the sender name “Cavaier”; US numbers send from the toll-free number already on the US account.</li>
      <li><b>Women / men:</b> texts are the same for both; links go to the women’s or men’s collection by Gender.</li>
    </ul>
  </section>
'''

PAGE['intro'] = '''  <header class="intro narrow">
    <span class="kicker">Cavaier · Q4 2026 · Klaviyo flows · mock-up</span>
    <h1>Q4 flows: Black Friday to Christmas</h1>
    <p>{n_flows} flows and {n_emails} emails that replace the evergreen flows from Oct 27 to Jan 10. Every email changes with the calendar, inside one Klaviyo template: use the bar to switch women’s / men’s and the Q4 phase. Brief card on the right of each email: send time, subject and preview for the phase, the job, the urgency device and the Klaviyo build. Mock-up only: nothing is live in Klaviyo.</p>
  </header>'''

PAGE['top'] = '''  <section class="card narrow" style="border-color:var(--red)">
    <span class="kicker" style="color:var(--red)">Fix first · before Oct 27</span>
    <h2>Product tracking has been broken since early September.</h2>
    <p class="notes" style="color:inherit;font-size:14px">“Viewed Product” fell from about 10,000 a week in August to about 2,800 since Sep 1. Orders fell too, but views per order halved (about 21 → 11). The old “Added to Cart” tracking died the same day, and “Viewed Page” and shipping events went quiet. Browse (F2), Sale live (F10) and the recently-viewed feeds all run on this event: Browse earned €7,048 last Q4. Check the Klaviyo onsite tracking on the theme (product page snippet / app embed) and test a product view on a known profile.</p>
  </section>

  <section class="card narrow">
    <span class="kicker">What the Q4 flows have to beat · Q4 2025, email, Placed Order</span>
    <div class="stats">
      <div><b>€10,886</b><span>Checkout Abandoned · €1.37 per recipient · 8,212 recipients</span></div>
      <div><b>€8,643</b><span>Add to Cart · €0.86 per recipient · 10,068 recipients</span></div>
      <div><b>€7,048</b><span>Browse · €0.35 per recipient · 20,138 recipients</span></div>
      <div><b>€231</b><span>Winback · €0.02 per recipient · 11,172 recipients</span></div>
    </div>
    <p class="notes">Also in Q4 2025: the Trustpilot review flow, €1,147. No welcome or post-purchase flow sent in Q4 2025.</p>
  </section>

  <section class="card narrow">
    <span class="kicker">The Q4 calendar · every email switches by date</span>
    <div class="cal">
      <div><i>Pre-sale</i><b>Oct 27 – Nov 10</b><span>Join early access. No sale talk in recovery flows.</span></div>
      <div><i>Early access</i><b>Nov 11 – 12</b><span>Members shop 30% off first with code BF26.</span></div>
      <div><i>Black Friday</i><b>Nov 13 – 30</b><span>30% off everything, no code. Black Friday Nov 27, Cyber Monday Nov 30, Matte Cuff Nov 28.</span></div>
      <div><i>Cyber Week</i><b>Dec 1 – 6</b><span>30% ends Sun Dec 6, midnight.</span></div>
      <div><i>Christmas</i><b>Dec 7 – Dec 10</b><span>Gifting, case with 2+, order-by dates.</span></div>
      <div><i>Last minute</i><b>Dec 10 – Dec 24</b><span>Digital gift card.</span></div>
      <div><i>After Christmas</i><b>Dec 25 – Jan 10</b><span>New year, treat yourself.</span></div>
    </div>
  </section>'''

PAGE['urgency'] = '''
  <section class="card narrow">
    <span class="kicker">Urgency · every email sells today</span>
    <p class="notes" style="color:inherit;font-size:14px">The reason to act comes from the day the email sends, not from the end of the sale. On Nov 13 the email says “The Black Friday sale is open”, on Nov 26 “Black Friday is tomorrow”, on Nov 27 “It’s Black Friday”, on Nov 28 “The Matte Cuff launches today”, on Nov 29 “Sunday is for Sets”, on Dec 2 “Christmas gifts, at 30% off”. “Sun Dec 6” only leads from Thu Dec 3, and “Tonight” only on Dec 6. Same for Christmas: “In time” first, then “[3] days left”, then “Last day”. Use the day buttons under the phases to see each day. In Klaviyo it’s one saved block with one line per date.</p>
    <div class="tbl" style="border:0"><table style="min-width:0"><thead><tr><th>Day</th><th>Big word</th><th>Headline</th><th>Subject</th><th>Preview</th><th>Today row</th></tr></thead><tbody>{day_rows}</tbody></table></div>
  </section>
'''

PAGE['bottom'] = '''  <section class="card narrow">
    <span class="kicker">Switchover plan</span>
    <div class="tbl" style="border:0"><table style="min-width:0"><tbody>
      <tr><td class="n"><b>Oct 13 – 16</b></td><td>Build F1–F9 in Klaviyo as drafts: one template per email, phase blocks by date, W/M blocks by Gender. Test each phase in a copy with the date thresholds moved.</td></tr>
      <tr><td class="n"><b>Mon Oct 19</b></td><td>F8 Sunset live. Sunset Flow (YiWP9H) → Manual.</td></tr>
      <tr><td class="n"><b>Tue Oct 27, 09:00</b></td><td>F1–F7, F9 and F11–F13 live. Same hour → Manual: Welcome Series (QVmUhV), Browse Abandonment (RkFCNW), Add to Cart Abandoned (Syiqdb), Checkout Abandoned (Ub2mSt), Customer Winback (VipiiT). Emails waiting in a Manual flow don’t send. Send the one-off winback launch campaign to the lapsed segment.</td></tr>
      <tr><td class="n"><b>Sun Nov 1</b></td><td>F8 off. Nov 2–9: suppress profiles who got both sunset emails and didn’t click.</td></tr>
      <tr><td class="n"><b>Wed Nov 11</b></td><td>Pop-up: publish the early-access version at 09:00 (and the Black Friday, Christmas, last-minute and after-Christmas versions on Nov 13, Dec 7, the cut-off and Dec 26). Window emails on: F1E5, F5E4 (from Nov 13), F2E3 (from Nov 13), F6E3, F7E3, F11E3. 09:00: add early-access members from the “browsed, didn’t buy” segment to the F10 list. Everything else switches copy by itself.</td></tr>
      <tr><td class="n"><b>Fri Nov 13, 08:00</b></td><td>Black Friday opens on the website. Add everyone else from that segment to the F10 list.</td></tr>
      <tr><td class="n"><b>Fri Dec 11</b></td><td>The day after the Christmas cut-off (Thu Dec 10): the emails switch to gift cards by themselves. F1E5, F2E3, F5E4, F7E3 stop by themselves (they only send in their periods).</td></tr>
      <tr><td class="n"><b>Fri Dec 25</b></td><td>No flow sends: send-time windows skip Christmas Day.</td></tr>
      <tr><td class="n"><b>Sun Jan 10</b></td><td>Q4 flows → Manual, evergreen flows back on. Keep F6 Post-purchase and F3 live if they beat the old numbers.</td></tr>
    </tbody></table></div>
  </section>

  <section class="card narrow">
    <span class="kicker">Priority and frequency</span>
    <ul class="levers">
      <li><b>One recovery flow at a time, highest intent wins:</b> Checkout (F5) › Cart (F4) › Browse (F2) › Collection (F3). Each lower flow’s filter excludes the higher events since it started.</li>
      <li><b>Smart sending (16 h)</b> on every email except F1E1, F5E1, F6E1 and F9E1.</li>
      <li><b>Campaign days</b> (Nov 11, 12, 13, 15, 17, 19, 22, 24, 26, 27, 28, 29, 30, Dec 2, 4, 6, 7, 8, 9, 10, 11, 24): the email campaigns own these days. Flows that start from a bulk add (F7, F10, F11) start on days without a campaign. Smart Sending (16 h) keeps a flow email from landing on top of a campaign, except the checkout and cart reminders (F5E1, F4E1), which always send.</li>
      <li><b>Re-entry:</b> checkout 1 day, cart and browse 3 days, collection 7 days, post-purchase 14 days.</li>
      <li><b>Send windows:</b> 08:00–21:00 recipient-local on F2, F3, F4 and F7 delays.</li>
      <li><b>No fixed prices</b> in static blocks (multi-currency list). Dynamic blocks print the event price; checkout emails print the real discount and total.</li>
    </ul>
  </section>

  <section class="card narrow">
    <span class="kicker">Open items</span>
    <ul class="levers">
      <li><b>Christmas cut-off dates</b> per region (CEO): fill every Dec 10 and the order-by calendar.</li>
      <li><b>Christmas and after-Christmas offer</b>, if any, and the shipping offer outside Nov 11 – Dec 6. The December emails sell without a discount until then.</li>
      <li><b>Trustpilot quotes</b> (Katrina): every quote is a placeholder.</li>
      <li><b>Customers in early access:</b> F7 promises lapsed customers first access, so they need to be in the early-access audience.</li>
      <li><b>Viewed Collection fields</b> (F3) and the <b>gift-card delivery</b> setup (“arrives instantly”, scheduled delivery) to confirm in Shopify/Klaviyo.</li>
      <li><b>Figma:</b> the Figma connection dropped in this session; reconnect it (claude.ai connector settings) before frames can be synced.</li>
    </ul>
  </section>'''
