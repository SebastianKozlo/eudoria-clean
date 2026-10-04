# QC_REPORT — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004

QC_SCOPE = SELF_CHECK_FACTORY_PLUS_84_C2_AF1_AF3_CORRECTION — executor
self-QC, explicitly NOT an independent audit (the independent verdict is
PENDING PE-MASTER/desktop post-audit of this exact package). The authoritative
machine record is 01_RAW/CQC_FINAL.json; this report summarizes it.

## Production gates (all read the ACTUAL package artifacts and re-derive from the pinned EXE)

| Gate | Scope (measured) | Verdict |
|---|---|---|
| Q1 | baseline + EXE identity: LOCAL_HEAD == ORIGIN_MASTER == ACTUAL_REMOTE_MASTER == BASE 535e1a00fe793299dea7fc639e552560a6ac633b at run time; EXE 8,015,872 B / E7785430… exact | PASS |
| Q2 | C1 pin JSON integrity vs fresh EXE re-derivation (133 pins: opcode_bytes, length, boundary_status/source, JSON<->CSV consistency; pin_fail_count==0) — **M1 gate** | PASS |
| Q3 | pin CSV full-row re-derivation (measured_operand / raw_operand / measured_target / boundary fields / status, 133 rows) — **M2 gate** | PASS |
| Q4 | decoder unit battery (18 vectors incl. the AF2 class-A/B/C/D rules, truncation rejects, segment recording, far-branch rejects) + census re-decode consistency (2,612 rows) + 10 coverage windows | PASS |
| Q5 | AF2 boundary counterexamples A1/A2/B/C/D/E (6/6) + 3 real-EXE positive controls + non-E8 control + census discipline sweep (0 CONFIRMED rows with untrusted source; 0 REFUTED rows without anchors; 34/34 anchor provenance records complete) | PASS |
| Q6 | census boundary-anchor integrity: every non-control row re-derived (boundary_status/source/containing_function/boundary_refuted_by, 2,227 rows) — **M4 gate** | PASS |
| Q7 | AF3 provenance discipline: manager identity chain physically re-derived (this-flow at FUN_00707E50); ledger<->census consistency; the 4 layout controls verified DOWNGRADED (not PROVEN); ESP-SIB control (register naming is not proof) — **AF3/Q8 gate** | PASS |
| Q8 | P3-A segment-semantics: C3 store census re-derived (3 stores incl. 2 FS; FS set exactly {0x009723A0, 0x009724CB}); segment-relative stores excluded from this+0 eligibility; DIRECT_VPTR=NOT_OBSERVED derived; callsites re-derived — **M3 gate** | PASS |
| Q9 | census arithmetic re-summed from the emitted CSV (tally == JSON; denominators distinct; RAW=2612 regression expectation MATCH) | PASS |
| Q10 | known stores physical re-pin (bytes + KNOWN_FUNCTION_ENTRY boundary + classification + THIS_OF_KNOWN_FUNCTION provenance) | PASS |
| Q11 | factory identity/enumeration derived from measured evidence (ranges from pin CSV; dispatcher entry5 = 0x0073C8D8; CONTROL B mutant fails) | PASS |
| Q12 | object structural identity (0xA4=164, 0x118=280, ctor target, extent, tail stores, cursor pin, THE_STORE/NULL_INIT pins) | PASS |
| Q13 | P3-B: DECLARED_ENCODING_FAMILY_COUNT derived from the actual scanner table (9) == JSON == scan_coverage == explicit list count; out-of-scope families disclosed | PASS |
| Q14 | docs: required claim strings present; superseded-phrase sweep clean; supersession quotecheck 13 records / 15 excerpt lines, 0 failures; P3-C verified (exactly 1 source occurrence at BASE; corrected identity present; old typo absent from the new file; historical file untouched); forbidden-input census clean (no .vfs/.bnt/.nif/.ark opened; no http literals in instruments); forbidden-work flags NO | PASS |

## Causal mutation matrix (AF1) — 01_RAW/CQC_MUTATION_RESULTS.json + AF1_MUTATION_MATRIX.csv

