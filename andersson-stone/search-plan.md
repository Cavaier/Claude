# Andersson Stone – Search plan: first sales from new customers

Google Ads 842-044-6950 · 2026-10-11 · **nothing has been changed in the account yet**

## 1. What the plan is based on
| Source | What it gave us |
|---|---|
| Shopify Admin API (read-only) | 97 products, EUR prices, markets. **0 orders so far**, no cost prices (margin unknown), inventory not tracked (made to order). |
| Google autocomplete, 1,458 lookups | **9,604 real search queries** in Sweden (sv+en), Denmark, Germany and the Netherlands (nl+en), ranked by how prominently Google suggests them. |
| Google Ads API | Account, goals and conversion setup. Keyword Planner volumes are **not** available with Explorer access. |

Not available: absolute search volumes and CPCs. → Run `search-keywords.csv` through Keyword Planner in the UI ("Get search volume and forecasts") or apply for Basic API access. The structure and keywords stay the same; only the budget split and bids get adjusted.

## 2. Products and prices (EUR)
| Category | From | Median | Comment |
|---|---|---|---|
| Diamond studs (31) | €499 (0.25 ct lab) | €1,549 | Cheapest way in, gift item |
| Tennis bracelets (13) | €1,799 (3 ct lab) | €3,399 | Highest order value, lengths 15–21.6 cm, so men's sizes too |
| Ring settings (51) | €510 | €750 + diamond | Engagement rings, build your own |

## 3. What the search data shows
1. **25–40% of all searches are not buyers for us.** Silver/zirconia (7–14%), competitor brands (5–19%), second hand, children, informational questions. → A large negative list is essential (`negative-keywords.txt`).
2. **Swedes search for lab-grown in English.** In Swedish, lab-grown is only 5–7% of queries; in English in Sweden it's 35–68%. → Separate English lab-grown ad groups targeting Sweden.
3. **Germany is the strongest lab-grown ring market.** 36% of German ring queries are about lab-grown ("labordiamant verlobungsring" and similar). Denmark 27%, Netherlands 26%.
4. **Gold terms are 15–19% of searches** (guld, weißgold, 585, hvidguld). Everything we sell is gold or platinum, so these are perfect high-intent terms.
5. **Men's tennis bracelets: 6–10%** in DE/DK/NL. Our 19.1–21.6 cm lengths fit men, so a separate ad group with lower bids.
6. Strongest competitors in searches: Christ (DE), Guldfynd (SE), Georg Jensen/Pandora (DK), Lucardi (NL), Tiffany/Cartier everywhere. People searching for those brands get excluded. Our angle against them: **lab-grown at a lower price, made to order, certified, delivered within 10 days.**
7. Drop earrings, men's earrings and men's rings, wedding bands and loose diamonds are not in the range, so they're excluded.

## 4. Campaigns (3 non-brand, no brand campaign)
| Campaign | Budget | Ad groups per market and language | Landing page |
|---|---|---|---|
| **S-Earrings** | 35% | Diamond earrings · Gold · Lab grown · Carat/shape | /{lang}/collections/earrings |
| **S-Tennis** | 35% | Tennis bracelet · Gold · Lab grown · Men | /{lang}/collections/tennis-bracelets |
| **S-Rings** | 30% | Engagement ring · Diamond/solitaire ring · Lab grown | /{lang}/collections/rings |

- **258 keywords** (`search-keywords.csv`), 251 of them confirmed directly in Google autocomplete. Each ad group is one market + one language and sends people to the matching language version of the site.
- Match types: **exact + phrase**. No broad match until there are 30+ conversions.
- Markets: **Sweden, Denmark, Germany, Netherlands**. Location: "presence" only. Language targeting: the market's language + English.
- Networks: Google Search only (no Search partners, no Display).
- Ad schedule: all hours at first. Evaluate per hour after 2–3 weeks.
- Devices: all. Check mobile vs desktop after 2 weeks (high-ticket items often convert better on desktop).

## 5. Bidding and budget
- **Phase 1 (weeks 1–3): Maximise clicks with a max CPC cap of €2.00**. Without conversion history, Smart Bidding has nothing to optimise from. Budget **~€80/day** total (€28 Earrings, €28 Tennis, €24 Rings).
- **Phase 2 (from ~15 purchases): Maximise conversion value.** Begin checkout may be used temporarily as an extra conversion signal if purchases are too few.
- **Phase 3 (≥30 purchases in 30 days): target ROAS.** Based on buy-in prices (SEK, 786 variants: earrings + tennis bracelets; rings missing):

  | Category | Median price incl. VAT | Median buy-in | Margin excl. VAT | Break-even ROAS* |
  |---|---|---|---|---|
  | Earrings, lab-grown | 18,599 kr | 4,541 kr | 71% | ~180% |
  | Earrings, natural | 49,099 kr | 23,071 kr | 41% | ~300% |
  | Tennis, lab-grown | 54,199 kr | 17,282 kr | 60% | ~210% |
  | Tennis, natural | 174,699 kr | 57,266 kr | 60% | ~210% |

  *ROAS on order value incl. 25% VAT, before payment fees, shipping/insurance and returns. Start target **350%** (buffer for fees and returns), then lower towards 250% if volume is too low.
  - Lab-grown earrings have the best margin, so they get priority in budget and ads.
- Estimate (verify with Keyword Planner): CPC €0.80–2.00, conversion rate 0.5–1.5%, order value ~€1,500 → about €100–400 per sale.
- "New customers only" needs a customer list of ≥1,000. Until then, every sale is a new customer anyway.

## 6. Ads
One RSA per ad group (8–15 headlines, 4 descriptions) in the ad group's language, with the keyword theme in headlines 1–2. Messages ranked by importance:
1. Product + keyword: "Lab-Grown Diamond Tennis Bracelets" / "Tennisarmband i guld med diamanter" / "Diamant-Ohrstecker in Gold"
2. Price anchor: "From €499" (earrings), "From €1,799" (tennis), in local currency where the site shows it
3. Proof: "IGI-certified diamonds" · "Conflict-free – Kimberley Process" · "9K/14K/18K gold or platinum"
4. Risk reducers: "Insured DHL Express – delivered within 10 days" · "30-day free returns" · "Klarna"
5. Made to order: "Made to order in your choice of gold and diamond"
- Assets: sitelinks (Earrings, Tennis bracelets, Rings, Conflict-free diamonds), callouts (Insured delivery, 30-day returns, IGI-certified, Klarna), structured snippet (Shapes: Round, Oval, Pear, Princess, Emerald), price assets, image assets.
- Never promise anything that isn't on the site (because of the Merchant Center misrepresentation review).

## 7. Before launch (checklist)
- [ ] Test purchase recorded in Google Ads (Purchase is the only goal Google bids on)
- [ ] Site fixes live: one address, contact page, About page, shipping/delivery time
- [ ] Gross margin known (sets the ROAS target)
- [ ] Keyword Planner export (adjusts budget split and bids)
- [ ] Old PMAX campaign stays paused (avoids overlap while Search learns)

## 8. Follow-up
- Day 2–3: search terms report, add negatives (expected to be the biggest early win).
- Week 1–2: keywords with clicks but 0 add-to-carts → lower bids or pause. Check per market which one converts.
- Week 3: switch bidding (phase 2) and shift budget to the best market/category.
- Once Merchant Center is approved: Shopping/PMax alongside Search. Compare results per category before moving budget.
- December: increase the Rings budget (Christmas/New Year's proposals).
