"""Per-shot grade for flat camera footage: base normalise, white-patch match, then a shared look.

Usage: python3 grade.py <clip> <time> <look>   -> prints the ffmpeg filter string for that shot.
The white patch is the bright, least-coloured pixels (studio wall, boucle, white top; nails and skin excluded); its mean is matched to
the look's white target, so every cut in an ad lands on the same white balance and exposure.
"""
import subprocess, sys, io, os
import numpy as np
from PIL import Image

BASE = "colorlevels=rimin=0.06:gimin=0.06:bimin=0.06:rimax=0.80:gimax=0.80:bimax=0.80"
LOOKS = {
    # white target (RGB 0-255), S-curve, saturation, skin tweak: sun-kissed / tanned skin (Eli), whites stay neutral
    'gold':  dict(white=(234, 229, 220), curve="0/0 0.25/0.22 0.5/0.53 0.75/0.81 1/1", sat=1.10,
                  sel="reds='-0.14 0.04 0.20 0.22':yellows='-0.08 0.03 0.14 0.14'"),
    'black': dict(white=(232, 231, 228), curve="0/0 0.25/0.22 0.5/0.53 0.75/0.81 1/1", sat=1.22,
                  sel="reds='-0.16 0.04 0.24 0.24':yellows='-0.10 0.03 0.16 0.16'"),
    'edit':  dict(white=(222, 222, 221), curve="0/0 0.22/0.16 0.5/0.51 0.78/0.84 1/0.99", sat=1.12,
                  sel="reds='-0.15 0.04 0.22 0.24':yellows='-0.09 0.03 0.15 0.16'"),
}

def frame(clip, t, vf):
    raw = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-ss', str(t), '-i', clip, '-frames:v', '1',
                          '-vf', vf + ',scale=540:960', '-f', 'image2pipe', '-vcodec', 'png', '-'],
                         capture_output=True, check=True).stdout
    return np.asarray(Image.open(io.BytesIO(raw)).convert('RGB')).astype(float)

def shot_filter(clip, t, look):
    L = LOOKS[look]
    pre = f"{BASE},curves=all='{L['curve']}'"
    a = frame(clip, t, pre)
    luma = a @ [0.2126, 0.7152, 0.0722]
    chroma = a.max(axis=2) - a.min(axis=2)
    bright = luma >= np.percentile(luma, 75)
    # neutral candidates: bright AND the least coloured half of those (wall, boucle, white top; not nails or skin)
    neutral = bright & (chroma <= np.percentile(chroma[bright], 40))
    white = a[neutral].mean(axis=0)
    gains = np.clip(np.array(L['white']) / white, 0.7, 1.5)
    mix = f"colorchannelmixer=rr={gains[0]:.4f}:gg={gains[1]:.4f}:bb={gains[2]:.4f}"
    # Skin rule (Eli): sun-kissed / tanned, never pale. Measure the graded skin and add warmth + depth per shot
    # until it reaches the same tan target, so bright, washed-out clips land on the same skin as the rest.
    if os.environ.get('GRADE_ADAPT', '1') == '0':   # fixed tan only (the look Eli preferred on W422 C2)
        return f"{pre},{mix},eq=saturation={L['sat']},selectivecolor={L['sel']},unsharp=5:5:0.35"
    best = None
    for k in (0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6):
        sel = _boost(L['sel'], min(k, 2))
        # beyond the selective boost: more saturation and a touch of depth on red/yellow hues only (skin).
        # Neutral tones (charcoal dress, white walls, bouclé) carry no hue, so they stay neutral.
        w = max(0, k - 1)
        w2 = min(w, 2)   # a capped midtone warm balance, with the opposite shift in the shadows (dress stays neutral)
        bal = (f"huesaturation=saturation={0.09*w:.3f}:intensity={-0.012*w:.3f}:colors=r+y:strength=6,"
               f"colorbalance=rm={0.035*w2:.3f}:gm={0.008*w2:.3f}:bm={-0.05*w2:.3f}"
               f":rs={-0.035*w2:.3f}:gs={-0.004*w2:.3f}:bs={0.045*w2:.3f}")
        f = f"{pre},{mix},{bal},eq=saturation={L['sat']},selectivecolor={sel}"
        sk = skin(frame(clip, t, f))
        if sk is None:
            if k == 0:
                return f"{f},unsharp=5:5:0.35"   # no skin in the shot: base look only
            continue
        rb, lum = sk[0] - sk[2], sk @ [0.2126, 0.7152, 0.0722]
        err = abs(rb - SKIN_RB)
        if best is None or err < best[0]:
            best = (err, f)
    return f"{best[1]},unsharp=5:5:0.35"

SKIN_RB, SKIN_LUM = 60, 168   # target: warm golden tan (red minus blue) and not over-bright

def skin(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    l = a @ [0.2126, 0.7152, 0.0722]
    m = (r > g + 6) & (g > b + 4) & (r - b > 22) & (l > 90) & (l < 232)
    return a[m].mean(axis=0) if m.mean() > 0.04 else None

def _boost(sel, k):
    # extra warmth (less cyan, more yellow) and depth (black) on reds and yellows only: whites stay neutral
    add = {'reds': (-0.05, 0.015, 0.08, 0.06), 'yellows': (-0.03, 0.01, 0.06, 0.05)}
    out = []
    for part in sel.split(':'):
        name, vals = part.split('=')
        v = [float(x) for x in vals.strip("'").split()]
        d = add.get(name, (0, 0, 0, 0))
        v = [max(-1, min(1, a + k * b)) for a, b in zip(v, d)]
        out.append(f"{name}='{' '.join(f'{x:.3f}' for x in v)}'")
    return ':'.join(out)

if __name__ == '__main__':
    print(shot_filter(sys.argv[1], float(sys.argv[2]), sys.argv[3]))
