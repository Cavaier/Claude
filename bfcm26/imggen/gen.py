#!/usr/bin/env python3
"""Generate one slot image from the real Shopify photo (+ look reference) via OpenAI images/edits.

usage: gen.py <slot_id> <out.png> <quality low|medium|high> <prompt_file> <ref1> [ref2 ...]
Appends cost to costs.jsonl. Costs use the higher published gpt-image-2 rates
(text in $5, image in $8, image out $30 per 1M tokens) so totals are never under-reported.
"""
import json, os, sys, time, base64, subprocess
RATES = {"text_in": 5e-6, "image_in": 8e-6, "image_out": 30e-6}
MODEL = os.environ.get("IMG_MODEL", "gpt-image-2")
slot, out, quality, pfile, *refs = sys.argv[1:]
prompt = open(pfile).read()
cmd = ["curl", "-sS", "https://api.openai.com/v1/images/edits",
       "-H", f"Authorization: Bearer {os.environ['OPENAI_API_KEY']}",
       "-F", f"model={MODEL}", "--form-string", f"prompt={prompt}", "-F", f"quality={quality}",
       "-F", "size=1024x1536", "-F", "n=1"]
MIME = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}
for r in refs: cmd += ["-F", f"image[]=@{r};type={MIME[r.rsplit('.', 1)[1].lower()]}"]
t = time.time()
res = json.loads(subprocess.run(cmd, capture_output=True, text=True, timeout=600).stdout)
if "error" in res: sys.exit(json.dumps(res["error"]))
open(out, "wb").write(base64.b64decode(res["data"][0]["b64_json"]))
u = res.get("usage", {}); d = u.get("input_tokens_details", {})
cost = d.get("text_tokens", 0)*RATES["text_in"] + d.get("image_tokens", 0)*RATES["image_in"] + u.get("output_tokens", 0)*RATES["image_out"]
rec = {"slot": slot, "out": out, "model": MODEL, "quality": quality, "usage": u, "cost_usd": round(cost, 4), "secs": round(time.time()-t), "at": int(time.time())}
log = os.path.join(os.path.dirname(os.path.abspath(__file__)), "costs.jsonl")
open(log, "a").write(json.dumps(rec) + "\n")
total = sum(json.loads(l)["cost_usd"] for l in open(log))
print(f"{slot}: ${cost:.4f}  (running total ${total:.4f})  {rec['secs']}s")
