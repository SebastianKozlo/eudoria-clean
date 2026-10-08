# FINAL_REPORT — PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008

## 0. Run identity

```text
RUN_ID            = PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008
RUN_CLASS         = RECORDS_AND_QC_MACHINERY_CORRECTION
REPO_ROOT         = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
EXPECTED_BASE_SHA = 91598a9868037c4954e22e16c535d6a5a671771e
SOURCE_PACKAGE         = docs/audits/PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007/ (READ-ONLY)
PRIOR_SCIENCE_PACKAGE  = docs/audits/PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/ (READ-ONLY)
PRIOR_CORRECTION_PACKAGE = docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/ (READ-ONLY)
OUTPUT_REPO_PATH  = docs/audits/PE_935_CAND4_CHILD_ROOT_NC2_NC3_DECODER_CORRECTION_R1_20261008/
WRITE_ALLOWLIST    = OUTPUT_REPO_PATH/** + AUDIT_ENTRYPOINT.md
NEW_EXE_ACCESS    = NO
NEW_FUNCTION_BODIES = 0
NEW_SCIENCE_EDGE_INTERPRETATIONS = 0
QC_REPAIR_ROUNDS_MAX = 1
RUNTIME = NO (STATIC_ONLY — the client never ran; all buffers synthetic/in-memory)
```

Phases: executor = pe-reconstruction (correction + PRE/POST matrices + regressions A–D);
fresh independent internal QC = pe-master-auditor fresh-context (QC_VERDICT = PASS);
PE-MASTER review = MASTER_ACCEPTED (advisory) persisted VERBATIM as PE_MASTER_REVIEW.md;
persistence/publication = this phase (one commit, MANIFEST LAST).

## 1. Contract identity (verified before any action; re-verified at persistence)

```text
CONTRACT = C:\Users\User\Documents\ChatGPT\PE\PE_935_NC2_NC3_CORRECTION_PROMPT_20261008\OPENCODE_NC2_NC3_CORRECTION.md
SIZE     = 14069 B  (required 14069)     -> MATCH
SHA256   = 3E0BDB58A0CDC1488DE9477A855CEC04D712D492E147CC92CDB3C021B5143B8F  -> MATCH
```

Frozen Desktop inputs (contract §2; re-verified by the executor, the QC and PE-MASTER):

```text
REPORT.md                  11570 B  SHA256 125C47CA195C5D2F782EA1DBCEA0BA1CA65B973CBABEBABDD4F78963C43E83B4  -> MATCH
CONTROL_COUNTERCHECKS.json 132471 B  SHA256 AD8DC2052F714439497A277512944EF729F53BDC94B436CB20EE09FEE6BCC28D  -> MATCH
AUDIT_CHECKS.json           46417 B  SHA256 593B03C3AB87FD274BE8C02E7196D60A961975C95631278C97A8271E528862B7  -> MATCH
```

Frozen repo inputs (disk AND committed-blob equality at BASE, executor INPUT_IDENTITIES.md §3):

```text
SOURCE_PACKAGE 03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py
  17740 B  SHA256 44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405  -> MATCH (blob 48485dca)
SOURCE_PACKAGE 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py
  51943 B  SHA256 529B61DB312AEC338221425B12F2D94DE2BE351B5C62F68DDBA6BF915B007B25  -> MATCH (blob 6fd3d146)
PRIOR_SCIENCE_PACKAGE 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt
  4043 B   SHA256 A0DEFAA16D6934FC307BD88210BCCA59B823C58FB57319A2C090F9ED59AD01E3  -> MATCH (blob 6836b893)
```

## 2. Preflight results (fail-closed)

Executor phase (INPUT_IDENTITIES.md §5, UTC-timestamped queries):

