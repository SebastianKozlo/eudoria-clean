# QC_REVALIDATION_R2 — PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916 (C13 fresh revalidation)

- REVALIDATOR: pe-master-auditor, FRESH context (independent of the
  correction generator; dispatched by PE-MASTER, revalidation leg C13).
- REVALIDATED RUN: PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916 (the
  bounded correction of PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915).
- Contract verified before execution: 00_CONTROL/REVALIDATOR_PROMPT_C13.md
  (9,738 B; SHA256 C79A1E400055C51E04702EBA637CE57B18DBEFBA41FD3EDA5518B836
  5D345940 — size+hash MATCH).
- Repo state (read-only checks; ZERO git operations by this revalidator):
  HEAD == origin/master == 91e2af0249f4242cf41eb1f96bc8a1a7f3e63839 == BASE.
  Working tree: 13 modified tracked files + 31 untracked paths inside the
  package (30 correction files + REVALIDATOR_PROMPT_C13.md itself) + the
  2 pre-existing untracked roots outside the package (untouched).
  `git diff` on 00_CONTROL/scripts = EMPTY (s01-s12 tracked scripts
  byte-unchanged; s13-s19 untracked new).
- Re-execution discipline: all re-runs performed with `python -B` in a TEMP
  COPY of the script tree (C:\Users\User\AppData\Local\Temp\opencode\
  c13_reval\reexec\), so NO executor evidence file was overwritten; every
  regenerated artifact was compared byte-wise (or field-wise where the
  artifact legitimately contains wall-clock durations) against the
  packaged originals. External D:\TESTAI materials were used as
  post-derivation comparators only, never as truth.

## 1. VERDICT

**QC_PASS_WITH_FINDINGS** — all 17 C13 items VERIFIED (17/17); every
load-bearing executor number reproduced or independently re-derived;
re-executions of s15/s16/s13/s17/s18/s19 reproduce the packaged evidence
byte-identically (or structurally identically where durations are part
of the artifact). Findings: 4 x P3 (hygiene; none contradicts any
correction claim; none touches a measurement). No P0/P1/P2.

## 2. The 17 C13 items — each with VERIFIED + method + measured vs claim

### Item 1 — BABYLENGUIN actual block boundary — VERIFIED
- Method: re-execution (s15, python -B) + own byte probe + row recount.
- Claim: block5 NiTexturingProperty 1408-1464; block6 NiSourceTexture
  1464-1517; block7 NiPixelData @1517; CSV 351 rows, 3 negative controls;
  479309 = 0x0007504D @1498 (bytes 4D 50 07 00); u32 @1517 = 0; file SHA
  A86C49384E62DF41339101B62E48BE6DCAE10E06B5F7CAC39DC627CF89635EA9.
- Measured: s15 re-run prints block5 1408-1464 / block6 1464-1517 /
  block7 NiPixelData gid=0 @1517; needle_479309_le_hits=[1498] (single
  occurrence in the whole file); 351 CSV rows; 3 NC all fail as designed
  (NC_TRUNCATED WalkFail EOF @1500; NC_CORRUPTED_TYPESTR_LENGTH WalkFail
  implausible length; NC_WRONG_VERSION WalkFail not 10.1.0.0). Regenerated
  CSV BYTE-IDENTICAL to the packaged file (SHA256 F5D89C67434E11924021A3
  3A263D28B7BE3E2909B94EFC791F8C31C634E439DE, 37,425 B; 3
  NEGATIVE_CONTROL rows present in both). OWN probes (PowerShell, not
  executor code): size 1,737,966 B; SHA256 A86C4938...5EA9 (match);
  u32 @1498 = 479309 (bytes 4D 50 07 00); u32 @1517 = 0; u32 @1464 = 0.
  ALL MATCH.

### Item 2 — BABYLENGUIN block7 GroupID = 0 @1517 — VERIFIED
- Method: own byte probe + re-execution (s15; s16 old-vs-v2).
- Claim: block7 GroupID = 0 @1517.
- Measured: u32 @1517-1520 = 00 00 00 00 = 0 (own probe); s15 re-run
  block7_groupid 0 @1517; s16 re-run: OLD model reproduces the false
  479309@1498 read [REPRODUCED], V2 gives 0@1517 [PASS]. MATCH.

### Item 3 — Exact ownership of bytes@1498 — VERIFIED
- Method: own byte probe (end-to-end string read).
- Claim: bytes@1498 = FileName tail 'MP' of 'LEN-SKIN_02.BMP' + low 2
  bytes of the Pixel Data link u32 (value 7 -> block 7 NiPixelData).
