#!/usr/bin/env bash
# Vacier-style Black Friday ad: slow-motion macro shots, muted neutral grade, minimal mid-frame text.
set -euo pipefail
S=/tmp/claude-0/-home-user-Claude/72807007-e1d8-5697-9604-f4ebb6fbe10f/scratchpad
R=$S/raw/w11 C=$S/cards3 O=$S/out3
mkdir -p $O/seg
SLOW=1   # 25 fps source already reads slow
# clip | source in-point | source duration | card
SHOTS=(
  "C2287 1.6 3.0 s1"
  "C2384 1.0 2.6 s2"
  "C2386 1.8 2.6 s3"
  "C2360 3.2 2.4 s4"
  "C2382 2.0 2.4 s5"
)
# flat camera footage graded to the brand reference: expanded levels, soft S-curve,
# neutral bright whites, deep blacks, peach skin, light sharpening
GRADE="colorlevels=rimin=0.06:gimin=0.06:bimin=0.05:rimax=0.79:gimax=0.79:bimax=0.765,curves=all='0/0 0.25/0.22 0.5/0.53 0.75/0.81 1/1',eq=saturation=1.15,selectivecolor=reds='-0.08 0.02 0.07 0':yellows='-0.04 0 -0.02 0':whites='0 0 0 0',unsharp=5:5:0.35"
: > $O/list.txt
i=0
for s in "${SHOTS[@]}"; do
  read -r clip in sdur card <<<"$s"
  dur=$(python3 -c "print($sdur*$SLOW)")
  ffmpeg -v error -y -ss "$in" -t "$sdur" -i "$R/$clip.MP4" -loop 1 -t "$dur" -i "$C/$card.png" -filter_complex \
    "[0:v]setpts=$SLOW*PTS,fps=30,scale=1080:1920,setsar=1,$GRADE,scale=w='1080*(1+0.025*t/$dur)':h='1920*(1+0.025*t/$dur)':eval=frame,crop=1080:1920[v];[1:v]format=rgba,fade=in:st=0.3:d=0.6:alpha=1[t];[v][t]overlay=0:0:format=auto,format=yuv420p[o]" \
    -map "[o]" -an -c:v libx264 -preset medium -crf 16 -r 30 "$O/seg/$i.mp4"
  echo "file '$O/seg/$i.mp4'" >> $O/list.txt
  i=$((i+1))
done
OUT=$O/cavaier-black-friday-30off-black-9x16.mp4
ffmpeg -v error -y -f concat -safe 0 -i $O/list.txt -i $S/assets/music2.mp3 \
  -filter_complex "[0:v]fade=in:st=0:d=0.4,fade=out:st=12.4:d=0.6[v];[1:a]atrim=0:13,afade=t=in:d=0.3,afade=t=out:st=11.6:d=1.4,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest "$OUT"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
