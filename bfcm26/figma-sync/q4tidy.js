const img=await figma.getNodeByIdAsync('663:2');const lib=await figma.getNodeByIdAsync('359:3');
if(!img||!lib)return {img:!!img,lib:!!lib};
const maxY=Math.max(0,...lib.children.map(c=>c.y+c.height));lib.appendChild(img);img.x=0;img.y=maxY+40;img.name='93be2e645635';
return {moved:true,parent:img.parent.name,x:img.x,y:img.y};
