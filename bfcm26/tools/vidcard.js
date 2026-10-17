// node vidcard.js in.dc.html outdir spec.json
// Animated card video layers: the photo becomes a Seedance clip in its fixed box, the other elements appear on a schedule.
// spec: {photoAlt, total, fps, steps:[{alt|text|css, up, t, pop}]}  (elements not in steps are visible from 0)
// Writes: photo.png (2x crop of the photo box, Seedance first frame), box.json, mask.png, a/f####.png (page, photo hidden), top/f####.png (elements drawn over the photo)
const fs=require('fs');const {chromium}=require('playwright');
const [src,out,specF]=process.argv.slice(2);const spec=JSON.parse(fs.readFileSync(specF));const fps=spec.fps||15;
fs.mkdirSync(out+'/a',{recursive:true});fs.mkdirSync(out+'/top',{recursive:true});
const map=JSON.parse(fs.readFileSync(process.env.S+'/tools/blobmap.json'));
let h=fs.readFileSync(src,'utf8').replace('<script src="./support.js"></script>','').replace(/<\/?x-dc>|<\/?helmet>/g,'').replace(/<div data-tag="status"[\s\S]*?<\/div>/g,'').replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>map[id]?'file://'+map[id]:m);
const tmp=out+'/page.html';fs.writeFileSync(tmp,h);
const setup=`window.__find=(s)=>{const root=document.body.querySelector('div');let e=null;
 if(s.css)e=root.querySelector(s.css);else if(s.alt)e=[...root.querySelectorAll('img')].find(i=>(i.alt||'').includes(s.alt));
 else{e=[...root.querySelectorAll('*')].filter(x=>x.textContent.includes(s.text)).pop();}
 for(let i=0;i<(s.up||0);i++)e=e.parentElement;return e;};`;
(async()=>{const b=await chromium.launch();
const open=async(scale)=>{const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:scale});await p.goto('file://'+tmp);await p.addScriptTag({content:setup});await p.waitForTimeout(1200);return p;};
// photo crop + box
let p=await open(2);const img=await p.evaluateHandle((a)=>__find({alt:a}),spec.photoAlt);
const box=await img.evaluate(e=>{const r=e.getBoundingClientRect();return {x:Math.round(r.left),y:Math.round(r.top),w:Math.round(r.width),h:Math.round(r.height)};});
await img.screenshot({path:out+'/photo.png'});fs.writeFileSync(out+'/box.json',JSON.stringify(box));await p.close();
// mask: only the photo, painted white, clipped by its own radius and its parents' overflow
p=await open(1);await p.evaluate((a)=>{const root=document.body.querySelector('div');const im=__find({alt:a});
 document.documentElement.style.background=document.body.style.background='transparent';
 root.querySelectorAll('*').forEach(e=>e.style.visibility='hidden');root.style.background='transparent';
 im.style.visibility='visible';im.style.background='#fff';im.src='data:image/svg+xml,'+encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><rect width="10" height="10" fill="#fff"/></svg>');},spec.photoAlt);
await p.screenshot({path:out+'/mask.png',omitBackground:true});await p.close();
// frames
p=await open(1);
const info=await p.evaluate(({steps,a})=>{const im=__find({alt:a});im.style.visibility='hidden';
 // elements drawn over the photo: later siblings of the photo inside the same box
 const top=[];let s=im.nextElementSibling;while(s){top.push(s);s=s.nextElementSibling;}
 top.forEach((e,i)=>e.dataset.top=i);
 window.__steps=steps.map(st=>{const e=__find(st);return {e,t:st.t,pop:st.pop};});
 return {top:top.length};},{steps:spec.steps,a:spec.photoAlt});
const total=Math.round(spec.total*fps);
for(const layer of ['a','top']){if(layer==='top'&&!info.top)break;
 await p.evaluate((layer)=>{const root=document.body.querySelector('div');
  if(layer==='top'){document.documentElement.style.background=document.body.style.background='transparent';
   root.querySelectorAll('*').forEach(e=>{e.style.visibility='hidden';});root.style.background='transparent';
   root.querySelectorAll('[data-top]').forEach(e=>{e.style.visibility='visible';e.querySelectorAll('*').forEach(c=>c.style.visibility='visible');});
   [...root.querySelectorAll('[data-top]')].forEach(e=>{let q=e.parentElement;while(q&&q!==root){q.style.background='transparent';q=q.parentElement;}});}
  else{root.querySelectorAll('[data-top]').forEach(e=>e.style.opacity=0);}},layer);
 for(let i=0;i<total;i++){const t=i/fps;
  await p.evaluate(({t,layer})=>{for(const s of __steps){if(layer==='a'&&s.e.dataset.top!==undefined)continue;const k=Math.max(0,Math.min(1,(t-s.t)/0.28));const ease=1-Math.pow(1-k,3);
   s.e.style.opacity=ease;s.e.style.transform=s.pop?`scale(${0.6+0.4*ease}) rotate(${(1-ease)*-8}deg)`:`translateY(${(1-ease)*14}px)`;}},{t,layer});
  await p.screenshot({path:`${out}/${layer}/f${String(i).padStart(4,'0')}.png`,omitBackground:layer==='top'});}}
await b.close();console.log(JSON.stringify({box,top:info.top,frames:total}));})();
