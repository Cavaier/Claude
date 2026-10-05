const FOOTID='312:27';const PAGE='398:2';const FOOT=FOOTID?await figma.getNodeByIdAsync(FOOTID):null;
const page=await figma.getNodeByIdAsync(PAGE);await figma.setCurrentPageAsync(page);
const FM={Figtree:{200:'Light',300:'Light',400:'Regular',500:'Medium',600:'SemiBold',700:'Bold'},Inter:{200:'Extra Light',300:'Light',400:'Regular',500:'Medium',600:'Semi Bold',700:'Bold'},'Bodoni Moda':{400:'Regular'}};
function fname(ff,fw,it){let s=(FM[ff]||FM.Inter)[fw]||'Regular';if(ff==='Bodoni Moda')s='Regular';if(it)s=s==='Regular'?'Italic':s+' Italic';return {family:ff,style:s}}
function col(h){const n=parseInt(h.slice(1),16);const a=h.length>7?parseInt(h.slice(7,9),16)/255:1;return [{r:parseInt(h.slice(1,3),16)/255,g:parseInt(h.slice(3,5),16)/255,b:parseInt(h.slice(5,7),16)/255},a]}
function solid(h,o){const [c,a]=col(h);return {type:'SOLID',color:c,opacity:Math.max(0,Math.min(1,a*(o??1)))}}
const GT={180:[[0,1,0],[-1,0,1]],0:[[0,-1,1],[1,0,0]],90:[[1,0,0],[0,1,0]],270:[[-1,0,1],[0,-1,1]]};
async function build(E,X,Y,old){
  const fonts=new Map();for(const it of E.I)if(it[0]==='x'){const f=fname(it[7],it[8],it[9]);fonts.set(f.family+'|'+f.style,f)}
  for(const f of fonts.values())await figma.loadFontAsync(f);
  // edit the existing frame in place: find it by id, else by its code in the name (e.g. "03-A"); keep the frame, its position and parent
  let em=old?await figma.getNodeByIdAsync(old):null;
  if(!em||em.type!=='FRAME'){const code=E.name.slice(0,4);em=figma.currentPage.findOne(n=>n.type==='FRAME'&&n.name.startsWith(code+' ·'))}
  if(em){for(const c of [...em.children])c.remove();em.name=E.name}else{em=figma.createFrame();em.name=E.name;page.appendChild(em);em.x=X;em.y=Y}
  em.resize(E.w,E.h);em.fills=[solid(E.bg)];em.clipsContent=true;
  const secs=E.S.map(s=>{if(s[0]==='FOOTER'&&FOOT){const ins=FOOT.createInstance();em.appendChild(ins);ins.x=s[1];ins.y=s[2];return null}const f=figma.createFrame();f.name=s[0];em.appendChild(f);f.x=s[1];f.y=s[2];f.resize(Math.max(1,s[3]),Math.max(1,s[4]));f.fills=[];f.clipsContent=!!s[5];return f});
  for(const it of E.I){const s=E.S[it[1]];const P=secs[it[1]];const x=it[2]-s[1],y=it[3]-s[2],w=Math.max(.5,it[4]),h=Math.max(.5,it[5]);let n;
    if(it[0]==='r'){n=figma.createRectangle();n.resize(w,h);n.fills=it[6]?[solid(it[6],it[7])]:[];if(it[9]){n.strokes=[solid(it[9],it[7])];n.strokeWeight=it[10];n.strokeAlign='INSIDE';if(it[11])n.dashPattern=[4,3]}if(it[8])n.cornerRadius=it[8];n.name='bg'}
    else if(it[0]==='g'){n=figma.createRectangle();n.resize(w,h);n.fills=[{type:'GRADIENT_LINEAR',gradientTransform:GT[it[7]]||GT[180],gradientStops:it[6].map(([p,c])=>{const [cc,a]=col(c);return {position:p,color:{...cc,a}}}),opacity:it[8]??1}];if(it[9])n.cornerRadius=it[9];n.name='gradient'}
    else if(it[0]==='i'){n=figma.createRectangle();n.resize(w,h);n.fills=[{type:'IMAGE',imageHash:it[6],scaleMode:it[7],opacity:it[8]??1}];if(it[9])n.cornerRadius=it[9];if(it[10])n.blendMode='MULTIPLY';n.name='image'}
    else if(it[0]==='v'){n=figma.createNodeFromSvg(it[6]);n.resize(w,h);n.opacity=it[7]??1;n.name='icon'}
    else if(it[0]==='x'){n=figma.createText();n.fontName=fname(it[7],it[8],it[9]);n.characters=it[6];n.fontSize=it[10];n.lineHeight={unit:'PIXELS',value:it[11]};n.letterSpacing={unit:'PIXELS',value:it[12]};n.fills=[solid(it[13],it[14])];if(it[15]==='S')n.textDecoration='STRIKETHROUGH';if(it[15]==='U')n.textDecoration='UNDERLINE';
      if(it[16]){n.textAutoResize='HEIGHT';n.resize(w+2,h);n.textAlignHorizontal={left:'LEFT',center:'CENTER',right:'RIGHT',justify:'JUSTIFIED'}[it[17]]||'LEFT'}else{n.textAutoResize='WIDTH_AND_HEIGHT'}
      n.name=it[6].slice(0,40)}
    P.appendChild(n);n.x=x;n.y=y;}
  for(const s of secs)if(s)for(const c of [...s.children])if(c.type==='RECTANGLE'&&(c.height<=1.5||c.width<=1.5))s.appendChild(c);  // hairlines on top of images
  return em;
}
async function brief(B,X,Y,old){
  await figma.loadFontAsync({family:'Figtree',style:'Medium'});await figma.loadFontAsync({family:'Figtree',style:'Regular'});await figma.loadFontAsync({family:'Figtree',style:'Light'});
  let f=old?await figma.getNodeByIdAsync(old):null;
  if(!f){f=figma.currentPage.findOne(n=>n.type==='FRAME'&&n.name===B.name)}
  if(f){for(const c of [...f.children])c.remove()}else{f=figma.createAutoLayout('VERTICAL',{name:B.name,itemSpacing:6});page.appendChild(f);f.x=X;f.y=Y;f.fills=[]}
  const lines=[[B.l1,'Medium',11,0.16,true,'#6B6B68'],[B.l2,'Regular',15,0,false,'#171717'],[B.l3,'Light',13,0,false,'#3A3A38'],[B.l4,'Light',12,0,false,'#6B6B68']];
  for(const [t,st,sz,ls,up,c] of lines){if(!t)continue;const n=figma.createText();n.fontName={family:'Figtree',style:st};n.characters=up?t.toUpperCase():t;n.fontSize=sz;n.letterSpacing={unit:'PERCENT',value:ls*100};n.fills=[solid(c)];f.appendChild(n);n.layoutSizingHorizontal='FIXED';n.resize(600,n.height);n.textAutoResize='HEIGHT'}
  return f;
}
