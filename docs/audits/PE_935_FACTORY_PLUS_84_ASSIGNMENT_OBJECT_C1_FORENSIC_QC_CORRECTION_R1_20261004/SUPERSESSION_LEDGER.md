# SUPERSESSION_LEDGER.md — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004

Every record below points to ACTUAL historical evidence: SOURCE_FILE (relative
to the repo root, inside the READ-ONLY historical package
`docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/`), the
FIELD/SECTION, and a VERBATIM excerpt. No historical literal field is invented
or reconstructed. The corrected statement cites this correction package's own
measured evidence (`01_RAW/C1_PIN_EVIDENCE.json`, `01_RAW/C2_CENSUS.json`,
`01_RAW/C3_OBJECT_SCOPE.json`, `CORRECTED_PIN_LEDGER.csv`,
`CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv`). The QC battery machine-verifies
every excerpt as a real substring of its named source file (quotecheck).

Historical package root below = `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/`.

---

## S-01 — F84-C3 (vtable/polymorphism overclaim)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/OBJECT_IDENTITY.md`
- FIELD/SECTION: the object table, ASSIGNED_OBJECT_VTABLE row
- ORIGINAL_EXCERPT: `| ASSIGNED_OBJECT_VTABLE | **NONE — the object is NON-POLYMORPHIC**: no vtable store exists anywhere in the ctor extent (searched C7 06/89 06/89 07/C7 07-style [this] stores of .rdata pointers); all its methods are invoked by DIRECT rel32 calls, not virtual dispatch |`
- DEFECT: the "searched ... patterns" claim was NOT a machine search — the
  historical S3 generator stored `vtable_store_found: false` as a PREFILLED
  value and the historical Q7 validated that literal (see S-21/S-24). "NONE"
  and "NON-POLYMORPHIC" are global claims unsupported by any measurement.
- SUPERSEDED_BY: the bounded machine search over the EXAMINED ctor extent
  (C3): `DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED` (decode completed
  RET_REACHED over 0x00972380..0x009724DA; exactly one offset-0 store found in
  the extent — the cursor buffer store `89 07` MOV [EDI],EAX @0x00972452 with
  base EDI ≠ the machine-checked this-register ESI). Global scope:
  `ASSIGNED_OBJECT_VTABLE = UNVERIFIED`, `OBJECT_POLYMORPHISM =
  NOT_ESTABLISHED`, `KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES` (measured over
  the 3 examined callsites only — NOT "all its methods").

## S-02 — P3 (decimal)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/OBJECT_IDENTITY.md`
- FIELD/SECTION: the object table, Allocation size row
- ORIGINAL_EXCERPT: `| Allocation size | 0xA4 bytes (280) |`
- DEFECT: 0xA4 = 164, not 280. 280 = 0x118 is a DIFFERENT object's size (the
  FACTORY allocation), which the historical package itself pins at
  `PUSH 0x118 @0x0073E2CC`.
