"""Delete the link comments, but only those whose URL is now an annotation on the target layer (or its instance).
Run after comments_to_annotations.js. Needs FIGMA_TOKEN. Leaves every non-link comment alone.
Usage: python3 delete_link_comments.py          (dry run)
       python3 delete_link_comments.py --apply  (delete)"""
import json, os, sys, urllib.request
KEY = 'e0aqnfx3SvHowbEDDyMNMW'
H = {'X-Figma-Token': os.environ['FIGMA_TOKEN']}
rows = json.load(open(os.path.join(os.path.dirname(__file__), 'link_comments.json')))
def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=H)))
ids = sorted({r[1] for r in rows} | {r[2] for r in rows if r[2]})
ann = {}
for i in range(0, len(ids), 50):
    d = get(f'https://api.figma.com/v1/files/{KEY}/nodes?ids=' + ','.join(ids[i:i+50]))
    for k, v in (d.get('nodes') or {}).items():
        if v: ann[k] = [a.get('label', '') for a in v['document'].get('annotations', [])]
ok, missing = [], []
for cid, node, inst, url, label in rows:
    labels = ann.get(node, []) + (ann.get(inst, []) if inst else [])
    (ok if any(url in l for l in labels) else missing).append((cid, node, url))
print(f'{len(ok)} comments have a matching annotation, {len(missing)} do not (kept).')
for m in missing[:20]: print('  kept:', m)
if '--apply' in sys.argv:
    n = 0
    for cid, _, _ in ok:
        req = urllib.request.Request(f'https://api.figma.com/v1/files/{KEY}/comments/{cid}', headers=H, method='DELETE')
        try: urllib.request.urlopen(req); n += 1
        except Exception as e: print('  failed', cid, e)
    print('deleted', n)
