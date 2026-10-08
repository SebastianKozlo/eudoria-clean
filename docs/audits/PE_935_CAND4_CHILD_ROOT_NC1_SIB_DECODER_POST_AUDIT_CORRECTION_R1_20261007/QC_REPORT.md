# QC_REPORT — Fresh Independent Internal QC of the NC1 correction

```text
RUN_ID      = PE_935_CAND4_CHILD_ROOT_NC1_SIB_DECODER_POST_AUDIT_CORRECTION_R1_20261007
RUN_CLASS   = RECORDS_AND_QC_MACHINERY_CORRECTION (correction-only; ZERO new science / ZERO new RE)
QC_ORIGIN   = FRESH_INDEPENDENT_INTERNAL_QC_BY_PE_MASTER_AUDITOR
              (direct PE-MASTER dispatch of 2026-10-07, per frozen human-authorized
              contract §8; this QC is NOT the future Desktop post-audit)
AUDITED_EXECUTOR = pe-reconstruction (executor phase: 03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py,
              03_SCRIPTS/run_nc1_matrix.py, CONTROL_RESULTS_PRE.json, CONTROL_RESULTS_POST.json,
              INPUT_IDENTITIES.md, SOURCE_STATE.md)
QC_VERDICT  = PASS
EXECUTION   = python -B (bytecode writing disabled; post-run residue scan: NONE in
              OUTPUT_ROOT and NONE in the READ-ONLY SOURCE_PACKAGE); all buffers
              SYNTHETIC / IN-MEMORY ONLY; EXE never accessed; no file outside this
              QC's own three outputs was written, staged, committed or pushed
```

Machine-readable results: `00_CONTROL_INTERNAL_QC/QC_RESULTS.json` (deterministic — no
timestamps). QC engine: `00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py` (this QC's own
independent implementation; the FINAL engine version was executed once, exit code 0, and is
pinned by the QC_RESULTS.json provenance written after its last edit; two earlier intermediate
executions disclosed self-corrections of my own QC tooling, see §9).

---

## 1. Scope and gate

Frozen dispatch contract (read IN FULL by this QC before any action):

```text
PATH      = C:\Users\User\Documents\ChatGPT\PE\PE_935_NC1_FULL_CONTRACT_REVIEW_EFECB205_20261007\OPENCODE_NC1_CORRECTION_REVIEWED.md
SIZE      = 18981 bytes   (required 18981)      -> MATCH
SHA256    = D93E793CA0B9EBAA96D2D03F0D0BA31E3F2ED7C234BBBB4BC863631873AE35D3   -> MATCH
```

The QC gate (dispatch §8, applied exactly):

```text
QC_VERDICT = PASS only if
  (a) ALL 10 rows (5 cases x production/independent) match the required results,
  (b) the production-authenticity establishment succeeds,
  (c) the clean-window decode boundary regression holds.
Any deviation -> QC_VERDICT FAIL/PARTIAL with exact rows.
```

Measured: (a) ten_rows_ok = TRUE, (b) authenticity_establishment = SUCCEEDED,
(c) boundary_regression = HOLDS -> **QC_VERDICT = PASS**.

## 2. Method

1. Re-verified every pinned input physically (contract, both Desktop inputs, window record,
   production script, matrix runner, old READ-ONLY checker, both CONTROL_RESULTS_*.json —
   sizes and SHA256 in §3).
2. Re-derived the 0x42 clean window MY OWN way from the published record
   (`PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007/01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt`,
   BASE-blob-verified) with my own regex parser: 22 instructions, first VA 0x0050A3B7,
   contiguous boundaries, total 0x42. My window SHA256
   `9AC6A7529F1EB2F2424C424E6B3E3BD0BAB133C39CEC18FCC13ADCB02B349398` — byte-identical to the
   executor's declared fixture (extracted as TEXT from its script — no execution for the
   comparison source) and to the CONTROL_RESULTS_POST.json clean buffer.
