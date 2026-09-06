# CONTRACT — RUN A: PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500

- RUN_CLASS: LOAD_BEARING (declared by PE-MASTER at FORMALIZE per A1.1)
- EXECUTOR: pe-reconstruction | INTERNAL_QC: fresh pe-master-auditor context | PE-MASTER full 5-layer audit follows
- PARENT: PE-MASTER loop bd17344b-a054-4cf4-be8d-5f0b250e8509 (iteration 1) | MILESTONE: EU935-M1 (NO crossing)
- ERA: PCG_9_3_5 primary; 2003 = ERA_TRANSFER_DIAGNOSTIC reference only
- BASE_SHA: 90c86be9e52d00e4dd916ea75bc99ea93354c88f

ONE_PRIMARY_QUESTION: "Do the FROZEN H5a truncated-tail and H5c idx-relaxed grammars and the H7 adjacency-join model, exactly as defined in K2 (PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209), hold (i) on file-grouped splits of the 9.3.5 eligible populations they were selected from (RETROSPECTIVE_REVALIDATION — explicitly NOT unseen data), and (ii) on the 2003-era morph corpus (ERA_TRANSFER_DIAGNOSTIC — subject to prior-use, duplicate and family checks; explicitly NOT a substitute for 9.3.5-target correctness)?"

## 1. RESULT-CLASS SEPARATION (every output labeled with exactly one class)
BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / ERA_TRANSFER_DIAGNOSTIC / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope). Standing sentence in every artifact: no semantic claims; class -256/field1 MEANING remains unknown; the -256=>zero-entry association remains ONE-WAY.

