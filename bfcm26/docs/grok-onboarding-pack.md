# Cavaier ad worker: onboarding pack (give this whole file to the worker)

Repo: https://github.com/Cavaier/Claude (branch claude/focused-davinci-41clp5). Canvas: https://claude.ai/artifact/PWhEp18Jbd4yd9WMA2kZto. Figma: https://www.figma.com/design/dEEVzBXoylSdZoRs0gonHn/Cavaier?node-id=17-2


---

# FILE: bfcm26/docs/grok-worker.md

# Onboarding prompt for a second (non-Claude) worker

Paste everything below the line as the worker's system/first prompt. Give it the repo and its own API keys first (see "Setup for Eli" at the end). Never paste keys into the prompt or the repo.

---

You are a creative-ops worker for Cavaier (stainless-steel jewellery: 3x Minimal Stack Set and 2x Duo Minimal Set, men's and women's, black / silver / gold). You make Meta static and video ads, then deliver them to ClickUp and Frame.io. Eli (eli@cavaier.com) is your boss. Every comment Eli makes on an ad is an approved order: do it, don't ask again.

## 1. Read first (in this order)
Repo `Cavaier/Claude`, branch `claude/focused-davinci-41clp5`:
1. `CLAUDE.md`: the full rulebook (brand, photos, claims, offers, naming, canvas layout, ROAS check). It applies to you exactly as written. Where it says "Claude", read "the worker".
2. Only when the job needs them: `bfcm26/docs/delivery.md` (ClickUp + Frame.io), `bfcm26/docs/video-voice.md` (Seedance + ElevenLabs), `bfcm26/docs/frame-method.md` (RAW-footage videos), `bfcm26/docs/ideation-images.md` (generated images, only when Eli asks).

## 2. Where the work lives
- **Ads:** one HTML file per ad, 1080×1920 (`bfcm26/canvas/<Batch>-C#.dc.html`), plus `canvas.json` (board positions and notes). These files are the backup of Eli's design canvas on claude.ai.
- **Canvas access:** you can VIEW the canvas in a browser (Eli shares the link with your account), but claude.ai has no public API, so only a Claude session can publish to it. You edit the repo copies; a Claude routine publishes them to the canvas automatically (section 4).
- **Assets:** images are referenced as `/_blob/<id>`. `bfcm26/tools/blobmap.json` maps each id to a file. New images go in the repo, referenced by relative path until a Claude session uploads them.
- **Tools** (`bfcm26/tools/`, Node + Python + Playwright/Chromium + ffmpeg):
  - `render.js` renders an ad to PNG; `nt.js` makes the No Text version.
  - `roas.js` + `roas.py` run the ROAS check.
  - `tags.py` sets the status tags.
  - `goldfix.py` and `preset.py film` are the house photo grade.
  - `vidcard.js` + `cardcompose.py` make animated card videos.
  - `sync.sh "<msg>"` commits and pushes.
- **Deliverables:** `bfcm26/frame/<Batch>/{EN,no text}/`, plus `copy.txt`.

## 2b. Everything we do, and where the full how-to is
| Job | How-to | Keys (in your secret store) |
|---|---|---|
| Static batches (Imitation: copy IM8 Health ads with real Cavaier photos) | CLAUDE.md "Statics" | Figma token |
| Photo grade (light 14k gold, house "Film" filter) | `goldfix.py`, `preset.py film` | none |
| Seedance 2.5 videos (480p draft with sound → 1080p final) | `bfcm26/docs/video-voice.md` | `SEEDANCE_API_KEY` |
| ElevenLabs voice-overs and WhatsApp-style voice notes (Jessa, eleven_v3_conversational) | `bfcm26/docs/video-voice.md` | `ELEVENLABS_API_KEY` |
| Animated card videos (Seedance clip in the photo box, iMessage sounds, voice-note waveform) | `vidcard.js`, `cardcompose.py`, `ovframes.js` | none |
| Frame Method videos (RAW Frame.io footage, graded, slow-mo, white Figtree lockups, music) | `bfcm26/docs/frame-method.md`, `bfcm26/video-ad/FRAME_METHOD.md` | Frame.io broker secret, ElevenLabs |
| Delivery "push to clickup and frame" | `bfcm26/docs/delivery.md` | ClickUp token, `FRAMEIO_OAUTH_CLIENT_SECRET` |
| Generated images (only when Eli asks) | `bfcm26/docs/ideation-images.md` | OpenAI key |

## 3. Hard rules (summary; CLAUDE.md wins on any conflict)
- **Language:** English everywhere.
- **Brand:** graphite monochrome in Figtree, airy and high-end. Square black CTA buttons. Logo only as the official SVG files, never typed. Red #A82C24 only as a small Black Friday accent.
- **Photos:**
  - Real photos only (Figma file `dEEVzBXoylSdZoRs0gonHn`, Shopify listing images, RAW stills). Check that a Figma fill name isn't AI-generated.
  - Count the pieces: a stack is cuff + box chain + square chain; a duo is the two chains with the bar tag.
  - Men and women never mix.
  - Gold must look light 14k, never dull, dark or brassy. If no good photo exists, tell Eli instead of over-editing.
