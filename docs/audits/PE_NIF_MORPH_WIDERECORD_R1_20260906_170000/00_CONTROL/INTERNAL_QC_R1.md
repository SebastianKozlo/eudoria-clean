# INTERNAL_QC_R1 — RUN C: PE_NIF_MORPH_WIDERECORD_R1_20260906_170000

- QC RUN_ID: PE_NIF_MORPH_WIDERECORD_QC_R1_20260906 (fresh independent internal-QC context; did NOT execute RUN C)
- PARENT: PE-MASTER loop bd17344b-a054-4cf4-be8d-5f0b250e8509 (iteration 3) | MILESTONE: EU935-M1
- MODE: INTERNAL_QC, independent re-derivation from disk; READ-ONLY everywhere except this one file
- RUN under QC: PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 (RUN_CLASS LOAD_BEARING; executed 2026-09-06 ~10:07-10:08, NOT committed)
- QC method note: every number below was re-derived by the QC context with its own parsers/scripts (paths in `C:\Users\User\AppData\Local\Temp\opencode\qc_runc_*.py`), NOT by re-running the run driver. Grammar verdicts were independently re-executed on the raw K2 dump bytes with the QC's own transcription of the frozen blocks.
- Evidence status vocabulary: CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED. Claim status, gate result and report-honesty are kept separate.

## Q1. Contract hash — PASS

- Command: `Get-FileHash -Algorithm SHA256 00_CONTROL\CONTRACT.md`
- Got: `404f73687913a5ee934ce123b6bd9588bc2427dfd7b73b2f217f1b21f6ff5f3e` — equals the expected SHA256. CONFIRMED.
- Contract read in full (48 lines). RUN A package path and K2 package path as cited in the contract exist and were pinned (see Q2/Q8).

## Q2. Freeze discipline — PASS (with one report-level consequence recorded under D1)

(a) Freeze artifacts present in 00_CONTROL BEFORE outputs, substantiated by the marker's hash list (not mtimes):
- PREREG_MARKER.txt (own sha256 `78bfc31e2d6513d4fc9b15a91a0447a6d2fdbf73a2d600e858b82e92b67be7f0`, matching PIN_RESULTS.json) records:
  - WIDE_GRAMMARS.md `3079ecabee7b95721668e24e4ff3845c11d76835d651379d81ac7ad2c0b8557e` — re-hashed by QC: MATCH
  - POPULATION_269.json `17b69675af9db80e31ecb2ae61a675c89cbfb160b2cd0493951859407910d2f0` — MATCH
  - SPLIT_SIDES_269.json `cf49d0fa6a7ee169c335f368025125e0a0a23dcd08e15a1ac5684393f2dde49f` — MATCH
  - NC_PROCEDURES.md `2c7ee0013a07a3ddcca70f39f3f4537247e8b9ab11ad11f03fe40855400e2fa2` — MATCH
  - GATES_PREREGISTERED.md `72ab73393c4053690d1485bb760c62f88f21ad9ac78c1b0d3f9195b41d3ffcbc` — MATCH
  - 5/5 freeze files byte-identical to the marker's records; W1/W2/W3 definitions verbatim from CONTRACT §3; gates verbatim from CONTRACT §4 (+ frozen operationalization d1-d7).
- The driver (S0, L396-429) re-verified every freeze hash against the marker and byte-verified the 6 grammar blocks vs the pinned K2 source before any test; the run completed (no hard stop), and the QC re-verified all of the above independently.
- Freeze script `freeze_wide_r1.py` (read in full, 454 lines) derives the population ONLY from pinned artifacts (K2 NOFIT334 dump + RUN A RETRO_SPAN_OUTCOMES); it never opens Models.bnt — consistent with the marker's "no corpus parse at freeze time".

