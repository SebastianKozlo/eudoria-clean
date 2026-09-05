# GATES — THE CORRECTED M1 GATE DELIVERABLE MATRIX (layering note)

## What is here

- `M1_GATE_DELIVERABLE_MATRIX.md` — the 19-row final matrix + the fresh
  regression sweep + the era-bounded registry (19 placeholders) + the
  known-open list (27) + the SHA-verification summary. This is the
  milestone-gate deliverable written at ledger ITER_034 (session ITER_048,
  "M1 MILESTONE-GATE PREPARATION"), byte-exact copy (SHA256
  F0C7D0F29EEE32F156D4BBF9565724009188BBE8C1C9B0F4CA0BBEC4184D76E1 —
  matches the value recorded in the V1 audit).
- `M1_GATE_DELIVERABLE_MATRIX.json` — the machine-readable equivalent
  (VALID json; 19 rows, 19 registry entries, 27 open items; SHA256
  F373E60ABF87BF04CF7CC72A98423B19E861054D3B1F5F10CDD3C2041D478928).
- `AMENDMENT_ITER035_ROWS10_11.json` — the rows 10/11 RE-JUDGMENT after the
  FLOAT64 operand lock (byte-exact copy of iter035_matrix_row_corrections.json,
  SHA256 2B1FF548D1323BA46D1A8B533BF8BA943B5A508390637C632817D90B58254385).
- `AMENDMENT_ITER036_CLOSURE.json` — the cross-chain float-constant closure
  verdict (byte-exact copy of iter036_closure.json, SHA256
  CBBEEEB9DF345FA804FE79011AF23D0F685E2CE51582B472BB3709BB3D590AE1).

## The layering (the matrix "as amended by iter035/036")

The md/json matrix files are the ITER_034 deliverable AS WRITTEN (history is
never rewritten — contract "do not reorganize historical runs destructively").
The corrections that post-date it are carried by the amendment records above
and are summarized here so the reader can apply them while reading the matrix:

| Matrix row | As written (ITER_034) | As amended (the correction series) | Amendment record |
|---|---|---|---|
| 10 FOLIAGE_DISTRIBUTION | "CONFIRMED (mechanism) + [P-CELLSTREAM] stand-in" — but with the WRONG arithmetic knowledge ("scale = \|rand*2.0\| MEASURED"; "pos = u16/K", K=2.0 candidate) | REJECTED-as-written -> CORRECTED-TO-CONFIRMED (mechanism): the arithmetic is NOW BYTE-LOCKED (nodeX/Y = f32(u16/65535.0 f64) = [0,1] NODE-LOCAL fractions; nodeScale = f32(\|value * 0.00007812499825377017\|) = float32(1/12800) widened; Math.fround at the six binary FSTP-DWORD points); revalidated 76/76 BIT-EXACT vs the binary-derived reference; the CELL CONTENT stays RECONSTRUCTION-ONLY ([P-CELLSTREAM]/[P-CLIMATE]/[P-WINDOW]). [P-RNG-DIV]/[P-POS-SCALE] REMOVED — now LOCKED. | AMENDMENT_ITER035_ROWS10_11.json |
| 11 FOLIAGE_SEED/RNG | "CONFIRMED (position-keyed determinism, decompiled + cross-checked 76/76)" — but the cross-check was CIRCULAR (the reference shared the JS assumptions: 32768.0, 2.0, no f32 rounding) | CONFIRMED — ONLY ON THE NEW BASIS: the integer LCG identity stands; the FLOAT64 operands are BYTE-LOCKED (_DAT_00a7d7a8 = 32767.0 f64 FDIV QWORD; rand01 = f32(r/32767.0) inclusive [0,1]; the FSTP f32 rounding before return); revalidated 76/76 BIT-EXACT by the ANTI-CIRCULAR reference (constants FROM the binary bytes, records FROM the original VegetationClimates.bnt, its own implementation); the human's vector RNG 9719 (/32767 = 0.2966093935972167) PASSES. "FOLIAGE_FULLY_PROCEDURAL_ZERO_SERVER_RNG" STAYS DEMOTED. | AMENDMENT_ITER035_ROWS10_11.json |
| 6 TERRAIN_BLEND_SEMANTICS | CONFIRMED (era 9.3.5: shader op + factor content + filtering) — with the noise-table constants carried as inexact JS decimal literals and the RNG draw as the documented (state>>11)/2^53 [P4] variant | The verdict STANDS, strengthened: the noise-table constants are now the BINARY f64 slots (4 corrected-at-code: float32(0.01/0.005/0.4/0.2) widened slots at 0x00A7B360/0x00A81D18/0x00A7B308/0x00A7B2D0; NOISE_OPERAND_LOCK exported); the RNG DRAW is the engine's EXACT construction (FUN_00405920: draw = (state & 0xFFFFFFFFFFFF)/2^48, EXACT by Sterbenz — SUPERSEDING the documented variant); the 9 f32 rounding points replicated (FUN_0093cbf0 FSTP sites P1-P9); [P4] reduced to the SEED only; the revalidation 2048/2048 BIT-EXACT (the OLD chain FAILS 2048/2048 — the demonstrative negative). | AMENDMENT_ITER036_CLOSURE.json |
| 19 RUNTIME_INTEGRATION | 5/5 fresh sweep MATCH at the ITER_034 hashes (materials_confirmed 3C785581..., foliage A79CB65C...) | The sweep verdict STANDS methodologically; the CURRENT deterministic hashes after the correction series: materials_confirmed EA4411B5... (supersedes 3C785581...; delta root-caused = the draw-construction correction shifts every table entry), foliage 8770AAA0... (supersedes A79CB65C...; delta root-caused = the /32767 rand01 shift + the f32 roundings; the ?foliage-off control A3339D4A... UNCHANGED — the terrain path contributed zero delta); heights 50BD7F9E... / materials 5F4677E6... / water D7C13F1F... UNCHANGED; the witness page 381A80C4... (iter037) + the ?model-off negative control 2084DB5A... DIFFERS. | AMENDMENT_ITER036_CLOSURE.json + the ledger ITER_035/036/037 records |
| 8 FOLIAGE_MODEL_BINDING | CONFIRMED (mechanism) + GENERATED_CACHE assets (honestly labeled) | UNCHANGED as a verdict, but the ORIGINAL-DIRECT chain is now DEMONSTRATED for ONE model (the witness 457485: Models.bnt bytes -> NifModelReader.js -> NiTriShape -> NiArkTextureExtraData 457490 -> resolveTexture -> TGA2 A32 -> deterministic render; cross-validated vs the frozen R61 python parser 575 leaves / 0 mismatches). The foliage page still uses the GENERATED_CACHE GLBs; the switch is the recorded next step. NEW canon evidence: the era binds textures via the ARK system (0/10 candidates contain NiSourceTexture). | ledger ITER_037 + the repo commit c97ed73 |
| 18 PESOURCE_MOUNT | CONFIRMED | UNCHANGED, strengthened: getModelResource() LIVE (the era Models.bnt BNT2 container, SHA-pinned). | ledger ITER_037 + the repo commit c97ed73 |

All other rows are UNAMENDED by the correction series (see
AMENDMENT_ITER036_CLOSURE.json for the full cross-chain closure statement:
the FLOAT64/FLOAT32 error class is CLOSED milestone-wide; the single
remaining era-bounded item in that class = the noise-table SEED [P4]).

## Where the full correction records live

- The iteration ledger (local, Polish-side project tree):
  99_Audits\PE_MILESTONE_1_WORLD_SURFACE_R1\04_SESSIONs\M1_LEDGER.md —
  entries ITER_035, ITER_036, ITER_037 (the correction series), each with
  the full MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
  WHY_NON_CIRCULAR / FAILURE_CASE fields.
