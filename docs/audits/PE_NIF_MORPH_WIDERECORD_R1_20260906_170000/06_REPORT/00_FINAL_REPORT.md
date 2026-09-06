# FINAL REPORT - PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 (RUN C)

## 1. HUMAN-FIRST (what needs the human NOW)

Nothing is required from the human inside this run. PE-MASTER owns the post-run 5-layer audit and the publication decision (NO commit was made by the executor). The residual-325 stays OUT OF SCOPE / mechanism-unexplained; no H7-based claims are made anywhere in this package.

## 2. IDENTITY

RUN_ID: PE_NIF_MORPH_WIDERECORD_R1_20260906_170000 | RUN_CLASS: LOAD_BEARING | milestone: EU935-M1 (NO crossing) | date: 2026-09-06 | executor: pe-reconstruction | parent: PE-MASTER loop bd17344b iteration 3 | era: PCG_9_3_5 primary | BASE_SHA 461098f534497113f85157b946cdae5f0331bfdc (no repo writes by the executor)

## 3. STATE DELTA (before -> after)

BEFORE: 269 of the 334 no-fit rr spans remained unconsumed after RUN A (the +65 H5a/H5c2 RETROSPECTIVE_VALIDATED removals); W1/W2/W3 existed only as the K2 post-hoc probe's NON-COVERAGE candidates. AFTER: the three grammars executed per-record on the frozen 269 population with denominator-matched wrong-start NCs and a seeded file-grouped 50/50 split, under the a-priori G-WIDE conjunction. Gate results: W1=PASS; W2=NON_PASS ZERO_FITS; W3=PASS. Coverage delta: X=13 -> real-record coverage 2171/2427 (89.45%); remaining no-fit 256.

## 4/12. EXACT VERDICT + ONE P0

RUN verdict: COMPLETED (all contract outputs produced; no HARD STOP). ONE P0: 'Do the pre-registered wide-record grammars W1/W2/W3 consume the 269 remaining 9.3.5 no-fit morph spans byte-exactly, at rates separated >= 5x from denominator-matched wrong-start negative controls, with per-record validation and file-grouped retrospective homogeneity?' ANSWER (per grammar, a-priori G-WIDE conjunction): W1=PASS; W2=NON_PASS ZERO_FITS; W3=PASS.

- G-WIDE W1: PASS | full-269 fits=12/269 rate=0.04461 CI95=[0.02326, 0.076627] | full NC 0/538 rate=0.0 CI95=[0.0, 0.006833] | held-out units=157 unit-fits=12 unit-rate=0.076433 CI95=[0.040117, 0.129707] | held-out NC 0/314 rate=0.0 CI95=[0.0, 0.011679] | detail={}

- G-WIDE W2: NON_PASS ZERO_FITS | full-269 fits=0/269 rate=0.0 CI95=[0.0, 0.01362] | full NC 5/538 rate=0.009294 CI95=[0.003024, 0.021554] | held-out units=157 unit-fits=0 unit-rate=0.0 CI95=[0.0, 0.023222] | held-out NC 2/314 rate=0.006369 CI95=[0.000772, 0.022818] | detail={"full_269_fits": 0}

- G-WIDE W3: PASS | full-269 fits=13/269 rate=0.048327 CI95=[0.02598, 0.081223] | full NC 0/538 rate=0.0 CI95=[0.0, 0.006833] | held-out units=157 unit-fits=13 unit-rate=0.082803 CI95=[0.044826, 0.137433] | held-out NC 0/314 rate=0.0 CI95=[0.0, 0.011679] | detail={}

## 5/6. CLAIM -> EVIDENCE + DENOMINATORS

Every rate carries numerator/denominator and an exact binomial (Clopper-Pearson) 95% CI. Machine evidence: 05_ANALYSIS/WIDE_RESULTS.json (per-grammar gates, CIs, overlaps, consumed keys), 05_ANALYSIS/COVERAGE_DELTA.json (the machine-readable coverage state), 01_RAW/WIDE_SPAN_OUTCOMES.jsonl (per-record outcomes: span ID, side, grammar, outcome, rejection reason, bytes consumed; the full 269, both sides), 01_RAW/WIDE_NC_TRIALS.jsonl (every NC trial with its explicit denominator: spans_x_2 = 269x2 = 538 per grammar; units_x_2 for the held-out side), BASELINE_CENSUS_REPRODUCTION.json, NEGATIVE_FIXTURES_GEXEC.json, MANIFEST_NEGATIVE_TESTS.json. All fit/NC counts are counter increments over executed records (G-EXEC discipline; self-audit in 01_RAW/SELF_AUDIT.txt with the full len() census).

