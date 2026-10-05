# FINAL REPORT — PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005

One bounded correction-only run for the THREE P2 defects of the independent
Desktop post-audit (PE_935_F84_C2_DESKTOP_POST_AUDIT_20261004, verdict
REQUIRE_CORRECTIONS) plus the two bounded decoder-hygiene items H1/H2. This
run exists SOLELY to repair reusable forensic/QC machinery. NO new
placement science, NO 0xA4 source/init experiment, NO new Ark/Ni research,
NO templates.vfs, NO RECORD_A, NO Model 194013, NO world placement/XYZ, NO
client execution, NO broad function discovery, NO class atlas, NO
general-purpose x86 decoder project, NO new backing-source work.

Correction statuses (this run, measured):

- P2_1_BOUNDARY_CACHE = CORRECTED_SORTED_EXTENTS
- P2_2_66_0F8X_NEAR_JCC = CORRECTED_BRANCH_A_REL16
- P2_3_Q2_EFFECTIVE_ADDRESS = CORRECTED_RE_DERIVED_FROM_EXE
- H1_REG16_RM7 = CORRECTED_BX_TABLE
- H2_GROUP_OPCODES = CORRECTED_FAIL_CLOSED_VALIDITY

Phase-1 semantics (this is a two-phase flow; phase 2 is NOT this task):

- PHASE_1_MANIFEST_GENERATED = NO
- PHASE_1_ENTRYPOINT_MODIFIED = NO
- PHASE_1_COMMIT_OR_PUSH_PERFORMED = NO
- PHASE_1_ONLY_REVIEW_PENDING = YES
- PE-MASTER INTERNAL PRE-PUBLICATION REVIEW = NOT_PERFORMED_AT_PHASE_1
  (phase 2 will persist the PE-MASTER internal pre-publication review
  verdict before the manifest; the independent post-audit of the published
  commit remains a separate human-relayed ChatGPT Desktop step; PE-MASTER
  remains advisory/pre-qualification, CANONICAL_GATE_EFFECT=NONE).

## P2-1 — boundary cache / anchor conflict (pebnd.py)

DEFECT: the C2 `_BoundaryCache` stored decode extents as a SET and
`covers_mid_instruction` early-broke at `a >= target_off` over UNORDERED
iteration, so the covering extent could be visited after a later-starting
extent already triggered the break. Two measured consequences: (a)
REFUTED_MID_INSTRUCTION was underclaimed - real manifestations re-derived
this run: 0x004B0A02 interior to `BB 01 00 00 00` @0x004B0A01 and
0x004B0A21 interior to `E8 4D 14 F5 FF` @0x004B0A1E, anchor 0x004B0980
(both were committed UNRESOLVED); (b) ANCHOR_CONFLICT could be suppressed -
when anchor A covers the candidate mid-instruction and anchor B lands
exactly on it, the honest result is UNRESOLVED/ANCHOR_CONFLICT with
CALL_VALIDATION != PASS and the target NOT promoted; the defect could hide
A's coverage and let B's exact landing confirm - a FALSE CALL promotion.

REPAIR (no policy weakening): extents are stored and iterated SORTED; the
coverage scan is a module-level order-independent function (it sorts its
input, so the early break is valid only over the sorted scan);
lands+refutes => UNRESOLVED/ANCHOR_CONFLICT remains the exact policy.

FALSIFIERS (all PASS, each with bytes/anchors/expected+measured
boundaries/promotion result/failure condition persisted):

- NEW-F (`B8 00 E8 01 00 00 00 90 CC`, anchors A=+0, B=+2, candidate
  E8=+2): BOUNDARY_STATUS=UNRESOLVED, BOUNDARY_SOURCE=ANCHOR_CONFLICT,
  CALL_VALIDATION=NOT_VERIFIED (not PASS), TARGET not promoted; the same
  result on the cached and the uncached paths; NEW_F_INTERNAL_E8_PROMOTED = NO.
- Order-independence proofs: 56 synthetic insertion permutations of the
  same cached extents (every order: stream-A coverage of the candidate
  = True; stream-B coverage = False) + 50 randomized orders of the real
  0x004B0980 production stream (75 extents; per-target results identical to
  the baseline in every order) - persisted in
  01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json.
