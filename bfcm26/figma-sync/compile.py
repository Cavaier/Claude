import json,sys,os
KEEPF=os.environ.get('KEEPF')=='1'
D=sys.argv[1]
E=json.load(open(f'{D}/emails.json'));H=json.load(open('hashes.json'))
def hx(c):
    if not c: return None
    a=c.get('a',1)
    s='#%02x%02x%02x'%(round(c['r']*255),round(c['g']*255),round(c['b']*255))
    return s+('%02x'%round(a*255) if a<1 else '')
def r1(v): return round(v,1)
def comp(e):
    S=[[s['n'],r1(s['x']),r1(s['y']),r1(s['w']),r1(s['h']),1 if s['clip'] else 0] for s in e['secs']]
    I=[]
    fsec=[i for i,s in enumerate(e['secs']) if s['n']=='footer']
    for i in fsec: S[i][0]='FOOTER'
    for it in e['items']:
        sec=it.get('sec',0)
        if sec in fsec and not KEEPF: continue
        if sec is None or sec<0: continue
        b=[sec,r1(it['x']),r1(it['y']),r1(it['w']),r1(it['h'])]
        o=round(it.get('o',1),3)
        if it['t']=='r': I.append(['r',*b,hx(it['f']),o,r1(it.get('cr',0)),hx(it.get('st')),it.get('sw',0),1 if it.get('dash') else 0])
        elif it['t']=='g': I.append(['g',*b,[[round(s['pos'],3),hx(s['c']) if s['c']['a']>=1 else hx(s['c'])] for s in it['g']['stops']],it['g']['ang'],o,r1(it.get('cr',0))])
        elif it['t']=='i': I.append(['i',*b,H[it['k']],it['m'],o,r1(it.get('cr',0)),1 if it.get('bl')=='multiply' else 0])
        elif it['t']=='v': I.append(['v',*b,it['svg'],o])
        elif it['t']=='x':
            ca=it['h'] if not it['ml'] else it['fs']*1.2
            # line box top
            yy=it['y']-(it['lh']-min(ca,it['h']))/2
            b[2]=r1(yy)
            I.append(['x',*b,it['s'],it['ff'],it['fw'],1 if it['it'] else 0,it['fs'],r1(it['lh']),round(it['ls'],2),hx(it['c']),o,it['dec'],it['ml'],it.get('al','left')])
    return S,I
order=['A','B','C','D','E','F','G','H','I','J']
rows={}
for e in E: rows.setdefault(e['eid'],{})[e['ver']]=e
layout={};y=0
for eid in sorted(rows):
    r=rows[eid];hmax=max(v['h'] for v in r.values())
    for i,v in enumerate(order):
        if v in r: layout[eid+v]=dict(x=320+i*680,y=y+180,by=y,rowY=y)
    layout[eid]=dict(y=y,h=hmax)
    y+=180+hmax+220
out={}
for e in E:
    S,I=comp(e)
    m=e['meta'];subj=m.get('Subject','');prev=m.get('Preview','')
    idea=m.get('The idea') or m.get('What’s new') or m.get('Note') or ''
    name=f"{e['no']}-{e['ver']} · {subj}"
    spec=dict(name=name,w=round(e['w']),h=round(e['h']),bg=hx(e['bg']) or '#ffffff',S=S,I=I)
    br=dict(name=f"{e['no']}-{e['ver']} brief",l1=f"{e['no']} · {e['date']} · {e['time']} · Version {e['ver']} · {e['tag']}",l2=f"Subject: {subj}",l3=f"Preview: {prev}",l4=idea[:260])
    out[e['id']]=dict(spec=spec,brief=br,pos=layout[e['id']])
json.dump(dict(emails=out,rows={k:v for k,v in layout.items() if len(k)==3}),open(f'{D}/compiled.json','w'))
print(len(out), max(len(json.dumps(v['spec'])) for v in out.values()))
