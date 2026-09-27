# AMEND_LOG_R1 — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926

**Batch**: AMEND_R1 (bounded correction batch). **Dispatcher**: PE-MASTER (direct
dispatch, NO_NESTED_TASKS). **Executor**: pe-reconstruction. **Date**: 2026-09-26.
**Scope**: EXACTLY the 7 confirmed QC P3 findings of the fresh INTERNAL_QC
(fresh-context pe-master-auditor, READ-ONLY: QC_PASS_WITH_FINDINGS — 0×P0/P1/P2,
7×P3, all confirmed by PE-MASTER) + the manifest regeneration + the single
AUDIT_ENTRYPOINT.md verdict-cell edit. NOTHING else changed. STATIC-ONLY (no
client/GPU/physical-console experiment; the only executed code = this package's
own probes over pinned static inputs). PRE-PERSISTENCE preserved: NO git add /
commit / push / staging; HEAD before == after ==
`cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d`. Historical packages and raw evidence
untouched (the historical trace CSV/.pml READ-ONLY: SHA re-verified
2BFA1F7C71EED9AD74098D4E078FDD06F265E87C8764067A0359F8E006ED2BE8, byte-identical).

Method notes for every byte-level fix below: all mojibake/BOM findings were made
by BYTE inspection (byte-pattern scan over all package files), never by console
rendering; every replacement was executed with strict expected-count assertions;
every re-run output was byte-diffed against the pre-amend snapshot.

---

## ITEM 1 — QC-P3-1: HANDOFF numstats (06_REPORT/HANDOFF_TO_DESKTOP_REAUDIT.md)

- **Reason**: QC P3 ref QC-P3-1 (HANDOFF diff statistics were wrong vs the true
  `git diff --numstat`).
- **Before** (GIT STATE section): "AUDIT_ENTRYPOINT.md (+1 row only),
  src/pesource/VegetationClimateDecoder.js (+36/-6 comment-only),
  src/peworld/PEFoliageCore.js (+25/-11 comment-only)."
- **After**: "AUDIT_ENTRYPOINT.md (+1/-0: one new row only),
  src/pesource/VegetationClimateDecoder.js (+30/-6 comment-only),
  src/peworld/PEFoliageCore.js (+20/-5 comment + one documentation-metadata
  string)." — verified against live `git diff --numstat` output captured for this
  batch: `1 0 AUDIT_ENTRYPOINT.md`, `30 6 src/pesource/VegetationClimateDecoder.js`,
  `20 5 src/peworld/PEFoliageCore.js` (re-verified again AFTER the item-8
  entrypoint-cell edit: still 1/0 — the whole entrypoint row was ADDED by the
  original run, so a within-line cell edit keeps the vs-HEAD delta at 1
  insertion / 0 deletions).

## ITEM 2 — QC-P3-2: DIFF patches byte-exactness (03_EVIDENCE/DIFF_*.patch)

- **Reason**: QC P3 ref QC-P3-2 (the stored patches were NOT byte-identical to the
  actual `git diff` output: BOM + mojibake).
- **Generator method**: `node:child_process.execSync('git diff -- <path>')` with
  RAW stdout bytes written directly by Node fs.writeFileSync — no PowerShell
  pipe, no console decoding, no re-encoding (the original capture chain —
  PowerShell stdout with a non-UTF-8 console code page — was the mojibake/BOM
  source).
- **Before**: DIFF_VegetationClimateDecoder.js.patch = 3,464 B, BOM present,
  6× cp437-roundtrip em-dash (`cp437-roundtrip glyph sequence` = stored bytes CE 93 C3 87 C3 B6), SHA256
  c585bd14791986db556e7bb47addcc8f72bd0a05a2f8771b332ffc4c4a6c2953c.
  DIFF_PEFoliageCore.js.patch = 3,445 B, BOM present, 7× cp437-roundtrip
  em-dash, SHA256 b0fa06cddc901abc342e634df0d8036afb597ed160dc49527af244974e5e81fc.
- **After**: regenerated from raw `git diff` output.
  DIFF_VegetationClimateDecoder.js.patch = 3,389 B, SHA256
  5978ff6b3cd9c787284b829e59d8cccf18d14d0fa956b6d760d86c4278728723.
  DIFF_PEFoliageCore.js.patch = 3,377 B, SHA256
  27dee19810fded98fbe37e2013b742da500bcd107ad0c85feafbccdbf1ea96dd.