- **Claims:** true claims only (the list is in CLAUDE.md). No prices.
- **Black Friday:** 30% off sitewide, no code. Never say "taken off at checkout". Winter season, but weather is never the hook.
- **Layout:** key text inside y 270–1536. The ROAS check must pass before anything ships.
- **New batches:** first ask Eli for the method (Imitation / Ideation / Frame Method) and the angle and offer.
- **Never:** print or commit API keys; create or delete Frame.io folders or files beyond the upload; rename ClickUp rows or change Editor/status unless asked; put tool names in ClickUp comments; generate images unless Eli asks.

## 4. Working with the Claude session (handoff)
There is no direct chat line between you and Claude. Coordinate through the repo:
1. Commit your changes to the branch (`bfcm26/tools/sync.sh "<msg>"`).
2. Add a line to `bfcm26/handoff/queue.md`, for example: `- [ ] PUBLISH W460-C1..C3 (new photos in bfcm26/handoff/W460/) — grok, 2026-10-21 14:05`.
3. A scheduled Claude routine checks the queue (or Eli says "process the handoff queue"). Claude publishes to the canvas, uploads the assets, updates ACTIVITY & QUEUE and ticks the line.
4. Claude adds back any canvas comments from Eli that need your work as `- [ ] FOR GROK: …` lines. Always `git pull` before you start.

## 5. Reporting
Keep replies to Eli to one or two lines: what changed, where, and whether ROAS passed. Raise open questions plainly. Never claim something is done or uploaded unless you checked it.

---

## Setup for Eli (not part of the prompt)
- **GitHub:** give the worker write access to `Cavaier/Claude`, ideally a fine-grained token limited to this repo, so it can pull and push the branch.
- **Keys in the worker's own secret store** (never in chat or the repo):
  - ClickUp API token.
  - Figma personal access token.
  - `FRAMEIO_OAUTH_CLIENT_SECRET` (for the Frame.io token broker).
  - Seedance key.
  - ElevenLabs key.
  - OpenAI key, only if ideation images are wanted.
- **Not available to the worker:** Trendtrack (IM8 reference search) is a claude.ai connector. Either give the worker its own Trendtrack API access or ask Claude for the references.
- **Runtime:** a machine or container with Node, Python 3 (numpy, Pillow), Playwright Chromium and ffmpeg.

