const fs=require('fs');const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:140}});
for(const [i,f] of process.argv.slice(2).entries()){let h=fs.readFileSync(f,'utf8').replace('<script src="./support.js"></script>','').replace(/<\/?x-dc>|<\/?helmet>/g,'');fs.writeFileSync('/tmp/claude-0/strip.html',h);await p.goto('file:///tmp/claude-0/strip.html');await p.waitForTimeout(800);await p.screenshot({path:process.env.S+'/renders/strip'+i+'.png'});}
await b.close();})();
