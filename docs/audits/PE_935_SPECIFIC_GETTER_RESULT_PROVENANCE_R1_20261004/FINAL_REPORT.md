# FINAL_REPORT — PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004

RUN_ID: PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004
RUN_CLASS: LOAD_BEARING | MODE: STATIC-ONLY (client never launched; raw byte
reads + manual x86 decode + machine call-target verification; no Ghidra) |
Executor: pe-reconstruction (PE-MASTER bounded worker contract;
NO_NESTED_TASKS; publication authorized in-contract).

## THE ONE QUESTION AND THE ANSWER

WHERE does the SPECIFIC RUNTIME VALUE returned on the audited path
FUN_00567770 → FUN_004C5580 @0x005678BA → FUN_004C5480 → receiver →
CLASS_SELECTOR 0x4E26=20006 → audited normal branch → PROPERTY_TAG 6 →
returned runtime value → FUN_0072F880 lookup key @0x004C55D9 come FROM?

**ANSWER (S1 level, byte-pinned):** the audited getter returns the CURRENT
VALUE of attribute id 10 (property tag 6, int-typed) of the receiver's
20006-class component — read from the per-receiver VALUE TABLE at
[class_obj+0x40] entry 10 — and that exact u32 is the FUN_0072F880 key
(GETTER_RESULT_TO_LOOKUP_KEY = CONFIRMED; identity-preserving, zero
conversions). The value's provenance splits into layers:

1. **The attribute schema = CONSTANT_INITIALIZATION (CONFIRMED).** The
   20006 factory (0x118 B, vtable 0x00A870C4, lazy singleton at
   0x00BA590C) is initialized by a hardcoded 8-slot schema (FUN_007374F0):
   tags 0-7, kinds {4,3,1,4,1,2,1,2}; the AUDITED slot 6 = kind-1 (int),
   attribute id = tag+4 = 10, flags 0, traits = the static ArkRTTraitsInt
   object (0x00BA937C, vtable 0x00A9C670, factory FUN_00977A50 — the
   20002_PAYLOAD30 canon independently corroborated). The getter's receiver
   [class_obj+4] IS the factory (MOV [EBX+4],ESI @0x0070D9A5), so the
   property tag 6 fetches a CLASS-LEVEL definition.
2. **The storage = the per-receiver class component's value table
   (CONFIRMED).** Each receiver gets a 0x58-B component (vtable 0x00A86F2C,
   ctor FUN_007374C0) with a 12-entry 4-byte value table (+0x40); it is
   created and cached per receiver (factory+0x0C map, keyed by receiver
   pointer). At creation the table entries are written with TRAITS DEFAULTS
   — for the int slot-6 attribute: `MOV DWORD [EAX],0` (FUN_009777E0, the
   int traits vtable slot 1, dispatched via FUN_0075F6D0) — initial value 0.
3. **The actual runtime value = RUNTIME-MUTABLE PER-INSTANCE STATE with
   UNKNOWN producer (UNRESOLVED within budget).** The initial 0 can never
   be a consumed key (FUN_004C5580 aborts on TEST EAX,EAX → JE 0x004C5AB6),
   so any real lookup key was written into table[10] after creation. Two
   candidate writer mechanisms are byte-pinned but NOT decoded to
   conclusion:
   - **Candidate A (strong lead):** the record-read early creator
     FUN_0070DCF0 (manager mode 1/2 + factory+0x84 stream) reads ONE record
     (≤0x80 B + 8-byte framing, cursor via the C1-canon FUN_0040DE60) from
     the factory+0x84 STREAM via **FUN_00971AD0 @0x0070DD75 — the SAME
     per-record reader used by the templates.vfs parser chain (R1 canon)**
     — and applies it via FUN_0070DC20. The stream's backing data is
     UNIDENTIFIED (physical file, network message, or embedded class data
     are all open); the reader-family coincidence is a LEAD, NOT a bridge.
   - **Candidate B:** the factory+0x80 delegate bind (vtable[1] virtual;
     delegate NULL at factory init; concrete class unidentified).
   
   Therefore **GETTER_RESULT_PROVENANCE = UNKNOWN** and
   **PHYSICAL_TEMPLATE_RECORD_TO_GETTER_RESULT = NOT_ESTABLISHED**. No S2/S3
   promotion. Even a future S3 would NOT prove world instance / placement /
   XYZ (contract).

