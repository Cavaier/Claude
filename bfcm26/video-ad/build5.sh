#!/usr/bin/env bash
# Build one ad from a shot list: per-shot matched grade (grade.py), 2x motion-compensated slow motion
# for 25 fps footage, lockup overlay with fade + rise, music bed.
# Usage: build5.sh <shots file> <lockup dir> <music mp3> <output mp4>
# shots file lines: <look> <raw subdir> <clip> <in> <source dur> <lockup name>
set -euo pipefail
S=/tmp/claude-0/-home-user-Claude/72807007-e1d8-5697-9604-f4ebb6fbe10f/scratchpad
SHOTS=$1 CARDS=$2 MUSIC=$3 OUT=$4
W=$(mktemp -d -p $S build5.XXXX)
SLOW=2
: > $W/list.txt
i=0
TOTAL=0
while read -r look dir clip in sdur card <&3; do
  [ -z "$look" ] && continue
  src=$S/raw/$dir/$clip.MP4
  mid=$(python3 -c "print($in+$sdur/2)")
  G=$(python3 -I $S/tools/grade.py "$src" "$mid" "$look" < /dev/null)
  dur=$(python3 -c "print($sdur*$SLOW)")
  base=$S/cache5/${clip}_${in}_${sdur}.mp4
  if [ ! -s "$base" ]; then
    mkdir -p $S/cache5
    ffmpeg -nostdin -v error -y -ss "$in" -t "$sdur" -i "$src" -vf \
      "minterpolate=fps=50:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:me=epzs:vsbmc=1:scd=none,setpts=$SLOW*PTS,fps=25,scale=1080:1920,setsar=1,$G,scale=w='1080*(1+0.02*t/$dur)':h='1920*(1+0.02*t/$dur)':eval=frame,crop=1080:1920,format=yuv420p" \
      -an -c:v libx264 -preset medium -crf 12 -r 25 "$base"
  fi
  ffmpeg -nostdin -v error -y -i "$base" -loop 1 -t "$dur" -i "$CARDS/$card.png" -filter_complex \
    "[1:v]format=rgba,fade=in:st=0.35:d=0.9:alpha=1[t];[0:v][t]overlay=x=0:y='16*pow(1-min(max((t-0.35)/1.1,0),1),3)':eval=frame:format=auto,format=yuv420p[o]" \
    -map "[o]" -an -c:v libx264 -preset medium -crf 15 -r 25 -t "$dur" "$W/$i.mp4"
  echo "file '$W/$i.mp4'" >> $W/list.txt
  TOTAL=$(python3 -c "print($TOTAL+$dur)")
  i=$((i+1))
done 3< "$SHOTS"
ffmpeg -nostdin -v error -y -f concat -safe 0 -i $W/list.txt -i "$MUSIC" \
  -filter_complex "[0:v]fade=in:st=0:d=0.5,fade=out:st=$(python3 -c "print($TOTAL-0.7)"):d=0.7[v];[1:a]atrim=0:$TOTAL,afade=t=in:d=0.4,afade=t=out:st=$(python3 -c "print($TOTAL-1.6)"):d=1.6,loudnorm=I=-16:TP=-1.5:LRA=11[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest "$OUT"
rm -rf $W
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$OUT"
