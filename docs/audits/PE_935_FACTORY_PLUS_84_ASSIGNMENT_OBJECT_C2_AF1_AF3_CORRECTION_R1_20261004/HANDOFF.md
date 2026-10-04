# HANDOFF — PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004

RUN_ID: PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004
Executor: pe-reconstruction | Dispatch: HUMAN + PE-MASTER direct (bounded C2
AF1/AF3 correction contract with Ni reference support; NO_NESTED_TASKS;
publication assigned in-contract) | 2026-10-04.

## RUN_STATUS

RUN_STATUS = COMPLETED; PACKAGE_CORRECTION_STATUS = CORRECTED (AF1 + AF2 +
AF3 + P3-A/P3-B/P3-C corrections all executed with fresh measurements; the
production QC passed 14/14 gates with 5/5 causal mutations — see QC_REPORT.md;
the honest UNRESOLVED census candidates, the four downgraded layout controls
and the not-promoted ArkEstateObject lead remain UNRESOLVED by discipline,
which is corrected honesty, not a failure).

## PHASE-SPECIFIC SHA SEMANTICS (at package freeze)

HEAD_SHA = 535e1a00fe793299dea7fc639e552560a6ac633b
HEAD_SHA_AT_PACKAGE_FREEZE = 535e1a00fe793299dea7fc639e552560a6ac633b
COMMIT_SHA = NOT_AVAILABLE_AT_PACKAGE_FREEZE

(The resulting commit's own SHA is reported only in the final executor
response AFTER push and remote verification; no committed artifact embeds its
own commit SHA; this HANDOFF is NOT modified after manifest generation.)

## THE CORRECTION IN FIVE LINES

1. **AF1**: the production QC now validates the ACTUAL committed artifacts —
   gate Q2 re-derives every C1-JSON pin field from the pinned EXE, Q3 the
   pin CSV rows (measured_operand included), Q6 the census boundary anchors,
   Q7 the AF3 identity chains, Q8 the C3 store collection — and the causal
   mutation harness routes TEMPORARY COPIES of the ACTUAL final artifacts
   through the SAME gates: M1 (C1 JSON ctor bytes) / M2 (CSV callback
   measured_operand) / M3 (C3 store collection) / M4 (census
   containing_function=entry~0xDEADBEEF) / AF3-Q8 (manager identity edge
   removed) = 5/5 UNMUTATED=PASS -> MUTATED=FAIL.
2. **AF2**: boundary policy is strong-anchor-only (34-entry prior-canon
   KNOWN_FUNCTION_ENTRY table with recorded ANCHOR_VA/ANCHOR_CLASS/
   EXISTING_PHYSICAL_EVIDENCE/EVIDENCE_SOURCE/EVIDENCE_STATUS); the C1
   CC-padding/RET-delimited starts are HEURISTIC_START_CANDIDATE (recorded,
   never confirming, never promoting); a proven decode covering a candidate
   mid-instruction REFUTES it; the decoder fixes the SHUFPS imm8 (0F C4/C5/C6),
   16-bit-address (67) and 66 E8 rel16 classes and rejects fail-closed
   otherwise; counterexample classes A1/A2/B/C/D all REFUTE with no promotion,
   the E positive control still promotes, and 3 real-EXE callsites re-validate
   (0x0070C715 -> 0x00972380; 0x0070DD75 -> 0x00971AD0; 0x0070C742 ->
   0x00972DF0).
3. **AF3**: REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE = 1 (the manager
   row 0x00707EC0 with its full per-row identity chain in
   AF3_PROVENANCE_LEDGER.csv); the four C1 layout-evidence rejections are
   downgraded to UNRESOLVED (grammar hypotheses, not identity chains); the
   0x0075138F ArkEstateObject lead is physically re-verified (vptr immediate
   0x00A87410 at 0x00751370; RTTI chain byte-read matches
   .?AVArkEstateObject@@) but NOT promoted — its containing function has no
   strong anchor, so the base/object cannot be bridged within this
   discipline.
