"""Q4 flows -> Figma (page 'Email Flows' 359:2). Usage:
  python3 sync_q4.py build <workdir>            extract + compile + write q4batchNN.js for emails changed since the last push
  python3 sync_q4.py commit <workdir> <res.json> record frame ids + hashes in ../q4/sync_state.json (figma part)
Section ids live in sync_state.json too; a missing section is created by batch 00."""
import json,sys,os,subprocess,hashlib
HERE=os.path.dirname(os.path.abspath(__file__));ST=os.path.join(HERE,'..','q4','sync_state.json')
def H(o): return hashlib.sha1(json.dumps(o,sort_keys=True).encode()).hexdigest()[:16]
def spec_js(s):
    head=json.dumps({k:v for k,v in s.items() if k!='I'},separators=(',',':'))[:-1]
    return head+',"I":[\n'+',\n'.join(json.dumps(it,separators=(',',':')) for it in s['I'])+'\n]}'
st=json.load(open(ST)) if os.path.exists(ST) else {}
fg=st.setdefault('figma',{'file':'e0aqnfx3SvHowbEDDyMNMW','page':'359:2','sections':{},'emails':{}})
cmd,D=sys.argv[1],os.path.join(HERE,sys.argv[2])
if cmd=='commit':
    res=json.load(open(sys.argv[3]));C=json.load(open(f'{D}/compiled.json'))['emails']
    fg['sections'].update(res.get('sections',{}))
    for i,v in res.get('emails',{}).items():
        fg['emails'][i]=dict(em=v['em'],br=v.get('br'),hash=H([C[i]['spec'],C[i]['brief']]))
    json.dump(st,open(ST,'w'),indent=1);print('sync_state: figma',len(fg['emails']),'emails',len(fg['sections']),'sections');sys.exit()
env={**os.environ,'NODE_PATH':subprocess.run(['npm','root','-g'],capture_output=True,text=True).stdout.strip()}
subprocess.run(['node',f'{HERE}/extract_q4.js',os.path.join(HERE,'..','q4','cavaier-q4-flows.html'),D],check=True,env=env)
imgs=json.load(open(f'{D}/images.json'));hashes=json.load(open(f'{HERE}/hashes.json'))
missing=[k for k in imgs if k not in hashes]
if missing: json.dump(missing,open(f'{D}/missing_images.json','w'));print('NEW IMAGES TO UPLOAD FIRST:',missing);sys.exit(2)
subprocess.run(['python3',f'{HERE}/compile_q4.py',D],check=True,cwd=HERE)
CC=json.load(open(f'{D}/compiled.json'));C=CC['emails']
changed=[i for i in C if i not in fg['emails'] or fg['emails'][i]['hash']!=H([C[i]['spec'],C[i]['brief']])]
ONLY=set(filter(None,os.environ.get('ONLY','').split(',')))
if ONLY: changed=[i for i in changed if i in ONLY]
import re
if os.environ.get('ONLYRE'): changed=[i for i in changed if re.match(os.environ['ONLYRE'],i)]
removed=[i for i in fg['emails'] if i not in C]
print('changed',len(changed),changed[:12],'removed',removed)
b=open(f'{HERE}/builder_q4.js').read()
secjs=("\nconst SEC={};\nawait figma.loadFontAsync({family:'Figtree',style:'Regular'});\n"
 "async function sec(k,name,x,y,w,h,old){let s=old?await figma.getNodeByIdAsync(old):null;if(!s){s=page.findOne(n=>n.type==='SECTION'&&n.name===name)}"
 "if(!s){s=figma.createSection();page.appendChild(s)}s.x=x;s.y=y;s.resizeWithoutConstraints(w,h);s.name=name;SEC[k]=s;return s}\nSEC.PAGE=page;\n")
for s_ in CC['sections']:
    secjs+=f"await sec({json.dumps(s_['key'])},{json.dumps(s_['name'])},{s_['x']},{s_['y']},{s_['w']},{s_['h']},{json.dumps(fg['sections'].get(s_['key']))});\n"
rm=''.join(f"{{for(const k of {json.dumps([fg['emails'][i]['em'],fg['emails'][i].get('br')])}){{const a=k&&await figma.getNodeByIdAsync(k);if(a)a.remove()}}}}\n" for i in removed)
# frames that did not change: put them where the layout says (section + position), drop briefs the layout no longer has
mv=[[fg['emails'][i]['em'],C[i]['sec'],C[i]['pos']['x'],C[i]['pos']['y'],fg['emails'][i].get('br') if not C[i]['brief'] else None] for i in C if i in fg['emails'] and i not in changed]
rm+=('const MV='+json.dumps(mv)+';for(const [id,sk,x,y,br] of MV){const n=await figma.getNodeByIdAsync(id);if(n){if(n.parent!==SEC[sk])SEC[sk].appendChild(n);n.x=x;n.y=y}if(br){const a=await figma.getNodeByIdAsync(br);if(a)a.remove()}}\n') if mv else ''
batches=[];cur=[];base=len(b)+len(secjs)+300;size=base+len(rm)
order=sorted(changed,key=lambda i:(i.split('-')[0]!='POP',list(C).index(i)))
for i in order:
    s=len(spec_js(C[i]['spec']))+700
    if size+s>int(os.environ.get("QMAX","47000")) and cur: batches.append(cur);cur=[];size=base
    cur.append(i);size+=s
batches.append(cur)
for f in [x for x in os.listdir(HERE) if x.startswith('q4batch')]: os.remove(f'{HERE}/{f}')
for n,bt in enumerate(batches):
    code=b+secjs+'const R={emails:{},sections:{}};for(const k in SEC)if(k!=="PAGE")R.sections[k]=SEC[k].id;\n'+(rm if n==0 else '')
    for i in bt:
        e=C[i];p=e['pos'];o=fg['emails'].get(i,{})
        brj=(f"const br=await brief({json.dumps(e['brief'],separators=(',',':'))},{p['x']},{p['by']},{json.dumps(o.get('br'))},P);" if e['brief'] else 'const br=null;')
        code+=(f"{{const P=SEC[{json.dumps(e['sec'])}];const em=await build({spec_js(e['spec'])},{p['x']},{p['y']},{json.dumps(o.get('em'))},P);\n"
               f"{brj}R.emails[{json.dumps(i)}]={{em:em.id,br:br&&br.id}};}}\n")
    code+='return R;'
    if bt or rm or n==0: open(f'{HERE}/q4batch{n:02d}.js','w').write(code)
print('batches',[len(x) for x in batches])
