# FINAL_REPORT — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004

RUN_ID: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004
RUN_CLASS: LOAD_BEARING CORRECTION | MODE: STATIC-ONLY (the client never ran;
corrected instruments read ONLY the pinned EXE; no Ghidra) | Executor:
pe-reconstruction (PE-MASTER bounded C2 correction contract; NO_NESTED_TASKS;
publication assigned in-contract; QC_SCOPE =
SELF_CHECK_FACTORY_PLUS_84_C2_AF1_AF3_CORRECTION — executor self-check,
explicitly NOT an independent PE-MASTER audit).

CORRECTION ONLY: this run corrects the Desktop post-audit findings AF1
(production-artifact QC completeness), AF2 (safe instruction-boundary / decode
/ CALL-promotion provenance), AF3 (wrong-object provenance discipline) and the
directly dependent P3 hygiene defects (P3-A segment-relative stores, P3-B
declared-families metadata, P3-C INPUT_IDENTITIES typo). No new
backing-source science; templates.vfs NOT opened; RECORD_A NOT analyzed; Model
194013 NOT traced; no placement/XYZ; no client execution; no new
function-discovery sweep; no class atlas; no attempt to resolve every
newly-UNRESOLVED census candidate. The 0xA4 object received NO class name.

## THE CORRECTION IN ONE PARAGRAPH

The preserved assignment science survives the corrected re-measurement
unchanged (both known stores re-pinned at strong-anchor-confirmed boundaries;
the setter chain re-validated pin-by-pin), while every AF1/AF2/AF3/P3 defect
class named by the Desktop post-audit is repaired with fresh machinery: the
boundary policy is strong-anchor-only with heuristic starts recorded but never
confirming (census boundary-confirmed rows 1,685 -> 10, all
KNOWN_FUNCTION_ENTRY); a proven decode covering a candidate mid-instruction
REFUTES it (new census class REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE,
0 rows in the final census — the demoted rows are outside the proven streams);
the decoder decodes SHUFPS imm8 / 16-bit-address / 66 E8 rel16 forms correctly
and rejects fail-closed otherwise (counterexample classes A/B/C/D/E all pass,
with real-EXE positive controls); REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE
now requires a per-row identity chain (5 -> 1: the manager-ctor row only; the
four layout controls downgraded to UNRESOLVED with their grammar hypotheses
recorded and the 0x0075138F ArkEstateObject lead physically re-verified but
NOT promoted); the QC battery validates the ACTUAL artifacts against fresh EXE
re-derivation and the M1–M4 + AF3/Q8 mutations through the SAME production
gates are 5/5 causal; the ctor store census now represents SEGMENT semantics
(the two FS:[0] SEH stores included and explicitly excluded from this+0
evidence); DECLARED_ENCODING_FAMILY_COUNT is derived (9, was mislabeled 10);
the INPUT_IDENTITIES repository-owner typo is corrected as
SebastianKozlo/eudoria-clean (P3-C, old->new recorded in S-C2-12).

## F84-C2 — AF1: production-artifact QC completeness (measured)

The production QC gates re-derive the load-bearing fields of the ACTUAL
committed artifacts from the pinned EXE and compare field-by-field:
Q2 the C1 pin JSON (opcode_bytes/length/boundary per pin + JSON<->CSV
consistency), Q3 the pin CSV (full row re-derivation incl. measured_operand),
Q6 the census boundary anchors per row (boundary_status/source/
containing_function), Q7 the AF3 identity chains, Q8 the C3 store collection.
Causal mutations through the SAME gates on TEMPORARY COPIES of the ACTUAL
final artifacts (01_RAW/CQC_MUTATION_RESULTS.json + AF1_MUTATION_MATRIX.csv):

