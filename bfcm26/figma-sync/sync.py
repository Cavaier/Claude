"""Page -> Figma sync. Usage: python3 sync.py <artifact.html> <workdir-name>
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
subprocess.run(['node',f'{HERE}/extract.js',html,f'{HERE}/{D}'],check=True,env={**os.environ,'NODE_PATH':subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()})
# new images need uploading first
imgs=json.load(open(f'{HERE}/{D}/images.json'));hashes=json.load(open(f'{HERE}/hashes.json'))
missing=[k for k in imgs if k not in hashes]
if missing:
    json.dump(missing,open(f'{HERE}/{D}/missing_images.json','w'));print('NEW IMAGES TO UPLOAD FIRST:',missing);sys.exit(2)
subprocess.run(['python3',f'{HERE}/compile.py',f'{HERE}/{D}'],check=True,cwd=HERE)
C=json.load(open(f'{HERE}/{D}/compiled.json'))['emails'];man=json.load(open(f'{HERE}/manifest.json'))
changed=[i for i in C if i not in man or man[i]['hash']!=H([C[i]['spec'],C[i]['brief']])]
SKIP=set(filter(None,os.environ.get('SKIP','').split(',')))  # frames edited in Figma beyond text: leave alone
changed=[i for i in changed if i not in SKIP]
json.dump(changed,open(f'{HERE}/{D}/changed.json','w'))
removed=[i for i in man if i not in C]
moved=[]  # never move frames: people arrange them by hand in Figma
print('changed',changed,'removed',removed,'moved',len(moved))
b=open(f'{HERE}/builder_f.js').read()
pre='\nconst R={};\n'
mv=''.join(f"{{const a=await figma.getNodeByIdAsync('{man[i]['em']}');if(a){{a.x={C[i]['pos']['x']};a.y={C[i]['pos']['y']}}}const c=await figma.getNodeByIdAsync('{man[i]['br']}');if(c){{c.x={C[i]['pos']['x']};c.y={C[i]['pos']['by']}}}}}\n" for i in moved)
rails=json.load(open(f'{HERE}/rails.json'));R2=json.load(open(f'{HERE}/{D}/compiled.json'))['rows']
# row labels are never moved either
rm=''.join(f"{{for(const k of ['{man[i]['em']}','{man[i]['br']}']){{const a=await figma.getNodeByIdAsync(k);if(a)a.remove()}}}}\n" for i in removed)
batches=[];cur=[];size=len(b)+len(mv)+len(rm)
for i in sorted(changed):
    s=len(spec_js(C[i]['spec']))+600
    if size+s>46000 and cur: batches.append(cur);cur=[];size=len(b)
    cur.append(i);size+=s
batches.append(cur)
for f in [x for x in os.listdir(HERE) if x.startswith('syncbatch')]: os.remove(f'{HERE}/{f}')
for n,bt in enumerate(batches):
    code=b+pre+(mv+rm if n==0 else '')
    for i in bt:
        e=C[i];p=e['pos'];o=man.get(i,{})
        code+=f"{{const em=await build({spec_js(e['spec'])},{p['x']},{p['y']},{json.dumps(o.get('em'))});\nconst br=await brief({json.dumps(e['brief'],separators=(',',':'))},{p['x']},{p['by']},{json.dumps(o.get('br'))});R[{json.dumps(i)}]={{em:em.id,br:br.id}};}}\n"
    code+='return R;'
    if bt or mv or rm: open(f'{HERE}/syncbatch{n:02d}.js','w').write(code)
print('batches',[len(x) for x in batches])
