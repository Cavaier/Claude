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
- Only campaign: **Brand Search** (renamed from "Brand Search | WW" Oct 11; Search, target
  impression share 95% absolute top, max CPC 10 SEK, budget 300 SEK/day shared by all languages,
  worldwide except US). Since Oct 11 one ad group per language: English, German, Dutch, Spanish,
  French, Hebrew, Japanese, Italian, Chinese, Swedish, Polish, Norwegian, Danish. Each has the
  same brand keywords (exact: cavaier, cavaier jewelry, cavaier jewellery, cavaier bracelet,
  cavaier.com, cavaierofficial; phrase: cavaier, cavaierofficial) + local exact keywords, one RSA
  in its language (15 headlines, 4 descriptions, "Cavaier – Official Store" pinned first), 4 callouts,
  1 "Types" snippet, and 2 local Women/Men sitelinks (English uses the campaign-level ones).
  Landing pages: cavaier.com, cavaier.de, cavaier.nl, cavaier.com/es, cavaier.fr/fr, cavaier.com/he,
  cavaier.com (Japanese), cavaier.it/it, cavaier.com/zh, cavaier.se/sv, cavaier.pl, cavaier.no,
  cavaier.dk. Ad texts: scratchpad brand_spec.py (copy in google-ads/brand-search-ads.json).
- Store languages (Shopify, Oct 11): translated pages exist for de, nl, es, fr, he, it, zh-TW (/zh),
  sv, pl, nb, ar, id, pt-PT, th. Note cavaier.fr, .it, .es, .se default to English; the local
  language is at /fr, /it, /es, /sv. **No Japanese or Danish** on any domain yet (ja is published
  but not on a domain; no da locale) → those ads link to English pages until Eli adds them.
- Automatically created ad-group assets (sitelinks to login/contact/FAQ, old callouts) were
  overriding the clean sitelinks; 32 removed Oct 11. Text asset automation is opted out. Check
  at every evaluation that none come back.
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

### Research: campaign structure for local languages (Oct 11, 2026)
- Google removed the campaign language setting from Search (announced Aug 14, 2026, live from
  late Sept 2026). Ads are now matched by the language of the ad + landing page. For searches
  with no clear language (brand names like "cavaier"), Google shows the ad in the user's most
  preferred language. If several campaigns/ad groups in different languages are eligible,
  Google picks the one in the user's language. Google does not translate ads. No language
  exclusions. Source: support.google.com/google-ads/answer/1722078, ppc.land, SERoundtable.
- So P-003 (all languages) is moot now: the setting no longer exists.
- Consequence for per-country campaigns: a German-only campaign in Germany may show no ad to
  an English-preferring searcher there. Per-language ad groups in one campaign avoid that.
- Agency guides (Go Fish, Search Engine Land, Meticulosity) still default to one campaign per
  country/language for control; trade-off is more budgets and management.

### Brand search terms (12 months to Oct 10, 2026, Google Ads)
- Top: cavaier 13.6k impr / 536 purchases · cavaier jewelry 5.5k / 352 · cavaier bracelet 1.6k / 77 ·
  cavaier (jewelry) reviews ~2.2k / 48 · cavaier official 411 / 20 · cavaierofficial 254 / 20.
- Local-language brand searches seen: armband 175 (12 purch.), bijoux 118 (11), gioielli 71 (9),
  schmuck 59 (9), erfahrungen 64 (6), armbånd 26, opinie 29, recensioni 8; Chinese 香港 82 (3.5),
  評價 86, hk 28; Japanese アクセサリー 40, 日本 9, 口コミ 2. No Hebrew terms (ads were English-only).
- Phrase "cavaier" already reaches all of these; exact local keywords help Google route the
  search to the ad group in the matching language.
- Shipping: free standard shipping on all orders (shipping policy, confirmed by Eli Oct 11).
- Reviews: 4.5/5 from 3,000+ reviews (Eli, Oct 11). No lifetime warranty anymore: the live brand
  RSA still says "Lifetime Warranty" → replace via P-004. Shopify product texts checked: no
  warranty or old review claims.

### Brand budget analysis (Oct 11, 2026)
- Brand keywords only, 30 days to Oct 10: 1,132 impr at ~33% IS, 606 clicks, 2,276 SEK, 50.5 purchases,
  31,260 SEK (ROAS 13.7; 45 SEK/purchase; CPC 3.76; conv. rate ~8%; order ~620 SEK). The broad
  "cavaierofficial" took 6,762 SEK of the 9,039 SEK in the same period (5.5 purchases).