| Mutation | Artifact / field corrupted | Gate | UNMUTATED | MUTATED | Causality |
|---|---|---|---|---|---|
| M1 | C1_PIN_EVIDENCE.json stream_ctor_entry.opcode_bytes `6A FF` -> `EB FF` | Q2 | PASS | FAIL | CAUSAL_PASS |
| M2 | CORRECTED_PIN_LEDGER.csv slotpred callback measured_operand `0x70BEF0 (7402752)` -> `0x70BEF0B8 (118482808)` | Q3 | PASS | FAIL | CAUSAL_PASS |
| M3 | C3_OBJECT_SCOPE.json offset_zero_stores collection removed | Q8 | PASS | FAIL | CAUSAL_PASS |
| M4 | census row 0x0070DD1A containing_function -> `entry~0xDEADBEEF` | Q6 | PASS | FAIL | CAUSAL_PASS |
| AF3/Q8 | AF3 ledger manager row identity edge + provenance removed (candidate bytes unchanged) | Q7 | PASS | FAIL | CAUSAL_PASS |

Identity preserved between both executions of every mutation: pinned EXE
identity (re-hashed by the loader at both executions), git baseline, unrelated
artifacts (copied byte-identical into the temp tree), unrelated QC inputs, and
the SAME gate function object. No corrupted copy is persisted as a canonical
artifact. A clean production gate that does not PASS would make
MUTATION_DETECTION = NOT_ESTABLISHED — all five clean gates PASS, so all five
mutation detections are established.

## F84-C2 — AF2: boundary / decode / CALL-promotion provenance (measured)

Boundary policy (pebnd.py, corrected): strong anchors ONLY — the 34-entry
prior-canon KNOWN_FUNCTION_ENTRY table, each recorded with ANCHOR_VA /
ANCHOR_CLASS / EXISTING_PHYSICAL_EVIDENCE / EVIDENCE_SOURCE /
EVIDENCE_STATUS (anchor registry persisted in 01_RAW/
CQC_BOUNDARY_COUNTEREXAMPLES.json and C1_PIN_EVIDENCE.json). The C1 T2/T3
padding classes are HEURISTIC_START_CANDIDATE: enumerated and recorded per
candidate, never confirming, never promoting, never beating a conflicting
proven decode. A proven decode covering a candidate strictly inside one of
its instructions yields BOUNDARY_STATUS = REFUTED_MID_INSTRUCTION (a
successful-decode refutation — never an inference from a failed decode);
no census row was refuted in the final enumeration (the demoted rows lie
outside the proven streams). If one anchor lands and another refutes, the
result is UNRESOLVED (ANCHOR_CONFLICT, disclosed).

Decoder (x86dec.py, corrected): 0F C4/C5/C6 carry their trailing imm8 (class B:
`0F C6 C0 E8` is a 4-byte SHUFPS whose imm8 is the E8 — C1 measured 3 and
promoted the imm8 to CALL); the 67 prefix decodes true 16-bit ModRM addressing
(class C: `67 8B 06 84 00` is a 5-byte MOV EAX,[0x0084] — C1 fabricated a
3-byte 32-bit ModRM length); 66 E8/E9 decode as rel16 near branches (class D:
`66 E8 01 00` is a 4-byte CALL rel16 — C1 silently parsed a 6-byte ordinary
E8 rel32); segment prefixes are recorded (P3-A); more than five prefix bytes
or a doubled segment prefix or an unsupported far branch is REJECTED
fail-closed.

Mandatory counterexamples (01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json +
AF2_BOUNDARY_TEST_MATRIX.csv; every case persisted with BYTES / START_OFFSET /
EXPECTED_DECODE / ACTUAL_DECODE / EXPECTED_CALL_PROMOTION /
ACTUAL_CALL_PROMOTION / BOUNDARY_SOURCE / BOUNDARY_STATUS):

| Case | Class | Result |
|---|---|---|
| A1 `B8 CC CC E8 00 00 00 00 C3` (candidate +3) | delimiter bytes inside an immediate | REFUTED_MID_INSTRUCTION; CALL promotion NONE (C1: PASS via CC_PADDING start at the candidate VA) |
| A2 `B8 C3 CC E8 00 00 00 00 C3` (candidate +3) | same, RET+CC variant | REFUTED_MID_INSTRUCTION; promotion NONE |
| B `0F C6 C0 E8 00 00 00 00 C3` (candidate +3) | SHUFPS imm8 | REFUTED_MID_INSTRUCTION; promotion NONE (C1: promoted even with KNOWN_FUNCTION_ENTRY) |
| C `67 8B 06 E8 00 90 C3` (candidate +3) | 16-bit-address disp16 | REFUTED_MID_INSTRUCTION; promotion NONE (C1: fabricated 32-bit ModRM length) |
| D `66 E8 01 00 90 C3` (candidate +1) | operand-size-prefixed CALL rel16 | REFUTED_MID_INSTRUCTION; promotion NONE — the form is handled at its actual width and never silently parsed as five-byte E8 rel32 |
| E `B8 01 00 00 00 E8 05 00 00 00 C3` (candidate +5) | positive control | CONFIRMED; CALL validated; target 0x00A0000F PROMOTED |

