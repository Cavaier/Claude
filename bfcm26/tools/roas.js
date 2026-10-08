// ROAS pass: per text element -> bbox, font size, contrast vs pixels behind it, safe-zone check.
const fs=require('fs');const {chromium}=require('playwright');
const S=process.env.S,map=JSON.parse(fs.readFileSync(S+'/tools/blobmap.json'));
function lum(r,g,b){const f=c=>{c/=255;return c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4)};return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)}
(async()=>{const out=[];const b=await chromium.launch();
for(const file of process.argv.slice(2)){let h=fs.readFileSync(file,'utf8');
h=h.replace('<script src="./support.js"></script>','').replace(/<\/?x-dc>|<\/?helmet>/g,'').replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>map[id]?'file://'+map[id]:m);
const tmp=S+'/renders/_roas.html';fs.writeFileSync(tmp,h);const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+tmp);await p.waitForTimeout(1200);
const els=await p.evaluate(()=>{const r=[];document.querySelectorAll('h1,p,span,a,figcaption').forEach((e,i)=>{const own=[...e.childNodes].some(n=>n.nodeType==3&&n.textContent.trim());if(!own)return;const bb=e.getBoundingClientRect();const cs=getComputedStyle(e);e.setAttribute('data-roas',i);r.push({i,text:e.innerText.replace(/\s+/g,' ').slice(0,50),x:bb.x,y:bb.y,w:bb.width,h:bb.height,fs:parseFloat(cs.fontSize),color:cs.color,bg:cs.backgroundColor})});return r});
// hide all text, screenshot backdrop
await p.addStyleTag({content:'*{color:transparent!important;text-shadow:none!important}'});
const shot=S+'/renders/_bd_'+file.split('/').pop()+'.png';await p.screenshot({path:shot});out.push({file:file.split('/').pop(),shot,els});await p.close();}
await b.close();fs.writeFileSync(S+'/renders/_roas.json',JSON.stringify(out));})();
