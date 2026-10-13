# Email OS

Cavaier's email programme run by Claude Code agents: one manager, nine specialists, and
the owner signing off at four gates. Modelled on Jesse Streur's HappyFlops setup ("I replaced
my email marketing agency with 10 AI agents", Oct 2026), with its weak spots fixed.

## How it runs

```
analyst ─► planner ─► [APPROVE calendar] ─► researcher ─► copywriter ─► [APPROVE copy]
   ─► designer + image director ─► [APPROVE layout] ─► localizer ─► facts + hosted images
   ─► QA ─► [APPROVE final] ─► builder (drafts) ─► verify_build ─► schedule (send gate)
   ─► daily reconcile ─► analyst …
```

- **Manager:** the main Claude session with the `email-os` skill (`.claude/skills/email-os/SKILL.md`).
  Say "plan November", "move the Black Friday send to design", "status", or "run the daily check".
- **Specialists:** `.claude/agents/email-*.md`. Each has one job, one input, one output, and the
  same skeleton (INPUT / OUTPUT / DONE MEANS / YOU NEVER / WHEN UNSURE), plus only the tools it needs.
- **Owner gates:** you type `APPROVE <campaign-id> <gate>` (calendar, copy, layout, final) or
  `REVOKE …`. Several at once: `APPROVE 2026-11-27-bf-public calendar,copy`.

## Files: one source of truth per stage

| Stage | File | Written by |
|---|---|---|
| Rules | `config/rules.yaml`, `config/brand.yaml` | owner |
| Markets, products | `config/markets.yaml`, `config/products.yaml` | owner |
| Results | `data/performance/YYYY-MM.yaml` | analyst |
| Calendar | `calendar/YYYY-MM.yaml` | planner |
| Brief | `campaigns/<id>/brief.yaml` | planner |
| Copy | `campaigns/<id>/copy/<locale>.yaml` | copywriter, localizer |
| Design | `campaigns/<id>/layout.yaml`, `images.yaml` | designer, image director |
| Prices, stock, photos, "from" prices | `data/facts/<market>.json` (live from the store) | `tools/facts.py` |
| Collection groups | `config/collections.yaml` | owner |
| Optimised images | `campaigns/<id>/images.lock.yaml`, `data/hosted.yaml` | `tools/images.py` |
| Reviews | `data/reviews.yaml` (verbatim, source logged) | owner / analyst |
| Rendered emails | `campaigns/<id>/out/<market>.html` | `tools/render.py` |
| Klaviyo drafts | `campaigns/<id>/build.yaml` | builder via `tools/verify_build.py` |
| Approvals | `approvals/ledger.jsonl` | **only** the hook, from your typed message |

Git is the backup: every change to every stage is a commit you can diff or roll back.

## Tools

```bash
python3 tools/facts.py                 # live prices, stock, photos, collection "from" prices
python3 tools/render.py <id>           # HTML + plain text per market
python3 tools/images.py prepare <id>   # optimise images; then host them via the Shopify connector
python3 tools/lint.py <id> [--final]   # every auto rule; writes lint.json
python3 tools/verify_build.py <id> <market> <template.json> <message.json>   # Klaviyo = approved?
python3 tools/status.py [2026-11]      # pipeline board with gates
python3 tools/reconcile.py <klaviyo-export.json> --market eu   # calendar vs Klaviyo
python3 tests/test_system.py           # 25 end-to-end tests on a fixture campaign
```

## Copy tokens

Copy never contains a price, currency or discount code. It uses tokens, filled per market
from live store data at render time:

| Token | Becomes (EU) |
|---|---|
| `{offer_price:3x-minimal-stack-set-for-him}` | €66.43 (94.90 − 30%) |
| `{price:3x-minimal-stack-set-for-him}` | €94.90 |
| `{from_offer_price:him-bracelets}` | €20.93 (cheapest in-stock bracelet − 30%) |
| `{money:25}` | €25 (US: $25) |
| `{code}` / `{pct}` | the calendar offer's code / 30% |

## Blocks

`strip, logo, hero, image, heading, text, ticket, timeline, section_header, tiles,
offer_card, product, review, button, note, trust, divider, spacer, footer` in
`templates/email.html.j2`, and `style: plain` for text-only sends (`para, link, footer`).
Tables and inline styles, Outlook-safe buttons, rows that stack on phones, under 90 KB.

## What's different from the HappyFlops setup

