"""Q4 flows page -> Figma specs. Usage: python3 compile_q4.py <workdir>  (after extract_q4.js)
Layout on page 'Email Flows' (359:2), right of the old flows master: pop-up section on top,
then a Women band and a Men band, one Figma section per flow, emails stacked under each other."""
import json,sys,os,re
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','q4'))
os.environ['KEEPF']='1'
import types
C0=types.SimpleNamespace();_src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'compile.py')).read()
_g={'__name__':'c0'};exec(_src[:_src.index('order=')],_g)  # reuse comp()/hx() from compile.py
C0.comp=_g['comp'];C0.hx=_g['hx']
import q4_specs as Q
D=sys.argv[1]
E={e['id']:e for e in json.load(open(f'{D}/emails.json'))}
PN={'pre':'Pre-sale','ea':'Early access','bf':'Black Friday','cw':'Cyber Week','xmas':'Christmas','late':'Last minute','post':'After Christmas'}
def ph(v,p):
    if not isinstance(v,dict): return v
    for k,x in v.items():
        if p in k.split(): return x
    return next(iter(v.values()))
def clean(s): return re.sub(r'«\w+»','',re.sub(r'<[^>]+>','',str(s or ''))).strip()
X0,Y0=6000,0;COLW=600;GAP=220;PAD=80;BRH=150;EGAP=140
out={};secs=[]
# pop-up
y=Y0;px=X0+PAD;row_h=0;pops=[e for e in E.values() if e['g']=='P']
for i,e in enumerate(sorted(pops,key=lambda e:int(e['id'].split('-')[1]))):
    if i==3: px=X0+PAD;y+=BRH+row_h+EGAP;row_h=0
    out[e['id']]=dict(pos=dict(x=px-X0,y=y-Y0+BRH,by=y-Y0),sec='POP',
        spec_name=f"POP-{e['id'][4:]} · Sign-up pop-up · {e['cap']}",brief=dict(name=f"{e['id']} brief",l1=f"Sign-up pop-up · {e['cap']}",l2='',l3='',l4=''))
    px+=round(e['w'])+GAP;row_h=max(row_h,e['h'])
popw=max(o['pos']['x']+round(E[k]['w']) for k,o in out.items())+PAD
secs.append(dict(key='POP',name='Sign-up pop-up',x=X0,y=Y0-PAD,w=popw,h=y-Y0+BRH+row_h+2*PAD))
yb=Y0+secs[0]['h']+600
for G,GN in (('W','Women'),('M','Men')):
    x=X0;band_h=0
    for f in Q.FLOWS:
        yy=PAD
        for e in f['emails']:
            k=f"{G}-{e['id']}";x_=E[k];p0=e['phases'][0]
            subj=clean(ph(e['subject'],p0));prev=clean(ph(e['preview'],p0))
            out[k]=dict(pos=dict(x=PAD,y=yy+BRH,by=yy),sec=f"{G}-{f['id']}",
                spec_name=f"{e['id']}-{G} · {subj}",
                brief=dict(name=f"{e['id']}-{G} brief",l1=f"{e['id']} · {e['name']} · {GN} · {e['delay']} · shown: {PN[p0]}",
                           l2=f"Subject: {subj}",l3=f"Preview: {prev}",l4=clean(e['goal'])[:260]))
            yy+=BRH+x_['h']+EGAP
        h=yy+PAD;secs.append(dict(key=f"{G}-{f['id']}",name=f"{GN} · {f['id']} · {f['name']}",x=x,y=yb,w=COLW+2*PAD,h=h))
        x+=COLW+2*PAD+200;band_h=max(band_h,h)
    yb+=band_h+800
emails={}
for k,o in out.items():
    S,I=C0.comp(E[k]);e=E[k]
    emails[k]=dict(spec=dict(name=o['spec_name'],w=round(e['w']),h=round(e['h']),bg=C0.hx(e['bg']) or '#ffffff',S=S,I=I),brief=o['brief'],pos=o['pos'],sec=o['sec'])
json.dump(dict(emails=emails,sections=secs),open(f'{D}/compiled.json','w'))
print(len(emails),'emails',len(secs),'sections',max(len(json.dumps(v['spec'])) for v in emails.values()))
