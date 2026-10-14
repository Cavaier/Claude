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
  whites, peach-beige skin (never orange tan), deep true blacks, soft diffused light, crisp skin texture.
- **Luxury slow motion.** Real high frame rate footage played slower, every frame used. No jerky real-time movement.
- Format: 9:16, 1080×1920, H.264 MP4 with AAC music, about 13-17 s, 5 shots of about 3 s, the last one the closing scene.

## 2. Text and logo (strict)

- **White text only.** Never dark or charcoal text. If a background is too bright, choose another shot or move the
  text onto skin, fabric or a darker area. Don't change the colour.
- **Logo:** the CAVAIER Bodoni wordmark (`assets/logo_white.png`). **Only once, on the closing scene.**
  **28 px tall** on the 1080×1920 canvas, so its letters equal the headline's capital height. Never bigger than the
  headline. No logo on the other scenes.
- **One type system in every scene (Figtree), never a one-off size:**
  - headline: **38 px**, weight 300, uppercase, letter-spacing 0.18em
  - sub-line: **17 px**, weight 400, uppercase, letter-spacing 0.32em, 14 px under the headline
- **Every scene is two lines: headline + sub-line.** Never a headline alone. One headline per scene.
- Closing scene: wordmark, then the same headline + sub-line.
- Lockups fade in over 0.9 s (starting 0.35 s into the shot) with a 16 px ease-out rise.
- **Never put text on the jewellery** (chains, cuff, clasp, tag). Check every scene.
- Key text between y=270 and y=1536 (Meta safe zone).
- On bright, high-key frames, a very soft, wide shadow sits behind the lockup (`.veil` in `cards4.js`, max ~15% black)
  so the white reads. It must look like natural falloff, never a grey patch.
- What did NOT work (don't repeat): big "30% OFF" numerals, red pills, dark text, the logo on several scenes, a 47 px
  logo (too big), a 17 px logo (too small), sizes changing per scene, single-line scenes.

## 3. Copy, offer and claims

- **The angle is decided batch by batch.** Black Friday is one angle, not the default. Ask Eli for each new batch (Black Friday, Evergreen with no offer, or another angle). The Black Friday offer, scene pairs and closing lines below apply only to Black Friday batches. For other angles, keep the same two-line system and true claims, and drop the offer lines.
- Offer (Black Friday batches only): **Black Friday, 30% off sitewide, no code needed (taken off at checkout).** Say it in different ways.
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
  - NO CODE NEEDED / TAKEN OFF AT CHECKOUT
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
  | Women / Session 10 / Video (334) | | 50 |
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

## 6. Slow motion

- **120 fps footage:** play every frame 4x slower: `setpts=4*PTS,fps=30000/1001` (or 3x at fps 30). No invented frames.
- **25-50 fps footage** (Session 11 is 25 fps): motion-compensated interpolation to 2x:
  `minterpolate=fps=50:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:me=epzs:vsbmc=1:scd=none,setpts=2*PTS,fps=25`.
  Always check the in-between frames for smearing on fingers before using it. Slow: about 45 s of CPU per source second.
- Add a gentle 2-3% push-in over each shot.

## 7. Colour (professional, every ad)

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
5. **Always make a before/after sheet of every shot** and look at it: whites neutral, skin peach (not orange, not grey,
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
   changes don't redo the interpolation), lockup overlay with fade + rise, 0.5 s fade in, 0.7 s fade out, music trimmed
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
