# Read-only Google Ads REST helper. Token kept in memory only.
import os, sys, json, urllib.request, urllib.parse
CID = "8420446950"; LOGIN = "9574419833"
def token():
    data = urllib.parse.urlencode({"client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
        "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data))["access_token"]
def search(tok, q, ver):
    req = urllib.request.Request(f"https://googleads.googleapis.com/{ver}/customers/{CID}/googleAds:search",
        data=json.dumps({"query": q}).encode(), method="POST",
        headers={"Authorization": "Bearer " + tok, "login-customer-id": LOGIN, "Content-Type": "application/json"})
    try:
        return 200, json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()[:3000]
if __name__ == "__main__":
    # usage: gads.py VERSION < queries.json  (list of {name, query}); only SELECT queries allowed
    ver = sys.argv[1]; qs = json.load(sys.stdin); tok = token(); out = {}
    for item in qs:
        assert item["query"].strip().upper().startswith("SELECT")
        code, res = search(tok, item["query"], ver)
        out[item["name"]] = {"status": code, "result": res}
        print(item["name"], code, file=sys.stderr)
    print(json.dumps(out, indent=1))
