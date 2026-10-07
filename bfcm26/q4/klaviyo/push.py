"""Q4 push to Klaviyo. python3 push.py EU|US [step ...]
Steps: images templates lists segments flows campaigns backfill (default: all, in that order).
Everything is created as a draft. Nothing is set live, nothing is sent. Ids land in ../sync_state.json['klaviyo'][acct]."""
import os, sys, json, time, re, base64, hashlib, uuid, urllib.request, urllib.parse
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); Q4 = os.path.dirname(HERE)
sys.path.insert(0, Q4); sys.path.insert(0, HERE)
import q4_specs as Q
from emailer import R
from preview import IMG as LOCALIMG
ST = os.path.join(Q4, 'sync_state.json')
REV = '2026-01-15'
ACCT = sys.argv[1]; STEPS = sys.argv[2:] or ['images', 'templates', 'lists', 'segments', 'flows', 'campaigns', 'backfill']
BASE = 'https://cavaier.com' if ACCT == 'EU' else 'https://us.cavaier.com'


def call(path, body=None, method=None, raw=None, ctype='application/vnd.api+json'):
    k = os.environ['KLAVIYO_KEY_' + ACCT]
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    req = urllib.request.Request('https://a.klaviyo.com/api/' + path, data=data, method=method or ('POST' if data is not None else 'GET'),
                                 headers={'Authorization': 'Klaviyo-API-Key ' + k, 'revision': REV, 'accept': 'application/vnd.api+json', 'content-type': ctype})
    for i in range(7):
        try:
            r = urllib.request.urlopen(req, timeout=120); t = r.read(); return json.loads(t) if t else {}
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(min(60, 2 ** i)); continue
            raise Exception(f'{e.code} {path}: {e.read().decode()[:1500]}')
        except (ConnectionError, TimeoutError, urllib.error.URLError) as e:
            time.sleep(min(60, 2 ** i))
    raise Exception(f'gave up on {path}')


def pages(path):
    while path:
        d = call(path); yield from d['data']
        nx = d.get('links', {}).get('next'); path = nx.split('/api/')[1] if nx else None


state = json.load(open(ST))
K = state.setdefault('klaviyo', {}).setdefault(ACCT, {})
def save(): json.dump(state, open(ST, 'w'), indent=1)
def H(o): return hashlib.sha1(json.dumps(o, sort_keys=True, default=str).encode()).hexdigest()[:16]

# ---------------------------------------------------------------- account map (ids never copied across accounts)
FLOWS_NOW = {}
for f in pages('flows/?page[size]=50'):
    FLOWS_NOW[f['attributes']['name']] = f['id']
def flowdef(name):
    fid = FLOWS_NOW.get(name)
    if not fid: return None
    time.sleep(1.1)
    return call(f'flows/{fid}/?additional-fields[flow]=definition')['data']['attributes']['definition']
METRICS = {}
for m in pages('metrics/'):
    METRICS.setdefault(m['attributes']['name'], []).append(m['id'])
def metric(name): return METRICS[name][0]
if 'map' not in K:
    br, atc, chk, wel = (flowdef(n) for n in ('Browse Abandonment', 'Add to Cart Abandoned', 'Checkout Abandoned', 'Welcome Series'))
    M = dict(viewed=br['triggers'][0]['id'], cart=atc['triggers'][0]['id'], checkout=chk['triggers'][0]['id'], welcome_list=wel['triggers'][0]['id'],
             ordered=metric('Ordered Product'), active=metric('Active on Site'), collection=metric('Viewed Collection'), clicked=metric('Clicked Email'))
    M['order'] = next(c['metric_id'] for g_ in chk['profile_filter']['condition_groups'] for c in g_['conditions'] if c.get('type') == 'profile-metric')
    LISTS = {l['attributes']['name']: l['id'] for l in pages('lists/')}
    M['sms_list'] = LISTS.get('SMS List') or LISTS.get('SMS-List')
    msg = next(a['data']['message'] for a in chk['actions'] if a['type'] == 'send-email')
    K['map'] = dict(metrics=M, from_email=msg['from_email'], from_label=msg['from_label']); save()
