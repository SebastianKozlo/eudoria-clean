# FINAL REPORT — PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005

One bounded correction-only run for the TWO P2 defects (D1/D2) found by the
independent Desktop post-audit of the published THREE-P2 package
(PE_935_F84_C2_C1_DESKTOP_POST_AUDIT_20261005, verdict REQUIRE_CORRECTIONS).
This run exists SOLELY to repair the reusable forensic/QC machinery and to
regenerate its dependent artifacts with honest records. NO new placement
science, NO 0xA4 source/init experiment, NO general decoder hardening, NO
placement/XYZ, NO mask/OpenMW/Gamebryo comparison, NO templates.vfs, NO
RECORD_A, NO Model 194013, NO client execution, NO atlas, NO new backing
source. The tested original THREE-P2 repairs (P2-1, P2-2, P2-3, H1) are
PRESERVED and reproduced as controls, not reopened.

Correction statuses (this run, measured):

- D1_H2_0F73_4_STATUS = CORRECTED_PER_OPCODE_LEGAL_REG_TABLES
- D1_INVALID_FIXTURES = 2/2_REJECTED (0F 73 E0 02; 66 0F 73 E0 02)
- D1_DOWNSTREAM_CALL_STATUS = CORRECTED_NO_PASS_NO_PROMOTION_NOT_VERIFIED
- D2_PINSET_STATUS = CORRECTED_ROSTER_BOUND_BIDIRECTIONAL_MULTISET
- D2_ROLE_APPLICABILITY_STATUS = CORRECTED_EXPECTED_ROLE_DRIVEN_EA
- H2_GROUP_OPCODES = CORRECTED_PER_OPCODE_VALIDITY_TABLES
- P2_1_BOUNDARY_CACHE = PRESERVED_CORRECTED_SORTED_EXTENTS (REPRODUCED_THIS_RUN)
- P2_2_66_0F8X_NEAR_JCC = PRESERVED_CORRECTED_BRANCH_A_REL16 (REPRODUCED_THIS_RUN)
- P2_3_Q2_EFFECTIVE_ADDRESS = PRESERVED_CORRECTED_RE_DERIVED_FROM_EXE (D2_EXTENDS)
- H1_REG16_RM7 = PRESERVED_CORRECTED_BX_TABLE (REPRODUCED_THIS_RUN)

Phase semantics of THIS executor run (persistence is the separate PE-MASTER
phase under the dispatch):

- PE_MASTER_REVIEW_PERFORMED_BY_THIS_RUN = NO (PE_MASTER_REVIEW.md is an
  explicit placeholder; the review verdict is persisted by the PE-MASTER
  phase)
- AUDIT_ENTRYPOINT_MODIFIED = NO (a proposed newest-first row is provided in
  HANDOFF.md; the persistence phase adds it and regenerates the manifest)
- COMMIT_OR_PUSH_PERFORMED = NO
- MANIFEST_PREPARED_FOR_PERSISTENCE_PHASE = YES (generated LAST, bijection
  verified; covers AUDIT_ENTRYPOINT.md at its CURRENT BASE state - the
  persistence phase MUST regenerate/re-verify it after adding the run row)
- NEXT_EXPERIMENT_AUTHORIZED = NO
- CANONICAL_GATE_EFFECT = NONE

## D1 — the reserved `0F 73 /4` sub-encoding (x86dec.py)

DEFECT (Desktop D1/P2, reproduced in-run from the committed BASE modules):
the BASE `_group_imm8_ok` shared one legal-reg whitelist across opcodes
0F 71/72/73 in both the MMX and the SSE2 branch, so the non-existent
`0F 73 /4` form was decoded as a 4-byte instruction without 66 and a 5-byte
instruction with 66. Per the ISA there is no PSRADQ: MMX 0F 73 is PSRLQ /2
and PSLLQ /6 only, and the 66 SSE2 0F 73 forms are PSRLQ /2, PSRLDQ /3,
PSLLQ /6, PSLLDQ /7. The independent oracle (GNU objdump, GNU Binutils for
Debian 2.44) returns (bad) for both negative forms.

