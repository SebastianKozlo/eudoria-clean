# QC P3 FIX BATCH RECORD — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927

Dispatcher: PE-MASTER. Executor: pe-reconstruction. Date: 2026-09-27.
Scope: EXACTLY the six dispatched fixes FIX-1..FIX-6 (QC findings P3-QC-1 /
P3-QC-2 / P3-QC-3 + the PE-MASTER dependent-search timing-consistency
finding + this batch record + the manifest refresh); NO other file was
touched. Authorization: human run contract section 14 (bounded P3 hygiene
may be corrected inside authorized paths, then fresh QC repeats); the fresh
QC repeat belongs to the later QC worker.

Method discipline: every dispatched value was independently re-measured
BEFORE any write (all matched; NO HARD STOP fired). Every "before" hash
below is the pre-batch value (re-hashed fresh before the edits AND
cross-checked machine-read against the pre-batch 06_REPORT/
MANIFEST_SHA256.csv rows — cross-check PASS x5); every "after" hash is a
fresh measurement of the final bytes. All five edited files and this
record are UTF-8 without BOM, LF-only (per-file CR count = 0 verified).
NO git add/commit/push was performed at any point; the predecessor R1
package and the BEFORE_IMAGES were never written.

Changed-file census of this batch: exactly 7 paths inside this package —
5 edited (02_ANALYSIS/R2_F01_TERRAIN_SAMPLE_COUNTER.md,
02_ANALYSIS/SELF_ADVERSARIAL_PASS.md, 02_ANALYSIS/BLAST_RADIUS.md,
02_ANALYSIS/R2_F02_VCL_REVIEW_ERRATUM.md, 06_REPORT/REPORT.md) + 1 new
(this record) + 1 regenerated (06_REPORT/MANIFEST_SHA256.csv, computed
LAST). Zero paths outside this package were modified.

## FIX-1 — garbled dir_off phrase (QC finding P3-QC-1)

- File: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/R2_F01_TERRAIN_SAMPLE_COUNTER.md, line 16.
- OLD (exact span):

```
(dir_off = 24608-independent value recorded in the JSON; count = 58,451).
```

- NEW (exact text):

```
(dir_off = 123,369,726, recorded in the JSON; count = 58,451).
```

- Grounds: 03_EVIDENCE/R2_F01_TERRAIN_COUNTER.json "bnt2"."dir_off" =
  123369726, "count" = 58451 (re-verified fresh from the JSON before
  writing). 24608 is not a terrain.bnt value; the dispatch attributes it to
  the VegetationClimates.bnt dir_off (a copy artifact) — attribution not
  re-derived by this batch (not load-bearing for the fix).
- Bounded-authorized: human run contract section 14.
- File before: sha256 10e77ed1bb6038101d15de04b4a731d91801b564c101fcb50421c8bbb9b31a12, 3993 B
- File after (final; this file also carries FIX-3): sha256 fc5cec19d55e40c8241a7ac25e91f81ae04316ca76464873bd2261a5a300ff97, 4419 B

## FIX-2 — "9,916" typo (QC finding P3-QC-2)

- File: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/SELF_ADVERSARIAL_PASS.md, table row 2, TEST cell.
- OLD (exact span):

```
9,216/9,916 -> 9,216/9,216 region-tile samples = 9 x 1,024 internal consistency
```

- NEW (exact text):

```
9,216/9,216 region-tile samples = 9 x 1,024 internal consistency
```

- Grounds: the historical quote is 9,216/9,216 (R1 F03 decode evidence;
  03_EVIDENCE/R2_F01_TERRAIN_COUNTER.json region_tiles_samples
  "9216/9216 samples identical for 9 region tiles = 9 * 1024"). Measured:
  "9,916" occurred exactly ONCE in the whole package pre-batch (this TEST
  cell) and ZERO times post-fix; there is no 9,916 anywhere.
