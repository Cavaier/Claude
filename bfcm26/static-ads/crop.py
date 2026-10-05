# Pre-crops each source photo to the exact aspect of its slot in each ad format.
from PIL import Image
T='SCREENSHOT_DIR/'  # folder with get_screenshot PNGs of the Figma source nodes named below
SRC={
 'm_beach_face':T+'mcp-Figma-blob-1791217033012-ex2u0i.png',   # Cavaier 300:1485 DSC02487
 'm_wrist_close':T+'mcp-Figma-blob-1791217033557-pljosp.png',  # Cavaier 300:1486 DSC02511
 'm_bw_fist':T+'mcp-Figma-blob-1791217034530-xte3b3.png',      # Cavaier 377:256 DSC04856
 'w_face_gold':T+'mcp-Figma-blob-1791217037623-tcyfgo.png',    # Cavaier 306:111 DSC08998
 'w_wrists_gold':T+'mcp-Figma-blob-1791217040723-5y9gv5.png',  # Cavaier 312:9 DSC08318
 'cb_sky_black':T+'mcp-Figma-blob-1791217044810-3eux3r.png',   # Creative Bank 280:5 DSC09628
 'cb_white_black':T+'mcp-Figma-blob-1791217338369-3b0c6i.png', # Creative Bank 280:8 DSC09734
 'cb_sand_black':T+'mcp-Figma-blob-1791217339608-nh9qmn.png',  # Creative Bank 280:4 DSC09625
 'cb_water_black':T+'mcp-Figma-blob-1791217340751-dewgav.png', # Creative Bank 280:16 DSC09924
 'set_black':'src/3x-minimal-stack-set-1__0.png','set_gold':'src/3x-minimal-stack-set-1__1.png','set_silver':'src/3x-minimal-stack-set-1__2.png',
 'cuff_pack':'src/minimal-cuff-1__0.jpg','cube_wrist':'src/cube-bracelet__1.png','case_pack':'src/jewelry-case__0.jpg',
}
def crop(key,w,h,fx,fy,tx=.5,ty=.5,out=None):
    im=Image.open(SRC[key]).convert('RGB'); W,H=im.size; a=w/h
    cw,ch=(W,W/a) if W/H<a else (H*a,H)
    if ch>H: cw,ch=H*a,H
    x=fx*W-tx*cw; y=fy*H-ty*ch
    x=max(0,min(W-cw,x)); y=max(0,min(H-ch,y))
    c=im.crop((round(x),round(y),round(x+cw),round(y+ch)))
    if c.width>2400: c=c.resize((2400,round(2400/a)),Image.LANCZOS)
    c.save('crops/'+out+'.jpg',quality=92); return out,c.size,round(c.width/w,2)
J=[]
for F,H in (('45',1350),('11',1080)):
    J+=[crop('m_beach_face',540,H,.55,.5,out=f'ad01_{F}')]
    for k in ('set_silver','cuff_pack','cube_wrist'): J+=[crop(k,1,1,.5,.5,out=f'ad02_{k}')]
    th = 520 if F=='45' else 400
    for k in ('set_black','set_gold','set_silver'): J+=[crop(k,360,th,.5,.5,out=f'ad03_{F}_{k}')]
    J+=[crop('cb_water_black',1080,H,.5,.44,out=f'ad04_{F}')]
    J+=[crop('cb_white_black',1080,H,.5,.5,ty=.45,out=f'ad05_{F}')]
    J+=[crop('case_pack',1,1,.5,.52,out='ad05_case')]
    ph = 1050 if F=='45' else 820
    J+=[crop('m_wrist_close',539,ph,.4,.48,out=f'ad06_{F}_m'), crop('w_face_gold',539,ph,.5,.45,out=f'ad06_{F}_w')]
    J+=[crop('w_wrists_gold',436,H-128,.52,.55,out=f'ad07_{F}')]
    fh = 820 if F=='45' else 560
    J+=[crop('m_bw_fist',952,fh,.5,.45,out=f'ad08_{F}')]
    J+=[crop('cb_sky_black',1080,H,.5,.46,ty=(.36 if F=='45' else .32),out=f'ad09_{F}')]
    sh = 420 if F=='45' else 330
    J+=[crop('cb_sand_black',1080,sh,.5,.45,out=f'ad10_{F}')]
for j in dict((x[0],x) for x in J).values(): print(j)