Real-EXE positive controls (production anchors): 0x0070C715 -> 0x00972380,
0x0070DD75 -> 0x00971AD0, 0x0070C742 -> 0x00972DF0 — all three still
CALL_VALIDATION=PASS at KNOWN_FUNCTION_ENTRY-confirmed boundaries with the
correct targets (ordinary correctly-aligned E8 rel32 from independently
established entries still validate and resolve). Non-E8 control: FAIL, no
target.

## F84-C2 — AF3: wrong-object provenance discipline (measured)

REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE = 1 — the manager-ctor row
0x00707EC0 (`8D 86 84 00 00 00` LEA ECX,[ESI+0x84] + linked store), with the
concrete identity chain persisted per row in AF3_PROVENANCE_LEDGER.csv:
EFFECTIVE_ADDRESS = ESI+132; BASE_REGISTER = ESI = machine-checked this of
FUN_00707E50 (entry this-flow re-derived this run); IDENTIFIED_OBJECT = the
MANAGER object (prior canon: manager class 0x100 B, singleton global
0x00BA12E4, manager getter FUN_00415470 -> ctor FUN_00707E50; manager global
reference census re-measured this run); IDENTITY_EVIDENCE_STATUS =
IDENTITY_CHAIN_PHYSICALLY_REVERIFIED_THIS_RUN; FINAL_CLASSIFICATION =
REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE. The manager/factory distinction
(factory class 0x118 B singleton 0x00BA590C) is preserved prior canon.

The four C1 layout-evidence rejections are DOWNGRADED to UNRESOLVED (0x0074955A,
0x006D4F88, 0x0075138F, 0x007196AA): each carries a layout/value/init GRAMMAR
hypothesis, not an identity chain, and each is now also boundary-unresolved
(no strong anchor reaches its containing function). Their window byte evidence
is re-verified and recorded as HYPOTHESIS support only (ledger rows with
IDENTITY_EVIDENCE_STATUS = HEURISTIC_WINDOW_ONLY_NOT_AN_IDENTITY_CHAIN /
HEURISTIC_WINDOW_LEAD_NOT_PROMOTED_NO_BOUNDARY). The 0x0075138F lead
(Desktop post-audit: direct store of vptr 0x00A87410 and MSVC TypeDescriptor
.?AVArkEstateObject@@ in the same ctor window) is physically re-verified this
run — the vptr immediate 0x00A87410 is present at 0x00751370 (`C7 06 10 74
A8 00` MOV [ESI],0x00A87410 within the same ESI-based window) and the RTTI
chain byte-read matches ([vptr-4]=0x00AA9AD4 COL; [COL+0x0C]=0x00B8E9D4
TypeDescriptor; name = .?AVArkEstateObject@@) — but the candidate's containing
function has NO strong anchor, so the candidate's base/object CANNOT be
physically bridged to that vptr/object identity within this correction's
boundary discipline; the lead is recorded NOT_PROMOTED and the row stays
UNRESOLVED (ADDRESS_PROVENANCE_STATUS=UNRESOLVED -> FINAL_CLASSIFICATION =
UNRESOLVED, not PROVEN_WRONG_OBJECT). No broad ArkEstateObject/class-atlas
investigation was performed — a single bounded window read + one RTTI chain
read for the one contract-named lead.

## F84-C2 — regenerated census (all boundary/provenance-dependent counts superseded)

