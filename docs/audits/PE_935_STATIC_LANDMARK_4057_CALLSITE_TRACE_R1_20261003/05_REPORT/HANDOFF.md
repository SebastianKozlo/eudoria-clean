# HANDOFF — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Finalization + staging phase (pe-master-auditor under direct PE-MASTER dispatch,
NO_NESTED_TASKS). This handoff covers the run's complete record: executor
science phase → fresh targeted QC → repair round R1 → PE-MASTER audit →
finalization R2 (PM-F1 citation fix + reports + entrypoint row + manifest) →
path-limited STAGE (NO commit, NO push — the commit happens in a separate
later phase after PE-MASTER verifies the staged state).

```text
RUN_ID =
PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003
(RUN_CLASS LOAD_BEARING; RUN_TYPE BOUNDED_STATIC_LANDMARK_CALLSITE_TRACE;
 STATIC_ONLY — the client never ran; human run-specific authorization
 2026-10-03: exactly ONE bounded static RE experiment on the deferred 4057
 lead, with mandatory falsifier; one commit + push; terminal HARD STOP)

BASE_SHA =
a4992788982f8ff7f59866fa46aad1176897c69d

HEAD_SHA =
a4992788982f8ff7f59866fa46aad1176897c69d  (at staging; ZERO intervening
commits since BASE; commit SHA appended at publication — the single
publication commit executes only in the separate later phase after PE-MASTER
verifies the staged state)

INPUT_BUILD_SHA256 =
E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
(Entropia.exe, PCG_9_3_5; re-hashed by executor, fresh QC and PE-MASTER)

EXECUTOR_BUDGET =
planned 120 tool calls / 180 wall min; used 84 / ~130
(preregistered in 00_CONTROL/RUN_BUDGET.md BEFORE science; no limit exceeded;
no STOP-by-budget fired; STOP S2 fired — the science-branch terminal)

QC_BUDGET =
planned max 80 tool calls / 120 wall min; used 52 / ~85
(04_QC/TARGETED_QC_REPORT.md §0; fresh context; executor scripts never used
as oracles)

QC_REPAIR_ROUND_R1_BUDGET =
planned 30 tool calls / 60 wall min; used 27 / ~50
(the single authorized repair round; AMEND_LOG_R1.md §7)

SCIENCE RECORD (measured; unchanged through QC, repair R1 and finalization R2):

TEMPLATE_4057_REPIN        = CONFIRMED
TEMPLATE_4057_A            = 218757
TEMPLATE_4057_B            = 218758
MODEL_INDEX_218757        = PRESENT
COLLISION_INDEX_218758    = PRESENT
IMMEDIATE_4057_RAW_PIN    = CONFIRMED

CONTAINING_FUNCTION =
FUN_00599D30, entry 0x00599D30, body 0x00599D30..0x0059AC88, size 3,929 B,
951 instructions, sole caller FUN_0059BE70 @0x0059BF11 (RTTI-gated
ArkRepairUI_Impl builder)

4057_ARGUMENT_ROLE =
thiscall arg1 of this->FUN_008DFCD0(4057), this = LEA ECX,[ESP+0xC8]
(call @0x0059AB1E; RET 4 @0x008DFD61); terminal composite-key element of the
sids string-table lookup ({section_object, 4057} via mgr->FUN_00823C10 ->
generic mapfind FUN_004D1430); the resolved string is stored via FUN_008DFB70
(ArkUI::Component-family store). Full chain: 02_ANALYSIS/CALLSITE_DATAFLOW.md §3.

IMMEDIATE_4057_IS_TEMPLATE_ID =
REJECTED_FOR_THIS_CALLSITE

MANDATORY_FALSIFIER_RESULT =
FAIL_NUMERIC_COINCIDENCE  (gate MANDATORY_FALSIFIER_4057_CALLSITE EXECUTED
and FIRED — STOP S2; a designed terminal, not a failure; certificate verbatim
in 05_REPORT/PE_MASTER_REVIEW.md)

HARDCODED_TEMPLATE_REFERENCE_4057 =
NOT_ESTABLISHED

IMMEDIATE_4057_TO_MODEL_218757 =
NOT_ESTABLISHED

MODEL_RESOURCE_REQUEST_STATUS =
NOT_ESTABLISHED

RUNTIME_NIF_OPEN_218757 =
NOT_ESTABLISHED

CONCRETE_RUNTIME_INSTANCE =
NOT_ESTABLISHED

STATIC_BUILDING_INSTANCE =
UNVERIFIED

WORLD_TRANSFORM_SOURCE =
UNKNOWN

TRANSFORM_SEMANTIC_ROLE =
UNVERIFIED

INSTANCE_TO_SCENE_EDGE =
NOT_ESTABLISHED

PLACEMENT_XYZ_RECOVERED =
NO  (PLACEMENT_X/Y/Z = UNKNOWN)

ROTATION_RECOVERED =
NO

IMMEDIATE_886_SEMANTIC_ROLE =
MECHANICALLY_SIDS_STRING_TABLE_ENTRY_ID_S_GENERIC_CLEAR
(PUSH 0x376 @0x0059AB37 -> FUN_008F0780 -> store FUN_008F01C0; same resolution
chain as 4057); deeper semantics UNKNOWN

LANDMARK_TRACE_LEVEL =
0

QC_VERDICT =
QC_PASS_WITH_FINDINGS (0xP0, 0xP1, 1xP2, 5xP3 — F-P2-1 + F-P3-1..5; all
findings legitimate; ALL FIXED: QC repair round R1 + PE-MASTER-audit
finalization fix R2 (PM-F1 citation cell); verified from disk by the QC and by
PE-MASTER)

PE_MASTER_VERDICT =
MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION — PE_MASTER_STATUS =
PROVISIONAL_UNTIL_QUALIFIED, Q1 record absent; CANONICAL_GATE_EFFECT = NONE)
— the negative result is a full-value outcome per contract §31; verbatim
verdict persisted in 05_REPORT/PE_MASTER_REVIEW.md

NOT_CHECKED (summary) =
02_ANALYSIS/NOT_CHECKED.md N-01..N-16 (executor's honest record: other 4057
call-sites NOT searched; the landmark placement question as a whole; the sids
display layer; composite-key part-1 semantics; the [ESP+0xC8] owner's exact
class; executor-side independent RTTI chain walks; the deeper 0x008D-0x008F
family; whether model 218757 is a static building anywhere — untouched)
+ PE-MASTER coverage notes (05_REPORT/PE_MASTER_REVIEW.md COVERAGE): the
951/951 Ghidra-listing crosscheck re-execution (executor-internal; every
load-bearing instruction independently read from the physical file by
PE-MASTER; QC plausibility-checked); instruction-by-instruction decode of the
FUN_00821BB0/FUN_00821760 intermediate bodies (endpoints + singleton
disjointness + the global caller census close the load-bearing question at a
stronger level); the deeper 0x008D-0x008F family (bounded out by N-03, not
load-bearing).

MANIFEST_ROWS =
83  (every file in the package EXCEPT MANIFEST_SHA256.csv itself)

PHYSICAL_FILE_COUNT =
84  (83 covered + MANIFEST_SHA256.csv)

MANIFEST_SHA256 =
SELF-EXCLUDED FROM EMBEDDING (L12 precedent — this file is covered by
MANIFEST_SHA256.csv; a covered file cannot embed its covering manifest's final
hash without being stale by construction; a manifest cannot contain its own
hash). The literal SHA256 of the final MANIFEST_SHA256.csv is recorded in the
persistence worker's publication RETURN and is independently re-computable by
any re-hash of the package root.

BIJECTION (full re-hash of the physical package against the manifest; NO
sampling; verified at finalization):
MISSING = 0    EXTRA = 0    DUPLICATES = 0    SIZE_MISMATCH = 0
SHA256_MISMATCH = 0

COMMIT_PATH_CENSUS (at staging) =
exactly the package docs/audits/PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_
R1_20261003/ (all 84 files incl. MANIFEST_SHA256.csv) + AUDIT_ENTRYPOINT.md
(ONE appended LATEST RUNS row) = 85 staged paths total; the 5 foreign
untracked groups + experiments/ remain UNSTAGED; nothing else staged.

LOCAL_HEAD            = a4992788982f8ff7f59866fa46aad1176897c69d (at staging)
FETCHED_ORIGIN_MASTER = a4992788982f8ff7f59866fa46aad1176897c69d (at staging)
LIVE_REMOTE_HEAD      = a4992788982f8ff7f59866fa46aad1176897c69d (at staging;
  to be re-fetched and re-verified in the commit phase)
PUSH_VERIFIED         = NO (commit phase; at staging NO commit and NO push
  were performed — the commit + push execute only in the separate later phase
  after PE-MASTER's staged-state verification)

CANONICAL_GATE_EFFECT = NONE
M1_CLOSED             = NO
M2_AUTHORIZED         = NO
M3_AUTHORIZED         = NO
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP             = YES (pending, in order: PE-MASTER staged-state
  verification -> the single commit + push -> independent Desktop post-audit
  of the exact pushed SHA -> human decision; no other 4057 call-site search,
  no generalization to other statics, no next experiment designed or
  authorized — contract §31/§36 terminal)
```