```text
LOCAL_HEAD                    = 91598a9868037c4954e22e16c535d6a5a671771e
origin/master                 = 91598a9868037c4954e22e16c535d6a5a671771e
actual remote master (live ls-remote, available) = 91598a9868037c4954e22e16c535d6a5a671771e
EXPECTED_BASE_SHA             = 91598a9868037c4954e22e16c535d6a5a671771e   (all equal -> GIT_IDENTITY PASS)
OUTPUT_ROOT did not exist (Test-Path False, 2026-10-08T07:16Z); created only after preflight PASS
tracked modifications at start = NONE
foreign untracked census recorded WITHOUT touching (5x PE_935_* packages + experiments/)
```

Persistence phase (this phase): LOCAL_HEAD == origin/master == live remote master ==
EXPECTED_BASE_SHA re-verified (live ls-remote) before writing; still no tracked modifications
outside the allowlist; foreign untracked census unchanged and untouched. No
BLOCKED_INPUT_IDENTITY / BLOCKED_BASE_MISMATCH / BLOCKED_EXTERNAL at any phase.

## 3. The exact NC2/NC3 defects (with the Desktop citations)

Source of both findings: the independent Desktop post-audit
PE_935_NC1_DESKTOP_POST_AUDIT_91598A98_20261007 at AUDITED_SHA 91598a98 (verdict
REQUIRE_CORRECTIONS_FOR_RESIDUAL_MACHINERY; REPORT.md §3/§4/§5 — citations below; the
measurement records are CONTROL_COUNTERCHECKS.json residual_tests:
NON_SIB_TEST_HIDDEN_EDI, INVALID_FF_FAR_CALL_REGISTER, INVALID_LEA_REGISTER — transcribed
VERBATIM into CONTROL_RESULTS_PRE.json as SOURCE_DESKTOP_MEASUREMENT with cited path+size+SHA;
equality with the source JSON verified programmatically 3/3).

### NC2 — production `decode()`, opcode 0x84 (RESIDUAL_NC2_PRODUCTION_NON_SIB_BOUNDARY = CONFIRMED_P2)

Desktop REPORT §3: in 03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py, the 0x84 branch line 236
`size = 2 if mod == 0b11 else (3 if mod == 0b01 else 6)` assigns 6 bytes to the 2-byte memory
TEST form `84 06` (mod=00, rm=6 — no SIB, so the NC1 guard does not block it). On the synthetic
buffer `84 06 BF AA BB CC E8 90 90 90 90 90` @0x0050A3DD..0x0050A3E8 (window stays 0x42;
P1/P3/P4 and all bytes outside the span identical to clean) the production consumed
`84 06 BF AA BB CC` as one TEST, decoded `E8 90 90 90 90` as a CALL and FALSE-PASSED, hiding
`mov edi,0xE8CCBBAA` @0x0050A3DF — an EDI write inside the prohibited P2 interval
(0x0050A3B7, 0x0050A3F6). Desktop measurement: EXPECTED=FAIL, ACTUAL_PRODUCTION=PASS,
ACTUAL_INTERNAL_QC=FAIL, REFERENCE_EDI_WRITE=0x0050A3DF; Desktop capstone 5.0.7 reference
decode: `84 06` = 2-byte `test byte ptr [esi],al`; `BF AA BB CC E8` = 5-byte
`mov edi,0xE8CCBBAA`.

### NC3-A — independent QC `my_decode()`, opcode 0xFF (RESIDUAL_NC3_QC_INVALID_FORMS = CONFIRMED_P2)

Desktop REPORT §4.A: in 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py the FF branch `reg == 0b011`
described FF /3 as PUSH and, for `FF D8` (mod=11), fabricated a harmless 2-byte `push eax` and
FALSE-PASSED the buffer. FF /3 is far CALL with a memory-only operand; the register form FF D8
is an INVALID x86 encoding. Desktop measurement: PRODUCTION=FAIL, INTERNAL_QC=PASS (the false
PASS), CAPSTONE decode stops at 0x0050A3DD (38 of 66 B).

### NC3-B — both decoders, opcode 0x8D (part of RESIDUAL_NC3_QC_INVALID_FORMS)

