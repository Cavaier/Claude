import sys, pandas as pd, numpy as np

def load(p):
    d = pd.read_csv(p); d["date"] = pd.to_datetime(d.ts, unit="s"); d = d.set_index("date")[["open","high","low","close"]].astype(float)
    return d[(d > 0).all(axis=1)]

def backtest(d, entry_len=55, exit_len=20, trend_len=200, atr_len=20, atr_mult=3.0, risk_pct=1.0,
             full_size=False, fee=0.001, slip=0.0005, start="2013-01-01", end=None, cap=10000.0):
    d = d.copy()
    d["upper"] = d.high.rolling(entry_len).max().shift(1)
    d["lower"] = d.low.rolling(exit_len).min().shift(1)
    d["ema"] = d.close.ewm(span=trend_len, adjust=False).mean()
    tr = pd.concat([d.high - d.low, (d.high - d.close.shift()).abs(), (d.low - d.close.shift()).abs()], axis=1).max(axis=1)
    d["atr"] = tr.ewm(alpha=1/atr_len, adjust=False).mean()
    d = d.loc[start:end]
    cash, qty, stop, pending = cap, 0.0, np.nan, None
    eq, trades, entry_px, entry_cost = [], [], 0, 0
    o, h, l, c = d.open.values, d.high.values, d.low.values, d.close.values
    up, lo, ema, atr = d.upper.values, d.lower.values, d.ema.values, d.atr.values
    for i in range(len(d)):
        if pending is not None:                       # fill entry at this bar's open
            px = o[i] * (1 + slip); q = pending
            cost = q * px * (1 + fee)
            if cost > cash: q = cash / (px * (1 + fee)); cost = cash
            cash -= cost; qty, entry_px, entry_cost = q, px, cost; pending = None
        if qty > 0:
            if l[i] <= stop:                          # stop hit (gap -> fill at open)
                px = min(o[i], stop) * (1 - slip)
                proceeds = qty * px * (1 - fee); cash += proceeds
                trades.append(proceeds / entry_cost - 1); qty = 0; stop = np.nan
        equity = cash + qty * c[i]
        if qty == 0 and pending is None and not np.isnan(up[i]) and c[i] > up[i] and c[i] > ema[i]:
            dist = atr_mult * atr[i]
            q = equity * 0.99 / c[i] if full_size else min(equity * risk_pct / 100 / dist, equity * 0.99 / c[i])
            pending, stop = q, c[i] - dist
        if qty > 0: stop = max(stop, lo[i])
        eq.append(equity)
    eq = pd.Series(eq, index=d.index)
    yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    t = np.array(trades)
    bh = d.close / d.close.iloc[0] * cap
    def dd(s): return (s / s.cummax() - 1).min()
    return dict(ret=eq.iloc[-1]/cap - 1, cagr=(eq.iloc[-1]/cap)**(1/yrs) - 1, maxdd=dd(eq), trades=len(t),
                win=(t > 0).mean() if len(t) else np.nan,
                pf=t[t > 0].sum() / -t[t < 0].sum() if (t < 0).any() else np.inf,
                bh_ret=bh.iloc[-1]/cap - 1, bh_cagr=(bh.iloc[-1]/cap)**(1/yrs) - 1, bh_dd=dd(bh),
                exposure=None)

def fmt(name, r):
    print(f"{name:34s} ret {r['ret']*100:9.0f}%  CAGR {r['cagr']*100:6.1f}%  maxDD {r['maxdd']*100:6.1f}%  "
          f"trades {r['trades']:3d}  win {r['win']*100:4.0f}%  PF {r['pf']:4.1f}  | B&H CAGR {r['bh_cagr']*100:6.1f}%  B&H DD {r['bh_dd']*100:6.1f}%")

if __name__ == "__main__":
    btc, eth = load(sys.argv[1]), load(sys.argv[2])
    print("=== Strategy exactly as written (1% risk per trade) ===")
    fmt("BTC 2013-2026", backtest(btc))
    fmt("ETH 2018-2026", backtest(eth, start="2018-03-01"))
    print("\n=== Same signals, fully invested when in a trade ===")
    fmt("BTC 2013-2026", backtest(btc, full_size=True))
    fmt("ETH 2018-2026", backtest(eth, start="2018-03-01", full_size=True))
    print("\n=== BTC, fully invested, split into separate periods ===")
    for s, e in [("2013-01-01","2017-12-31"),("2018-01-01","2021-12-31"),("2022-01-01","2026-10-11")]:
        fmt(f"BTC {s[:4]}-{e[:4]}", backtest(btc, full_size=True, start=s, end=e))
    print("\n=== Robustness: BTC fully invested, different settings (CAGR / maxDD) ===")
    for el in [20, 40, 55, 80, 100]:
        row = []
        for xl in [10, 20, 40]:
            r = backtest(btc, entry_len=el, exit_len=xl, full_size=True); row.append(f"{r['cagr']*100:5.1f}%/{r['maxdd']*100:4.0f}%")
        print(f"entry {el:3d}: " + "   ".join(f"exit {x}: {v}" for x, v in zip([10,20,40], row)))
