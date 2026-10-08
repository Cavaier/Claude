# Kickoff for the Meta static ads chat (paste this as the first message of the new chat)

I'm Eli at Cavaier. We already started a Black Friday static-ads lab in another chat; continue it here. Read this whole message before doing anything. When I say **run**, you make the next 10 ads.

## Where things are
- **The canvas (keep using this one, don't make a new one):** https://claude.ai/artifact/PWhEp18Jbd4yd9WMA2kZto ("Cavaier Static Ads Lab", Design canvas type). Read `project/canvas.json` first. It already holds Run 1: M Batch 467, 468, 469 and W Batch 415, plus the reference columns and a brief note. Continue with **M Batch 470** and **W Batch 416**.
- Repo: Cavaier/Claude, branch `claude/sharp-franklin-iy8kax`, folder `bfcm26/`. Email master page (offer facts): https://claude.ai/artifact/21hL1pG8bndjPaBr8p8G6S (read only).
- **References to imitate: IM8 Health's top image ads** (Meta page 345914995276546). Pull them with Trendtrack `search_ads` (query "IM8 Health", search_in brand, media_type image, status all, sort_by reach, about 1.5 credits per ad). Run 1 used the top 20; continue from page 2 so no reference repeats. Download the media URL of each one you use.

## Image sources (use variety; fall back to the plain Shopify shots only when nothing better fits)
1. **My winning static ads in the Meta ad account** (Meta connector): find the best image ads by results, and use their images so the ads don't all share the same base photos.
2. **Figma, file `dEEVzBXoylSdZoRs0gonHn`, page "Static Ads 2" (node 3096-171):** https://www.figma.com/design/dEEVzBXoylSdZoRs0gonHn/Cavaier?node-id=3096-171. It has about 220 frames named "… No Text(s)" (clean images of earlier batches) and a section "Proven Ads - STATICS" (18 proven winners). Use only images that show the **3x set or the 2x Duo set**. Render them with the Figma REST API (FIGMA_TOKEN): `GET /v1/images/:key?ids=…&format=jpg`; some render URLs return 404, skip those.
3. **Live Shopify listings** (always pull fresh, never a cached copy): handles `3x-minimal-stack-set-for-him`, `3x-minimal-stack-set-for-her`, `2x-duo-minimal-set-for-him` (`https://cavaier.com/products/<handle>.json`, images with `?width=1500`). Note: the "for her" 3x listing photos show a man's arm, so they count as men's images.
4. Already uploaded to the canvas: Shopify 3x shots, 2x Duo black / silver / gold, my black 2x Duo close-up, the jewelry case, the logo, and one women's gold 3x photo (low resolution).

## Rules
- **Products:** only the **3x Minimal Stack Set** and the **2x Duo Minimal Set**.
- **Angle:** Black Friday, **30% off sitewide** (no code, taken off at checkout), said in different ways and wordings.
- **No prices or currency symbols on any ad.** The same ads run in the EUR and USD accounts, so the offer is always "30% off".
- **Format:** always 9:16, 1080×1920. Keep key text out of the top 270 px and the bottom 384 px.
- **Batches:** 3 creatives per batch, named `M Batch 470 - C1`, `C2`, `C3` (men) and `W Batch 416 - C1`, `C2`, `C3` (women), numbers counting up. A batch is **men only or women only, never mixed**, and no single ad shows both.
- **One IM8 reference per batch.** C1, C2 and C3 are three iterations of that one concept, each **visually very different** (different photo, composition, colour field, wording). Use different images within a batch when good ones exist.
- **Canvas layout:** one batch per row: a narrow column on the left with the IM8 reference (420×1920 artboard), then C1, C2, C3 side by side.
- **Imitate the reference closely.** Don't be too strict on my branding: copy the reference's layout, colour blocking, overlays, badges and text placement much more literally (for example, the IM8 checklist ad's dark red full-bleed photo with the checklist straight on the image, not a white card), and swap in my product, photos, logo and copy.
- **Font:** Figtree like cavaier.com. Headings uppercase, regular (400) or light (300), no extra letter spacing; labels uppercase with 0.1em spacing; body 400, emphasis 500. Bodoni wordmark = the logo image. Brand red is `#A82C24`.
- **Only true claims:** waterproof, sweat and heat resistant · recycled 316L stainless steel · adjustable S/M/L · black, silver or gold · jewelry case included with sets ("case included", never "free case") · free shipping (check the US store too) · Trustpilot 4.5, 3,000+ reviews. Nothing invented.
