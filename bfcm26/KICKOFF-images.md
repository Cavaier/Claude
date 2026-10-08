# KICKOFF: new campaign and flow images (OpenAI image API)

Start a new session in this environment and say: "Continue from bfcm26/KICKOFF-images.md".
The previous session couldn't reach the API (the key and network change only apply to new sessions).

## Setup check (first thing)
- `OPENAI_API_KEY` must be set in the environment (Network secrets / env var). Never print it.
- `api.openai.com` must be allowed in Network access. Test: `curl -s -o /dev/null -w "%{http_code}" https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"` → 200.
- Before the first image, read OpenAI's current image-API pricing page and show the per-image cost for the model and quality used. Draft at low/medium quality, final at high.

## The look (Eli's reference photos are in `lookref/`: open them before every prompt)
- **Default = colour** (`lookref/colour-default_black-3x-set-wrist.webp`). **This photo is the exact target ("the reference of perfection"). Match its grade as is: bright soft daylight, neutral white balance, natural pink-beige skin only slightly desaturated. Do not push it colder, bluer or darker** (v3 rejected; v4 "neutral/pink-beige" wording rejected on skin tone). **Eli picked pilot v2 as best: use the v2 prompt wording in `imggen/p_02D_men.txt` / `p_02D_women.txt` as the base for every colour image.** This is the baseline for every email unless one is chosen as monochrome. Macro close-up of the black 3x set on a hairy male wrist, white background. Icy, muted, desaturated tones, natural cool skin with visible pores and fine hairs, soft daylight, shallow depth of field, the piece in sharp focus. Every colour image matches this tone, colour grade and style.
- **Monochrome = the full-email alternative** (`lookref/mono_woman-eye-bar-pendant.webp`, `lookref/mono_man-eye-bar-pendant.webp`). True black and white, tight crop on the face, the silver snake chain with the engraved CAVAIER bar held taut across the face under the eye. Soft studio light, high skin-texture detail, fine grain, quiet and intimate.
- **One direction per email: when an email is monochrome, every image in it is monochrome. Never mix the two in one email.**
- Calm, minimal, premium. No props overload, no text in images.
- Period vibe goes into the setting and light, not into loud props:
  - Black Friday: high contrast.
  - Matte Cuff weekend: matte stone or concrete.
  - Cyber Monday / Cyber Week: cool night light.
  - Christmas: warm low light, wool, the wrapped jewelry case.
  - Last minute: a gift card moment.
  - After Christmas: soft daylight.

## Product accuracy (non-negotiable)
- Every image is generated from the real Shopify product photo as the reference (images edit endpoint). Only the scene, model and light change; the piece must stay identical (chain types, the 3 bands of the set, the CAVAIER engraved bar, clasp).
- Women's vs men's: Shopify titles with " - " are women's ("3x Minimal - Stack Set" = `3x-minimal-stack-set-for-her`), without are men's ("3x Minimal Stack Set" = `3x-minimal-stack-set-for-him`). Match the copy next to the image: "3X SET · WOMEN" → women's set on a woman, "· MEN" → men's set on a man.
- Best seller all year: the 3x Minimal Cuff/Stack Set (both versions).
- Duo: only `2x-duo-minimal-set-for-him` exists. Crystal Necklace / Crystal Bracelet exist only for her.
- Matte Cuff and Glossy + Matte duo don't exist in Shopify yet, so there's no reference photo. Skip those slots or ask Eli.
- Pull product images: Shopify Admin GraphQL `products(query:"handle:...") { media { ... on MediaImage { image { url } } } }`.

## Review workflow Eli asked for
- One review page (artifact or Figma page), campaign by campaign, slot by slot.
- Each slot shows: current image, new image, product and finish it must show, colour or monochrome, cost of that image and running total.
- Eli answers yes → place it into the Figma frame (replace the IMAGE fill on that layer, keep crop) and go to the next slot. No → regenerate with his note.
- Start with **email campaigns** (Figma page 310:2: EU section 382:1418, US section 536:919; US copies use the same images). Flows come later; many flow blocks are dynamic Klaviyo product feeds.

