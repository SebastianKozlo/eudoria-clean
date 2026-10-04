# HANDOFF — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004

RUN_ID: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004
Executor: pe-reconstruction | Dispatch: PE-MASTER direct (bounded correction
contract, NO_NESTED_TASKS, publication assigned in-contract) | 2026-10-04.

## RUN_STATUS

**RUN_STATUS = COMPLETED; PACKAGE_CORRECTION_STATUS = CORRECTED** (F84-C1 +
F84-C2 + F84-C3 + P3 corrections all executed with fresh measurements; the
fresh targeted QC passed — see QC_REPORT.md; the honest UNRESOLVED census
candidates remain UNRESOLVED by discipline, which is a corrected-honesty
result, not a failure).

## THE CORRECTION IN FIVE LINES

1. **F84-C1 (pins)**: 133-record authoritative same-VA pin ledger, 0
   failures. Corrected: callback MOV @0x0070CC9B (immediate @0x0070CC9C =
   0x0070BEF0; historical record declared 0x0070CC9A and published the
   opcode-contaminated 0x70BEF0B8); cursor+0x3C allocation CALL @0x0097244A →
   0x0095D3BE (historical 0x00972449 produced the negative phantom
   "0x-0B96BCA"); EDI save @0x00708025 `89 7C 24 30` (historical
   "0x00708030" was the stack displacement misread as an address); 0x004B0A02
   and 0x004B0A21 DECLASSIFIED as CALL records (measured bytes 0x01/0xF5);
   the real CALL in the region pinned: 0x004B0A1E → 0x00401E70. Every CALL
   target is now promoted ONLY after byte[VA]==E8 + full operand + trusted
   boundary.
2. **F84-C2 (census)**: MOD01 disp8 0x84 is −0x7C (385 negative-control rows);
   POSITIVE +0x84 requires effective +132 (2,227 rows, all disp32); no
   register-name rejections (828 ADDRESS_PROVENANCE=UNRESOLVED write
   candidates); no not-an-instruction inferences from failed decodes;
   declared trusted boundary sources only (known entries, CC-padding-
   delimited, RET-delimited); decoder passes the mandated unit battery
   (7/3/4/REJECT). Fresh quantities: RAW=2612, positive=2227,
   boundary-confirmed=1685, KN confirmed writes=2, read-not-write=1003,
   proven wrong-object=5, CENSUS_UNRESOLVED_ROWS=1217,
   FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES=828 (two defined denominators).
3. **F84-C3 (vtable/polymorphism)**: the historical prefilled vtable flag (SUPERSESSION_LEDGER S-21)
   superseded by the bounded machine search over the examined ctor —
   DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED (exactly one offset-0
   store in the extent: the cursor buffer store `89 07` @0x00972452, base
   EDI, not the machine-checked this-register ESI); global:
   ASSIGNED_OBJECT_VTABLE = UNVERIFIED, OBJECT_POLYMORPHISM =
   NOT_ESTABLISHED, KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES (3 examined
   callsites only).
4. **P3**: 0xA4 = 164 B (assigned object; 0x118=280 is the FACTORY size);
   the 129-vs-64 denominator ambiguity superseded by the two defined
   quantities; FUN_0070BF40 = measured 16-byte literal body, no semantic-role
   promotion; function-ledger hygiene recorded (8_DECLARED_AND_MECHANICALLY_
   REPRODUCED; PRE_ANALYSIS_CHRONOLOGY_INDEPENDENTLY_ESTABLISHED=NO;
   ACTUAL_HISTORICAL_BUDGET_OVERRUN=NOT_ESTABLISHED); ctor call-site census
   machine-measured (10 raw, 10 boundary-confirmed).
5. **PRESERVED CORE SCIENCE** (re-measured, unchanged):
   FACTORY_PLUS_84_ASSIGNMENT_CORE=CONFIRMED_STATIC_CONDITIONAL;
   ASSIGNMENT_FUNCTION=FUN_0070C680; ASSIGNMENT_VA=0x0070C71E;
   ASSIGNMENT_STORE_BYTES=89 86 84 00 00 00; ASSIGNED_OBJECT_SIZE=0xA4/164 B;
   ASSIGNED_OBJECT_CONSTRUCTOR=FUN_00972380;
   STATIC_FACTORY_MEMBER_IDENTITY=CONFIRMED_WITH_EXAMINED_PATH_CONDITIONS;
   both known stores physically re-pinned (0x0070D013 INITIALIZATION_NULL;
   0x0070C71E CONDITIONAL_OBJECT_OR_NULL_ATTACH_STORE).

## TERMINAL STATE (exact strings in FINAL_REPORT.md)