- SUPERSEDED_BY: `ASSIGNED_OBJECT_SIZE = 0xA4/164 B` (C3 machine-measured: the
  setter's `68 A4 00 00 00` PUSH imm32 @0x0070C6F9 == 0xA4 == 164);
  `0x118 = 280` recorded as the FACTORY size (`68 18 01 00 00`
  @0x0073E2CC). Corrected everywhere in this package.

## S-03 — F84-C3/P3 (identity terminology)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/OBJECT_IDENTITY.md`
- FIELD/SECTION: terminal Phase D fields block
- ORIGINAL_EXCERPT: `ASSIGNED_OBJECT_IDENTITY       = 0xA4-BYTE NON-POLYMORPHIC RECORD-STREAM OBJECT`
- ORIGINAL_EXCERPT (2): `ASSIGNED_OBJECT_VTABLE         = NONE (non-polymorphic; no vtable store in the ctor)`
- DEFECT: the identity string bundles the unsupported non-polymorphic claim and
  states "RECORD-STREAM OBJECT" as a confirmed fact of identity.
- SUPERSEDED_BY: `ASSIGNED_OBJECT_STRUCTURAL_IDENTITY =
  CONFIRMED_WITHIN_EXAMINED_LAYOUT` (0xA4 allocation + FUN_00972380
  construction + examined internal stores + embedded cursor/buffer + known
  direct callsites); `FINAL_SEMANTIC_ROLE_RECORD_STREAM =
  STRONGLY_SUPPORTED` (semantic naming, NOT confirmed from structural
  observations alone); vtable status per S-01.

## S-04 — F84-C3 (methods claim)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: THE ONE QUESTION AND THE ANSWER, item 2 (WHAT)
- ORIGINAL_EXCERPT: `NO vtable anywhere in its ctor` — with the continuation
  `all methods direct-called: FUN_00971AD0 the`
- DEFECT: "all methods direct-called" is a global claim; only three callsites
  were examined.
- SUPERSEDED_BY: `KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES` measured over the
  examined callsites (0x0070DD75→0x00971AD0, 0x0070DD84→0x00971650,
  0x0070C742→0x00972DF0; all three validate as direct E8 rel32 calls);
  no statement about the object's full method set.

## S-05 — F84-C3 (terminal field)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: terminal fields block
- ORIGINAL_EXCERPT: `ASSIGNED_OBJECT_VTABLE = NONE (non-polymorphic; no vtable store in the ctor extent)`
- SUPERSEDED_BY: `ASSIGNED_OBJECT_VTABLE = UNVERIFIED` (S-01); the strongest
  permitted direct observation is
  `DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED`.

## S-06 — dispatch clarification 1 (absence-of-others wording)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: THE ONE QUESTION AND THE ANSWER, item 3
- ORIGINAL_EXCERPT: `**The member's other writer**: only ONE other census-confirmed write exists:`
- DEFECT: "only ONE other census-confirmed write EXISTS" reads as a global
  exclusivity claim; what was measured is: within the examined census, one
  other confirmed store.
- SUPERSEDED_BY: within the corrected examined census there is one other
  confirmed store (0x0070D013, INITIALIZATION_NULL);
  `EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED` — alias writes,
  helper-mediated writes, bulk/memory-copy writes, other address
  constructions, unexamined encodings and runtime mutation are NOT excluded by
  any census result.

## S-07 — F84-C2 (census distribution)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: Census (PHASE A) paragraph
- ORIGINAL_EXCERPT: `entry guard), 1,488 REJECTED_WRONG_OBJECT (all stack-based SIB forms — the factory` — and:
- ORIGINAL_EXCERPT (2): `patterns + partial-width stores), 129 UNRESOLVED (honest window-level bound).`
- DEFECT: the 1,488 wrong-object rejections rested largely on the ESP/EBP
  register-naming shortcut (S-18); the census totals are superseded as
  canonical conclusions.
- SUPERSEDED_BY: the fresh corrected census:
  RAW_PATTERN_ROWS=2612, POSITIVE_PLUS_84_ENCODING_ROWS=2227,
  NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS=385,
  REJECTED_READ_NOT_WRITE=1003,
  REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE=5
  (4 layout-evidence controls with window bytes re-verified + the manager-ctor
  wrapper with machine-checked manager-this provenance),
  KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES=2, CENSUS_UNRESOLVED_ROWS=1217,
  FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES=828 (definitions in C2).

## S-08 — P3 (denominator)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: terminal fields block
- ORIGINAL_EXCERPT: `FACTORY_PLUS_84_UNRESOLVED_WRITE_COUNT = 64`
- SUPERSEDED_BY: the two separately-defined, separately-derived quantities:
  `CENSUS_UNRESOLVED_ROWS = 1217` (all unresolved rows: boundary-unresolved
  read/LEA rows + all unresolved write candidates) and
  `FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES = 828` (write-form
  positive-encoding rows not resolved to a confirmed factory write or a
  proven wrong-object rejection).

## S-09 — P3 (denominator, the other half of the ambiguity)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/ASSIGNMENT_CHAIN.md`
- FIELD/SECTION: PHASE C table, UNRESOLVED row
- ORIGINAL_EXCERPT: `| FACTORY_PLUS_84_UNRESOLVED_WRITE_COUNT | **129** | census rows classified UNRESOLVED at window level`
- DEFECT: the same quantity name carried 64 in FINAL_REPORT and 129 in
  ASSIGNMENT_CHAIN — the superseded denominator ambiguity.
- SUPERSEDED_BY: as S-08 (both historical values are superseded by the fresh
  measured pair with published definitions).

## S-10 — dispatch clarification 1 (exactly-two wording)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/ASSIGNMENT_CHAIN.md`
- FIELD/SECTION: THE ANSWER IN ONE PARAGRAPH
- ORIGINAL_EXCERPT: `factory+0x84 is assigned by exactly TWO confirmed mechanisms within the census bound:`
- DEFECT: "exactly TWO ... within the census bound" invites the global reading
  "exactly two sites exist in the entire client".
- SUPERSEDED_BY: `KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES = 2` — two confirmed
  stores WITHIN THE EXAMINED CENSUS (positive observations that survive the
  corrected re-pin); the corrected wording never translates "two confirmed
  sites within the examined census" into "exactly two sites exist";
  `EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED`.

## S-11 — F84-C1 (operand-VA error)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/01_RAW/S3_CHAINS.json`
- FIELD/SECTION: assignment_chain_edges.e2_register_append.edi_saved_for_append
- ORIGINAL_EXCERPT: `"edi_saved_for_append": "0x00708030",`
- DEFECT: 0x00708030 is the STACK-SLOT DISPLACEMENT VALUE (+0x30), not an
  instruction VA; the actual instruction is `89 7C 24 30`
  MOV [ESP+0x30],EDI starting at 0x00708025.
- SUPERSEDED_BY: corrected pin `register_EDI_saved_for_append`:
  instruction_va=0x00708025, opcode_bytes=89 7C 24 30, length 4, EA
  base=ESP disp8=+0x30, boundary CONFIRMED from KNOWN_FUNCTION_ENTRY
  FUN_00707FB0 (CORRECTED_PIN_LEDGER.csv).

## S-12 — F84-C1 (phantom CALL #1)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/01_RAW/S3_CHAINS.json`
- FIELD/SECTION: assignment_chain_edges.e4_driver.driver_call_after_parameters_str
- ORIGINAL_EXCERPT: `"driver_call_after_parameters_str": {` — with the continuation lines
- ORIGINAL_EXCERPT (2): `"target": "0x514B0A07"`
- DEFECT: 0x004B0A02 is not a CALL — the measured byte there is 0x01 (byte 1 of
  the imm32 of `BB 01 00 00 00` MOV EBX,1 @0x004B0A01); the "target"
  0x514B0A07 was fabricated by reading a rel32 from a mid-instruction
  position.
- SUPERSEDED_BY: ledger record `driver_declassified_0x004B0A02`:
  DECLASSIFIED_NOT_A_CALL (CALL_VALIDATION=FAIL, byte_is_E8=false) +
  `driver_MOV_EBX_1` (the real instruction @0x004B0A01).

## S-13 — F84-C1 (phantom CALL #2)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/01_RAW/S3_CHAINS.json`
- FIELD/SECTION: assignment_chain_edges.e4_driver.driver_call_pre_attach
- ORIGINAL_EXCERPT: `"driver_call_pre_attach": {` — with the continuation lines
- ORIGINAL_EXCERPT (2): `"target": "0x190F8E25"`
- DEFECT: 0x004B0A21 is not a CALL — the measured byte there is 0xF5 (byte 3 of
  the rel32 operand of the REAL CALL @0x004B0A1E); the "target" 0x190F8E25 is
  fabricated.
- SUPERSEDED_BY: ledger record `driver_declassified_0x004B0A21`:
  DECLASSIFIED_NOT_A_CALL, plus the corrected NEW pin
  `driver_real_call_0x004B0A1E`: E8 4D 14 F5 FF @0x004B0A1E → 0x00401E70,
  boundary CONFIRMED (CORRECTED_VALIDATED).

## S-14 — F84-C1 (declared-VA ≠ read-VA + operand-position error)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/01_RAW/S1_ANCHORS.json`
- FIELD/SECTION: pins.condition_battery.slotpred_callback_ptr (pretty-printed record)
- ORIGINAL_EXCERPT: `"slotpred_callback_ptr": {` — with the continuation lines
- ORIGINAL_EXCERPT (2): `"va": 7392410,` (the declared VA 0x0070CC9A)
- ORIGINAL_EXCERPT (3): `"hex": "b8 f0 be 70 00",` (read at 0x0070CC9B — a DIFFERENT VA than declared)
- ORIGINAL_EXCERPT (4): `"imm32_value": "0x70BEF0B8"` (the opcode-contaminated immediate)
- DEFECT: the record declared VA 0x0070CC9A (7392410) but read its bytes at
  0x0070CC9B (declared VA ≠ VA used for byte reads), AND the immediate was
  read at the INSTRUCTION VA (0x0070CC9B) instead of the operand position
  (0x0070CC9C), producing the opcode-contaminated value 0x70BEF0B8.
- SUPERSEDED_BY: corrected pin `slotpred_callback_MOV_EAX_imm32`:
  instruction_va=0x0070CC9B (B8 F0 BE 70 00, MOV EAX,imm32, length 5),
  immediate operand at va+1 = 0x0070CC9C == 0x0070BEF0, boundary CONFIRMED
  from FUN_0070CC80 (CORRECTED_VALIDATED).

## S-15 — F84-C1 (mid-instruction rel32 + never-validated record)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/01_RAW/S1_ANCHORS.json`
- FIELD/SECTION: pins.stream_ctor.cursor_at_3C_buffer_new (pretty-printed record)
- ORIGINAL_EXCERPT: `"cursor_at_3C_buffer_new": {` — with the continuation lines
- ORIGINAL_EXCERPT (2): `"va": 9905225,` (0x00972449)
- ORIGINAL_EXCERPT (3): `"measured_target": "0x-0B96BCA"` (a NEGATIVE phantom "VA")
- DEFECT: the cursor+0x3C buffer allocation CALL is at 0x0097244A, not
  0x00972449 (9905225); the historical machinery read its rel32 from a
  mid-instruction position and produced a negative phantom "target"; additionally
  this record's expect/measured keys formed no complete check pair in the
  historical battery, so it was never validated at all.
- SUPERSEDED_BY: corrected pin `stream_ctor_buffer_alloc_CALL`:
  instruction_va=0x0097244A (E8 6F AF FE FF) → 0x0095D3BE, boundary CONFIRMED
  from FUN_00972380 (CORRECTED_VALIDATED).

## S-16 — F84-C1 (pin machinery itself)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/03_SCRIPTS/s1_identify_and_anchors.py`
- FIELD/SECTION: call_target() function docstring
- ORIGINAL_EXCERPT: `"""given a CALL/JMP instruction VA (opcode E8/E9 at call_va), machine-compute the target."""`
- DEFECT: the machinery computed a rel32 target from ANY supplied VA without
  proving the VA is a CALL/JMP boundary and without even checking byte[VA] ==
  0xE8/0xE9 — the direct cause of the phantom targets in S-12/S-13/S-15.
- SUPERSEDED_BY: the corrected DIRECT CALL VALIDATION (pebnd.validate_direct_call):
  byte[VA] MUST equal 0xE8; all 5 operand bytes must be present; the boundary
  must be CONFIRMED from a declared trusted source; only then
  TARGET = VA+5+signed_rel32(VA+1); any failure → FAIL|NOT_VERIFIED and NO
  target promoted (negative CONTROL C and CONTROL E demonstrate the failure
  paths).

## S-17 — F84-C2 (MOD01 signed displacement)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/03_SCRIPTS/s2_write_census.py`
- FIELD/SECTION: T1 raw pattern scan, displacement pattern table
- ORIGINAL_EXCERPT: `(1, b"\x84", 1, "MOD01_disp8"), (2, b"\x84\x00\x00\x00", 4, "MOD10_disp32")`
- DEFECT: MOD01 disp8 is SIGNED: raw 0x84 = −124 = −0x7C, NOT +0x84. The
  historical census represented every such row as `[reg+0x84]`
  (`desc = "MOV [%s+0x84],%s" % (REGS[rm], regf)`).
- SUPERSEDED_BY: all 385 MOD01-raw-0x84 rows are
  NEGATIVE_DISP8_MINUS_0x7C_CONTROL rows (encoding-level: a +132 displacement
  cannot be encoded as disp8 under any decoding); POSITIVE_PLUS_84 requires
  an actual effective signed displacement +132 (measured: 2227 rows, all
  MOD10 disp32).

## S-18 — F84-C2 (ESP/EBP register-naming rejection)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/03_SCRIPTS/s2_write_census.py`
- FIELD/SECTION: classify(), stack-relative rejection branch
- ORIGINAL_EXCERPT: `"stack-relative slot; the factory object is heap-allocated (new 0x118 "`
- DEFECT: rejection of every ESP/EBP-based row SOLELY from the register name
  (EBP is not automatically a frame pointer; ESP with an unresolved SIB index
  is not automatically a pure stack slot).
- SUPERSEDED_BY: no row is rejected from register naming; ESP/EBP-based write
  rows carry ADDRESS_PROVENANCE=UNRESOLVED and classification UNRESOLVED
  (measured in the corrected census; synthetic CONTROL F proves the
  discipline).

## S-19 — F84-C2 (boundary-failure inference)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/03_SCRIPTS/s2_write_census.py`
- FIELD/SECTION: classify(), boundary-unverified rejection branch
- ORIGINAL_EXCERPT: `"raw byte-pattern occurrence not at a verified instruction start "`
- DEFECT: a failed decode attempt was treated as proof of "not an
  instruction"/unrelated offset (the historical 387 REJECTED_UNRELATED_OFFSET
  class mixes this inference with partial-width stores).
