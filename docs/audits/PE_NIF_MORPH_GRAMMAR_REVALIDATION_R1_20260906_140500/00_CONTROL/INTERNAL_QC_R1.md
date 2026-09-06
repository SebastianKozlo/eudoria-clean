# INTERNAL_QC_R1.md — fresh independent internal QC of RUN A
RUN: PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500 (RUN_CLASS LOAD_BEARING; executed, NOT committed)
QC context: fresh pe-master-auditor (did NOT execute the run); QC date 2026-09-06.
Assignment mode: INTERNAL_QC. Scope: re-derive every checklist item Q1..Q11 independently
from disk. READ-ONLY everywhere except this one file. NO_NESTED_TASKS.
Standing sentence: no semantic claims; class -256/field1 MEANING remains unknown; the
-256=>zero-entry association remains ONE-WAY. Result classes: BYTE_MATCH /
REPEATABILITY / RETROSPECTIVE_VALIDATION / ERA_TRANSFER_DIAGNOSTIC / RUNTIME_SEMANTICS
(= explicitly NOT_TESTED here, out of scope).

METHOD SUMMARY (independence):
1. Re-hashed every pinned input myself (contract, driver, K2 package, corpora, R61 tree).
2. Re-derived every reported number from the raw rows (my own code, standard parsers).
3. Re-executed the gate function with my own synthetic fixtures (import of the pinned
   driver module; module-level code only; no writes).
4. Re-executed the ENTIRE census + grammar pipeline from the physical corpora with my
   own replica code (pinned R61 reader + pinned K2 module functions; my own
   orchestration; 5,596-entry 9.3.5 corpus + 5,426-entry 2003 corpus) — the strongest
   counter-check: 4,283 per-record executions compared, 0 mismatches.