- Bounded-authorized: human run contract section 14.
- File before: sha256 aa810fb6c554c4bea0bd0f38ec6b2c70e7375d3647331bc92bb5504f0d268a46, 6673 B
- File after (final; this file also carries FIX-4's row-9 clause): sha256 0d64ec62df854c2e5ac1c85a680bb021f1057980203a11fa285a35233cf12c1c, 6772 B

## FIX-3 — falsifiable timing inconsistency in the dependent-search record (PE-MASTER finding)

Files: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/R2_F01_TERRAIN_SAMPLE_COUNTER.md section 5 AND docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/BLAST_RADIUS.md section 1. The old text recorded
a byte-level search of "ALL 2,594 tracked repo files (133,463,531 bytes)"
that "found exactly ONE hit — the new AUDIT_ENTRYPOINT.md row added by
this run" — internally inconsistent: 133,463,531 bytes is the PRE-R2-row
worktree state, which cannot contain the R2 row (+2,161 B). Both records
were rewritten to carry the measured phases (a)-(d) explicitly with their
timings and byte counts; each section's structure and conclusion are
unchanged (ZERO live dependents; the only occurrences are correction
descriptions).

- OLD span (02_ANALYSIS/R2_F01_TERRAIN_SAMPLE_COUNTER.md section 5, exact):

```
A byte-level search of ALL 2,594 tracked repo files (133,463,531 bytes) for
"1,664,000", "1664000", "1.664.000" found exactly ONE hit — the new
AUDIT_ENTRYPOINT.md row added by this run, whose text DESCRIBES the correction
("1,664,000 -> 53,166,080"). A search of the 49-file R1 predecessor package
found exactly ONE occurrence — inside the corrected F03 statement itself (the
correction text quoting the superseded value). ZERO live dependents of the old
counter remain. Per-item dispositions in 02_ANALYSIS/BLAST_RADIUS.md.
```

- NEW (02_ANALYSIS/R2_F01_TERRAIN_SAMPLE_COUNTER.md section 5, exact full replacement):

```
The dependent-search record, timing-explicit (each value re-measured
2026-09-27): (a) Phase-1 search — pre-edit worktree, ALL 2,594 tracked repo
files (133,463,531 bytes), byte-level, literals "1,664,000"/"1664000"/
"1.664.000": ZERO tracked hits (the defect text lived only in the UNTRACKED
R1 package F03). (b) Post-Phase-4 re-verification — worktree WITH the R2 row
(all 2,594 tracked files, 133,465,692 bytes): exactly ONE tracked hit —
AUDIT_ENTRYPOINT.md line 30, this run's own R2 registration row, whose text
DESCRIBES the correction ("1,664,000 -> 53,166,080"); HEAD (cc747df)
contains ZERO hits; the R1 registration row (line 31) contains none. (c) The
R1 predecessor package (49 files, post-EDIT-A): exactly ONE occurrence — the
corrected F03 statement quoting the superseded value. (d) ZERO live
dependents of the old counter remain anywhere; the only occurrences are
correction descriptions. Per-item dispositions in 02_ANALYSIS/BLAST_RADIUS.md.
```

- OLD span (02_ANALYSIS/BLAST_RADIUS.md section 1, exact):

```
- SEARCH: all 2,594 tracked repo files (git ls-files at HEAD cc747df
  worktree; 133,463,531 bytes scanned) for the literals "1,664,000",
  "1664000", "1.664.000". RESULT: exactly ONE hit — AUDIT_ENTRYPOINT.md, the
  new row added by THIS run, whose text DESCRIBES the correction
  ("1,664,000 -> 53,166,080"). Additional search of the 49-file R1
  predecessor package: exactly ONE occurrence — inside the corrected F03
  statement itself (the correction text quoting the superseded value).
- DEPENDENTS: ZERO live dependents of the old counter remain anywhere.
```

- NEW (02_ANALYSIS/BLAST_RADIUS.md section 1, exact full replacement):

```
- SEARCH (timing-explicit record, each value re-measured 2026-09-27):
  - (a) Phase 1 — pre-edit worktree (git ls-files at HEAD cc747df), all
    2,594 tracked repo files, 133,463,531 bytes, literals "1,664,000" /
    "1664000" / "1.664.000": ZERO tracked hits (the defect text lived only
    in the UNTRACKED R1 package F03).
  - (b) Post-Phase-4 re-verification — worktree WITH the R2 row, all 2,594
    tracked files, 133,465,692 bytes: exactly ONE tracked hit —
    AUDIT_ENTRYPOINT.md line 30, THIS run's own new R2 registration row,
    whose text DESCRIBES the correction ("1,664,000 -> 53,166,080"). HEAD
    (cc747df) contains ZERO hits; the R1 registration row (line 31) contains
    none.
  - (c) The R1 predecessor package (49 files, post-EDIT-A): exactly ONE
    occurrence — the corrected F03 statement itself (the correction text
    quoting the superseded value).
- DEPENDENTS: (d) ZERO live dependents of the old counter remain anywhere;
  the only occurrences are correction descriptions.
```

- Grounds: every value re-measured by this batch's own READ-ONLY probes
  before any write (see SELF-VERIFICATION below): Phase-1 = 133,463,531 B
  with ZERO tracked hits; post-Phase-4 = 133,465,692 B with exactly ONE
  tracked hit (AUDIT_ENTRYPOINT.md line 30, the R2 registration row);
  HEAD = ZERO hits; R1 row (line 31) = none; R1 package = 49 files with
  exactly ONE occurrence (the corrected F03 statement).
- Bounded-authorized: human run contract section 14 (PE-MASTER-adjudicated
  finding).
- File before/after:
  - docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/R2_F01_TERRAIN_SAMPLE_COUNTER.md (also carries FIX-1): before sha256 10e77ed1bb6038101d15de04b4a731d91801b564c101fcb50421c8bbb9b31a12, 3993 B -> after sha256 fc5cec19d55e40c8241a7ac25e91f81ae04316ca76464873bd2261a5a300ff97, 4419 B
  - docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/BLAST_RADIUS.md (also carries FIX-4's section-2 clause): before sha256 9fdd9d2b5e635b2d6051ccd89be4a9feeecd43fc940267f371dfbf071ab98f01, 4463 B -> after sha256 34339b39519dbd474487e95081923ffc4c8f153350f9ba38d29454117a467d82, 5368 B

## FIX-4 — missing search-timing/self-hit disclosure for the bad equation (QC finding P3-QC-3)

Five sites: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/R2_F02_VCL_REVIEW_ERRATUM.md section 5; docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/BLAST_RADIUS.md section 2; docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/SELF_ADVERSARIAL_PASS.md row 9
TEST cell; docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/REPORT.md section 4 (the R2-F02 "Repo search:" sentence) and
section 7 (the bad-equation bullet). The existing 0-hit record is the TRUE
Phase-1 record and was NOT replaced — one timing/self-hit clause was ADDED
at each site (add-only; the surrounding substance is byte-unchanged).

- Site 1 — docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/R2_F02_VCL_REVIEW_ERRATUM.md section 5. Insertion point: directly after "— 0
  HITS." (before "The defect existed only in the human-pasted chat
  relay"). Inserted text (exact):

```
Search timing: Phase 1 (pre-edit
worktree, 133,463,531 bytes; the R2 entrypoint row and this package's own
records did not yet exist); post-run, the equation string appears ONLY in
this run's own correction records — inside THIS package (its erratum,
self-check, blast-radius, report, raw/control and evidence records) and in
the new AUDIT_ENTRYPOINT.md R2 row — always quoted AS the corrected-false
OLD_STATEMENT; no repo file asserts it.
```

- Site 2 — docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/BLAST_RADIUS.md section 2. Insertion point: directly after "RESULT:
  0 hits." (before "- DEPENDENTS: none"). Inserted text (exact):

```
Search timing: Phase 1
  (pre-edit worktree, 133,463,531 bytes; the R2 entrypoint row and this
  package's own records did not yet exist); post-run, the equation string
  appears ONLY in this run's own correction records — inside THIS package
  (its erratum, self-check, blast-radius, report, raw/control and evidence
  records) and in the new AUDIT_ENTRYPOINT.md R2 row — always quoted AS the
  corrected-false OLD_STATEMENT; no repo file asserts it.
```

- Site 3 — docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/SELF_ADVERSARIAL_PASS.md row 9, TEST cell. Appended to the TEST cell
  (exact appended text):

```
Phase-1 timing (133,463,531 B, pre-R2-row); post-run occurrences are this run's own quoted-as-false records only
```

- Site 4 — docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/REPORT.md section 4. Insertion point: directly after "the
  defect existed only in the human-pasted chat relay." (before "NO repo
  edit was required for this edge"). Inserted sentence (exact):

```
Search timing: Phase 1 (pre-edit worktree, 133,463,531 bytes; the
  R2 entrypoint row and this package's own records did not yet exist);
  post-run, the equation string appears only in this run's own
  quoted-as-false correction records — this package's own records and the
  new AUDIT_ENTRYPOINT.md R2 row — no repo file asserts it.
```

- Site 5 — docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/REPORT.md section 7. Insertion point: at the end of the
  bad-equation bullet, directly after "(a hit would have flagged an
  unlisted affected file).". Inserted sentence (exact, same sentence as
  site 4):

