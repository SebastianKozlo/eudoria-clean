# FINDING N-7 — THE R-CHANNEL OF THE GLOBAL HEIGHT TEXTURE (429259)

**RUN**: the georef open bound #3 (the R-channel role). Offline, read-only.

## THE MEASUREMENT

The 257x257 24bpp TGA (429259): (B,G) = the 16-bit fixed-point height (RUN-3 verified);
R = the third channel. Analysis over all 66,049 texels:

1. R is NOT a biome/palette class mask: no discrete class structure; the top value
   R=93 covers 22,929 texels (34.7%) but the rest is a continuum (179 unique).
2. **The inverted-height relation: R + B ~= 254 +/- 3** (the histogram mode at
   254/255; 42.3k texels within the top-8 bins) — i.e. **R ~= 255 - B = the INVERTED
   HIGH BYTE OF THE HEIGHT**. The linear fit over R!=93: R = 188.955 - 0.4244*h with
   only 1.8% exact matches — the relation is BYTE-level (R ~= 255 - B), not a clean
   linear function of the 16-bit height (the G low bits break it).
3. Pearson(R, height) = -0.711 — the strong negative correlation = the direct
   consequence of the inversion.
4. **The Q3 anomaly (UNVERIFIED)**: one 129x129 corner (16,641 texels) carries
   R = 93 CONSTANT while its heights span 147.2..171.0 (all land) — decoupled from
   the inversion there. Recorded as-is; the semantics (a fill region? an edit-era
   artifact? a watermark?) = UNVERIFIED.

## THE VERDICT

**CONFIRMED**: R ~= 255 - B for ~75% of the texels — the red channel = an
INVERTED-HEIGHT auxiliary channel, not an independent field. **NOT the biome mask**
(iter028's 129x129 "water/biome mask candidates" hypothesis: WEAKENED for this
texture — the 2x2-constant-block test = 38.3% only, and the height correlation
dominates). The Q3 corner = an honest open micro-bound.

MILESTONE IMPACT: the 429259 texture is now a three-channel artifact with ONE
semantic height field (16-bit, (B,G)) + its inverted byte copy (R) + one
unexplained constant corner. The palette-selection [P-CLIMATE] search space
narrows: the palette selector is NOT in this texture's channels.