3. Built the five matrix buffers MY OWN way (mutation builders with fail-closed asserts on the
   replaced original bytes); verified byte-identity of my NC1 buffer with the executor's declared
   Desktop-case buffer and with the Desktop CONTROL_COUNTERCHECKS.json
   `sib_hidden_edi_write` case bytes.
4. Wrote MY OWN independent x86-32 decoder + P1-P4 exact-endpoint checker (§4), with the NC1
   defect fixed in it (fail-closed SIB rejection before any displacement/length computation).
5. Ran the mandatory five-case matrix on MY checker.
6. Importlib-executed the ACTUAL corrected production checker
   (`03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py` — module inert at import, full-read verified:
   no file I/O, no writers; no writer ever called) on the SAME five buffers, and compared every
   CONTROL_RESULTS_POST.json matrix row to my re-execution case-by-case.
7. Established production authenticity (script SHA + row equality + structural guard-coverage
   check with measured line ranges, complementing my FULL READ of the production source to EOF).
8. Ran the clean-window boundary regression on MY decoder (22-instruction VA/size map vs the
   published record and vs the POST.json measured map; head/final-push/join-call endpoints;
   window arithmetic recomputed).
9. Ran my own SIB-aware true-boundary diagnostic over the NC1 replacement span (separate from
   the checker's fail-closed verdict path) and cross-checked against the Desktop capstone
   reference decode.
10. Ran a 9-form SIB negative battery (every memory-ModRM branch of both engines, mod=00/01/10,
    including the SIB base=101 moffs32 special form) — all forms must be rejected fail-closed by
    BOTH decoders.

## 3. Input identities (all physically re-measured by this QC)

| Input | Size | SHA256 | Required pin |
|---|---|---|---|
| Dispatch contract | 18981 | D93E793CA0B9EBAA96D2D03F0D0BA31E3F2ED7C234BBBB4BC863631873AE35D3 | MATCH |
| Desktop REPORT.md | 10543 | 2324C31F173AF433A7C7A41FCE0CCA2674EEB1F62B4DCDD00F8B8972086E5771 | MATCH |
| Desktop CONTROL_COUNTERCHECKS.json | 46675 | 2288CB39E357343C4A404F83D6327E5A628547C467D28869A2C34237C0090C00 | MATCH |
| Published window record (01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt, PROVENANCE pkg) | 4043 | A0DEFAA16D6934FC307BD88210BCCA59B823C58FB57319A2C090F9ED59AD01E3 | BASE-blob-verified |
| Corrected production script (03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py) | 17740 | 44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405 | equals POST.json claim |
| Matrix runner (03_SCRIPTS/run_nc1_matrix.py) | 26734 | 0655CEBFD6A55FB57BA86B78CCEBBC0378258A3918701F4CA97DD115D89E5C31 | — |
| Old production checker (SOURCE_PACKAGE, READ-ONLY) | 20592 | FDB5F16E6F9A6352030DD2F4D9523E1CAA0AB924F2112DDEC787CC7B3A84A330 | BASE-blob-verified |
| CONTROL_RESULTS_POST.json | 37353 | C28A32EF9A9B13EDA596B70FC8DE1B69636E9337039454D17C78C45B4581624A | — |
| CONTROL_RESULTS_PRE.json | 8289 | 4D3DB2E3F1F7FECBA200618FA6BC8A2A3895F57B3CBE02E879D1D4F8E8B1ADC9 | — |

Repository state during this QC: LOCAL_HEAD = 57ecf3506481e73ca27548ea02e4864904d9883a
(= EXPECTED_BASE_SHA; unchanged); `git status` — the same 6 pre-existing untracked paths as the
executor's preflight plus this run's OUTPUT_ROOT; ZERO tracked modifications; SOURCE_PACKAGE
unchanged (27 physical files). This QC staged/committed/pushed NOTHING (not assigned).

## 4. Independence statement (code lineage, disclosed honestly)

- **My reference decoder/checker** (`00_CONTROL_INTERNAL_QC/qc_ind_ctrl_sib_own.py`): the
  CORRECTED SUCCESSOR of the historical internal-QC implementation
  (`SOURCE_PACKAGE 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_own.py`, pe-master-auditor lineage,
  READ-ONLY, BASE-blob-verified). It keeps the historical internal-QC style (own
  `mem_dlen` — the successor of `modrm_len`; own `Insn` class; own fail-closed linear decode;
  own P1-P4 exact-address/byte-form checker) and fixes the NC1 defect in it: a memory ModRM
  form with `mod != 0b11 and rm == 0b100` (SIB byte present) raises inside `mem_dlen` BEFORE any
  displacement/length arithmetic, in every memory-ModRM branch it supports (0x8B/0x89/0x8D and
  0x83 via `mem_dlen`; 0x84 and 0xFF support register forms only and raise on every non-11 form,
  which covers SIB). Full SIB decoding is NOT implemented (NOT required).
- **Production** (`03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py`, pe-reconstruction lineage):
  a standalone `_reject_sib(mod, rm)` helper called after `_modrm` and before the branch's
  inline size/memoff computation, in every memory-ModRM branch (0x8B/0x89/0x8D, 0x84, 0x83,
  0xFF).
- No import of the production decoder in my verdict path; no delegation of decoding to
  production; no shared decoder helper; no verbatim copy of production's ModRM/SIB helper
  (different helper structure — fused-in-`mem_dlen` vs standalone `_reject_sib` — different
  names, different messages; the *predicate* `mod != 0b11 and rm == 0b100` is dictated by the
  frozen contract §5 and is therefore necessarily identical). The ModRM byte splitter
  (`mrm_split`) is my own field-mask form of an architecturally-fixed 1-line idiom.
- **DISCLOSED SHARED ASSUMPTION (by design)**: BOTH checkers implement the SAME
  contract-mandated P1-P4 exact-endpoint predicate and the SAME five-case matrix definitions
  (frozen contract §6-§8). The predicate and case set are contract-fixed; the implementations
  are independent. Their 10/10 agreement is therefore a same-predicate cross-check of two
  independent decoders — NOT a universal x86-decoder correctness proof, and NOT claimed.
- The ACTUAL production function was executed separately (importlib) ONLY for comparison; the
  production module is inert at import (verified by full read to EOF: 318 lines, no file I/O, no
  writers) and no writer was ever called.

## 5. Mandatory five-case matrix — both implementations, same re-derived buffers

Buffers re-derived MY OWN way (clean window from the published record; mutants via my own
builders with fail-closed asserts on the replaced original bytes). All 66 bytes / 0x42 window;
buffer SHA256 recorded in QC_RESULTS.json for every case.

| Case | Required (prod / indep) | Production re-executed by this QC | My independent checker | Row OK |
|---|---|---|---|---|
| REAL_RECORDED_CLEAN | PASS / PASS | **PASS** | **PASS** | YES |
| HISTORICAL_EDI_CLOBBER (8B 3D D0 D8 B9 00 @0x0050A3DD) | FAIL / FAIL | **FAIL** (P2 @0x0050A3DD) | **FAIL** (P2 @0x0050A3DD) | YES |
| FINAL_PUSH_ESI (57→56 @0x0050A3F6) | FAIL / FAIL | **FAIL** (P3: push esi) | **FAIL** (P3: push esi) | YES |
| FINAL_PUSH_NOP (57→90 @0x0050A3F6) | FAIL / FAIL | **FAIL** (P3: nop) | **FAIL** (P3: nop) | YES |
| NC1_SIB_HIDDEN_EDI_WRITE (8B 8C 24 8C 00 00 E8 BF AA BB CC 90 @0x0050A3DD..E8) | FAIL / FAIL | **FAIL** (fail-closed SIB guard) | **FAIL** (fail-closed SIB guard) | YES |

Exact measured details (both implementations, per case):

- CLEAN — production: `PASS: P1 exact head mov edi,eax @0x0050A3B7 (8B F8); P2 no caller-side
  EDI write in (0x0050A3B7, 0x0050A3F6); P3 exact final child argument push edi @0x0050A3F6
  (57); P4 exact join call endpoint call edx @0x0050A3F7 (FF D2) — all on verified decode
  boundaries`. Mine (own wording): `PASS: P1 head ... exact; P2 ...; P3 ...; P4 ... — on MY OWN
  verified decode boundaries`.
- CLOBBER — both: `P2 FAIL: caller-side EDI write @0x0050A3DD in the required range
  (mov edi, dword ptr [0x00b9d8d0])` (production quotes the operand; word-for-word same
  verdict).
- ESI — both: `P3 FAIL: ... push edi @0x0050A3F6 (57) not found (got: push esi [56])`.
- NOP — both: `P3 FAIL: ... (got: nop  [90])`.
- NC1 — production: `window not boundary-decodable (unsupported SIB form (mod=10 rm=100) —
  FAIL CLOSED) — FAIL closed`; mine: `window not boundary-decodable (SIB memory form rejected
  fail-closed (mod=10, rm=100) before any displacement/length computation — NC1 guard) — FAIL
  closed`. Both are fail-closed guard rejections at the FIRST instruction of the replacement
  span; no instruction at/after 0x0050A3DD was produced by either decoder.

Every CONTROL_RESULTS_POST.json matrix row equals my production re-execution case-by-case
(actual, checker_detail exact string, buffer hex, buffer SHA256, expected, match-flag — all
equal for all five cases). My NC1 buffer is byte-identical to the executor's declared
Desktop-case buffer and to the Desktop CONTROL_COUNTERCHECKS.json `sib_hidden_edi_write`
case bytes.

## 6. Production-result authenticity establishment

(i) **The actual corrected production function was executed** (importlib import of
`03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py`; its `ctrl4_exact_endpoint` run on all five of MY
buffers). Its exact NC1-buffer detail string, recorded verbatim:
`window not boundary-decodable (unsupported SIB form (mod=10 rm=100) — FAIL CLOSED) — FAIL closed`.

(ii) **Script SHA256** measured by this QC:
`44155437F20FA6DA9D6847A236F708C7F2A40F26BABE71424B21C325B4FB4405` — equals the
CONTROL_RESULTS_POST.json `production_checker.script_sha256` claim; and every POST.json matrix
row equals my re-execution case-by-case (5/5 rows: actual/detail/buffer identity/expected/
match-flag all equal). The NC1 result therefore came from the actual corrected production
function.

(iii) **Structural guard coverage** (text-measured line positions in the production source,
complemented by this QC's FULL READ of the production source to EOF — 318 lines — before any
execution):

```text
guard def   : line 170   (def _reject_sib(mod, rm): ... raise ... "FAIL CLOSED" at line 175)
guard calls : lines 194 (0x8B/0x89/0x8D branch, start 192: _modrm@193 -> guard@194 -> first size@196),
              234 (0x84 branch, start 232: _modrm@233 -> guard@234 -> first size@236),
              244 (0x83 branch, start 242: _modrm@243 -> guard@244 -> first size@247),
              272 (0xFF branch, start 270: _modrm@271 -> guard@272 -> first size@274)
checker catch: line 294  (except (ValueError, IndexError) -> return False, "... — FAIL closed")
```

In EVERY memory-ModRM branch the guard call site is AFTER the ModRM split and BEFORE the
branch's first size/displacement computation (verified programmatically per branch: modrm <
guard < first-size, all four branches TRUE). These are the only ModRM-consuming branches in the
production decoder; behavioral evidence (the five-case matrix and the 9-form battery below)
agrees.

