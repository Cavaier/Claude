"""List (and with --delete remove) Q4 objects in Klaviyo that the current plan no longer uses. python3 sweep.py EU|US [--delete]"""
import sys, os, json, time, urllib.request, urllib.parse
A = sys.argv[1]; DEL = '--delete' in sys.argv
STP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sync_state.json'); st = json.load(open(STP)); K = st['klaviyo'][A]
def call(path, method=None):
    for i in range(8):
        try:
            req = urllib.request.Request('https://a.klaviyo.com/api/' + path, method=method, headers={'Authorization': 'Klaviyo-API-Key ' + os.environ['KLAVIYO_KEY_' + A], 'revision': '2026-01-15', 'accept': 'application/vnd.api+json'})
            b = urllib.request.urlopen(req, timeout=60).read(); return json.loads(b) if b else None
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(2 * (i + 1)); continue
            raise Exception(f'{e.code} {e.read().decode()[:200]}')
def pages(path):
    while path:
        d = call(path); yield from d['data']; n = d['links'].get('next'); path = n.split('/api/')[1] if n else None
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); import q4_specs as Q
live_eids = {e['id'] for f in Q.FLOWS for e in f['emails'] if not e.get('kind')}
keep = {
 'flows': {v['id'] for v in K.get('flows', {}).values() if v.get('id')},
 'campaigns': set(K.get('campaigns', {}).values()),
 'templates': {v['id'] for k, v in K.get('templates', {}).items() if k in live_eids},
 'lists': set(K.get('lists', {}).values()),
 'segments': set(K.get('segments', {}).values()),
 'forms': set(str(v).replace('v1:', '') for v in K.get('forms', {}).values()),
}
found = {}
found['flows'] = [(x['id'], x['attributes']['name']) for x in pages('flows/?page[size]=50') if x['attributes']['name'].startswith('Q4')]
for ch in ('email', 'sms'):
    found.setdefault('campaigns', []).extend((x['id'], x['attributes']['name']) for x in pages('campaigns/?filter=' + urllib.parse.quote(f"equals(messages.channel,'{ch}')")) if x['attributes']['name'].startswith('Q4'))
found['templates'] = [(x['id'], x['attributes']['name']) for x in pages('templates/?page[size]=10&fields[template]=name&filter=' + urllib.parse.quote('contains(name,"Q4")')) if x['attributes']['name'].startswith('Q4')]
found['lists'] = [(x['id'], x['attributes']['name']) for x in pages('lists/?fields[list]=name') if x['attributes']['name'].startswith('Q4')]
found['segments'] = [(x['id'], x['attributes']['name']) for x in pages('segments/?fields[segment]=name') if x['attributes']['name'].startswith('Q4')]
found['forms'] = [(x['id'], x['attributes']['name']) for x in pages('forms/?fields[form]=name') if x['attributes']['name'].startswith('Q4')]
for kind, items in found.items():
    orphan = [(i, n) for i, n in items if i not in keep[kind] and 'TEST (datetest' not in n]
    print(f'{A} {kind}: {len(items)} Q4 items, {len(items) - len(orphan)} in the plan, {len(orphan)} not in the plan')
    for i, n in orphan:
        print('   ', i, n)
        if DEL:
            try: call(f'{kind}/{i}/', 'DELETE'); print('      deleted')
            except Exception as ex: print('      delete failed', str(ex)[:150])
    missing = keep[kind] - {i for i, _ in items}
    if missing: print('    in the plan but not found:', missing)
if DEL:
    for k in [k for k in K.get('templates', {}) if k not in live_eids]: del K['templates'][k]
    json.dump(st, open(STP, 'w'), indent=1)