## HANDOFF BLOCK (worker contract mapping)

```text
ASSIGNMENT_MODE      = FINALIZATION + STAGING (PERSIST_PUBLISH-equivalent
                       bounded to pre-commit persistence: verbatim verdict
                       persistence + documentation fix + reports + manifest +
                       path-limited stage; commit/push NOT in this phase)
PARENT_LOOP_ID       = PE-MASTER loop 18e522c6 (direct dispatch,
                       NO_NESTED_TASKS)
MILESTONE            = EU935-M1 — OPEN (unchanged)
SCOPE                = the run package + the single AUDIT_ENTRYPOINT.md row;
                       NOTHING ELSE (verified at staging)
QC_VERDICT           = QC_PASS_WITH_FINDINGS, all findings fixed (R1 + R2)
PE_MASTER_VERDICT    = MASTER_ACCEPTED (advisory; CANONICAL_GATE_EFFECT = NONE)
FINDINGS             = PM-F1 (P2, citation cell) FIXED in R2 — BEFORE/AFTER
                       SHA256 in 05_REPORT/AMEND_LOG_R2.md; PM-O1 (cosmetic)
                       NOTED, non-blocking
FINAL_REPORT_PATH    = docs/audits/PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_
                       R1_20261003/05_REPORT/FINAL_REPORT.md
GATES_PATH           = the run's hard gate is the falsifier certificate
                       (GATE_ID MANDATORY_FALSIFIER_4057_CALLSITE, EXECUTED,
                       FIRED S2), persisted verbatim in 05_REPORT/
                       PE_MASTER_REVIEW.md (mapped equivalent — this package
                       has no separate STAGE_ACCEPTANCE_GATES.csv file)
MANIFEST_PATH        = docs/audits/PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_
                       R1_20261003/MANIFEST_SHA256.csv
INPUT_AND_OUTPUT_HASHES =
  CLAIM_MATRIX.csv PM-F1: BEFORE E793E3887D2C96A78F7BCD95B1AB9025B8DE53886F6
  326794583AAE8F40604C8 -> AFTER 3323D054B4D5566248B91F8345A12DE6F67C8317CBB
  318F3BF7C472B85370CFA (revert-test verified: only the one cell changed)
  Created-file hashes: recorded in MANIFEST_SHA256.csv (83 rows) + AMEND_LOG_
  R2.md; MANIFEST_SHA256.csv's own hash: publication RETURN (self-exclusion)
FILES_CHANGED         = package: 02_ANALYSIS/CLAIM_MATRIX.csv (1 cell) +
  CREATED 05_REPORT/{FINAL_REPORT.md, HANDOFF.md, PE_MASTER_REVIEW.md,
  AMEND_LOG_R2.md} + MANIFEST_SHA256.csv; outside the package:
  AUDIT_ENTRYPOINT.md (+1 LATEST RUNS row at the top; every prior row
  byte-identical; CURRENT STATE untouched)
BASE_SHA              = a4992788982f8ff7f59866fa46aad1176897c69d
HEAD_SHA              = a4992788982f8ff7f59866fa46aad1176897c69d (unchanged at
                       staging; commit SHA appended at publication)
PUSH_STATUS           = NOT_PUSHED (this phase: staged only, by explicit order)
UNRELATED_WORK_EXCLUDED =
  the 5 known foreign untracked groups (4 foreign audit packages +
  experiments/) remain untracked and UNSTAGED; DRAFT_FINAL_REPORT.md,
  AMEND_LOG_R1.md, 00_CONTROL/, 01_RAW/, 03_SCRIPTS/, 04_QC/ untouched
NEXT_PARENT_ACTION    = PE-MASTER staged-state verification -> the single
                       publication commit + push phase -> HARD STOP ->
                       independent Desktop post-audit of the exact pushed SHA
                       -> human decision
```

END OF HANDOFF.
