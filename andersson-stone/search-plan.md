# Andersson Stone – Search plan: first sales from new customers

Google Ads 842-044-6950 · 2026-10-11 · **nothing has been changed in the account yet**

## 1. Data the plan is based on
- **Keyword Planner (historical metrics, Sep 2025–Aug 2026), one run per country**: SE, DK, DE, NL with the right location. Volumes are rounded by Google (50/500/5,000…) because the account has no spend history.
- **Google autocomplete**: 9,604 real search queries, used to find buyer phrases and build the negative list.
- **Shopify (read-only)**: 97 products, EUR prices, markets. 0 orders so far.
- **Buy-in prices (SEK)**: earrings and tennis bracelets (786 variants). Rings missing.

## 2. Demand and click prices per market (deduplicated)
| Market | Earrings vol/mo · CPC* | Tennis vol/mo · CPC* | Rings vol/mo · CPC* |
|---|---|---|---|
| Sweden | 7,550 · 7–24 kr | 7,950 · 5–19 kr | 69,000 · 12–28 kr |
| Denmark | 7,700 · 6–21 kr | 7,850 · 8–22 kr | 62,000 · 9–22 kr |
| Germany | 7,850 · 6–24 kr | 13,900 · 6–18 kr | 594,000 · 14–36 kr |
| Netherlands | 6,900 · 6–23 kr | 7,850 · 5–16 kr | 68,000 · 12–29 kr |

*Top-of-page bid low–high, volume-weighted.

Conclusions:
- **Earrings and tennis bracelets**: similar volume (7–14k/mo per market) and cheap clicks (5–24 kr), plus high margin (lab-grown earrings 71%, tennis 60%). → **The engine for first sales.**
- **Rings**: 10–80× more volume, but 2× the price per click, unknown margin and a more complex purchase (setting + diamond). → Only specific terms (gold, white gold, oval, diamond, lab-grown). **The 6 huge generic terms** (verlobungsring 500k, förlovningsring, forlovelsesring, verlovingsring… 50k each) **wait until phase 2**.
- **Men's tennis bracelets**: 500/mo in SE, DE and NL at 3–14 kr. Cheap traffic for the 19–21.6 cm lengths.
- **Lab-grown**: low volume (50–500 per term) but strong intent. In Germany lab-grown rings are expensive (16–59 kr).

## 3. Structure: one campaign per market
Budget is set per campaign. Germany has 2–10× the volume of the other markets, so campaigns are split **by market** so each country gets a controlled budget. Product categories become ad groups, each with its own bid.

| Campaign | Budget/day | Ad groups |
|---|---|---|
| **S-SE \| Non-brand** | 250 kr | Earrings (Diamond earrings, Gold, Lab grown, EN: Diamond studs, Lab grown) · Tennis (Tennis bracelet, Gold, Lab grown, Men, EN) · Rings (Engagement ring, Solitaire/diamond ring, Lab grown, EN) |
| **S-DE \| Non-brand** | 250 kr | Earrings (Diamond studs, Gold, Lab grown, Carat/shape) · Tennis (Tennis bracelet, Gold, Lab grown, Men) · Rings (Engagement ring, Diamond ring, Lab grown) |
| **S-NL \| Non-brand** | 200 kr | as DE + English lab-grown ad groups |
| **S-DK \| Non-brand** | 200 kr | as DE |
| **Total** | **900 kr/day (~€80)** | 56 ad groups, 233 keywords (`search-keywords.csv`) |

- Keywords: exact + phrase match. 6 generic ring terms in phase 2, 6 duplicate variants removed (Google groups singular/plural).
- Every ad group sends people to the collection in its language (/sv, /da, /de, /nl or English).
- Location: "presence" only (people in the country). Language: the local language + English.
- Networks: Google Search only. Search partners and Display off.
- Negatives: `negative-keywords.txt`, shared list + extra lists for earrings and rings.

## 4. Bidding
- **Phase 1 (weeks 1–3): manual CPC per ad group**, so spend between categories is controlled while there is no conversion data. Bids (`ad_group_max_cpc_sek`) = top-of-page low + 40% of the range, capped at 20 kr (earrings), 18 kr (tennis), 25 kr (rings) and 10 kr (men's).
  - Typical bids: tennis 9–13 kr, earrings 11–16 kr, rings 12–25 kr.
- **Expected outcome at 900 kr/day**: ~80–110 clicks/day ≈ 2,500–3,300 clicks/month. At a 0.5–1% conversion rate ≈ **12–30 purchases/month**. Average order (lab-grown) ~10,000–18,000 kr gives revenue of roughly 150k–450k kr on ~27k kr spend. *This is an estimate. The real conversion rate is the big unknown and is measured in the first 2–3 weeks.*
- **Phase 2 (from ~15 purchases): Maximise conversion value.** Then add the generic ring terms with their own budget.
- **Phase 3 (≥30 purchases/30 days): target ROAS 350%** (break-even ~180–210% for lab-grown earrings and tennis, 300% for natural earrings; see buy-in analysis). Lower towards 250% if volume is too low.

### Margins (buy-in, SEK, median per variant)
| Category | Price incl. VAT | Buy-in | Margin excl. VAT | Break-even ROAS |
|---|---|---|---|---|
| Earrings lab-grown | 18,599 | 4,541 | 71% | ~180% |
| Earrings natural | 49,099 | 23,071 | 41% | ~300% |
| Tennis lab-grown | 54,199 | 17,282 | 60% | ~210% |
| Tennis natural | 174,699 | 57,266 | 60% | ~210% |

## 5. Ads
One RSA per ad group in its language (8–15 headlines, 4 descriptions), with the keyword theme in headlines 1–2. Messages:
1. Product + keyword ("Diamantörhängen i guld", "Tennisarmband mit Diamanten", "Lab-grown diamond tennis bracelet")
2. Price anchor in local currency ("Från 5 649 kr", "Ab 499 €")
3. Proof: IGI-certified · conflict-free (Kimberley Process) · 9K/14K/18K gold or platinum
4. Risk reducers: insured DHL Express · delivered within 10 days · 30-day returns · Klarna
5. Made to order in your choice of gold and diamond

Assets: sitelinks (Earrings, Tennis bracelets, Rings, Conflict-free diamonds), callouts, structured snippet (Shapes), price assets. Nothing that isn't on the site.

## 6. Before launch
- [ ] Test purchase recorded in Google Ads
- [ ] Site fixes live (address, contact page, About page, delivery time)
- [ ] Buy-in prices for rings (ROAS target for rings)
- [ ] Approve budget (900 kr/day) and markets
- [ ] Old PMAX campaign stays paused

## 7. Follow-up
- Day 2–3: search terms report → negatives (biggest early win).
- Week 1–2: ad groups with clicks but no add-to-carts → lower bids. Compare markets.
- Week 3: move budget to the best market/category, switch to Maximise conversion value.
- December: test the generic ring terms (Christmas/New Year's proposals).
- Once Merchant Center is approved: Shopping/PMax alongside Search.