4. **P3-A/P3-B/P3-C**: the ctor store census represents SEGMENT semantics
   (3 effective-displacement-0 writes: `89 07` [EDI] + the two FS:[0] SEH
   stores 0x009723A0/0x009724CB, segment=FS persisted, explicitly excluded
   from this+0/vptr eligibility; DIRECT_VPTR_STORE_IN_EXAMINED_CTOR stays
   NOT_OBSERVED); DECLARED_ENCODING_FAMILY_COUNT = 9 derived from the actual
   scanner family table (C1 metadata 10 superseded); the INPUT_IDENTITIES
   repository-owner typo corrected to SebastianKozlo/eudoria-clean (exact
   old->new recorded in S-C2-12; historical file untouched).
5. **PRESERVED CORE** (re-measured, unchanged):
   FACTORY_PLUS_84_ASSIGNMENT_CORE=CONFIRMED_STATIC_CONDITIONAL;
   ASSIGNMENT_FUNCTION=FUN_0070C680; ASSIGNMENT_VA=0x0070C71E;
   ASSIGNMENT_STORE_BYTES=89 86 84 00 00 00; ASSIGNED_OBJECT_SIZE=0xA4/164 B;
   ASSIGNED_OBJECT_CONSTRUCTOR=FUN_00972380; both known stores re-pinned at
   KNOWN_FUNCTION_ENTRY-confirmed boundaries (133 pin records, 0 failures).

## TERMINAL STATE (exact strings in FINAL_REPORT.md)