REPAIR (per-opcode legal-reg tables, exactly the contract tables):

| Opcode | Without 66, legal reg | With mandatory 66, legal reg |
|---|---|---|
| 0F 71 | 2,4,6 | 2,4,6 |
| 0F 72 | 2,4,6 | 2,4,6 |
| 0F 73 | 2,6 | 2,3,6,7 |

Other sub-encodings of this family stay rejected: register-only (mod=3)
requirement, memory forms, F2/F3 forms. /4 remains LEGAL for 0F 71/72
(PSRAW/PSRAD); 66 0F 73 /3,/7 remain legal (PSRLDQ/PSLLDQ). 0F BA behaviour
is unchanged. All earlier fixes (P2-2 rel16 Jcc, H1 rm table, AF2 classes)
are preserved verbatim.

ORACLE-FIRST: the D1 expected verdicts were locked from the contract + the
ISA reference BEFORE the corrected decoder was evaluated; objdump was run
first and persisted (80 fixtures: the 71 carried fixtures recaptured + 9
D1 fixtures). Measured oracle verdicts: `0F 73 E0 02` -> (bad);
`66 0F 73 E0 02` -> data16 (bad); the six contract legal controls decode at
their true lengths (`0F 71 E0 02` psraw, `0F 72 E0 02` psrad,
`0F 73 D0 02` psrlq, `0F 73 F0 02` psllq, `66 0F 73 D8 02` psrldq,
`66 0F 73 F8 02` pslldq). Production results: the two negatives REJECT
(2/2), the six legal controls decode (6/6), all carried H2 controls still
pass (0F BA positives/negatives, imm-shift register forms, reserved /1,/3,
/no-66-/7, memory forms, F2/F3) - 72 unit-battery entries, 0 failures.
The unit battery also includes two byte-identical duplicates of the carried
0F 73 /2 and /6 patterns carrying D1-specific notes (disclosed; the distinct
new byte patterns are 6).

MANDATORY DOWNSTREAM FALSIFIER (synthetic bytes
`0F 73 E0 02 E8 05 00 00 00 C3`, synthetic strong entry at the first byte;
no VA/fixture special-casing):
- CORRECTED machinery (measured): the sequential decode ABORTS at the
  invalid first instruction -> BOUNDARY_STATUS=UNRESOLVED (no strong evidence
  either way; no heuristic start in the buffer), CALL_VALIDATION=NOT_VERIFIED,
  TARGET NOT promoted. D1_INTERNAL_E8_PROMOTED = NO.
- BASE (THREE-P2) reproduction (measured in-run through a READ-ONLY import
  of the committed BASE modules; file identities recorded): the invalid form
  decoded as 4 bytes, the stream advanced onto the E8 at +4 ->
  BOUNDARY_STATUS=CONFIRMED, CALL_VALIDATION=PASS, TARGET=0x00A0000E - the
  unearned certification the Desktop audit found. Objdump recovery
  disassembly after (bad) is NOT treated as execution evidence.
- Scope honesty: SYNTHETIC bytes are not evidence this pattern occurs in
  PCG. The falsifier's .text census MEASURED zero occurrences of the
  `0F 73` mod=3 reg=4 pattern (with and without 66) in the pinned EXE, and
  the regenerated census/pins are identical to BASE (below) - so this
  correction changed no real stream, while closing the unsafe certification
  path.

## D2 — gate Q2 pin universe, roles and EA applicability (cqc_battery.py)

DEFECT (Desktop D2/P2, reproduced by the audit and closed by 8 causal
controls): the BASE gate_q2 iterated ONLY the JSON's supplied pins, decided
EA applicability solely from the mutable JSON kind field, and trusted the
declared fail_count - so a relabelled kind, a removed EA object, a DELETED
load-bearing pin, a DUPLICATED claim or an EXTRA claim all still passed.

