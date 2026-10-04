const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});const p=await b.newPage({viewport:{width:900,height:1000}});
const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/cavaier-bfcm26-sequence.html');await p.waitForTimeout(2500);
await p.addStyleTag({content:'.bar2{display:none!important}'});
for(const id of ['e01','e02','e03','e04','e05','e06','e08','e10','e12','e13']){const el=await p.$(`#${id} .em`);await el.screenshot({path:`v3_${id}.png`});}
console.log('errors',errs);await b.close();})();
