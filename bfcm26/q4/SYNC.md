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

## Calendar (changed Oct 8, aligned with the campaigns page)

Pre-sale Oct 27 – Nov 10 · early access Wed Nov 11 – Thu Nov 12, members only, code **BF26** (30% off) · Black Friday sale Nov 13 – 30 (the website switches to Black Friday on Nov 13; no code; Black Friday day Nov 27, Matte Cuff Nov 28, Cyber Monday Nov 30) · Cyber Week Dec 1 – 6 · Christmas Dec 7 – 10 · **Christmas cut-off Thu Dec 10, every country** (after it: gift cards) · last minute Dec 11 – 24 · after Christmas Dec 25 – Jan 10. F8 sunset runs Oct 19 – Nov 1 (suppress non-clickers Nov 2). Day lines: `b1` Nov 14 – 25, `x1` Dec 7 – 8, `l1` Dec 11 – 23.
Campaign days on the campaigns page (Figma 310:2): Nov 11, 12, 13, 15, 17, 19, 22, 24, 26, 27, 28, 29, 30, Dec 2, 4, 6, 7, 8, 9, 10, 11, 24. F1E6/F1E7 were dropped: the campaigns send those days. US: same content in USD with AM/PM times (pop-ups and SMS included); the US campaigns are their own duplicates on the campaigns page.
After a copy change, `push.py EU|US templates lists flows dated campaigns` rebuilds the affected draft flows (flow hashes include template HTML) and the SMS campaigns; `forms.py EU|US --replace` rebuilds the pop-ups.

## Checks before any push or go-live

- `klaviyo/datetest.py EU|US [dates]` renders every template through Klaviyo with the date pinned (Nov 1, 11, 18, 26, 27, Dec 1, 9, 15, 30 by default), women and men, and checks every line of the local preview is in Klaviyo's output and no raw tag or `[placeholder]` leaks. Oct 8: EU and US 538 renders each, 0 problems.
- `klaviyo/sweep.py EU|US [--delete]` lists Q4-named flows, campaigns, templates, lists, segments and forms that are not in `sync_state.json` (strays from earlier pushes) and deletes them with `--delete`. Oct 8: both accounts clean (17 flows, 8 SMS campaigns, 37 templates, 6 lists, 14 segments, 6 forms each).

## Scheduled steps (routines, created Oct 8)

Each is a one-off routine that starts a fresh session, pulls this branch, runs one gated `push.py` step, commits `sync_state.json` and reports by push + email. Gated = it does nothing (prints "skipped") unless the flow it feeds is live, so nothing can send before Eli's go.

| When (local) | Step |
|---|---|
| Mon Oct 19 09:00 | `bulkadd unengaged sunset F8` (EU, US) |
| Mon Nov 2 | `suppress_sunset`: suppress Sunset-list profiles with no click in 14 days |
| Mon Nov 9 09:00 | `bulkadd second second F11` |
| Wed Nov 11 00:05 | `subjects` + publish pop-up Early access |
| Fri Nov 13 00:05 | `subjects` + publish pop-up Black Friday + Cyber Week |
| Sat Nov 14 09:00 | `bulkadd browsed salelive F10` |
| Mon Nov 16 09:00 | `bulkadd lapsed winback F7` |
| Tue Dec 1 00:05 | `subjects` (Cyber Week) |
| Sat Dec 5 09:00 | `release F10E3` |
| Mon Dec 7 00:05 | `subjects` + publish pop-up Christmas |
| Mon Dec 7 09:00 | `bulkadd lapsed winback F7 bulkadd second second F11` (top-up) |
| Fri Dec 11 00:05 | `subjects` + publish pop-up Last minute |
| Fri Dec 25 00:05 | `subjects` + publish pop-up After Christmas |
| Sat Jan 2 09:00 | `release F13E2` |

EU runs on Stockholm time, US on New York time. Reminders to this chat on Oct 18 (go for F8) and Oct 26 (go for everything else, Oct 27 09:00).

## Segments (audited Oct 8, profile counts EU / US)

| Segment | EU | US | Use |
|---|---|---|---|
| Engaged 30 days | 7,792 | 1,755 | too small for a sale; use only for a test send |
| Engaged 60 days | 14,329 | 3,494 | default campaign audience (was 30) |
| Engaged 90 days | 25,277 | 6,202 | key sale days (was "30 + 90") |
| Engaged 180 days | 52,606 | 10,774 | Black Friday, Cyber Monday, cut-off day |
| BIG send: engaged 180 days, or clicked / ordered in 2 years | 57,942 | 12,097 | Nov 27, Nov 30, Dec 10 only |
| Unengaged (Sunset): no click, real open, visit or order in 180 days, subscribed 90+ days | 6,435 | 1,317 | F8 bulk add Oct 19 (old rule would have taken 48,480 / 8,016) |
| Browsed 60 days, no order | 7,967 | 1,743 | F10 bulk add Nov 14 |
| Lapsed 120+ days | 15,720 | 4,713 | F7 |
| One order 30–119 days ago | 5,658 | 2,719 | F11 |
| Can receive SMS | 29,637 | 2,806 | S2 |
| On the Sunset list, no click in 14 days | 0 until Oct 19 | 0 | Nov 2 suppression |

