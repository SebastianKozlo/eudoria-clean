# FAIL_CLOSED_TESTS — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (order s17)

The fail-closed detector set (s17) is implemented in the gb12 adapter and
exercised by tools/gamebryo_oracle/tests/test_gb12.py. Every control records
MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR /
FAILURE_CASE_DETECTED (raw outputs: 04_EVIDENCE/T_runs + test stdout in this
batch's execution log).

| detector | implementation | negative control exercising it | result |
|---|---|---|---|
| unknown type | LoadRTTI/LoadObject factory miss -> RTTIError(<class>) verdict (NiStream.cpp L427-433, L451-468) | T-corpus NiArk* payloads (original verdict) + mutated RTTI name NiXyzzyx | DETECTED (PASS) |
| missing factory | same path as unknown type (factory lookup miss IS RTTIError; NO_CREATE_FUNCTION message) | same | DETECTED (PASS) |
| unsupported block | registered-but-not-implemented classes -> boundary-only records with status REGISTERED_BUT_NOT_DECODED_BY_ADAPTER (never silently skipped) | T3 (NiPSys* run) -- full-decode honest PARTIAL at wall cap | DETECTED (PASS) |
| link failure | linkID >= num_blocks -> LINK_FAILURE warning per block/field | mutated child link 0xFFFFFFFE | DETECTED (PASS) |
| PostLink failure | GB 1.2 PostLinkObject is migration-only (NiObjectNET.cpp L656-693); no byte-consuming failure path exists at load; the adapter implements the link phase + count invariant instead | object-count invariant below | N/A (source-proven; recorded honestly) |
| partial scene | --full-decode: accepted=false + partial=true + unknowns listed + decode_continued_after_rtti_gate=true | T1/T2/T4/T5 full-decode outputs | DETECTED (PASS) |
| exception | decode exceptions -> error JSON + nonzero exit, never silent success | corrupted mid-file flip control | DETECTED (PASS) |
| object-count mismatch | header num_blocks vs decoded count invariant; corrupted type index -> INVALID_TYPE_INDEX (source assert L440) | mutated header count +5 | DETECTED (PASS) |

A silent success in ANY of the above controls = GATE FAIL; none occurred.

---

## C1 addendum (2026-10-03, correction round C1)

The five mutation-control raw outputs are now persisted as JSON in
04_EVIDENCE/controls/ (corrupted_header_version.json,
corrupted_midfile.json, unknown_class_mutation.json,
link_failure_mutation.json, object_count_mutation.json), re-executed
on SANDBOX COPIES of the pinned T1/T2 payloads and the GB SDK stock
samples (STOCK = 1310 HN (Plane).nif; the link control additionally
exercised on 2310 HN (Plane).nif), using the same control code paths
from tools/gamebryo_oracle/tests/test_gb12.py (runners:
04_EVIDENCE/scripts/c1_control_persist.py + c1_followup.py +
c1_complete.py). In E2 these controls were executed in-memory with
only the batch stdout captured (disclosed then); C1 closes that
persistence gap. Per-payload check verdicts are recorded inside each
JSON with the MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED labels; all five controls
have a DETECTED case; honest per-payload non-detections are
explained inside each JSON. Payload-dependence disclosed: on NiArk payloads (T1) the original-mode load
stops at the RTTI gate before the link phase, and the verbatim
link-control find() resolves to the footer num-top field on the 1310
sample (DecodeError, fail-closed); the link-failure case is DETECTED
on the 2310 sample where the verbatim path reaches the link phase.
For the mid-file control on the 1310 sample the flipped byte
(844 of 1689) lies deep inside the data region of a NiTriStripsData block
(offset-in-block 260), so the mutated file remains structurally
valid and loads -- consistent with original loader semantics,
not a fail-closed violation; the structural-corruption case is
DETECTED on T2.
Original text above unchanged; no detector verdict changed by this
addendum.