Behavioral + structural evidence together: the production NC1 result is the corrected
function's fail-closed guard rejection, and the guard covers every memory-ModRM branch, not only
the exact `8B 8C` counterexample.

## 7. Clean-window decode boundary regression (my independent decode)

My decoder over MY re-derived window produces the SAME 22-instruction VA/size map as the
published record (identical VA sets AND sizes; 22 instructions; total 0x42 = 66 bytes):

```text
0x0050A3B7:2  B9:5  BE:2  C0:2  C2:4  C6:2  C8:4  CC:3  CF:5  D4:2  D6:1  D7:1
0x0050A3D8:5  DD:6  E3:1  E4:5  E9:3  EC:2  EE:6  F4:2  F6:1  F7:2
```

- head exact: `8B F8` mov edi,eax @0x0050A3B7 — TRUE
- final push exact: `57` push edi @0x0050A3F6 — TRUE
- join call exact: `FF D2` call edx @0x0050A3F7 — TRUE
- my map also identical to the POST.json `measured_va_size_map` — TRUE
- window arithmetic recomputed on MY decoder: call rel32 targets 0x006C0F90 / 0x006C10B0 /
  0x0050A1E0 / 0x005246E0 and the join `call edx`; je/jmp rel8 targets 0x0050A3C8 / 0x0050A3CC
  — all exact.

