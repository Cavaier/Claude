# Andersson Stone – Search campaign plan (new customers)

Google Ads account 842-044-6950 · drafted 2026-10-11 · nothing has been changed in the account.

## Starting point
- Catalogue (97 products, prices in SEK, ~11.2 SEK = €1):
  - Diamond stud earrings (31): lab-grown from ~€500 (0.25 ct) up to ~€3,300 (3 ct); natural from ~€700 up to ~€26,000.
  - Tennis bracelets (13): lab-grown ~€1,800–€11,000; natural ~€6,100–€38,000.
  - Ring settings (51) from ~€510–€3,100, plus the centre diamond (build your own ring).
- The site is in 8 languages (en, sv, da, de, fr, it, nl, es), with insured DHL Express from Sweden and 30-day returns.
- Shopify (Admin API, read-only): **0 orders so far**, no cost prices entered, so margin is unknown. Inventory isn't tracked (made to order). Markets: Sweden (SEK), Denmark (DKK), Norway (NOK), Switzerland (CHF), International/EU (EUR), Rest of world (EUR excl. VAT). EUR prices from: earrings €499 (median €1,549), tennis bracelets €1,799 (median €3,399), ring settings €510 (median €750) plus the diamond.
- Account history: 0 conversions. The Purchase action ("Google Shopping App Purchase") is the only goal Google bids on.
- Keyword Planner can't be used through the API with "Explorer" access. Search volumes and CPCs need either a Keyword Planner export from the UI or Basic API access.

## Prerequisites before launch
1. Test purchase recorded in Google Ads.
2. Site fixes live: one address, contact page, About page, production and delivery times.
3. Search ads do **not** depend on the Merchant Center suspension, so Search can launch before Merchant Center is approved.

## Campaign structure
| Campaign | Share of budget | Why |
|---|---|---|
| S-Earrings | 35% | Lowest entry price (~€500), the largest gift market, Christmas demand from November |
| S-Tennis | 35% | Highest order value relative to CPC, lab-grown gives a clear price advantage |
| S-Rings | 25% | Highest CPCs and competition; only precise terms (lab grown, shape, style) |
| S-Brand | 5% | Cheap, protects brand traffic, kept separate so it doesn't inflate non-brand results |

- One campaign per product group and **one language per ad group**. Each ad group sends people to the matching language version of the collection (/sv, /de, /nl, /da).
- Match types: exact + phrase. Broad match only once Smart Bidding has 30+ conversions.
- Networks: Search only. Search partners and Display off.
- Locations: "presence" only (not "presence or interest"). Markets phase 1: **Sweden, Denmark, Germany, Netherlands** (EU, no customs, site language available). Phase 2: Norway, Finland, Austria, Belgium, UK, depending on results.
- Brand keywords are excluded as negatives in all non-brand campaigns.
- Shared negative keyword list: see `negative-keywords.txt` (cheap, silver, moissanite, jobs, competitor brand names, etc.).

## Bidding and budget (estimate, check against the Keyword Planner export)
- Assumption: CPC €0.80–2.50 for non-brand jewellery searches in Northern Europe, conversion rate 0.5–1.5% for high-ticket items, average order ~€1,000–2,000.
- That gives a cost per sale of about €100–400, and a return on ad spend (ROAS) of roughly 4–15x.
- Phase 1 (weeks 1–3): **Maximise clicks with a max CPC cap of €2.50**, or Manual CPC. Budget about **€80/day** total (~SEK 900).
- Phase 2: from ~15 purchases, **Maximise conversion value**. Begin checkout may be used temporarily as an extra signal.
- Phase 3: from ~30 purchases in 30 days, a **tROAS target of 500–600%**, then raise budget in 20% steps.
- "New customers only" (customer acquisition) needs an audience list of ≥1,000 customers. Until then, nearly every purchase is a new customer anyway.

## Ads (RSA per ad group, keyword in headline 1)
Examples, English (translate for sv/de/nl/da):
- Headlines: "Lab-Grown Diamond Tennis Bracelets" · "From €1,800 – Made to Order" · "IGI-Certified Diamonds" · "Free Insured DHL Express" · "30-Day Free Returns" · "9K, 14K & 18K Gold or Platinum" · "Natural or Lab-Grown – You Choose" · "Swedish Fine Jewellery"
- Descriptions: "Every piece made to order in your choice of gold and diamond. Delivered insured within 10 business days." · "Conflict-free natural or lab-grown diamonds with independent certificates. 30-day returns."
- Assets: sitelinks (Earrings, Tennis bracelets, Rings, Conflict-free diamonds), callouts, structured snippets (Shapes: Round, Oval, Pear, Princess, Emerald), price assets.
- Don't promise anything the site doesn't deliver, because that hurts the misrepresentation review.

## Timing
- Launch in late October, so the campaigns learn before Black Friday/Christmas (earrings and tennis bracelets as gifts).
- Engagement season Dec–Feb (Christmas/New Year's/Valentine's proposals), so increase the Rings budget from December.

## Follow-up
- Day 2, 7 and 14: search terms → negatives, CPCs, impression share, conversions.
- Check whether the purchase tag fires correctly in every language version.
- Once Merchant Center is approved: PMax/Shopping alongside Search, with brand terms excluded.
