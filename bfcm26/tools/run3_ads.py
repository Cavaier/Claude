import sys
P=sys.argv[1]
LOGO="/_blob/b5d78a878b48e10609c923597dd1852e"; CASE="/_blob/3db4e3c55a1e58f2cb03bc8662f8fcf9"
def wrap(title,body):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Figtree:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0}}
a{{color:#141414}}a:hover{{color:#000000}}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1080,"height":1920}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''
ads={}
ads["M473-C1"]=("M Batch 473 C1 Yesterday today",'''<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #0E0E0E; font-family: Figtree, sans-serif; color: #FFFFFF">
<img src="/_blob/d296923ca694428fda5b29da1c5a267d" alt="The silver 3x set on a man's wrist against black" style="position: absolute; top: 640px; left: 0; width: 1080px; height: 1100px; object-fit: cover; object-position: 50% 45%; display: block; -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000000 22%, #000000 78%, transparent 100%); mask-image: linear-gradient(180deg, transparent 0%, #000000 22%, #000000 78%, transparent 100%)">
<div style="position: absolute; top: 300px; left: 0; width: 1080px; display: flex; flex-direction: column; align-items: center; gap: 18px; text-align: center">
<span style="font-size: 52px; font-weight: 400; color: #8F8F8B; text-decoration: line-through; text-decoration-thickness: 4px; text-transform: uppercase">Yesterday: full price</span>
<h1 style="margin: 0; font-size: 104px; line-height: 1.02; letter-spacing: 0; font-weight: 400; text-transform: uppercase">Today: 30% off</h1>
<p style="margin: 0; font-size: 32px; line-height: 1.4; color: #D6D6D3">Meet the 3x Minimal Stack Set at its Black Friday price.</p>
<a href="https://cavaier.com/" style="margin-top: 12px; display: inline-flex; align-items: center; justify-content: center; height: 84px; padding: 0 48px; background: #FFFFFF; color: #141414; text-decoration: none; font-size: 24px; font-weight: 500; letter-spacing: 0.1em">SHOP THE STACK</a>
</div>
<div style="position: absolute; top: 1420px; left: 0; width: 1080px; height: 96px; background: #2A2A28; display: flex; align-items: center; justify-content: center; gap: 20px; font-size: 26px; font-weight: 500; letter-spacing: 0.1em">
<span>4.5 ON TRUSTPILOT</span><span style="width: 2px; height: 30px; background: #6B6B68; display: block"></span><span>3,000+ REVIEWS</span>
</div>
</div>''')
ads["M473-C2"]=("M Batch 473 C2 Notes list",'''<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #0B0B0B; font-family: Figtree, sans-serif; color: #FFFFFF">
<div style="position: absolute; top: 300px; left: 64px; width: 952px; display: flex; justify-content: space-between; align-items: center; font-size: 34px; color: #E3B341">
<span style="display: flex; align-items: center; gap: 10px"><svg width="22" height="36" viewBox="0 0 22 36" fill="none" stroke="#E3B341" stroke-width="4" aria-hidden="true"><path d="M19 3 L4 18 L19 33"></path></svg><span style="text-decoration: underline">Notes</span></span>
<span style="font-weight: 600; text-decoration: underline">Done</span>
</div>
<h1 style="position: absolute; top: 420px; left: 64px; width: 900px; margin: 0; font-size: 60px; line-height: 1.15; font-weight: 600">Signs your wrist is ready for a stack</h1>
<ul style="position: absolute; top: 600px; left: 64px; width: 600px; margin: 0; padding-left: 40px; display: flex; flex-direction: column; gap: 18px; font-size: 36px; line-height: 1.3; font-weight: 400">
<li>Your watch does all the work</li>
<li>Bracelets you take off to shower</li>
<li>Pieces that never match</li>
<li>Ones that pinch or slide off</li>
<li>Sweat and heat dull them</li>
<li>You keep saying "next month"</li>
<li style="font-weight: 600">Black Friday: 30% off, no code</li>
</ul>
<img src="/_blob/5c61a9e1acd7a02aca23cd775539f169" alt="The black 3x set on a man's wrist" style="position: absolute; top: 880px; left: 680px; width: 340px; height: 420px; object-fit: cover; object-position: 45% 50%; display: block">
<p style="position: absolute; top: 1330px; left: 680px; width: 340px; margin: 0; font-size: 24px; line-height: 1.35; color: #BDBDBA">3x Minimal Stack Set<br>waterproof · 316L steel</p>
</div>''')
ads["M473-C3"]=("M Batch 473 C3 Big headline",'''<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #1C2127; font-family: Figtree, sans-serif; color: #FFFFFF">
<img src="/_blob/a88b57c085de7055c1d7f20c8f86e9c0" alt="The silver 3x set on a man's wrist with water splashing" style="position: absolute; top: 0; left: 0; width: 1080px; height: 1920px; object-fit: cover; object-position: 50% 50%; display: block">
<div style="position: absolute; top: 0; left: 0; width: 1080px; height: 1920px; background: linear-gradient(180deg, rgba(14, 16, 20, 0.7) 0%, rgba(14, 16, 20, 0.15) 34%, rgba(14, 16, 20, 0) 60%, rgba(14, 16, 20, 0.55) 100%)"></div>
<img src="/_blob/b5d78a878b48e10609c923597dd1852e" alt="Cavaier" style="position: absolute; top: 300px; left: 390px; width: 300px; height: auto; display: block; filter: invert(1)">
<h1 style="position: absolute; top: 400px; left: 56px; width: 968px; margin: 0; font-size: 124px; line-height: 0.98; letter-spacing: 0; font-weight: 600; text-transform: uppercase; text-shadow: 0 4px 30px rgba(0,0,0,0.35)">Made for<br><span style="display: block; text-align: right">the splash</span></h1>
<a href="https://cavaier.com/" style="position: absolute; top: 1400px; left: 290px; width: 500px; height: 92px; display: flex; align-items: center; justify-content: center; background: #FFFFFF; color: #141414; text-decoration: none; font-size: 24px; font-weight: 500; letter-spacing: 0.1em">HERE'S WHY · 30% OFF →</a>
</div>''')
ads["M474-C1"]=("M Batch 474 C1 Duo behind the stack",'''<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #F2F2F1; font-family: Figtree, sans-serif; color: #141414">
<img src="/_blob/b99e75987c70fa30b998c5d291370bae" alt="The gold 2x Duo Minimal Set on a man's wrist" style="position: absolute; top: 760px; left: 0; width: 1080px; height: 1160px; object-fit: cover; object-position: 50% 40%; display: block; -webkit-mask-image: linear-gradient(180deg, transparent 0%, #000000 18%); mask-image: linear-gradient(180deg, transparent 0%, #000000 18%)">
<div style="position: absolute; top: 300px; left: 72px; width: 900px; display: flex; flex-direction: column; gap: 22px">
<img src="/_blob/b5d78a878b48e10609c923597dd1852e" alt="Cavaier" style="width: 200px; height: auto; display: block">
<h1 style="margin: 0; font-size: 76px; line-height: 1.06; letter-spacing: 0; font-weight: 300; text-transform: uppercase">The duo behind<br>every stack<br><span style="font-weight: 600">— now 30% off.</span></h1>
<p style="margin: 0; font-size: 30px; line-height: 1.4; color: #444444; max-width: 820px">Two chains, worn as one. The 2x Duo Minimal Set in black, silver or gold, adjustable S, M or L.</p>
<a href="https://cavaier.com/" style="align-self: flex-start; display: inline-flex; align-items: center; justify-content: center; height: 80px; padding: 0 40px; background: #141414; color: #FFFFFF; text-decoration: none; font-size: 22px; font-weight: 500; letter-spacing: 0.1em">SHOP THE DUO →</a>
</div>
<figure style="position: absolute; top: 1200px; left: 72px; width: 280px; margin: 0; padding: 12px 12px 16px; background: #FFFFFF; transform: rotate(-4deg); box-shadow: 0 16px 36px rgba(20,20,20,0.25); display: flex; flex-direction: column; gap: 10px">
<img src="/_blob/3db4e3c55a1e58f2cb03bc8662f8fcf9" alt="The black Cavaier jewelry case" style="width: 256px; height: 200px; object-fit: cover; display: block">
<figcaption style="font-size: 20px; font-weight: 500; letter-spacing: 0.1em">CASE INCLUDED</figcaption>
</figure>
</div>''')
ads["M474-C2"]=("M Batch 474 C2 Photo over block",'''<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #1C1C1B; font-family: Figtree, sans-serif; color: #FFFFFF">
<img src="/_blob/5d6f6bad0112df468b8ba981b610acb8" alt="The black 2x Duo Minimal Set on a man's wrist" style="position: absolute; top: 0; left: 0; width: 1080px; height: 1000px; object-fit: cover; object-position: 50% 45%; display: block">
<img src="/_blob/b5d78a878b48e10609c923597dd1852e" alt="Cavaier" style="position: absolute; top: 300px; left: 410px; width: 260px; height: auto; display: block">
<div style="position: absolute; top: 1000px; left: 0; width: 1080px; height: 920px; background: #1C1C1B"></div>
<div style="position: absolute; top: 1070px; left: 0; width: 1080px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center">
<span style="font-size: 42px; line-height: 1.15; font-weight: 400; text-transform: uppercase">Every day asks for<br>an everyday stack.</span>
<h1 style="margin: 0; font-size: 104px; line-height: 1.0; letter-spacing: 0; font-weight: 600; text-transform: uppercase">The duo does it.</h1>
<p style="margin: 6px 0 0; font-size: 30px; line-height: 1.4; color: #C9C9C6">2 chains · waterproof · 30% off this Black Friday</p>
<a href="https://cavaier.com/" style="margin-top: 14px; display: inline-flex; align-items: center; justify-content: center; height: 84px; padding: 0 48px; background: #FFFFFF; color: #141414; text-decoration: none; font-size: 24px; font-weight: 500; letter-spacing: 0.1em">SHOP THE DUO →</a>
</div>
</div>''')
ads["M474-C3"]=("M Batch 474 C3 What's in the box",'''<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #FFFFFF; font-family: Figtree, sans-serif; color: #141414">
<h1 style="position: absolute; top: 290px; right: 64px; width: 760px; margin: 0; text-align: right; font-size: 74px; line-height: 1.05; letter-spacing: 0; font-weight: 400; text-transform: uppercase">Black Friday<br><span style="font-weight: 300">in one box</span></h1>
<img src="/_blob/f389ce3bd8c2a722e8067a63d47c744c" alt="The silver 2x Duo Minimal Set on a man's wrist" style="position: absolute; top: 560px; left: 64px; width: 560px; height: 760px; object-fit: cover; object-position: 50% 45%; display: block">
<img src="/_blob/3db4e3c55a1e58f2cb03bc8662f8fcf9" alt="The black Cavaier jewelry case" style="position: absolute; top: 1010px; left: 660px; width: 356px; height: 310px; object-fit: cover; display: block">
<div style="position: absolute; top: 300px; left: 64px; display: flex; flex-direction: column; gap: 6px">
<span style="font-size: 22px; font-weight: 500; letter-spacing: 0.1em">2X DUO MINIMAL SET</span>
<span style="align-self: flex-start; font-size: 22px; font-weight: 600; letter-spacing: 0.1em; color: #FFFFFF; background: #A82C24; padding: 4px 10px">30% OFF</span>
</div>
<div style="position: absolute; top: 640px; left: 660px; display: flex; flex-direction: column; gap: 6px">
<span style="font-size: 22px; font-weight: 500; letter-spacing: 0.1em">FIT</span>
<span style="font-size: 26px; font-weight: 400">Adjustable S · M · L</span>
</div>
<div style="position: absolute; top: 790px; left: 660px; display: flex; flex-direction: column; gap: 6px">
<span style="font-size: 22px; font-weight: 500; letter-spacing: 0.1em">FINISH</span>
<span style="font-size: 26px; font-weight: 400">Black, silver or gold</span>
</div>
<div style="position: absolute; top: 930px; left: 660px; display: flex; flex-direction: column; gap: 6px">
<span style="font-size: 22px; font-weight: 500; letter-spacing: 0.1em">JEWELRY CASE <span style="color: #A82C24">INCLUDED</span></span>
</div>
<div style="position: absolute; top: 1360px; left: 64px; width: 952px; display: flex; align-items: center; justify-content: space-between; gap: 24px; border-top: 1px solid #DCDCDA; padding-top: 28px">
<span style="font-size: 28px; font-weight: 400">Free shipping · no code needed</span>
<a href="https://cavaier.com/" style="display: inline-flex; align-items: center; justify-content: center; height: 84px; padding: 0 40px; background: #141414; color: #FFFFFF; text-decoration: none; font-size: 22px; font-weight: 500; letter-spacing: 0.1em">SHOP THE DUO</a>
</div>
</div>''')
ads["W417-C1"]=("W Batch 417 C1 Photo with side panel",'''<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #F2F2F1; font-family: Figtree, sans-serif; color: #141414">
<img src="/_blob/1813fe77a372238ed113820347e67d52" alt="The gold 3x set on a woman's wrist, white dress" style="position: absolute; top: 0; left: 0; width: 660px; height: 1920px; object-fit: cover; object-position: 55% 50%; display: block">
<div style="position: absolute; top: 0; left: 660px; width: 420px; height: 1920px; background: #EDEAE6"></div>
<div style="position: absolute; top: 520px; left: 700px; width: 340px; display: flex; flex-direction: column; gap: 26px">
<h1 style="margin: 0; font-size: 52px; line-height: 1.08; letter-spacing: 0; font-weight: 400; text-transform: uppercase">The piece your outfit was missing.<br><span style="font-weight: 600">Now 30% off.</span></h1>
<div style="display: flex; flex-wrap: wrap; gap: 8px">
<span style="font-size: 20px; border: 1px solid #141414; border-radius: 999px; padding: 6px 12px">Gold, silver or black</span>
<span style="font-size: 20px; border: 1px solid #141414; border-radius: 999px; padding: 6px 12px">Waterproof</span>
<span style="font-size: 20px; border: 1px solid #141414; border-radius: 999px; padding: 6px 12px">Sweat + heat resistant</span>
<span style="font-size: 20px; border: 1px solid #141414; border-radius: 999px; padding: 6px 12px">Adjustable S · M · L</span>
<span style="font-size: 20px; border: 1px solid #141414; border-radius: 999px; padding: 6px 12px">Case included</span>
</div>
<a href="https://cavaier.com/" style="display: flex; align-items: center; justify-content: center; height: 80px; background: #141414; color: #FFFFFF; text-decoration: none; font-size: 22px; font-weight: 500; letter-spacing: 0.1em">SHOP THE SET</a>
</div>
</div>''')
ads["W417-C2"]=("W Batch 417 C2 Save 30",'''<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #F2F2F1; font-family: Figtree, sans-serif; color: #141414">
<img src="/_blob/b433916dabadaa84706ba70a15d30daf" alt="The gold 3x set on a woman's wrist" style="position: absolute; top: 820px; left: 560px; width: 460px; height: 560px; object-fit: cover; object-position: 40% 45%; display: block">
<div style="position: absolute; top: 290px; left: 64px; width: 952px; display: flex; flex-direction: column; gap: 16px">
<img src="/_blob/b5d78a878b48e10609c923597dd1852e" alt="Cavaier" style="width: 210px; height: auto; display: block">
<span style="align-self: flex-start; font-size: 22px; font-weight: 500; letter-spacing: 0.1em; background: #FFFFFF; padding: 8px 14px">3X MINIMAL STACK SET · FOR HER</span>
<h1 style="margin: 0; font-size: 200px; line-height: 0.92; letter-spacing: -0.01em; font-weight: 700; text-transform: uppercase">Save 30%</h1>
<span style="width: 520px; height: 6px; background: #A82C24; display: block"></span>
<span style="font-size: 64px; line-height: 1.05; font-weight: 500; text-transform: uppercase">& free shipping</span>
<span style="font-size: 30px; line-height: 1.4; color: #444444">Your Black Friday stack, gold,<br>silver or black.</span>
</div>
<div style="position: absolute; top: 1000px; left: 64px; width: 460px; display: flex; flex-direction: column; gap: 22px">
<div style="display: flex; align-items: center; gap: 16px"><svg width="52" height="52" viewBox="0 0 52 52" fill="none" stroke="#141414" stroke-width="2" aria-hidden="true"><circle cx="26" cy="26" r="24"></circle><path d="M26 12 C21 20 17 25 17 31 a9 9 0 0 0 18 0 c0-6-4-11-9-19z"></path></svg><span style="font-size: 26px; line-height: 1.25">Waterproof,<br>sweat + heat resistant</span></div>
<div style="display: flex; align-items: center; gap: 16px"><svg width="52" height="52" viewBox="0 0 52 52" fill="none" stroke="#141414" stroke-width="2" aria-hidden="true"><circle cx="26" cy="26" r="24"></circle><path d="M17 23 a10 10 0 0 1 17-4 M34 15 v5 h-5 M35 29 a10 10 0 0 1 -17 4 M18 37 v-5 h5"></path></svg><span style="font-size: 26px; line-height: 1.25">Recycled 316L<br>stainless steel</span></div>
<div style="display: flex; align-items: center; gap: 16px"><svg width="52" height="52" viewBox="0 0 52 52" fill="none" stroke="#141414" stroke-width="2" aria-hidden="true"><circle cx="26" cy="26" r="24"></circle><rect x="14" y="21" width="24" height="15"></rect><path d="M14 21 l3 -6 h18 l3 6"></path></svg><span style="font-size: 26px; line-height: 1.25">Jewelry case<br>included</span></div>
</div>
<a href="https://cavaier.com/" style="position: absolute; top: 1410px; left: 64px; width: 952px; height: 92px; display: flex; align-items: center; justify-content: center; background: #141414; color: #FFFFFF; text-decoration: none; font-size: 26px; font-weight: 500; letter-spacing: 0.1em">SAVE 30% ON THE SET →</a>
</div>''')
ads["W417-C3"]=("W Batch 417 C3 Dark moody",'''<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #121212; font-family: Figtree, sans-serif; color: #FFFFFF">
<img src="/_blob/79488081a05c4c4da7f28f17bf2c432f" alt="The silver 3x set on a woman's arm, head resting" style="position: absolute; top: 160px; left: 0; width: 1080px; height: 1920px; object-fit: cover; object-position: 50% 50%; display: block; filter: brightness(0.5) contrast(1.1) saturate(0.85)">
<div style="position: absolute; top: 0; left: 0; width: 1080px; height: 1920px; background: linear-gradient(180deg, #121212 0%, #121212 14%, rgba(18,18,18,0.2) 40%, rgba(18,18,18,0) 70%, rgba(18,18,18,0.6) 100%)"></div>
<div style="position: absolute; top: 340px; left: 0; width: 1080px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center">
<h1 style="margin: 0; font-size: 72px; line-height: 1.08; letter-spacing: 0; font-weight: 300; text-transform: uppercase">Her Black Friday stack</h1>
<p style="margin: 0; font-size: 40px; font-style: italic; font-weight: 300; color: #DADAD7">(now 30% off, no code)</p>
</div>
<p style="position: absolute; top: 1440px; left: 0; width: 1080px; margin: 0; text-align: center; font-size: 26px; font-weight: 500; letter-spacing: 0.1em; color: #E4E4E2">GOLD · SILVER · BLACK — CASE INCLUDED</p>
</div>''')
for k,(t,b) in ads.items(): open(f"{P}/{k}.dc.html","w").write(wrap(t,b))
print("ok")
