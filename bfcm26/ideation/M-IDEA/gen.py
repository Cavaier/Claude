#!/usr/bin/env python3
"""Generate M-IDEA ideation images via OpenAI images/edits.
Usage: python3 -I gen.py KEY [KEY...]   (keys from prompts.json)
Writes gen/<KEY>.png. Never prints the API key."""
import base64, json, os, sys, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.join(HERE, "refs", "refs_duo_r1crop.jpg")
LOOK = "/home/user/Claude/bfcm26/ideation/style/cavaier-look.jpg"
prompts = json.load(open(os.path.join(HERE, "prompts.json")))


def gen(key):
    files = [
        ("image[]", ("product.jpg", open(PROD, "rb"), "image/jpeg")),
        ("image[]", ("look.jpg", open(LOOK, "rb"), "image/jpeg")),
    ]
    data = {"model": "gpt-image-2.5-sunburst", "prompt": prompts[key],
            "size": "1024x1536", "quality": "high", "n": "1"}
    for attempt in range(3):
        r = requests.post("https://api.openai.com/v1/images/edits",
                          headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
                          data=data, files=files, timeout=600)
        if r.ok:
            b = r.json()["data"][0]["b64_json"]
            out = os.path.join(HERE, "gen", key + ".png")
            open(out, "wb").write(base64.b64decode(b))
            print("ok", key, out)
            return
        print("err", key, r.status_code, r.text[:400])
        time.sleep(5)
        for _, f in files:
            f[1].seek(0)


if __name__ == "__main__":
    import threading
    ts = [threading.Thread(target=gen, args=(k,)) for k in sys.argv[1:]]
    [t.start() for t in ts]
    [t.join() for t in ts]
