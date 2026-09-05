# ITER036 — The Float-Constant Lock Sweep (M1 ITER_050)

Ledger: ITER_036 · Session: 2026-09-05 (per the ITER_050 prompt, SHA 109DB0AA...) ·
Binary: Entropia.exe 9.3.5.6746 sandbox (SHA E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31, verified before import; FRESH Ghidra project `ITER050_CONSTLOCK`, never TMF1_12H).

## P0

Is EVERY float constant cited by the milestone (material/water/foliage chains) operand-width-locked
from the binary bytes — and do the affected pages re-validate after any corrections?

## The census (the deliverable)

`03_EVIDENCE/iter036g_census.json` — every cited constant with VA + file offset + the full 8 bytes +
the instruction opcode width (m64 vs m32, re-derived from the FRESH project listing; 71/71 cross-check
vs the frozen iter035 pattern findings, 0 mismatches) + the exact FLOAT64-or-FLOAT32 value (exact
rationals) + the first-citation + the verdict:

- **79 exe VAs** (71 pattern-findings + 2 iter028 extras + 6 discovered at the claim sites),
  0 byte-lock failures;
- **57 .fx text-constant tokens** (materials.vfs records 0x3ea Terrain_14 + 0x3eb Water — both eras
  byte-identical, SHAs 2624c019…/857dea6e… verified against the raw containers, every token
  byte-located at its record offset);
- **5 immediate/integer entries** (PUSH 0x38A8 @0x0044d3de; the integer (t-128)×5 = SUB 0x80 +
  LEA ×5 in FUN_0094aac0 — no float constant at all; the wind FLDZ/FLD1 clamps; the ps.1.4 CND 0.5).

Classes: 22 plain f64 QWORDs; 8 f32-literal-widened-to-f64 (the danger class); 3 exact-literal
widened (0.5/1.5/0.25 — no pitfall); 27 genuine DWORD f32 slots; 10 .data globals (NOT floats);
9 virtual-only runtime slots (beyond the file image).

## The 7 dangers (resolved)

`03_EVIDENCE/iter036_dangers.json` — the f32-literal-widened-to-f64 class from
iter035_pattern_findings.json, each byte-locked:

- **4 CORRECTED at code**: 0x00A7B360/0x00A81D18/0x00A7B308/0x00A7B2D0 (float32(0.01/0.005/0.4/0.2)
  widened) — the `materials_confirmed.js` noise tables used the JS decimal literals (which differ from
  the binary slots in the 8th+ significant digit). FIXED this iteration.
- **3 OK**: 0x00A7B268/0x00A7B3E8 (0.7/0.3 — the uncited n2D inner blend of the noise modulation,
  byte-locked now @FUN_00939c40 0x0093a464/0x0093a474) + 0x00A7AF78 (0.8 — the iter030 zone claim
  read the f64 value correctly; FUN_00942cf0 FLD qword @0x00942eb0 confirmed).
- The 8th class member (float32(1/12800) @0x00A980D0) was locked in ITER_049 — carried.

## The corrected chain (the fix)

`terrain/materials_confirmed.js` — the manager noise tables (FUN_0093cbf0 @0x0093CDC0..0x0093CE5C):

- the constants = the BINARY f64 slots (byte-derived; `NOISE_OPERAND_LOCK` exported in the page
  result for the anti-circular reference);
- **the RNG draw rewritten**: FUN_00405920's exact construction
  `(state & 0xFFFFFFFFFFFF) / 2^48` (the OR 0x3ff0000 exponent stitch + <<4 + FSUB 1.0 — EXACT by
  Sterbenz) supersedes the documented `(state >> 11)/2^53` [P4] variant;
- the 9 f32 rounding points (the draw/product/accumulator FSTP dwords + the final division stores)
  replicated with `Math.fround`;
- `[P4]` reduced to the SEED only (the engine seed is per-session runtime state).

## The anti-circular revalidation — PASS

`00_CONTROL/m1_iter036_noise_reference.py` (constants byte-derived from the census at load;
the chain implemented independently; exact rationals):

- the page tables vs the reference: **2048/2048 BIT-EXACT** (u32 bit patterns, 0 mismatches);
- the demonstrative negative: the OLD chain FAILS 2048/2048 — the correction is material in
  EVERY entry;
- the division double-rounding question settled: f32(exact) == f32(f64-rounded) over all 2048
  actual quotients + a 100,000-value randomized sweep: **0 mismatches** (the JS
  f64-division+Math.fround is bit-identical to the engine's 80-bit FDIV + FSTP-dword here).

## The render revalidation

- fresh deterministic render `EA4411B57A33FA22936D20C002EB8D137EB39C775B5A52AB411E6521DDB2E3E7`
  (3/3 fresh loads identical + in-page double-render deterministic; the load JSONs and PNGs are
  byte-identical);
- the old `3C785581…` (iter030/034) SUPERSEDED — the delta ROOT-CAUSED: the draw-construction
  correction changes every noise-table entry → the palette row/col indices differ at affected
  cells; the behavioral stats reproduce EXACTLY (naive white 43.36%, confirmed white 0.0% —
  the one-hot signature unchanged);
- regression sweep: heights `50BD7F9E…`, materials `5F4677E6…`, water `D7C13F1F…`,
  foliage `8770AAA0…` — **4/4 MATCH** their recorded hashes (zero regression elsewhere).

## The cross-chain closure verdict

**THE ERROR CLASS IS CLOSED MILESTONE-WIDE.** Every float constant cited by the milestone
evidence is byte-locked + width-locked + value-locked + verdict-attached. The single remaining
era-bounded item = the noise-table SEED ([P4]; unknowable static). The .data runtime globals are
classified NOT-FLOAT (pointer/storage slots). The key confirmations: 73.0 = f32 @0x00A97C90 +
53.0 = f64 @0x00A97C98 (the iter027 width-label error confirmed value-correct); the row formula
constants (255/2/512/63/10/0.25 + the -20/+512 clamps); the water 10.0f @0x00A7B128; the wind
chain instruction-exact (0.5f32+2.0f32, the 1.5 derived); the x100 f32 @0x00A7AF68; the
integer (t-128)×5; the zone falloff 8.0/1-256/1-128; the .fx constants era-stable.

The RECONSTRUCTION-ONLY labels are unchanged (the operand lock does NOT promote them):
[P1]/[P2]/[P3a]/[P3b]/[P5] (materials), [P-CLIMATE]/[P-CELLSTREAM]/[P-WINDOW] (foliage),
[P-WAVES]/[P-SKY]/[P-DATUM] (water), [P4]=the seed (noise tables).