(b) Independent re-derivation of 334 - 65 = 269 (QC's own code):
- K2 `01_RAW\NOFIT334_SPANS.txt` re-hashed: `8bb6556b166df656631af168031e58518b3147fe962d5815ca4e19009e0f605d` (pin match). QC's own regex parser: **334 span headers, 334 unique keys** — equals freeze `P1_nofit334_keys`.
- RUN A `01_RAW\RETRO_SPAN_OUTCOMES.jsonl` re-hashed: `6b6c7fa98d5ad0682e8947d54a00cf370a271b2d16cf5b4b1430b5d99a08f8cb` (equals the ordinary-row pin in RUN A's artifact_index.csv, whose own sha `66baea67efbf57a773ba04c2b59c6a8aea6620170c4444de65897f8fa5223f3d` matches PIN_RESULTS). QC's own JSONL parse (993 rows; grammar-filtered): **H5a FIT = 39, H5c2 FIT = 26, overlap 0, union 65** — equals the freeze subtraction lists exactly. (H7 FIT=74 rows exist in RUN A's file and were correctly ignored per contract.)
- **334 - 65 = 269 EXACT**; QC's derived 269-key set == freeze `pop269_keys` (set equality; 62 files).
- Split re-derivation: `random.Random(20260906)` shuffle over the sorted 62-file list → side A 31 / side B 31 files; spans 112 / 157; disjoint; family integrity — **identical to SPLIT_SIDES_269.json** (both file lists and both span lists set-equal).
- Timeline corroboration (mtimes, informational only): freeze 09:54:15, driver 10:07:19, outputs 10:07:51-10:08:15; RUN A completed 09:26-09:38 — freeze-after-RUN-A ordering consistent. The ID timestamps (140500/170000) are identifiers, not wall-clock execution times — no finding.

## Q3. Driver audit — PASS

- Driver sha256: `b4fa818a7f7b42de565eb73837b1c10e368f021c3ab54f54146eb84cb499a714` — equals the expected pin AND PIN_RESULTS.json AND report §18 AND the manifest row. Driver read in FULL (2,161 lines, chunks).
- Size-derived validation assignments: QC's own scan (strings stripped to STR, both quote styles): **120 `len(` occurrences — equals SELF_AUDIT.txt's "120 classified"; 0 forbidden patterns**. All fit/hit counters (`full_fits`, `nc_hits_full`, `unit_fits_B`, `member_fits_B`, `fits_A`, `ufits_all`, `unit_fits_B_t`) are counter increments inside per-record loops; `len()` appears only as denominators, transparency counts, loop bounds, header arithmetic and the coverage-count `x = len(x_keys)` (a count of per-record-executed FIT keys, not a group-size validation). CONFIRMED no size-derived validation.
- G-WIDE conjunction in code (`evaluate_gwide`, L898-1041) vs contract §4 — all SIX components present and ordered per frozen d3, fail-closed:
  1. full-269 fits >= 10 → `ZERO_FITS` (L981)
  2. full-269 rate >= 5x matched-NC rate → `NC_INSUFFICIENT_SEPARATION` (L988)
  3. NC denominator > 0 (both full and held-out per d2) → `NC_EMPTY_DENOMINATOR` (L969)
  4. held-out units >= 30 → `INSUFFICIENT_TRIALS` (L973)
  5. held-out fits >= 10 → `HETEROGENEOUS_SPLIT` (L1003)
  6. held-out rate >= 5x held-out-side matched-NC rate → `HETEROGENEOUS_SPLIT` (L1003, with BOTH numbers reported per d3)
  Plus the preceding fail-closed classes CORRUPTED_RECORD / DUPLICATE_ACROSS_SIDES / EMPTY_GROUP / DENOMINATOR_MISMATCH — exactly the frozen d3 order. Full-269 components MEMBER-level (269 spans; NC 538), held-out UNIT-level side B (d1) — implemented as specified (mA/mB unit-side filters; 4 split-family members excluded from side A, counted once on first-member side B).
- Eight fixtures (`NEGATIVE_FIXTURES_GEXEC.json`, re-read by QC): **8/8 fail-closed with explicit non-pass classes** — F1 ZERO_FITS, F2 EMPTY_GROUP, F3 HETEROGENEOUS_SPLIT (full passes / held-out fails, both numbers reported), F4 DUPLICATE_ACROSS_SIDES, F5 DENOMINATOR_MISMATCH (63 vs 64), F6 CORRUPTED_RECORD, F7 MALFORMED_MANIFEST_ROW, F8 MISSING_INPUT_FILE. `all_eight_fail_closed: true`, `gexec_verdict: PASS`.
- Frozen grammar blocks: QC's own byte-extraction of B1-B6 (lines 79-83, 86, 100-103, 251-285, 288-320, 871-882) from the pinned K2 driver (re-hashed `b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a`): **6/6 byte-exact** vs WIDE_GRAMMARS.md code fences. The executed grammars are the pinned K2 module's functions (imported at runtime) — identical algorithms to the QC's independent transcription used in Q4.

## Q4. Raw re-derivation (01_RAW) — PASS (all numbers CONFIRMED, including by independent re-execution)

Row counts (QC's own JSONL parsers):
- `WIDE_SPAN_OUTCOMES.jsonl`: **807 rows** = 269 spans x 3 grammars; every span key ∈ the frozen 269 (0 off-population rows); per-row `result_class: RETROSPECTIVE_VALIDATION`.
- `WIDE_NC_TRIALS.jsonl`: **2,556 rows** = 1,614 span-level (269x2x3 = 538 per grammar) + 942 unit-level (157x2x3 = 314 per grammar); explicit denominators `spans_x_2` / `units_x_2` on every row.

Re-derived numbers (from raw rows, then INDEPENDENTLY re-executed on the K2 dump bytes — see (h) below):
- (b) **W1 full: 12 FIT / 269, rate 0.044610**; NC span-level **0/538** (rate 0.0).
- (c) **W3 full: 13 FIT / 269** (rate 0.048327); **W1 ⊆ W3 with 12 shared**; W3\W1 = `548808.nif bi=164 si=129`.
- (d) **W2: 0 FIT / 269** vs NC span-level **5/538** (rate 0.009294); W2 unit-level NC 2/314 (rate 0.006369).
- (e) Side split: **side A 0 FITs (W1 and W3 both), side B 12 (W1) / 13 (W3) FITs; side B units = 157** (265 total dp-sha units; side A 108; 4 split-family units counted on first-member side B; NC unit denominator 314).
- (f) Family concentration (QC verified the span keys itself): the 13 fitted spans are exactly `548296.nif bi=75 si in {32,43,52,53,58,59,70,81,87,89,93,94}` (12 spans, one file+block) plus `548808.nif bi=164 si=129` — **12 of 13 in 548296.nif block 75**; union of all grammars = 13 unique spans (W1∩W2=0, W1∩W3=12, W2∩W3=0 — matches `grammar_overlaps`).
- (g) Exact binomial CI: QC implemented Clopper-Pearson independently via the regularized incomplete beta function + bisection (a DIFFERENT algorithm than the driver's CDF-sum bisection): **W1 full 12/269 → [0.02326, 0.076627]** — equals the recorded `[0.02326, 0.076627]` (the task's [0.0233, 0.0766] is its 4-dp rounding). ALL 11 recorded CIs match the QC computation to 6 dp: W1 NC 0/538 [0.0, 0.006833]; W3 full 13/269 [0.02598, 0.081223]; W2 full 0/269 [0.0, 0.01362]; W2 NC 5/538 [0.003024, 0.021554]; W1 held-out 12/157 [0.040117, 0.129707]; W3 held-out 13/157 [0.044826, 0.137433]; W2 held-out 0/157 [0.0, 0.023222]; held-out NC 0/314 [0.0, 0.011679]; W2 held-out NC 2/314 [0.000772, 0.022818]; side A 0/108 [0.0, 0.03358].
- (h) INDEPENDENT RE-EXECUTION (counter-check by execution, not re-running the driver): QC re-parsed the K2 NOFIT334 dump (dp hex per span; 323/334 spans have full payloads, hex_cap 2048) and executed its own transcription of the frozen W1/W2/W3 + NC predicates on the actual bytes:
  - **807/807 outcome verdicts agree with WIDE_SPAN_OUTCOMES.jsonl (0 mismatches)**; my W1 fits = 12, W2 = 0, W3 = 13, W1 ⊆ W3 — identical key sets.
  - **2,556/2,556 NC trial verdicts agree (0 mismatches)**; my span-level hits W1 0/538, W2 5/538, W3 0/538; my unit-level (side-B unit representatives, first-member-in-sorted-order, incl. all 157 reps) W1 0/314, W2 2/314, W3 0/314.
  - The 11 spans with truncated hex (dp_len > 2048; 11 of them in the 269) are proven NOFIT independently: W1 — stride arithmetic on the FULL dp_len: `(dp_len - u) % 130 != 0` for all 11; W2 — recorded+re-executed failure positions (40..1400; +134 max record probe <= cap) all inside the dumped prefix; W3 — for the 6 spans with no stride-candidate offset in the +/-64/step-4 window on full dp_len (arithmetically no window position can even start), and for the 5 remaining stride candidates a record-level failure (IDX_GE_N / UNCLEAN_FLOAT) inside the prefix. So ALL 269 spans' verdicts are independently proven, not just the 258 full-payload ones.
- Driver gate re-evaluation from raw rows: W1 PASS (12>=10; 0.04461 >= 5x0; 538>0; 157>=30; 12>=10; 0.076433 >= 5x0), W2 NON_PASS ZERO_FITS (0<10; per d3 ZERO_FITS precedes the also-failing separation), W3 PASS (13/269; 13>=10) — matches STAGE_ACCEPTANCE_GATES.csv and WIDE_RESULTS.json.

## Q5. G-CENSUS (BASELINE_CENSUS_REPRODUCTION.json) — PASS

- Artifact census (re-read): walk 10,274/6,167/65,050/143,874; rr_state rr 2,427 / var 2,093 / nofit 334 = 62 alt + 272 none; corpus_grammars g1 132 / g2 1,547 / var 3,186 / mscan_any 3,705; residual neither 3,438 / backtrack 3,105 / shift 114 / shift_only 8 / **unknown325 = 325** / r21_unknown 333 / 56 files / top 551564x84; r21_probe 41 / 0.4197 / 0.8096; blocks 354 / 334; row_agreement [6167, 6167, 0]; `census_exact: true` (26/26 checks pass).
- QC cross-check vs the PINNED K2 baseline (`05_ANALYSIS\BASELINE_REPRODUCTION.json`, re-hashed `2e4014c9652df8adf6854b87c17388f9a5288c2c32dc757b34946320db46f1ca` — pin match): every K2 value equals the RUN C reproduction (walk incl. `exact: true` semantic, r34_state, corpus, residual, r21_probe, morph_blocks/blocks_with_tag). The driver's K2_EXPECT_* anchors equal K2's own recorded baseline.
- RUN A removals: pinned FIT keys 39 + 26 (QC re-derived from RUN A raw — see Q2) reproduce under the driver's re-execution (`H5a_reexecuted_FIT_keys: 39`, `H5c2_reexecuted_FIT_keys: 26`, hard stop armed on mismatch; run completed) AND equal K2's HYPOTHESIS_RESULTS H5a / H5c2_idx_lt_0x8000 fit lists (hard stop armed). Union 65; **334 - 65 = 269 EXACT**; `pop269: 269`.
- Note (NOT_CHECKED): the QC did not re-execute the full 5,596-entry corpus census itself; it is corroborated by the pinned-anchor equality above, the driver's fail-closed checks, and the QC's independent re-derivation of the 269 from pinned dumps.

## Q6. COVERAGE_DELTA.json — PARTIAL PASS (arithmetic and labels CONFIRMED; concentration disclosure ABSENT → D3)

- Arithmetic: **2,093 + 65 + 13 = 2,171**; 2,171/2,427 = 89.452% → recorded `2171/2427 (89.45%)` ✓; remaining no-fit **269 - 13 = 256** ✓ (`remaining_nofit_note`).
- X definition per frozen d5: X = UNION of spans consumed by PASS grammars = W1(12) ∪ W3(13) = **13**; W2 consumed 0 and is excluded with the explicit K2 OC-precedent status. `X_keys` == the QC's independently derived fit-union set (13 keys, verified one by one).
- Labels: every added span carries RETROSPECTIVE_VALIDATION — per-row in WIDE_SPAN_OUTCOMES.jsonl AND `this_run_additions.status` = "RETROSPECTIVE_VALIDATED (RUN C; explicitly retrospective, NOT unseen)"; per-grammar statuses machine-readable.
- MISSING (D3): no concentration disclosure anywhere in the package (grep `concentrat` = 0 hits); the fact that 12 of the 13 X-spans are one file+block (548296.nif bi=75) is present only implicitly in X_keys.

## Q7. Manifest (artifact_index.csv per RUN B spec) — PASS

- Spec read (MANIFEST_SCHEMA_SPEC.md, sha `c1cc62a2952ced6e741745c0e3a6eebaffd41801ec1a334992c6d3c7d2d3c641` — matches manifest external row).
- QC re-ran the validation ITSELF (own RFC-4180 csv parser + own hashing): **21/21 ordinary rows OK** (exactly 3 fields; 64-hex sha; relative forward-slash path with no drive/absolute/.. shapes; file exists; physical hash equals the row — 0 findings, 0 duplicates) and **12/12 external rows OK** (kind=external_source; era in {PCG_9_3_5, 2003}; 64-hex; physical path exists; physical hash equals). Matches the claimed 21 ordinary + 12 external.
- Coverage completeness: package holds 23 files = 21 manifest rows + the 2 documented exclusions (artifact_index.csv self-hash; 05_ANALYSIS/MANIFEST_VALIDATION.json circular) — no unlisted files, no stale rows.
- Negative tests: `MANIFEST_VALIDATION.json` + `01_RAW\MANIFEST_NEGATIVE_TESTS.json` record the spec's a-f cases, **6/6 `gate_failed_as_required: true`, `all_six_fail_the_gate: true`**; the QC's own validator confirms each synthetic case fails (MALFORMED_MANIFEST_ROW / MISSING_FILE / MALFORMED_HASH / UNSUPPORTED_PATH_SHAPE / DUPLICATE_ROW(+HASH_MISMATCH)). `manifest_gate_verdict: PASS`.
- Anomaly recorded for D1 (not a gate failure): `pre_validation_in_memory.ordinary_rows = 19` — see Q9/D1; the final manifest itself is complete and correct for the 21 files on disk.

## Q8. Scope — PASS

- **Models.bnt current sha256 = `c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0`** (QC re-hash) — equals the pin. 5,596 unique entries asserted by the driver (S0), consistent with the corpus pin record.
- **R61 frozen parser untouched**: QC re-hashed all 10 `.py` files vs `SHA256_SOURCE.json` — **10/10 match**; directory structure unchanged (01_source contains exactly the 10 pinned .py + pre-existing __pycache__ with 3.12/3.13 .pyc — not from this run, which sets `sys.dont_write_bytecode = True`).
- **RUN A package unchanged**: 29/29 ordinary rows of RUN A's own artifact_index.csv re-hash OK (incl. RETRO_SPAN_OUTCOMES.jsonl 6b6c7fa9... and revalidate_driver_r1.py 02ecb955...); RUN A manifest sha `66baea67...` equals RUN C's pin. RUN A's unlisted files are its own documented structure (PRE_EDIT_P2 backups, BATCH_P2_PERSIST_RECORD, its MANIFEST_VALIDATION).
- **K2 package unchanged**: 18 files; the 5 RUN C-pinned files (driver b7e4cd32, NOFIT334 8bb6556b, COVERAGE_STATE 86c12fa7, HYPOTHESIS_RESULTS c08fb473, BASELINE_REPRODUCTION 2e4014c9) re-hash OK, plus RESIDUAL333_SPANS.txt e936ed51 and PRE_REGISTERED_HYPOTHESES.json 5bde44ac verified against RUN A's manifest pins — 7/18 files hash-verified against independent baselines; no RUN C artifacts present in the K2 dir. (Remaining K2 files have no independent baseline — its manifest is DEFECTIVE, a known pre-existing condition disclosed by the contract; QC found no sign of modification.)
- **Zero payloads in the run dir**: extensions present are only .csv/.md/.py/.json/.txt/.jsonl; total package 1.1 MB; no file > 2 MB; no hex dumps, no corpus bytes (identifiers, outcomes, reasons, byte counts only). CONFIRMED.
- Write-guard: driver `_guard()` hard-stops any write outside RUN; no HARD_STOP_EVIDENCE.json exists; no writes outside the run dir were detected by the QC's independent hash checks above.

## Q9. Report honesty (06_REPORT\00_FINAL_REPORT.md) — FAIL (numbers all verified; four required disclosures ABSENT)

Numbers: every quantitative statement in the report matches the QC's independent Q2-Q8 results — W1=PASS 12/269 rate 0.04461 CI [0.02326, 0.076627], NC 0/538 [0.0, 0.006833], held-out 12/157 units rate 0.076433 CI [0.040117, 0.129707], held-out NC 0/314 [0.0, 0.011679]; W2=NON_PASS ZERO_FITS 0/269, NC 5/538 rate 0.009294 CI [0.003024, 0.021554], held-out NC 2/314 rate 0.006369 CI [0.000772, 0.022818]; W3=PASS 13/269 rate 0.048327 CI [0.02598, 0.081223], held-out 13/157 rate 0.082803 CI [0.044826, 0.137433]; X=13, 2171/2427 (89.45%), remaining 256; split 62 files 31/31, spans 112/157; 8/8 fixtures; 6/6 manifest negative tests; census row agreement 6,167/6,167; generator hashes (b4fa818a driver, b7e4cd32 K2 module, 6/6 blocks) — ALL CONFIRMED.

Standing sentences: present in every control/analysis/report artifact (CONTRACT, WIDE_GRAMMARS, NC_PROCEDURES, GATES, PREREG_MARKER, PIN_RESULTS, BASELINE_CENSUS, WIDE_RESULTS, COVERAGE_DELTA, MANIFEST_VALIDATION, SELF_AUDIT, gates CSV header, final report, HANDOFF). Per-row result_class RETROSPECTIVE_VALIDATION on all 807 outcome rows. NO residual-325 claims (OUT OF SCOPE everywhere; the COVERAGE_DELTA residual_325 entry is the permitted status note referencing RUN A) and NO H7-based claims (H7 mentioned only inside the standing sentence as UNVALIDATED). CONFIRMED.

REQUIRED DISCLOSURES — ALL FOUR ABSENT (grep evidence: `typo|re-run|rerun` = 0 hits; `concentrat` = 0 hits):
1. **The in-driver pin typo + clean re-run is NOT disclosed anywhere in the package.** Independent on-disk corroboration of a prior execution attempt: `MANIFEST_VALIDATION.json pre_validation_in_memory.ordinary_rows = 19`, but a single clean pass has exactly 18 package files at that point (10 in 00_CONTROL + 5 in 01_RAW + 3 in 05_ANALYSIS + 0 in 06_REPORT; artifact_index.csv / MANIFEST_VALIDATION.json / STAGE_ACCEPTANCE_GATES.csv did not exist yet and the walk excludes them). 19 + 3 files written later (gates CSV, report, handoff) with one overwrite ⇒ 21 final rows — the arithmetic pins the 19th pre-validated file to a stale 06_REPORT file from an earlier execution attempt (overwritten by the clean run). The report §14 says "NONE encountered" (true only for the final pass) and never mentions the first attempt; if that attempt hard-stopped at S0, its HARD_STOP_EVIDENCE.json (written by `hard_stop_now` to 05_ANALYSIS) was removed outside the driver (no such file exists and no driver code removes it) — an undisclosed disposition either way. See D1.
2. **The 0-hit NC structural caveat is NOT stated.** W1/W3 PASS rests on "rate >= 5x the matched-NC rate" with NC = 0/538 and 0/314 (denominators > 0, hits = 0, rate 0.0): the separation conjunct is satisfied by ANY non-negative rate and could not have failed. Report §13 discloses only the denominator-0 vacuity guard ("0 >= 5x0 cannot pass"), which is a different case. See D2.
3. **The family concentration is NOT disclosed** (12 of the 13 X-spans in 548296.nif block 75; the 13th in 548808.nif block 164 — 2 of the 62 population files). See D3.
4. **Side A 0 fits is NOT disclosed.** All positive evidence sits on the held-out side B; side A: 0 fits, unit rate 0.000, CI [0.0, 0.03358], 108 units (machine-only in WIDE_RESULTS side_A_transparency). See D4.

Minor label gaps (P2, D5/D6): WIDE_NC_TRIALS.jsonl rows carry no result_class and the file carries no standing sentence (contract §1 "every output labeled with exactly one class" / §5 "the standing sentence in every artifact"); NEGATIVE_FIXTURES_GEXEC.json uses result_class "G-EXEC" (outside the frozen 4-class vocabulary); PIN_RESULTS.json / SELF_AUDIT.txt / MANIFEST_NEGATIVE_TESTS.json / MANIFEST_VALIDATION.json carry the standing sentence but no result_class label.

## Q10. Honest-bound check on the +13 claim — FLAGGED (under-bounded report)

- What the report DOES bound: the retrospective nature ("The 269 leg is RETROSPECTIVE by construction ... explicitly NOT 'unseen' evidence" §7/8); the d5 coverage-gating honesty; RUNTIME_SEMANTICS NOT_TESTED; no semantic claims. Those bounds are accurate.
- What the report does NOT bound: the +13 is gate-validated per the frozen conjunction, BUT it is (i) family-concentrated — 12/13 in one file+block, 2 of 62 files, so cross-file generality is NOT established; (ii) one-sided — all fits on side B, side A 0 fits (the "file-grouped retrospective homogeneity" phrase in the P0 answer is not contradicted by the frozen gate, which tests side B only, but the material asymmetry is nowhere stated); (iii) trivially separated — the NC had 0 hits, so the ">= 5x" component adds no discriminating evidence for W1/W3 (W2's NC DID produce 5/538 and 2/314 hits, which makes the W1/W3 0-hit structural point a necessary disclosure).
- Verdict: the report does not overclaim numbers (all numbers are gate-true and independently reproduced), but it UNDER-DISCLOSES the material limits of the +13 claim; the honest-bound requirement of the QC checklist is NOT met. Corrections D2-D4 (a few sentences in §3/§4/§7/§13) are sufficient; no re-run is required.

## DISCREPANCIES

**D1 (P1) — Undisclosed prior execution attempt (pin typo + clean re-run missing from the report).**
Source: 06_REPORT/00_FINAL_REPORT.md §14 ("NONE encountered") + whole package (grep `typo|re-run` = 0 hits); MANIFEST_VALIDATION.json `pre_validation_in_memory.ordinary_rows = 19` vs 18 files present in a single clean pass at that point (arithmetic above). Effect: the package's provenance narrative omits an execution attempt that preceded the clean run; a hard-stop evidence artifact, if one was created, was disposed of outside the driver without a record. Correction: report amendment (a CORRECTION run, no re-execution) disclosing the first attempt, the in-driver pin typo, the fix, the clean re-run, and the disposition of any stale/hard-stop artifacts; PE-MASTER should get the executor's statement of what exactly happened and what was deleted. Revalidation: the amended report contains the disclosure; a walk+count reconciliation of the package at pre-validation time is included; no other file changes.

**D2 (P1) — Missing disclosure: 0-hit NC structural caveat.**
Source: 06_REPORT/00_FINAL_REPORT.md §13 (only the denominator-0 vacuity guard); WIDE_RESULTS.json full_nc hits 0/538 and held_out_nc 0/314 for W1/W3. Effect: a reader can believe the ">= 5x separation" component actively discriminated for W1/W3, when with NC rate 0.0 it is satisfied by any non-negative rate (the gate is frozen and correctly applied; the evidence-strength caveat is the missing part). Correction: add the caveat sentence to §13 (and optionally to the W1/W3 lines in §4). Revalidation: report contains an explicit statement that the W1/W3 NC rates were 0.0 with non-zero denominators, so the separation conjunct was trivially satisfied.

**D3 (P1) — Missing disclosure: family concentration of the +13 (12/13 in 548296.nif block 75).**
Source: 06_REPORT/00_FINAL_REPORT.md §3/§4/§20 and COVERAGE_DELTA.json (grep `concentrat` = 0); the X_keys machine data shows it. Effect: the coverage delta reads as a broad +13; the fact that it is one family in one block (plus a single span elsewhere) — hence no cross-file generality — is not visible to a report reader. Correction: disclosure sentence in §3 and/or §7/8 with the exact 12+1 split and the "2 of 62 files" statement. Revalidation: report contains it.

**D4 (P1) — Missing disclosure: side A 0 fits.**
Source: 06_REPORT/00_FINAL_REPORT.md (no side-A fit statement anywhere); WIDE_RESULTS.json side_A_transparency (unit_fits 0, rate 0.0, CI [0.0, 0.03358], 108 units) — machine-only. Effect: the report's split description (§20: "spans 112/157; family integrity") and the P0 answer's "file-grouped retrospective homogeneity" do not reveal that the entire positive signal is on side B. Correction: add the side-A zero statement with its CI. Revalidation: report contains it.

**D5 (P2) — WIDE_NC_TRIALS.jsonl rows carry no result_class and the file has no standing sentence.**
Source: 01_RAW/WIDE_NC_TRIALS.jsonl (row schema: level/span/grammar/trial/u2/hit/reason/bytes_consumed/denominator). Contract §1 ("every output labeled with exactly one class") and §5 REPORTING ("the standing sentence in every artifact"). Effect: minor contract-compliance gap on a required raw output; no numeric consequence (the QC re-derived every trial). Correction: future driver convention or an amendment note; not blocking. Revalidation: n/a (convention fix).

**D6 (P2) — result_class vocabulary deviations in auxiliary artifacts.**
Source: 01_RAW/NEGATIVE_FIXTURES_GEXEC.json `"result_class": "G-EXEC"` (outside BYTE_MATCH/REPEATABILITY/RETROSPECTIVE_VALIDATION/RUNTIME_SEMANTICS); PIN_RESULTS.json, SELF_AUDIT.txt, MANIFEST_NEGATIVE_TESTS.json, MANIFEST_VALIDATION.json carry the standing sentence but no result_class label. Effect: minor; the class vocabulary governs claims-bearing outputs, which are all correctly labeled. Correction: labeling convention; not blocking.

Data-integrity findings: NONE. Every load-bearing number of the run (population 334-65=269, split, all 807 verdicts, all 2,556 NC trials, all 11 CIs, coverage 2,171/2,427, census anchors, pins) was independently reproduced by the QC, including a from-bytes re-execution of the frozen grammars on the K2 dump payloads (807/807 + 2,556/2,556 agreement; the 11 truncated spans proven by stride arithmetic and prefix byte-failures).

## FULL_READ_LOG

Fully read (to EOF, in chunks where noted): CONTRACT.md (48); PREREG_MARKER.txt (11); WIDE_GRAMMARS.md (142); GATES_PREREGISTERED.md (37); NC_PROCEDURES.md (23); POPULATION_269.json (3,696 lines — full JSON parsed programmatically + head read); SPLIT_SIDES_269.json (full parse); PIN_RESULTS.json (73); widerecord_driver_r1.py (2,161 lines, 4 chunks — FULL); freeze_wide_r1.py (454 — FULL); SELF_AUDIT.txt (127); NEGATIVE_FIXTURES_GEXEC.json (full parse); MANIFEST_NEGATIVE_TESTS.json (full parse); MANIFEST_VALIDATION.json (124); WIDE_RESULTS.json (full parse, all grammars + gate verdicts); COVERAGE_DELTA.json (full parse); BASELINE_CENSUS_REPRODUCTION.json (full parse); 00_FINAL_REPORT.md (82); HANDOFF.md (9); STAGE_ACCEPTANCE_GATES.csv (9); artifact_index.csv (all 34 rows parsed + re-hashed); WIDE_SPAN_OUTCOMES.jsonl (807 rows, all parsed); WIDE_NC_TRIALS.jsonl (2,556 rows, all parsed). External, fully read/hashed: K2 BASELINE_REPRODUCTION.json (48); K2 NOFIT334_SPANS.txt (all 334 headers + hex bodies processed by the QC parser); RUN A RETRO_SPAN_OUTCOMES.jsonl (993 rows, all parsed); RUN A artifact_index.csv (external rows read; 29 ordinary rows re-hashed); MANIFEST_SCHEMA_SPEC.md (22); R61 SHA256_SOURCE.json (10/10 re-hashed).

## NOT_CHECKED

- The full 5,596-entry corpus census was NOT re-executed by the QC (anchors cross-verified vs the pinned K2 baseline; population independently re-derived from pinned dumps; grammar verdicts independently re-executed on dumped bytes — see Q4/Q5). The in-driver census reproduction is STRONGLY_SUPPORTED, not QC-executed.
- The exact content/provenance of the stale 19th pre-validation file (overwritten during the clean run) cannot be recovered from disk; D1 rests on the 19-vs-18/21 arithmetic plus the executor's own (Task-return) account.
- K2 package files without any independent hash baseline (H1_DESYNC_PROBE.json, h1_desync_probe_posthoc.py, INPUT_PIN_RESULTS.json, PREREG_MARKER.txt, 06_REPORT files, PE_MASTER_REVIEW*.md, SHA256_DRIVER.txt, STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv) were not hash-verified (K2's manifest is DEFECTIVE — a known, disclosed pre-existing condition); no sign of modification found.
- No independent re-derivation of the driver's internal K2 module import behavior at runtime was performed beyond the byte-exact block verification + independent re-execution of the same algorithms.
- Git state: the run is NOT committed (per contract); QC made no commits and no repo writes; BASE_SHA 461098f... not independently re-verified against the repo (out of QC scope items; no repo write by the executor was found — the run dir is outside the repo working tree of D:\TESTAI and no git commands were recorded).

QC_VERDICT = QC_FAIL (reasons: D1-D4 — the final report of a LOAD_BEARING run omits four required material disclosures: the prior execution attempt/pin-typo+re-run (independently corroborated by the 19-vs-18 pre-validation row arithmetic), the 0-hit-NC trivial-separation caveat, the 12/13-in-one-block family concentration, and the side-A-zero-fits asymmetry; plus minor P2 label gaps D5-D6. All quantitative claims, gates, raw data and manifests were independently reproduced and confirmed — the correction is a narrow report amendment, NOT a re-run.)
