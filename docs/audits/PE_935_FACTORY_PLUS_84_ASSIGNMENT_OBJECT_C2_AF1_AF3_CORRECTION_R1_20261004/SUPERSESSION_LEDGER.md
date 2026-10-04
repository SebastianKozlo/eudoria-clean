# SUPERSESSION_LEDGER.md — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004

NEW ledger for THIS C2 correction: it records ONLY claims/artifacts affected or
newly superseded by THIS run. The historical 31-record S-01..S-31 ledger belongs
to the SOURCE_RUN package (`PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/SUPERSESSION_LEDGER.md`) and is NOT modified. Every
record below points to ACTUAL historical evidence in the READ-ONLY SOURCE
package (paths relative to the repo root), with a VERBATIM excerpt; the QC
battery machine-verifies each excerpt as a real substring of its named source
file (quotecheck). Unaffected historical claims are preserved (not silently
reworded): the FACTORY_PLUS_84 assignment core, the two known stores, the
corrected F84-C1 pins, the 0xA4/164 facts, the AF3 manager-ctor rejection and
all preserved predecessor states carry forward unchanged.

SOURCE package root below = `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/`.

---

## S-C2-01 — AF2 (boundary policy: padding starts promoted to trusted)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: F84-C1, DIRECT CALL VALIDATION paragraph
- ORIGINAL_EXCERPT: `(known function entry / CC-padding-delimited start / RET-delimited start,`
- DEFECT: the C1 machinery declared raw CC-padding and RET-delimited patterns
  as trusted boundary sources able to CONFIRM boundaries and promote CALL
  targets. A raw delimiter/padding pattern is only a HEURISTIC_START_CANDIDATE
  (the Desktop post-audit AF2 counterexamples A1/A2/B show a padding-derived
  start at the candidate VA confirming trivially and promoting an E8 that is
  immediate data of another instruction).
- SUPERSEDED_BY: the C2 pebnd.py boundary machinery — strong anchors only
  (KNOWN_FUNCTION_ENTRY with recorded anchor provenance); heuristic starts
  (the C1 T2/T3 classes) are ENUMERATED and RECORDED but can NEVER confirm a
  boundary, NEVER beat a conflicting proven decode, and NEVER promote a CALL
  target.

## S-C2-02 — AF2 (the exact-landing safeguard claim)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/HANDOFF.md`
- FIELD/SECTION: FOR PE-MASTER, Known QC limitations
- ORIGINAL_EXCERPT: `DECLARED heuristics with exact-landing sequential-decode safeguards (a`
- DEFECT: the claimed safeguard does not hold: a hostile start EQUAL to the
  candidate VA lands trivially (`seq_decode_lands(start==target)` returns
  True with zero decodes), and a nearer false start beats the correct known
  entry under the C1 nearest-first policy — the historical safeguard claim is
  refuted by the Desktop counterexamples and superseded.
- SUPERSEDED_BY: the C2 machinery — heuristic starts never confirm at all
  (the exact-landing question for heuristic starts is moot), and a proven
  entry decode that covers a candidate mid-instruction REFUTES it (precedence
  rule: the proven decode always wins over a padding-derived heuristic start).

## S-C2-03 — AF2 (census boundary-confirmed count)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: F84-C2 measured quantities table
- ORIGINAL_EXCERPT: `| BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS | **1,685** |`
- DEFECT: 1,675 of those 1,685 confirmations came from padding-derived
  heuristic starts (census boundary_source census: CC_PADDING_DELIMITED_START
  1567 + RET_DELIMITED_START 108 vs KNOWN_FUNCTION_ENTRY 10) — under the
  corrected strong-anchor policy they are NOT boundary-confirmed.
- SUPERSEDED_BY: BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS = 10 (this run,
  strong anchors only; 01_RAW/C2_CENSUS.json + the census CSV, re-summed by
  gate Q9 and per-row re-derived by gate Q6).

## S-C2-04 — AF2 (census read-rejection count)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: F84-C2 measured quantities table
- ORIGINAL_EXCERPT: `| REJECTED_READ_NOT_WRITE (boundary-confirmed read/CMP/LEA forms) | **1,003** |`
- DEFECT: same padding-confirmation dependency as S-C2-03: only
  strong-anchor-confirmed reads may be rejected as read-not-write.
- SUPERSEDED_BY: REJECTED_READ_NOT_WRITE = 6 (this run: the 5 KNOWN_READS
  0x0070DD1A/0x0070DD6A/0x0070DD7E/0x0070C6BE/0x0070BFD0 + the
  LEA-unlinked row 0x0072FBC3, all KNOWN_FUNCTION_ENTRY-confirmed).

