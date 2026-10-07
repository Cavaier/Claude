"""Q4 sign-up pop-ups -> Klaviyo forms (drafts), built to the Figma / dashboard design. python3 forms.py EU|US [--replace]
Left: the two black-and-white photos (one side image). Right: logo, red kicker, light headline, sub, field, black button,
fine print, "Not now". Steps: email -> phone (SMS consent) -> who do you shop for (Women / Men / Both) -> done.
Teaser tab bottom-left after closing. Hidden on cart and checkout. One draft form per sale period."""
import os, sys, json, re, copy, time, io, uuid, base64, html as H, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); Q4 = os.path.dirname(HERE)
sys.path.insert(0, Q4); sys.path.insert(0, HERE)
import q4_specs as Q
from preview import g as GEN
from PIL import Image
A = sys.argv[1]; REPLACE = '--replace' in sys.argv
LIVE = {'EU': 'SyHM2E', 'US': 'YdzGsM'}[A]
ST = os.path.join(Q4, 'sync_state.json')


def call(path, body=None, method=None, raw=None, ctype='application/vnd.api+json'):
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request('https://a.klaviyo.com/api/' + path, data=data, method=method or ('POST' if data is not None else 'GET'),
                                 headers={'Authorization': 'Klaviyo-API-Key ' + os.environ['KLAVIYO_KEY_' + A], 'revision': '2026-01-15',
                                          'accept': 'application/vnd.api+json', 'content-type': ctype})
    for i in range(6):
        try:
            r = urllib.request.urlopen(req, timeout=120); t = r.read(); return json.loads(t) if t else {}
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503): time.sleep(2 ** i); continue
            raise Exception(f'{e.code} {path}: {e.read().decode()[:2000]}')


def upload(name, data, mime):
    bnd = uuid.uuid4().hex; ext = 'png' if 'png' in mime else 'jpg'
    body = (f'--{bnd}\r\nContent-Disposition: form-data; name="name"\r\n\r\n{name}\r\n'
            f'--{bnd}\r\nContent-Disposition: form-data; name="file"; filename="{uuid.uuid4().hex[:8]}.{ext}"\r\nContent-Type: {mime}\r\n\r\n').encode() + data + f'\r\n--{bnd}--\r\n'.encode()
    d = call('image-upload/', raw=body, ctype=f'multipart/form-data; boundary={bnd}')['data']
    return {'src': d['attributes']['image_url'], 'alt_text': None, 'original_image_url': None, 'id': int(d['id']), 'asset_id': int(d['id'])}


state = json.load(open(ST)); K = state.setdefault('klaviyo', {}).setdefault(A, {})
def save(): json.dump(state, open(ST, 'w'), indent=1)

# ---------------------------------------------------------------- assets: the two photos as one side image, and the logo
FA = K.setdefault('form_assets', {})
if 'side' not in FA:
    def photo(k):
        uri = GEN['load_img'](k); return Image.open(io.BytesIO(base64.b64decode(uri.split(',', 1)[1]))).convert('RGB')
    W, Hh = 1200, 1500; out = Image.new('RGB', (W, Hh), (232, 232, 230))
    for i, k in enumerate(['lf_w_black_top', 'lf_m_linen_chin']):  # same pair as the mock-up
        im = photo(k); s = max(600 / im.width, Hh / im.height); im = im.resize((round(im.width * s), round(im.height * s)))
        x0 = (im.width - 600) // 2; y0 = (im.height - Hh) // 2; out.paste(im.crop((x0, y0, x0 + 600, y0 + Hh)), (i * 600, 0))
    b = io.BytesIO(); out.save(b, 'JPEG', quality=82); FA['side'] = upload('Q4 · pop-up photos', b.getvalue(), 'image/jpeg'); save()
if 'mobile' not in FA:  # mobile: the same two photos as a 300 px strip on top (as in the mock-up)
    def photo(k):
        uri = GEN['load_img'](k); return Image.open(io.BytesIO(base64.b64decode(uri.split(',', 1)[1]))).convert('RGB')
    W, Hh = 780, 600; out = Image.new('RGB', (W, Hh), (232, 232, 230))
    for i, k in enumerate(['lf_w_black_top', 'lf_m_linen_chin']):
        im = photo(k); s_ = max(390 / im.width, Hh / im.height); im = im.resize((round(im.width * s_), round(im.height * s_)))
        x0 = (im.width - 390) // 2; y0 = (im.height - Hh) // 3; out.paste(im.crop((x0, y0, x0 + 390, y0 + Hh)), (i * 390, 0))
    b = io.BytesIO(); out.save(b, 'JPEG', quality=82); FA['mobile'] = upload('Q4 · pop-up photos (mobile)', b.getvalue(), 'image/jpeg'); save()