M = K['map']['metrics']
print(ACCT, 'map', K['map'])

# ---------------------------------------------------------------- images
class Rec(dict):
    def __missing__(s, k): s[k] = f'https://example.invalid/{k}'; return s[k]
def emails():
    for f in Q.FLOWS:
        for e in f['emails']:
            if not e.get('kind'): yield f, e
def used_images():
    rec = Rec()
    for f, e in emails(): R(ACCT, f['id'], rec).email(e)
    for k in ('logo', 'ic_ig', 'ic_tt', 'ic_fb'): rec[k]
    return sorted(rec)
def upload(k):
    uri = LOCALIMG()[k]; mime, b64 = uri[5:].split(';base64,'); data = base64.b64decode(b64)
    bnd = uuid.uuid4().hex; ext = 'png' if 'png' in mime else 'jpg'
    body = (f'--{bnd}\r\nContent-Disposition: form-data; name="name"\r\n\r\nQ4 · {k}\r\n'
            f'--{bnd}\r\nContent-Disposition: form-data; name="file"; filename="q4_{k}.{ext}"\r\nContent-Type: {mime}\r\n\r\n').encode() + data + f'\r\n--{bnd}--\r\n'.encode()
    return call('image-upload/', raw=body, ctype=f'multipart/form-data; boundary={bnd}')['data']['attributes']['image_url']
def step_images():
    I = K.setdefault('images', {})
    for k in used_images():
        if k not in I: I[k] = upload(k); save(); print('image', k)
    print('images', len(I))

# ---------------------------------------------------------------- templates (one per email; phase + Gender logic inside)
def step_templates():
    T = K.setdefault('templates', {}); I = K['images']
    for f, e in emails():
        r = R(ACCT, f['id'], I); html = r.email(e); h = H(html); name = f'Q4 · {e["id"]} · {e["name"]}'
        cur = T.get(e['id'])
        if cur and cur['hash'] == h: continue
        if cur: call(f'templates/{cur["id"]}/', {'data': {'type': 'template', 'id': cur['id'], 'attributes': {'name': name, 'html': html}}}, 'PATCH'); tid = cur['id']
        else: tid = call('templates/', {'data': {'type': 'template', 'attributes': {'name': name, 'editor_type': 'CODE', 'html': html}}})['data']['id']
        T[e['id']] = dict(id=tid, hash=h); save(); print('template', e['id'], tid)
    print('templates', len(T))

# ---------------------------------------------------------------- lists and segments
def step_lists():
    L = K.setdefault('lists', {}); have = {l['attributes']['name']: l['id'] for l in pages('lists/')}
    for key, name in [('winback', 'Q4 · Winback'), ('second', 'Q4 · Second purchase'), ('sunset', 'Q4 · Sunset'), ('salelive', 'Q4 · Sale live')]:
        if key not in L:
            L[key] = have.get(name) or call('lists/', {'data': {'type': 'list', 'attributes': {'name': name}}})['data']['id']; save(); print('list', name, L[key])
def pm(mid, op, val, tf, filters=None):
    return {'type': 'profile-metric', 'metric_id': mid, 'measurement': 'count', 'measurement_filter': {'type': 'numeric', 'operator': op, 'value': val},
            'timeframe_filter': tf, 'metric_filters': filters}
