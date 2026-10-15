#!/usr/bin/env python3
"""Generate W-IDEA ideation images. Usage: gen.py KEY [KEY...] (keys from prompts.json)."""
import base64, json, os, sys, concurrent.futures as cf
import requests

D = os.path.dirname(os.path.abspath(__file__))
REFS = [os.path.join(D, "refs_in/chains_gold.jpg"),
        os.path.join(D, "refs_in/cuff_silver.jpg"),
        "/home/user/Claude/bfcm26/ideation/style/cavaier-look.jpg"]
PROMPTS = json.load(open(os.path.join(D, "prompts.json")))


def run(key):
    files = [("image[]", (os.path.basename(p), open(p, "rb"), "image/jpeg")) for p in REFS]
    data = {"model": "gpt-image-2.5-sunburst", "prompt": PROMPTS[key], "size": "1024x1536",
            "quality": "high", "n": "1"}
    r = requests.post("https://api.openai.com/v1/images/edits",
                      headers={"Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]},
                      data=data, files=files, timeout=600)
    if r.status_code != 200:
        return key, "ERR %s %s" % (r.status_code, r.text[:400])
    b = base64.b64decode(r.json()["data"][0]["b64_json"])
    out = os.path.join(D, "gen", key + ".png")
    open(out, "wb").write(b)
    return key, out


with cf.ThreadPoolExecutor(6) as ex:
    for k, res in ex.map(run, sys.argv[1:]):
        print(k, res, flush=True)