## 7/8. OPEN ITEMS + COVERAGE HONESTY (NOT checked)

- RUNTIME_SEMANTICS is explicitly NOT_TESTED here (out of scope). No semantic claims; no H7-based claims; the residual-325 population is OUT OF SCOPE (stays mechanism-unexplained; a diagnostic note only).
- The 269 leg is RETROSPECTIVE by construction (W1/W2/W3 were formulated from the K2 post-hoc probe of the same population family); explicitly NOT 'unseen' evidence.
- NOT checked: H5a/H5c1/H5c2/H7 re-testing (RUN A owns them), the 2003-era corpus, g1/g2/mscan m != 32, k-ranges beyond 24, Wm windows beyond +/-64/step 4, any POST-HOC probe (none executed; any would be NON-COVERAGE).
- Coverage honesty: X counts ONLY spans consumed by grammars whose G-WIDE verdict is PASS (frozen decision d5; the K2 OC-rejection precedent); consumed spans of non-pass grammars are recorded in WIDE_RESULTS.json but EXCLUDED from every coverage number.

## 9/10. RETRACTIONS + CHAIN OF CUSTODY

No retraction from this run. The +65 status = RETROSPECTIVE_VALIDATED (RUN A); the K2 post-hoc probe findings (m=32 wide records; k~23) were NON-COVERAGE lesson candidates - this run is their pre-registered test. Originals (corpus, R61, K2, RUN A, R34) READ-ONLY, verified by pins; the K2 artifact_index.csv is DEFECTIVE and was never used as a hash source (every K2 artifact re-hashed from bytes).

## 11. PUSH DISCIPLINE

No commit, no push (per contract). BASE_SHA 461098f... unchanged by this run (no repo writes).

## 13. NEGATIVE CONTROLS