- **Byte-identity VERIFICATION method** (recorded as required): the regeneration
  script captured `git diff -- <path>` TWICE independently (fresh child process
  each time) and hashed (a) capture #1, (b) capture #2, (c) the file on disk
  after write. Three-way hash equality = byte-identity of the stored patch vs the
  actual git diff bytes: BOTH patches `byte_identical: true` (capture_hash ==
  refetch_hash == file_hash). Encoding invariants verified on the captured bytes:
  BOM=false, first CR byte offset=-1 (LF-only line endings), mojibake=false,
  true em-dash U+2014 (E2 80 94) counts = 6 and 7 (exactly matching the 6/7
  mojibake occurrences they replace — the context lines' true em-dashes restored).
  The MODIFIED_PATHS.csv / EVIDENCE_INDEX.csv "byte-exact" labels are now TRUE.

## ITEM 3 — QC-P3-3: mojibake + BOM normalization (BYTE-WISE, not visual)

- **Reason**: QC P3 ref QC-P3-3. Systematic byte-pattern scan of ALL package
  files (stored-byte evidence only, no console-render inference) for: UTF-8 BOM
  (EF BB BF); cp1252-roundtrip em-dash ("cp1252-roundtrip glyph sequence" stored as UTF-8 = C3 A2 E2 82 AC E2
  80 9D); cp437-roundtrip em-dash ("cp437-roundtrip glyph sequence" stored as UTF-8 = CE 93 C3 87 C3 B6);
  the latin1-double and en-dash roundtrip classes; raw en-dash E2 80 93
  (adjudication flag); U+FFFD; double-roundtrip NBSP class.
- **Scan result (46 files scanned)**: BOM in exactly 6 files (matching QC);
  REAL stored mojibake in exactly 5 files (the 2 DIFF patches, SELFADV json,
  r1_f02_vcl_census.mjs, F02_VCL_CENSUS.json). NO en-dash hits, NO U+FFFD, NO
  latin1-double/NBSP-class hits anywhere. IMPORTANT adjudication: the QC-suspect
  CSVs GATE_REVALIDATION.csv (8 true U+2014), RETRACTION_SUPERSESSION_DELTA.csv
  (4) and STAGE_ACCEPTANCE_GATES.csv (7) are BYTE-CLEAN — their em-dashes are
  TRUE U+2014 (E2 80 94); the QC saw console-render artifacts, so per the
  instruction ("if the byte-scan confirms them") those three files were NOT
  modified.
- **Fixes applied** (each with strict expected-count assertions):
  1. **03_EVIDENCE/scripts/r1_f02_vcl_census.mjs**: UTF-8 BOM stripped + 5
     stored cp1252-roundtrip em-dashes (byte offsets 28, 919, 4487, 5816, 7199 =
     4 comment lines + the numberBehavior.note string literal at line ~154)
     normalized to true U+2014. 10,245 B → 10,217 B; SHA256
     f8ef739a567623e85f896b32962907ae555bd51deb5d146faff6711b7137437d →
     f056c448666a196bd9547bd080c725ab92921dffc4220bea79dae9a8964b4c2d.
  2. **03_EVIDENCE/F02_VCL_CENSUS.json** (re-run, not hand-edited): after the
     script fix, the probe was re-executed (node v22.22.0; BNT re-hashed
     7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4 = pin MATCH).
     **Diff verification vs the pre-amend snapshot (structural walk of both
     JSONs): EXACTLY 1 differing path** — `number_runtime_behavior.note` (old
     contained the mojibake sequence â€"/U+00E2,U+20AC,U+201D; new contains true
     U+2014). ALL counts identical: 32 files / 492 nonempty lines / 5,916 tokens /
     493 groups of 12 / 31 successes / 1 failure / 472 records / 6 bad tokens /
     256→246 ids / 10 lost; cross_check_vs_desktop_claims ALL MATCH
     (desktop_492_lines / desktop_493_groups / desktop_31_successes_1_failure /
     desktop_472_records / desktop_first_bad_token_offset_447 /
     desktop_bad_files_25vcl_only). 21,156 B → 21,151 B; SHA256
     5ef724cf58a250bc32f118a9b17371d8cabf10e582d84cfee25d578ad4519655 →
     b67e1fc41820cdc165fb8033abca0a035cd23f7838623e166534527b6fe7093d.
  3. **03_EVIDENCE/SELFADV_DECODER_CONTROLS.json** (re-captured by executing the
     decoder again, per the instruction): the self-adversarial probe
     r1_selfadversarial_decoder_controls.mjs re-run with BYTE-FAITHFUL stdout
     capture (cmd /c raw redirect — no PowerShell stdout decoding). Line-level
     diff vs pre-amend: EXACTLY 3 differing lines = (L1) BOM removed, (L13/L19)
     the two decoder-exception texts cp437-roundtrip glyph sequence → true U+2014. All 4 control cases /
     expected values / pass flags identical (all_pass=true; node v22.22.0).
     **Byte-faithfulness of the recorded exception verified against the real
     decodeVclPayload throw messages**: the decoder source's two throw literals
     contain true U+2014 at exactly the recorded positions ("col ${c} " + U+2014 +
     " LOUD (the engine stream would fail here too)"; "${VCL_VALUES_PER_RECORD} " +
     U+2014 + " trailing partial record, LOUD") — the re-captured JSON now stores
     the same E2 80 94 bytes (2 true em-dashes, 0 mojibake, 0 BOM, LF-only).
     879 B → 839 B; SHA256
     cf38b559c23b91bc9a9b7589d436fb0683e48437d7abf1384f39144e4c7af59f →
     416febb8a2717c496e3be02d16286e1d0ea527314174816e93689defcda656b3.
  4. **03_EVIDENCE/scripts/r1_iter032k_RUN_COPY.py**: UTF-8 BOM stripped
     (7,112 B → 7,109 B; SHA256
     8ac2e6ebed70ed312b48d7b487a848bb388c207c9a65027a78278847371793be →
     6dc0067d13e8e60de36aef7478ddb64f123ab55f5499ed8a1ae14a76604d7cbb).
     **Post-fix verification**: the RUN copy now differs from the VERBATIM copy
     (historical original, SHA 202FE509... unchanged) in EXACTLY ONE line (line
     16 = the OUT redirect line) — the package's "byte-identical to the
     historical original EXCEPT the single OUT line" claim is NOW TRUE (the BOM
     had silently violated it; python utf-8-sig tolerated the BOM at execution
     time, so the recorded re-run results were never affected). Consequential
     stale-SHA text references updated: 02_ANALYSIS/F02_VCL_CORPUS_DECODER_
     REVALIDATION.md §2 ("run copy SHA256 8AC2E6EB..." → "6DC0067D..." with an
     AMEND_R1 QC-P3-3 note) and 03_EVIDENCE/EVIDENCE_INDEX.csv (the
     F02_ITER032K_RERUN row's generator field, same correction + explanation).
  5. **03_EVIDENCE/scripts/r1_selfadversarial_decoder_controls.mjs**: UTF-8 BOM
     stripped (2,129 B → 2,126 B; SHA256
     3f3fdd6f141c1fdd8fe1f990a3267e7110e8de128a1c07a4a7079e63f19d6c1a →
     8ab79918c4f0eebb40ca31b054a5867e56c1a973e967a6bac6663d77c87bda52).
     No mojibake in this file (its source was clean; the mangling was in the
     stdout capture chain — see item 3.3).
  6. **The 2 DIFF patches** — covered by ITEM 2 (regeneration fixes their BOM +
     mojibake).

## ITEM 4 — QC-P3-4: trace-row delta ROOT CAUSE (upgraded to a root-caused erratum)

- **Reason**: QC P3 ref QC-P3-4 (the 282,192-vs-282,059 total-row delta was
  disclosed-but-unexplained).
- **Independent re-derivation (this executor's own byte-level probe, per the
  instruction)**: NEW probe 03_EVIDENCE/scripts/r1_amend_f01_trace_linecount.mjs
  (node v22.22.0) → NEW evidence
  03_EVIDENCE/F01_TRACE_LINECOUNT_ERRATUM.json. Source =
  99_Audits/PE_M1_X87CW_AUTOMATION_R1_20260905_140126/04_Runtime/live_test/
  entropia_death_trace.csv — READ-ONLY; re-hashed 50,053,186 B, SHA256
  2BFA1F7C71EED9AD74098D4E078FDD06F265E87C8764067A0359F8E006ED2BE8 (SOURCE_INDEX
  pin MATCH). **Measured: LF bytes = 282,060; CR bytes total = 282,193; CRLF
  pairs = 282,060; LONE CR bytes (CR NOT followed by LF, embedded inside quoted
  Detail fields) = 133; LFs not preceded by CR = 0; leading UTF-8 BOM present
  (the trace's own first bytes); final two bytes 0D 0A.** Cross-check vs
  PE-MASTER's independent counts (LF 282,060 / lone CR 133): BOTH MATCH.
- **Adjudication recorded in the erratum JSON**: 282,060 LF-terminated lines =
  header + **282,059 data rows — the HISTORICAL QUOTE IS CORRECT** (independently
  confirmed twice: the LF convention AND a quote-aware RFC4180 parse of the same
  bytes returning 282,059 data rows with 0 rows of wrong field count). 282,192 =
  the CR-sensitive line-counting artifact (282,060 + 133 = 282,193 counted lines
  → 282,192 "data rows") — exactly the number this run's original F01 line reader
  reported. The 133-row delta is a LINE-COUNTING ARTIFACT, NOT a data discrepancy.
  **Per-client load-bearing facts re-derived under the CR-correct parse and
  UNAFFECTED**: exactly 1 distinct Entropia.exe PID (12976); 2,193 Entropia.exe
  rows; exactly ONE Entropia.exe Process Exit row ("Exit Status: -1"); ZERO
  ddraw/d3d8/d3d9 Load Image rows; 77 Entropia.exe Load Image rows; d3dx9_30 x2
  (the pre-amend F01 wording "77 Load Image rows total" is the Entropia.exe scope;
  the all-process total is 129 — recorded both in the erratum JSON).
- **Doc updates (the three enumerated locations)**:
  - **02_ANALYSIS/F01_PRIMARY_DEVICE_REVALIDATION.md §5.2.B**: the "HONEST DELTA
    vs the historical record ... delta (133) is recorded, not forced" note
    replaced by the ROOT-CAUSED statement (historical 282,059 CORRECT; 282,192 =
    CR-splitting artifact; per-client facts 1 PID / 2,193 rows / one
    Exit Status: -1 / 0 ddraw-d3d8-d3d9 loads UNAFFECTED; pointer to
    F01_TRACE_LINECOUNT_ERRATUM.json; the live_test_record.json pid provenance
    note preserved verbatim).
  - **06_REPORT/GATEC_FINDINGS_REVALIDATION_REPORT.md §11**: the NOT_CHECKED
    entry "total-row count differs ... delta 133 recorded, not forced" replaced
    by the root-caused statement (282,192 = CR-sensitive count incl. 133 embedded
    lone CRs; 282,059 = the correct LF data-row count — the N-2 historical quote
    STANDS; byte census LF = 282,060 / lone CR = 133 both MATCH PE-MASTER's
    independent counts; quote-aware parse returns 282,059).
  - **02_ANALYSIS/SELF_ADVERSARIAL_PASS.md NOT_CHECKED list**: the corresponding
    line upgraded from "delta 133 recorded, not forced" to the root-caused
    statement.
- **NOT touched**: the historical .pml/CSV trace evidence (read-only; SHA
  re-verified unchanged).

## ITEM 5 — QC-P3-5: CSV schema normalization (01_RAW CSVs)

- **Reason**: QC P3 ref QC-P3-5.
- **RETRACTION_SUPERSESSION_DELTA.csv**: strict field-count parse confirmed the
  6 NEW-* edges carried 7 fields against the 8-column header (edge_id, edge_type,
  old_claim, counterexample_or_basis, correction, current_disposition,
  dependent_fields, preservation_note); the 9 PRIOR rows had 8. BYTE-LEVEL
  column-content analysis of each NEW row shows field 6 contains
  DEPENDENT-FIELDS content and field 7 contains PRESERVATION-NOTE content — the
  missing column is **current_disposition**. Repair: an evidence-accurate
  current_disposition value INSERTED between correction and the dependent-fields
  content for each NEW edge (NEW-F01: RETRACTED; NEW-F02: RETRACTED + SUPERSEDED;
  NEW-P3A: CORRECTED (provenance history); NEW-P3B: RESOLVED_BY_EXPLICIT_SCOPE;
  NEW-P3D: CORRECTED (true count 17); NEW-P3C: PRESERVED + CLARIFIED — each
  derived from that row's own correction field). Result: ALL 16 rows (header + 15
  edges) parse at exactly 8 fields AND every column now carries its
  semantically-correct content — the preservation_note column is now FILLED for
  all NEW edges, as the QC finding required (a plain positional append would
  have left the current_disposition column holding dependent-fields content and
  the dependent_fields column holding preservation-note content). Text-level
  anchored edits (unique-anchor asserted, single occurrence each); PRIOR rows
  byte-unchanged. SHA256
  6d3b5ffa009b5e0747b8554fc8d423f6d4eb4868a24d154564b598fe3481c665 →
  75629d8bb6af2bcad0ec9495793199bfed10c2a21af65888041808a537eddaad.
- **UNRESOLVED_DELTA.csv**: the TOTALS row carried 4 fields against the 5-column
  header (the note field absent; all 39 item rows had 5). Repair: note field
  appended to the TOTALS row ("AMEND_R1 QC-P3-5: TOTALS row normalized to the
  declared 5-field schema ... strict field-count census after the fix = 39 item
  rows + TOTALS, all 5 fields"). Result: ALL 41 rows parse at exactly 5 fields.
  SHA256
  67531405f24e5ba403f53f80f0dcece124140c81386c6b83c6044e6f22b02b54 →
  04747bea735465790af7f2038e95da090da40dc6616dc1116f83045ef927e44a.
- **Census recorded (strict field-count parse, post-fix)**: FINDINGS.csv 7 rows ×
  18 fields (header + 6 findings ✓); V4_1_DELTA.csv 21 rows × 9 fields (header +
  19 + TOTALS ✓); UNRESOLVED_DELTA.csv 41 rows × 5 fields (header + 39 + TOTALS ✓);
  RETRACTION_SUPERSESSION_DELTA.csv 16 rows × 8 fields (header + 15 ✓);
  GATE_REVALIDATION.csv 6 rows × 8 fields (header + 5 gates ✓);
  MODIFIED_PATHS.csv rows intact (see the pre-existing caveat below).

## ITEM 6 — QC-P3-6: BLAST_RADIUS wording (PEFoliageCore.js change class)

- **Reason**: QC P3 ref QC-P3-6 (the package said both "comment-only" and the
  precise "comment lines + ONE documentation-metadata string" for
  PEFoliageCore.js — potential document-vs-document contradiction).
- **02_ANALYSIS/BLAST_RADIUS.md (row for the unconditional BIT-EXACT wording)**:
  before "corrected in-code (comment-only; four-way separation)" → after
  "corrected in-code (comment lines + ONE documentation-metadata string
  (FOLIAGE_OPERAND_LOCK.exactness) — no executable/behavior change; four-way
  separation)" — now identical in substance to MODIFIED_PATHS.csv row 3.
- **06_REPORT/GATEC_FINDINGS_REVALIDATION_REPORT.md §10**: before
  "src/peworld/PEFoliageCore.js (comment-only)" → after "src/peworld/PEFoliageCore.js
  (comment-only (PEFoliageCore.js additionally: the one exactness metadata
  string — no executable change))" — no document contradicts another on this
  point between BLAST_RADIUS, REPORT §10 and MODIFIED_PATHS row 3.

## ITEM 7 — QC-P3-7: REPORT QC section + manifest result line

- **Reason**: QC P3 ref QC-P3-7 (the report lacked the fresh INTERNAL_QC verdict
  and the current manifest result line).
- **06_REPORT/GATEC_FINDINGS_REVALIDATION_REPORT.md**: NEW section **"## 11.5
  INTERNAL_QC (fresh-context pe-master-auditor, READ-ONLY)"** inserted between
  §11 (NOT_CHECKED) and §12 (HANDOFF) — existing section numbering preserved.
  Content: "QC_PASS_WITH_FINDINGS — 0×P0/P1/P2, 7×P3 (all confirmed by PE-MASTER
  and fixed by AMEND_R1; the correction list in 00_CONTROL/AMEND_LOG_R1.md)." +
  the manifest result line with the TRUE post-AMEND_R1 values:
  "MANIFEST: 48 rows / 49 package files / self_excluded=YES / missing=0 / stale=0
  (re-hashed after AMEND_R1; PE-MASTER re-verification pending its final audit)."
  (True values: the batch added 3 package files — 00_CONTROL/AMEND_LOG_R1.md,
  03_EVIDENCE/F01_TRACE_LINECOUNT_ERRATUM.json,
  03_EVIDENCE/scripts/r1_amend_f01_trace_linecount.mjs — so 46 + 3 = 49 package
  files, manifest self-excluded = 48 rows; verified by the item-9 regeneration.)

## ITEM 8 — AUDIT_ENTRYPOINT.md verdict cell (the ONLY tracked-file edit of this batch)

- **Reason**: the batch contract item 8 (PE-MASTER's verdict for this run; NOT a
  QC finding — the QC listed 7 P3s, this is the dispatcher's verdict-cell update).
- **Edit**: in the row this run added (the EU935_M1_GATE_C_FINDINGS_
  REVALIDATION_R1_20260926 registration row, LATEST RUNS table line 30), the
  verdict cell replaced:
  - before: "PENDING (advisory review by PE-MASTER; Desktop re-audit required for
    Gate C; NOT MILESTONE_CLOSED; nothing authorizes M2)"
  - after: "MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION;
    CANONICAL_GATE_EFFECT=NONE; QC_PASS_WITH_FINDINGS + AMEND_R1; Gate C Desktop
    re-audit MANDATORY next; human closure only; nothing authorizes M2)"
    — exactly the dispatcher-provided string.