LAST = lambda n: {'type': 'date', 'operator': 'in-the-last', 'unit': 'day', 'quantity': n}
ALLTIME = {'type': 'date', 'operator': 'alltime'}
CONSENT = lambda ch: {'type': 'profile-marketing-consent', 'consent': {'channel': ch, 'can_receive_marketing': True, 'consent_status': {'subscription': 'subscribed'}}}
SEGS = {
    'lapsed': ('Q4 · Lapsed 120+ days (bulk-add to Q4 · Winback)', lambda: [[pm(M['order'], 'greater-than', 0, ALLTIME)], [pm(M['order'], 'equals', 0, LAST(120))]]),
    'second': ('Q4 · One order, 30–119 days ago (bulk-add to Q4 · Second purchase)', lambda: [[pm(M['order'], 'equals', 1, ALLTIME)], [pm(M['order'], 'equals', 0, LAST(30))]]),
    'unengaged': ('Q4 · No click or order in 120 days (bulk-add to Q4 · Sunset)', lambda: [[pm(M['clicked'], 'equals', 0, LAST(120))], [pm(M['order'], 'equals', 0, LAST(120))], [CONSENT('email')]]),
    'browsed': ('Q4 · Browsed in 30 days, no order (bulk-add to Q4 · Sale live)', lambda: [[pm(M['viewed'], 'greater-than', 0, LAST(30)), pm(M['cart'], 'greater-than', 0, LAST(30))], [pm(M['order'], 'equals', 0, LAST(30))]]),
    'sms': ('Q4 · Can receive SMS', lambda: [[CONSENT('sms')]]),
    'popup_presale': ('Q4 · Pop-up list, no order in 30 days (F1E6 / F1E7 campaigns)', lambda: [[{'type': 'profile-group-membership', 'is_member': True, 'group_ids': [M['welcome_list']]}], [pm(M['order'], 'equals', 0, LAST(30))]]),
    'giftcard': ('Q4 · Bought a gift card in the last 60 days (F13E2 campaign)', lambda: [[pm(M['ordered'], 'greater-than', 0, LAST(60), [{'property': 'Name', 'filter': {'type': 'string', 'operator': 'contains', 'value': 'Gift Card'}}])]]),
    'gender_set': ('Q4 · Gender set', lambda: [[{'type': 'profile-property', 'property': "properties['Gender']", 'filter': {'type': 'existence', 'operator': 'is-set'}}]]),
}
def step_segments():
    S = K.setdefault('segments', {}); have = {s['attributes']['name']: s['id'] for s in pages('segments/')}
    for key, (name, fn) in SEGS.items():
        if key in S: continue
        try:
            S[key] = have.get(name) or call('segments/', {'data': {'type': 'segment', 'attributes': {'name': name, 'definition': {'condition_groups': [{'conditions': c} for c in fn()]}}}})['data']['id']
            save(); print('segment', name, S[key])
        except Exception as ex: print('SEGMENT FAILED', name, str(ex)[:400])

# ---------------------------------------------------------------- flows (drafts)
class FB:
    def __init__(s): s.acts = []; s.n = 0; s.prev = []
    def add(s, typ, data, nexts=('next',)):
        s.n += 1; a = {'temporary_id': f'a{s.n}', 'type': typ, 'data': data, 'links': {}}
        for act, key in s.prev: act['links'][key] = a['temporary_id']
        s.acts.append(a); s.prev = [(a, k) for k in nexts]; return a
    def delay(s, ds):
        m = re.fullmatch(r'\+?(\d+)([mhd])', ds or '')
        if m: s.add('time-delay', {'unit': {'m': 'minutes', 'h': 'hours', 'd': 'days'}[m.group(2)], 'value': int(m.group(1)), 'secondary_value': None, 'timezone': 'profile'})