CORRECTION (the expected roster is the BASE-pinned
`03_SCRIPTS/c1_pin_ledger.py::PINS`, Git blob 5a7b642f..., extracted by AST
literal evaluation - no historical code executed - and re-derived IN-RUN by
the gate from the same Git blob, never taken from the checked artifacts and
never edited to make a record pass; persisted as EXPECTED_PIN_REGISTRY.json,
which the gate must EQUAL):

- JSON claim multiset == CSV claim multiset == expected roster multiset;
  each expected claim occurs EXACTLY ONCE (missing/extra/duplicate = FAIL;
  bidirectional, not count-only).
- claim_id + instruction_va + declared kind(role) agree with the roster per
  claim (role mapping explicit against PINS; the CSV operand_kind is NOT an
  independent role oracle - Q3 now verifies every CSV row's operand_kind
  against the EXE-derived kind, with the generator's imm-over-mem
  convention, and checks row membership/VA against the roster).
- declared totals agree with measurement: total_pins == roster cardinality
  == measured JSON count == measured CSV count; status_tally == the
  CSV-recomputed tally; fail_count == 0 (carried).
- EA applicability derives from the EXPECTED role: a mutated JSON kind
  FAILS the role check AND cannot disable EA validation. The carried
  effective_address EXE re-derivation is preserved with EXACTLY this
  coverage:
  Q2_EFFECTIVE_ADDRESS_FIELDS = effective_address present/memop state; operand_width; segment; base_register; index_register; scale; raw_displacement; signed_displacement; effective_displacement; address_provenance_status
  plus a NEW spec cross-check: the EXE-derived EA must also agree with the
  roster's pinned expect_ea (base/index/scale/displacement) - either side
  disagreeing is a FAIL, never silently resolved.
- A memory store with an immediate still serializes the immediate in the
  CSV while the JSON is required to carry the EA object (the roster says
  mem); a code-entry pin whose first instruction accesses memory does NOT
  become a memory-role pin (the role comes from the roster, not from the
  instruction shape).
- Cardinality is a coverage contract, not a padding target: if generation
  omits a pin, the gate FAILS on actual coverage; no results are padded to
  historical counts.

Clean-package measurement: expected 133; JSON 133; CSV 133; declared
total 133; status_tally matches the CSV-recomputed tally (VALIDATED 120,
CORRECTED_VALIDATED 4, DECLASSIFIED_NOT_A_CALL 2,
VALIDATED_BYTES_BOUNDARY_UNRESOLVED 5, NOT_VERIFIED 2); 46 mem-role pins,
46 EA objects checked, 46 re-derived from the EXE, 0 mismatches.

## Mandatory D2 causal controls (actual-artifact mutations; all 8/8
CAUSAL_PASS; each an ISOLATED TEMP COPY of the ACTUAL newly generated C1
JSON/CSV outside the repo, same pinned EXE, same production loader, same
production gate_q2, no substitute failure from a manifest/Git
baseline/another gate; per-case input-hash census proves the unrelated
inputs byte-identical):

| ID | Mutation (class) | Q2 |
|---|---|---|
| D2-M1 | THE_STORE_plus_84: kind mem->code_entry + EA object removed (COMPOUND two-field) | PASS -> FAIL (2 predicates: role mismatch + required-EA missing) |
| D2-M2 | the ENTIRE THE_STORE_plus_84 JSON pin deleted; CSV and declared totals unchanged | PASS -> FAIL (missing claim) |
| D2-M3 | stream_ctor_buffer_store: kind mem->code_entry + EA object removed (COMPOUND two-field) | PASS -> FAIL (2 predicates) |
| D2-M4 | the ENTIRE stream_ctor_buffer_store JSON pin deleted | PASS -> FAIL (missing claim) |
| D2-M5 | an EXACT duplicate of THE_STORE_plus_84 appended (duplicate-claim protection) | PASS -> FAIL (multiplicity) |
| D2-M6 | a foreign claim FAKE_EXTRA_PIN_0xDEADBEEF appended (extra-claim protection, JSON) | PASS -> FAIL (extra claim) |
| D2-M7 | a foreign CSV row FAKE_EXTRA_CSV_ROW_0xDEADBEEF appended (extra-claim protection, CSV) | PASS -> FAIL (extra claim + tally) |
| D2-M8 | synchronized JSON+CSV omission of THE_STORE_plus_84 with INTERNALLY CONSISTENT adjusted declared totals (132/132) | PASS -> FAIL (3 predicates: JSON missing, CSV missing, totals vs roster) |

