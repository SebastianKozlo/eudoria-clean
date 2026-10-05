# PE_MASTER_REVIEW — PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005

REVIEW_CLASS = PE-MASTER INTERNAL PRE-PUBLICATION REVIEW (phase 2 of the two-phase human-authorized flow of 2026-10-05; performed BEFORE the manifest and BEFORE commit/push). Per the human's instruction this is an internal/pre-publication review, NOT an independent post-audit of the published commit; the independent post-audit of the published SHA remains a separate human-relayed ChatGPT Desktop step. PE-MASTER remains advisory/pre-qualification; CANONICAL_GATE_EFFECT = NONE.

REVIEW_VERDICT = ACCEPTED_WITH_TWO_P3_NOTES

## Independently verified by PE-MASTER (from disk, not from the executor's report)

- Allowlist discipline: HEAD still == BASE c4cb60f at review time; only OUTPUT_ROOT created (32 files); historical C1/C2 packages + AUDIT_ENTRYPOINT.md byte-untouched; the 6 foreign untracked paths untouched.
- P2-1 (pebnd.py): the fix (extents stored SORTED as a list + the module-level order-independent covers_mid_instruction which sorts its input; anchor-conflict policy unchanged) verified by PE-MASTER's own executions: NEW-F yields UNRESOLVED/ANCHOR_CONFLICT with CALL_VALIDATION=NOT_VERIFIED and no promotion under BOTH anchor orders and on both machinery paths; the coverage scan is order-invariant over PE-MASTER's own 500-shuffle stress with the full truth map (strict-interior semantics incl. boundary exclusion); REAL-REFUTE: 0x004B0A02 and 0x004B0A21 re-derive REFUTED_MID_INSTRUCTION with boundary_refuted_by=0x004B0980 through the REAL cached path (no VA special-casing); the E positive control and the three real-EXE CALL controls still PASS with exact targets (0x0070C715->0x00972380, 0x0070DD75->0x00971AD0, 0x0070C742->0x00972DF0).
- P2-2 (x86dec.py, branch A): 66-prefixed near Jcc 0x80..0x8F decode as rel16 (length 5 with one prefix; 67-prefixed REJECTED). PE-MASTER's own execution of NEW-G: first instruction = 5 bytes (C2 measured 7), the E8 at +7 is interior to the MOV immediate -> REFUTED_MID_INSTRUCTION, FAIL_MID_INSTRUCTION, no promotion (C2 fabricated CALL PASS/target 0x00A0000D there).
- P2-3 (cqc_battery.py gate_q2): the corrected Q2 re-derives the effective_address object (present/memop state, operand_width, segment, base/index/scale, raw/signed/effective displacement, address_provenance_status) from the pinned EXE + boundary/entry-this-flow context for every semantically-applicable pin; missing-required = FAIL; spurious EA = FAIL; CSV participates only as a secondary cross-check. PE-MASTER's own count: 46 kind=mem pins, all carrying the EA object, 46/46 = the gate's measured coverage. M5 (base_register ESI->EAX) and M6 (fake provenance) flip the SAME gate_q2 PASS->FAIL with exact failing predicates (committed records verified; reproduced in PE-MASTER's full battery re-run).
- H1: 67 8B 07 -> [BX] verified by PE-MASTER's own execution; the full rm table corrected; lengths unchanged (PE-MASTER's byte-diff shows zero census/pin length changes).
- H2: the validity matrix (0F BA reg 4-7 any mod; 0F 71/72/73 register-only, MMX reg {2,4,6}, SSE2 66 reg {2,4,6} + 66 0F 73 reg {3,7} legal PSRLDQ/PSLLDQ; F2/F3 rejected; reserved sub-opcodes REJECT) verified by PE-MASTER's own executions: 66 0F 73 /3 (0xDB) and /7 (0xF7) mod=3 legal; 0F 71/73 /2 legal; /0 reserved rejected; 0F BA /4 legal, /0 rejected.
- Regression vs C2 (PE-MASTER's own byte-level diff, independent of diff_vs_c2.py): CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv byte-identical; AF3_PROVENANCE_LEDGER.csv byte-identical; C3_OBJECT_SCOPE.json and C2_CENSUS.json content-identical (only the run label differs); CORRECTED_PIN_LEDGER.csv + C1_PIN_EVIDENCE.json differ in EXACTLY 16 boundary fields (driver_declassified_0x004B0A02 + 0x004B0A21 x 4 fields x CSV+JSON: UNRESOLVED/HEURISTIC_START_CANDIDATE/empty -> REFUTED_MID_INSTRUCTION/KNOWN_FUNCTION_ENTRY/0x004B0980/0x004B0980) and NOTHING else; census tally 2218/385/1/6/2 and pin statuses 120/4/2/5/2 unchanged.
- Targeted QC reproduction: PE-MASTER re-ran the full battery (data mode): gates Q1-Q13 PASS (Q1 PASS pre-commit), mutations 7/7 CAUSAL_PASS; CQC_DECODER_UNIT_TESTS.json, CQC_BOUNDARY_COUNTEREXAMPLES.json and AF2_BOUNDARY_TEST_MATRIX.csv reproduced BYTE-IDENTICAL; CQC_FINAL.json differs only in mode=data vs docs + the Q14 gate presence (by design).
- Supersession ledger: PE-MASTER's own quotecheck 10/10 ORIGINAL_EXCERPTs verbatim in their named READ-ONLY sources (9 records); the C2 commit-message verbatim copy == git log -1 --format=%B c4cb60f (machine-checked by PE-MASTER).
- Oracle discipline: ORACLE_INDEPENDENT_RECORDS.json carries 71 fixtures with verbatim objdump (Binutils 2.44) command lines and disassembly; the production decoder is never its own source of truth for the fixtures.
- Claim correction compliance: the C2 "every C1-JSON pin field" / "field-by-field" wordings are superseded (S-P2-01..03); the ArkEstate wording is pinned (instruction start 0x0075136E, immediate 0x00751370, S-P2-09); PRIOR_CANON_ANCHOR_INPUT labeling present.

## Findings (both P3; neither blocks publication)

1. [P3 LABELING] In the NEW-F case record (01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json), the first conflict check is labeled "cached path" while boundary_confirm with explicit entries exercises the uncached walk (the cached path engages only when entries is None). Practical coverage is COMPLETE (the cached extents are permutation-tested directly through covers_mid_instruction; the REAL cached path is proven by REAL-REFUTE and Q6), and the record's own UNCACHED_CROSSCHECK compares both calls — the label alone is imprecise. No action required before publication; note for any future battery revision.
2. [P3 PROCESS-REPORT] INPUT_IDENTITIES states the oracle boundaries were "locked BEFORE the corrected decoder was written" — consistent with all artifacts, but the temporal ordering is executor-process-reported, not independently verifiable from the artifacts alone. Recorded as such.

## Claim statuses (this review's own measurements)

P2_1_BOUNDARY_CACHE = CORRECTED_SORTED_EXTENTS (CONFIRMED by independent execution)
P2_2_66_0F8X_NEAR_JCC = CORRECTED_BRANCH_A_REL16 (CONFIRMED by independent execution)
P2_3_Q2_EFFECTIVE_ADDRESS = CORRECTED_RE_DERIVED_FROM_EXE (CONFIRMED: 46/46 coverage measured; M5/M6 causal)
H1_REG16_RM7 = CORRECTED_BX_TABLE (CONFIRMED)
H2_GROUP_OPCODES = CORRECTED_FAIL_CLOSED_VALIDITY (CONFIRMED)
PRESERVED CORE = CONFIRMED_STATIC_CONDITIONAL (re-measured unchanged: FUN_0070C680 / 0x0070C71E / 89 86 84 00 00 00 / 0xA4=164 B / FUN_00972380)
EXECUTOR SELF-QC = QC_PASS (Q1-Q14 + 7/7 mutations) — reproduced by this review
INDEPENDENT POST-AUDIT OF THE PUBLISHED COMMIT = NOT_PERFORMED (pending; human-relayed ChatGPT Desktop step)

## Coverage honesty

Fully read: the phase-1 delivery notice, FINAL_REPORT.md, QC_REPORT.md, SUPERSESSION_LEDGER.md, INPUT_IDENTITIES.md, HANDOFF.md, PE_MASTER_REVIEW.md placeholder, the corrected pebnd.py + x86dec.py (full), gate_q2 + the mutation harness + the NEW-F/NEW-G construction + the battery header/Q1/CTX of cqc_battery.py; CQC_MUTATION_RESULTS.json, CQC_FINAL.json (gates + Q2/Q5/Q9-Q14 details), CQC_BOUNDARY_COUNTEREXAMPLES.json (13 cases + permutation proofs), CHANGED_FIELDS_VS_C2.json/CSV. Census-level: full parse of the regenerated census CSV + pin CSV with PE-MASTER's own byte-diff vs C2; the c1/c2/c3 script diffs vs C2 (RUN-label-only changes verified). NOT_CHECKED: the remaining prose sections of cqc_battery.py (Q4 vector list, Q6-Q13, Q14 internals) were audited behaviorally via the byte-identical battery reproduction rather than line-by-line (the instrument was executed twice by PE-MASTER with identical results); the 71 oracle fixture outputs were spot-checked against ISA knowledge, not re-run against objdump by PE-MASTER; the executor's in-session chronology is process-reported.

REVIEW_AUTHORITY = ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE.