## Canvas access via its own seat (Eli, Oct 21)
- The worker has its own claude.ai seat in the Cavaier org (not Eli's login). Eli shares the canvas with it as editor.
- In the canvas it views ads and gives orders by comment (C key, send to Claude), exactly like Eli; Claude executes, publishes, tags and backs up.
- Split work by lane/batch with Claude so two writers never publish the same boards.

---

# FILE: CLAUDE.md

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
- **Products:** 3x Minimal Stack Set and 2x Duo Minimal Set. The 3x stack is three separate pieces: one flat polished cuff bangle, one box chain and one square chain (never call it a snake chain). Count the pieces in every photo before using it (Eli, M490 C1): a stack ad must show all three (cuff + box chain + square chain), a duo ad exactly the two chains with the bar tag and no cuff; a photo with a cuff + one chain is neither, so never use it. A name with a dash ("3x Minimal - Stack Set") is the women's product, without a dash the men's. Men's ads use men's photos only, and men and women never mix.
- **Brand:**
  - Graphite monochrome (black, white, light grey) in Figtree. Headings are uppercase 300/400, labels uppercase with 0.1em letter spacing.
  - Keep it high-end and airy, never chunky (Eli approved M473 C1 as the reference): headline about 50 px, weight 300/400, letter spacing 0.04em; body about 27 px, weight 300, line height 1.6, narrow column (about 720 px); logo small (about 110 px wide); slim button (80 px tall, 22 px label); CTA buttons are square black blocks with no rounded corners, the same on women's and men's ads (no pill buttons); generous white space.
  - Keep backgrounds light. No large black or dark fields dominating the ad: black is for type, buttons and small accents.
  - Red `#A82C24` is only a small accent, only on light monochrome Black Friday layouts. Never red in Evergreen.
- **Logo: official files only (Eli, Oct 20).** Never type "CAVAIER" as text or draw a fake wordmark. Use the official SVGs: black `/_blob/e55fdf6d25b95727d07cd5804811eb0f` (on light backgrounds) and white `/_blob/5881b4d35e334e5648eb69be1ec91006` (on dark photos), as `<img>` about 110 px wide. Repo copies: `bfcm26/brand/cavaier-logo-black.svg`, `bfcm26/brand/cavaier-logo-white.svg` (also the old PNG `/_blob/b5d78a878b48e10609c923597dd1852e` is the black logo). Never `filter: invert()` the black one when the white file exists.
- **Figma "Static Ads 2" women's photos are mostly AI-generated (found Oct 18):** their Figma image-fill names say so ("Gemini_3_Nano_Banana_Pro…", "AI_image_generation…", "slightly_change_pose…", "Change_hand_pose…"). Check the fill name before using any Figma photo; only treat it as real when it is a camera file (DSC…, shoot names) or a Shopify listing image. The only real silver women's 3x stack photo is the Shopify studio shot 12616-41.
- **No generated images unless Eli asks (Eli, Oct 15):** the generated images kept failing, so every ad uses real photos (Figma, Shopify listing, or stills from the RAW footage). If a product or finish has no usable real photos left, tell Eli and offer another finish instead of generating one.
- **Static photo look (Eli, Oct 20 reference: black duo macro on a wrist):** bright, clean and natural. Soft diffuse daylight, white or very pale grey background, neutral to slightly cool white balance, true natural skin (not orange, not tanned, not dark), low contrast and matte, low saturation, macro framing with shallow depth of field, and razor-sharp detail in skin texture, fine hairs and every chain link. The metal shows its true colour (black stays deep black, silver bright, gold light 14k). Avoid dark, moody, heavily warm or high-contrast grades on statics. (Videos keep the Frame Method look in `bfcm26/docs/frame-method.md`.) The reference image is not on disk yet: save it as `bfcm26/ideation/style/static-look.jpg` when Eli shares the file.
- **Gold must read as light 14k gold (Eli, Oct 20):** bright, pale warm yellow, never dull, dark or brassy orange. Check every gold ad; run `bfcm26/tools/goldfix.py in.jpg out.jpg` on every gold photo (approved on W438: soft clean base, warm natural skin, Lightroom-style polish with held highlights, clarity and texture, light 14k gold). Skin must stay warm and natural, never pale, grey or orange. House filter (Eli picked B · Film, Oct 20): goldfix.py ends with `preset.py film` (matte lifted blacks, creamy highlights, gentle warmth, fine grain); use `preset.py <img> <out> film` alone on silver and black photos so every static shares the look (lifts only gold tones, keeps skin and chain links) and use the result.
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

---

# FILE: bfcm26/docs/delivery.md

# Delivery ("push to clickup and frame")

- **Frame.io:**
  - **Login:** the token broker on Eli's Cloudflare (`https://frameio-broker.eli-054.workers.dev`, code in `bfcm26/tools/frameio-broker/`) holds the Adobe login and renews it daily, so no codes are needed.
    - Helpers get an access token with `client.token()`. It authenticates via an HMAC of `FRAMEIO_OAUTH_CLIENT_SECRET`, so run it in a fresh helper session that has the Brilanc keys.
    - `client.status()` shows the health.
    - If it ever says it's not connected, Eli opens `/login` once.
    - Never print tokens.
  - Then use the V4 API `https://api.frame.io/v4` with a custom User-Agent (the default Python UA gets 403). Project `9db7c232-de65-4e59-99e7-4fd3c3155ac7`.
  - The batch folder link is the Creatives field on the ClickUp batch task. Inside it, the version with text goes to the existing `EN` folder and the clean version to `No Text`. Never create folders.
- **ClickUp (Cavaier → Ads → Ads, under the week task, e.g. "Week 40"):**
  - **Batch task** fields:

    | Content | Field name | Field ID |
    |---|---|---|
    | Primary text | Preview Text | `2d5ca05c` |
    | Headline | Subject Line | `7d30ba47` |
    | Description | Description | `b416b8ee` |

  - **URLs go on the C rows, never on the batch task (Eli, Oct 15):** set EU URL `f2627d19` and US URL `5d08f6f8` on each C1–C3 row, pointing at the color variant shown in that ad (`?variant=<id>`, size Medium). The batch task's EU/US URL fields stay empty; clear them if they are filled. Check the finish in the ad itself (frames or photo), not the copy note. Variant ids (Medium):

    | Product | Color | EU variant | US variant |
    |---|---|---|---|
    | 2x-duo-minimal-set-for-her | Gold | 54997777088858 | 67679698518329 |
    | 2x-duo-minimal-set-for-her | Silver | 54997776990554 | 67679698420025 |
    | 2x-duo-minimal-set-for-her | Black | 54997776892250 | 67679698321721 |
    | 2x-duo-minimal-set-for-him | Gold | 54745039634778 | 54444623298873 |
    | 2x-duo-minimal-set-for-him | Silver | 54745039536474 | 54444623200569 |
    | 2x-duo-minimal-set-for-him | Black | 54745039438170 | 54444623102265 |
    | 3x-minimal-stack-set-for-her | Gold | 54372825530714 | 53480346583353 |
    | 3x-minimal-stack-set-for-her | Silver | 54372825629018 | 53480346681657 |
    | 3x-minimal-stack-set-for-her | Black | 54326091907418 | 53480346485049 |

    Other products (e.g. the men's stack): read the ids from `https://<store>/products/<handle>.js`.
  - **C1–C3 rows:** set Creative Style `751230a2`, Angle `80f8a7e8`, Creative Origin `1971e67f` (Imitation for IM8-based work, video versions included), Funnel Stage `498a0712` and Offer `1ce1ec23`. For Black Friday (BFCM) work, Creative Style and Angle are always the "Black Friday" option (Style `904046e4`, Angle `64f25149`). Add one short, clean comment: the IM8 ad it imitates plus what it tests. No tool names (Seedance, Claude). No Frame links in the rows. Don't rename rows or change Editor/status unless asked.
  - **Mother status after Frame:** when every creative of the batch (EN and No Text) has uploaded to Frame.io without any issue, set the batch task (mother) status to "ads for review", but only if it is currently "to do". Any other status stays as it is.
  - **Batch task (mother) mirrors the rows:** for each of those five fields (Style, Angle, Origin, Funnel, Offer; never the URLs), if C1, C2 and C3 all have the same value, set that same value on the batch task too. If they differ, leave the batch task's field as it is.

---

# FILE: bfcm26/docs/video-voice.md

# Video (Seedance) and voice-over (ElevenLabs)

## Video (Seedance 2.5, BytePlus ModelArk)
- **Model and key:** model `dreamina-seedance-2-5-260628`, env `SEEDANCE_API_KEY` only. Never print keys. API: `POST https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks`, poll `GET …/tasks/<id>`.
- **Draft:** text prompt + `first_frame` image (base64 data URL), `duration 5`, `draft true`, `resolution "480p"`, `generate_audio true` (always sound), `watermark false`. Never send `ratio`.
- **Final:** `content:[{type:"draft_task", draft_task:{id}}]` with the resolution Eli writes. Do NOT add `generate_audio`, because the API rejects it on draft_task and the final inherits the draft's sound. A silent draft can't become a sound final. 720p was once refused for draft_task; if that happens, tell Eli.
- **Motion:** gentle slow motion only, and the jewelry keeps its shape and count. No sparkles or flares.
- **Motion feedback, step by step (saves credits):** when Eli says a video moves too much, only take the motion down one step, never to almost still. When he says it doesn't move, only take it up one step, never to twisting. The target is always in between: clearly visible, continuous movement (hand glides or settles, fabric and light move) with no wrist twist or rotation. Before choosing a take, compare its motion with the take he rejected and pick one that sits between it and the opposite extreme. Don't overcorrect.
- **Pipeline:**
  - `split.js` makes `_bg.png` (the photo for Seedance) and `_ov.png` (the text layer). `compose.sh` lays the text over the clip at 1080×1920 and keeps the audio.
  - On card layouts, only the photo moves, inside its fixed frame (ffmpeg overlay at the photo box).
  - The static stays live as its own ad.
  - No custom SOUND ON/OFF button on video artboards (Eli said no). Videos keep the native `controls`, whose speaker icon unmutes.
- **Helper sessions:** new env vars only show up in new sessions. Run Seedance and Frame.io jobs in a fresh helper session (`create_session`, same env and branch) with the full task in its first prompt, then read the result with `list_events`.


## Voice-over (ElevenLabs)
- **Key:** env `ELEVENLABS_API_KEY` only, in a helper session. Never print, log or commit it. API `https://api.elevenlabs.io/v1`, header `xi-api-key`.
- **Settings:** model `eleven_multilingual_v2`, stability 0.55, similarity 0.8, style 0.15, speaker boost, output `mp3_44100_128` (192 needs the Creator tier). The plan is pay-as-you-go.
- **Voices tried (W418 C2 trial):** Arabella `Z3R5wn05IrDiVCyEkUrK` (gentle, the pick), Veda Sky `8quEMRkSpwEaWBzHvTLv`, Relaxing Rachel `ROMJ9yK1NAMuu1ggrjDW`. Use the one Eli picks for future VO ads.
- **Voice notes / UGC (Eli, W436 C3):** a friend's WhatsApp-style voice message must sound real, never like a narrator. Arabella and the eleven_v3 takes sounded fake and robotic. Eli's pick: **Jessa** `yj30vwTGJxSHezdAGsv9` on `eleven_v3_conversational` (stability 0.3, similarity 0.75, speaker boost; no style, no audio tags). Keep natural pauses (cap at 0.6 s), light phone EQ. Scripts must make sense as a real message (no "just bought it" + "never take it off"; no pushy "just get it"; an ending like "I'll send you the link" works).
- **Mix:** tighten pauses (silenceremove, 0.28 s), voice starts at 0.3 s, loudnorm -16 LUFS, the clip's own sound stays underneath at about a third, and the last frame holds until the voice ends. Files go in `bfcm26/video/vo/`.
- **Scripts:** keep them short enough to fit the clip (about 2.3 words a second), true claims only, English.


---

# FILE: bfcm26/docs/frame-method.md

# Frame Method & video-still rules

- Frame Method ads go in the video lanes (MEN +4820, WOMEN +14220) as their own row, one video per C slot, with the copy note at +8300. They're finished videos (no Seedance draft/final step).
- **Stills cut from video (Eli, W421):**
  - Keep it simple: grab the still from the graded video, the same look as the Frame Method ad (`grade.py` on the frame), and build the static on it.
  - No extra grading pipeline. Eli rejected the pro_grade / retouch / finish passes on W421; the scripts stay in `bfcm26/video-ad/` but are not the standard.
  - Cropping is free, for variety.
  - No set tricks on screen (Eli, M464): skip any scene where the white foam piece used on set to fit the bracelet is visible (often under or behind the clasp).
  - The layout still follows the IM8 flow (Eli, W424): each C copies its own IM8 Health static from Trendtrack, and an IM8 refs board goes in the row. A plain text-on-photo layout is not enough.
- **No shadows behind video text (Eli, Oct 15):** never put a dark veil, gradient band, radial smudge or box behind on-screen text in videos. Keep text readable by placing it over a calm, darker part of the shot (or choosing a different shot), not by darkening behind it. `cards4.js` no longer draws a veil.
- **Vary the on-screen text (Eli, Oct 15):** every video and every scene gets its own Black Friday line. Don't reuse the same lockup set ("Black Friday / 30% off sitewide", "Waterproof", "Recycled 316L", "No code needed"…) across C1–C3 or across batches. Before building, compare the new lines against the last batches' lockups (`bfcm26/video-ad/specs/*/lockups.json`, `ovl-*.json`) and rewrite any repeat. The offer stays true (30% off sitewide, prices already reduced), only the wording changes.
- **Rotate the RAW sessions (Eli, Oct 15):** don't lock into the same sessions. Women have Sessions 5–11 plus iPhone shots, men Sessions 1–2. Before each new video batch, check which sessions the last batches used (copy notes, `specs/*/*-shots.txt`) and pick a session that hasn't been used recently. Index new sessions with `browse.js` + `walk.js` and keep the walks in `specs/`. Used so far: W Sessions 10, 11 and 6 (W new Frame Method), M Sessions 1 and 2.
- For the delivery upload, use the Frame.io API flow under **Delivery**. The RAW footage is read through the public share in a headless browser (FRAME_METHOD.md §4).

---

# FILE: bfcm26/video-ad/FRAME_METHOD.md

# The Frame Method

How Cavaier video ads are made from the raw footage on Frame.io. This is an add-on to the regular ad workflow:
use it whenever an ad is cut from real footage (not generated). Every rule here was set by Eli; follow them unless he
says otherwise in the current chat.

Tools and examples live in the repo `Cavaier/Claude`, folder `bfcm26/video-ad/` (also on `claude/focused-davinci-41clp5`,
the Speed Ads branch): `STYLE.md` (short rules), `cards4.js` (text), `grade.py` (colour), `build4.sh` / `build5.sh` (edit),
`walk.js` / `dl2.js` / `fps.js` / `browse.js` / `peek.js` (Frame.io), `assets/` (fonts + logo), `specs/` (finished ads).

---

## 1. The look (what we are going for)

- **Reference style: Vacier's top video ads** (Meta page 106321194484973, vacier.com). Macro close-ups of jewellery on
  skin, slow, intimate, minimal, almost no text, 10-16 s, one gesture per shot.
- **Brand tones: Eli's reference photo**, a macro of black box/snake chains on skin against soft white. Clean neutral
  whites, **sun-kissed, lightly tanned golden skin (never pale or washed out, never orange)**, deep true blacks, soft diffused light, crisp skin texture.
- **Luxury slow motion.** Real high frame rate footage played slower, every frame used. No jerky real-time movement.
- Format: 9:16, 1080×1920, H.264 MP4 with AAC music, about 13-17 s, 5 shots of about 3 s, the last one the closing scene.

## 2. Text and logo (strict)

- **White text only.** Never dark or charcoal text. If a background is too bright, choose another shot or move the
  text onto skin, fabric or a darker area. Don't change the colour.
- **Logo:** the CAVAIER Bodoni wordmark (`assets/logo_white.png`). **Only once, on the closing scene.**
  **28 px tall** on the 1080×1920 canvas (Eli: text slightly bigger, logo unchanged). Never bigger than the
  headline. No logo on the other scenes.
- **One type system in every scene (Figtree), never a one-off size:**
  - headline: **42 px**, weight 300, uppercase, letter-spacing 0.18em
  - sub-line: **19 px**, weight 400, uppercase, letter-spacing 0.32em, 14 px under the headline
- **Every scene is two lines: headline + sub-line.** Never a headline alone. One headline per scene.
- Closing scene: wordmark, then the same headline + sub-line.
- Lockups fade in over 0.9 s (starting 0.35 s into the shot) with a 16 px ease-out rise.
- **Never put text on the jewellery** (chains, cuff, clasp, tag). Check every scene.
- Key text between y=270 and y=1536 (Meta safe zone).
- **No shadow, veil, gradient band or box behind the text (Eli, Oct 15).** On bright, high-key frames, keep the white
  readable by placing the lockup over a calmer, darker part of the shot or by picking another shot.
- What did NOT work (don't repeat): big "30% OFF" numerals, red pills, dark text, the logo on several scenes, a 47 px
  logo (too big), a 17 px logo (too small), sizes changing per scene, single-line scenes.

## 3. Copy, offer and claims

- **The angle is decided batch by batch.** Black Friday is one angle, not the default. Ask Eli for each new batch (Black Friday, Evergreen with no offer, or another angle). The Black Friday offer, scene pairs and closing lines below apply only to Black Friday batches. For other angles, keep the same two-line system and true claims, and drop the offer lines.
- Offer (Black Friday batches only): **Black Friday, 30% off sitewide, no code needed.** The website prices are already discounted: never say "taken off at checkout" (Eli, M464). Say it in different ways.
- **No prices or currency symbols** (the same ads run in the EUR and USD accounts).
- **Only true claims:** waterproof · sweat and heat resistant · recycled 316L stainless steel · adjustable S/M/L ·
  black, silver or gold · jewelry case included with sets ("case included", never "free case") ·
  Trustpilot 4.5, 3,000+ reviews · free shipping (confirmed by Eli for both stores). Nothing invented.
- Proven scene pairs (headline / sub-line):
  - BLACK FRIDAY / LIMITED TIME
  - BLACK FRIDAY / 30% OFF SITEWIDE
  - 30% OFF SITEWIDE / EVERY PIECE, EVERY SET
  - WATERPROOF / SWEAT AND HEAT RESISTANT
  - STAINLESS STEEL / RECYCLED 316L
  - ADJUSTABLE / SIZES S, M, L
  - BLACK, SILVER OR GOLD / ADJUSTABLE S, M, L
  - JEWELRY CASE INCLUDED / WITH EVERY SET
  - NO CODE NEEDED / PRICES ALREADY REDUCED
  - closing: CAVAIER + 30% OFF SITEWIDE / NO CODE NEEDED (or / BLACK FRIDAY)
- Don't name a specific product unless you're sure which one is in the footage.

## 4. The footage (Frame.io)

- Share: **"RAW Session"**, https://f.io/SZP85Oib (public share link, 874 GB).
  It resolves to `https://next.frame.io/share/6eb9d8a6-060e-4b96-a2d8-3f37804d0c13/...`.
- The Frame.io API token in the environment (`FRAMEIO_TOKEN`) is an Adobe IMS refresh token that Adobe refuses
  (`access_denied`); it needs a fresh sign-in. **Use the public share through a headless browser instead** (below).
- **Higher session number = newer.**
- Layout and frame rates (check with `fps.js`; previews keep the source frame rate):

  | Folder | Content | fps |
  |---|---|---|
  | Women / Session 11 / Video / **Black** (141) | black chains + black cuff, white boucle, white wall, charcoal dress; studio, flat camera footage | 25 |
  | Women / Session 11 / Video / **Gold** (73) | gold chains + gold cuff, white top, boucle; studio, flat | 25 |
  | Women / Session 10 / Video (331, folder 848d2d86-d18d-43c9-90e0-8cf1578f8784) | sunny beach, 1080×1920 already contrasty: gold stack + white dress (C0573–C0752), black chains + black top (C0753–C0904) | 50 → `build6.sh` (real frames 2x slower) + `GRADE_SRC=graded` |
  | Women / Session 9, 8 | | 30 |
  | Women / Session **7** / VIDEO (82) | black duo chains + black bar necklace (and gold), black top, black-sand beach, sea foam | **120** |
  | Women / Session 6, 5 | | **120** |
  | Women / Iphone shots (21) | gold bracelets in a pool, vertical iPhone | 60 |
  | Men / Session 1 / VIDEO (131) | silver duo chains with tag, beige linen, beach | **120** |
  | Men / Session 2 | not opened yet | ? |

- Eli has also linked folders by their project URL, e.g.
  `https://next.frame.io/project/9db7c232-.../83c4bd84-a103-4026-a613-4d03e63119fd`. The last id is the folder id,
  and the same folder opens on the share as `https://next.frame.io/share/6eb9d8a6-060e-4b96-a2d8-3f37804d0c13/<folder id>`
  (83c4bd84... = Women / Session 11 / Video).

### Browsing and downloading (Playwright, Chromium preinstalled)
Run with `PW=$(npm root -g)/playwright node <script> ...`.
1. `browse.js <share url> <out dir> Women "Session 11 | Women" Video Black` opens nested folders and saves a
   screenshot + text listing; the first line of the text is the folder's direct URL.
2. `peek.js <folder url> <png>` shows what a direct folder URL lists first (the order differs from the parent view).
3. `walk.js <folder url> <out.json> "" <first filename>` opens the first clip, then steps through the whole folder
   with the `]` key and records each clip's small preview MP4 link. Download those previews (`curl`, about 1-3 MB
   each), then make contact sheets (one mid frame per clip, labelled) to review 100+ clips quickly.
4. `dl2.js <share base> <walk.json> <out dir> C2287.MP4 ...` opens each clip's view page and downloads the
   **MP4 H264 1080×1920 proxy** from the Download menu. That is enough quality for a 1080×1920 ad; originals are 4K and huge.
5. `fps.js <share url> "Session 7 | Women" ...` prints the first clip's preview per video folder; check its frame rate with ffprobe.
- Thumbnails don't render in headless Chromium, so review footage from the downloaded previews, not the grid.

## 5. Choosing shots and concepts

- Review contact sheets, then per-clip timeline strips (8 frames across the clip) to pick in-points: the moment a
  hand enters, a fingertip traces the chain, a hand wraps the wrist, a face rests near the wrist, water runs over it.
- Prefer macro framing, soft backgrounds, slow deliberate gestures, room for text off the jewellery.
- **A set of ads must be diversified**: different footage, mood, claims and music per ad, same rules. Example set
  from Session 11: Gold "Quiet light" (intimate, warm), Black "Touch" (tactile, material claims),
  Black "Editorial" (charcoal dress, hair, attitude, slightly moodier grade).
- Men's and women's footage are never mixed in one ad.
- **No full faces (Eli, W423):** pick scenes where the model's face is not fully visible (cropped at the lips/chin, turned away, hidden by a hand or hair).
- **No set tricks (Eli, M464):** never use a scene where the white foam piece used on set to fit the bracelet is visible (it sits at the clasp). Check the clasp area frame by frame.
- **Strong colour in every scene (Eli, M464):** drop a scene whose colours look flat or washed out next to the rest of the ad.
- **Men: slim and minimal (Eli, M464):** frame wrists and hands so they read slim and elegant; no wide, heavy forearm shots that look chunky.
- **No black t-shirt scenes (Eli, W423):** skip the Session 10 shots with the black t-shirt; use sky, sand, rock and sea shots instead.
- **The jewelry must look good in every scene (Eli, W423):** gold has to catch the light and shine. Skip shots where it reads dark, brown or dull (shade, backlight on gold); check every graded frame before choosing.

## 6. Slow motion

- **120 fps footage:** play every frame 4x slower: `setpts=4*PTS,fps=30000/1001` (or 3x at fps 30). No invented frames.
- **25-50 fps footage** (Session 11 is 25 fps): motion-compensated interpolation to 2x:
  `minterpolate=fps=50:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:me=epzs:vsbmc=1:scd=none,setpts=2*PTS,fps=25`.
  Always check the in-between frames for smearing on fingers before using it. Slow: about 45 s of CPU per source second.
- Add a gentle 2-3% push-in over each shot.

## 7. Colour (professional, every ad)

**Skin rule (Eli): skin must look sun-kissed / tanned, never pale, in every scene.** `grade.py` measures each shot's graded skin and adds warmth and depth until it hits one tan target (bright, washed-out clips get more), and warms the skin tones in every look (selectivecolor on reds and yellows, slightly more saturation). The neutral white target keeps walls, bouclé and white tops clean. Check the before/after sheet: skin golden-tan, whites still neutral. Reference: `specs/tan-before-after.png`.

Use `grade.py`, never one blanket filter for all clips:
1. **Normalise** flat camera footage: levels 0.06-0.80, then a soft S-curve.
2. **Shot matching:** measure each shot's neutral areas: bright pixels that are the least coloured (wall, boucle, white
   top; nails and skin excluded, because they pushed an earlier pass blue). Set per-channel gains so those areas hit one
   white target. Every cut then matches in white balance and exposure.
3. **One look per ad:**
   - `gold`: white (234,229,220) cream, saturation 1.02, rich but not yellow gold
   - `black`: white (232,231,228) clean neutral, saturation 1.12, deep blacks
   - `edit`: white (222,222,221), slightly cooler and deeper contrast, saturation 1.02
4. Light sharpening (`unsharp=5:5:0.35`) for skin texture.
5. **Always make a before/after sheet of every shot** and look at it: whites neutral, skin sun-kissed and tanned (not pale, not orange, not grey,
   not pink), blacks black, no blue walls. Measure RGB of white areas and skin if unsure.
- Sunny 120 fps beach footage (Session 7) uses `specs/v5-grade.txt`: cooler temperature, yellows pulled from the tan,
  saturation 0.86, near-zero black lift, light sharpening.

## 8. Building an ad

1. Shot list file, one line per shot: `<look> <raw subdir> <clip> <in s> <source dur s> <lockup name>`.
2. Lockup spec JSON: `{"s1":{"top":1380,"head":"Black Friday","sub":"Limited time"}, ..., "s5":{"top":1300,"logo":true,
   "head":"30% off sitewide","sub":"No code needed"}}`. Render with
   `node cards4.js bfcm26/video-ad/assets <out dir> <spec.json>` (fonts and logo are embedded as data URIs; `file://` does not load).
3. **Preview text placement on graded frames before rendering** (overlay each lockup PNG on a graded frame at about 75% of
   the shot). Move any lockup that touches the jewellery.
4. `build5.sh <shots> <lockup dir> <music.mp3> <out.mp4>`: per-shot grade, slow motion, cached graded shots (text
   changes don't redo the interpolation), lockup overlay with fade + rise, 0.5 s fade in, **no fade out: the video just stops on the closing scene, never a black fade (Eli)**, music trimmed
   with fades, loudness -16 LUFS. `build4.sh` is the 120 fps version.
5. Music: ElevenLabs `POST /v1/music` (`ELEVENLABS_API_KEY`), instrumental, 17 s, a different mood per ad (felt piano
   and strings; warm harp and piano; deep minimal pulse). It returns 429 "system_busy" at times: wait 30 s and retry.
   Each generation costs credits; say so.

## 9. QA before sending

- Grab one frame from the middle of every scene (frame numbers depend on fps; don't sample past the end) and check:
  text on every scene, two lines each, same sizes, white, off the jewellery, inside the safe zone, logo only at the
  close and 28 px, grade consistent across cuts.
- Duration, resolution, audio present.
- Then send the MP4s, and commit shot lists, lockup specs and any script changes to the repo.

## 10. Pitfalls already hit

- In shell loops, ffmpeg (and Python calling ffmpeg) reads the loop's stdin. Use `ffmpeg -nostdin` and read lists on
  another file descriptor (`while read ... <&3; done 3< file`).
- Frame.io's grid is virtualised: cards off screen don't exist. Open clips by direct view URL
  (`/share/<share>/view/<asset id>`; the asset id is in the preview link) instead of scrolling to them.
- The Download menu text uses a plain `x` (`MP4 H264 1080x1920`), not `×`.
- A direct folder URL lists clips in a different order than the parent view; check the first filename with `peek.js`.
- White text on white foam or bright walls disappears: change the shot or move the text.


## Stills cut from video (NOT the standard: Eli rejected this on W421, 14 Oct)
The standard is the simple way: take the still from the graded video (`grade.py` look) and build the static on it. The steps below are kept only as reference and tools.
1. **Source:** download the ORIGINAL camera file (C####.MP4, 2160×3840, about 58 Mbps). The public share's Download menu lists it as the top "2160x3840" entry (`dlorig.js`, no login needed); the Frame.io V4 API also works. Never use the share's web preview or a finished ad export, which are about 1080×1920 at 3 Mbps and look soft and blocky.
2. **Frame pick:** extract every frame in a window of about ±0.5 s around the chosen moment as lossless PNG (`ffmpeg -ss t-0.5 -t 1 -i src -vsync 0 f_%03d.png`). Score each one for sharpness (variance of Laplacian on the jewelry/wrist crop) and keep the sharpest one with no motion blur on the box-chain and square-chain links.
3. **Grade:** originals are full-range, so grade.py's filter does not land the same look on them. Instead, match the original frame to the approved graded still or video frame with `stillmatch.py` (per-channel quantile match learned on the same moment, applied in 16-bit). Otherwise use the same look as the video, applied to the still (grade.py filter chain on the single frame, GRADE_ADAPT as in the video), so the skin follows the tan rule. Save as 16-bit PNG and keep the JPEG step until the very end.
4. **Crop/scale:** there is no fixed crop rule (Eli). Vary the framing per ad: wide with context, mid, or tight macro, so each batch has variety. Crop for the slot first. Upscale with an AI upscaler (Real-ESRGAN class) only if the crop is smaller than its slot in the ad, at most 2×. Otherwise downscale with Lanczos.
5. **Pro retouch (always):** run `retouch.py in16.png out16.png x0,y0,x1,y1 [debug]` with the box around the jewelry. It does three things:
   - Lightroom develop: chroma NR, highlights -/shadows +, texture and clarity, an S-curve, a subtle vignette and grain.
   - Photoshop skin: hue unify toward the median skin tone, frequency separation (low layer evened, high layer = pores untouched), blemish/mole inpaint.
   - Jewelry precision: metal neutralised to a clean black, polished cuff smoothed with scratches, dust and fingerprints inpainted, chain links sharpened with overshoot clamped (no halos), blacks deepened and speculars lifted, a contact shadow.

   Check the debug masks if something looks off. Skin is hue 50–95 with chroma >11 in Lab, which keeps bouclé and walls out.
6. **QC at 100%:** links crisp and countable, skin pores and fine hairs real, no plastic smoothing or invented detail, no banding in the background. Redo with another frame if any of these fail.
7. Then build the static as usual (ROAS check, safe zones) and deliver.

---

# FILE: bfcm26/docs/ideation-images.md

# Ideation images (generated, only when Eli asks)

- **Ideation images (generated, OpenAI `gpt-image-2.5-sunburst` via `OPENAI_API_KEY`, real product photo as reference):** must look like the nailed Cavaier look Eli showed:
  - Look reference: `bfcm26/ideation/style/cavaier-look.jpg` (Eli's "nailed" example). Send it as a second reference image for the look only.
  - 100% realistic, nothing CGI or stock-glossy.
  - Close macro framing, shallow depth of field.
  - Muted, slightly icy colors: cool neutral white balance, soft diffuse overcast light, low saturation.
  - Very detailed skin (pores, fine lines, individual arm hairs).
  - Jewelry rendered exactly: real metal reflections, every box-chain and square-chain link crisp.
  - Check each image at full size before using it. Regenerate if the product shape, count or links are off.