- SUPERSEDED_BY: the corrected boundary policy: if no trusted decode reaches
  the candidate → BOUNDARY_STATUS=UNRESOLVED and the row stays UNRESOLVED; NO
  NOT_AN_INSTRUCTION/IMMEDIATE_DATA/WRONG_OBJECT inference is made from a
  failed decode. Multi-start decoding is NOT a trusted source.

## S-20 — F84-C2 (fail-closed decoder wording)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/03_SCRIPTS/s2_write_census.py`
- FIELD/SECTION: decoder banner
- ORIGINAL_EXCERPT: `# ---------------- mini x86 length decoder (bounded, fail-closed) ----------------`
- DEFECT: the historical decoder was NOT fail-closed in fact:
  (a) mod=0 SIB was missing (8B 04 85 00 00 00 00 decoded as length 2 instead
  of 7); (b) 66-prefixed immediates kept imm32 width (66 B8 01 00 → 6 instead
  of 4); (c) no truncation check (89 86 at a buffer end fabricated a length).
- SUPERSEDED_BY: the corrected decoder (03_SCRIPTS/x86dec.py) passes the
  mandated unit battery: `8B 04 85 00 00 00 00` → 7; `8B 04 24` → 3;
  `66 B8 01 00` → 4; `89 86` truncated → REJECT (no length fabricated).

