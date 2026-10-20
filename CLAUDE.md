# Cavaier Speed Ads Creator

Eli (Cavaier) makes Meta static and video ads on a canvas and drives the work with comments. This file is the working rulebook for any Claude session on this repo. The canvas Brief note carries the same rules for the team.

## Where things live
- **Canvas:** "Cavaier Static Ads Lab", https://claude.ai/artifact/PWhEp18Jbd4yd9WMA2kZto (Design canvas). Files: `project/canvas.json` plus one `project/*.dc.html` per artboard. Keep the `<script src="./support.js"></script>` line. Assets are uploaded to the artifact and referenced as `/_blob/<id>`. Re-read `canvas.json` before editing, because Eli edits it too.
- **Repo:** `Cavaier/Claude`, branch `claude/focused-davinci-41clp5`. `bfcm26/canvas/` holds the canvas backup, `bfcm26/tools/` the scripts, `bfcm26/video/` the Seedance inputs, prompts, drafts, finals, ads and `tasks.json`, and `bfcm26/frame/<Batch>/{EN,no text}/` the files that went to Frame.io. Back up the canvas and push after every change.
- **Language:** everything is in English: canvas, replies, ClickUp, deliverables.

## Canvas layout
- **Two sections:** BLACK FRIDAY on the left (x 0–18300) and EVERGREEN on the right (starts at x 19400).
- **Lanes:** each section has four: MEN statics (+0), MEN video ad sets (+4820), WOMEN statics (+9400) and WOMEN video ad sets (+14220).
- **Rows:** one batch per row, rows 2400 px apart. Columns inside a statics lane:

  | Column | x offset |
  |---|---|
  | IM8 refs | +0 (width 420) |
  | C1 | +500 |
  | C2 | +1660 |
  | C3 | +2820 |
  | Copy note | +3980 (width 600) |
  | Video C1 | +4820 |
  | Video C2 | +5980 |
  | Video C3 | +7140 |
  | Video copy note | +8300 |

- **Notes:** Brief (x -720), red COMMANDS note (x -720, y 1300), Evergreen rules (x 18680, y 0) and the blue ACTIVITY & QUEUE note (x 18680, y -1700).

## Choose the method first (every new batch)
Before making any new batch, always ask Eli which method to use, with one short question:

| Method | What it is | Rules |
|---|---|---|
| **Imitation** (current default) | C1–C3 each closely copy their own IM8 Health ad, using real Cavaier photos from Figma. | **Statics** below. ClickUp Creative Origin: Imitation. |
| **Ideation** | Our own concepts with our own generated images (OpenAI image model, real product photo + look reference). | **Ideation images** below. Creative Origin: Ideation. |
| **Frame Method** | Video ads cut from the real RAW footage on Frame.io, in the Vacier-style macro look: graded (skin sun-kissed / tanned, never pale), slow motion, white Figtree lockups, ElevenLabs music. | `bfcm26/video-ad/FRAME_METHOD.md` (full rules) and the tools in `bfcm26/video-ad/`. Creative Origin: Ideation. |

- **Ask the angle too, batch by batch.** Black Friday is one angle, not the default. Each new batch gets its angle and offer from Eli (Black Friday 30% off, Evergreen with no offer, or another angle). The copy, labels, red accent and ClickUp Style/Angle/Offer follow that answer. The Black Friday examples in FRAME_METHOD.md apply only when the batch is Black Friday.
- A comment on an existing ad (redo, video, 1080p, push…) never needs this question. Only new batches do.
- Whatever the method, the batch still goes through our system:
  - Canvas slot, ACTIVITY & QUEUE, IN PROGRESS box and status tags.
  - `M/W Batch ###` naming, copy note and ROAS/safe-zone check.
  - Backup and push.
  - Delivery via "push to clickup and frame".
- Frame Method, stills from video, video text and RAW session rules: read `bfcm26/docs/frame-method.md` before that kind of work.

## Workflow
1. **Commands:** Eli comments on an ad (C key) and sends it to Claude. A comment is the approval, so never ask again. Commands are redo, video, 720p/1080p, reject, mp4, "push to clickup and frame", or free text.
2. **Queue:** every comment goes onto ACTIVITY & QUEUE right away (QUEUED → RUNNING → DONE, with times).
   - Commands on the same ad merge, and the latest wins.
   - Seedance work arriving within ~2 min is sent as one job.
   - Update the note when a job starts and when it ends.
3. **In progress:** a blue IN PROGRESS box goes in the exact slot while it's being worked on.
4. **Status tags:** `bfcm26/tools/tags.py file "TEXT|color" …` puts a tag stack top left.
   - Labels: DRAFT · 480p (yellow), RENDERING (blue), FINAL · 1080p · SOUND (green), CLICKUP ✓ DONE and FRAME ✓ UPLOADED (green; blue while running).
   - The stack carries `data-tag="status"`, and render.js, split.js, strip.js and roas.js strip it from exports.
5. **Replies:** reply in the comment thread, resolve it, and keep the chat reply to one short line.

## Statics
- **Batches:**
  - A batch is one ad set: C1, C2 and C3, each copying its own IM8 Health ad closely.
  - Find them with Trendtrack `search_ads` (query "IM8 Health", brand, image, all statuses, sort by reach).
  - Text sits on the photo, never in a box over the product.