## S-C2-05 — AF3 (wrong-object provenance discipline)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: F84-C2 measured quantities table
- ORIGINAL_EXCERPT: `| REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE | **5** (4 layout-evidence controls with window bytes re-verified this run + the manager-ctor wrapper with machine-checked manager-this provenance) |`
- DEFECT: the four layout-evidence controls (0x0074955A, 0x006D4F88,
  0x0075138F, 0x007196AA) were classified REJECTED_WRONG_OBJECT_WITH_PROVEN_
  PROVENANCE although their address_provenance_status remained UNRESOLVED and
  their evidence is a layout/value/init GRAMMAR hypothesis, not a concrete
  identity chain from the effective-address base to a specific independently
  established object (Desktop post-audit AF3); their C1 boundary
  confirmations were also padding-derived (S-C2-01).
- SUPERSEDED_BY: REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE = 1 (the
  manager-ctor row 0x00707EC0 only, with the full per-row identity chain
  persisted in AF3_PROVENANCE_LEDGER.csv); the four layout controls are
  DOWNGRADED to UNRESOLVED with their window evidence recorded as HYPOTHESIS
  (contract AF3 option B; no forced option A); the 0x0075138F ArkEstateObject
  lead (vptr 0x00A87410 / MSVC TypeDescriptor .?AVArkEstateObject@@) is
  physically re-verified this run (window immediate at 0x00751370; RTTI chain
  byte-read: [vptr-4]=0x00AA9AD4 COL, [COL+0x0C]=0x00B8E9D4 TD, name matches)
  but NOT promoted — the containing function has no strong anchor, so the
  candidate base cannot be physically bridged to that object identity within
  this correction's discipline.

## S-C2-06 — AF2 (census unresolved denominator)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: F84-C2 measured quantities table
- ORIGINAL_EXCERPT: `| CENSUS_UNRESOLVED_ROWS (all unresolved rows: boundary-unresolved read/LEA rows + all unresolved write candidates) | **1,217** |`
- DEFECT: the count depended on the invalid padding confirmations.
- SUPERSEDED_BY: CENSUS_UNRESOLVED_ROWS = 2,218 (this run; the demoted rows
  move from resolved to honest UNRESOLVED — an honest-bounds increase, not a
  regression).

## S-C2-07 — AF2 (write-candidate denominator)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: F84-C2 measured quantities table
- ORIGINAL_EXCERPT: `| FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES (write-form positive rows not resolved to a confirmed factory write or a proven wrong-object rejection) | **828** |`
- DEFECT: same padding-confirmation dependency (plus the four AF3 downgrades
  below move from wrong-object-rejected to unresolved write candidates).
- SUPERSEDED_BY: FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES = 832 (this run).

## S-C2-08 — P3-B (declared-family metadata inconsistency)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/01_RAW/C2_CENSUS.json`
- FIELD/SECTION: closure.scan_coverage
- ORIGINAL_EXCERPT: `"declared_families": 10,`
- DEFECT: the C1 metadata declared 10 families while the explicit family list
  (and the actual scanner) has 9 — the metadata/report/implementation did not
  agree (Desktop post-audit P3-B).
- SUPERSEDED_BY: DECLARED_ENCODING_FAMILY_COUNT = 9, DERIVED from the actual
  scanner family table (len(FAMILIES) in c2_census.py); metadata, JSON,
  CSV-family column and report agree (gate Q13 verifies JSON == scan_coverage
  == implementation == explicit list count); the disclosed-but-out-of-scope
  families are documented separately.

## S-C2-09 — AF2 (pin ledger padding-derived confirmations and promoted targets)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/CORRECTED_PIN_LEDGER.csv`
- FIELD/SECTION: modeinit_caller_CALL row (and the lazyinit_CALL_ctor row; the
  same defect class affects 7 rows total: modeinit_caller_PUSH_2,
  modeinit_caller_MOV_ECX, modeinit_caller_CALL, lazyinit_CMP_singleton_null,
  lazyinit_PUSH_0x118_factory_size, lazyinit_CALL_ctor, lazyinit_store_singleton)
- ORIGINAL_EXCERPT: `modeinit_caller_CALL,0x00417524,E8 97 0B 2F 00,5,rel32,1,4,97 0B 2F 00,,0x007080C0,CC_PADDING_DELIMITED_START,CONFIRMED,VALIDATED,chain:modeinit(caller)`
- ORIGINAL_EXCERPT (2): `lazyinit_CALL_ctor,0x0073E2EB,E8 30 D5 FF FF,5,rel32,1,4,30 D5 FF FF,,0x0073B820,CC_PADDING_DELIMITED_START,CONFIRMED,VALIDATED,chain:lazy_init`
- DEFECT: these 7 pin rows were boundary-CONFIRMED (and the 2 call targets
  PROMOTED) from CC-padding-derived heuristic starts — invalid under the
  corrected policy (the byte/operand evidence itself is unchanged and still
  re-verifies).
- SUPERSEDED_BY: the C2 CORRECTED_PIN_LEDGER.csv — the 5 byte/imm/mem rows
  become VALIDATED_BYTES_BOUNDARY_UNRESOLVED; the 2 call rows become
  NOT_VERIFIED with the target NOT_PROMOTED (apparent targets recorded,
  e.g. modeinit_caller_CALL apparent=0x007080C0); pin total failures stay 0
  (these are honest downgrades of boundary CONFIRMATION, not pin defects).

