# v10 page sync (Figma page "BFCM26 · v10", 398:2)

Same tools as the parent folder, pointed at the v10 page:
- `builder_f.js`: PAGE = 398:2 (the "Email Campaign" page 310:2 is not touched).
- `compile.py`: one column per send in date order (s01A … s13A, s13B … s20A), 680px apart, brief above each email.
- `manifest.json`: frame + brief ids for the 21 v10 emails.

To sync: copy these three files over the parent ones in a work dir (keep `hashes.json`, `extract.js`, `sync.py`), then follow ../RUNBOOK.md.
