# PE_MASTER_REVIEW — PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007

AUDITED_RUN = PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007
AUDITED_RANGE = uncommitted working tree at BASE 57ecf3506481e73ca27548ea02e4864904d9883a (records/QC-machinery correction-only; commit pending at persistence)
CONTRACT = C:\Users\User\Documents\ChatGPT\PE\PE_935_NC1_FULL_CONTRACT_REVIEW_EFECB205_20261007\OPENCODE_NC1_CORRECTION_REVIEWED.md — 18981 B, SHA256 D93E793CA0B9EBAA96D2D03F0D0BA31E3F2ED7C234BBBB4BC863631873AE35D3 — verified MATCH
DESKTOP INPUTS = REPORT.md 10543 B / 2324C31F173AF433A7C7A41FCE0CCA2674EEB1F62B4DCDD00F8B8972086E5771 and CONTROL_COUNTERCHECKS.json 46675 B / 2288CB39E357343C4A404F83D6327E5A628547C467D28869A2C34237C0090C00 — verified MATCH
VERDICT = MASTER_ACCEPTED
AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION
CANONICAL_GATE_EFFECT = NONE

## Preflight

LOCAL_HEAD == origin/master == actual remote master == 57ecf3506481e73ca27548ea02e4864904d9883a (live ls-remote). OUTPUT_ROOT created fresh. No tracked modifications at start.

## Claim matrix (load-bearing)

- NC1 SIB false-pass corrected in production (guard rejects mod!=11 & rm==100 before any displacement/length computation in every memory-ModRM branch) — CONFIRMED (full source read, lines 170-175, 194, 234, 244, 272; behavioral execution).
- Production five-case matrix PASS/FAIL/FAIL/FAIL/FAIL — CONFIRMED (PE-MASTER counter-check by execution: importlib of the actual corrected function on PE-MASTER-derived buffers; buffers byte-verified, NC1 bytes identical to the contract counterexample).
- Independent QC checker independently implemented (no production import in verdict path; own modrm/mem_dlen helpers) — CONFIRMED (structural inspection; shared P1-P4 predicate and five-case definitions are contract-mandated and disclosed as shared assumption lineage by QC — this is by design and does not weaken the decoder-independence claim).
- QC five-case matrix identical results — CONFIRMED (QC_RESULTS.json field-level inspection + PE-MASTER witnessed full QC re-execution).
- Production NC1 result came from the actual corrected production function — CONFIRMED (script SHA 44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405 recorded in POST; case-by-case equality QC re-execution vs CONTROL_RESULTS_POST.json; PE-MASTER re-execution equal).
- Clean-window boundary regression (guard changed no boundary; 22-instruction VA/size map identical; total 0x42) — CONFIRMED (QC independent decode + PE-MASTER production execution).
- Pre-correction state provenance separation (Desktop measurement vs executor reproduction; old checker false-pass reproduced read-only) — CONFIRMED (CONTROL_RESULTS_PRE.json field-level inspection).
- True NC1 boundary diagnostic (7-byte MOV+SIB @0x0050A3DD; mov edi,0x90CCBBAA @0x0050A3E4 inside prohibited P2 interval) — CONFIRMED as a SYNTHETIC boundary-validator counterexample (Desktop capstone reference + QC hand-derivation); it does NOT establish an EDI clobber in the real clean PCG window.

## Gate predicates

- Production matrix gate: PASS iff REAL_RECORDED_CLEAN==PASS AND the four mutant cases==FAIL, executed by the ACTUAL corrected production function. Measured: PASS. Negative controls: clobber (P2), esi (P3), nop (P3), NC1 SIB (fail-closed guard). Denominator: 5 cases, all asserted individually.
- QC gate (QC_VERDICT=PASS): PASS iff ALL 10 rows (5 cases x production/independent) match required results AND production-authenticity succeeds AND boundary regression holds. Measured: PASS. Independent oracle legs: QC's own decoder implementation; PE-MASTER execution counter-check; Desktop capstone as cited cross-check (not relabeled).
- Scope gates: NEW_PCG_FUNCTION_BODIES=0, NEW_SCIENCE_EDGE_INTERPRETATIONS=0, NEW_EXE_DECODING=0, RUNTIME=NO — all verified.

## Strongest permitted claims (contract §8)

NC1_SHARED_SIB_FALSE_PASS = CORRECTED_AND_REVALIDATED
CTRL4_BOUNDARY_VALIDATION = SUPPORTED_WITHIN_RECORDED_CLEAN_WINDOW_AND_REGISTERED_FALSIFIERS
NOT GENERAL_X86_DECODER_PROVEN.

## Findings

NONE material. P3_TOOLING_CLEANUP performed (grp1-imm8 operand text; lengths unchanged). QC disclosed two self-corrections of its own tooling before the final run (recorded in QC_REPORT) — process-honesty items, not production defects.

## Coverage

Full read: corrected production script (318 lines), contract (950 lines), QC handoffs, PRE/POST JSONs (field-level). Census: QC script imports/independence, package file census. NOT_CHECKED: the 9 historical QC adversarial mutants' re-execution (persisted results inspected by QC, not re-run), universal x86 decoder correctness, AUDIT_ENTRYPOINT.md full text, runtime (prohibited by contract). PE-MASTER counter-checks were executed outside the package tree; one witnessed full QC re-execution reproduced QC_RESULTS.json byte-identically (deterministic).

SOURCE_DESKTOP_POST_AUDIT = PERFORMED (of 57ecf350)
NEW_CORRECTION_DESKTOP_POST_AUDIT = NOT_PERFORMED
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
