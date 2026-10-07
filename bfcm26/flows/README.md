# Cavaier BFCM26 flows

5 Klaviyo flows, 14 emails, each in a women's (W) and a men's (M) version, Oct 27 – Dec 6, 2026.
Brief: *Cavaier BFCM 2026 Flows — Simple Brief* (docx, from Eli). Same process as the campaign (`../README.md`).

## The master

**The one master is the shared page: https://claude.ai/artifact/CAab5coU9rgBbEfatBgsEu**

- One row per flow email: the brief card (flow, trigger, timing, subject, preview, banner, audience, goal, note) and the email at 600px.
- The bar switches W / M and the date state (Pre-sale, Early access, Live, Dec 6). Emails that change with
  the date (Flow 0, Flow 1, Flow 4 #4) show that state; the rest show the only state they run in.
- Version A is the brief as written. New versions (B, C…) go to the right of A in each row, with a "Show" toggle.
- Live bar (who's online, what Claude is doing, activity log) works like the campaign page: any Claude session
  that edits the page sets `live/claude` and adds an `activity` doc (see `../README.md`). Keep the page's
  capabilities on republish (`db`, `room`, `user` with `profile`): omit `capabilities`.
- Never regenerate the page from `gen_flows.py`: it only seeded Version A. Edit the published page.
  `cavaier-bfcm26-flows.html` here is a snapshot.

## Figma

Page **"BFCM Flows (synced)"** (`359:2`) in the BFCM file. One frame per email × version × W/M × date state
(48 frames for Version A), named `NN-V-G-state · Subject`, with a brief block above each. Row = email.
The "Email Campaign" and "Email Flow" pages are not touched. Tools and the loop: `figma/RUNBOOK.md`.

## Built for Klaviyo

Every email is drawn the way Klaviyo will render it, and each brief card has a "Klaviyo" line with the
trigger metric, the event fields and the show/hide logic. Checked on the Klaviyo account with a temporary
test template (rendered, then deleted): the `today` tag for the date switch, `find_replace` ("Stack Set" →
"Set"), the loop over `event.extra.line_items`, and `person|lookup:'Gender'`.
- Browse: Viewed Product. Cart: Shopify "Added to Cart" (the API metric stopped on Sep 2). Checkout: Shopify
  "Checkout Started" (the API "Started Checkout" has no names or images).
- No fixed prices in static cards (multi-currency list; 30% comes off at checkout). Dynamic blocks print the
  event price; checkout emails show the discount line and total.

## Open items

Listed on the page under "Open items": timezone of the `today` date switch, Trustpilot quotes
(Katrina), holiday delivery cut-off (CEO), Matte Cuff photos (from Nov 28 swaps not drawn), neutral version
for Flow 0, pop-ups not on the page yet.
