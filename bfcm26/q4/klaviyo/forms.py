"""Q4 sign-up pop-ups -> Klaviyo forms (drafts). python3 forms.py EU|US
Clones the live POP-UP form (styles, background image, display rules, lists), then sets the Q4 copy for each sale period:
step 1 email -> step 2 phone (SMS consent) -> step 3 who do you shop for -> done. One draft form per period."""
import os, sys, json, re, copy, time, html as H, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__)); Q4 = os.path.dirname(HERE)
sys.path.insert(0, Q4)
import q4_specs as Q
A = sys.argv[1]
LIVE = {'EU': 'SyHM2E', 'US': 'YdzGsM'}[A]
ST = os.path.join(Q4, 'sync_state.json')


def call(path, body=None, method=None):
    req = urllib.request.Request('https://a.klaviyo.com/api/' + path, data=json.dumps(body).encode() if body is not None else None,
                                 method=method or ('POST' if body is not None else 'GET'),
                                 headers={'Authorization': 'Klaviyo-API-Key ' + os.environ['KLAVIYO_KEY_' + A], 'revision': '2026-01-15',
                                          'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json'})
    for i in range(6):
        try:
            r = urllib.request.urlopen(req, timeout=120); t = r.read(); return json.loads(t) if t else {}
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503): time.sleep(2 ** i); continue
            raise Exception(f'{e.code} {path}: {e.read().decode()[:2000]}')


PH = ['pre', 'ea', 'bf', 'xmas', 'late', 'post']
PNAME = {'pre': 'Pre-sale', 'ea': 'Early access', 'bf': 'Black Friday + Cyber Week', 'xmas': 'Christmas', 'late': 'Last minute', 'post': 'After Christmas'}
DAY = {p: next((d for d in Q.DAYS if d['phase'] == p and d['default']), None) or next(d for d in Q.DAYS if d['phase'] == p) for p in PH}
def txt(v, p):
    if isinstance(v, dict): v = next((x for k, x in v.items() if p in k.split()), '')
    return re.sub(r'«(\w+)»', lambda m: DAY[p].get(m.group(1), ''), v)
FONT = "Helvetica, Arial, sans-serif"
def block_html(kick, head, sub, mobile):
    hs, ss = (34, 15) if mobile else (52, 17)
    o = ''
    if kick: o += f'<p style="text-align:center;line-height:1.4;letter-spacing:2px;font-family:{FONT};font-size:11px;color:rgb(168,44,36)">{H.escape(kick.upper())}</p>'
    o += f'<p style="text-align:center;line-height:1.05;letter-spacing:-1px;font-family:{FONT};font-size:{hs}px;color:rgb(11,11,11)">{H.escape(head)}</p>'
    if sub: o += f'<p style="text-align:center;line-height:1.5;font-family:{FONT};font-size:{ss}px;color:rgb(58,58,56)">{H.escape(sub)}</p>'
    return o
def strip_ids(o):
    if isinstance(o, dict): return {k: strip_ids(v) for k, v in o.items() if k != 'id'}
    if isinstance(o, list): return [strip_ids(x) for x in o]
    return o
def blocks(step):
    for c in step['columns']:
        for r in c['rows']:
            for b in r['blocks']: yield r, b
def set_texts(step, kick, head, sub):
    for r, b in blocks(step):
        if b['type'] == 'html_text':
            b['properties']['content'] = block_html(kick, head, sub, b['properties'].get('display_device') == ['mobile'])
def build(live, p):
    v = copy.deepcopy(live)
    steps = {s['name'] or 'Success': s for s in v['steps']}
    gender, email, sms, done = steps['Micro Commit'], steps['Email Opt-In'], steps['SMS Opt-In'], steps['Success']
    P = Q.POPUP
    set_texts(email, txt(P['kick'], p), txt(P['head'], p), txt(P['sub'], p))
    for r, b in blocks(email):
        if b['type'] == 'button': b['properties']['label'] = txt(P['cta'], p).upper()
    set_texts(sms, 'One more step', txt(P['sms_head'], p), txt(P['sms_sub'], p))
    for r, b in blocks(sms):
        if b['type'] == 'button': b['properties']['label'] = 'TEXT ME'
    set_texts(gender, 'One more tap', 'Who do you shop for?', 'So every email shows the right pieces.')
    rows = [r for r, b in blocks(gender) if b['type'] == 'button']
    for r, b in blocks(gender):
        if b['type'] == 'button':
            g = b['properties']['additional_fields'][0]['value']
            b['properties']['label'] = g.upper()
    both = copy.deepcopy(rows[-1])  # third button: Both
    for b in both['blocks']:
        b['properties']['label'] = 'BOTH'; b['properties']['additional_fields'] = [{'name': 'Gender', 'value': 'Both'}]
    gender['columns'][0]['rows'].insert(gender['columns'][0]['rows'].index(rows[-1]) + 1, both)
    set_texts(done, txt(P['kick'], p), txt(P['done_head'], p), txt(P['done_sub'], p))
    for r, b in blocks(done):
        if b['type'] == 'button': b['properties']['label'] = ('Keep browsing' if p == 'pre' else txt(P['done_cta'], p)).upper()  # the button closes the form
    email['name'], sms['name'], gender['name'], done['name'] = 'Email', 'Phone (SMS)', 'Who do you shop for', 'Done'
    v['steps'] = [email, sms, gender, done]
    for t in v['triggers']:  # never on cart or checkout pages
        if t['type'] == 'url_patterns': t['properties'] = {'allow_list': None, 'deny_list': ['*/cart*', '*/checkouts/*', '*/checkout*']}
    v['name'] = f'Q4 · {PNAME[p]}'
    v['status'] = 'draft'
    return strip_ids(v)
live_def = call(f'forms/{LIVE}/')['data']['attributes']['definition']
live = next(x for x in live_def['versions'] if x.get('status') == 'live')
state = json.load(open(ST)); K = state.setdefault('klaviyo', {}).setdefault(A, {}).setdefault('forms', {})
for p in PH:
    if p in K: continue
    d = {'versions': [build(live, p)]}
    res = call('forms/', {'data': {'type': 'form', 'attributes': {'name': f'Q4 Pop-up · {PNAME[p]}', 'status': 'draft', 'ab_test': False, 'definition': d}}})
    K[p] = res['data']['id']; json.dump(state, open(ST, 'w'), indent=1); print('form', p, K[p])
