# RETRACTIONS — the consolidated retraction/supersession record of the M1 gate package

- PURPOSE (per `GATE_INDEX.md`): the human rejection (ENTRY #10), the V1 verdict
  supersession, the iter024 RTTI negative, the water-lead naming, the per-cell-renorm
  refinement, the RNG draw construction, the circular-reference demonstrative failures —
  consolidated. **Rule: nothing retracted is cited as standing evidence anywhere in this
  package; everything superseded says so here.**
- CREATED BY: PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816 (mechanical consolidation;
  every item below quotes an existing record — the cited file/entry is the authority).
- HISTORICAL RECORDS ARE NEVER REWRITTEN: each retraction below points at the frozen
  original + the superseding record.

## 1. The human rejection of the V1 gate verdict (decisions-ledger ENTRY #10)

- RETRACTED: the V1 milestone gate audit's **PASS** verdict (`REPORT_V1_SUPERSEDED.md` §5,
  "MILESTONE_1 = GATE PASSED") — REJECTED by the human independent audit on a
  **byte-proven FLOAT64 operand misread** (the three foliage constants read as their LOW
  DWORDs: "0.0 statically" / "32768.0" / "2.0f" instead of the QWORD f64 values
  32767.0 / 65535.0 / 0.00007812499825377017).
- Also demoted at the same entry: **"FOLIAGE_FULLY_PROCEDURAL_ZERO_SERVER_RNG"** — the
  honest form is "the local spawn-loop chain is decoded; the cell-content origin remains
  open" (the demotion STANDS through every later re-judgment; see `REPORT_V2_REJUDGMENT.md` §1).
- SUPERSEDED BY: the correction series (ledger ITER_035/036/037; amendment records
  `GATES\AMENDMENT_ITER035_ROWS10_11.json`, `GATES\AMENDMENT_ITER036_CLOSURE.json`) +
  `REPORT_V2_REJUDGMENT.md` (PARTIAL_PASS_CORRECTED, PROPOSED).
- The V1 audit file itself is RETAINED AS HISTORY (superseded, never deleted) — the
  diff between V1 and V2 IS the correction story.

## 2. The V1 audit's methodology retraction (the LESSON, per REPORT_V2 §1)

- RETRACTED: accepting the 76/76 validation without checking that the reference derived
  its constants independently (assumption-circular validation). The recorded LESSON:
  load-bearing arithmetic claims require independent operand-width + constant
  re-derivation at audit time.
- SUPERSEDED BY: the anti-circular method (ITER_035: the reference derives its constants
  FROM the binary extraction + the ORIGINAL VegetationClimates.bnt; the OLD shared-
  assumption reference now FAILS 76/76 — the demonstrative negative).

## 3. The self-correcting-loop retractions inside the milestone (V1 §1.5, all in the ledger)

- **iter024 RTTI negative** — RETRACTED (a file-offset-as-VA bug); corrected iter026
  (14 terrain classes resolved). The correction is in the ledger, never hidden.
- **iter025 "per-cell renormalization UNVERIFIED"** — REFINED (not a flat retraction)
  into the engine's actual ONE-HOT palette-alpha 3-band partition mechanism (iter027,
  worked-example gate 0.0% saturation vs the naive 84.0%); the RAW + CLAMP255
  renormalization candidates were FALSIFIED by measurement.
- **iter030 "type-6 = water-lead planes" naming** — REFUTED by the full census (iter031:
  type-6 is a per-tile 1/tile LOD-ring TEXTURE-CARRIER, present on 46,218 dry tiles too);
  the water-plane-candidate hypothesis is REJECTED-as-primary.
- **iter038-era "TDF masks feed the details"** — SUPERSEDED by the 129x129
  detail-selector tables (iter029): the TDF masks feed the LOD VERTEX-COLOR BAKE + ZONE
  SHADOW PAINT, NOT the base/factor/detail texel source (the exhaustive 838/838 census).
