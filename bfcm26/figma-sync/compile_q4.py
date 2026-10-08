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
PERIOD={'pre':'Oct 27 – Nov 10','ea':'Nov 11 – 12 · code BF26 · publish Nov 11, 09:00','bf':'Nov 13 – Dec 6 · Black Friday + Cyber Week · publish Nov 13, 08:00',
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
BANDTOP={};BANDY={}
for G,GN,FL in (('S','SMS + profile',Q.SFLOWS),('W','Women',Q.FLOWS),('M','Men',Q.FLOWS)):
    put(f'L-{G}',dict(name=f'{G} band title · {GN}',w=8000,h=1000,bg='#ECECEA',S=[['label',0,0,8000,1000,0]],
        I=[T(0,120,90,7760,520,GN,480,520,200),T(0,120,650,7760,200,SUB[G],90,110,300,MU)]),'PAGE',X0,yb-1300)
    BANDTOP[G]=yb-1200;BANDY[G]=yb
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
# ---------- by period: next to each gender band, one section per flow, a row per email and a column per sale period
PHS=['pre','ea','bf','cw','xmas','late','post']
PDATE={'pre':'Oct 27 – Nov 10','ea':'Nov 11 – 12 · code BF26','bf':'Nov 13 – 30 · shown: Nov 14 – 26','cw':'Dec 1 – 6',
       'xmas':'Dec 7 – [cut-off]','late':'[Cut-off] – Dec 24','post':'Dec 26 – Jan 10'}
COLW,CG,LW=600,220,1000
GW=LW+len(PHS)*(COLW+CG)+PAD;LIM=16000;VG=1800  # VG: room for the section name between stacked sections
px0=max(s_['x']+s_['w'] for s_ in secs)+1500;pbottom=0
for G,GN in (('W','Women'),('M','Men')):
    top=max(BANDY[G],pbottom+3200);cx,cy=px0,top;maxx=cx
    put(f'L-P{G}',dict(name=f'P{G} title · {GN} · every period',w=GW,h=1000,bg='#ECECEA',S=[['label',0,0,GW,1000,0]],
        I=[T(0,120,90,GW-240,520,f'{GN} · every period',480,520,200),
           T(0,120,650,GW-240,200,'Each email once per sale period it sends in. Copy that changes by the day is in the Day lines table next to the pop-up.',90,110,300,MU)]),'PAGE',px0,top-1300)
    for f in Q.FLOWS:
        rows=[]
        for e in f['emails']:
            if e.get('kind'): continue
            grp={}
            for ph in PHS:
                k=f'PV-{G}-{e["id"]}-{ph}'
                if k not in E: continue
                sp=emspec(k,'');sg=json.dumps([sp['S'],sp['I'],sp['h'],sp['bg']])
                grp.setdefault(sg,[]).append(ph)
            if grp: rows.append((e,list(grp.values())))
        hh=PAD+620;h=hh+sum(max(round(E[f'PV-{G}-{e["id"]}-{g[0]}']['h']) for g in gs)+420 for e,gs in rows)+PAD
        if cy>top and cy+h>top+LIM: cx+=GW+800;cy=top
        sk=f'P{G}-{f["id"]}'
        secs.append(dict(key=sk,name=f"{GN} · {f['id']} · {f['name']} · every period",x=cx,y=cy,w=GW,h=h))
        put('PT-'+sk,dict(name=f"{sk} title · {f['name']}",w=GW-2*PAD,h=360,bg=None,S=[['title',0,0,GW-2*PAD,360,0]],
            I=[T(0,0,0,GW-2*PAD,130,f"{f['id']} · {f['name']}",110,130,300),T(0,0,160,GW-2*PAD,60,'Trigger · '+f['trigger_short'],48,60,400),
               T(0,0,240,GW-2*PAD,52,'One row per email · one column per sale period · a frame covers every period named above it',40,52,300,MU)]),sk,PAD,PAD)
        put('PH-'+sk,dict(name=f"{sk} periods",w=len(PHS)*(COLW+CG),h=170,bg=None,S=[['periods',0,0,len(PHS)*(COLW+CG),170,0]],
            I=[it for i,ph in enumerate(PHS) for it in (T(0,i*(COLW+CG),0,COLW,70,PN[ph],56,70,500),T(0,i*(COLW+CG),84,COLW,44,PDATE[ph],34,44,300,MU))]),sk,LW,PAD+440)
        ry=hh
        for e,gs in rows:
            rh=max(round(E[f'PV-{G}-{e["id"]}-{g[0]}']['h']) for g in gs)
            put(f'PL-{G}-{e["id"]}',dict(name=f"PL-{G}-{e['id']} · row label",w=LW-PAD-120,h=420,bg=None,S=[['label',0,0,LW-PAD-120,420,0]],
                I=[T(0,0,0,LW-PAD-120,110,e['id'],96,110,300),T(0,0,130,LW-PAD-120,120,e['name'],44,56,400),T(0,0,270,LW-PAD-120,100,e['delay'],34,44,300,MU)]),sk,PAD,ry+150)
            for g in gs:
                k=f'PV-{G}-{e["id"]}-{g[0]}';subj=re.sub(r'^subject\s*·\s*','',E[k]['subj'].strip(),flags=re.I)
                lab=' + '.join(PN[x] for x in g)
                put(k,emspec(k,f"{e['id']}-{G}-{g[0]} · {lab} · {subj}"),sk,LW+PHS.index(g[0])*(COLW+CG),ry+150,
                    dict(name=f'{k} brief',l1=lab,l2=subj,l3='',l4=''))
            ry+=rh+420
        pbottom=max(pbottom,cy+h);cy+=h+VG;maxx=max(maxx,cx+GW)
# ---------- day lines: the «token» copy for every sale day
DCOL=[('Day','label',420),('Period','phase',380),('Kicker','kick',620),('Big word','big',330),('Headline','head',820),('Line','line',1500),('Subject','subj',700),('Preview','prev',760),('Button','cta',560)]
DW=sum(c[2]+60 for c in DCOL)+240;dI=[T(0,120,90,DW-240,200,'Day lines · what changes each day',150,180,200),
    T(0,120,300,DW-240,60,'Every «token» in the emails is filled from the row for the day the email sends; a range row covers each day in it.',44,60,300,MU)]
xx=120
for nm,_,w in DCOL: dI.append(T(0,xx,460,w,50,nm.upper(),30,50,500,MU));xx+=w+60
yy=540
for d in Q.DAYS:
    if d['phase'] in ('pre','post'): continue
    vals={**{k:d[k] for k in Q.KEYS},'label':d['label'],'phase':PN[d['phase']]};xx=120;rh=0
    for nm,key,w in DCOL:
        v=str(vals.get(key,'') or '—');n=lines(v,34,w);dI.append(['x',0,xx,yy,w,n*46,v,'Figtree',500 if key=='label' else 300,0,34,46,0,FG,1,'',1,'left']);xx+=w+60;rh=max(rh,n*46)
    dI.append(['r',0,120,yy+rh+22,DW-240,1,'#DCDCDA',1,0,None,0,0]);yy+=rh+46
DH=yy+120
popsec=next(s_ for s_ in secs if s_['key']=='POP')
secs.append(dict(key='DAYS',name='Day lines · what changes each day',x=popsec['x']+popsec['w']+800,y=Y0,w=DW+200,h=DH+200))
put('DAYTAB',dict(name='DAYTAB · day lines',w=DW,h=DH,bg='#FFFFFF',S=[['table',0,0,DW,DH,0]],I=dI),'DAYS',100,100)
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