5. Recomputed Clopper-Pearson CIs with my own continued-fraction incomplete-beta
   implementation (different algorithm from the driver's lgamma-sum CDF bisection).

---

## Q1. Contract integrity — PASS

Command: `(Get-FileHash -Algorithm SHA256 00_CONTROL\CONTRACT.md).Hash`
My result: 02F32099AD7D9A528A6BC08C46E6C4F55C8218A06FBB482B5BE529E76DC34F95
Expected:  02F32099AD7D9A528A6BC08C46E6C4F55C8218A06FBB482B5BE529E76DC34F95 — EXACT MATCH.
Contract read to EOF (52 lines); driver also self-verifies the contract hash in S0
(PIN_RESULTS.contract_sha256, match asserted with hard stop armed).

## Q2. Freeze discipline — PASS (with P3 timestamp note, see DISCREPANCIES D2)

(a) Existence + timestamps (UTC, `Get-ChildItem ... LastWriteTimeUtc`):
- FROZEN_GRAMMARS.md 15:26:27 | NC_PROCEDURES.md 15:26:47 | GATES_PREREGISTERED.md 15:27:02
  — all three STRICTLY PRECEDE every 01_RAW/05_ANALYSIS output (earliest 15:59:18).
- POPULATIONS_334_325.json / SPLIT_SIDES.json / PREREG_MARKER.txt: 15:59:18 — the SAME
  second as the earliest raw outputs (RETRO_*.jsonl, BASELINE_CENSUS, PRIOR_USE_VERDICT).
  mtime alone cannot prove sub-second ordering for these 3 artifacts. Substance verified:
  (i) driver main() calls s2_freeze() BEFORE s3_retro() (code order read to EOF, lines
  2669-2691); (ii) PREREG_MARKER's recorded sha256 of all 5 frozen files == current
  bytes (re-hashed by me: FROZEN_GRAMMARS 3be116e7..., POPULATIONS 384a08b3...,
  SPLIT_SIDES 1a8f1e1d..., NC_PROCEDURES bb819ca6..., GATES bb525b3c...) — no
  post-freeze modification; (iii) the split is DETERMINISTIC and my seeded re-derivation
  reproduces it EXACTLY (below) — it could not have been adjusted after seeing results;
  (iv) the populations equal the pinned K2 dump headers EXACTLY (below).
(b) VERBATIM extraction verified PROGRAMMATICALLY (my comparison script over the pinned
  K2 driver b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a — re-hashed
  by me from bytes): ALL 10 blocks (B1 constants 79-82, B2 sane 96-97, B3 clean 100-103,
  B4 greedy_r18 121-144, B5 parse_variable 288-320, B6 parse_variable_trunctail 357-396,
  B7 H5a invocation 1003-1016, B8 H5c invocation 1035-1052, B9 H7 join 1152-1171,
  B10 nc2 871-882) are BYTE-EXACT VERBATIM matches at the claimed line ranges
  (10/10 VERBATIM_MATCH_RANGE; no rewording, no parameter changes). freeze_extraction.py
  (read to EOF) extracts by line range from the pinned file; the driver byte-verifies
  every block in S0 (recorded "10/10 VERBATIM byte-exact").
(c) GATES_PREREGISTERED.md gate text vs contract Section 5 (my normalized comparison):
  G-PINS/G-CENSUS/G-ERA/G-EXEC/G-SCOPE IDENTICAL; G-RETRO identical in every predicate
  (units >= 30 AND fits >= 10 AND rate >= 5x matched-NC AND NC denominator > 0; the
  explicit "THE VACUOUS CASE 0 >= 5x0 CANNOT PASS (NC denominator 0 => NC_EMPTY_-
  DENOMINATOR non-pass)" present; all five non-pass classes listed) — the only
  differences are two cosmetic whitespace insertions in class names
  ("INSUFFICIENT_TRIALS (<30 units)" vs "INSUFFICIENT_TRIALS(<30 units)";
  "NC_INSUFFICIENT_SEPARATION (<5x)" vs "NC_INSUFFICIENT_SEPARATION(<5x)").
  Semantics identical. P3 note D5.

## Q3. Driver code audit — PASS

(a) `Get-FileHash revalidate_driver_r1.py` = 02ecb955bc3796128ed3f3b99cc302df61649f9ac2202e83ee5860ed5de9dbe0 — EXACT MATCH. EXECUTED-BYTES PIN: PIN_RESULTS.driver_sha256 (computed by the driver itself in S0, mtime 15:58:56 > driver mtime 15:58:29) == current bytes → the executed script is the current script; no post-run edit. Driver read to EOF (2,695 lines).
(b) My independent scan (string-literals stripped, then pattern scan): 138 len()
  occurrences; ZERO assignments of validation/fit counts from len()/count arithmetic;
  only 2 `// 2` patterns = lines 1122-1123 `sideA = shuffled[:n // 2]` /
  `sideB = shuffled[n // 2:]` — the contract Section 3 file-level 50/50 split procedure,
  NOT a validation count. Matches SELF_AUDIT.txt (140 classified, forbidden patterns [],
  verdict CLEAN — count difference 138 vs 140 is a literal-stripping methodology
  artifact; the substantive result is identical: 0 forbidden).
(c) G-RETRO gate function `evaluate_gretro` (lines 859-955, read in full): n_units < 30
  -> INSUFFICIENT_TRIALS; n_unit_fits < 10 -> ZERO_FITS; nc_den == 0 ->
  NC_EMPTY_DENOMINATOR (checked BEFORE any rate comparison — the vacuous 0 >= 5x0 case
  cannot pass); `if not (rate >= 5 * nc_rate)` -> NC_INSUFFICIENT_SEPARATION; empty
  population / held-out side -> EMPTY_GROUP; plus fail-closed CORRUPTED_RECORD,
  DUPLICATE_ACROSS_SIDES, DENOMINATOR_MISMATCH (nc_den != units x expected). All fit
  counts are loop counter increments over executed records. MATCHES the contract.
(d) Eight negative fixtures exist in code (s6_gexec, lines 2083-2145) and are recorded
  in 01_RAW/NEGATIVE_FIXTURES_GEXEC.json: F1 zero-successes -> ZERO_FITS, F2 empty ->
  EMPTY_GROUP, F3 only-previously-selected (side A fits, B none) -> ZERO_FITS,
  F4 duplicate across groups -> DUPLICATE_ACROSS_SIDES, F5 63 trials for 32 units ->
  DENOMINATOR_MISMATCH, F6 corrupted record -> CORRUPTED_RECORD, F7 malformed manifest
  row -> MALFORMED_MANIFEST_ROW, F8 missing input -> MISSING_INPUT_FILE;
  all_eight_fail_closed = true, gexec PASS. INDEPENDENT RE-EXECUTION (my own fixture
  data through the imported driver's gate/validator): all 8 reproduce the same
  fail-closed classes; my extra vacuous-case fixture (non-empty population, 0 NC
  trials) also fails closed (DENOMINATOR_MISMATCH / NC_EMPTY_DENOMINATOR family);
  my positive control (32 unique valid units, NC 2/64) PASSES — the gate is not a
  fail-everything gate. Both directions verified.

## Q4. Raw re-derivation (the core) — PASS (all numbers EXACT)

From 01_RAW/RETRO_SPAN_OUTCOMES.jsonl + RETRO_NC_TRIALS.jsonl with my own parser:
(a) Row counts: 993 span-outcome rows (H5a 334 + H5c2 334 + H7 325; covers P1/P2 exactly,
  sides consistent with the split: 0 mismatches) and 1,947 NC rows (NC-A 1,336 = 668
  per grammar; NC-B 611). Executor claims 993 / 1,947 — CONFIRMED.
(b) H5a side-B (unit = byte-identical dp payload dedup, first-member side rule per
  GATES decision 1, re-derived by my own code): members 164 (7 cross-side members of
  6 split units excluded by the first-member rule, excl_B=0), units 163, unit fits 14,
  rate 0.085890 (recorded 0.08589), member fits 15, side A 163 units / 21 fits / 35
  files, side B 33 files. Gate NC re-derived FROM THE RAW NC ROWS via unit
  representatives: hits 2 / trials 326 = 0.006135 — CONFIRMED (2/326).
(c) H5c2 side-B: 163 units, 20 fits, rate 0.122699, member fits 20, same NC 2/326;
  side A 6 unit fits. CONFIRMED.
(d) H7 side-B: members 124, join-explained 40, rate 0.322581, units 124, unit fits 40;
  side A 200 members / 33 explained (0.165). Gate NC = 30 hits / 102 executed = rate
  0.294118 — CONFIRMED. NOTE: this 30/102 is the PER-UNIT representative NC
  (nc_units_B_executed/hits in RETROSPECTIVE_RESULTS.gate_nc_detail), not the per-span
  NC; per-span side-B NC = 23/102 = 0.225490 and pooled per-span NC = 53/290 = 0.182759
  (recorded pooled_span_level_nc 53/290 — CONFIRMED). All three quantities recorded;
  my re-derivations match. (The QC prompt's label "per-span NC 30/102" was imprecise;
  the run's own labels are correct.)
(e) Binomial CI recomputed with MY OWN implementation (continued-fraction regularized
  incomplete beta + bisection — algorithm independent of the driver's):
  H5a side-B rate 14/163: [0.047754, 0.139909] — EXACT MATCH with the recorded CI.
  Also recomputed exact: H5a NC 2/326 [0.000744, 0.021985]; H5c2 20/163
  [0.076584, 0.183123]; H7 40/124 [0.241451, 0.412412]; H7 gate NC 30/102
  [0.208024, 0.392546]; H7 side A 33/200 [0.116383, 0.223843]; era H5a 30/278
  [0.074003, 0.15046]; era H5a NC 4/556 [0.001964, 0.018317]; era H5c2 26/278
  [0.062006, 0.13403]; era H7 66/311 [0.168101, 0.261912]; era H7 NC 61/539
  [0.087682, 0.142993]; era H7 family 35/49 [0.56737, 0.834158]. 12/12 EXACT.
(f) Repeatability: the union of both sides' fits (from my raw-row re-derivation)
  equals K2's pinned FULL-population fit lists as IDENTICAL SETS (not just counts):
  H5a 39 = 39 (set-identical), H5c2 26 = 26 (set-identical), H7 join_of_325 74 = 74
  (set-identical, computed as (K2 H7a | H7b) & P2-325 by me); H5a NC hits 5 = 5
  (list-identical), H5c2 NC n_nc 5 = 5. Cross-checked against K2
  05_ANALYSIS/HYPOTHESIS_RESULTS.json (fit lists) and COVERAGE_STATE.json
  (h7_join_of_325 = 74; newly_covered 65 = 39+26; 2158/2427 candidate) — CONFIRMED.

INDEPENDENT RE-EXECUTION FROM THE PHYSICAL CORPUS (my own census replica; pinned R61
reader + pinned K2 module functions; zero payloads written; ~41 s):
- MY 9.3.5 census: big_spans 10,274 / fits 6,167 / entries 65,050 / pad_floats 143,874;
  g1 132 / g2 1,547 / var 3,186 / mscan_any 3,705; rr 2,427 / var-of-rr 2,093 / nofit
  334 = 62 alt + 272 none; neither 3,438 / backtrack 3,105 / shift 114 / shift_only 8 /
  unknown325 325 / r21_unknown 333 / files 56 / top 551564.nif x84; blocks 354/334;
  files_with_morph 109 — EVERY anchor reproduces the run's G-CENSUS EXACTLY.
- MY populations: nofit == pinned NOFIT334_SPANS.txt headers (334, set-identical);
  r21u == pinned RESIDUAL333 headers (333); unknown325 = 325, subset of 333.
- Per-record RE-EXECUTION vs the run's recorded rows (outcome + reason +
  bytes_consumed + leftover/records + unit sha256): H5a 334 checked / 0 mismatches;
  H5c2 334 / 0; H7 325 / 0; NC-A 1,336 / 0 — every recorded row is a faithful
  execution of the frozen grammars on the true spans.
- MY gate numbers from MY OWN data: H5a units 163 / fits 14 / rate 0.085890 / NC 2/326;
  H5c2 163/20/0.122699/NC 2/326; H7 124/40/0.322581; H7 per-unit gate NC (rng2 seed
  20260906, sorted unit hashes, representative mirror joins) = 102 executed / 30 hits
  / rate 0.294118 — EXACT (closes the transparency gap for the not-persisted
  per-unit NC trial rows).

## Q5. The 2003 leg — PASS

(a) PRIOR_USE_VERDICT.json cites REAL evidence: grep'd line numbers in the R34/R18/R21
  derivation drivers + K2 driver + R35 report. I verified each cited line myself:
  morph_quant_r34.py:60, morph_keyframe_r18.py:26, unknown325_r21.py:22,
  morph_residual_deepdive_r1.py:48 all contain `MODELS_BNT = r"D:\...\pcg_install\
  Data\Models\Models.bnt"` (the 9.3.5 corpus); R35 REPORT.md:5 contains the P0
  ("Do the grammars CONFIRMED on the 9.3.5 corpus hold on the 2003 corpus") and :56
  the FORMAT EVOLUTION TABLE. Verdict "NO grammar derived from 2003 data; R35 =
  prior VALIDATION exposure (pre-K2), recorded with paths" — SUPPORTED by real
  evidence, not a bare assertion.
(b) ERA_DUPLICATE_CENSUS.json re-verified from the container bytes of BOTH eras
  (my own payload hashing of both Models.bnt indexes): 8/8 sampled claimed-identical
  pairs byte-identical (e.g., 546483.nif c414397f... == c414397f..., 574845.nif
  087464f4... ==, 588768.nif 0f0e5e81... ==); all 3 claimed-changed pairs DIFFER
  (548296.nif 733,491 vs 732,481 B; 548808.nif 744,536 vs 742,912 B; 566482.nif
  161,254 vs 161,422 B — different sizes AND hashes); 4/4 sampled only-935 files
  absent from the 2003 container; FULL re-derivation of all 79 recorded shared
  morph files: 76 identical + 3 changed — EXACT (claim 76/79).
(c) Era numbers re-derived from ERA_SPAN_OUTCOMES.jsonl + ERA_NC_TRIALS.jsonl
  (867 + 1,651 rows): H5a 30/278 = 0.107914 vs NC 4/556 = 0.007194; H5c2 26/278
  (NC 4/556); H7 66/311 = 0.212219 vs NC 61/539 = 0.113173 — ALL EXACT.
  Reinforced by my corpus re-execution: MY 2003 census reproduces every anchor
  EXACTLY (walk 8,385/4,674/41,438/115,755; rr 1,457; var-of-rr 1,179 bi-keyed;
  nofit 278 = 58+220; unknown 311; neither 3,133; backtrack 2,815; shift 81;
  shift_only 7; blocks 286/272; files_with_morph 79) AND the two-way rr_var
  resolution (tag-keyed 1,180 == R35's published value; collider = 574845.nif
  bi=77 si=14 tag=3, var_ok but NOT rr — exactly as documented); per-record era
  re-execution: H5a 278/0, H5c2 278/0, H7 311/0, era NC-A 1,112/0 mismatches;
  era populations == era JSONL span sets (278/311 EXACT); cross-era dp overlap
  278/278 and 311/311 EXACT (re-derived from my own dp hashes across eras);
  P1_2003 families 54 and P2_2003 families 49 EXACT (my union-find re-derivation).

## Q6. The 2003 corpus resolution — PASS

PIN_RESULTS.json + ERA_CENSUS_2003.json record physical path
D:\Eudoria_Reconstruction\01_Original_Files\BNT_Models\Models.bnt with FULL SHA256
1322adf2919b1b24a8b4fda9618347e00c5a2b35dbb54516e353f1cefd3524a6 — I re-hashed the
physical file myself: MATCH. Entry count re-derived with my own BNT index parser:
5,426 entries / 5,426 unique names / 5,426 .nif — the 5,426-name class EXACTLY.
The count cross-check RAN (in-driver, hard stop armed) and I reproduced it
independently: R12 manifest_2003.csv = 5,442 physical lines incl. header = 5,426
CSV records (5,426 PASS rows) — the contract's "~5,441" class is the physical-LINE
count, and the extraction dir contains exactly 5,426 .nif files; the driver's
container<->extraction byte-tie (5,426/5,426) is recorded in PIN_RESULTS
(container_extraction_tie). NOTE (D3): the R12 detail fields
(physical_lines/csv_records/pass_rows) were overwritten in PIN_RESULTS.json by the
generic pin loop (key collision) — the numbers survive in the corpus_2003
name_class_check prose and I verified them independently.

## Q7. G-CENSUS — PASS

05_ANALYSIS/BASELINE_CENSUS_REPRODUCTION.json: rr 2,427 / var 2,093 / nofit 334 =
62 alt + 272 none; unknown-325 = 325 across 56 files (551564.nif x84); walk
10,274/6,167/65,050/143,874; g1 132/g2 1,547/var 3,186/mscan 3,705; neither 3,438/
backtrack 3,105/shift 114/shift_only 8/r21u 333; row agreement [6,167, 6,167, 0].
All 27 census_checks true; census_exact true. The expected anchors are K2's own
recorded numbers (verified against K2 05_ANALYSIS/BASELINE_REPRODUCTION.json —
identical; not invented). MY OWN census re-execution reproduces EVERY anchor EXACTLY
(see Q4) — G-CENSUS independently CONFIRMED by execution, not just by reading the
driver's output. R34 corroboration: REAL_SPARSE_GRAMMAR per_span has 6,167 rows with
g1_ok sum 132 and var_ok sum 3,186 — equal to my census aggregates (consistent with
the recorded 6,167/6,167 row agreement).

## Q8. Manifest — PASS

Per RUN B's MANIFEST_SCHEMA_SPEC.md (read to EOF). My independent validation
(standard csv.reader; 64-hex regex; path existence; physical hash re-computation;
duplicate check):
- Ordinary rows: 27 valid (artifact,role,sha256; every file exists; every hash equals
  the current physical bytes; no duplicates). External section: 22 valid
  (source_id,kind=external_source,era in {PCG_9_3_5,2003},physical_path exists,hash
  matches — I re-hashed all 22 physical files). Total data rows 49; findings NONE.
- Every on-disk package file except the two DOCUMENTED exclusions (artifact_index.csv
  self-hash; 05_ANALYSIS/MANIFEST_VALIDATION.json circular — both per the spec's
  self-hash precedent and disclosed in MANIFEST_VALIDATION.json) is present in the
  manifest. STAGE_ACCEPTANCE_GATES.csv is included with its final on-disk hash.
- MANIFEST_NEGATIVE_TESTS.json: 6/6 cases (a unquoted comma, b missing newline,
  c missing file, d malformed hash, e unsupported path shape, f duplicate row)
  recorded as gate_failed_as_required = true; all_six_fail_the_gate = true. My
  re-execution of fixture-7/manifest validation reproduces MALFORMED_MANIFEST_ROW.
- MANIFEST_VALIDATION.json records pre-validation (26 rows, before the gates CSV) and
  post-write validation (27 ordinary + 22 external, PASS) — matches my counts.
NOTE (D6): the QC prompt's "49 ordinary rows" — the run's records correctly say
27 ordinary + 22 external (= 49 total data rows); no run-side discrepancy.

## Q9. Scope/boundaries — PASS

- Corpora (recorded in PIN_RESULTS): Models.bnt 9.3.5 re-hashed by me =
  c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0 (pin c950a8c2...);
  Models.bnt 2003 = 1322adf2919b1b24a8b4fda9618347e00c5a2b35dbb54516e353f1cefd3524a6
  (pin 1322adf2...) — both UNCHANGED.
- K2 package: all 7 contract-pinned artifacts re-hashed by me — ALL MATCH (driver
  b7e4cd32..., NOFIT334 8bb6556b..., RESIDUAL333 e936ed51..., COVERAGE_STATE
  86c12fa7..., BASELINE_REPRODUCTION 2e4014c9..., HYPOTHESIS_RESULTS c08fb473...,
  PRE_REGISTERED 5bde44ac...). K2 package NOT modified by this run.
- R61 frozen parser tree: 10/10 .py pins re-hashed by me — ALL MATCH; source file
  mtimes 2026-08-21..2026-08-25 (pre-run; untouched).
- Repo state (eudoria-clean): BASE_SHA 90c86be9e52d00e4dd916ea75bc99ea93354c88f is
  commit 90c86be (2026-09-06T11:56:47Z) — the HEAD at contract formalization
  (14:11:58Z). Current HEAD = bc11a63 (15:09:17Z); the four intervening commits
  (14eda26, 0470985, cdbbb53, bc11a63) are PE-MASTER loop bd17344b RUN B governance/
  persistence commits touching ONLY RUN B / entrypoint / ledger paths — NONE touch
  RUN A, and the RUN A run dir (99_Audits) lies OUTSIDE the eudoria-clean repo tree.
  The executor made NO commit / NO repo write — the report's "BASE_SHA ... unchanged
  by this run" is accurate as scoped to this run's writes.
- Zero payloads: run-dir extension census = 2 .csv, 6 .md, 2 .py, 13 .json, 4 .jsonl,
  2 .txt — ALL small text artifacts (no .nif/.bnt/.bin or any binary; every JSONL
  parsed as text; no hex dumps). The 2 .txt files are PREREG_MARKER.txt and
  SELF_AUDIT.txt (text metadata, not payloads).

## Q10. Report honesty — PASS (with P2 note D1)

06_REPORT/00_FINAL_REPORT.md read to EOF. Every number checked against my own
re-derivations (Q2-Q9) — ALL EXACT:
- H5a PASS units 163 / fits 14 / rate 0.08589 / CI [0.047754, 0.139909] / NC 2/326
  0.006135 [0.000744, 0.021985];
- H5c2 PASS 163 / 20 / 0.122699 / [0.076584, 0.183123] / NC 2/326;
- H7 NON_PASS NC_INSUFFICIENT_SEPARATION 0.322581 vs NC 0.294118; held-out 124/40
  CI [0.241451, 0.412412]; NC units 102 / hits 30 CI [0.208024, 0.392546] — the
  HONEST NON-PASS IS REPORTED (also in §3, §4, gates CSV, RETROSPECTIVE_RESULTS).
- Era: 278/311 populations, 30/26/66 fits, NC 4/556 + 61/539, near_zero_transfer=False
  (H5a 0.108 and H5c2 0.094 >= 5x their NC 0.0072 -> transfer signal; H7 0.212 < 5x
  0.113 -> no signal) — consistent.
- Split 85 files (42 A / 43 B) — my seeded re-derivation EXACT.
- "+65/88.88% coverage status REMAINS CANDIDATE" stated (§1, §3, §9); no wiki action;
  no commit; result-class labels applied CORRECTLY (RETROSPECTIVE_VALIDATION with
  explicit "NOT unseen"/"NOT holdout" statements §4/§7-8; REPEATABILITY for census +
  repeatability blocks; ERA_TRANSFER_DIAGNOSTIC for the era leg with "explicitly NOT a
  substitute for 9.3.5-target correctness"; RUNTIME_SEMANTICS explicitly NOT_TESTED
  §7-8/§16); the standing sentence present in EVERY artifact of the package (all 29
  files checked; JSONL rows carry per-row result_class).
- §20 numbers (5,426-name class, 5,442 lines, 334/325, 56 files, 551564 x84,
  seed 20260906, prior-use NO) — all verified above.
- §18 provenance (driver SHA, K2 module import, 10/10 byte-verified, row agreement
  6,167/6,167) — all verified.
NOTE D1 (P2): §14 "HARD STOPS: NONE encountered" is TRUE for the final completed
execution, but does not cross-reference the preserved development-phase hard-stop
evidence (05_ANALYSIS/HARD_STOP_EVIDENCE.json) — see Q11. The underlying finding is
disclosed in §7/8 (R35 key-collision), so no claim is false; the gap is a missing
cross-reference, not a misstatement.

## Q11. HARD_STOP_EVIDENCE.json — PASS (disclosed stop + resolution documented)

The file (mtime 15:43:32 UTC, BEFORE the final run's outputs) preserves the disclosed
in-run development hard stop: reason "2003 era census mismatch vs R35 published
anchors (corpus/process divergence)", evidence = census checks with
rr_state.var_exact_of_rr 1179 (computed) vs 1180 (then-expected), elapsed 54.3 s.
Its RESOLUTION is documented in three places: (i) the driver source (lines 118-126:
the (file,tag,si) key-collision analysis — 26 collisions among 2003 fit spans, exactly
one load-bearing collider; both values asserted two-way in s45_era with hard stop
armed); (ii) 05_ANALYSIS/ERA_CENSUS_2003.json rr_var_resolution (bi-keyed collision-
free 1,179 + tag-keyed 1,180 reproducing R35 + collider record 574845.nif bi=77
si=14 tag=3 var_ok-but-NOT-rr); (iii) final report §7/8 (the R35 prior-evidence defect
paragraph). My independent census re-execution CONFIRMS both values and the exact
collider. The final run completed with no hard stop; the evidence file was preserved,
not deleted, and is hashed in the manifest. Related development disclosures preserved
in-source: the Clopper-Pearson direction inversion of the first two executions
(docstring, "caught in output review, fixed, and re-run before any use of these
numbers downstream") and the self-audit scanner's two first-execution false
positives (its own pattern literals). NOTE: neither development iteration is named in
the final report itself (only in-source + the preserved evidence file) — see D1.

---

## INDEPENDENT RE-EXECUTION SUMMARY (counter-check by execution; the strongest evidence)

My own replica census (pinned R61 reader + pinned K2 grammar functions; my code) over
the physical corpora, then per-record comparison with the run's raw rows:

| check | mine | run's | verdict |
|---|---|---|---|
| 9.3.5 census anchors (all 27) | identical | identical | EXACT |
| 2003 census anchors | identical | identical | EXACT |
| rr_var two-way (2003) | 1179 / 1180 + collider 574845 bi=77 si=14 tag=3 | same | EXACT |
| H5a per-record (334) | 0 mismatches | — | EXACT |
| H5c2 per-record (334) | 0 mismatches | — | EXACT |
| H7 per-record (325) | 0 mismatches | — | EXACT |
| NC-A per-trial (1,336) | 0 mismatches | — | EXACT |
| era H5a/H5c2/H7 per-record (867) | 0 mismatches | — | EXACT |
| era NC-A per-trial (1,112) | 0 mismatches | — | EXACT |
| H5a gate | 163/14/0.085890 NC 2/326 | same | EXACT |
| H5c2 gate | 163/20/0.122699 NC 2/326 | same | EXACT |
| H7 gate | 124/40/0.322581 NC 102/30 | same | EXACT |
| split (seed 20260906, 85 files) | A 42 / B 43, all ID lists | same | EXACT |
| cross-era dp overlap | 278/278, 311/311 | same | EXACT |
| era families | 54 / 49 | same | EXACT |
| Clopper-Pearson CIs (12 recomputed) | identical to 6 dp | same | EXACT |

Total per-record re-executions compared: 4,283 (334+334+325+1336+278+278+311+112 plus
gate representative executions) — 0 mismatches.

## DISCREPANCIES

None of the discrepancies below affects any gate verdict, reported number, or claim;
they are documentation/process-level and disclosed here for PE-MASTER's post-run audit.

1. **P2 — Final report §14 does not cross-reference the preserved development hard
   stop.** 06_REPORT/00_FINAL_REPORT.md §14 "NONE encountered" is accurate for the
   final completed execution, but a report-only reader is not pointed to
   05_ANALYSIS/HARD_STOP_EVIDENCE.json (an earlier same-RUN_ID execution hard-stopped
   on the 2003 rr_var anchor; the driver's expected-anchor logic was amended to the
   documented two-way resolution). The substance IS disclosed (§7/8 R35 key-collision
   finding; in-source resolution comments; the evidence file preserved + manifest-
   hashed). Skutek: incomplete disclosure surface; poprawka (proposed to PE-MASTER):
   an amendment note cross-referencing HARD_STOP_EVIDENCE.json in §14 of any
   persisted review copy; rewalidacja: §14 wording + file presence.
2. **P3 — Freeze mtimes tie for 3 of 6 freeze artifacts.** POPULATIONS_334_325.json,
   SPLIT_SIDES.json, PREREG_MARKER.txt have mtime 15:59:18 UTC — the same second as
   the earliest 01_RAW/05_ANALYSIS outputs, so mtime alone cannot prove freeze-before-
   test for these three. Substantiation provided instead: driver code order (s2_freeze
   before s3_retro in main()), marker hashes == current bytes, seeded deterministic
   split/populations re-derived EXACTLY, in-driver hard stops on any population/pin
   mismatch. No evidence of post-hoc adjustment exists; the freeze is substantiated by
   content, not by filesystem timestamps.
3. **P3 — PIN_RESULTS.json R12 detail fields lost to a key collision.** The
   R12_manifest_2003 dict (physical_lines 5,442 / csv_records 5,426 / pass_rows 5,426)
   is overwritten by the generic pin loop's entry of the same key. The numbers survive
   in corpus_2003.name_class_check prose; I verified them independently (5,442/5,426/
   5,426). Effect: reduced machine-readability of the count cross-check in PIN_RESULTS.
4. **P3 — Era H5a/H5c2 per-record rows omit the `unit` field.** Retro rows and era H7
   rows carry it; era H5a/H5c2 rows do not, so era unit-level and P1-family numbers
   are not row-re-derivable from the package alone (member-level and NC are). Closed
   by my corpus re-execution (era units/families verified: P1 families 54 EXACT).
5. **P3 — Two cosmetic whitespace insertions in GATES_PREREGISTERED.md's G-RETRO text
   vs the contract** ("INSUFFICIENT_TRIALS (<30 units)", "NC_INSUFFICIENT_SEPARATION
   (<5x)"). Predicates semantically identical (verified field by field).
6. **P3 (no-run-defect) — Two imprecisions in the QC instruction itself, corrected
   here:** (a) "49 ordinary rows" — the manifest has 27 ordinary + 22 external = 49
   total data rows (the run's own records are correct); (b) H7 "per-span NC 30/102" —
   30/102 is the per-UNIT representative gate NC (the run labels it correctly);
   per-span side-B NC is 23/102 = 0.225490, pooled per-span NC 53/290 = 0.182759,
   both recorded. All three values independently verified.

## FULL_READ_LOG (read to EOF unless noted)

Run package (all 29 files): CONTRACT.md; revalidate_driver_r1.py (2,695 lines);
freeze_extraction.py; FROZEN_GRAMMARS.md; GATES_PREREGISTERED.md; NC_PROCEDURES.md;
PREREG_MARKER.txt; PIN_RESULTS.json; SPLIT_SIDES.json (full programmatic parse +
verbatim-comparison of all ID lists); POPULATIONS_334_325.json (full programmatic
parse of all 334+325 IDs); BASELINE_CENSUS_REPRODUCTION.json; ERA_CENSUS_2003.json;
ERA_TRANSFER_RESULTS.json; RETROSPECTIVE_RESULTS.json; PRIOR_USE_VERDICT.json;
ERA_DUPLICATE_CENSUS.json; NEGATIVE_FIXTURES_GEXEC.json; MANIFEST_NEGATIVE_TESTS.json;
MANIFEST_VALIDATION.json; HARD_STOP_EVIDENCE.json; SELF_AUDIT.txt;
STAGE_ACCEPTANCE_GATES.csv; artifact_index.csv; 00_FINAL_REPORT.md; HANDOFF.md;
RETRO_SPAN_OUTCOMES.jsonl / RETRO_NC_TRIALS.jsonl / ERA_SPAN_OUTCOMES.jsonl /
ERA_NC_TRIALS.jsonl (100% of rows parsed programmatically; spot reads shown).
External (read-only): RUN B MANIFEST_SCHEMA_SPEC.md; K2 BASELINE_REPRODUCTION.json;
K2 COVERAGE_STATE.json; K2 HYPOTHESIS_RESULTS.json (fit lists + n_nc, programmatic);
K2 driver (pinned b7e4cd32... — the 10 frozen blocks byte-verified + cited lines
verified; not read to full EOF beyond that, see NOT_CHECKED); NOFIT334_SPANS.txt /
RESIDUAL333_SPANS.txt (header lines, programmatic); R12 manifest_2003.csv (line +
CSV-record census); R34 REAL_SPARSE_GRAMMAR.json (per_span count + field sums);
R34/R18/R21 drivers + R35 REPORT (cited lines); both Models.bnt corpora (full byte
read: hash + index + payload parse for the census re-execution); R61 01_source (10
files hashed + used via import); 2003 extraction dir (file count).

NOT_CHECKED (explicit; none gates a verdict):
- Full EOF read of the pinned K2 driver beyond the 10 frozen blocks + verified lines
  (its load-bearing content for this run IS the frozen grammar code — byte-verified —
  and it is a prior completed run's artifact, not this run's code).
- Full EOF read of the R61 parser modules (pinned by hash 10/10, exercised by import,
  corroborated by the exact census reproduction + R34 row agreement).
- K2 HYPOTHESIS_RESULTS.json fields outside this run's claims (H5c1, H1-H4, H6, H8
  details — out of this run's gate set per contract).
- Payload hex bodies of NOFIT334/RESIDUAL333 dump files (headers only; the spans were
  instead re-derived from the corpus — stronger).
- K2 artifact_index.csv (contract §2 forbids using it as a hash source; all K2
  artifacts re-hashed from bytes instead).
- eudoria-clean remote (origin) state — this run makes no remote claims (no commit/
  push; local HEAD/BASE verified).
- PE-MASTER loop state files — outside this run's contract inputs.

QC_VERDICT = QC_PASS
