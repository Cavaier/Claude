import sys,os
from PIL import Image,ImageDraw
src,out,start,cnt=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
fs=sorted(f for f in os.listdir(src) if f.endswith('.jpg'))[start:start+cnt]
W,H=200,356;cols=10;rows=(len(fs)+cols-1)//cols
sh=Image.new('RGB',(cols*W,rows*(H+18)),'white');d=ImageDraw.Draw(sh)
for i,f in enumerate(fs):
    im=Image.open(os.path.join(src,f)).convert('RGB');im.thumbnail((W-4,H))
    x,y=(i%cols)*W,(i//cols)*(H+18);sh.paste(im,(x,y));d.text((x+2,y+H+2),f[:-4],fill='black')
sh.save(out,quality=85)
