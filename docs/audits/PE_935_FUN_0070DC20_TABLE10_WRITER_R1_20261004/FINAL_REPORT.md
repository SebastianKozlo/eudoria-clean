# FINAL_REPORT — PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004

RUN_ID: PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004
RUN_CLASS: LOAD_BEARING | MODE: STATIC-ONLY (client never launched; raw byte
reads from the pinned EXE + manual x86 decode + machine call-target/byte/
branch verification; no Ghidra) | Executor: pe-reconstruction (PE-MASTER
bounded worker contract; NO_NESTED_TASKS; publication authorized in-contract).

## THE ONE QUESTION AND THE ANSWER

DOES FUN_0070DC20 (the record-apply candidate called @0x0070DDBD), directly
or through a bounded subordinate setter, WRITE ATTRIBUTE ID 10 INTO
TABLE[10] OF THE SAME class-20006 COMPONENT THAT THE AUDITED class-20006/
property-tag-6 GETTER LATER READS?

**ANSWER (S2 level, byte-pinned): YES.**

FUN_0070DC20 is the create-and-apply orchestrator of the record path:
it creates the per-receiver class-20006 component with the canon default-0
value table (FUN_0070D990), applies the record read from the factory+0x84
stream by FUN_0070DCF0 — and THAT apply, through the bounded subordinate
chain FUN_00726900 -> FUN_0075F660 -> int-traits vtable slot 5
(FUN_009777F0), writes for each record entry (tag, value) the VALUE read
from the record cursor into the entry **[class_obj+0x40] + id*4** where
**id = slot(tag)->id = tag+4** — for the audited slot-6 tag this is
**id 10 -> &table[10]**, with the exact byte-pinned store
**`89 02` MOV [EDX],EAX @0x00977810** (value read `8B 04 10` @0x00977807).
FUN_0070DC20 then inserts (receiver -> class_obj) into the SAME
factory+0x0C cache map the getter-side lookup (FUN_0070E100 ->
FUN_004D1430 -> node+0x14) consumes — so the written object IS the object
the audited getter later reads table[10] from (SAME_COMPONENT_IDENTITY =
CONFIRMED; identity-preserving chain, not numeric coincidence).

The selection form is: the RECORD contains a property TAG (u16 per loop
entry), converted to the ATTRIBUTE ID by the factory schema descriptor
(FUN_0070C180 -> slot; id = slot+8; id = tag+4 byte-pinned in the SLOT_ADD
writer `83 C1 04` @0x0070CBF6). The mechanism therefore deterministically
writes &table[10] whenever the applied record carries tag 6 (the audited
attribute; tags are runtime record data — STATIC-ONLY run, no record
content claim).

The value entering the write is the record's value field (u32 read through
the record cursor — TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD).
Per the contract THIS RUN STOPS at that boundary: the ULTIMATE source of the
record value (templates.vfs / other VFS / network / cache / embedded /
disk) is NOT determined (ULTIMATE_VALUE_SOURCE = UNKNOWN); the factory+0x84
stream setter/backing was NOT traced.

## Success level

S2 (the BEST possible result of this run): the exact writer is confirmed.
GETTER_RESULT_PRODUCER = CONFIRMED_AT_IMMEDIATE_WRITER_LEVEL — the
immediate writer of the value the audited getter returns as its lookup key
is identified (this chain), while the ultimate provenance of that value
remains UNKNOWN by design.

## Exact identities (writer-side, independently derived)

- WRITER_FUNCTION: FUN_009777F0 (ArkRTTraitsInt "read u32 from cursor and
  store" — vtable 0x00A9C670 slot 5, dword @0x00A9C684 = 0x009777F0,
  machine-read; canon-corroborated by the 20002_PAYLOAD30 run).
- WRITER_VA: 0x00977810 (`89 02` MOV [EDX],EAX; EDX = &table[id]).
- WRITE targets: TABLE_BASE = [class_obj+0x40] (of the component created
  inside FUN_0070DC20); TABLE_INDEX = slot->id = tag+4 (= 10 for tag 6);
  SOURCE = u32 at [cursor.base+cursor.pos] @0x00977807.
- ORCHESTRATOR: FUN_0070DC20 (extent 0x0070DC20..0x0070DCF0, thiscall
  (factory; receiver, &cursor, mode), RET 0xC; returns the class_obj).
