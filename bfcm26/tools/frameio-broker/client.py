# Helper side: get a Frame.io access token from the broker (no Adobe sign-in needed).
# usage in code: from client import token; T = token()   (reads FRAMEIO_OAUTH_CLIENT_SECRET from env)
import os, hmac, hashlib, json, time, urllib.request
BROKER = os.environ.get('FRAMEIO_BROKER_URL', 'https://frameio-broker.eli-054.workers.dev')
def _auth():
    key = os.environ['FRAMEIO_OAUTH_CLIENT_SECRET'].strip().encode()
    return hmac.new(key, str(int(time.time() // 60)).encode(), hashlib.sha256).hexdigest()
def _req(path, method='GET'):
    r = urllib.request.Request(BROKER + path, method=method, data=b'' if method == 'POST' else None,
                               headers={'X-Broker-Auth': _auth(), 'User-Agent': 'cavaier-uploader/1.0'})
    return json.load(urllib.request.urlopen(r))
def token(): return _req('/token', 'POST')['access_token']
def status(): return _req('/status')
if __name__ == '__main__':
    print(json.dumps(status(), indent=1))   # never prints a token