```
Search timing: Phase 1 (pre-edit worktree,
  133,463,531 bytes; the R2 entrypoint row and this package's own records did
  not yet exist); post-run, the equation string appears only in this run's
  own quoted-as-false correction records — this package's own records and
  the new AUDIT_ENTRYPOINT.md R2 row — no repo file asserts it.
```

- Grounds (measured): Phase-1 worktree tracked total = 133,463,531 B
  (133,465,692 − the 2,161-B R2 row); the R2 entrypoint row and this
  package's own records did not exist at Phase 1; post-run the equation
  string appears only in this run's own quoted-as-false correction
  records (tracked: exactly ONE regex hit = the entrypoint R2 row; literal
  variants 0; HEAD = 0; worktree-wide at batch start: 33 occurrences = 1
  entrypoint + 32 in this package); no repo file asserts it.
- Bounded-authorized: human run contract section 14.
- File before/after:
  - docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/R2_F02_VCL_REVIEW_ERRATUM.md: before sha256 849c03658ec8bf3494d3ca14c1b387de6accef09286713a654cf5328f5fc252b, 3848 B -> after sha256 f1c7dff548ce7120854697251ede6dcdb627e43b11b52e5bb9bf274786b10cc4, 4292 B
  - docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/BLAST_RADIUS.md: before sha256 9fdd9d2b5e635b2d6051ccd89be4a9feeecd43fc940267f371dfbf071ab98f01, 4463 B -> after sha256 34339b39519dbd474487e95081923ffc4c8f153350f9ba38d29454117a467d82, 5368 B (with FIX-3)
  - docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/SELF_ADVERSARIAL_PASS.md: before sha256 aa810fb6c554c4bea0bd0f38ec6b2c70e7375d3647331bc92bb5504f0d268a46, 6673 B -> after sha256 0d64ec62df854c2e5ac1c85a680bb021f1057980203a11fa285a35233cf12c1c, 6772 B (with FIX-2)
  - docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/REPORT.md: before sha256 8d34dae617357798863441bf636341a9e71ddfea4990cffdda134dcc30ffeb65, 14543 B -> after sha256 e7ebfb53ed8f81aa522dcec383e9c0dd0c0103a698b029c9e915fcc22ffe3056, 15221 B