## S-C2-10 — AF2 (ctor call-site census confirmation count)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/HANDOFF.md`
- FIELD/SECTION: P3 corrections list, item 4 continuation
- ORIGINAL_EXCERPT: `machine-measured (10 raw, 10 boundary-confirmed).`
- DEFECT: the boundary-confirmed subset depended on the invalid padding
  confirmations.
- SUPERSEDED_BY: the C2 C3 re-measurement — 10 raw E8 rel32 target matches
  (unchanged), boundary_confirmed_count = 2 (strong anchors only:
  0x0070C715 in FUN_0070C680 and 0x0072FA76 in FUN_0072FA30); 01_RAW/
  C3_OBJECT_SCOPE.json ctor_callsite_census.

## S-C2-11 — P3-A (ctor store-census scope omission)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: F84-C3 corrected bounded machine search paragraph
- ORIGINAL_EXCERPT: `with effective displacement 0 recorded — exactly one found, the embedded`
- ORIGINAL_EXCERPT (2): `cursor's buffer store `89 07` MOV [EDI],EAX @0x00972452 with base EDI (this`
- DEFECT: the C1 report claimed "every memory-write instruction with effective
  displacement 0" but enumerated only selected MOV forms with disp_width==0,
  silently omitting the two FS:[0] SEH/TLS stores physically present in the
  examined ctor extent (0x009723A0 `64 A3 00 00 00 00` MOV FS:[0],EAX and
  0x009724CB `64 89 0D 00 00 00 00` MOV FS:[0],ECX) — the scope wording
  overclaimed the enumeration (Desktop post-audit P3-A).
- SUPERSEDED_BY: the C2 C3 store census with SEGMENT SEMANTICS EXPLICITLY
  REPRESENTED: 3 memory-write encodings with effective displacement 0 in the
  extent (the [EDI] buffer store `89 07` @0x00972452 + the two FS:[0] SEH
  stores with segment=FS persisted per store); the segment-relative stores are
  explicitly EXCLUDED from DIRECT_VPTR_STORE_IN_EXAMINED_CTOR and from any
  object-member offset-zero evidence; the census scope wording now names every
  covered write form (explicit stores incl. 66-word variants + MOFFS + RMW
  forms) and machine-checks/discloses the implicit-destination forms.

## S-C2-12 — P3-C (INPUT_IDENTITIES repository-owner typo)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/INPUT_IDENTITIES.md`
- FIELD/SECTION: Repository / baseline table
- ORIGINAL_EXCERPT: `(remote `SebastianKlo/eudoria-clean`, branch master)`
- DEFECT: the repository-owner spelling in the historical INPUT_IDENTITIES is
  a typo; the actual canonical remote identity is SebastianKozlo/eudoria-clean
  (verified this run: `git remote get-url origin` =
  https://github.com/SebastianKozlo/eudoria-clean.git).
- SUPERSEDED_BY: the corrected wording `SebastianKozlo/eudoria-clean` in THIS
  package's INPUT_IDENTITIES.md; the historical file itself is READ-ONLY and
  NOT modified; no unrelated editorial cleanup was performed (the exact
  old->new wording is this record).

## S-C2-13 — AF1 (QC artifact-validation scope)

- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/FINAL_REPORT.md`
- FIELD/SECTION: F84-C1 negative-controls paragraph
- ORIGINAL_EXCERPT: `Negative controls A–F (synthetic bytes only, no new PCG function tracing):`
- DEFECT: the C1 negative controls were synthetic-byte fixtures of the QC's
  own constants — the production gates never validated the ACTUAL committed
  artifacts' load-bearing fields, so corruption of the real C1 JSON
  opcode_bytes, the CSV measured_operand, the C3 store collection or the
  census boundary anchors passed undetected (Desktop post-audit AF1, four
  reproduced private mutants).
- SUPERSEDED_BY: the C2 production QC — gates Q2/Q3/Q6/Q7/Q8 re-derive the
  ACTUAL artifacts' load-bearing fields from the pinned EXE and compare
  field-by-field; the causal mutation harness M1–M4 + AF3/Q8 mutates a
  TEMPORARY COPY of the ACTUAL final artifact through the SAME production
  gate (5/5 UNMUTATED=PASS -> MUTATED=FAIL, 01_RAW/
  CQC_MUTATION_RESULTS.json + AF1_MUTATION_MATRIX.csv).

---

Ledger counts (measured by the Q14 gate quotecheck):
NEW_SUPERSECTION_NOTE: the record count below is the number of S-C2-NN
records; two records (S-C2-09, S-C2-11) carry two ORIGINAL_EXCERPT lines
each, so the machine quotecheck verifies 15 excerpt lines across 13 records.
NEW_SUPERSESSION_RECORD_COUNT = 13
