#!/usr/bin/env python3
"""Build an imitation video ad (copies the structure of a reference ad) from 120 fps men's footage.

Usage: FM=<frame method work dir> python3 imit.py spec.json
spec.json:
  "slow":     playback slow-down of the 120 fps footage (4 = every frame 4x slower, 2 = livelier montage)
  "shots":    [[look, raw subdir, clip, in, source dur, (optional) "push"|"slide"|"still"], ...]
  "inset":    optional {"x","y","w","h","bg"}: footage sits in a box on a flat colour (IM8 inset frame)
  "end":      optional {"dur", "bg"}: closing card segment on a flat colour (its layers come from overlays)
  "overlays": [{"png": name, "t0": s, "t1": s|null, "fi": fade in s, "fo": fade out s, "rise": px}, ...]
              PNGs from the overlay dir (ovl.js), timed on the whole timeline; t1 null = until the end
  "ovl":      overlay dir, "music": mp3, "out": mp4 (relative paths are relative to FM)
Grade: grade.py per shot (GRADE_SRC=graded light grade). Cache: <FM>/cache8.
"""
import json, os, subprocess, sys, tempfile

FM = os.environ['FM']
spec = json.load(open(sys.argv[1]))
P = lambda p: p if os.path.isabs(p) else os.path.join(FM, p)
SLOW = spec.get('slow', 4)
FPS = '30000/1001'
inset = spec.get('inset')
W = tempfile.mkdtemp(dir=FM, prefix='imit.')
os.makedirs(P('cache8'), exist_ok=True)

def run(args):
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y'] + args, check=True)

parts, total = [], 0.0
for i, sh in enumerate(spec['shots']):
    look, d, clip, t_in, sdur = sh[:5]
    move = sh[5] if len(sh) > 5 else 'push'
    src = P(f'raw/{d}/{clip}.MP4')
    dur = round(sdur * SLOW, 3)
    G = subprocess.run(['python3', '-I', P('tools/grade.py'), src, str(t_in + sdur / 2), look],
                       capture_output=True, text=True, check=True).stdout.strip()
    base = P(f'cache8/{clip}_{t_in}_{sdur}_{SLOW}_{move}.mp4')
    if not os.path.exists(base) or os.path.getsize(base) == 0:
        if move == 'slide':   # IM8 macro lateral slide
            mv = f"scale=1166:2074,crop=1080:1920:x='86*t/{dur}':y=77"
        elif move == 'still':
            mv = 'null'
        else:                 # gentle push-in
            mv = f"scale=w='1080*(1+0.035*t/{dur})':h='1920*(1+0.035*t/{dur})':eval=frame,crop=1080:1920"
        run(['-ss', str(t_in), '-t', str(sdur), '-i', src, '-vf',
             f'setpts={SLOW}*PTS,fps={FPS},scale=1080:1920,setsar=1,{G},{mv},format=yuv420p',
             '-an', '-c:v', 'libx264', '-preset', 'medium', '-crf', '12', '-r', FPS, base])
    out = f'{W}/s{i}.mp4'
    if inset:
        x, y, w, h, bg = inset['x'], inset['y'], inset['w'], inset['h'], inset['bg']
        run(['-i', base, '-f', 'lavfi', '-i', f'color=c={bg}:s=1080x1920:r={FPS}:d={dur}', '-filter_complex',
             f'[0:v]scale={w}:-2,crop={w}:{h}[f];[1:v][f]overlay={x}:{y}:shortest=1,format=yuv420p[o]',
             '-map', '[o]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-r', FPS, '-t', str(dur), out])
    else:
        run(['-i', base, '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-r', FPS, '-t', str(dur), out])
    parts.append(out); total += dur

end = spec.get('end')
if end:
    out = f'{W}/end.mp4'
    run(['-f', 'lavfi', '-i', f"color=c={end['bg']}:s=1080x1920:r={FPS}:d={end['dur']}",
         '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', out])
    parts.append(out); total += end['dur']

with open(f'{W}/list.txt', 'w') as f:
    f.writelines(f"file '{p}'\n" for p in parts)
run(['-f', 'concat', '-safe', '0', '-i', f'{W}/list.txt', '-c', 'copy', f'{W}/base.mp4'])

# timed overlays: fade + small rise, each enabled only inside its window
inputs, chain, last = ['-i', f'{W}/base.mp4'], [], '0:v'
for k, o in enumerate(spec.get('overlays', [])):
    t0 = o['t0']; t1 = o['t1'] if o.get('t1') is not None else total
    fi, fo, rise = o.get('fi', 0.25), o.get('fo', 0.2), o.get('rise', 0)
    inputs += ['-loop', '1', '-t', str(total), '-i', os.path.join(P(spec['ovl']), o['png'] + '.png')]
    fades = f'fade=in:st={t0}:d={fi}:alpha=1' if fi > 0 else 'null'
    if t1 < total and fo > 0:
        fades += f',fade=out:st={max(t0, t1 - fo)}:d={fo}:alpha=1'
    chain.append(f'[{k + 1}:v]format=rgba,{fades}[t{k}]')
    y = f"'{rise}*pow(1-min(max((t-{t0})/0.6,0),1),3)'" if rise else '0'
    chain.append(f"[{last}][t{k}]overlay=x=0:y={y}:eval=frame:enable='between(t,{t0},{t1})'[v{k}]")
    last = f'v{k}'
music = P(spec['music'])
inputs += ['-i', music]
mi = len(spec.get('overlays', [])) + 1
chain.append(f'[{last}]format=yuv420p[vo]')
chain.append(f'[{mi}:a]atrim=0:{total},afade=t=in:d=0.3,afade=t=out:st={total - 1.4}:d=1.4,'
             f'loudnorm=I=-16:TP=-1.5:LRA=11[a]')
run(inputs + ['-filter_complex', ';'.join(chain), '-map', '[vo]', '-map', '[a]', '-t', str(total),
              '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', FPS,
              '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', P(spec['out'])])
subprocess.run(['rm', '-rf', W])
print(spec['out'], round(total, 2), 's')