Scope: the SAME 9 declared examined encoding families (byte grammar
enumeration preserved independently of boundary classification), byte-by-byte
over every .text position (6,766,592 positions tested, no skip-ahead).
DECLARED_ENCODING_FAMILY_COUNT = 9 (P3-B: derived from the actual scanner
family table; the C1 metadata value 10 is superseded — S-C2-08); metadata,
JSON, CSV and this report agree; disclosed-but-out-of-scope families
documented separately (66-form SIB variants, mod00 absolute forms,
67-prefixed variants).

| Quantity | C1 (superseded) | C2 (measured) |
|---|---|---|
| RAW_PATTERN_ROWS | 2,612 | **2,612** (regression expectation MATCH — the raw byte grammar is unchanged by the boundary policy) |
| POSITIVE_PLUS_84_ENCODING_ROWS | 2,227 | **2,227** |
| NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS | 385 | **385** |
| BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS | 1,685 (padding-derived for 1,675) | **10** (strong anchors only) |
| BOUNDARY_REFUTED_MID_INSTRUCTION_ROWS | (class did not exist) | **0** (no candidate lies interior to a proven stream) |
| KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES | 2 | **2** (0x0070D013 INITIALIZATION_NULL; 0x0070C71E CONDITIONAL_OBJECT_OR_NULL_ATTACH_STORE — re-pinned) |
| REJECTED_READ_NOT_WRITE | 1,003 | **6** |
| REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE | (class did not exist) | **0** |
| REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE | 5 | **1** (manager row with full identity chain) |
| CENSUS_UNRESOLVED_ROWS | 1,217 | **2,218** |
| FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES | 828 | **832** |
| ADDRESS_PROVENANCE_UNRESOLVED | 828 | **832** |
| DECODER_REJECT_ROWS | 0 | **0** |

EXAMINED_ENCODING_CANDIDATE_CLOSURE = CLOSED — scoped exactly as before to the
declared encodings/effective-address forms and now also explicitly scoped to
the RAW BYTE-GRAMMAR ENUMERATION (every .text position tested against every
declared family); the AF2 correction reduces BOUNDARY/IDENTITY coverage INSIDE
the closed enumeration (only strong-anchor-reachable rows are
boundary-classified) and never translates enumeration closure into write
closure. **EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED
(invariant — never upgradable by any census result).**
CLEAR_RESET_CONFIRMED_COUNT = 0 (no clear/reset store of the member CONFIRMED
within the examined census; NOT proven absent).

## F84-C3 — P3-A: segment-aware store census (measured)

The examined ctor extent 0x00972380..0x009724DA (sequential decode
RET_REACHED, 93 instructions, this-register ESI machine-checked at entry)
is re-enumerated with SEGMENT SEMANTICS EXPLICITLY REPRESENTED: every
memory-WRITE encoding with effective displacement 0 (explicit MOV-to-memory
stores incl. 66-word variants, MOFFS stores, RMW forms) — exactly THREE found:

| Store | Segment | Class |
|---|---|---|
| `89 07` MOV [EDI],EAX @0x00972452 | (none) | REGISTER_BASED_ZERO_OFFSET_STORE (base EDI = the cursor at +0x3C, NOT the this-register) |
| `64 A3 00 00 00 00` MOV FS:[0],EAX @0x009723A0 | **FS** | SEGMENT_RELATIVE_SEH_TLS_STORE |
| `64 89 0D 00 00 00 00` MOV FS:[0],ECX @0x009724CB | **FS** | SEGMENT_RELATIVE_SEH_TLS_STORE |

```text
DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED   (direct observation over the examined ctor extent ONLY;
                                                      segment-relative stores are explicitly EXCLUDED from
                                                      this+0/vptr eligibility — a FS:[0] store is a TLS/SEH
                                                      write, never an offset-zero write to the assigned object's this)
ASSIGNED_OBJECT_VTABLE             = UNVERIFIED     (global scope)
OBJECT_POLYMORPHISM                = NOT_ESTABLISHED (global scope)
KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES            (measured over the 3 examined callsites ONLY:
                                                       0x0070DD75 -> 0x00971AD0,
                                                       0x0070DD84 -> 0x00971650,
                                                       0x0070C742 -> 0x00972DF0; all direct E8 rel32,
                                                       KNOWN_FUNCTION_ENTRY-confirmed)
```

