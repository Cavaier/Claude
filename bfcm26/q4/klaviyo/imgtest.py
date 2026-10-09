"""IMAGE CHECK. Render every Q4 template through Klaviyo as it would look on a given day (one day per period + key days), women and men,
and check that every line of copy the local preview shows for that day is in Klaviyo's output. python3 datetest.py EU|US [YYYY-MM-DD ...]"""
import sys, os, re, json, time, html as H, urllib.request
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import q4_specs as Q
from emailer import R
A = sys.argv[1]
DATES = sys.argv[2:] or ['2026-11-01', '2026-11-11', '2026-11-18', '2026-11-26', '2026-11-27', '2026-12-01', '2026-12-09', '2026-12-15', '2026-12-30']
ST = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sync_state.json')))['klaviyo'][A]
def call(path, body=None, method=None):
    for i in range(8):
        try:
            req = urllib.request.Request('https://a.klaviyo.com/api/' + path, data=json.dumps(body).encode() if body else None, method=method,
                headers={'Authorization': 'Klaviyo-API-Key ' + os.environ['KLAVIYO_KEY_' + A], 'revision': '2026-01-15', 'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json'})
            r = urllib.request.urlopen(req, timeout=60); b = r.read(); return json.loads(b) if b else None
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(2 * (i + 1)); continue
            raise Exception(f'{e.code} {e.read().decode()[:300]}')
        except Exception:
            time.sleep(2 * (i + 1))
    raise Exception('gave up ' + path)
LI = [{'title': 'Braid Bracelet', 'variant_title': 'Black / Medium', 'quantity': 1, 'line_price': '39.90', 'product': {'images': [{'src': 'https://cavaier.com/x.png'}]}}]
EV = {'F2': {'Name': '3x Minimal Set', 'ImageURL': 'https://cavaier.com/x.png', 'URL': 'https://cavaier.com/p', 'Price': '94.90'},
      'F4': {'Product Name': 'Crystal Necklace', 'ImageURL': 'https://cavaier.com/x.png', 'Variant Name': 'Black / 55 cm', 'URL': 'https://cavaier.com/p', 'Price': 89.9, '$currency': 'EUR'},
      'F5': {'extra': {'checkout_url': 'https://cavaier.com/c', 'line_items': LI, 'presentment_currency': 'EUR'}, 'Total Discounts': '10.00', '$value': '29.90'},
      'F9': {'Name': '3x Minimal Set', 'ImageURL': 'https://cavaier.com/x.png', 'URL': 'https://cavaier.com/p', 'Price': '94.90'}}
def day_row(d):
    for x in Q.DAYS:
        if x['id'] == d: return x
    from emailer import DAYRANGE, PR
    for k, (a, b) in DAYRANGE.items():
        if a <= d < b: return next(x for x in Q.DAYS if x['id'] == k)
    ph = next(p for p, (a, b) in PR.items() if (a is None or a <= d) and (b is None or d < b))
    return next((x for x in Q.DAYS if x['phase'] == ph and x['id'] == ph), None) or {'phase': ph}
def phase_of(d):
    from emailer import PR
    return next(p for p, (a, b) in PR.items() if (a is None or a <= d) and (b is None or d < b))
SAMPLE = {'3x Minimal Set', 'Black / Medium', '€94.90', '$94.90', 'Crystal Necklace', 'Cuban Necklace', 'Black / 55 cm'}  # the preview's sample product; Klaviyo shows the event's product
def visible(h):
    h = re.sub(r'<div style="display:none[^>]*>.*?</div>', ' ', h, flags=re.S)
    h = re.sub(r'<(style|head|title)[^>]*>.*?</\1>', ' ', h, flags=re.S | re.I)
    t = H.unescape(re.sub(r'<[^>]+>', '\n', h))
    return [re.sub(r'\s+', ' ', x).strip() for x in t.split('\n') if x.strip()]
class Img(dict):
    def __missing__(s, k): return ST['images'].get(k, 'https://x/' + k)
tmp = call('templates/', {'data': {'type': 'template', 'attributes': {'name': 'Q4 · TEST (datetest, deleted after)', 'editor_type': 'CODE', 'html': '<html><body><p>test</p></body></html>'}}})['data']['id']
bad = 0; n = 0; seen = {}
try:
    for f in Q.FLOWS:
        for e in f['emails']:
            if e.get('kind') or e['id'] not in ST['templates']: continue
            src = R(A, f['id'], Img()).email(e)
            for d in DATES:
                ph = phase_of(d)
                if ph not in e['phases']: continue
                hd = src.replace("{% today '%Y-%m-%d' as d %}", "{% with d='" + d + "' %}", 1).replace('</body>', '{% endwith %}</body>', 1)
                call(f'templates/{tmp}/', {'data': {'type': 'template', 'id': tmp, 'attributes': {'html': hd}}}, 'PATCH')
                for g, gk in (('Women', 'W'), ('Men', 'M')):
                    out = call('template-render/', {'data': {'type': 'template', 'attributes': {'id': tmp, 'context': {'person': {'Gender': g}, 'event': EV.get(f['id'], {})}}}})['data']['attributes']['html']
                    n += 1
                    srcs = lambda h: [x for x in re.findall(r'<img[^>]+src="([^"]+)"', h) if '{{' not in x and 'x.png' not in x and x != 'None']
                    local = srcs(R(A, f['id'], Img(), ctx=dict(phase=ph, day=day_row(d), g=gk)).email(e))
                    got = srcs(out)
                    if local != got:
                        bad += 1; print(e['id'], d, g, 'IMAGES DIFFER', len(local), len(got), [x[-40:] for x in local if x not in got][:2], [x[-40:] for x in got if x not in local][:2])
                    seen.setdefault((e['id'], d), {})[g] = got
    same = sum(1 for v in seen.values() if len(v) == 2 and v['Women'] == v['Men'])
    print(A, n, 'renders,', bad, 'image problems;', len(seen) - same, 'of', len(seen), 'email/date pairs show different images for women and men')
finally:
    call(f'templates/{tmp}/', method='DELETE')