- Measured: u32 @1481 = 15 (FileName len); bytes @1485-1499 decode to
  ASCII 'LEN-SKIN_02.BMP' end-to-end (15/15 chars); bytes @1498-1499 =
  4D 50 = 'M','P'; bytes @1500-1503 = 07 00 00 00 = link u32 = 7;
  type-table block 7 = NiPixelData. MATCH.

### Item 4 — Has Bump Map Texture VALUE condition — VERIFIED
- Method: row recount (CSV trace) + s15 source read + adjudication read.
- Claim: block5 TextureCount=7, slot[5]=BUMP HasMap=0 -> BumpMap bytes
  NOT read -> block5 END=1464; discriminator demonstrated.
- Measured: CSV trace block5 TextureCount=7 @1428; slot[5].HasMap=0
  @1458; slot[1..6].HasMap=0 @1454-1459; NumShaderMaps=0 @1460; block5
  END=1464; ZERO Luma/BumpMat rows in the 351-row trace. s15 source:
  bump extras read only inside `if has == 1` (read_map kind="Bump").
  Discriminator IS in the evidence: BABYLENGUIN_GROUPID_ADJUDICATION.md
  C1A states an unconditional read would shift block5 end 1464->1488 and
  produce a false boundary before NiSourceTexture; measured end = 1464.
  NO FINDING REQUIRED. MATCH.

### Item 5 — Duplicate-field census — VERIFIED
- Method: re-execution (s13) + own row re-derivation from raw rows.
- Claim: 302 occurrences / 148 groups / 58 types / 21 load-bearing; the
  two NiSourceTexture "File Name" rows present + load-bearing; group
  classification coherent.
- Measured: s13 re-run summary identical (148/302/58/21; observed LB
  types NiMeshPSysData, NiPSysData, NiSourceTexture, NiTriShapeData);
  regenerated census CSV BYTE-IDENTICAL (SHA256 3F874FEC7844122EE16736
  E73F32D4A11226B4FF66040234FEDF2DB4F70CCF3B, 60,214 B). My own
  re-derivation from the PACKAGED csv's raw rows (my code, not s13):
  rows=302; groups=148; types_with_dups=58; LOAD_BEARING groups=21
  (17 niobject + 4 compound); occurrence_index contiguous 0..n-1 in
  every group; exactly one SURVIVOR per group; 7 coherent bucket
  combinations (each group single-valued). The two NiSourceTexture
  "File Name" rows: occ=0 cond='Use External == 1' SURVIVOR;
  occ=1 cond='Use External == 0' ver1=10.1.0.0 LOST — both
  group_load_bearing_at_10_1=LOAD_BEARING, reason "cond differs".
  ALL MATCH.

### Item 6 — Corrected field-identity implementation — VERIFIED
- Method: full source read (s13+s14+s16 in full; also s15, s17, s18, s19,
  s06, s04, s01, s02, run-local aggregate_world_slice_v2.py) + git diff.
- Claim: identity includes owner_type/field_name/occurrence_index/
  field_type/ver1/ver2/vercond/cond/template/schema_order per C4;
  conditional alternatives stay separate until value-condition
  evaluation; SUPERSEDES/DOES-NOT-REWRITE statements present; s01-s12
  untouched.
- Measured: s14 preserves every occurrence parent-first (NO name dedup);
  the census CSV carries all identity columns; decode_block evaluates
  field_included (version gate) then cond per occurrence — alternatives
  remain distinct until value-condition evaluation (empirically proven
  by s16: V2 keeps BOTH File Name occurrences, old kept 1). Statements
  verbatim in s13/s14/s15 headers. s01-s12: git diff EMPTY under
  00_CONTROL/scripts; frozen hypothesis sha 6DB2F1E3... unchanged.
  NOTE (observation, not a finding): s16 itself does not carry the two
  literal phrases — it is the executed old-vs-v2 comparison harness over
  the frozen s06 (read-only); the statements live in the successor
  tooling proper (s13/s14/s15). VERIFIED.

### Item 7 — NiSourceTexture physical denominator — VERIFIED
- Method: re-execution (s17) + OWN independent scan (revalidator parser).
- Claim: 45 blocks / 5 files; 44 external + 1 internal (204828.nif blk159,
  FileName="NPC_Animals_scaboreas_01_01.tga", link=160 -> NiPixelData).
