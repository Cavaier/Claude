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
PERIOD={'pre':'Oct 27 – Nov 22','ea':'Nov 23 – 26 · publish Nov 23, 09:00','bf':'Nov 27 – Dec 6 · Black Friday + Cyber Week · publish Nov 27, 08:00',
        'xmas':'Dec 7 – Christmas cut-off · publish Dec 7','late':'Cut-off – Dec 24 · publish on the cut-off day','post':'Dec 26 → · publish Dec 26'}
LABW,GAP,ROWH=1500,120,844+420
y=200
for ph in ['pre','ea','bf','xmas','late','post']:
    put(f'L-POP-{ph}',dict(name=f'{PN[ph]} · pop-up label',w=LABW-200,h=600,bg=None,S=[['label',0,0,LABW-200,600,0]],
        I=[T(0,0,0,LABW-200,150,PN[ph],120,132,300),T(0,0,170,LABW-200,120,PERIOD[ph],44,56,300,MU)]),'POP',80,y)
    x=LABW
    for i in range(1,8):
        k=f'POP-{ph}-{i}';e=E[k]
        put(k,emspec(k,f"POP-{ph}-{i} · {PN[ph]} · {e['cap']}"),'POP',x,y+150,dict(name=f'{k} brief',l1=f"{PN[ph]} · {e['cap']}",l2='',l3='',l4=''))
        x+=round(e['w'])+GAP
    y+=ROWH
popw=x+80
secs.append(dict(key='POP',name='Sign-up pop-up · one version per sale period',x=X0,y=Y0,w=popw,h=y+100))
put('L-POP',dict(name='Sign-up pop-up · title',w=6000,h=900,bg=None,S=[['label',0,0,6000,900,0]],
    I=[T(0,0,0,6000,520,'Sign-up pop-up',480,520,200),T(0,0,560,6000,200,'Full screen · email → who do you shop for → done · copy changes on each date below',90,110,300,MU)]),'PAGE',X0,Y0-1200)
# ---------- bands
SW,DX,PAD=1000,200,80
yb=Y0+y+100+1800
for G,GN in (('W','Women'),('M','Men')):
    put(f'L-{G}',dict(name=f'{GN} · title',w=8000,h=900,bg=None,S=[['label',0,0,8000,900,0]],
        I=[T(0,0,0,8000,520,GN,480,520,200),T(0,0,560,8000,200,f"{len(Q.FLOWS)} flows · {sum(len(f['emails']) for f in Q.FLOWS)} emails · profile property Gender = "+('“Men”' if G=='M' else '“Women”, “Both” or empty'),90,110,300,MU)]),'PAGE',X0,yb-1200)
    x=X0;bandh=0
    for f in Q.FLOWS:
        sk=f'{G}-{f["id"]}';tw=SW-2*PAD
        nl=lines(f['name'],96,tw);tl=lines('Trigger · '+f['trigger_short'],48,tw)
        ty=[0,300,300+nl*106+30,300+nl*106+30+tl*60+16]
        th=ty[3]+lines(f"{len(f['emails'])} emails · replaces {f['replaces']}",40,tw)*52+160
        put('T-'+sk,dict(name=f"{f['id']} · title",w=tw,h=th,bg=None,S=[['title',0,0,tw,th,0]],
            I=[T(0,0,ty[0],tw,290,f['id'],300,290,200),T(0,0,ty[1],tw,nl*106,f['name'],96,106,300),
               T(0,0,ty[2],tw,tl*60,'Trigger · '+f['trigger_short'],48,60,400),
               T(0,0,ty[3],tw,52,f"{len(f['emails'])} email{'s' if len(f['emails'])!=1 else ''} · replaces {f['replaces']}",40,52,300,MU)]),sk,PAD,PAD)
        dk='D-'+sk;de=E[dk];dy=PAD+th
        put(dk,emspec(dk,f"{f['id']} · flow diagram ({GN})"),sk,DX,dy)
        for e in f['emails']:
            k=f"{G}-{e['id']}";px,py=de['place'][k]
            put(k,emspec(k,f"{e['id']}-{G} · "+re.sub(r'^subject\s*·\s*','',E[k]['subj'].strip(),flags=re.I)),sk,DX+px,dy+py)
        h=dy+round(de['h'])+PAD
        secs.append(dict(key=sk,name=f"{GN} · {f['id']} · {f['name']}",x=x,y=yb,w=SW,h=h))
        x+=SW+300;bandh=max(bandh,h)
    yb+=bandh+2600
for k,v in out.items():
    if k[:2] in ('D-','T-'): v['spec']['back']=1
json.dump(dict(emails=out,sections=secs),open(f'{D}/compiled.json','w'))
print(len(out),'frames',len(secs),'sections',max(len(json.dumps(v['spec'])) for v in out.values()))