The NC1 guard (and the executor's authorized P3 tooling cleanup) changed NO clean-window decode
boundary.

## 8. NC1 true-boundary diagnostic (my own computation, separate from the verdict path)

My checker's verdict on the NC1 buffer is the FAIL-CLOSED SIB-guard rejection — the
contract-preferred minimal CORRECT behavior. Additionally, my own SIB-aware decode of the
replacement span (computed by this QC from the bytes; recorded in QC_RESULTS.json
`nc1_true_boundary_diagnostic`) identifies what the guard rejects:

```text
0x0050A3DD  8B 8C 24 8C 00 00 E8   mov ecx, [esp + disp32]   ; 7 bytes
             || || || ||------||
             || || || \\-> disp32 little-endian = 0xE800008C (signed -0x17FFFF74)
             || || \\-> SIB 0x24: scale=0, index=none(100b), base=esp(100b)
             || \\-> ModRM 0x8C: mod=10 reg=001(ecx) rm=100 -> SIB + disp32
             \\-> opcode 8B (MOV r32, r/m32)
0x0050A3E4  BF AA BB CC 90          mov edi, 0x90CCBBAA       ; 5 bytes, WRITES EDI
0x0050A3E9  (= span end 0x0050A3DD+12) — clean tail 8B 4E 30 resumes exactly there
```

The EDI write at 0x0050A3E4 is INSIDE the prohibited P2 interval (0x0050A3B7, 0x0050A3F6)
exclusive — so the TRUE expected verdict for this buffer is FAIL, and the guard rejection is
the correct minimal behavior: a genuinely hidden EDI write can no longer be boundary-shifted
out of P2's sight. My hand-derivation (full arithmetic recorded in QC_RESULTS.json
`hand_derivation`) is MY OWN computation; the Desktop capstone 5.0.7 reference decode agrees
with my boundaries (7-byte MOV @0x0050A3DD; mov edi, 0x90ccbbaa @0x0050A3E4, 5 bytes) — cited
as an INDEPENDENT cross-check, NOT relabeled as my measurement. The old-defect mechanism (the
SIB-less 6-byte length, boundary 0x0050A3E3, `E8 BF AA BB CC` swallowed as CALL, `90` as NOP,
EDI write never decoded) is documented arithmetically and independently confirmed by the
Desktop `production_decode` listing and the executor's CONTROL_RESULTS_PRE.json old-decode
reproduction (both cited, neither relabeled as my measurement).

