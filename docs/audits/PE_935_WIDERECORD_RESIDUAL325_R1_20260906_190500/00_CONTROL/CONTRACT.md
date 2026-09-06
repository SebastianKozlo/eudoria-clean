# CONTRACT — RUN E: PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500

- RUN_CLASS: LOAD_BEARING (declared by PE-MASTER at FORMALIZE per A1.1 — it can add coverage)
- EXECUTOR: pe-reconstruction | INTERNAL_QC: fresh pe-master-auditor context | PE-MASTER full audit follows
- PARENT: PE-MASTER loop bd17344b-a054-4cf4-be8d-5f0b250e8509 (iteration 5) | MILESTONE: EU935-M1 (NO crossing) | ERA: PCG_9_3_5
- BASE_SHA: cd1ee07f35d43a631021dcde0cd6b439a2bda63b

ONE_PRIMARY_QUESTION: "Do the FROZEN W1/W3 wide-record grammars (verbatim from RUN C, PE_NIF_MORPH_WIDERECORD_R1_20260906_170000) consume any of the 325 R21-unknown residual 9.3.5 morph spans byte-exactly, at rates separated from the denominator-matched wrong-start negative controls?"

## 1. RESULT-CLASS DISCIPLINE
Every output carries the standing sentence: no semantic claims; the +65 (RUN A) = RETROSPECTIVE_VALIDATED; the +13 (RUN C) = RETROSPECTIVE_VALIDATED with the family-concentration bounds; the H7 join-mechanism = UNVALIDATED (RUN A) — NO H7-based claims; the residual-325 remains the heterogeneous bucket this run only PROBES.

## 2. INPUTS (READ-ONLY; pins verified in-driver; HARD STOP on mismatch)
- The 325 population: K2 05_ANALYSIS/COVERAGE_STATE.json (SHA256 86c12fa7f3df1149213fbfdef3097f022bb7c7ba38dc2cf4289de4aab1b12fa4 — the unknown-325 census) + 01_RAW/RESIDUAL333_SPANS.txt (e936ed510cbfc6a8ab45b99d3ac7892d467b5d05b24a5ede606f80ddf7bf0100) — re-hash directly (the K2 manifest is DEFECTIVE); the 325 = the 325 R21-unknown keys (56 files; 551564.nif x84).
- The FROZEN grammars: RUN C's 00_CONTROL (the W1/W3 definitions + the driver procedures — pin from RUN C's artifact_index: the contract 404f73687913a5ee934ce123b6bd9588bc2427dfd7b73b2f217f1b21f6ff5f3e and the driver b4fa818a7f7b42de565eb73837b1c10e368f021c3ab54f54146eb84cb499a714); the grammar definitions copied VERBATIM (no rewording, no parameter changes).
- Models.bnt 9.3.5 (c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0); R61 10/10; the RUN B manifest spec (the artifact_index dogfood).

## 3. FREEZE (before any testing; PREREG_MARKER + hashes)
- The W1/W3 definitions verbatim + the NC procedures (per-span wrong-start trials u+2/u-2, 2 per span, explicit denominators) + the split (file-level 50/50, random.Random(20260906), sorted file list, family integrity) + ALL predicates below.
- The 325-key list with hashes, written BEFORE testing.

## 4. GATES (a-priori; NEVER adjusted after seeing results)
- G-PINS: all pins in-driver; mismatch = HARD STOP.
- G-CENSUS: the K2 baseline reproduces (rr 2,427 / var 2,093 / nofit 334; unknown-325 = 325 across 56 files; 551564.nif x84); mismatch = HARD STOP.
- G-WIDE325 (per grammar W1, W3 separately): PASS iff (full-325 fits >= 5) AND (full-325 rate >= 5x the matched-NC rate) AND (NC denominator > 0). A-PRIORI JUSTIFICATION (recorded): fits >= 5 (not 10) because this is a LOW-PREVALECE probe of a heterogeneous fragment bucket — 5+ fits with >= 5x separation and exact CIs establish the class's existence; fewer than 5 = the class ABSENT/RARE (a valid bound, not a failure). Report the exact binomial CI for every rate. THE VACUOUS CASE 0 >= 5x0 CANNOT PASS.
- G-CONCENTRATION (new — the RUN C lesson): the per-side/per-family fit distribution is ALWAYS reported; if ALL fits land on one split side or one file+block, the label CONCENTRATED is MANDATORY in every output (a disclosure class, not a gate failure by itself; the PASS stands only with the separation intact + the concentration disclosed).
- NON-PASS classes: EMPTY_GROUP / ZERO_FITS(<5) / NC_EMPTY_DENOMINATOR / NC_INSUFFICIENT_SEPARATION(<5x).
- G-EXEC: per-record outcomes only; zero size-derived validation numbers (the driver self-audit); the EIGHT negative fixtures fail-closed (the standard list).
- G-SCOPE: read-only originals; zero payloads; run-local tooling only; the artifact_index per the spec + self-validation PASS.

## 5. REQUIRED OUTPUTS
- 00_CONTROL: the driver + the frozen W-definitions + the 325-key list + split lists + PREREG_MARKER + pins.
- 01_RAW: per-span outcomes JSONL (span, side, grammar, outcome, reason, bytes_consumed) + NC trials JSONL (explicit denominators) + the eight fixture results.
- 05_ANALYSIS: WIDE325_RESULTS.json (per-grammar: full + per-side rates, exact binomial CIs, NC rates + CIs, separations, verdicts, non-pass classes, the concentration labels); COVERAGE_DELTA.json (the machine-readable coverage state: 2,171/2,427 = 89.45% stands; + any W1/W3 additions X with the RETROPECTIVE_VALIDATED + CONCENTRATED labels; the 325 -> 325 - X); MANIFEST_VALIDATION.json.
- 06_REPORT: 00_FINAL_REPORT.md (the s15 essentials) + HANDOFF.md; STAGE_ACCEPTANCE_GATES.csv; artifact_index.csv per the spec.
- REPORTING: OBSERVED/RETROSPECTIVE_VALIDATED labels; NO H7 claims; NO semantic claims; the wiki HOLD; if ZERO_FITS: the honest bound statement ("the wide-record class is absent/rare in the 325 residual") is a VALID OUTCOME — report it plainly.

## 6. HARD STOPS / FORBIDDEN
- HARD STOPS: pin/census mismatch; any write outside the run dir.
- FORBIDDEN: modifying any completed run package; wiki; runtime work; the R61 parser; payloads; M2/milestone action; H7-based claims; adjusting gates after results.

## 7. FINAL HANDOFF SCHEMA
AUDIT_OUTPUT_ROOT / FINAL_REPORT_PATH / PRIMARY_EVIDENCE_PATHS / RUN_STATUS / HARD_STOP_REASON.