if 'logo' not in FA:
    FA['logo'] = upload('Q4 · logo', open(os.path.join(Q4, 'logo0.png'), 'rb').read(), 'image/png'); save()

# ---------------------------------------------------------------- design tokens (from popup.css)
FONT = "Figtree, 'Helvetica Neue', Helvetica, Arial, sans-serif"
BLACK, INK2, GREY, RED, BG = '#0B0B0B', '#3A3A38', '#8B8B88', '#A82C24', '#F2F2F1'
def ts(size, weight=400, color=BLACK, spacing=0):
    return {'font_family': FONT, 'font_size': size, 'font_weight': weight, 'text_color': color, 'character_spacing': spacing, 'font_style': 'normal', 'text_decoration': None}
def pad(t=0, b=0, l=0, r=0): return {'left': l, 'right': r, 'top': t, 'bottom': b}
def html(content, dev, t=0, b=0):
    return {'type': 'html_text', 'styles': {'padding': pad(t, b, 6, 6), 'background_color': None},
            'properties': {'display_device': dev, 'classname': None, 'block_animation': None, 'content': content}}
def P(text, size, weight=300, color=BLACK, spacing=0, lh=1.15):
    return (f'<p style="text-align:center;line-height:{lh};letter-spacing:{spacing}px;color:{color};font-family:{FONT};font-size:{size}px;font-weight:{weight}">'
            f'{text}</p>')
def button(label, action, filled=True, extra=None, height=54):
    return {'type': 'button', 'styles': {'padding': pad(5, 5, 6, 6), 'background_color': None, 'width': 'fill', 'inner_padding': None, 'height': height,
            'alignment': 'center', 'hover_background_color': None, 'hover_text_color': None,
            'border_styles': {'radius': 0, 'color': BLACK if not filled else None, 'style': 'solid' if not filled else None, 'thickness': 1 if not filled else None},
            'text_styles': ts(12, 500, '#FFFFFF' if filled else BLACK, 2), 'color': BLACK if filled else '#FFFFFF',
            'drop_shadow': {'enabled': False, 'color': '#000000', 'blur': 15, 'x_offset': 0, 'y_offset': 0}},
            'properties': {'display_device': ['desktop', 'mobile'], 'classname': None, 'block_animation': None, 'label': label.upper(), 'additional_fields': extra or []},
            'action': action}
def link(label, action):  # "Not now" / "Skip": text-only button
    b = button(label, action, filled=False, height=30)
    b['styles']['border_styles'] = {'radius': 0, 'color': None, 'style': None, 'thickness': None}
    b['styles']['color'] = 'rgba(0,0,0,0)'; b['styles']['text_styles'] = ts(12, 400, INK2, 0); b['styles']['text_styles']['text_decoration'] = 'underline'
    b['properties']['label'] = label
    return b
def logo():
    return {'type': 'image', 'styles': {'horizontal_alignment': 'center', 'width': 84, 'padding': pad(0, 28), 'background_color': None,
            'drop_shadow': {'enabled': False, 'color': '#000000', 'blur': 15, 'x_offset': 0, 'y_offset': 0}},
            'properties': {'display_device': ['desktop', 'mobile'], 'classname': None, 'block_animation': None, 'image': FA['logo'], 'additional_fields': None}, 'action': None}
def headblocks(kick, head, sub):
    out = []
    for dev, hs, ss in ((['desktop'], 54, 16), (['mobile'], 34, 14.5)):
        c = (f'<p style="text-align:center;margin:0 0 26px"><img src="{FA["logo"]["src"]}" width="84" alt="Cavaier"></p>' +
             (P(H.escape(kick.upper()), 10.5, 500, RED, 2, 1.4) if kick else '') + P(H.escape(head), hs, 300, BLACK, -1.5, 1.02))
        if sub: c += P(H.escape(sub), ss, 300, INK2, 0, 1.55)
        out.append(html(c, dev, 4, 14))
    return out
