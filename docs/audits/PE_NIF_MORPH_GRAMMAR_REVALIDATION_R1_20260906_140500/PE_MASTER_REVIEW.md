# PE_MASTER_REVIEW — PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500 (loop bd17344b iteration 2)

AUDITED_RUN = PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1_20260906_140500 (RUN_CLASS LOAD_BEARING; BASE bc11a63)
VERDICT = MASTER_ACCEPTED (advisory)
AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE

## BASIS
(1) Contract SHA256 02F32099... verified; driver 02ecb955... verified. (2) PE-MASTER own re-derivations from the raw JSONL: H5a side-B 164 rows / 15 fits / 163 units / 14 unit-fits (rate 0.0859, exact binomial CI95 [0.0478, 0.1399]) vs NC 2/326 = 0.006135 [0.0007, 0.0220] -> 14.0x; H5c2 163 units / 20 fits (0.1227 [0.0766, 0.1831]) -> 20.0x; H7 124 units / 40 join-explained (0.3226 [0.2415, 0.4124]) vs the per-unit non-adjacent-join NC 30/102 = 0.2941 [0.2080, 0.3925] -> 1.10x; pooled NC 5/668 — ALL gate numbers re-derived by PE-MASTER personally from the raw rows. (3) Repeatability: the deterministic re-execution reproduces K2 exactly (H5a 39, H5c2 26, H7 74; NC 5/668). (4) FRESH INTERNAL_QC (independent session): QC_PASS with a FULL independent re-execution from the physical corpora (4,283 per-record comparisons, 0 mismatches; exact binomial CIs 12/12; the seeded split reproducible; 6 disclosed P2/P3 documentation-level, none affecting verdicts or numbers; record 00_CONTROL/INTERNAL_QC_R1.md SHA256 0cb21dc3ae517c18e4da50f3756020d2c5f71196bc3e69cac6f0d9c39c266540). (5) The driver contains ZERO size-derived validation assignments; the eight negative fixtures fail-closed; the gates demonstrably CAN fail — H7 failed its own gate, the live proof of the vacuous-pass protection.

## THE P0 ANSWER
(i) The FROZEN H5a and H5c2 grammars HOLD on the file-grouped retrospective split (RETROSPECTIVE_VALIDATION PASS: 14x / 20x NC separation on the held-out side; the +65 fits are NOT file-level selection artifacts; explicitly RETROSPECTIVE — NOT unseen-data validation). (ii) The H7 adjacency-join MECHANISM does NOT hold: NON_PASS NC_INSUFFICIENT_SEPARATION (1.10x < the pre-registered 5x; the denominator-matched per-unit NC reproduces 91% of the held-out rate; K2's one-per-file NC had hidden this — post-audit F1's prediction CONFIRMED live). The 2003 era leg (DIAGNOSTIC): prior-use NONE, but 76/79 files byte-identical between eras (duplicate-dominated, correctly labeled diagnostic-only); the H7 non-separation REPLICATES in 2003 (0.212 vs 0.113).

## CANONICAL STATUS CHANGES (ordered follow-ups)
(a) K2's +65 (H5a 39 + H5c2 26) UPGRADED: CANDIDATE -> RETROSPECTIVE_VALIDATED (advisory; the coverage 2,158/2,427 = 88.88% now carries this status). (b) K2's "H7: 74 join-explained CONFIRMED" DOWNGRADED: the 74 spans remain join-COMPATIBLE observations (74/74 repeatability) but the false-tag-split mechanism is UNVALIDATED at the 5x standard — the residual-325 decomposition becomes "74 join-compatible (mechanism unvalidated) + 251 unexplained", all 325 mechanism-unexplained at this depth. (c) Wiki HOLD unchanged.

## FINDINGS (all disclosed, none blocking)
[P3 x6, documentation-level, disclosed by the executor/QC]: the report's HARD-STOPS cross-reference; the freeze mtime ordering substantiated by code + marker hashes; a PIN_RESULTS key-collision overwriting R12 detail fields (numbers survived in prose, QC-verified); the era rows' missing unit field (closed by the QC's corpus re-execution); two cosmetic whitespace differences in the prereg gates text; QC-prompt label imprecisions (49-ordinary vs 27+22; per-span vs per-unit NC — the run's own labels were correct).

## COVERAGE
PE-MASTER read: the contract, the results JSONs (full), the QC record, the driver's gate section + the zero-assignment grep + the hash. PE-MASTER re-derived: the full gate numbers from the raw JSONL (both grammars + H7 + the pooled NC). NOT_CHECKED: the full 125 KB driver line-by-line (the QC's independent re-execution covers the grammar semantics; PE-MASTER's re-derivations cover the outputs); the R34/R18/R21 lineage reads (the QC's prior-use verification accepted); the 2003 corpus physical bytes beyond the QC's hash checks.

## HANDOFF
This review + the package + the canonical updates (entrypoint row + L31 resolution + ledger +2 + the K2 addendum RESOLUTION append) are persisted next; then RUN C (the wide-record campaign on the remaining 269 no-fit spans + the mechanism-unexplained 325).
