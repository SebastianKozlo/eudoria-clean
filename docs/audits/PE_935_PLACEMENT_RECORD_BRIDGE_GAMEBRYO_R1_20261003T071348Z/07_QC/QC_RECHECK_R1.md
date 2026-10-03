# QC_RECHECK_R1 — FOCUSED RE-QC OF THE REPAIR ROUND — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

- REQC_RUN_ID: PE_935_PLACEMENT_RECORD_BRIDGE_RECHECK_R1_20261003
- AUDITED SCOPE: the executor's one repair round (AMEND-1..5 per
  06_REPORT/AMEND_LOG_R1.md) — NOT a re-audit of the run's science.
- MODE: fresh-context FOCUSED RE-QC (A1.6), artifacts-only, STATIC_ONLY,
  NO_NESTED_TASKS. This QC did not author any of the prior findings and did
  not modify any executor file. Outputs: this report +
  07_QC/raw/recheck/*.py|json (this QC's own instruments and raw results only).
- INPUT IDENTITIES (re-measured by this QC at start):
  - Entropia.exe SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31,
    8,015,872 B — MATCH (own re-hash).
  - Audit package = 40 executor-owned physical files (39 index rows + the
    index itself) + 07_QC/ (QC-owned).
  - Git baseline: HEAD = origin/master = live remote =
    743f9fac2dd5c9e94eaba074b46903b4d3686b46 (git ls-remote re-executed).

## RE_QC_VERDICT: **RE_QC_PASS**

(with 2 new P3 findings in AMEND_LOG_R1.md itself — documentation-precision
defects in the repair log, NOT defects in the repaired content; neither blocks
persistence. Details in section 8.)

Reason: all five corrections are physically present exactly as declared in the
AMEND_LOG AFTER quotes, and the corrected content is TRUE by this QC's own
independent measurements (own JSON parsing, own PE section mapper, own
decompile-structure slicing — no executor or QC-round-1 code reused). No file
outside the declared set of 4 (2 repaired + 1 new + 1 regenerated index)
carries a repair-round mtime; all load-bearing analysis data classes that QC
round 1 baselined (all 88 decompile bodies + all census data) are content-
identical to the pre-repair QC dumps; the current C9/C10V2 byte-pin data was
additionally re-verified physically true NOW (962/962 + 113/113 by this QC's
own mapper). All untouchable claims are present and unchanged. Package and
git state are exactly as expected for the persistence phase.

---

## 1. PER-AMEND VERIFICATION (text presence + own truth measurement)

Method: for each AMEND, (1) locate the corrected text in the current file and
byte-compare with the AMEND_LOG AFTER quote; (2) verify the truth of the
corrected content with this QC's own instrument (L9: independent source of
truth, non-circular; L13: report -> physical evidence -> independent check).

### AMEND-1 (P2-1, first occurrence) — PASS
- FILE/LOC: 06_REPORT/DRAFT_FINAL_REPORT.md lines 29-31.
- AFTER text present: YES — byte-exact match with the AMEND_LOG AFTER quote
  ("COVERAGE = own machine census: 45 = 19+10+4+8+4 census-target caller
  enumerations (C2=19, C4=10, C5=4, C6=8, C8=4; denominators reported per
  target in the C2/C4/C5/C6/C8 JSONs);").
- OWN TRUTH MEASUREMENT: recounted from the CURRENT 01_RAW JSONs with this
  QC's own parser (recheck_1): C2_CALLER_CENSUS.json measured.targets = 19
  keys (census_denominator field = 19); C4 census = 10 (K01..K10); C5 = 4
  (M01..M04); C6 = 8 (N01..N08); C8 = 4 (P01..P04). Sum = **45**; breakdown
  19+10+4+8+4 reconstructs exactly. The OLD figure/strings ("69",
  "19+10+8+4+4+8+4+12") do not reconstruct from any countable census
  structure in the package (negative control). Consistency: the same 45 now
  appears in DRAFT_FINAL COVERAGE + INDEPENDENT_CROSSCHECKS and in
  02_ANALYSIS/NOT_CHECKED.md line 65 ("45 census target lookups") — one
  package-wide figure (verified by grep).

### AMEND-2 (P2-1, second occurrence) — PASS
- FILE/LOC: 06_REPORT/DRAFT_FINAL_REPORT.md lines 118-119.
- AFTER text present: YES — byte-exact match ("INDEPENDENT_CROSSCHECKS = own
  census caller enumerations (45 target enumerations with denominators =
  19+10+4+8+4) vs the decompile chains; C1 file walk (own").
- OWN TRUTH MEASUREMENT: same recount basis as AMEND-1 — TRUE.

### AMEND-3 (P3-1) — PASS
- FILE/LOC: 02_ANALYSIS/TRACE_EDGE_BLOCKS.md line 333 (E9(a)).
- AFTER text present: YES — "FUN_005B6597: 68 D3 3E 00 00  PUSH 0x3ED3
  (16083) -> CALL FUN_005B5F90".
- OWN TRUTH MEASUREMENT (recheck_2, own PE section mapper — not the
  executor's, not QC-1's): VA 0x005B6597 -> RVA 0x1B6597 -> file offset
  1,795,479 (.text). Physical bytes: **68 D3 3E 00 00** + E8 EF F9 FF FF.
  PUSH imm32 = 0x003ED3 = **16083** (matches the prose); CALL rel32 =
  -1553 -> target **0x005B5F90** (matches). Uniqueness cross-check: exactly
  ONE `PUSH 0x3ED3` site in the whole .text (0x005B6597). Negative control:
  the pre-repair transcription "68 2D..." is NOT the physical byte sequence
  (byte[1] = 0xD3 != 0x2D). The C10V2 pin data already carried the correct
  value (raw_imm32 0x00003ED3, match=true) — re-confirmed in this QC's
  C10V2 re-verification (113/113 pins OK, incl. the 0x005B6597 record).

### AMEND-4 (P3-2, E9c) — PASS
- FILE/LOC: 02_ANALYSIS/TRACE_EDGE_BLOCKS.md lines 345-346 (E9(c)).
- AFTER text present: YES — byte-exact match ("...reads per-slot {u16@+0xC,
  float@+0x10} under flag 2, and for flag-1 slots: id2 from property
  machinery (Q05: class 20006...").
- OWN TRUTH MEASUREMENT (recheck_3, structural slice of the CURRENT
  01_RAW/C3_DECOMP.json R08 body, brace-matched branches):
  - The `else` branch of the outer `if (FUN_00745540(1) == '\0')` — i.e. the
    FUN_00745540(**1**) == TRUE path — contains the ENTIRE id2/lerp chain:
    FUN_00844660 (id2 property read) -> FUN_0043a550 (lazy-init) ->
    FUN_0072f580 (lookup) -> FUN_0072fce0 (valid gate) -> FUN_0072fe30
    (template list2 -> 3x vec3) -> FUN_00745690 (attr float) -> FUN_006c1f90
    (lerp) -> vec3 store (*puVar6/puVar6[1]/puVar6[2] via FUN_007333e0 slot
    getter). All 7 chain functions + _DAT_00a7b25c default present in that
    branch. VERDICT_flag1_id2_lerp_path = TRUE.
  - The nested `FUN_00745540(2)` branch contains ONLY the per-slot stores
    `*(uint *)(iVar4 + 0xc) = uVar9` and `*(float *)(iVar4 + 0x10) =
    local_68`, and NONE of the lookup/lerp chain functions.
    VERDICT_flag2_u16_float_stores = TRUE.
  - Supporting chain re-reads from the CURRENT package: Q05 body sets
    class literal 0x4e26 (=20006) and calls FUN_007376a0, whose body calls
    FUN_0070c180(**6**) — the corrected sentence's "class 20006 property tag
    6 via FUN_007376A0 / FUN_0070C180(6)" is accurate; W03 lerp body =
    out[i] = a[i] + t*(b[i]-a[i]); Q06 body = *(float*)(base + 0x1c +
    slot*4). Loop bound = 3 slots (`uVar10 < 3`).

### AMEND-5 (P3-2, E10) — PASS
- FILE/LOC: 02_ANALYSIS/TRACE_EDGE_BLOCKS.md line 399 (E10
  SELECTED_PATH_AND_REACHABILITY_PROOF).
- AFTER text present: YES — "flag-1 branch executes lookup -> FUN_0072FE30
  -> lerp -> store."
- OWN TRUTH MEASUREMENT: same R08 structural basis as AMEND-4 — TRUE.

All 5 AMEND line references in AMEND_LOG_R1.md (~line numbers) match the
actual locations (29-31, 118-119, 333, 345-346, 399).

## 2. INTEGRITY (file-level, pre-repair vs post-repair)

Baseline availability (L10/L12, honestly stated): the first QC round did
NOT persist full pre-repair hashes of the package files —
07_QC/raw/ARTIFACT_INDEX_CHECK.json stores only row counts and issue lists
(38/38 ok at that time), and no hash values. Therefore byte-identity vs
pre-repair is provable only where a pre-repair CONTENT baseline exists:
QC round 1's dumps (07_QC/raw/CENSUS_TARGETS_DUMP.txt, C2_TARGETS_DUMP.txt,
C2_STRUCTURE_DUMP.txt, and all 88 decomp_dump/*.c copies). For the remaining
files this QC used: repair-window mtime sweep + current-index rehash +
content-class corroboration (stated per file below). Unexpected change
policy per dispatch: any = P1. **None found.**

### CHANGED_EXPECTED (3) — exactly as declared in AMEND_LOG
- 06_REPORT/DRAFT_FINAL_REPORT.md — LastWriteTimeUtc 2026-10-03T07:50:06Z
  (original creation 07:33:41Z preserved = in-place edit, not delete+recreate).
- 02_ANALYSIS/TRACE_EDGE_BLOCKS.md — 07:50:12Z (creation 07:32:10Z).
- 06_REPORT/artifact_index.csv — 07:50:46Z (creation 07:34:17Z) — regenerated
  by design.

### NEW_EXPECTED (1)
- 06_REPORT/AMEND_LOG_R1.md — created+written 07:50:35Z.

### CHANGED_UNEXPECTED (0) / NEW_UNEXPECTED (0)
- mtime sweep over ALL 163 package files: every one of the other 36
  executor-owned files retains its original-run mtime window
  2026-10-03T07:14:16Z..07:34:14Z (run creation); QC-1's own files
  07:37:40Z..07:47:27Z; ONLY the 4 files above fall in the repair window
  07:50:06Z..07:50:46Z. Timeline is coherent: run -> QC-1 -> repair -> this
  re-QC (07:53Z+). (Caveat L1-style honesty: mtime is corroboration, not
  proof; the content-level checks below carry the weight.)

### Content-level integrity vs pre-repair baselines (QC-1 dumps)
- **All 88 decompile bodies** (C2 D01-D04, C3 R01-R17, C4 W01-W12, C5
  X01-X12, C6 Y01-Y17, C7 Z01-Z12, C8 Q01-Q10, C11 O01-O04): whitespace-
  insensitive comparison against the pre-repair decomp_dump copies ->
  **88/88 IDENTICAL, 0 mismatches** (recheck_4). The decompilation content of
  the 01_RAW JSONs is unchanged since QC round 1.
- **All census data**: C2's 19 targets (meta fields callsites /
  unique_callers / function_entry + FULL caller lists incl. per-caller
  callsite counts) and C4/C5/C6/C8's 26 census entries (same field set +
  caller lists) compared against the pre-repair dumps -> **0 mismatches**
  (recheck_1). The census data is unchanged since QC round 1.

### Physical-truth revalidation of the remaining byte-pin data (this QC, now)
- C9_LISTING_WINDOWS.json: all 20 windows re-compared against the physical
  EXE with THIS QC's own mapper + signed-hex normalization ->
  **962/962 instructions byte-identical, 0 mismatches**; independent rel32
  re-decode of CALL instructions inside the windows -> 112/112 target matches
  (recheck_9).
- C10V2_BYTE_CROSSCHECK.json: all 113 pin records (windows/call_targets/
  string_pin) re-checked against physical EXE bytes/offsets -> **113/113 OK**.
- So the package's claimed 962/962 and 113/113 hold for the CURRENT data by
  this QC's own instruments (QC-1 had verified the pre-repair data; the
  current data is both mtime-unchanged AND independently re-verified true).

### NOT_CHECKED (byte-identity vs pre-repair; no baseline exists on disk)
- 00_CONTROL (3 files), 01_RAW/{C1_CENSUS, C7_LISTS_AND_ATTACH,
  C10_BYTE_PINS, C12_NINODE_VTABLE_REPIN} (the other 9 01_RAW files are
  covered by the content baselines above; C9/C10V2 additionally re-proven
  physically true now), 02_ANALYSIS/{CLAIM_MATRIX.csv, NOT_CHECKED.md,
  RETRACTIONS_SUPERSESSIONS.md, SELECTION.md}, 03_SCRIPTS (13),
  04_CONTROLS/CONTROLS.md, 05_ORACLE/ORACLE_RECORDS.md,
  06_REPORT/HANDOFF.md.
- Reason: QC round 1 persisted only counts (ARTIFACT_INDEX_CHECK.json), not
  hashes (a manifest cannot re-serve as a pre-state hash list once the
  executor regenerates it; the old index file was overwritten by design).
- Mitigations applied instead: (a) zero repair-window mtimes on these files;
  (b) current artifact_index.csv rehash 39/39 OK; (c) the two repaired files
  were the only ones needing edits per AMEND_LOG, and every load-bearing
  claim QC-1 verified in the pre-repair DRAFT/TRACE is re-confirmed present
  and consistent in the current versions (section 6); (d) "68 2D" residue
  analysis confirms the pre-existing v1 instrument record (C10_BYTE_PINS)
  is the documented, intentional, unchanged v1 history (byte_match=false),
  not a repair-round edit. Residual risk (a timestamp-faked in-place edit of
  a baseline-less file) is assessed LOW and is disclosed here rather than
  converted into a positive result.

## 3. artifact_index.csv VERIFICATION — PASS

- Row count: **39** data rows (+ header) = 39 executor-owned files indexed;
  physical executor files (excluding 07_QC/) = **40** = 39 rows + the index
  itself (self-exclusion per contract; `phys_not_in_index` = exactly
  ["06_REPORT/artifact_index.csv"]).
- Schema: header = `relative_path,size_bytes,sha256` — stable, parses with
  utf-8-sig (UTF-8 BOM present, cosmetic); no malformed quoting, no merged
  rows, no duplicates (recheck_5).
- FULL rehash: **39/39 rows size+SHA256 match the disk** — 0 mismatches,
  0 missing files, 0 extra rows (L10: fresh recomputation, exact equality).
- 06_REPORT/AMEND_LOG_R1.md row: PRESENT (7,462 B,
  C5DC34C3D8EBD6C0FDE81BA026A9FAF5AD6C6D9916DAEC992D0F93B9B3E80022).
- 07_QC/ rows: **0** (correct — QC-owned; the whole-package final manifest is
  the publication phase's job, per HANDOFF/DRAFT_FINAL MANIFEST_* fields).
- The two repaired files carry their POST-repair hashes (TRACE 100C81BF...,
  DRAFT 2910289F...) consistent with the regeneration-by-design statement.

## 4. PAYLOAD DISCIPLINE — PASS (whole package incl. 07_QC/)

- 163 files censused (whole package incl. 07_QC and this re-QC's own
  outputs). Extensions present: .md 13, .json 26, .csv 2, .py 31, .txt 3,
  .c 88 — **zero** forbidden extensions (.exe/.dll/.vfs/.bnt/.bvi/.ark/.nif/
  .tga/.cpp/.h/.lib/... all absent) (recheck_8).
- Binary-content sniff: 0 suspects (every file is text).
- Embedded raw-payload dump check: 0 hex/base64 blobs > 2048 continuous
  chars; the hex present is short derived instruction/record extracts
  (allowed class).
- Gamebryo sources: NO Gb12_Source *.cpp/*.h file copies anywhere; the
  05_ORACLE records are locators + hashes + short quotes (QC-1 physically
  verified the quoted lines exist; not re-litigated — out of repair-round
  scope).
- Original corpora: no EXE/VFS/BNT/ARK/NIF payloads; EXE-derived content is
  instruction listings/extracts and decompilates (allowed derived evidence).
  Total package mass ~1.27 MB, all text.
- No violating file found.

## 5. RESIDUE SWEEP (whitespace-normalized; executor-owned files) — LIVE RESIDUE: 0

Numeric results (recheck_6; every hit listed with location):

| Phrase | Hits | Where |
|---|---|---|
| "69 census" | 1 | AMEND_LOG_R1.md:41 — documented BEFORE quote of AMEND-1 |
| "= 69" | 2 | AMEND_LOG_R1.md:41 (BEFORE quote); :145 (the log's own sweep-pattern description) |
| "68 2D" | 6 | AMEND_LOG_R1.md:22,83,89 (BEFORE/REASON quotes), :145 (sweep description); 01_RAW/C10_BYTE_PINS.json:217 (v1 pin record `expected_from_ghidra_listing:"68 2D 3E 00 00"` vs `actual_raw_exe_bytes:"68 D3 3E 00 00"`, byte_match=false); 03_SCRIPTS/c10_byte_pins.py:99 (as-executed v1 generator pin tuple) |
| "flag-2 slots" | 3 | AMEND_LOG_R1.md:105 (BEFORE), :116 (REASON), :145 (sweep description) |
| "flag-2 branch executes lookup" | 1 | AMEND_LOG_R1.md:128 (BEFORE quote of AMEND-5) |

Classification:
- ALL AMEND_LOG hits are the repair log's own BEFORE/REASON documentation —
  required by the log format (exact BEFORE/AFTER per entry) — not live
  residue.
- The two non-log "68 2D" occurrences are PRE-EXISTING, UNCHANGED (original
  mtimes 07:27:18/07:27:16Z), and intentional: the v1 pin record honestly
  documents the signed-hex transcription with byte_match=false (superseded by
  C10V2), and the v1 generator must remain as-executed (changing it would
  falsify provenance). QC-1's P3-1 correction was scoped to the E9(a) prose —
  which was fixed. These files must NOT be "cleaned".
- **Live residue of the corrected defects in current executor content: 0.**
- Additional negative control: the old breakdown string
  "19+10+8+4+4+8+4+12" occurs ONLY in the AMEND_LOG BEFORE quote (:41).

## 6. UNTOUCHABLE CLAIMS (Task 6) — ALL PRESENT AND CONSISTENT

Machine-verified in the CURRENT 06_REPORT/DRAFT_FINAL_REPORT.md (recheck_7):
RESULT_LEVEL = B (PARTIAL RESOURCE/SCENE CHAIN) ✓; MODEL_RESOURCE_EDGE =
CONFIRMED for record 4508 ✓; INSTANCE_IDENTITY world-instance identity from
a physical record NOT ESTABLISHED (CONTROL-2 FAIL -> UNKNOWN) ✓;
PERSISTENT_PLACEMENT_EDGE = NOT ESTABLISHED ✓; MODEL_ID_RECOVERED = YES ✓;
PLACEMENT_XYZ_RECOVERED = NO ✓; 962/962 (4 occurrences) ✓; 113/113 (4
occurrences) ✓; FUNCTIONS_DETAILED 88 (limit 120) (2 forms) ✓; 3/3 records +
3/3 oracle mechanisms ✓; corrected census figure present in both places
(COVERAGE + INDEPENDENT_CROSSCHECKS, "45 = 19+10+4+8+4") ✓; the
"C2/C4/C5/C6/C8 JSONs" denominators reference ✓. NONE of the repairs'
values were altered by the repair round; the package now carries ONE
consistent census figure (45), matching NOT_CHECKED.md line 65.

## 7. GIT / ENTRYPOINT — PASS

- HEAD = 743f9fac2dd5c9e94eaba074b46903b4d3686b46; origin/master = same;
  `git ls-remote --exit-code origin refs/heads/master` = same live value.
- `git diff --cached` = EMPTY (0 staged changes).
- `git status --porcelain`: ONLY the untracked audited package
  (docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/)
  + the foreign untracked groups exactly as predeclared
  (PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/,
  PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/, experiments/) —
  no tracked modifications, no staging, no commit, no push by the executor.
- AUDIT_ENTRYPOINT.md: tracked and clean (no modification).

## 8. FINDINGS OF THIS RE-QC (both new, both P3, both in AMEND_LOG_R1.md; neither blocks)

### P3-A — **AMEND_LOG_R1.md post-repair sweep statement over-claims "68 2D" absence**
- PATH/LINE: 06_REPORT/AMEND_LOG_R1.md:143-145 ("Grep sweep of the
  executor-owned files (00_CONTROL, 01_RAW, ... 06_REPORT): no remaining ...
  '68 2D' ... occurrences").
- COUNTER-EVIDENCE: this QC's whitespace-normalized sweep finds "68 2D" in
  TWO executor-owned files outside the repair log: 01_RAW/C10_BYTE_PINS.json
  line 217 (`"expected_from_ghidra_listing": "68 2D 3E 00 00"` — the v1
  pin's Ghidra-side expectation, paired with
  `"actual_raw_exe_bytes": "68 D3 3E 00 00"`, `"byte_match": false`) and
  03_SCRIPTS/c10_byte_pins.py line 99 (the as-executed v1 pin tuple).
  Both are pre-existing (original mtimes), legitimate, and protected
  instrument-history evidence that P3-1 never required changing — but they
  ARE remaining occurrences in executor-owned files, so the log's blanket
  "no remaining occurrences" is inaccurate as worded.
- MECHANISM: the executor's sweep evidently covered the corrected prose
  scope (or searched specific file classes) but the sentence claims the full
  file set it lists.
- BLAST RADIUS: none on the repairs, claims, gates, or raw evidence; purely
  a precision defect in the NEW log file's verification note. A future
  reader grepping "68 2D" per the log's claim would get 2 hits and could
  mistakenly infer an incomplete repair.
- NARROW CORRECTION (for PE-MASTER to authorize, since the one repair round
  is consumed — or ship as an erratum line in the publication commit):
  scope the sentence to the repaired prose/report files and note explicitly
  that "68 2D" intentionally remains only in the immutable v1 instrument
  record (byte_match=false, superseded by C10V2) and the as-executed v1
  generator pin tuple.
- REVALIDATION PREDICATE: grep "68 2D" over executor files returns exactly
  the 2 annotated instrument-history hits (both explained in the log or
  erratum) and 0 others outside AMEND_LOG quotes.

### P3-B — **AMEND_LOG_R1.md repair timestamp does not reconstruct from physical file mtimes**
- PATH/LINE: 06_REPORT/AMEND_LOG_R1.md:31 ("Repair UTC: 2026-10-03T09:04:00Z
  (measurements + edits + this log written in one round ...)").
- COUNTER-EVIDENCE: physical NTFS LastWriteTimeUtc of the repair edits:
  DRAFT_FINAL_REPORT.md 07:50:06Z, TRACE_EDGE_BLOCKS.md 07:50:12Z,
  AMEND_LOG_R1.md 07:50:35Z, artifact_index.csv 07:50:46Z — a coherent
  40-second edit window. No file in the package was written at/near 09:04Z.
  The machine timezone is UTC-7 (Pacific), so 09:04 local would be 16:04Z —
  no local/UTC reinterpretation produces 09:04Z. All other package
  timestamps are UTC-coherent (run ID 07:13:48Z -> first files 07:14:16Z;
  QC-1 raw files 07:37-07:45Z; QC_AUDIT_R1.md 07:47:27Z).
- MECHANISM: most plausibly a projected/pre-written stamp never updated, or
  a transcription slip; the declared "one round" content itself is
  verified TRUE (all 5 corrections + index + log are physically present and
  correct).
- BLAST RADIUS: provenance metadata precision only; no science, claim, gate,
  or evidence impact.
- NARROW CORRECTION: at publication, correct/annotate the stamp to the
  physical window (2026-10-03T07:50:06Z..07:50:46Z) or mark it as a declared
  (not measured) planning timestamp.
- REVALIDATION PREDICATE: the log's timestamp field is consistent with file
  mtimes or explicitly labeled declared-not-measured.

### Observation (no finding)
- QC-1's optional P3-3 method note (T10 census 817 Ghidra vs 808 raw) was
  NOT added — consistent with the repair round's declared scope (it was
  explicitly optional/"not required for closure"); the C2 T10 record retains
  817/367 as the Ghidra-side census with QC-1's method note living in
  QC_AUDIT_R1.md P3-3.

## 9. COVERAGE OF THIS RE-QC (explicit; L11 coverage algebra)

FULL_READ (to EOF):
- 06_REPORT/AMEND_LOG_R1.md (160 lines); 06_REPORT/DRAFT_FINAL_REPORT.md
  (238 lines); 02_ANALYSIS/TRACE_EDGE_BLOCKS.md (465 lines);
  06_REPORT/artifact_index.csv (all 39 rows + header);
  07_QC/QC_AUDIT_R1.md (436 lines — the designated raw-data source for the
  first-round findings); 07_QC/raw/{ARTIFACT_INDEX_CHECK.json,
  C2_STRUCTURE_DUMP.txt, CENSUS_TARGETS_DUMP.txt, QC_DERIVATIONS4.json,
  QC_DERIVATIONS5.json}; the R08, Q05, Q06, W03 decompile bodies; the C2/C4/
  C5/C6/C8 census structures (19 + 26 entries, meta + full caller lists).
- TOTAL executor package files = 40; of these: 2 repaired files + AMEND_LOG +
  artifact_index.csv read fully; 01_RAW census+decompile content (8 files'
  data classes) machine-compared to pre-repair baselines; C9 + C10V2
  physically re-verified instruction-by-instruction (962 + 113 records).

BOUNDED_INSPECTION:
- 07_QC/raw/C2_TARGETS_DUMP.txt: structure + all 19 target meta lines; the
  T10 367-entry caller list at head-sample level (not load-bearing — QC-1
  P3-3 note).
- 07_QC/raw/decomp_dump/*.c: machine-compared as baselines (whitespace-
  insensitive), not re-read line-by-line as prose.
- 00_CONTROL/, 04_CONTROLS/, 05_ORACLE/, 02_ANALYSIS prose files,
  06_REPORT/HANDOFF.md, 03_SCRIPTS/: NOT re-read in full in this re-QC
  (they were QC-1's FULL_READ scope; this round re-checked their identity
  via mtime + index rehash; none is implicated by any repair).

NOT_CHECKED (with reasons — see also section 2):
- Byte-identity vs pre-repair for the 24 executor files with no persisted
  pre-repair content baseline (list in section 2) — first QC round stored
  counts, not hashes. Mitigations + residual risk stated there.
- Physical re-walks of templates.vfs / 20002.vfs / Models.bnt / NiMain.lib
  oracle: NOT re-executed (STATIC bounded re-QC; QC-1 re-derived all of
  them physically; none is implicated by any repair; EXE identity re-hashed
  by this QC at start).
- Ghidra re-decompilation: not re-run (STATIC_ONLY; same bound as QC-1; the
  decompile bodies' underlying listing windows are byte-verified against the
  EXE by this QC's own mapper instead — 962/962).
- The executor's OWN pre-edit verification runs (its recount/re-read): not
  re-executed as such; instead every corrected fact was re-derived
  independently by this QC (non-circular).

QC RAW EVIDENCE (this re-QC): 07_QC/raw/recheck/ — recheck_1_census45.py,
recheck_2_byte_va.py, recheck_3_r08_flags.py, recheck_4_decomp_integrity.py,
recheck_5_index.py, recheck_6_residue.py, recheck_7_claims.py,
recheck_8_payload.py, recheck_9_physical_c9.py + result JSONs
(recheck1..recheck9_*.json). All are this QC's own instruments; no executor
or QC-1 code was executed or reused.

## 10. RECOMMENDATION TO PE-MASTER

**Proceed to persistence.** The repair round is verified: all five
corrections present and TRUE by independent measurement; no unexpected file
changes; index, payload discipline, residue (live = 0), untouchable claims
and git state all as expected. QC round 1's QC_PASS_WITH_FINDINGS verdict
now stands with P2-1/P3-1/P3-2 CLOSED (P3-3 remains an optional note, no
action).

Two new P3 findings live in the repair log itself (P3-A sweep over-claim,
P3-B timestamp) — both documentation-precision items with zero science
impact. Options: (a) authorize one bounded wording amendment of
AMEND_LOG_R1.md (2 lines) before persistence, or (b) persist as-is and
carry both as an erratum note in the publication commit / final manifest.
This QC has no blocking objection to either; option (a) is cleaner if a
further executor touch is acceptable, option (b) if zero-touch persistence
is preferred.

```text
RE_QC_VERDICT = RE_QC_PASS
AMEND-1..5 = ALL PASS (present + true by independent measurement)
INTEGRITY = CHANGED_EXPECTED 3 (DRAFT_FINAL_REPORT.md, TRACE_EDGE_BLOCKS.md,
  artifact_index.csv) + NEW_EXPECTED 1 (AMEND_LOG_R1.md) + UNCHANGED 36
  (mtime-corroborated; census + all 88 decompile bodies content-proven
  unchanged vs pre-repair; C9/C10V2 physically re-verified 962/962 + 113/113)
  + CHANGED_UNEXPECTED 0
ARTIFACT_INDEX = 39 rows, 39/39 rehash OK, AMEND_LOG row present, 0 QC rows,
  self-excluded (40 executor files total)
PAYLOAD_DISCIPLINE = PASS (0 violations, whole package incl. 07_QC)
RESIDUE = live residue 0 (all hits are AMEND_LOG BEFORE/REASON documentation
  or protected pre-existing v1 instrument history)
UNTOUCHABLE CLAIMS = ALL PRESENT/CONSISTENT
GIT = HEAD == origin/master == live remote == 743f9fac...; cached diff empty;
  status = untracked package + declared foreign groups only; ENTRYPOINT clean
NEW FINDINGS = P3-A (AMEND_LOG:143-145 sweep over-claim "68 2D"),
  P3-B (AMEND_LOG:31 repair timestamp 09:04:00Z vs physical 07:50Z window)
NEXT_PARENT_ACTION = proceed to persistence (optionally after one bounded
  AMEND_LOG_R1.md wording amendment, or with both P3s as erratum notes)
```
