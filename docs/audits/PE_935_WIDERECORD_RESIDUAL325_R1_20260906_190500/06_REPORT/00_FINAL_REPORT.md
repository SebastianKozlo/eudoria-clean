# FINAL REPORT - PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500 (RUN E)

## 1. HUMAN-FIRST (what needs the human NOW)

Nothing is required from the human inside this run. PE-MASTER owns the post-run audit and the publication decision (NO commit was made by the executor). NO H7-based claims are made anywhere in this package; the residual-325 remains the heterogeneous bucket this run only PROBES.

## 2. IDENTITY

RUN_ID: PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500 | RUN_CLASS: LOAD_BEARING | milestone: EU935-M1 (NO crossing) | date: 2026-09-06 | executor: pe-reconstruction | parent: PE-MASTER loop bd17344b iteration 5 | era: PCG_9_3_5 | BASE_SHA cd1ee07f35d43a631021dcde0cd6b439a2bda63b (no repo writes by the executor)

## 3. STATE DELTA (before -> after)

BEFORE: the 325 R21-unknown residual spans (fail greedy walk + r19 + backtrack + shift-scan; 333 R21-unknown minus 8 shift-only; 56 files; 551564.nif x84) were the heterogeneous mechanism-unexplained bucket; the FROZEN W1/W3 grammars had been validated ONLY on the 269 no-fit rr population (RUN C). AFTER: W1/W3 executed per-record on the frozen 325 with denominator-matched wrong-start NCs (650 trials per grammar) under the a-priori G-WIDE325 predicate. Gate results: W1=NON_PASS ZERO_FITS; W3=NON_PASS ZERO_FITS. Coverage delta: X=0 -> residual 325 -> 325; rr coverage 2,171/2,427 = 89.45% stands; combined consumed 2171.

## 4/12. EXACT VERDICT + ONE P0

RUN verdict: COMPLETED (all contract outputs produced; no HARD STOP). ONE P0: 'Do the FROZEN W1/W3 wide-record grammars (verbatim from RUN C) consume any of the 325 R21-unknown residual 9.3.5 morph spans byte-exactly, at rates separated from the denominator-matched wrong-start negative controls?' ANSWER: NO - the wide-record class is absent/rare in the 325 residual (the honest bound: W1=NON_PASS ZERO_FITS; W3=NON_PASS ZERO_FITS; ZERO_FITS is a VALID outcome)

- G-WIDE325 W1: NON_PASS ZERO_FITS | full-325 fits=0/325 rate=0.0 CI95=[0.0, 0.011286] | NC 0/650 rate=0.0 CI95=[0.0, 0.005659] | separation=- | concentration labels=NOT_APPLICABLE_ZERO_FITS | per-side fits A=0 B=0 | file-blocks-with-fits=0 | detail={"full_325_fits": 0, "threshold": 5}

- G-WIDE325 W3: NON_PASS ZERO_FITS | full-325 fits=0/325 rate=0.0 CI95=[0.0, 0.011286] | NC 0/650 rate=0.0 CI95=[0.0, 0.005659] | separation=- | concentration labels=NOT_APPLICABLE_ZERO_FITS | per-side fits A=0 B=0 | file-blocks-with-fits=0 | detail={"full_325_fits": 0, "threshold": 5}

## 5/6. CLAIM -> EVIDENCE + DENOMINATORS

Every rate carries numerator/denominator and an exact binomial (Clopper-Pearson) 95%% CI. Machine evidence: 05_ANALYSIS/WIDE325_RESULTS.json (per-grammar gates, CIs, per-side rates, concentration reports, W3 offset histogram, consumed keys), 05_ANALYSIS/COVERAGE_DELTA.json (the machine-readable coverage state), 01_RAW/WIDE325_SPAN_OUTCOMES.jsonl (per-record outcomes: span ID, side, grammar, outcome, rejection reason, bytes consumed; the full 325, both grammars), 01_RAW/WIDE325_NC_TRIALS.jsonl (every NC trial with its explicit denominator: spans_x_2 = 325x2 = 650 per grammar), BASELINE_CENSUS_REPRODUCTION.json, NEGATIVE_FIXTURES_GEXEC.json, MANIFEST_NEGATIVE_TESTS.json. All fit/NC counts are counter increments over executed records (G-EXEC discipline; self-audit in 01_RAW/SELF_AUDIT.txt with the full len() census).

## 7/8. OPEN ITEMS + COVERAGE HONESTY (NOT checked)

