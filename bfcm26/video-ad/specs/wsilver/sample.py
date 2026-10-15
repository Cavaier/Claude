import json,sys,os,subprocess
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
# sample.py <folderid> <label> <max> [start name] [end name]
fid,label,mx=sys.argv[1],sys.argv[2],int(sys.argv[3])
lo=sys.argv[4] if len(sys.argv)>4 else ''; hi=sys.argv[5] if len(sys.argv)>5 else '~'
d=json.load(open('women.json'))
items=sorted([v for v in d.values() if v['path'].split('/')[-1]==fid and lo<=v['name']<=hi],key=lambda v:v['name'])
step=max(1,-(-len(items)//mx)); items=items[::step]
od='th/'+fid; os.makedirs(od,exist_ok=True)
def get(v):
    f=f"{od}/{v['name']}.jpg"
    if not os.path.exists(f) or os.path.getsize(f)<1000: subprocess.run(['curl','-s','-o',f,v['thumb']])
    return f
with ThreadPoolExecutor(24) as ex: files=list(ex.map(get,items))
C=12; W=160; H=240
rows=-(-len(items)//C)
sh=Image.new('RGB',(C*W,rows*(H+16)),'white'); dr=ImageDraw.Draw(sh)
for i,(v,f) in enumerate(zip(items,files)):
    try: im=Image.open(f).convert('RGB'); im.thumbnail((W,H))
    except Exception: continue
    x,y=(i%C)*W,(i//C)*(H+16); sh.paste(im,(x,y)); dr.text((x+2,y+H+2),v['name'][:24],fill='black')
sh.save(f'sheet_{label}.jpg',quality=82); print(label,len(items),'step',step)