## S-21 — F84-C3 (prefilled measurement value)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/01_RAW/S3_CHAINS.json`
- FIELD/SECTION: stream_object.vtable_store_found
- ORIGINAL_EXCERPT: `"vtable_store_found": false,`
- DEFECT: a PREFILLED literal in the generator, not a measurement.
- SUPERSEDED_BY: the C3 bounded machine search:
  DIRECT_VPTR_STORE_IN_EXAMINED_CTOR=NOT_OBSERVED (offset-0 store census in
  the extent: exactly 1 store, `89 07` @0x00972452, base EDI = the embedded
  cursor, NOT the machine-checked this-register ESI).

## S-22 — F84-C3 (prefilled prose note)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/01_RAW/S3_CHAINS.json`
- FIELD/SECTION: stream_object.vtable_note
- ORIGINAL_EXCERPT: `the object is non-polymorphic: all its methods are called directly `
- SUPERSEDED_BY: `OBJECT_POLYMORPHISM = NOT_ESTABLISHED`;
  `KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES` (3 examined callsites measured —
  see S-04).

## S-23 — P3 (prefilled count)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/01_RAW/S3_CHAINS.json`
- FIELD/SECTION: stream_object.ctor_callsites_count
- ORIGINAL_EXCERPT: `"ctor_callsites_count": 10,`
- DEFECT: prefilled literal in the generator (no machine derivation recorded).
- SUPERSEDED_BY: the machine census (C3): 10 raw E8 rel32 target matches,
  all 10 boundary-confirmed (both counts measured; the prefilled value
  coincidentally equals the raw count — it is now measured, not assumed).