- RUNTIME_SEMANTICS is explicitly NOT_TESTED here (out of scope). No semantic claims; NO H7-based claims; the residual-325 remains the heterogeneous bucket this run only PROBES.
- The 325 leg is a RETROSPECTIVE probe (W1/W3 were formulated on the K2/RUN C no-fit population family, not on this residual); explicitly NOT 'unseen' evidence.
- NOT checked: W2 (out of this run's pre-registered set), the 2003-era corpus, g1/g2/mscan m != 32, Wm windows beyond +/-64/step 4, any POST-HOC probe (none executed; any would be NON-COVERAGE), the 8 shift-only spans, H6/H7/H8 mechanisms (K2 owns them; H7 = UNVALIDATED, NO H7-based claims).
- Coverage honesty: X counts ONLY spans consumed by grammars whose G-WIDE325 verdict is PASS (frozen decision d5; the K2 OC-rejection precedent); consumed spans of non-pass grammars are recorded in WIDE325_RESULTS.json but EXCLUDED from every coverage number. ZERO_FITS is a VALID honest outcome (d6) - reported plainly if it is the result.

## 9/10. RETRACTIONS + CHAIN OF CUSTODY

No retraction from this run. The +65 (RUN A) = RETROSPECTIVE_VALIDATED; the +13 (RUN C) = RETROSPECTIVE_VALIDATED with the family-concentration bounds; the H7 join-mechanism = UNVALIDATED (RUN A) - NO H7-based claims. Originals (corpus, R61, K2, RUN C, R34) READ-ONLY, verified by pins; the K2 manifest is DEFECTIVE and was never used as a hash source (every K2 artifact re-hashed directly from bytes).

## 11. PUSH DISCIPLINE

No commit, no push (per contract). BASE_SHA cd1ee07f... unchanged by this run (no repo writes).

## 13. NEGATIVE CONTROLS

- NC-A: per-span wrong-start trials u+2/u-2 (2 per span; denominator spans x 2 = 650 per grammar), the SAME grammar at the wrong start (W3's NC shifts the whole frozen window). Rate-vs-rate comparisons only. The vacuous case 0 >= 5x0 cannot pass (NC_EMPTY_DENOMINATOR / ZERO_FITS fail-closed ordering, checked before any separation comparison).
- G-EXEC: 8/8 synthetic fixtures fail-closed (NEGATIVE_FIXTURES_GEXEC.json); manifest negative tests a-f: 6/6 FAIL the gate as required.

## 14. HARD STOPS

NONE encountered. (HARD_STOP classes armed by the driver: pin mismatch / census mismatch / write-outside / population mismatch.)

## 15. NEXT STEP + GATES (PE-MASTER decision)

Proposed next: PE-MASTER post-run audit of this package (verdict persistence + publication decision). Gate needs: nothing from the human; no human-gated action inside this run.

## 16. UNKNOWN STAYS UNKNOWN

No semantic claims anywhere in this package; the per-record semantics of the residual spans remain unknown; RUNTIME_SEMANTICS not tested; the counts recorded above are the only quantitative claims.

## 17. PAYLOAD DISCIPLINE

Zero proprietary payloads in this package: outputs carry identifiers, outcomes, rejection reasons and byte COUNTS only (no payload bytes, no hex dumps). Originals appear as identity metadata (SHA-256 + paths) in artifact_index.csv external-sources section.

## 18. DERIVED-NUMBER PROVENANCE

Generator: 00_CONTROL/widerecord325_driver_r1.py sha256 b06cb445cf12c5f25cd3f383f81a639ebeefc0380cb395c8635206d14aad2e3c (this file); freeze module 00_CONTROL/freeze_wide325_r1.py sha256 18e34478930f31ad30f27fcceac0ca356bf14a7637ec14038e87c96c8ec32e01. Grammar execution = IMPORT of the pinned K2 module (sha256 b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a); WIDE_GRAMMARS_325.md blocks byte-verified against the pinned K2 source (6/6); the W1/W3 definitions + invocation semantics byte-verified VERBATIM against RUN C's pinned WIDE_GRAMMARS.md. Census = the K2 stage-1 replica (G-CENSUS PASS, row agreement 6,167/6,167).

## 19. HANDOFF BLOCK (copyable)

AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500\06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500\05_ANALYSIS\WIDE325_RESULTS.json; D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500\05_ANALYSIS\COVERAGE_DELTA.json; D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500\05_ANALYSIS\BASELINE_CENSUS_REPRODUCTION.json; D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500\00_CONTROL\PIN_RESULTS.json; D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500\00_CONTROL\POPULATION_325.json; D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500\00_CONTROL\SPLIT_SIDES_325.json; D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500\01_RAW\WIDE325_SPAN_OUTCOMES.jsonl; D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500\01_RAW\WIDE325_NC_TRIALS.jsonl; D:\Eudoria_Reconstruction\99_Audits\PE_935_WIDERECORD_RESIDUAL325_R1_20260906_190500\01_RAW\NEGATIVE_FIXTURES_GEXEC.json
RUN_STATUS = COMPLETED
HARD_STOP_REASON = NONE

## 20. SELF-CONTAINED NOTES

Population: the 325 R21-unknown residual 9.3.5 morph spans = the census unknown-325 (fail greedy walk + r19 + backtrack + shift-scan); 333 - 8 shift-only = 325 EXACT (56 files; 551564.nif x84); frozen in 00_CONTROL/POPULATION_325.json BEFORE any test (derived by the freeze-script census replica; re-derived + cross-checked in-driver: frozen == census EXACT). Split: seeded Random(20260906) file-level 50/50 over 56 files (side A 28 / side B 28; spans 96/229; family integrity; both side lists frozen BEFORE testing; reproduces from the seed). Gates a-priori in 00_CONTROL/GATES_PREREGISTERED.md (never adjusted). Consumed spans carry RETROSPECTIVE_VALIDATION (the RUN A/C standard - explicitly retrospective, NOT unseen) + the G-CONCENTRATION labels wherever they hold.

Standing sentence: no semantic claims; the +65 (RUN A) = RETROSPECTIVE_VALIDATED; the +13 (RUN C) = RETROSPECTIVE_VALIDATED with the family-concentration bounds; the H7 join-mechanism = UNVALIDATED (RUN A) - NO H7-based claims; the residual-325 remains the heterogeneous bucket this run only PROBES. Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

