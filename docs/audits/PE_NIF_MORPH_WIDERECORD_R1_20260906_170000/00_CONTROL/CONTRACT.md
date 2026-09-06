# CONTRACT — RUN C: PE_NIF_MORPH_WIDERECORD_R1_20260906_170000

- RUN_CLASS: LOAD_BEARING (declared by PE-MASTER at FORMALIZE per A1.1)
- EXECUTOR: pe-reconstruction | INTERNAL_QC: fresh pe-master-auditor context | PE-MASTER full 5-layer audit follows
- PARENT: PE-MASTER loop bd17344b-a054-4cf4-be8d-5f0b250e8509 (iteration 3) | MILESTONE: EU935-M1 (NO crossing)
- ERA: PCG_9_3_5 primary | BASE_SHA: 461098f534497113f85157b946cdae5f0331bfdc

ONE_PRIMARY_QUESTION: "Do the pre-registered wide-record grammars — W1: the fixed-m mscan unit [u16 idx][32 x f32] (m=32, head weights — the K2 post-hoc probe's candidate); W2: var-k with the k-range extended to 9..24 (the 'k~23' candidate); W3: W1 with a Wm mis-estimate window (Wm +/- 64, step 4) — consume the 269 remaining 9.3.5 no-fit morph spans (334 minus the 65 RUN-A-validated H5a/H5c2 fits) byte-exactly, at rates separated >= 5x from denominator-matched wrong-start negative controls, with per-record validation and file-grouped retrospective homogeneity?"

## 1. RESULT-CLASS SEPARATION (every output labeled with exactly one class)
BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope). Standing sentences in every artifact: no semantic claims; the +65 H5a/H5c2 status = RETROSPECTIVE_VALIDATED (RUN A); the H7 join-mechanism = UNVALIDATED (RUN A) — this run makes NO H7-based claims; the residual-325 population is OUT OF SCOPE (stays mechanism-unexplained; a diagnostic note only, no new claims).

