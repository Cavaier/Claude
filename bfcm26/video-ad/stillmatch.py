# Stills cut from video: map an original-camera frame to the approved grade by per-channel quantile matching against a reference still.
import numpy as np, subprocess, sys
from PIL import Image
# usage: match.py src16.png ref_src16.png ref_graded8.png out16.png
src,refsrc,refg,out=sys.argv[1:]
def rd(p,w=2160,h=3840):
    b=subprocess.run(['ffmpeg','-v','error','-i',p,'-f','rawvideo','-pix_fmt','rgb48le','-'],capture_output=True,check=True).stdout
    return np.frombuffer(b,np.uint16).reshape(h,w,3).astype(np.float64)/65535
A=rd(refsrc)
A=A.reshape(1920,2,1080,2,3).mean(axis=(1,3))           # to 1080x1920
B=np.asarray(Image.open(refg).convert('RGB'),np.float64)/255
X=rd(src); Y=np.empty_like(X)
q=np.linspace(0,1,513)
for c in range(3):
    xs=np.quantile(A[...,c],q); ys=np.quantile(B[...,c],q)
    xs=np.maximum.accumulate(xs+np.arange(513)*1e-9)
    Y[...,c]=np.interp(X[...,c],xs,ys)
Y=(np.clip(Y,0,1)*65535+0.5).astype('<u2')
subprocess.run(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb48le','-s','2160x3840','-i','-','-pix_fmt','rgb48be',out],input=Y.tobytes(),check=True)
