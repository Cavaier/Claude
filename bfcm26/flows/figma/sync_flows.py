"""Flows page -> Figma sync (page "BFCM Flows (synced)" 359:2). Usage: python3 sync.py <artifact.html> <workdir-name>
Extracts every email version, compares with manifest.json, writes syncbatchNN.js
files that rebuild only changed emails (removing the old frames) and move the rest
if row heights changed. After running the batches, call: python3 sync.py --commit <workdir> <results.json>"""
import json,sys,os,subprocess,hashlib
HERE=os.path.dirname(os.path.abspath(__file__))
def H(o): return hashlib.sha1(json.dumps(o,sort_keys=True).encode()).hexdigest()[:16]
def spec_js(s):
    head=json.dumps({k:v for k,v in s.items() if k!='I'},separators=(',',':'))[:-1]
    return head+',"I":[\n'+',\n'.join(json.dumps(it,separators=(',',':')) for it in s['I'])+'\n]}'
if sys.argv[1]=='--commit':
    D=sys.argv[2];res=json.load(open(sys.argv[3]));man=json.load(open(f'{HERE}/manifest.json'))
    C=json.load(open(f'{D}/compiled.json'))['emails']
    for i,v in res.items():
        man[i]=dict(em=v['em'],br=v['br'],hash=H([C[i]['spec'],C[i]['brief']]),pos=C[i]['pos'],spec=C[i]['spec'])  # spec = what is in the Figma frame now
    for i in C:  # positions of moved ones
        if i in man: man[i]['pos']=C[i]['pos']
    json.dump(man,open(f'{HERE}/manifest.json','w'),indent=0);print('manifest updated',len(man));sys.exit()
html,D=sys.argv[1],sys.argv[2]
subprocess.run(['node',f'{HERE}/extract_flows.js',html,f'{HERE}/{D}'],check=True,env={**os.environ,'NODE_PATH':subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()})
# new images need uploading first
imgs=json.load(open(f'{HERE}/{D}/images.json'));hashes=json.load(open(f'{HERE}/hashes.json'))
missing=[k for k in imgs if k not in hashes]
if missing:
    json.dump(missing,open(f'{HERE}/{D}/missing_images.json','w'));print('NEW IMAGES TO UPLOAD FIRST:',missing);sys.exit(2)
subprocess.run(['python3',f'{HERE}/compile_flows.py',f'{HERE}/{D}'],check=True,cwd=HERE)
C=json.load(open(f'{HERE}/{D}/compiled.json'))['emails'];man=json.load(open(f'{HERE}/manifest.json'))
changed=[i for i in C if i not in man or man[i]['hash']!=H([C[i]['spec'],C[i]['brief']])]
SKIP=set(filter(None,os.environ.get('SKIP','').split(',')))  # frames edited in Figma beyond text: leave alone
changed=[i for i in changed if i not in SKIP]
json.dump(changed,open(f'{HERE}/{D}/changed.json','w'))
removed=[i for i in man if i not in C]
moved=[]  # never move frames: people arrange them by hand in Figma
print('changed',changed,'removed',removed,'moved',len(moved))
b=open(f'{HERE}/builder_flows.js').read()
pre='\nconst R={};\n'
mv=''.join(f"{{const a=await figma.getNodeByIdAsync('{man[i]['em']}');if(a){{a.x={C[i]['pos']['x']};a.y={C[i]['pos']['y']}}}const c=await figma.getNodeByIdAsync('{man[i]['br']}');if(c){{c.x={C[i]['pos']['x']};c.y={C[i]['pos']['by']}}}}}\n" for i in moved)
R2=json.load(open(f'{HERE}/{D}/compiled.json'))['rows']
# row labels are never moved either
rm=''.join(f"{{for(const k of ['{man[i]['em']}','{man[i]['br']}']){{const a=await figma.getNodeByIdAsync(k);if(a)a.remove()}}}}\n" for i in removed)
import difflib
J=lambda x:json.dumps(x,separators=(',',':'))
def ops(a0,b0):
    a=[J(x) for x in a0];b=[J(x) for x in b0];o=[]
    for tag,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
        if tag!='equal': o.append([i1,i2,b0[j1:j2]])
    return o
# one unit per row: first changed frame in full, the others as patches against the closest earlier one
units=[]
byrow={}
for i in sorted(changed): byrow.setdefault(i[:3],[]).append(i)
for r,ids in sorted(byrow.items()):
    code='';done=[]
    for i in ids:
        e=C[i];p=e['pos'];o=man.get(i,{});sp=e['spec']
        if not done:
            code+=f"const V_{len(done)}={spec_js(sp)};\n";expr=f"V_{len(done)}"
        else:
            best=min(done,key=lambda d:len(J(ops(C[d[0]]['spec']['I'],sp['I']))))
            hd=J({k:v for k,v in sp.items() if k!='I'})[:-1]
            code+=f"const V_{len(done)}={hd},\"I\":P(V_{best[1]}.I,{J(ops(C[best[0]]['spec']['I'],sp['I']))})}};\n"
        n=len(done)
        code+=f"{{const em=await build(V_{n},{p['x']},{p['y']},{json.dumps(o.get('em'))});\nconst br=await brief({json.dumps(e['brief'],separators=(',',':'))},{p['x']},{p['by']},{json.dumps(o.get('br'))});R[{json.dumps(i)}]={{em:em.id,br:br.id}};}}\n"
        done.append((i,n))
    units.append(('{\n'+code+'}\n',ids))
batches=[];cur='';size=len(b)
for u,ids in units:
    if size+len(u)>46000 and cur: batches.append(cur);cur='';size=len(b)
    cur+=u;size+=len(u)
batches.append(cur)
for f in [x for x in os.listdir(HERE) if x.startswith('syncbatch')]: os.remove(f'{HERE}/{f}')
for n,bt in enumerate(batches):
    code=b+pre+(mv+rm if n==0 else '')+bt+'return R;'
    if bt or mv or rm: open(f'{HERE}/syncbatch{n:02d}.js','w').write(code)
print('batches',[len(x)//1024 for x in batches],'KB')
