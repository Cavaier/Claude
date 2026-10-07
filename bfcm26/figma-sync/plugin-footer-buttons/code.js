// Cavaier · BRACELETS + NECKLACES footer buttons get the same link as that footer's SHOP ALL (one-shot development plugin).
// The link is read from the SHOP ALL annotation at run time (fallback: EU https://cavaier.com/, US https://us.cavaier.com/).
// Annotation goes on the button's outer bg layer (as on 01-J), category "URL". A button whose layers already have
// any annotation is skipped. Safe to re-run.
const F=[["402:1754","https://cavaier.com/"],["406:1428","https://cavaier.com/"],["406:1605","https://cavaier.com/"],["402:1575","https://cavaier.com/"],["402:1651","https://cavaier.com/"],["406:1550","https://cavaier.com/"],["407:1428","https://cavaier.com/"],["407:1530","https://cavaier.com/"],["407:1644","https://cavaier.com/"],["402:1850","https://cavaier.com/"],["412:1484","https://cavaier.com/"],["412:1562","https://cavaier.com/"],["412:1635","https://cavaier.com/"],["412:1750","https://cavaier.com/"],["412:1842","https://cavaier.com/"],["468:552","https://cavaier.com/"],["468:654","https://cavaier.com/"],["468:737","https://cavaier.com/"],["468:764","https://cavaier.com/"],["468:789","https://cavaier.com/"],["468:866","https://cavaier.com/"],["468:954","https://cavaier.com/"],["468:1027","https://cavaier.com/"],["468:1095","https://cavaier.com/"],["468:1191","https://cavaier.com/"],["468:1317","https://cavaier.com/"],["468:1379","https://cavaier.com/"],["468:1446","https://cavaier.com/"],["468:1508","https://cavaier.com/"],["468:1601","https://cavaier.com/"],["468:1671","https://cavaier.com/"],["536:984","https://us.cavaier.com/"],["536:1095","https://us.cavaier.com/"],["536:1129","https://us.cavaier.com/"],["536:1372","https://us.cavaier.com/"],["536:1461","https://us.cavaier.com/"],["536:1488","https://us.cavaier.com/"],["536:1573","https://us.cavaier.com/"],["536:1670","https://us.cavaier.com/"],["536:1749","https://us.cavaier.com/"],["536:1864","https://us.cavaier.com/"],["536:2017","https://us.cavaier.com/"],["536:2090","https://us.cavaier.com/"],["536:2163","https://us.cavaier.com/"],["536:2237","https://us.cavaier.com/"],["536:2350","https://us.cavaier.com/"],["536:2427","https://us.cavaier.com/"],["402:1430","https://cavaier.com/"]];
const BTN={BRACELETS:['312:16','312:17','312:18'],NECKLACES:['312:19','312:20','312:21']};
(async()=>{try{
const cats=await figma.annotations.getAnnotationCategoriesAsync();
const cat=cats.find(c=>/^url$/i.test(c.label))||cats.find(c=>/interaction/i.test(c.label));
const out={added:0,skipped:0,missing:0,fromShopAll:0};
const has=x=>x&&x.annotations&&x.annotations.length>0;
for(const [inst,fallback] of F){
  const shop=await figma.getNodeByIdAsync(`I${inst};312:14`);
  const sa=shop&&shop.annotations&&shop.annotations.find(a=>a.label||a.labelMarkdown);
  const url=sa?(sa.label||sa.labelMarkdown):fallback; if(sa)out.fromShopAll++;
  for(const ids of Object.values(BTN)){
    const nodes=await Promise.all(ids.map(s=>figma.getNodeByIdAsync(`I${inst};${s}`)));
    if(!nodes[0]){out.missing++;continue}
    if(nodes.some(has)){out.skipped++;continue}
    const a={label:url};if(cat)a.categoryId=cat.id;nodes[0].annotations=[a];out.added++;
  }
}
figma.closePlugin(`Done: ${out.added} buttons added, ${out.skipped} skipped (already had one), ${out.missing} missing · category ${cat?cat.label:'none'}`);
}catch(e){figma.closePlugin('Error: '+e);}})();