def mphoto():
    return {'type': 'image', 'styles': {'horizontal_alignment': 'center', 'width': 390, 'padding': pad(0, 18), 'background_color': None,
            'drop_shadow': {'enabled': False, 'color': '#000000', 'blur': 15, 'x_offset': 0, 'y_offset': 0}},
            'properties': {'display_device': ['mobile'], 'classname': None, 'block_animation': None, 'image': FA['mobile'], 'additional_fields': None}, 'action': None}
def step(name, rows):
    # Klaviyo: blocks in one row sit side by side; at most 6 rows per column; content column styles must be null next to a side image
    side = {'rows': [], 'styles': {'background_color': None, 'background_image': {
        'styles': {'horizontal_alignment': 'center', 'width': 1200, 'position': 'cover', 'vertical_alignment': 'center', 'custom_width': None}, 'properties': FA['side']}}}
    rows = [[mphoto()]] + rows
    assert len(rows) <= 6, (name, len(rows))
    return {'name': name, 'columns': [side, {'rows': [{'blocks': r} for r in rows], 'styles': None}]}

# ---------------------------------------------------------------- copy per sale period
PH = ['pre', 'ea', 'bf', 'xmas', 'late', 'post']
PNAME = {'pre': 'Pre-sale', 'ea': 'Early access', 'bf': 'Black Friday + Cyber Week', 'xmas': 'Christmas', 'late': 'Last minute', 'post': 'After Christmas'}
DAY = {p: next((d for d in Q.DAYS if d['phase'] == p and d['default']), None) or next(d for d in Q.DAYS if d['phase'] == p) for p in PH}
def txt(v, p):
    if isinstance(v, dict): v = next((x for k, x in v.items() if p in k.split()), '')
    return re.sub(r'«(\w+)»', lambda m: DAY[p].get(m.group(1), ''), v)

live_def = call(f'forms/{LIVE}/')['data']['attributes']['definition']
live = next(x for x in live_def['versions'] if x.get('status') == 'live')
def walk():
    for s in live['steps']:
        for c in s['columns']:
            for r in c['rows']:
                for b in r['blocks']: yield s, b
def find(t): return next((copy.deepcopy(b) for s, b in walk() if b['type'] == t), None)
LISTS = {s['name']: b['action']['properties']['list_id'] for s, b in walk()
         if (b.get('action') or {}).get('type') == 'next_step' and (b['action'].get('properties') or {}).get('list_id')}
EMAIL_LIST, SMS_LIST = LISTS['Email Opt-In'], LISTS['SMS Opt-In']
NEXT = lambda lst=None, submit=True: {'submit': submit, 'type': 'next_step', 'properties': {'list_id': lst} if lst else {}}
CLOSE = {'submit': False, 'type': 'close', 'properties': {}}

def strip_ids(o):
    if isinstance(o, dict): return {k: strip_ids(v) for k, v in o.items() if k != 'id'}
    if isinstance(o, list): return [strip_ids(x) for x in o]
    return o

