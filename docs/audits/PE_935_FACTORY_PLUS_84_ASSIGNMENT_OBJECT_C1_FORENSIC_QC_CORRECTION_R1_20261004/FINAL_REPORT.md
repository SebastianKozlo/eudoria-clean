# FINAL_REPORT — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004

RUN_ID: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004
RUN_CLASS: LOAD_BEARING CORRECTION | MODE: STATIC-ONLY (the client never ran;
corrected pin/boundary/census instruments read ONLY the pinned EXE; no
Ghidra) | Executor: pe-reconstruction (PE-MASTER bounded correction contract;
NO_NESTED_TASKS; publication assigned in-contract; QC_SCOPE =
SELF_CHECK_FACTORY_PLUS_84_C1_FORENSIC_QC_CORRECTION — executor self-check,
explicitly NOT an independent PE-MASTER audit).

CORRECTION ONLY: no new backing-source science; templates.vfs NOT opened;
RECORD_A NOT analyzed; Model 194013 NOT traced; no placement/XYZ; no client
execution; no network analysis; no attempt to resolve every newly-UNRESOLVED
census candidate. Corrected: F84-C1 (address/pin/QC defects), F84-C2 (census
encoding/boundary/provenance defects), F84-C3 (vtable/polymorphism overclaim)
+ the directly dependent P3 terminology/count/decimal defects.

## THE CORRECTION IN ONE PARAGRAPH

The historical package's core assignment science SURVIVES the corrected
re-measurement unchanged (both known stores physically re-pinned; the setter
chain revalidated pin-by-pin), while every defective pin, encoding semantics,
boundary/provenance rule and over-scoped claim named in the F84-C1/C2/C3+P3
findings is superseded with fresh machine measurements: the callback MOV is
@0x0070CC9B with immediate @0x0070CC9C = 0x0070BEF0 (the historical record
declared 0x0070CC9A and published the opcode-contaminated 0x70BEF0B8); the
cursor+0x3C allocation CALL is @0x0097244A → 0x0095D3BE (the historical
0x00972449 record produced the negative phantom target "0x-0B96BCA"); the
EDI save for append is `89 7C 24 30` MOV [ESP+0x30],EDI @0x00708025 (the
published 0x00708030 was a stack displacement misread as an address);
0x004B0A02 and 0x004B0A21 are DECLASSIFIED as CALL records (measured bytes
0x01 / 0xF5 — mid-instruction positions; the real CALL in the region is
0x004B0A1E → 0x00401E70); MOD01 disp8 0x84 is −0x7C (385 negative-control
rows), never +0x84; no census row is rejected by register name; failed
decodes never license "not-an-instruction" inferences; and
the vtable/polymorphism global claims are replaced by the bounded machine
observation DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED with
ASSIGNED_OBJECT_VTABLE = UNVERIFIED and OBJECT_POLYMORPHISM =
NOT_ESTABLISHED.

## F84-C1 — authoritative pin/address/QC correction (measured)

One authoritative instruction VA per pin; opcode bytes, length, operand
offset/width, immediate, rel32 and target ALL derived from that SAME VA
(CORRECTED_PIN_LEDGER.csv: 133 records, 0 failures; 127 VALIDATED +
4 CORRECTED_VALIDATED + 2 DECLASSIFIED_NOT_A_CALL):

| Corrected record | Measured truth |
|---|---|
| slotpred_callback_MOV_EAX_imm32 | instruction @0x0070CC9B `B8 F0 BE 70 00` (MOV EAX,imm32); immediate operand @0x0070CC9C = **0x0070BEF0**; boundary CONFIRMED (FUN_0070CC80) |
| stream_ctor_buffer_alloc_CALL | instruction @0x0097244A `E8 6F AF FE FF` → **0x0095D3BE** (the new(0x80) allocation CALL); boundary CONFIRMED (FUN_00972380) |
| register_EDI_saved_for_append | instruction @0x00708025 `89 7C 24 30` MOV [ESP+0x30],EDI; boundary CONFIRMED (FUN_00707FB0); the published 0x00708030 was the operand displacement, not an address |
| driver_real_call_0x004B0A1E | instruction @0x004B0A1E `E8 4D 14 F5 FF` → **0x00401E70**; boundary CONFIRMED (FUN_004B0980) — the real CALL in the region |
| driver_declassified_0x004B0A02 | measured byte 0x01 (≠E8): byte 1 of the imm32 of MOV EBX,1 @0x004B0A01; **DECLASSIFIED_NOT_A_CALL**; the historical phantom target 0x514B0A07 superseded |
| driver_declassified_0x004B0A21 | measured byte 0xF5 (≠E8): byte 3 of the rel32 operand of the CALL @0x004B0A1E; **DECLASSIFIED_NOT_A_CALL**; the historical phantom target 0x190F8E25 superseded |

