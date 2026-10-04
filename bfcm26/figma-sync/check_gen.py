"""Write check.js: a read-only Figma script that dumps the current contents of the given emails' frames.
Usage: python3 check_gen.py e08E e03A ...   (or: --from <workdir> to use <workdir>/changed.json)
Run check.js with use_figma, save its JSON result, then: python3 pull.py <result.json> <page.html> <out.html>"""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
man = json.load(open(f'{HERE}/manifest.json'))
ids = json.load(open(f'{HERE}/{sys.argv[2]}/changed.json')) if sys.argv[1] == '--from' else sys.argv[1:]
ids = [i for i in ids if i in man]
js = """const IDS=%s;const out={};
function hex(p){if(!p)return null;if(p.type==='IMAGE')return 'img:'+p.imageHash;if(p.type!=='SOLID')return p.type;const c=p.color,t=v=>Math.round(v*255).toString(16).padStart(2,'0');return '#'+t(c.r)+t(c.g)+t(c.b)}
const r=v=>Math.round(v*10)/10;
for(const [id,nid] of IDS){let fr=await figma.getNodeByIdAsync(nid);
  if(!fr){const pg=await figma.getNodeByIdAsync('310:2');fr=pg.findOne(n=>n.type==='FRAME'&&n.name.startsWith(id.slice(1,3)+'-'+id[3]+' ·'));if(!fr){out[id]=null;continue}}
  const S=[];
  for(const s of fr.children){if(s.type==='INSTANCE'){S.push('FOOTER');continue}
    S.push((s.children||[]).map(n=>{const f=Array.isArray(n.fills)?n.fills[0]:null;
      return n.type==='TEXT'?['x',r(n.x),r(n.y),n.characters,typeof n.fontSize==='number'?n.fontSize:'mixed',typeof n.fontName==='object'&&n.fontName.family?n.fontName.family+'/'+n.fontName.style:'mixed',hex(f)]
        :[n.type==='RECTANGLE'?'r':n.type,r(n.x),r(n.y),r(n.width),r(n.height),hex(f)]}))}
  out[id]={name:fr.name,S};}
return out;""" % json.dumps([[i, man[i]['em']] for i in ids])
open(f'{HERE}/check.js', 'w').write(js)
print('check.js for', ids, len(js), 'chars')