- APPLY LOOP: FUN_00726900 (record payload grammar: [flags u16 | 0xFFFF +
  ext u16] + [count u16] + count x (tag u16 + traits-typed value); also
  ORs flags into class_obj+0x30 and, at mode word 1 (constant on this
  path), reads a u32-length typed blob via class_obj->vtable[3] — NOT
  decoded, out of scope).
- CONTROL: the same loop body writes &table[6] for tag 2 and &table[10]
  for tag 6 through the identical instructions (same int traits, same
  store) — the mechanism genuinely discriminates attribute identity
  (CONTROL_CASE = PASS).

## Terminal fields (exact)

```text
BASE_SHA = 2bfb0f23c5b438eef7a8af47a963260d1df193b1
HEAD_SHA = (this publication commit; discover: git log -1 -- docs/audits/PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004)
EXE_IDENTITY = PASS
FUN_0070DC20_IDENTITY = CONFIRMED (extent 0x0070DC20..0x0070DCF0; thiscall (factory; receiver, &cursor, mode); RET 0xC; returns the created class_obj or 0)
FUN_0070DC20_ROLE = ATTRIBUTE_VALUE_WRITER (orchestrator; the store executes through the bounded subordinate chain FUN_00726900 -> FUN_0075F660 -> FUN_009777F0)
SAME_COMPONENT_IDENTITY = CONFIRMED
ATTRIBUTE10_SELECTION = CONFIRMED
TABLE10_WRITE = CONFIRMED
CANDIDATE_A_WRITER_ROLE = CONFIRMED_ATTRIBUTE10_WRITER
GETTER_RESULT_PRODUCER = CONFIRMED_AT_IMMEDIATE_WRITER_LEVEL
TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD
ULTIMATE_VALUE_SOURCE = UNKNOWN
FILE_DERIVED_VALUE_EXCLUDED = NO
RECORD_A_RELATION = NOT_ESTABLISHED
PHYSICAL_TEMPLATE_RECORD_TO_GETTER_RESULT = NOT_ESTABLISHED
CONTROL_CASE = PASS
NEW_FUNCTION_COUNT = 8
FUNCTION_BUDGET_PRECHECK = PASS
FIRST_MISSING_EDGE = TABLE10_VALUE_SOURCE_PROVENANCE
GETTER_RESULT_TO_LOOKUP_KEY = PRESERVED_CONFIRMED
C1 = PRESERVED_CLOSED
C2 = PRESERVED_CLOSED
S1_STATIC_MECHANISM = PRESERVED_CONFIRMED
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED
MODEL_JOIN_EXECUTED = NO
MODEL_194013_TRACE_EXECUTED = NO
POSITION_RECOVERY_GOAL = OUT_OF_SCOPE
WORLD_XYZ_RECOVERED = NO
NEW_PLACEMENT_SCIENCE_EXECUTED = YES
NEXT_EXPERIMENT_EXECUTED = NO
CANONICAL_GATE_EFFECT = NONE
```

## FUNCTION BUDGET (hard pre-check enforced — the R1-overrun lesson)

MAX_NEW_FUNCTIONS_ANALYZED_IN_DETAIL = 8; NEW_FUNCTION_COUNT = 8 (at the
limit, never exceeded; NO 9th detailed decode; every entry has count_before
recorded in FUNCTION_LEDGER.csv before its analysis). Counted:
FUN_0070DC20, FUN_0075D8D0, FUN_00726900, FUN_00413440,
FUN_00413450, FUN_0075F660, FUN_009777F0*, FUN_0070CBC0* (* = canon
functions counted conservatively because this run derived new semantics
beyond their canon pins — 009777F0: fail-path zero store + advance-4;
0070CBC0: factory+4 flag ORs + full arg mapping). Narrow reverifications
(NOT counted; pin-level only; no new semantic claims):
FUN_0070DCF0, FUN_0070D990, FUN_0070C180, FUN_0040DE60, FUN_007374C0,
FUN_0092B660, FUN_0070E100, FUN_004D1430, FUN_00977A50, FUN_007374F0
(call-site), FUN_0075F6D0, FUN_004926E0/FUN_00977780 (target-level),
FUN_00971AD0/FUN_00971650/FUN_0040E160 (target-level), the audited getter
chain region 0x004C5520-0x004C5568, and the second-caller context
0x007046C0-0x00704744 (surface context only; its containing function was
NOT deep-decoded). NOT decoded (out of scope, disclosed):
class_obj->vtable[3] tail reader, delegate vtable slots, traits-null
fallbacks 0x00412D80/0x004129C0, FUN_00843340, candidate B.

