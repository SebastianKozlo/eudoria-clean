# FINAL_REPORT — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004

RUN_ID: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004
RUN_CLASS: LOAD_BEARING | MODE: STATIC-ONLY (client never launched; raw byte reads
from the pinned EXE + machine call-target verification + a machine instruction-
boundary verifier; no Ghidra) | Executor: pe-reconstruction (PE-MASTER bounded
worker contract; NO_NESTED_TASKS; publication assigned in-contract; QC_SCOPE =
SELF_CHECK_FACTORY_PLUS_84_ASSIGNMENT_OBJECT — executor self-check, explicitly NOT
an independent PE-MASTER audit).

## THE ONE QUESTION AND THE ANSWER

WHO ASSIGNS factory+0x84 AND WHAT EXACT VALUE/OBJECT IS WRITTEN THERE?

**ANSWER (S3 level, byte-pinned):**

1. **WHO (the producer/setter)**: the factory-class stream-attach method
   **FUN_0070C680**, store instruction **`89 86 84 00 00 00`
   MOV [ESI+0x84],EAX @0x0070C71E** (ESI = this). It is called with
   this = a manager-list FACTORY element by **FUN_00703E80** (the bulk-attach loop,
   CALL @0x00703EF0), which is driven by **FUN_004B0980** (the attach driver: it
   loads the manager singleton via FUN_00415470, builds driver locals from the
   string constants "Cache\" and "Parameters\", and passes {0x80, 8} locals +
   frame pointers). The attach chain is fully identity-preserving:
   [0x00BA590C] singleton → the SAME class dispatcher FUN_0073C870 (entry 5 →
   getter `MOV EAX,[0x00BA590C]; RET` @0x0073C8D8) → the registration
   FUN_00707FB0 appends the resolved pointer UNMODIFIED into the manager's factory
   list (vector {begin +0x78, end +0x7C, cap +0x80}; `MOV [EAX],EDI` @0x00708077,
   `ADD [ECX+4],4` @0x00708079) — the registration is driven by FUN_007080C0,
   which sets the MANAGER MODE (store @0x007080CA) and enumerates ALL class ids
   0x4E20..0x4E4B + 0x5DC1..0x5DD1 (20006 inside the first range; the enumerated
   calls @0x007080E3/@0x007080FB); the loop then passes each list element as the
   setter's this (register-propagated, no substitution).
2. **WHAT (the value/object)**: **a 0xA4-byte heap object constructed by
   FUN_00972380** (`PUSH 0xA4` @0x0070C6F9; ctor CALL @0x0070C715) — a
   **non-polymorphic record-stream object** (NO vtable anywhere in its ctor
   extent 0x00972380..0x009724D9; all methods direct-called: FUN_00971AD0 the
   per-record reader — the same function the consumer invokes on [factory+0x84] —
   FUN_00971650 the advance, and the post-attach method 0x00972DF0 whose body is
   NOT decoded), with an **embedded 0x80-byte record buffer/cursor at +0x3C**
   and {1, 0x80} pairs — structurally matching the consumer's record-read
   discipline (records ≤0x80 + 8-byte framing). On allocation failure the SAME
   store writes 0 (`XOR EAX,EAX` @0x0070C71C). The store executes only when the
   member is NULL at entry (guard `CMP [ESI+0x84],EDI` @0x0070C6BE → return TRUE
   if already attached): a guarded, idempotent lazy attach.
3. **The member's other writer**: only ONE other census-confirmed write exists:
   the base-constructor NULL initialization `MOV [ESI+0x84],EBX` (EBX=0)
   **@0x0070D013** in FUN_0070CF80, which runs for EVERY factory class (the 20006
   derived ctor FUN_0073B820 calls it with the class id: `PUSH 0x4E26` @0x0073B871
   + CALL @0x0073B87D).

