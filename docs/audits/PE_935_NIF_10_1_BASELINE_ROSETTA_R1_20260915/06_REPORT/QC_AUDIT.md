# QC_AUDIT — PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915 (INTERNAL_QC, fresh context)

- RUN_ID: PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915
- RUN_CLASS: LOAD_BEARING (RUN_TYPE FORENSIC_REFERENCE_BASELINE)
- QC executor: pe-master-auditor (fresh context, dispatched by PE-MASTER)
- QC date: 2026-09-15
- QC verdict (top, per contract): **QC_PASS_WITH_FINDINGS**
  - 0 × P0; **1 × P1 (OPEN — requires PE-MASTER adjudication)**;
    2 × P2 (OPEN); 4 × P3 (fixed-in-QC); 3 × P3 (OPEN, minor).
- Countercheck tools: PE-MASTER-auditor's OWN code, OUTSIDE the project
  tree (C:\Users\User\AppData\Local\Temp\opencode\pe_master_countercheck\
  qc_nif_baseline_r1\): qc_walk.py (own BNT2 walker + version/type scan of
  the FULL corpus), qc_type_compare.py (census/baseline/R61 algebra),
  qc_holdout.py (holdout recomputation + OWN split reconstruction),
  qc_slice_decoder.py (INDEPENDENT hand-written world-slice decoder with
  full-file closure, layouts derived from MY OWN reading of the pinned
  HIST nif.xml; run over all 2,363 slice files), qc_tex_headers.py (raw
  byte scan of every ArkTexture block header in the slice),
  qc_negative_controls.py (my own NC sets A/B/C + EE2 header reader),
  qc_provenance.py (full provenance rehash). Executor scripts s01–s10
  were READ (L3) but never used as oracles; the single s07 'ALL' re-run
  (item 6, reproduction leg) was executed with backup/restore and
  produced a byte-identical evidence file.

## 1. Re-derivation table (claim | executor number | my independent method | my number | verdict)

