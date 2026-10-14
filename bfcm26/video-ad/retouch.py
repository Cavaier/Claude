# Professional retouch for stills cut from video (Lightroom develop + Photoshop retouch + jewelry precision pass).
# usage: retouch.py in16.png out16.png x0,y0,x1,y1 [debug_prefix]
#   in16.png: graded 16-bit frame (from stillmatch.py), 2160x3840
#   x0..y1  : jewelry box in pixels (the precision pass only works inside it)
import sys, subprocess, numpy as np, cv2

src, out, box = sys.argv[1:4]; dbg = sys.argv[4] if len(sys.argv) > 4 else None
x0, y0, x1, y1 = map(int, box.split(','))

def rd(p):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint16).reshape(3840, 2160, 3).astype(np.float32) / 65535
def wr(p, im):
    y = (np.clip(im, 0, 1) * 65535 + 0.5).astype('<u2')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', '2160x3840', '-i', '-', '-pix_fmt', 'rgb48be', p], input=y.tobytes(), check=True)
def blur(a, s): return cv2.GaussianBlur(a, (0, 0), s)
def smooth(m, s): return np.clip(blur(m.astype(np.float32), s), 0, 1)
def save_mask(name, m):
    if dbg: cv2.imwrite(f'{dbg}_{name}.png', (np.clip(cv2.resize(m, (540, 960)), 0, 1) * 255).astype(np.uint8))

im = rd(src)
H, W = im.shape[:2]

# ---------- LIGHTROOM: develop ----------
# 1. Noise reduction: kill video chroma noise / blocking, keep luminance detail.
lab = cv2.cvtColor(im, cv2.COLOR_RGB2Lab)           # L 0..100, a/b ~ -127..127
for c in (1, 2):
    lab[..., c] = cv2.bilateralFilter(lab[..., c], 9, 4, 6)
L = lab[..., 0]
L = 0.7 * L + 0.3 * cv2.bilateralFilter(L, 5, 2.0, 3)  # light luminance NR
# 2. Highlights -12, shadows +10 (on a soft base so edges keep their contrast)
base = blur(L, 25)
hl = np.clip((base - 70) / 30, 0, 1); sh = np.clip((40 - base) / 40, 0, 1)
L = L - 6 * hl * (L / 100) + 5 * sh * (1 - L / 100)
# 3. Texture (fine) + clarity (mid), midtones only
mid = np.exp(-((L - 55) / 30) ** 2)
L = L + 0.35 * (L - blur(L, 3)) + 0.18 * mid * (L - blur(L, 40))
# 4. Tone curve: gentle S, true blacks, clean whites
t = np.clip(L / 100, 0, 1)
t = t + 0.06 * np.sin(np.pi * t) * (t - 0.5) * 2
t = np.clip((t - 0.012) / (0.995 - 0.012), 0, 1)
lab[..., 0] = t * 100

# ---------- PHOTOSHOP: skin ----------
a, b = lab[..., 1], lab[..., 2]
hue = np.degrees(np.arctan2(b, a)); chroma = np.hypot(a, b)
dk = cv2.dilate(((lab[..., 0] < 45) & (chroma < 16)).astype(np.uint8), np.ones((25, 25), np.uint8))  # metal/hair + margin
skin = ((hue > 50) & (hue < 95) & (chroma > 11) & (chroma < 50) & (lab[..., 0] > 25) & (lab[..., 0] < 95)).astype(np.uint8)
skin = cv2.morphologyEx(skin, cv2.MORPH_CLOSE, np.ones((31, 31), np.uint8))
skin = cv2.morphologyEx(skin, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
skin = smooth(skin.astype(np.float32) * (1 - dk), 10)
# HSL: unify skin hue toward its median (less blotchy red/green), saturation -4%, luminance +1
if skin.sum() > 1000:
    ws = skin > 0.5
    hmed = np.median(hue[ws]); cmed = np.median(chroma[ws])
    hn = hue + 0.35 * skin * (hmed - hue)
    cn = chroma * (1 - 0.04 * skin)
    a = cn * np.cos(np.radians(hn)); b = cn * np.sin(np.radians(hn))
# Frequency separation: low = colour/tone, high = pores/texture (kept untouched)
Lc = lab[..., 0]
low = blur(Lc, 8); high = Lc - low
# dodge & burn: even out tone blotches inside skin (large-scale stays: shape/light)
even = blur(low, 30)
low2 = low + 0.55 * skin * (even - low)   # pull mid-scale blotches toward the smooth form
# blemish / red-spot removal on the low layer (small dark or red dots on skin)
spot = ((low - blur(low, 15)) < -2.2) | ((a - blur(a, 15)) > 3.0) | ((low - blur(low, 40)) < -4.0)
spot = (spot & (skin > 0.8) & (dk == 0)).astype(np.uint8)
n, lbl, st, _ = cv2.connectedComponentsWithStats(spot, 8)
keep = np.zeros_like(spot)
for i in range(1, n):
    if 6 <= st[i, cv2.CC_STAT_AREA] <= 3000 and max(st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT]) <= 90: keep[lbl == i] = 1
keep = cv2.dilate(keep, np.ones((9, 9), np.uint8))
if keep.any():
    km = smooth(keep, 3)
    for arr in (low2, a, b):
        lo_, hi_ = np.percentile(arr, 0.5), np.percentile(arr, 99.5)
        u8 = np.clip((arr - lo_) / (hi_ - lo_) * 255, 0, 255).astype(np.uint8)
        fill = cv2.inpaint(u8, keep, 9, cv2.INPAINT_TELEA).astype(np.float32) / 255 * (hi_ - lo_) + lo_
        arr[...] = arr + km * (fill - arr)