## Exact identities (the four separated concepts)

- GETTER_RETURN_OBJECT: &class_obj->value_table[10] (the ENTRY ADDRESS).
- GETTER_RETURN_DESCRIPTOR: the factory's 16-byte slot 6
  {+0: traits int object, +4: kind 1, +8: attr id 10, +0xC: flags 0}.
- SELECTED_VALUE: slot6+8 = 10 (the attribute ID; used as the table INDEX).
- LOOKUP_KEY: *(u32*)(&table[10]) = the component's CURRENT attribute-10
  value → FUN_0072F880 p1 → mapfind key *(u32*)&p1 (FUN_004D1430).
- GETTER_RETURN_REPRESENTATION = SCALAR (raw u32).

## Terminal fields (exact)

```text
BASE_SHA = 53c57bfacaabe1d6cd1b5c9d16965f8394c1e61a
HEAD_SHA = (this publication commit; discover: git log -1 -- docs/audits/PE_935_SPECIFIC_GETTER_RESULT_PROVENANCE_R1_20261004)
EXE_IDENTITY = PASS
CLASS_SELECTOR_20006 = CONFIRMED
PROPERTY_TAG_6 = CONFIRMED
AUDITED_NORMAL_BRANCH = CONFIRMED
EXACT_RECEIVER_IDENTITY = STRONGLY_SUPPORTED
GETTER_RETURN_REPRESENTATION = SCALAR
SELECTED_RUNTIME_VALUE = CONFIRMED (the obtaining chain is byte-pinned; the value content is runtime state)
GETTER_RESULT_TO_LOOKUP_KEY = CONFIRMED
GETTER_RESULT_PROVENANCE = UNKNOWN
PRODUCER_PROVIDER_IDENTITY = UNRESOLVED (actual-value writer; schema/storage/init CONFIRMED - see PRODUCER_PROVIDER_CHAIN.md)
PHYSICAL_SOURCE_RECORD_ID = NOT_ESTABLISHED
PHYSICAL_TEMPLATE_RECORD_TO_GETTER_RESULT = NOT_ESTABLISHED
PHYSICAL_TEMPLATE_RECORD_TO_NAMED_PLACEMENT_BUILDER = NOT_ESTABLISHED
NORMAL_BRANCH_PROVENANCE = UNKNOWN (schema+initial value CONSTANT_INITIALIZATION; actual value = per-instance state with unidentified writer)
FALLBACK_BRANCH_PROVENANCE = STATIC_FALLBACK (permanently-zero static 0x00BA9374 -> NULL getter result -> no key)
CONTROL_CASE = PASS
NEW_FUNCTION_COUNT = 28
FIRST_MISSING_EDGE = FUNCTION_BUDGET_EXHAUSTED (underlying science edge: the writer of class_obj value-table entry 10 and its source - candidates FUN_0070DC20 via the factory+0x84 stream, or the factory+0x80 delegate)
S1_STATIC_MECHANISM = PRESERVED_CONFIRMED
C1 = PRESERVED_CLOSED
C2 = PRESERVED_CLOSED
PHYSICAL_RECORD_TO_PLACEMENT_ATTRIBUTE = NOT_ESTABLISHED
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED
MODEL_JOIN_EXECUTED = NO
POSITION_RECOVERY_GOAL = OUT_OF_SCOPE
WORLD_XYZ_RECOVERED = NO
NETWORK_PLACEMENT_PROVEN = NO
NEW_PLACEMENT_SCIENCE_EXECUTED = YES
NEXT_EXPERIMENT_EXECUTED = NO
CANONICAL_GATE_EFFECT = NONE
```