DIRECT CALL VALIDATION (corrected machinery): byte[VA] must equal 0xE8; all
5 operand bytes present; boundary CONFIRMED from a declared trusted source
(known function entry / CC-padding-delimited start / RET-delimited start,
each with an exact-landing sequential decode); only then is
TARGET = VA+5+signed_rel32(VA+1) promoted. Any failure → FAIL|NOT_VERIFIED,
no target promoted. The historical `call_target()` machinery computed rel32
targets from ANY supplied VA without opcode or boundary proof — the direct
cause of the phantom targets (SUPERSESSION_LEDGER S-12/S-13/S-15/S-16).

Also corrected (prose-vs-machine divergence, disclosed): the historical s1
prose note "CALL 0x009724DF" for the bridge target — both the historical
machine record and this re-measure give **0x009724E0** (E8 FC 64 26 00
@0x0070BFDF); the corrected ledger carries 0x009724E0 (S-15-class defect,
transcription-level, not load-bearing).

Negative controls A–F (synthetic bytes only, no new PCG function tracing):
all six PASS — see QC_REPORT.md and 01_RAW/CQC_NEGATIVE_CONTROLS.json.

## F84-C2 — corrected census (freshly recomputed; all historical counts superseded)

Scope: the declared examined encoding families (9 families incl. all SIB
variants; 66-form SIB variants disclosed as outside the examined scope),
byte-by-byte over every .text position (6,766,592 positions tested, no
skip-ahead). Measured quantities (01_RAW/C2_CENSUS.json +
CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv, 2,612 rows):

| Quantity | Value |
|---|---|
| RAW_PATTERN_ROWS | **2,612** |
| POSITIVE_PLUS_84_ENCODING_ROWS (effective signed displacement +132) | **2,227** |
| NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS (MOD01 raw disp8 0x84 = −124; an encoding that cannot express +0x84 under any decoding) | **385** |
| BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS | **1,685** |
| KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES | **2** (0x0070D013 INITIALIZATION_NULL; 0x0070C71E CONDITIONAL_OBJECT_OR_NULL_ATTACH_STORE — physically re-pinned) |
| REJECTED_READ_NOT_WRITE (boundary-confirmed read/CMP/LEA forms) | **1,003** |
| REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE | **5** (4 layout-evidence controls with window bytes re-verified this run + the manager-ctor wrapper with machine-checked manager-this provenance) |
| CENSUS_UNRESOLVED_ROWS (all unresolved rows: boundary-unresolved read/LEA rows + all unresolved write candidates) | **1,217** |
| FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES (write-form positive rows not resolved to a confirmed factory write or a proven wrong-object rejection) | **828** |
| ADDRESS_PROVENANCE_UNRESOLVED | **828** |
| DECODER_REJECT_ROWS | **0** |

Definitions and discipline (the two denominators are DISTINCT quantities with
published definitions — the historical 129-vs-64 ambiguity is superseded):
CENSUS_UNRESOLVED_ROWS includes boundary-unresolved read/LEA rows (no write
established, but their instruction-level identity is unproven without a
trusted boundary — no NOT_AN_INSTRUCTION inference is made from a failed
decode); FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES is the write-form
subset. No row is rejected by register name: every ESP/EBP-based write row
carries ADDRESS_PROVENANCE=UNRESOLVED and classification UNRESOLVED (EBP is
not automatically a frame pointer; ESP with an unresolved SIB index is not
automatically a pure stack slot — synthetic CONTROL F proves the rule).
CLEAR_RESET_CONFIRMED_COUNT = 0 means no clear/reset store of the member was
CONFIRMED within the examined census; it does NOT mean clear/reset is proven
absent.

EXAMINED_ENCODING_CANDIDATE_CLOSURE = **CLOSED** (the scanner tested every
.text position against every declared family with the validated decoder —
the ENUMERATION is closed within the explicitly declared encodings,
effective-address forms and trusted-boundary coverage; it does NOT mean all
candidates were classified, and it does not exclude alias writes,
helper-mediated writes, bulk/memory-copy writes, other address constructions,
unexamined encodings or runtime mutation).
**EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED (invariant —
never upgradable to CONFIRMED by any census result).**

## F84-C3 — vtable/polymorphism claim scope (corrected)

