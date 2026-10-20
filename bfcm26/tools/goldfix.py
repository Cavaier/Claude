# python3 goldfix.py in.jpg out.jpg : approved finish for gold statics (Eli, Oct 20; W438 v3 look + pro polish).
# 1) statlook 0.2 (soft, clean, slightly brighter)  2) +10% saturation so skin stays warm and natural, never pale
# 3) Lightroom-style polish: highlights held, gentle clarity on mid tones, fine texture sharpening  4) goldlift 1.0 (light 14k gold)
# 5) house filter: preset.py film (Eli picked B · Film, Oct 20)
import sys, subprocess, os, numpy as np
from PIL import Image, ImageFilter
src,dst=sys.argv[1],sys.argv[2]; T=os.path.dirname(os.path.abspath(__file__)); a=dst+'.a.jpg'
subprocess.run([sys.executable,f'{T}/statlook.py',src,a,'0.2'],check=True)
x=np.asarray(Image.open(a)).astype(np.float32)/255
l=x.mean(-1,keepdims=True); x=np.clip(l+(x-l)*1.10,0,1)                        # saturation back
L=x.mean(-1,keepdims=True); x=x-0.05*np.clip((L-0.75)/0.25,0,1)*x              # hold highlights
blur=np.asarray(Image.fromarray((x*255+.5).astype(np.uint8)).filter(ImageFilter.GaussianBlur(16))).astype(np.float32)/255
mid=1-np.abs(x.mean(-1,keepdims=True)-0.5)*2; x=np.clip(x+(x-blur)*0.12*mid,0,1)  # clarity
Image.fromarray((x*255+.5).astype(np.uint8)).filter(ImageFilter.UnsharpMask(radius=1.0,percent=45,threshold=2)).save(a,quality=95)  # texture
subprocess.run([sys.executable,f'{T}/goldlift.py',a,a,'1.0'],check=True)
subprocess.run([sys.executable,f'{T}/preset.py',a,dst,'film'],check=True); os.remove(a)
