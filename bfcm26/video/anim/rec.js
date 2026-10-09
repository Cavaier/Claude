const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const tl=JSON.parse(fs.readFileSync('timeline.json'));const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.cwd()+'/anim.html');await p.waitForTimeout(1500);
const N=Math.round(tl.end*30);for(let f=0;f<N;f++){await p.evaluate(t=>setT(t),f/30);await p.screenshot({path:'frames/'+String(f).padStart(4,'0')+'.png'});}
await b.close();console.log('frames',N);})();