Ctor call-site census (machine, corrected policy): 10 raw E8 rel32 target
matches (unchanged), boundary_confirmed_count = 2 (0x0070C715 in FUN_0070C680;
0x0072FA76 in FUN_0072FA30 — the LEAD ONLY callsite, still no bridge claim).

## Pin ledger re-validation (measured, corrected machinery)

133 preserved pin records, 0 failures: 120 VALIDATED + 4 CORRECTED_VALIDATED
(the F84-C1 corrected records re-verify: slotpred callback @0x0070CC9B imm
0x0070BEF0; stream-ctor alloc CALL @0x0097244A -> 0x0095D3BE; EDI save
@0x00708025; the real region CALL @0x004B0A1E -> 0x00401E70) + 2
DECLASSIFIED_NOT_A_CALL (0x004B0A02/0x004B0A21, measured bytes 0x01/0xF5) +
5 VALIDATED_BYTES_BOUNDARY_UNRESOLVED + 2 NOT_VERIFIED (the C1
padding-confirmed rows honestly downgraded — S-C2-09: the modeinit-caller and
lazy-init chains' byte/operand evidence still re-verifies; the two CALL
targets are NOT_PROMOTED with apparent targets recorded).

## PRESERVED_CORE (re-measured and revalidated this run — unchanged)

```text
FACTORY_PLUS_84_ASSIGNMENT_CORE = CONFIRMED_STATIC_CONDITIONAL
ASSIGNMENT_FUNCTION = FUN_0070C680
ASSIGNMENT_VA = 0x0070C71E
ASSIGNMENT_STORE_BYTES = 89 86 84 00 00 00
ASSIGNED_OBJECT_SIZE = 0xA4/164 B
ASSIGNED_OBJECT_CONSTRUCTOR = FUN_00972380
STATIC_FACTORY_MEMBER_IDENTITY = CONFIRMED_WITH_EXAMINED_PATH_CONDITIONS
```

Both known stores re-pinned at KNOWN_FUNCTION_ENTRY-confirmed boundaries:
0x0070D013 (INITIALIZATION_NULL; `89 9E 84 00 00 00` in FUN_0070CF80,
THIS_OF_KNOWN_FUNCTION provenance) and 0x0070C71E
(CONDITIONAL_OBJECT_OR_NULL_ATTACH_STORE; `89 86 84 00 00 00` in FUN_0070C680,
THIS_OF_KNOWN_FUNCTION provenance).

## CLAIM SURFACE (separated, per contract)

- PHYSICAL BYTE FACT: the pinned-EXE bytes at every pinned VA (133 pins), the
  census raw grammar (2,612 rows), the ctor extent bytes, the two FS:[0]
  store encodings, the ArkEstateObject lead bytes (vptr immediate 0x00A87410
  at 0x00751370; RTTI chain bytes 0x00AA9AD4/0x00B8E9D4/.?AVArkEstateObject@@).
- MEASURED TOOL OUTPUT: the C2 census counts, the boundary determinations, the
  mutation matrix results (5/5 CAUSAL_PASS), the decoder unit battery, the
  counterexample outcomes.
- FUNCTION_IDENTITY: FUN_0070C680 = the stream-attach setter (prior canon,
  re-validated); FUN_00972380 = the assigned object's constructor (prior
  canon, re-validated); manager ctor FUN_00707E50 (identity chain for the
  manager row).
- OBSERVED_OPERATION: the store `89 86 84 00 00 00` writes [ESI+0x84] with
  EAX = the new(0xA4) object or NULL; the ctor's FS:[0] stores are SEH/TLS
  segment writes.
- OBJECT_IDENTITY: the assigned 0xA4 object's identity is
  CONFIRMED_WITHIN_EXAMINED_LAYOUT; it received NO class name in this run;
  the manager object identity (prior canon) supports the one proven
  wrong-object rejection; the ArkEstateObject identity is a NOT-PROMOTED
  lead for an unrelated candidate.
- FINAL_SEMANTIC_ROLE: FINAL_SEMANTIC_ROLE_RECORD_STREAM =
  STRONGLY_SUPPORTED (semantic naming, NOT confirmed from structural
  observations alone). WORKS != UNDERSTAND: the corrected parser/QC success
  upgrades NO semantic claim. The private Desktop RTTI research is NOT
  imported into canonical status (the ArkEstateObject lead is recorded as a
  physically re-verified NON-CANONICAL lead only).

