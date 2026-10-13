#!/usr/bin/env bash
# Assemble the Black Friday ad: 1080x1920, 30fps, cuts on 120 BPM beats.
set -euo pipefail
S=/tmp/claude-0/-home-user-Claude/72807007-e1d8-5697-9604-f4ebb6fbe10f/scratchpad
R=$S/raw/iphone C=$S/cards O=$S/out
mkdir -p $O/seg
# clip | in-point | duration | card | card fades in (0/1)
SHOTS=(
  "IMG_2153 0.0 2.5 hook 0"
  "IMG_2150 3.0 2.0 pool 1"
  "IMG_2151 0.3 2.0 pool 0"
  "IMG_2157 0.5 2.5 steel 1"
  "IMG_2167 1.0 2.5 fit 1"
  "IMG_2149 5.0 2.5 reviews 1"
  "IMG_2154 2.0 4.0 end 1"
)
: > $O/list.txt
i=0
for s in "${SHOTS[@]}"; do
  read -r clip in dur card fade <<<"$s"
  if [ "$fade" = 1 ]; then cf="fade=in:st=0:d=0.25:alpha=1"; else cf="null"; fi
  # gentle 4% push-in over the shot keeps static phone shots alive
  ffmpeg -v error -y -ss "$in" -t "$dur" -i "$R/$clip.MOV" -loop 1 -t "$dur" -i "$C/$card.png" -filter_complex \
    "[0:v]fps=30,scale=1080:1920,setsar=1,scale=w='1080*(1+0.04*t/$dur)':h='1920*(1+0.04*t/$dur)':eval=frame,crop=1080:1920,eq=saturation=1.08:contrast=1.03[v];[1:v]format=rgba,$cf[t];[v][t]overlay=0:0:format=auto,format=yuv420p[o]" \
    -map "[o]" -an -c:v libx264 -preset medium -crf 17 -r 30 "$O/seg/$i.mp4"
  echo "file '$O/seg/$i.mp4'" >> $O/list.txt
  i=$((i+1))
done
ffmpeg -v error -y -f concat -safe 0 -i $O/list.txt -i $S/assets/music.mp3 \
  -filter_complex "[1:a]atrim=0:18,afade=t=out:st=16.8:d=1.2,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
  -map 0:v -map "[a]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest \
  "$O/cavaier-black-friday-30off-pool-9x16.mp4"
ffprobe -v error -show_entries format=duration,size -of default=nw=1 "$O/cavaier-black-friday-30off-pool-9x16.mp4"