def since_start(*mids): return [{'conditions': [pm(x, 'equals', 0, {'type': 'date', 'operator': 'flow-start'})]} for x in mids]
def not_in_flow(days): return [{'conditions': [{'type': 'profile-not-in-flow', 'timeframe_filter': LAST(days)}]}]
SMS_SPLIT = {'condition_groups': [{'conditions': [{'type': 'profile-marketing-consent', 'consent': {'channel': 'sms', 'can_receive_marketing': True, 'consent_status': {'subscription': 'subscribed', 'filters': None}}}]}]}
NO_SS = {'F1E1', 'F5E1', 'F6E1', 'F9E1'}
SKIP_IN_FLOW = {'F1E6', 'F1E7', 'F10E3', 'F13E2'}  # fixed dates: drafted as campaigns (no "wait until date" in the flow API)
def sms_body(f, e, r):
    prod = {'F2': '{{ event.Name }}', 'F4': "{{ event|lookup:'Product Name' }}", 'F9': '{{ event.ProductName }}'}.get(f['id'], '')
    link = {'F2': '{{ event.URL }}', 'F4': BASE + '/cart', 'F5': '{{ event.extra.checkout_url }}', 'F9': '{{ event.URL }}'}.get(f['id'])
    one = lambda txt, ph: txt.replace('{product}', prod).replace('{link}', link or (BASE + '/products/cavaier-gift-card' if ph == 'late' else r.shop()))
    tx = e['text']
    if isinstance(tx, str): return one(tx, e['phases'][0])
    out, first = "{% today '%Y-%m-%d' as d %}", True
    for k, v in tx.items():
        out += ('{% if ' if first else '{% elif ') + (r.cond(k.split()) or 'True') + ' %}' + one(v, k.split()[0]); first = False
    return out + '{% endif %}'
# subject + preview: full date logic when it fits Klaviyo's 250 characters, else the current period's text
# (switched on each period's first day by `push.py EU subjects`)
import datetime
SWITCH = [('pre', '2026-11-23'), ('ea', '2026-11-27'), ('bf', '2026-12-01'), ('cw', '2026-12-07'), ('xmas', '2026-12-18'), ('late', '2026-12-25')]
def phase_now(day=None):
    day = day or datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    return next((p for p, end in SWITCH if day < end), 'post')
def subj_prev(r, e, phase=None):
    out = []
    for v in (e['subject'], e['preview']):
        logic = r.short(v, e['phases'])
        out.append(logic if len(logic) <= 250 else r.phase_texts(v, e['phases'])[phase or phase_now()])
    return out
def build_flow(f):
    fid, L = f['id'], K['lists']; fb = FB(); r = R(ACCT, fid, K['images']); T = K['templates']; pf = []
    trig = {
        'F1': {'type': 'list', 'id': M['welcome_list']},
        'F2': {'type': 'metric', 'id': M['viewed'], 'trigger_filter': None}, 'F3': {'type': 'metric', 'id': M['collection'], 'trigger_filter': None},
        'F4': {'type': 'metric', 'id': M['cart'], 'trigger_filter': None}, 'F5': {'type': 'metric', 'id': M['checkout'], 'trigger_filter': None},
        'F6': {'type': 'metric', 'id': M['order'], 'trigger_filter': None}, 'F7': {'type': 'list', 'id': L['winback']}, 'F8': {'type': 'list', 'id': L['sunset']},
        'F10': {'type': 'list', 'id': L['salelive']}, 'F11': {'type': 'list', 'id': L['second']}, 'F12': {'type': 'metric', 'id': M['active'], 'trigger_filter': None},
        'F13': {'type': 'metric', 'id': M['ordered'], 'trigger_filter': {'condition_groups': [{'conditions': [{'type': 'metric-property', 'metric_id': M['ordered'], 'field': 'Name', 'filter': {'type': 'string', 'operator': 'contains', 'value': 'Gift Card'}}]}]}},
        'S1': {'type': 'list', 'id': M['sms_list']}}.get(fid)
    if trig is None: return None  # F9: the Back in Stock trigger can't be created through the API
    pf = {'F2': since_start(M['cart'], M['checkout'], M['order']) + not_in_flow(3), 'F3': since_start(M['viewed'], M['cart'], M['checkout'], M['order']) + not_in_flow(7),
          'F4': since_start(M['checkout'], M['order']) + not_in_flow(3), 'F5': since_start(M['order']) + not_in_flow(1), 'F6': not_in_flow(14),
          'F7': since_start(M['order']), 'F8': since_start(M['clicked']), 'F10': since_start(M['order']), 'F11': since_start(M['order']),
          'F12': since_start(M['viewed'], M['cart'], M['order']) + not_in_flow(7), 'S1': not_in_flow(3650)}.get(fid, [])
    for e in f['emails']:
        if e['id'] in SKIP_IN_FLOW: continue
        fb.delay(e['delay_short'])
        if e.get('kind') == 'sms':
            split = fb.add('conditional-split', {'profile_filter': SMS_SPLIT}, ('next_if_true', 'next_if_false'))
            fb.prev = [(split, 'next_if_true')]
            sms = fb.add('send-sms', {'message': {'body': sms_body(f, e, r), 'shorten_links': True, 'add_org_prefix': False, 'add_info_link': False,
                         'add_opt_out_language': True, 'smart_sending_enabled': e['id'] != 'F5T1', 'sms_quiet_hours_enabled': True, 'transactional': False,
                         'add_tracking_params': True, 'name': f'{e["id"]} · {e["name"]}'}, 'status': 'draft'})
            fb.prev = [(sms, 'next'), (split, 'next_if_false')]
            continue
        t = T[e['id']]; sj, pv = subj_prev(r, e)
        fb.add('send-email', {'message': {'from_email': K['map']['from_email'], 'from_label': K['map']['from_label'], 'subject_line': sj, 'preview_text': pv,
               'template_id': t['id'], 'smart_sending_enabled': e['id'] not in NO_SS, 'transactional': False, 'add_tracking_params': True, 'name': f'{e["id"]} · {e["name"]}'},
               'status': 'draft'})
    return dict(triggers=[trig], profile_filter={'condition_groups': pf} if pf else None, actions=fb.acts, entry_action_id=fb.acts[0]['temporary_id'], reentry_criteria=None)