## FIX-5 — this batch record

- File: 00_Control/QC_P3_FIX_BATCH.md (NEW — created by this batch).
- Before: ABSENT (the file did not exist in the pre-batch package).
- After: this file itself; a self-hash cannot be printed inside itself —
  its final hash + size are carried by the regenerated
  06_REPORT/MANIFEST_SHA256.csv row (computed LAST, after this record is
  final) and reported in the executor's handoff notice.
- Bounded-authorized: human run contract section 14 (the record of the
  bounded batch).

## FIX-6 — manifest refresh

- File: 06_REPORT/MANIFEST_SHA256.csv.
- Before: sha256 d6d302a713515c37f0b124e1f9ba69559914fa4b63186a9f1994a7ad9fc035e8, 5,513 B
  (measured directly pre-regeneration; the manifest is self-excluded from
  its own rows, so no manifest row carries this value).
- After: regenerated as the LAST step of this batch (after this record is
  final) by re-running the package's own UNCHANGED
  03_EVIDENCE/scripts/r2_manifest.mjs (node v22.22.0; same algorithm: full
  package walk, sort, repo-relative paths, header, row order,
  self-exclusion). Expected census: full R2 package file set = 35 files ->
  34 rows (= file count − 1), 0 stale / 0 missing / 0 unlisted. The
  manifest's own after-hash is self-excluded from the manifest and is
  reported in the executor's handoff notice.
