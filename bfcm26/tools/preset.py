# python3 preset.py in.jpg out.jpg <editorial|film|luxe> : finishing "filter" applied after goldfix.py, so statics don't look straight out of camera.
#  editorial: bright airy magazine look - soft S-curve, faint matte, warm highlights / neutral shadows, subtle glow
#  film:      warm analogue look - matte lifted blacks, creamy highlights, gentle warm cast, fine grain
#  luxe:      rich jewellery-campaign look - deeper contrast, polished highlights, slight vignette, cooler shadows
import sys, numpy as np
from PIL import Image, ImageFilter
src,dst,mode=sys.argv[1],sys.argv[2],sys.argv[3]
x=np.asarray(Image.open(src).convert('RGB')).astype(np.float32)/255; H,W=x.shape[:2]
def curve(v,a): return v+a*(v-0.5)*(1-np.abs(2*v-1))          # soft S (a>0) around mid grey
L=x.mean(-1,keepdims=True)
if mode=='editorial':
    x=curve(x,0.18); x=x*0.97+0.025
    x=x+np.clip((L-0.55)/0.45,0,1)*np.array([0.025,0.012,-0.012])
    glow=np.asarray(Image.fromarray((np.clip(x,0,1)*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(12))).astype(np.float32)/255
    x=x*0.9+np.maximum(x,glow)*0.1
elif mode=='film':
    x=curve(x,0.12); x=x*0.92+0.06
    x=x*np.array([1.03,1.0,0.95])+np.clip((L-0.6)/0.4,0,1)*np.array([0.02,0.015,0.0])
    l=x.mean(-1,keepdims=True); x=l+(x-l)*0.9
    x=x+np.random.default_rng(1).normal(0,0.012,(H,W,1)).astype(np.float32)
elif mode=='luxe':
    x=curve(x,0.32)
    x=x+np.clip((0.35-L)/0.35,0,1)*np.array([-0.01,0.0,0.015])
    yy,xx=np.mgrid[0:H,0:W]; r=np.sqrt(((xx-W/2)/(W/2))**2+((yy-H/2)/(H/2))**2); x=x*(1-0.14*np.clip(r-0.55,0,1)[...,None])
out=Image.fromarray((np.clip(x,0,1)*255+.5).astype(np.uint8))
out.save(dst,quality=94)