MEN_ORD = ['For Him', "Men's Sets", 'Men Necklace', 'You may also like - Men - Necklace']
WOMEN_ORD = ['For Her', "Women's Sets", 'Women Necklace', 'You may also like - Women - Necklace']
def build_gender(kind):
    fb = FB()
    if kind == 'G1': mid, prop, men, women, tf, need, src = M['ordered'], 'Collections', MEN_ORD, WOMEN_ORD, ALLTIME, 0, 'order'
    else:
        mid, prop, men, women, tf, need, src = M['viewed'], 'Categories', Q.MEN_CATS, Q.WOMEN_CATS, LAST(14), 1, 'browsing'
        fb.add('time-delay', {'unit': 'hours', 'value': 1, 'secondary_value': None, 'timezone': 'profile'})
    anyof = lambda vals: [{'property': prop, 'filter': {'type': 'list', 'operator': 'contains-any', 'value': vals}}]
    has = lambda vals: pm(mid, 'greater-than', need, tf, anyof(vals))
    none = lambda vals: pm(mid, 'equals', 0, tf, anyof(vals))
    branches = [('Men', [[has(men)], [none(women)]]), ('Women', [[has(women)], [none(men)]])] + ([('Both', [[has(men)], [has(women)]])] if kind == 'G1' else [])
    split = fb.add('multi-branch-split', {'name': 'Which side', 'branches': [
        {'branch_id': f'b{i}', 'branch_filter': {'condition_groups': [{'conditions': c} for c in conds]}, 'links': {}, 'order': i, 'name': f'Gender = {gv}'} for i, (gv, conds) in enumerate(branches)]
        + [{'branch_id': 'else', 'branch_filter': None, 'links': None, 'is_else': True}]}, ())
    for i, (gv, _) in enumerate(branches):
        fb.prev = []
        a = fb.add('update-profile', {'profile_operations': [
            {'operator': 'update', 'property_type': 'string', 'property_key': "properties['Gender']", 'property_value': gv},
            {'operator': 'create', 'property_type': 'string', 'property_key': "properties['Gender source']", 'property_value': src}], 'status': 'draft'})
        split['data']['branches'][i]['links'] = {'next': a['temporary_id']}
    pf = [{'conditions': [{'type': 'profile-property', 'property': "properties['Gender']", 'filter': {'type': 'existence', 'operator': 'not-set'}}]}]
    return dict(triggers=[{'type': 'metric', 'id': mid, 'trigger_filter': None}], profile_filter={'condition_groups': pf}, actions=fb.acts,
                entry_action_id=fb.acts[0]['temporary_id'], reentry_criteria=None)
