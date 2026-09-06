# FINAL REPORT - PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500 (RUN A)

## 1. HUMAN-FIRST (what needs the human NOW)

Nothing is required from the human inside this run. PE-MASTER owns the post-run 5-layer audit and the publication decision (NO commit was made by the executor). The +65/88.88% coverage status REMAINS CANDIDATE regardless of this run's outcome until PE-MASTER's post-run audit.

## 2. IDENTITY

RUN_ID: PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500 | RUN_CLASS: LOAD_BEARING | milestone: EU935-M1 (NO crossing) | date: 2026-09-06 | executor: pe-reconstruction | parent: PE-MASTER loop bd17344b iteration 2

## 3. STATE DELTA (before -> after)

BEFORE: K2 confirmed H5a/H5c1/H5c2/H7 on the FULL 9.3.5 populations (+65 spans, 2158/2427 = 88.88% candidate; status CANDIDATE). No file-grouped split validation and no 2003-era transfer of H5a/H5c2/H7 existed. AFTER: the three frozen grammars revalidated per-record on a seeded file-grouped 50/50 split (RETROSPECTIVE; NOT unseen data) with denominator-matched NCs, executed on the 2003 corpus (ERA_TRANSFER_DIAGNOSTIC), with prior-use/duplicate/family prechecks, G-EXEC per-record discipline + 8/8 fail-closed fixtures, and a spec-compliant manifest. Gate results: H5a=PASS; H5c2=PASS; H7=NON_PASS NC_INSUFFICIENT_SEPARATION.

## 4/12. EXACT VERDICT + ONE P0

RUN verdict: COMPLETED (all contract outputs produced; no HARD STOP). ONE P0: 'Do the FROZEN H5a and H5c2 grammars and the H7 join model hold on (i) file-grouped splits of the 9.3.5 eligible populations (RETROSPECTIVE) and (ii) the 2003-era morph corpus (ERA_TRANSFER_DIAGNOSTIC)?' ANSWER (retro leg, load-bearing): H5a=PASS; H5c2=PASS; H7=NON_PASS NC_INSUFFICIENT_SEPARATION. ANSWER (era leg, diagnostic only): see 9/13 below; explicitly NOT a substitute for 9.3.5-target correctness.

- G-RETRO H5a: PASS | units=163 fits=14 rate=0.08589 CI95=[0.047754, 0.139909] | NC 2/326 rate=0.006135 CI95=[0.000744, 0.021985]

- G-RETRO H5c2: PASS | units=163 fits=20 rate=0.122699 CI95=[0.076584, 0.183123] | NC 2/326 rate=0.006135 CI95=[0.000744, 0.021985]

- G-RETRO H7: NON_PASS NC_INSUFFICIENT_SEPARATION | detail={"positive_rate": 0.322581, "nc_rate": 0.294118} | held-out members=124 explained=40 rate=0.322581 CI95=[0.241451, 0.412412] | NC units=102 hits=30 rate=0.294118 CI95=[0.208024, 0.392546]

## 5/6. CLAIM -> EVIDENCE + DENOMINATORS

Every rate above carries numerator/denominator and an exact binomial (Clopper-Pearson) 95% CI. Machine evidence: 05_ANALYSIS/RETROSPECTIVE_RESULTS.json (per-grammar gates, CIs, repeatability), 01_RAW/RETRO_SPAN_OUTCOMES.jsonl + RETRO_NC_TRIALS.jsonl (per-record outcomes: span ID, side, grammar, outcome, rejection reason, bytes consumed), ERA_TRANSFER_RESULTS.json, ERA_DUPLICATE_CENSUS.json, BASELINE_CENSUS_REPRODUCTION.json, NEGATIVE_FIXTURES_GEXEC.json, MANIFEST_NEGATIVE_TESTS.json. Validation counts are counter increments over executed records (G-EXEC discipline; self-audit in 01_RAW/SELF_AUDIT.txt with the full len() census).

## 7/8. OPEN ITEMS + COVERAGE HONESTY (NOT checked)

- RUNTIME_SEMANTICS is explicitly NOT_TESTED here (out of scope). Class -256/field1 MEANING remains unknown; the -256=>zero-entry association remains ONE-WAY. No semantic claim is made anywhere in this package.
- The retro leg is RETROSPECTIVE by construction (the grammars were selected on the FULL populations in K2); it is explicitly NOT 'unseen'/'holdout' evidence.
- The 2003 leg is DIAGNOSTIC ONLY; near-zero transfer would be the finding CORPUS_SPECIFIC_935 (valid outcome): reported near_zero_transfer=False (see ERA_TRANSFER_RESULTS.json, including per-stratum fits over byte-identical / changed / only-2003 files).
- NOT checked: g1/g2/mscan/H1-H4/H5b/H5d/H6/H8 grammars (out of contract scope); H5c1 (idx<2N) was NOT in this run's gate set (contract fixes H5a/H5c2/H7).
- 2003 era census finding (prior-evidence defect, documented): R35's published 2003 rr_var=1180 uses the (file,tag,si) span key, which collides when one file carries multiple same-tag morph blocks; the collider (574845.nif bi=77 si=14 tag=3; var_ok but NOT rr) inflates R35's count by exactly one. This run's census reproduces EVERY other R35 anchor EXACTLY and reproduces 1,180 under R35's own keying; the collision-free (file,bi,si) census value is 1,179, which defines the era populations (see ERA_CENSUS_2003.json rr_var_resolution).

