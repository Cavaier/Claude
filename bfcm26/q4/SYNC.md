# Q4 flows: chat ↔ Figma ↔ Klaviyo sync

The source of truth is this folder: `q4_specs.py` (every flow, email, day line, pop-up) → `gen_q4.py` → the canvas artifact
https://claude.ai/artifact/34FGtPENzj3EypMcka45UU. Figma and the two Klaviyo accounts are mirrors of it.

## Commands

| Eli says | Claude does |
|---|---|
| a change in chat | Edit `q4_specs.py` / CSS, regenerate, republish the canvas, commit. Nothing leaves the repo yet. |
| **push** | Push every change since the last push: Figma frames, then Klaviyo templates / saved blocks / flows in **both** accounts. Report what changed where. |
| **refresh** | Pull changes made in Figma (image swaps, copy, order) into `q4_specs.py`, regenerate the canvas, then push those same changes to Klaviyo. |
| push figma / push eu / push us | Push to that target only. |

Before every push or refresh: diff against the last synced state (`sync_state.json`, hashes per email) so only changed emails move.
Never switch a flow live or to manual without an explicit go in chat.

## Targets

| Target | What | Access |
|---|---|---|
| Figma | File `e0aqnfx3SvHowbEDDyMNMW` (BFCM), page node `359-2`. One frame per email, one section per flow, Women and Men pages. | Figma connector (re-authorise in claude.ai connector settings). |
| Klaviyo EU | cavaier.com · account `KCTpHb` · EUR · Europe/Stockholm | env `KLAVIYO_KEY_EU` (private key) |
| Klaviyo US | us.cavaier.com · account [to read on first connect] | env `KLAVIYO_KEY_US` (private key) |

Both keys need: Flows, Templates, Lists, Segments, Profiles, Events, Catalogs (read/write); Metrics, Accounts (read).
Network: `a.klaviyo.com` must be allowed in the environment (blocked as of Oct 7).

## Figma push (how)

Tooling in `../figma-sync/` (`extract_q4.js`, `compile_q4.py`, `builder_q4.js`, `sync_q4.py`):
1. `QMAX=26000 python3 sync_q4.py build q4w` — renders the canvas, compiles every email + pop-up frame, writes `q4batchNN.js` for emails whose hash changed since the last push (exit 2 + `missing_images.json` → upload those via `upload_assets` into the image library frame `359:3`, add to `hashes.json`).
2. Run each `q4batchNN.js` unchanged via `use_figma` (parallel workers are fine after batch 00, which creates any missing sections); save results to `q4res/`.
3. `python3 sync_q4.py commit q4w q4res/<file>.json` for each result → frame ids + hashes land in `sync_state.json` (`figma` key).
4. `python3 verify_q4.py js` → run `q4verify.js` via `use_figma` (read-only), save the result, `python3 verify_q4.py cmp <result.json>`: every frame's layers, positions and text are checked against its spec (a 1 px difference from half-pixel rounding is fine).

Layout on page Email Flows (`359:2`), from x = 6000 (right of the old flows master, which is left untouched): section “Sign-up pop-up”, then one section per flow for Women, then the same for Men. Frames are edited in place on later pushes (found by id, else by `F1E1-W ·` name), never moved.

## Per-account differences (never copy IDs across)

- Metric, list, segment and template IDs differ per account: map by name on first connect into `accounts.json`.
- Currency and time zone differ: “Tonight, midnight” and the date switches run on each account’s time zone; the sale end is set per account.
- Christmas cut-off dates, shipping copy and the US catalog / product URLs are per store.
- The pop-up is built by hand in each account’s form editor (no create-form API).

## What stays manual

Pop-up forms · Shopify-side test events (view, cart, checkout, order on each store) · real back-in-stock restocks · the product-tracking fix on the themes.
