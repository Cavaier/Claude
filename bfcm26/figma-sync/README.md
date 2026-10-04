# Page → Figma sync (BFCM26)

Turns every email on the shared master page (one `<article class="em">` per version) into an editable Figma frame, and keeps Figma in step when the page changes.

Built for the BFCM26 campaign master (https://claude.ai/artifact/21hL1pG8bndjPaBr8p8G6S) and the Figma file `e0aqnfx3SvHowbEDDyMNMW`, page "Email Campaign" (`310:2`). The same tools work for another page (e.g. the flows master) after changing the ids at the top of `builder_f.js` and the version order in `compile.py`.

## Files

| File | What it does |
|---|---|
| `extract.js` | `node extract.js <page.html> <outdir>`: renders the page in headless Chromium and writes every email as layers (rects, gradients, images, text) to `emails.json` + images to `img/`. |
| `compile.py` | Compacts `emails.json` into `compiled.json` (one spec per email + its brief). Version order lives in `order=[...]`. |
| `builder_f.js` | Figma Plugin API prefix with `build()` / `brief()`. Edits an email **inside its existing frame** (found by id, else by its `NN-X ·` name); never moves or replaces frames. Thin lines are kept above images. |
| `sync.py` | `python3 sync.py <page.html> <workdir>` → writes `syncbatchNN.js` for the emails that changed. `python3 sync.py --commit <workdir> <results.json>` records the new frame state in `manifest.json`. `SKIP=e08E,...` leaves listed emails alone. |
| `check_gen.py` + `pull.py` | Safety check before any update: dump the email's current Figma frame, compare it with what the sync last put there. Text edited in Figma is copied onto the page first; any other Figma edit makes that email get skipped and flagged. |
| `manifest.json` | Figma node ids, hash and last-built spec per email. |
| `hashes.json` | Image key → Figma image hash (images uploaded once into the image library frame `310:3`). |
| `RUNBOOK.md` | The step-by-step loop. |

## Rules learned on BFCM26

- Never move frames: people arrange them by hand (e.g. a "Selected" column).
- Update in place: same frame id, parent, position and layer order.
- New versions land next to the last version of their row, wherever that row currently sits.
- Before updating an email, check its Figma frame; carry Figma text edits to the page.