Per the contract, this run STOPS at the object identity: the backing data source of
the stream object (file / VFS / network / cache / embedded) is NOT identified
(ULTIMATE_VALUE_SOURCE = UNKNOWN). The driver's "Cache\" / "Parameters\" string
constants are bounded context recorded from an already-required function, NOT a
provenance classification. The same stream-ctor call site inside the
templates.vfs reader-chain region (0x0072FA76) is recorded as a LEAD ONLY — no
bridge claim (anti-numeric-coincidence discipline).

## Consumer-side re-pin (the minimum required)

FACTORY_PLUS_84_CONSUMER_FIELD = CONFIRMED — FUN_0070DCF0 receives the factory as
this (`MOV ESI,ECX` @0x0070DD16) and addresses factory+0x84 at three
machine-verified sites: the NULL gate `CMP [ESI+0x84],EBX` @0x0070DD1A / JE
@0x0070DD20, and the stream loads `MOV ECX,[ESI+0x84]` @0x0070DD6A (→ CALL
FUN_00971AD0 @0x0070DD75) and @0x0070DD7E (→ CALL FUN_00971650 @0x0070DD84).
(Pin-precision note: the predecessor's prose pins "@0x0070DD17/1D" were 3 bytes
early; the predecessor's raw S7 window is byte-identical to this run's evidence —
a pin precision correction, not a contradiction.)
FACTORY_PLUS_84_CONSUMER_FUNCTION = FUN_0070DCF0 (contract-expected value,
machine re-pinned).

## Census (PHASE A) — bounded, mechanical, full-.text

Scope: every .text raw form with displacement 0x84 — dword write forms
(MOV [reg+0x84],reg and MOV [reg+0x84],imm32, mod01/mod10, incl. all SIB
encodings), read forms (8B/CMP 39) and LEA (8D) forms as negative controls,
byte/word partial-width forms. 2,604 raw hits; every hit got instruction-boundary
verification (anchor-decode from a padding-delimited function start OR multi-start
greedy decode with a fail-closed mini length-decoder), base-register extraction,
containing-function attribution, and window-level provenance. 483 dword-write-form
hits; 74 with non-stack base (70 boundary-verified); exactly **2
CONFIRMED_FACTORY_PLUS_84_WRITE** rows (0x0070D013 INITIALIZATION_NULL; 0x0070C71E
NONNULL_ASSIGNMENT). Mechanical rejections: 598 reads
(REJECTED_READ_NOT_WRITE — incl. the consumer's own three reads and the setter's
entry guard), 1,488 REJECTED_WRONG_OBJECT (all stack-based SIB forms — the factory
is heap-allocated, new 0x118 @0x0073E2CC — plus the manager-ctor LEA-wrapper and
4 layout-evidence rejections), 387 REJECTED_UNRELATED_OFFSET (non-instruction byte
patterns + partial-width stores), 129 UNRESOLVED (honest window-level bound).
Natural negative controls inside the bound: the sibling-class ctor 0x0074955A
(writes +0x88/+0x89 as BYTES — layout mismatch vs the factory's dword +0x88
vector), 0x006D4F88 (integer 4 at +0x84 of another class), 0x0075138F
(synchronization object at its +0x88), 0x007196AA (static globals into
+0x84/+0x88/+0x8C). Full evidence: FACTORY_PLUS_84_WRITE_CENSUS.csv (2,604 rows,
real csv module) + 01_RAW/S2_CENSUS.json.

## Terminal fields (exact)