- **Verification**: `git diff --numstat AUDIT_ENTRYPOINT.md` = **1/0** (still one
  insertion / zero deletions vs HEAD cc747df — the whole row was added by the
  original run, so the within-line cell edit keeps the vs-HEAD shape); no other
  entrypoint line touched (all other rows byte-preserved; the only entrypoint
  change of the original run + this cell edit). The HANDOFF numstat reference
  (+1/-0) remains correct (see ITEM 1).

## ITEM 9 — Manifest regeneration + final census

- **Reason**: batch contract item 9.
- **06_REPORT/MANIFEST_SHA256.csv**: regenerated — EVERY package file re-hashed
  fresh; the manifest itself self-excluded (L12 precedent); rows = 49 − 1 = 48;
  missing = 0; stale = 0. Strict re-hash census after generation: every row
  re-hashed, 0 stale, 0 missing; package file census re-walked (49 files).
- **EVIDENCE_INDEX.csv**: registered the 2 new evidence files
  (F01_TRACE_LINECOUNT_ERRATUM.json + scripts/r1_amend_f01_trace_linecount.mjs)
  + the RUN-copy SHA correction (ITEM 3.4). 24 → 26 data rows (all 5-field,
  strict parse).
- **Final verification**: all CSVs parse at their declared field counts (ITEM 5
  census); `git status --short` shape unchanged (3 tracked modified
  — AUDIT_ENTRYPOINT.md, src/pesource/VegetationClimateDecoder.js,
  src/peworld/PEFoliageCore.js — + this package + the 2 pre-existing untracked
  roots, untouched); HEAD unchanged cc747df...; UNAUTHORIZED_CHANGED_PATHS = 0.
