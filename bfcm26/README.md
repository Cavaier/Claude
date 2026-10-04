# Cavaier BFCM26 email sequence

14 sends, Nov 23 – Dec 6, 2026. Mock-ups for review before they are built in Figma
(BFCM file, page "Email Campaign") and Klaviyo.

## The master

**The one master is the shared page: https://claude.ai/artifact/21hL1pG8bndjPaBr8p8G6S**
Eli and Katrina both work on it:

- Leave a comment on the page and send it to Claude. The change goes live within a minute.
- Any Claude session that edits the page starts from the latest published version and
  republishes on top of it. Never regenerate it from older files: that would wipe the
  other person's edits.
- `cavaier-bfcm26-sequence.html` here is a backup snapshot of the master, not the source.

## Live bar (who's on the page, what Claude is doing)

The top of the master page shows who has it open right now and which email each person is
looking at, what Claude is doing, and an activity log (the **Activity** button). People can
post "I'm working on…", "Waiting for Claude…" or a note there.

**Any Claude session that edits the master must post to it** (page database, via `ArtifactData`):

1. Before starting: set `live/claude` to `{state: "working", task: "<short task>", at: <epoch ms>, label: "<Eli's|Katrina's> Claude"}`
   and add an `activity` doc `{at, actor: "claude", label, kind: "start", text}`.
2. After publishing: set `live/claude` to `{state: "idle", task: "<what changed>", at, label}`
   and add an `activity` doc with `kind: "done"`.

Republishing the page must keep its capabilities (`room`, `user` with the `profile` scope, `db`):
omit `capabilities` on a redeploy so they carry over.

`archive/` holds the first generator scripts (v1–v7). They are out of date: the master has
moved on since, so don't rebuild from them. `figimg/` and `imgcache26*/` are the source photos.

## Open placeholders

- Christmas delivery cut-off date (`[CEO to confirm date]`)
- Matte Cuff restock month
- Matte Cuff photos (Minimal Cuff stand-ins for now)

`older/` holds the first single-email and 5-email Black Week mock-ups.