Desktop REPORT §4.B: the QC engine treated LEA with `mod=11` (`8D C0`) as a valid `lea eax, eax`
and FALSE-PASSED (LEA requires a memory operand); the historical production instead crashed with
`TypeError` (formatting `memoff=None`) — an uncontrolled exception instead of a verdict.
Desktop measurement: INTERNAL_QC=PASS, PRODUCTION=TypeError; CAPSTONE stops at 0x0050A3DD.
Intel SDM citations in the Desktop report: CALL FF /3 memory forms; PUSH FF /6; LEA #UD for a
non-memory source.

None of the three is a SIB regression and none is evidence of an EDI clobber in the real clean
PCG window: they are SYNTHETIC boundary-validator counterexamples against the residual
machinery, disjoint from the (then already closed) NC1.

## 4. Corrections implemented (successors only; historical scripts READ-ONLY; contract §3)

```text
03_SCRIPTS/ctrl4_exact_endpoint_nc23fixed.py  (production successor; 21069 B;
  SHA256 68BEC1AEFDF6A0F32A3ED12F3AED9B72255F8A89AA2F5BA4EFD11C709C4D9F13; 377 lines;
  module INERT at import, NO file I/O, checker catch only (ValueError, IndexError))
00_CONTROL_INTERNAL_QC/qc_ind_ctrl_nc23_own.py  (fresh independent QC successor of the
  historical internal-QC engine; own implementation lineage — own mem_dlen helper, own Insn
  class, own fail-closed linear decode, own P1–P4 checker; only stdlib imports; 71164 B /
  SHA256 31B610745AD4C991237FA36CE197BFA3AA423C9F0530D79FF1664592CA50A703)
```

- NC2 (production 0x84 branch): the sibfixed memory length table is REMOVED BY DESIGN; EVERY
  memory TEST form (mod != 11) is rejected fail-closed BEFORE any length computation — raise
  @line 289 `ValueError: unsupported memory TEST form (mod=00) — FAIL CLOSED` precedes
  `size = 2` @line 291. Register TEST `84 C0` (used in clean) stays supported. Full memory-TEST
  support NOT added (contract §3: preferred minimal repair).
- NC3-A (QC 0xFF branch): the erroneous FF /3 acceptance is REMOVED; only FF /2 mod=11 remains
  accepted, incl. the required FF D2 endpoint; FF D8 rejected fail-closed (`uncovered FF /3
  mod=11`); FF /6 and further forms NOT added (verified: FF F0 raises on both engines). The
  production 0xFF branch is UNCHANGED (it already rejected FF D8).
- NC3-B (both decoders, 0x8D branch): LEA mod=11 is rejected EXPLICITLY BEFORE operand
  formatting — production raise @line 247 precedes the LEA operand formatting @line 282 —
  returning the controlled (False, diagnostic) verdict; the historical production TypeError is
  eliminated (zero TypeError in any POST row). Memory LEA `8D 06` stays supported.
- NC1 PRESERVED: the fail-closed SIB guard runs in EVERY memory-ModRM branch before any
  displacement/length computation (production guard `_reject_sib` def @line 221; call sites
  @lines 245, 287, 299, 328 for branches 0x8B/0x89/0x8D, 0x84, 0x83, 0xFF) — no guard bypassed,
  no rejected byte skipped, decode never continues past an unsupported instruction.
- P1–P4 UNCHANGED: P1 exact `8B F8` @0x0050A3B7; P2 no caller-side EDI write in
  (0x0050A3B7, 0x0050A3F6); P3 exact `57` @0x0050A3F6; P4 exact `FF D2` @0x0050A3F7.
- Decoder independence: no production import in the QC verdict path (production executed
  separately via importlib for comparison only); no shared decoder helper. DISCLOSED shared
  assumption (by design, contract-mandated): both checkers implement the SAME frozen P1–P4
  predicate and 8-case definitions — the agreement is a same-predicate cross-check of two
  independent decoders, NOT a universal x86-decoder proof.