def step_flows():
    F = K.setdefault('flows', {})
    for f, d in [(f, build_flow(f)) for f in Q.FLOWS + [Q.S1]] + [(Q.G1, build_gender('G1')), (Q.G2, build_gender('G2'))]:
        if d is None: F[f['id']] = dict(id=None, note='build by hand: Back in Stock trigger, templates are ready'); save(); continue
        h = H(d); cur = F.get(f['id'])
        if cur and cur.get('hash') == h: continue
        if cur and cur.get('id'):  # flows can't be edited through the API: replace our own draft
            try: call(f'flows/{cur["id"]}/', method='DELETE')
            except Exception as ex: print('delete failed', cur['id'], str(ex)[:200])
        time.sleep(1.2)
        res = call('flows/', {'data': {'type': 'flow', 'attributes': {'name': f'Q4 · {f["id"]} · {f["name"]}', 'definition': d}}})
        F[f['id']] = dict(id=res['data']['id'], hash=h); save(); print('flow', f['id'], res['data']['id'])

# ---------------------------------------------------------------- campaigns (drafts with the planned send time; nothing is scheduled)
TZ = '+01:00' if ACCT == 'EU' else '-05:00'
CAMP_EMAIL = [('F1E6', 'popup_presale', '2026-11-23T09:00:00'), ('F1E7', 'popup_presale', '2026-11-27T08:00:00'), ('F10E3', None, '2026-12-05T09:00:00'), ('F13E2', 'giftcard', '2027-01-02T09:00:00')]
CAMP_SMS = {'S2C1': '2026-11-23T09:00:00', 'S2C2': '2026-11-27T08:00:00', 'S2C3': '2026-11-30T12:00:00', 'S2C4': '2026-12-06T18:00:00', 'S2C5': '2026-12-17T10:00:00', 'S2C6': '2026-12-22T10:00:00'}
def step_campaigns():
    C = K.setdefault('campaigns', {}); S = K['segments']; T = K['templates']
    for eid, seg, when in CAMP_EMAIL:
        if eid in C: continue
        f, e = next((f, e) for f, e in emails() if e['id'] == eid)
        body = {'data': {'type': 'campaign', 'attributes': {'name': f'Q4 · {eid} · {e["name"]}', 'audiences': {'included': [S[seg]] if seg else [K['lists']['salelive']], 'excluded': []},
                'send_strategy': {'method': 'static', 'datetime': when + TZ, 'options': {'is_local': True, 'send_past_recipients_immediately': False}},
                'campaign-messages': {'data': [{'type': 'campaign-message', 'attributes': {'definition': {'channel': 'email', 'label': eid,
                    'content': dict(zip(('subject', 'preview_text'), subj_prev(R(ACCT, f['id'], K['images']), e, phase_now(when[:10]))), from_email=K['map']['from_email'], from_label=K['map']['from_label'])}}}]}}}}
        try:
            res = call('campaigns/', body); cid = res['data']['id']
            mid = res['data']['relationships']['campaign-messages']['data'][0]['id']
            call('campaign-message-assign-template/', {'data': {'type': 'campaign-message', 'id': mid, 'relationships': {'template': {'data': {'type': 'template', 'id': T[eid]['id']}}}}})
            C[eid] = cid; save(); print('campaign', eid, cid)
        except Exception as ex: print('CAMPAIGN FAILED', eid, str(ex)[:500])
    r = R(ACCT, 'S2', K['images'])
    for e in Q.S2['emails']:
        if e['id'] in C: continue
        body = {'data': {'type': 'campaign', 'attributes': {'name': f'Q4 · {e["id"]} · SMS · {e["name"]}', 'audiences': {'included': [S['sms']], 'excluded': []},
                'send_strategy': {'method': 'static', 'datetime': CAMP_SMS[e['id']] + TZ, 'options': {'is_local': True, 'send_past_recipients_immediately': False}},
                'campaign-messages': {'data': [{'type': 'campaign-message', 'attributes': {'definition': {'channel': 'sms', 'content': {'body': sms_body(Q.S2, e, r)}}}}]}}}}
        try: C[e['id']] = call('campaigns/', body)['data']['id']; save(); print('sms campaign', e['id'], C[e['id']])
        except Exception as ex: print('SMS CAMPAIGN FAILED', e['id'], str(ex)[:500])