## S-24 — F84-C3 (historical QC gate validated the prefill)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/QC_REPORT.md`
- FIELD/SECTION: gate table, Q7 row
- ORIGINAL_EXCERPT: `| Q7 | assigned object identity | PASS | ctor FUN_00972380, extent 0x00972380..0x009724D9, size 0xA4, NO vtable store (non-polymorphic), embedded 0x80-B record cursor |`
- DEFECT: Q7's PASS validated the PREFILLED vtable_store_found=False — that
  is not an independent measurement.
- SUPERSEDED_BY: corrected gate Q13 verifies the C3 machine-search result and
  the scope-bounded global fields (ASSIGNED_OBJECT_VTABLE=UNVERIFIED,
  OBJECT_POLYMORPHISM=NOT_ESTABLISHED) + the superseded-phrase absence sweep.

## S-25 — F84-C2 (historical census arithmetic)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/QC_REPORT.md`
- FIELD/SECTION: gate table, Q3 row
- ORIGINAL_EXCERPT: `classification totals re-summed from the CSV (2 CONFIRMED + 598 + 1,488 + 387 + 129 = 2,604)`
- SUPERSEDED_BY: the fresh corrected census arithmetic (corrected gate Q9
  re-sums CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv; all historical
  classification totals are superseded as canonical conclusions).