- Unexpected exceptions propagate and are recorded as ERROR, never as an expected FAIL; no
  blanket catch hides a defect.

## 5. PRE reproduction on the REAL historical functions (16/16; AST method; provenance-separated)

Method (CONTROL_RESULTS_PRE.json METHOD_SAFE_AST_EXTRACTION): SAFE AST EXTRACTION ONLY — the
exact historical function/class definitions and needed constants were extracted from the
READ-ONLY committed sources (sibfixed production checker; qc_ind_ctrl_sib_own QC checker) via
ast.parse with whitelisted symbols, static call census and isolated namespaces;
`top_level_executed: false` for BOTH sources — the historical QC top level (which writes
QC_RESULTS.json) was NEVER executed. The SAME eight buffers were run on the REAL historical
functions; all 16 rows (8 cases × 2 checkers) equal the contract's expected PRE:

| case | historical production | historical QC | required PRE |
|---|---|---|---|
| REAL_RECORDED_CLEAN | PASS | PASS | PASS/PASS |
| HISTORICAL_EDI_CLOBBER | FAIL | FAIL | FAIL/FAIL |
| FINAL_PUSH_ESI | FAIL | FAIL | FAIL/FAIL |
| FINAL_PUSH_NOP | FAIL | FAIL | FAIL/FAIL |
| NC1_SIB_HIDDEN_EDI_WRITE | FAIL | FAIL | FAIL/FAIL |
| NC2_NON_SIB_TEST_HIDDEN_EDI | PASS (false pass reproduced) | FAIL | PASS/FAIL |
| NC3_INVALID_FF_FAR_CALL_REGISTER | FAIL | PASS (false pass reproduced) | FAIL/PASS |
| NC3_INVALID_LEA_REGISTER | ERROR (TypeError captured as ERROR, never FAIL) | PASS | ERROR/PASS |

PRE_REPRODUCED = YES (per-case flags). Provenance separation: SOURCE_DESKTOP_MEASUREMENT
(the Desktop residual_tests transcribed VERBATIM with citation, 3/3 deep-equal) is kept
separate from EXECUTOR_REPRODUCTION (this run's own execution of the real historical
functions); no prior verdict was copied as a new measurement; the historical defect mechanisms
were additionally confirmed statically by full reads of both historical scripts (sibfixed 318
lines; qc_ind_ctrl_sib_own 851 lines).

## 6. POST 8-case matrix on the ACTUAL corrected production function (measured actuals)

Buffers: clean re-derived from the published JOIN_WINDOW record (22 instructions, 66 B,
verified against the historical fixture); cases 2–5 keep the NC1 package definitions; cases
6–8 replace EXACTLY the 12 bytes @0x0050A3DD..0x0050A3E8; all windows stay 0x42 with
P1/P3/P4 preserved; bytes outside each mutation span verified identical to clean; all buffers
synthetic/in-memory, full hex+SHA per case recorded in CONTROL_RESULTS_POST.json.

| # | case | production (actual) | independent QC |
|---|---|---|---|
| 1 | REAL_RECORDED_CLEAN | PASS | PASS |
| 2 | HISTORICAL_EDI_CLOBBER | FAIL | FAIL |
| 3 | FINAL_PUSH_ESI | FAIL (P3) | FAIL (P3) |
| 4 | FINAL_PUSH_NOP | FAIL (P3) | FAIL (P3) |
| 5 | NC1_SIB_HIDDEN_EDI_WRITE | FAIL (decoder reject @0x0050A3DD) | FAIL (decoder reject) |
| 6 | NC2_NON_SIB_TEST_HIDDEN_EDI | FAIL (decoder reject @0x0050A3DD) | FAIL (decoder reject) |
| 7 | NC3_INVALID_FF_FAR_CALL_REGISTER | FAIL (decoder reject @0x0050A3DD) | FAIL (decoder reject) |
| 8 | NC3_INVALID_LEA_REGISTER | FAIL (decoder reject @0x0050A3DD) | FAIL (decoder reject) |