Two confirmed stores WITHIN THE EXAMINED CENSUS (never worded as "exactly
two exist in the entire client"); EXAMINED_ENCODING_CANDIDATE_CLOSURE=CLOSED
(scoped to the declared encodings/effective-address forms/boundary coverage);
EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE=NOT_ESTABLISHED (invariant);
ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT=UNVERIFIED;
WRITE_TO_CONSUMER_VALUE_PRESERVATION=NOT_ESTABLISHED;
FACTORY_PLUS_84_LIFETIME_SINGLE_ASSIGNMENT=NOT_ESTABLISHED;
ULTIMATE_VALUE_SOURCE=UNKNOWN; WORLD_INSTANCE_SEMANTIC=NOT_ESTABLISHED;
WORLD_XYZ_RECOVERED=NO; all preserved predecessor states carried verbatim
(FINAL_REPORT.md "Preserved predecessor states").

## What the NEXT run needs to know

- The recommended next science experiment remains OBJECT_BACKING_PROVENANCE
  (the historical FIRST_MISSING_EDGE) — it is DESIGNED but NOT EXECUTED and
  requires independent post-audit and new human authorization. The pinned
  entry points stand corrected and revalidated: the post-attach method
  0x00972DF0 (called by the setter @0x0070C742, body NOT decoded), the reader
  family FUN_00971AD0/FUN_00971650, the driver "Cache\"/"Parameters\" locals
  — WITHOUT templates.vfs/RECORD_A/Model 194013/placement/XYZ.
- The corrected machinery (03_SCRIPTS/x86dec.py + pebnd.py) is reusable for
  any future pin/census work: fail-closed decoder with mandated unit-battery
  semantics; trusted-boundary sources DECLARED (T1/T2/T3) with exact-landing
  sequential decode; DIRECT CALL VALIDATION that refuses non-E8/boundary-
  unconfirmed VAs (negative controls C/E prove the refusal).
- The census CSV is the corrected canonical row universe (2,612 rows with
  full EA fields); the 828 unresolved write candidates are the honest bound
  for "unknown additional writes within the examined encodings" — a future
  run may resolve individual candidates ONLY with proven provenance (never
  register naming) and must keep EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE
  NOT_ESTABLISHED.
- LEAD discipline unchanged: the same-ctor call site @0x0072FA76 (templates.vfs
  reader-chain region) is a LEAD ONLY (validated as a CALL → 0x00972380; no
  bridge claim; anti-numeric-coincidence discipline).

## FOR PE-MASTER (audit pointers)

- Claim matrix source: FINAL_REPORT.md (terminal fields block).
- Physical evidence: 01_RAW/C1_PIN_EVIDENCE.json (133 same-VA pin records),
  01_RAW/C2_CENSUS.json + CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv (2,612
  rows), 01_RAW/C3_OBJECT_SCOPE.json (machine vptr search + object scope),
  01_RAW/CQC_*.json (decoder unit battery, negative controls A-F, final QC),
  CORRECTED_PIN_LEDGER.csv.
- SUPERSESSION_LEDGER.md: 30 records, every ORIGINAL_EXCERPT a verbatim
  substring of its named READ-ONLY historical source file (machine
  quotecheck in the QC battery).
- Counter-check suggestions: re-hash the EXE; re-run any instrument with
  `--out`/`--csv` to a temp location and diff against the committed
  evidence; byte-read 0x0070CC9B/0x0097244A/0x00708025/0x004B0A1E and the
  two known stores; re-run the negative controls.
- Known QC limitations (honest): the trusted-boundary sources T1/T2/T3 are
  DECLARED heuristics with exact-landing sequential-decode safeguards (a
  hostile start cannot confirm a row unless the decode lands exactly on it);
  the census provenance is window-level (the 828 unresolved write candidates
  were NOT individually deep-proven — by discipline, since register naming
  and decode failures are not proof); DIRECT_VPTR_STORE_IN_EXAMINED_CTOR is
  scoped to the examined ctor extent (base/helper constructor bodies were NOT
  entered).

## PERSISTENCE

Output root verified non-existent, created fresh; foreign untracked paths
untouched; the historical R1 package READ-ONLY. Immediately before commit:
`git fetch`; actual remote master re-verified ==
a0e176803aed23b19040d4310de1668efec4511f (else BASE_DIVERGENCE, no push,
HARD STOP). Path-limited staging of THIS package + exactly one new
AUDIT_ENTRYPOINT.md row; no `git add .`; no force push; manifest generated
LAST (self-excluded; bijection verified). After push: local HEAD ==
origin/master after fetch == actual remote master. PUBLICATION_HEAD_SHA is
reported in the final executor response AFTER the push (pre-commit artifacts
carry PUBLICATION_HEAD_SHA = POST_PUSH_ONLY; no artifact embeds its own
commit SHA).

## HARD STOP

Per the contract: HARD STOP after publication verification. Do NOT begin
OBJECT_BACKING_PROVENANCE/templates.vfs/RECORD_A/Model 194013/placement/XYZ;
the next science experiment requires an independent post-audit of THIS
correction package and new human authorization.
