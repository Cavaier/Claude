# Deploy the Frame.io token broker to Cloudflare Workers via the API (no wrangler needed).
# Reads CLOUDFLARE_API_TOKEN, FRAMEIO_OAUTH_CLIENT_ID and FRAMEIO_OAUTH_CLIENT_SECRET from env. Never prints secrets.
import os, json, sys, urllib.request, urllib.error, uuid
NAME = 'frameio-broker'
HERE = os.path.dirname(os.path.abspath(__file__))
API = 'https://api.cloudflare.com/client/v4'
H = {'Authorization': 'Bearer ' + os.environ['CLOUDFLARE_API_TOKEN']}

def call(method, path, body=None, ctype='application/json', raw=False):
    data = body if raw else (json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(API + path, data=data, method=method, headers={**H, 'Content-Type': ctype})
    try:
        d = json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        d = json.loads(e.read().decode() or '{}')
    if not d.get('success'):
        sys.exit(f'{method} {path} failed: {d.get("errors")}')
    return d['result']

acct = call('GET', '/accounts')[0]['id']
ns = next((n for n in call('GET', f'/accounts/{acct}/storage/kv/namespaces?per_page=100') if n['title'] == NAME), None)
if not ns:
    ns = call('POST', f'/accounts/{acct}/storage/kv/namespaces', {'title': NAME})
meta = {
    'main_module': 'worker.js',
    'compatibility_date': '2025-09-01',
    'bindings': [
        {'type': 'kv_namespace', 'name': 'KV', 'namespace_id': ns['id']},
        {'type': 'secret_text', 'name': 'ADOBE_CLIENT_ID', 'text': os.environ['FRAMEIO_OAUTH_CLIENT_ID'].strip()},
        {'type': 'secret_text', 'name': 'ADOBE_CLIENT_SECRET', 'text': os.environ['FRAMEIO_OAUTH_CLIENT_SECRET'].strip()},
    ],
}
b = uuid.uuid4().hex
code = open(os.path.join(HERE, 'worker.js'), 'rb').read()
parts = [
    f'--{b}\r\nContent-Disposition: form-data; name="metadata"; filename="metadata.json"\r\nContent-Type: application/json\r\n\r\n'.encode() + json.dumps(meta).encode() + b'\r\n',
    f'--{b}\r\nContent-Disposition: form-data; name="worker.js"; filename="worker.js"\r\nContent-Type: application/javascript+module\r\n\r\n'.encode() + code + b'\r\n',
    f'--{b}--\r\n'.encode(),
]
call('PUT', f'/accounts/{acct}/workers/scripts/{NAME}', b''.join(parts), ctype=f'multipart/form-data; boundary={b}', raw=True)
call('PUT', f'/accounts/{acct}/workers/scripts/{NAME}/schedules', [{'cron': '17 4 * * *'}])
call('POST', f'/accounts/{acct}/workers/scripts/{NAME}/subdomain', {'enabled': True})
sub = call('GET', f'/accounts/{acct}/workers/subdomain')['subdomain']
print(f'deployed: https://{NAME}.{sub}.workers.dev  (kv {ns["id"][:6]}…, cron daily 04:17 UTC)')