## 9. Negative controls and process honesty

- **9-form SIB negative battery** (both decoders, every memory-ModRM branch, mod=00/01/10,
  including the SIB base=101 moffs32 special form): ALL 9 forms are REJECTED fail-closed BY
  BOTH decoders BEFORE any displacement/length computation (my engine: `mem_dlen` guard for
  0x8B/0x89/0x8D/0x83, register-only non-11 raises for 0x84/0xFF; production: `_reject_sib`
  guard in every ModRM branch). Zero decoded, zero boundary-shifted. Falsifier: any NO-RAISE or
  any decoded SIB instruction would have failed Q9; none occurred.
- **Disclosed self-corrections of my own QC engine (honest process record, both before the
  final measured run):**
  1. First run exposed a self-referential counting defect in my own structural self-check
     (a naive substring count over my own source counted the check's own string literals —
     inflating the call-site count and failing Q6). Fixed by counting actual call-site LINES
     via regex; disclosed in the script comment. The first run's FAIL was an honest negative
     intermediate result of MY tooling, not a production finding.
  2. My grp1-imm8 (0x83 mod=01) operand text initially rendered the `and` immediate as `0xfd`
     (the raw byte, inherited from the historical internal-QC rendering formula) instead of
     the sign-extended `0xfffffffd`. Fixed (sign-extend before masking); instruction LENGTHS and
     all verdicts were unaffected in both runs; my final listing now matches the published
     record's rendering exactly.
