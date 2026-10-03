# EXECUTION LOG — PHASE B (CORRECTIONS)

```text
RUN_ID = PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003
PHASE = B (CORRECTIONS), executor pe-reconstruction, dispatched by PE-MASTER
COUNTING_RULE = 00_CONTROL/CORRECTION_BUDGET.md §5 (1 explicit tool invocation = 1 tool call; failed calls count)
```

## 1. Phase B window and budget

```text
PHASE_B_WINDOW_START_UTC ≈ 2026-10-03T09:17Z (approximate — first Phase B tool call; the first UTC-stamped
  Phase B tool call was 2026-10-03T09:21:08Z)
PHASE_B_WINDOW_END_UTC = final verification call (see handoff; self-exclusion: this file cannot contain
  numbers produced after its own write)
TOOL_CALLS_USED_AS_OF_THIS_WRITE = 25 of MAX 65 (this write included)
PLANNED_FINAL_TOTAL = 26/65 (one final verification call follows: sizes/hashes of the 6 created files,
  git status re-check, HEAD re-check, end UTC)
WALL_MINUTES_AS_OF_THIS_WRITE ≈ 14 of MAX 95
NO_PARTIAL: all six authorized 01_ANALYSIS files are created by this write; no gate blocked; budget far under caps
```

Tool-call census (25 as of this write): 1-3 read 00_Control (AUTHORIZATION/CORRECTION_BUDGET/PREFLIGHT); 4-6 read AUTHORIZATION.md to EOF + historical RUN_PLAN.md + NOT_CHECKED.md; 7 failed rg anchor batch (counted per COUNTING_RULE; rg absent from this environment); 8 historical anchors via native Select-String + HEAD/porcelain check; 9 F-D3 source identity measurement; 10 C3_DECOMP.json recount; 11 E10 live-surface census; 12 session-store attempt call 1/5; 13 session-store attempt call 2/5; 14 historical anchor full-line extraction + first union decompilation recount; 15 session-store attempt call 3/5; 16 §8A recount fix (union, corrected address extraction); 17 session-store attempt call 4/5; 18 session-store attempt call 5/5; 19 01_ANALYSIS directory creation + package tree + UTC; 20-25 the six authorized writes (this file = call 25).

## 2. Measurements performed (the ONLY new physical measurements; all preregistered classes)

### 2.1 F-D3 — static source identity verification (class 1; measured 2026-10-03T09:21:53Z)

```text
EXISTS = YES
EXACT_PATH = D:\gamebyroengine\extracted\Gb12_Source\CoreLibs\NiMain\Win32\NiAVObject_Win32.cpp
FILE_SIZE_BYTES = 999
SHA256 = 75E452680D4B52D469EC69EF33C79CF94BF0F3E334250B8FAB3892077BF23FD4
FILE_MTIME_UTC = 2007-07-05T11:52:25Z
LINE_22 = void NiAVObject::UpdateWorldData() (the file's sole function, 32 lines; local→world transform propagation)
POST_AUDIT_SOURCE_CHECK = YES; MEASURED_DURING_CORRECTION = YES; ORACLE_MECHANISMS = 3 (unchanged)
```

### 2.2 §8A — decompilation records vs unique function entries (class 2 bounded recount of EXISTING artifacts; 2026-10-03T09:21:56Z + in-run fix)

```text
DECOMPILATION_RECORDS = 88
UNIQUE_FUNCTION_ENTRY = 87
duplicate pair = 006baa20 → C3:R10_other_006baa20 + C6:Y07_consumer_006baa20 (FUN_006baa20, confirmed)
per-file: C2=4, C3=17, C4=12, C5=12, C6=17, C7=12, C8=10, C11=4 (C10/C10v2/C12/C1/C9 have none)
C3_DECOMP.json ALONE = 17 records / 17 unique (the 88-record census spans the full raw C*.json set)
C2 records identified by code-signature fallback: D01→FUN_0072f580, D02→FUN_004c5580, D03→FUN_00726e70, D04→FUN_0070bf50
QC corroboration (historical artifact, read-only): 07_QC/raw/recheck/recheck4_decomp_integrity.json =
  {dump_files: 88, match: 88, mismatch: [], all_match: true}; decomp_dump contains exactly 88 .c files
hard limit 120 NOT demonstrated exceeded
```

