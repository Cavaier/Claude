"""Per-shot grade for flat camera footage: base normalise, white-patch match, then a shared look.

Usage: python3 grade.py <clip> <time> <look>   -> prints the ffmpeg filter string for that shot.
The white patch is the bright, least-coloured pixels (studio wall, boucle, white top; nails and skin excluded); its mean is matched to
the look's white target, so every cut in an ad lands on the same white balance and exposure.
"""
import subprocess, sys, io
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
    return f"{pre},{mix},eq=saturation={L['sat']},selectivecolor={L['sel']},unsharp=5:5:0.35"

if __name__ == '__main__':
    print(shot_filter(sys.argv[1], float(sys.argv[2]), sys.argv[3]))