- Cosmetic implementation differences disclosed (no effect on any verdict/boundary): production
  renders mod=00 indirect operands as `eax, [ecx]`, mine as `eax, dword ptr [ecx]`; guard
  message wording differs between the two engines (both fail-closed).

## 10. Verdict

```text
QC_VERDICT = PASS
  ten_rows_ok                  = TRUE   (all 10 rows: 5 cases x production/independent)
  authenticity_establishment   = SUCCEEDED
  boundary_regression           = HOLDS

NC1_SHARED_SIB_FALSE_PASS = CORRECTED_AND_REVALIDATED
CTRL4_BOUNDARY_VALIDATION =
  SUPPORTED_WITHIN_RECORDED_CLEAN_WINDOW_AND_REGISTERED_FALSIFIERS

NOT CLAIMED: GENERAL_X86_DECODER_PROVEN
  (both engines cover only the recorded clean window's opcode universe and reject
   everything else fail-closed; the matrix agreement is a same-predicate cross-check
   of two independent decoders, per §4)
```

This QC verifies VALIDATION MACHINERY only. It creates NO science, retracts NO historical
result, and does NOT adjudicate any claim beyond the frozen contract's five-case matrix,
authenticity and boundary-regression scope.

## 11. Audit-state separation and science preservation (verbatim, contract §10/§16)

```text
SOURCE_DESKTOP_POST_AUDIT = PERFORMED
  (Desktop post-audit of 57ecf3506481e73ca27548ea02e4864904d9883a)

NEW_CORRECTION_DESKTOP_POST_AUDIT = NOT_PERFORMED
  (this fresh independent internal QC is NOT the future Desktop post-audit of the
   new published correction SHA; set to PERFORMED only when such an independent
   post-audit actually occurs)

WORLD_INSTANCE = NOT_ESTABLISHED
MODEL_ROOT = NOT_ESTABLISHED
MAIN_VISUAL_CHILD = NOT_ESTABLISHED

CHILD_RESOURCE_PROVENANCE = STRONGLY_SUPPORTED_MODEL_DERIVED
MODEL_ROOT_RELATION = UNKNOWN
WRAPPER_DEPTH = UNRESOLVED
CHILD_VISUAL_ROLE = UNRESOLVED
CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED
EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30
  scoped to examined ACLD path
JOIN_OPERATION = STRONGLY_SUPPORTED
CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND

WORLD_XYZ_RECOVERED = NO
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED
HISTORICAL_INSTANCE_DATA_RECOVERED = NO
```

NC1 changes validation machinery. It does NOT create or retract historical placement data.

## 12. Coverage / FULL_READ_LOG / NOT_CHECKED

