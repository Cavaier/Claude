# Cavaier Google Ads — context book

Running memory for the Google Ads / Merchant Center / feed work. Read this before any
Google Ads task. Add to it whenever we look at something, decide something, or learn
something. Newest entries go at the top of the Log. Keep facts with dates and sources.

Live view: Cavaier Google Ads Desk — https://claude.ai/artifact/BEmCjut8iisbsUQsezpmNa
(the change log there is the record of every change; this book is the reasoning behind it).

---

## 1. Business facts

- Store: cavaier.com (Shopify `cavaierwatch.myshopify.com`), store currency EUR. Google Ads
  account currency SEK.
- Country stores (same Shopify store, Markets): cavaier.de (German), cavaier.nl (Dutch),
  cavaier.no (Norwegian, NOK), cavaier.pl (Polish, PLN). cavaier.se, .dk, .it, .es,
  .co.uk are English. No French store.
- US: separate Shopify store us.cavaier.com (`d3d79e.myshopify.com`). US visitors on cavaier.com
  end up buying there (cavaier.com: 10,204 US sessions, 3 checkouts in 90 days).
- Products: 36 active (bracelets, cuffs, chain necklaces, pendant necklaces, 4 bracelet sets,
  jewelry case, gift card). Men's (`-for-him`) and women's (`-for-her`, titles with " - ")
  versions of each design. Recycled 316L stainless steel; black, silver or gold-plated.
  Necklaces are not adjustable. Free jewelry case offer only on sets.
- Main acquisition is Meta. Brand searches on Google mostly come from people who saw Meta ads.
- Buyers decide fast: 80% of Google Ads purchases happen the same day as the click,
  86% within 2 days (Google Ads conversion lag, 90 days to Oct 10, 2026). Eli confirms
  the same on Meta. Keep the 7-day click window.

### Shopify demand by market (last 90 days to Oct 11, 2026, net sales EUR)

| Market | Orders | Net sales | Local store |
|---|---|---|---|
| United Kingdom | 716 | 50,992 | English |
| Australia | 374 | 30,363 | English |
| Canada | 350 | 27,829 | English |
| Germany | 428 | 27,228 | cavaier.de |
| Mexico | 176 | 16,236 | — |
| Israel | 193 | 15,745 | — |
| France | 231 | 13,972 | — |
| Netherlands | 233 | 13,769 | cavaier.nl |
| Japan | 162 | 12,933 | — |
| Switzerland | 125 | 11,962 | cavaier.de |
| Hong Kong | 148 | 11,496 | — |
| Belgium | 177 | 11,489 | cavaier.nl |
| Italy | 158 | 9,345 | English |
| Sweden | 89 | 5,675 | English |
| Poland | 81 | 4,888 | cavaier.pl |
| Norway | 69 | 4,405 | cavaier.no |
| Austria | 60 | 4,181 | cavaier.de |

Total 4,740 orders. German-speaking (DE+CH+AT) 613 orders / €43k; Dutch-speaking (NL+BE) 410.

Order sources (90 days, Shopify referrer): direct/unknown 1,798 · Instagram 956 + 178 ·
Facebook 971 · "cavaier" (own) 706 · Google search 648 (€44k, organic + paid) · Bing 17.

---

## 2. Account setup (state as of Oct 11, 2026)

- Google Ads 3104616697 "Cavaier" under MCC 9574419833 (MCC also holds Andersson Stone 8420446950).
- Only campaign: **Brand Search | WW** (Search, target impression share 95% absolute top,
  max CPC 10 SEK, budget 300 SEK/day, English only, worldwide). Ad groups "Exact Keywords"
  and "Phrase Keywords". All other 28 campaigns removed Oct 11.
- Conversion tracking: one primary action **"Purchase"** (7678303151, label T6oUCK-3ps0c…),
  fired by the Google & YouTube app pixel; real order values; every purchase counted;
  data-driven attribution; 7-day click / 1-day view. Six "Google Shopping App …" actions
  are secondary (observation only). Enhanced conversions on. Consent: Cookiebot →
  Shopify customer privacy → Google consent mode.
- Website tags (live, checked Oct 11): G-8KBLDWLJ7V (= Google Ads tag, AW-16488775779)
  and the Merchant Center tag (changed to GT-5NTG64C6 / MC-M8RX5JMRXT after the
  Merchant Center reconnect). No Google Analytics, no Tag Manager. Google tag has
  10 cross-domain domains (cavaier.com/.no/.es/.dk/.co.uk/.it/.pl/.de/.se/.nl).
- Linked: Merchant Center 747874697, Business Manager (411477105 — keep), Shopify
  (Customer Match list uploads only, not conversions). Google Analytics unlinked.
- Shared lists available: brand list "Cavaier", negative lists "Brand Keywords" (5),
  "Irrelevant Keywords" (16). None attached to Brand Search.
- Merchant Center 747874697: standalone (AdNabu parent removed Oct 11), Terms accepted (SE),
  address country SE, only links Shopify + Google Ads 3104616697 + Google Shopping.
  Data sources: Primary feed (API, empty), cavaier.com website crawl (514 products,
  free listings only), Judge.me reviews, promotions. Square logo pending Eli's upload
  (file `cavaier-logo-square.png` in repo; API cannot upload logos).
