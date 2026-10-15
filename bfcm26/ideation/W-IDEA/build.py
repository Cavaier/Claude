#!/usr/bin/env python3
"""Build W-IDEA C1-C3 artboards (EN + No Text)."""
import os, re
D = os.path.dirname(os.path.abspath(__file__))
PH = "file://" + D + "/photos/W-IDEA-%s.jpg"
LOGO = "/_blob/b5d78a878b48e10609c923597dd1852e"
URL = "https://cavaier.com/products/3x-minimal-stack-set-for-her"
RED = "#A82C24"

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0}}
a{{color:#141414}}a:hover{{color:#000000}}
</style>
</helmet>
"""
TAIL = """</x-dc>
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":1080,"height":1920}}'>
class Component extends DCLogic {
  renderVals() { return {}; }
}
</script>
</body>
</html>
"""
LABEL = '<span data-t style="font-size: 22px; font-weight: 500; letter-spacing: 0.1em; color: %s">{}</span>' % RED
H1 = '<h1 data-t style="margin: 0; font-size: {size}px; line-height: 1.15; letter-spacing: 0.04em; font-weight: 300; text-transform: uppercase">{txt}</h1>'
BODY = '<p data-t style="margin: 0; font-size: 27px; line-height: 1.6; font-weight: 300; color: #2E2E2C; max-width: {w}px">{txt}</p>'
BTN = '<a data-t href="' + URL + '" style="display: inline-flex; align-items: center; justify-content: center; height: 80px; padding: 0 48px; background: #141414; color: #FFFFFF; text-decoration: none; font-size: 22px; font-weight: 500; letter-spacing: 0.1em">{}</a>'
LOGOIMG = '<img data-t src="' + LOGO + '" alt="Cavaier" style="width: 110px; height: auto; display: block">'

ADS = {}

# C1 - gifting moment with the case (gold). Text panel on top, photo below.
ADS["C1"] = ("W-IDEA - C1 · Gift in the case (gold)", f"""<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #EDECE9; font-family: Figtree, sans-serif; color: #141414">
<img src="{PH % 'C1'}" alt="Hands opening a black case holding the gold 3x Minimal - Stack Set on pale linen" style="position: absolute; top: 790px; left: 0; width: 1080px; height: 1130px; object-fit: cover; object-position: 50% 62%; display: block">
<div style="position: absolute; top: 300px; left: 0; width: 1080px; display: flex; flex-direction: column; align-items: center; gap: 18px; text-align: center">
{LOGOIMG}
<div style="height: 18px"></div>
{LABEL.format('BLACK FRIDAY · 30% OFF SITEWIDE')}
{H1.format(size=50, txt='A gift she can<br><span style="font-weight: 500">wear every day.</span>')}
{BODY.format(w=720, txt='Cuff, box chain and square chain. Case included, free shipping, no code needed.')}
<div style="height: 4px"></div>
{BTN.format('SHOP THE GIFT')}
</div>
</div>
""")

# C2 - cosy self-gift (silver). Photo on top, left-aligned text panel below.
ADS["C2"] = ("W-IDEA - C2 · Cosy self-gift (silver)", f"""<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #F1EFEB; font-family: Figtree, sans-serif; color: #141414">
<img src="{PH % 'C2'}" alt="A wrist in a cream knit sweater holding a mug, wearing the silver 3x Minimal - Stack Set" style="position: absolute; top: 0; left: 0; width: 1080px; height: 1140px; object-fit: cover; object-position: 50% 58%; display: block">
<div style="position: absolute; top: 1176px; left: 80px; width: 920px; display: flex; flex-direction: column; align-items: flex-start; gap: 16px">
{LABEL.format('BLACK FRIDAY · 30% OFF SITEWIDE')}
{H1.format(size=50, txt='This year,<br><span style="font-weight: 500">gift yourself first.</span>')}
{BODY.format(w=760, txt='Three pieces in recycled 316L steel, adjustable S/M/L. Prices already 30% off.')}
{BTN.format('SHOP 30% OFF')}
</div>
</div>
""")

# C3 - crisp macro, one strong line (black). Photo bleeds up into a matching light field.
ADS["C3"] = ("W-IDEA - C3 · Macro, one line (black)", f"""<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #F2F3F5; font-family: Figtree, sans-serif; color: #141414">
<img src="{PH % 'C3'}" alt="Macro of the black 3x Minimal - Stack Set on a woman's wrist against a bright white blur" style="position: absolute; top: 300px; left: 0; width: 1080px; height: 1620px; object-fit: cover; display: block">
<div style="position: absolute; top: 300px; left: 0; width: 1080px; height: 160px; background: linear-gradient(#F2F3F5, rgba(242,243,245,0))"></div>
<div style="position: absolute; top: 310px; left: 0; width: 1080px; display: flex; flex-direction: column; align-items: center; gap: 18px; text-align: center">
{LABEL.format('BLACK FRIDAY')}
{H1.format(size=58, txt='Three pieces.<br><span style="font-weight: 500">30% off.</span>')}
{BODY.format(w=720, txt='Waterproof, adjustable S/M/L. No code needed.')}
<div style="height: 2px"></div>
{BTN.format('SHOP THE STACK')}
</div>
</div>
""")

for k, (title, body) in ADS.items():
    open(os.path.join(D, k + ".dc.html"), "w").write(HEAD.format(title=title) + body + TAIL)
    nt = re.sub(r'<(span|h1|p|a) data-t[^>]*>.*?</\1>', '', body, flags=re.S)
    nt = re.sub(r'<img data-t[^>]*>', '', nt)
    open(os.path.join(D, "nt_" + k + ".dc.html"), "w").write(HEAD.format(title=title + " (No Text)") + nt + TAIL)
for k in ADS:  # strip helper attribute from EN files
    p = os.path.join(D, k + ".dc.html"); s = open(p).read().replace(" data-t", ""); open(p, "w").write(s)
print("ok")
