# Pro colour grade for stills cut from video, straight from the 4K camera original (Eli's reference look):
# even golden sun-kissed skin (no pink/yellow blotches), neutral whites, true blacks, clean full tonal range.
# usage: pro_grade.py raw16.png out16.png grabcut|global [mask_preview.png]
#   grabcut: skin found with GrabCut seeded by the warmest pixels (frames with bouclé / walls)
#   global : the frame is (nearly) all skin, every non-dark pixel is treated as skin
import sys, subprocess, numpy as np, cv2
src, out, mode = sys.argv[1:4]; prev = sys.argv[4] if len(sys.argv) > 4 else None
TA, TB = 7.0, 13.5          # target skin colour (Lab a/b): muted golden tan, hue ~63 (ref: a 10 / b 15 at L~56; lighter skin needs less chroma or it reads orange)

def rd(p):
    b = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(b, np.uint16).reshape(3840, 2160, 3).astype(np.float32) / 65535
def wr(p, im):
    y = (np.clip(im, 0, 1) * 65535 + 0.5).astype('<u2')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', '2160x3840', '-i', '-', '-pix_fmt', 'rgb48be', p], input=y.tobytes(), check=True)
G = lambda x, s: cv2.GaussianBlur(x, (0, 0), s)

im = rd(src); H, W = im.shape[:2]
lab = cv2.cvtColor(im, cv2.COLOR_RGB2Lab); L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]

# ---- skin mask ----
sm = cv2.resize(im, (540, 960), interpolation=cv2.INTER_AREA)
sl = cv2.cvtColor(G(sm, 3), cv2.COLOR_RGB2Lab); sL, sa, sb = sl[..., 0], sl[..., 1], sl[..., 2]
sc = np.hypot(sa, sb); sh = np.degrees(np.arctan2(sb, sa))
if mode == 'global':
    m = (sL > 25).astype(np.uint8)
else:
    warm = (sh > 40) & (sh < 100)
    gm = np.full(sL.shape, cv2.GC_PR_BGD, np.uint8)
    gm[warm & (sc > np.percentile(sc[warm], 60))] = cv2.GC_PR_FGD
    gm[warm & (sc > np.percentile(sc[warm], 80)) & (sL > 35)] = cv2.GC_FGD
    gm[(sc < np.percentile(sc, 25)) & (sL > 40)] = cv2.GC_BGD
    gm[sL < 22] = cv2.GC_BGD
    u8 = (np.clip(sm, 0, 1) * 255).astype(np.uint8)[..., ::-1].copy()
    cv2.grabCut(u8, gm, None, np.zeros((1, 65)), np.zeros((1, 65)), 6, cv2.GC_INIT_WITH_MASK)
    m = ((gm == cv2.GC_FGD) | (gm == cv2.GC_PR_FGD)).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
skin = np.clip(G(cv2.resize(m.astype(np.float32), (W, H), interpolation=cv2.INTER_LINEAR), 10), 0, 1)
dark = np.clip((28 - G(L, 4)) / 12, 0, 1)                   # jewelry, black top, hair: stay neutral
metal = np.clip((3.5 - G(np.hypot(a, b), 2)) / 2.0, 0, 1)    # neutral metal (chain links, cuff) never gets skin colour
skin *= (1 - dark) * (1 - metal)
if prev: cv2.imwrite(prev, (cv2.resize(skin, (540, 960)) * 255).astype(np.uint8))

# ---- tone: true blacks, clean whites, gentle S ----
p1, p99 = np.percentile(L, 0.7), np.percentile(L, 99.7)
t = np.clip((L - p1) / (p99 - p1), 0, 1)
t = t + 0.07 * np.sin(np.pi * t) * (t - 0.5) * 2
L = 100 * (0.035 + 0.945 * t)

# ---- skin colour: only the low-frequency colour moves (blotches go, fine colour detail stays) ----
al, bl = G(a, 24), G(b, 24)
ms = skin > 0.6
am, bm = np.median(al[ms]), np.median(bl[ms])
k = 1.6                                                      # keep (and slightly boost) natural colour variation: real skin, not paint
a = a + skin * ((TA + k * 0.6 * (al - am)) - al)
b = b + skin * ((TB + k * 0.6 * (bl - bm)) - bl)
L = L - skin * 7.0 * np.clip(L / 80, 0, 1)                  # deeper = sun-kissed tan, highlights keep sheen

# ---- everything else neutral & quiet (graphite brand): whites/greys/blacks lose their cast ----
rest = 1 - skin
a = a * (1 - 0.8 * rest); b = b * (1 - 0.8 * rest)
L = L + rest * (1 - dark) * 4.0 * np.clip((L - 55) / 30, 0, 1)   # light backgrounds a little brighter/cleaner

lab[..., 0], lab[..., 1], lab[..., 2] = L, a, b
wr(out, cv2.cvtColor(lab, cv2.COLOR_Lab2RGB))
print('ok', out, 'skin %.2f' % (skin > 0.5).mean(), 'src skin a %.1f b %.1f' % (am, bm))
