# SUPERSESSION LEDGER — PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005

NEW_SUPERSESSION_RECORD_COUNT = 9

A NEW ledger for THIS correction run (the historical 13-record ledger of
SOURCE_RUN PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004
and the 31-record ledger of the C1 package remain untouched, READ ONLY).
Every ORIGINAL_EXCERPT below is machine-verified a verbatim substring of its
named READ-ONLY historical source (quotecheck gate Q14; the commit-message
source is the verbatim copy under 01_RAW whose fidelity to the immutable git
object at c4cb60f is itself machine-checked by Q14).

## S-P2-01

- SUPERSEDED_CLAIM: the C2 HANDOFF's statement of the Q2 gate's JSON-pin
  coverage was broader than the gate's actual validation: Q2 as committed
  re-derived opcode_bytes / instruction_length / boundary_status /
  boundary_source (+ limited JSON<->CSV fields) and did NOT validate the
  JSON pins' effective_address object (the Desktop post-audit corrupted
  THE_STORE_plus_84 base_register and provenance with all gates still
  passing).
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004/HANDOFF.md`
- ORIGINAL_EXCERPT: `gate Q2 re-derives every C1-JSON pin field from the pinned EXE`
- NEW_STATEMENT: the corrected Q2 re-derives, for every JSON pin where a
  field is semantically applicable, EXACTLY the enumerated set
  Q2_EFFECTIVE_ADDRESS_FIELDS (effective_address present/memop state;
  operand_width; segment; base_register; index_register; scale;
  raw_displacement; signed_displacement; effective_displacement;
  address_provenance_status via EXE decode + boundary/function context) in
  ADDITION to the inherited opcode_bytes / instruction_length /
  boundary_status / boundary_source and JSON<->CSV consistency; JSON fields
  outside that set are NOT claimed as Q2-validated.
- EVIDENCE: M5/M6 causal mutations (01_RAW/CQC_MUTATION_RESULTS.json),
  01_RAW/CQC_FINAL.json gate_details.Q2 (46 EA pins checked, 46 derived).

## S-P2-02

- SUPERSEDED_CLAIM: the C2 FINAL_REPORT's QC-coverage wording implied a
  complete field-by-field comparison of the committed artifacts; the
  effective_address JSON object was not part of the committed Q2 (see
  S-P2-01), so the historical wording overstated the coverage.
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004/FINAL_REPORT.md`
- ORIGINAL_EXCERPT: `committed artifacts from the pinned EXE and compare field-by-field:`
- NEW_STATEMENT: THIS run's FINAL_REPORT states the corrected Q2 coverage
  exactly (the Q2_EFFECTIVE_ADDRESS_FIELDS enumeration); the phrase
  describing the historical Q2 as a complete field-by-field comparison is
  not restated for this run's machinery.
- EVIDENCE: 01_RAW/CQC_FINAL.json gate_details.Q2; AF1_MUTATION_MATRIX.csv
  rows M5/M6.

## S-P2-03