| # | Claim (location) | Executor | My method | Mine | Verdict |
|---|---|---|---|---|---|
| 1 | Models.bnt pin (G0) | 395,412,868 B; SHA256 C950A8C2…BEE0 | own SHA256 (4th independent measurement) | identical | MATCH |
| 2 | BNT2 walk (G1) | 5,596 entries; EOF-exact; 0 gaps/overlaps; 100% coverage | own walker, own invariants | 5,596; DirOffset 395,262,727; trailing 0; interior gaps 0; overlaps 0 | MATCH |
| 3 | Version census (G1) | 4,838×10.1.0.0 / 757×4.1.0.12 / 1×4.0.0.2; 0 failures | own header scan of all 5,596 payloads | identical; per-file vs NIF_VERSION_CENSUS.csv: 5,596/5,596 MATCH | MATCH |
| 4 | Type census (G5) | 76 types; 364,062 blocks; per-type blocks/files | own type-table decode of ALL 4,838 files | 76 types; 364,062 blocks; per-type blocks AND files: 76/76 types, 0 mismatches | MATCH |
| 5 | UV/NumGroups/GID0 (census) | UserVersion 0 ×4838; NumGroups 0 ×4838; first GID 0 ×4838 | my scan | identical (0/0/0 distributions) | MATCH |
| 6 | Baseline algebra (G4/G10) | 10,890 field rows; 425−76=349 not-observed | my own recomputation from BASELINE_TYPE_TABLE.csv | 10,890 rows; HIST table types = 423 applicable-with-fields + 2 observed UNDEFINED_IN_SCHEMA; 423−74=349; not-observed SET exactly equals applicable−observed (0 extra, 0 missing) | MATCH (label imprecision → AMEND-005(d); s04's own summary "442" = schema-level incl. 19 zero-field types, unreconciled in reports → F-QC-8) |
| 7 | Classification (G8) | "25 CONFIRMED + 7 MindArk + 44 UNKNOWN" | my status tally from NIF_10_1_STANDARD_COVERAGE.csv | 23 CONFIRMED / 6 MINDARK / 3 STANDARD_NAME_CUSTOM_LAYOUT_PENDING / 44 UNKNOWN (incl. NiVertexMorphExtraData) | **MISMATCH (claim drift)** → fixed AMEND-005(a) |
| 8 | MindArk set identity (§23 item 4) | 7 types | my census ∩ matrix | exact set {NiArkAnimationExtraData, NiArkImporterExtraData, NiArkTextureExtraData, NiArkViewportInfoExtraData, NiArkShaderExtraData, NiArkBillboardNode, NiVertexMorphExtraData}; NO_MOD_SCHEMA census rows = exactly NiArkBillboardNode + NiVertexMorphExtraData | MATCH |
| 9 | Census-set vs R61-set (Q-F / LIVE_DOC row 5) | "76 = v10.1-only count coincidentally equal to era-mixed claim" | my census ∪ R61 manifest (whole corpus) | the SETS are IDENTICAL (R61 union = census v10.1 set = 76 names; all non-10.1 types ⊆ v10.1 types) | **RESOLVED: identity, not coincidence** (LIVE_DOC row 5 recommendation can be strengthened) |
| 10 | NiCamera (WORLD_VIEWER) | 0 occurrences in v10.1 | my scan + R61 whole-corpus | 0 in my 76-type scan; absent from R61 manifest entirely | MATCH |
| 11 | World slice (G6/G7) | 2,363 = TRAIN 1,890 + HOLDOUT 473; closure 1,876+467=2,343; 20 blocked (14+6); hypothesis_sha 6DB2F1E3… | recomputed from WORLD_SLICE_VALIDATION.json + OWN split reconstruction from my own payload SHA256s + rehash of s04‖s06 | all identical (blocked list matches exactly; my split sets == run sets, 0 differences; 505775.nif lands in TRAIN NATURALLY); sha256(s04‖s06)=6DB2F1E3… EXACT | MATCH |
| 12 | s07 determinism | TRAIN/HOLDOUT numbers from single ALL-pass | re-ran s07 'ALL' (backup/restore discipline) | TRAIN 1,876/1,890; HOLDOUT 467/473; regenerated WORLD_SLICE_VALIDATION.json **byte-identical** (SHA 674E0038…); original restored byte-identical | MATCH (reproducibility proven by re-execution) |
| 13 | HOLDOUT_RESULTS per-type (G7) | 29 type rows | my recomputation from JSON per-file records | 29/29 rows, 0 diffs (train/hold files+blocks) | MATCH |
| 14 | Importer tail (C-07/F-07) | 41B (13B + 7×f32) in 2,343/2,343; wiki 38B superseded | my independent closure harvest (final-path only) | tail=41 in 2,361/2,361 of my closed files; 38 accepted in ZERO paths; version strings Gamebryo_1_1 2,320 / 4.1.0.12 36 / 4.0.0.2 5, garbage 0 (their 2,302/36/5 + 18 = their 20 blocked − 2 my-blocked: arithmetic exact) | MATCH — 41B byte-CONFIRMED; 38+3 split = mis-attribution CONFIRMED (both consume identical bytes; my parse never needs the 38-split) |
| 15 | ArkTexture count formula (C-08/F-09) | count==(field2>>8)&0xFFFFFF in 2,319/2,343 (99.0%); "24-block variant family" (17× count=1/field2=0; 7× count=3; f1=15 ×24 / 0x1000000 ×3; 24 garbage refs) | my closure harvest + RAW byte scan of every ArkTexture header in the slice + byte dumps of variant files | **formula TRUE count in 2,361/2,361 of my closed files (100%); zero deviations; zero garbage refs; zero f1 anomalies.** Byte dumps (510661, 510636, 27876, 15522; and counter-example 386950 with a real entry) show: in every C=0 / C=0xFF "variant" file the bytes immediately after the ArkTexture header are `00 00 00 00 | 0F 00 00 00 | "ArkViewportInfo"` = the NEXT BLOCK's GroupID + canonical name → true count = 0 = field2>>8 | **MISMATCH — the variant family is a candidate-order artifact of the run's own decoder (F-QC-1, P1)** |
| 16 | TopObjects footer (F-11) | count=1, root=block0 NiNode in 2,343/2,343 | my closure footer (enforced EOF-exact) | ntop=1 ×2,361; top ref=0 ×2,361 | MATCH |
| 17 | GroupID framing (C-01, load-bearing) | engine 5.0.0.6 ≤ v < 10.1.0.114; PE always 0; modern schema wrong (since=10.1.0.114); HIST lacks it | direct engine-source read (NiObject.cpp L134–143: `GetVersion(5,0,0,6) && < GetVersion(10,1,0,114)` → u32 GroupID) + MOD nif.xml L3882 (`Group ID since="10.1.0.114"`) + HIST grep (no NiObject GroupID) + my closure (gid==0 enforced, all blocks) | engine condition EXACT as claimed; MOD mis-version EXACT as claimed; HIST omission EXACT as claimed; bytes agree | MATCH — C-01 fully CONFIRMED at the primary source (except the NiflySharp sub-claim → F-QC-2) |
| 18 | NiStream load order (Q-D) | LoadHeader → LoadRTTI → LoadObjectGroups → per-block LoadBinary → LoadTopLevelObjects | direct source read | NiStream.cpp: LoadHeader L303 (UserVersion if ≥10.0.1.8 at L335; NumObjects L355), LoadRTTI L412 (u16 count), LoadObjectGroups L470 (u32 count + u32 sizes), LoadTopLevelObjects L362 (u32 count + u32 LinkID); LoadStream calls in order L508→L524→L531→L566 | MATCH |
| 19 | ApplyMode/TextureCount (C-04/F-10) | ApplyMode u32 ∈ {0,2}; TextureCount=7 | my closure harvest | apply mode {2: 7,098, 0: 136}; texture count 7 ×7,234 | MATCH |
| 20 | NiVertexColorProperty (C-05) | 10B; width-identical split ambiguity disclosed | my closure harvest (block tail width) | width 10 ×2,556 (u16+u32+u32 schema split works everywhere) | MATCH (semantic split stays OPEN — correctly disclosed) |
| 21 | NiArkBillboardNode (F-10/matrix) | NiNode + u16 mode, 22/22 | my closure | 22 blocks accepted with u16 mode (values {0: 12, 2: 10}), 7 slice files | MATCH |
| 22 | HasShader=0 / ntp=3×ntri | =0 ×8,605; relation observed in samples | my closure harvest | hasShader 0 ×8,794; NumTrianglePoints==3×NumTriangles 8,772 ok / 0 bad | MATCH (relation now verified at scale, not just samples) |
| 23 | Cross-publisher (G14/§14) | EE2 lodtest.nif = 10.1.0.0, 7 blocks, CLOSURE_OK with frozen layouts | my own byte header/footer read | header "Gamebryo File Format, Version 10.1.0.0"; ver 0x0A010000; uv=0; 7 blocks; types [NiNode, NiLODNode, NiTriShape, NiTriShapeData, NiRangeLODData]; footer ntop=1 ref=0. (lodtest-skinned: 14 blocks, same version.) EE2-side 7-block CLOSURE itself = executor evidence (my decoder does not implement NiLODNode/NiRangeLODData) | MATCH (header/footer/claim-consistent) |
| 24 | Negative controls (G13) | NC-A 4, NC-B 4, NC-C 6 executed, failing as required | my OWN control sets on my own tools | my NC-A 4/4 (synthetic truncation/corrupt-count/bad-magic fail my walker; base passes), NC-B 4/4 (corrupt version/nbt/nb/truncated header fail my scanner), NC-C 4/4+control (extra-count +1, footer-count flip, importer strlen flip, GroupID flip each FAIL my closure; unmodified passes) | MATCH — methodology independently reproduced |
| 25 | Anti-circularity (G2) | census from own walker before manifest comparison | code read s01–s05 + timestamps | s01/s02/s03 read NO manifest/parser file; s05 is the only manifest reader (post-hoc); 02_WORK mtimes: census 14:03–14:04 < crosscheck 14:05:46 < validation 14:50 < cross-publisher 14:52 | MATCH |
| 26 | Provenance (G15/§21) | 10 script rows, 37 index rows, 39 manifest rows, 0 stale, self-exclusion L12 | full rehash of all rows vs disk | SCRIPT_SHA 10/10 ok; EVIDENCE_INDEX 37/37 ok; MANIFEST 39/39 ok; self-exclusion ok; **physical 45 files incl. 5 .pyc at freeze** ("no __pycache__" claim false → AMEND-003) | MATCH post-fix |
| 27 | 16 pinned sources (G3/Q-G) | SOURCE_REGISTRY rows | existence + spot-hash | all 5 nif.xml variants exist with EXACT claimed hashes (MOD D6B76A83…, HIST 1D5C8E58…, NifSkope 0DCE5092…, NiflySharp 752C7978… at `…\nifxml\nif.xml`, fo76utils 880C3167…); engine NiStream.cpp/NiObject.cpp exist; SDK + EE2 samples exist; Models.bnt pin matches | MATCH |
| 28 | NiflySharp 10.1 handling (F-03/C-01 note) | "NiHeader reads only NumGroups after array → would misalign blocks on real 10.1.0.0 files" | direct code read (Q-E) | **FALSE**: NiflySharp 104d79f reads per-block GroupID — `NiObject.cs` Sync: `if (vfile >= NiFileVersion.V10_0_0_0 && vfile < NiFileVersion.V10_1_0_114) stream.Sync(ref groupId);` — the range COVERS 10.1.0.0. The header itself reads only NumGroups (true) but each block syncs its own GroupID; no misalignment on 10.1.0.0 | **MISMATCH (F-QC-2, P2)** |

## 2. Findings

**F-QC-1 (P1, OPEN — to PE-MASTER; NOT fixed in QC — science).**
"24-block ArkTexture variant family" is a decoder candidate-order
artifact, not a corpus fact; the count formula holds 100% in-slice.
- Where: FINDINGS_LOG F-09; BASELINE_CONFLICT_MATRIX C-08;
  PARSER_GAP_MATRIX row 7 (PARSER_FIELD_WRONG_ON_24_BLOCKS); REPORT §2.7
  ("ArkTexture count = (field2>>8)&0xFFFFFF in 2,319/2,343 (99.0%) …
  24-block variant family (NEW open finding)"); HANDOFF TOP-10 gap (1);
  LIVE_DOC_IMPACT_MATRIX row 12 (REVALIDATE "99% not 100%").
- Contradicted claim: (a) formula matches in only 99.0%; (b) a real
  variant family exists with count from field1/numfield, f1=15/0x1000000
  entries and garbage refs; (c) the JS/R61 parser formula "would
  mis-read the 24 blocks" (defect class).
- Physical counter-evidence (my own bytes, no executor tooling):
  raw scan of ALL slice ArkTexture blocks found 32 blocks with
  field2>>8==0: 24 with (A,B,C,pad)=(3,1,0,0) and 8 with
  (3,0xFFFFFF00,0xFF,0). Byte dumps of 510661/510636/27876 (C=0 family)
  and 15522 (C=0xFF family) show the identical canonical sequence right
  after the header: `00000000 0F000000 "ArkViewportInfo"` = next block's
  GroupID=0 + name-length 15 + canonical name. TRUE count = 0 =
  (field2>>8)&0xFFFFFF. The executor's accepted count=1 (from field1=1)
  or count=3 (numfield) parses those bytes as "entries" — producing
  exactly their recorded anomalies (entry f1 = 0x0F = **15**; garbage
  f2/ref = the "ArkViewport…" ASCII; 24 OOR refs) — and its elastic
  viewport-ext boundary search then absorbed the remainder, so the
  file still closed byte-totally. My decoder (candidates ordered
  field2>>8-first) closes the same files with count=0, canonical
  viewport names, **zero** garbage refs and **zero** f1 anomalies
  (2,361/2,361 formula==true count). Counter-example 386950 (C=0x100):
  ONE real entry ("geodoor_0_BASE", f2=-1, ref=7) followed by
  gid+name — the formula count=1 is byte-true there; count-1 blocks
  exist and the formula reads them correctly.
- Failure mechanism: s06 `ark_candidates` orders count sources
  (A=numfield, B=field1, C>>8, C&0xFFFFFF, 0) and backtracks on
  full-file closure only; with a variable-length ArkViewportInfo
  ext search downstream, a mis-counted texture block can still
  close, so closure cannot arbitrate this boundary. The run's own
  NEGATIVE_CONTROL_RAW "residual honesty notes" anticipated the
  class ("greedy candidate ORDER could in principle accept a
  byte-compatible but semantically mislabeled split") — but F-09
  promoted the artifact to a corpus finding.
- Blast radius: (a) 24 of the 2,343 "closure OK" files carry a
  byte-mis-attributed ArkTexture/ArkViewportInfo boundary (file
  structure totals unchanged); (b) the supersession of the prior
  wiki claim "field2>>8 4,838/4,838 PERFECT" is itself unfounded at
  slice level (formula = 100% in-slice; corpus-wide outside the
  slice remains untested — 2,475 non-slice files); (c) PARSER_GAP
  row 7's defect verdict is INVERTED (the JS/R61 formula reads those
  blocks CORRECTLY; it is s06's candidate order that mis-reads
  them); (d) the recommended correction run
  PE_935_NIF_PARSER_TEXTURECOUNT_24BLOCK_CORRECTION_R1 rests on a
  false premise (a fallback is harmless, but there is no family to
  investigate in-slice); (e) HANDOFF TOP-10 gap (1) and LIVE_DOC
  row 12's REVALIDATE direction are wrong in-slice.
- Narrow correction (for PE-MASTER to dispatch): re-adjudicate F-09/
  C-08/PARSER_GAP row 7/REPORT §2.7/HANDOFF/LIVE_DOC row 12 against
  the QC byte dumps; restore the formula to 100% (slice-scoped,
  corpus-wide test as an explicit open item); drop or re-scope the
  24-block correction run; PE-MASTER may direct a bounded amendment
  run (I did NOT alter these science rows — only status-pointer
  notes added under AMEND-005).
- Revalidation predicate: an independent decoder with
  field2>>8-first ordering + viewport-name validation must close
  the 32 zero-count blocks with count=0 and canonical
  "ArkViewportInfo" names at the boundary (my tools + JSON outputs
  already satisfy this; re-derivable from qc_tex_headers.py +
  qc_slice_decoder.py + the recorded dumps).

**F-QC-2 (P2, OPEN — to PE-MASTER).** NiflySharp sub-claim in C-01
is false.
- Where: FINDINGS_LOG F-03 NOTE; BASELINE_CONFLICT_MATRIX C-01
  ("NiflySharp header read would misalign on real 10.1.0.0 files");
  NIF_10_1_BASELINE_SPEC.md ("NiflySharp's header read would
  misalign…"); HANDOFF ("NiflySharp 10.1 header bug — external,
  documented"); REPORT §2.2 ("NiflySharp's header reader would
  misalign on real 10.1.0.0 files").
- Claim contradicted: NiflySharp (104d79f) misaligns on real
  10.1.0.0 files.
- Evidence: `…\NiflySharp\BaseTypes\NiHeader.cs` reads (after type
  index) strings (≥20.1.0.1) + groupSizes (≥5.0.0.6) — true so far;
  but block deserialization includes the per-block u32:
  `…\NiflySharp\NiflySharp\NiObject.cs` (Sync):
  `if (stream.Version.FileVersion >= NiFileVersion.V10_0_0_0 &&
  stream.Version.FileVersion < NiFileVersion.V10_1_0_114)
  stream.Sync(ref groupId);` — 10.1.0.0 IS inside the range.
  NiflySharp parses real 10.1.0.0 block streams without misalignment
  (its range differs from the engine's only for 5.0.0.6–9.x files,
  which is a separate, unstated nuance).
- Failure mechanism: the executor stopped the analysis at the header
  reader and did not read NiObject.Sync.
- Blast radius: 4-5 doc locations; C-01's core verdict (engine range,
  physical presence, modern mis-version, historical omission) is
  UNAFFECTED and stands confirmed; only the NiflySharp impact
  statement is wrong.
- Correction: replace the NiflySharp note with the actual code
  citation (above) in a bounded amendment; the "untested against real
  Gamebryo-1.x-era files" hedge in F-03 can stay as a test-gap note.

**F-QC-3 (P2, OPEN — to PE-MASTER).** Undisclosed post-s03 edit of a
census CSV column (provenance/reproducibility).
- Where: 01_RAW/ENTROPIA_NIF_10_1_TYPE_CENSUS.csv column
  `baseline_type_present` (YES_HIST / NO_MOD_SCHEMA) vs
  00_CONTROL/scripts/s03_type_census.py line 190 (writes
  `PENDING_BASELINE`).
- Claim contradicted: EVIDENCE/README "run s03_type_census.py; expect
  … ENTROPIA_NIF_10_1_TYPE_CENSUS.csv" (re-derivation) and §21
  provenance order (artifact = pinned-script output); AMEND-002's
  "No evidence file modified post-freeze".
- Evidence: grep — no packaged script writes YES_HIST; the packaged
  s03 writes PENDING_BASELINE; therefore the packaged CSV is not the
  byte-output of the pinned s03 (either hand-edited or produced by an
  unshipped s03 revision).
- Blast radius: reproducibility of one labeling column only — the
  measurement columns (blocks/files/min/max/examples) match
  TYPE_CENSUS_SUMMARY.json AND my independent recount (76 types,
  364,062 blocks, 0 mismatches); the NO_MOD_SCHEMA values are
  consistent with BASELINE_GEN_SUMMARY (observed_not_in_mod_schema =
  the 7 Ark types) and observed_not_in_hist_schema =
  NiArkBillboardNode+NiVertexMorphExtraData — so the values are
  correct, the edit was just undisclosed.
- Correction: disclosed as AMEND-007 (no file change by QC);
  PE-MASTER may require either a re-run of s03 (restoring
  PENDING_BASELINE + a separate post-hoc labeling table) or an
  explicit amendment normalizing the column provenance.

**F-QC-4 (P3, FIXED in QC).** "no __pycache__" claims false at
executor freeze.
- Where: REPORT §8; STAGE_ACCEPTANCE_GATES G15 evidence;
  PROGRESS_STATE "Package complete per §20 layout (40 files; …; no
  __pycache__)".
- Evidence: 5 .pyc physically present (s01,s02,s03,s04,s06;
  SHAs recorded in AMEND-003).
- Fixed: __pycache__ removed (build artifacts, never evidence;
  MANIFEST always excluded .pyc); claims corrected to the factual
  state; provenance regenerated (AMEND-003; post-cleanup package =
  40 files + manifest itself; rehash 0 stale).
- Note: PE-MASTER's dispatch said "46 files" — QC physical census =
  **45** at freeze (40 + 5 .pyc), independently counted twice.

**F-QC-5 (P3, FIXED in QC).** PROGRESS_STATE self-contradiction:
top section "FINAL STATE (COMPLETE)" vs middle "Current state:
§8/§9/§10 IN PROGRESS". Fixed by relabeling the mid-run snapshot as
HISTORICAL/superseded (AMEND-004); stage log preserved.

**F-QC-6 (P3, FIXED in QC).** G6 = PASS did not carry the disclosed
NiSourceTexture deferral in its status. Relabeled
PASS_WITH_DISCLOSED_DEFERRAL with explicit follow-up recommendation
(AMEND-006). Decision rationale: the §8 minimum family list includes
"source texture"; census-level-only validation with 45 blocks / 5
files is a material scope reduction that the status label must carry
(deferral was disclosed in prose in 3 places, which is why this is
P3, not P2).

**F-QC-7 (P3, FIXED in QC).** Claim-vs-artifact number drifts
(AMEND-005): "25 world-slice standard types CONFIRMED" → 23 (+3
PENDING disclosed); "17 matrix rows / 8 MATCHES / 4 UNVERIFIED" →
16 rows / 7 MATCHES / 3 UNVERIFIED (+2 mis-attribution, +1 semantic
gap, +2 scope, +1 defect under QC challenge); "KEEP 8 / CLARIFY 5 /
SUPERSEDE 4" → KEEP 4 / CLARIFY 6 / SUPERSEDE 4 / REVALIDATE 2 /
NO_CHANGE 1; C-11 "5320 raw conflict rows" → 5513; F-01 "175.nif" →
"16175.nif" (byte values unchanged); G4 "425 HIST-applicable" →
label precision (423 + 2 UNDEFINED_IN_SCHEMA).

**F-QC-8 (P3, OPEN — to PE-MASTER, minor).** Remaining counting-mode
ambiguities NOT corrected by QC (would require choosing an
interpretation): (a) G12/REPORT "REQUIRED_FOR_STATIC_WORLD = 23 type
rows" — the table has 24 capability rows naming 28 distinct types
(counting mode unclear); (b) BASELINE_GEN_SUMMARY's schema-level
"hist_types_applying_to_10_1 = 442" vs the materialized 423/425
(19 zero-field types) is unreconciled in any report; (c) the "7
MindArk" rollup includes NiVertexMorphExtraData whose coverage-CSV
status is UNKNOWN (REPORT wording fixed in QC, but the headline
"7 = STRONGLY_SUPPORTED" rollup remains in the extension matrix
framing).

**F-QC-9 (P3, OPEN — informational, adjudication optional).**
Closure counts are decoder-search-dependent, not corpus invariants.
Executor decoder: 2,343/2,363 (20 blocked: 14 train + 6 hold).
QC independent decoder (same framing: GroupID + TopObjects +
EOF-exact + ref ranges; different candidate ordering and caps):
2,361/2,363 (blocked only 386950.nif + 386951.nif — sibling files,
"trailing 23"; the executor closes both). The blocked sets are
DISJOINT; every one of the 2,363 world-slice files closes under at
least one of the two independent decoders. Consequences: (a) the
G6/G7 headline (99.2%) is honest for the frozen decoder but should
not be read as a corpus property; (b) the executor's 20 PARSE_BLOCKED
files are closable — the per-file reasons ("deep ArkAnimation-variant
territory") reflect the frozen decoder's search limits; (c) BABYLENGUIN.NIF
(CROSS_PUBLISHER_TEST) fails at block 7 GroupID=479309 — a NONZERO
engine GroupID in a non-PE 10.1.0.0 file, which is *positive*
evidence for GroupID realism but contradicts the "SDK samples fail
only at types ABSENT from the Entropia corpus" wording (REPORT §2.4
/ F-12).

## 3. Hygiene amendments executed by QC (details in AMEND_LOG_R1.md; PRE_EDIT snapshots in 00_CONTROL/PRE_EDIT/)

- AMEND-003: __pycache__ removal (5 .pyc, SHAs logged) + factual
  file-count/pycache claims (PROGRESS_STATE).
- AMEND-004: PROGRESS_STATE historical-snapshot relabel (Q-B).
- AMEND-005: claim-vs-artifact number corrections (REPORT.md,
  HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv, FINDINGS_LOG.md,
  BASELINE_CONFLICT_MATRIX.csv) — SHA pairs in the log.
- AMEND-006: G6 → PASS_WITH_DISCLOSED_DEFERRAL (Q-C decision:
  relabel + explicit follow-up recommendation, because the §8
  minimum family list includes source-texture and its byte-level
  validation was deferred with only 45 census blocks).
- AMEND-007: disclosure-only — the pre-existing post-s03 census
  column edit (F-QC-3); no file changed.
- AMEND-008: post-amendment provenance regeneration in canonical
  §21 order (s10), self-exclusion L12 held, rehash clean.

## 4. COVERAGE

- FULL (my own tools, whole denominators): BNT2 walk (5,596);
  version scan (5,596) + per-file compare vs run census (5,596/5,596);
  type-table decode (4,838) + per-type compare (76/76); world-slice
  closure attempt (2,363/2,363; 2,361 OK); ArkTexture header raw scan
  (all slice ArkTexture blocks); holdout recomputation (all 2,363
  records + 29/29 type rows); own split reconstruction (2,363 files,
  sets identical); provenance rehash (10+37+39 rows, all files);
  negative controls (my A:4, B:4, C:4+1); engine source (NiObject.cpp
  L134–143; NiStream.cpp L303–360/362–385/412–425/470–487); HIST
  schema reads (all slice-relevant niobjects/compounds/enum storages,
  with line numbers); 5 nif.xml variant existence+hash; EE2
  header/footer reads (2 files); NiflySharp code read (NiHeader.cs
  header path + NiObject.cs Sync).
- SAMPLE: BASELINE_CONFLICT_RAW (5513 rows — column distribution +
  targeted greps for Group ID / NiArkImporterExtraData / presence
  rows; not a manual full row read); BASELINE_TYPE_TABLE (full
  algorithmic analysis of all 10,890 rows; not a manual row read);
  per-payload SHA verification (my own SHAs computed for all 2,363
  slice files for the split; the run's sha256_stored column compared
  per-file for slice records via JSON, 0 mismatches — non-slice
  payload SHAs not rehashed).
- NOT_CHECKED (explicit): corpus-wide ArkTexture count formula
  OUTSIDE the slice (2,475 non-slice files — the wiki claim was
  corpus-wide; my 100% verdict is slice-scoped); 4.1.0.12 / 4.0.0.2
  block layouts (out of contract scope); BASELINE_CONFLICT_RAW
  row-by-row full read; R61/NifModelReader.js semantic behavior
  beyond the audited rows (REPORT-ONLY audit accepted as scoped);
  runtime/consumer semantics of any field; NifSkope/fo76utils
  nif.xml contents beyond hash identity; Textures.bnt; the exact
  root cause of my 2 residual blocked files (386950/386951 — byte
  dumps recorded; the executor's closure of them stands on their
  attribution).

## 5. §23 falsification questions — answers

1. **"standard layout"** — ATTEMPTED AND SURVIVED (with one
   inversion): my own HIST-derived decoder closes 2,361/2,363 slice
   files with the standard framing (GroupID + TopObjects + EOF-exact);
   EE2 cross-publisher header/footer byte-verified; engine source
   confirms the framing at exact lines. Falsification SUCCEEDED
   against one sub-claim: the "variant family" (F-QC-1) — the
   standard formula was right, the run's deviation claim was the
   artifact.
2. **"MindArk extension"** — SURVIVED where claimed: the 7-type set
   identity holds; 6 Ark layouts closure-confirmed by my decoder;
   NiVertexMorph deferral honest. FALSIFIED in one direction: the
   ArkTexture "extension anomaly family" is not a MindArk corpus
   fact but an attribution artifact (F-QC-1).
3. **"field coverage"** — SURVIVED: coverage CSV numerically coherent
   (numerator==denominator on validated; 0/N on deferred); the
   load-bearing field checks (ApplyMode {0,2}, TextureCount=7,
   VertexColor 10B, hasShader=0, ntp=3×ntri) verified at scale by my
   closure harvest, not just samples.
4. **"parser correctness"** — the ECHO side SURVIVED (census is
   manifest-independent; ordering timestamp-consistent; NC-ECHO 4/4
   run + 4/4 mine); the DEFECT side FALSIFIED (F-QC-1): the JS/R61
   count formula reads the "variant" blocks correctly; the run's
   own decoder mis-read them. The 2 bit-compatible mis-attribution
   rows (importer 38+3) and 3 width-identical assumption rows stand
   as disclosed.
5. **"world-viewer minimum slice"** — SURVIVED with the G6 deferral
   made explicit: 23 closure-confirmed standard types + 6 Ark types
   structure-confirmed; NiCamera=0 confirmed; remaining blockers
   (texture pixels / world placement / UV orientation) honest.

## 6. QC verdict rationale

Every load-bearing denominator and headline number of the run was
independently re-derived from raw bytes and matched (corpus pin,
5,596/4,838/757/1, 76 types, 364,062 blocks, split 1,890/473,
closure 1,876+467, 20 blocked, hypothesis freeze + determinism
byte-identical, importer 41B, TopObjects, GroupID framing,
EE2, anti-circularity, provenance). The single P1 (variant-family
artifact) affects a NEW finding of this run — its supersession of
the prior "PERFECT" claim, one parser-defect verdict, and one
recommended correction run — not the baseline framing, census,
classification or closure methodology. Verdict:
**QC_PASS_WITH_FINDINGS** — G16 closure recommendation to PE-MASTER:
PASS_WITH_FINDINGS, with F-QC-1/F-QC-2/F-QC-3 requiring
adjudication before the 24-block correction run is chartered and
before any of the run's supersessions are pushed to live docs.

## 7. Verdict-independent notes for PE-MASTER

- G17/G18 remain PENDING (adjudication + persistence are not the
  QC's to close).
- The executor performed no git operations; HEAD == BASE_SHA
  f3a3d401f1f254f32cee072260fdc15a6549d378 verified; tracked tree
  clean (only this package + 2 pre-existing untracked roots).
- All QC countercheck tools + outputs live outside the project tree
  (Temp\opencode\pe_master_countercheck\qc_nif_baseline_r1\) and are
  available to PE-MASTER on request; no proprietary payload left the
  corpus archive.
- The s07 'ALL' reproduction was executed under backup/restore
  discipline; the original WORLD_SLICE_VALIDATION.json was restored
  byte-identical (SHA 674E0038… verified before and after).