Exact rejection mechanisms (both engines, each pinpointed at 0x0050A3DD by prefix decode —
the 38-byte prefix decodes cleanly; the rejection happens exactly AT the span, not by an
accidental earlier parse error):

```text
NC2  : ValueError: unsupported memory TEST form (mod=00) — FAIL CLOSED  (before any length computation)
NC3 FF D8 : ValueError: uncovered FF /3 mod=11  (FF /2 mod=11 only)
NC3 LEA  : ValueError: unsupported LEA register form (mod=11) — FAIL CLOSED  (before operand formatting)
```

Every rejection is the controlled (False, diagnostic) checker verdict — never a TypeError,
never a PASS. ZERO unexpected exceptions in all 16 rows (each engine's checker catches only
(ValueError, IndexError)). Production authenticity: the ACTUAL function was executed via
importlib by the executor, re-executed by the QC (8/8 POST row equality: verdict, full
checker_detail, buffer_len, buffer_hex, buffer_sha256, expected, match) and independently
re-executed by PE-MASTER on PE-MASTER-derived buffers (8/8 match); production script SHA256
68BEC1AEFDF6A0F32A3ED12F3AED9B72255F8A89AA2F5BA4EFD11C709C4D9F13 == pin == POST declared.
Supplementary register-form battery: 6/6 positives decode exactly as before (8B F8, 8B C0,
89 C8, 84 C0, 8D 06, FF D2) and 4/4 negative controls raise with the expected mechanisms —
the correction did not over-reject any required form.

## 7. Regressions A–D (all PASS)

```text
A. Clean boundary regression: the production, QC and PE-MASTER VA/size maps are IDENTICAL to
   the published record — 22 instructions, total 0x42 (66 B), P1 8B F8 @0x0050A3B7 exact,
   P3 57 @0x0050A3F6 exact, P4 FF D2 @0x0050A3F7 exact; call rel32 targets 0x006C0F90 /
   0x006C10B0 / 0x0050A1E0 / 0x005246E0 and je/jmp rel8 targets 0x0050A3C8 / 0x0050A3CC
   recomputed on the QC's own decoder. The NC2/NC3 corrections altered NO clean boundary.
B. Nine historical SIB negative cases (re-derived SAFELY from the READ-ONLY historical QC
   script via ast.parse + ast.literal_eval of the SIB_BATTERY constant — literal-only,
   ZERO code execution): all 9 rejected fail-closed BY BOTH decoders at the DECODER level 9/9.
C. 144-form Desktop sweep preserved: 6 opcode branches (8B/89/8D/84/83/FF) × 3 memory mod
   (00/01/10) × 8 reg, always rm=4 — 144 synthetic SIB forms (full SIB/disp bytes, so a missing
   guard would DECODE rather than raise), 288 decoder calls: ALL 144 rejected AT THE DECODER
   LEVEL by BOTH decoders (144/144 each). Tested at DECODER level — never presented as an
   accidental whole-checker P1 FAIL.
D. NC2/NC3 rejection mechanisms recorded (section 6 above) + independent instruction-level
   diagnosis: the CITED Desktop capstone 5.0.7 reference decode (CONTROL_COUNTERCHECKS.json
   residual_tests, SHA-pinned citation; cited reference != new measurement; nothing installed).
```

## 8. Fresh independent internal QC — terminal gate G1–G6 (every measured value)

QC_ORIGIN = pe-master-auditor fresh-context independent internal QC under direct PE-MASTER
dispatch (NOT a Desktop post-audit; NOT independent of PE-MASTER — recorded). Own successor
implementation lineage (historical internal-QC style kept; only stdlib imports; production
executed separately via importlib for comparison only); shared contract-mandated P1–P4
predicate and 8-case definitions disclosed as shared assumption lineage, by design.
One targeted repair round was used (1 of 1 allowed) — on the QC's OWN static structure
control (docstring exclusion via ast end_lineno + branch anchoring; falsifiability preserved);
the ENTIRE QC was re-executed from scratch after the repair; no stale PASS copied.

