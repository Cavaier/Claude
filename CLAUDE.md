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
