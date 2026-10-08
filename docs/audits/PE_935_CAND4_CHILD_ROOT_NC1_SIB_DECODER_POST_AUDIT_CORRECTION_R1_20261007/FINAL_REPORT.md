# FINAL_REPORT — PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007

## 0. Run identity

```text
RUN_ID          = PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007
RUN_CLASS       = RECORDS_AND_QC_MACHINERY_CORRECTION
RUN_TYPE        = CTRL4_SHARED_SIB_BOUNDARY_FALSE_PASS_CORRECTION
REPO_ROOT       = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
BASE_SHA        = 57ecf3506481e73ca27548ea02e4864904d9883a
SOURCE_PACKAGE  = docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/ (READ-ONLY)
OUTPUT_ROOT     = docs/audits/PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007/
NEW_PCG_FUNCTION_BODIES        = 0
NEW_SCIENCE_EDGE_INTERPRETATIONS = 0
NEW_EXE_DECODING               = 0
RUNTIME                        = NO
```

Phases: executor = pe-reconstruction (correction + PRE/POST matrices);
fresh independent internal QC = pe-master-auditor (QC_VERDICT = PASS);
PE-MASTER review = MASTER_ACCEPTED (advisory) persisted verbatim as PE_MASTER_REVIEW.md;
persistence/publication = this phase (one commit, manifest LAST).

## 1. Contract identity (verified before any action)

```text
CONTRACT = C:\Users\User\Documents\ChatGPT\PE\PE_935_NC1_FULL_CONTRACT_REVIEW_EFECB205_20261007\OPENCODE_NC1_CORRECTION_REVIEWED.md
SIZE     = 18981 B  (required 18981)     -> MATCH
SHA256   = D93E793CA0B9EBAA96D2D03F0D0BA31E3F2ED7C234BBBB4BC863631873AE35D3  -> MATCH
```

Frozen Desktop inputs (contract §1; both re-verified by the executor, the QC and the
persistence preflight):

```text
REPORT.md                 10543 B  SHA256 2324C31F173AF433A7C7A41FCE0CCA2674EEB1F62B4DCDD00F8B8972086E5771  -> MATCH
CONTROL_COUNTERCHECKS.json 46675 B  SHA256 2288CB39E357343C4A404F83D6327E5A628547C467D28869A2C34237C0090C00  -> MATCH
```

## 2. Preflight results (fail-closed; measured at execution start and re-verified at persistence)

```text
LOCAL_HEAD        = 57ecf3506481e73ca27548ea02e4864904d9883a
origin/master     = 57ecf3506481e73ca27548ea02e4864904d9883a
actual remote master (live ls-remote) = 57ecf3506481e73ca27548ea02e4864904d9883a
OUTPUT_ROOT       = created fresh only AFTER preflight PASS (executor phase)
SOURCE_PACKAGE    = exists at BASE; 27 physical files; READ-ONLY (unchanged before/after)
tracked modifications at start = NONE
```

No BLOCKED_INPUT_IDENTITY, no BLOCKED_BASE_MISMATCH, no BLOCKED_EXTERNAL occurred.
Full query log: INPUT_IDENTITIES.md §5 and SOURCE_STATE.md §1 (executor phase).

## 3. The exact defect (contract §4 — NC1 / P2)

Both published CTRL_4 decoders (production 03_SCRIPTS/ctrl4_exact_endpoint.py and internal QC
00_CONTROL_INTERNAL_QC/qc_ind_ctrl_own.py of the SOURCE_PACKAGE) omit the SIB byte when
decoding memory ModRM forms with:

```text
mod != 0b11
rm  == 0b100
```

They compute displacement/instruction length as though no SIB exists. This can shift
subsequent decode boundaries and hide an actual EDI write. Authoritative synthetic
counterexample (replacement range 0x0050A3DD..0x0050A3E8, same 12-byte span, window stays 0x42):

```text
bytes: 8B 8C 24 8C 00 00 E8 BF AA BB CC 90

reference x86-32 boundaries:
0x0050A3DD  8B 8C 24 8C 00 00 E8   7-byte MOV with ModRM rm=4 + SIB
0x0050A3E4  BF AA BB CC 90          mov edi,0x90CCBBAA   (writes EDI inside the prohibited P2 interval)
```