## 9/10. RETRACTIONS + CHAIN OF CUSTODY

No retraction from this run. Supersession-sensitive context: K2's +65/88.88% coverage status REMAINS CANDIDATE. This run made NO commit (PE-MASTER handles publication after its audit); BASE_SHA per contract 90c86be9e52d00e4dd916ea75bc99ea93354c88f (no repo writes by the executor). Originals (corpora, R61, K1/K2/K3, all prior packages) READ-ONLY, verified by pins.

## 11. PUSH DISCIPLINE

No commit, no push (per contract). BASE_SHA 90c86be9... unchanged by this run.

## 13. NEGATIVE CONTROLS

- NC-A: per-span trials at pinned wrong starts u+2/u-2 (denominator spans x 2), K2 nc2 VERBATIM semantics; NC-B: per-span non-adjacent joins (seeded 20260906, mirroring the <=2 adjacency trials per span; NEVER one-per-file). Vacuous 0>=5x0 CANNOT pass (NC_EMPTY_DENOMINATOR).
- G-EXEC: 8/8 synthetic fixtures fail-closed (see NEGATIVE_FIXTURES_GEXEC.json); manifest negative tests a-f: 6/6 FAIL the gate as required. The gates CAN fail (several produce explicit non-pass classes on the real populations where the a-priori thresholds are not met).

## 14. HARD STOPS

NONE encountered. (HARD_STOP classes armed by the driver: pin mismatch / census mismatch / write-outside / 2003 corpus unresolvable.)

## 15. NEXT STEP + GATES (PE-MASTER decision)

Proposed next: PE-MASTER post-run audit of this package (verdict persistence + publication). Gate needs: nothing from the human; no human-gated action inside this run.

## 16. UNKNOWN STAYS UNKNOWN

-256/field1 semantics unknown; RUNTIME_SEMANTICS not tested; family/corpus counts as recorded above are the only quantitative claims.

## 17. PAYLOAD DISCIPLINE

Zero proprietary payloads in this package: outputs carry identifiers, outcomes, rejection reasons and byte COUNTS only (no payload bytes, no hex dumps). Originals appear as identity metadata (SHA-256 + paths) in artifact_index.csv external-sources section.

## 18. DERIVED-NUMBER PROVENANCE

Generator: 00_CONTROL/revalidate_driver_r1.py sha256 02ecb955bc3796128ed3f3b99cc302df61649f9ac2202e83ee5860ed5de9dbe0
Frozen grammars executed by IMPORT of the pinned K2 module (sha256 b7e4cd328d7c5e0a7881519f428938c03a68cab4b93dd044319caace636c595a); FROZEN_GRAMMARS.md blocks byte-verified against the pinned source (10/10 VERBATIM byte-exact vs pinned K2 source). Census pipeline replicates the K2 stage-1 exactly (G-CENSUS PASS with row agreement 6,167/6,167).

## 19. HANDOFF BLOCK (copyable)

AUDIT_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500
FINAL_REPORT_PATH = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500\06_REPORT\00_FINAL_REPORT.md
PRIMARY_EVIDENCE_PATHS = D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500\05_ANALYSIS\RETROSPECTIVE_RESULTS.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500\05_ANALYSIS\ERA_TRANSFER_RESULTS.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500\05_ANALYSIS\BASELINE_CENSUS_REPRODUCTION.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500\00_CONTROL\PIN_RESULTS.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500\00_CONTROL\SPLIT_SIDES.json; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500\01_RAW\RETRO_SPAN_OUTCOMES.jsonl; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500\01_RAW\RETRO_NC_TRIALS.jsonl; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500\01_RAW\ERA_SPAN_OUTCOMES.jsonl; D:\Eudoria_Reconstruction\99_Audits\PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500\01_RAW\NEGATIVE_FIXTURES_GEXEC.json
RUN_STATUS = COMPLETED
HARD_STOP_REASON = NONE

## 20. SELF-CONTAINED NOTES

Populations: P1 = the 334 no-fit rr spans (pinned NOFIT334_SPANS.txt headers == census set, EXACT); P2 = the 325 residual spans (subset of pinned 333, count 325 EXACT, 56 files, 551564.nif x84). Split: seeded Random(20260906) file-level 50/50 over 85 files (side A 42 / side B 43). Prior-use verdict: NO grammar of the family was derived from 2003-era data (evidence in PRIOR_USE_VERDICT.json). 2003 corpus: 01_Original_Files\BNT_Models\Models.bnt sha256 1322adf2...4a6, 5,426 entries (5,426-name class EXACT; container<->extraction tie 5,426/5,426); the contract's '~5,441' is the R12 manifest CSV physical-line count (5,442 incl. header) whose true CSV record count is 5,426 (standard CSV parser; recorded in PIN_RESULTS.json).

Standing sentence: no semantic claims; class -256/field1 MEANING remains unknown; the -256=>zero-entry association remains ONE-WAY. Result classes: BYTE_MATCH / REPEATABILITY / RETROSPECTIVE_VALIDATION / ERA_TRANSFER_DIAGNOSTIC / RUNTIME_SEMANTICS (= explicitly NOT_TESTED here, out of scope).

