# Tests three common short-term (hours) BTC strategies at several fee levels.
# Usage: python3 fetch_bitstamp_any.py btcusd btc_1h.csv 1577836800 3600 && python3 short_term_test.py btc_1h.csv
import sys, numpy as np, pandas as pd
d = pd.read_csv(sys.argv[1]); d.index = pd.to_datetime(d.ts, unit="s"); d = d[["open","high","low","close"]].astype(float)
d = d[(d > 0).all(axis=1)]
c = d.close
delta = c.diff(); up = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean(); dn = (-delta.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
d["rsi"] = 100 - 100 / (1 + up / dn)
d["hi24"] = d.high.rolling(24).max().shift(1)
d["mid"] = c.rolling(20).mean(); d["lowband"] = d.mid - 2 * c.rolling(20).std()

def run(entry, tp=None, sl=None, max_h=24, exit_fn=None):
    """Long-only: signal on bar close, enter next open; exit on take-profit/stop intrabar, exit_fn on close, or time limit."""
    o, h, l, cl = d.open.values, d.high.values, d.low.values, d.close.values
    sig = entry.values; ex = exit_fn.values if exit_fn is not None else np.zeros(len(d), bool)
    gross, holds, i, n = [], [], 0, len(d)
    while i < n - 2:
        if not sig[i]: i += 1; continue
        j = i + 1; px = o[j]; out = None
        for k in range(j, min(j + max_h, n)):
            if sl and l[k] <= px * (1 - sl): out = min(o[k], px * (1 - sl)); break
            if tp and h[k] >= px * (1 + tp): out = max(o[k], px * (1 + tp)); break
            if ex[k] or k == j + max_h - 1: out = cl[k]; break
        if out is None: break
        gross.append(out / px - 1); holds.append(k - j + 1); i = k + 1
    return np.array(gross), np.array(holds)

years = (d.index[-1] - d.index[0]).days / 365.25
strats = {
    "A. Buy RSI dips (RSI<25, sell RSI>55)": dict(entry=d.rsi < 25, sl=0.03, max_h=24, exit_fn=d.rsi > 55),
    "B. Breakout scalp (+1.5% / -1%)":       dict(entry=c > d.hi24, tp=0.015, sl=0.01, max_h=12),
    "C. Bollinger bounce (to middle band)":  dict(entry=c < d.lowband, sl=0.02, max_h=12, exit_fn=c > d.mid),
}
fees = [0.0, 0.0005, 0.001, 0.004, 0.01]
print(f"BTC hourly {d.index[0].date()} -> {d.index[-1].date()} ({years:.1f} yrs). Just holding: {((c.iloc[-1]/c.iloc[0])**(1/years)-1)*100:.0f}%/yr\n")
for name, kw in strats.items():
    g, hd = run(**kw)
    print(f"{name}\n  {len(g)/years:.0f} trades/yr, avg hold {hd.mean():.1f}h, win rate before fees {(g>0).mean()*100:.0f}%, avg trade before fees {g.mean()*100:+.3f}%")
    line = []
    for f in fees:
        net = (1 + g) * (1 - f) / (1 + f) * (1 - 0.0002) / (1 + 0.0002) - 1
        cagr = np.prod(1 + net) ** (1 / years) - 1
        line.append(f"fee {f*100:.2f}%: {cagr*100:+6.1f}%/yr (win {(net>0).mean()*100:.0f}%)")
    print("  " + " | ".join(line) + "\n")
