# PE_935_SAVED_PROOF_REQUALIFICATION_FLASH_PILOT_SAVED_R1_20261021 — FINAL REPORT

RUN_ID = PE_935_SAVED_PROOF_REQUALIFICATION_FLASH_PILOT_SAVED_R1_20261021
RUN_CLASS = SAVED_ONLY_REQUALIFICATION + MODEL-TEAM FLASH PILOT (5 real CLI sessions, no Task/seq transport)
AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE
NEW_SCIENCE_STATUS = PENDING_EXTERNAL_POSTAUDIT
INHERITED_OLD_R2 = UNSEALED_NONPASS preserved (46 actual attempts, 5 orphans, 5 obligations at 3 attempts; untouched)

## 1. Co wykonano
- SETTLE: binding verified (token match, contract SHA 7CEBFAE6...12E3E4B); INPUT_PINS 16/16 PASS before and after (INPUT_RECHECK.json); inherited 455-file snapshot bijection PASS, 0 drift before and after; ORJ-A01..A09 pinned prior postaudit read as prior (not as new instructions).
- SOURCE_ADMISSION.json written BEFORE the first semantic read of packets (hash-read is not semantic read). Closed material: F1=26, F2=92 (explicit gap 182383..182429), F3=79 rows; 197 total; body-fragment cap 10, used 5. No new H5/LEA/00414130/EXE/runtime; no disk scan.
- Faza0 (authorized by contract): minimal CLI tooling created in OUTPUT/CONTROL only (run_role.py, recover_result.py, prompt authoring), based on the PINNED, UNMODIFIED MODEL_TEAM_R2 driver.py/postprocess.py. Exclusive reservation BEFORE process; literal prompt file + pin; direct exe, shell=False; -f last; child env without NODE_TLS_REJECT_UNAUTHORIZED and without OPENCODE_CONFIG (coordinator scoped config would hide the opencode provider; removal restores the validated env surface); raw bytes stdout/stderr; DB mode=ro parity; explicit terminal RESULT also on failure. Synthetic tests: 14/14 PASS, 0 API calls (duplicate reservation, unknown role, active limit, prompt missing, pin drift, dup-key rejection, list handling, JSON round-trip, Unicode parity, recovery-without-launch).
- Roles (all real, separate CLI sessions, agent=build, inline-only, 1 attempt each, 0 retries): PLANNER (nask-glm/glm-5-3 medium) -> F1/F2/F3 (opencode/glm-5.3-flash-free) -> fresh REVIEWER (nask-glm/glm-5-3 medium). Parity PARITY_OK 5/5; tool_calls 0/5; DB census delta exactly 5; no additional unauthorized sessions (3 preexisting pe-master sessions predate the run window). REQUEST_EFFORT=NOT_OBSERVED; SERVER_EFFECTIVE_EFFORT=UNKNOWN; no 400k context claim.

## 2. Wyniki naukowe (closed 197 rows; master row-level recomputation, not model self-report)
- F1: wrapper 0085B840 mechanics CONFIRMED; reader ECX comes from the SECOND CALL 004123D0 (rows 4702..4704) - independently convergent with OAWC-A05 direction without showing the correction key. REVIEWER materially corrected the worker's slot-distinction premise: all three LEAs (rows 4692/4694/4701) target the SAME slot B+0x74 under ESP shift; master recomputation CONFIRMS this aliasing (convergent with pinned ORJ-A01, not shown to models). Bit-equality of the two lookup results remains UNVERIFIED (same slot, different second argument, 004123D0 body semantics = PRIOR_DECOMP_NOT_BYTE_CLOSED premise). Arity/types of 004154F0/008544D0 NOT proved by shown rows (CONFIRMED).
- F2: RET 0x10 = 16B/4-DWORD argument-area footprint CONFIRMED (row 182498); frame balance 0x38 prologue / 0x28+0x10 epilogue recomputed by master; base call 0085B1B0 image reads entry+4/+8/+C (recomputed); three PUSHes prove ONLY the base-call image; formal arity/types of derived ctor 00528E50 NOT provable; [ESP+0x48]@182437 = entry+0x10 only under gap-balance + 0085AD60-cleanup premises. Consistent with OAWC-A04 separation; no complete-ctor claims; explicit gap treated as missing evidence.
- F3: node-identity facts, bidirectional +4/+8 pair writes, +C child-chain recursion and sentinel self-links CONFIRMED as row-level observations; UNIQUENESS of the intrusive-linked-list interpretation REJECTED - concrete two-level/tree countermodels fit all shown rows (worker + independent reviewer countermodel); owner join NOT established (no node-to-owner tie-back shown); no library/class name used. Consistent with OAWC-A06.