Instrument-error disclosure (honest): the first union pass extracted addresses only from key-name suffixes, grouping the four C2 records (no address in key) under an empty key → intermediate UNIQUE=84; corrected in-run (same phase) by extracting the function entry from each record's decompiled-code signature → UNIQUE=87 with exactly one duplicate pair. Both passes are disclosed; the corrected result is the recorded one.

### 2.3 E10 live-surface census (class 2; grep census of live surfaces; measured 2026-10-03T09:21:57Z, BEFORE Phase B writes)

```text
FILES_SCANNED = 582 repo *.md (node_modules excluded)
PATTERN = slot-position|slot position|payload-derived|payload derived
CASE-SENSITIVE: 24 matching lines / 29 matches
CASE-INSENSITIVE: 25 matching lines / 30 matches
CLASSIFICATION → 01_ANALYSIS/CURRENT_CLAIM_STATE.md §8 (historical package = preserved artifacts, superseded;
  new 00_Control/AUTHORIZATION.md = quoted order text; NINODE_SLOT17 ×3, SF_ARG2 ×2, SCENEFEEDER ×1 = UNRELATED_SENSE
  (vtable slot alignment); AUDIT_ENTRYPOINT.md = 0 hits; all other live docs = 0 hits)
ACTIVE E10 POSITION/TRANSFORM SEMANTIC PROMOTIONS = 0
```

### 2.4 F-D4 session-store census attempt (class 3; EXACTLY 5 of 5 allowed calls; ~09:22-09:25Z)

```text
calls spent = 5/5 (cap reached; store work stopped)
pre-checked candidates (no store): C:\Users\User\.opencode = {agents, agents_removed_backup_2026-09-05,
  node_modules, skills} — NO storage dir; AppData\Local\opencode and AppData\Roaming\opencode = single config file each
store found (within the same bounded attempt): C:\Users\User\.local\share\opencode = {log, repos, snapshot,
  storage, tool-output} + opencode.db (SQLite; read-only URI-mode queries only; never written)
results (python 3.12.10 sqlite3; part rows with data JSON type='tool' per session):
  historical parent ses_eff65ce0dffehQR2H4VAoaJOIv ("Eksperyment PE_935 Placement Bridge", 2026-10-03T07:11:07Z)
  executor session ses_eff63660cffeJE8ariHPxOW4KQ (2026-10-03T07:13:45Z): 148 tool parts = 125 + 23 EXACTLY
  fresh QC ses_eff4f9ba2ffe54l7YQDmBq294P (2026-10-03T07:35:22Z): 109 — INDEPENDENTLY_RECOMPUTED (exact match)
  focused re-QC ses_eff40a7ffffex6TtoVQEAWrKmX (2026-10-03T07:51:42Z): 69 — INDEPENDENTLY_RECOMPUTED (exact match)
dispositions → 01_ANALYSIS/HISTORY_BUDGET_RECONCILIATION.md §3 (125/23 = INHERITED_FROM_DESKTOP_POST_AUDIT
  + machine-verified sum; 109/69 = RECOMPUTED_FROM_LOCAL_SESSION_STORE, exact matches)
temp probe scripts fd4_schema_probe.py / fd4_session_census.py were created OUTSIDE the package
  (C:\Users\User\AppData\Local\Temp\opencode\) and DELETED after use; no writer process remains
```

## 3. Explicit statement of what was NOT done