- **Blocker:** the Google & YouTube app does not upload products to Merchant Center
  (no "Shopify App API" source; reconnected Oct 11, still 0 after hours). Support
  message drafted for Eli. No Shopping / Performance Max possible until fixed.

---

## 3. Findings (with numbers)

### Brand Search audit (Oct 11, 2026, 90 days Jul 13 – Oct 10)
- Real brand search terms: 6,801 SEK → 148.5 purchases, 112,535 SEK revenue (ROAS 16.5).
- Broad "cavaierofficial": 19,046 SEK, 11.5 purchases, ROAS 0.57. Its non-brand searches
  (Pandora, Swarovski, Cartier, Giva, CaratLane, Tanishq, "silver bracelet for men"…):
  **14,600 SEK, 0 purchases**. Broad only brought 57 SEK of brand searches the exact/phrase
  keywords don't cover ("cavaierofficial" itself: 2 purchases).
- India 12,271 SEK / 0 purchases (almost all via broad). US 2,376 SEK / 0 (US store not
  tracked). Pakistan, South Africa, Bangladesh, Egypt: spend, 0 purchases.
- Last 30 days brand keywords show on only ~35% of brand searches: **~63% lost to budget**,
  1–2% lost to ranking (exact "cavaier" CPC ~3 SEK, QS 10). Competitors are not
  outbidding us; our own broad keyword eats the budget.
- Ad: one RSA in each ad group, ad strength Poor, 6 headlines / 3 descriptions; copy says
  "Adjustable…jewelry" and "Buy 2 Get Free Shipping" (offer to be confirmed).
- Monthly brand purchases on exact "cavaier": Feb–Jun ~55–70, Jul–Sep ~27 (demand drop or
  earlier double counting via old tracking; unclear).
- Brand Search last 28 days to Oct 10: 8,406 SEK, 53 purchases, 34,129 SEK revenue, ROAS 4.06;
  71% of search-term spend on non-brand terms.

### Tracking history
- Before Oct 11 two primary purchase actions existed ("Purchase" + "Google Shopping App
  Purchase"), but the app one recorded 0 in 30 days, so no real double counting happened
  recently.

---

## 4. Decisions (Eli)

- Only the Google & YouTube app feeds products; no third-party feeds (Simprosys removed).
- No Google Analytics, no extra Google tags.
- Keep 7-day click window (buyers decide within a day).
- Do the work myself where tools allow; destructive changes need Eli's OK.
- Old paused campaigns: removed. Don't build new campaigns until Eli says so.
- Sitelinks on brand: only Men's / Women's collection (no Sets sitelink).
- Localized brand campaigns: yes in principle for markets with a local-language store,
  sized by Shopify demand (not Google Ads data).
- Working method: one change at a time per campaign, logged on the Desk with baseline,
  judged by the rules on its "How we judge changes" tab.

---

## 5. Proposals and open questions

- **P-001** Pause broad "cavaierofficial", add [exact] — waiting for OK. Urgent: frees ~63%
  lost brand impression share.
- **P-003** All languages on the English brand campaign (ads stay English) — waiting for OK.
- **P-004** Rewrite brand RSA (12–15 headlines, 4 descriptions, no "adjustable", confirm
  shipping offer) — needs Eli's current offer.
- **P-006** Brand Search | DE: DE+AT+CH, German, German ads → cavaier.de; exclude those
  countries from WW. Judge on brand impression share (target 90%+), CTR, CPC; guardrail ROAS.
- **P-007** Brand Search | NL: NL+BE, Dutch ads → cavaier.nl. Launch ~1 week after DE.
- Later: Norway, Poland local brand campaigns if worthwhile.
- Open questions to Eli: target (min ROAS / max CPA), monthly budget and ceiling,
  weekly review day; current shipping offer for ad copy; Minimal Cuff "adjustable"
  wording; correct US shipping terms for US product texts.
- US: us.cavaier.com cannot be claimed in Merchant Center 5087698947 while 747874697 claims
  cavaier.com (all 194 US products disapproved). Fix when US ads start (shared parent account).

---

## 6. Log (newest first)

- **2026-10-11** Shopify market analysis (above). Localization plan revised: DE first, NL next.
- **2026-10-11** Applied P-002 (exclude US from Brand Search) and P-005 (sitelinks: only
  Men's/Women's with clean URLs; removed Bracelets/Necklaces sitelinks and 5 account
  sitelinks to us.cavaier.com). Evaluate Oct 25.
- **2026-10-11** Brand Search audit (section 3). Desk dashboard created.
- **2026-10-11** Removed 28 paused campaigns. "Other/Default" goal set not biddable.
- **2026-10-11** Conversion cleanup: removed duplicate app purchase, 3 wetracked.io actions,
  4 Google Analytics imports. Removed GA4 and duplicate Merchant Center tag from the app.
  Google tag domains configured. Enhanced conversions / user-provided data confirmed on.
- **2026-10-11** Merchant Center: deleted 92 Simprosys feeds + GB feed + supplemental;
  removed Simprosys, AdNabu, Google Ads 7501004470 links; unlinked old MCs 5340570137 (old
  cavaier.no) and tried 411477105 (= Business Manager, keep); address → SE; Terms accepted;
  app reconnected. Feed still empty.
- **2026-10-11** Shopify (EU + US): product types, Google gender/age group, SEO titles and
  descriptions, removed outdated offer and necklace "adjustable" text, gift card off Google.
  Backups in `shopify-backups/`.
