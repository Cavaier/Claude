#!/usr/bin/env python3
"""W-IMIT2 C1/C2 images via OpenAI images/edits. Usage: python3 -I gen.py KEY:prompt_key ... Never prints the key."""
import base64, json, os, sys, time, threading
import requests
HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(HERE, "..", "photos", "w_silver_wrist_shopify_12616-532.jpg")
LOOK = "/home/user/Claude/bfcm26/ideation/style/cavaier-look.jpg"
prompts = json.load(open(os.path.join(HERE, "prompts.json")))
def gen(out, pk):
    for attempt in range(3):
        files = [("image[]", ("product.jpg", open(PROD, "rb"), "image/jpeg")),
                 ("image[]", ("look.jpg", open(LOOK, "rb"), "image/jpeg"))]
        data = {"model": "gpt-image-2.5-sunburst", "prompt": prompts[pk], "size": "1024x1536", "quality": "high", "n": "1"}
        r = requests.post("https://api.openai.com/v1/images/edits",
                          headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]}, data=data, files=files, timeout=600)
        if r.ok:
            open(os.path.join(HERE, "gen", out + ".png"), "wb").write(base64.b64decode(r.json()["data"][0]["b64_json"]))
            print("ok", out); return
        print("err", out, r.status_code, r.text[:300]); time.sleep(5)
ts = [threading.Thread(target=gen, args=a.split(":")) for a in sys.argv[1:]]
[t.start() for t in ts]; [t.join() for t in ts]