## S-26 — P3 (historical denominator in the QC)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/QC_REPORT.md`
- FIELD/SECTION: gate table, Q9 row
- ORIGINAL_EXCERPT: `UNRESOLVED_WRITE_COUNT=64 (boundary-verified non-stack dword-write candidates not resolved to any factory object — derived mechanically from the census CSV)`
- SUPERSEDED_BY: corrected gate Q9: two separately-derived measured
  denominators (S-08) with published definitions.

## S-27 — F84-C3 (handoff wording)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/HANDOFF.md`
- FIELD/SECTION: THE RESULT IN FIVE LINES, item 3
- ORIGINAL_EXCERPT: `NON-POLYMORPHIC record-stream object (no vtable; direct-call methods`
- SUPERSEDED_BY: the corrected object terminology (S-01/S-03/S-04).

## S-28 — F84-C1 (pin-machine-validation wording)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/INPUT_IDENTITIES.md`
- FIELD/SECTION: PE image ground truth section, closing wording
- ORIGINAL_EXCERPT: `every rel32 call target is machine-computed` — with the continuation line
- ORIGINAL_EXCERPT (2): `(`call_va + 5 + rel32`), never hand-quoted. The S1 anchor battery initially caught`
- DEFECT: the wording claims complete pin-machine validation, but the
  machinery computed targets without opcode/boundary proof (S-16) and the
  battery passed records whose expect/measured keys formed no complete check
  pair (S-14/S-15 escaped it; its "31 slips caught" record is real but
  insufficient).
- SUPERSEDED_BY: every corrected pin derives opcode bytes, length, operand
  offset/width, immediate, rel32 and target from ONE authoritative instruction
  VA, with byte[VA]==0xE8, operand-presence and trusted-boundary validation
  required before any target is promoted (C1; validated by corrected gate Q2).

## S-29 — F84-C3 (ledger row wording)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/FUNCTION_LEDGER.csv`
- FIELD/SECTION: row 6 (FUN_00972380), new_semantics_this_run
- ORIGINAL_EXCERPT: `NON-POLYMORPHIC (no vtable store in the extent); embedded 0x14-B cursor-like object`
- DEFECT: the ledger row embeds the prefilled-prose-derived vtable claim (the
  historical ledger file is READ-ONLY; the supersession is recorded here, not
  by editing history).
- SUPERSEDED_BY: the C3 machine-search observation (S-01); the row's OTHER
  content (extent, cursor, tail pairs, 10 call sites incl. the 0x0072FA76
  LEAD) is preserved — the call-site count now machine-measured (S-23).

## S-30 — P3 (transcription byte count)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/FUNCTION_LEDGER.csv`
- FIELD/SECTION: row 14 (FUN_0070BF40), new_semantics_this_run
- ORIGINAL_EXCERPT: `14-byte body kept at transcription level: MOV EAX,[ECX+4]; AND EAX,[ESP+4]; NEG; SBB; NEG; RET 4`
- DEFECT: the measured body is 0x0070BF40..0x0070BF4F = 16 bytes
  (8B 41 04 / 23 44 24 04 / F7 D8 / 1B C0 / F7 D8 / C2 04 00), not 14; the
  transcription content itself is identical.