## SMS and Gender (on push)

- SMS texts live inside the same Klaviyo flows (F2, F4, F5, F7, F9) behind a “can receive SMS” split, plus S1 SMS Welcome. S2 is eight SMS campaigns (S2C1–C8, drafts with send times), not a flow.
- Every text is checked by `gen_q4.py` to be plain GSM-7 and one segment (160 incl. 23-char link and the opt-out line).
- G1/G2 set the profile property `Gender`. Rule (both stores, every language): women's product names have a spaced hyphen (“Cube - Bracelet”), men's never do (“Cube Bracelet”). Orders: women's = Name contains ` - `, men's = Tags contain `man`/`men`/`mens sets` (add-ons like Jewelry Case and Lifetime Warranty have neither). Views: women's = Name contains ` - `, men's = Name without it. Klaviyo's API takes only one filter per metric condition, hence the split. They never overwrite an existing Gender; the order backfill uses the same rule.
- One-off backfill on the first push to each account: set `Gender` (+ `Gender source = order`) for existing customers with no Gender from their Ordered Product history, via the API.
- F7, F8, F11 are list-triggered: bulk-add their segments on the dates in each flow's trigger (F8 Oct 19, F11 Nov 9, F10 Nov 14, F7 Nov 16; F7/F11 top-up Dec 7); the routines above do it.

## Klaviyo push (done Oct 7, both accounts, all drafts)

`klaviyo/push.py EU|US [images templates lists segments flows dated campaigns backfill subjects | release <EID>]`; ids in `sync_state.json['klaviyo']`.
- 39 templates per account (`Q4 · F1E1 · …`), email-safe HTML from `klaviyo/emailer.py`; date phase + Gender logic inside; `klaviyo/rendertest.py` renders all through Klaviyo.
- 17 flows per account as drafts (F1–F8, F10–F13, S1, G1, G2 + the 2 dated ones below). F9 Back in Stock: build by hand (no API trigger), templates `Q4 · F9E1/E2` are ready.
- Fixed-date emails F10E3 (Dec 5 09:00) and F13E2 (Jan 2 09:00) are their own one-email draft flows (`Q4 · F10E3 · … · date`), triggered by lists `Q4 · Send <EID> · <date>`. The flow API has no "wait until date", so on the send date (flow live first) a routine runs `push.py EU|US release <EID>`: it adds the segment (On Sale live no order in 7 days / gift card buyers) to the list and the flow sends at once. Each flow skips anyone who orders after entering. F1E6/F1E7 and their lists were deleted (Oct 8): the campaigns cover Nov 11 and 13.
- The only Klaviyo campaigns are S2C1–C8, draft SMS campaigns. Email campaigns live on the Figma campaigns page and are built by hand.
- Lists `Q4 · Winback / Second purchase / Sunset / Sale live` + segments for the bulk adds.
- Subject/preview: Klaviyo caps them at ~250 characters incl. logic. Where the date logic doesn't fit, the flow carries the current period's text; the routines run `push.py EU|US subjects` on Nov 11, Nov 13, Dec 1, Dec 7, Dec 11 and Dec 25.
- Gender backfill from order history: done Oct 8–9 (approved). EU 10,966 + earlier run set (3,287 ordered profiles no longer exist), US 14,067 (76 gone). Profiles with Gender now EU 50,657, US 20,204 (were 9,793 / 6,029). `push.py EU|US backfill` can be rerun: it skips anyone who has a Gender.
- Pop-ups: `klaviyo/forms.py EU|US` built six draft forms per account (`Q4 Pop-up · Pre-sale` … `After Christmas`), built to the Figma design (two B/W photos as the side image, #F2F2F1 panel, logo, red kicker, light headline, black buttons, “Not now”, teaser tab), steps email → phone → who → done, shown after 5 s / exit intent / 2nd page, hidden from cart/checkout. `--replace` rebuilds them. Klaviyo limits: max 6 rows per column; the content column's styles must be null next to a side image; skip links must submit (they re-submit the email list). Publish the next one on each switch date and switch the previous one off.

## What stays manual

Going live (needs Eli's go: F8 on Oct 19, the rest Oct 27 09:00, old flows to Manual in the same hour) · publishing the pop-up for each period (the forms API only makes drafts; each switch routine reminds with the link) · building F9 Back in Stock by hand · filling `[[EARLY_ACCESS_URL]]` before Nov 11 · Shopify-side test events (view, cart, checkout, order on each store) · real back-in-stock restocks · the product-tracking fix on the themes.