- REAL-REFUTE: 0x004B0A02 and 0x004B0A21 re-derive
  REFUTED_MID_INSTRUCTION / KNOWN_FUNCTION_ENTRY with
  boundary_refuted_by=0x004B0980 - WITHOUT special-casing the VAs (the
  same-VA pins flow through the same generic machinery as all 133 pins and
  all 2227 positive census candidates). The DECLASSIFIED_NOT_A_CALL ledger
  statuses of the two pins are UNCHANGED (the declassification as not-a-CALL
  remains correct; its recorded boundary evidence is strengthened -
  ledger records S-P2-05/S-P2-06).
- The positive control E and the three real-EXE CALL controls
  (0x0070C715->0x00972380, 0x0070DD75->0x00971AD0, 0x0070C742->0x00972DF0)
  still PASS with their exact targets.

## P2-2 — 66 0F 8x near Jcc false CALL (x86dec.py)

DEFECT: `_2BYTE[0x80..0x8F] = ("F", 6)` treated near Jcc as fixed 6-byte
rel32 forms even with the 66 operand-size override; in 32-bit mode
`66 0F 8x` is a near Jcc rel16 (length 5 with the prefix). The C2 decoder
measured the NEW-G fixture's first instruction as 7, its anchor stream
landed on an E8 interior to the following MOV's immediate, and
validate_direct_call fabricated a CALL edge (PASS, target 0x00A0000D).

BRANCH A CHOSEN (and why): the corrected decoder implements the TRUE rel16
form for the whole 0x80..0x8F class (length = prefixes + 2 + 2, operand
recorded, rel16=True; 67-prefixed near Jcc REJECTED fail-closed, consistent
with the standing 67 E8/E9 policy). Branch A was chosen because the
independent oracle (GNU objdump Binutils 2.44) establishes the exact
semantics (`66 0f 84 00 00` = je rel16, 5 B), the rel16 pattern is the same
already-corrected class as 66 E8/E9, and a correct length preserves honest
boundary coverage instead of aborting real decode streams. The alternative
(REJECTED_UNSUPPORTED) was rejected for this production decoder because a
fail-closed stop on a decodable form would UNDERCLAIM boundaries on real
streams; the fail-closed discipline is preserved for genuinely unsupported
forms.

MANDATORY FIXTURE NEW-G (`66 0F 84 00 00 B8 00 E8 01 00 00 00 C3`):
first instruction measured 5 bytes (oracle: je rel16, 5 B; the C2 decoder
measured 7 and promoted a fabricated CALL edge); the E8 at +7 is interior
to `B8 00 E8 01 00` (MOV EAX,0x0001E800, +5..+10) ->
BOUNDARY_STATUS=REFUTED_MID_INSTRUCTION, CALL_VALIDATION=FAIL_MID_INSTRUCTION,
TARGET not promoted, NEW_G_INTERNAL_E8_PROMOTED = NO.

Oracle record: verbatim objdump command line + raw disassembly persisted in
01_RAW/ORACLE_INDEPENDENT_RECORDS.json (the production decoder is never its
own source of truth for synthetic fixtures).

Required unit battery (measured from the generated artifact: 64 vectors;
count derived, never hard-coded): ordinary `0F 84` rel32 = 6;
`66 0F 84` / `66 0F 8F` rel16 = 5; `67 0F 84` REJECT; ordinary E8 rel32
positive control = 5; existing 66 E8 rel16 = 4; existing 0F C6 /r ib = 4;
existing 67-address-size = 5; A1/A2 false-E8-immediate vectors; H1 vectors;
H2 vectors. ALL PASS.

## P2-3 — gate Q2 effective_address validation (cqc_battery.py)

DEFECT: the C2 gate_q2 re-derived only opcode_bytes, instruction_length,
boundary_status/source + limited JSON<->CSV fields; the JSON pins'
`effective_address` object was NOT validated (the Desktop post-audit
mutated the real THE_STORE_plus_84 pin - VA 0x0070C71E, bytes
`89 86 84 00 00 00` - base_register ESI->EAX and provenance -> a fake
known-function provenance, and ALL gates Q2-Q13 still passed).