The old decoders instead walk a false 6-byte MOV boundary at 0x0050A3E3, swallow
`E8 BF AA BB CC` as a CALL, `90` as NOP — the EDI write at 0x0050A3E4 is never decoded and
both OLD checkers FALSE-PASS the buffer. This is a SYNTHETIC boundary-validator
counterexample: it does NOT establish an EDI clobber in the real clean PCG window.

## 4. Correction strategy implemented (contract §5 — both successors, fail-closed)

Historical scripts remain READ-ONLY. Successors created in the NEW OUTPUT_ROOT:

```text
03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py          (production successor; SHA256 44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405)
00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py       (fresh independent QC engine; own implementation, no production import in its verdict path)
```

Bounded correction applied in EVERY branch of `decode()` that consumes a memory ModRM
operand, BEFORE any displacement/instruction-length computation:

```text
if mod != 0b11 and rm == 0b100:
    reject unsupported SIB form
    FAIL CLOSED
```

- Production: standalone `_reject_sib(mod, rm)` helper (def line 170; call sites lines 194
  (0x8B/0x89/0x8D), 234 (0x84), 244 (0x83), 272 (0xFF)); checker fail-closed catch line 294.
  Verified programmatically per branch: modrm split < guard < first size computation.
- Independent QC: the same predicate fused in its own `mem_dlen` helper (guard-if line 267
  precedes any length return) for 0x8B/0x89/0x8D/0x83; 0x84/0xFF support register forms only
  and raise fail-closed on every non-11 form (which covers SIB).
- The old length logic never runs for such forms. Full SIB decoding NOT implemented (NOT
  required; fail-closed rejection is the preferred minimum-blast-radius solution).
- The P1-P4 exact-endpoint predicate is unchanged: P1 `8B F8` @0x0050A3B7 mov edi,eax;
  P2 no caller-side EDI write inside the required interval; P3 `57` @0x0050A3F6 push edi;
  P4 `FF D2` @0x0050A3F7 call edx.
- Decoder independence (contract §8): no import of the production decoder in the QC verdict
  path, no delegation, no shared decoder helper, no verbatim copy of production's
  ModRM/SIB helper (different helper structure/names/messages; the predicate
  `mod != 0b11 and rm == 0b100` is dictated by the frozen contract and necessarily identical).
  DISCLOSED shared assumption (by design): both checkers implement the same
  contract-mandated P1-P4 predicate and five-case definitions — the agreement is a
  same-predicate cross-check of two independent decoders, NOT a universal x86-decoder proof.

## 5. Measured five-case matrix (contract §7/§8 — the ACTUAL corrected production function; all buffers SYNTHETIC / IN-MEMORY ONLY; EXE never accessed)

Production (CONTROL_RESULTS_POST.json; executed via importlib import of
ctrl4_exact_endpoint_sibfixed.py — the ACTUAL corrected function, NOT a rewritten imitation):

| Case | Expected | Measured | Exact result string |
|---|---|---|---|
| REAL_RECORDED_CLEAN | PASS | PASS | `PASS: P1 exact head mov edi,eax @0x0050A3B7 (8B F8); P2 no caller-side EDI write in (0x0050A3B7, 0x0050A3F6); P3 exact final child argument push edi @0x0050A3F6 (57); P4 exact join call endpoint call edx @0x0050A3F7 (FF D2) — all on verified decode boundaries` |
| HISTORICAL_EDI_CLOBBER | FAIL | FAIL | `P2 FAIL: caller-side EDI write @0x0050A3DD in the required range: 'mov edi, dword ptr [0x00b9d8d0]'` |
| FINAL_PUSH_ESI (57->56) | FAIL | FAIL | `P3 FAIL: exact final child argument push edi @0x0050A3F6 (57) not found (got: push esi [56])` |
| FINAL_PUSH_NOP (57->90) | FAIL | FAIL | `P3 FAIL: exact final child argument push edi @0x0050A3F6 (57) not found (got: nop  [90])` |
| NC1_SIB_HIDDEN_EDI_WRITE | FAIL | FAIL | `window not boundary-decodable (unsupported SIB form (mod=10 rm=100) — FAIL CLOSED) — FAIL closed` |

