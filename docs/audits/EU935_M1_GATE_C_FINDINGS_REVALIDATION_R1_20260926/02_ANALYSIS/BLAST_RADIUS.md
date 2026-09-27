# BLAST RADIUS — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926

RUN_ID: EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926 (02_ANALYSIS)

## 1. WHAT THE SIX FINDINGS DID AND DID NOT TOUCH

CONFIRMED-INVALIDATED (corrections applied or successor edges recorded):

| Carried item | Location (historical; NOT modified) | Defect | Successor correction |
|---|---|---|---|
| "ZERO PRIMARY_DEVICE" premise | M1-CL-20; X87_RUNTIME_AUDIT item 3; CLOSURE_GATE_MATRIX Gate-A evidence; PE_MASTER_M1_FULL_AUDIT §14/§16/§11; OPEN_LIMITS OL-05; UNRESOLVED C7; AUDIT_ENTRYPOINT IMMEDIATE BLOCKER; night-aggregate N-3/N-13 | mask decode error (&2 = MULTI_DRIVER; true 1/6 primary) | RETRACTION_NEW-F01; x87 cause class ENVIRONMENT_BLOCKED -> UNKNOWN; C7 = STATUS_REVALIDATION; Gate-A old PASS not inherited |
| "492 engine records" census chain | VegetationClimateDecoder.js comments (EDITED); V4 row 7; M1-CL-07; FOLIAGE_AUDIT; PE_MASTER_M1_FULL_AUDIT §18 | the comma group (25.vcl group 9) silently dropped by the TSV-line census; matches neither 493 (raw) nor 472 (decoder) | RETRACTION_NEW-F02; V4 row 7 = CONTRADICTION_FOUND; decoder coverage = 31/32 + 472 + 25.vcl UNSUPPORTED |
| "text is numeric throughout" | VegetationClimateDecoder.js comments (EDITED) | 6 comma tokens in 5,916 slots | corrected in-code (comment-only) |
| Unconditional BIT-EXACT wording | PEFoliageCore.js header + FOLIAGE_OPERAND_LOCK.exactness (EDITED) | missing the PC {53,64}+RC condition | corrected in-code (comment lines + ONE documentation-metadata string (FOLIAGE_OPERAND_LOCK.exactness) — no executable/behavior change; four-way separation) |
| Shortened origin formula "W * 0.01" | M1_DOWNSTREAM_OUTPUT_CONTRACT.md §1 L11 (historical) | typed-K ambiguity (distinct f32 results at W=5,S=0) | successor contract content restored to (double)(float)0.01 with the control |
| NIF figures in terrain positions | M1_DOWNSTREAM_OUTPUT_CONTRACT.md §6; TERRAIN_WORLD_SURFACE_AUDIT §TEXTURE RESOLUTION; coverage-matrix row 5 | 24,474/24,508 + 80.40% are NIF model-texture binding/name-anchor measurements | re-labeled NIF/MODEL TEXTURE CROSS-REFERENCE; terrain layout = NOT recovered |
| Height "DECODE-MODEL VARIANTS" language | M1_DOWNSTREAM_OUTPUT_CONTRACT.md §5 | field model vs TDF u16 presented as interchangeable | A/B separation; BRIDGE_STATUS = UNKNOWN |
| Merged "exhaustive negatives" summary | CELLSTREAM_CLIMATE_AUDIT.md disposition wording; Gate-A evidence text | two methods + predicate scope conflated | per-method enumeration claims; NOT_DETECTED_UNDER_THESE_PREDICATES for omitted classes (UNRESOLVED A3/A4/A18/B4/C4/C5) |
| "PASS (advisory)" as Gate-B | CLOSURE_GATE_MATRIX Gate-B row; M1 report §14 | canonical authority conflated with advisory opinion | SPLIT: GATE_B_SCIENTIFIC_PACKAGE_STATUS / GATE_B_CANONICAL_AUTHORITY_STATUS (F06) |
| terrain.bnt "fresh pin" history claim | M1 report §3 F4; SOURCE_INDEX provenance | the full hash was ALREADY in code at base (0187e18 Bnt2TerrainArchive.js line ~6) | RETRACTION_NEW-P3A: FULL_HASH_ALREADY_PRESENT_IN_CODE; the fresh rehash stands |
| "WITNESS MATRIX stay OPEN" vs "closed" | V4 row 8 LIMITATIONS vs UNRESOLVED B5/C1/C2 | scope ambiguity | RETRACTION_NEW-P3B: queue-scope closed vs global-coverage open — explicit, never flattened |
| OPEN_LIMITS "16" in stale summaries | external pasted summaries | true count = 17 | RETRACTION_NEW-P3D; the repo report already said 17 |

