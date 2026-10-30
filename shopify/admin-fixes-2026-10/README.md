# Store fixes from the Q4 theme audit (Oct 2026)

Store settings, not theme files, so they work in every theme (live and all scheduled ones).
They need the Shopify connector in Claude (or someone in Shopify admin).

## International store (cavaier.com)
1. **Phone menu "Reviews"** (bottom block of the phone menu, admin menu `reviews`): its one item links to a customer-account page
   (`account.cavaier.com/pages/83c32665-6c37-4ad0-a13c-bd21069b037f`), so shoppers who are not signed in land on the sign-in page.
   Change the item's link to the Reviews page (`/pages/reviews`). Fixes the live and all scheduled themes at once.
2. **Cookie page** `/pages/cookie-declaration`: replace the Cookiebot embed with `cookie-page.html` (Online Store > Pages > Cookie Declaration > Show HTML).
   Add the translations from `cookie-page-translations.json` (one per store language).
   The button opens Shopify's own cookie panel; where Shopify shows no banner it goes to the privacy choices page.
3. **Gift card options**: rename `€10,00 … €1 000,00` to `€10, €25, €50, €100, €250, €500, €1000`
   (no thousands separator, so it reads the same in every language).
4. **FAQ pages**: `/pages/faq` (theme sample text) and `/pages/faq-2` (empty) are not linked anywhere.
   Hide both and redirect them to `/pages/contact-us-2`.

## US store (us.cavaier.com)
1. **FAQ**: put `us-faq-page.html` into `/pages/faq` and set its template to the default page template (it uses a PageFly template now).
2. **Old FAQ** `/pages/1-faq-2023-09-01-16-31-5` (outdated: "free shipping over $35", "6–10 days"): hide it and redirect it to `/pages/faq`.
3. **Menus**: header "FAQ", phone menu "FAQ" and footer "FAQ" link to the old page. Point them to `/pages/faq`.
4. **Cookie page**: same `cookie-page.html` as above (English).
5. **Gift card options**: rename `10,00 $ … 1 000,00 $` to `$10, $25, $50, $100, $250, $500, $1,000`.

PageFly is no longer used: after these steps no page depends on it, so the app can be uninstalled.
Edit these pages in the HTML view (`<>`), since the visual editor can strip the FAQ styling.