Superseded global claims: the historical NONE-vtable and
polymorphism-confirmed wording (SUPERSESSION_LEDGER records S-01/S-03/S-05/
S-21/S-22/S-24/S-27 — the historical global field asserted NONE and the
historical Q7 gate validated a PREFILLED literal as if it were a
measurement; that is not an independent measurement).

Corrected bounded machine search over the EXAMINED ctor extent
(0x00972380..0x009724DA, sequential decode RET_REACHED, 93 instructions,
this-register ESI machine-checked at entry): every memory-write instruction
with effective displacement 0 recorded — exactly one found, the embedded
cursor's buffer store `89 07` MOV [EDI],EAX @0x00972452 with base EDI (this
+0x3C), NOT the this-register. Therefore:

```text
DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED   (direct observation over the examined ctor extent ONLY)
ASSIGNED_OBJECT_VTABLE             = UNVERIFIED     (global scope)
OBJECT_POLYMORPHISM                = NOT_ESTABLISHED (global scope)
KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES            (measured over the 3 examined callsites ONLY:
                                                       0x0070DD75 -> 0x00971AD0,
                                                       0x0070DD84 -> 0x00971650,
                                                       0x0070C742 -> 0x00972DF0; all direct E8 rel32)
```

No helper/base-constructor bodies were entered to force closure (the object
may delegate vptr installation elsewhere; that is why the global fields stay
UNVERIFIED/NOT_ESTABLISHED). "All methods direct-called" is NOT claimed.

## P3 corrections (measured)

- **0xA4 = 164 bytes** (the ASSIGNED OBJECT allocation: `68 A4 00 00 00`
  @0x0070C6F9, imm32 == 0xA4 == 164, machine-measured). The historical
  0xA4/280 decimal conflation is corrected (SUPERSESSION_LEDGER S-02);
  **280 = 0x118 is the FACTORY allocation size** (`68 18 01 00 00`
  @0x0073E2CC) — a different object.
- **Distinct denominators**: CENSUS_UNRESOLVED_ROWS = 1,217 and
  FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES = 828 — separately derived,
  separately defined (above); the historical 129-vs-64 ambiguity is
  superseded.
- FUN_0070BF40 literal transcription (measured 16-byte body
  0x0070BF40..0x0070BF4F, superseding the historical "14-byte body" wording):
  loads [ECX+4]; ANDs with the supplied argument; normalizes the result to a
  boolean-like return (NEG; SBB EAX,EAX; NEG; RET 4). NO semantic-role
  promotion beyond the literal examined operation.
- Function-ledger hygiene: HISTORICAL_FUNCTION_BUDGET_COUNT = 8_DECLARED_AND_MECHANICALLY_REPRODUCED (the existing ledger mechanically reproduces 8 counted + 10 excluded); PRE_ANALYSIS_CHRONOLOGY_INDEPENDENTLY_ESTABLISHED = NO; ACTUAL_HISTORICAL_BUDGET_OVERRUN = NOT_ESTABLISHED — this correction does NOT claim a historical budget overrun.
- Ctor call-site census (machine-measured, superseding the prefilled
  "ctor_callsites_count: 10"): 10 raw E8 rel32 target matches, all 10
  boundary-confirmed.

## PRESERVED_CORE (re-measured and revalidated this run — unchanged)

```text
FACTORY_PLUS_84_ASSIGNMENT_CORE = CONFIRMED_STATIC_CONDITIONAL
ASSIGNMENT_FUNCTION             = FUN_0070C680 (the factory-class stream-attach setter)
ASSIGNMENT_VA                   = 0x0070C71E
ASSIGNMENT_STORE_BYTES          = 89 86 84 00 00 00
ASSIGNED_OBJECT_SIZE            = 0xA4/164 B
ASSIGNED_OBJECT_CONSTRUCTOR     = FUN_00972380
STATIC_FACTORY_MEMBER_IDENTITY  = CONFIRMED_WITH_EXAMINED_PATH_CONDITIONS
```

Both known stores re-pinned: **0x0070D013 (INITIALIZATION_NULL)** —
`89 9E 84 00 00 00` MOV [ESI+0x84],EBX in FUN_0070CF80 (EBX=0;
XOR EBX,EBX @0x0070CFBC; every factory class incl. 20006 via the derived ctor
FUN_0073B820 CALL @0x0073B87D with PUSH 0x4E26) — and **0x0070C71E
(CONDITIONAL_OBJECT_OR_NULL_ATTACH_STORE)** — `89 86 84 00 00 00`
MOV [ESI+0x84],EAX in FUN_0070C680 (EAX = new(0xA4) object constructed by
FUN_00972380 via CALL @0x0070C715, or 0 on allocation failure via XOR EAX,EAX
@0x0070C71C; guarded by the entry CMP [ESI+0x84],EDI @0x0070C6BE). The
full chain re-validated pin-by-pin in CORRECTED_PIN_LEDGER.csv (setter →
bulk-attach loop FUN_00703E80 → driver FUN_004B0980 → registration
FUN_00707FB0 → dispatcher FUN_0073C870 entry 5 → getter [0x00BA590C] →
manager mode/enum FUN_007080C0 → mode condition FUN_00703CD0 → slot predicate
FUN_0070CC80 → callback 0x0070BEF0; consumer chain FUN_0070DCF0 re-pinned:
gate CMP @0x0070DD1A, stream loads @0x0070DD6A/@0x0070DD7E →
FUN_00971AD0/FUN_00971650). All 133 corrected pins: 0 failures.

