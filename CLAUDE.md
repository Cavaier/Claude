# Working rules for Claude (Cavaier)

## Do the work yourself

- If Claude can do or check something with the tools it has (APIs, Shopify, Merchant Center,
  Google Ads, the live site, the repo), Claude does it itself. Don't hand Eli a list of clicks
  or a "check this and tell me" step when a tool call could do it.
- Verify after every change (re-read, re-list, fetch the live page) and report what is
  actually true now.
- Only hand a step to Eli when no tool can reach it (e.g. a UI-only setting, an app's own
  settings screen, a permission the session refuses). Then say exactly why, give the exact
  clicks, and check the result yourself afterwards.
- Destructive or hard-to-reverse changes (deletes, unlinking accounts, disabling tracking)
  still need Eli's OK first. Show what will change, then do it.

## Accounts and access

- Google Ads: 3104616697 (Cavaier), MCC 9574419833. Primary conversion action is "Purchase",
  fed by the Google & YouTube app (conversion ID AW-16488775779).
- Merchant Center: 747874697. GCP project `cavaier-ads` (415497972272) is registered as its
  Merchant API developer. Use the Merchant API v1 with an access token minted from the
  `GOOGLE_ADS_*` env vars (scopes: adwords + content).
- Google Ads API works from here: the agent proxy adds the developer token. Call
  `https://googleads.googleapis.com/v22/customers/3104616697/...` with the OAuth token and
  header `login-customer-id: 9574419833`.
- No Google Analytics and no extra Google tags (Eli's decision, Oct 2026). Keep the Google &
  YouTube app's Conversion measurement on: it is what sends purchases to Google Ads.
- Shopify: cavaierwatch.myshopify.com, via the Shopify MCP tools (products, themes, publications).
- Product feed: only the Google & YouTube app. Simprosys is uninstalled and its feeds were deleted
  (Oct 2026). Don't recreate third-party feeds.

## Product facts (from Eli, Oct 2026)

- `-for-him` handles are the men's versions, `-for-her` (titles with " - ") the women's. They are not duplicates.
- Necklaces are not adjustable. "Pendant" in the name = pendant + chain; otherwise it is a plain chain.
- Gold colour is gold-plated (write "gold-plated"). Material: recycled 316L stainless steel.
- The free jewelry case offer applies only to the sets, not single products.
- Google gender metafield: `mm-google-shopping.gender` (male/female), `age_group` adult.
- Original product descriptions before the Oct 2026 edit: `shopify-backups/product-descriptions-before-2026-10-11.json`.

## US store (us.cavaier.com)

- Separate Shopify store `d3d79e.myshopify.com`, Merchant Center 5087698947, Google Ads 6721676260 (not active). No Google Ads setup for the US yet.
- The Shopify MCP connects to one store at a time (`switch-shop`, then Eli re-authorizes in claude.ai connector settings).
- Oct 2026: same product types, gender, SEO and offer/adjustable cleanup applied as on the main store. Backup: `shopify-backups/us-products-before-2026-10-11.json`.
- Open: us.cavaier.com can't be claimed in MC 5087698947 because MC 747874697 claims cavaier.com (all US products disapproved). Older US texts contain outdated "Free Shipping" lines (necklaces list Germany/Europe times).

## Google Ads Desk (working log)

- **Before any Google Ads work, read both:**
  1. the context book `google-ads/CONTEXT.md` (facts, findings, decisions, proposals, log), and
  2. the Desk change log — every entry, whatever its status: Proposed, Applied, Evaluated
     (has a verdict) and Reverted. Read it with `ArtifactData` `get` on `datasets/changes`, then
     fetch the file its `source.url` names (Artifact `read` with that `/_blob/…` id as `path`).
- After any work, add to both: the change log for changes, the context book for what was
  looked at, decided or learned. Due evaluations (eval date passed, verdict Pending) come first.

- Dashboard: https://claude.ai/artifact/BEmCjut8iisbsUQsezpmNa ("Cavaier Google Ads Desk"), Dashboard type, data as attached JSON files.
- Every change to the account, feed or tracking gets an entry in the change log (`changes.json`): id (permanent: C-### for changes logged as already done, P-### for changes first proposed; the status field shows Proposed/Applied/Reverted), level, entity, change, why, expected, judged-by metric + guardrail, baseline numbers, eval date, then result, verdict and decision.
- Verdict rules live on the "How we judge changes" tab: equal before/after windows (≥14 days, 28 for bidding/budget), ±10% threshold, ≥20 purchases a side, hygiene changes are "Not measurable".
- To refresh: re-pull with the Google Ads API (scripts in session scratchpad were ad hoc), upload new JSON with Artifact `asset: true`, then `update` the dataset's `source.url`, `name`, `updated`.