- SUPERSEDED_CLAIM: the C2 commit message described gate Q2 as a complete
  per-field re-derivation of the pin JSON. The historical commit is
  IMMUTABLE - history is not edited; this record supersedes the claim only.
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005/01_RAW/C2_COMMIT_MESSAGE_VERBATIM.txt`
- ORIGINAL_EXCERPT: `gates Q2 (C1 pin JSON re-derived field-by-field from the pinned EXE + JSON<->CSV consistency)`
- NEW_STATEMENT: same as S-P2-01 (the corrected Q2 covers exactly the
  enumerated fields; Q2 fidelity for the commit message is recorded here
  because the message itself cannot change).
- EVIDENCE: Q14 commit_message_verbatim_fidelity=PASS (the verbatim copy
  equals git log -1 --format=%B c4cb60f...); M5/M6 causal results.

## S-P2-04

- SUPERSEDED_CLAIM: the advisory characterization of the P2-1
  boundary-cache defect as having no promotion impact (because CONFIRMED
  landing uses the positions-set) is superseded: the unordered-extents
  early-break can also HIDE a covering stream and let an exactly-landing
  stream confirm, suppressing the honest ANCHOR_CONFLICT veto and
  permitting a FALSE CALL promotion (Desktop NEW-F synthetic fixture:
  `B8 00 E8 01 00 00 00 90 CC`, anchors at +0 and +2, candidate E8 at +2).
- SOURCE_FILE: `C:\Users\User\Documents\ChatGPT\PE\PE_935_F84_C2_DESKTOP_POST_AUDIT_20261004\REPORT.md`
- ORIGINAL_EXCERPT: `Jednak stwierdzenie PE-MASTER „bezpieczne dla promocji”, ponieważ CONFIRMED używa positions-set, jest zbyt szerokie.`
- NEW_STATEMENT: the coverage scan is now order-independent (sorted
  extents; the scan function sorts its input), the synthetic anchor-conflict
  fixture yields UNRESOLVED/ANCHOR_CONFLICT with CALL_VALIDATION != PASS and
  NO target promotion, and the same result was proven invariant across 56
  synthetic insertion permutations and 50 randomized orders of a real 0x004B0980
  production stream (01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json NEW_F record).
- EVIDENCE: NEW_F case + ORDER_PERMUTATION_PROOFS in
  01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json; AF2_BOUNDARY_TEST_MATRIX.csv.

## S-P2-05

- SUPERSEDED_CLAIM: the committed C2 boundary fields for pin
  driver_declassified_0x004B0A02 recorded the position as
  UNRESOLVED/HEURISTIC_START_CANDIDATE with no refuting anchor; with the
  corrected order-independent coverage the pin VA is proven interior to the
  instruction `BB 01 00 00 00` (MOV EBX,1) at 0x004B0A01 on the
  0x004B0980 proven decode path: REFUTED_MID_INSTRUCTION,
  boundary_source=KNOWN_FUNCTION_ENTRY, boundary_start/boundary_refuted_by
  = 0x004B0980. The DECLASSIFIED_NOT_A_CALL ledger status itself is
  UNCHANGED (the declassification as not-a-CALL remains correct; its
  recorded boundary evidence is strengthened).
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004/CORRECTED_PIN_LEDGER.csv`
- ORIGINAL_EXCERPT: `driver_declassified_0x004B0A02,0x004B0A02,01 00,2,none,,,,,NONE,HEURISTIC_START_CANDIDATE,UNRESOLVED,,,DECLASSIFIED_NOT_A_CALL,correction:F84-C1(historical 'driver_call_after_parameters_str' target 0x514B0A07)`
- NEW_STATEMENT: the regenerated 20261005 ledger row carries
  boundary_source=KNOWN_FUNCTION_ENTRY, boundary_status=REFUTED_MID_INSTRUCTION,
  boundary_start=0x004B0980, boundary_refuted_by=0x004B0980 (same-VA
  re-derivation, no special-casing of the VA; the pin failure count remains
  0 because the declassified record class bypasses the VALIDATED family by
  design).
- EVIDENCE: 01_RAW/CHANGED_FIELDS_VS_C2.json; REAL_REFUTE_0x004B0A02 case;
  gate Q2/Q3 re-derivations.

## S-P2-06