CORRECTION: gate_q2 now independently re-derives, for every JSON pin where a
field is semantically applicable, from the pinned EXE (EXE decode +
independently derived boundary/function context; the battery decodes the
pinned EXE itself - it does NOT compare JSON to another field copied from
the same generator; the CSV row participates only as a secondary
consistency cross-check where it carries the EA representation):

Q2_EFFECTIVE_ADDRESS_FIELDS = effective_address present/memop state; operand_width; segment; base_register; index_register; scale; raw_displacement; signed_displacement; effective_displacement; address_provenance_status

Missing field where semantically required = FAIL. Mismatch = FAIL. The
displacement width is enforced through the raw_displacement NONE-vs-value
derivation (and the derived width is recorded per pin); the
effective-address textual form is validated where persisted (the CSV
measured_operand's EA pipe representation, cross-checked); the
this/object-base relation and provenance are re-derived via the boundary +
entry this-flow. Measured: 46 EA pins checked, 46 re-derived, 0
mismatches on the clean package.

CAUSAL MUTATIONS (P2-3): M5 (base_register ESI->EAX) and M6 (provenance ->
THIS_OF_KNOWN_FUNCTION:FUN_00000000_FAKE) - each a temporary mutated copy
of the ACTUAL final artifact outside the repo, routed through the SAME
gate_q2: CLEAN -> PASS, MUTATED -> FAIL with the exact failing predicate
recorded (01_RAW/CQC_MUTATION_RESULTS.json).

CLAIM CORRECTION: the C2 HANDOFF/commit-message Q2 coverage wordings are
SUPERSEDED (ledger records S-P2-01..S-P2-03; the historical commit itself
is immutable - the supersession is recorded, history is not edited). THIS
document states EXACTLY which fields the corrected Q2 covers (the
enumeration above); JSON fields outside that set are NOT claimed as
Q2-validated.

## H1 — 16-bit ModRM rm=7 (bounded hygiene)

DEFECT: REG16_ADDR_BASE mapped rm=7 -> "BP"; the correct 16-bit addressing
table is rm=7 mod=0 [BX], mod!=0 [BX+disp] (rm=6 mod=0 [disp16], mod!=0
[BP+disp]). The complete rm=0..7 table is corrected. Verified against the
independent oracle over the full table (mod 0/1/2): `67 8B 07` =
mov eax,[bx] (the H1 defect case), `67 8B 47 05` = [bx+0x5],
`67 8B 46 05` = [bp+0x5], `67 8B 06 34 12` = ds:0x1234, and the remaining
rm positions - 24 oracle fixtures. Lengths are UNCHANGED by this repair
(register naming only), so no boundary stream shifted (measured: zero
length differences across all 2612 census rows and all 133 pins).

## H2 — grouped opcode validity (bounded hygiene)

DEFECT: `0F BA` and `0F 71/72/73` decoded every ModRM.reg sub-opcode with
their trailing imm8. CORRECTION: validity is judged by opcode + ModRM.reg +
ModRM.mod + the relevant mandatory prefix - NOT by one shared reg
whitelist:

- 0F BA: reg 4..7 (BT/BTS/BTR/BTC r/m,imm8) legal with ANY mod (memory
  forms legal); reg 0..3 reserved -> REJECT fail-closed.
- 0F 71/72/73: the immediate-shift forms are REGISTER-ONLY (mod must be 3
  - both MMX and SSE2; a memory form is never guessed as a valid
  immediate-shift instruction); without 66: reg {2,4,6} legal (MMX
  PSRLW/PSRAW/PSLLW, PSRLD/PSRAD/PSLLD, PSRLQ/PSLLQ; 0F 73 reg {3,7}
  reserved without 66); with 66: reg {2,4,6} legal (SSE2) and
  `66 0F 73 /3` and `/7` with mod=3 are LEGAL PSRLDQ/PSLLDQ - they must NOT
  be misreported as reserved; F2/F3-prefixed forms have no legal encoding
  -> REJECT; reg {0,1,5} (and 7 for 71/72) reserved in every combination.

Oracle-verified legal positive controls: `0F BA E0 05` (bt eax,0x5),
`0F BA 6D 00 05` (bts [ebp+0x0],0x5), `0F 71 D0 02` (psrlw mm0,0x2),
`66 0F 71 D0 02` (psrlw xmm0,0x2), `66 0F 73 DB 03` (psrldq xmm3,0x3),
`66 0F 73 FB 03` (pslldq xmm3,0x3) and the family variants; illegal
negative controls (oracle verdict `(bad)`): `0F BA C0 05` (/0),
`0F 71 C8 02` (/1), `0F 73 D8 02` (/3 without 66), `0F 71 00 02` (MMX
memory form), `66 0F 73 5B 00 03` (PSRLDQ memory form), `F3 0F 71 D0 02`
and the remaining reserved combinations - 25 H2 fixtures. All decode as
expected (legal imm8 forms with their true length; reserved/invalid forms
REJECT with no invented length, never skipping past an undecodable byte).

## Preserved scientific core (re-measured, unchanged)

FACTORY_PLUS_84_ASSIGNMENT_CORE = CONFIRMED_STATIC_CONDITIONAL
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
WORLD_XYZ_RECOVERED = NO
WRITER_FUNCTION = FUN_009777F0
WRITER_VA = 0x00977810
TAG6_TO_ID10 = PRESERVED_CONFIRMED
SPECIFIC_RUNTIME_GETTER_VALUE_PRODUCER = UNVERIFIED
TABLE10_SOURCE_VALUE_REPRESENTATION = RECORD_FIELD
CLEAR_RESET_CONFIRMED_COUNT = 0

The 0xA4 object receives NO class name and is NOT called a stream (the
structural-identity and naming discipline of the source package is carried
unchanged; no ArkParameterCommon or NiNode bridge is created by naming
similarity). The 0x0075138F ArkEstateObject lead stays NOT_PROMOTED (no
strong anchor for the containing function); wherever this package repeats
that lead, the wording is exactly: instruction start =
ARK_ESTATE_INSTRUCTION_START_VA = 0x0075136E and immediate location =
ARK_ESTATE_IMMEDIATE_LOCATION_VA = 0x00751370 (the vptr 0x00A87410
immediate bytes; ledger record S-P2-09).

Scope/nonclaim invariants (all carried, all measured true this run):
NEW_BACKING_SOURCE_RE_EXECUTED = NO; TEMPLATES_VFS_OPENED = NO;
RECORD_A_ANALYZED = NO; MODEL_194013_TRACE_EXECUTED = NO;
PLACEMENT_XYZ_RE_EXECUTED = NO; CLIENT_EXECUTED = NO;
CANONICAL_GATE_EFFECT = NONE. The 34 strong anchors are
PRIOR_CANON_ANCHOR_INPUT (this run does not claim to independently
re-prove them; entry bytes were re-verified at the pinned VAs only).

## Regenerated artifacts and the changed-field regression vs C2

All dependent artifacts were REGENERATED from the corrected machinery
(never hand-patched): C1_PIN_EVIDENCE.json, CORRECTED_PIN_LEDGER.csv,
C2_CENSUS.json, CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv, the boundary
test evidence, the decoder unit tests, the mutation results, the QC final
record, C3_OBJECT_SCOPE.json, AF3_PROVENANCE_LEDGER.csv. C3/AF3 were
regenerated with the corrected instruments EVEN THOUGH their values
remained unchanged - measured: both output files are BYTE-IDENTICAL to the
committed C2 files (fresh regeneration, not copied records).

Census quantities (recomputed; old values NOT forced - every value
re-measured identical to the committed C2): RAW_PATTERN_ROWS=2612
(regression expectation MATCH), POSITIVE_PLUS_84_ENCODING_ROWS=2227,
NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS=385,
BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS=10,
BOUNDARY_REFUTED_MID_INSTRUCTION_ROWS=0,
KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES=2,
CENSUS_UNRESOLVED_ROWS=2218,
FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES=832,
REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE=1,
REJECTED_READ_NOT_WRITE=6, REJECTED_MID_INSTRUCTION_PER_PROVEN_DECODE=0,
ADDRESS_PROVENANCE_UNRESOLVED=832, DECODER_REJECT_ROWS=0. Pin ledger: 133
records, 0 failures (120 VALIDATED + 4 CORRECTED_VALIDATED + 2
DECLASSIFIED_NOT_A_CALL + 5 VALIDATED_BYTES_BOUNDARY_UNRESOLVED + 2
NOT_VERIFIED - identical status distribution to C2). The four unsupported
AF3 wrong-object promotions remain UNRESOLVED (no new identity edge was
established or attempted - no discovery sweep). Ctor call-site census: 10
raw E8 matches, 2 boundary-confirmed (0x0070C715 + 0x0072FA76 LEAD ONLY).

CHANGED-BOUNDARY-FIELDS table vs the committed C2 artifacts (complete
list; nothing else changed - measured by diff_vs_c2.py and
01_RAW/CHANGED_FIELDS_VS_C2.json):

| Artifact | Row/pin | Field | Old | New |
|---|---|---|---|---|
| CORRECTED_PIN_LEDGER.csv | driver_declassified_0x004B0A02 | boundary_source | HEURISTIC_START_CANDIDATE | KNOWN_FUNCTION_ENTRY |
| CORRECTED_PIN_LEDGER.csv | driver_declassified_0x004B0A02 | boundary_status | UNRESOLVED | REFUTED_MID_INSTRUCTION |
| CORRECTED_PIN_LEDGER.csv | driver_declassified_0x004B0A02 | boundary_start | (empty) | 0x004B0980 |
| CORRECTED_PIN_LEDGER.csv | driver_declassified_0x004B0A02 | boundary_refuted_by | (empty) | 0x004B0980 |
| CORRECTED_PIN_LEDGER.csv | driver_declassified_0x004B0A21 | boundary_source | HEURISTIC_START_CANDIDATE | KNOWN_FUNCTION_ENTRY |
| CORRECTED_PIN_LEDGER.csv | driver_declassified_0x004B0A21 | boundary_status | UNRESOLVED | REFUTED_MID_INSTRUCTION |
| CORRECTED_PIN_LEDGER.csv | driver_declassified_0x004B0A21 | boundary_start | (empty) | 0x004B0980 |
| CORRECTED_PIN_LEDGER.csv | driver_declassified_0x004B0A21 | boundary_refuted_by | (empty) | 0x004B0980 |
| 01_RAW/C1_PIN_EVIDENCE.json | driver_declassified_0x004B0A02 | boundary_status | UNRESOLVED | REFUTED_MID_INSTRUCTION |
| 01_RAW/C1_PIN_EVIDENCE.json | driver_declassified_0x004B0A02 | boundary_source | HEURISTIC_START_CANDIDATE | KNOWN_FUNCTION_ENTRY |
| 01_RAW/C1_PIN_EVIDENCE.json | driver_declassified_0x004B0A02 | boundary_start | null | 0x004B0980 |
| 01_RAW/C1_PIN_EVIDENCE.json | driver_declassified_0x004B0A02 | boundary_refuted_by | null | 0x004B0980 |
| 01_RAW/C1_PIN_EVIDENCE.json | driver_declassified_0x004B0A21 | boundary_status | UNRESOLVED | REFUTED_MID_INSTRUCTION |
| 01_RAW/C1_PIN_EVIDENCE.json | driver_declassified_0x004B0A21 | boundary_source | HEURISTIC_START_CANDIDATE | KNOWN_FUNCTION_ENTRY |
| 01_RAW/C1_PIN_EVIDENCE.json | driver_declassified_0x004B0A21 | boundary_start | null | 0x004B0980 |
| 01_RAW/C1_PIN_EVIDENCE.json | driver_declassified_0x004B0A21 | boundary_refuted_by | null | 0x004B0980 |
| 01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json | 7 new case records | <CASE> | MISSING | present (NEW-F, NEW-G, 2x REAL-REFUTE, 3x REAL positive controls) |

Census rows changed: 0 of 2612. Census quantities changed: 0. C3 changed:
0. AF3 rows changed: 0. The expected known change (the two declassified
driver pins UNRESOLVED -> REFUTED_MID_INSTRUCTION) was measured by the
machinery, not hard-coded - the two pins were the ONLY change the
correction produced across the entire artifact surface.

## Targeted QC (SELF_CHECK; honest labeling)

MUTATION_TOTAL = 7 (M1, M2, M3, M4, AF3/Q8 COMPOUND, M5, M6);
MUTATION_CAUSAL_PASS = 7/7. Each: unmutated ACTUAL artifact -> SAME
production gate PASS; precisely-declared mutated temporary copy (temp
tree outside the repo, deleted after, never persisted) -> SAME gate FAIL;
unrelated artifacts byte-identical; the pinned EXE re-hashed at both
executions; the SAME gate function object. The AF3/Q8 mutation is COMPOUND
and is reported with ALL changed fields (IDENTITY_EDGE, IDENTIFIED_OBJECT,
IDENTITY_EVIDENCE, ADDRESS_PROVENANCE_STATUS; 5 failing predicates), never
called a one-field mutation.

ANTI-SUCCESS-THEATER (every load-bearing PASS with its falsifier):

| PASS record | MEASURED_QUANTITY | INDEPENDENT_SOURCE_OF_TRUTH | WHY_NON_CIRCULAR | FAILURE_CASE_DETECTED |
|---|---|---|---|---|
| P2-1 coverage repair | 16 changed boundary fields, exactly the two driver pins; 56+50 permutation proofs all invariant | pinned EXE re-decode; objdump for the fixture semantics | the coverage scan sorts its input; permutation harness inserts the same extents in every order | unordered extent order (NEW-F: anchor-conflict suppression -> UNRESOLVED, no promotion) |
| P2-2 near-Jcc repair | 64 unit vectors; NEW-G boundary REFUTED, no promotion | GNU objdump Binutils 2.44 (fixtures locked BEFORE the decoder fix) | the oracle is a different toolchain than the production decoder | 66 0F 84 false-E8 promotion (NEW-G: CALL_VALIDATION=FAIL_MID_INSTRUCTION, NEW_G_INTERNAL_E8_PROMOTED=NO) |
| P2-3 Q2 EA validation | 46 EA pins re-derived; 7/7 mutations causal | pinned EXE decode + entry this-flow; CSV as secondary cross-check only | the battery re-derives from the EXE, never JSON-vs-JSON | base-register JSON corruption (M5) and fake-provenance JSON corruption (M6): clean PASS -> mutated FAIL |
| H1 rm table | 24 oracle fixtures (mod 0/1/2, full rm set) | objdump | register naming verified per-rm against the oracle | rm=7 misnamed [BP] (C2) -> [BX] |
| H2 group validity | 25 oracle fixtures (legal + illegal) | objdump `(bad)` verdicts | validity decided by opcode+reg+mod+prefix vs the oracle | reserved 0F BA /0-/3 and invalid imm-shift forms decoded as valid (C2) -> REJECT |
| Gates Q1-Q13 | 13/13 PASS + Q14 docs gate | measured inputs on disk | every status derived in-run | any gate FAIL would be reported honestly (outcome-conditional) |

Unit-test count: 64 (measured from 01_RAW/CQC_DECODER_UNIT_TESTS.json;
never hard-coded). Boundary matrix: 13 cases. Oracle fixtures: 71.

QC_SCOPE = SELF_CHECK_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION (executor
self-QC; author/origin explicit: pe-reconstruction worker session under
PE-MASTER dispatch; the phase-1 package does NOT claim an independent
review; QC PASS is outcome-conditional - the 2218 unresolved census rows
and every NOT_ESTABLISHED/UNVERIFIED state above are corrected honest
states, not failures).

## Honest limits

- No defect was found that could not be fixed within the bounded scope; the
  repair is COMPLETE for the three P2 + H1 + H2 as defined by the dispatch.
- The four unsupported AF3 wrong-object promotions remain UNRESOLVED (no
  new identity edge was established - establishing one was out of scope).
- The census boundary coverage is unchanged (10 confirmed rows; the
  correction did NOT resolve any of the 2218 unresolved census rows).
- This package does not claim the corrected decoder is a general-purpose
  x86 decoder; it is the bounded production instrument with the exact
  capability set documented above (and the H2 positive/negative controls
  as its boundary).