Retained controls (re-run through the corrected gates):
OLD_MUTATION_TOTAL = 7 (M1, M2, M3, M4, AF3/Q8 COMPOUND, M5, M6) -
7/7 CAUSAL_PASS (each UNMUTATED=PASS -> MUTATED=FAIL through the SAME
production gate function object). D2_NEW_MUTATION_TOTAL = 8.
MUTATION_TOTAL = 15 (15/15 causal).

## Reproduced carried falsifiers and controls (unchanged behaviour)

- NEW-F (P2-1): `B8 00 E8 01 00 00 00 90 CC`, anchors A=+0, B=+2,
  candidate E8=+2: BOUNDARY_STATUS=UNRESOLVED, BOUNDARY_SOURCE=
  ANCHOR_CONFLICT, CALL_VALIDATION=NOT_VERIFIED, TARGET not promoted - the
  SAME result on the CACHED path and the UNCACHED counterpart
  (UNCACHED_CROSSCHECK matches), invariant across the synthetic insertion
  permutations and the randomized real 0x004B0980 stream orders.
  NEW_F_INTERNAL_E8_PROMOTED = NO.
- NEW-G (P2-2): `66 0F 84 00 00 B8 00 E8 01 00 00 00 C3`: first instruction
  measured 5 bytes (oracle: je rel16); the E8 at +7 is interior to the MOV
  immediate -> REFUTED_MID_INSTRUCTION, FAIL_MID_INSTRUCTION, no promotion.
  NEW_G_INTERNAL_E8_PROMOTED = NO.
- H1: the full 16-bit-addressing rm table (24 oracle fixtures) recaptured;
  `67 8B 07` = mov eax,[bx]; lengths unchanged; zero census/pin length
  changes (regression: 0 field changes).
- Previous AF2 controls A1/A2/B/C/D/E: all reproduced (A1/A2/B/C/D refute
  the interior E8; E positive control promotes the aligned E8 rel32).
- REAL-REFUTE: the two real driver pins 0x004B0A02 (interior to
  `BB 01 00 00 00` @0x004B0A01) and 0x004B0A21 (interior to
  `E8 4D 14 F5 FF` @0x004B0A1E) re-derive REFUTED_MID_INSTRUCTION,
  boundary_refuted_by=0x004B0980, through the generic machinery (no VA
  special-casing); their DECLASSIFIED_NOT_A_CALL ledger statuses are
  unchanged.
- The three real-EXE positive CALL controls still PASS with exact targets:
  0x0070C715->0x00972380, 0x0070DD75->0x00971AD0, 0x0070C742->0x00972DF0.

## Regenerated artifacts and the regression vs the exact BASE package

All dependent artifacts were REGENERATED from the corrected instruments
(never hand-patched; every generation command and result in
GENERATION_RECORD.md). REGRESSION_DIFF.json measures the complete change
surface vs the committed THREE-P2 package:

- BYTE-IDENTICAL to BASE (fresh regeneration measured, not copied):
  CORRECTED_PIN_LEDGER.csv (133 rows, 0 field changes),
  CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv (2612 rows, 0 field changes),
  AF3_PROVENANCE_LEDGER.csv (5 rows, 0 field changes).