- Measured: s17 re-run: bnt2 entries 5,596; v10.1 files 4,838;
  files_with_NiSourceTexture 5; blocks 45; tally TOTAL=45, EXTERNAL=44,
  INTERNAL=1, PASS=45, FAIL=0, AMBIGUOUS=0, CLOSURE_OK=2, CLOSURE_FAIL=3.
  Regenerated CSV BYTE-IDENTICAL (SHA256 FB9905369E2EAE0F85D3164DE931629
  F0E95026DD8BE7FF6BFBBF3CE6E10DECA; fc /b: no differences). OWN
  independent denominator scan (my own BNT2 walk + header/type-table
  parse over ALL 4,838 v10.1 payloads, cross-checked against the
  packaged NIF_VERSION_CENSUS.csv): exactly 5 files, exactly 45 blocks,
  block indices identical to the packaged CSV (204828.nif:[159];
  526644.nif:[64..74]; 527569.nif:[23..33]; 527865.nif:[25..35];
  528310.nif:[19..29]). ALL MATCH.

### Item 8 — All 45 NiSourceTexture rows — VERIFIED
- Method: row recount (every row parsed) + own byte spot-checks.
- Claim: 45 rows; 45 PASS / 0 FAIL / 0 AMBIGUOUS; branch counts sum to
  45; closure_status distinguishes block closure from whole-file closure
  ("3/5 files still fail whole-file" visible per-row); spot-check >= 6
  rows incl. 204828.nif blk159 + >= 1 external-branch row.
- Measured: 45 data rows; 45 PASS / 0 FAIL / 0 AMBIGUOUS; 44 EXTERNAL +
  1 INTERNAL = 45; next_GroupID=0 on all rows; link=-1 on all 44
  external rows; internal row = 204828.nif blk159, FN='NPC_Animals_
  scaboreas_01_01.tga', link=160 -> NiPixelData. closure_status per
  row: 2 files CLOSURE_OK (527569, 527865) + 3 files CLOSURE_FAIL
  (526644, 528310, 204828) — the disclosed 3/5 whole-file failure is
  visible per-row with NO hidden failures. OWN spot-check with MY OWN
  parser (not s14/s17) of 6 rows + 1 type lookup — 204828.nif blk159
  (gid=0@52402; UE=0@52418; FN len=31@52419; FN @52423; pixel link=160
  @52454; layout=6/mips=1/alpha=3/isstatic=1; end=52471; next gid=0;
  next type NiPixelData), 527569.nif blk23, 527569.nif blk33 (next
  NiAlphaProperty), 527865.nif blk25, 528310.nif blk19 (CLOSURE_FAIL
  file), 526644.nif blk74, + 204828.nif block 160 = NiPixelData: ALL
  ALL-MATCH. Method note: my first pass mis-assumed the HIST "Unknown
  Byte"[UE==0] field is read at 10.1.0.0; BASELINE_TYPE_TABLE shows it
  is ver<=10.0.1.0 (EXCLUDED) and the raw bytes confirm no such byte
  exists — the packaged end-offsets are correct; my parser was fixed,
  the executor model was right. VERIFIED.

### Item 9 — World-slice regression accounting 2363/2363 — VERIFIED
- Method: row recount (every row) + re-execution (s18 --chunk 0
  --nchunks 1) + own re-aggregation from both chunk sources.
- Claim: 2,363 rows; PASS 2,343 + FAIL 20 + AMBIGUOUS 0 + INFRA_
  UNRESOLVED 0 = 2,363; zero newly_failed / zero newly_closed / zero
  boundary_changes; no infra timeout counted as parser failure.
- Measured: packaged CSV 2,363 data rows, every row parsed: PASS 2,343 +
  FAIL 20 + AMBIGUOUS 0 + INFRA_UNRESOLVED 0 = 2,363 (per-row algebra);
  subset train 1,890 + hold 473; changed_boundaries=True: 0 rows;
  changed_field_interpretations=True: 0 rows; same_closure=True: 2,363;
  newly_closing 0; newly_failing 0; duplicates 0. FAIL rows: exactly 20
  = 12 ArkBlockError + 8 struct.error, identical old vs v2 per file.
  Frozen replay: frozen_run_closure agrees with old_now on 2,363/2,363.
  My s18 re-run (python -B, temp WORK; ~327 s; infra_stop=0): my chunk
  JSON vs the executor's run-local WORLD_SLICE_V2_CHUNK_0.json — same
  2,363 keys, ZERO structural field differences (only wall-clock
  dur_old/dur_v2 differ; medians identical 0.016 s — durations are
  measurements, not results). My own C11 re-aggregation from BOTH chunk
  sources reproduces the packaged CSV with 0 mismatches / 0 missing /
  0 extra. ALL MATCH.

