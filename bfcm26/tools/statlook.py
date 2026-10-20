# python3 statlook.py in.jpg out.jpg [strength] : Cavaier static look (Eli, Oct 20): bright, soft, matte, low contrast,
# neutral-to-slightly-cool white balance, natural (not orange) skin, low saturation, detail kept. Run goldlift.py after it on gold ads.
import sys, numpy as np
from PIL import Image, ImageFilter
src,dst=sys.argv[1],sys.argv[2]; k=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
im=Image.open(src).convert('RGB'); x=np.asarray(im).astype(np.float32)/255
# white balance toward neutral: pull the bright neutrals (background) to grey, gently
lum=x.mean(-1); bright=(lum>np.percentile(lum,70))
if bright.sum()>100:
    avg=x[bright].mean(0); gain=avg.mean()/avg; gain=1+(gain-1)*0.7*k; x=x*gain
x=x*np.array([1-0.02*k,1.0,1+0.025*k],np.float32)        # a touch cooler
# exposure + lifted shadows, softer contrast (matte)
x=1-(1-np.clip(x,0,1))**(1+0.22*k)
mid=0.55; x=mid+(x-mid)*(1-0.12*k); x=x*(1-0.05*k)+0.05*k  # lower contrast, matte blacks
# lower saturation, extra on orange skin tones
l=x.mean(-1,keepdims=True); r,g,b=x[...,0],x[...,1],x[...,2]
orange=np.clip((r-b-0.08)/0.25,0,1)[...,None]
x=l+(x-l)*(1-(0.14+0.10*orange)*k)
out=Image.fromarray((np.clip(x,0,1)*255+0.5).astype(np.uint8))
out=out.filter(ImageFilter.UnsharpMask(radius=1.6,percent=int(40*k),threshold=2))  # keep skin/hair/link detail crisp
out.save(dst,quality=93)
