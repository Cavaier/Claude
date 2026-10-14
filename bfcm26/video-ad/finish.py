# Finish for stills cut from video (after pro_grade.py + retouch.py): light falloff toward the jewelry,
# midtone micro-contrast, crop. Colour is done in pro_grade.py.
# usage: finish.py in16.png out.jpg cx,cy crop_w,crop_h out_w,out_h
#   cx,cy    : jewelry centre (4K px); the light falls off away from it
#   crop_w,h : crop box in 4K px (keep it >= out size so no upscaling); cropping is free per ad (Eli: variety)
import sys, subprocess, numpy as np, cv2
from PIL import Image
src, out = sys.argv[1:3]
cx, cy = map(int, sys.argv[3].split(',')); cw, ch = map(int, sys.argv[4].split(',')); ow, oh = map(int, sys.argv[5].split(','))
b = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-'], capture_output=True, check=True).stdout
im = np.frombuffer(b, np.uint16).reshape(3840, 2160, 3).astype(np.float32) / 65535
H, W = im.shape[:2]
lab = cv2.cvtColor(im, cv2.COLOR_RGB2Lab)
L = lab[..., 0]
# light falloff: brightest on the jewelry, gently darker toward the edges (directional, 3D feel)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
d = np.hypot((xx - cx) / 1100, (yy - cy) / 1500)
L *= 1 - 0.14 * np.clip(d - 0.35, 0, 1) ** 1.4
# micro-contrast on midtones (crisp, not crunchy)
mid = np.exp(-((L - 60) / 30) ** 2)
L += 0.2 * mid * (L - cv2.GaussianBlur(L, (0, 0), 30))
lab[..., 0] = L
rgb = np.clip(cv2.cvtColor(lab, cv2.COLOR_Lab2RGB), 0, 1)
x0 = int(np.clip(cx - cw / 2, 0, W - cw)); y0 = int(np.clip(cy - ch / 2, 0, H - ch))
crop = (rgb[y0:y0 + ch, x0:x0 + cw] * 255 + 0.5).astype(np.uint8)
Image.fromarray(crop).resize((ow, oh), Image.LANCZOS).save(out, quality=95, subsampling=0)
print('ok', out, (x0, y0, cw, ch))