## Terminal fields (exact)

```text
RUN_ID = PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004
BASE_SHA = a0e176803aed23b19040d4310de1668efec4511f
PUBLICATION_HEAD_SHA = POST_PUSH_ONLY
RUN_STATUS = COMPLETED
EXE_IDENTITY = PASS (8015872 B, SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31)
FACTORY_PLUS_84_ASSIGNMENT_CORE = CONFIRMED_STATIC_CONDITIONAL
ASSIGNMENT_FUNCTION = FUN_0070C680
ASSIGNMENT_VA = 0x0070C71E
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
BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS = 1685
CENSUS_UNRESOLVED_ROWS = 1217
FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES = 828
REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE = 5
REJECTED_READ_NOT_WRITE = 1003
ADDRESS_PROVENANCE_UNRESOLVED = 828
NEW_BACKING_SOURCE_RE_EXECUTED = NO
TEMPLATES_VFS_OPENED = NO
RECORD_A_ANALYZED = NO
MODEL_194013_TRACE_EXECUTED = NO
CLIENT_EXECUTED = NO
KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES
PACKAGE_CORRECTION_STATUS = CORRECTED
CANONICAL_GATE_EFFECT = NONE
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

This correction resolved pin/address/QC, census encoding/boundary/provenance
and vtable/polymorphism claim-scope defects ONLY; it made no runtime-value
claims and reopened no predecessor verdict.

## ANTI-SUCCESS-THEATER record

- MEASURED_QUANTITY: the corrected pin ledger (133 same-VA records) and the
  corrected census (2,612 raw rows with full effective-address decoding,
  trusted-boundary verification and provenance-disciplined classification) —
  every number in this report is machine-derived from those artifacts.
- INDEPENDENT_SOURCE_OF_TRUTH: pinned-EXE bytes; every rel32 target computed
  only after E8+operand+boundary validation; the negative-control battery
  (A–F) demonstrates the gates actually fail on corrupted/synthetic inputs.
- WHY_NON_CIRCULAR: the corrected census re-derives every row from raw bytes
  with a decoder that passes the mandated unit battery; classifications rest
  on measured encodings, trusted boundaries and re-verified window evidence —
  never on register names or decode failures.
- FAILURE_CASES_DETECTED: 2 declassified CALL records (0x004B0A02,
  0x004B0A21 — measured bytes ≠ E8); the CONTROL B mutant (enumeration
  excluding 20006) fails the membership gate; CONTROL A/D mutants fail the
  raw-evidence gates; CONTROL C/E non-boundary VAs produce FAIL/NOT_VERIFIED
  with no promoted target; CONTROL F proves the ESP-SIB row stays UNRESOLVED.

## Honest boundaries

1. STATIC-ONLY: no runtime observation of any kind.
2. EXAMINED_ENCODING_CANDIDATE_CLOSURE=CLOSED is scoped to the declared
   encodings/effective-address forms/trusted boundary coverage; the 828
   unresolved write candidates are honest bounds, not failures; and even
   their complete resolution would not establish
   EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE (invariant NOT_ESTABLISHED).
3. DIRECT_VPTR_STORE_IN_EXAMINED_CTOR=NOT_OBSERVED is an observation over the
   EXAMINED ctor extent only; ASSIGNED_OBJECT_VTABLE=UNVERIFIED and
   OBJECT_POLYMORPHISM=NOT_ESTABLISHED are the honest global states.
4. The 5 proven-provenance rejections rest on re-verified window byte
   evidence (4 layout controls) and machine-checked manager-this flow
   (manager wrapper); the ADDRESS_PROVENANCE=UNRESOLVED rows (828) are
   unresolved by discipline, not by convenience.
5. Known-lead discipline unchanged: the same-ctor call site @0x0072FA76 in
   the templates.vfs reader-chain region remains LEAD ONLY (validated as a
   CALL; no bridge claim).