# ---------------------------------------------------------------- Gender backfill from order history (never overwrites a Gender)
def step_backfill():
    B = K.setdefault('backfill', {})
    if B.get('done'): print('backfill already done', B); return
    per = {}; f = urllib.parse.quote(f'equals(metric_id,"{M["ordered"]}")')
    for ev in pages(f'events/?filter={f}&page[size]=200&fields[event]=event_properties&include=profile&fields[profile]=id'):
        pid = ((ev.get('relationships') or {}).get('profile', {}).get('data') or {}).get('id')
        if not pid: continue
        cols = ev['attributes']['event_properties'].get('Collections') or []
        a = per.setdefault(pid, [False, False]); a[0] |= any(c in MEN_ORD for c in cols); a[1] |= any(c in WOMEN_ORD for c in cols)
    gset = set(p['id'] for p in pages(f'segments/{K["segments"]["gender_set"]}/profiles/?page[size]=100&fields[profile]=id'))
    todo = {pid: ('Both' if m and w else 'Men' if m else 'Women') for pid, (m, w) in per.items() if (m or w) and pid not in gset}
    print('customers with orders', len(per), 'already have Gender', len(gset & set(per)), 'to set', len(todo))
    for i, (pid, gv) in enumerate(todo.items()):
        call(f'profiles/{pid}/', {'data': {'type': 'profile', 'id': pid, 'attributes': {'properties': {'Gender': gv, 'Gender source': 'order backfill'}}}}, 'PATCH')
        if i % 250 == 0: print('backfill', i, '/', len(todo))
    B.update(done=True, updated=len(todo), split=dict(Counter(todo.values()))); save(); print('backfill', B)

def step_subjects(day=None):
    ph = phase_now(day); n = 0
    for f in Q.FLOWS:
        fl = K.get('flows', {}).get(f['id']) or {}
        if not fl.get('id'): continue
        r = R(ACCT, f['id'], K['images'])
        want = {f'{e["id"]} · {e["name"]}': subj_prev(r, e, ph) for e in f['emails'] if not e.get('kind') and e['id'] not in SKIP_IN_FLOW}
        for a in pages(f'flows/{fl["id"]}/flow-actions/'):
            time.sleep(0.3)
            d = call(f'flow-actions/{a["id"]}/')['data']['attributes'].get('definition') or {}
            if d.get('type') != 'send-email': continue
            msg = d['data']['message']; w = want.get(msg.get('name'))
            if not w or (msg.get('subject_line'), msg.get('preview_text')) == tuple(w): continue
            msg['subject_line'], msg['preview_text'] = w
            d.pop('temporary_id', None)
            call(f'flow-actions/{a["id"]}/', {'data': {'type': 'flow-action', 'id': a['id'], 'attributes': {'definition': d}}}, 'PATCH'); n += 1
    print('subjects switched to', ph, n, 'emails')

for s in STEPS: globals()['step_' + s]()
