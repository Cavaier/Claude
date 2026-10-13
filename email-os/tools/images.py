"""Optimise every image a campaign uses and host it on the store's Shopify CDN.

Store photos are multi-MB PNGs; Shopify only shrinks them for clients that ask for WebP,
which most email apps don't. So each image is resized to 2x its slot and saved as a
progressive JPEG, then uploaded to Shopify Files once (deduplicated by content hash).

    python3 tools/images.py prepare <campaign-id>
        Download, resize, save data/img/eos-<sha>.jpg, write campaigns/<id>/images.lock.yaml.
        Prints the stagedUploadsCreate input for files that aren't hosted yet.
    python3 tools/images.py upload <staged-response.json>
        After the Shopify connector ran stagedUploadsCreate: POST each file to its target.
        Prints the fileCreate input.
    python3 tools/images.py register <files-response.json>
        After fileCreate (or a files(query:"filename:eos-*") lookup) returns READY image URLs:
        record them in data/hosted.yaml and every campaign's lock file.

Then render again: the renderer uses hosted URLs when the lock file has them.
"""
import hashlib
import io
import json
import mimetypes
import sys
import urllib.request
import uuid
from pathlib import Path

import yaml
from PIL import Image

from common import CAMPAIGNS, DATA, calendar_rows, campaign_markets, config, load
from render import SLOT_WIDTH, Market

IMG = DATA / "img"
HOSTED = DATA / "hosted.yaml"
MAX_BYTES = 300_000


def used_images(campaign_id):
    """{img_id: (source_url, slot)} across every market of the campaign."""
    cfg = config()
    row = calendar_rows()[campaign_id]
    layout = load(CAMPAIGNS / campaign_id / "layout.yaml")
    found = {}
    for m in campaign_markets(row, cfg):
        mk = Market(campaign_id, m, cfg, row)
        mk.render(layout)
        for img in mk.meta["images"]:
            slot = next((s for s, w in SLOT_WIDTH.items() if w == img["width"]), "image")
            found[img["id"]] = (img["source_url"], slot)
    return found


# Slots whose images sit side by side get one shape, so labels under them line up.
SLOT_ASPECT = {"tile": 4 / 5, "tile2": 4 / 5, "product": 1.0}


def crop_to(im, aspect):
    w, h = im.size
    if abs(w / h - aspect) < 0.01:
        return im
    if w / h > aspect:  # too wide: trim the sides
        nw = round(h * aspect)
        return im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = round(w / aspect)  # too tall: trim top and bottom equally
    return im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))


def optimise(data, width, aspect=None):
    im = Image.open(io.BytesIO(data))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    if aspect:
        im = crop_to(im, aspect)
    if im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    for quality in (82, 76, 70, 64):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
        if buf.tell() <= MAX_BYTES:
            break
    return buf.getvalue(), im.size


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "cavaier-email-os/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def prepare(campaign_id):
    IMG.mkdir(parents=True, exist_ok=True)
    hosted = load(HOSTED) or {}
    lock_path = CAMPAIGNS / campaign_id / "images.lock.yaml"
    lock = {"images": {}}
    pending = []
    for img_id, (src, slot) in sorted(used_images(campaign_id).items()):
        width = SLOT_WIDTH[slot] * 2
        data, (w, h) = optimise(fetch(src), width, SLOT_ASPECT.get(slot))
        digest = hashlib.sha256(data).hexdigest()[:16]
        name = f"eos-{digest}.jpg"
        (IMG / name).write_bytes(data)
        entry = {"source_url": src, "file": name, "bytes": len(data), "width": w, "height": h,
                 "url": hosted.get(name)}
        lock["images"][img_id] = entry
        if not entry["url"] and name not in [p["filename"] for p in pending]:
            pending.append({"filename": name, "mimeType": "image/jpeg", "resource": "IMAGE",
                            "httpMethod": "POST", "fileSize": str(len(data))})
        print(f"{img_id:28} {slot:8} {w}x{h} {len(data) // 1024:4} KB  {'hosted' if entry['url'] else 'NOT HOSTED'}")
    lock_path.write_text(yaml.safe_dump(lock, sort_keys=False))
    if pending:
        print("\nstagedUploadsCreate input:")
        print(json.dumps(pending, indent=1))
    return pending


def multipart(fields, filename, data):
    boundary = uuid.uuid4().hex
    body = io.BytesIO()
    for k, v in fields:
        body.write(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode())
    ctype = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    body.write(f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
               f"Content-Type: {ctype}\r\n\r\n".encode())
    body.write(data)
    body.write(f"\r\n--{boundary}--\r\n".encode())
    return body.getvalue(), f"multipart/form-data; boundary={boundary}"


def find_key(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for v in obj.values():
            r = find_key(v, key)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_key(v, key)
            if r is not None:
                return r
    return None


def upload(staged_json):
    targets = find_key(json.loads(Path(staged_json).read_text()), "stagedTargets")
    creates = []
    for t in targets:
        params = [(p["name"], p["value"]) for p in t["parameters"]]
        name = next((v for k, v in params if k == "key"), "").rsplit("/", 1)[-1] or None
        # The filename is the last part of the staged key; fall back to matching by order.
        if not name or not (IMG / name).exists():
            raise SystemExit(f"can't match staged target to a local file: {t['resourceUrl']}")
        body, ctype = multipart(params, name, (IMG / name).read_bytes())
        req = urllib.request.Request(t["url"], data=body, method="POST", headers={"Content-Type": ctype})
        with urllib.request.urlopen(req, timeout=120) as r:
            print(f"uploaded {name}: HTTP {r.status}")
        creates.append({"originalSource": t["resourceUrl"], "filename": name, "contentType": "IMAGE",
                        "alt": "Cavaier"})
    print("\nfileCreate input:")
    print(json.dumps(creates, indent=1))


def register(files_json):
    data = json.loads(Path(files_json).read_text())
    hosted = load(HOSTED) or {}
    n = 0
    for node in iter_nodes(data):
        url = (node.get("image") or {}).get("url") or (node.get("preview") or {}).get("image", {}).get("url")
        status = node.get("fileStatus")
        name = (url or "").split("?")[0].rsplit("/", 1)[-1]
        if url and name.startswith("eos-") and status in (None, "READY"):
            hosted[name] = url
            n += 1
    HOSTED.write_text(yaml.safe_dump(hosted, sort_keys=True))
    for lock_path in CAMPAIGNS.glob("*/images.lock.yaml"):
        lock = load(lock_path)
        for entry in lock["images"].values():
            entry["url"] = hosted.get(entry["file"], entry.get("url"))
        lock_path.write_text(yaml.safe_dump(lock, sort_keys=False))
    print(f"registered {n} hosted images")


def iter_nodes(obj):
    if isinstance(obj, dict):
        if "fileStatus" in obj or "image" in obj:
            yield obj
        for v in obj.values():
            yield from iter_nodes(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_nodes(v)


if __name__ == "__main__":
    cmd, arg = sys.argv[1], sys.argv[2]
    {"prepare": prepare, "upload": upload, "register": register}[cmd](arg)
