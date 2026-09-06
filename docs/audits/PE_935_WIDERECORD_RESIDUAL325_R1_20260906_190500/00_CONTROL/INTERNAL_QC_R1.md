# INTERNAL_QC_R1 — RUN E: PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500

- QC mode: INTERNAL_QC, FRESH independent pe-master-auditor context (no executor involvement, no prior-session state carried over).
- Date: 2026-09-06 | PARENT: PE-MASTER loop bd17344b-a054-4cf4-be8d-5f0b250e8509 (iteration 5) | MILESTONE: EU935-M1 (NO crossing).
- Discipline honored: READ-ONLY against the entire run package except this ONE file; all QC tooling executed from `C:\Users\User\AppData\Local\Temp\opencode\` (outputs only there); NO_NESTED_TASKS (no Task dispatch); nothing committed; nothing else modified.
- QC verdict scope: this is INTERNAL_QC of RUN E, not MASTER_ACCEPTED and not milestone closure.

## Method (independence statement)

1. Re-hashed every pinned input from bytes (contract, driver, freeze module, freeze artifacts, RUN C contract/driver/WIDE_GRAMMARS, K2 driver/COVERAGE_STATE/RESIDUAL333/BASELINE_REPRODUCTION, R34 grammar, Models.bnt, R61 10/10 sources) with `Get-FileHash -Algorithm SHA256` (PowerShell) and `hashlib` (Python).
2. Byte-compared the frozen W1/W3 definitions and the 6 K2 grammar blocks against RUN C's pinned WIDE_GRAMMARS.md and the pinned K2 source lines with my own extraction code.
3. Independently re-derived the full 9.3.5 census (population derivation) with my OWN transcription of the census pipeline (span reconstruction from R61-parsed NiVertexMorphExtraData blocks, greedy walk, R34 grammar re-derivation + row agreement, r19/backtrack/shift classification, R21 probe), driving the PINNED K2 module functions and the PINNED R61 reader over the pinned Models.bnt bytes.
4. Executed the mandatory positive control: RUN C's known W1-fit spans (548296.nif bi=75) reconstructed from the corpus via R61, byte-verified against RUN C's recorded `unit` SHA-256s, then fed through RUN E's W1/W3 procedure (pinned `K2.parse_fixed`) AND through my own re-implementation of the frozen B4 unit typed from WIDE_GRAMMARS_325.md.
5. Re-executed W1/W3 and all u±2 NCs on all 325 population members myself (pinned K2 + own re-implementation) and compared row-by-row against the run's raw JSONL.
6. Re-evaluated the a-priori gate with my own classifier transcription; recomputed every reported exact binomial CI from the closed form; re-executed the 8 negative fixtures (my classifier + the driver's own `evaluate_gwide325` + comparison vs the recorded file) and the 6 manifest negative tests (own validator transcription); independently re-validated artifact_index.csv (every row re-hashed).
7. Full-read discipline: every RUN E package file read to EOF (see FULL_READ_LOG below); the RUN E driver (1739 lines) and freeze module (917 lines) read to EOF before any re-execution.

Exact commands (principal):
- `python C:\Users\User\AppData\Local\Temp\opencode\qc_rune_r1.py` -> `qc_rune_r1_results.json` (census re-derivation, positive control, full W1/W3+NC re-execution with row compare, gate + CI re-evaluation, manifest re-validation, self-audit scan, scope/payload scan)
- `python C:\Users\User\AppData\Local\Temp\opencode\qc_rune_r1_fixup.py` -> `qc_rune_r1_fixup.json` (K2 baseline pin re-verified against PIN_RESULTS.json; corrected fixture comparison)
- `python C:\Users\User\AppData\Local\Temp\opencode\qc_rune_r1_negtests.py` -> `qc_rune_r1_negtests.json` (6 manifest negative tests via my own validator)
- `Get-FileHash` / `Get-Content` / `Select-String` (PowerShell 5.1) for hash and raw-row checks.

---

## Q1. Contract + driver hashes; W1/W3 freeze VERBATIM vs RUN C — **PASS**

- CONTRACT.md SHA-256 = `da2843436e02d0148de8546e7e26a1a07afdb43699a61136dcbe09d705fdd7fd` — matches the expected pin. CONFIRMED.
- Driver `widerecord325_driver_r1.py` SHA-256 = `b06cb445cf12c5f25cd3f383f81a639ebeefc0380cb395c8635206d14aad2e3c` — matches the expected pin `b06cb445...aad2e3c`. CONFIRMED. Freeze module `freeze_wide325_r1.py` = `18e34478930f31ad30f27fcceac0ca356bf14a7637ec14038e87c96c8ec32e01` (matches PREREG_MARKER + report §18).
- Freeze artifacts re-hashed and matched vs PREREG_MARKER.txt: WIDE_GRAMMARS_325.md `4d3a943c...`, POPULATION_325.json `ab376009...`, SPLIT_SIDES_325.json `94700e94...`, NC_PROCEDURES_325.md `ac41397f...`, GATES_PREREGISTERED.md `1c963cb5...` (5/5).
- RUN C pins re-hashed from bytes: CONTRACT `404f73687913a5ee934ce123b6bd9588bc2427dfd7b73b2f217f1b21f6ff5f3e`, driver `b4fa818a7f7b42de565eb73837b1c10e368f021c3ab54f54146eb84cb499a714`, WIDE_GRAMMARS.md `3079ecabee7b95721668e24e4ff3845c11d76835d651379d81ac7ad2c0b8557e` (the "3079ecab pinned" claim — re-hashed by me, MATCH).
- W1/W3 definitions VERBATIM vs RUN C (my own byte-comparison, independent of the driver's check): W1 definition line, W3 definition line, invocation items 1 and 3 are BYTE-EXACT in both RUN C's WIDE_GRAMMARS.md and RUN E's WIDE_GRAMMARS_325.md; item 4 is byte-exact modulo the single declared run-local token substitution (`(NC_PROCEDURES.md)` -> `(NC_PROCEDURES_325.md)`); item 5 is the declared 325-specific replacement of RUN C's 269-specific item (documented in the freeze header). No rewording, no parameter changes found.
- 6/6 K2 blocks BYTE-EXACT: I extracted lines 79-83 (B1), 86 (B2), 100-103 (B3), 251-285 (B4), 288-320 (B5), 871-882 (B6) from the pinned K2 driver `morph_residual_deepdive_r1.py` and found each fenced block byte-exact in BOTH WIDE_GRAMMARS_325.md and RUN C's WIDE_GRAMMARS.md. 6/6 CONFIRMED.
- K2 baseline pins re-hashed: K2 driver `b7e4cd32...c595a`, COVERAGE_STATE `86c12fa7...b12fa4`, RESIDUAL333 `e936ed51...f0100`, BASELINE_REPRODUCTION `2e4014c9652df8adf6854b87c17388f9a5288c2c32dc757b34946320db46f1ca` (matches the pin recorded in RUN E's PIN_RESULTS.json and the contract's freeze anchor; my first scripted pass printed a 63-char "mismatch" that was MY OWN transcription typo — re-verified clean in qc_rune_r1_fixup.py). Models.bnt `c950a8c2...d3bee0`; R34 grammar `2c26ba86...a007e`; R61 sources 10/10 pins re-verified.

## Q2. THE MANDATORY POSITIVE CONTROL — **PASS: the known-positives FIT**

Executed exactly: I reconstructed the known-positive spans from the corpus via R61 (`PENifReader().parse_bytes` over the 548296.nif entry of pinned Models.bnt 9.3.5; block bi=75, NiVertexMorphExtraData, tag-split, spans, dp = s[2:], u = Wm−2 = 124, N = 801, Wm = 126), verified byte-identity of my reconstruction against RUN C's recorded `unit` hashes (SHA-256 of dp), then executed RUN E's W1 procedure = `K2.parse_fixed(dp, u, N, 32)` (the pinned module — the exact function the RUN E driver executes), AND my own independent re-implementation of the frozen B4 unit typed from WIDE_GRAMMARS_325.md, plus the frozen W3 window and the u±2 NC starts.

Results (primary two keys demanded by the QC instruction, plus all 12 of RUN C's 548296.nif bi=75 W1-fit keys for completeness):
- (548296.nif, 75, 32): dp SHA-256 `f41616aa...d9811d4` == RUN C unit (byte-identity CONFIRMED). W1 = `K2.parse_fixed(dp, 124, 801, 32)` -> ok=True, records=1, wp_pairs=1, bytes_consumed=130 — **FIT**, matching RUN C's recorded records=1/wp=1/130. My own B4 re-implementation: FIT, identical values, agrees with K2. W3 window first hit d=0 (RUN C: WINDOW_HIT_+0), records=1/wp=1; valid positions 17. NC W1 at u±2: NON-HIT both.
- (548296.nif, 75, 43): dp SHA-256 `574fcfa4...5a3d633` == RUN C unit. W1 -> FIT, records=1, wp_pairs=1, 130 B — matches RUN C exactly; my re-implementation agrees; W3 first hit d=0; NC u±2 NON-HIT.
- All 12 keys (si = 32,43,52,53,58,59,70,81,87,89,93,94): dp byte-identity 12/12 vs RUN C units; W1 FIT 12/12 via pinned K2 AND 12/12 via my re-implementation (K2 vs mine agree on all); records/wp_pairs/bytes_consumed equal RUN C's records in every row (si=70: records=2, wp=1, 260 B = L=386/dp_len=384, matches RUN C); W3 first-hit d=0 in 12/12 (superset relation intact); NC u±2 non-hits 24/24 trials.

Conclusion: RUN E's W1/W3 parse path demonstrably WORKS on known-positive input (byte-identical data, identical verdicts to RUN C). The ZERO_FITS result on the 325 is NOT an implementation artifact of the parser path. CONFIRMED.

## Q3. Raw re-derivation: counts, 0/325 + 0/650, side split, gate firing — **PASS**

- `01_RAW\WIDE325_SPAN_OUTCOMES.jsonl`: 650 rows exactly (325 x W1 + 325 x W3; 0 unparseable lines; 0 rows missing schema fields; 0 duplicate (span,grammar) rows). Claimed 325 x 2 grammars = 650 — CONFIRMED.
- `01_RAW\WIDE325_NC_TRIALS.jsonl`: 1,300 rows exactly (W1: 325 u_plus_2 + 325 u_minus_2; W3: 325 + 325; 0 duplicates; 0 missing fields). Claimed 1,300 — CONFIRMED.
- Fits recounted from the raw rows: W1 0/325, W3 0/325. NC hits recounted: W1 0/650, W3 0/650. My independent re-execution of W1/W3 + NCs on all 325 census-derived members (pinned K2 + my own re-implementation): fits {W1: 0, W3: 0}, NC hits {W1: 0, W3: 0} — IDENTICAL. Row-by-row comparison of my re-execution vs the file: 650/650 outcome rows match exactly on outcome, side, reason, bytes_consumed, extra.records, extra.wp_pairs (and for W3 also extra.offset / valid_positions / stride_ok_positions / window_positions); 1300/1300 NC rows match exactly on hit, reason, bytes_consumed, u2, denominator. 0 mismatches, 0 missing, 0 extra.
- Reason structure (corroboration): W1 positive trials all `STRIDE_MISMATCH` (325/325); W3 positive trials all `NO_WINDOW_HIT` (325/325); W1 NC trials 646 `STRIDE_MISMATCH` + 4 `IDX_GE_N_AT_*` (2x38, 1x42, 1x46); W3 NC all `NO_WINDOW_HIT`; no `INVALID_START_NONHIT` rows (u−2 >= 0 for all 325 members) — all reproduced by my re-execution.
- Side split: reproduces from seed `random.Random(20260906)` over the sorted 56-file list: side A = 28 files, side B = 28 files, side lists BYTE-IDENTICAL to SPLIT_SIDES_325.json; spans side A = 96 / side B = 229 (sums to 325; matches the frozen pop325_side_A/B lists member-for-member; 551564.nif's 84 spans land on side B). Claim A 96 / B 229 — CONFIRMED.
- ZERO_FITS verdicts fire correctly per the frozen gates: fits 0 < 5 (G-WIDE325 threshold), NC denominator = 650 > 0; my own transcription of the a-priori predicate returns NON_PASS / ZERO_FITS for both grammars — identical to WIDE325_RESULTS.json (`detail = {full_325_fits: 0, threshold: 5}`). Vacuous-case protection VERIFIED in code and by counter-check: ZERO_FITS is evaluated BEFORE any separation comparison (driver `evaluate_gwide325`; my transcription; fixture 1), so the vacuous `0 >= 5x0` conjunction can never produce a PASS; the 0/650 NC rate is never compared against 0 fits as a pass path.
- Exact binomial CIs re-derived from the closed form (k=0 upper bound = 1 − 0.025^(1/n)): n=325 -> 0.011286; n=650 -> 0.005659; n=96 -> 0.037697; n=192 -> 0.019030; n=229 -> 0.01598; n=458 -> 0.008022 — 8/8 reported CIs MATCH (W1/W3 full-325, full-NC, side A, side B, side A-NC, side B-NC).

## Q4. G-CENSUS + the 325-key list — **PASS**

My independent census re-derivation (own pipeline transcription; pinned K2 classification functions; pinned R61; pinned Models.bnt bytes):
- Parse closure 100% (parse_fail 0; 5,596 entries, 5,596 unique names).
- Anchors — mine vs BASELINE_CENSUS_REPRODUCTION.json: walk 10,274 / 6,167 / 65,050 / 143,874; corpus grammars g1 132 / g2 1,547 / var 3,186 / mscan_any 3,705; rr 2,427 / var 2,093 / nofit 334 = 62 alt + 272 none; residual neither 3,438 / backtrack 3,105 / shift 114 / shift_only 8 / unknown325 325 / r21_unknown 333 / r19_only 669; 56 files; top file 551564.nif x84; probe 41 / 0.4197 / 0.8096; blocks 354 / 334; row agreement 6,167/6,167 (0 disagreements). ALL EQUAL — 0 anchor diffs. CONFIRMED.
- The 325-key list: my census-derived unknown-325 keys == POPULATION_325.json `pop325_keys` (325 EXACT, sorted set equality); my 333 == the pinned K2 RESIDUAL333_SPANS.txt headers (333) == the frozen `r21_unknown_333_keys`; my 8 shift-only == the frozen `shift_only_8_keys`; 325 + 8 disjoint union == 333 EXACT; per-key byte identity: dp SHA-256 match 325/325 and N/tag/Wm/L/u/dp_len field match 325/325 — every tested population member is byte-identical to the census-derived span. K2 COVERAGE_STATE.json canon string "325 (of 333 R21-unknown; 56 files; 551564 x84)" verified verbatim.

## Q5. Fixtures 8/8 + manifest validation (21+11) + driver self-audit — **PASS**

- Eight negative fixtures fail-closed, verified THREE ways: (a) my own gate-classifier transcription on my own synthetic constructions; (b) re-execution via the driver's own `evaluate_gwide325` on the same constructions; (c) vs NEGATIVE_FIXTURES_GEXEC.json. All three agree with the frozen expectations: 1 ZERO_FITS, 2 EMPTY_GROUP, 3 ONLY_PREVIOUSLY_SELECTED (the d8 integrity guard fires), 4 DUPLICATE_KEYS, 5 DENOMINATOR_MISMATCH (63 trials vs 32x2=64), 6 CORRUPTED_RECORD, 7 MALFORMED_MANIFEST_ROW, 8 MISSING_INPUT_FILE. 8/8 CONFIRMED. (My first scripted comparison reported 6 "failures" — a dict-vs-string bug in MY comparison code; corrected in qc_rune_r1_fixup.py: 8/8.)
- Manifest: my independent re-validation of artifact_index.csv (own validator; every ordinary row path-shape-checked, deduplicated, re-hashed; every external row kind/era/path re-hashed): 21 ordinary rows + 11 external rows, 0 findings; all 23 files on disk accounted for (21 rows + the 2 documented exclusions artifact_index.csv and 05_ANALYSIS/MANIFEST_VALIDATION.json); 0 manifest rows missing on disk. Claims 21+11 — CONFIRMED. All six manifest negative tests (a-f) fail-closed under MY OWN validator transcription with the same finding classes recorded in MANIFEST_NEGATIVE_TESTS.json (a/b MALFORMED_MANIFEST_ROW; c MISSING_FILE; d MALFORMED_HASH; e UNSUPPORTED_PATH_SHAPE; f HASH_MISMATCH + DUPLICATE_ROW).
- Driver self-audit: my own scan (string literals stripped) counts 46 `len(` occurrences — equal to SELF_AUDIT.txt's 46 — and 0 forbidden size-derived validation/fit assignments; all fit/NC counts in `evaluate_gwide325` and in s4_results are counter increments over executed records (verified by reading the driver to EOF; the `len()` uses are denominators, transparency counts, loop bounds and consumed-length computations). "Zero size-derived" — CONFIRMED.

## Q6. Scope: originals untouched; zero payloads; nothing outside the run dir — **PASS**

- Originals re-hashed and intact: Models.bnt `c950a8c2...` (mtime 2008-09-17 — untouched); K2 driver/COVERAGE_STATE/RESIDUAL333/BASELINE_REPRODUCTION; RUN C contract/driver/WIDE_GRAMMARS; R34 grammar; R61 10/10 sources — all match their pins. Source-tree mtimes (K2 driver 2026-09-06 03:42, RUN C driver 2026-09-06 10:07, R61 reader 2026-08-24) all PREDATE the 19:05 run.
- Zero payloads: all package outputs are text (identifiers, outcomes, rejection reasons, byte counts, 64-char SHA-256 identities); my hex-run scan found only the synthetic `a*64` negative-test tokens in MANIFEST_NEGATIVE_TESTS.json / MANIFEST_VALIDATION.json (expected test content, not payload data); no binary files in the package.
- Nothing outside the run dir: 23 files on disk, all inside the run dir, all accounted for; no HARD_STOP_EVIDENCE.json (consistent with RUN_STATUS COMPLETED); the R61 source tree's `__pycache__` predates the run (2026-08-25/29 mtimes; the driver and freeze module set `sys.dont_write_bytecode = True`); the driver's every writer is behind a `_guard` run-dir prefix check (verified by full read). My own QC wrote only to the temp dir and this one file.

## Q7. Report honesty — **PASS**

Every number in 06_REPORT/00_FINAL_REPORT.md re-derived and matched my results: gate results W1/W3 NON_PASS ZERO_FITS; full-325 fits 0/325 rate 0.0 CI [0.0, 0.011286]; NC 0/650 rate 0.0 CI [0.0, 0.005659]; per-side fits A=0 B=0 (members 96/229; NC denominators 192/458); file-blocks-with-fits 0; X=0 -> residual 325 -> 325; rr coverage 2,171/2,427 = 89.45% stands (2093+65+13 = 2171, arithmetic verified; the residual-325 correctly stated as OUTSIDE the 2427 rr denominator); combined consumed 2171; split 28/28 files, spans 96/229; fixtures 8/8; manifest negative tests 6/6; census anchors and row agreement 6,167/6,167; §18 provenance hashes (driver b06cb445..., freeze module 18e34478..., K2 b7e4cd32...) all match the actual bytes.
The ZERO_FITS outcome is reported PLAINLY as the pre-registered honest bound ("NO - the wide-record class is absent/rare in the 325 residual ... ZERO_FITS is a VALID outcome"), matching the contract's §5 REPORTING clause and frozen d6 — no overclaim, no failure-dressing. No semantic or H7-based claims anywhere in the package (standing sentence present in every output; RUNTIME_SEMANTICS explicitly NOT_TESTED; the retrospective-NOT-unseen disclosure is present). The concentration labels NOT_APPLICABLE_ZERO_FITS are justified: zero fits => empty per-side/per-file/per-family distributions (reported), so CONCENTRATED_SIDE/FAMILY cannot hold; the label is the correct disclosure for the zero case per the frozen d8 ("if n_fits == 0: NOT_APPLICABLE_ZERO_FITS").
Cosmetic-only note: §5/6 renders "95%% CI" (see DISCREPANCIES item 1) — no numeric impact.

## Q8. COVERAGE_DELTA.json no-change state — **PASS**

- standing_total 2171 = 2093 (canon var-k, BYTE_MATCH) + 65 (RUN A, RETROSPECTIVE_VALIDATED) + 13 (RUN C, RETROSPECTIVE_VALIDATED with the family-concentration bounds) — arithmetic verified; "2171/2427 = 89.45% (rr coverage stands UNCHANGED this run)" is correct and correctly qualified.
- this_run_additions: X_spans = 0, X_keys = [], per_grammar W1/W3 gate_verdict NON_PASS / non_pass_class ZERO_FITS / consumed_spans 0 / counts_toward_coverage false / status "EXCLUDED from coverage (gate NON_PASS; the K2 OC-rejection precedent)" — exactly the frozen d5 rule (consumed spans of non-pass grammars recorded but excluded from every coverage number; here zero anyway).
- residual_325: before 325 / consumed_this_run 0 / after 325 — correct.
- combined_spans_consumed 2171; out_of_scope block (H7 NO claims, W2 not tested, 2003 era out of scope, post-hoc NONE) consistent with the contract and frozen d6/d7.

---

## DISCREPANCIES

Material claim discrepancies (run claims vs my independent re-derivation): **NONE (0)**. Every audited count, rate, CI, verdict, key list, hash and coverage number in the package reproduced exactly under independent execution from original bytes.

Non-material observations (P2; none affect any gate verdict, count, or coverage number):

1. **P2 — cosmetic "%%" literal in the FINAL_REPORT body.** Source: 06_REPORT/00_FINAL_REPORT.md §5/6 ("exact binomial (Clopper-Pearson) 95%% CI"); cause: driver line 1510 writes a non-%-formatted literal containing a doubled percent. Effect: cosmetic rendering only; no number or claim is affected. Fix: single "%" at publication time (PE-MASTER decision; a one-character report edit in a future correction pass). Revalidation predicate: re-read the rendered line.
2. **P2 — NC_EMPTY_DENOMINATOR is an unreachable defensive branch in `evaluate_gwide325`.** Source: driver lines 686-693 — the DENOMINATOR_MISMATCH guard (`nc_den != 2*n_members`) fires first; `nc_den == 0` with members > 0 is arithmetically impossible under that guard, and zero members fires EMPTY_GROUP earlier. Effect: none on fail-closed behavior (a zero/incorrect NC denominator still fails-closed via DENOMINATOR_MISMATCH/EMPTY_GROUP) and none on this run's ZERO_FITS verdicts (real denominators held at 650). Fix (optional, executor-side): document or remove the dead branch. Revalidation predicate: constructed unit cases (fits>=5 + nc_den=0 is unreachable; mismatch fires).
3. **P2 — BASE_SHA token unverifiable in this workspace.** Source: CONTRACT.md line 6 (`BASE_SHA cd1ee07f...`) and report §2/§11. D:\Eudoria_Reconstruction is not a git repository and the D:\TESTAI repository has zero commits, so the token cannot be re-derived here. Effect: none on run integrity — the executor's "no repo writes / not committed" statements are consistent with the workspace state (there is no repository to write), and no commit exists to inspect. Disposition: the token remains parent-contract metadata; PE-MASTER owns the repo mapping. Revalidation predicate: parent supplies the repository path containing cd1ee07f.

QC-side disclosure (defects in MY QC tooling, fixed in-run; they never touched the run package):
- My first scripted pass reported a pin "mismatch" for K2_BASELINE_REPRODUCTION — caused by my own 63-char typo of the 64-char pinned hash; re-verified clean (file hash `2e4014c9652df8adf6854b87c17388f9a5288c2c32dc757b34946320db46f1ca` == pin recorded in PIN_RESULTS.json == the contract's freeze anchor).
- My first scripted fixture comparison reported 6 "failures" — a dict-vs-string comparison bug in my own code; corrected comparison shows 8/8 fail-closed (mine == driver's function == package record == frozen expectation).

## NOT_CHECKED (scope honesty)

- W2, H6/H7/H8 mechanisms, the 2003-era corpus, and any post-hoc probe — out of this run's contract scope (frozen d6/d7); not executed, not claimed.
- R61 parser internal correctness — accepted as the pinned frozen baseline (10/10 SHA pins re-verified); its parse path was exercised end-to-end by my census re-derivation and the positive control, but its algorithms were not re-audited here.
- RUN C's and K2's internal run histories — input packages here; only their pinned artifacts were re-hashed, their WIDE_GRAMMARS.md byte-compared, and RUN C's known-positive rows re-derived.
- The d8 ONLY_PREVIOUSLY_SELECTED guard's placement between ZERO_FITS and NC_INSUFFICIENT_SEPARATION (driver docstring) vs the frozen d3 order listing it under d8 — read as documented (inert on real data; all 325 members carry previously_selected=False; verified via fixture 3); no behavioral difference on this run's data.
- Commit/remote state — nothing committed (consistent with the QC brief); nothing to inspect; see DISCREPANCIES item 3.

## FULL_READ_LOG

RUN E package (all to EOF): CONTRACT.md; widerecord325_driver_r1.py (1739/1739 lines); freeze_wide325_r1.py (917/917 lines); WIDE_GRAMMARS_325.md; GATES_PREREGISTERED.md; NC_PROCEDURES_325.md; PREREG_MARKER.txt; PIN_RESULTS.json; POPULATION_325.json (all 325 keys + per_key parsed); SPLIT_SIDES_325.json; 01_RAW: WIDE325_SPAN_OUTCOMES.jsonl (650 rows), WIDE325_NC_TRIALS.jsonl (1300 rows), NEGATIVE_FIXTURES_GEXEC.json, MANIFEST_NEGATIVE_TESTS.json, SELF_AUDIT.txt; 05_ANALYSIS: BASELINE_CENSUS_REPRODUCTION.json, WIDE325_RESULTS.json, COVERAGE_DELTA.json, MANIFEST_VALIDATION.json; 06_REPORT: 00_FINAL_REPORT.md, HANDOFF.md; STAGE_ACCEPTANCE_GATES.csv; artifact_index.csv (all 32 rows).
Inputs (read-only): RUN C WIDE_GRAMMARS.md (EOF), POPULATION_269.json (structure + keys), WIDE_SPAN_OUTCOMES.jsonl (FIT rows), driver spot-checks (exec_w1/unit convention, lines 785-790, 1283-1295); K2 COVERAGE_STATE.json + BASELINE_REPRODUCTION.json (EOF), RESIDUAL333_SPANS.txt (header format + 333-header count), driver signature spots (lines 79-103, 174-320, 1543); R34 REAL_SPARSE_GRAMMAR.json (per_span rows consumed by my census row-agreement check); R61 SHA256_SOURCE.json + pe_nif_reader.py (interface + pins).

## INPUT AND OUTPUT HASHES (principal)

- Inputs: CONTRACT.md da284343...dd7fd; driver b06cb445...aad2e3c; freeze module 18e34478...e01; Models.bnt c950a8c2...d3bee0; K2 driver b7e4cd32...c595a; K2 COVERAGE_STATE 86c12fa7...b12fa4; K2 RESIDUAL333 e936ed51...f0100; K2 BASELINE_REPRODUCTION 2e4014c9...f1ca; RUN C contract 404f7368...5f3e; RUN C driver b4fa818a...a714; RUN C WIDE_GRAMMARS 3079ecab...57e; R34 grammar 2c26ba86...007e.
- Re-verified outputs (vs artifact_index.csv rows, all matched): WIDE325_SPAN_OUTCOMES.jsonl 72b6e54e...; WIDE325_NC_TRIALS.jsonl 214220df...; WIDE325_RESULTS.json fd89f7a8...; BASELINE_CENSUS_REPRODUCTION.json b4f6f0b9...; COVERAGE_DELTA.json 2e760d93...; NEGATIVE_FIXTURES_GEXEC.json 77b51f96...; SELF_AUDIT.txt c18d777b...; 00_FINAL_REPORT.md 96abefac... (plus the remaining rows — 0 findings).
- QC artifacts (temp, outside the package): qc_rune_r1.py / qc_rune_r1_results.json; qc_rune_r1_fixup.py / qc_rune_r1_fixup.json; qc_rune_r1_negtests.py / qc_rune_r1_negtests.json.

## SUMMARY TABLE

| Item | Verdict | Key numbers (mine) |
|---|---|---|
| Q1 pins + verbatim | PASS | 12 pins + R61 10/10 matched; W1/W3 items 1/3/4 byte-exact vs RUN C; 6/6 K2 blocks; 3079ecab re-hashed |
| Q2 positive control | PASS | known-positives FIT 12/12 (K2 + my re-impl); dp byte-identity 12/12 vs RUN C units; W3 d=0 12/12 |
| Q3 counts + gates | PASS | 650 + 1300 rows; fits 0/325 + 0/325; NC 0/650 + 0/650; split 96/229 (28/28 files); ZERO_FITS correct; 8/8 CIs match |
| Q4 census | PASS | all anchors equal (0 diffs); 333 pinned dump == mine; 325+8=333 EXACT; dp hashes 325/325 |
| Q5 fixtures/manifest/self-audit | PASS | 8/8 fail-closed (3-way); manifest 21+11, 0 findings; 46 len() all clean |
| Q6 scope | PASS | originals intact (hashes + mtimes); zero payloads; 23 files all in-run |
| Q7 report honesty | PASS | every number matched; ZERO_FITS plainly the honest bound; no overclaim/semantic/H7 claims |
| Q8 coverage delta | PASS | 2171/2427 = 89.45% stands; X=0; 325 -> 325; exclusion per d5 correct |

Material discrepancies: 0. Non-material P2 observations: 3 (listed above). The package's ZERO_FITS outcome stands as an honest, independently re-derived bound: the frozen W1/W3 wide-record grammars do not consume any of the 325 R21-unknown residual spans (0/325 each, 0/650 matched-NC trials each), with the parse path proven working on known-positive input.

QC_VERDICT = QC_PASS