```text
RUN_ID = PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004
BASE_SHA = 288c53cc6b2552bbf9dc41907677e3fa1b6ab56d
PUBLICATION_HEAD_SHA = POST_PUSH_ONLY
RUN_STATUS = COMPLETED
EXE_IDENTITY = PASS (8015872 B, SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31)
FACTORY_PLUS_84_CONSUMER_FIELD = CONFIRMED
FACTORY_PLUS_84_CONSUMER_FUNCTION = FUN_0070DCF0
FACTORY_PLUS_84_ASSIGNMENT = CONFIRMED
FACTORY_PLUS_84_NONNULL_ASSIGNMENT = CONFIRMED
ASSIGNMENT_FUNCTION = FUN_0070C680 (the factory-class stream-attach setter)
ASSIGNMENT_VA = 0x0070C71E
ASSIGNMENT_WRITE_CLASS = NONNULL_ASSIGNMENT (0 on allocation failure; guarded by the +0x84==NULL entry check)
FACTORY_IDENTITY_AT_ASSIGNMENT = CONFIRMED (identity-preserving: same dispatcher-resolved [0x00BA590C] singleton appended to the manager list unmodified, iterated unmodified, passed as this; conditional resolution byte-pinned: manager mode in {1,3} -> slot-predicate-0x40 via FUN_0070CC80; else element+4 bit 0x20; else bit 0x2000 via FUN_0070BF40; pass/fail at any runtime event = runtime state, STATIC-ONLY)
ASSIGNED_VALUE_REPRESENTATION = OBJECT_POINTER
ASSIGNED_OBJECT_IDENTITY = 0xA4-BYTE NON-POLYMORPHIC RECORD-STREAM OBJECT (embedded 0x80-B record cursor at +0x3C; {1,0x80} pairs; direct-call methods FUN_00971AD0/FUN_00971650/0x00972DF0)
ASSIGNED_OBJECT_VTABLE = NONE (non-polymorphic; no vtable store in the ctor extent)
ASSIGNED_OBJECT_CONSTRUCTOR = FUN_00972380
ASSIGNMENT_TO_CONSUMER_FIELD_IDENTITY = CONFIRMED (static member identity only)
ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED
WRITE_TO_CONSUMER_VALUE_PRESERVATION = NOT_ESTABLISHED
FACTORY_PLUS_84_INITIAL_STATE = ZERO_AT_EXAMINED_INIT_PATH
FACTORY_PLUS_84_NULL_INIT_COUNT = 1
FACTORY_PLUS_84_CLEAR_RESET_COUNT = 0
FACTORY_PLUS_84_NONNULL_ASSIGNMENT_COUNT = 1
FACTORY_PLUS_84_UNRESOLVED_WRITE_COUNT = 64
FACTORY_PLUS_84_LIFETIME_SINGLE_ASSIGNMENT = NOT_ESTABLISHED
ULTIMATE_VALUE_SOURCE = UNKNOWN
FILE_DERIVED_VALUE_EXCLUDED = NO
RECORD_A_RELATION = NOT_ESTABLISHED
WRITER_MECHANISM = PRESERVED_CONFIRMED_STATIC_CONDITIONAL
ATTRIBUTE10_WRITER_MECHANISM = PRESERVED_CONFIRMED
WRITER_FUNCTION = FUN_009777F0 (preserved)
WRITER_VA = 0x00977810 (preserved)
TAG6_TO_ID10 = PRESERVED_CONFIRMED
SAME_STORAGE_IDENTITY = PRESERVED_CONFIRMED_STATIC_CONDITIONAL
SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED (preserved; this run resolved the ASSIGNMENT side, not the specific getter-value producer chain — the two are distinct: the setter assigns the member; which write supplied the value at any specific later getter event remains unproven)
WRITE_TO_LATER_GETTER_VALUE_PRESERVATION = NOT_ESTABLISHED
NO_CLOBBER_BETWEEN_WRITE_AND_READ = NOT_ESTABLISHED (broad no-clobber analysis OUT OF SCOPE; in-scope fact only: the setter's own entry guard makes the store skip an already-non-NULL member — setter idempotence, not a lifetime proof)
TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD (preserved)
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED
MODEL_194013_TRACE_EXECUTED = NO
WORLD_XYZ_RECOVERED = NO
NEW_PLACEMENT_SCIENCE_EXECUTED = YES
NEXT_EXPERIMENT_EXECUTED = NO
NEW_FUNCTION_COUNT = 8
FUNCTION_BUDGET_VALIDATION = PASS (derived from FUNCTION_LEDGER.csv parsed from disk by the QC validator; mandatory 9-function mutant battery: structure=PASS, derived=9, budget-limit predicate=FAIL)
FIRST_MISSING_EDGE = OBJECT_BACKING_PROVENANCE
CANONICAL_GATE_EFFECT = NONE
```

