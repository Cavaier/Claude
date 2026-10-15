#!/usr/bin/env python3
"""Build M-IDEA C1-C3 artboards (EN + No Text)."""
import os
H = os.path.dirname(os.path.abspath(__file__))
PH = "file://" + H + "/photos/"
LOGO = '<img src="/_blob/b5d78a878b48e10609c923597dd1852e" alt="Cavaier" style="width: 110px; height: auto; display: block">'
EU = "https://cavaier.com/products/2x-duo-minimal-set-for-him"
RED = "#A82C24"
BTN = ('<a href="%s" style="display: inline-flex; align-items: center; justify-content: center; height: 80px; padding: 0 48px; '
       'background: #141414; color: #FFFFFF; text-decoration: none; font-size: 22px; font-weight: 500; letter-spacing: 0.1em">%s</a>')
EYE = 'font-size: 22px; font-weight: 500; letter-spacing: 0.1em; text-transform: uppercase'
H1 = 'margin: 0; font-size: 50px; line-height: 1.15; letter-spacing: 0.04em; font-weight: 300; text-transform: uppercase'
BODY = 'margin: 0; font-size: 27px; font-weight: 300; line-height: 1.6; max-width: 720px'

TPL = """<!doctype html>
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
<div style="width: 1080px; height: 1920px; position: relative; overflow: hidden; background: #F2F1EE; font-family: Figtree, sans-serif; color: #141414">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1080,"height":1920}}}}'>
class Component extends DCLogic {{
  renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
"""

def img(f, style, alt):
    return f'<img src="{PH}{f}" alt="{alt}" style="position: absolute; {style}; object-fit: cover; display: block">'

C = {}
# C1 - Fastening moment: light top panel with text, photo below
C[1] = dict(
    title="M-IDEA - C1 · Fastening moment",
    photo=img("M-IDEA-C1-fasten.jpg", "top: 860px; left: 0; width: 1080px; height: 1060px; object-position: 50% 70%",
              "Fingers closing the clasp of the silver 2x Duo Minimal Set on a man's wrist"),
    text=f"""<div style="position: absolute; top: 290px; left: 0; width: 1080px; display: flex; flex-direction: column; align-items: center; gap: 18px; text-align: center">
{LOGO}
<span style="{EYE}; color: {RED}; margin-top: 8px">Black Friday</span>
<h1 style="{H1}">Two chains. One click.<br><span style="font-weight: 400">Now 30% off.</span></h1>
<p style="{BODY}">A box chain and a square chain in recycled 316L steel. Adjustable S/M/L.</p>
<div style="margin-top: 10px">{BTN % (EU, "SHOP THE DUO")}</div>
</div>""",
)
# C2 - Unboxing flat lay: full-bleed linen, text top, CTA bottom left
C[2] = dict(
    title="M-IDEA - C2 · Black Friday unboxing",
    photo=img("M-IDEA-C2-unbox.jpg", "top: 0; left: 0; width: 1080px; height: 1920px; object-position: 50% 50%",
              "The silver 2x Duo Minimal Set laid on pale linen beside its open case"),
    text=f"""<div style="position: absolute; top: 290px; left: 80px; width: 920px; display: flex; flex-direction: column; align-items: flex-start; gap: 16px">
<span style="{EYE}; font-size: 24px; color: {RED}">Black Friday · No code needed</span>
<h1 style="{H1}">Unbox the duo<br><span style="font-weight: 400">for 30% less</span></h1>
</div>
<div style="position: absolute; top: 1340px; left: 80px; display: flex; flex-direction: column; align-items: flex-start; gap: 22px">
<span style="{EYE}">Case included · Free shipping</span>
{BTN % (EU, "SHOP 30% OFF")}
</div>""",
)
# C3 - Minimal macro, one strong line: photo top, light panel bottom
C[3] = dict(
    title="M-IDEA - C3 · One line macro",
    photo=img("M-IDEA-C3-macro.jpg", "top: 0; left: 0; width: 1080px; height: 1190px; object-position: 50% 92%",
              "Macro of the silver box chain and square chain with tag on a man's wrist"),
    text=f"""<div style="position: absolute; top: 1225px; left: 0; width: 1080px; display: flex; flex-direction: column; align-items: center; gap: 14px; text-align: center">
<span style="{EYE}; color: {RED}">Black Friday</span>
<h1 style="{H1}">Wear it daily.<br><span style="font-weight: 400">Pay 30% less.</span></h1>
</div>
<div style="position: absolute; top: 1440px; left: 0; width: 1080px; display: flex; justify-content: center">{BTN % (EU, "SHOP THE DUO")}</div>
<div style="position: absolute; top: 1600px; left: 0; width: 1080px; display: flex; justify-content: center">{LOGO}</div>""",
)

for k, c in C.items():
    open(os.path.join(H, f"C{k}.dc.html"), "w").write(TPL.format(title=c["title"], body=c["photo"] + "\n" + c["text"]))
    open(os.path.join(H, f"nt_C{k}.dc.html"), "w").write(TPL.format(title=c["title"] + " (No Text)", body=c["photo"]))
print("built")
