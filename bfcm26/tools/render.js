// usage: node render.js in.dc.html out.png  (maps /_blob ids to local files)
const fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const S=process.env.S, map=JSON.parse(fs.readFileSync(S+'/tools/blobmap.json'));
(async()=>{let h=fs.readFileSync(process.argv[2],'utf8');
h=h.replace('<script src="./support.js"></script>','').replace(/<\/?x-dc>|<\/?helmet>/g,'').replace(/<div data-tag="status"[\s\S]*?<\/div>/g,'');
h=h.replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>map[id]?'file://'+map[id]:m);
const tmp=process.argv[3]+'.html';fs.writeFileSync(tmp,h);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+tmp);await p.waitForTimeout(1500);await p.screenshot({path:process.argv[3]});await b.close();})();
