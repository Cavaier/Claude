# Page → Figma sync runbook (run on every artifact republish wake)
Figma file e0aqnfx3SvHowbEDDyMNMW, page 310:2, footer comp 312:27. manifest.json = all 70 ids + hashes.
NEVER move or replace frames. Changed emails are edited inside their existing frame (found by id, else by "NN-X ·" name); frame keeps id, position, parent.
1. Artifact read https://claude.ai/artifact/21hL1pG8bndjPaBr8p8G6S → cp saved html to ../live/bfcm26-master.html
2. `python3 sync.py $PWD/../live/bfcm26-master.html sNN` (absolute path!)
   - exit 2 + missing_images.json → upload those img/<key>.jpg via upload_assets into image frame 310:3, add key→hash to hashes.json, rerun.
3. Run each sNN/syncbatchNN.js via use_figma; collect returned {id:{em,br}} into one json.
4. `python3 sync.py --commit sNN <results.json>`
5. Live bar: activity doc {actor:'claude',at,kind:'done',label:"Eli's Claude",text}; live/claude if_version.
