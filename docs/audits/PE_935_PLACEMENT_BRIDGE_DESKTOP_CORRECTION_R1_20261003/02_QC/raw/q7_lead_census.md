QC-F7 RAW — deferred placement lead (4057/218757/0x0059AB12/886) preserved-only verification
DATE = 2026-10-03 (UTC) | INSTRUMENT = package-wide content grep + full reads + package tree census

## 1. Package tree census (my own listing)
The new package contains EXACTLY 9 files (3 x 00_CONTROL, 6 x 01_ANALYSIS) + this QC's own 02_QC/raw outputs.
NO Ghidra artifacts, NO decompilation dumps, NO EXE scans, NO new trace/XYZ artifacts anywhere in the package. ✓

## 2. Package-wide grep for 4057|218757|218758|59AB12|0x008D|886 — hit classification
- 00_CONTROL/AUTHORIZATION.md — ALL hits are the VERBATIM human order: ss0 unauthorized list (139-141),
  ss11 deferred-lead block (975-1109), ss12 candidate experiment (1121-1265), ss13 QC scope (1278),
  ss15 entrypoint row spec (1423, 1537), ss20 final report fields (1878-1890, 2010-2012), ss22 hard stop
  (2060-2083), scope summaries (2110-2128). Contract text — not promotion. ✓
- 01_ANALYSIS/DEFERRED_PLACEMENT_LEADS.md — the authorized preservation record (ss1 lead, ss2 not-repinned
  note, ss3 human context, ss4 epistemic status block, ss5 do-not-execute guard, ss6 candidate experiment
  DESIGN ONLY + mandatory falsifier + 12-step ladder + 886 unknown + success thresholds, ss7 disposition). ✓
- 01_ANALYSIS/EXECUTION_LOG.md — ONLY the negatives (ss3: "NO tracing of 4057 / 0x0059AB12 / 0x008D-0x008F
  family... not executed, not repinned, not promoted") and the handoff field DEFERRED_LEAD_4057 =
  RECORDED_NOT_EXECUTED. ✓
- CURRENT_CLAIM_STATE.md / DESKTOP_FINDINGS.md / CORRECTION_MATRIX.csv — ZERO 4057/218757/59AB12 hits. ✓
NO occurrence promotes any lead status beyond the order ss11 block.

## 3. Epistemic status block (DEFERRED_PLACEMENT_LEADS.md ss4 vs order ss11 — verbatim comparison)
4057_EXISTS_AS_TEMPLATE_ID = LOCAL_LEAD / TO_BE_REPINNED ✓
4057_TO_A218757_MAPPING = LOCAL_LEAD / TO_BE_REPINNED ✓
B218758_COLLISION_MAPPING = LOCAL_LEAD / TO_BE_REPINNED ✓
IMMEDIATE_4057_AT_0x0059AB12 = LOCAL_LEAD / TO_BE_REPINNED ✓
IMMEDIATE_4057_IS_TEMPLATE_ID = UNVERIFIED ✓   (NOT promoted)
HARDCODED_TEMPLATE_REFERENCE_4057 = UNVERIFIED ✓
CLIENT_CONSTRUCTS_MODEL_218757_HERE = UNVERIFIED ✓
STATIC_BUILDING_INSTANCE = UNVERIFIED ✓
STATIC_LANDMARK_CONSTRUCTION_PATH = UNVERIFIED ✓
WORLD_TRANSFORM_SOURCE = UNKNOWN ✓
PLACEMENT_XYZ = UNKNOWN ✓
IMMEDIATE_886_SEMANTIC_ROLE = UNKNOWN ✓
→ ALL statuses preserved EXACTLY as the order ss11 block; NONE promoted.

## 4. Candidate experiment (ss12) — preserved, NOT executed
CANDIDATE_RUN_TITLE = PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1 ✓
AUTHORIZATION_STATUS = NOT_AUTHORIZED ✓
Anchor VA 0x0059AB12 / candidate raw immediate 4057 ✓
Primary question verbatim ✓
Mandatory falsifier verbatim: "If immediate 4057 does NOT reach FUN_0072F580 or another independently proven
template-id consumer, the numeric equality with templates.vfs id2=4057 must be treated as coincidental and
the lead rejected." ✓
12-step future proof ladder verbatim ✓ ; 886 = OBSERVED_LOCAL_LEAD / FINAL_SEMANTIC_ROLE = UNKNOWN,
no guessing ✓ ; success thresholds verbatim ✓ ; NEXT_4057_EXPERIMENT_AUTHORIZED = NO ✓

## 5. Earlier local claims NOT repinned
"218757.nif exists in Models.bnt" / "218758.bvi exists in Volumes.bnt" recorded ONLY as
LOCAL_LEAD_TO_BE_REPINNED_IN_FUTURE_AUTHORIZED_RUN ✓ (no repin, no promotion)

## 6. No-RE verification
- EXECUTION_LOG ss3 lists the full negatives (no Ghidra at 0x0059AB12, no containing-function decompile,
  no callee trace, no 0x008D-0x008F scan, no EXE rescan, no XYZ/similar-immediate search, no 886 guessing,
  no 4057-is-template-ID proof attempts, no 4057-registry or 218757-runtime connection attempts) ✓
- The ONLY binary/source touch in Phase B was the authorized F-D3 measurement of NiAVObject_Win32.cpp
  (a source file identity check — not the EXE, not the lead's addresses) ✓
- Package artifact census (section 1) confirms no RE products exist ✓
- My Q2 verification used ONLY pre-existing historical raw evidence; no new RE ✓

CONCLUSION: Q7 = PRESERVED-ONLY CONFIRMED. The lead is recorded exclusively as an unverified future lead;
no RE was performed; no status promoted; the candidate run is NOT executed and NOT authorized.
