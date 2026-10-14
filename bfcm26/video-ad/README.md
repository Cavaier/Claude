# Black Friday video ad (pool / waterproof)

18 s, 1080×1920, 30 fps. Cut from the Frame.io share "RAW Session" (https://f.io/SZP85Oib),
folder `Women/Iphone shots`, using the 1080×1920 MP4 proxies.

Shots: IMG_2153, 2150, 2151, 2157, 2167, 2149, 2154 (end card). Music: ElevenLabs instrumental (19 s).
Copy follows the static-ads rules: 30% off sitewide, no prices, Figtree, red #A82C24, key text
between y=270 and y=1536, only listed claims.

Steps (paths inside the scripts point at the session scratchpad; adjust):
1. `browse.js` lists a share folder; `dl.js` downloads clips via the player's Download → MP4 1080 proxy.
2. `cards.js` renders the transparent text cards (needs Figtree-300/400/500.ttf and logo_white.png).
3. `build.sh` cuts the shots, overlays the cards, adds the music, exports the MP4.

## v2: minimal macro style (after Vacier's top video ads)

12 s, slow motion (120 fps source played 3x slower), muted warm-neutral grade, small CAVAIER wordmark
with one tracked line per shot placed on empty skin or fabric. Footage: `Men/Session 1 | Men/VIDEO`
(silver duo chains on beige linen): C1133, C1070, C1176, C1132. Music: calm ElevenLabs ambient (13 s).

- `walk.js` steps through a folder in the player and records every clip's preview link (fast way to review 100+ clips).
- `dl2.js` downloads 1080 proxies by opening each clip's view page directly.
- `cards2.js` + `build2.sh` render the text and the edit.

## v4: women, black stack (Session 11, the newest)

13 s, footage from `Women/Session 11 | Women/Video/Black` (flat camera footage, 25 fps):
C2287, C2384, C2386, C2360, C2382. Graded to the brand reference (expanded levels, soft S-curve,
neutral bright whites, deep blacks, peach skin). Dark charcoal wordmark and text, because the
backgrounds are bright white. `cards3.js` + `build3.sh`.
