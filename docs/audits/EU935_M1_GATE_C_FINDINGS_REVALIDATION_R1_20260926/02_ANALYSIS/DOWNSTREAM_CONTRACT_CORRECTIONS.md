# DOWNSTREAM CONTRACT CORRECTIONS — the SUCCESSOR contract content (F03/F05)

RUN_ID: EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926 (02_ANALYSIS)

The historical `EU935_M1_FULL_MILESTONE_AUDIT_R1_20260916/02_ANALYSIS/
M1_DOWNSTREAM_OUTPUT_CONTRACT.md` is READ-ONLY history and is NOT mutated. This
file is the SUCCESSOR contract content for the sections its carried text got
wrong. Later milestones consume THIS correction layered over the historical
contract; where the two differ, this file governs, with the correction edges
(FINDINGS.csv F03/F05) as the authority chain. Sections not listed here stand
as written in the historical contract.

## §1 CORRECTION (origin formula — the typed K constant)

HISTORICAL (defective): "Consumer formula: out = f32(f32(W * 0.01) - S) with S a
MUTABLE runtime singleton..."

CORRECTED SUCCESSOR TEXT:

- Consumer formula: `out[i] = f32(f32(W[i] * (double)(float)0.01) - S[i])` with
  S a MUTABLE runtime singleton. The K constant is **f32(0.01) WIDENED to f64**
  (hex 0x3c23d70a = 0.009999999776482582...), NOT an unconstrained binary64
  0.01 literal (0x3F847AE147AE147B). The two readings give DIFFERENT f32
  results (precision control W=5, S=0, node v22.22.0):
  f32(5 * f32(0.01)) = 0.04999999701976776 (0x3d4ccccc) vs
  f32(5 * 0.01) = 0.05000000074505806 (0x3d4ccccd).
  Later milestones MUST NOT assume S==0 and MUST NOT assume an unconditional
  W*0.01 and MUST NOT read K as binary64 0.01 (RETRACTION_SUPERSESSION_LEDGER
  rows 2-3 + this successor correction).

## §5 CORRECTION (height representation — the A/B separation)

HISTORICAL (defective): "The two models are reconciled as DECODE-MODEL
VARIANTS - consumers MUST state which model they consume."

CORRECTED SUCCESSOR TEXT:

- TWO SEPARATE HEIGHT REPRESENTATIONS, not interchangeable "variants":
  - A. GLOBAL RGB HEIGHT FIELD MODEL: resource 429259.dat (LOCAL both 9.x eras;
    257x257, 24bpp); frame = the global field (origin -65,536; 512-unit texels;
    span 131,072; the +50.0 slot datum byte-locked); units = the (t-128)x5 m
    model (STRONGLY_SUPPORTED at data level; land 79.606% reproduced); the
    engine consumption chain partially RE'd (ArkHeightTree leaf recursion;
    quadtree construction NOT RE'd).
  - B. TDF u16 HEIGHT REPRESENTATION: resource = the TDF payload height blocks
    (32x32 uint16 LE at payload offset 64, per tile, the 220x236 filename-xy
    grid); units = u16 x 1/128 m = CURRENT_RUNTIME_CALIBRATION (heightScale 128
    u16/m = STRONGLY_SUPPORTED calibration, not an engine-extracted constant;
    the PE2003 decode identity+operation CONFIRMED at VA; the per-tile min/max
    source open #1; the full-lerp form in 9.3.5 open #9).
  - BRIDGE_STATUS = UNKNOWN: no bounded evidence proves the conversion between
    A and B; the field-vs-TILE datum mapping remains UNPINNED ([P3b]/open #5).
    Consumers MUST state which representation they consume and MUST NOT treat
    A and B as interchangeable; both evidence lines are PRESERVED.

## §6 CORRECTION (terrain texture inputs — the re-scoped table)

HISTORICAL (defective): "ID-resolution 99.8613% (24,474/24,508, era 9.3.5;
dangling 34 classified). Name-anchor 80.40% measured (OBSERVED class;
[79.90,80.90])." — presented under TERRAIN TEXTURE INPUTS.

CORRECTED SUCCESSOR TEXT:

- TERRAIN TEXTURE INPUTS / LIMITS (the actual terrain input chain):
  - Terrain container data: terrain.bnt TDF payloads — BYTE-EXACT from original
    bytes (58,451 entries; 51,920 regular tiles).
  - TDF material info: the tail records (175 material ids; masks RAW+RLE) —
    BYTE-EXACT; the masks feed the LOD mesh VERTEX-COLOR bake + zone shadow
    paint (838/838 consumer census), NOT the base/factor/detail texel source.
  - Terrain material palette: the 96/96 climate system textures EXIST in PCG
    Textures.bnt (iter027); materials_confirmed uses palette 421318
    (64x256x32bpp; LOCAL; provenance-carried).
  - Detail texture IDs: the engine byte-0 table entries C[0]=D[0]=458791,
    E[0]=458792 (real era entries) — RECONSTRUCTION-ONLY defaults while the
    selector grids are missing.
  - Blend inputs: the factor texture one-hot band selection + the
    binary-locked noise operands (iter036) + the FIXED reconstruction seed
    0x30303030 ([P4] — not the historical per-session seed).
  - 432502 (65x65 climate) / 459344 (129x129 detail selectors): MISSING
    locally (patcher-delivered; era-bounded placeholders [P1]/[P2]; the absence
    claim scoped NOT_DETECTED_UNDER_THESE_PREDICATES for non-raw encodings per
    the F04 correction).
  - WAVES/SKY plane textures: missing locally ([P-WAVES]/[P-SKY] synthetic
    stand-ins, labeled).
  - HISTORICAL TERRAIN TEXTURE LAYOUT: NOT RECOVERED.
- NIF/MODEL TEXTURE CROSS-REFERENCE (NOT a terrain input; recorded separately
  so the valid measurements survive with correct scope): 24,474/24,508 =
  99.8613% ArkTexture-id resolution over the K1 binding chain (5,596 NIF models;
  eabf6cf) and 19,705/24,508 = 80.40% own-file name-anchoring (OBSERVED class;
  CI [79.90,80.90]; c380a26) — NIF mesh->texture resource-binding domain.
  These figures MUST NOT be used as terrain-texture coverage in any later
  milestone.

## §8 ADDITION (exactness condition — pointer to the code-level correction)

The engine-parity arithmetic condition is restated here so the contract text and
the code comments cannot diverge: the foliage arithmetic claims are CONDITIONAL
on the x87 model (PC in {53,64}, RC = nearest-even); the actual original-client
foliage-site CW is UNMEASURED; original-client runtime parity UNVERIFIED;
historical foliage inputs NOT RECOVERED; foliage placement 1:1 NOT claimed
(see 02_ANALYSIS/F05_EXACTNESS_ORIGIN_PRECISION.md; the corrected
PEFoliageCore.js comments).

## §9 ADDITION (VCL decoder coverage — the corrected input contract)

The canonical .vcl decoder covers 31 of 32 files (472 records) over the original
corpus; 25.vcl = UNSUPPORTED_BY_CURRENT_DECODER (six comma tokens at group 9;
first "0,2" @payload byte 447; fail-closed whole-file throw). The raw corpus =
493 whitespace groups of 12 (492 fully numeric + 1 comma group). The
original-client locale/comma/failure semantics for 25.vcl = UNVERIFIED. Later
milestones MUST NOT (a) assume getVegetationClimate succeeds for all 32
indices, (b) normalize commas to dots without original-client evidence,
(c) cite "492 engine records" as a decoder-reproduced fact. (F02 correction
chain; the row-7 CONTRADICTION_FINDING.)
