// node nt.js in.dc.html out.png : photo-only render (hides text, logo, buttons, shapes; keeps photo <img>s and the page background)
const fs=require('fs');const {chromium}=require('playwright');const S=process.env.S,map=JSON.parse(fs.readFileSync(S+'/tools/blobmap.json'));
const LOGOS=['b5d78a878b48e10609c923597dd1852e','e55fdf6d25b95727d07cd5804811eb0f','5881b4d35e334e5648eb69be1ec91006'];
(async()=>{let h=fs.readFileSync(process.argv[2],'utf8');
h=h.replace('<script src="./support.js"></script>','').replace(/<\/?x-dc>|<\/?helmet>/g,'').replace(/<div data-tag="status"[\s\S]*?<\/div>/g,'');
h=h.replace(/<img([^>]*?)src="\/_blob\/([0-9a-f]{32})"/g,(m,a,id)=>'<img'+a+'data-blob="'+id+'" src="/_blob/'+id+'"').replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>map[id]?'file://'+map[id]:m);
const tmp=process.argv[3]+'.nt.html';fs.writeFileSync(tmp,h);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+tmp);await p.waitForTimeout(1500);
const kept=await p.evaluate((LOGOS)=>{const root=document.body.querySelector('div');let k=0;
for(const e of root.querySelectorAll('*')){const isPhoto=e.tagName==='IMG'&&!LOGOS.includes(e.dataset.blob)&&e.alt!=='Cavaier'&&e.getBoundingClientRect().width>=150;
e.style.visibility=isPhoto?'visible':'hidden'; if(isPhoto){k++;e.style.filter=e.style.filter;}}
return k;},LOGOS);
await p.screenshot({path:process.argv[3]});await b.close();console.log(process.argv[3].split('/').pop(),kept);})();
