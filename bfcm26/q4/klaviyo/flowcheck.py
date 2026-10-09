"""Read every Q4 flow back from Klaviyo and compare it with what push.py would build now: trigger, profile filter, and each step in
order (waits, template, subject, preview, smart sending, SMS text, splits, profile updates). Also checks that every flow is a draft and
that recent real events carry the fields the emails read. python3 flowcheck.py EU|US"""
import sys, os, json, re
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'push.py')).read()
exec(compile(src[:src.index('\nfor CUR in list(STEPS)')], 'push.py', 'exec'))

def walk(d):
    acts = {a['id'] if 'id' in a else a['temporary_id']: a for a in d['actions']}
    out, seen, todo = [], set(), [d['entry_action_id']]
    while todo:
        k = todo.pop(0)
        if k is None or k in seen or k not in acts: continue
        seen.add(k); a = acts[k]; out.append(a)
        links = a.get('links') or {}
        for key in ('next', 'next_if_true', 'next_if_false'):
            if links.get(key): todo.append(links[key])
        for b in (a.get('data') or {}).get('branches') or []:
            if (b.get('links') or {}).get('next'): todo.append(b['links']['next'])
    return out

_H = {}
def HTML(t):
    if t not in _H: _H[t] = call(f'templates/{t}/')['data']['attributes'].get('html') or ''
    return _H[t]
def sub(exp, act, path=''):  # every value in exp must be in act (ids and links ignored)
    errs = []
    if isinstance(exp, dict):
        if not isinstance(act, dict): return [f'{path}: expected object, got {str(act)[:60]}']
        for k, v in exp.items():
            if k in ('temporary_id', 'links', 'id', 'branch_id') or v is None: continue
            if k not in act: errs.append(f'{path}.{k}: missing'); continue
            errs += sub(v, act[k], f'{path}.{k}')
    elif isinstance(exp, list):
        if not isinstance(act, list) or len(exp) != len(act): return [f'{path}: list {len(exp)} vs {len(act) if isinstance(act, list) else act}']
        for i, (a, b) in enumerate(zip(exp, act)): errs += sub(a, b, f'{path}[{i}]')
    elif path.endswith('.template_id') and exp != act:  # Klaviyo keeps its own copy of the template in each flow email
        if HTML(exp) != HTML(act): errs.append(f'{path}: flow copy {act} differs from template {exp}')
    elif exp != act and not (isinstance(exp, str) and isinstance(act, str) and exp.strip() == act.strip()):
        errs.append(f'{path}: {str(exp)[:90]!r} != {str(act)[:90]!r}')
    return errs

plan = [(f['id'], build_flow(f)) for f in Q.FLOWS + [Q.S1] if not f.get('campaign')] + [('G1', build_gender('G1')), ('G2', build_gender('G2'))]
plan += [(eid, build_dated(eid)[2]) for eid in DATED]
bad = 0
for key, exp in plan:
    fid = K['flows'].get(key, {}).get('id')
    if not fid: print(key, 'NOT IN KLAVIYO'); bad += 1; continue
    got = call(f'flows/{fid}/?additional-fields[flow]=definition')['data']
    st, d = got['attributes']['status'], got['attributes']['definition']
    errs = [] if st == 'draft' else [f'status {st}']
    errs += sub(exp['triggers'], d['triggers'], 'trigger') + sub(exp.get('profile_filter'), d.get('profile_filter'), 'filter')
    ea, ga = walk(exp), walk(d)
    if [a['type'] for a in ea] != [a['type'] for a in ga]: errs.append(f'steps {[a["type"] for a in ea]} vs {[a["type"] for a in ga]}')
    else:
        for i, (a, b) in enumerate(zip(ea, ga)): errs += sub(a['data'], b['data'], f'step{i + 1}.{a["type"]}')
    n_mail = sum(a['type'] == 'send-email' for a in ga); n_sms = sum(a['type'] == 'send-sms' for a in ga)
    print(key, 'OK' if not errs else 'DIFF', f'({len(ga)} steps, {n_mail} emails, {n_sms} texts)'); bad += len(errs)
    for e in errs[:8]: print('   ', e)

# real events: do the fields the emails use exist on recent events?
NEED = {'viewed': ['Name', 'URL', 'ImageURL', 'Price'], 'cart': ['Product Name', 'ImageURL', 'Price', '$currency'],
        'checkout': ['$extra'], 'ordered': ['Name']}
for mk, fields in NEED.items():
    import urllib.parse
    f_ = urllib.parse.quote(f'equals(metric_id,"{M[mk]}")')
    evs = call(f'events/?filter={f_}&page[size]=5&sort=-datetime&fields[event]=event_properties,datetime')['data']
    if not evs: print('event', mk, 'NO RECENT EVENTS'); bad += 1; continue
    p = evs[0]['attributes']['event_properties']; miss = [x for x in fields if x not in p]
    if mk == 'checkout': miss += [x for x in ('checkout_url', 'line_items') if x not in (p.get('$extra') or {})]
    print('event', mk, evs[0]['attributes']['datetime'][:10], 'fields OK' if not miss else f'MISSING {miss}'); bad += len(miss)
print(ACCT, 'problems:', bad)