## 2. INPUTS (READ-ONLY; verify pins in-driver BEFORE any parse; HARD STOP on mismatch)
- RUN A package (repo docs/audits/PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500/ + the 99_Audits master): 01_RAW/RETRO_SPAN_OUTCOMES.jsonl (source of the H5a/H5c2 FIT keys = the validated removals; take the SHA256 pin from RUN A's artifact_index.csv, ordinary row) and 00_CONTROL/revalidate_driver_r1.py (SHA256 02ecb955bc3796128ed3f3b99cc302df61649f9ac2202e83ee5860ed5de9dbe0 — the parser/greedy procedure source).
- K2 package (docs/audits/PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209/ — its artifact_index.csv is DEFECTIVE, re-hash directly): 01_RAW/NOFIT334_SPANS.txt (8bb6556b166df656631af168031e58518b3147fe962d5815ca4e19009e0f605d); 05_ANALYSIS/COVERAGE_STATE.json (86c12fa7f3df1149213fbfdef3097f022bb7c7ba38dc2cf4289de4aab1b12fa4); 05_ANALYSIS/HYPOTHESIS_RESULTS.json (c08fb4738ece9d1f2c9cbcb43fe05b866f7560b1808597abc78e70e6e438e4a9); 05_ANALYSIS/BASELINE_REPRODUCTION.json (2e4014c9652df8adf6854b87c17388f9a5288c2c32dc757b34946320db46f1ca).
- Models.bnt 9.3.5 (SHA256 c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0, in-driver re-hash); R61 frozen parser 10/10 (READ-ONLY).
- The manifest spec: D:\Eudoria_Reconstruction\99_Audits\PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500\00_CONTROL\MANIFEST_SCHEMA_SPEC.md (this run's artifact_index must follow it + its self-validation gate).

## 3. FREEZE (write ALL of the following to 00_CONTROL BEFORE any test execution, with a PREREG_MARKER file; record hashes)
- HYPOTHESES VERBATIM: W1 = the fixed-m mscan unit [u16 idx][32 x f32] (m=32) with the head weight pair, consuming the span from the walk start; W2 = the var-k grammar with the k-range extended to 9..24 (all other constraints identical to the canon var-k); W3 = W1 with a Wm mis-estimate window (Wm-64..Wm+64, step 4). NO post-hoc variants; any additional probe must be labeled POST-HOC NON-COVERAGE and excluded from all coverage numbers.
- THE 269 POPULATION: the 334 no-fit span keys MINUS the union of RUN A's H5a (39) + H5c2 (26) FIT keys — the subtraction lists + the resulting 269-key list written with hashes BEFORE testing; assert 334 - 65 = 269 exactly.
- NC PROCEDURES (seeded, written before testing): per-span wrong-start trials u+2 and u-2 (2 trials per span; explicit denominators); rate-vs-rate comparisons only.
- SPLIT PROCEDURE: file-level 50/50 of the 269-population's files (random.Random(20260906) over the sorted file list; family integrity — all spans of a file on the same side); both side ID lists written BEFORE testing.
- ALL PREDICATES (Section 4) exactly as written in this contract.
## 4. GATES (a-priori; fixed HERE; NEVER adjusted after seeing results)
- G-PINS: every input pin verified in-driver before any parse (R61 10/10; Models.bnt; the RUN A artifacts; the K2 artifacts re-hashed from bytes). Mismatch = HARD STOP.
- G-CENSUS: the baseline reproduces EXACTLY (rr 2,427 / var 2,093 / nofit 334 = 62 alt + 272 none; unknown-325 = 325) AND the RUN A removals reproduce (H5a 39 + H5c2 26 FIT keys from the pinned RUN A artifacts) AND 334 - 65 = 269 exact. Mismatch = HARD STOP.
- G-WIDE (evaluated per grammar W1, W2, W3 separately; the PASS predicate is a conjunction — ALL components must hold):
  PASS iff (full-269 fits >= 10) AND (full-269 positive rate >= 5x the matched-NC rate) AND (NC denominator > 0) AND (held-out side units >= 30) AND (held-out fits >= 10) AND (held-out rate >= 5x the held-out-side matched-NC rate).
  THE VACUOUS CASE 0 >= 5x0 CANNOT PASS (NC denominator 0 => NC_EMPTY_DENOMINATOR). Report the exact binomial 95% CI for every rate (full and held-out, positive and NC).
  NON-PASS classes: EMPTY_GROUP / ZERO_FITS / INSUFFICIENT_TRIALS(held-out units < 30) / NC_EMPTY_DENOMINATOR / NC_INSUFFICIENT_SEPARATION(<5x) / HETEROGENEOUS_SPLIT (the full-269 passes its rate test but the held-out side fails — report BOTH numbers).
  A-PRIORI JUSTIFICATION (recorded, never adjusted): fits >= 10 so the rate is not a 1-2-span artifact; units >= 30 so the exact binomial CI is not degenerate; 5x = the K2/RUN A pre-registered separation standard; the held-out conjunction prevents full-population masking of file-level heterogeneity.
- G-EXEC: every validation number computed by executing the predicate on a SPECIFIC record; per-record outcomes recorded (span ID, side, grammar, outcome, rejection reason, bytes consumed); deriving any validation count from a group size is FORBIDDEN. The driver must (a) self-audit: grep its own gate code for size-derived assignments and record the audit; (b) unit-test the gate with the EIGHT synthetic fixtures (each must produce an explicit non-pass): (1) zero successes both sides; (2) empty population; (3) only-previously-selected successes; (4) a duplicate present in both groups; (5) unequal denominators; (6) a corrupted record; (7) a malformed manifest row; (8) a missing input file. All eight fail-closed => G-EXEC PASS.
- G-SCOPE: read-only originals; zero payloads; run-local tooling only in 00_CONTROL; this run's own artifact_index.csv written per MANIFEST_SCHEMA_SPEC.md and its self-validation gate PASSES (dogfooding).

## 5. REQUIRED OUTPUTS
- 00_CONTROL: the driver + the W1/W2/W3 definitions + the 269-key list + the subtraction lists + split side lists + PREREG_MARKER + pin results.
- 01_RAW: per-span outcomes JSONL (span, side, grammar, outcome, reason, bytes_consumed, result_class) for the full 269 both sides; NC trial records JSONL with explicit denominators; the eight negative-fixture results.
- 05_ANALYSIS: WIDE_RESULTS.json (per-grammar: full + held-out rates, exact binomial CIs, NC rates, separations, verdicts, non-pass classes); COVERAGE_DELTA.json (the machine-readable coverage state: 2,093 canon + 65 RETROSPECTIVE_VALIDATED (RUN A) + this run's validated additions X = the new real-record coverage with the exact status labels; remaining no-fit = 269 - X); MANIFEST_VALIDATION.json.
- 06_REPORT: 00_FINAL_REPORT.md (the s15 20-point contract) + HANDOFF.md; STAGE_ACCEPTANCE_GATES.csv (one row per gate with its result); artifact_index.csv per the spec.
- REPORTING: every consumed span added by W1/W2/W3 carries the RETROSPECTIVE_VALIDATION result-class (the RUN A standard — explicitly retrospective, NOT unseen); POST-HOC probes are NON-COVERAGE and excluded from every number; the wiki remains HOLD; NO residual-325 claims; NO H7-based claims; the standing sentence in every artifact.

## 6. HARD STOPS / FORBIDDEN
- HARD STOPS: any pin mismatch; G-CENSUS mismatch; any write outside the run dir.
- FORBIDDEN: modifying any completed run package; wiki (docs/nif); runtime work; x87/display experiments; the R61 parser; era legs (out of scope — narrow); residual-325 claims; H7-based claims; payloads; any M2/milestone action; adjusting any gate after seeing results.

## 7. FINAL HANDOFF SCHEMA
AUDIT_OUTPUT_ROOT / FINAL_REPORT_PATH / PRIMARY_EVIDENCE_PATHS / RUN_STATUS / HARD_STOP_REASON.
