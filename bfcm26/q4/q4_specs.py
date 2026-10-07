"""Cavaier Q4 2026 flows: every flow and email as data. Rendered by gen_q4.py.

Phases: pre (Oct 27–Nov 22) · ea (Nov 23–26) · bf (Nov 27–30, incl. Cyber Monday) · cw (Dec 1–6) ·
xmas (Dec 7–Christmas cut-off) · late (cut-off–Dec 24) · post (Dec 26–Jan 10).
Rules: 3–4 word subjects, 4–5 word previews, no FREE in subject/preview/banner/headline, no countdown timers,
no fixed prices in static content, Set not Stack, placeholders in [brackets].
"""

ALL = ['pre', 'ea', 'bf', 'cw', 'xmas', 'late', 'post']

def M(type, **kw):
    kw['type'] = type
    return kw

# ---------------------------------------------------------------- shared copy
B_WEL = {'pre': 'Early access · Opens Mon Nov 23', 'ea': 'Early access · 30% off is open',
         'bf': 'Black Friday · 30% off everything', 'cw': 'Cyber Week · 30% off ends Sun Dec 6',
         'xmas': 'Christmas · Order by [cut-off] for delivery', 'late': 'Last minute · Gift cards arrive instantly',
         'post': 'New year · Made to stay on'}
B_REC = {'pre post': 'Jewelry case included · With 2+ pieces', 'ea': 'Early access · Members shop 30% off now',
         'bf': 'Black Friday · 30% off everything', 'cw': 'Cyber Week · 30% off ends Sun Dec 6',
         'xmas': 'Christmas · Order by [cut-off] for delivery', 'late': 'Last minute · Gift cards arrive instantly'}
TAG = {'pre': 'From Nov 23 · 30% off', 'ea': 'Members 30% off', 'bf cw': '30% off', 'xmas': 'Gift pick',
       'late': 'Gift pick', 'post': 'Best seller'}
TAGR = {'pre post': 'Case with 2+', 'ea': 'Members 30% off', 'bf cw': '30% off', 'xmas': 'Gift picks', 'late': 'For next time'}
WHO = {'W': 'Her name · Trustpilot', 'M': 'His name · Trustpilot'}
USP = M('usp_bar', items=['100% waterproof', 'Stainless steel', 'Hypoallergenic'])
OFFER = M('offer_bar', phases=['ea', 'bf', 'cw'], items=['30% off everything', 'No code', 'Case with 2+ pieces'])
CAL = M('shipping_calendar', phases=['xmas'])
def GC(title='Gift card, sent in minutes.', text='Pick any amount, add a note, choose when it lands. They choose the piece.', cta='Send a gift card', phases=('late',)):
    return M('gift_card', phases=list(phases), title=title, text=text, cta=cta)
CASE = M('gift_box', img='p_case', kicker='Included', title='Jewelry case with 2+ pieces',
         text='Added at checkout automatically. Ready to give, or to keep.')
TICKET = M('ticket', phases=['pre', 'ea', 'bf', 'cw'], cells=[
    dict(label='Your price', value='30% off', sub='everything', red=True),
    dict(label='Code', value='None', sub='applied at checkout'),
    dict(label={'pre': 'Opens', 'ea': 'Public on', 'bf cw': 'Ends'}, value={'pre': 'Mon 23', 'ea': 'Fri 27', 'bf cw': 'Sun 6'},
         sub={'pre': 'November', 'ea': 'November', 'bf cw': 'December, midnight'})])
def TL_SALE():
    return [M('timeline', phases=['pre'], points=[dict(label='Today · On the list', state='now'), dict(label='Mon 23 · You shop first', state='next'), dict(label='Fri 27 · Everyone', state='end')]),
            M('timeline', phases=['ea'], points=[dict(label='Today · Members', state='now'), dict(label='Fri 27 · Everyone', state='next'), dict(label='Sun Dec 6 · Ends', state='end')]),
            M('timeline', phases=['bf', 'cw'], points=[dict(label='Fri 27 · Opened', state='past'), dict(label='Today · 30% off', state='now'), dict(label='Sun Dec 6 · Ends', state='end')]),
            M('timeline', phases=['xmas'], points=[dict(label='Today', state='now'), dict(label='[Cut-off] · Last order', state='end'), dict(label='Fri 25 · Christmas', state='next')])]
DEADLINE = M('deadline', phases=['ea', 'bf', 'cw', 'xmas'],
             label={'ea': 'Early access ends', 'bf cw': '30% off ends', 'xmas': 'Christmas delivery'},
             value={'ea': 'Fri Nov 27', 'bf cw': 'Sun Dec 6, midnight', 'xmas': 'Order by [cut-off]'})
SALE_LIST = M('offer_list', phases=['bf', 'cw'], rows=[['30% off everything', 'Applied at checkout, no code'], ['Two or more pieces', 'Jewelry case included'],
                                                        ['Shipping', 'Free on every order'], ['Ends', 'Sun Dec 6, midnight']])

C = lambda s: f'<code>{s}</code>'
DATE = ('Phase blocks switch inside one template: ' + C("{% today '%Y-%m-%d' as d %}") +
        ' — pre &lt; 2026-11-23 ≤ ea &lt; 11-27 ≤ bf &lt; 12-01 ≤ cw &lt; 12-07 ≤ xmas &lt; [cut-off] ≤ late &lt; 12-25 ≤ post.')
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
  why='Sign-ups spike in Q4 and decide fast. One welcome that is a members’ pass before Nov 23, a 30%-off welcome in the sale, a gifting welcome in December and a gift-card welcome after the cut-off. No welcome flow sent in Q4 2025.',
  emails=[])

