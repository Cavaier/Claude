import sys,os
from PIL import Image,ImageDraw
src,out=sys.argv[1],sys.argv[2]
fs=sorted(f for f in os.listdir(src) if f.lower().endswith(('.jpg','.png')))
W,H=240,420;cols=7;rows=(len(fs)+cols-1)//cols
sh=Image.new('RGB',(cols*W,rows*(H+24)),'white');d=ImageDraw.Draw(sh)
for i,f in enumerate(fs):
    im=Image.open(os.path.join(src,f)).convert('RGB');im.thumbnail((W,H))
    x,y=(i%cols)*W,(i//cols)*(H+24);sh.paste(im,(x,y));d.text((x+4,y+H+4),f+' %dx%d'%Image.open(os.path.join(src,f)).size,fill='black')
sh.save(out,quality=85)