### Item 10 — No unresolved infra timeout counted as parser failure — VERIFIED
- Method: row recount (INFRA scan) + re-execution + source read.
- Claim: part of item 9 + the C6 class separation in REPORT_CORRECTION_R1.
- Measured: zero INFRA* statuses anywhere in the packaged CSV (v2_status
  and old_now scanned); INFRA_UNRESOLVED=0 in the algebra; my s18 re-run
  infra_stop=0; s18 run_one() implements INFRA_RESOURCE_LIMIT as a
  separate class (never a parser FAIL); REPORT_CORRECTION_R1 C6 +
  BLAST_RADIUS state it explicitly. NO hidden failure. MATCH.

### Item 11 — LIVE_DOC tally — VERIFIED
- Method: own recount of the matrix + document reads.
- Claim: KEEP 5 / CLARIFY 6 / SUPERSEDE 4 / REVALIDATE 1 / NO_CHANGE 1
  (17 rows); AMEND-016/017 text matches.
- Measured: my recount of LIVE_DOC_IMPACT_MATRIX.csv (read in full; 17
  data rows) = 5/6/4/1/1 = 17 — EXACT MATCH. REPORT §5 and HANDOFF carry
  the same tally; AMEND-017 E2 states the same numbers and "NO edit
  required". The stale pre-AMEND-009 tally line inside PE_MASTER_REVIEW.md
  is correctly NOT edited (PE-MASTER-owned) and flagged via G17_OLD +
  SUPERSESSION_INPUTS_R2 #8. MATCH.

### Item 12 — s11/s12 SHA attribution — VERIFIED
- Method: rehash + erratum-discipline check.
- Claim: s11 = 6A8FD958E4EBA4A20BEE34BA4F531C4862B90E89B9339B25C3BD5A039
  6B8E0DB; s12 = CEC66531E3670872F51DF44F22724A468F59A7C097212BD560B37E0
  8A0753AAC; AMEND_LOG_R1 erratum discloses the old AMEND-009 text swap
  without rewriting history; SCRIPT_SHA256.csv values are correct.
- Measured: own Get-FileHash: s11 = 6A8FD958... (5,477 B); s12 =
  CEC66531... (26,530 B) — both match claims and SCRIPT_SHA256.csv
  rows. AMEND-009's historical text is still present UNMODIFIED in
  AMEND_LOG_R1.md (append-only held); the swap is disclosed in
  AMEND-017 E3 + FINDINGS_LOG F-20(a). MATCH.

### Item 13 — QC P3 tally — VERIFIED
- Method: full QC_AUDIT read + PRE_EDIT check + HANDOFF check.
- Claim: 2 OPEN P3 (F-QC-8, F-QC-9) + 4 fixed = 6 total; header
  previously "3 open", HANDOFF "7xP3"; corrections applied append-only
  via AMEND-016 (old text preserved with supersession pointers).
- Measured: QC_AUDIT.md enumeration: F-QC-4/5/6/7 (P3, FIXED) +
  F-QC-8/9 (P3, OPEN) = 6 P3 total. Header: "4 x P3 (fixed-in-QC);
  2 x P3 (OPEN: F-QC-8, F-QC-9)" + the AMEND-017 reconciliation note
  quoting the former "3 x P3 (OPEN, minor)". PRE_EDIT/06_REPORT__
  QC_AUDIT.md.AMEND-016.pre L9 preserves the old text ("3 x P3 (OPEN,
  minor)") — append-only held. HANDOFF: "6xP3 [4 fixed + 2 open
  (F-QC-8, F-QC-9) — AMEND-017 corrects the former '7xP3'/'3 open'
  drift...]". MATCH.

### Item 14 — NiflySharp path — VERIFIED
- Method: Test-Path + size + direct L61-62 read + citation sweep.
- Claim: NiObject.cs exists (1,674 B) at ousnius-NiflySharp-104d79f\
  NiflySharp\BaseTypes\NiObject.cs; L61-62 matches the cited Sync code;
  citations corrected per AMEND-016/017.
- Measured: file EXISTS, 1,674 B (my SHA256 659B3AA5F4E71A8CD80EAA721299
  1EBEFC7067E68E4AD8CDA0D716B03068FDF2). L61-62 read directly:
  `if (stream.Version.FileVersion >= NiFileVersion.V10_0_0_0 &&
  stream.Version.FileVersion < NiFileVersion.V10_1_0_114)` /
  `stream.Sync(ref groupId);` — byte-for-byte the cited code.
  Citations with the AMEND-016/017 path precision verified in QC_AUDIT.md
  (F-QC-2 evidence bracket), REPORT.md headline 2, NIF_10_1_BASELINE_SPEC
  .md framing paragraph, SOURCE_REGISTRY.md SRC-04, FINDINGS_LOG F-16
  (historical text preserved) + F-20(c). MATCH.

### Item 15 — WORK-AUDIT denominator — VERIFIED
- Method: physical full read of the external matrix + independent
  recompute of all 36 rows + row-by-row comparison with the packaged CSV.
