#!/bin/bash
# Stills from video, one clip: 4K original frames around TIME -> sharpest -> matched to the video grade -> retouch (natural skin + jewelry pass). Run from the fm work dir; then finish.py for skin colour + crop.
# usage: run.sh CLIP TIME BOX   (4K originals in orig/, proxy for the grade reference)
set -e
c=$1; t=$2; box=$3; V=/home/user/Claude/bfcm26/video-ad
d=redo/$c; mkdir -p $d/raw
st=$(python3 -c "print(max(0,$t-0.5))")
ffmpeg -nostdin -y -loglevel error -ss $st -t 1.0 -i orig/$c.MP4 -vsync 0 -pix_fmt rgb48be $d/raw/f_%04d.png
px=raw/w11/$c.MP4; [ -f $px ] || px=p180/$c.MP4
G=$(GRADE_ADAPT=0 python3 -I tools/grade.py $px $t black </dev/null)
ffmpeg -nostdin -y -loglevel error -ss $t -i $px -frames:v 1 -vf "$G,scale=1080:1920:flags=lanczos" $d/ref.png
best=$(python3 -I - $d <<'PY'
import numpy as np,glob,sys
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
echo "best $best"
python3 -I $V/stillmatch.py $best $d/raw/f_0012.png $d/ref.png $d/graded16.png
RETOUCH_SKIN=0 RETOUCH_NR=0 python3 -I $V/retouch.py $d/graded16.png $d/nat16.png $box