- **File-level proof of the changed-path census (two independent methods)**:
  (1) MTIME census — EXACTLY the authorized 20 package files (17 modified + 3
  new: the files named in ITEMS 1-8 + the manifest + AMEND_LOG_R1.md) carry
  AMEND_R1 batch write times; every other package file (29) carries the
  original run's write times (plus AUDIT_ENTRYPOINT.md outside the package, the
  item-8 verdict cell).
  (2) Unchanged-file hash check — the 29 out-of-scope package files were
  re-hashed and compared against the pre-amend manifest values: 25 exact
  matches; the remaining 4 (F05_PRECISION_CONTROLS.json + 3 synthetic fixtures)
  verified instead by independent in-package ground truth — all 8 synthetic
  fixtures byte-match the SHA256 values embedded in the UNCHANGED
  F04_NEGATIVE_SEARCH_CONTROLS.json (8/8 MATCH), and the F05 json carries the
  original run's MTIME with unchanged size/content — so 29/29 out-of-scope
  files byte-unchanged.

---

## DISCOVERED BUT NOT FIXED (out of the AMEND_R1 authorized scope; recorded for PE-MASTER's decision)

1. **01_RAW/MODIFIED_PATHS.csv row 3 (src/pesource/VegetationClimateDecoder.js
   row) pre-existing quoting defect**: the behavior_control field contains the
   literal sequence `\"0,2\"` — a raw mid-field double quote that is NOT
   RFC-4180-doubled, so a STRICT csv parse of that row yields 8 fields against
   the 6-column header (rows 1, 2, 4 parse at 6). This predates AMEND_R1 (the
   row is byte-unchanged this batch; "rows intact" holds). Not among the 7 QC
   P3s; fixing it would modify a file outside the authorized list. Proposed fix
   for a future authorized batch: double the embedded quotes (`""0,2""`) or
   replace with single quotes in that field.
2. **06_REPORT/HANDOFF_TO_DESKTOP_REAUDIT.md lines 27-29** still carry the
   pre-amendment "honest delta ... disclosed in §11 NOT_CHECKED, not forced"
   phrasing for the trace total-row count. It was not in ITEM 4's enumerated
   file list ((a) F01 analysis, (b) REPORT §11, (c) SELF_ADVERSARIAL_PASS), so it
   was left byte-unchanged per "NOTHING else may change"; its factual content
   (282,192 vs 282,059; per-client facts match; §11 discloses it) remains true,
   but the "NOT_CHECKED" label is now imprecise since §11's entry is
   root-caused. Proposed one-line upgrade for a future authorized batch.
3. **Summary-level "comment-only" phrasings outside ITEM 6's two enumerated
   targets** (all factually anchored to "no executable change" and NOT
   contradictory after ITEM 6, but less precise than MODIFIED_PATHS row 3):
   REPORT §2 ("the two authorized source files corrected COMMENT-ONLY with a
   proven zero behavior change"); STAGE_ACCEPTANCE_GATES.csv SG10 evidence cell
   ("src/peworld/PEFoliageCore.js (comment-only)"); HANDOFF F02 item ("comment-only
   corrections applied to VegetationClimateDecoder.js + PEFoliageCore.js, ZERO
   behavior change"); the AUDIT_ENTRYPOINT run row's purpose cell
   ("(comment-only)"). Left unchanged (not in the item-6 list; the entrypoint
   row is additionally protected by item 8's "NOTHING else in the entrypoint may
   change").
4. **06_REPORT/GATEC_FINDINGS_REVALIDATION_REPORT.md §3** contains the pointer
   "see §9 NOT_CHECKED + the trace total-row delta" — the NOT_CHECKED section is
   §11, not §9 (pre-existing cross-reference imprecision, byte-unchanged).

---

# AMEND_LOG_R2 — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926

**Batch**: AMEND_R2 (final cosmetic residue; 4 items + manifest). **Dispatcher**:
PE-MASTER (micro-batch contract; NO_NESTED_TASKS). **Executor**:
pe-reconstruction. **Date**: 2026-09-26. **Scope**: EXACTLY the 4 items this
package's AMEND_R1 handoff listed under "DISCOVERED BUT NOT FIXED" + the
manifest regeneration. NOTHING else changed. STATIC-ONLY. PRE-PERSISTENCE
preserved: NO git add / commit / push / staging; HEAD before == after ==
`cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d`. Historical packages and raw
evidence untouched. Files whose bytes changed in AMEND_R2: EXACTLY
01_RAW/MODIFIED_PATHS.csv, 06_REPORT/HANDOFF_TO_DESKTOP_REAUDIT.md,
06_REPORT/GATEC_FINDINGS_REVALIDATION_REPORT.md,
06_REPORT/STAGE_ACCEPTANCE_GATES.csv, 00_CONTROL/AMEND_LOG_R1.md (this
section), 06_REPORT/MANIFEST_SHA256.csv (regenerated) + AUDIT_ENTRYPOINT.md
(the ONLY tracked-file edit of this batch).

## ITEM R2-1 — MODIFIED_PATHS.csv row 3 CSV quoting (the `0,2` fragment)

- **File**: 01_RAW/MODIFIED_PATHS.csv.
- **Row-identity note (recorded, not silent)**: the dispatch contract labels the
  defective row "row 3 (PEFoliageCore.js)", but the row carrying the described
  defect (the `0,2`-style quoted fragment inside the change-description field)
  is DATA ROW 3 = the src/pesource/VegetationClimateDecoder.js row (file line
  4), exactly as AMEND_R1's DISCOVERED-BUT-NOT-FIXED item 1 recorded. The
  src/peworld/PEFoliageCore.js row is data row 2 (file line 3) and parses
  clean at 6 fields (verified pre- and post-fix; byte-untouched by this batch).
  The fix targeted the row uniquely identified by the defect description + the
  AMEND_R1 disclosure (strict-malformed / 8-field lenient parse).
- **Before**: the behavior_control field of that row contained the literal
  sequence `\"0,2\"` — backslash-escaped quotes, a non-RFC4180 encoding. STRICT
  RFC4180 parse: row MALFORMED (bare quote inside a quoted field); lenient
  (Python csv) parse: **8 fields** against the 6-field header; the other 4 rows
  at 6. The backslashes were ENCODING ARTIFACTS, not content: the true decoder
  exception text (verified against 03_EVIDENCE/F02_VCL_CENSUS.json, the 25.vcl
  THROW error, and the decoder source throw literal at
  src/pesource/VegetationClimateDecoder.js:95) is `non-numeric token "0,2" at
  record 9 col 1` — plain quotes.
- **After**: `""0,2""` (RFC4180-doubled quotes). The row now parses as EXACTLY
  6 fields under BOTH parsers, and the parsed field content now EQUALS the true
  exception text. Byte-neutral fix: exactly 2 bytes changed (0x5C -> 0x22 twice);
  size 4,629 B unchanged. SHA256
  5cad30147e8084cc6b0df1950e570b56627efa88342ededd5473e0f8c003dede ->
  4776b5d178c4dbbada81535279bfb7ed10b36fd60a645de73531f34ef6d6cc13.
- **Strict-parse census (recorded per the contract)**: verifier = this batch's
  own strict RFC4180 parser (bare quote inside a quoted field = MALFORMED)
  cross-checked against the Python 3.12.10 csv module (dual independent
  parsers). BEFORE: rows 1/2/3/5 = 6 fields; row 4 = MALFORMED (strict) / 8
  fields (Python csv). AFTER: **ALL 5 rows = 6 fields = the header field count,
  0 malformed, both parsers agree.**

## ITEM R2-2 — HANDOFF pre-amendment delta paragraph (root-caused erratum)

- **File**: 06_REPORT/HANDOFF_TO_DESKTOP_REAUDIT.md (the F01 item's closing
  NOTE, previously L26-29).
- **Before**: "NOTE the honest delta: our trace total-row count = 282,192 vs
  your quoted 282,059 (the per-client facts all match exactly; the 133-row
  delta is disclosed in §11 NOT_CHECKED, not forced)."
- **After**: "NOTE the trace total-row delta is ROOT-CAUSED (AMEND_R1,
  03_EVIDENCE/F01_TRACE_LINECOUNT_ERRATUM.json): your quoted 282,059 data rows
  = CORRECT (the LF convention: 282,060 LF bytes = header + 282,059 data rows;
  confirmed by a quote-aware RFC4180 parse of the same bytes, 0 malformed); our
  successor probe's 282,192 = a CR-splitting line-count artifact (133 lone CR
  bytes embedded inside quoted Detail fields were each counted as an extra
  line boundary: 282,060 LF + 133 = 282,193 reader lines -> 282,192 'data
  rows'); the per-client load-bearing facts (1 PID / 2,193 Entropia.exe rows /
  exactly one 'Exit Status: -1' / 0 ddraw-d3d8-d3d9 loads) are UNAFFECTED (all
  re-verified under the CR-correct parse)."
- **Reason**: the paragraph no longer presents the trace-row delta as merely
  "honest disclosure"; it now references the ROOT-CAUSED erratum
  (F01_TRACE_LINECOUNT_ERRATUM.json). Consistency VERIFIED against
  02_ANALYSIS/F01_PRIMARY_DEVICE_REVALIDATION.md §5.2.B and REPORT §11: the
  same numbers, the same adjudication (282,059 CORRECT; 282,192 =
  CR-splitting artifact; per-client facts unaffected) — no contradictions
  between the three documents.
- **File SHA256 (before -> after; this file's total R2 delta = R2-2 + R2-3 Fix
  4)**: 0995526d7a5b005f217c1a1d2f43bb94f679995a5f056e1dd89c8a5088835f4c
  (6,163 B) ->
  75d9e940b8430bb1527c27e3fbc41aa499cc84116507c8a88af1afeebb1113f6
  (6,841 B).

## ITEM R2-3 — Summary-level "comment-only" phrasings -> precise (V2R-001)

- **Reason**: align every SUMMARY position that says "comment-only" about the
  PEFoliageCore.js change (or about BOTH source files jointly) to the
  authoritative disclosure in MODIFIED_PATHS.csv row 3 + REPORT §10 +
  BLAST_RADIUS.md: "comment lines + ONE documentation-metadata string
  (FOLIAGE_OPERAND_LOCK.exactness) — no executable/behavior change"
  ("comment-only" for VegetationClimateDecoder.js alone remains accurate).
- **Fix 1 — REPORT §2 (state delta)**: before "the two authorized source files
  corrected COMMENT-ONLY with a proven zero behavior change" -> after
  "corrected with a proven zero behavior change (src/pesource/
  VegetationClimateDecoder.js comment-only; src/peworld/PEFoliageCore.js
  comment lines + ONE documentation-metadata string (FOLIAGE_OPERAND_LOCK.
  exactness) — no executable change)".