def version(p):
    PU = Q.POPUP
    email_in = find('email'); email_in['properties']['placeholder'] = 'Email address'
    phone_in = find('phone_number'); phone_in['properties']['placeholder'] = 'Phone number'
    disclosure = find('sms_disclosure')
    src = [{'name': '$source', 'value': 'POPUP26'}]
    fine = html(P('By signing up you agree to receive marketing emails from Cavaier. Unsubscribe anytime.', 11, 300, GREY, 0, 1.5), ['desktop', 'mobile'], 6, 0)
    s1 = step('Email', [headblocks(txt(PU['kick'], p), txt(PU['head'], p), txt(PU['sub'], p)), [email_in],
                        [button(txt(PU['cta'], p), NEXT(EMAIL_LIST), extra=src)], [fine], [link('Not now', CLOSE)]])
    s2 = step('Phone (SMS)', [headblocks('One more step', txt(PU['sms_head'], p), txt(PU['sms_sub'], p)), [phone_in],
                              [button('Text me', NEXT(SMS_LIST), extra=src)]] + ([[disclosure]] if disclosure else []) + [[link('No thanks', NEXT(EMAIL_LIST))]])
    who = [button(g, NEXT(EMAIL_LIST), filled=False, extra=[{'name': 'Gender', 'value': g}]) for g in ('Women', 'Men', 'Both')]
    s3 = step('Who do you shop for', [headblocks('One more tap', 'Who do you shop for?', 'So every email shows the right pieces.'), who, [link('Skip', NEXT(EMAIL_LIST))]])
    done_cta = 'Keep browsing' if p == 'pre' else txt(PU['done_cta'], p)  # the button closes the form
    s4 = step('Done', [headblocks(txt(PU['kick'], p), txt(PU['done_head'], p), txt(PU['done_sub'], p)), [button(done_cta, CLOSE)],
                       [html(P('★★★★★ &nbsp;Rated 4.5 on Trustpilot · 3,000+ reviews', 12, 300, INK2, 0, 1.4), ['desktop', 'mobile'], 16, 0)]])
    v = copy.deepcopy(live)
    v['steps'] = [s1, s2, s3, s4]
    v['name'] = f'Q4 · {PNAME[p]}'; v['status'] = 'draft'
    v['properties'] = dict(v.get('properties') or {}, side_image_settings={'size': 'large', 'alignment': 'left', 'device_type': ['desktop']},
                           show_close_button=True, rule_based_trigger_evaluation='any')
    st = v['styles']
    st.update(background_color=BG, background_image=None, width='custom', custom_width=1100, minimum_height=640,
              padding=pad(60, 60, 70, 70), border_styles={'radius': 0, 'color': '#000000', 'style': None, 'thickness': 0},
              overlay_color='rgba(11,11,11,0.55)')
    st['close_button'] = {'background_color': 'rgba(255,255,255,0)', 'outline_color': 'rgba(255,255,255,0)', 'color': BLACK, 'stroke': 1, 'size': 30,
                          'margin': {'left': 14, 'right': 14, 'top': 14, 'bottom': 14}}
    st['input_styles'] = dict(st.get('input_styles') or {}, text_styles=ts(15, 300, BLACK), label_color=BLACK, text_color=BLACK, placeholder_color=GREY,
                              background_color='#FFFFFF', border_color='#BDBDBA', border_focus_color=BLACK, corner_radius=0, field_height=52)
    for r in (st.get('rich_text_styles') or {}).values():
        if isinstance(r, dict) and 'font_family' in r: r['font_family'] = FONT
    # display rules from the plan: after 5 s, on exit intent or on the 2nd page view; never on cart / checkout; back after 3 days
    v['triggers'] = [{'type': 'unidentified_profiles', 'properties': {}}, {'type': 'previously_submitted', 'properties': {}},
                     {'type': 'after_close_or_submit_timeout', 'properties': {'timeout_days': 3}},
                     {'type': 'delay', 'properties': {'seconds': 5}}, {'type': 'exit_intent', 'properties': {}}, {'type': 'page_visits', 'properties': {'pages': 2}},
                     {'type': 'url_patterns', 'properties': {'allow_list': None, 'deny_list': ['*/cart*', '*/checkouts/*', '*/checkout*']}}]
    v['teasers'] = [{'content': P(H.escape(txt(PU['teaser'], p).upper()) + ' ›', 11, 500, '#FFFFFF', 2, 1), 'display_order': 'after', 'teaser_type': 'rectangle',
                     'location': 'bottom_left', 'size': 'small', 'styles': {'background_color': BLACK, 'corner_radius': 0,
                     'drop_shadow': {'enabled': False, 'blur': 30, 'color': 'rgba(0,0,0,0.15)'}}, 'close_button': True, 'device_type': 'both'}]
    return strip_ids(v)

F = K.setdefault('forms', {})
for p in PH:
    if p in F and not REPLACE and not str(F[p]).startswith('v1:'): continue
    old = str(F.get(p, '')).replace('v1:', '')
    if old:
        try: call(f'forms/{old}/', method='DELETE')
        except Exception as ex: print('delete failed', old, str(ex)[:200])
    res = call('forms/', {'data': {'type': 'form', 'attributes': {'name': f'Q4 Pop-up · {PNAME[p]}', 'status': 'draft', 'ab_test': False,
                                                                  'definition': {'versions': [version(p)]}}}})
    F[p] = res['data']['id']; save(); print('form', p, F[p])