| ID | Mutated artifact (temporary copy of the ACTUAL final artifact) | Gate | UNMUTATED | MUTATED | ACTUAL_CAUSALITY |
|---|---|---|---|---|---|
| M1 | 01_RAW/C1_PIN_EVIDENCE.json — stream_ctor_entry.opcode_bytes `6A FF` -> `EB FF` | Q2 | PASS | FAIL | CAUSAL_PASS |
| M2 | CORRECTED_PIN_LEDGER.csv — slotpred_callback_MOV_EAX_imm32.measured_operand -> `0x70BEF0B8 (118482808)` | Q3 | PASS | FAIL | CAUSAL_PASS |
| M3 | 01_RAW/C3_OBJECT_SCOPE.json — offset_zero_stores collection removed | Q8 | PASS | FAIL | CAUSAL_PASS |
| M4 | CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv — row 0x0070DD1A containing_function -> `entry~0xDEADBEEF` | Q6 | PASS | FAIL | CAUSAL_PASS |
| AF3/Q8 | AF3_PROVENANCE_LEDGER.csv — manager row identity edge + address-provenance support removed (candidate bytes unchanged) | Q7 | PASS | FAIL | CAUSAL_PASS |

MUTATION_TEST_COUNT = 5; MUTATION_CAUSAL_PASS_COUNT = 5;
MUTATION_CAUSAL_FAIL_COUNT = 0; MUTATION_NOT_ESTABLISHED_COUNT = 0 (every
clean production gate PASSed, so every mutation detection is established).
Identity preserved between both executions of every mutation: pinned EXE
identity (re-hashed at both executions), git baseline, unrelated artifacts
(byte-identical copies), unrelated QC inputs, and the SAME gate function
object. The temp mutated trees live outside the repo and are deleted after
the harness; no corrupted copy is persisted as a canonical artifact.

## AF2 boundary counterexamples — 01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json + AF2_BOUNDARY_TEST_MATRIX.csv

Classes A1 (B8 CC CC E8 imm), A2 (B8 C3 CC E8 imm), B (0F C6 SHUFPS imm8),
C (67 8B 06 disp16), D (66 E8 rel16): all REFUTED_MID_INSTRUCTION with NO
call promotion (the C1 machinery promoted all of them — the exact defect
classes of the Desktop post-audit). Class E positive control: CONFIRMED with
the target promoted (0x00A0000F). Real-EXE positive controls: 0x0070C715 ->
0x00972380, 0x0070DD75 -> 0x00971AD0, 0x0070C742 -> 0x00972DF0 (all PASS with
correct targets). Non-E8 control FAILs with no accepted target. No E8
discovered inside another instruction's operand/immediate is promoted in any
case.

## Decoder unit battery — 01_RAW/CQC_DECODER_UNIT_TESTS.json

18/18 vectors pass, including: SHUFPS `0F C6 C0 E8 00 00 00 00` = 4 bytes
with imm8=0xE8 (class B fix); `67 8B 06 84 00` = 5 bytes (16-bit-address
decode, class C fix); `66 E8 01 00` = 4 bytes CALL rel16 (class D fix);
truncated/unsupported forms (89 86 truncated; 0F C6 C0 truncated; CALL/JMP
far; 67-prefixed near branch; doubled segment prefix) all REJECT fail-closed;
segment prefixes recorded on both FS store forms (P3-A); census re-decode
consistency over all 2,612 rows (0 mismatches).

## Verdict

DATA MODE: 13/13 gates PASS, 5/5 mutations causal -> QC_PASS.
DOCS MODE: Q14 PASS -> full QC_PASS.
PACKAGE_CORRECTION_STATUS = CORRECTED (per contract §16: AF1/AF2/AF3 all
CORRECTED; all mandatory causal mutations established; all mandatory
decoder/boundary counterexamples pass; all final affected artifacts regenerated
from the corrected machinery; no unresolved internal contradiction).
An honest UNRESOLVED scientific candidate (the 2,218 unresolved census rows,
the four downgraded layout controls, the not-promoted ArkEstateObject lead,
ASSIGNED_OBJECT_VTABLE=UNVERIFIED) is NOT a QC failure.