- **Fix 2 — REPORT §4 F05**: before "BIT-EXACT wording corrected (comment-only)
  to the CONDITIONAL form" -> after "BIT-EXACT wording corrected in-code
  (comment lines + ONE documentation-metadata string (FOLIAGE_OPERAND_LOCK.
  exactness) — no executable/behavior change) to the CONDITIONAL form" (aligned
  with BLAST_RADIUS.md's authoritative phrasing for the same row).
- **Fix 3 — STAGE_ACCEPTANCE_GATES.csv SG10 evidence cell**: before
  "src/peworld/PEFoliageCore.js (comment-only)" -> after "src/peworld/
  PEFoliageCore.js (comment lines + ONE documentation-metadata string
  (FOLIAGE_OPERAND_LOCK.exactness) — no executable/behavior change)". The
  VegetationClimateDecoder.js parenthetical "(comment-only; pre/post-edit
  behavior control 31/1/472 identical)" UNCHANGED (decoder-only, accurate).
  The row still strict-parses at 5 fields (census below) and remains ONE line.
- **Fix 4 — HANDOFF F02 item**: before "The two authorized comment corrections
  are behavior-controlled (identical 31/1/472 + identical exception pre/post
  edit)." -> after "The two authorized source corrections are behavior-
  controlled (VegetationClimateDecoder.js comment-only, identical 31/1/472 +
  identical exception pre/post edit; PEFoliageCore.js comment lines + the one
  exactness metadata string — no executable change)."
- **Fix 5 — AUDIT_ENTRYPOINT.md (the ONLY tracked-file edit of this batch; the
  registration row this run added, LATEST RUNS table line 30; both hits in the
  purpose cell)**:
  - 5a. before "comment-only corrections applied to VegetationClimateDecoder.js
    + PEFoliageCore.js, ZERO behavior change — 31/1/472 identical pre/post
    edit" -> after "comment-only corrections applied to
    VegetationClimateDecoder.js + comment + one exactness metadata string in
    PEFoliageCore.js, ZERO behavior change (31/1/472 identical pre/post edit)"
    (the dispatcher-provided wording).
  - 5b. before "src/pesource/VegetationClimateDecoder.js + src/peworld/
    PEFoliageCore.js (comment-only)" -> after "... (comment-only;
    PEFoliageCore.js additionally: the one exactness metadata string — no
    executable change)" (mirrors REPORT §10's authoritative phrasing).
  - The cell remains ONE table line, no newlines (verified: the row's LF count
    unchanged; 6 pipes = 5 cells intact); `git diff --numstat
    AUDIT_ENTRYPOINT.md` remains **1/0** (the whole row was added by the
    original run, so the within-line edits keep the vs-HEAD delta at 1
    insertion / 0 deletions — re-verified after the edit). All pre-existing
    entrypoint rows byte-preserved (the file's only remaining `\"` sequence is
    at line 49, a pre-existing historical row, byte-untouched). Entry SHA256
    33ca2504f7d88aa750a967834ad3a45da28be67c10a055f7f806665aa379144d (113,551 B)
    -> d7c353c5f343b477da736b31b64be6e57591d7a111e49a60c1618faab7ad27d3
    (113,683 B).
