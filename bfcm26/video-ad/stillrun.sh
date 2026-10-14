#!/bin/bash
# Stills from video, one clip (run from the fm work dir that has orig/<CLIP>.MP4, the 4K original from dlorig.js):
#   frames around TIME -> sharpest -> pro_grade.py (reference look) -> retouch.py (skin natural, jewelry pass)
# usage: stillrun.sh CLIP TIME JEWELRY_BOX MASKMODE      e.g. stillrun.sh C2290 2.28 600,1500,1700,2500 grabcut
# then:  finish.py work/CLIP/nat16.png out.jpg cx,cy crop_w,crop_h out_w,out_h
set -e
c=$1; t=$2; box=$3; mode=${4:-grabcut}; V=/home/user/Claude/bfcm26/video-ad
d=work/$c; mkdir -p $d/raw
st=$(python3 -c "print(max(0,$t-0.5))")
ffmpeg -nostdin -y -loglevel error -ss $st -t 1.0 -i orig/$c.MP4 -vsync 0 -pix_fmt rgb48be $d/raw/f_%04d.png
best=$(python3 -I - $d <<'PY'
import numpy as np,sys
from PIL import Image
d=sys.argv[1]; best=None
for i in range(7,18):
    f=f'{d}/raw/f_{i:04d}.png'
    im=np.asarray(Image.open(f).convert('L').resize((1080,1920)),dtype=np.float32)
    lap=im[1:-1,1:-1]*4-im[:-2,1:-1]-im[2:,1:-1]-im[1:-1,:-2]-im[1:-1,2:]
    t=60; v=np.sort([lap[y:y+t,x:x+t].var() for y in range(0,lap.shape[0]-t,t) for x in range(0,lap.shape[1]-t,t)])[::-1]
    s=float(v[:len(v)//20].mean())
    if best is None or s>best[0]: best=(s,f)
print(best[1])
PY
)
echo "sharpest: $best"
python3 -I $V/pro_grade.py $best $d/graded16.png $mode $d/skinmask.png
RETOUCH_SKIN=0 RETOUCH_NR=0 python3 -I $V/retouch.py $d/graded16.png $d/nat16.png $box
