#!/usr/bin/env bash
# Vacier-style Black Friday ad: slow-motion macro shots, muted neutral grade, minimal mid-frame text.
set -euo pipefail
S=/tmp/claude-0/-home-user-Claude/72807007-e1d8-5697-9604-f4ebb6fbe10f/scratchpad
R=$S/raw/m1 C=$S/cards2 O=$S/out2
mkdir -p $O/seg
SLOW=3   # 120 fps source played 3x slower
# clip | source in-point | source duration | card
SHOTS=(
  "C1133 0.3 1.0 s1"
  "C1070 3.5 1.0 s2"
  "C1176 0.5 1.0 s3"
  "C1132 0.2 1.0 s4"
)
# matched to the brand reference: cooler white balance, tan pulled from orange to peach-beige,
# neutral whites, soft contrast, light sharpening for skin texture
GRADE="colortemperature=temperature=5600:mix=0.5:pl=1,selectivecolor=reds='0 0 -0.06 0':yellows='0 0 -0.15 0':whites='0 0 -0.05 0',colorbalance=bm=0.01:bh=0.015,eq=saturation=0.84:contrast=0.97:brightness=0.02,curves=all='0/0.03 0.5/0.53 1/0.98',unsharp=5:5:0.45"
: > $O/list.txt
i=0
for s in "${SHOTS[@]}"; do
  read -r clip in sdur card <<<"$s"
  dur=$(python3 -c "print($sdur*$SLOW)")
  ffmpeg -v error -y -ss "$in" -t "$sdur" -i "$R/$clip.MP4" -loop 1 -t "$dur" -i "$C/$card.png" -filter_complex \
    "[0:v]setpts=$SLOW*PTS,fps=30,scale=1080:1920,setsar=1,$GRADE,scale=w='1080*(1+0.03*t/$dur)':h='1920*(1+0.03*t/$dur)':eval=frame,crop=1080:1920[v];[1:v]format=rgba,fade=in:st=0.3:d=0.6:alpha=1[t];[v][t]overlay=0:0:format=auto,format=yuv420p[o]" \
    -map "[o]" -an -c:v libx264 -preset medium -crf 16 -r 30 "$O/seg/$i.mp4"
  echo "file '$O/seg/$i.mp4'" >> $O/list.txt
  i=$((i+1))
done
OUT=$O/cavaier-black-friday-30off-minimal-9x16.mp4
ffmpeg -v error -y -f concat -safe 0 -i $O/list.txt -i $S/assets/music2.mp3 \
  -filter_complex "[0:v]fade=in:st=0:d=0.4,fade=out:st=11.5:d=0.5[v];[1:a]atrim=0:12,afade=t=in:d=0.3,afade=t=out:st=10.8:d=1.2,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest "$OUT"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