- **Post-fix byte-scan (case-insensitive "comment-only|comment corrections"
  over the three 06_REPORT prose files + the entrypoint added row)**: every
  REMAINING hit is either (a) genuinely VegetationClimateDecoder.js-only —
  HANDOFF GIT STATE "(+30/-6 comment-only)"; REPORT §10 "(comment-only)" for
  the decoder; REPORT §4 F02 "the authorized comment corrections applied"
  (F02's own correction is decoder-only and cites the 31/1/472 decoder
  control); SG10's decoder parenthetical; the decoder-scoped "comment-only"
  fragments inside this batch's own replacement texts — or (b) the
  authoritative ALREADY-precise phrasings (REPORT §10 "comment-only
  (PEFoliageCore.js additionally: the one exactness metadata string — no
  executable change)" and the identical entrypoint fragment). No remaining hit
  characterizes the PEFoliageCore.js change as comment-only. Pre-existing
  entrypoint historical rows are byte-preserved (out of scope by design).
- **File SHA256 (before -> after)**: 06_REPORT/GATEC_FINDINGS_REVALIDATION_
  REPORT.md (this file's total R2 delta = Fixes 1, 2 + R2-4):
  d926116d546465acb51bcee1a8118beff79f9ed71c8bf9f463f91d3ff0fa1f95 (16,543 B)
  -> 1525ff8e7bd7290ac80e7bdcdbce1a4ba266c9056236445733b811c6f167c268
  (16,848 B). 06_REPORT/STAGE_ACCEPTANCE_GATES.csv (Fix 3):
  05ff636816e8506ec25b0ebce11912749b29ee7b0705fee65ef91c9b929c2100 (5,633 B)
  -> c761d5a8cc9c237a9c3c808011c414f51b833707c93903e48263106e25db0768
  (5,737 B).

## ITEM R2-4 — REPORT §3 pointer fix

- **File**: 06_REPORT/GATEC_FINDINGS_REVALIDATION_REPORT.md §3.
- **Before**: "reported, not forced (see §9 NOT_CHECKED + the trace total-row
  delta)." — **After**: "reported, not forced (see §11 NOT_CHECKED + the trace
  total-row delta)."
- **Reason**: the NOT_CHECKED section is §11 in the current report (§9 = GATES);
  the pre-amendment pointer was a cross-reference imprecision (AMEND_R1
  DISCOVERED-BUT-NOT-FIXED item 4).

## ITEM R2-5 — Close-out: manifest regeneration + final census

- **06_REPORT/MANIFEST_SHA256.csv**: regenerated — EVERY package file re-hashed
  fresh (node v22.22.0 = the repo runtime); the manifest itself self-excluded
  (L12 precedent); row order preserved from the previous manifest. **rows = 48
  / package files = 49 / missing = 0 / stale = 0** (post-generation strict
  re-hash census: every row re-hashed and compared — 0 stale, 0 missing;
  package walk re-counted 49 files; the manifest row/file census re-verified).
- **All package CSVs strict-parse at their declared field counts** (this
  batch's strict RFC4180 parser + Python csv cross-check): FINDINGS.csv 7 rows ×
  18 fields (header + 6 findings); GATE_REVALIDATION.csv 6 × 8 (header + 5
  gates); MODIFIED_PATHS.csv 5 × 6 (header + 4; the R2-1 fix closes the last
  malformed row); RETRACTION_SUPERSESSION_DELTA.csv 16 × 8 (header + 15);
  UNRESOLVED_DELTA.csv 41 × 5 (header + 39 + TOTALS); V4_1_DELTA.csv 21 × 9
  (header + 19 + TOTALS); EVIDENCE_INDEX.csv 27 × 5 (header + 26);
  STAGE_ACCEPTANCE_GATES.csv 13 × 5 (header + SG1-SG12);
  MANIFEST_SHA256.csv 49 × 3 (header + 48). 0 malformed rows anywhere.
- **Git verification**: HEAD before == after ==
  cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d (no staging/commit/push);
  `git status --short` shape UNCHANGED (3 tracked modified —
  AUDIT_ENTRYPOINT.md, src/pesource/VegetationClimateDecoder.js,
  src/peworld/PEFoliageCore.js — + this package + the 2 pre-existing untracked
  roots, untouched); `git diff --numstat` = **1/0** AUDIT_ENTRYPOINT.md,
  **30/6** src/pesource/VegetationClimateDecoder.js, **20/5**
  src/peworld/PEFoliageCore.js (the source files byte-untouched by this batch —
  their numstat is the original run's).
- **UNAUTHORIZED_CHANGED_PATHS = 0** (two independent methods): (1) HASH census
  — a pre-R2 baseline snapshot (SHA256 + size + mtime for all 49 package files
  + AUDIT_ENTRYPOINT.md) was taken BEFORE the first R2 edit; the post-batch
  re-hash comparison shows the changed set = EXACTLY the 6 authorized package
  files named at the top of this section + AUDIT_ENTRYPOINT.md; all other 43
  package files byte-identical. (2) MTIME census corroborates (only the
  authorized files carry R2 write times).
- **Byte-integrity of the edits**: all edited files verified byte-wise — no
  BOM, LF-only line endings, no U+FFFD, no cp1252/cp437 roundtrip mojibake,
  true U+2014 em-dashes (console rendering NOT used as evidence).
- **NOTED, not fixed (out of the 4-item scope)**: (a) REPORT §11.5's manifest
  line still reads "re-hashed after AMEND_R1" — its counts (48 rows / 49 files /
  missing=0 / stale=0) remain TRUE after the R2 regeneration; the R2 re-hash is
  recorded in THIS section. (b) STAGE_ACCEPTANCE_GATES.csv SG3's evidence cell
  still says "agreements + the honest deltas: the 282,192 vs 282,059 trace
  total-row delta" — a description of what SG3's cross-comparison recorded
  (the delta IS recorded, and it IS root-caused in REPORT §11 +
  F01_TRACE_LINECOUNT_ERRATUM.json; no contradiction); item 2's named target
  was the HANDOFF paragraph only. Both left byte-unchanged per "closes EXACTLY
  the 4 items — nothing else".

---

# AMEND_LOG_R3 — EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926

**Batch**: AMEND_R3 (edge-count reconciliation; final). **Dispatcher**: PE-MASTER
(micro-batch contract AMEND_R3; NO_NESTED_TASKS). **Executor**: pe-reconstruction.
**Date**: 2026-09-26. **Defect class (PE-MASTER final audit)**: the RETRACTION edge
census was miscounted as "5 new" in prose while the authoritative CSV carries 6 NEW
edges (NEW-F01, NEW-F02, NEW-P3A, NEW-P3B, NEW-P3C, NEW-P3D;
01_RAW/RETRACTION_SUPERSESSION_DELTA.csv = header + 9 PRIOR + 6 NEW = 16 lines).
**Scope**: EXACTLY the 7 dispatched items — the 5 prose/CSV-cell corrections
(including the 2 executor-disclosed R2 residues recorded in R2 ITEM R2-5's "NOTED,
not fixed" list) + the full edge-census reconciliation sweep + the manifest
regeneration. NOTHING else changed. STATIC-ONLY. PRE-PERSISTENCE preserved: NO git
add / commit / push / staging; HEAD before == after ==
`cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d`. Historical packages and raw evidence
untouched; 01_RAW/RETRACTION_SUPERSESSION_DELTA.csv itself NOT touched (it is
correct). Files whose bytes changed in AMEND_R3: EXACTLY
06_REPORT/HANDOFF_TO_DESKTOP_REAUDIT.md, 06_REPORT/GATEC_FINDINGS_
REVALIDATION_REPORT.md, 06_REPORT/STAGE_ACCEPTANCE_GATES.csv,
00_CONTROL/AMEND_LOG_R1.md (this section), 06_REPORT/MANIFEST_SHA256.csv
(regenerated) + AUDIT_ENTRYPOINT.md (the ONLY tracked-file edit of this batch).

## ITEM R3-1 — HANDOFF L73 edge census (9 preserved + 6 new)

- **File**: 06_REPORT/HANDOFF_TO_DESKTOP_REAUDIT.md (WHERE EVERYTHING IS section).
- **Before** (L73): "RETRACTION_SUPERSESSION_DELTA.csv (9 preserved + 5 new
  edges)," — **After**: "RETRACTION_SUPERSESSION_DELTA.csv (9 preserved + 6 new
  edges: NEW-F01, NEW-F02, NEW-P3A, NEW-P3B, NEW-P3C, NEW-P3D)," — the
  dispatcher-provided wording.
- **Verification**: now agrees with the CSV census (16 rows = header + 9 PRIOR +
  6 NEW). File SHA256
  75d9e940b8430bb1527c27e3fbc41aa499cc84116507c8a88af1afeebb1113f6 (6,841 B) ->
  715137bd8a08f766f7754444ad7c28e3b3de83fde860de01848d9dc1b160607c (6,899 B).
  LF-only, no BOM (byte-verified).

## ITEM R3-2 — REPORT §2 state-delta edge census + §5 claim/edge denominators

- **File**: 06_REPORT/GATEC_FINDINGS_REVALIDATION_REPORT.md.
- **Fix 2a — §2 (state delta, the AFTER bullet)**: before "the false premises
  RETRACTED (2 new successor edges + 3 housekeeping edges)" -> after "(2
  load-bearing correction edges NEW-F01/NEW-F02 + 4 housekeeping edges
  NEW-P3A/P3B/P3C/P3D = 6 new edges total; NEW-P3C is a chronology-clarification
  edge, no claim retracted)" — the dispatcher-provided wording.
- **Fix 2b — §5 (CORRECTED / UNCHANGED CLAIM COUNTS)**: the housekeeping claim
  enumeration previously listed only 3 (fresh-pin history / witness-matrix
  scope / OPEN_LIMITS); appended the 4th explicitly: "+ the PROGRESS_STATE
  phase-7 chronology clarification (NEW-P3C: preserved-as-checkpoint, not a
  retracted claim)"; the downstream-contract §1/§5/§6 item explicitly labeled
  "not an edge"; and the CLAIM count vs EDGE count denominators are now stated
  explicitly and separately: "claims = 2 load-bearing corrected + 3 housekeeping
  corrected + 1 chronology clarification; edges = 6 (NEW-F01, NEW-F02, NEW-P3A,
  NEW-P3B, NEW-P3C, NEW-P3D; 01_RAW/RETRACTION_SUPERSESSION_DELTA.csv = 9 PRIOR
  preserved + 6 NEW)". The two denominators are NOT flattened: the 4th CLAIM
  position is a chronology clarification (not a housekeeping-corrected claim)
  and maps to NEW-P3C, one of the 6 edges.
- **Verification**: file SHA256
  1525ff8e7bd7290ac80e7bdcdbce1a4ba266c9056236445733b811c6f167c268 (16,848 B) ->
  3d94fc2506711ceeb7172154dbd7a7546999ec6ee1dd3c2d0cf06a0c9859a497 (17,416 B).
  LF-only, no BOM. The §5 unchanged-families
  bullet's "the retraction canon (9 prior edges preserved verbatim)" was
  already correct — untouched.

## ITEM R3-3 — AUDIT_ENTRYPOINT.md run-row purpose cell (the ONLY tracked-file edit)

- **File**: AUDIT_ENTRYPOINT.md (the registration row this run added; LATEST
  RUNS table line 30; purpose cell).
- **Before**: "2 new retraction/correction edges added (F01, F02) + P3-A/P3-B/
  P3-D housekeeping corrections" — **After**: "6 new retraction/correction
  edges added (NEW-F01, NEW-F02, NEW-P3A, NEW-P3B, NEW-P3C, NEW-P3D)" — the
  dispatcher-provided wording; the cell remains ONE line.
- **Verification**: `git diff --numstat AUDIT_ENTRYPOINT.md` = **1/0** (the
  whole row was added by the original run, so the within-line cell edit keeps
  the vs-HEAD delta at 1 insertion / 0 deletions); the file's line count
  unchanged (117 LFs); no other entrypoint byte changed — the byte-delta vs the
  pre-R3 snapshot is confined to this one substring (92 -> 94 ASCII bytes, +2;
  file 113,683 B -> 113,685 B; SHA256
  d7c353c5f343b477da736b31b64be6e57591d7a111e49a60c1618faab7ad27d3 ->
  8eec84e65c19b56705b023aadab27b5ad0a05e03686e5992f4c47a4836bee45e). All
  pre-existing entrypoint rows byte-preserved. The row's
  verdict cell (the dispatcher-provided AMEND_R1 verdict string) NOT touched
  (out of the dispatched scope).

## ITEM R3-4 — FULL EDGE-CENSUS RECONCILIATION SWEEP (the closing control)

- **Method**: byte-level content scan of EVERY package file (49) + the
  AUDIT_ENTRYPOINT run row for references to the new-edge census — patterns:
  "5 new" / "five new" / "3 housekeeping" / "three housekeeping" / "2 new" /
  "two new" / "+ 3" / "new edges" / "new successor edges" / "6 new" / "6 edges"
  / "9 preserved" / "9 PRIOR" / "15 edges" / "housekeeping" / "P3A|P3B|P3C|P3D"
  / "P3-A..P3-D" / "NEW-P3" / "NEW-F0" / "NEW_CORRECTION_EDGE" / "successor
  edge" / "correction edge" / "RETRACTION_SUPERSESSION_DELTA". **Authoritative
  ground truth**: 01_RAW/RETRACTION_SUPERSESSION_DELTA.csv = 16 lines = header
  + 9 PRIOR + 6 NEW (file order: NEW-F01, NEW-F02, NEW-P3A, NEW-P3B, NEW-P3D,
  NEW-P3C); housekeeping edges = P3A/P3B/P3C/P3D; NEW-P3C = chronology-
  clarification edge (no claim retracted).
- **HIT LIST + DISPOSITIONS**:

  FIXED this batch:
  1. HANDOFF L73 "(9 preserved + 5 new edges)" — wrong NEW-edge count (5 != 6)
     — ITEM R3-1.
  2. REPORT §2 "(2 new successor edges + 3 housekeeping edges)" — wrong
     NEW-edge count (2+3=5 != 6) — ITEM R3-2 Fix 2a.
  3. REPORT §5 housekeeping enumeration listed only 3 claim positions without
     the 4th (NEW-P3C) and without the claims-vs-edges separation — ITEM R3-2
     Fix 2b.
  4. AUDIT_ENTRYPOINT run-row purpose cell "2 new retraction/correction edges
     added (F01, F02) + P3-A/P3-B/P3-D housekeeping corrections" — named
     P3A/P3B/P3D WITHOUT P3C, used the old hyphenated names, and carried the
     5-flavored count — ITEM R3-3.
  5. REPORT §11.5 "(re-hashed after AMEND_R1...)" — stale manifest-provenance
     label (counts true; the manifest was regenerated in R2 and again in R3) —
     ITEM R3-5.
  6. STAGE_ACCEPTANCE_GATES.csv SG3 evidence cell "agreements + the honest
     deltas: the 282,192 vs 282,059 trace total-row delta" — pre-root-cause
     description — ITEM R3-6.

  ALREADY-CORRECT (agree with the CSV census; byte-untouched):
  7. 01_RAW/RETRACTION_SUPERSESSION_DELTA.csv — the authoritative census itself
     (16 rows = header + 9 PRIOR + 6 NEW; all 8 fields; LF-only) — NOT touched
     per the dispatch.
  8. REPORT §5 unchanged-families bullet: "the retraction canon (9 prior edges
     preserved verbatim)" — correct (9 PRIOR).
  9. REPORT §4 F01/F02 verdicts: "RETRACTED (edge NEW-F01)" / "CONTRADICTION_
     FOUND at V4 row 7 (edge NEW-F02)" — single-edge references, correct.
  10. 02_ANALYSIS/F01_PRIMARY_DEVICE_REVALIDATION.md: "RETRACTED
      (RETRACTION_SUPERSESSION_DELTA.csv NEW-F01)" — correct.
  11. 02_ANALYSIS/F02_VCL_CORPUS_DECODER_REVALIDATION.md: "correction edges
      NEW-F02 in RETRACTION_SUPERSESSION_DELTA.csv" — correct.
  12. 02_ANALYSIS/BLAST_RADIUS.md rows: RETRACTION_NEW-F01 / NEW-F02 / NEW-P3A
      / NEW-P3B / NEW-P3D — correct per-edge rows (see hit 21 for the absent
      P3C row adjudication).
  13. 01_RAW/MODIFIED_PATHS.csv row 1: "...corrected by the successor row +
      RETRACTION_SUPERSESSION_DELTA.csv NEW-F01" — single-edge reference,
      correct.
  14. 00_CONTROL/AMEND_LOG_R1.md R1 ITEM 5: "the 6 NEW-* edges" + the full
      6-edge enumeration (incl. NEW-P3C) + "ALL 16 rows (header + 15 edges)" —
      correct (historical R1 record, byte-preserved).
  15. 00_CONTROL/AMEND_LOG_R1.md R1 ITEM 5 census + R2 ITEM R2-5 census:
      "RETRACTION_SUPERSESSION_DELTA.csv 16 rows × 8 fields (header + 15)" /
      "16 × 8 (header + 15)" — correct (historical records).
  16. 00_CONTROL/RUN_CONTRACT.md §12: the dispatcher's verbatim original
      contract enumerates all four housekeeping items P3-A/P3-B/P3-C/P3-D —
      agrees with the census; the control document is byte-preserved by design.
  17. 01_RAW/V4_1_DELTA.csv row 8 + 01_RAW/UNRESOLVED_DELTA.csv rows A21/B5/C1/
      C2: single "P3-B" scope references — correct.

  NOT-AN-EDGE-COUNT (different denominators / different objects; explicitly
  labeled; byte-untouched):
  18. The UNRESOLVED-set disposition census "6 NEW_CORRECTION_EDGE (A3/A4/A18/
      B4/C4/C5 — the F04 language narrowing)" at REPORT §7, STAGE_ACCEPTANCE_
      GATES SG5, 01_RAW/UNRESOLVED_DELTA.csv TOTALS, 02_ANALYSIS/F04: this
      counts 39-item UNRESOLVED-set dispositions (32 NO_CHANGE + 6
      NEW_CORRECTION_EDGE + 1 STATUS_REVALIDATION), NOT the retraction CSV
      edges — a different denominator that happens to carry the same numeric
      value 6; every occurrence is explicitly labeled as the UNRESOLVED delta
      and the retraction census is separately named, so the two 6s are never
      flattened.
  19. 01_RAW/FINDINGS.csv correction_edge column (F01_CORRECTION_EDGE ..
      F06_CORRECTION_EDGE): per-finding edge descriptions; no counts.
  20. 01_RAW/V4_1_DELTA.csv TOTALS: "the 3 prior SUPERSEDED_WITH_VALID_EDGE
      relationships (rows 3, 8, 14)" — the V4.1 19-row delta census; correct,
      different denominator.
  21. 02_ANALYSIS/BLAST_RADIUS.md: the CONFIRMED-INVALIDATED table names
      NEW-P3A/P3B/P3D WITHOUT a NEW-P3C row — adjudicated CORRECT-BY-SCOPE: the
      table is scoped to invalidated/corrected carried items; NEW-P3C's own
      CSV disposition is "PRESERVED + CLARIFIED ... chronology-clarification
      only; the historical file is NOT modified" (nothing invalidated, no
      claim retracted), so no blast-radius row exists for it; the table makes
      no completeness claim over the NEW-edge census. (Its §1 note "all 9
      prior retractions preserved verbatim" is correct.)
  22. RUN_CONTRACT §"RETRACTIONS": "ADD explicit new successor/correction
      edges: F01 ...; F02 ...; plus every directly dependent carried field
      found false" — the original dispatcher contract's instruction (the 4
      housekeeping edges come from its §12); no count; byte-preserved control
      document. RUN_CONTRACT §"Record" "retractions/supersession edges added"
      — required-report-content list, no count.
  23. Generic no-count references: 02_ANALYSIS/F03 ("the correction edges are
      recorded (FINDINGS.csv F03; V4_1_DELTA...") / F06 ("corrected by
      successor edge, not by editing history") / DOWNSTREAM_CONTRACT_
      CORRECTIONS ("with the correction edges") / F02 analysis ("(historical;
      successor edge)") — no counts.
  24. The AUDIT_ENTRYPOINT run row's verdict cell "(... QC_PASS_WITH_FINDINGS
      + AMEND_R1; ...)" — QC/amendment provenance, not an edge count; the
      dispatcher-provided verdict string, out of the dispatched scope —
      byte-untouched.
  25. AMEND_LOG R1 ITEM 7 "46 + 3 = 49 package files" / R1 ITEM 9 "(17 modified
      + 3 new ...)" — file-count arithmetic, not edges.

