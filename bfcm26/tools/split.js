// node split.js in.dc.html outprefix -> outprefix_bg.png (photo layer, no text) + outprefix_ov.png (transparent text layer)
const fs=require('fs');const {chromium}=require('playwright');const S=process.env.S,map=JSON.parse(fs.readFileSync(S+'/tools/blobmap.json'));
(async()=>{let h=fs.readFileSync(process.argv[2],'utf8');
h=h.replace('<script src="./support.js"></script>','').replace(/<\/?x-dc>|<\/?helmet>/g,'').replace(/<div data-tag="status"[\s\S]*?<\/div>/g,'').replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>map[id]?'file://'+map[id]:m);
const tmp=process.argv[3]+'.html';fs.writeFileSync(tmp,h);const b=await chromium.launch();
for(const mode of ['bg','ov']){const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+tmp);await p.waitForTimeout(1200);
await p.evaluate((mode)=>{const root=document.body.querySelector('div');
const isBg=e=>e.tagName==='IMG'||(e.tagName==='DIV'&&e.children.length===0&&!e.textContent.trim()&&e.offsetWidth>=1000&&e.offsetHeight>=1800);
for(const c of root.children){const bg=isBg(c);c.style.visibility=(mode==='bg')===bg?'visible':'hidden';}
if(mode==='ov'){root.style.background='transparent';document.body.style.background='transparent';document.documentElement.style.background='transparent';}},mode);
await p.screenshot({path:process.argv[3]+'_'+mode+'.png',omitBackground:mode==='ov'});await p.close();}
await b.close();})();