- Claim: TOTAL 36 = CONFIRMED 31 + REJECTED 4 + UNCHECKED 1 (+1 confirmed
  vs the first audit's 30 = row 36; QC 24/8 vs 25/7 resolved in the
  executor's favor); WORKAUDIT_DENOMINATOR_RECOMPUTE.csv (36 rows)
  matches.
- Measured: I read D:\TESTAI\audits\work-audit\audyt-pe935-nif101-
  rosetta-r1-20260915-1040\01_TWIERDZENIA.md in full (comparator only).
  My recompute: CONFIRMED 31 (rows 1-24, 26-28, 30-31, 34, 36);
  REJECTED 4 (rows 25, 29, 32, 33); UNCHECKED 1 (row 35); PARTIAL 0;
  OTHER 0; TOTAL 36 = 31 + 4 + 1 — algebra closes. Row 36 is the QC
  24/8-vs-25/7 signature-split dispute, resolved by that auditor's own
  scan in the executor's favor (25/7) — consistent with F-14's
  "per-block CSV rows are authoritative" note and F-20(e).
  WORKAUDIT_DENOMINATOR_RECOMPUTE.csv (36 rows, read in full) matches my
  recompute ROW-BY-ROW (identical 31/4/1 classification per row; row 15
  properly CSV-quoted after the AMEND-018 ADDENDUM 2 quoting fix).
  MATCH.

### Item 16 — All 5 nif.xml SHA pins — VERIFIED
- Method: rehash (all five myself) + CSV row comparison.
- Claim: MOD D6B76A83...; HIST 1D5C8E58...; NifSkope 0DCE5092...;
  fo76utils 880C3167...; NiflySharp-bundled 752C7978... (570,454 B) at
  the REAL path ...\ousnius-NiflySharp-104d79f\nifxml\nif.xml; the old
  documented path does not exist; NIFXML_SOURCE_REHASH.csv rows match;
  SRC-04 annotation is append-only.
- Measured (my own SHA256 + size): MOD nifxml\nif.xml = D6B76A83EA5FBA
  DD21DA5F06348B236A1C43DA6BB76D108A2E8B749C22618DD6 (565,041 B);
  HIST nifxml_historical\nif.xml = 1D5C8E580B95D3EB8E1EEF06E1A12A8F2C06
  BF441FE97E3332080A5099D9FAF5 (401,093 B); NifSkope = 0DCE5092060E0C
  ABB95B8C07AF1BC59049C685D8D6E681771C816988505DDED3 (466,952 B);
  fo76utils = 880C316787950299A29291FEB609593949E726AC13E581ED36C6636A1
  57E7003 (667,577 B); NiflySharp-bundled = 752C79786CEB217641FD7E94BE4
  033898C97E9AA38025BF05F2CBEE9CFFBBF0D (570,454 B). ALL 5/5 MATCH.
  The old path (...\NiflySharp\nif.xml) DOES NOT EXIST (Test-Path
  false). NIFXML_SOURCE_REHASH.csv (read in full): 5 rows, all MATCH,
  measured hashes identical to mine, SRC-04 row carries the REAL-path +
  DOES-NOT-EXIST erratum text; SOURCE_REGISTRY.md SRC-04 carries the
  AMEND-017 annotation (append-only; the wrong path never existed in a
  package file). MATCH.

### Item 17 — Final provenance — VERIFIED
- Method: full rehash + physical census + coverage checks.
- Claim: MANIFEST 110 rows / 0 stale / 0 missing / L12 self-exclusion /
  0 .pyc / 0 __pycache__; physical census = manifest rows + manifest
  itself; SCRIPT_SHA256 covers s01-s19; EVIDENCE_INDEX covers the new
  artifacts; python -B everywhere.
- Measured: FULL independent rehash of all 110 MANIFEST rows — 110/110
  hash+size MATCH, 0 stale, 0 missing, 0 self rows (L12 self-exclusion
  held). Physical census: 112 files = 110 manifest rows + the manifest
  itself + 00_CONTROL/REVALIDATOR_PROMPT_C13.md (this revalidation's
  contract, added by PE-MASTER AFTER the AMEND-018 regeneration —
  expected; the "manifest rows + manifest itself" = 111 claim holds for
  the post-AMEND-018 state). 0 .pyc / 0 __pycache__ in the package
  (physical walk). SCRIPT_SHA256.csv: 19 rows s01-s19, every row
  re-hashed by me (19/19 MATCH). EVIDENCE_INDEX.csv: 108 rows, all
  re-hashed (0 stale/missing); covers ALL 13 new correction artifacts
  by name (BABYLENGUIN_BOUNDARY_REDERIVATION.csv, FIELD_IDENTITY_V2_
  NEGATIVE_CONTROL.csv, DUPLICATE_FIELD_IDENTITY_CENSUS.csv,
  NISOURCETEXTURE_FIELDIDENTITY_REGRESSION.csv, WORLD_SLICE_
  FIELDIDENTITY_REGRESSION.csv, CROSS_PUBLISHER_RETEST_FIELDIDENTITY
  .csv, NIFXML_SOURCE_REHASH.csv, WORKAUDIT_DENOMINATOR_RECOMPUTE.csv,
  BABYLENGUIN_GROUPID_ADJUDICATION.md, FIELD_IDENTITY_V2_BLAST_RADIUS
  .md, SUPERSESSION_INPUTS_R2.md, ENTRYPOINT_ROW_R2.md,
  REPORT_CORRECTION_R1.md); the 2-row difference vs the manifest is
  03_EVIDENCE/README.md + EVIDENCE_INDEX.csv itself (by construction).
  All my re-executions used python -B; NO scripts/__pycache__ was
  created. MATCH.

## 3. FINDINGS (all P3 hygiene; none contradicts any correction claim; none touches a measurement)

**F-R2-1 (P3) — Invalid UTF-8 byte 0x97 in STAGE_ACCEPTANCE_GATES.csv
(rows G16_OLD and G17_OLD).**
- Where: 06_REPORT/STAGE_ACCEPTANCE_GATES.csv, byte offsets 6794 and
  7179 — inside the AMEND-016-appended rows G16_OLD ("HISTORICAL state
  [0x97] one material counterexample reopened the gate...") and G17_OLD
  ("...the pre-AMEND-009 LIVE_DOC tally [0x97] both superseded..."),
  notes column.
- Claim contradicted: none (no number is affected) — hygiene only. This
  is the ONLY package file failing strict UTF-8 decode (all 112 files
  scanned).
- My evidence: strict `data.decode('utf-8')` fails with 'invalid start
  byte' at 6794; offending bytes 0x97 0x97 (cp1252 em-dash) instead of
  UTF-8 em-dash E2 80 94. PowerShell (cp1252) shows them as an em-dash;
  Python strict UTF-8 readers raise UnicodeDecodeError on this file.
- Failure mechanism: the AMEND-016 row text passed through a cp1252
  console/here-string path — the same slip class as the AMEND-018
  ADDENDUM 1 `$($h.Hash)` placeholder the executor themselves disclosed
  and fixed in ADDENDUM 3.
- Narrow correction: bounded AMEND entry (PRE_EDIT snapshot + SHA pair +
  s10 provenance regeneration) replacing the two 0x97 bytes with UTF-8
  E2 80 94; PE-MASTER may fold it into the persistence dispatch.
- Revalidation predicate: strict UTF-8 decode of the file succeeds and
  MANIFEST rehash is 0 stale after the entry.

**F-R2-2 (P3) — Stale script-row counts in REPORT.md §8 and gates G15
evidence (historical "12 rows" / "10 scripts" vs current 19).**
- Where: 06_REPORT/REPORT.md §8 ("...(SCRIPT_SHA256 now 12 rows), two
  new evidence CSVs..."); 06_REPORT/STAGE_ACCEPTANCE_GATES.csv G15
  evidence ("SCRIPT_SHA256.csv (10 scripts)").
- Claim contradicted: none of the correction's claims — both texts
  describe the AMEND-009..014-era state; the current state (19 rows
  s01-s19) is correctly recorded in AMEND-018, PROGRESS_STATE.md and
  SCRIPT_SHA256.csv itself. A reader of the current REPORT.md/G15 can,
  however, read "now 12"/"(10 scripts)" as present tense.
- My evidence: SCRIPT_SHA256.csv physically has 19 rows (all re-hashed);
  AMEND-018 documents the 19-row regeneration.
- Narrow correction: a one-line append-only pointer note at the next
  authorized edit (e.g. "[AMEND-018: SCRIPT_SHA256 now 19 rows s01-s19]")
  — or accept as historical text. PE-MASTER adjudicates; no measurement
  is affected.

**F-R2-3 (P3) — 03_EVIDENCE/README.md re-derivation guide does not
cover the correction scripts s13-s19.**
- Where: 03_EVIDENCE/README.md "How to re-derive any load-bearing
  claim" — bullets stop at s12 (the AMEND-011-era s10 template); no
  bullets for s13 (census), s15/s16 (BABYLENGUIN), s17 (C5), s18 +
  run-local aggregator (C6), s19 (C7).
- Claim contradicted: AMEND-018 states provenance was regenerated
  (SCRIPT_SHA256 -> README -> INDEX -> MANIFEST) — it was, but the README
  body is generated from the un-updated s10 template, so the guide
  silently omits the new tooling while the index/manifest cover it.
- My evidence: full read of README.md (39 lines; bullets s01-s12 only).
- Narrow correction: extend the s10 EVIDENCE_README template with
  correction-run bullets (expected outputs: 351-row CSV / 302-row
  census / 45-45 / 2,363-row algebra / 5-5 rehash) at the next
  provenance-regenerating amendment.

**F-R2-4 (P3) — NIF_10_1_BASELINE_SPEC.md still labels NiSourceTexture /
NiPixelData "NOT closure-validated this run — deferred" without a
pointer to the C5 lifting.**
- Where: 02_ANALYSIS/NIF_10_1_BASELINE_SPEC.md, NiSourceTexture and
  NiPixelData entries.
- Claim contradicted: none — historically true for the 2026-09-15 run;
  the correction lifted the NiSourceTexture deferral to structural
  level (C5 45/45; SUPERSESSION_INPUTS_R2 #6), but the spec entry
  carries no supersession pointer (unlike the same file's NiflySharp
  paragraph, which AMEND-016/017 annotated).
- Narrow correction: one appended note at the next authorized edit
  ("[2026-09-16 correction: NiSourceTexture structurally validated 45/45
  (s17); NiPixelData still deferred (1 block)]") — or accept as
  historical text.

### Non-finding observations (disclosed; no action required)

1. s16 does not carry the literal "SUPERSEDES TOOLING BEHAVIOR / DOES
   NOT REWRITE HISTORICAL HOLDOUT" phrases (present in s13/s14/s15);
   s16's header documents its role as the executed old-vs-v2 negative
   control over the frozen s06 (read-only) — the discipline is
   materially held (recorded under item 6 as VERIFIED-with-note).
2. s15's NC_WRONG_VERSION patch writes 0x0A020000 at byte 37 — inside
   the header-string text "10.1.0.0\n" — rather than the Version u32 at
   byte 41; the walker still fails the control exactly as designed (the
   header/version is no longer 10.1.0.0). The control is effective;
   only the patch mechanism is coarser than its label suggests.
3. My s18 re-run's chunk JSON differs from the executor's ONLY in the
   per-file wall-clock dur_old/dur_v2 fields (medians identical at
   0.016 s); all result fields are identical on all 2,363 files.
4. REVALIDATOR_PROMPT_C13.md is untracked and outside the (earlier-
   regenerated) manifest — expected (added by PE-MASTER after AMEND-018);
   this QC_REVALIDATION_R2.md likewise post-dates the manifest. The
   persistence-phase provenance regeneration will pick both up.

## 4. FULL_READ_LOG

Fully read (entire file, Read tool):
- 00_CONTROL/: REVALIDATOR_PROMPT_C13.md (contract), RUN_CONTRACT.md,
  AMEND_LOG_R1.md (455 L, AMEND-001..018 + addenda), FINDINGS_LOG.md
  (144 L, F-01..F-20), PROGRESS_STATE.md (156 L), SOURCE_REGISTRY.md,
  SCRIPT_SHA256.csv (19 rows).
- 00_CONTROL/scripts/ FULL SOURCE: s01, s02, s04, s06 (frozen decoder,
  incl. _fields_for L90-117), s13, s14, s15, s16, s17, s18, s19; plus
  run-local aggregate_world_slice_v2.py (93 L, read-only).
- 01_RAW/: NISOURCETEXTURE_FIELDIDENTITY_REGRESSION.csv (all 45 rows),
  CROSS_PUBLISHER_RETEST_FIELDIDENTITY.csv (all 5 rows),
  NIFXML_SOURCE_REHASH.csv (all 5 rows), WORKAUDIT_DENOMINATOR_
  RECOMPUTE.csv (all 36 rows), FIELD_VALIDATION_RAW.md (113 L);
  MANIFEST_SHA256.csv (all 110 rows — every row re-hashed);
  BABYLENGUIN_BOUNDARY_REDERIVATION.csv (all 351 rows parsed + field
  checks); WORLD_SLICE_FIELDIDENTITY_REGRESSION.csv (all 2,363 rows
  parsed programmatically); DUPLICATE_FIELD_IDENTITY_CENSUS.csv (all
  302 rows parsed programmatically);
  NIF_VERSION_CENSUS.csv (used programmatically as the v10.1 cross-check
  denominator — 4,838 rows; not a manual line read).
- 02_ANALYSIS/: BABYLENGUIN_GROUPID_ADJUDICATION.md (136 L),
  FIELD_IDENTITY_V2_BLAST_RADIUS.md (95 L), LIVE_DOC_IMPACT_MATRIX.csv
  (17 rows), NIF_10_1_BASELINE_SPEC.md (135 L).
- 03_EVIDENCE/README.md (39 L); EVIDENCE_INDEX.csv (108 rows, all
  re-hashed programmatically).
- 06_REPORT/: REPORT_CORRECTION_R1.md (197 L), SUPERSESSION_INPUTS_R2.md
  (169 L), REPORT.md (261 L), HANDOFF.md (171 L), QC_AUDIT.md (373 L),
  PE_MASTER_REVIEW.md (38 L), ENTRYPOINT_ROW_R2.md (22 L),
  STAGE_ACCEPTANCE_GATES.csv (26 rows).
- External comparator (post-derivation only, never truth):
  D:\TESTAI\audits\work-audit\audyt-pe935-nif101-rosetta-r1-20260915-1040
  \01_TWIERDZENIA.md (92 L, full).
- Physical files probed: BABYLENGUIN.NIF (hash + byte probes @1464,
  1481, 1485, 1498, 1500, 1516, 1517); Models.bnt (full rehash);
  NiflySharp NiObject.cs (L50-67 + size + hash); all five nif.xml pins.

Re-executed (python -B, temp tree; regenerated artifacts compared with
the packaged ones): s15, s16, s13, s17, s18 (--chunk 0 --nchunks 1),
s19. Executor run-local 02_WORK JSONs only READ (chunk JSON compared
field-wise; never modified — my re-run wrote to my own temp WORK).

Grep/targeted (not full manual reads): BASELINE_TYPE_TABLE.csv
(NiSourceTexture HIST block, 23 rows + version-gate lookup for "Unknown
Byte"); PRE_EDIT/06_REPORT__QC_AUDIT.md.AMEND-016.pre (header lines);
PRE_EDIT directory listing; EVIDENCE_INDEX vs MANIFEST set difference
(programmatic); UTF-8 strict validity scan over all 112 package files
(programmatic).

## 5. NOT_CHECKED (honest)

- s03/s05/s07/s08/s09/s10/s11/s12 source code in full (frozen earlier
  scripts untouched by the correction; s01-s12 tracked-diff verified
  EMPTY; s11/s12 hashes re-verified; s10's template behavior assessed
  via its generated outputs, not a full source read this session).
- The 2,475 non-slice v10.1 files beyond the 5 NiSourceTexture files
  (out of C5/C6 scope — the disclosed OPEN item, unchanged).
- Whole-file re-derivation of the 3 CLOSURE_FAIL NiSourceTexture files'
  non-NiSourceTexture blockers (the "unsupported controller/PSys types"
  attribution was accepted from the per-row evidence + my
  closure_status verification, not re-derived block by block).
- BASELINE_CONFLICT_RAW.csv / BASELINE_TYPE_TABLE.csv full manual
  row-by-row reads (prior QC + PE-MASTER scope; this revalidation used
  the NiSourceTexture schema rows and the census algebra already
  re-verified by two prior independent audits).
- Original engine source files (NiObject.cpp, NiStream.cpp, ...) — not
  re-read this session; the GroupID framing stands on the prior
  QC/PE-MASTER direct reads + F-02/F-03 and my physical BABYLENGUIN
  slot probes (all GroupID==0; framing A/B/C unaffected by the D
  retraction).
- R61/NifModelReader.js behavior, Textures.bnt, runtime/consumer
  semantics — out of this correction's scope, untouched.
- Remote publication state: not verified by me (local refs only; the
  correction is on-disk uncommitted by design; persistence is a later
  phase; no remote claim made by the executor, none verified).

## 6. Compact return line

RUN_ID: PE_935_NIF_10_1_WORKAUDIT_CORRECTION_R1_20260916 (C13 leg);
VERDICT: QC_PASS_WITH_FINDINGS; ITEMS: 17/17 VERIFIED; FINDINGS: 0xP0,
0xP1, 0xP2, 4xP3 (F-R2-1 UTF-8 byte 0x97 in STAGE_ACCEPTANCE_GATES.csv;
F-R2-2 stale script-row counts REPORT §8/G15; F-R2-3 README re-derivation
guide missing s13-s19; F-R2-4 BASELINE_SPEC deferred note without C5
pointer) + 4 non-finding observations; every executor claim reproduced
(byte-identical re-runs: s15/s16/s13/s17/s19 CSVs; s18 structurally
identical modulo wall-clock durations; all independent recomputations
match). Revalidator: pe-master-auditor, fresh context, zero git
operations, python -B throughout, no executor evidence modified.