- **iter028 "server/patcher runtime channel"** — REFINED to a LOCAL-ONLY fetch with
  PATCHER-delivered bytes at install/update time (iter029; the client fetch is
  LOCAL-ONLY and a miss HALTS init).
- **"Geowater:0" auction-UI write** — DISPOSITIONED as a FALSE POSITIVE (iter031; the
  +0x184 wind-slot write was misattributed; the real wind chain is
  FUN_009512a0 <- FUN_009516f0 per-frame).

## 4. The RNG draw construction supersession (iter036)

- RETRACTED: the documented `(state >> 11) / 2^53` draw variant (a documented
  reconstruction choice, `[P4]`).
- SUPERSEDED BY: the engine's EXACT construction `(state & 0xFFFFFFFFFFFF) / 2^48`
  (FUN_00405920 decompiled; EXACT by Sterbenz) — `[P4]` is thereby REDUCED TO THE SEED
  ONLY (the FIXED reconstruction seed 0x30303030; the per-session engine seed is runtime
  state, UNKNOWABLE statically). Recorded in `GATES\AMENDMENT_ITER036_CLOSURE.json`.

## 5. The circular-reference demonstrative failures (kept as NEGATIVE evidence — never cited as positives)

- The OLD shared-assumption RNG reference (m1_iter033_rng_reference.py, SHA 43E31935...):
  SUPERSEDED by m1_iter035_rng_reference.py (SHA 8EDB17C9...); the old one now FAILS
  76/76 against the corrected page (the demonstrative negative PROVING the old
  validation was assumption-circular). The old file is retained for the record.
- The OLD noise-table chain: FAILS 2048/2048 against the byte-derived-constant rebuild
  (the demonstrative negative; the old validator's defects were measured LATENT on the
  actual data — 0 recorded result changes — so the old CONCLUSIONS were accidentally
  correct and are now re-proven independently).

## 6. The rendered-hash supersessions (iter035/036; deterministic renders)

- materials_confirmed: **EA4411B5...** SUPERSEDES **3C785581...** (delta root-caused =
  the draw-construction correction shifts every table entry).
- foliage: **8770AAA0...** SUPERSEDES **A79CB65C...** (delta root-caused = the /32767
  rand01 shift + the f32 roundings; the `?foliage-off` control **A3339D4A... UNCHANGED**
  — the terrain path contributed ZERO delta).
- heights 50BD7F9E... / materials 5F4677E6... / water D7C13F1F... UNCHANGED.
- Source: `GATES\AMENDMENTS.md` (the layering table) + ledger ITER_035/036. The V3 row 19
  carries the re-verified 76/2048/16 offline bit-exact re-checks of the recorded results.

## 7. The validator-infrastructure supersessions (the repair run, 19/19 allegations ACCEPTED)

From the repair run's `SUPERSESSION.csv` + `VALIDATOR_MUTATION_MATRIX.csv`
(99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\05_ANALYSIS\):