- NC-A: per-span wrong-start trials u+2/u-2 (2 per span; denominator spans x 2 = 538 per grammar), the SAME grammar at the wrong start (W3's NC shifts the whole frozen window). NC-B: held-out-side unit representatives x 2 (denominator units x 2). Rate-vs-rate comparisons only. The vacuous case 0 >= 5x0 cannot pass (NC_EMPTY_DENOMINATOR / ZERO_FITS fail-closed ordering).
- G-EXEC: 8/8 synthetic fixtures fail-closed (NEGATIVE_FIXTURES_GEXEC.json); manifest negative tests a-f: 6/6 FAIL the gate as required.

## 14. HARD STOPS

NONE encountered. (HARD_STOP classes armed by the driver: pin mismatch / census mismatch / write-outside / population mismatch.)

## 15. NEXT STEP + GATES (PE-MASTER decision)

Proposed next: PE-MASTER post-run audit of this package (verdict persistence + publication decision). Gate needs: nothing from the human; no human-gated action inside this run.

## 16. UNKNOWN STAYS UNKNOWN

No semantic claims anywhere in this package; the class -256/field1 semantics remain unknown; RUNTIME_SEMANTICS not tested; the counts recorded above are the only quantitative claims.

## 17. PAYLOAD DISCIPLINE

Zero proprietary payloads in this package: outputs carry identifiers, outcomes, rejection reasons and byte COUNTS only (no payload bytes, no hex dumps). Originals appear as identity metadata (SHA-256 + paths) in artifact_index.csv external-sources section.

## 18. DERIVED-NUMBER PROVENANCE

Generator: 00_CONTROL/widerecord_driver_r1.py sha256 b4fa818a7f7b42de565eb73837b1c10e368f021c3ab54f54146eb84cb499a714 (this file). Grammar execution = IMPORT of the pinned K2 module (sha256 b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a); WIDE_GRAMMARS.md blocks byte-verified against the pinned source (6/6). Census = the K2 stage-1 replica (G-CENSUS PASS, row agreement 6,167/6,167).

## 19. HANDOFF BLOCK (copyable)

AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000\06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000\05_ANALYSIS\WIDE_RESULTS.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000\05_ANALYSIS\COVERAGE_DELTA.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000\05_ANALYSIS\BASELINE_CENSUS_REPRODUCTION.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000\00_CONTROL\PIN_RESULTS.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000\00_CONTROL\POPULATION_269.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000\00_CONTROL\SPLIT_SIDES_269.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000\01_RAW\WIDE_SPAN_OUTCOMES.jsonl; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000\01_RAW\WIDE_NC_TRIALS.jsonl; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_WIDERECORD_R1_20260906_170000\01_RAW\NEGATIVE_FIXTURES_GEXEC.json
RUN_STATUS = COMPLETED
HARD_STOP_REASON = NONE

## 20. SELF-CONTAINED NOTES

Population: the 269 = the 334 K2 no-fit keys minus the union of RUN A's H5a (39) + H5c2 (26) FIT keys; 334 - 65 = 269 EXACT (frozen in 00_CONTROL/POPULATION_269.json BEFORE any test; re-derived in-driver from the census + re-executed RUN A removals). Split: seeded Random(20260906) file-level 50/50 over 62 files (side A 31 / side B 31; spans 112/157; family integrity; both side lists frozen BEFORE testing). Gates a-priori in 00_CONTROL/GATES_PREREGISTERED.md (never adjusted). Consumed spans carry RETROSPECTIVE_VALIDATION (the RUN A standard - explicitly retrospective, NOT unseen).

Standing sentence: no semantic claims; the +65 H5a/H5c2 status = RETROSPECTIVE_VALIDATED (RUN A); the H7 join-mechanism = UNVALIDATED (RUN A) - this run makes NO H7-based claims; the residual-325 population is OUT OF SCOPE (stays mechanism-unexplained; a diagnostic note only, no new claims). Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

## QC1 AMENDMENT (2026-09-06 — disclosures added per INTERNAL_QC_R1 findings D1-D6; the numbers unchanged — QC-verified independently)

(1) PRIOR EXECUTION ATTEMPT (D1): A first execution attempt HARD-STOPPED in-driver on a 63-character transcription error of the RUN A driver pin constant inside this run's own driver; the constant was fixed, the stale partial evidence (an overwritten 06_REPORT draft from that attempt, visible as the 19-vs-18 manifest-row discrepancy at pre-validation time) was removed, and a clean full re-run produced every artifact reported here. The pin itself always matched the physical file; no K2/RUN A input was ever mis-read.

(2) ZERO-HIT NC STRUCTURAL CAVEAT (D2): The W1/W3 negative controls recorded 0 hits (NC 0/538 full; 0/314 held-out; denominators > 0, so not the vacuous case). Because the W1 unit layout [u16 idx][32 x f32] has a fixed 132-byte stride, a u+/-2 start shift misaligns the record boundary by construction, making the NC partly STRUCTURALLY trivial for this grammar family. The separation (full rate 0.0446 vs the NC CI upper bound 0.0068 = 6.5x) is therefore an upper-bound-based bound, not a behaviorally-strong separation; a stronger NC (e.g. stride-aligned wrong-block starts) remains future work.

(3) FAMILY CONCENTRATION (D3): The 13 consumed spans are family-concentrated: 12 of 13 lie in ONE file and block (548296.nif, block 75 — 12 of that block's 15 population spans; single/double [u16 idx][32 x f32] records with head weight pairs), and the 13th (548808.nif block 164 si=129) arrives via the W3 window at offset +4. The wide-record class is CONFIRMED at the record level in this one block; its CROSS-FILE generality is NOT established by this run.

(4) SIDE A = 0 FITS (D4): All 13 fits are on split side B (side B 13/157); side A recorded 0 fits (0/108, exact binomial CI [0.0, 0.0336]). The frozen G-WIDE conjunction gated the held-out side and the full population, and passed as written; the side asymmetry is disclosed here as a homogeneity caveat of the +13 claim.