- IDENTICAL AFTER EXCLUDING DECLARED METADATA (the top-level `run` label):
  01_RAW/C1_PIN_EVIDENCE.json (0 pin-field changes, 0 nested-EA changes),
  01_RAW/C2_CENSUS.json (all 13 measured quantities identical:
  RAW_PATTERN_ROWS=2612, POSITIVE_PLUS_84_ENCODING_ROWS=2227,
  NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS=385,
  BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS=10,
  KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES=2, CENSUS_UNRESOLVED_ROWS=2218,
  FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES=832,
  REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE=1, REJECTED_READ_NOT_WRITE=6,
  REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE=0,
  ADDRESS_PROVENANCE_UNRESOLVED=832, DECODER_REJECT_ROWS=0),
  01_RAW/C3_OBJECT_SCOPE.json (identical values).
- EXPECTED content changes (all new or extended D1/D2 artifacts, each
  declared): the unit battery 64 -> 72 entries (+ the D1 vectors); the
  boundary matrix 13 -> 14 cases (+ D1_0F73_4_DOWNSTREAM_FALSIFIER; the only
  changed carried case is NEW-G's oracle-record filename reference);
  01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json (71 -> 80 fixtures, renamed
  from ORACLE_INDEPENDENT_RECORDS.json; the carried fixtures' role texts
  carry REPRODUCED_THIS_RUN annotations); NEW 01_RAW/D2_MUTATION_RESULTS.json
  (8 records), NEW 01_RAW/D1_BOUNDARY_FALSIFIER.json, NEW
  EXPECTED_PIN_REGISTRY.json, NEW 01_RAW/BASE_COMMIT_MESSAGE_VERBATIM.txt.
- Old totals were NOT forced: every quantity was re-measured and came out
  identical (the D1 repair could not change any real stream - zero
  occurrences of the affected pattern in .text).

## Preserved scientific core (re-measured, unchanged)

FACTORY_PLUS_84_ASSIGNMENT_CORE = PRESERVED_CONFIRMED_STATIC_CONDITIONAL
ASSIGNMENT_FUNCTION = FUN_0070C680
ASSIGNMENT_VA = 0x0070C71E
ASSIGNMENT_STORE_BYTES = 89 86 84 00 00 00
ASSIGNED_OBJECT_SIZE = 0xA4/164 B
ASSIGNED_OBJECT_CONSTRUCTOR = FUN_00972380
ASSIGNED_OBJECT_VTABLE = UNVERIFIED
OBJECT_POLYMORPHISM = NOT_ESTABLISHED
STATIC_FACTORY_MEMBER_IDENTITY = CONFIRMED_WITH_EXAMINED_PATH_CONDITIONS
KNOWN_EXAMINED_CALLSITES_ARE_DIRECT = YES
DIRECT_VPTR_STORE_IN_EXAMINED_CTOR = NOT_OBSERVED
EXAMINED_ENCODING_CANDIDATE_CLOSURE = CLOSED
EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE = NOT_ESTABLISHED
ASSIGNED_VALUE_AT_SPECIFIC_CONSUMER_EVENT = UNVERIFIED
WRITE_TO_CONSUMER_VALUE_PRESERVATION = NOT_ESTABLISHED
FACTORY_PLUS_84_LIFETIME_SINGLE_ASSIGNMENT = NOT_ESTABLISHED
ULTIMATE_VALUE_SOURCE = UNKNOWN
WORLD_INSTANCE_SEMANTIC = NOT_ESTABLISHED
PHYSICAL_RECORD_TO_WORLD_INSTANCE = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
WRITER_FUNCTION = FUN_009777F0
WRITER_VA = 0x00977810
TAG6_TO_ID10 = PRESERVED_CONFIRMED
SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED
TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD
CLEAR_RESET_CONFIRMED_COUNT = 0

The 0xA4 object receives NO class name and is NOT called a stream; the
structural-identity and naming discipline of the chain is carried unchanged
(historical identifiers containing "stream" do not establish the object's
semantic role). The 0x0075138F ArkEstateObject lead stays NOT_PROMOTED;
wherever this package repeats that lead, the wording is exactly
ARK_ESTATE_INSTRUCTION_START_VA = 0x0075136E and
ARK_ESTATE_IMMEDIATE_LOCATION_VA = 0x00751370 (ledger record S-P2-09 of the
BASE chain remains the pinned reference). The four AF3-downgraded layout
controls remain UNRESOLVED (no new identity edge was attempted).

Scope/nonclaim invariants (all carried, all measured true this run):
NEW_BACKING_SOURCE_RE_EXECUTED = NO; TEMPLATES_VFS_OPENED = NO;
RECORD_A_ANALYZED = NO; MODEL_194013_TRACE_EXECUTED = NO;
PLACEMENT_XYZ_RE_EXECUTED = NO; CLIENT_EXECUTED = NO;
CANONICAL_GATE_EFFECT = NONE. The 34 strong anchors are
PRIOR_CANON_ANCHOR_INPUT (not independently re-proven this run; entry bytes
re-verified at the pinned VAs only).

## Retractions and supersessions

The BASE claims retracted by this run (with exact source quotes and
replacement statements) are recorded in SUPERSESSION_LEDGER.md (9 records:
S-D1-01..03, S-D2-01..04, S-CM-01, S-AUD-01; quotecheck machine-verifies
every ORIGINAL_EXCERPT against its READ-ONLY source). Retracted claim
classes: the H2 family-closure wording, the Q2 JSON-closure wording, the
whole-scope completeness wording, and the implication of an unqualified
green light for dependent reuse. After this correction, within the measured
scope, OPEN_P0_P1_P2_IN_CORRECTION_SCOPE =
NONE_AFTER_D1_D2_IN_TESTED_SCOPE (P0/P1: none identified by the audit or
this run; the 2218 unresolved census rows are honest UNRESOLVED states, not
machinery defects). Historical files and commits are not edited.

## Targeted QC (SELF_CHECK; honest labeling)

QC_SCOPE = SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION (executor
self-QC; author/origin: pe-reconstruction worker session under the PE-MASTER
direct dispatch of 2026-10-05). This is NOT an independent audit; the
independent Desktop post-audit of the eventually published commit remains a
separate human-relayed step; the PE-MASTER internal review is the
persistence-phase gate (advisory/pre-qualification;
PE_MASTER_REVIEW_PERFORMED_BY_THIS_RUN = NO).

- Gates Q1-Q13: 13/13 PASS (data mode; Q1 pre-publication BASE check:
  LOCAL_HEAD == ORIGIN/master == ACTUAL_REMOTE_MASTER == 9d31a82... at the
  pre-commit state; after the persistence-phase commit the HEAD moves BY
  DESIGN - publication verification is separate).
- Mutations: 15/15 CAUSAL_PASS (7 retained + 8 D2).
- Q14 (docs mode, final full run): required-string battery over this
  FINAL_REPORT, forbidden/overclaim sweep (0 hits on the active claim
  surfaces), supersession quotecheck (all ORIGINAL_EXCERPTs verbatim in
  their named READ-ONLY sources; declared record count == measured),
  commit-message verbatim fidelity (the 01_RAW copy equals
  `git log -1 --format=%B 9d31a82...`), required-files battery, P3-C
  identity hygiene, forbidden-input census over the instruments.
- Unit battery: 72 entries, 0 failures (count measured from the generated
  artifact, never hard-coded). Boundary matrix: 14 cases. Oracle fixtures:
  80.
- Process honesty: three pre-first-full-pass construction fixes are
  disclosed in GENERATION_RECORD.md/QC_REPORT.md; the ONE authorized
  targeted QC repair round WAS USED: the first docs-mode Q14 failed on two
  instrument/report-alignment findings (the required-string list still
  carried the BASE-form core status; one forbidden-phrase hit in the
  ledger's S-AUD-01 summary line), both fixed within the correction scope,
  after which the final full run passed 14/14 + 15/15 (QC_REPORT.md records
  the exact findings and fixes; the repair-round budget is exhausted by
  design).

ANTI-SUCCESS-THEATER (every load-bearing PASS with its falsifier; each
row's limit is the tested scope, not a general claim):

| PASS record | MEASURED_QUANTITY | INDEPENDENT_SOURCE_OF_TRUTH | WHY_NON_CIRCULAR | FAILURE_CASE_DETECTED |
|---|---|---|---|---|
| D1 per-opcode tables | 2 negatives REJECT + 6 legal controls at true lengths + all carried H2 controls (72 unit entries) | GNU objdump Binutils 2.44 ((bad)/legal verdicts captured BEFORE decoder evaluation) | the oracle is a different toolchain; the expectations are fixed in the capture script | `0F 73 E0 02` accepted by BASE (reproduced in-run via the committed BASE modules) -> now REJECT |
| D1 downstream falsifier | boundary UNRESOLVED, CALL_VALIDATION=NOT_VERIFIED, no promoted target; BASE measured CONFIRMED/PASS/target 0x00A0000E | the production boundary machinery through BOTH decoder versions (BASE imported READ-ONLY with recorded identities) | the BEFORE state is measured, not asserted; no VA special-casing | decoding an invalid first instruction grants unearned continuity to a later E8 |
| D2 pin universe | 133 == 133 == 133 == declared total; 46/46 EA re-derived; 8/8 D2 mutations causal | the BASE-pinned PINS Git blob (ast literal extraction; re-derived in-run by the gate) + the pinned EXE | the roster is never derived from the checked artifacts; the registry file is itself checked against the git re-derivation | whole-pin deletion, duplicate claim, extra claim, synchronized omission with adjusted totals (D2-M2/M4/M5/M6/M7/M8) |
| D2 role/EA applicability | kind mutation fails the role check AND EA validation stays enforced (D2-M1/M3); operand_kind now EXE-verified in Q3 | the expected role from PINS + the EXE decode | applicability never decided by the mutable JSON kind or CSV operand_kind | relabelled mem->code_entry + removed EA object (the Desktop bypass, now caught with 2 predicates) |
| Carried repairs reproduced | NEW-F cached+uncached+permutations; NEW-G; H1 table; A1/A2/B/C/D/E; REAL-REFUTE x2; 3 real positive CALLs; M1-M6+AF3 7/7 | objdump (fixtures) + the pinned EXE (real cases) | same machinery re-executed fresh; not copied records | any behavioural drift of a carried control would fail its case (outcome-conditional) |
| Regression measurement | 3 artifacts byte-identical; 3 metadata-only; census 0/2612 rows changed; quantities identical | both sides read from disk; byte-identity is SHA256-based | the diff never trusts declared equality | any D1-caused stream change would surface as a census/pin row change (none did; zero pattern occurrences in .text) |
| Gates Q1-Q14 | every status derived in-run from measured inputs | the pinned EXE, Git state, the physical artifacts | no hard-coded PASS anywhere in the battery | any gate FAIL would be reported honestly (outcome-conditional) |

## Honest limits

- The D1 repair is measured on the oracle-verified fixture set and the
  unit battery; this package does NOT claim the decoder is a general-purpose
  x86 decoder (the bounded fail-closed instrument boundary is the H2/H1/P2-2
  control set; the census re-decode of all 2612 rows is clean).
- The D2 repair binds Q2 to the pinned 133-claim roster; it does not claim
  the roster's semantic correctness beyond what the EXE re-derivation
  validates (the specification defines what must be measured; the gate
  checks both sides - roster vs artifacts and EXE vs artifacts - and a
  disagreement of either is a FAIL).
- The 2218 unresolved census rows remain unresolved (this correction did
  not resolve any; none was in its scope).
- The four AF3-downgraded layout controls remain UNRESOLVED; the
  0x0075138F ArkEstateObject lead remains NOT_PROMOTED.
- ULTIMATE_VALUE_SOURCE = UNKNOWN; the assignment core's open states are
  preserved without promotion.
- After the persistence-phase commit the HEAD moves BY DESIGN; the manifest
  covers AUDIT_ENTRYPOINT.md at its BASE state and must be regenerated by
  the phase that adds the run row.
