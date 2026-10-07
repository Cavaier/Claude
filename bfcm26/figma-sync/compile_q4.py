"""Q4 flows page -> Figma specs. Usage: python3 compile_q4.py <workdir>  (after extract_q4.js)
Page 'Email Flows' (359:2), from x=6000: pop-up section (one row per sale period), then a Women band and a Men band.
Each flow is a section laid out like the canvas: big title, then the flow diagram (header, trigger, waits, labels, exit)
with every email frame placed where the canvas shows it."""
import json,sys,os,re,math
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,os.path.join(HERE,'..','q4'))
os.environ['KEEPF']='1'
_src=open(os.path.join(HERE,'compile.py')).read();_g={'__name__':'c0'};exec(_src[:_src.index('order=')],_g)  # comp()/hx() from compile.py
comp,hx=_g['comp'],_g['hx']
import q4_specs as Q
D=sys.argv[1]
E={e['id']:e for e in json.load(open(f'{D}/emails.json'))}
PN={'pre':'Pre-sale','ea':'Early access','bf':'Black Friday','cw':'Cyber Week','xmas':'Christmas','late':'Last minute','post':'After Christmas'}
FG,MU='#171717','#6B6B68'
def T(sec,x,y,w,h,s,fs,lh,fw=300,c=FG,ml=1,ls=0):  # text item in compile.py's format
    return ['x',sec,x,y,w,h,s,'Figtree',fw,0,fs,lh,ls,c,1,'',ml,'left']
def lines(s,fs,w): return max(1,math.ceil(len(s)*fs*0.5/w))
out={};secs=[]
def put(k,spec,sec,x,y,brief=None): out[k]=dict(spec=spec,sec=sec,pos=dict(x=x,y=y,by=y-150),brief=brief)
def emspec(k,name):
    S,I=comp(E[k]);e=E[k];bg=hx(e['bg']) if e['bg'] and e['bg']['a']>0 else None
    return dict(name=name,w=round(e['w']),h=round(e['h']),bg=bg,S=S,I=I)
X0,Y0=6000,0
# ---------- pop-up: one row per period
ROWH0=844+420
PERIOD={'pre':'Oct 27 – Nov 22','ea':'Nov 23 – 26 · publish Nov 23, 09:00','bf':'Nov 27 – Dec 6 · Black Friday + Cyber Week · publish Nov 27, 08:00',
        'xmas':'Dec 7 – Christmas cut-off · publish Dec 7','late':'Cut-off – Dec 24 · publish on the cut-off day','post':'Dec 26 → · publish Dec 26'}
LABW,GAP,ROWH=1500,120,844+420
y=200
for ph in ['pre','ea','bf','xmas','late','post']:
    put(f'L-POP-{ph}',dict(name=f'POP-{ph} label · {PN[ph]}',w=LABW-200,h=600,bg=None,S=[['label',0,0,LABW-200,600,0]],
        I=[T(0,0,0,LABW-200,150,PN[ph],120,132,300),T(0,0,170,LABW-200,120,PERIOD[ph],44,56,300,MU)]),'POP',80,y)
    x=LABW
    for i in range(1,len([k for k in E if k.startswith(f'POP-{ph}-')])+1):
        k=f'POP-{ph}-{i}';e=E[k]
        put(k,emspec(k,f"POP-{ph}-{i} · {PN[ph]} · {e['cap']}"),'POP',x,y+150,dict(name=f'{k} brief',l1=f"{PN[ph]} · {e['cap']}",l2='',l3='',l4=''))
        x+=round(e['w'])+GAP
    y+=ROWH
popw=x+80
secs.append(dict(key='POP',name='Sign-up pop-up · one version per sale period',x=X0,y=Y0,w=popw,h=y+100))
put('L-POP',dict(name='POP title · Sign-up pop-up',w=7600,h=1000,bg='#ECECEA',S=[['label',0,0,7600,1000,0]],
    I=[T(0,120,90,7360,520,'Sign-up pop-up',480,520,200),T(0,120,650,7360,200,'Full screen · email → phone → who do you shop for → done · copy changes on each date below',90,110,300,MU)]),'PAGE',X0,Y0-1300)
# ---------- bands
SW,DX,PAD=1000,200,80
yb=Y0+y+100+1800
def mc(f):
    ne=sum(1 for e in f['emails'] if not e.get('kind'));ns=sum(1 for e in f['emails'] if e.get('kind')=='sms')
    p=([f"{ne} email"+('s' if ne!=1 else '')] if ne else [])+([f"{ns} text"+('s' if ns!=1 else '')] if ns else [])
    return ' + '.join(p) or 'no messages, sets a profile property'
NE=sum(1 for f in Q.FLOWS for e in f['emails'] if not e.get('kind'))
SUB={'S':'S1 SMS welcome · S2 the six SMS campaigns · G1–G2 fill in Gender from orders and browsing',
     'W':f"{len(Q.FLOWS)} flows · {NE} emails + their texts · profile property Gender = “Women”, “Both” or empty",
     'M':f"{len(Q.FLOWS)} flows · {NE} emails + their texts · profile property Gender = “Men”"}