Independent QC (00_CONTROL_INTERNAL_QC/QC_RESULTS.json; own decoder on its own re-derived
buffers — identical results on all five cases):

| Case | Independent result | Exact result string |
|---|---|---|
| REAL_RECORDED_CLEAN | PASS | `PASS: P1 head mov edi,eax @0x0050A3B7 (8B F8) exact; P2 no caller-side EDI write inside (0x0050A3B7, 0x0050A3F6); P3 final push edi @0x0050A3F6 (57) exact; P4 join call edx @0x0050A3F7 (FF D2) exact — on MY OWN verified decode boundaries` |
| HISTORICAL_EDI_CLOBBER | FAIL | `P2 FAIL: caller-side EDI write @0x0050A3DD in the required range (mov edi, dword ptr [0x00b9d8d0])` |
| FINAL_PUSH_ESI | FAIL | `P3 FAIL: exact final child argument push edi @0x0050A3F6 (57) not found (got: push esi [56])` |
| FINAL_PUSH_NOP | FAIL | `P3 FAIL: exact final child argument push edi @0x0050A3F6 (57) not found (got: nop  [90])` |
| NC1_SIB_HIDDEN_EDI_WRITE | FAIL | `window not boundary-decodable (SIB memory form rejected fail-closed (mod=10, rm=100) before any displacement/length computation — NC1 guard) — FAIL closed` |

The NC1 rejection occurs at the FIRST instruction of the replacement span @0x0050A3DD,
BEFORE any displacement/length computation for it; no instruction at/after that VA is
produced by either decoder. Production-authenticity: every CONTROL_RESULTS_POST.json matrix
row equals the QC re-execution case-by-case (actual / detail string / buffer identity /
expected / match-flag), and the PE-MASTER counter-check (importlib of the actual corrected
function on PE-MASTER-derived buffers) produced 5/5 equal results.

## 6. PRE provenance separation (contract §14)

CONTROL_RESULTS_PRE.json separates, without relabeling:

- `SOURCE_DESKTOP_MEASUREMENT` — the Desktop post-audit's measurement of the OLD checkers on
  the NC1 buffer (transcribed from CONTROL_COUNTERCHECKS.json case sib_hidden_edi_write,
  cited by path+SHA): EXPECTED=FAIL, PRODUCTION_CHECKER=PASS, INTERNAL_QC_CHECKER=PASS,
  REFERENCE_EDI_WRITE=0x0050A3E4, FALSE_PASS_REPRODUCED=YES (capstone 5.0.7 reference).
- `EXECUTOR_REPRODUCTION` (status PERFORMED) — this run's own independent in-memory
  measurement of the OLD production checker (imported READ-ONLY via importlib from the
  SOURCE_PACKAGE; module-level inert; `run_and_write` never invoked; python -B; no .pyc
  residue): five-case matrix on the OLD checker = clean PASS / clobber FAIL / esi FAIL /
  nop FAIL / **NC1 PASS (the false pass)** — `nc1_false_pass_reproduced_by_old_checker =
  YES`. The OLD checker's false old-decode boundaries at the replacement span (6-byte MOV
  @0x0050A3DD, CALL @0x0050A3E3, NOP @0x0050A3E8) and the boundary-shift note are recorded.

The old required endpoint cases remain preserved as authentic historical results.

## 7. P3_TOOLING_CLEANUP (contract §9 — performed)

The known grp1-imm8 (0x83 mod=01) operand-text rendering issue was fixed within the same
decoder-only edit: the immediate is now read from opcode+3 (after the disp8 at opcode+2);
the old code printed the disp byte as the immediate. Regression-tested separately:
`83 4E 2C 02` and `83 66 2C FD` keep size 4; the full clean window decodes to the identical
instruction VA set; CONTROL_RESULTS_POST.json `clean_window_full_decode_listing.
boundary_regression.result` = PASS. No science status is affected by this cleanup.

## 8. Clean-window boundary regression