The fresh census quantities: RAW_PATTERN_ROWS=2612 (regression expectation
MATCH), POSITIVE=2227, NEGATIVE_DISP8=385, BOUNDARY_CONFIRMED=10 (strong
anchors only; C1's 1685 padding-derived confirmations superseded),
KNOWN_CONFIRMED_WRITES=2, REJECTED_READ_NOT_WRITE=6,
REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE=1, CENSUS_UNRESOLVED_ROWS=2218,
FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES=832,
EXAMINED_ENCODING_CANDIDATE_CLOSURE=CLOSED (raw byte-grammar enumeration
scope), EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE=NOT_ESTABLISHED (invariant),
CLEAR_RESET_CONFIRMED_COUNT=0; ASSIGNED_OBJECT_VTABLE=UNVERIFIED,
OBJECT_POLYMORPHISM=NOT_ESTABLISHED, DIRECT_VPTR_STORE_IN_EXAMINED_CTOR=
NOT_OBSERVED, KNOWN_EXAMINED_CALLSITES_ARE_DIRECT=YES; all preserved
predecessor states carried verbatim; NEW_BACKING_SOURCE_RE_EXECUTED=NO,
TEMPLATES_VFS_OPENED=NO, RECORD_A_ANALYZED=NO,
MODEL_194013_TRACE_EXECUTED=NO, PLACEMENT_XYZ_RE_EXECUTED=NO,
CLIENT_EXECUTED=NO, CANONICAL_GATE_EFFECT=NONE.

## COMMON TERMINAL FIELDS (measured this run)

```text
RUN_ID = PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004
RUN_CLASS = LOAD_BEARING
RUN_TYPE = DESKTOP_POST_AUDIT_FOCUSED_CORRECTION
BASE_SHA = 535e1a00fe793299dea7fc639e552560a6ac633b
SOURCE_RUN_ID = PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004
SOURCE_PACKAGE = docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/
OUTPUT_ROOT = docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_C2_AF1_AF3_CORRECTION_R1_20261004/
EXE_SIZE = 8015872
EXE_SHA256 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
AF1_STATUS = CORRECTED
AF2_STATUS = CORRECTED
AF3_STATUS = CORRECTED
P3_STATUS = CORRECTED (P3-A + P3-B + P3-C all corrected; P3_C verified)
PACKAGE_CORRECTION_STATUS = CORRECTED
QC_STATUS = QC_PASS (SELF_CHECK 14/14 gates + 5/5 causal mutations; NOT an independent audit)
MUTATION_TEST_COUNT = 5
MUTATION_CAUSAL_PASS_COUNT = 5
MUTATION_CAUSAL_FAIL_COUNT = 0
MUTATION_NOT_ESTABLISHED_COUNT = 0
RAW_PATTERN_ROWS = 2612
POSITIVE_PLUS_84_ENCODING_ROWS = 2227
NEGATIVE_DISP8_MINUS_0x7C_CONTROL_ROWS = 385
BOUNDARY_CONFIRMED_POSITIVE_PLUS_84_ROWS = 10
KNOWN_CONFIRMED_FACTORY_PLUS_84_WRITES = 2
REJECTED_READ_NOT_WRITE = 6
REJECTED_WRONG_OBJECT_WITH_PROVEN_PROVENANCE = 1
CENSUS_UNRESOLVED_ROWS = 2218
FACTORY_PLUS_84_UNRESOLVED_WRITE_CANDIDATES = 832
ADDRESS_PROVENANCE_UNRESOLVED = 832
DECODER_REJECT_ROWS = 0
DECLARED_ENCODING_FAMILY_COUNT = 9
NEW_SUPERSESSION_RECORD_COUNT = 13
MANIFEST_ROW_COUNT = 25
MANIFEST_MISSING = 0
MANIFEST_EXTRA = 0
MANIFEST_DUPLICATES = 0
MANIFEST_SIZE_MISMATCHES = 0
MANIFEST_SHA256_MISMATCHES = 0
FILES_CHANGED = OUTPUT_ROOT/** (25 files incl. this manifest) + 1 AUDIT_ENTRYPOINT.md insertion
AUDIT_ENTRYPOINT_UPDATED = YES
NEW_BACKING_SOURCE_RE_EXECUTED = NO
TEMPLATES_VFS_OPENED = NO
RECORD_A_ANALYZED = NO
MODEL_194013_TRACE_EXECUTED = NO
PLACEMENT_XYZ_RE_EXECUTED = NO
CLIENT_EXECUTED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES (after publication verification)
```

(The manifest bijection fields above are the verified results of
make_manifest.py — generated LAST, self-excluded, bijection-verified, with
this HANDOFF's declared MANIFEST_ROW_COUNT cross-checked against the measured
count; any mismatch aborts the manifest generation.)

## NI REFERENCE SUPPORT (separate from the C2 result; outside the repo)

A local Ni reference card was prepared per the dispatch:
`D:\Eudoria_Reconstruction\99_Audits\PE_935_NI_REFERENCE_SUPPORT_R1_20261004\NI_SUPPORT_CARD.md`
(12,723 B, SHA256 4D1534695AB886AA4CCD0398B164D933A595249A7DE6CC3BC8692F20EC3DA2BC).
NI_SUPPORT_CARD_STATUS = PREPARED. Honest limitation recorded on the card and
in the final response: the OpenCode `skill` tool served a STALE rendering of
`pe-nif-gamebryo-reference-stack/SKILL.md` (pre-2026-10-04 wording); the
corrected NiArk statement was verified on the pinned on-disk SKILL.md
(F51F5AB63CF0E70AF4C4443BC599056D87E870C11A329EEE4A7203E344E9A689) instead.
This does NOT affect and does NOT block the C2 result.

## What the NEXT run needs to know

- The recommended next science experiment remains the 0xA4 backing-source
  question (where the object's data/backing comes from and its relation to
  the 20006/tag-6 track) — DESIGNED, NOT EXECUTED, requires independent
  post-audit of THIS package and new human authorization.
- The corrected machinery (03_SCRIPTS/x86dec.py + pebnd.py) is reusable:
  fail-closed decoder with the AF2 counterexample semantics; strong-anchor
  boundary policy with recorded anchor provenance; DIRECT CALL VALIDATION that
  refuses prefixed/mid-instruction/unanchored forms.
- Boundary coverage is now honestly bounded by the 34 strong anchors: 10
  census rows + 124+2 pin rows are confirmed. Extending coverage requires NEW
  anchors with independent physical provenance (a future authorization) —
  heuristic starts are recorded per row but never confirm.
- The four downgraded layout controls (0x0074955A, 0x006D4F88, 0x0075138F,
  0x007196AA) are recorded with their grammar hypotheses and the
  physically-verified ArkEstateObject lead (not promoted) in
  AF3_PROVENANCE_LEDGER.csv — a future run may promote them ONLY with a real
  identity chain (e.g. an independently proven entry for the containing
  function plus a this-binding proof).
- The census CSV is the corrected canonical row universe (2,612 rows with
  full EA fields + corrected boundary columns); the 832 unresolved write
  candidates are the honest bound within the examined encodings under the
  strong-anchor policy; EXHAUSTIVE_FACTORY_PLUS_84_WRITE_CLOSURE stays
  NOT_ESTABLISHED regardless.
- LEAD discipline unchanged: the same-ctor call site @0x0072FA76
  (templates.vfs reader-chain region) is LEAD ONLY (validated CALL ->
  0x00972380; no bridge claim).

## FOR PE-MASTER (audit pointers)

- Claim matrix source: FINAL_REPORT.md (terminal fields block).
- Physical evidence: 01_RAW/C1_PIN_EVIDENCE.json (133 pins + anchor
  registry), 01_RAW/C2_CENSUS.json + CORRECTED_FACTORY_PLUS_84_WRITE_CENSUS.csv
  (2,612 rows), AF3_PROVENANCE_LEDGER.csv (5 rows), 01_RAW/
  C3_OBJECT_SCOPE.json (segment-aware store census), 01_RAW/
  CQC_DECODER_UNIT_TESTS.json, 01_RAW/CQC_BOUNDARY_COUNTEREXAMPLES.json,
  01_RAW/CQC_MUTATION_RESULTS.json, 01_RAW/CQC_FINAL.json,
  AF1_MUTATION_MATRIX.csv, AF2_BOUNDARY_TEST_MATRIX.csv.
- SUPERSESSION_LEDGER.md: 13 records (15 excerpt lines, two records carry two
  excerpts each), every ORIGINAL_EXCERPT a verbatim substring of its named
  READ-ONLY historical source file (machine quotecheck in the Q14 gate).
- Counter-check suggestions: re-hash the EXE; re-run any instrument with
  --out/--csv/--pkg-root to a temp location and diff against the committed
  evidence; re-run the mutation harness (it rebuilds its temp trees from the
  committed artifacts); byte-read the two known stores, the two FS:[0] stores
  and the ArkEstateObject lead bytes (0x00751370 vptr immediate).
- Known QC limitations (honest): boundary coverage is bounded by the 34-entry
  prior-canon anchor table (no new function-discovery sweep was performed);
  census provenance is window/anchor-level (the 832 unresolved write
  candidates were NOT individually deep-proven — by discipline, since register
  naming and decode failures are not proof); the mutation harness covers the
  contract-mandated corruption classes (M1-M4 + AF3/Q8), not every possible
  field corruption; DIRECT_VPTR_STORE_IN_EXAMINED_CTOR is scoped to the
  examined ctor extent.

## PERSISTENCE

Output root verified non-existent, created fresh; foreign untracked paths
untouched; the SOURCE_PACKAGE and all historical packages READ-ONLY.
Immediately before persistence: `git fetch`; the actual remote master
re-verified == 535e1a00fe793299dea7fc639e552560a6ac633b (else
PERSISTENCE_STATUS = BLOCKED_BASE_MOVED, no rebase, no merge, no force push,
local evidence preserved, honest stop). Stage ONLY OUTPUT_ROOT/** and the one
new AUDIT_ENTRYPOINT.md row (never `git add .`; the 6 foreign untracked paths
never staged). Commit once; push normally to master. After push verify
independently: LOCAL_HEAD == ORIGIN_MASTER == ACTUAL_REMOTE_MASTER == the
resulting commit SHA; the exact SHA is reported in the final executor
response only (post-push). Manifest generated LAST (self-excluded; bijection
verified; HANDOFF row-count cross-checked). Any covered file changing after
manifest generation makes the manifest STALE and requires regeneration + full
re-verification.

## HARD STOP

Per the contract: HARD STOP after publication verification. Do NOT begin
backing-source research, 0xA4 input-source research, Engine Rosetta, NiRTTI,
PyFFI, SceneFeeder, templates.vfs, RECORD_A, Model 194013, placement, XYZ or
any other follow-up task. NEXT_EXPERIMENT_AUTHORIZED = NO. The next science
run requires a new HUMAN authorization after independent post-audit of this
exact published SHA.
