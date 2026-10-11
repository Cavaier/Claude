import json, sys, time, urllib.request, csv
pair, out, start, step = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
rows = {}
while True:
    u = f"https://www.bitstamp.net/api/v2/ohlc/{pair}/?step={step}&limit=1000&start={start}"
    for k in range(4):
        try: d = json.load(urllib.request.urlopen(u, timeout=30))["data"]["ohlc"]; break
        except Exception: time.sleep(2 ** k)
    if not d: break
    for r in d: rows[int(r["timestamp"])] = r
    last = int(d[-1]["timestamp"])
    if last <= start or len(d) < 2: break
    start = last + step; time.sleep(0.25)
with open(out, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["ts","open","high","low","close"])
    for t in sorted(rows): r = rows[t]; w.writerow([t, r["open"], r["high"], r["low"], r["close"]])
print(pair, step, len(rows), time.strftime("%Y-%m-%d", time.gmtime(min(rows))), "->", time.strftime("%Y-%m-%d", time.gmtime(max(rows))))
