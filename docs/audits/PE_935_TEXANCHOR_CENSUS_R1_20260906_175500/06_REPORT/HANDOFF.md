# HANDOFF — PE_935_TEXANCHOR_CENSUS_R1_20260906_175500 (era PCG_9_3_5)

STANDING SENTENCE: correlation/association outputs are OBSERVED-level evidence; semantic
roles remain runtime-gated; no semantic claims.

## FINAL HANDOFF BLOCK

AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_935_TEXANCHOR_CENSUS_R1_20260906_175500
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_935_TEXANCHOR_CENSUS_R1_20260906_175500\06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = 01_RAW\ANCHOR_OUTCOMES.jsonl; 01_RAW\NC_TRIALS.jsonl; 01_RAW\FILE_UNIVERSES.jsonl; 01_RAW\CENSUS_REPRODUCTION.json; 01_RAW\NEGATIVE_FIXTURES_GEXEC.json; 01_RAW\SELF_AUDIT.json; 05_ANALYSIS\ANCHOR_RESULTS.json; 00_CONTROL\texanchor_census_r1.py; 00_CONTROL\FROZEN_METHOD.md; 00_CONTROL\PREREG_MARKER.txt; 00_CONTROL\PIN_RESULTS.json; STAGE_ACCEPTANCE_GATES.csv; artifact_index.csv
RUN_STATUS = COMPLETED (G-PINS/G-CENSUS/G-METHOD/G-EXEC/G-SCOPE all PASS; no HARD STOP fired; anchor fractions are MEASUREMENT outputs with no PASS/FAIL, per contract)
HARD_STOP_REASON = NONE

## Key numbers (OBSERVED; denominators explicit)

- Anchored (own-file mesh-part resolution AND slot-field==suffix):
  **19,705/24,508 = 80.4023%**, exact binomial 95% CI [79.8997%, 80.8977%].
- Components: own-file resolution 19,705/24,508 = 80.4023% (exact 1,103 / bridge 18,602 /
  none 4,803); slot consistency 24,508/24,508 = 100.0000% [99.9849%, 100.0000%].
- Cross-file NC (seed 20260906, 10,000 trials): anchored **67/10,000 = 0.6700%**
  CI [0.5196%, 0.8501%] -> anchored/NC ratio **120.0x**; NC other-file resolution identical
  (67); self-pairing 0; determinism re-proven.
- Per-slot: static slots 87.27–98.00%; ENVIRONMENT 0/1,694; ANIM0–31 0/1,157 (all 0.0000%).
- Supplementary OBSERVED: f1 enum agreement 24,336/24,508 = 99.2982% (the ITER-32 172 ANIM
  exceptions reproduced exactly); NiNode-universe variant resolves 21/24,508 = 0.0857%.

## Pins (verified in-driver BEFORE any parse; re-hashed after)

- K1 table SHA256 34f64fc8c4dc2ffe84dde52efa588a8cfa843197250b8efd57224729c7c1bbf9 (24,508
  rows reproduced row-for-row from the corpus: 0 mismatches; 24,474/34 split untouched).
- Models.bnt SHA256 c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0
  (5,596/5,596 parse closure; R61 frozen parser 10/10, READ-ONLY).
- Driver SHA256 be22fae22383b66ee9dc3ffda33b0fadad1fc9dec42342663333eff191aa3f8c;
  frozen method SHA256 823bf9fd12367271a55a7c614681faf28b1b6eac9ed7ec6b77c967fe7a1347ff
  (pre-registered via PREREG_MARKER.txt BEFORE the run).

## Discipline

Read-only originals (Models.bnt, K1 table, R61 source, contract) re-hashed after the run,
untouched; zero payload bytes written; run-local tooling only in 00_CONTROL; all outputs
inside the run dir; NO commit (per contract); NO nested tasks; NO wiki writes; the K1
resolution stands untouched; OBSERVED labels + standing sentence everywhere.
