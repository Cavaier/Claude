# Cavaier video ad style rules

Set by Eli. Apply to every video ad unless he says otherwise. `cards4.js` already uses these values
(`LOGO_H`, `HEAD`, `SUB`).

## Text and logo
- **Logo:** the CAVAIER Bodoni wordmark (`logo_white.png`), used **once only, on the closing scene**.
  Size: **28px tall** on the 1080×1920 canvas, so its letters match the headline's capital height. It must never
  look bigger than the headline. Not on the other scenes.
- **White text only.** No dark/charcoal text. If a background is too bright for white, pick a different shot or
  move the text onto skin, fabric or a darker area. Don't switch the text colour.
- **One consistent type system in every scene** (Figtree), never a one-off size:
  - headline: 38px, weight 300, uppercase, letter-spacing 0.18em (e.g. "BLACK FRIDAY", "30% OFF SITEWIDE", "WATERPROOF")
  - sub-line (always, under the headline): 17px, weight 400, uppercase, letter-spacing 0.32em
  - closing scene: wordmark, then the same headline + sub-line sizes
- **Every scene is two lines: headline + sub-line.** Never a headline on its own.
  Example: BLACK FRIDAY / LIMITED TIME · 30% OFF SITEWIDE / EVERY PIECE, EVERY SET.
- One headline per scene. Lockups fade in (0.9s) with a 16px ease-out rise. Never put text on the jewellery.
- Key text stays between y=270 and y=1536 (Meta safe zone).
- On bright, high-key frames a very soft, wide shadow sits behind the lockup (`.veil` in `cards4.js`, max 15% black)
  so white text reads; it must look like natural falloff, never a visible patch.

## Look
- **Reference style:** Vacier's top video ads (Meta page 106321194484973): macro close-ups of jewellery on skin,
  slow, minimal, almost no text.
- **Brand tones:** Eli's reference photo is a macro of black chains on skin against soft white: neutral clean whites,
  peach-beige skin (not orange tan), deep blacks, soft light, crisp skin texture. Grade every clip towards that
  (see `specs/v5-grade.txt` for sunny footage, `build3.sh` for flat camera footage) and compare before/after frames.
- **Luxury slow motion:** use high frame rate footage and play every frame (120 fps played 4x slower, 29.97 fps output).
  Women's sessions by frame rate: 11 = 25 fps, 10 = 50 fps, 9 and 8 = 30 fps, 7 / 6 / 5 = 120 fps.
  Men Session 1 = 120 fps. Higher session number = newer.
  If the footage asked for is only 25-50 fps (Women Session 11 is 25 fps), use motion-compensated interpolation to
  2x (`build5.sh`: ffmpeg minterpolate mci/aobmc) and check in-between frames for smearing on fingers before using it.
- **Professional colour, every ad:** grade per shot with `grade.py`. It normalises the flat footage, then matches each
  shot's neutral areas (wall, boucle, white top; nails and skin excluded) to one white target, so cuts match in white
  balance and exposure, and then applies one look per ad: `gold` (cream whites, rich but not yellow gold), `black`
  (clean bright neutral), `edit` (slightly cooler, deeper contrast). Always review a before/after sheet of every shot.
- **Diversify concepts across a set of ads** (different footage, moods and claims per ad) while keeping these rules.

## Offer and claims
- Black Friday, 30% off sitewide, no code needed (taken off at checkout). No prices or currency symbols.
- Only true claims: waterproof, sweat and heat resistant, recycled 316L stainless steel, adjustable S/M/L,
  black / silver / gold, jewellery case included with sets, Trustpilot 4.5 with 3,000+ reviews.
