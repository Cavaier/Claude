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
