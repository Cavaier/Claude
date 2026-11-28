# Andersson Stone – handoff (state as of 24 Oct 2026)

Read this first when continuing Andersson Stone work in a new session or channel. Account states may have changed since this was written; re-check them before acting.

## Ground rules from the owner
- **Google Ads:** Andersson Stone only, customer ID **842-044-6950** (`8420446950`).
  - Login customer ID `9574419833` (Cavaier MCC). Ignore `GOOGLE_ADS_CUSTOMER_ID`, which points to a different account. Never touch other accounts.
  - Don't send a developer token. API access runs through Google Cloud project "cavaier-ads" with Explorer access: 2,880 operations a day, shared with another chat. Keyword Planner is not available through the API.
  - API v22 is deprecated; use **v23**.
- **No changes without the owner's approval.** Propose first, then apply.
- **Shopify:** store `tdngxf-ev.myshopify.com` (anderssonstone.com).
  - Admin GraphQL `2025-07`, using a client-credentials token from `ANDERSSON_CLIENT_ID` / `ANDERSSON_CLIENT_SECRET`.
  - Keep tokens in memory only; writing them to disk is blocked.
- **Merchant Center:** account `5710276899`, read through the Merchant API (`merchantapi.googleapis.com`) with the same OAuth token. Writes to Merchant Center were blocked by the permission classifier, so the owner made those changes in the UI.
- No brand campaign for now; the store is too new.
- The jewellery is for women; don't target men's terms.

## Google Ads – current state
| Campaign | ID | Status | Notes |
|---|---|---|---|
| S-SE / S-DE / S-NL / S-DK \| Non-brand (Search) | 24348441967 / 24342394688 / 24342393722 / 24342393731 | **Paused 22 Oct** | Manual CPC, exact + phrase. Budgets when paused: DE 200, SE 150, DK 100, NL 50 kr/day. |
| SH-DE \| Earrings (Standard Shopping) | 24380363469 | Enabled, **but has no products** | Germany only, feed label `EUR_106462478667`, 150 kr/day, manual CPC. Earrings were deleted from Shopify on 23 Oct. |
| PMAX | 23460547174 | Paused | Old campaign; leave it. |

- **Shared negative list:** "AS \| Shared negatives", ID 12269552252, about 245 phrase terms. Attached to all campaigns.
- **Conversions:** the Google & YouTube app actions. "Google Shopping App Purchase" is primary.
- **Known bug in SH-DE price tiers:** the item-ID listing groups were built as `shopify_zz_<productId>_<variantId>` from Shopify IDs. These **don't match** the feed's real offer IDs, so the tier nodes matched nothing and everything fell into the 7 kr "everything else" node. If you rebuild tiers, read the real `offerId` values from Merchant Center.

### Results 11–24 Oct
- About 8,300 kr spent (all on Search), about 575 clicks, **0 orders**.
- About 4 add-to-carts and 3 checkout starts: Germany 18 Oct (engagement ring), Netherlands 21 Oct, one more on 22 Oct with unknown source.
- **Germany:** most add-to-carts and checkouts, all on the engagement ring.
- **Sweden:** most engaged visitors, but the owner says Swedish data may be inflated by family visits.
- **Netherlands:** weakest at first, then produced a checkout.
- **Denmark:** 0 add-to-carts, visits of about 1 second.
- Shopping spent 0 kr: 7 impressions in total.
- Likely reasons nothing sold: new store with no reviews or trust signals, a small budget spread too thin, and the delivery time on the site not matching the ads.

## Shopify – changes made (all approved)
- **Theme:** scroll-reveal animation and page transitions turned off.
- **Engagement ring rename:** "Solitaire ring 1" became "Classic 4-Prong Solitaire Engagement Ring", with translations into sv/de/da/nl.
- **Other ring renames:** 23 numbered ring settings got descriptive names.
  - "…Marquise and Round Accents" became "…Marquise and Brilliant Accents", to keep it out of the automatic "Round Diamonds" collection.
  - All 51 ring titles are translated into sv/de/da/nl.
- **New collection "Engagement Rings":** handle `engagement-rings`, manual, 16 rings, template suffix `rings`, translated into 7 languages. The products are the same ones, not duplicates.
- **Main menu:** Earrings · Tennis Bracelets · Engagement Rings · Rings · Contact, translated. The owner wants Rings kept alongside Engagement Rings.
- **Theme snippet `as-label-text.liquid`:** products in `engagement-rings` show the label "Engagement ring", localised, instead of "Ring". A backup of the old snippet existed only in the session scratchpad.
- **Theme `templates/product.json`:** earring delivery estimate changed from 7–14 to 7–10 days. Default (rings) is 7–14; tennis bracelets are 25–35.

## Open issues (as of 24 Oct)
1. **Earrings and tennis bracelets were deleted** from Shopify on 23 Oct around 09:20 UTC, by a user in Shopify admin.
   - The store now has 67 products: 51 settings, 10 "Completed Ring" and 6 diamonds.
   - The owner hasn't yet said whether this was intentional.
   - The Earrings and Tennis Bracelets menu links now go to empty collections.
2. **Merchant Center business info:**
   - Customer service email is a Cavaier address, not an Andersson Stone one.
   - Phone is unverified.
   - Town and region are swapped (should be locality Järfälla, region Stockholm).
   - The return policy has an empty return window (the site says 30 days).
3. **Delivery promise:** Merchant Center says at most 10 days, rings show 7–14 on the site, tennis 25–35.
4. **No reviews, launch offer or trust proof** on the site. Payment methods for Germany (PayPal, Klarna) haven't been checked.
5. **Buy-in prices for rings** are unknown, so ring ROAS targets can't be set.

## Suggested next step (pending the owner's answer)
- **If earrings are gone for good:** pause SH-DE \| Earrings and build a Germany engagement-ring Shopping campaign (the 16 rings in `engagement-rings`, about 150 kr/day, real offer IDs). Show it to the owner paused before enabling. Tidy the menu.
- **If earrings come back:** re-import them, then fix the SH-DE price tiers using real offer IDs.

## Margins (buy-in, SEK, median per variant)
| Category | Margin excl. VAT | Break-even ROAS |
|---|---|---|
| Earrings, lab-grown | 71% | about 180% |
| Earrings, natural | 41% | about 300% |
| Tennis bracelets | about 60% | about 210% |

## Files in this folder
- `search-plan.md`: the original Search plan.
- `search-keywords.csv`, `negative-keywords.txt`, `keyword-planner/`, `research-autocomplete-queries.csv`: keyword research.
- `build/`: build scripts for the Search campaigns.
