# BFCM26 · Meta static ads (v1)

10 concepts, each with its own layout, in 4:5 (1080×1350) and 1:1 (1080×1080).
Built natively in Figma (editable text, image fills, logo vector): file `e0aqnfx3SvHowbEDDyMNMW`, page 429:2,
section **"BFCM26 · Meta statics v1 (Claude)"** (449:2), to the right of the existing draft sections (those were not touched).
Each row: brief + Meta copy on the left, 4:5, then 1:1. Frame ids are in `manifest.json`.

| # | Concept · layout | Flight | Headline |
|---|---|---|---|
| 01 | Big 30 · split photo / huge 30% | Nov 13 – Dec 6 | 30% off everything. No code. |
| 02 | Ranked list · 01–02–03 ledger | Nov 13 – Dec 6 | What's selling first. |
| 03 | Receipt · triptych + receipt card | Nov 13 – Dec 6 | €66.47 for three. |
| 04 | Water checklist · full bleed + tick card | Nov 13 – Dec 6 | Shower, gym, sleep, repeat. |
| 05 | Case card · overlapping product card | Nov 13 – Dec 6 | Two pieces. The case comes with it. |
| 06 | Diptych · his silver / hers gold | Nov 13 – Dec 6 | Goes with everything. |
| 07 | Trust stat · huge 4.5 + tall photo | retargeting | Rated 4.5 by 3,000+. |
| 08 | Timeline · Today ——— ● Fri 27 | Nov 25 – 26 | Black Friday is tomorrow. |
| 09 | Week calendar · 7-day strip | Nov 30 – Dec 5 | Black Friday didn't end. It got a week. |
| 10 | Ends tonight · big type | Dec 6 | Ends tonight. |

## Photos
High resolution only. Creative Bank RAW (1580×2370 canvas nodes) for full-bleed ads; Cavaier Image Assets
(760–940 px exports) only where the photo fills half the ad or less; Shopify originals (2070×2760) for packshots.
`crop.py` pre-crops every photo to the exact aspect of its slot; `crops/` holds the uploaded files and
`hashes.json` their Figma image hashes (images live in the "Image library" frame 449:5 — keep it).

Why not the Figma originals directly: this environment blocks figma.com downloads, Figma image hashes don't
carry across files, and plugin returns are capped, so the Figma photos come from `get_screenshot` at node size.

## Open flags
- 02: confirm the top-3 order from Shopify sales.
- 04: water-friendly claim kept off the image; confirm before using it in primary text.
- 07: Trustpilot badge in Cavaier › Assets says 4.7/5 · 10,000+, campaign line says 4.5 · 3,000+.
- 09: the black "today" cell needs a daily swap, or run a version without it.
- Matte Cuff (no photos yet) and early-access code ad not built.
