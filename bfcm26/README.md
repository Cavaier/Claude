# Cavaier BFCM26 email sequence

14 sends, Nov 23 – Dec 6, 2026. Mock-ups for review before they are built in Figma
(BFCM file, page "Email Campaign") and Klaviyo.

- Live review page: https://claude.ai/artifact/21hL1pG8bndjPaBr8p8G6S
- `cavaier-bfcm26-sequence.html`: the built page (all images embedded).

## Rebuild

    python3 gen_bfcm26_v7.py

The generators are layered patches: `gen_bfcm26.py` is the base and `v2`…`v7` each patch the
one before. `bfcm26.tpl.html` is the page template. Images come from `figimg/` (Figma shoot)
and the cavaier.com product images cached in `imgcache26*/`.

## Open placeholders

- Christmas delivery cut-off date (`[CEO to confirm date]`)
- Matte Cuff restock month
- Matte Cuff photos (Minimal Cuff stand-ins for now)

`older/` holds the first single-email and 5-email Black Week mock-ups.