## P3 corrections (measured)

- **P3-A**: the store-census scope is corrected as above (S-C2-11); segment
  information is persisted per store; FS:[0] can never become
  DIRECT_VPTR_STORE_IN_EXAMINED_CTOR or object-member offset-zero evidence.
- **P3-B**: DECLARED_ENCODING_FAMILY_COUNT = 9, derived from the actual
  scanner configuration (len(FAMILIES)); IN_SCOPE_FAMILIES = the 9 examined
  families; DISCLOSED_BUT_OUT_OF_SCOPE_FAMILIES = 66-form SIB variants,
  mod00 absolute forms, 67-prefixed variants (documented in the census JSON);
  metadata/report/JSON/implementation agree (gate Q13).
- **P3-C**: the repository-owner typo is corrected in THIS package's
  INPUT_IDENTITIES.md (`SebastianKlo/eudoria-clean` ->
  `SebastianKozlo/eudoria-clean`; the exact source occurrence verified at
  BASE: exactly one, line 18 of the SOURCE_PACKAGE INPUT_IDENTITIES; the
  actual remote identity verified via `git remote get-url origin`;
  historical file NOT modified; S-C2-12).

## Terminal fields (exact)

```text
RUN_ID = PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004
BASE_SHA = 535e1a00fe793299dea7fc639e552560a6ac633b
HEAD_SHA_AT_PACKAGE_FREEZE = 535e1a00fe793299dea7fc639e552560a6ac633b
COMMIT_SHA = NOT_AVAILABLE_AT_PACKAGE_FREEZE
RUN_STATUS = COMPLETED
EXE_IDENTITY = PASS (8015872 B, SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31)
FACTORY_PLUS_84_ASSIGNMENT_CORE = CONFIRMED_STATIC_CONDITIONAL
ASSIGNMENT_FUNCTION = FUN_0070C680
ASSIGNMENT_VA = 0x0070C71E
ASSIGNMENT_STORE_BYTES = 89 86 84 00 00 00
ASSIGNED_OBJECT_SIZE = 0xA4/164 B
ASSIGNED_OBJECT_CONSTRUCTOR = FUN_00972380
STATIC_FACTORY_MEMBER_IDENTITY = CONFIRMED_WITH_EXAMINED_PATH_CONDITIONS
DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED
ASSIGNED_OBJECT_VTABLE = UNVERIFIED
OBJECT_POLYMORPHISM = NOT_ESTABLISHED
ASSIGNED_OBJECT_STRUCTURAL_IDENTITY = CONFIRMED_WITHIN_EXAMINED_LAYOUT
FINAL_SEMANTIC_ROLE_RECORD_STREAM = STRONGLY_SUPPORTED
ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED
WRITE_TO_CONSUMER_VALUE_PRESERVATION = NOT_ESTABLISHED
FACTORY_PLUS_84_LIFETIME_SINGLE_ASSIGNMENT = NOT_ESTABLISHED
EXAMINED_ENCODING_CANDIDATE_CLOSURE = CLOSED
EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED
ULTIMATE_VALUE_SOURCE = UNKNOWN
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES = 2 (within the examined census)
CLEAR_RESET_CONFIRMED_COUNT = 0 (no clear/reset store CONFIRMED within the examined census; NOT proven absent)
RAW_PATTERN_ROWS = 2612
POSITIVE_PLUS_84_ENCODING_ROWS = 2227
NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS = 385
BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS = 10
BOUNDARY_REFUTED_MID_INSTRUCTION_ROWS = 0
REJECTED_READ_NOT_WRITE = 6
REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE = 0
REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE = 1
CENSUS_UNRESOLVED_ROWS = 2218
FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES = 832
ADDRESS_PROVENANCE_UNRESOLVED = 832
DECODER_REJECT_ROWS = 0
DECLARED_ENCODING_FAMILY_COUNT = 9 (derived; P3-B)
NEW_SUPERSESSION_RECORD_COUNT = 13 (measured; the historical 31-record ledger belongs to SOURCE_RUN only)
MUTATION_TEST_COUNT = 5
MUTATION_CAUSAL_PASS_COUNT = 5
MUTATION_CAUSAL_FAIL_COUNT = 0
MUTATION_NOT_ESTABLISHED_COUNT = 0
NEW_BACKING_SOURCE_RE_EXECUTED = NO
TEMPLATES_VFS_OPENED = NO
RECORD_A_ANALYZED = NO
MODEL_194013_TRACE_EXECUTED = NO
PLACEMENT_XYZ_RE_EXECUTED = NO
CLIENT_EXECUTED = NO
CANONICAL_GATE_EFFECT = NONE
KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES
NEXT_EXPERIMENT_AUTHORIZED = NO
```