## 2. INPUTS (READ-ONLY; verify pins in-driver BEFORE any parse; HARD STOP on mismatch)
- K2 package docs/audits/PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209/: driver morph_residual_deepdive_r1.py = the source of the FROZEN grammar definitions; physical SHA256 b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a. WARNING: the K2 artifact_index.csv is DEFECTIVE (unquoted comma L2; symbolic rows L17-18) — NEVER use it as a hash source; re-hash every K2 artifact directly from bytes.
- K2 populations: 01_RAW/NOFIT334_SPANS.txt (8bb6556b166df656631af168031e58518b3147fe962d5815ca4e19009e0f605d); 01_RAW/RESIDUAL333_SPANS.txt (e936ed510cbfc6a8ab45b99d3ac7892d467b5d05b24a5ede606f80ddf7bf0100); 05_ANALYSIS/COVERAGE_STATE.json (86c12fa7f3df1149213fbfdef3097f022bb7c7ba38dc2cf4289de4aab1b12fa4); 05_ANALYSIS/BASELINE_REPRODUCTION.json (2e4014c9652df8adf6854b87c17388f9a5288c2c32dc757b34946320db46f1ca); 05_ANALYSIS/HYPOTHESIS_RESULTS.json (c08fb4738ece9d1f2c9cbcb43fe05b866f7560b1808597abc78e70e6e438e4a9); 00_CONTROL/PRE_REGISTERED_HYPOTHESES.json (5bde44acd0817441bc3dadb1f4898f52221d566cfd6da1af4dc89c6027789836).
- Corpora: Models.bnt 9.3.5 SHA256 c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0 (in-driver re-hash before parse); R61 frozen parser 10/10 (READ-ONLY, never modified); the 2003-era corpus: identify the canonical 2003 Models container from the project corpus references, record FULL SHA256 + physical path + entry count from the physical bytes, cross-check the count vs the 2003 canon (~5,441/5,426-class numbers); HARD STOP if unresolvable, ambiguous, or count-mismatched.
- R34/R18/R21 packages (READ-ONLY): for the prior-use lineage check (Section 4).
- RUN B spec: D:\Eudoria_Reconstruction\99_Audits\PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500\00_CONTROL\MANIFEST_SCHEMA_SPEC.md (the run's own artifact_index must follow it).

## 3. FREEZE (write ALL of the following to 00_CONTROL BEFORE any test execution, with a PREREG_MARKER file; record hashes)
- GRAMMARS VERBATIM: extract the exact H5a parse_variable_trunctail and H5c parse_variable(idx_limit) definitions, the H7 prev/next join procedure and greedy_r18 from the pinned K2 driver — copied VERBATIM into a frozen definitions file (no rewording, no parameter changes, no improvements).
- POPULATIONS: the 334 no-fit spans and the 325 residual spans enumerated from the pinned K2 artifacts (file/bi/si ID lists + hashes).
- SPLIT PROCEDURE: file-level 50/50 of the files carrying the eligible populations; seeded random.Random(20260906) over the sorted file list; FAMILY INTEGRITY: all spans of a file land on the same side; both side ID lists written to 00_CONTROL BEFORE testing.
- NC PROCEDURES (seeded, written before testing): H5a/H5c NC = per-span trials at pinned wrong starts u+2 and u-2 (2 trials per span; denominator = spans x 2) vs positives = 1 trial per span at the true start; H7 NC = per-span non-adjacent joins sampled per span (matching the <=2 adjacency trials per span, seeded) — NEVER one-per-file; every comparison rate-vs-rate on explicit denominators; raw-count cross-population comparisons FORBIDDEN.
- ALL PREDICATES (Section 5) exactly as written in this contract.
## 4. 2003-LEG PRECHECKS (before any 2003 testing; outputs to 05_ANALYSIS)
- PRIOR-USE: read the era labels and derivation provenance in the R34 REAL_SPARSE_GRAMMAR / R18 / R21 / K2 packages; record (with paths) whether ANY grammar of the family (var-k, g1/g2, H5a, H5c, H7 join) was derived FROM 2003-era data; if yes, label the 2003 leg RETROSPECTIVE as well.
- DUPLICATE CENSUS: byte-identical payload census between the eras for the morph-relevant file set; group duplicates.
- FAMILY GROUPING: same file = one family; byte-identical payloads = one family; report the family count used as the independence unit.

## 5. GATES (a-priori; fixed HERE; NEVER adjusted after seeing results)
- G-PINS: every input pin verified in-driver before any parse (R61 10/10; K2 artifacts re-hashed from bytes; the 2003 corpus SHA recorded). PASS = all match. Mismatch = HARD STOP.
- G-CENSUS: the baseline census reproduces K2 EXACTLY (rr 2,427 / var 2,093 / nofit 334 = 62 alt + 272 none; unknown-325 = 325 across 56 files; 551564.nif x84). Mismatch = HARD STOP.
- G-RETRO (the 9.3.5 retrospective leg; evaluated per grammar H5a, H5c2, and the H7 join model separately): PASS iff (held-out independent trial units after family grouping >= 30) AND (held-out fits >= 10) AND (held-out positive rate >= 5x the matched-NC rate) AND (NC denominator > 0). A-PRIORI JUSTIFICATION (recorded with the contract, never adjusted): >=30 units so the exact binomial 95% CI of the held-out rate is not degenerate; >=10 fits so the rate is not a 1-2-span artifact; 5x = K2's own pre-registered separation standard. Report the exact binomial 95% CI for every rate. THE VACUOUS CASE 0 >= 5x0 CANNOT PASS (NC denominator 0 => NC_EMPTY_DENOMINATOR non-pass). NON-PASS classes: EMPTY_GROUP / ZERO_FITS / INSUFFICIENT_TRIALS(<30 units) / NC_EMPTY_DENOMINATOR / NC_INSUFFICIENT_SEPARATION(<5x).
- G-ERA (the 2003 leg): DIAGNOSTIC ONLY, no PASS/FAIL; outputs: fit counts, rates with exact binomial CIs, the prior-use verdict, the duplicate/family census; near-zero transfer = the finding CORPUS_SPECIFIC_935 (a valid outcome, not a failure). Explicitly NOT a substitute for 9.3.5-target correctness.
- G-EXEC: every validation/validation_exact number computed by executing the predicate on a SPECIFIC record; per-record outcomes recorded (span ID, side, grammar, outcome, rejection reason, bytes consumed); deriving any validation count from a group size is FORBIDDEN. The driver must (a) self-audit: grep its own gate code for size-derived assignments (patterns like "// 2" applied to a population count, len()-derived validation counts) and record the audit result; (b) unit-test the gate with EIGHT synthetic fixtures, EACH producing an explicit non-pass outcome: (1) zero successes both sides; (2) empty population; (3) only-previously-selected successes; (4) a duplicate present in both groups; (5) unequal denominators; (6) a corrupted record; (7) a malformed manifest row; (8) a missing input file. All eight fail-closed => G-EXEC PASS.
- G-SCOPE: read-only originals; zero payloads; run-local tooling only in 00_CONTROL; this run's own artifact_index.csv written per RUN B's MANIFEST_SCHEMA_SPEC.md and its self-validation gate PASSES (dogfooding).

## 6. REQUIRED OUTPUTS
- 00_CONTROL: the driver + frozen definitions + population/split ID lists + PREREG_MARKER + pin results.
- 01_RAW: per-span outcomes (machine-readable: span ID, side, grammar, outcome, rejection reason, bytes consumed) for BOTH legs; NC trial records with denominators; the eight negative-fixture results.
- 05_ANALYSIS: RETROSPECTIVE_RESULTS.json (per-grammar rates, CIs, denominators, verdicts); ERA_TRANSFER_RESULTS.json (diagnostic numbers + the prior-use verdict + the duplicate census); MANIFEST_VALIDATION.json.
- 06_REPORT: 00_FINAL_REPORT.md (the s15 20-point contract) + HANDOFF.md; STAGE_ACCEPTANCE_GATES.csv (one row per gate with its result); artifact_index.csv per the spec.
- REPORTING: every outcome labeled with its result-class (Section 1); the +65/88.88% coverage status REMAINS CANDIDATE regardless of this run's outcome until PE-MASTER's post-run audit; NO wiki updates (HOLD).

## 7. HARD STOPS / FORBIDDEN
- HARD STOPS: any pin mismatch; G-CENSUS mismatch; any write outside the run dir; the 2003 corpus unresolvable or count-ambiguous.
- FORBIDDEN: modifying the K1/K2/K3 packages or ANY completed run dir; wiki (docs/nif); runtime work; x87/display experiments; the R61 parser; the post-audit package; PE_MASTER_LOOP_STATE.json + PE_MASTER_LOOP_EVENTS (plugin-owned); payloads; any M2/milestone action; adjusting any gate after seeing results; claiming the 9.3.5 split leg is "unseen"/"holdout" (it is RETROSPECTIVE by construction).

## 8. FINAL HANDOFF SCHEMA
AUDIT_OUTPUT_ROOT / FINAL_REPORT_PATH / PRIMARY_EVIDENCE_PATHS / RUN_STATUS / HARD_STOP_REASON.