BANDTOP={}
for G,GN,FL in (('S','SMS + profile',Q.SFLOWS),('W','Women',Q.FLOWS),('M','Men',Q.FLOWS)):
    put(f'L-{G}',dict(name=f'{G} band title · {GN}',w=8000,h=1000,bg='#ECECEA',S=[['label',0,0,8000,1000,0]],
        I=[T(0,120,90,7760,520,GN,480,520,200),T(0,120,650,7760,200,SUB[G],90,110,300,MU)]),'PAGE',X0,yb-1300)
    BANDTOP[G]=yb-1200
    x=X0;bandh=0
    for f in FL:
        sk=f'{G}-{f["id"]}';tw=SW-2*PAD
        nl=lines(f['name'],96,tw);tl=lines('Trigger · '+f['trigger_short'],48,tw)
        ty=[0,300,300+nl*106+30,300+nl*106+30+tl*60+16]
        th=ty[3]+lines(f"{mc(f)} · replaces {f['replaces']}",40,tw)*52+160
        put('T-'+sk,dict(name=f"{f['id']}-{G} title · {f['name']}",w=tw,h=th,bg=None,S=[['title',0,0,tw,th,0]],
            I=[T(0,0,ty[0],tw,290,f['id'],300,290,200),T(0,0,ty[1],tw,nl*106,f['name'],96,106,300),
               T(0,0,ty[2],tw,tl*60,'Trigger · '+f['trigger_short'],48,60,400),
               T(0,0,ty[3],tw,52,f"{mc(f)} · replaces {f['replaces']}",40,52,300,MU)]),sk,PAD,PAD)
        dk='D-'+sk;de=E[dk];dy=PAD+th
        put(dk,emspec(dk,f"{f['id']}-{G} diagram · {f['name']} ({GN})"),sk,DX,dy)
        for e in f['emails']:
            if e.get('kind')=='step': continue
            k=f"{G}-{e['id']}";px,py=de['place'][k]
            nm=f"{e['id']}-{G} · SMS · {e['name']}" if e.get('kind')=='sms' else f"{e['id']}-{G} · "+re.sub(r'^subject\s*·\s*','',E[k]['subj'].strip(),flags=re.I)
            put(k,emspec(k,nm),sk,DX+px,dy+py)
        h=dy+round(de['h'])+PAD
        secs.append(dict(key=sk,name=f"{GN} · {f['id']} · {f['name']}",x=x,y=yb,w=SW,h=h))
        x+=SW+300;bandh=max(bandh,h)
    yb+=bandh+2600
SEC={s_['key']:s_ for s_ in secs}
pop=SEC['POP'];jx=X0+out['POP-post-5']['pos']['x']+310;jy=Y0+out['POP-post-5']['pos']['y']+750
gy=pop['y']+pop['h']+250
AX0=X0-1500
svgp=[];txt=[]
for i,(key,lab) in enumerate([('M-F1','Email · Men → F1, men’s versions'),('W-F1','Email · Women, Both or skipped → F1, women’s versions'),('S-S1','Phone number → S1 SMS Welcome')]):
    s_=SEC[key];gx=X0-1200+i*300;ty=s_['y']+300;tx=s_['x']-30
    pts=[(jx,pop['y']+pop['h']),(jx,gy+i*60),(gx,gy+i*60),(gx,ty),(tx,ty)]
    svgp.append('<path d="M'+' L'.join(f'{a-AX0},{b-Y0}' for a,b in pts)+'" fill="none" stroke="#A82C24" stroke-width="24" stroke-linejoin="round"/>')
    svgp.append(f'<path d="M{tx-90-AX0},{ty-60-Y0} L{tx-AX0},{ty-Y0} L{tx-90-AX0},{ty+60-Y0}" fill="none" stroke="#A82C24" stroke-width="24" stroke-linejoin="round"/>')
    txt.append(T(0,s_['x']-AX0,s_['y']-260-Y0,6000,150,lab,120,140,500,'#A82C24',ml=0))
AW=max(jx+200,max(SEC[k]['x'] for k in ('S-S1','W-F1','M-F1'))+200)-AX0
svgp.insert(0,f'<circle cx="{jx-AX0}" cy="{pop["y"]+pop["h"]-Y0}" r="40" fill="#A82C24"/>');AH=SEC['M-F1']['y']+600-Y0
svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{AW}" height="{AH}" viewBox="0 0 {AW} {AH}">'+''.join(svgp)+'</svg>'
put('A-POP',dict(name='A-POP arrows · pop-up to flows',w=AW,h=AH,bg=None,S=[['arrows',0,0,AW,AH,0]],I=[['v',0,0,0,AW,AH,svg,1]]+txt,back=1),'PAGE',AX0,Y0)
for k,v in out.items():
    if k[:2] in ('D-','T-'): v['spec']['back']=1
json.dump(dict(emails=out,sections=secs),open(f'{D}/compiled.json','w'))
print(len(out),'frames',len(secs),'sections',max(len(json.dumps(v['spec'])) for v in out.values()))
