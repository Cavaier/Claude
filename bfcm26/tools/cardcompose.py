# python3 cardcompose.py <clip.mp4> <vidcard outdir> <photo appear t> <total s> <out.mp4> [--notext]
# Lays a Seedance clip into its fixed photo box under the animated vidcard.js layers. The clip starts when its photo appears,
# is slowed to fill the rest of the video, and keeps its own sound. --notext: the clip alone, full frame, same length.
import json,subprocess,sys
clip,d,tp,total,out=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4]),sys.argv[5]
notext='--notext' in sys.argv
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',clip]))
b=json.load(open(d+'/box.json'))
run=total-(0 if notext else tp);F=run/dur+0.005
aud=f"[0:a]atempo={1/F:.4f},volume=0.8,adelay={int(0 if notext else tp*1000)}:all=1,apad,atrim=0:{total},loudnorm=I=-16:TP=-1.5:LRA=11,aresample=48000[a]"
if notext:
    fc=f"[0:v]setpts={F:.4f}*PTS,fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,format=yuv420p[v];"+aud
    ins=['-i',clip]
else:
    w,h,x,y=b['w'],b['h'],b['x'],b['y']
    fc=(f"[0:v]setpts={F:.4f}*PTS,fps=30,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,tpad=start_duration={tp}:start_mode=clone,format=rgba[c];"
        f"[2:v]format=rgba,crop={w}:{h}:{x}:{y},alphaextract[m];[c][m]alphamerge,fade=t=in:st={tp}:d=0.28:alpha=1[cm];"
        f"[1:v]fps=30,format=rgba[base];[base][cm]overlay={x}:{y}:format=auto[v1];")
    ins=['-i',clip,'-framerate','15','-i',d+'/a/f%04d.png','-loop','1','-i',d+'/mask.png']
    import os
    if os.listdir(d+'/top'):
        ins+=['-framerate','15','-i',d+'/top/f%04d.png'];fc+="[3:v]fps=30,format=rgba[t];[v1][t]overlay=0:0:format=auto,format=yuv420p[v];"
    else: fc+="[v1]format=yuv420p[v];"
    fc+=aud
subprocess.run(['ffmpeg','-y','-loglevel','error',*ins,'-filter_complex',fc,'-map','[v]','-map','[a]','-t',str(total),
 '-c:v','libx264','-crf','18','-preset','medium','-c:a','aac','-b:a','192k','-movflags','+faststart',out],check=True)
print(out)