## Success level

**S3** (the contract's best expected outcome for this question): non-null
assignment CONFIRMED + FACTORY_IDENTITY_AT_ASSIGNMENT = CONFIRMED + immediate
object identity established (ASSIGNED_OBJECT_IDENTITY measured) +
ASSIGNMENT_TO_CONSUMER_FIELD_IDENTITY = CONFIRMED, with
ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED and
WRITE_TO_CONSUMER_VALUE_PRESERVATION = NOT_ESTABLISHED carried per the dispatch
clarifications. The run STOPS at object identity: FIRST_MISSING_EDGE =
OBJECT_BACKING_PROVENANCE is the next edge, for a SEPARATELY authorized run.

## FUNCTION BUDGET (hard pre-check honored)

MAX_NEW_FUNCTIONS_ANALYZED_IN_DETAIL = 8; the ledger
(FUNCTION_LEDGER.csv, csv.writer format, parsed from disk by the QC) counts
exactly 8 functions that received NEW detailed semantic analysis:
FUN_0070C680 (the setter), FUN_00703E80 (the loop), FUN_004B0980 (the driver),
FUN_00707FB0 (register+append), FUN_007080C0 (manager-mode + class enumeration),
FUN_00972380 (the stream ctor), FUN_00703CD0 (mode condition {1,3}),
FUN_0070CC80 (slot-predicate scan). Explicitly NOT counted (pin-level /
transcription-level / re-pin, each with its reason in the ledger):
FUN_0070CF80 (established +0x84 store re-pin), FUN_0073B820 (ctor call-edge pin),
FUN_00415470, FUN_0073C870/FUN_0073C8D8, FUN_00707E50 (list-triple zero
transcription), FUN_0070BF40 (14-byte helper kept at transcription level — its
internal rule is NOT load-bearing: the condition evaluation at any runtime event is
runtime state), FUN_0070BFD0 (census-row transcription),
FUN_00971AD0/FUN_00971650 (canon target re-pins), FUN_00972DF0 (target pin only —
body NOT decoded, STOP at object identity), the 0x0072FA76 ctor site (LEAD ONLY).
The pre-analysis hard check was honored: no 9th detailed analysis was performed.

## ANTI-SUCCESS-THEATER record

- MEASURED_QUANTITY: the writer instruction(s) of [this+0x84] for the factory
  class, from a full-.text displacement census — NOT inferred from the consumer.
- INDEPENDENT_SOURCE_OF_TRUTH: pinned-EXE bytes; every rel32 target
  machine-computed; the S1 battery caught and forced correction of 31 real
  executor pin slips + 1 comparison bug before publication (final: 0 failures —
  the battery demonstrably fails).
- WHY_NON_CIRCULAR: the setter was found from the write side; its this-provenance
  was derived upward (loop → list → registration → dispatcher) independently of
  the consumer chain; the two sides meet only at the same dispatcher getter and
  the same member expression this+0x84. The identity does NOT rest on "same
  factory family" — it rests on the unmodified pointer flow.
- FAILURE_CASE_DETECTED: the natural controls listed in the Census section
  (sibling-class layout mismatches, the integer-4 ctor, the read-form rows, the
  stack-based SIB forms) — plus the in-run battery corrections above.

## FORBIDDEN-SHORTCUT / out-of-scope compliance

No proof rests on displacement-0x44 coincidence, same-family-only identity, NULL
init as provider identity, proximity, naming ("stream"), templates.vfs historical
reuse, or model/resource IDs. templates.vfs was NOT opened; RECORD_A untouched; no
backing provenance; no broad no-clobber analysis; no re-decode of the table[10]
writer/getter chain (all its fields preserved verbatim above); no Model 194013; no
NIF/model join; no position/XYZ; no client run; no network. The scripts read ONLY
the pinned EXE (QC Q14 machine-verifies no forbidden input appears in any script).

## FIRST_MISSING_EDGE + the ONE recommended next experiment (designed, NOT executed)

FIRST_MISSING_EDGE = OBJECT_BACKING_PROVENANCE — the attached 0xA4 record-stream
object's backing data source. The narrowest next discriminator (ONE experiment,
separately authorized): decode the stream-object's own method family —
FUN_00972380's companions 0x00972DF0 (the post-attach method already pinned as
this+0x84's method call) and the reader internals of FUN_00971AD0's backing read
path — to determine what the stream READS FROM (the driver's "Cache\" /
"Parameters\"-built locals are the leading input), WITHOUT touching
templates.vfs/RECORD_A/Model 194013/placement/XYZ. If the backing resolves to a
physical source class, ULTIMATE_VALUE_SOURCE can be classified in a bounded way;
else it stays UNKNOWN.

## Evidence index

- `01_RAW/S1_ANCHORS.json` — identity + the full anchor/pin battery (0 failures;
  singleton/manager reference censuses; all chain call-target verifications).
- `01_RAW/S2_CENSUS.json` + `FACTORY_PLUS_84_WRITE_CENSUS.csv` — the full census
  (2,604 rows) with boundary verification + provenance + classification.
- `01_RAW/S3_CHAINS.json` — the 8 counted-function windows + the chain edges
  (e1-e6 + consumer chain) + the stream-object identity evidence.
- `01_RAW/S4_QC.json` — the Q1-Q14 battery results + the budget validator +
  the 9-function mutant battery.
- `03_SCRIPTS/s1..s4` — the bounded read-only instruments (own PE mapper, own
  fail-closed length decoder, real csv module, sys.dont_write_bytecode).
- `ASSIGNMENT_CHAIN.md` (Phases B/C/E/F), `OBJECT_IDENTITY.md` (Phase D),
- `INPUT_IDENTITIES.md`, `FUNCTION_LEDGER.csv`, `QC_REPORT.md`, `HANDOFF.md`,
- `COMMITTED_PACKAGE_MANIFEST_SHA256.csv` (generated LAST, self-excluded).

## PERSISTENCE

Before the first canonical write: output root verified non-existent, created fresh;
foreign untracked paths untouched. Immediately before commit: git fetch; actual
remote master re-verified == 288c53cc6b2552bbf9dc41907677e3fa1b6ab56d (else
BASE_DIVERGENCE, no push, HARD STOP). Path-limited staging of THIS package +
exactly one new AUDIT_ENTRYPOINT.md row; no `git add .`; no force push; historical
packages READ-ONLY. COMMITTED_PACKAGE_MANIFEST_SHA256.csv generated LAST
(self-excluded; scope = all physical files of this package + the updated
AUDIT_ENTRYPOINT.md); bijection verified. After push: local HEAD == origin/master
after fetch == actual remote master. PUBLICATION_HEAD_SHA is reported in the final
executor response AFTER the push (pre-commit artifacts carry
PUBLICATION_HEAD_SHA = POST_PUSH_ONLY; no artifact embeds its own commit SHA).

## Honest boundaries

1. STATIC-ONLY: no runtime observation; whether the attach or the record-read ever
   executes for the 20006 factory in any session is runtime state. All verdicts
   are structural ("WHEN the pinned path runs...").
2. The condition battery is byte-pinned at instruction level; the internal rule of
   the slot-predicate callback 0x0070BEF0 and the 14-byte flag helper
   FUN_0070BF40 are NOT decoded (disclosed; not load-bearing for the member-
   identity verdicts).
3. The stream object's backing source is UNKNOWN by contract design (STOP at object
   identity); the "Cache\" / "Parameters\" constants are driver context only.
4. 129 census rows remain UNRESOLVED at window level (honest bound; no absence
   claim beyond the measured scan classes); the UNRESOLVED write-candidate count
   (64) counts boundary-verified non-stack dword-write candidates not resolved to
   any factory object.
5. All preserved predecessor states (the writer mechanism chain, C1/C2/S1,
   RECORD_A/B, SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER=UNVERIFIED, etc.) are
   untouched; no supersession of any historical claim is made by this run.
