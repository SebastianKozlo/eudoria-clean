# CORRECTION_NOTES — hygiene supplements of the M1 gate package

- CREATED BY: PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816 (the bounded, mechanical
  completion run; PE-MASTER ORDERED_WORK relayed verbatim by the human 2026-09-05).
- RULE: these are NOTES/SUPPLEMENTS ONLY. The frozen evidence files of the completed
  validator-coverage repair run (PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439) and of
  the historical M1 tree are NEVER edited — every correction below lives HERE, in the
  completion run's records, and in EVIDENCE_MANIFEST.json fields. No history rewrite.

## HYG-1 — the synthetic-domain PC24 field is NOT a measurement (PE_MASTER CODE_FINDING 1)

`01_RAW\domain_reproof.json` → `lerp_scale_synthetic.lerp_pc24_mismatches = 0` of the
validator-coverage repair run is a DEFAULT COUNTER (`measure_pc24=False` in
`00_CONTROL\repair_02_domain.py`), NOT a measurement. Read as a measured value it is
misleading (a false "real 14,104 / synthetic 0" asymmetry).

- STATUS OF THAT FIELD: **NOT_MEASURED** by the repair run.
- THE ACTUAL VALUE (independent, auditor-side): **103,073/1,245,184** — PE-MASTER's own
  platform-validated re-derivation on the synthetic extended sensitivity domain
  (PE_MASTER_REVIEW.md CODE_FINDING 1: "prawdziwa wartość = 103,073/1,245,184").
  Physically this STRENGTHENS the x87 conditional model (PC=24 is even more material on the
  synthetic domain); it changes no recorded verdict.
- The load-bearing number for the open x87 CW item remains the REAL-domain sensitivity
  **14,104/229,376** (independently confirmed by PE-MASTER: "DOKŁADNIE 14104"), plus
  rand01/positions PC24 = 0.

## HYG-2 — the dead null key in domain_reproof.json (PE_MASTER CODE_FINDING 2)

`01_RAW\domain_reproof.json` → `counter_sums_generated` contains a descriptive key
(`rand01_32768_plus_positions_65536_plus_real_2x229376_plus_synth_2x1245184`) with value
`null` beside the real counter `total_exactness_comparisons: 3047424`
(`00_CONTROL\repair_02_domain.py` lines 417-420). Cosmetic JSON cruft in a FROZEN evidence
file — noted here, NOT edited out. The authoritative counter is `total_exactness_comparisons
= 3,047,424` (generated from results, never typed; both sums independently recomputed by
PE-MASTER).

## HYG-3 — the failed-attempts register: 8 log FILES vs 10 EVENTS (PE_MASTER CODE_FINDING 3)

The repair-run report/gates figure "8 failed attempts" counts the retained LOG FILES
(`02_LOGS\repair_01_oracle_run1..4.log` = 4, `repair_02_domain_run1.log` +
`repair_02_domain_run4_progress.log` = 2, `repair_05_recheck_run1.log` +
`repair_05_recheck_run2.log` = 2). `02_LOGS\LOGS.md` describes 10 failed-attempt EVENTS:
- repair_01_oracle.py: 4 events (run1 ValueError; run2 13 failures incl. 1 real library gap;
  run3 SyntaxError BOM; run4 1 vector error) — 4 log files;
- repair_02_domain.py: 4 events (run1 TypeError; run2 + run3 = 2 TIMEOUT KILLS **without log
  files**; run4 stalled, progress log retained) — 2 log files;
- repair_05_recheck.py: 2 events (run1 KeyError; run2 3 failures) — 2 log files.
Both numbers are correct answers to different questions: **8 files / 10 events**. The
register is honest (every attempt root-caused, fixed, re-hashed; ZERO evidence claimed from
failed attempts).

## HYG-4 — hardcoded numbers without assert-vs-evidence (PE_MASTER CODE_FINDING 4, process note)

`repair_06_analysis.py` reads the evidence JSONs but typed the numbers into the
V3_ROW_DELTAS / VALIDATOR_MUTATION_MATRIX texts (no extraction/assert). PE-MASTER manually
verified every present value (all consistent), so NO recorded result is in question; the
missing mechanism is only future-inconsistency detection. Recorded as a PROCESS NOTE:
- completed-run files are NOT retrofitted with asserts (frozen history stays frozen);
- THIS completion run's builder (00_CONTROL\build_gate_package.py of
  PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816) extracts its load-bearing numbers from
  the evidence JSONs and ASSERTS the PE_MASTER_REVIEW figures (fail-loud on any
  disagreement) instead of typing them.

## HYG-5 — the iter033_manifest.json citation-label defect (THIS run's pre-build verification)

The OLD matrix (frozen ITER_048 copy in GATES\M1_GATE_DELIVERABLE_MATRIX.md, rows 7/8/10/18
EVIDENCE lines) and — carried verbatim — the V3 `carried_evidence` cite
"iter033_manifest.json (F299C622...)". **F299C622... is NOT the SHA256 of
iter033_manifest.json**; it is the SHA256 of `assets/foliage_glb/MANIFEST.json` — the repo
runtime file pinned INSIDE iter033_manifest.json (its `repo_runtime` list).

Mechanical reconciliation, from existing records ONLY (no re-derivation):
1. `iter033_manifest.json` (physical, mtime 2026-09-04 21:59:41) re-hashes to
   **DD59815206F35E795B6A9E6BE6A89C053DF17B9DF696CAB9658D0026179BBFAA** (6,328 bytes) and its
   own content records `assets/foliage_glb/MANIFEST.json` = F299C622... (3,182 bytes);
2. the present-day repo file `assets/foliage_glb/MANIFEST.json` re-hashes to EXACTLY
   F299C6222917DA8859351D9BE4D2DF0D40F9C6BB7767378DFB22B18C4FFAD46C (committed in b7d38ad);
3. the ITER_034 build-time sweep (iter034_regression_sweep.json.evidenceShaVerification)
   verified the manifest's INTERNAL records ("iter033 manifest 4/4 evidence + 7/7 repo
   runtime files ... ALL MATCH") — it never recorded the manifest file's own hash;
4. the manifest mtime PRECEDES the old-matrix mtime (22:10:24) — no post-matrix file
   modification occurred; this is a citation-label defect in the matrix authorship, not
   tampering.

NO claim verdict is affected: row 8's validation basis ("the manifest SHAs pinned in
iter033_manifest.json") remains true, the V1 audit's spot-check (iter033_rng_crosscheck
F8056CD5... EXACT) and PE-MASTER's input re-hashes (census 3AAFBF48..., probe 3D878E5F...)
all re-verify. EVIDENCE_MANIFEST.json carries BOTH files with their physically-verified
SHAs. The frozen OLD matrix copies are NOT edited; this note is the standing correction.

## Standing rule for all five

If any future evidence contradicts these notes, the evidence wins and the contradiction gets
reported — these notes correct READING of the records, they do not alter any frozen file.