## FIRST_MISSING_EDGE + the ONE recommended next experiment (designed, NOT executed)

FIRST_MISSING_EDGE = TABLE10_VALUE_SOURCE_PROVENANCE — the chain now ends
at a byte-pinned writer whose value comes from the record cursor; the next
edge is the provenance of the factory+0x84 stream that feeds FUN_00971AD0
(candidate A's reader): identify the factory+0x84 stream SETTER (who
attaches the stream object to the factory — a bounded imm32/`MOV
[reg+0x84]` census around the manager init FUN_00707E50 and the
factory-lazy-init region), then resolve the stream object's backing data
source class (file-backed VFS / network / cache / embedded) — WITHOUT
re-touching the getter/writer chain. That single bounded experiment would
convert ULTIMATE_VALUE_SOURCE from UNKNOWN to a physical/message class or
a controlled rejection, directly closing the candidate-A provenance edge.
(Model 194013 landmark trace remains a separate future track.)

## Evidence index

- 01_RAW/S1..S5 (5 bounded instrument records; S5 = the final 92-pin QC
  battery, 0 failures).
- 03_SCRIPTS/s1..s5 (the bounded read-only instruments).
- FUN_0070DC20_DECODE.md (extent/arguments/return + full decode),
  ATTRIBUTE10_WRITE_CHAIN.md (Phases A/C/D/E + anti-theater),
  SAME_COMPONENT_IDENTITY.md (Phase B), CONTROL_CASE.md,
  QC_REPORT.md (Q1-Q12), INPUT_IDENTITIES.md, FUNCTION_LEDGER.csv,
  WRITER_CHAIN.csv, HANDOFF.md.

## PERSISTENCE

Before the first canonical write: git fetch; local HEAD == origin/master ==
actual remote master == 2bfb0f23c5b438eef7a8af47a963260d1df193b1 (rev-parse
+ ls-remote; recorded in INPUT_IDENTITIES.md); output root created fresh
(verified non-existent first); foreign untracked paths untouched.
Immediately before commit: actual remote master re-verified ==
2bfb0f23c5b438eef7a8af47a963260d1df193b1 (else BASE_DIVERGENCE, no push,
HARD STOP). Path-limited staging of THIS package + exactly one NEW
AUDIT_ENTRYPOINT.md row; no `git add .`; no force push; historical
packages READ-ONLY. COMMITTED_PACKAGE_MANIFEST_SHA256.csv generated LAST
(self-excluded; scope = all physical files of this package + the updated
AUDIT_ENTRYPOINT.md); bijection verified. After push: local HEAD ==
origin/master after fetch == actual remote master, all equal.

## Honest boundaries

1. STATIC-ONLY: no runtime observation. Whether the candidate-A path is
   live (manager mode in {1,2}; factory+0x84 stream non-NULL) is runtime
   state (R1 canon gate, preserved); the writer identity is structural —
   WHEN this path runs, the byte-pinned chain writes table[10] for records
   carrying tag 6. Which tags a given runtime record carries is runtime
   data; NO record-content claim is made (and templates.vfs was NOT
   opened).
2. The record framing (8 bytes skipped by FUN_0070DCF0 before the apply)
   and the record payload grammar ([flags|0xFFFF+ext][count](tag,value)*)
   are decoded STRUCTURALLY only; their physical file format is NOT
   identified (out of scope by contract).
3. FUN_0070DC20 is a generic per-factory helper (2 call sites; the second
   re-applies records to already-cached components through the same
   FUN_00726900) — the CONFIRMED verdict is for the audited 20006 factory
   instance and its slot-6/id-10 attribute; it does not assert that every
   use writes id 10.
4. The class_obj tail blob reader (vtable[3]) and the delegate notify are
   byte-pinned shells only (undecoded, out of scope).
5. All preserved predecessor states (GP1/GP2/GP3, C1/C2, S1, RECORD_A,
   non-claims) are untouched; this run adds the writer identity without
   reopening any closed question.