## Campaign image slots (EU frame IDs; visible slot layer first, the larger layer is the cropped photo inside)
| Email | Slots (product) |
|---|---|
| 01-J Your VIP early access (353:1394) | For him: Bracelets, Sets, Necklaces · For her: Bracelets, Sets, Necklaces · "Not sure? 3x Minimal Set" |
| 02-D Used your VIP code? (315:26) | 3X SET · WOMEN (402:1616), 3X SET · MEN (402:1627) |
| V10-03 It's open to everyone (412:1424) | hero (412:1445) · 3X MINIMAL SET, 2X DUO, ROPE BRACELET, MINIMAL CUFF tiles |
| V10-04 What's selling first (412:1496) | 4 rank thumbnails: men's set, women's set, Rope, Cube |
| V10-05 Shower, gym, sleep (412:1574) | In the water / Every day / By the sea + Cube bracelet, Minimal Cuff |
| V10-07 Goes with everything (412:1673) | 4 finish photos (Silver, Gold, Black, Silver) + 5 product thumbs |
| V10-09 Black Friday is tomorrow (412:1785) | 2 hero halves + 3X SET, ROPE BRACELET, 2X DUO |
| 03-A 30% off · Black Friday (319:1298) | hero (505:1247) · 3X MINIMAL SET, MINIMAL CUFF, 3X SET banner |
| 04-B Rated 4.5 (315:962) | 3 review photos: 3X SET · MEN, 3X SET · WOMEN, 2X DUO |
| 05-B Gifts under €25 (315:1377) | Rope, Cube, Minimal Cuff, Cuban Necklace, Crystal Bracelet, Braid, Rope Pendant Necklace, 3x Set |
| 06-C Meet the Matte Cuff (316:1276) | Matte Cuff images: no product photo yet, ask Eli |
| 07-C One more thing (317:1332) | Matte Cuff thumbnail: no product photo yet |
| 08-E It's Cyber Monday (318:1508) | hero (Glossy + Matte): no product photo yet |
| 10-B €66.43 for three (315:3793) | hero 3x set (407:1481) · men's set, women's set, duo tiles |
| 12-C Compliments every single day (315:1682) | hero (407:1556) · 3x set, Crystal Necklace, Matte Cuff, Rope Pendant thumbs |
| 13-A Final call (315:1877) | hero (407:1675) · men's set, women's set, Matte Cuff, duo |

Text-only letters (no images): V10-06, V10-08, V10-16, V10-17, 14-A.

## Context
Strategy, rules and audit history: Figma flows page 359:2, Rules panel 754:2 (sections 1–8). Sale from Nov 13: prices already 30% off on the site, no code (only early access Nov 11–12 uses BF26). Domains: EU cavaier.com, US us.cavaier.com.

## Status (session 2, Oct 8)
- `OPENAI_API_KEY` is set, but `api.openai.com` is still denied by the environment's network policy (proxy 403 on CONNECT). Eli needs to add `api.openai.com` under Allowed domains in Network access (environment settings → Edit), then start a new session.
- Product reference photos are mapped in `imgref/refs.json` (handle → Shopify CDN URLs). Rerun the download snippet into `imgref/` (images are gitignored, ~100 MB).
- Not yet done: the pricing check (platform.openai.com wasn't reachable either), the review page, and any generation.
- 02-D picks (Eli): the v2 low-quality drafts `imggen/d_02D_*_low2.png` → saved as `imggen/pick_02D_men.png` / `pick_02D_women.png` (gitignored; regenerate from the v2 prompt if the container is gone). Detail is sufficient at 1024×1536 for the 270×360 slots, so a chosen draft can be the final without a high-quality rerun.
- **Review page:** https://claude.ai/artifact/6qveSFWV9yGiTAEKqDsGPh (source `review/index.html`, images in `review/img/`). Eli's answers land in its db collection `decisions` (doc id = slot id, `{verdict: yes|no, note, by, at}`): read them with ArtifactData `list`. Republish the same file path to add campaigns; omit `capabilities` on redeploy.
- Figma: `figma.com` downloads are blocked by the proxy; get current slot images with `get_screenshot` + `enableBase64Response` (the PNG is saved under tool-results) and crop locally.
- 01-J drafts done (6 slots). Flags: the men's necklace tile says €34.90, but the Rope Pendant Necklace is €39.90 in Shopify; both current necklace tiles are B&W in a colour email. 02-D current tiles show the women's set in gold and the men's in silver, while the picks are silver/black: Eli to confirm.