- **Sweep result**: after ITEMS R3-1/2/3/5/6, ZERO remaining prose reference
  contradicts the CSV census (9 preserved + 6 NEW; housekeeping = P3A/P3B/P3C/
  P3D; NEW-P3C = chronology clarification); every remaining "6" that could be
  confused is explicitly labeled with its own denominator (UNRESOLVED-set vs
  retraction CSV); the claims-vs-edges denominators are kept separate at
  REPORT §5.

## ITEM R3-5 — REPORT §11.5 manifest provenance (executor-disclosed R2 residue (a))

- **Before** (§11.5 closing line): "(re-hashed after AMEND_R1; PE-MASTER
  re-verification pending its final audit)." — **After**: "(re-hashed after
  AMEND_R1/R2/R3; PE-MASTER re-verification pending its final audit)." — the
  dispatcher-provided wording. The counts (48 rows / 49 files / missing=0 /
  stale=0) were and remain TRUE; the R2 re-hash was recorded in the R2 log and
  this R3 regenerates the manifest again (ITEM R3-7). Part of ITEM R3-2's file
  delta.

## ITEM R3-6 — STAGE_ACCEPTANCE_GATES.csv SG3 evidence cell (executor-disclosed R2 residue (b))

- **File**: 06_REPORT/STAGE_ACCEPTANCE_GATES.csv (SG3 row; the only CSV-cell
  edit of this batch).
