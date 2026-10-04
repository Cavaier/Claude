# Flows page → Figma sync runbook

Figma file `e0aqnfx3SvHowbEDDyMNMW`, page "BFCM Flows (synced)" `359:2`, image library frame `359:3`.
Same rules as the campaign: NEVER move or replace frames; edit them in place (found by id, else by the
`NN-V-G-state ·` name); new versions are placed after the last frame of their row.

Differences from `../../figma-sync`:
- `extract_flows.js` renders every W/M × date-state combination the email runs in (one frame each).
- `compile_flows.py` stores item coordinates relative to their section, so variants diff cleanly.
- `sync_flows.py` sends one full frame per row and the other frames of that row as patches (`P(base, ops)`),
  which keeps each `use_figma` script under 46 KB. No footer component: the footer is drawn from the page.
- `check_flows.py` / `pull_flows.py`: the Figma-edit check. A text edit that also appears in other
  W/M or date versions of the email is flagged instead of guessed: make it on the page by hand.

Loop (on every republish of the page):
1. Artifact read https://claude.ai/artifact/CAab5coU9rgBbEfatBgsEu → copy the saved html to `../live/flows-master.html`.
2. Check Figma first: `python3 check_flows.py <ids>` → run `check.js` with use_figma → save result →
   `python3 pull_flows.py <result.json> <page.html> <page.html>`; republish the page if text came back,
   and leave flagged emails out of the sync (`SKIP=id,id`).
3. `python3 sync_flows.py $PWD/../live/flows-master.html sNN` (absolute path).
   Exit 2 + `missing_images.json` → upload those `sNN/img/*` with upload_assets into rectangles in `359:3`,
   add key → hash to `hashes.json`, rerun.
4. Run each `syncbatchNN.js` with use_figma (verbatim; scripts are safe to re-run). Merge the returned
   `{id:{em,br}}` objects into one json.
5. `python3 sync_flows.py --commit sNN <results.json>` → `manifest.json`.
6. Live bar: activity doc `{actor:'claude',at,kind:'done',label,text}` saying what changed where; `live/claude` idle.
