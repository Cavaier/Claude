# Cavaier video ad style rules

Set by Eli. Apply to every video ad unless he says otherwise. `cards4.js` already uses these values.

## Text and logo
- **Logo:** the CAVAIER Bodoni wordmark (`logo_white.png`), always **17px tall** on the 1080×1920 canvas.
- **White text only.** No dark/charcoal text. If a background is too bright for white, pick a different shot or
  move the text onto skin, fabric or a darker area. Don't switch the text colour.
- **Font:** Figtree. Text is small and minimal: these are the reduced sizes (30% below the first lockup draft):
  - small label (e.g. "BLACK FRIDAY"): 20px, weight 400, uppercase, letter-spacing 0.34em
  - offer numerals (e.g. "30% OFF"): 92px, weight 300, uppercase, letter-spacing 0.02em
  - supporting line (e.g. "SITEWIDE", "WATERPROOF"): 32px, weight 300, uppercase, letter-spacing 0.16em
  - sub-line under a supporting line / end card: 15px, uppercase, tracked
  - end card: wordmark, 40px hairline rule, label, line, sub-line
- Lockups fade in (0.9s) with a 16px ease-out rise. Never put text on the jewellery.
- Key text stays between y=270 and y=1536 (Meta safe zone).

## Look
- **Reference style:** Vacier's top video ads (Meta page 106321194484973): macro close-ups of jewellery on skin,
  slow, minimal, almost no text.
- **Brand tones:** Eli's reference photo is a macro of black chains on skin against soft white: neutral clean whites,
  peach-beige skin (not orange tan), deep blacks, soft light, crisp skin texture. Grade every clip towards that
  (see `specs/v5-grade.txt` for sunny footage, `build3.sh` for flat camera footage) and compare before/after frames.
- **Luxury slow motion:** use high frame rate footage and play every frame (120 fps played 4x slower, 29.97 fps output).
  Women's sessions by frame rate: 11 = 25 fps, 10 = 50 fps, 9 and 8 = 30 fps, 7 / 6 / 5 = 120 fps.
  Men Session 1 = 120 fps. Higher session number = newer.

## Offer and claims
- Black Friday, 30% off sitewide, no code needed (taken off at checkout). No prices or currency symbols.
- Only true claims: waterproof, sweat and heat resistant, recycled 316L stainless steel, adjustable S/M/L,
  black / silver / gold, jewellery case included with sets, Trustpilot 4.5 with 3,000+ reviews.
