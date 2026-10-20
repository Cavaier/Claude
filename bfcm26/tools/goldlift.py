# python3 goldlift.py in.jpg out.jpg [strength] : make dull/dark/brassy gold read as light 14k gold.
# Small global lift + a soft mask on gold tones only (hue 33-58 deg, saturated, not dark): brighter, paler, more yellow, less orange.
# Works in float RGB (no 8-bit HSV round trip, so no banding in hair or shadows).
import sys, numpy as np
from PIL import Image, ImageFilter
src,dst=sys.argv[1],sys.argv[2]; k=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
x=np.asarray(Image.open(src).convert('RGB')).astype(np.float32)/255
x=np.clip(1-(1-x)**(1+0.12*k),0,1)                         # gentle global lift
r,g,b=x[...,0],x[...,1],x[...,2]; mx=x.max(-1); mn=x.min(-1); d=mx-mn+1e-6
h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))*60
s=d/(mx+1e-6)
m=np.clip(1-np.abs(h-45)/14,0,1)*np.clip((s-0.22)/0.2,0,1)*np.clip((mx-0.3)/0.2,0,1)
m=np.asarray(Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(np.float32)/255*k
m=m[...,None]
light=1-(1-x)*0.55                                          # brighter metal
tint=np.array([1.0,0.95,0.80],np.float32)                   # light 14k: pale warm yellow
light=light*tint+ (light.mean(-1,keepdims=True)*tint)*0.0
lum=x.mean(-1,keepdims=True)
light=lum+(light-lum)*0.85                                  # a touch less saturated than brass
out=np.clip(x*(1-0.75*m)+light*0.75*m,0,1)
Image.fromarray((out*255+0.5).astype(np.uint8)).save(dst,quality=93)
