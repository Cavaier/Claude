import json,sys,re
from PIL import Image
def lum(c):
    f=lambda v:(v/255)/12.92 if v/255<=0.03928 else ((v/255+0.055)/1.055)**2.4
    return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2])
cr=lambda a,b:(max(a,b)+0.05)/(min(a,b)+0.05)
for o in json.load(open(sys.argv[1])):
    im=Image.open(o['shot']).convert('RGB');px=im.load();print('##',o['file'])
    for e in o['els']:
        t=tuple(map(int,re.findall(r'\d+',e['color'])[:3]));tl=lum(t);L=[]
        for y in range(max(0,int(e['y'])),min(1920,int(e['y']+e['h'])),3):
            for x in range(max(0,int(e['x'])),min(1080,int(e['x']+e['w'])),3): L.append(lum(px[x,y]))
        if not L: continue
        L.sort(); worst=L[int(len(L)*0.9)] if tl<0.5 else L[int(len(L)*0.1)]
        c10=cr(tl,worst); fl=[]
        if not(e['y']>=270 and e['y']+e['h']<=1536): fl.append('SAFEZONE')
        if c10<(3 if e['fs']>=24 else 4.5): fl.append('LOWCONTRAST')
        if e['fs']/3<7: fl.append('TINY@FEED')
        print(f"{','.join(fl) or 'ok':12} fs{e['fs']:.0f} cr{c10:4.1f} y{e['y']:.0f}-{e['y']+e['h']:.0f}  {e['text']}")
