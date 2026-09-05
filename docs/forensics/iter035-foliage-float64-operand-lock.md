# ITER 35 — The Foliage FLOAT64 Operand Lock + RNG/Spawn Revalidation (Gate C correction)

- **Iteration:** M1 ITER_049 (session ledger ITER_035) — 2026-09-04, pe-reconstruction.
- **Trigger:** the human independent audit REJECTED the M1 gate PASS (architect decisions ledger ENTRY #10): the foliage RNG/spawn constants had been read as FLOAT32 when the binary uses FLOAT64 QWORD operands. This is the mandated P0 correction.
- **Era:** PCG_9_3_5. Static Ghidra RE (FRESH project `ITER049_FLOAT64`, sandbox copy SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31` verified before import — never TMF1_12H, never the ITER046_GATEC project) + exact-rational proofs + the corrected runtime.

## The three constants — BYTE-LOCKED (the old reads were the LOW DWORDS of QWORD doubles)

| Symbol | VA | file offset | bytes (LE) | value (f64) | operand | the old WRONG read |
|---|---|---|---|---|---|---|
| `_DAT_00a7d7a8` | 0x00A7D7A8 | 0x67D7A8 | `00 00 00 00 C0 FF DF 40` | **32767.0** | FDIV QWORD @0x0098CE5A | low dword 0.0f -> assumed 32768.0 `[P-RNG-DIV]` |
| `_DAT_00a8c758` | 0x00A8C758 | 0x68C758 | `00 00 00 00 E0 FF EF 40` | **65535.0** | FLD QWORD @0x0095B2BC/0x0095B3DB | low dword 0.0f -> assumed 2.0 `[P-POS-SCALE]` |
| `_DAT_00a980d0` | 0x00A980D0 | 0x6980D0 | `00 00 00 40 E1 7A 14 3F` | **0.00007812499825377017** | FMUL QWORD @0x0095B347 | low dword 0x40000000 = 2.0f -> "MEASURED 2.0f" |

The scale multiplier derivation: `C = float32(1/12800) widened to float64` — mantissa `0x47AE140000000 = 2348810 * 2^29`; the binary stores the f32-rounded decimal `0.000078125` (= 1/12800 = 2^-7/100) in a QWORD slot. Role: `nodeScale = |lerp| / 12800` — a per-model size value -> the NiNode local scale through /12800 (= /100 × /128); the ABSOLUTE world-size meaning depends on the impl scale-field values (the `[P-SCALE-FIELDS]` bound: the fields are f32 per the census, their value source not byte-pinned).

## The operand census + the six f32 rounding points

Full census (17 chain functions, 51 FPU/SSE instructions, every operand width locked — `iter035_operand_table.json`):
the chain computes in 80-bit x87 and rounds to f32 ONLY at the FSTP DWORD stores:
- **P1** @0x0098CE60 `rand01 = f32(r / 32767.0)` — FUN_0098ce30 writes the result to FLOAT32 before returning (the human's byte-proven claim, instruction-confirmed);
- **P2** @0x0095ACF0 `value = f32(rand01*(max-min)+min)` — the sampler's lerp result (min/max = f32 fields at impl+0x44/impl+0x40, FLD DWORD);
- **P3/P4** @0x0095B318/0x0095B322 `nodeX/Y = f32(u16 / 65535.0)` — the NiNode local translate: a [0,1] NODE-LOCAL fraction (65535.0 = the u16 max), NOT a world scale;
- **P5/P6** @0x0095B353/0x0095B365 `nodeScale = f32(|value * C|)` (the FABS commutes with the f32 rounding).

Notes: the `FADD dword [2^32f]` @0x0098CE54 is the compiler's generic unsigned-conversion idiom — DEAD CODE on this path (r = AND 0x7FFF is always >= 0, the JGE always skips it); the position divisor survives in st(1) across the per-record A/B divisions (FDIV ST0,ST1 / FDIVRP), re-loaded per iteration (0x0095B3DB); the census found the query/grid paths INTEGER-ONLY; FUN_00990810's FPU usage is exact 4-byte moves; the VCL parser's 12-value copy is a raw REP MOVSD (per-column types remain unverified).

## The exactness proofs (exhaustive, exact-rational)

The JS replication (`f64 arithmetic + Math.fround at the binary's points`) vs the binary (`80-bit x87 + FSTP DWORD`) — double-rounding compared over the COMPLETE input domains (fractions.Fraction, no float shortcuts):
- rand01: 32768/32768 values of r — **0 mismatches**;
- node positions: 65536/65536 u16 values — **0 mismatches**;
- the lerp: 1,245,184 (min,max)×r combinations (the VCL climate-0 col2/col3 pairs + synthetic) — **0 mismatches**;
- the scale: 1,245,184 combinations — **0 mismatches**.

The JS formula is therefore BIT-EXACT vs the binary everywhere on these domains — no extended-precision emulation needed.

## The anti-circular revalidation (the discipline change)

`m1_iter035_rng_reference.py` SUPERSEDES the iter033 reference (which shared the JS assumptions — agreement-at-assumptions, not engine parity). The rebuilt reference:
1. derives its CONSTANTS from the binary extraction (`iter035_operand_table.json` — the Ghidra census artifact; validated from the bytes at load, nothing hand-typed, nothing read from the JS);
2. decodes the ORIGINAL `VegetationClimates.bnt` (SHA `7B858401...`) by its own BNT2 + flat-12-token-stream parse (FUN_0083a7d0 semantics) — the records are NOT taken from the page;
3. recomputes all 76 instances from the original records + the seed inputs with its own implementation of the census chain;
4. carries the human's vector as a built-in test.

Result: **76/76 BIT-EXACT** (every f32 field via bit comparison — samplerValue, scale, node01x/y — plus every u32 state and position); records cross-check PASS; the vector 9719 PASS (`/32767 = 0.2966093935972167` exact, f32 `0.29660940170288086`, vs the rejected `/32768 = 0.296600341796875`). Instance 0 of the deployed page IS the human's vector case (record col2/col3 = 0.5/1.5 -> value = 0.5 + rand01) — verified bit-exact. The demonstrative negative: the OLD shared-assumption reference now FAILS 76/76 against the corrected page (`iter035_old_reference_negative.json`) — the correction is material in every case, exactly as the human computed.

## The fix (this repo)

- `src/peworld/PEFoliageCore.js`: the three constants locked (f64) + `Math.fround` at the binary's six points + `FOLIAGE_OPERAND_LOCK` (the census record) + the placeholders re-labeled (`[P-RNG-DIV]`/`[P-POS-SCALE]` REMOVED — now LOCKED; `[P-CLIMATE]`/`[P-CELLSTREAM]`/`[P-WINDOW]` explicitly RECONSTRUCTION-ONLY; `[P-SCALE-FIELDS]` re-derived). The generator now emits the BINARY node fields (`node01` = the f32 [0,1] node-local positions; `scale` = the f32 node scale; `samplerValue` = the f32 lerp) + the caller-supplied `windowWorld` calibration for the world mapping.
- `terrain/foliage_system.js`: the world mapping made explicit (`[P-WINDOW]` page calibration, u16 = world × 2 — placements UNCHANGED vs the old render); the node-scale render bridge documented (`2.0 / NODE_SCALE_MUL` — a CURRENT_RUNTIME_CALIBRATION preserving the deployed effective sizes while the census carries the BIT-EXACT binary node scale; the visualizer's world-scale transform is not decompiled).

## The render + census re-run

- fresh deterministic render: **`8770AAA09AF79B358B912691AD0F28452D1CA14CE3B6D88BE8808245529F1668`** (3/3 fresh loads identical; in-page double-render deterministic);
- the superseded old hash recorded: `A79CB65C1852E8893E1346905D2F29BCBAC0C076D3EA6491AC1E2A7BDD92929F` (iter033/034);
- the `?foliage-off` variant: `A3339D4A6DF945BCFBA2CA52FE1DD5B9FADF444E4877F3AAF24C8E6D95E6F7BC` — IDENTICAL to the old off hash: the terrain path contributed ZERO delta; the default-render delta comes only from the instance chain (root-caused: the /32767 rand01 shift + the f32 roundings + the C multiplier with the size-preserving bridge);
- census re-run: 76 instances / 4 sub-cells / 4 distinct models / 28 zero-counts — every instance now carries the binary node fields.

## The pattern re-check (report-only; other chains = follow-ups)

71 evidence-cited `_DAT_*` constants re-examined (every referencing instruction width-locked): the engine's float constants are predominantly QWORD f64s (27 found, many with low-dword = 0.0f); the DANGEROUS sub-class = f32 literals widened to f64 whose low dword reads as a plausible value: 0.01 / 0.3 / 0.005 / 0.2 / 0.4 / 0.7 / 0.8 at 0x00A7B360 / 0x00A7B3E8 / 0x00A81D18 / 0x00A7B2D0 / 0x00A7B308 / 0x00A7B268 / 0x00A7AF78 (plus the fixed foliage 1/12800) — the exact misread class the human caught. Also recorded: the iter027 `thresholds_doubles` width-label error (0x00A97C90 = 73.0 is f32; the value was correct). Per the iteration mandate: ONLY the foliage chain is fixed here; the other chains are follow-ups.

## Matrix rows 10/11 re-judged

- **FOLIAGE_DISTRIBUTION:** PARTIAL -> CORRECTED-TO-CONFIRMED (mechanism) — the mechanism stands; the arithmetic is now byte-locked and revalidated; the cell content remains the labeled RECONSTRUCTION-ONLY stand-in.
- **FOLIAGE_SEED/RNG:** CONFIRMED on the NEW basis — the integer LCG identity + the byte-locked f64 operands + the f32 rounding + the anti-circular bit-exact revalidation; the `fully procedural, zero server RNG` overclaim stays demoted to "the local spawn-loop chain is decoded; the cell-content origin remains open".

Artifacts: `iter035_operand_table.json`, `iter035_rng_crosscheck.json`, `iter035_foliage_render_hashes.json`, `iter035_foliage_census.json`, `iter035_pattern_findings.json`, `iter035_old_reference_negative.json`, `iter035_matrix_row_corrections.json` (the audit tree 03_EVIDENCE) + `m1_iter035_rng_reference.py` (00_CONTROL).
