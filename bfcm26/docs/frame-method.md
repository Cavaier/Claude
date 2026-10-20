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