- **Before** (evidence field): "...cross-comparisons recorded per finding
  (agreements + the honest deltas: the 282,192 vs 282,059 trace total-row
  delta)" — **After**: "...cross-comparisons recorded per finding (agreements +
  the trace total-row delta recorded in REPORT §11 AND root-caused by
  03_EVIDENCE/F01_TRACE_LINECOUNT_ERRATUM.json: 282,059 = the correct LF
  data-row count, 282,192 = the CR-splitting line-count artifact)" — aligned
  with the root-caused state (REPORT §11 + F01_TRACE_LINECOUNT_ERRATUM.json).
- **Verification**: the row remains 5 fields (strict RFC4180 parse; census in
  ITEM R3-7) and ONE line (13 LF lines file-wide: header + SG1-SG12, row count
  unchanged); no other row touched. File SHA256
  c761d5a8cc9c237a9c3c808011c414f51b833707c93903e48263106e25db0768 (5,737 B) ->
  a40334b81be62223ee01f9c7fef259a35905914969768c53f16082bb146e804c (5,876 B).
  LF-only, no BOM.

## ITEM R3-7 — Close-out: manifest regeneration + final census

- **06_REPORT/MANIFEST_SHA256.csv**: regenerated — EVERY package file re-hashed
  fresh (node v22.22.0 = the repo runtime); the manifest itself self-excluded
  (L12 precedent); row order preserved from the previous manifest. **rows = 48
  / package files = 49 / missing = 0 / stale = 0** (pre-regeneration census
  guard: the disk file set == the manifest row set + the manifest itself, 0
  added / 0 removed; post-generation strict re-hash census: every row re-hashed
  and compared — 0 stale, 0 missing).
- **All 9 package CSVs strict-parse at their declared field counts** (strict
  RFC4180 parser): FINDINGS.csv 7 × 18 (header + 6 findings); GATE_REVALIDATION.
  csv 6 × 8 (header + 5 gates); MODIFIED_PATHS.csv 5 × 6 (header + 4);
  RETRACTION_SUPERSESSION_DELTA.csv 16 × 8 (header + 15); UNRESOLVED_DELTA.csv
  41 × 5 (header + 39 + TOTALS); V4_1_DELTA.csv 21 × 9 (header + 19 + TOTALS);
  EVIDENCE_INDEX.csv 27 × 5 (header + 26); STAGE_ACCEPTANCE_GATES.csv 13 × 5
  (header + SG1-SG12); MANIFEST_SHA256.csv 49 × 3 (header + 48). 0 malformed
  rows anywhere.
- **RETRACTION_SUPERSESSION_DELTA.csv census (the ground truth; UNTOUCHED)**:
  16 lines = header + 9 PRIOR (PRIOR-1..PRIOR-9) + 6 NEW (NEW-F01, NEW-F02,
  NEW-P3A, NEW-P3B, NEW-P3D, NEW-P3C); all rows 8 fields; LF-only (16 LF, 0 CR);
  SHA256 75629d8bb6af2bcad0ec9495793199bfed10c2a21af65888041808a537eddaad
  (8,256 B) — byte-identical to the pre-R3 baseline.
- **Git verification**: HEAD before == after ==
  cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d (no staging/commit/push);
  `git status --short` shape UNCHANGED (3 tracked modified —
  AUDIT_ENTRYPOINT.md, src/pesource/VegetationClimateDecoder.js,
  src/peworld/PEFoliageCore.js — + this package + the 2 pre-existing untracked
  roots, untouched); `git diff --numstat` = **1/0** AUDIT_ENTRYPOINT.md,
  **30/6** src/pesource/VegetationClimateDecoder.js, **20/5**
  src/peworld/PEFoliageCore.js (the two source files byte-untouched by this
  batch — their numstat is the original run's).
- **UNAUTHORIZED_CHANGED_PATHS = 0** (two independent methods): (1) HASH
  census — a pre-R3 baseline snapshot (SHA256 + size + mtime for all 49 package
  files + AUDIT_ENTRYPOINT.md) was taken BEFORE the first R3 edit; the
  post-batch re-hash comparison shows the changed set = EXACTLY the 5
  authorized package files named at the top of this section +
  AUDIT_ENTRYPOINT.md; all other 44 package files byte-identical. (2) MTIME
  census corroborates (only the authorized files carry R3 write times).
- **Byte-integrity of the edits**: all edited files verified byte-wise — no
  BOM, LF-only line endings, no U+FFFD, no cp1252/cp437 roundtrip mojibake
  (console rendering NOT used as evidence).
