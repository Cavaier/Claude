# Cavaier video ad style rules

Set by Eli. Apply to every video ad unless he says otherwise. `cards4.js` already uses these values
(`LOGO_H`, `HEAD`, `SUB`).

## Text and logo
- **Logo:** the CAVAIER Bodoni wordmark (`logo_white.png`), used **once only, on the closing scene**.
  Size: **47px tall** on the 1080×1920 canvas (= 17pt as seen on a phone screen). Not on the other scenes.
- **White text only.** No dark/charcoal text. If a background is too bright for white, pick a different shot or
  move the text onto skin, fabric or a darker area. Don't switch the text colour.
- **One consistent type system in every scene** (Figtree), never a one-off size:
  - headline: 38px, weight 300, uppercase, letter-spacing 0.18em (e.g. "BLACK FRIDAY", "30% OFF SITEWIDE", "WATERPROOF")
  - sub-line (optional, under the headline): 17px, weight 400, uppercase, letter-spacing 0.32em
  - closing scene: wordmark, then the same headline + sub-line sizes
- One headline per scene. Lockups fade in (0.9s) with a 16px ease-out rise. Never put text on the jewellery.
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