The corrected decode of the 0x42 published clean window produces the SAME 22-instruction
VA/size map as the published record (identical VA sets AND sizes; total 0x42 = 66 bytes):
0x0050A3B7:2, B9:5, BE:2, C0:2, C2:4, C6:2, C8:4, CC:3, CF:5, D4:2, D6:1, D7:1, D8:5,
DD:6, E3:1, E4:5, E9:3, EC:2, EE:6, F4:2, F6:1, F7:2. Head `8B F8`, final push `57`
@0x0050A3F6 and join call `FF D2` @0x0050A3F7 all exact; window arithmetic (rel32/rel8
targets) recomputed. The NC1 guard and the P3 cleanup changed NO clean-window decode
boundary (QC independent decode + PE-MASTER production execution agree).

## 9. Independent QC (contract §8)

```text
QC_ORIGIN  = FRESH_INDEPENDENT_INTERNAL_QC_BY_PE_MASTER_AUDITOR
             (direct PE-MASTER dispatch; NOT the future Desktop post-audit)
QC_VERDICT = PASS
```

Exact gate (applied as specified): PASS only if (a) ALL 10 rows (5 cases x
production/independent) match the required results, (b) the production-authenticity
establishment succeeds, (c) the clean-window decode boundary regression holds. Measured:
(a) ten_rows_ok = TRUE, (b) authenticity_establishment = SUCCEEDED, (c)
boundary_regression = HOLDS → QC_VERDICT = PASS.

The QC additionally:
- identified the true NC1 boundary itself (own SIB-aware hand-derivation, cross-checked
  against the Desktop capstone reference decode, cited as an independent cross-check and
  NOT relabeled): 7-byte MOV+SIB @0x0050A3DD (disp32 0xE800008C), then
  `mov edi,0x90CCBBAA` @0x0050A3E4 (5 bytes, WRITES EDI) INSIDE the prohibited P2 interval
  (0x0050A3B7, 0x0050A3F6); span covered exactly (7+5=12); clean tail `8B 4E 30` resumes
  @0x0050A3E9;
- ran a 9-form synthetic SIB negative battery (every memory-ModRM branch of both engines,
  mod=00/01/10, incl. the SIB base=101 moffs32 special form): ALL forms rejected
  fail-closed BY BOTH decoders BEFORE any displacement/length computation — zero decoded,
  zero boundary-shifted;
- disclosed two self-corrections of its own QC tooling before the final measured run
  (a self-referential counting defect in its own structural self-check; the grp1-imm8
  sign-extension rendering inherited from the historical internal-QC formula) — honest
  process records, not production defects; and cosmetic implementation differences
  (operand rendering wording; guard message wording) with no effect on any verdict.

## 10. PE-MASTER review

```text
VERDICT               = MASTER_ACCEPTED
AUTHORITY_STATUS      = ADVISORY_PRE_QUALIFICATION
CANONICAL_GATE_EFFECT = NONE
```

PE-MASTER independently executed the actual corrected production function on
PE-MASTER-derived buffers (5/5 match; NC1 bytes verified byte-identical to the contract
counterexample), fully read the corrected production script (guard before any
disp/length computation in every memory-ModRM branch), verified the QC independence
structurally, the PRE/POST provenance separation and the SOURCE_PACKAGE unchanged vs BASE.
Persisted VERBATIM as PE_MASTER_REVIEW.md. Publication is not acceptance; the advisory
authority status (Q1 absent, PROVISIONAL_UNTIL_QUALIFIED) is unchanged.

## 11. Strongest permitted claims (contract §8)

```text
NC1_SHARED_SIB_FALSE_PASS = CORRECTED_AND_REVALIDATED
CTRL4_BOUNDARY_VALIDATION = SUPPORTED_WITHIN_RECORDED_CLEAN_WINDOW_AND_REGISTERED_FALSIFIERS
```