- Bounded-authorized: human run contract section 14.

## SELF-VERIFICATION (re-measured facts; READ-ONLY probes, node v22.22.0)

Every value below was re-measured by this batch before any write; all
matched the dispatched values (NO HARD STOP).

- Tracked census: 2,594 tracked files (git ls-files at the HEAD cc747df
  worktree).
- Worktree byte counts: post-Phase-4 (with the R2 row) = 133,465,692 B;
  the R2 entrypoint row = AUDIT_ENTRYPOINT.md line 30 = 2,161 B incl. LF
  -> Phase-1 (pre-R2-row) = 133,463,531 B.
- Old-counter literals "1,664,000" / "1664000" / "1.664.000":
  - tracked worktree hits: exactly ONE — AUDIT_ENTRYPOINT.md line 30 (this
    run's own R2 registration row; text "1,664,000 -> 53,166,080");
  - HEAD (cc747df) tree: ZERO hits (git grep);
  - the R1 registration row (AUDIT_ENTRYPOINT.md line 31): ZERO;
  - the R1 predecessor package: 49 files, exactly ONE occurrence —
    F03_TERRAIN_TEXTURE_SCOPE.md line 104 (inside the EDIT-A corrected
    statement; the correction text quoting the superseded value);
  - worktree-wide at batch start (3,913 files excluding .git): 43
    occurrences total = 1 entrypoint + 1 R1-F03 + 41 in this package —
    all correction descriptions; ZERO live dependents anywhere.
- Bad-equation string (literals "491x12 + 24 + 252", "491*12 + 24 +
  252", "491 × 12 + 24" + regex /491\s*[x*×]\s*12\s*\+\s*24/):
  - tracked literal hits: 0; tracked regex hits: exactly ONE —
    AUDIT_ENTRYPOINT.md line 30 (the R2 row quoting it as false);
  - HEAD tree: ZERO (literals + regex);
  - worktree-wide at batch start: 33 occurrences = 1 entrypoint + 32 in
    this package — all quoted-as-false correction records; no repo file
    asserts it.
- dir_off: 123,369,726 (re-verified fresh from
  03_EVIDENCE/R2_F01_TERRAIN_COUNTER.json before writing FIX-1; count =
  58,451).
- Git state re-verified at batch end: HEAD = cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d
  (unchanged; NO git add/commit/push performed); staged = NONE; numstat:
  AUDIT_ENTRYPOINT.md 2/0, src/pesource/VegetationClimateDecoder.js 30/6,
  src/peworld/PEFoliageCore.js 20/5; tracked-modified set = exactly those
  three files (unchanged by this batch); untracked roots unchanged (incl.
  this R2 package and the R1 predecessor package).
- Frozen-source byte-identity re-verified: live git diff raw buffers ==
  the pinned patch hashes — src/peworld/PEFoliageCore.js
  27dee19810fded98fbe37e2013b742da500bcd107ad0c85feafbccdbf1ea96dd (3,377 B);
  src/pesource/VegetationClimateDecoder.js
  5978ff6b3cd9c787284b829e59d8cccf18d14d0fa956b6d760d86c4278728723
  (3,389 B).
- BEFORE_IMAGES re-hashed, untouched:
  BEFORE_F03_TERRAIN_TEXTURE_SCOPE.md
  5704d1c8f8166fe5bf1b88b0e8d0b13e7a0de3ac83463bdaf920831e863489df
  (9,807 B); BEFORE_EVIDENCE_INDEX.csv
  02e03b7d073e5579123a95b03383bac26cebff46e83a24b36a1693caedd05b08
  (7,536 B); BEFORE_MANIFEST_SHA256.csv
  3a91f3a3505f6f3d46edee246ff91e26b373586d32803e57e18d6da4d1c46462
  (8,520 B).
- The predecessor R1 package: NOT modified by this batch (read-only).
- Self-hit disclosure: THIS record quotes the old-counter literals and
  the equation string only inside its OLD/NEW span documentation above —
  always as quoted-false / correction-description spans; this record is
  itself one of this run's own correction records and adds no live
  dependent.