| gate | predicate | measured value | result |
|---|---|---|---|
| G1 | 16/16 required matrix rows match | 16/16 (8 cases × 2 engines); QC's clean window byte-identical to the production fixture (SHA 9AC6A7529F1EB2F2424C424E6B3E3BD0BAB133C39CEC18FCC13ADCB02B349398) | PASS |
| G2 | production authenticity | SHA 68BEC1AE…4D9F13 == pin == POST declared; 8/8 POST rows equal QC re-execution (verdict+detail+buffer identity+expected+match); structural guard verification ON CODE LINES (docstring excluded): NC1 guards @245/287/299/328 each after _modrm and before the branch's first length computation; NC2 raise @289 before size @291; NC3-B raise @247 before LEA formatting @282; catch only (ValueError, IndexError) @353; sibfixed 0x84 memory length table REMOVED (explicit sub-check True); 8/8 self-falsifiers (FF F7/FF D8 raise, FF F0 raises, FF D2 decodes, 8D C0 raises, 8D 06 decodes, 84 06 raises, 84 C0 decodes) | PASS |
| G3 | clean map regression | QC's own VA/size map == published record == POST measured map; 22 instructions; total 0x42 (66 B); P1/P3/P4 exact; rel32/rel8 arithmetic recomputed OK | PASS |
| G4 | nine historical SIB cases rejected by both decoders | 9/9 rejected at DECODER level by BOTH decoders (AST-extracted constants; historical QC top level NEVER executed) | PASS |
| G5 | 144-form sweep rejected at DECODER level | 144/144 by the QC engine + 144/144 by the actual production = 288 decoder calls, all rejected at DECODER level; form set == cited Desktop sweep == POST raw_forms | PASS |
| G6 | explicit NC2/NC3 rejections + zero unexpected exceptions | mechanisms explicitly recorded for cases 5–8 on both engines, each pinpointed @0x0050A3DD by prefix decode; 0 unexpected exceptions in 16 rows; no TypeError escape | PASS |

**QC_VERDICT = PASS** (G1..G6 all PASS; executable terminal gate — every condition recorded
individually in 00_CONTROL_INTERNAL_QC/QC_RESULTS.json, 120193 B /
900EF2273ECFA9F125106786522E24CF58C3B3881A889AA68AF10C5BC415D397). An unperformed QC would
have forbidden a positive QC_VERDICT (contract §4); the QC WAS performed (operational
disclosure: two prior QC dispatch sessions returned empty with zero files written — child
session failures, not gate failures; the third fresh-context dispatch completed the QC).

## 9. PE-MASTER review (advisory)

```text
VERDICT               = MASTER_ACCEPTED
AUTHORITY_STATUS      = ADVISORY_PRE_QUALIFICATION
CANONICAL_GATE_EFFECT = NONE
```

PE-MASTER independently executed the actual corrected production function on PE-MASTER-derived
buffers (8/8 match), fully read the corrected production script (377 lines) verifying all
three corrections structurally, verified the QC independence (only stdlib imports; production
executed separately via importlib), the QC_RESULTS.json gate structure, and the PRE/POST
provenance separation. Persisted VERBATIM as PE_MASTER_REVIEW.md. Publication is not
acceptance; the advisory authority status (Q1 absent, PROVISIONAL_UNTIL_QUALIFIED) is unchanged.

## 10. Strongest permitted claims

