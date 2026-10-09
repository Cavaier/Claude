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
- **Naming:**
  - Men: `M Batch ### - C#`. Women: `W Batch ### - C#`.
  - Black Friday men started at 467 and women at 415. Evergreen men start at 445.
  - Video batches take the next free number.
- **Products:** 3x Minimal Stack Set and 2x Duo Minimal Set. A name with a dash ("3x Minimal - Stack Set") is the women's product, without a dash the men's. Men's ads use men's photos only, and men and women never mix.
- **Brand:**
  - Graphite monochrome (black, white, light grey) in Figtree. Headings are uppercase 300/400, labels uppercase with 0.1em letter spacing.
  - Red `#A82C24` is only a small accent, only on light monochrome Black Friday layouts. Never red in Evergreen.
- **Format:** 1080×1920. Key text stays out of the top 270 px and the bottom 384 px.
- **True claims only:**
  - Waterproof; sweat and heat resistant.
  - Recycled 316L stainless steel.
  - Adjustable S/M/L.
  - Black, silver or gold.
  - "Case included" (never "free case").
  - Free shipping.
  - Trustpilot 4.5, 3,000+ reviews.
  - No prices or currencies.
- **Offers:** Black Friday is 30% off sitewide, no code, taken off at checkout. Evergreen has no offer and no deadline.
- **Copy note per batch:** primary text, a headline and a description of 27 characters or less each, plus landing pages: EU `https://cavaier.com/products/<handle>`, US `https://us.cavaier.com/products/<handle>`. Duo for men: `2x-duo-minimal-set-for-him`.
- **ROAS check per ad** (roas.js + roas.py):
  - Contrast p10 ≥ 4.5, or ≥ 3 for text of 24 px and up.
  - Text inside y 270–1536.
  - Readable at feed size.

## Video (Seedance 2.5, BytePlus ModelArk)
- **Model and key:** model `dreamina-seedance-2-5-260628`, env `SEEDANCE_API_KEY` only. Never print keys. API: `POST https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks`, poll `GET …/tasks/<id>`.
- **Draft:** text prompt + `first_frame` image (base64 data URL), `duration 5`, `draft true`, `resolution "480p"`, `generate_audio true` (always sound), `watermark false`. Never send `ratio`.
- **Final:** `content:[{type:"draft_task", draft_task:{id}}]` with the resolution Eli writes. Do NOT add `generate_audio`, because the API rejects it on draft_task and the final inherits the draft's sound. A silent draft can't become a sound final. 720p was once refused for draft_task; if that happens, tell Eli.
- **Motion:** gentle slow motion only, and the jewelry keeps its shape and count. No sparkles or flares.
- **Pipeline:**
  - `split.js` makes `_bg.png` (the photo for Seedance) and `_ov.png` (the text layer). `compose.sh` lays the text over the clip at 1080×1920 and keeps the audio.
  - On card layouts, only the photo moves, inside its fixed frame (ffmpeg overlay at the photo box).
  - The static stays live as its own ad.
- **Helper sessions:** new env vars only show up in new sessions. Run Seedance and Frame.io jobs in a fresh helper session (`create_session`, same env and branch) with the full task in its first prompt, then read the result with `list_events`.

## Delivery ("push to clickup and frame")
- **Frame.io:**
  - Exchange `FRAMEIO_TOKEN` (an Adobe refresh token) at `https://ims-na1.adobelogin.com/ims/token/v3`, with `FRAMEIO_OAUTH_CLIENT_ID` and `FRAMEIO_OAUTH_CLIENT_SECRET`.
  - Then use the V4 API `https://api.frame.io/v4` with a custom User-Agent (the default Python UA gets 403). Project `9db7c232-de65-4e59-99e7-4fd3c3155ac7`.
  - The batch folder link is the Creatives field on the ClickUp batch task. Inside it, the version with text goes to the existing `EN` folder and the clean version to `No Text`. Never create folders.
- **ClickUp (Cavaier → Ads → Ads, under the week task, e.g. "Week 40"):**
  - **Batch task** fields:

    | Content | Field name | Field ID |
    |---|---|---|
    | Primary text | Preview Text | `2d5ca05c` |
    | Headline | Subject Line | `7d30ba47` |
    | Description | Description | `b416b8ee` |
    | EU URL | EU URL | `f2627d19` |
    | US URL | US URL | `5d08f6f8` |

  - **C1–C3 rows:** set Creative Style `751230a2`, Angle `80f8a7e8`, Creative Origin `1971e67f` (Imitation for IM8-based work, video versions included), Funnel Stage `498a0712` and Offer `1ce1ec23`. Add one short, clean comment: the IM8 ad it imitates plus what it tests. No tool names (Seedance, Claude). No Frame links in the rows. Don't rename rows or change Editor/status unless asked.