- **New batch tasks in ClickUp (Eli):** create the batch task as a subtask of the current parent (e.g. BF26), named only `M Batch` or `W Batch` with no number, and set right away **Editor = Eli** (field `f718a78d`, option `4a2dc5cb`) and **📸 Ad Type** (field `0d443f6d`: IMAGE `5ac86b91`, VIDEO `8683b62f`, IMAGE & VIDEO `69ad1397`, CAROUSEL `6c4a57d6`); without those two the automation does not fire (Eli). The ClickUp automation assigns the next batch number (numeric order of the whole ClickUp) and creates its Frame.io folders about 5 minutes later. Read the number back from ClickUp before naming the canvas boards, then fill the fields and C1–C3 rows.
- **Naming:**
  - Men: `M Batch ### - C#`. Women: `W Batch ### - C#`.
  - Black Friday men started at 467 and women at 415. Evergreen men start at 445.
  - Video batches take the next free number.
- **Photos:** pull fresh product photos for every new batch from the Cavaier Figma file (https://www.figma.com/design/dEEVzBXoylSdZoRs0gonHn/Cavaier?node-id=17-2, file key `dEEVzBXoylSdZoRs0gonHn`, node `17-2`). Photos already on the canvas may be reused, but never build a batch only from them: each new batch brings in new images that fit its IM8 reference (right product, finish and gender).
- **Products:** 3x Minimal Stack Set and 2x Duo Minimal Set. The 3x stack is three separate pieces: one flat polished cuff bangle, one box chain and one square chain (never call it a snake chain). A name with a dash ("3x Minimal - Stack Set") is the women's product, without a dash the men's. Men's ads use men's photos only, and men and women never mix.
- **Brand:**
  - Graphite monochrome (black, white, light grey) in Figtree. Headings are uppercase 300/400, labels uppercase with 0.1em letter spacing.
  - Keep it high-end and airy, never chunky (Eli approved M473 C1 as the reference): headline about 50 px, weight 300/400, letter spacing 0.04em; body about 27 px, weight 300, line height 1.6, narrow column (about 720 px); logo small (about 110 px wide); slim button (80 px tall, 22 px label); CTA buttons are square black blocks with no rounded corners, the same on women's and men's ads (no pill buttons); generous white space.
  - Keep backgrounds light. No large black or dark fields dominating the ad: black is for type, buttons and small accents.
  - Red `#A82C24` is only a small accent, only on light monochrome Black Friday layouts. Never red in Evergreen.
- **Figma "Static Ads 2" women's photos are mostly AI-generated (found Oct 18):** their Figma image-fill names say so ("Gemini_3_Nano_Banana_Pro…", "AI_image_generation…", "slightly_change_pose…", "Change_hand_pose…"). Check the fill name before using any Figma photo; only treat it as real when it is a camera file (DSC…, shoot names) or a Shopify listing image. The only real silver women's 3x stack photo is the Shopify studio shot 12616-41.
- **No generated images unless Eli asks (Eli, Oct 15):** the generated images kept failing, so every ad uses real photos (Figma, Shopify listing, or stills from the RAW footage). If a product or finish has no usable real photos left, tell Eli and offer another finish instead of generating one.
- **Ideation images:** only when Eli asks; rules in `bfcm26/docs/ideation-images.md`.
- **Format:** 1080×1920. Key text stays out of the top 270 px and the bottom 384 px.
- **True claims only:**
  - Waterproof; sweat and heat resistant.
  - Recycled 316L stainless steel.
  - Adjustable S/M/L.
  - Black, silver or gold.
  - "Case included" (never "free case").
  - Free shipping (both stores, confirmed by Eli).
  - Trustpilot 4.5, 3,000+ reviews.
  - No prices or currencies.
- **Black Friday is winter (Eli, Oct 18):** Black Friday is the end of November: cold, dark, rain or snow, cozy, holiday shopping. Concepts, copy and scene details (weather, plans, packing lists, captions) must fit that season; no sunny beach-day or summer framing in Black Friday concepts. But don't make cold, snow or weather the hook either (Eli rejected the W435 snow weather widget): keep the season neutral and sell the product and the offer.
- **Offers:** Black Friday is 30% off sitewide, no code needed. The prices on the website are already discounted, so NEVER say "taken off at checkout" (Eli: not true). Evergreen has no offer and no deadline.
- **Copy note per batch:** primary text, a headline and a description of 27 characters or less each, plus landing pages: EU `https://cavaier.com/products/<handle>`, US `https://us.cavaier.com/products/<handle>`. Handles: men's duo `2x-duo-minimal-set-for-him`, women's duo `2x-duo-minimal-set-for-her`, men's stack `3x-minimal-stack-set-for-him`, women's stack `3x-minimal-stack-set-for-her`.
- **ROAS check per ad** (roas.js + roas.py):
  - Contrast p10 ≥ 4.5, or ≥ 3 for text of 24 px and up.
  - Text inside y 270–1536.
  - Readable at feed size.

## Video, voice-over, delivery
- Seedance + ElevenLabs rules: `bfcm26/docs/video-voice.md`. ClickUp + Frame.io delivery: `bfcm26/docs/delivery.md`. Read the relevant one before that job.

## Token discipline (Eli, Oct 20)
- Load the detail docs only when the task needs them: `bfcm26/docs/video-voice.md` (Seedance, ElevenLabs), `bfcm26/docs/delivery.md` (ClickUp + Frame.io ids and steps), `bfcm26/docs/frame-method.md`, `bfcm26/docs/ideation-images.md`.
- Hand multi-step jobs (new batches, redos, delivery) to subagents or helper sessions, and ask them for a report of at most ~10 lines: what changed, file paths, ROAS pass/fail, open questions. No long tables or id dumps.
- Don't Read whole board HTML or big JSON into the chat. Use scripts/grep that print only what is needed. Check renders on one small contact sheet, not one image per ad.
- After every canvas change run `bfcm26/tools/sync.sh "<message>"` (backup + commit + push in one call).
- Chat replies: one or two short lines.