NOT claimed: GENERAL_X86_DECODER_PROVEN (both engines cover only the recorded clean
window's opcode universe and reject everything else fail-closed).

## 12. Science preservation (contract §10 — verbatim; NC1 changes validation machinery only, it does NOT create or retract historical placement data)

```text
FUN_006C66D0 direct field getter [manager+0x68] =
CONFIRMED byte/operation fact

measured store manager+0x68 <- [returned_object+4] =
CONFIRMED physical dataflow fact

CHILD_RESOURCE_PROVENANCE =
STRONGLY_SUPPORTED_MODEL_DERIVED

MODEL_ROOT_RELATION =
UNKNOWN

WRAPPER_DEPTH =
UNRESOLVED

CHILD_VISUAL_ROLE =
UNRESOLVED

CHILD_TO_JOIN_IDENTITY =
STRONGLY_SUPPORTED

EXACT_PARENT =
CONFIRMED_EXACT_SCENEFEEDER_PLUS_30
scoped to examined ACLD path

JOIN_OPERATION =
STRONGLY_SUPPORTED

CAND4_CHILD_ROOT_CLOSURE =
NOT_ESTABLISHED_WITHIN_BOUND

WORLD_XYZ_RECOVERED =
NO

STATIC_BUILDING_CHANNEL =
NOT_ESTABLISHED

HISTORICAL_INSTANCE_DATA_RECOVERED =
NO
```

The established `model/resource -> instance -> [instance+4] -> child` summary is NOT adopted;
only the bounded recorded-producer-path wording applies (WORLD_INSTANCE = NOT_ESTABLISHED,
MODEL_ROOT = NOT_ESTABLISHED, MAIN_VISUAL_CHILD = NOT_ESTABLISHED).

## 13. Governance preservation (contract §11 — verbatim, permanent)

```text
MINIMUM_NEW_ANALYZED_EDGE_COUNT >= 32
EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED

MINIMUM_NEW_FUNCTION_BODIES_OPENED >= 7
EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED

ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL
ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL
ORIGINAL_SCOPE_COMPLIANCE = FAIL

RETROACTIVE_PRIOR_AUTHORIZATION = NO

WRAPPER_DEPTH = UNRESOLVED

HISTORICAL_LINEAGE_BUDGET_CHARGE =
NEW_WRAPPER_HOPS = 2
MAX_NEW_WRAPPER_HOPS = 3
```

## 14. Audit-state separation (contract §16)

```text
SOURCE_DESKTOP_POST_AUDIT = PERFORMED
  (Desktop post-audit of 57ecf3506481e73ca27548ea02e4864904d9883a)

NEW_CORRECTION_DESKTOP_POST_AUDIT = NOT_PERFORMED
  (this run's fresh independent internal QC is NOT the future Desktop post-audit of the
   NEW published correction SHA; set to PERFORMED only when such an independent post-audit
   actually occurs)
```

## 15. Open findings

NONE material.

Disclosed (process-honesty items, not defects of the corrected machinery):
1. QC self-correction 1 — a self-referential counting defect in the QC's own structural
   self-check (naive substring count over its own source inflated the call-site count);
   fixed before the final measured run; the intermediate FAIL was an honest negative of
   the QC's own tooling, not a production finding (QC_REPORT.md §9).
2. QC self-correction 2 — the QC engine's grp1-imm8 operand text initially rendered the
   `and` immediate as `0xfd` (raw byte, inherited from the historical internal-QC rendering
   formula) instead of the sign-extended `0xfffffffd`; fixed before the final measured run;
   instruction lengths and all verdicts unaffected (QC_REPORT.md §9).
3. P3_TOOLING_CLEANUP note — the production grp1-imm8 operand-text rendering fix
   (lengths unchanged; clean-window VA map identical; no science status affected).
4. Historical records wording backlog (Desktop §5.2: "69 x 9" should read "69 x 10"
   original fields; the "fourth" scope-breach recurrence ordinal) — documented by the
   Desktop post-audit as a documentation backlog; NOT reopened by this run (contract §9:
   the harmless historical wording issues do not require reopening C4-C1).

## 16. Terminal governance (contract §20)

```text
NEXT_EXPERIMENT_AUTHORIZED = NO
CANONICAL_GATE_EFFECT     = NONE
HARD_STOP                 = YES
```

Even after this successful correction, no automatic next science anchor is selected
(FUN_006C9700, FUN_006C8BB0, CMO_XYZ_SOURCE_PROVENANCE, placement RE remain NOT
authorized by this run). The next science anchor is a separate HUMAN decision after the
independent Desktop post-audit of the new published correction SHA.