F1['emails'].append(dict(id='F1E1', name='The pass', delay='Immediately', delay_short='0', phases=ALL, bg='white', banner=B_WEL,
  subject={'pre': 'You’re on the list.', 'ea': 'Your access is open.', 'bf': 'Your 30% is waiting.', 'cw': '30% off, until Sunday.',
           'xmas': 'Welcome. Gifts, sorted.', 'late': 'Welcome. Gift in minutes.', 'post': 'Welcome to Cavaier.'},
  preview={'pre': 'First access: Monday, Nov 23.', 'ea': 'Before the public sale, Friday.', 'bf': 'Everything. Applied at checkout.',
           'cw': 'Ends Sunday, Dec 6, midnight.', 'xmas': 'Order by [cut-off] for Christmas.', 'late': 'Digital gift cards, sent instantly.',
           'post': 'Jewelry made to stay on.'},
  goal='One job per phase: save the date (pre), shop first (ea), shop 30% (bf/cw), shop gifts before the cut-off (xmas), send a gift card (late).',
  urgency='Members’ pass ticket + timeline to the next date; cut-off calendar in xmas.',
  klaviyo='Trigger: Added to List. Send immediately, smart sending off. ' + DATE + ' ' + GEN + ' Product cards static (no prices).',
  modules=[
    M('big_type', kicker={'pre': 'Early access · Member', 'ea': 'Early access · Open now', 'bf': 'Black Friday weekend', 'cw': 'Cyber Week',
                          'xmas late post': 'Welcome to Cavaier'},
      big={'pre ea': 'You’re in.', 'bf cw': '30%', 'xmas': 'Gifts.', 'late': 'Minutes.', 'post': 'Welcome.'},
      title={'pre': 'First pick, Monday Nov 23.', 'ea': '30% off. Before everyone.', 'bf': 'off everything. No code.', 'cw': 'off everything, until Sunday.',
             'xmas': 'They’ll never take them off.', 'late': 'That’s how fast a gift card arrives.', 'post': 'Jewelry you never take off.'},
      sub={'pre': 'Members shop 30% off everything before the public sale. We’ll email you the moment it opens.',
           'ea': 'Early access is open for you now. On Friday, Nov 27, it opens to everyone.',
           'bf': 'Black Friday to Cyber Monday: every piece, every finish, 30% off at checkout.',
           'cw': 'Cyber Week is the last stretch. 30% off ends Sunday, Dec 6 at midnight.',
           'xmas': 'Waterproof stainless steel, made to be worn every day. Order by [cut-off] for Christmas delivery.',
           'late': 'Too late for shipping, not for a gift. Pick an amount and it lands in their inbox.',
           'post': 'Minimal pieces made for real life: shower, sea, gym, sleep.'}),
    TICKET, *TL_SALE()[:3],
    M('cta', label={'pre': 'Save the date', 'ea': 'Shop early access', 'bf': 'Shop 30% off', 'cw': 'Shop before Sunday', 'xmas': 'Shop the gifts',
                    'late': 'Send a gift card', 'post': 'Shop best sellers'},
      note={'pre': 'Adds Mon Nov 23 to your calendar.', 'ea': 'Members only until Friday, Nov 27.'}),
    M('hero_photo', img={'W': 'lf_w_3x_set', 'M': 'lf_m_3x_set'}, shape='wide'),
    CAL, GC(),
    M('section_header', title={'pre': 'Your shortlist', 'ea bf cw': 'Start here', 'xmas': 'Gift picks', 'late': 'For yourself', 'post': 'Best sellers'},
      label={'pre': 'From Nov 23 · 30% off', 'ea bf cw': '30% off', 'xmas late post': 'Case included with 2+'}),
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
  preview={'pre': 'Shortlist now. Shop Nov 23.', 'ea': 'Best sellers, members first.', 'bf cw': 'Three pieces, one tap.',
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
    M('offer_list', phases=['ea', 'bf', 'cw'], rows=[['30% off', 'Applied at checkout, no code'], ['Two or more pieces', 'Jewelry case included'],
                                                    ['Shipping', 'Free on every order'], ['Ends', {'ea': 'Early access: Fri Nov 27', 'bf cw': 'Sun Dec 6, midnight'}]]),
    M('promise', phases=['pre'], text='Every Set here is 30% off for members from Monday, Nov 23.'),
    M('promise', phases=['xmas'], text='A Set is three gifts in one box. Order by [cut-off] for Christmas.'),
    M('promise', phases=['post'], text='Three pieces, worn every day. Start there.'),
    GC(title='Can’t ship in time? Give the choice.', text='A digital gift card lands in their inbox in minutes. Any amount.'),
    M('quote', count=1, who=WHO),
    M('cta', label={'pre': 'See the Sets', 'ea': 'Shop before Friday', 'bf cw': 'Shop the Sets at 30% off', 'xmas': 'Shop gift Sets',
                    'late': 'Send a gift card', 'post': 'Shop the Sets'}, proof=True)]))

F1['emails'].append(dict(id='F1E3', name='Made to stay on', delay='+2 days', delay_short='+2d', phases=ALL, bg='white', banner=B_WEL,
  subject={'pre': 'Shower. Gym. Sleep.', 'ea': 'Made to stay on.', 'bf cw': 'Worn daily. 30% off.', 'xmas': 'A gift worn daily.',
           'late': 'Worn daily, gifted instantly.', 'post': 'Made to stay on.'},
  preview={'pre': 'Why nobody takes them off.', 'ea': 'And members save 30%.', 'bf cw': 'Rated 4.5 on Trustpilot.',
           'xmas': 'Waterproof steel, case included.', 'late': 'Gift cards arrive in minutes.', 'post': 'Rated 4.5 on Trustpilot.'},
  goal='Kill the doubts (tarnish, water, skin, fit) with product facts and proof, then sell.',
  urgency='Deadline row in ea/bf/cw/xmas.', klaviyo='Smart sending on. ' + DATE + ' ' + GEN,
  modules=[
    M('hero_photo', img={'W': 'lf_w_wet_swim', 'M': 'lf_m_bw_fist'}, shape='tall'),
    M('headline', title='Put it on once. Live in it.', sub='Shower, sea, gym, sleep. Stainless steel that doesn’t rust, tarnish or come off.'),
    M('checklist', items=['100% waterproof, sweat and heat resistant', 'Recycled 316L stainless steel', 'Hypoallergenic, kind to skin',
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
  subject={'pre': 'Nov 23. You’re first.', 'ea': 'Members only, until Friday.', 'bf': '30% off. Everything.', 'cw': 'Final days at 30%.',
           'xmas': 'Christmas delivery deadline.', 'late': 'A gift in minutes.', 'post': 'Your first piece.'},
  preview={'pre': 'Members shop 30% off first.', 'ea': 'Then it opens to everyone.', 'bf': 'Applied automatically at checkout.',
           'cw': 'Ends Sunday, Dec 6, midnight.', 'xmas': 'Order by [cut-off date].', 'late': 'Pick an amount, send now.',
           'post': 'Case included with two pieces.'},
  goal='The loudest welcome email: the phase’s one date, huge, and one button.',
  urgency='Giant date lockup + timeline; cut-off calendar in xmas.', klaviyo='Smart sending on. ' + DATE + ' ' + GEN,
  modules=[
    M('big_type', kicker={'pre ea': 'Early access', 'bf': 'Black Friday weekend', 'cw': 'Cyber Week', 'xmas': 'Christmas', 'late': 'Last minute', 'post': 'New year'},
      big={'pre': 'Nov 23', 'ea bf': '30%', 'cw': 'Sun 6', 'xmas': '[Dec 17]', 'late': 'Now.', 'post': '2027.'},
      title={'pre': 'You shop first.', 'ea': 'Members only. Until Friday.', 'bf': 'off everything.', 'cw': '30% off ends at midnight.',
             'xmas': 'Last day for Christmas delivery.', 'late': 'The gift card arrives today.', 'post': 'Something you’ll wear every day.'},
      sub={'pre': 'Members get 30% off everything before the public sale on Friday, Nov 27.',
           'ea': 'Early access ends when the sale opens to everyone on Friday, Nov 27.',
           'bf': 'Black Friday through Cyber Monday. No code: it comes off at checkout.',
           'cw': 'After Sunday, Dec 6, prices go back to normal.',
           'xmas': 'Order by [cut-off date] and it arrives before Christmas. [Per-country dates below]',
           'late': 'Pick an amount, write a note, choose when it arrives. They pick the piece.',
           'post': 'Start the year with a piece made to stay on.'}),
    M('cta', label={'pre': 'Add to calendar', 'ea': 'Shop early access', 'bf': 'Shop 30% off', 'cw': 'Shop before Sunday midnight',
                    'xmas': 'Order for Christmas', 'late': 'Send a gift card', 'post': 'Shop best sellers'}),
    *TL_SALE(),
    M('hero_photo', img={'W': 'lf_w_black_top', 'M': 'lf_m_linen_chin'}, shape='wide'),
    OFFER, CAL, GC(),
    M('section_header', title='Best sellers', label=TAG),
    M('product_feed', source='bestsellers', count=3),
    M('cta', label={'pre': 'See the Sets', 'ea': 'Shop early access', 'bf': 'Shop 30% off', 'cw': 'Shop before Sunday midnight',
                    'xmas': 'Order for Christmas', 'late': 'Send a gift card', 'post': 'Shop best sellers'}, proof=True)]))

F1['emails'].append(dict(id='F1E5', name='Last call', delay='+4 days', delay_short='+4d', phases=['ea', 'bf', 'cw', 'xmas'], bg='fog', banner=B_WEL,
  subject={'ea': 'Last call: early access.', 'bf': 'Don’t wait for Sunday.', 'cw': 'Last call: 30% off.', 'xmas': 'Last call for Christmas.'},
  preview={'ea': 'Public sale starts Friday.', 'bf': '30% ends Sun Dec 6.', 'cw': 'Ends Sunday at midnight.', 'xmas': 'Order by [cut-off date].'},
  goal='Close the welcome on the real deadline of the window they’re in.',
  urgency='Deadline row + single hero product.',
  klaviyo='Live Nov 23 → [cut-off] only; set to Manual outside (no date-based skip exists in a flow). ' + DATE + ' ' + GEN,
  notes='Doesn’t send in pre, late or post.',
  modules=[
    M('headline', size='xl', title={'ea': 'Last call for early access.', 'bf': 'Don’t leave it to Sunday.', 'cw': 'Last call.', 'xmas': 'Last call for Christmas.'},
      sub={'ea': 'On Friday it opens to everyone. Today it’s still yours first.',
           'bf': 'It’s 30% off now, until Sunday, Dec 6 at midnight. Then full price.',
           'cw': '30% off everything ends Sunday, Dec 6 at midnight. After that, full price.',
           'xmas': 'Order by [cut-off date] for delivery before Christmas. After that, gift cards.'}),
    M('deadline', label={'ea': 'Early access ends', 'bf cw': '30% off ends', 'xmas': 'Last order for Christmas'},
      value={'ea': 'Fri Nov 27', 'bf cw': 'Sun Dec 6, midnight', 'xmas': '[cut-off date]'}),
    M('split', reverse=True, img={'W': 'p_set_w', 'M': 'p_set_m_silver'}, kicker='Best seller', title='3x Minimal Set',
      body='If you get one thing, get the Set. Three pieces, and the jewelry case comes with it.', cta='Shop the Set'),
    M('quote', count=1, who=WHO),
    M('offer_list', phases=['ea', 'bf', 'cw'], rows=[['30% off', 'Applied at checkout, no code'], ['Two or more pieces', 'Jewelry case included'],
                                                    ['Shipping', 'Free on every order']]),
    M('offer_list', phases=['xmas'], rows=[['Christmas delivery', 'Order by [cut-off]'], ['Two or more pieces', 'Jewelry case included'],
                                         ['Shipping', '[shipping offer to confirm]']]),
    M('cta', label={'ea': 'Shop before Friday', 'bf cw': 'Shop before it ends', 'xmas': 'Order for Christmas'}, proof=True)]))

# ================================================================= F2 Browse
F2 = dict(id='F2', name='Q4 Browse Abandonment', trigger_short='Viewed Product', replaces='Browse Abandonment (RkFCNW) → Manual on Oct 27',
  trigger='Viewed Product (HtsYBH)',
  filters='No Added to Cart, Checkout Started or Placed Order since starting · not in this flow in the last 3 days · smart sending on',
  exits='Added to Cart / Checkout Started / Placed Order', live='Oct 27 → Jan 10',
  why='The biggest audience of any flow (20,138 recipients in Q4 2025) at only €0.35 per recipient. Faster first touch, the product front and centre, a real reason to act in each phase, and a third email in the sale and Christmas windows.',
  emails=[])

F2['emails'].append(dict(id='F2E1', name='Still looking?', delay='2 hours after viewing', delay_short='2h', phases=ALL, bg='white', banner=B_REC,
  subject={'pre post': 'Still thinking about it?', 'ea': 'Unlock 30% on this.', 'bf cw': 'It’s 30% off now.', 'xmas': 'Gift it by Christmas.', 'late': 'Too late to ship?'},
  preview={'pre post': 'It’s still here for you.', 'ea': 'Join early access to save.', 'bf cw': 'Applied automatically at checkout.',
           'xmas': 'Order by [cut-off date].', 'late': 'Send a gift card instead.'},
  goal='Bring them back to the exact piece with the phase’s reason to buy now.',
  urgency='bf/cw: 30% now; xmas: cut-off; ea: join to unlock. Pre/post: no sale talk (don’t make October shoppers wait).',
  klaviyo='Trigger Viewed Product. ' + VIEW + ' ' + DATE,
  modules=[
    M('headline', title={'pre post': 'Made to stay on.', 'ea': 'Members save 30% on this.', 'bf cw': 'It’s 30% off right now.',
                         'xmas': 'Give it before Christmas.', 'late': 'Too late to ship. Not to give.'},
      sub={'pre post': 'The piece you looked at: waterproof, stainless steel, made to be worn every day.',
           'ea': 'Early access is open. Join and the 30% comes off at checkout, before Friday’s public sale.',
           'bf cw': 'The piece you looked at is 30% off until Sunday, Dec 6. No code needed.',
           'xmas': 'Order by [cut-off date] and it arrives before Christmas.',
           'late': 'Christmas shipping has closed. A gift card lands in their inbox in minutes.'}),
    M('dynamic_product', source='viewed', size='big'),
    M('cta', label={'pre post': 'Take another look', 'ea': 'Join & save 30%', 'bf cw': 'Get it at 30% off', 'xmas': 'Order for Christmas', 'late': 'Send a gift card'}),
    M('note', phases=['ea'], text='Button goes to the early-access sign-up page; members get the 30% straight away.'),
    M('usp_bar', items=['100% waterproof', 'Stainless steel', 'Rated 4.5 on Trustpilot']),
    GC(),
    M('section_header', title='You might also like', label=TAGR),
    M('product_feed', source='viewed_together', count=3)]))

F2['emails'].append(dict(id='F2E2', name='Worth it', delay='+1 day', delay_short='+1d', phases=ALL, bg='fog', banner=B_REC,
  subject={'pre post': 'Worth a second look.', 'ea': 'Still 30% for members.', 'bf cw': 'Still 30% off.', 'xmas': 'The gift they’ll wear.', 'late': 'A gift, in minutes.'},
  preview={'pre post': 'Rated 4.5 on Trustpilot.', 'ea': 'Join today, save 30%.', 'bf cw': 'Ends Sun Dec 6, midnight.',
           'xmas': 'Case included with two pieces.', 'late': 'Digital gift card, sent instantly.'},
  goal='Proof and reassurance for the piece they viewed.', urgency='Deadline row in ea/bf/cw/xmas.',
  klaviyo='As F2E1. ' + VIEW,
  modules=[
    M('score'),
    M('headline', title='Worth it. Ask them.',
      sub={'pre post': 'Rated 4.5 on Trustpilot from 3,000+ reviews.', 'ea': 'Rated 4.5 on Trustpilot, and 30% off for members now.',
           'bf cw': 'Rated 4.5 on Trustpilot from 3,000+ reviews, and still 30% off.', 'xmas': 'Rated 4.5 on Trustpilot. A gift they’ll actually wear.',
           'late': 'Rated 4.5 on Trustpilot. Let them choose with a gift card.'}),
    M('dynamic_product', source='viewed', size='side'),
    M('quote', count=1, who=WHO),
    M('checklist', items=['Waterproof: shower, sea, gym', 'Hypoallergenic stainless steel', 'Adjustable size']),
    dict(CASE, phases=['pre', 'xmas', 'post']), DEADLINE, GC(),
    M('cta', label={'pre post': 'Back to your piece', 'ea': 'Join & save 30%', 'bf cw': 'Get it at 30% off', 'xmas': 'Order for Christmas', 'late': 'Send a gift card'})]))

F2['emails'].append(dict(id='F2E3', name='Before it ends', delay='+2 days', delay_short='+2d', phases=['bf', 'cw', 'xmas'], bg='white', banner=B_REC,
  subject={'bf cw': 'Your 30% ends Sunday.', 'xmas': 'Christmas cut-off: [date].'},
  preview={'bf cw': 'After Sunday, full price.', 'xmas': 'Last day for delivery.'},
  goal='The real deadline, once, with the product.', urgency='Giant date + timeline.',
  klaviyo='Live Nov 27 → [cut-off]; Manual outside. ' + VIEW + ' ' + DATE, notes='Doesn’t send in pre, ea, late or post.',
  modules=[
    M('big_type', kicker={'bf cw': 'Before it ends', 'xmas': 'Before Christmas'}, big={'bf cw': 'Sun 6', 'xmas': '[Dec 17]'},
      title={'bf cw': '30% off ends at midnight.', 'xmas': 'Last day to order for Christmas.'},
      sub={'bf cw': 'The piece you looked at is still 30% off, until Sunday, Dec 6.', 'xmas': 'Order by [cut-off date] and it arrives in time.'}),
    M('timeline', phases=['bf', 'cw'], points=[dict(label='Today', state='now'), dict(label='Sun Dec 6 · Midnight', state='end')]),
    M('timeline', phases=['xmas'], points=[dict(label='Today', state='now'), dict(label='[Cut-off] · Last order', state='end')]),
    M('dynamic_product', source='viewed', size='big'),
    dict(OFFER, phases=['bf', 'cw']), CAL,
    M('cta', label={'bf cw': 'Get it before Sunday', 'xmas': 'Order for Christmas'}, proof=True)]))

# ================================================================= F3 Collection / search
F3 = dict(id='F3', name='Q4 Collection & Search Browse', trigger_short='Viewed Collection / Search', replaces='NEW',
  trigger='Viewed Collection (Shopify, TK8Zdc) · clone the flow for Submitted Search (SwVpBj)',
  filters='No Viewed Product since starting (F2 takes over) · no Added to Cart or Placed Order · not in this flow in 7 days',
  exits='Viewed Product / Added to Cart / Placed Order', live='Oct 27 → Jan 10',
  why='People who browse collections or search but never open a product get nothing today. In gifting season they are the biggest undecided group: a gift guide sorts them by who they’re buying for.',
  emails=[])

GUIDE = M('gift_guide', tiles=[dict(img='lf_w_crossed', label='For her'), dict(img='lf_m_linen_chest', label='For him'),
                                dict(img='p_set_m_silver', label='The Sets', sub='3 pieces'), dict(img='p_giftcard', label='Gift card', sub='Arrives instantly')])
F3['emails'].append(dict(id='F3E1', name='The gift guide', delay='3 hours after', delay_short='3h', phases=ALL, bg='white', banner=B_REC,
  subject={'pre post': 'Find their piece.', 'ea': 'Your 30% gift guide.', 'bf cw': 'Gift guide: 30% off.', 'xmas': 'The Christmas gift guide.', 'late': 'Gifts that arrive instantly.'},
  preview={'pre post': 'For her, him, or you.', 'ea': 'Members shop first, 30% off.', 'bf cw': 'Every piece, no code needed.',
           'xmas': 'Order by [cut-off date].', 'late': 'Send a gift card now.'},
  goal='Sort an undecided browser by recipient, then into a product page.', urgency='Phase offer bar / cut-off calendar.',
  klaviyo='Trigger Viewed Collection. ' + DATE + ' Feed blocks: best sellers.',
  notes='Viewed Collection event fields not checked yet: add the collection name to the headline once confirmed.',
  modules=[
    M('headline', kicker={'pre post': 'Gift guide', 'ea': 'Early access · Gift guide', 'bf cw': '30% off · Gift guide', 'xmas': 'Christmas gift guide',
                          'late': 'Last-minute gifts'}, title='Who are you shopping for?', sub='Start with who it’s for. We’ll take it from there.'),
    GUIDE, OFFER, CAL, GC(),
    M('section_header', title='Best sellers', label=TAGR), M('product_feed', source='bestsellers', count=3),
    M('cta', label={'pre post': 'Shop the gift guide', 'ea': 'Join & shop 30% off', 'bf cw': 'Shop the gift guide', 'xmas': 'Shop for Christmas',
                    'late': 'Send a gift card'}, proof=True)]))

F3['emails'].append(dict(id='F3E2', name='Start here', delay='+1 day', delay_short='+1d', phases=ALL, bg='fog', banner=B_REC,
  subject={'pre post': 'Our best sellers.', 'ea bf cw': 'Best sellers, 30% off.', 'xmas': 'Our best-selling gifts.', 'late': 'Best gift: the choice.'},
  preview={'pre post': 'Start with the Set.', 'ea': 'Members only, until Friday.', 'bf cw': 'Ends Sun Dec 6, midnight.',
           'xmas': 'Order by [cut-off date].', 'late': 'Gift cards arrive in minutes.'},
  goal='Hand the undecided the safest first pick.', urgency='Deadline row.', klaviyo='As F3E1.',
  modules=[
    M('hero_photo', img={'W': 'lf_w_black_bracelet', 'M': 'lf_m_wrist_close'}, shape='tall'),
    M('headline', align='left', title='Start here.', sub='The pieces most people choose first, and keep on.'),
    M('product_feed', source='bestsellers', count=3),
    M('split', img={'W': 'p_set_w', 'M': 'p_set_m'}, kicker='Best seller', title='3x Minimal Set',
      body='Three pieces, one decision, and the jewelry case comes with it.', cta='Shop the Set'),
    DEADLINE, GC(),
    M('cta', label={'pre post': 'Shop best sellers', 'ea': 'Join & save 30%', 'bf cw': 'Shop 30% off', 'xmas': 'Shop for Christmas', 'late': 'Send a gift card'})]))

# ================================================================= F4 Cart
F4 = dict(id='F4', name='Q4 Add to Cart', trigger_short='Added to Cart', replaces='Add to Cart Abandoned (Syiqdb) → Manual on Oct 27',
  trigger='Added to Cart (Shopify, WBpdcS) — not the API metric, silent since Sep 2',
  filters='No Checkout Started or Placed Order since starting · not in this flow in 3 days · smart sending on',
  exits='Checkout Started / Placed Order', live='Oct 27 → Jan 10',
  why='€8,643 at €0.86 per recipient in Q4 2025. Faster first touch, a pair-and-case push to lift order value, and a real-deadline third email.',
  emails=[])

F4['emails'].append(dict(id='F4E1', name='Still yours', delay='1 hour after', delay_short='1h', phases=ALL, bg='white', banner=B_REC,
  subject={'pre post': 'Still in your cart.', 'ea': 'Your cart, 30% off?', 'bf cw': 'Your cart, 30% off.', 'xmas': 'Your gift is waiting.', 'late': 'Too late? Gift card.'},
  preview={'pre post': 'We saved it for you.', 'ea': 'Join early access to save.', 'bf cw': 'Already applied at checkout.',
           'xmas': 'Order by [cut-off date].', 'late': 'Arrives in their inbox instantly.'},
  goal='One tap back to the cart.', urgency='Phase line under the product.', klaviyo='Trigger Shopify Added to Cart. ' + CART + ' ' + DATE,
  modules=[
    M('headline', size='xl', title='Still yours.',
      sub={'pre post': 'We saved your pick. Two pieces or more and the jewelry case comes with it.',
           'ea': 'Join early access and 30% comes off this at checkout, before Friday.',
           'bf cw': 'We saved your pick. 30% comes off automatically at checkout.',
           'xmas': 'We saved your pick. Order by [cut-off] for Christmas delivery.',
           'late': 'Shipping won’t make Christmas now. A gift card will.'}),
    M('dynamic_product', source='cart', size='big'),
    M('cta', label={'pre post': 'Return to cart', 'ea': 'Join & check out', 'bf cw': 'Check out at 30% off', 'xmas': 'Check out for Christmas', 'late': 'Send a gift card'}),
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
    M('cta', label={'pre post': 'Complete the pair', 'ea': 'Join & save 30%', 'bf cw': 'Pair it at 30% off', 'xmas': 'Order for Christmas', 'late': 'Send a gift card'})]))

F4['emails'].append(dict(id='F4E3', name='Before it ends', delay='+1 day', delay_short='+1d', phases=['pre', 'ea', 'bf', 'cw', 'xmas', 'post'], bg='white', banner=B_REC,
  subject={'pre post': 'Last reminder: your cart.', 'ea': 'Early access ends Friday.', 'bf cw': '30% ends on Sunday.', 'xmas': 'Last day for Christmas.'},
  preview={'pre post': 'Waterproof steel, made to stay.', 'ea': 'Then it opens to everyone.', 'bf cw': 'Your cart, still 30% off.', 'xmas': 'Order by [cut-off date].'},
  goal='Close the cart on the phase deadline.', urgency='Giant date + deadline row.', klaviyo='As F4E1.', notes='Doesn’t send in late (F4E1 already offers the gift card).',
  modules=[
    M('big_type', kicker={'pre post': 'Your cart', 'ea': 'Early access', 'bf cw': 'Before it ends', 'xmas': 'Christmas'},
      big={'pre post': 'Still here.', 'ea': 'Fri 27', 'bf cw': 'Sun 6', 'xmas': '[Dec 17]'},
      title={'pre post': 'Your pick is waiting.', 'ea': 'Members’ 30% ends.', 'bf cw': '30% off ends at midnight.', 'xmas': 'Last day for delivery.'}),
    dict(DEADLINE, phases=['ea', 'bf', 'cw', 'xmas']),
    M('dynamic_product', source='cart', size='big'),
    M('quote', count=1, who=WHO),
    M('cta', label={'pre post': 'Return to cart', 'ea': 'Shop before Friday', 'bf cw': 'Check out at 30% off', 'xmas': 'Order for Christmas'}, proof=True)]))

# ================================================================= F5 Checkout
F5 = dict(id='F5', name='Q4 Checkout Recovery', trigger_short='Checkout Started', replaces='Checkout Abandoned (Ub2mSt) → Manual on Oct 27',
  trigger='Checkout Started (Shopify, LrhH24) — not the API “Started Checkout”', filters='No Placed Order since starting · smart sending off for E1',
  exits='Placed Order', live='Oct 27 → Jan 10',
  why='The top earner: €10,886 at €1.37 per recipient in Q4 2025, and the first email did most of it (€1.90–2.02 per recipient). Keep the fast first touch, show the real cart and total, then delivery certainty and proof, and end on the real deadline.',
  emails=[])

F5['emails'].append(dict(id='F5E1', name='One step left', delay='45 minutes after', delay_short='45m', phases=ALL, bg='white', banner=B_REC,
  subject={'pre ea bf cw post': 'One step left.', 'xmas': 'One step to Christmas.', 'late': 'Your order is saved.'},
  preview={'pre post': 'Your order is saved.', 'ea': 'Finish before the public sale.', 'bf cw': 'Your 30% is already applied.',
           'xmas': 'Order by [cut-off date].', 'late': 'Or send a gift card.'},
  goal='Back to checkout in one tap, with the real total.', urgency='Deadline row in ea/bf/cw/xmas.',
  klaviyo='Trigger Shopify Checkout Started. ' + CHK + ' ' + DATE,
  modules=[
    M('headline', title={'pre ea bf cw post': 'One step left.', 'xmas': 'One step to Christmas.', 'late': 'Your order is saved.'},
      sub={'pre ea post': 'Everything you picked is saved. Finish in one tap.', 'bf cw': 'Your order is saved, with 30% off already applied.',
           'xmas': 'Finish by [cut-off date] and it arrives before Christmas.',
           'late': 'Christmas delivery has closed. Finish it for yourself, or send a gift card.'}),
    M('order_table'),
    M('cta', label='Complete my order', note='Questions? Reply to this email.'),
    DEADLINE, GC(text='A digital gift card lands in their inbox in minutes. Any amount.')]))

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
    M('offer_list', phases=['pre', 'ea', 'xmas', 'late', 'post'], rows=[['Shipping', '[shipping offer to confirm]'], ['Two or more pieces', 'Jewelry case included'], ['Checkout', 'Secure']]),
    CAL, GC(),
    M('order_table', compact=True),
    M('faq', items=[['When will it arrive?', '[Delivery times by region — to confirm]'], ['Will it tarnish or rust?', 'No. 316L stainless steel, 100% waterproof.'],
                    ['Will it fit?', 'Every bracelet adjusts with an extension chain.']]),
    M('cta', label='Complete my order')]))

F5['emails'].append(dict(id='F5E3', name='Loved, then worn daily', delay='+1 day', delay_short='+1d', phases=ALL, bg='white', banner=B_REC,
  subject='Why they kept theirs.', preview='Rated 4.5 on Trustpilot.',
  goal='Trust: proof, then the cart.', urgency='Deadline row.', klaviyo='As F5E1. Compact table. ' + GEN + ' for the two quotes.',
  modules=[
    M('score'), M('headline', title='Loved, then worn daily.', sub='Rated 4.5 on Trustpilot from 3,000+ reviews.'),
    M('quote', count=2, who=WHO),
    M('hero_photo', img={'W': 'lf_w_chair', 'M': 'lf_m_hand_rock'}, shape='inset'),
    M('order_table', compact=True), DEADLINE,
    M('cta', label='Complete my order')]))

F5['emails'].append(dict(id='F5E4', name='Final hours', delay='+2 days', delay_short='+2d', phases=['bf', 'cw', 'xmas'], bg='white', banner=B_REC,
  subject={'bf': 'Still saved, still 30%.', 'cw': '30% ends on Sunday.', 'xmas': 'Last day for delivery.'},
  preview={'bf': 'Until Sun Dec 6, midnight.', 'cw': 'After that, full price.', 'xmas': 'Order by [cut-off date].'},
  goal='The real deadline; last email before full price or the cut-off.', urgency='Giant headline + deadline row.',
  klaviyo='Live Nov 27 → [cut-off]; Manual outside. As F5E1. On Dec 6: ' + C("{% if d == '2026-12-06' %}") + ' swaps the headline to “Final hours.”',
  notes='Doesn’t send in pre, ea, late or post.',
  modules=[
    M('headline', size='xl', title={'bf': 'Still saved for you.', 'cw': 'Before it ends.', 'xmas': 'Last day for Christmas.'},
      sub={'bf': 'Your 30% stays applied until Sunday, Dec 6 at midnight.', 'cw': '30% off ends Sunday, Dec 6 at midnight. After that, full price.',
           'xmas': 'Finish by [cut-off date] and it arrives before Christmas.'}),
    M('deadline', label={'bf cw': '30% off until', 'xmas': 'Last order'}, value={'bf cw': 'Sun Dec 6, midnight', 'xmas': '[cut-off date]'}),
    M('order_table', compact=True),
    M('cta', label='Complete my order', note='Questions? Reply to this email.')]))

# ================================================================= F6 Post-purchase
F6 = dict(id='F6', name='Q4 Post-Purchase · Gifting', trigger_short='Placed Order', replaces='NEW (none exists)',
  trigger='Placed Order (Shopify, M8VZY5)', filters='Not in this flow in 14 days · smart sending on except E1', exits='E3 skips if they ordered again',
  live='Oct 27 → Jan 10 · Trustpilot review flow stays live alongside',
  why='There is no post-purchase flow. A Black Friday buyer is the warmest Christmas customer there is: confirm and reassure, then turn them into the gift-giver while 30% and Christmas delivery still apply.',
  emails=[])

F6['emails'].append(dict(id='F6E1', name='Thank you', delay='1 hour after', delay_short='1h', phases=ALL, bg='white', banner=B_WEL,
  subject='Thank you. Truly.',
  preview={'pre post': 'Here’s what happens next.', 'ea bf cw': 'Gifts too? Still 30% off.', 'xmas': 'More gifts? Order by [cut-off].', 'late': 'Gift cards arrive instantly.'},
  goal='Confirm, set expectations, and open the gift list while the offer lasts.', urgency='Deadline row in bf/cw/xmas.',
  klaviyo='Trigger Placed Order. Smart sending off. ' + DATE + ' ' + GEN,
  modules=[
    M('headline', title='Thank you.', sub='Your order is confirmed. Here’s what happens next.'),
    M('steps', items=['We pack it, with the jewelry case if you chose 2+ pieces.', 'It ships with tracking: [delivery times to confirm].', 'Put it on. Leave it on.']),
    M('section_header', title={'pre post': 'Complete the look', 'ea bf cw': 'While it’s 30% off', 'xmas': 'Their gift, sorted', 'late': 'Last-minute gifts'},
      label={'pre post': 'Case with 2+', 'ea': 'Members until Fri 27', 'bf cw': 'Until Sun Dec 6', 'xmas': 'Order by [cut-off]', 'late': 'Gift cards'}),
    GUIDE,
    M('deadline', phases=['bf', 'cw', 'xmas'], label={'bf cw': '30% off ends', 'xmas': 'Christmas delivery'}, value={'bf cw': 'Sun Dec 6, midnight', 'xmas': 'Order by [cut-off]'}),
    M('cta', label={'pre post': 'Shop the collection', 'ea': 'Shop early access', 'bf cw': 'Shop gifts at 30% off', 'xmas': 'Shop gifts for Christmas', 'late': 'Send a gift card'}),
    M('text', size='s', body='Questions about your order? Reply to this email.')]))

F6['emails'].append(dict(id='F6E2', name='How to wear it', delay='+4 days', delay_short='+4d', phases=ALL, bg='fog', banner=B_WEL,
  subject='How to wear it.', preview='Stack, layer, leave it on.',
  goal='Delight, then cross-sell the piece that completes theirs.', urgency='Offer bar in the sale.',
  klaviyo='Smart sending on. Feed: “Recommended for you” (based on what they bought). ' + DATE + ' ' + GEN,
  modules=[
    M('hero_photo', img={'W': 'lf_w_crossed', 'M': 'lf_m_hand_hair'}, shape='tall'),
    M('headline', title='Stack it. Layer it. Leave it on.'),
    M('steps', items=['Start with one. Add a second in another texture.', 'Layer necklaces at two lengths.', 'Pull the extension chain for a close fit.']),
    M('split', img={'W': 'p_braid_silver', 'M': 'p_braid_black'}, kicker='Pairs well', title='Braid Bracelet',
      body='The texture that makes a Set look considered.', cta='Shop the Braid'),
    M('section_header', title='Picked for you', label=TAGR), M('product_feed', source='recommended', count=3),
    dict(OFFER, phases=['bf', 'cw']),
    M('cta', label={'pre post': 'Shop the collection', 'ea': 'Shop early access', 'bf cw': 'Shop 30% off', 'xmas': 'Shop for Christmas', 'late': 'Send a gift card'})]))

F6['emails'].append(dict(id='F6E3', name='One for them', delay='+8 days', delay_short='+8d', phases=['ea', 'bf', 'cw', 'xmas', 'late'], bg='white', banner=B_WEL,
  subject={'ea bf cw': 'One for them?', 'xmas': 'Their gift, sorted.', 'late': 'A gift in minutes.'},
  preview={'ea': 'Members’ 30% until Friday.', 'bf cw': '30% off until Sun Dec 6.', 'xmas': 'Order by [cut-off date].', 'late': 'Gift cards arrive instantly.'},
  goal='Turn a happy buyer into the gift-giver.', urgency='Deadline row.',
  klaviyo='Filter: no Placed Order in the last 7 days. Live Nov 23 → Dec 24; Manual outside. ' + DATE + ' ' + GEN, notes='Doesn’t send in pre or post.',
  modules=[
    M('big_type', kicker='You love yours', big={'ea bf cw': '30%', 'xmas': 'Gifts.', 'late': 'Now.'},
      title={'ea bf cw': 'off their gift, too.', 'xmas': 'Give what you wear.', 'late': 'Send a gift card.'},
      sub={'ea': 'Members’ 30% runs until Friday, Nov 27.', 'bf cw': '30% off everything until Sunday, Dec 6 at midnight.',
           'xmas': 'Order by [cut-off date] for Christmas delivery.', 'late': 'Christmas shipping has closed. A gift card arrives in minutes.'}),
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
  preview={'pre': 'Customers shop first, Nov 23.', 'ea': 'Before the public sale Friday.', 'bf cw': 'Everything, applied at checkout.',
           'xmas': 'Order by [cut-off date].', 'late': 'Choose an amount, send now.', 'post': 'Case included with two pieces.'},
  goal='Give a lapsed customer a reason to return: first access, then 30%.', urgency='Pass ticket + timeline.',
  klaviyo='Trigger: segment. Lapsed customers must be in the early-access audience for the pre/ea promise. Feed: “Recommended for you”. ' + DATE + ' ' + GEN,
  modules=[
    M('headline', kicker='For customers',
      title={'pre': 'You’re on the early-access list.', 'ea': 'Your early access is open.', 'bf cw': '30% off. Everything.', 'xmas': 'Back for Christmas?',
             'late': 'Too late to ship? Give the choice.', 'post': 'Ready for the next one?'},
      sub={'pre': 'As a customer you shop 30% off everything from Monday, Nov 23, before the public sale.',
           'ea': 'Shop 30% off now, before it opens to everyone on Friday.', 'bf cw': 'Every piece, every finish, until Sunday, Dec 6. No code.',
           'xmas': 'Order by [cut-off date] for delivery before Christmas.', 'late': 'A gift card lands in their inbox in minutes.',
           'post': 'Two pieces or more and the jewelry case comes with them.'}),
    TICKET, *TL_SALE()[:3],
    M('hero_photo', img={'W': 'lf_w_face_wet', 'M': 'lf_m_beach_arm'}, shape='wide'),
    M('section_header', title='Picked for you', label=TAG), M('product_feed', source='recommended', count=3),
    CAL, GC(),
    M('cta', label={'pre': 'Add to calendar', 'ea': 'Shop early access', 'bf cw': 'Shop 30% off', 'xmas': 'Shop for Christmas', 'late': 'Send a gift card',
                    'post': 'Shop what’s new'}, proof=True)]))

F7['emails'].append(dict(id='F7E2', name='What’s new', delay='+3 days', delay_short='+3d', phases=ALL, bg='fog', banner=B_WEL,
  subject={'pre post': 'What’s new at Cavaier.', 'ea': 'Members’ 30% is open.', 'bf': '30% off, everything.', 'cw': 'New: the Matte Cuff.',
           'xmas': 'The gift guide.', 'late': 'Gift cards, sent instantly.'},
  preview={'pre post': 'Sets, cuffs and the classics.', 'ea': 'Before the public sale Friday.', 'bf': 'Applied automatically at checkout.',
           'cw': '30% off until Sunday.', 'xmas': 'Order by [cut-off date].', 'late': 'They choose. You look good.'},
  goal='Show what changed since their last order.', urgency='Offer bar in the sale.',
  klaviyo='As F7E1. Matte Cuff block only from 2026-11-28.', notes='Matte Cuff photo pending: Minimal Cuff shown as a stand-in.',
  modules=[
    M('headline', align='left', title={'pre post': 'What’s new.', 'ea': 'Members first.', 'bf': '30% off. Everything.', 'cw': 'New: the Matte Cuff.',
                                       'xmas': 'Gifts, sorted.', 'late': 'Give the choice.'}),
    M('split', phases=['cw'], img='p_cuff_black', kicker='New · from Nov 28', title='The Matte Cuff',
      body='Our cuff, in a matte finish. 30% off until Sunday. [Matte Cuff photo pending — Minimal Cuff shown]', cta='Shop the Matte Cuff'),
    M('split', phases=['pre', 'ea', 'bf', 'xmas', 'post'], img={'W': 'p_set_w_gold', 'M': 'p_set_m_silver'}, kicker='Best seller', title='3x Minimal Set',
      body='Black, silver or gold. The one most people start with.', cta='Shop the Set'),
    M('product_grid', cols=3, items=[
        dict(gender='W', img='p_role_pend_worn', name='Role Pendant Necklace', tag=TAG), dict(gender='W', img='p_cuban_neck_worn', name='Cuban Necklace', tag=TAG),
        dict(gender='W', img='p_crystal_br', name='Crystal Bracelet', tag=TAG), dict(gender='M', img='p_rope_neck_worn', name='Rope Pendant Necklace', tag=TAG),
        dict(gender='M', img='p_cube_br_m', name='Cube Bracelet', tag=TAG), dict(gender='M', img='p_cuff_worn', name='Minimal Cuff', tag=TAG)]),
    dict(OFFER, phases=['ea', 'bf', 'cw']), GC(),
    M('cta', label={'pre post': 'Shop what’s new', 'ea': 'Shop early access', 'bf': 'Shop 30% off', 'cw': 'Shop the Matte Cuff', 'xmas': 'Shop the gift guide',
                    'late': 'Send a gift card'})]))

F7['emails'].append(dict(id='F7E3', name='Last call', delay='+4 days', delay_short='+4d', phases=['ea', 'bf', 'cw', 'xmas'], bg='white', banner=B_WEL,
  subject={'ea': 'Early access ends Friday.', 'bf': 'Don’t wait for Sunday.', 'cw': 'Last call: 30% off.', 'xmas': 'Last call for Christmas.'},
  preview={'ea': 'Then it opens to everyone.', 'bf': '30% ends Sun Dec 6.', 'cw': 'Ends Sun Dec 6, midnight.', 'xmas': 'Order by [cut-off date].'},
  goal='Close on the real deadline.', urgency='Giant date + deadline row.',
  klaviyo='Live Nov 23 → [cut-off]; Manual outside. As F7E1.', notes='Doesn’t send in pre, late or post.',
  modules=[
    M('big_type', kicker={'ea': 'Early access', 'bf cw': 'Before it ends', 'xmas': 'Christmas'}, big={'ea': 'Fri 27', 'bf cw': 'Sun 6', 'xmas': '[Dec 17]'},
      title={'ea': 'Customers’ head start ends.', 'bf cw': '30% off ends at midnight.', 'xmas': 'Last day for delivery.'}),
    DEADLINE, M('product_feed', source='recommended', count=3), M('quote', count=1, who=WHO),
    M('cta', label={'ea': 'Shop before Friday', 'bf cw': 'Shop before it ends', 'xmas': 'Order for Christmas'}, proof=True)]))

# ================================================================= F8 Sunset
F8 = dict(id='F8', name='Pre-Black Friday Sunset', trigger_short='Unengaged 120 days', replaces='Sunset Flow (YiWP9H) → Manual on Oct 19',
  trigger='Segment entry: subscribed, no open or click in 120 days', filters='Runs Oct 19 → Nov 15 only', exits='Clicked any email (stays on the list)',
  live='Oct 19 → Nov 15, then suppress non-clickers before Nov 22',
  why='Inbox placement decides Black Friday. Sending the sale to people who never open drags every send towards spam. Ask once, keep the ones who answer, suppress the rest before Nov 23.',
  emails=[])

F8['emails'].append(dict(id='F8E1', name='Stay for Black Friday?', delay='On entry', delay_short='0', phases=['pre'], bg='white', banner={'pre': 'Early access · Opens Mon Nov 23'},
  subject='Still want early access?', preview='One tap keeps you listed.',
  goal='A click that proves they want to stay.', urgency='Nov 15 cut-off for staying on the list.',
  klaviyo='Trigger: segment. Any click = engaged → leaves the sunset segment. ' + GEN,
  modules=[
    M('headline', size='xl', title='Stay for Black Friday?', sub='Members shop 30% off everything first, from Monday, Nov 23. Tap below and you stay on the list.'),
    M('cta', label='Keep me on the list'), TICKET,
    M('hero_photo', img={'W': 'lf_w_chair', 'M': 'lf_m_linen_chest'}, shape='inset'),
    M('text', size='s', body='Not for you anymore? No hard feelings. Do nothing and we’ll stop emailing you after Nov 15.')]))

F8['emails'].append(dict(id='F8E2', name='Last email?', delay='+5 days', delay_short='+5d', phases=['pre'], bg='fog', banner={'pre': 'Early access · Opens Mon Nov 23'},
  subject='Last email from us?', preview='Unless you tap below.',
  goal='Final chance to stay before suppression.', urgency='The list closes Nov 15.', klaviyo='As F8E1.',
  modules=[
    M('big_type', big='Last one.', title='Unless you want early access.', sub='Tap once and you’re on the list for 30% off everything from Monday, Nov 23.'),
    M('cta', label='Yes, keep me on'),
    M('text', size='s', body='Do nothing and this is the last email you’ll get from us.')]))

# ================================================================= F9 Back in stock
F9 = dict(id='F9', name='Back in Stock', trigger_short='Back in Stock', replaces='NEW',
  trigger='Klaviyo Back in Stock trigger (subscribers from the back-in-stock form, metric NdHAwx)', filters='Their variant is back · smart sending off',
  exits='Placed Order', live='Oct 27 → Jan 10',
  why='Variants sell out on the 30% weekend. Waiting lists are high-intent and need one fast email per restock.',
  emails=[])

F9['emails'].append(dict(id='F9E1', name='It’s back', delay='When their variant restocks', delay_short='on restock', phases=ALL, bg='white', banner=B_REC,
  subject={'pre ea post late': 'It’s back in stock.', 'bf cw': 'Back, and 30% off.', 'xmas': 'Back for Christmas.'},
  preview={'pre ea post late': 'The one you waited for.', 'bf cw': '30% off at checkout.', 'xmas': 'Order by [cut-off date].'},
  goal='Convert the waiting list the moment it restocks.', urgency='Real restock + phase offer.',
  klaviyo='Back in Stock event fields (product name, image, URL, price) in the product block. ' + DATE,
  modules=[
    M('headline', size='xl', title='It’s back.',
      sub={'pre ea post late': 'The piece you asked about is in stock again.', 'bf cw': 'The piece you asked about is in stock again, and 30% off until Sunday, Dec 6.',
           'xmas': 'In stock again, and in time: order by [cut-off] for Christmas.'}),
    M('dynamic_product', source='bis', size='big'),
    M('cta', label={'pre ea post late': 'Shop it now', 'bf cw': 'Get it at 30% off', 'xmas': 'Order for Christmas'}),
    USP,
    M('text', size='s', body='You’re getting this because you asked to hear when it was back.')]))

FLOWS = [F1, F2, F3, F4, F5, F6, F7, F8, F9]

# ================================================================= page copy
PAGE = {}
PAGE['intro'] = '''  <header class="intro narrow">
    <span class="kicker">Cavaier · Q4 2026 · Klaviyo flows · mock-up</span>
    <h1>Q4 flows: Black Friday to Christmas</h1>
    <p>{n_flows} flows and {n_emails} emails that replace the evergreen flows from Oct 27 to Jan 10. Every email changes with the calendar, inside one Klaviyo template: use the bar to switch women’s / men’s and the Q4 phase. Brief card on the right of each email: send time, subject and preview for the phase, the job, the urgency device and the Klaviyo build. Mock-up only: nothing is live in Klaviyo.</p>
  </header>'''

PAGE['top'] = '''  <section class="card narrow">
    <span class="kicker">What the Q4 flows have to beat · Q4 2025, email, Placed Order</span>
    <div class="stats">
      <div><b>€10,886</b><span>Checkout Abandoned · €1.37 per recipient · 8,212 recipients</span></div>
      <div><b>€8,643</b><span>Add to Cart · €0.86 per recipient · 10,068 recipients</span></div>
      <div><b>€7,048</b><span>Browse · €0.35 per recipient · 20,138 recipients</span></div>
      <div><b>€231</b><span>Winback · €0.02 per recipient · 11,172 recipients</span></div>
    </div>
    <p class="notes">Also in Q4 2025: Aimerce app flows €4,094 (Checkout €1,916, Browse €1,683, Add to Cart €401, Site abandonment €93) and the Trustpilot review flow €1,147. About €32,000 from flows in total. No welcome or post-purchase flow sent in Q4 2025.</p>
  </section>

  <section class="card narrow">
    <span class="kicker">The Q4 calendar · every email switches by date</span>
    <div class="cal">
      <div><i>Pre-sale</i><b>Oct 27 – Nov 22</b><span>Join early access. No sale talk in recovery flows.</span></div>
      <div><i>Early access</i><b>Nov 23 – 26</b><span>Members shop 30% off first.</span></div>
      <div><i>Black Friday</i><b>Nov 27 – 30</b><span>30% off everything, incl. Cyber Monday. Matte Cuff Nov 28.</span></div>
      <div><i>Cyber Week</i><b>Dec 1 – 6</b><span>30% ends Sun Dec 6, midnight.</span></div>
      <div><i>Christmas</i><b>Dec 7 – [cut-off]</b><span>Gifting, case with 2+, order-by dates.</span></div>
      <div><i>Last minute</i><b>[cut-off] – Dec 24</b><span>Digital gift card.</span></div>
      <div><i>After Christmas</i><b>Dec 26 – Jan 10</b><span>New year, treat yourself.</span></div>
    </div>
  </section>'''

PAGE['bottom'] = '''  <section class="card narrow">
    <span class="kicker">Switchover plan</span>
    <div class="tbl" style="border:0"><table style="min-width:0"><tbody>
      <tr><td class="n"><b>Oct 13 – 16</b></td><td>Build F1–F9 in Klaviyo as drafts: one template per email, phase blocks by date, W/M blocks by Gender. Test each phase in a copy with the date thresholds moved.</td></tr>
      <tr><td class="n"><b>Mon Oct 19</b></td><td>F8 Sunset live. Sunset Flow (YiWP9H) → Manual.</td></tr>
      <tr><td class="n"><b>Tue Oct 27, 09:00</b></td><td>F1–F7 and F9 live. Same hour → Manual: Welcome Series (QVmUhV), Browse Abandonment (RkFCNW), Add to Cart Abandoned (Syiqdb), Checkout Abandoned (Ub2mSt), Customer Winback (VipiiT). Emails waiting in a Manual flow don’t send. Send the one-off winback launch campaign to the lapsed segment. Check the Aimerce app flows are off (they sent in Q4 2025) or shoppers get two of everything.</td></tr>
      <tr><td class="n"><b>Sun Nov 15</b></td><td>F8 off. Nov 16–22: suppress profiles who got both sunset emails and didn’t click.</td></tr>
      <tr><td class="n"><b>Mon Nov 23</b></td><td>Window emails on: F1E5, F5E4 (from Nov 27), F2E3 (from Nov 27), F6E3, F7E3. Everything else switches copy by itself.</td></tr>
      <tr><td class="n"><b>[Cut-off date]</b></td><td>Fill every [cut-off] placeholder once the dates are confirmed. F1E5, F2E3, F5E4, F7E3 → Manual after the cut-off.</td></tr>
      <tr><td class="n"><b>Fri Dec 25</b></td><td>No flow sends: send-time windows skip Christmas Day.</td></tr>
      <tr><td class="n"><b>Sun Jan 10</b></td><td>Q4 flows → Manual, evergreen flows back on. Keep F6 Post-purchase and F3 live if they beat the old numbers.</td></tr>
    </tbody></table></div>
  </section>

  <section class="card narrow">
    <span class="kicker">Priority and frequency</span>
    <ul class="levers">
      <li><b>One recovery flow at a time, highest intent wins:</b> Checkout (F5) › Cart (F4) › Browse (F2) › Collection (F3). Each lower flow’s filter excludes the higher events since it started.</li>
      <li><b>Smart sending (16 h)</b> on every email except F1E1, F5E1, F6E1 and F9E1.</li>
      <li><b>Campaign days</b> (Nov 23, 27, 30, Dec 6, cut-off day): campaigns go to engaged segments and exclude anyone who got a flow email in the last 12 hours.</li>
      <li><b>Re-entry:</b> checkout 1 day, cart and browse 3 days, collection 7 days, post-purchase 14 days.</li>
      <li><b>Send windows:</b> 08:00–21:00 recipient-local on F2, F3, F4 and F7 delays.</li>
      <li><b>No fixed prices</b> in static blocks (multi-currency list). Dynamic blocks print the event price; checkout emails print the real discount and total.</li>
    </ul>
  </section>

  <section class="card narrow">
    <span class="kicker">Open items</span>
    <ul class="levers">
      <li><b>Christmas cut-off dates</b> per region (CEO): fill every [cut-off] and the order-by calendar.</li>
      <li><b>Christmas and after-Christmas offer</b>, if any, and the shipping offer outside Nov 23 – Dec 6. The December emails sell without a discount until then.</li>
      <li><b>Trustpilot quotes</b> (Katrina): every quote is a placeholder.</li>
      <li><b>Matte Cuff photos</b> (launches Nov 28): F7E2 shows the Minimal Cuff as a stand-in.</li>
      <li><b>Customers in early access:</b> F7 promises lapsed customers first access, so they need to be in the early-access audience.</li>
      <li><b>Viewed Collection fields</b> (F3) and the <b>gift-card delivery</b> setup (“arrives instantly”, scheduled delivery) to confirm in Shopify/Klaviyo.</li>
      <li><b>Figma:</b> the Figma connection dropped in this session; reconnect it (claude.ai connector settings) before frames can be synced.</li>
    </ul>
  </section>'''
