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

Layout on page Email Flows (`359:2`), from x = 6000 (the old flows master on the left is untouched), mirroring the canvas: “Sign-up pop-up” section with one row per sale period (6 × 7 frames), then a big “Women” title and one section per flow (huge title, then the flow diagram: header card, trigger, waits, email labels, exits, with each email frame placed on it), then the same for Men. Emails show the Black Friday view (others show their own first period), never greyed out. Frames are edited in place on later pushes (found by id, else by the code before ` · ` in the name). Batch 00 must run first (sections, moves, removals); the rest can run in parallel. `ONLYRE=<regex>` limits a push to matching keys.

## Per-account differences (never copy IDs across)

- Metric, list, segment and template IDs differ per account: map by name on first connect into `accounts.json`.
- Currency and time zone differ: “Tonight, midnight” and the date switches run on each account’s time zone; the sale end is set per account.
- Christmas cut-off dates, shipping copy and the US catalog / product URLs are per store.
- The pop-up is built by hand in each account’s form editor (no create-form API).

## SMS and Gender (on push)

- SMS texts live inside the same Klaviyo flows (F2, F4, F5, F7, F9) behind a “can receive SMS” split, plus S1 SMS Welcome. S2 is six scheduled SMS campaigns, not a flow.
- Every text is checked by `gen_q4.py` to be plain GSM-7 and one segment (160 incl. 23-char link and the opt-out line).
- G1/G2 set the profile property `Gender` from Ordered Product (English collections / tags) and Viewed Product (translated category names, list in `q4_specs.py`). They never overwrite an existing Gender.
- One-off backfill on the first push to each account: set `Gender` (+ `Gender source = order`) for existing customers with no Gender from their Ordered Product history, via the API.
- F7, F8, F11 are list-triggered: bulk-add their segments on the dates in each flow's trigger (F8 Oct 19, F11 Nov 19, F7 Nov 23; F7/F11 top-up Dec 7).

## Klaviyo push (done Oct 7, both accounts, all drafts)

`klaviyo/push.py EU|US [images templates lists segments flows campaigns backfill subjects]`; ids in `sync_state.json['klaviyo']`.
- 39 templates per account (`Q4 · F1E1 · …`), email-safe HTML from `klaviyo/emailer.py`; date phase + Gender logic inside; `klaviyo/rendertest.py` renders all through Klaviyo.
- 15 flows per account as drafts (F1–F8, F10–F13, S1, G1, G2). F9 Back in Stock: build by hand (no API trigger), templates `Q4 · F9E1/E2` are ready.
- Fixed-date steps F1E6, F1E7, F10E3, F13E2 are draft email campaigns; S2C1–C6 are draft SMS campaigns. None scheduled.
- Lists `Q4 · Winback / Second purchase / Sunset / Sale live` + segments for the bulk adds.
- Subject/preview: Klaviyo caps them at ~250 characters incl. logic. Where the date logic doesn't fit, the flow carries the current period's text; run `push.py EU subjects` and `push.py US subjects` on Nov 23, Nov 27, Dec 1, Dec 7, Dec 18 [cut-off] and Dec 25.
- Gender backfill from order history: not run yet (needs an explicit go).
- Pop-ups: `klaviyo/forms.py EU|US` built six draft forms per account (`Q4 Pop-up · Pre-sale` … `After Christmas`), built to the Figma design (two B/W photos as the side image, #F2F2F1 panel, logo, red kicker, light headline, black buttons, “Not now”, teaser tab), steps email → phone → who → done, shown after 5 s / exit intent / 2nd page, hidden from cart/checkout. `--replace` rebuilds them. Klaviyo limits: max 6 rows per column; the content column's styles must be null next to a side image; skip links must submit (they re-submit the email list). Publish the next one on each switch date and switch the previous one off.

## What stays manual

Publishing the pop-up for each period · Shopify-side test events (view, cart, checkout, order on each store) · real back-in-stock restocks · the product-tracking fix on the themes.
