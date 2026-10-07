// Usage: node extract.js <html> <outdir>
const { chromium } = require('playwright');
const fs=require('fs'),crypto=require('crypto');
(async()=>{
const [,,html,out]=process.argv;fs.mkdirSync(out+'/img',{recursive:true});
const b=await chromium.launch({proxy:{server:process.env.HTTPS_PROXY||'http://127.0.0.1:44451'},args:['--ignore-certificate-errors']});
const p=await b.newPage({viewport:{width:1600,height:1000}});
await p.goto('file://'+html,{waitUntil:'load'});
await p.evaluate(()=>document.fonts.ready);
await p.addStyleTag({content:'.board{transform:none!important}.vtrack{display:flex!important;flex-direction:column!important;overflow:visible!important}.vtrack>.main{width:600px!important;flex:none}.vtrack>[hidden]{display:flex!important}html{scroll-behavior:auto!important}.live,.lvpanel,.bar2{position:static!important}'});
await p.waitForTimeout(800);
const data=await p.evaluate(()=>{
  const px=v=>parseFloat(v)||0;
  function rgba(c){const m=c&&c.match(/rgba?\(([^)]+)\)/);if(!m)return null;const a=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return {r:a[0]/255,g:a[1]/255,b:a[2]/255,a:a.length>3?a[3]:1}}
  function splitTop(s){const out=[];let d=0,cur='';for(const ch of s){if(ch=='(')d++;if(ch==')')d--;if(ch==','&&d==0){out.push(cur.trim());cur=''}else cur+=ch}if(cur.trim())out.push(cur.trim());return out}
  function grad(g){ // linear-gradient(...) -> {angle, stops}
    const inner=g.slice(g.indexOf('(')+1,g.lastIndexOf(')'));const parts=splitTop(inner);let ang=180;
    if(/deg$/.test(parts[0])){ang=parseFloat(parts.shift())}else if(/^to /.test(parts[0])){const t=parts.shift();ang={'to bottom':180,'to top':0,'to right':90,'to left':270}[t]??180}
    const stops=parts.map((s,i)=>{const m=s.match(/(rgba?\([^)]+\)|#[0-9a-f]+|\w+)\s*([\d.]+%|[\d.]+px)?/i);let c=rgba(m[1]);if(!c&&m[1][0]=='#'){const h=m[1].slice(1);c={r:parseInt(h.substr(0,2),16)/255,g:parseInt(h.substr(2,2),16)/255,b:parseInt(h.substr(4,2),16)/255,a:1}}if(!c)c={r:0,g:0,b:0,a:0};let pos=m[2]?(m[2].endsWith('%')?parseFloat(m[2])/100:null):null;return {c,pos}});
    stops.forEach((s,i)=>{if(s.pos==null)s.pos=stops.length==1?0:i/(stops.length-1)});
    return {ang,stops};
  }
  // materialise pseudo elements
  const props=['position','top','left','right','bottom','width','height','display','background-color','background-image','color','font-family','font-size','font-weight','font-style','letter-spacing','line-height','text-transform','box-shadow','border-radius','margin-left','margin-right','white-space','opacity','inset','z-index','flex','vertical-align','border-top','border-bottom','border-left','border-right','animation'];
  const NS='http://www.w3.org/2000/svg';
  document.querySelectorAll('.conn').forEach(c=>{const d=document.createElement('span');d.style.cssText='position:absolute;bottom:-1px;left:50%;transform:translateX(-50%);width:11px;height:7px;line-height:0';d.innerHTML='<svg xmlns="'+NS+'" width="11" height="7" viewBox="0 0 11 7"><path d="M0.5 0.5 L5.5 6 L10.5 0.5" fill="none" stroke="currentColor" stroke-width="1"/></svg>';c.appendChild(d)});
  document.querySelectorAll('.conn .wait').forEach(w=>{const d=document.createElement('span');d.style.cssText='display:inline-block;width:11px;height:11px;margin-right:7px;vertical-align:-1px;line-height:0';d.innerHTML='<svg xmlns="'+NS+'" width="11" height="11" viewBox="0 0 11 11"><circle cx="5.5" cy="5.5" r="5" fill="none" stroke="currentColor"/><path d="M5.5 2.5 V5.5 H8" fill="none" stroke="currentColor"/></svg>';w.insertBefore(d,w.firstChild)});
  const xs=document.createElement('style');xs.textContent='.conn::after,.conn .wait::before{content:none!important}';document.head.appendChild(xs);
  document.querySelectorAll('article.em *, .pscreen *, .col *').forEach(el=>{
    for(const ps of ['::before','::after']){const cs=getComputedStyle(el,ps);if(!cs.content||cs.content=='none'||cs.content=='normal')continue;
      const sp=document.createElement('span');sp.dataset.pseudo='1';let txt=cs.content;txt=txt.replace(/^["']|["']$/g,'').replace(/\\A/g,'\n');sp.textContent=txt;
      for(const k of props)sp.style.setProperty(k,cs.getPropertyValue(k));
      if(ps=='::before')el.insertBefore(sp,el.firstChild);else el.appendChild(sp);}
  });
  const st=document.createElement('style');st.textContent='article.em *::before,article.em *::after,.pscreen *::before,.pscreen *::after,.col *::before,.col *::after{content:none!important}';document.head.appendChild(st);
  const res=[];
  const click=d=>{const bt=document.querySelector('#days button[data-day="'+d+'"]');if(bt)bt.click()};
  const BF='2026-11-27';
  function ext(R0){
      const art=R0.art;if(!art)return;
      const A=art.getBoundingClientRect();

      const items=[];
      function vis(el){const cs=getComputedStyle(el);return !(cs.display=='none'||cs.visibility=='hidden')}
      function op(el){let o=1;for(let e=el;e&&e!==art.parentElement;e=e.parentElement){o*=parseFloat(getComputedStyle(e).opacity)}return o}
      function rel(r){return {x:+(r.left-A.left).toFixed(1),y:+(r.top-A.top).toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)}}
      function boxStuff(el,cs,r,sec){
        if(r.width<0.5||r.height<0.5)return;
        const o=op(el);const R=rel(r);const cr=px(cs.borderTopLeftRadius);
        const bg=rgba(cs.backgroundColor);
        const bi=cs.backgroundImage&&cs.backgroundImage!='none'?splitTop(cs.backgroundImage):[];
        // url images (bottom), then bg color? CSS: color below images. order: color, then images from last to first
        if(bg&&bg.a>0)items.push({t:'r',...R,sec,f:bg,o,cr});
        for(const layer of bi.slice().reverse()){
          if(layer.startsWith('url(')){const src=layer.slice(4,-1).replace(/^["']|["']$/g,'');items.push({t:'i',...R,sec,src,m:'FILL',o,cr})}
          else if(layer.startsWith('linear-gradient')){items.push({t:'g',...R,sec,g:grad(layer),o,cr})}
          else if(layer.startsWith('repeating-linear-gradient')){const g=grad(layer.replace('repeating-',''));items.push({t:'r',...R,sec,f:g.stops[0].c,o,cr})}
        }
        // borders
        for(const s of ['Top','Right','Bottom','Left']){const w=px(cs['border'+s+'Width']);if(!w||cs['border'+s+'Style']=='none')continue;const c=rgba(cs['border'+s+'Color']);if(!c||c.a==0)continue;
          let bx;if(s=='Top')bx={x:R.x,y:R.y,w:R.w,h:w};if(s=='Bottom')bx={x:R.x,y:R.y+R.h-w,w:R.w,h:w};if(s=='Left')bx={x:R.x,y:R.y,w:w,h:R.h};if(s=='Right')bx={x:R.x+R.w-w,y:R.y,w:w,h:R.h};
          if(cr>0&&['Top','Right','Bottom','Left'].every(q=>px(cs['border'+q+'Width'])==w)){items.push({t:'r',...R,sec,f:null,st:c,sw:w,o,cr,dash:cs['border'+s+'Style']=='dashed'});break}
          items.push({t:'r',...bx,sec,f:c,o,dash:cs['border'+s+'Style']=='dashed'});}
      }
      const fam=f=>{f=f.toLowerCase();if(f.includes('bodoni'))return 'Bodoni Moda';if(f.includes('figtree'))return 'Figtree';return 'Inter'};
      let secIdx=-1;
      function walk(el,sec){
        if(el.nodeType!==1)return;if(!vis(el))return;
        const cs=getComputedStyle(el);const r=el.getBoundingClientRect();
        const tag=el.tagName.toLowerCase();
        if(tag=='svg'){const c=cs.color;let s=el.outerHTML.replace(/currentColor/g,c);if(!/width=/.test(s.slice(0,s.indexOf('>'))))s=s.replace('<svg',`<svg width="${r.width}" height="${r.height}"`);items.push({t:'v',...rel(r),sec,svg:s,o:op(el)});return}
        boxStuff(el,cs,r,sec);
        if(tag=='img'){if(!el.getAttribute('src'))return;const fit=cs.objectFit=='contain'?'FIT':'FILL';
          const cr=px(cs.borderTopLeftRadius);
          // content box
          const pl=px(cs.paddingLeft),pt=px(cs.paddingTop),pr=px(cs.paddingRight),pb=px(cs.paddingBottom);
          const R=rel(r);items.push({t:'i',x:R.x+pl,y:R.y+pt,w:R.w-pl-pr,h:R.h-pt-pb,sec,src:el.getAttribute('src'),m:fit,o:op(el),cr,pos:cs.objectPosition,bl:cs.mixBlendMode});return}
        for(const ch of el.childNodes){
          if(ch.nodeType===3){textNode(ch,el,cs,sec)}else walk(ch,sec);
        }
      }
      function blockOf(el){let e=el;while(e&&e!==art){const d=getComputedStyle(e).display;if(!d.startsWith('inline'))return e;e=e.parentElement}return art}
      function textNode(tn,el,cs,sec){
        let s=tn.data;if(!s.trim())return;
        const ws=cs.whiteSpace;if(!ws.startsWith('pre'))s=s.replace(/\s+/g,' ');
        const rg=document.createRange();const a0=tn.data.search(/\S/);const a1=tn.data.length-tn.data.split('').reverse().join('').search(/\S/);rg.setStart(tn,a0);rg.setEnd(tn,a1);
        const rects=[...rg.getClientRects()].filter(q=>q.width>0.5);if(!rects.length)return;
        const tt=cs.textTransform;
        const T=x=>tt=='uppercase'?x.toUpperCase():tt=='lowercase'?x.toLowerCase():tt=='capitalize'?x.replace(/\b\w/g,m=>m.toUpperCase()):x;
        const fsz=px(cs.fontSize);const lh=cs.lineHeight=='normal'?fsz*1.2:px(cs.lineHeight);
        const st={ff:fam(cs.fontFamily),fw:+cs.fontWeight,it:cs.fontStyle=='italic',fs:fsz,lh,ls:cs.letterSpacing=='normal'?0:px(cs.letterSpacing),c:rgba(cs.color),o:op(el),dec:cs.textDecorationLine.includes('line-through')?'S':cs.textDecorationLine.includes('underline')?'U':''};
        const tops=[...new Set(rects.map(q=>Math.round(q.top)))];
        const blk=blockOf(el);const bcs=getComputedStyle(blk);const br=blk.getBoundingClientRect();
        const cl=br.left+px(bcs.paddingLeft)+px(bcs.borderLeftWidth),cw=br.width-px(bcs.paddingLeft)-px(bcs.paddingRight)-px(bcs.borderLeftWidth)-px(bcs.borderRightWidth);
        const solo=blk.textContent.replace(/\s+/g,' ').trim()==s.trim()&&blk.querySelectorAll('*').length==0;
        if(tops.length==1){const u=rg.getBoundingClientRect();const R=rel(u);items.push({t:'x',...R,sec,s:T(s.trim()),...st,ml:0});return}
        if(solo){ // one multi-line text box with block width
          const u=rg.getBoundingClientRect();items.push({t:'x',x:+(cl-A.left).toFixed(1),y:+(u.top-A.top).toFixed(1),w:+cw.toFixed(1),h:+u.height.toFixed(1),sec,s:T(s.trim()),...st,ml:1,al:bcs.textAlign=='start'?'left':bcs.textAlign});return}
        // split per line by words
        const words=[];const re=/\S+/g;let m;const raw=tn.data;
        while((m=re.exec(raw))){const wr=document.createRange();wr.setStart(tn,m.index);wr.setEnd(tn,m.index+m[0].length);const q=[...wr.getClientRects()].filter(z=>z.width>0)[0];if(q)words.push({w:m[0],top:Math.round(q.top),l:q.left,r:q.right,t:q.top,b:q.bottom})}
        const lines={};words.forEach(w=>{(lines[w.top]=lines[w.top]||[]).push(w)});
        Object.values(lines).forEach(L=>{const l=Math.min(...L.map(w=>w.l)),r=Math.max(...L.map(w=>w.r)),t=Math.min(...L.map(w=>w.t)),bt=Math.max(...L.map(w=>w.b));
          items.push({t:'x',x:+(l-A.left).toFixed(1),y:+(t-A.top).toFixed(1),w:+(r-l).toFixed(1),h:+(bt-t).toFixed(1),sec,s:T(L.map(w=>w.w).join(' ')),...st,ml:0})});
      }
      const secs=[];
      [...art.children].forEach((ch,i)=>{if(ch.nodeType!==1||!vis(ch))return;const r=ch.getBoundingClientRect();secs.push({n:(ch.tagName.toLowerCase()=='footer'?'footer':(ch.className||ch.tagName).toString().split(' ')[0]||'block'),...rel(r),clip:getComputedStyle(ch).overflow=='hidden'});walk(ch,secs.length-1)});
      const acs=getComputedStyle(art);
      res.push({id:R0.id,eid:R0.eid,g:R0.g,cap:R0.cap||'',subj:R0.subj||'',st:R0.st||'',ph:R0.ph||'',place:R0.place||null,w:A.width,h:A.height,bg:rgba(acs.backgroundColor),secs,items});
  }
  click(BF);
  document.querySelectorAll('section.entry').forEach(sec=>{const g=sec.id.split('-')[0];ext({art:sec.querySelector('article.em'),id:sec.id,eid:sec.dataset.id,g,subj:(sec.querySelector('.elab .subj')||{}).innerText||'',st:sec.dataset.s})});
  for(const [ph,d] of [['pre','pre'],['ea','2026-11-23'],['bf',BF],['xmas','x1'],['late','l1'],['post','post']]){click(d);
    document.querySelectorAll('#band-P figure.pf').forEach((f,i)=>ext({art:f.querySelector('.pscreen'),id:'POP-'+ph+'-'+(i+1),eid:'POP',g:'P',ph,cap:f.querySelector('figcaption').textContent}))}
  click(BF);
  const hs=document.createElement('style');hs.textContent='.col article.em{visibility:hidden!important}';document.head.appendChild(hs);
  document.querySelectorAll('.band .col').forEach(col=>{const C=col.getBoundingClientRect();const place={};
    col.querySelectorAll('section.entry').forEach(sec=>{const r=sec.querySelector('article.em').getBoundingClientRect();place[sec.id]=[+(r.left-C.left).toFixed(1),+(r.top-C.top).toFixed(1)]});
    ext({art:col,id:'D-'+col.id,eid:col.id.split('-')[1],g:col.id.split('-')[0],place})});
  return res;
});
// images: dedupe
const imgs={};let n=0;
for(const e of data){for(const it of e.items){if(it.src){const h=crypto.createHash('sha1').update(it.src).digest('hex').slice(0,12);if(!imgs[h]){const m=it.src.match(/^data:([^;]+);base64,(.*)$/);if(m){const ext=m[1].includes('png')?'png':m[1].includes('svg')?'svg':'jpg';fs.writeFileSync(`${out}/img/${h}.${ext}`,Buffer.from(m[2],'base64'));imgs[h]={file:`${h}.${ext}`,type:m[1]}}else imgs[h]={file:null,url:it.src}}it.k=h;delete it.src}}}
fs.writeFileSync(out+'/emails.json',JSON.stringify(data));fs.writeFileSync(out+'/images.json',JSON.stringify(imgs,null,1));
console.log('emails',data.length,'images',Object.keys(imgs).length,'items',data.reduce((a,e)=>a+e.items.length,0));
await b.close()})();
