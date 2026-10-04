# HANDOFF — PE_935_FUN_0070DC20_TABLE10_WRITER_R1_20261004

To: PE-MASTER. From: pe-reconstruction (bounded worker; NO_NESTED_TASKS).
This package answers the dispatched question to the S2 level within the
stated scope limits; the terminal sequence (stop science -> preserve ->
targeted SELF_CHECK QC -> report/handoff/entrypoint -> manifest LAST ->
commit/push -> remote verify) was executed as required.

## One-paragraph result

FUN_0070DC20 IS the audited writer: it creates the per-receiver
class-20006 component (FUN_0070D990, default-0 value table), applies the
record read by FUN_0070DCF0 through the bounded subordinate chain
FUN_00726900 -> FUN_0075F660 -> int-traits vtable slot 5 (FUN_009777F0),
which writes each record entry (tag u16, value) into **&[class_obj+0x40] +
id*4** with **id = slot(tag)->id = tag+4** — so the audited tag 6 writes
**table[10]** via the byte-pinned store **`89 02` @0x00977810** (value
read from the record cursor @0x00977807) — and then inserts
(receiver -> class_obj) into the SAME factory+0x0C cache map the getter-side
lookup consumes (FUN_0070E100 -> FUN_004D1430 -> node+0x14).
TABLE10_WRITE = CONFIRMED; SAME_COMPONENT_IDENTITY = CONFIRMED;
ATTRIBUTE10_SELECTION = CONFIRMED (record tag -> schema descriptor ->
id 10); CANDIDATE_A_WRITER_ROLE = CONFIRMED_ATTRIBUTE10_WRITER;
GETTER_RESULT_PRODUCER = CONFIRMED_AT_IMMEDIATE_WRITER_LEVEL;
ULTIMATE_VALUE_SOURCE = UNKNOWN (contract stop BEFORE provenance); the
control (tag 2 -> table[6] vs tag 6 -> table[10] through the identical
instructions) PASSES. Budget: 8/8 functions (hard pre-check enforced; no
9th decode; the two canon functions counted conservatively for new
semantics). QC: 92/92 machine pins PASS, 12/12 gates PASS (SELF_CHECK
scope).

## What is preserved (no retractions)

Everything: GETTER_RESULT_TO_LOOKUP_KEY, CLASS_SELECTOR_20006,
PROPERTY_TAG_6, the audited normal path, IMMEDIATE_VALUE_STORAGE,
ULTIMATE_VALUE_SOURCE=UNKNOWN, FILE_DERIVED_VALUE_EXCLUDED=NO,
RECORD_A_RELATION=NOT_ESTABLISHED, DEFAULT_CREATION_PATH_INITIAL_VALUE=0,
C1/C2, S1_STATIC_MECHANISM, GP1/GP2/GP3 scoped wording, and all
world/XYZ/model/network non-claims. This run ADDS the immediate writer
identity; it does not reopen any closed question.

## What THIS run adds (all byte-pinned, machine-verified)

- FUN_0070DC20 fully decoded (extent/args/return/role) + its genericity
  (2 call sites; the second re-applies to cached components).
- The record-apply loop FUN_00726900 and the record payload grammar
  ([flags|0xFFFF+ext][count](tag,value)*) — structural only.
- The traits dispatch chain + the exact store (FUN_009777F0
  READ @0x00977807 / STORE @0x00977810; fail path zero-store).
- The schema id formula id=tag+4 byte-pinned in SLOT_ADD
  (`83 C1 04` @0x0070CBF6) — the writer-side id-10 derivation.
- The writer/reader identity bridge: insert into factory+0x0C
  (@0x0070DC7C) == the getter-side map (FUN_0070E100, FUN_004D1430).
- The guard pair named: EnterCriticalSection/LeaveCriticalSection
  (KERNEL32 IAT slots 0x00A75064/0x00A7506C, hints 152/593) on
  class_obj+8 and factory+0x24.

## Deviations (honest record)

- MULTIPLE hand-analysis slips were made and ALL were caught by the
  machine battery and corrected pre-publication (guard-pair rel32 slip;
  a 4-byte tokenization drift in the long S2 window that briefly produced
  phantom 0x0040DE5C/0x0070C17C "thunk" targets; the 0x0075F65C->0x0075F660
  dispatch-target slip; several pin-VA off-by-1/2/4; an 8-byte-stride
  import-walk bug). Full list in QC_REPORT.md; no semantic verdict was
  affected (each correction was confirmed by direct-VA probes + battery
  re-runs; final battery 92/92).
- NEW_FUNCTION_COUNT = 8 == the MAX (not exceeded): two of the eight are
  canon functions counted conservatively for new semantics; the ledger
  (FUNCTION_LEDGER.csv) discloses the classification per entry for audit.

## The single next experiment (designed, NOT executed)

FIRST_MISSING_EDGE = TABLE10_VALUE_SOURCE_PROVENANCE. Decode the
factory+0x84 stream SETTER (bounded `MOV [reg+0x84]` / imm32 census around
the manager init FUN_00707E50 + the factory lazy-init region) and resolve
the stream object's backing source class — WITHOUT touching the now-closed
writer chain. That closes candidate A's provenance edge
(ULTIMATE_VALUE_SOURCE) or rejects it cleanly.

## Audit pointers

- Verdict terminal fields: FINAL_REPORT.md.
- Chain detail: ATTRIBUTE10_WRITE_CHAIN.md + WRITER_CHAIN.csv.
- Component identity: SAME_COMPONENT_IDENTITY.md.
- Function budget: FUNCTION_LEDGER.csv (8 entries, pre-checks recorded).
- Raw evidence: 01_RAW/S1..S5 (S5 = final QC battery).
- Repo state: BASE 2bfb0f23...; publication = this package + one
  AUDIT_ENTRYPOINT.md row (path-limited; historical packages READ-ONLY).
