const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+__dirname+'/m.html');await p.waitForTimeout(2000);
const F=24,N=F*7;for(let i=0;i<N;i++){await p.evaluate(t=>setT(t),i/F);await p.screenshot({path:__dirname+'/frames/f'+String(i).padStart(4,'0')+'.jpg',type:'jpeg',quality:92});}
await b.close();})();
