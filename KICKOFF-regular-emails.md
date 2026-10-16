# Kickoff for the regular email campaigns chat (paste this as the first message, then add the Figma link and the brief)

I'm Eli at Cavaier. We built the BFCM26 email campaign together in another chat; now I want the **same way of working for our regular (non-Black-Friday) email campaigns**. Read this whole message first, then the brief I add at the end, then look at the Figma file and tell me what you see before changing anything.

## Where things are
- **Figma file for the regular emails:** [PASTE THE FIGMA LINK HERE]. Work on that file only. The BFCM file (`e0aqnfx3SvHowbEDDyMNMW`) is a reference for how we work; don't change it.
- Reference for quality and process: the BFCM master page https://claude.ai/artifact/21hL1pG8bndjPaBr8p8G6S (read it with the Artifact tool, don't change it).
- Repo: Cavaier/Claude, branch `claude/sharp-franklin-iy8kax`. The BFCM tools are in `bfcm26/figma-sync/` (README, RUNBOOK, page → Figma sync, annotation plugins). Put this work in a new folder `regular-emails/`.
- Co-worker: Katrina edits the same pages and Figma files.

## How we work
1. **One shared master page** (an Artifact, shared with the org): one row per email with a brief card (date, send time, audience, subject, preview, goal) and the email at 600px. Versions side by side (A as briefed, then B, C… with real design swings), plus the live bar (who's online, what Claude is doing, activity log).
2. **Everything changed on the page is mirrored into Figma in place.** Never move or replace frames people arranged, never shift rows; new versions go next to the last version of their row. Before updating a frame, check it for Figma edits: copy text edits back to the page, flag anything else. Log every change and say plainly what changed and where.
3. **Links live in Figma as annotations**, category "URL", with the label being just the URL, on the layer people click (button bg, card, logo, icon). Not comments. EU emails link to `cavaier.com`, US emails to `us.cavaier.com`. Footer: SHOP ALL, BRACELETS and NECKLACES carry the same link; social icons go to instagram.com/cavaierofficial, tiktok.com/@cavaier, facebook.com/cavaier; MANAGE PREFERENCES and UNSUBSCRIBE use `{% manage_preferences_link %}` and `{% unsubscribe_link %}`.
4. **Into Klaviyo:** build each email as a CODE template from the Figma design: 600px table HTML, live text for headlines, buttons and offers (images only for photos and the logo), good alt text, and the annotation links. Real photos are cropped from the Figma render of the frame (not the image fill underneath, which can be an older photo). Create **draft** campaigns only, never schedule or send unless I say so. Test drafts get "Eli" in the name, and **never touch campaigns or drafts made by someone else**. Check the result with the template's screenshot.
5. Klaviyo account: timezone Europe/Stockholm, sender info@cavaier.com / "Cavaier". Regular campaigns have used segments `VSrsMu` and `Wb6Tr5`; `SxyYP7` is "ALL – Engaged 2 Years — big blasts". Ask me which audience if the brief doesn't say.
6. Photos: always pull fresh from the live Shopify listings or from Figma, never from an old cached copy (product handles have changed, e.g. `3x-minimal-stack-set-for-him`).

## Tools and known workarounds
- **Figma:** read with the REST API (`FIGMA_TOKEN`: nodes, annotations, comments, image renders). Writing (frames, text, annotations) needs the Figma connector (`use_figma`). If it isn't connected, write a small development plugin I can import (desktop app → ⌘K → "Import plugin from manifest") and run, like we did for the footer links.
- `git push` sometimes returns a GitHub 500; then push with the GitHub connector (`push_files`) and reset local to origin.
- Klaviyo strips a Google Fonts `<link>`, so the font falls back to Helvetica/Arial unless handled.

## Brand (Cavaier)
- Clean, minimal, premium: white and soft fog (#F2F2F1), thin hairlines (#DCDCDA), square black buttons (no pills), small spaced caps labels. No big black blocks or dark sections.
- Type: **Figtree**, like cavaier.com. Headings uppercase, regular (400) or light (300), no extra letter spacing; labels uppercase with 0.1em spacing; body 400, emphasis 500. The Bodoni wordmark is the logo image.
- Red **#A82C24** only as a small accent (labels, sale prices, a dot). Struck-through old price in grey, new price in red.
- Let real photos breathe. Only true claims: waterproof, sweat and heat resistant · recycled 316L stainless steel · adjustable S/M/L · black, silver or gold · jewelry case included with 2+ pieces ("case included", never "free case") · free shipping · Trustpilot 4.5, 3,000+ reviews. Flag anything you can't verify, including prices.

## Brief
(paste here: which emails, dates, products, offers, audiences)