- SUPERSEDED_CLAIM: the committed C2 boundary fields for pin
  driver_declassified_0x004B0A21 recorded the position as
  UNRESOLVED/HEURISTIC_START_CANDIDATE with no refuting anchor; with the
  corrected coverage the pin VA is proven interior to the instruction
  `E8 4D 14 F5 FF` (the real CALL) at 0x004B0A1E on the 0x004B0980 proven
  decode path: REFUTED_MID_INSTRUCTION with the same field changes as
  S-P2-05. The DECLASSIFIED_NOT_A_CALL status is UNCHANGED.
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004/CORRECTED_PIN_LEDGER.csv`
- ORIGINAL_EXCERPT: `driver_declassified_0x004B0A21,0x004B0A21,F5,1,none,,,,,NONE,HEURISTIC_START_CANDIDATE,UNRESOLVED,,,DECLASSIFIED_NOT_A_CALL,correction:F84-C1(byte inside the rel32 of the CALL @0x004B0A1E)`
- NEW_STATEMENT: same field set as S-P2-05 (0x004B0980 refutation), same-VA
  re-derivation, no special-casing.
- EVIDENCE: 01_RAW/CHANGED_FIELDS_VS_C2.json; REAL_REFUTE_0x004B0A21 case.

## S-P2-07

- SUPERSEDED_CLAIM: the C2 FINAL_REPORT's decoder-capability wording
  implied the corrected decoder's near-branch and reject coverage was
  complete as stated. Two bounded defect classes were NOT covered: (a)
  `66 0F 8x` near Jcc was decoded as a fixed 7-byte prefixed rel32 form
  (the rel16 truth is 5 bytes; the Desktop NEW-G fixture fabricated a CALL
  edge from an interior data byte), and (b) grouped opcodes 0F BA and
  0F 71/72/73 decoded every ModRM.reg sub-opcode with a trailing imm8
  (reserved/invalid sub-opcodes must REJECT fail-closed, and validity
  depends on opcode + ModRM.reg + ModRM.mod + mandatory prefix).
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004/FINAL_REPORT.md`
- ORIGINAL_EXCERPT: `the decoder decodes SHUFPS imm8 / 16-bit-address / 66 E8 rel16 forms correctly`
- ORIGINAL_EXCERPT: `and rejects fail-closed otherwise (counterexample classes A/B/C/D/E all pass,`
- NEW_STATEMENT: THIS run's decoder adds the P2-2 BRANCH A rule (66-prefixed
  near Jcc 0x80..0x8F = rel16, length 5 with one prefix, operand recorded;
  67-prefixed near Jcc REJECTED, same policy as 67 E8/E9) and the H2
  grouped-opcode validity rule (0F BA reg 4..7 legal any mod, reg 0..3
  rejected; 0F 71/72/73 register-only, MMX reg {2,4,6}, SSE2 66 reg {2,4,6}
  plus 66 0F 73 reg {3,7} = PSRLDQ/PSLLDQ mod=3 only, F2/F3 forms rejected),
  all oracle-verified against GNU objdump Binutils 2.44.
- EVIDENCE: NEW_G case; 01_RAW/CQC_DECODER_UNIT_TESTS.json (64 vectors);
  01_RAW/ORACLE_INDEPENDENT_RECORDS.json (71 fixtures).

## S-P2-08

- SUPERSEDED_CLAIM: the historical decoder's 16-bit addressing table
  documentation stated rm=7 as [BP] (and the implementation mapped
  REG16_ADDR_BASE[7] to "BP"); the correct ISA table is rm=7 mod=0 [BX],
  mod!=0 [BX+disp] (rm=6 mod=0 [disp16], mod!=0 [BP+disp]). The repair
  changes register NAMING only - no instruction length changes, so no
  boundary stream shifted (measured: zero census/pin length differences).
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004/03_SCRIPTS/x86dec.py`
- ORIGINAL_EXCERPT: `4 [SI] 5 [DI] 6 mod0=[disp16] else [BP+disp] 7 mod0=[BP] else [BP+disp]`
- NEW_STATEMENT: the corrected table (this package's 03_SCRIPTS/x86dec.py)
  maps rm=7 to "BX"; the full rm=0..7 table is verified against GNU objdump
  (67 8B 07 = mov eax,[bx]; 67 8B 47 05 = mov eax,[bx+0x5];
  67 8B 46 05 = mov eax,[bp+0x5]).
- EVIDENCE: 01_RAW/ORACLE_INDEPENDENT_RECORDS.json H1 fixtures;
  01_RAW/CQC_DECODER_UNIT_TESTS.json H1 vectors.

## S-P2-09

- SUPERSEDED_CLAIM: none superseded - this record PREVENTS a wording
  defect the correction contract requires: wherever the ArkEstateObject
  lead is repeated, the instruction start is 0x0075136E and the immediate
  (vptr 0x00A87410) is located at 0x00751370; the two VAs must not be
  conflated. The historical C2 package states the lead correctly ("vptr
  immediate 0x00A87410 present at 0x00751370"); this record pins the
  wording for every restatement in THIS package.
- SOURCE_FILE: `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004/FINAL_REPORT.md`
- ORIGINAL_EXCERPT: `the 0x0075138F ArkEstateObject lead physically re-verified but`
- NEW_STATEMENT: this package uses exactly: ARK_ESTATE_INSTRUCTION_START_VA
  = 0x0075136E (the C7 06 vptr store instruction starts there) and
  ARK_ESTATE_IMMEDIATE_LOCATION_VA = 0x00751370 (the immediate bytes live
  there); the lead itself remains NOT_PROMOTED (no strong anchor for the
  containing function; unchanged from C2).
- EVIDENCE: FINAL_REPORT.md preserved-context section; the C2 commit's
  own wording is the historical reference (01_RAW/C2_COMMIT_MESSAGE_VERBATIM.txt).