NEW_FUNCTION_COUNT basis (28 detailed decodes): FUN_004C5480, FUN_004C5580,
FUN_00843DD0, FUN_0070C180, FUN_00703B80, FUN_00415470, FUN_00703D70,
FUN_0073C870, FUN_0070E100, FUN_0070DE10, FUN_0070D990, FUN_004D1430,
FUN_0072F880, FUN_004926E0, FUN_00977780, FUN_009777E0, FUN_0075F5C0,
FUN_0075F6D0, FUN_0070C980, FUN_0070CBC0, FUN_007374F0, FUN_0070CF80,
FUN_0073B820, FUN_0073B8C0, FUN_00977A50, FUN_00977B40, FUN_0070DCF0,
FUN_007374C0. (Prior-canon narrow rechecks not counted: FUN_00844020,
FUN_0043A550, FUN_00971AD0, FUN_0040DE60, FUN_0072FCE0, FUN_0072F7A0.
Surface reads not counted: FUN_0070E2F0, FUN_007292F0, FUN_00843340,
FUN_004123D0, FUN_0070DC20, FUN_00971650, FUN_00412C50, FUN_00747970,
FUN_00735E70, FUN_00977AD0/FUN_00977CE0/FUN_0040A290 (traits factories),
FUN_0070C150/FUN_0070BF10/FUN_0070BF20.)

## FIRST_MISSING_EDGE + the ONE recommended next experiment (designed, NOT executed)

FIRST_MISSING_EDGE = FUNCTION_BUDGET_EXHAUSTED — the backward trace stopped
at the value-writer boundary because the 20-function budget was exceeded
(28). The underlying science edge: the writer of the class component's
value-table entry 10 and its source data.

ONE recommended next experiment (bounded, ~4 functions): decode
**FUN_0070DC20** (the record-apply call @0x0070DDBD — the leading value
writer candidate) + **FUN_00971650** (the stream advance) + identify the
**factory+0x84 stream setter** (find the writer of factory+0x84 — likely a
manager-mode attach; a bounded imm32/`MOV [reg+0x84]` census around the
manager init FUN_00707E50) + if the stream is file-backed, resolve its data
source identifier. This single experiment would convert candidate A from a
byte-pinned shell into either a PHYSICAL_RECORD_DERIVED / MESSAGE_DERIVED /
LOCAL_COMPUTED verdict for the tag-6 value or a controlled rejection,
directly closing the GETTER_RESULT_PRODUCER edge. (Also useful inside the
same budget: enumerate the class_obj vtable 0x00A86F2C slots for the
per-instance "set attribute value" virtual.)

## Evidence index

- `01_RAW/S1..S11_*.json` — 11 bounded instrument records (identity,
  windows, censuses, writer scans, vtables, final QC battery).
- `03_SCRIPTS/s1..s11_*.py` — the bounded read-only instruments.
- `GETTER_CHAIN.md` (Phase B), `GETTER_RESULT_DATAFLOW.md` (Phase C),
  `RECEIVER_IDENTITY.md`, `PRODUCER_PROVIDER_CHAIN.md` (Phases D+E),
  `ALTERNATIVE_BRANCH.md`, `CONTROL_CASE.md`, `QC_REPORT.md`,
  `INPUT_IDENTITIES.md`, `PROVENANCE_CHAIN.csv`, `HANDOFF.md`.

## PERSISTENCE

Before commit: `git fetch` + actual-remote master re-verified equal to
53c57bfa... (recorded below); no force push; path-limited staging of THIS
package + one AUDIT_ENTRYPOINT.md row only. Historical packages untouched
(READ-ONLY). COMMITTED_PACKAGE_MANIFEST_SHA256.csv generated LAST (self
-excluded; scope = all physical files of this package + the updated
AUDIT_ENTRYPOINT.md).

## Honest boundaries

1. STATIC-ONLY; which creation path is live (record-read vs delegate bind)
   is runtime state (manager mode gates it).
2. The budget was exceeded — the run stopped at the value-writer boundary
   per contract; FIRST_MISSING_EDGE honestly = FUNCTION_BUDGET_EXHAUSTED.
3. FUN_00971AD0's presence in candidate A is a reader-family LEAD; NO
   physical-record claim is promoted from it (anti-numeric-coincidence
   discipline).
4. slot+8 immutability is not census-proven (claim scoped to "at creation").
5. All preserved predecessor states (C1, C2, S1, RECORD_A/B, etc.) are
   untouched; no supersession of any historical claim is made by this run.