FULL_READ (to EOF, this QC session):
- dispatch contract OPENCODE_NC1_CORRECTION_REVIEWED.md (950 lines)
- 03_SCRIPTS/ctrl4_exact_endpoint_sibfixed.py (318 lines — production source, before execution)
- 03_SCRIPTS/run_nc1_matrix.py (465 lines)
- CONTROL_RESULTS_POST.json (1199 lines), CONTROL_RESULTS_PRE.json (127 lines)
- INPUT_IDENTITIES.md (133 lines), SOURCE_STATE.md (107 lines)
- historical internal-QC implementation SOURCE_PACKAGE 00_CONTROL_INTERNAL_QC/qc_ind_ctrl_own.py
  (393 lines — my lineage predecessor)
- Desktop REPORT.md (196 lines)
- published window record 01_RAW/JOIN_WINDOW_50A3B7_REPIN.txt (53 lines)
- SOURCE_PACKAGE 03_SCRIPTS/FIXTURES.md (109 lines)
- my own qc_ind_ctrl_sib_own.py (own artifact, self-check honestly labeled)

BOUNDED_INSPECTION: Desktop CONTROL_COUNTERCHECKS.json — the `sib_hidden_edi_write` case read
and field-verified in full (bytes, expected, production/internal results, capstone decode,
capstone_edi_writes); the executor's PRE.json transcription of that case verified field-level
against the raw Desktop fields (all equal); the remaining cases of that file NOT re-verified
(out of this QC's five-case scope).

NOT_CHECKED (explicit):
- the OLD production checker was NOT re-executed by this QC (its NC1 false pass is already
  established by two independent measurements — the Desktop measurement and the executor's
  EXECUTOR_REPRODUCTION in CONTROL_RESULTS_PRE.json — whose agreement I verified field-level;
  re-execution would add no independence to the CORRECTED-machinery verification, and the old
  module was not fully read by this QC);
- full 27-file SOURCE_PACKAGE Git-blob equality (spot-verified only for the four files this QC
  load-bearing-used: old checker, historical QC engine, FIXTURES.md, window record — all
  BASE-blob-identical; the full bijection is the parent/manifest phase);
- AUDIT_ENTRYPOINT.md (244929 B; read-only for this QC; untouched by the executor and by this QC);
- the nine historical internal-QC adversarial mutants of the SOURCE run (historical results
  preserved, not re-run — outside the NC1 five-case scope);
- PE_MASTER_ACTIVE_ORDER.md / PE_MASTER_LOOP_STATE.json (paths not present in this environment;
  the frozen dispatch contract is the authoritative parent instruction for this bounded QC);
- universal x86-32 decoder correctness (explicitly NOT claimed and NOT tested beyond the
  recorded window's opcode universe and the registered falsifiers);
- any EXE byte remeasurement (no EXE access of any kind by this QC).

## 13. Limitations

- The strongest claim this QC supports is exactly:
  `NC1_SHARED_SIB_FALSE_PASS = CORRECTED_AND_REVALIDATED` and
  `CTRL4_BOUNDARY_VALIDATION = SUPPORTED_WITHIN_RECORDED_CLEAN_WINDOW_AND_REGISTERED_FALSIFIERS`
  — scoped to the recorded clean window and the registered falsifiers (five-case matrix + 9-form
  SIB battery), NOT a universal x86-decoder correctness proof.
- Both checkers implement the same contract-mandated predicate (disclosed in §4); agreement of
  the two engines is a same-predicate cross-check, not an independent-predicate confirmation.
- My SIB-aware diagnostic implements only the SIB arithmetic needed for the NC1 replacement
  span; it is evidence for the hidden EDI write, not a general SIB decoder.
- This QC does not publish anything (no staging/commit/push — not assigned); manifest
  regeneration, SUPERSESSION.md, FINAL_REPORT.md, HANDOFF.md and the PE-MASTER review are the
  parent/persistence phase (contract §13 items 10-14).
