"""Fingerprint check: Figma frames vs compiled specs. python3 verify_q4.py js > writes q4verify.js; python3 verify_q4.py cmp <result.json>"""
import json,sys,math,os
HERE=os.path.dirname(os.path.abspath(__file__))
C=json.load(open(f'{HERE}/q4w/compiled.json'))['emails'];st=json.load(open(f'{HERE}/../q4/sync_state.json'))['figma']['emails']
M=1000000007
def r(v): return math.floor(v+0.5)
def fp(spec):
    parts=[]
    for si,s in enumerate(spec['S']):
        its=[it for it in spec['I'] if it[1]==si]
        ch=[]
        for it in its:
            x=it[2]-s[1];y=it[3]-s[2];w=max(.5,it[4]);h=max(.5,it[5])
            if it[0]=='x': ch.append(('T',r(x),r(y),it[6]))
            elif it[0]=='v': ch.append(('V',r(x),r(y),''))
            else: ch.append(('R',r(x),r(y),'%d,%d'%(r(w),r(h)),w<=1.5 or h<=1.5))
        ch=[c for c in ch if not(c[0]=='R' and c[4])]+[c for c in ch if c[0]=='R' and c[4]]
        parts+= [c[:4] for c in ch]
    s=''.join(f'{a}{b},{c};{d}|' for a,b,c,d in parts)
    h=0
    for i,chr_ in enumerate(s): h=(h*31+ord(chr_))%M
    return [len(parts),h]
if sys.argv[1]=='js':
    ids={k:v['em'] for k,v in st.items()}
    js=("const ids="+json.dumps(ids)+";const M=1000000007;const out={};\n"
    "function r(v){return Math.floor(v+0.5)}\n"
    "for(const k in ids){const em=await figma.getNodeByIdAsync(ids[k]);if(!em){out[k]=null;continue}let s='';let n=0;\n"
    " for(const sec of em.children){if(!('children' in sec))continue;for(const c of sec.children){n++;\n"
    "  if(c.type==='TEXT')s+='T'+r(c.x)+','+r(c.y)+';'+c.characters+'|';else if(c.type==='RECTANGLE')s+='R'+r(c.x)+','+r(c.y)+';'+r(c.width)+','+r(c.height)+'|';else s+='V'+r(c.x)+','+r(c.y)+';|'}}\n"
    " let h=0;for(let i=0;i<s.length;i++){h=(h*31+s.charCodeAt(i))%M}out[k]=[n,h,em.parent&&em.parent.name.slice(0,12),Math.round(em.x),Math.round(em.y)]}\nreturn out;")
    open(f'{HERE}/q4verify.js','w').write(js);print(len(js))
else:
    R=json.load(open(sys.argv[2]));bad=[]
    for k,v in R.items():
        if v is None: bad.append((k,'missing'));continue
        e=fp(C[k]['spec'])
        if [v[0],v[1]]!=e: bad.append((k,v[0],e[0]))
    print(len(R),'checked;',len(bad),'mismatch',bad)