EXPLICITLY UNAFFECTED (verified; with the reason):

- The terrain height/grid/material/water claim families (F01-F06 touch none of
  their physical evidence).
- The foliage MECHANISM claims: loader registration FUN_0041dae0 + factory
  @0x00420007 + 45 RTTI classes (independent of corpus tokenization); the
  grid/cell-record/spawn-loop/RNG arithmetic (address-level RE; the demo and
  iter035 validations consume 0.vcl — a fully numeric file, byte-unchanged,
  decoding identically pre/post edit).
- The BYTE-LOCKED operands + the six FSTP rounding points (re-verified from the
  EXE this run) and the iter035 proofs UNDER THE STATED MODEL.
- The PC24 sensitivity counts (14,104/229,376 real; 103,073/1,245,184 synthetic)
  and the 463,141 platform cross-validation.
- The measured negative counts themselves (0/27; 0/8,381; 26/179,774/70;
  178-container known-ID search; 429259 local x4; the 12-byte stub byte-exact).
- The witness/falsification queue verdicts (RUN-C/RUN-E), the georef run verdict
  (8b8b106), the r185 canonical decision, and all era-validation records.
- The retraction canon (all 9 prior retractions preserved verbatim; none
  re-litigated; nothing retracted is cited as standing by this package).

## 2. THE CLIMATE-0 DEMO / 76 INSTANCES / SPAWN-LOOP / RNG CONSTANTS — WHY F02 DOES NOT INVALIDATE THEM

No physical dependency exists between the F02 corpus-coverage defect and those
results:
1. The demo + the iter035 anti-circular validation consume 0.vcl (12 records,
   fully numeric — verified in the census: 144 tokens/0 bad tokens). Its bytes
   are unchanged; decodeVclPayload(0.vcl) returns the same 12 records pre and
   post the comment edit (31/1/472 total unchanged).
2. The mechanism claims (grid subdivision, cell-record layout, spawn arithmetic,
   RNG identity) are decompile-level facts about FUN_0098fe00/FUN_00990810/
   FUN_0095b180/FUN_0098cdf0/FUN_0098ce30 — they do not depend on how many
   records the corpus has or on 25.vcl's tokens.
3. The RNG constants were re-verified against the binary bytes this run (F05
   probe) — independent of VCL entirely.
4. The conditional arithmetic model was never conditioned on VCL coverage.

The NARROWING that DOES apply: corpus coverage statements ("all 32 decode",
"492 engine records") are corrected; consumers of getVegetationClimate for index
25 must expect the unsupported-file exception (V4 row 18 correction).

## 3. GATE EFFECTS

See 01_RAW/GATE_REVALIDATION.csv: Gate A = REVALIDATION_REQUIRED; Gate B
scientific = REVALIDATION_REQUIRED; Gate B canonical authority = BLOCKED; Gate C
= REQUIRES_INDEPENDENT_DESKTOP_REAUDIT; Gate D = HUMAN_PENDING. Nothing in this
package awards MILESTONE_POST_AUDIT_PASS, closes M1, or authorizes M2.