What they got right, and kept here: a manager with rules, one job per agent, written testable
rules, one source of truth per stage, few non-negotiable human gates, data before the calendar,
and a daily check of the calendar against what Klaviyo will actually send.

What's changed:

1. **Rules are code, not memory.** They keep the rules in every agent's memory and have Carl
   check emails against them, which is a model checking a model. Here every testable rule is
   a function in `tools/lint.py` with a test. "One accent colour" means the HTML is parsed and
   the colours counted.
2. **The non-negotiables are enforced, not requested.** Their "agents never approve" and "no
   unasked messages" are prompt text. Here they're Claude Code hooks (`tools/gate.py`, wired in
   `.claude/settings.json`):
   - Approvals are recorded only from a line you type. Subagents can't trigger that hook, so a
     relayed "he said it's fine" records nothing. Agent attempts to write the ledger are blocked.
   - Each approval stores the hash of exactly what you saw. If the copy changes after you
     approved it, the gate shows `~` and you're asked again.
   - `send_campaign` is refused unless all four gates are approved, the final approval matches
     the current render, and the Klaviyo draft was built from that same version.
   - Test sends always ask first. Deletes ask for a backup first.
   - The ledger is hash-chained, so a deleted or edited entry stops all sends.
3. **Live HTML instead of sliced images.** Their builder slices each design into images. That
   puts the text inside images: invisible when images are off, unreadable to screen readers,
   weaker for deliverability, and every market needs its own image set. Here the text is real
   HTML, one layout serves every market, and localizing only swaps strings.
4. **Prices are never typed.** They come from the live store per market. Two things this
   already caught while building: cavaier.com prices by the visitor's location (a US server
   sees USD 109.00 for the 3x Set), so facts are pinned per market with `?country=`; and the
   3x Set is €94.90 live, while the ads kickoff still says €94.95.
5. **Novelty is a rule.** They run two designers so one house layout doesn't take over. Here
   R11 blocks repeating any of the last three structures, and the designer makes variants
   when you ask for them.
6. **Independent QA.** Their manager both routes work and checks it. Here `email-qa` didn't
   make the email, checks it fresh, and can't approve.
7. **What's in Klaviyo is checked, not assumed.** After the builder makes a draft, it reads
   it back and `verify_build.py` compares template HTML, text, subject, preview, name,
   audiences and send time with what you approved. The send gate needs that match. If
   someone edits the draft in Klaviyo afterwards, it must be verified again.
8. **Images built for email.** Store photos are up to 7 MB PNGs; Shopify only shrinks them
   for WebP clients. `images.py` makes 2x progressive JPEGs under 300 KB, crops side-by-side
   images to one shape, and hosts them on the store's own Shopify CDN.
9. **Deterministic reconcile.** Their daily Slack bot is an agent's reading. Here
   `tools/reconcile.py` checks: missing from Klaviyo, wrong date or time, no recipients,
   scheduled without final approval, approved but never scheduled, subject changed, cancelled
   sends, and Klaviyo sends that aren't on the calendar.

## Trial builds

A draft named `EOS TEST · <calendar name>` is verified like any build but the send gate
refuses it permanently. Use it to try the system next to a real draft.

## Limits

- Design is limited to the block library in `templates/email.html.j2`. A layout that needs a
  new kind of block means adding one to the template. Their freeform Figma design has more
  range; for big creative swings, design on the master page and use `bfcm26/figma-sync/`.
- Only the EU Klaviyo account (Cavaier AB) is connected. The US account needs connecting
  before the builder and reconcile can work for US.
- Tested in Chromium at 640 and 375px, not in real Gmail/Outlook/Apple Mail inboxes. A
  Litmus or Email on Acid check (or test sends to real accounts, when asked) is still needed.
- The builder re-types the HTML into Klaviyo and the read-back into files; verify_build
  catches transcription errors, but an agent could in principle save a wrong read-back.
  With `KLAVIYO_API_KEY` in the environment, `verify_build.py … --fetch <message id>` reads
  Klaviyo directly instead (written to the documented API, not yet run against it).
- Klaviyo rewrites HTML on save and drops `<link>` tags; fonts load through `@import`
  instead, and verification compares text, links and images rather than bytes.
- `data/reviews.yaml` is empty: Trustpilot blocks automated reads, so real reviews have to be
  added by hand with their source URL.
- The hooks stop mistakes and well-meaning agents. They aren't a security boundary against a
  hostile process with shell access; the hash chain shows tampering but can't prevent it.
- The `de` market is configured but off: turn it on when German emails start.
