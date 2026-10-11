# Manual version: signals on the daily close, you act at the next open.
# Compares fee levels against just holding. Usage: python3 manual_exits.py <data folder>
import sys; sys.path.insert(0, ".")
import backtest as bt, numpy as np, pandas as pd
D = sys.argv[1].rstrip("/") + "/" if len(sys.argv) > 1 else "data/"  # btc.csv / eth.csv from fetch_bitstamp.py
def manual(d, fee, start, delay=1, slip=0.0005):
    d = d.copy()
    d["upper"] = d.high.rolling(55).max().shift(1); d["lower"] = d.low.rolling(20).min().shift(1)
    d["ema"] = d.close.ewm(span=200, adjust=False).mean()
    tr = pd.concat([d.high - d.low, (d.high - d.close.shift()).abs(), (d.low - d.close.shift()).abs()], axis=1).max(axis=1)
    d["atr"] = tr.ewm(alpha=1/20, adjust=False).mean(); d = d.loc[start:]
    o, c, up, lo, ema, atr = d.open.values, d.close.values, d.upper.values, d.lower.values, d.ema.values, d.atr.values
    cash, qty, stop, act, what, eq = 10000.0, 0.0, np.nan, None, None, []
    for i in range(len(d)):
        if act == i:
            if what == "buy": qty = cash / (o[i] * (1 + slip) * (1 + fee)); cash = 0
            else: cash = qty * o[i] * (1 - slip) * (1 - fee); qty = 0
            act = None
        if act is None:
            if qty == 0 and c[i] > up[i] and c[i] > ema[i]: stop = c[i] - 3 * atr[i]; act, what = i + delay, "buy"
            elif qty > 0:
                if c[i] < stop: act, what = i + delay, "sell"
                else: stop = max(stop, lo[i])
        eq.append(cash + qty * c[i])
    eq = pd.Series(eq, index=d.index); yrs = (eq.index[-1] - eq.index[0]).days / 365.25
    return (eq.iloc[-1] / 10000) ** (1 / yrs) - 1
for name, f, s in [("BTC", "btc.csv", "2018-01-01"), ("BTC", "btc.csv", "2022-01-01"), ("ETH", "eth.csv", "2018-03-01"), ("ETH", "eth.csv", "2022-01-01")]:
    d = bt.load(D + f); bh = (d.loc[s:].close.iloc[-1] / d.loc[s:].close.iloc[0]) ** (365.25 / (d.loc[s:].index[-1] - d.loc[s:].index[0]).days) - 1
    print(f"{name} from {s[:4]}: " + "  ".join(f"fee {fee*100:.1f}%: {manual(d, fee, s)*100:5.1f}%/yr" for fee in [0.001, 0.005, 0.01, 0.02]) + f"  | just holding {bh*100:5.1f}%/yr")
