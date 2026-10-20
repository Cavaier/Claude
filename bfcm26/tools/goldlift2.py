# python3 goldlift2.py in.jpg out.jpg [strength] : stronger light-14k gold (Eli, Oct 20: "dull, almost black, earwax yellow").
# Finds the metal (gold-hue pixels + the dark reflections next to them), then: lifts its darks hard, adds brightness,
# pulls it from brassy orange to pale champagne yellow and adds a clean specular sheen. Skin away from the metal is untouched.
import sys, numpy as np
from PIL import Image, ImageFilter
src,dst=sys.argv[1],sys.argv[2]; k=float(sys.argv[3]) if len(sys.argv)>3 else 1.0
im=Image.open(src).convert('RGB'); x=np.asarray(im).astype(np.float32)/255; H,W=x.shape[:2]
r,g,b=x[...,0],x[...,1],x[...,2]; mx=x.max(-1); mn=x.min(-1); d=mx-mn+1e-6
h=np.where(mx==r,((g-b)/d)%6,np.where(mx==g,(b-r)/d+2,(r-g)/d+4))*60; s=d/(mx+1e-6)
gold=np.clip(1-np.abs(h-44)/15,0,1)*np.clip((s-0.30)/0.2,0,1)*np.clip((mx-0.25)/0.2,0,1)   # saturated gold tones
u8=lambda a: Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8))
f=lambda a: np.asarray(a).astype(np.float32)/255
R=max(3,int(min(H,W)/220))
near=f(u8(gold).filter(ImageFilter.MaxFilter(2*R+1)).filter(ImageFilter.GaussianBlur(R)))   # region around the metal
dark=np.clip((0.55-mx)/0.3,0,1)*np.clip(1-np.abs(h-35)/32,0,1)                             # dark brownish reflections
metal=np.clip(np.maximum(gold, dark*near*1.0),0,1)
metal=f(u8(metal).filter(ImageFilter.GaussianBlur(max(1,R//3))))*k; m=metal[...,None]
L=x.mean(-1,keepdims=True)
L2=0.58+0.42*L                                              # lift darks of the metal: no near-black in the gold
champ=np.array([1.00,0.87,0.58],np.float32)                 # pale champagne 14k
newc=np.clip(L2*champ/champ.mean()*0.98,0,1)
sheen=np.clip((L-0.6)/0.4,0,1)*0.25                         # clean bright highlights
newc=np.clip(newc+sheen,0,1)
out=x*(1-0.9*m)+newc*0.9*m
u8(out).save(dst,quality=94)
