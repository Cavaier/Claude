// node ovframes.js in.dc.html outdir voiceStart voiceDur totalDur fps : transparent text-layer frames with the waveform playing in sync
const fs=require('fs');const {chromium}=require('playwright');
const [src,out,vs,vd,td,fps]=[process.argv[2],process.argv[3],+process.argv[4],+process.argv[5],+process.argv[6],+(process.argv[7]||10)];
fs.mkdirSync(out,{recursive:true});
let h=fs.readFileSync(src,'utf8').replace('<script src="./support.js"></script>','').replace(/<\/?x-dc>|<\/?helmet>/g,'');
const map=JSON.parse(fs.readFileSync(process.env.S+'/tools/blobmap.json'));h=h.replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>map[id]?'file://'+map[id]:m);
const tmp=out+'/page.html';fs.writeFileSync(tmp,h);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+tmp);await p.waitForTimeout(1200);
await p.evaluate(()=>{const root=document.body.querySelector('div');root.style.background='transparent';document.body.style.background='transparent';document.documentElement.style.background='transparent';
for(const c of root.children){if(c.tagName==='IMG')c.style.visibility='hidden';}});
const total=Math.round(td*fps);const fmt=s=>'0:'+String(Math.floor(s)).padStart(2,'0');
for(let i=0;i<total;i++){const t=i/fps;const playing=t>=vs&&t<vs+vd;const prog=t<vs?0:Math.min(1,(t-vs)/vd);
await p.evaluate(({prog,playing,label})=>{const svg=[...document.querySelectorAll('svg')].find(s=>s.getAttribute('width')==='504');const rects=[...svg.querySelectorAll('rect')];const n=Math.round(prog*rects.length);
rects.forEach((r,j)=>r.setAttribute('fill',j<n?'#141414':'#B9B8B3'));
const icon=[...document.querySelectorAll('svg')].find(s=>s.getAttribute('width')==='34');icon.innerHTML=playing?'<rect x="6" y="5" width="8" height="28" rx="1.5"/><rect x="20" y="5" width="8" height="28" rx="1.5"/>':'<path d="M5 3 L31 19 L5 35 Z"></path>';
const sp=[...document.querySelectorAll('span')].find(s=>/^0:\d\d$/.test(s.textContent.trim()));sp.textContent=label;sp.style.fontVariantNumeric='tabular-nums';},{prog,playing,label:playing?fmt(t-vs):fmt(Math.ceil(vd))});
await p.screenshot({path:`${out}/f${String(i).padStart(4,'0')}.png`,omitBackground:true});}
await b.close();})();