- **iter035f round_mantissa** (the proof oracle) — DEFECT_CONFIRMED_REPAIRED (carry bug:
  to_f32(1-2^-25)=0.25; + the run's OWN new finding: the subnormal sliding-scale defect);
  superseded by `repair_lib_ieee.py` (platform-cross-validated, 463k+ samples,
  0 mismatches). Old-bug frequency on every recorded domain measured 0 (latent, not
  material) — the old conclusions re-proven independently.
- **The domain read** (`cen.get("climate")` on a wrapped JSON) — DEFECT_CONFIRMED_REPAIRED
  (38 synthetic pairs had silently replaced the real domain); the REAL domain now
  exhaustively covered (7 original pairs; the synthetic set survives as a LABELED
  extended sensitivity domain).
- **The comparison counter 4,912,912** — RETRACTED (a reporting error; the four JSON
  counters sum to **2,588,672**; the repair run's own generated total is **3,047,424**
  on a fully-labeled domain mix).
- **m1_iter036 zip-gate** (empty/prefix tables PASS) — DEFECT_CONFIRMED_REPAIRED
  (gate_noise_new: exact length 1024 + finite + all-elements; 8/8 mutations FAIL).
- **f32_round_exact subnormal sign bug** (-2^-149 -> +2^-149) — DEFECT_CONFIRMED_REPAIRED
  (latent on the actual tables).
- **m1_iter037 entrySize fallback** (oracle-vs-oracle, always PASS) + **index-as-label** —
  DEFECT_CONFIRMED_REPAIRED (gate_witness_new: payloadSize REQUIRED; index compared AS A
  FIELD; 5/5 witness mutations FAIL).
- **m1_iter036c VA-0x400000 mapping** — DEFECT_CONFIRMED_REPAIRED (section-derived map;
  the 79 census VAs reclassified 60 file-backed / 19 virtual-only; the 10 foreign-.rsrc
  "bytes8_le" records SUPERSEDED as evidence hygiene; NO load-bearing claim changed).
- **"71/71" as completeness** — RETRACTED as worded; the claim coverage matrix now
  states every searched-set boundary explicitly (`CLAIM_COVERAGE_MATRIX.csv`).
- The old frozen scripts themselves are retained as evidence; they are NEVER run by
  later runs (read/reconstructed only).

## 8. The matrix supersession (V2 "as amended" -> V3 physical)

- RETRACTED: the "as amended by iter035/036" READING convention (the V2-audit-era pointer
  that was never physical).
- SUPERSEDED BY: the V3 matrix — a NEW physical file consolidating iter035/036/037 + the
  repair run (`GATES\M1_GATE_DELIVERABLE_MATRIX_V3.md/.json` in this package; the OLD
  matrix copies stay FROZEN and are marked SUPERSEDED-BY-V3 in `GATES\AMENDMENTS.md`).
- [P-RNG-DIV] / [P-POS-SCALE] SUPERSEDED-LOCKED (32767.0 / 65535.0 f64 byte-locked);
  the divisor-candidate lines are GONE from the live matrix (the old candidate wording
  is history).

## 9. Hygiene retractions of READINGS (this completion run; supplements ONLY — see CORRECTION_NOTES.md)

- **HYG-1**: `domain_reproof.json` `lerp_scale_synthetic.lerp_pc24_mismatches = 0` — the
  reading "measured 0" is RETRACTED; the field is a DEFAULT COUNTER (measure_pc24=False)
  = **NOT_MEASURED**. The actual value (auditor-side independent measurement, cited from
  `PE_MASTER_REVIEW.md`): **103,073/1,245,184** — strengthening, not weakening, the x87
  conditional model. The load-bearing real-domain number **14,104/229,376** (+ rand01/
  positions PC24 = 0) is CONFIRMED by the same independent post-audit.
- **HYG-3**: the summary counter "8 failed attempts" is REFINED to **8 log FILES / 10
  logged EVENTS** (4x r01 + 4x r02 including 2 timeout kills without log files + 2x r05);
  the register itself was honest.
- **HYG-5**: the citation "iter033_manifest.json (F299C622...)" in the frozen matrix rows
  7/8/10/18 (and carried verbatim into the V3 carried_evidence) is RETRACTED AS A LABEL:
  F299C622... is the SHA of `assets/foliage_glb/MANIFEST.json` pinned INSIDE
  iter033_manifest.json; the manifest's own SHA is DD598152.... Both files are carried
  with physically-verified SHAs in `EVIDENCE_MANIFEST.json`. No claim verdict affected.

## 10. Standing rule

If any future evidence contradicts a supersession above, the evidence wins and the
contradiction gets reported — this file corrects the READING of the records; it does not
alter any frozen file. Historical runs are not rewritten; supersessions/retractions are
recorded as new evidence (docs/audits/README.md convention).