- Full brand coverage estimate: ~3,400 impr, ~1,800 clicks, ~6,800 SEK/month (~230 SEK/day).
- Lost IS to rank on exact brand ~1–2%, CPC ~3 SEK → little or no competition on "cavaier".
  Auction insights are not available through the API (UI only). Trendtrack shows no other
  advertiser using "cavaier" in ad text.
- Shopify last click (utm_campaign 21651817099): Jul 38, Aug 28, Sep 38 orders; 75% new customers.
  Google-referred orders (organic + paid) ~250/month (Sept 142) → paid brand is ~15% of Google orders.
- Research: eBay (Blake/Nosko/Tadelis) brand ads ~0 extra sales (strong brand, top organic, no
  rivals); Edmunds lost ~50% of paid traffic when off; Bing 824-firm study: bigger effect for
  lesser-known brands; vendor holdout tests 20–50% incremental. Competitor bidding raises it.
- Break-even: a brand click earns ~52 SEK revenue. Brand pays off if extra share × margin × 52 >
  CPC. At 60% margin and 20% extra: ~6 SEK per click; at 50% extra: ~15 SEK.
- Revised after the account history: P-008 = budget 150 SEK/day + CPC cap 4 SEK; P-009 country
  holdout in January to confirm.

### Brand Search history and natural experiment (Oct 11, 2026; Google Ads + Shopify)
- Brand terms by month: 2025 ~1,000–2,100 clicks/month at CPC ~1.7–2.5 SEK, 1,000–4,500 SEK/month.
  2026 CPC rose to 3.3–4.0 SEK and clicks fell to ~600–800/month (Jul–Sep), budget eaten by broad.
- Non-brand (broad) spend Jul 2025 – Oct 2026: ~58,000 SEK for ~6.5 purchases.
- Brand Search fully off Apr 12 – May 20, 2025 (39 days; Shopify has no referrer data then).
- **Brand keywords off Dec 12, 2025 – Feb 9, 2026** (all budget to broad). Shopify Google-referred
  orders (paid + organic; brand-ad orders are counted as referrer google) as share of all orders:
  Nov 17 – Dec 14 (ads on, peak season) 14.0% (446/3,184); Dec 15 – Feb 8 (off) 12.0% (654/5,450);
  Feb 9 – Mar 15 (on again) 11.3% (294/2,591), while ads claimed ~40 purchases/week. No rise when
  ads came back → most brand-ad sales would have come through the organic result anyway.
  Caveats: not randomized, seasonality, Meta mix; still the cleanest signal available.

### Non-brand / new-customer analysis (Oct 11, 2026)
- Every non-brand campaign since 2024 lost money: ~160,000 SEK total. Demand Gen Women 34k SEK
  ROAS 0.12; P-Max Women UK 22k 0.41; P-Max Norway 19k 1.23; PMax retargeting UK 17.7k 1.44;
  Demand Gen Men 10.7k 0.75; Shopping bracelets 10k 0.82; generic search men UK (Jan 2025)
  4.8k SEK / 2 purchases; generic search women UK 2.5k / 0; DSA 2.8k 0.48.
- Non-brand search terms all time: 11,099 SEK, 17.5 purchases; 12 of them from "caviar bracelet"
  (186 clicks, 694 SEK) = people mishearing "Cavaier" → treat as brand misspelling.
- Keyword Planner is not available via API (developer token has explorer access only).
- Shopify 90d: 5,457 orders, €393k, AOV €72.8; 4,419 new vs 955 returning customers. 3x Minimal
  Stack Set (men + women) = ~2,670 orders / €242k (~60% of sales, AOV ~€91). Then Cube, Rope,
  Minimal Cuff, Role bracelets (~€20–35).
- Customer Match list "817 Buyers" is too small to use (search size 0). Remarketing lists: product
  viewers 180d ~73k (search).
- Vacier (vacier.com): Swedish, "Timeless Versatile Jewelry from Sweden", near-identical offer
  (bracelets, necklaces, rings, sets; adjustable; free shipping over €35; lifetime warranty; 4.96/5
  from 14k reviews; Trustpilot 4.9 from 3.4k). "vacier" searches in our account: ~80 impressions
  all time, 1 purchase. Bidding on "vacier" risks Vacier bidding on "cavaier".
