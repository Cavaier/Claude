#!/usr/bin/env bash
# Luxury slow-mo Black Friday ad from Women Session 7 (120 fps): every source frame used (4x slower),
# grade matched to the brand reference, editorial lockups that fade in with a slight rise.
set -euo pipefail
S=/tmp/claude-0/-home-user-Claude/72807007-e1d8-5697-9604-f4ebb6fbe10f/scratchpad
R=$S/raw/w7 O=$S/out4
mkdir -p $O/seg
SLOW=4
GRADE=$(cat $S/grade7/grade.txt)
# clip | source in-point | source duration | lockup png
SHOTS=(
  "C0709 10.8 0.80 $S/cards4l/s1.png"
  "C0715 0.40 0.75 $S/cards4l/s2.png"
  "C0769 3.90 0.75 $S/cards4d/s3.png"
  "C0758 13.5 0.75 $S/cards4l/s4.png"
  "C0718 0.50 1.00 $S/cards4l/s5.png"
)
: > $O/list.txt
i=0
for s in "${SHOTS[@]}"; do
  read -r clip in sdur card <<<"$s"
  dur=$(python3 -c "print($sdur*$SLOW)")
  # lockup: fades in from 0.35s over 0.9s while rising 16px with an ease-out
  ffmpeg -v error -y -ss "$in" -t "$sdur" -i "$R/$clip.MP4" -loop 1 -t "$dur" -i "$card" -filter_complex \
    "[0:v]setpts=$SLOW*PTS,fps=30000/1001,scale=1080:1920,setsar=1,$GRADE,scale=w='1080*(1+0.02*t/$dur)':h='1920*(1+0.02*t/$dur)':eval=frame,crop=1080:1920[v];[1:v]format=rgba,fade=in:st=0.35:d=0.9:alpha=1[t];[v][t]overlay=x=0:y='16*pow(1-min(max((t-0.35)/1.1,0),1),3)':eval=frame:format=auto,format=yuv420p[o]" \
    -map "[o]" -an -c:v libx264 -preset medium -crf 16 "$O/seg/$i.mp4"
  echo "file '$O/seg/$i.mp4'" >> $O/list.txt
  i=$((i+1))
done
OUT=$O/cavaier-black-friday-30off-slowmo-9x16.mp4
T=$(python3 -c "print(round(sum(float(l.split()[2]) for l in '''$(printf '%s\n' "${SHOTS[@]}")'''.splitlines())*$SLOW,2))")
ffmpeg -v error -y -f concat -safe 0 -i $O/list.txt -i $S/assets/music3.mp3 \
  -filter_complex "[0:v]fade=in:st=0:d=0.5,fade=out:st=$(python3 -c "print($T-0.7)"):d=0.7[v];[1:a]atrim=0:$T,afade=t=in:d=0.4,afade=t=out:st=$(python3 -c "print($T-1.6)"):d=1.6,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest "$OUT"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
