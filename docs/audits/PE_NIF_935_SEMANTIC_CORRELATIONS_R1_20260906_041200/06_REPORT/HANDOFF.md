# HANDOFF — PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200

EU935-M1 KROK-3 (final ladder step), RUN_CLASS MATERIAL, era PCG 9.3.5.
One primary question: what do the four pre-registered offline statistical
probes OBSERVE about the four open NiArk/semantic fields — every result
OBSERVED-labeled, every correlation tested against a 10,000-label permutation
control.

STANDING SENTENCE: correlation outputs are OBSERVED-level evidence; semantic
roles remain runtime-gated (KROK 4 class).

## COMPLETION STATUS

- COMPLETED: all 4 probes executed on the full pinned corpus
  (parse closure 5,596/5,596; R61 10/10 READ-ONLY; corpus SHA
  c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0 re-hashed
  in-driver). 42 test rows = 33 executed with permutation controls
  (RNG seed 20260906) + 9 constant variables documented NO TEST.
- G2 canon reconciliation: ZERO mismatches (flag 558/128/72; field1
  3,042/1,796; events 263/136/113; viewport 2,304/752/592/79/11;
  importer 4,838/758; R29 exporter matrix 8/8; viewport total 4,095 =
  registry). A transient CENSUS_MISMATCH HARD STOP during development
  execution #2 was a reconciliation-CODE bug (joint-tuple destructuring),
  investigated and fixed before the final run; final G2 = 0 mismatches.

## HEADLINE OBSERVATIONS (all OBSERVED-level; control numbers in 05_ANALYSIS)

1. PROBE-1 (758 v4 importer flags): flag state OBSERVED-correlates with the
   EXPORTER STRING (chi2 61.6 vs perm p95 9.5), block count (21.1/12.5),
   geometry size (55.5/13.0), texture entry count (19.7/12.9) — but NOT with
   nif version (0.36/9.5). Mesh/morph/mirror constants documented. 00ffff is
   exclusively 4.1.0.12-exporter (72/72); 0000ff mostly (126/128).
2. PROBE-2 (4,838 v10 ArkTexture): the field1=-256/low8=255 class (1,796) has
   entry_count=0 in 1,796/1,796 files and NO slot entries of any kind; all
   19,637 entries live in the field1=1 class. Every slot/effect/mesh/mirror
   test is OBSERVED (e.g., BASE 4,703/3.7; mesh 4,736/3.9) but they are
   correlates of this one zero-entry structure — NOT independent semantic
   evidence. Class MEANING remains unknown.
3. PROBE-3 (263 event strings): zero/non-zero × family OBSERVED (24.8 vs
   p95 9.0, p_perm 1e-4). SOUND_HIT (20/20) and END_MORPH1 (2/2) strings
   NEVER carry 0.0; ANIMCMD_500078 10/11 non-zero; MORPH_LR ~49% zero.
   Families: 213 morph-LR / 20 sound-hit / 17 start_usetool / 11 animcmd /
   2 end+morph:1; OTHER=0; all 263 float-interpretable.
4. PROBE-4 (viewport floats): position 1 = exactly 2.0 in 592/592 + 79/79
   (fov-like constant, canon-consistent; POSITION-STATISTICS only). 43B
   subclasses 3 all-zero-default / 8 parametric (R28-exact). k-means
   (pre-registered): 85B k=3 {587,2,3}, 121B k=4 {76,1,1,1}; 85B outlier
   clusters OBSERVED-correlate with skinned (54.0/12.6) and block-count
   (29.9/17.1); 121B none. Pooled ext-length class × block-count OBSERVED
   (98.9/19.2), × era-mirror weakly OBSERVED (8.2/6.6). 27/592 + 4/79
   vectors carry non-finite 4-aligned bit patterns (censused, sanitized for
   clustering — pre-registered amendment).

## RUN_CLASS MATERIAL packaging

- COMPLETION: COMPLETED; HARD_STOP_REASON = NONE in the final run.
- AUDIT_OUTPUT_ROOT: docs/audits/PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200
  + byte-identical 99_Audits mirror (D:\Eudoria_Reconstruction\99_Audits\...).
- Driver 00_Control/semantic_correlations_r1.py SHA256
  927b256679e28dfc1e1e2284ceebd680d9ee52f1b5b8e53f3ed48b3397d1f4a7 ==
  SHA256_DRIVER.txt (hash-after-last-edit; 3 pre-final-run defect fixes
  documented in the report process note + driver docstring amendments).
- Machine-readable: 01_RAW/EXTRACTION.json + PROBE1-4_RAW.csv;
  05_ANALYSIS/{RECONCILIATION,PROBE1_CONTINGENCY,PROBE2_CONTINGENCY,
  PROBE3_FAMILIES,PROBE4_POSITION_STATS,PROBE4_CLUSTERS}.json;
  STAGE_ACCEPTANCE_GATES.csv (G1-G6); artifact_index.csv (in-driver hashes).
- Gates: G1 PASS / G2 PASS (0 mismatches) / G3 PASS (33 permutation
  controls + 9 documented constants) / G4 PASS (OBSERVED labels + standing
  sentence everywhere) / G5 PASS / G6 PASS (read-only originals, zero
  payloads, path-limited commit exactly 1 path, push, origin==HEAD).
- COMMIT_SHA: see git log — path-limited commit of exactly
  docs/audits/PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200/
  (this HANDOFF cannot contain its own commit SHA).