## 3. Proces — honest failures (no retry used; see QC_FINDINGS.json PF1..PF6)
- PF1 (P2): collector crash on CompletedProcess.pid after the PLANNER session; additive recovery of the EXISTING session (DB mode=ro + parity); NOT a model retry; same defect class as the pinned MODEL_TEAM_R2 driver crashes; patched before F1.
- PF2 (P2): REVIEWER short user-message nonce had a fabricated tail (payload carried the true nonce; model echoed the payload nonce correctly); message/payload nonce equality obligation violated once; no retry permitted.
- PF4 (P2): word caps exceeded by all five roles on the content measure (PLANNER 282/250, F1 480/350, F2 352/350, F3 365/350, REVIEWER 932/900); honest failures; both raw-token and content measures in ACCEPTANCE.json.
- PF3/PF5/PF6 (P3): one stray local python invocation with invalid path + stderr suppressed (no side effects); planner schema lacked nonce echo field (authoring/Checker spec defect, not planner defect); initial word measure included JSON syntax (corrected to content measure).

## 4. Status algebra
- Deliveries: 5/5 roles DELIVERED, 5/5 PARITY_OK, 5/5 parseable JSON (2 bare, 3 single fenced), nonce echo 4/5 correct (PF5), word caps 0/5 content-pass (PF4), inline-only 5/5.
- Claims: 15 master-dispositioned claims in CLAIMS.json (worker/reviewer/master statuses kept separate). Local science convergence with OAWC-A04/A05/A06 and ORJ-A01 directions is an observation of this run, not a promotion of those corrections to CONFIRMED beyond their existing status.
- Old R2: unchanged UNSEALED_NONPASS; no checker/reservation/manifest edits; no orphan removal; publication of old R2 NOT performed and NOT claimed.

## 5. Granice
- Same model family for all five roles; no cross-engine check inside this run; n=3 flash jobs is NOT a general capability claim about Flash Free or reviewer effectiveness.
- The two pinned source-extract lineages (R2 extracts) were re-hashed (pins PASS) but their derivation from H5 was not re-executed here; reliance is on the pinned deep postaudit verification.
- Disconnected fragments: complete function coverage NOT claimed for any packet; all callee bodies (004123D0, 004154F0, 008544D0, 00527AB0, 0085B1B0, 0085AD60, 00414130, 00529DE0, 00413C70, 008C3580, 0095D500) remain outside the shown rows.
- WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN.

## 6. FIRST_MISSING_EDGE
Derived ctor 00528E50 stack-map closure: the unshown gap rows 182383..182429 (esp. 0085B1B0 RET n and 0085AD60 cleanup convention) are the cheapest next window; five unopened LEA and 00414130 remain later-contract frontier (FIRST_MISSING_EDGE.json).

## 7. Publikacja
Sanitized publication of this report + derived claims + gates + QC findings + additive errata (OAWC-A01..A08, ORJ-A01..A09) per contract section 10: fresh isolated worktree from LIVE dfda081b..., per-file allowlist, pinned pub_manifest.py create->commit->verify->FF push->remote verify; 8f80190 excluded from ancestry; no raw packets/instructions/prompts/answers/stdout/DB/config/env/secrets published; PUBLICATION_RESULT.json only in the RECEIPT root. Publication is NOT scientific acceptance. See PUBLICATION_RESULT.json.

## 8. Artefakty
SOURCE_ADMISSION, BASELINE, CORRECTION_LEDGER, CLAIMS, ROLE_LEDGER, MODEL_ATTESTATION, PACKET_COVERAGE, ACCEPTANCE, QC_FINDINGS, FIRST_MISSING_EDGE, INPUT_RECHECK, SELF_REVIEW_1/2, STAGE_ACCEPTANCE_GATES.csv, artifact_index.csv, HANDOFF, REPORT, MANIFEST_SHA256.csv (LAST, self-excluded). CONTROL/ holds the phase0 tools, synthetic tests, prompts (with nonces) and per-role attempts (prompt.txt, stdout.bin, stderr.bin, receipts, metadata, original answers) - all LOCAL_ONLY.

HARD_STOP = YES (contract scope exhausted; no arithmetic test, no additional PE experiment, no new model sessions)
