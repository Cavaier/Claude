import json, sys, time, urllib.request, csv
pair, out = sys.argv[1], sys.argv[2]
start, rows = int(sys.argv[3]) if len(sys.argv) > 3 else 1300000000, {}
while True:
    u = f"https://www.bitstamp.net/api/v2/ohlc/{pair}/?step=86400&limit=1000&start={start}"
    d = json.load(urllib.request.urlopen(u, timeout=30))["data"]["ohlc"]
    if not d: break
    for r in d: rows[int(r["timestamp"])] = r
    last = int(d[-1]["timestamp"])
    if last <= start or len(d) < 2: break
    start = last + 86400
    time.sleep(0.3)
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ts","open","high","low","close"])
    for t in sorted(rows): r = rows[t]; w.writerow([t, r["open"], r["high"], r["low"], r["close"]])
print(pair, len(rows), time.strftime("%Y-%m-%d", time.gmtime(min(rows))), "->", time.strftime("%Y-%m-%d", time.gmtime(max(rows))))