- SUPERSEDED_BY: the measured literal transcription (C3); the corrected
  wording restricts FUN_0070BF40 to its literal examined operation (loads
  [ECX+4]; ANDs with the supplied argument; normalizes the result to a
  boolean-like return) with NO semantic-role promotion. Function-ledger
  hygiene recorded: HISTORICAL_FUNCTION_BUDGET_COUNT =
  8_DECLARED_AND_MECHANICALLY_REPRODUCED;
  PRE_ANALYSIS_CHRONOLOGY_INDEPENDENTLY_ESTABLISHED = NO;
  ACTUAL_HISTORICAL_BUDGET_OVERRUN = NOT_ESTABLISHED (this correction does
  NOT claim the historical run overran its budget).

---

## S-31 — F84-C2 (SIB display/effective-address decode defect, discovered by the corrected census)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_R1_20261004/FACTORY_PLUS_84_WRITE_CENSUS.csv`
- FIELD/SECTION: the 8D_MOD10_disp32_SIB rows (e.g. row `8D_MOD10_disp32_SIB@0x0063236B`)
- ORIGINAL_EXCERPT: `"LEA ECX,[ESP+ESP*1+0x84]",ESP (boundary-verified)` — and
- ORIGINAL_EXCERPT (2): `"MOV EAX,[ESP+ESP*1+0x84]",ESP (boundary-verified)` (the 0x00812944 read row)
- DEFECT: an IMPOSSIBLE effective address display. In x86 SIB encoding, index
  field 100b means NO INDEX register (ESP cannot be an index); the historical
  scanner's `ireg = REGS[(sib >> 3) & 7]` printed ESP*1 for every index==4
  row. The actual instructions at these rows decode as
  `8D 8C 24 84 00 00 00` LEA ECX,[ESP+0x84] and
  `8B 84 24 84 00 00 00` MOV EAX,[ESP+0x84] (SIB 0x24: base=ESP, NO index).
- SUPERSEDED_BY: the corrected census decodes base/index/scale before any
  classification (the corrected rows carry index_register=NONE for these
  rows); the full-EA discipline of the corrected census is validated by
  corrected gate Q7 (self-consistency: every census row re-decodes
  identically) and synthetic CONTROL F.

---

## PRESERVED (explicitly NOT superseded)

1. The two independently identified stores SURVIVE the corrected re-pin:
   `0x0070D013` (INITIALIZATION_NULL, `89 9E 84 00 00 00` MOV [ESI+0x84],EBX
   in FUN_0070CF80) and `0x0070C71E`
   (CONDITIONAL_OBJECT_OR_NULL_ATTACH_STORE, `89 86 84 00 00 00`
   MOV [ESI+0x84],EAX in FUN_0070C680, guarded by the entry NULL check) —
   both physically re-pinned, boundary-confirmed and classified
   KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITE in the corrected census
   (`CLEAR_RESET_CONFIRMED_COUNT = 0` means no clear/reset store was
   CONFIRMED within the examined census; it does NOT mean clear/reset is
   proven absent).
2. The preserved core science (PRESERVED_CORE in FINAL_REPORT.md):
   FACTORY_PLUS_84_ASSIGNMENT_CORE=CONFIRMED_STATIC_CONDITIONAL,
   ASSIGNMENT_FUNCTION=FUN_0070C680, ASSIGNMENT_VA=0x0070C71E,
   ASSIGNMENT_STORE_BYTES=89 86 84 00 00 00, ASSIGNED_OBJECT_SIZE=0xA4/164 B,
   ASSIGNED_OBJECT_CONSTRUCTOR=FUN_00972380,
   STATIC_FACTORY_MEMBER_IDENTITY=CONFIRMED_WITH_EXAMINED_PATH_CONDITIONS —
   none of these is contradicted by any corrected pin; every one was
   re-measured and revalidated this run.
3. The historical S1/S2/S3/S4 raw JSON files stand as historical physical
   evidence (READ-ONLY); only the defective records named above are
   superseded. The historical FUNCTION_LEDGER.csv stands as a historical
   record (the corrected hygiene fields are recorded in this package).
4. The prior-canon preserved predecessor states (the table[10] writer chain,
   the getter chain, the preserved UNVERIFIED/NOT_ESTABLISHED states) are
   carried unchanged into FINAL_REPORT.md.