save_mask('skin', skin); save_mask('spots', keep.astype(np.float32))
lab[..., 0] = low2 + high; lab[..., 1] = a; lab[..., 2] = b

# ---------- PHOTOSHOP: jewelry precision pass ----------
Lj = lab[..., 0]; cj = np.hypot(lab[..., 1], lab[..., 2])
roi = np.zeros((H, W), np.float32); roi[y0:y1, x0:x1] = 1
jew = ((Lj < 42) & (cj < 14)).astype(np.uint8) * (roi > 0)
jew = cv2.morphologyEx(jew.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
n, lbl, st, _ = cv2.connectedComponentsWithStats(jew, 8)
jm = np.zeros_like(jew)
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] > 4000: jm[lbl == i] = 1          # drop specks / pores
Jc = smooth(jm, 1.5) * roi                                       # colour: metal only (no skin rim)
jm = cv2.dilate(jm, np.ones((3, 3), np.uint8))                   # luminance: + speculars on the rim
J = smooth(jm, 1.5) * roi
# texture map: chains = busy, cuff = smooth polished surface
var = blur(Lj ** 2, 4) - blur(Lj, 4) ** 2
busy = smooth((var > 12).astype(np.float32), 3)
chain = J * busy; cuff = J * (1 - busy)
save_mask('jewelry', J); save_mask('chain', chain); save_mask('cuff', cuff)
# a) metal colour: black finish = neutral, very slightly cool, no skin spill / fringing
lab[..., 1] = lab[..., 1] * (1 - 0.7 * Jc) + (-0.4) * Jc
lab[..., 2] = lab[..., 2] * (1 - 0.7 * Jc) + (-1.0) * Jc
Lj = lab[..., 0]
# b) cuff: polished = clean smooth gradient (remove noise/grain/dust), then crisp specular
cu = cv2.bilateralFilter(Lj, 15, 6, 8)
cu = cv2.medianBlur(np.clip(cu, 0, 100).astype(np.float32), 5)
Lj = Lj + cuff * (cu - Lj)
# b2) scratches / dust / fingerprints on the polished cuff: anything that sticks out of the smooth
#     reflection gradient inside the eroded cuff is inpainted from its surroundings
cuffzone = blur(busy, 25) < 0.45                                   # cuff body (chains stay busy at this scale)
inner = (cv2.erode((J > 0.5).astype(np.uint8), np.ones((9, 9), np.uint8)) > 0) & cuffzone
ref = blur(cv2.medianBlur(np.clip(Lj * 2.55, 0, 255).astype(np.uint8), 31).astype(np.float32) / 2.55, 4)
d0 = (inner & (np.abs(Lj - ref) > 4.0)).astype(np.uint8)
n, lbl, st, _ = cv2.connectedComponentsWithStats(d0, 8)
defect = np.zeros_like(d0)
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] <= 600 and max(st[i, cv2.CC_STAT_WIDTH], st[i, cv2.CC_STAT_HEIGHT]) <= 70: defect[lbl == i] = 1
defect = cv2.dilate(defect, np.ones((5, 5), np.uint8)) * inner
if defect.any():
    L8 = np.clip(Lj * 2.55, 0, 255).astype(np.uint8)
    fill = cv2.inpaint(L8, defect.astype(np.uint8), 5, cv2.INPAINT_TELEA).astype(np.float32) / 2.55
    Lj = np.where(defect > 0, blur(fill, 1.5), Lj)
save_mask('defects', defect.astype(np.float32))
# c) chains: precision sharpening of every link (fine radius), micro-contrast
L0 = Lj.copy()
Ls = Lj + 0.55 * (Lj - blur(Lj, 1.0)) + 0.18 * (Lj - blur(Lj, 5))
lo = cv2.erode(L0, np.ones((3, 3), np.uint8)) - 1.5; hi = cv2.dilate(L0, np.ones((3, 3), np.uint8)) + 1.5
Lj = Lj + chain * (np.clip(Ls, lo, hi) - Lj)                     # no halos: clamp overshoot to local range
# d) depth: deepen blacks, lift speculars (reflections read as real polished metal)
dark = np.clip((30 - Lj) / 30, 0, 1); spec = np.clip((Lj - 45) / 40, 0, 1)
Lj = Lj - Jc * 3 * dark + Jc * 4 * spec
# e) edge definition: thin contact shadow where metal meets skin
edge = np.clip(smooth(jm, 6) - smooth(jm, 1.5), 0, 1) * roi * (skin > 0.3)
Lj = Lj - 2.0 * edge
lab[..., 0] = Lj

# ---------- LIGHTROOM: finish ----------
rgb = cv2.cvtColor(lab, cv2.COLOR_Lab2RGB)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / np.sqrt(2)
rgb = rgb * (1 - 0.10 * np.clip((r - 0.45) / 0.55, 0, 1) ** 2)[..., None]   # subtle vignette
rng = np.random.default_rng(7)
g = blur(rng.standard_normal((H, W)).astype(np.float32), 0.7) * 0.006          # fine film grain
rgb = rgb + g[..., None]
wr(out, rgb)
print('ok', out)