- The per-iteration evidence manifests (local): 03_EVIDENCE\
  iter035_* (8 files), iter036_* (21 files, SHAs in
  iter036_evidence_hashes.json), iter037_manifest.json (6 files).
- The repo English commit trail: b3fe74b (ITER_035), 47f6ab4 (ITER_036),
  c97ed73 (ITER_037) — each commit message carries the full result summary.
- The consolidated per-claim view (with the section-7 fields): see
  ../EVIDENCE_MANIFEST.json in this package.

---

## THE V3 CONSOLIDATION (appended 2026-09-05 by PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816)

The two matrix files above — `M1_GATE_DELIVERABLE_MATRIX.md` and
`M1_GATE_DELIVERABLE_MATRIX.json` — are the ITER_034 deliverable AS WRITTEN: FROZEN
HISTORY, never edited, never deleted. They are now **SUPERSEDED-BY-V3**:

- `M1_GATE_DELIVERABLE_MATRIX_V3.md` (NEW file in THIS directory) — a SHA-verified
  byte-identical copy of the LIVE V3 matrix (source:
  `D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\05_ANALYSIS\M1_GATE_DELIVERABLE_MATRIX_V3.md`,
  SHA256 B0B69F0634774CC4032A471D7F69BFF7312D427166DC24217C26B93B2DFF797F).
- `M1_GATE_DELIVERABLE_MATRIX_V3.json` (NEW file in THIS directory) — the machine-readable
  equivalent (SHA256
  0E46AB2C94EA1BA7B4527950A4D8851AB69DFA48B7DCDDD449F9A52BD39931F8; both copies re-hashed
  hash-identical at packaging time by the completion run's consistency check).

What the V3 changes relative to the frozen matrix (per the V3 files' own consolidation
statements + the repair run's report — quoted, not re-derived):

- the rows 10/11 re-judgment (iter035) is PHYSICALLY CONSOLIDATED into V3 (no longer
  sidecar-only: `AMENDMENT_ITER035_ROWS10_11.json` remains the historical record);
- the noise-table validator was REPAIRED and the tables re-proven 2048/2048 bit-exact
  with the byte-derived-constant method (the OLD validator's zip-gate and f32 subnormal
  sign defects were latent on the actual data — measured 0 recorded result changes);
- the original-direct single-model witness is integrated (iter037) and was re-checked
  16/16 blocks strict under the repaired gates (payloadSize 262188 == own BNT2 read ==
  oracle; payload SHAs equal);
- the REAL VCL domain is exhaustively re-proven: all 7 original 0.vcl pairs x all 32768 r
  values + 65536 u16, engine-vs-JS 0 mismatches, with the platform-validated oracle
  (463k+ cross-validation samples);
- the x87 model is now CONDITIONAL: PC=24 would differ on 14,104/229,376 real-domain lerp
  values (independently confirmed by PE-MASTER), rand01/positions PC24 = 0; the actual
  client control word is UNMEASURED (a NEW open item);
- [P-RNG-DIV] / [P-POS-SCALE] are SUPERSEDED-LOCKED (32767.0 / 65535.0 f64 byte-locked);
  the divisor-candidate lines are GONE from the live matrix;
- the explicit open list (7 items) replaces the old "NO open item blocks" phrasing.

Layering rule (unchanged in spirit, now explicit): read the frozen matrix + the amendment
records above for HISTORY; read the V3 copies for the LIVE verdicts; read
`../EVIDENCE_MANIFEST.json` for the per-claim evidence chain (source/generator/SHA/
denominator/independent truth/why_non_circular/failure case); read `../CORRECTION_NOTES.md`
for the hygiene corrections — including the citation-label defect in the frozen matrix's
EVIDENCE lines (rows 7/8/10/18 attach F299C622... to `iter033_manifest.json`'s name; that
SHA belongs to `assets/foliage_glb/MANIFEST.json` pinned INSIDE the manifest — see HYG-5).
