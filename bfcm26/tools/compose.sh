#!/bin/sh
# compose.sh <seedance.mp4> <overlay.png> <out.mp4> : scale clip to 1080x1920, lay the sharp text layer on top, keep the clip's sound
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1")
ffmpeg -y -loglevel error -i "$1" -loop 1 -t "$D" -i "$2" -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1[b];[b][1:v]overlay=0:0:format=auto,format=yuv420p[v]" -map "[v]" -map "0:a?" -c:a aac -b:a 192k -t "$D" -c:v libx264 -crf 18 -preset medium -movflags +faststart "$3"