- Proposals: P-010 misspellings, P-011 UK non-brand search test, P-012 Customer Match +
  new-customer goal, P-013 hold on Vacier. Shopping/PMax (after feed fix) is the main Google
  route to cold buyers for a visual product.

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
- "cavaierofficial" is Cavaier's Instagram handle: a real brand search. Cover it with
  [exact] and [phrase], never broad.
- Localized brand campaigns: every market gets ads in its own language (Eli, Oct 11), sized by
  Shopify orders, not Google Ads data. Each country sits in exactly one campaign; multi-language
  countries get one main language: Belgium → Dutch, Switzerland → German, Canada → English.
- Eli will translate the English country stores in Shopify (T Lab – AI Language Translate is
  installed).
- Pick local brand campaigns by data (Shopify orders per language), not by whether the store is
  translated yet (Eli, Oct 11). First wave: every language with ~150+ orders in 90 days:
  German, Dutch, Spanish, French, Hebrew, Japanese, Italian, Chinese (HK). Eli added Polish,
  Swedish, Norwegian, Danish (Oct 11) → 12 local brand campaigns. Thai, Vietnamese, Korean,
  Portuguese and English markets stay in Brand Search | WW.
- Working method: one change at a time per campaign, logged on the Desk with baseline,
  judged by the rules on its "How we judge changes" tab.

---

## 5. Proposals and open questions

- Ask Eli: add Japanese to cavaier.com and a Danish language to cavaier.dk in Shopify (then
  point those ad groups to the local pages); consider making /fr, /it, /es, /sv the default
  language on cavaier.fr/.it/.es/.se.
- Open questions to Eli: target (min ROAS / max CPA), monthly budget and ceiling,
  weekly review day; current shipping offer for ad copy; Minimal Cuff "adjustable"
  wording; correct US shipping terms for US product texts.
- US: us.cavaier.com cannot be claimed in Merchant Center 5087698947 while 747874697 claims
  cavaier.com (all 194 US products disapproved). Fix when US ads start (shared parent account).

---

## 6. Log (newest first)

- **2026-10-11** Non-brand / new-customer analysis (section 3); proposed P-010 to P-013.
- **2026-10-11** Brand budget analysis + account history (section 3): Dec–Feb natural experiment shows
  little extra from brand ads; proposed P-008 (150 SEK/day, CPC cap 4) and P-009 (holdout test).
- **2026-10-11** Executed Brand Search makeover (C-009, P-004, P-006, P-007): renamed, English
  ad group merged, 12 language ad groups with ads/keywords/sitelinks/callouts/snippets, 32 auto
  assets removed, old English ad paused after new one approved. All verified against the spec
  (0 differences). Snapshot before: google-ads/snapshots/brand-search-before-2026-10-11.json.
  Evaluate P-004 Oct 25, P-006 Nov 1 (local ad's share of impressions in its countries ≥70%).
- **2026-10-11** Researched structure (section 3): proposed one brand campaign with an ad group
  per language instead of 12 country campaigns; awaiting Eli.
- **2026-10-11** Local brand campaign list set: DE, NL, ES, FR, IL, JP, IT, HK + PL, SE, NO, DK
  (Eli added the last four). Plan: build paused, launch in waves, Eli reviews ads first.
- **2026-10-11** Markets regrouped by language (Shopify, 90 days): English 1,797 orders (~€131k),
  German 613 (€43.4k), Dutch 410 (€25.3k), Spanish 348 (€26.5k: MX 176, ES 125, PE 24, CO 23),
  French 231 (€14.0k), Hebrew 193 (€15.7k), Japanese 162, Italian 158, Chinese (HK) 148,
  Swedish 89, Polish 81, Thai/Vietnamese/Korean ~200, Norwegian 69, Portuguese 55, Danish 48.
  German and Dutch ads drafted (P-006, P-007; formal Sie / u as on the stores).
- **2026-10-11** Applied P-001 (paused "cavaierofficial" [broad]; added [exact] + [phrase] —
  it's the Instagram handle) and P-003 (all languages; ads stay English). Evaluate Oct 25:
  expect brand impression share up from ~35% and spend down.
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
