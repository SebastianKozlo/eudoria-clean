# HANDOFF — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004

RUN_ID: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004
Executor: pe-reconstruction | Dispatch: PE-MASTER direct (bounded worker contract,
NO_NESTED_TASKS, publication assigned in-contract) | 2026-10-04.

## RUN_STATUS

**RUN_STATUS = COMPLETED** (the bounded question answered to S3 — the contract's
best expected level; QC_PASS 14/14; publication performed per the contract's
publication clause).

## THE RESULT IN FIVE LINES

1. **WHO assigns factory+0x84**: FUN_0070C680 — the factory-class stream-attach
   setter — store `MOV [ESI+0x84],EAX` @0x0070C71E (ESI = this), called by the
   bulk-attach loop FUN_00703E80 (CALL @0x00703EF0) over the MANAGER's factory
   list, driven by FUN_004B0980 (manager singleton via FUN_00415470; driver
   locals built from "Cache\" / "Parameters\" constants; {0x80, 8} locals).
2. **The identity chain (CONFIRMED, identity-preserving)**: the SAME dispatcher
   FUN_0073C870 (entry 5 → getter [0x00BA590C] @0x0073C8D8) that serves the
   consumer path also feeds the registration FUN_00707FB0, which appends the
   resolved factory pointer UNMODIFIED into the manager's list
   ({begin +0x78, end +0x7C, cap +0x80}; append @0x00708077); FUN_007080C0 sets
   the MANAGER MODE and enumerates ALL classes 0x4E20..0x4E4B + 0x5DC1..0x5DD1
   (20006 inside); the loop passes each element as this — no substitution anywhere.
3. **WHAT is written**: a 0xA4-byte heap object constructed by FUN_00972380 — a
   NON-POLYMORPHIC record-stream object (no vtable; direct-call methods
   FUN_00971AD0/FUN_00971650/0x00972DF0; embedded 0x80-byte record cursor at
   +0x3C; {1,0x80} pairs) — or NULL on allocation failure. Guarded: the store runs
   only when the member is NULL at entry (idempotent lazy attach).
4. **The other census-confirmed write**: the base-ctor NULL init
   `MOV [ESI+0x84],EBX` (EBX=0) @0x0070D013 in FUN_0070CF80 (runs for every
   factory class incl. 20006 via FUN_0073B820's CALL @0x0073B87D).
5. **Census**: 2,604 raw hits; 483 dword-write forms; 74 non-stack (70
   boundary-verified); exactly 2 CONFIRMED factory+0x84 writes; 1,488
   wrong-object rejects (incl. all stack-based SIB forms + 4 layout-evidence
   rejections); 598 read-not-write rejects; 387 unrelated-offset rejects; 129
   UNRESOLVED (64 write-candidates among them — honest window-level bound).

## TERMINAL STATE (exact strings in FINAL_REPORT.md)

S3 outcome: FACTORY_PLUS_84_ASSIGNMENT = CONFIRMED;
FACTORY_PLUS_84_NONNULL_ASSIGNMENT = CONFIRMED;
FACTORY_IDENTITY_AT_ASSIGNMENT = CONFIRMED;
ASSIGNMENT_TO_CONSUMER_FIELD_IDENTITY = CONFIRMED (static member identity only);
ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED;
WRITE_TO_CONSUMER_VALUE_PRESERVATION = NOT_ESTABLISHED;
ASSIGNED_VALUE_REPRESENTATION = OBJECT_POINTER;
ASSIGNED_OBJECT_CONSTRUCTOR = FUN_00972380;
ASSIGNED_OBJECT_VTABLE = NONE (non-polymorphic);
FIRST_MISSING_EDGE = OBJECT_BACKING_PROVENANCE;
NEW_FUNCTION_COUNT = 8 (budget 8, validator PASS + 9-function mutant battery);
ALL predecessor states preserved verbatim (WRITER_MECHANISM /
SAME_STORAGE_IDENTITY / SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER=UNVERIFIED /
TABLE10_SOURCE_VALUE_REPRESENTATION=RECORD_FIELD / WORLD_* / MODEL_194013=NO).

## What the NEXT run needs to know (if the recommended experiment is authorized)

- The next missing edge: the ATTACHED STREAM OBJECT'S BACKING SOURCE. The
  already-pinned entry points: the stream method 0x00972DF0 (called by the setter
  right after the store, this = the attached object, args = driver locals),
  FUN_00971AD0/FUN_00971650 internals (the reader family), and the driver's
  "Cache\"/"Parameters\"-built locals ({0x80, 8} config values visible).
- The stream object layout is pinned in 01_RAW/S3_CHAINS.json (stream_object) —
  0xA4 bytes, +0x18=-1 sentinel, +0x3C cursor {0x80 buffer}, {1,0x80} pairs.
- LEADS recorded, NOT proven: the same ctor is used at 0x0072FA76 inside the
  templates.vfs reader-chain region (reader-family coincidence — a class-level
  lead, NOT a data-source bridge).
- The manager list/mode machinery is now pinned: FUN_007080C0 (mode store +
  enumeration), FUN_00707FB0 (append), FUN_00703E80 (loop + condition battery:
  mode ∈ {1,3} → slot-predicate-0x40 via FUN_0070CC80; else +4 flag bits 0x20 /
  0x2000 via FUN_0070BF40). The predicate internals (0x0070BEF0, the flag-bit
  derivation in FUN_0070CBC0's schema ORs) are NOT decoded.
- Budget-critical: 8 slots were consumed; the NOT-counted/pin-level inventory is
  in FUNCTION_LEDGER.csv (rows 9-18) — a next run must re-derive, not assume.

## FOR PE-MASTER (audit pointers)

- Claim matrix source: FINAL_REPORT.md (terminal fields block).
- Physical evidence: 01_RAW/S1_ANCHORS.json (pin battery, 0 failures after the
  31-slip correction cycle), 01_RAW/S2_CENSUS.json + the census CSV,
  01_RAW/S3_CHAINS.json, 01_RAW/S4_QC.json.
- Counter-check suggestions: re-hash the EXE; re-run
  03_SCRIPTS/s2_write_census.py (deterministic, package-local outputs); re-parse
  the ledger with the QC validator; byte-read 0x0070C71E and 0x0070D013.
- Known QC limitations (honest): boundary verification is a fail-closed greedy
  decoder over the common x86 subset (unknown opcodes abort a path); the
  containing-function attribution is padding-delimited + a known-entry table
  (extent-limited 0x1000); window-level provenance is tag-based — the 64
  UNRESOLVED write-candidates were NOT individually deep-proven (disclosed).
- Scope compliance: templates.vfs NOT opened; RECORD_A untouched; no backing
  provenance; no re-decode of the table[10] chain; no Model 194013; no placement
  science beyond the assignment-object question; scripts read ONLY the pinned EXE.

## PUBLICATION

Path-limited commit of THIS package + exactly one new AUDIT_ENTRYPOINT.md row;
manifest COMMITTED_PACKAGE_MANIFEST_SHA256.csv generated LAST (self-excluded);
remote re-verified == BASE_SHA before the push; no force push; historical
packages READ-ONLY. PUBLICATION_HEAD_SHA is reported in the final executor
response AFTER the push (artifacts carry PUBLICATION_HEAD_SHA = POST_PUSH_ONLY).
