// node boxshot.js in.dc.html out.png x y w h : 2x screenshot of one box (photo-only input for card layouts)
const fs=require('fs');const {chromium}=require('playwright');const S=process.env.S,map=JSON.parse(fs.readFileSync(S+'/tools/blobmap.json'));
(async()=>{let h=fs.readFileSync(process.argv[2],'utf8');
h=h.replace('<script src="./support.js"></script>','').replace(/<\/?x-dc>|<\/?helmet>/g,'').replace(/<div data-tag="status"[\s\S]*?<\/div>/g,'').replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>map[id]?'file://'+map[id]:m);
const tmp=process.argv[3]+'.html';fs.writeFileSync(tmp,h);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:2});await p.goto('file://'+tmp);await p.waitForTimeout(1500);
const [x,y,w,hh]=process.argv.slice(4,8).map(Number);await p.screenshot({path:process.argv[3],clip:{x,y,width:w,height:hh}});await b.close();})();
