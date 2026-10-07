"""Render every Q4 template through Klaviyo with sample event data: python3 rendertest.py EU|US"""
import sys, os, json, re, time, urllib.request
A = sys.argv[1]
st = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sync_state.json')))['klaviyo'][A]
def call(path, body):
    req = urllib.request.Request('https://a.klaviyo.com/api/' + path, data=json.dumps(body).encode(), method='POST',
        headers={'Authorization': 'Klaviyo-API-Key ' + os.environ['KLAVIYO_KEY_' + A], 'revision': '2026-01-15', 'accept': 'application/vnd.api+json', 'content-type': 'application/vnd.api+json'})
    for i in range(6):
        try: return json.load(urllib.request.urlopen(req, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(2 ** i); continue
            raise Exception(e.read().decode()[:300])
LI = [{'title': 'Braid Bracelet', 'variant_title': 'Black / Medium', 'quantity': 1, 'line_price': '39.90', 'product': {'images': [{'src': 'https://cavaier.com/x.png'}]}}]
EV = {'F2': {'Name': '3x Minimal Stack Set', 'ImageURL': 'https://cavaier.com/x.png', 'URL': 'https://cavaier.com/p', 'Price': '94.90'},
      'F4': {'Product Name': 'Crystal Necklace', 'ImageURL': 'https://cavaier.com/x.png', 'Variant Name': 'Black / 55 cm', 'URL': 'https://cavaier.com/p', 'Price': 89.9, '$currency': 'EUR'},
      'F5': {'extra': {'checkout_url': 'https://cavaier.com/c', 'line_items': LI, 'presentment_currency': 'EUR'}, 'Total Discounts': '10.00', '$value': '29.90'},
      'F9': {'ProductName': 'Cuban Necklace', 'ImageURL': 'https://cavaier.com/x.png', 'URL': 'https://cavaier.com/p'}}
bad = 0
for eid, t in st['templates'].items():
    fl = re.match(r'(F\d+)', eid).group(1)
    for g in ('Men', 'Women'):
        ctx = {'person': {'Gender': g}, 'event': EV.get(fl, {})}
        try:
            h = call('template-render/', {'data': {'type': 'template', 'attributes': {'id': t['id'], 'context': ctx}}})['data']['attributes']['html']
            if '{%' in h or '{{' in h: print(eid, g, 'UNRENDERED TAG'); bad += 1
        except Exception as e: print(eid, g, 'FAIL', str(e)[:160]); bad += 1
print(A, len(st['templates']), 'templates x 2 genders,', bad, 'problems')