```text
NO other new measurements beyond sections 2.1-2.4 (the three preregistered classes).
NO new RE; NO Ghidra; NO client launch; NO runtime capture; NO new placement trace.
NO tracing of 4057 / 0x0059AB12 / 0x008D–0x008F family (the deferred lead is RECORD-ONLY — preserved verbatim in
  01_ANALYSIS/DEFERRED_PLACEMENT_LEADS.md; not executed, not repinned, not promoted).
NO XYZ search; NO parser extension; NO color decoders; NO new E10 consumer trace; NO fourth oracle mechanism.
NO promotion of any UNKNOWN; no invariant weakened.
HISTORICAL PACKAGE docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/ = UNTOUCHED
  (read-only; byte-preserved; verified: no tracked modification appears anywhere in the tree).
AUDIT_ENTRYPOINT.md = UNTOUCHED (not in Phase B's authorized output paths; the correction row belongs to a later phase).
NO stage, NO commit, NO push; HEAD unchanged = b151d428fc46818bc3b84d8ca000d92caa2cd76b
  (verified 2026-10-03T09:21:08Z: HEAD == b151d428…; porcelain = 6 untracked groups only, all expected:
  5 foreign untracked dirs + this new correction package dir; 0 tracked modifications; 0 staged; re-checked at
  the final verification call).
00_CONTROL of the new package = untouched by Phase B (frozen Phase A artifacts).
```

## 4. Deviations from the dispatch (honest)

1. `rg` is not installed in this environment: the anchor-verification batch (call 7) failed wholesale and was redone with native Select-String (failed call counted per COUNTING_RULE). Method difference disclosed in §2.3 (Select-String semantics; both case variants measured).
2. Session store: the three dispatch-pre-checked candidate roots contain no store; the actual per-session store was discovered at `C:\Users\User\.local\share\opencode` and queried (read-only) within the SAME bounded ≤5-call attempt (exactly 5/5 used). Two of the four Desktop census values were INDEPENDENTLY RECOMPUTED (exact matches: 109, 69); the executor values 125/23 remain INHERITED with a machine-verified sum constraint (148 = 125+23) — no fake measurement, no fake split.
3. Census count deviations vs the dispatch's stated expectations (honestly recorded): SF_ARG2 package = 2 matching lines (dispatch expected 1; lines 260 and 265, both vtable-slot-alignment sense → UNRELATED_SENSE); one additional case-insensitive-only hit in PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/00_CONTROL/RUN_CONTRACT.md:105 ("slot POSITION_TO_CALL" → UNRELATED_SENSE). Conclusion unchanged: ACTIVE E10 POSITION/TRANSFORM SEMANTIC PROMOTIONS = 0.
4. §8A locator precision: `01_RAW/C3_DECOMP.json` alone contains 17 records/17 unique; the expected 88/87 census spans the full historical 01_RAW C*.json record set (union recounted machine-wise; single duplicate pair confirmed as R10/Y07 = FUN_006baa20). Both facts recorded; no historical artifact was modified.
5. Phase B window start is approximate (≈09:17Z; first UTC-stamped call 09:21:08Z). Wall minutes are computed from the first Phase B tool call to the final verification call (reported in the handoff).
6. Console encoding artifacts (em-dash/≤ rendered as mojibake in some console grep outputs) were NOT propagated: all quotes in the package files are restored from the actual file content.
7. Self-exclusion: this file cannot contain its own SHA256 or the numbers of the final verification call; final numbers are reported in the Phase B handoff, and post-write sizes/hashes of all six files are measured by the final verification call (for the Phase D manifest).

## 5. Phase B handoff fields (reported to PE-MASTER)

```text
PHASE_B_STATUS = COMPLETE
CREATED_FILES = the six authorized 01_ANALYSIS files (sizes/SHA256 in the final verification call + handoff)
F-D1 = CORRECTED; F-D2 = CORRECTED; F-D3 = CORRECTED; F-D4 = CORRECTED_BY_HONEST_PROCESS_RECORD
INVARIANTS_UNCHANGED = YES
HISTORICAL_PACKAGE_UNTOUCHED = YES
ENTRYPOINT_UNTOUCHED = YES
HEAD = b151d428fc46818bc3b84d8ca000d92caa2cd76b
DEFERRED_LEAD_4057 = RECORDED_NOT_EXECUTED (candidate future experiment per order §11/§12 — carried in this handoff)
```