## Preserved predecessor states (carried unchanged)

```text
WRITER_MECHANISM = PRESERVED_CONFIRMED_STATIC_CONDITIONAL
ATTRIBUTE10_WRITER_MECHANISM = PRESERVED_CONFIRMED
WRITER_FUNCTION = FUN_009777F0
WRITER_VA = 0x00977810
TAG6_TO_ID10 = PRESERVED_CONFIRMED
SAME_STORAGE_IDENTITY = PRESERVED_CONFIRMED_STATIC_CONDITIONAL
SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED
WRITE_TO_LATER_GETTER_VALUE_PRESERVATION = NOT_ESTABLISHED
NO_CLOBBER_BETWEEN_WRITE_AND_READ = NOT_ESTABLISHED
TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD
RECORD_A_RELATION = NOT_ESTABLISHED
FILE_DERIVED_VALUE_EXCLUDED = NO
MODEL_JOIN_EXECUTED = NO
```

## ANTI-SUCCESS-THEATER record

- MEASURED_QUANTITY: the re-validated 133-record pin ledger, the regenerated
  2,612-row census, the segment-aware C3 store census, the mutation matrix
  (M1–M4 + AF3/Q8) and the boundary-counterexample matrix — every number in
  this report is machine-derived from those artifacts.
- INDEPENDENT_SOURCE_OF_TRUTH: pinned-EXE bytes re-read by every gate; every
  mutation routes the ACTUAL final artifact (temporary copy) through the SAME
  production gate that accepted the clean package.
- WHY_NON_CIRCULAR: the gates never consult their own recorded verdicts — they
  re-derive from the EXE and compare against the artifacts; the mutation
  harness proves the gates actually fail on corrupted real artifacts; the
  counterexamples prove the promotion rules fail exactly where the C1 rules
  falsely passed.
- FAILURE_CASES_DETECTED: M1–M4 + AF3/Q8 mutated artifacts FAIL their gates
  (5/5); counterexample classes A/B/C/D produce FAIL_MID_INSTRUCTION with no
  promotion; the CONTROL B enumeration mutant fails Q11's membership
  derivation; the non-E8 control FAILs with no accepted target.

## Honest boundaries

1. STATIC-ONLY: no runtime observation of any kind; the client never ran.
2. The 2,218 unresolved census rows (832 write candidates) are honest bounds
   produced by the corrected strong-anchor policy — NOT failures, and NOT
   claims that the underlying positions are or are not instructions (no
   inference is drawn from failed decodes; heuristic starts are recorded but
   never confirming).
3. REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE = 1 is the honest count under
   the identity-chain discipline; the four downgraded layout controls and the
   not-promoted ArkEstateObject lead are recorded for a future authorized run.
4. DIRECT_VPTR_STORE_IN_EXAMINED_CTOR=NOT_OBSERVED is scoped to the examined
   ctor extent only; ASSIGNED_OBJECT_VTABLE=UNVERIFIED and
   OBJECT_POLYMORPHISM=NOT_ESTABLISHED remain the honest global states.
5. BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS = 10 reflects the strong-anchor
   coverage bound of THIS machinery; extending coverage requires NEW anchors
   with independent physical provenance (a future authorization) — heuristic
   starts were NOT renamed to inflate it.
6. LEAD discipline unchanged: the same-ctor call site @0x0072FA76 in the
   templates.vfs reader-chain region remains LEAD ONLY (validated as a CALL
   -> 0x00972380; no bridge claim).