```text
NC1 = CLOSED_FOR_AUDITED_STATE for 91598a98 (unchanged historical status)
NC2/NC3 = CORRECTED_AND_REVALIDATED_IN_TEST_SCOPE
  (test scope = the 8-case matrix + the 9-case SIB battery + the 144-form sweep;
   established only after the positive QC gate + the PE-MASTER advisory review)
NOT GENERAL_X86_DECODER_PROVEN — never claimed; both engines cover only the window's
opcode universe and reject everything else fail-closed WITHIN THE TESTED SCOPE.
```

## 11. Science preservation (contract §5 — verbatim)

```text
MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32; EXACT = UNRESOLVED.
MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7; EXACT = UNRESOLVED.
ORIGINAL_SCOPE/BUDGET_COMPLIANCE = FAIL; RETROACTIVE_PRIOR_AUTHORIZATION = NO.
WRAPPER_DEPTH = UNRESOLVED; HISTORICAL_LINEAGE_BUDGET_CHARGE = 2/3.
CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED.
MODEL_ROOT_RELATION = UNKNOWN; CHILD_VISUAL_ROLE = UNRESOLVED.
CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED.
EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30,
scoped to examined ACLD+0x18 SF instance.
JOIN_OPERATION = STRONGLY_SUPPORTED.
CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND.
WORLD_INSTANCE = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO.
```

## 12. Audit-state separation

```text
SOURCE_DESKTOP_POST_AUDIT      = PERFORMED_FOR_91598a98 (the NC1 Desktop post-audit whose
                                 residual_tests are the cited NC2/NC3 basis)
NEW_CORRECTION_DESKTOP_POST_AUDIT = NOT_PERFORMED (this run's fresh internal QC is NOT the
                                 future Desktop post-audit of the newly published correction SHA)
HISTORICAL_CLAIM (NC1-era open defects) = superseded by SUPERSESSION.md SN-1/SN-2/SN-3
CURRENT_CANONICAL_STATE (machinery) = corrected successors authoritative within test scope
```

The three historical packages are READ-ONLY and byte-unchanged vs BASE (verified by the
executor, the QC and re-verified at persistence before commit). The historical PRE behavior is
preserved as the honest defect record; the POST behavior is the corrected successors' own
measured state. NC2/NC3 changes VALIDATION MACHINERY ONLY — no historical placement data
created or retracted.

## 13. OPEN_FINDINGS

NONE material. Disclosed (process items, no evidence affected):

1. One targeted QC repair round (1 of 1 allowed) on the QC's OWN static structure control —
   docstring exclusion + branch anchoring; falsifiability preserved; full QC re-run after the
   repair, no stale PASS copied (QC_REPORT.md §9).
2. Two prior QC dispatch sessions returned empty with zero files written (child session
   failures, not gate failures); the third fresh-context dispatch completed the QC; per
   contract, an unperformed QC would have forbidden a positive QC_VERDICT.
3. Executor disclosed two in-scope process fixes (AST census allowlist extended to exception
   constructors in the extracted historical raise statements — inherently non-I/O, before any
   evidence file was accepted; a placeholder hash replaced with the measured value before
   handoff) — no evidence affected (SOURCE_STATE.md §6).
4. Executor run 1 of run_nc23_matrix.py aborted at its own AST static call census guard
   (RuntimeError; no evidence accepted from that run); runs 2–3 measured identical results.
5. Historical records wording backlog documented by the prior NC1 package (not reopened here).

## 14. Terminal governance

```text
NEXT_EXPERIMENT_AUTHORIZED      = NO
CANONICAL_GATE_EFFECT           = NONE
HARD_STOP                       = YES
NEW_CORRECTION_DESKTOP_POST_AUDIT = NOT_PERFORMED
SOURCE_PACKAGES_UNCHANGED       = verified vs BASE blobs and physically, before commit
PUBLICATION                     = one normal commit at BASE 91598a98…; MANIFEST_SHA256.csv
                                  generated LAST; normal fast-forward push; live remote verify
```

Publication does not mean acceptance. This run does not run the next science/correction
experiment. The published exact SHA is returned for the independent Desktop post-audit.
