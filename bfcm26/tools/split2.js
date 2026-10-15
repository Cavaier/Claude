// node split2.js in.dc.html outprefix -> outprefix_bg.png (photo layer: root bg + photo boxes + full-size bg divs, no text, no logo)
//                                       + outprefix_ov.png (transparent: text, buttons, logo, cards).
// Unlike split.js, the logo IMG and text cards never land in the bg layer, and photo boxes nested in a div count as bg.
const fs=require('fs');const {chromium}=require('playwright');const S=process.env.S,map=JSON.parse(fs.readFileSync(S+'/tools/blobmap.json'));
const LOGO='b5d78a878b48e10609c923597dd1852e';
(async()=>{let h=fs.readFileSync(process.argv[2],'utf8');
h=h.replace('<script src="./support.js"></script>','').replace(/<\/?x-dc>|<\/?helmet>/g,'').replace(/<div data-tag="status"[\s\S]*?<\/div>/g,'').replace(/\/_blob\/([0-9a-f]{32})/g,(m,id)=>map[id]?'file://'+map[id]:m);
const tmp=process.argv[3]+'.html';fs.writeFileSync(tmp,h);const b=await chromium.launch();
for(const mode of ['bg','ov']){const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+tmp);await p.waitForTimeout(1200);
await p.evaluate(([mode,LOGO])=>{const root=document.body.querySelector('div');
 const isLogo=e=>e.tagName==='IMG'&&e.src.includes(LOGO);
 const isPhoto=e=>(e.tagName==='IMG'&&!isLogo(e))||(e.tagName==='DIV'&&!e.textContent.trim()&&e.querySelector('img')&&![...e.querySelectorAll('img')].some(isLogo));
 const isBgDiv=e=>e.tagName==='DIV'&&e.children.length===0&&!e.textContent.trim()&&e.offsetWidth>=1000&&e.offsetHeight>=1800;
 for(const c of root.children){const bg=isPhoto(c)||isBgDiv(c);c.style.visibility=(mode==='bg')===bg?'visible':'hidden';}
 if(mode==='ov'){root.style.background='transparent';document.body.style.background='transparent';document.documentElement.style.background='transparent';}},[mode,LOGO]);
await p.screenshot({path:process.argv[3]+'_'+mode+'.png',omitBackground:mode==='ov'});await p.close();}
await b.close();})();
