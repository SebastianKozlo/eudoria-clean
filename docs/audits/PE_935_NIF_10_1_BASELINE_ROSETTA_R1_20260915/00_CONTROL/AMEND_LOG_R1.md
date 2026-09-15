# AMEND_LOG_R1 — PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915 (append-only)

## AMEND-001 (2026-09-15, executor, pre-freeze disclosure)
- WHAT: s07_full_validation.py subset-merge fix.
- CONTEXT: the first TRAIN invocation wrote results keyed
  {'train': [...], 'hold': []}; the subsequent HOLDOUT invocation overwrote
  the file losing TRAIN rows. The driver was corrected to merge subsets and
  the final single 'ALL' invocation re-produced both subsets with FULL
  evidence in one pass.
- IMPACT ON HYPOTHESIS: NONE. The frozen hypothesis = the decoder (s06) +
  schema extractor (s04); their sha
  (6DB2F1E37E900A2573FEE07B5945B5E25B438066EA0A26AF0841540C96693752) is
  IDENTICAL across the TRAIN, HOLDOUT and ALL invocations (recorded in each
  console output and in WORLD_SLICE_VALIDATION.json). The ALL-pass
  reproduced TRAIN 1876/1890 and HOLDOUT 467/473 exactly.
- FILES: no run evidence file was hand-edited; the driver re-ran
  deterministically. No PRE_EDIT snapshot needed (regeneration, not edit).

## AMEND-002 (2026-09-15, executor, pre-freeze disclosure)
- WHAT: s06 decoder development iterations on TRAIN (discovery file
  505775.nif): cond/vercond key separation in s04; eval int-return fix;
  arr2 storage fix; field-name dedup version-preference fix; dangling-cond
  semantics (absent field => false); Ark importer tail candidates
  (38→41-family); candidate ordering + footer-constrained candidates;
  ArkBillboardNode double-name-read fix; Unresolved catch in the Ark branch.
- STATUS: all completed BEFORE the HOLDOUT run; hypothesis frozen at sha
  6DB2F1E3...; HOLDOUT + ALL runs used the frozen decoder. TRAIN results
  reported are from the FINAL decoder.
- No evidence file modified post-freeze.

## AMEND-003 (2026-09-15, QC auditor pe-master-auditor, hygiene)
- WHAT: removed 00_CONTROL/scripts/__pycache__/ (5 .pyc build artifacts,
  NOT evidence; MANIFEST had always excluded .pyc via s10 filter, but the
  directory physically contradicted the "no __pycache__" claims).
- DELETED (SHA256 at deletion):
  s01_bnt2_walk.cpython-312.pyc       FAF16153662A1BB7BFCCC3A99656D78BE3398D556D62167BE0578539500FAF04 (14902B)
  s02_nif_version_scan.cpython-312.pyc F8C204274F112C887E6475652FBF04B9DBA54937517D2BDCF532A8CCFF61F65 (9154B)
  s03_type_census.cpython-312.pyc      35F25E2A4EE4AC35430F493EC0FB3AD76DAAD9D6448D2762D91419DE56A46076 (12002B)
  s04_nifxml_baseline.cpython-312.pyc 4103BB86169AA20CEBA8B097FF6FF6D905CC21FB20E8758BF9591DEFD55811B2 (29199B)
  s06_world_slice_validator.cpython-312.pyc C3A0F936EA7789FA65C903B30962922F04F038675F9A680211380BBAB77DD6C3 (39024B)
- IMPACT ON SCIENCE: NONE (build artifacts; no evidence row referenced them).
- CLAIM FIX (PROGRESS_STATE.md): "Package complete per §20 layout (40
  files; ...; no __pycache__)" -> factual state: 45 physical files at
  executor freeze incl. 5 .pyc; post-cleanup 40 files (MANIFEST 39 rows +
  manifest itself). OLD SHA 65F01F2C74E1804AC26D72E582E8F8D81EBC31654B102E40247CE7E0B7580E53
  -> NEW SHA E3299EDA364E6CB019F7EB3B07092C0A16FE3A53624A4A8979A8CA8EB5319D2A.

## AMEND-004 (2026-09-15, QC auditor, hygiene — PROGRESS_STATE self-contradiction)
- WHAT: the mid-run section "Current state: SECTION 8/9/10 IN PROGRESS"
  contradicted the header "FINAL STATE (executor phase COMPLETE)". The
  mid-run snapshot is retained but explicitly relabeled HISTORICAL/superseded
  (Q-B). Same file as AMEND-003 (SHA pair above).

## AMEND-005 (2026-09-15, QC auditor, claim-vs-artifact number corrections)
- WHAT: report claims corrected to match the run's own artifacts (no
  evidence rows changed):
  (a) "25 world-slice standard types = STANDARD_10_1_CONFIRMED" ->
      23 CONFIRMED + 3 STANDARD_NAME_CUSTOM_LAYOUT_PENDING
      (NIF_10_1_STANDARD_COVERAGE.csv status tally: 23 CONFIRMED /
      6 MINDARK / 3 PENDING / 44 UNKNOWN = 76).
  (b) "17 matrix rows: 8 PARSER_MATCHES_STANDARD, 4 ASSUMPTION_UNVERIFIED"
      -> 16 rows: 7 MATCHES / 3 UNVERIFIED / 2 MISATTRIBUTION / 1 DEFECT /
      1 SEMANTIC_GAP / 2 SCOPE (PARSER_GAP_MATRIX.csv).
  (c) "LIVE DOC IMPACT: KEEP 8 / CLARIFY 5 / SUPERSEDE 4" -> KEEP 4 /
      CLARIFY 6 / SUPERSEDE 4 / REVALIDATE 2 / NO_CHANGE 1
      (LIVE_DOC_IMPACT_MATRIX.csv action tally).
  (d) G4 evidence "(425 HIST-applicable types)" -> label precision:
      423 HIST-applicable-with-fields + 2 observed UNDEFINED_IN_SCHEMA;
      algebra 425-76=349 holds numerically (2 undefined cancel).
  (e) C-11 "5320 raw conflict rows" -> 5513 (BASELINE_CONFLICT_RAW.csv).
  (f) FINDINGS_LOG F-01 typo "175.nif" -> "16175.nif" (bytes unchanged).
- SHA PAIRS (OLD -> NEW):
  REPORT.md        AA00E49996AEB3AE44EF34A5B45BD09C09A7BA28C361FB01CE85669C1B75872B -> 2BEF5CC01D43EC57B1E71D1C6E6DFE468D0841645DADE40F9A1FA2F78E12E6EF
  HANDOFF.md       FC84A3AE4551F6F1F10EDDC73C39F8533AFE6111D436864C1CB4F500523B952E -> 8BCAF978C854F21E2552FA7F68D68D8C6E6739A0400E5C61013C5AFF8EAC9120
  STAGE_ACCEPTANCE_GATES.csv B23C965001E1293890A32304229DB8E9FB8A14C79B45CA9560FFBE4B67A414C3 -> 10B0BDCB9A5B58EB904869D850BAEBA7AB9E7757F5FC33B3DFCC46C53BA6D228
  FINDINGS_LOG.md  A1ADEA87CDF78FC826E9223C72F42105FB351845F3E551D167097E94919A07E2 -> 189702FCFB6155125FF0C8043E9D21FAEEC4D9A173B42E20648108FF52532E4C
  BASELINE_CONFLICT_MATRIX.csv 5C4C947ED80BB0A830A12B43D3891CC878D1EA142167AD340E31DD35D6F53A12 -> AD9CE01EE590B4934D30D6C7096A4FD735772689BC6C7EE9514DB28B10489626
  PROGRESS_STATE.md (see AMEND-003 pair)
- PRE_EDIT snapshots: 00_CONTROL/PRE_EDIT/*.pre.
- IMPACT ON SCIENCE: NONE (numbers brought into agreement with the
  artifacts; the 24-block-family defect claim itself is NOT changed here —
  it is under QC challenge, see QC_AUDIT.md finding F-QC-1; the REPORT/HANDOFF
  rows carry a status-pointer note only).

## AMEND-006 (2026-09-15, QC auditor, G6 relabel)
- WHAT: G6 NO_NAME_EQUALS_LAYOUT status PASS ->
  PASS_WITH_DISCLOSED_DEFERRAL. The S8 minimum family list includes
  "source texture" (NiSourceTexture, 45 blocks, all in 5 non-slice
  files) which was validated census-level only; the deferral was
  disclosed in 3 places but the PASS label did not carry it. Explicit
  follow-up recommended (binds to the texture-pixel-resolution blocker).
- FILE: STAGE_ACCEPTANCE_GATES.csv (SHA pair in AMEND-005(b));
  REPORT.md S7 updated accordingly (same REPORT.md SHA pair).

## AMEND-007 (2026-09-15, QC auditor, disclosure of a pre-existing
  post-s03 artifact edit discovered during QC — NO file change)
- WHAT (disclosure only): 01_RAW/ENTROPIA_NIF_10_1_TYPE_CENSUS.csv
  column baseline_type_present contains YES_HIST/NO_MOD_SCHEMA values,
  but the packaged s03_type_census.py writes PENDING_BASELINE for that
  column. The column was therefore edited after s03 ran (or written by a
  non-pinned tool version), WITHOUT an AMEND_LOG entry. The measurement
  columns (blocks/files/min/max/examples) are consistent with
  TYPE_CENSUS_SUMMARY.json and with the QC independent recount
  (76 types, 364,062 blocks, 0 mismatches) — no science impact — but the
  artifact is not byte-reproducible from the pinned s03 alone.
  Disclosure per S20/S21; adjudication belongs to PE-MASTER.

## AMEND-008 (2026-09-15, QC auditor, provenance regeneration)
- WHAT: after AMEND-003..006 and the addition of 06_REPORT/QC_AUDIT.md,
  provenance regenerated in the canonical S21 order by s10_provenance.py
  (SCRIPT_SHA256.csv -> EVIDENCE README -> EVIDENCE_INDEX.csv ->
  MANIFEST_SHA256.csv; self-exclusion L12 held). This log entry and the
  PRE_EDIT snapshots are themselves covered by the regenerated manifests.
- IMPACT ON SCIENCE: NONE (hash bookkeeping only).

### AMEND-005 ADDENDUM (2026-09-15, QC auditor — final SHA pairs)
- After the AMEND-005 entry was written, the QC status-pointer notes in
  REPORT.md item 8 and HANDOFF.md (parser-audit section) were softened to
  pure status-pointers (verdict content lives only in QC_AUDIT.md). The
  FINAL post-amendment SHAs for the two files are therefore:
  REPORT.md   -> 486C4BDEF97666AA4275B80118A33F92CFA352757D03A0C9D44C82BCA380B2A3
  HANDOFF.md  -> 246A689348DC923A1E83A2E1FF044E6E359FC8AD3C3B768025C4999F9508275C
  (All other AMEND-005 SHA pairs unchanged; PRE_EDIT snapshots unchanged.)

## AMEND-009 (2026-09-15, executor, PE-MASTER-adjudicated correction
  batch — F-QC-1 RETRACTION of the "24-block ArkTexture variant family")
- AUTHORITY: PE-MASTER adjudication of QC F-QC-1 (ACCEPTED_FINDING) on
  PE-MASTER's own bytes; dispatch = this bounded correction batch.
- WHAT (science): F-09's "24-block ArkTexture variant family" and the
  "formula == closure-truth in 2,319/2,343 (99.0%)" verdict are RETRACTED
  as decoder candidate-order artifacts of the frozen s06 instrument, not
  corpus facts. Corrected verdict: (field2>>8)&0xFFFFFF == TRUE entry
  count in 100% IN-SLICE (2,343/2,343 frozen closures — 2,319 direct +
  24 re-derived; QC independent decoder 2,361/2,363; union = all 2,363
  slice files closable). The prior wiki claim "4,838/4,838 PERFECT" is
  UNSUPERSEDED (confirmed in-slice); corpus-wide outside the slice
  (2,475 files) remains an explicit OPEN item. Byte-verified deviation
  structure (supersedes F-09's 17/7 description): 18 zero-count blocks
  (header (3,1,0,0); accepted count=1 via field1) + 6 true-count-1/2
  blocks (headers C=0x100/C=0x200; accepted count=3 via numfield:
  386950/386951/386590 + 488579/493785/490489). In-slice zero-count
  signature census by raw scan: 32 blocks = 25x(3,1,0,0) +
  7x(3,0xFFFFFF00,0xFF,0) [the QC summary's 24/8 split differs by one
  file; per-block CSV rows are authoritative]. ALL recorded ref/f1/f2
  anomalies were fake entries of the 24 mis-parsed blocks (27 fake
  entries: 24 OOR "iewp" + 3 NiNode ref=0; f1=15 x24 = len
  "ArkViewportInfo"; f1=16777216 x3; f2 "ArkV" x24): the TRUE ref
  targets NiTexturingProperty 10,610 / NiTextureEffect 1,105 were NEVER
  polluted; 0 NiNode / 0 OOR refs remain; TRUE f1 domain {0,1,2,3,4,5,6,9}
  (11,715 true entries) matches the prior claim; TRUE f2 domain
  {-1: 10,226; 0: 1,489}.
- WHAT (parser verdict): PARSER_GAP_MATRIX row 7 verdict INVERTED to
  PARSER_MATCHES_STANDARD — the JS/R61 formula reads ALL these blocks
  correctly; there is NO parser defect; the recommended run
  PE_935_NIF_PARSER_TEXTURECOUNT_24BLOCK_CORRECTION_R1 is WITHDRAWN
  (false premise). A decoder-INSTRUMENT documentation note (count-
  candidate ordering formula-first / next-block signature validation)
  replaces it. F-13's defect-class row is superseded by F-14.
- WHAT (verdict-preservation): frozen TRAIN/HOLDOUT/ALL results
  (1,876/1,890; 467/473; 2,343/2,363) and all census measurements
  UNCHANGED (closure byte consumption identical); F-09 retained as a
  historical entry per the append-only discipline (marked retracted by
  F-14 in FINDINGS_LOG).
- NEW EVIDENCE (run-local tools; SCRIPT_SHA256-covered):
  00_CONTROL/scripts/s12_arktexture_zero_count_rederivation.py
  (SHA 6A8FD958E4EBA4A20BEE34BA4F531C4862B90E89B9339B25C3BD5A0396B8E0DB,
  26,530B): phase 1 raw byte scan of all 4,838 v10.1 payloads for the two
  zero-count signatures (backscan-validated: u32 name_len, prior u32
  GroupID==0, block name; next-block signature gid=0+len+canonical name;
  type-index agreement); phase 2 frozen-decoder instrument pass over all
  2,363 slice files (ASSERTS byte-exact reproduction of the recorded
  WORLD_SLICE_VALIDATION.json ArkTexture evidence aggregates — f1/f2/
  ref-targets/count_source; 2,343 closures); phase 3 true-count
  re-derivation of every deviation block (true entries read from bytes;
  next-block signature verified after the last true entry).
  01_RAW/ARKTEXTURE_ZERO_COUNT_REDERIVATION.csv (SHA 775C1199697D9C311D
  4CD90233D8189818F32FB6D0663532CD273F4B8E7E3AC1, 10,053B): 38 rows
  (18 ZERO_COUNT_MISPARSED_FROZEN + 8 ZERO_COUNT_CONSISTENT_FROZEN + 6
  ZERO_COUNT_FILE_BLOCKED_FROZEN + 6 COUNT_MISMATCH_TRUE_EQ_FORMULA),
  every row signature_verified + type_index_agreement TRUE
  (next block NiArkViewportInfoExtraData, name "ArkViewportInfo").
  01_RAW/ARKTEXTURE_FAKE_ENTRIES_RETRACTED.csv (SHA F188B1C1D6C283419A8
  D60DDC178F543645671ED40FAD93DE5B3ADFECF338E3E, 6,087B): 27 fake
  entries with per-file/block/entry attribution and ref targets
  (24x OOR(1886872937), 3x NiNode via ref=0).
- BOUNDED EDITS (PRE_EDIT snapshots at 00_CONTROL/PRE_EDIT/*.AMEND-009.pre;
  OLD -> NEW SHA256):
  00_CONTROL/FINDINGS_LOG.md      189702FCFB6155125FF0C8043E9D21FAEEC4D9A173B42E20648108FF52532E4C -> 190DBC00D6267F32ADBDA1628EF03DE6893B01E275EDA81C3A8DD08CB49B9786 (append F-14 RETRACTION + F-15 F-08 update; F-09/F-03 bytes unchanged)
  01_RAW/FIELD_VALIDATION_RAW.md  D1DC147A3EEFEC7CE6647B98F5C2BAB3126391CDF982D575CBB5D273EA8E3391 -> 92FAAB6930E966BC2F57DB89E45B58C5EE345A020F60EF7B8935F8ED056E778E (count/ref/f1 rows + count-source section relabeled: value-coincidence labels; formula 100% in-slice)
  02_ANALYSIS/BASELINE_CONFLICT_MATRIX.csv AD9CE01EE590B4934D30D6C7096A4FD735772689BC6C7EE9514DB28B10489626 -> 4F19FBD99AB983B45539687A6423D8DFEC5E922F71694AD171C0F97D55B1ED47 (C-08)
  02_ANALYSIS/PARSER_GAP_MATRIX.csv 376922B350653FC44592E37D37938A069252E4EAC3B01DF0F34ED1D4CC478041 -> FB1BBCFD4892C7E82A6E368CC865037965A9D3B814210C0DD40E90C85F306BBC (row 7 verdict inverted; blast radius 24->0; correction run withdrawn)
  06_REPORT/REPORT.md             486C4BDEF97666AA4275B80118A33F92CFA352757D03A0C9D44C82BCA380B2A3 -> 7113FC16585C5B4CAD236199DDDFF8A8EC110B7C4D1A2140B21F005EC6D89056 (headline 7 ArkTexture bullet; headline 8 parser audit; headline 9 world-viewer blocker clause; §5 tally KEEP 5/REVALIDATE 1; §6 honest unknowns)
  06_REPORT/HANDOFF.md            246A689348DC923A1E83A2E1FF044E6E359FC8AD3C3B768025C4999F9508275C -> E00DD342FFF11A610D68C6C7583D6CAE39AA4DC443DA850F070669C50B9B459A (known gaps; world-viewer blockers; parser-audit defects; recommended runs; oracles summary; TOP-10 gap 1; retractions list; live-doc tally)
  02_ANALYSIS/LIVE_DOC_IMPACT_MATRIX.csv 01F391909C0F5F130A60A7E5A5BFB8289C1FC06AEBD5154497CA49C172786013 -> 94D0529DCC17D335FB4F866AF590C472FDDD5DF3DC74657AC44DC1DBA68CD6A9 (row 12 REVALIDATE->KEEP with F-14 evidence; row 13 evidence cleaned, SUPERSEDE stands)
  02_ANALYSIS/WORLD_VIEWER_MINIMUM_NIF_SLICE.md 21777E535DCD3D5522386A7EA9B0A7EEA4EF41C1AD7AB1E56827BE47DE9F9AA6 -> 1C618F2ACD83414C3414B7B595F872354A12F31E2009D316FDA9020231A56D47 (blocker 2: "include the 24-block family" clause withdrawn)
  02_ANALYSIS/NIF_10_1_STANDARD_COVERAGE.csv EF0E70ED6FECA6C4E88E21041180277643057208B3906BF1A32197313EDA79C8 -> 93F9ED28F19AC790C789E11CBC55413ACCE6EC790F99B65B6E3F943773B5BB50 (ArkTexture row: count semantics confirmed; trailing-9 split still OPEN; parser_support note)
  02_ANALYSIS/MINDARK_NIF_EXTENSION_MATRIX.csv 8C7047CBA6AE858B5DEF7A6C431C84F719E317E7D1623479D25A7F4D3EE3A2C2 -> 86AA583D19436A120A8BCA35BFFA6EE4E53624EF8E86C04B80C53BE88FC4EEFD (ArkTexture row count semantics; per-type structural_status made explicit — 6 STRONGLY_SUPPORTED + NiVertexMorphExtraData UNKNOWN, resolving the "7 MindArk" rollup framing; ALSO repairs the pre-existing s09 generation defect: rows were 14 cells vs the 15-column header with truncated duplicated cells — s09 itself NOT modified (frozen), so a future s09 regeneration would re-introduce that defect; the closure= block counts are preserved unchanged. Also serves F-QC-8(c), see AMEND-013)
  02_ANALYSIS/NIF_10_1_ROSETTA_BASELINE.md CEEB5F4831E14852E3655392BDE6913BAA90DE8D342DDAF9867EF8E9B06FF3F5 -> D50EEC29C250199E30A8BBCCDF71B1296C25C038CAAD24BBFFBDA887A9A17EEF (D6 count verdict; open-link F2 retracted + replaced by the corpus-wide OPEN item)
  01_RAW/NEGATIVE_CONTROL_RAW.md  F670D0B915A86FB5BFDF9301375FC2C0ED405FBBA57FCB7B824C122579E26988 -> DEE6C64E05CA5D51B3EE634CCFEE0CF98C2581B9E8AFE8F28E8CB7EFBBB22F91 (NC_REF_RANGE row + NC-SET-D bullet + residual-honesty notes annotated with the F-14 retraction; the "greedy candidate order" anticipation note marked CONFIRMED)
- IMPACT ON FROZEN MEASUREMENTS: NONE (census, closure counts, holdout,
  blocked lists unchanged; only semantic attribution + verdict labels).
- OPEN items introduced/kept: corpus-wide count-formula test outside the
  slice (2,475 files; 1,790 raw-signature observations recorded, 1,101
  already byte-consistent, unverified); 386950/386951 trailing-23 tail
  semantics (see AMEND-012).

## AMEND-010 (2026-09-15, executor, PE-MASTER-adjudicated correction
  batch — F-QC-2 NiflySharp sub-claim correction)
- AUTHORITY: PE-MASTER adjudication of QC F-QC-2 (ACCEPTED_FINDING;
  PE-MASTER verified on the pinned NiflySharp source itself).
- WHAT (science): the claim "NiflySharp (104d79f) would misalign on real
  10.1.0.0 files" is FALSE and RETRACTED. Actual code (NiflySharp\
  NiflySharp\NiObject.cs L61-62, Sync): `if
  (stream.Version.FileVersion >= NiFileVersion.V10_0_0_0 &&
  stream.Version.FileVersion < NiFileVersion.V10_1_0_114)
  stream.Sync(ref groupId);` — 10.1.0.0 IS inside the range; every block
  syncs its own per-block u32 groupId; the header reader (NumGroups only)
  is correct engine behavior. RESIDUAL (separate note): NiflySharp's
  per-block range starts at V10_0_0_0 vs the ENGINE's 5.0.0.6
  (NiObject.cpp L134-143) — differs only for 5.0.0.6–9.x files, out of
  this run's 10.1 scope. F-03's "untested against real Gamebryo-1.x-era
  files" hedge stays as a test-gap note.
- UNAFFECTED: C-01 core verdict (engine range; physical presence; modern
  mis-version since=10.1.0.114; historical omission) — CONFIRMED.
- WHERE (5 QC-listed locations + 1 same-claim occurrence found by
  sweep): FINDINGS_LOG F-03 NOTE (via appended F-16; F-03 bytes
  unchanged); BASELINE_CONFLICT_MATRIX C-01 impact column;
  NIF_10_1_BASELINE_SPEC.md framing paragraph; REPORT §2.2; HANDOFF
  TOP-10 standard gaps item (8); plus SOURCE_REGISTRY.md C-01 bullet
  (same false sentence — fixed in the same pass, disclosed here).
- BOUNDED EDITS (PRE_EDIT snapshots at 00_CONTROL/PRE_EDIT/*.AMEND-010.pre;
  OLD -> NEW SHA256):
  00_CONTROL/FINDINGS_LOG.md      190DBC00D6267F32ADBDA1628EF03DE6893B01E275EDA81C3A8DD08CB49B9786 -> 34EAFBB610427888523334DF80787D04F7976A152159464D98E3DC0DF34B01F0 (append F-16)
  02_ANALYSIS/BASELINE_CONFLICT_MATRIX.csv 4F19FBD99AB983B45539687A6423D8DFEC5E922F71694AD171C0F97D55B1ED47 -> 9ADCFEF0E79CEDA4386A74DF27B3453D48E9D7EF910C6A3BD94F90CBE91EAC5C (C-01 impact column)
  02_ANALYSIS/NIF_10_1_BASELINE_SPEC.md 4699FF33A43FE4A6848BA1680C824B10509961082B59B8377D3DB0179806148A -> 61C912A251F106420628BCB21804813726B299E4FA707A1FD1BAE69F7178F322 (framing paragraph with actual code quote)
  06_REPORT/REPORT.md             7113FC16585C5B4CAD236199DDDFF8A8EC110B7C4D1A2140B21F005EC6D89056 -> 020032DF88E71756BEB48622D4F91018E9BEF1F2792C945C04AF907CA17A1182 (§2.2)
  06_REPORT/HANDOFF.md            E00DD342FFF11A610D68C6C7583D6CAE39AA4DC443DA850F070669C50B9B459A -> 6CF4815ACEBC9A6EEE0A70A18A0A87579088AA025AB9485A7F8B0C727919A7DF (TOP-10 std gaps item 8)
  00_CONTROL/SOURCE_REGISTRY.md   FA6517289793443E457F781AD1B934718FC8BFA1DFB0D1950BCC0D8A9236BC7B -> 26925174B9A9AB547929CB3F3CA7ABC8CAA170FEB7A65A8E58D69BB3A8E74F13 (C-01 bullet)
- IMPACT ON MEASUREMENTS: NONE (wording correction with the primary-source
  code citation).

## AMEND-011 (2026-09-15, executor, PE-MASTER-adjudicated correction
  batch — F-QC-3 census-column provenance normalization; option (a))
- AUTHORITY: PE-MASTER adjudication of QC F-QC-3 (ACCEPTED_FINDING).
- WHAT: the packaged 01_RAW/ENTROPIA_NIF_10_1_TYPE_CENSUS.csv column
  baseline_type_present (YES_HIST / NO_MOD_SCHEMA) originated from an
  undisclosed post-s03 edit (disclosed by QC as AMEND-007/F-QC-3). The
  packaged s03 writes PENDING_BASELINE there (s03 L190) — measurement
  columns are s03's; the labeling column is a separate pass.
- NORMALIZATION (chosen option (a) — new labeling script; s03 NOT
  modified): NEW SCRIPT 00_CONTROL/scripts/s11_census_labels.py
  (SHA 6A8FD958E4EBA4A20BEE34BA4F531C4862B90E89B9339B25C3BD5A0396B8E0DB,
  5,477B). Regeneration rule (byte-reproduces the packaged values on all
  76 census rows): YES_HIST iff BASELINE_TYPE_TABLE.csv has >=1
  NIFXML_HIST_0_7_1_1 row for the type with APPLIES_TO_10_1_0_0 == True
  (else NO_MOD_SCHEMA — the two observed UNDEFINED_IN_SCHEMA placeholders
  NiArkBillboardNode + NiVertexMorphExtraData). VERIFICATION EXECUTED:
  s11 --check over the packaged CSV → BYTE-IDENTICAL (exit 0; 76 rows =
  74 YES_HIST + 2 NO_MOD_SCHEMA). PIPELINE: s03 → s11 produces the
  packaged census CSV byte-reproducibly.
- CENSUS CSV: NOT byte-changed by this amendment (values already correct;
  provenance path added; census SHA remains
  94D4B550AAFF85C1DF435510EDD4020B2F54F219D28F3BF238F857A25B8BB9BB,
  7,434B — byte-identical to the AMEND-008 manifest state).
- s10 TEMPLATE: 00_CONTROL/scripts/s10_provenance.py EVIDENCE_README
  updated (census bullet now documents the s03‖s11 pipeline; new bullet
  documents the s12 re-derivation) so the final §21 pass (AMEND-014)
  writes the honest README. PRE_EDIT snapshot
  00_CONTROL/PRE_EDIT/00_CONTROL_scripts__s10_provenance.py.AMEND-011.pre;
  OLD -> NEW SHA256:
  CA5A73D5CB688024A4A028A918E8C7EA00BAAC71CF75E7440081339A7F8A8109 ->
  218B794073576FB0A69F4606904D1C6973E82C2EC7894FECD0A4CF82BC2B95AA
- IMPACT ON MEASUREMENTS: NONE (labeling-column provenance only; the
  measurement columns were never in question — QC-verified vs
  TYPE_CENSUS_SUMMARY.json and the QC independent recount).

## AMEND-012 (2026-09-15, executor, PE-MASTER-adjudicated correction
  batch — F-QC-9 search-dependence + QC-blocked-file disclosures;
  BABYLENGUIN positive-realism note)
- AUTHORITY: PE-MASTER adjudication of QC F-QC-9 (ACCEPTED disclosure).
- WHAT: (a) closure counts disclosed as DECODER-SEARCH-DEPENDENT (the
  frozen decoder's search limits), not corpus invariants: frozen decoder
  2,343/2,363 (20 blocked); QC independent decoder 2,361/2,363 (blocked
  only 386950/386951, "trailing 23"); blocked sets DISJOINT; union = all
  2,363 slice files closable; (b) the 2 QC-blocked files 386950/386951
  recorded as OPEN items with THIS RUN's attribution disclosed (their
  executor closure rests on the ArkTexture count=3 mis-attribution
  retracted in F-14; their true count=1 is byte-evidenced — one real
  entry "*_0_BASE" with ref to a NiTexturingProperty block; the 23-byte
  tail after the viewport block remains unexplained); (c)
  CROSS_PUBLISHER_TEST wording corrected: BABYLENGUIN.NIF fails at block
  7 GroupID=479309 — a NONZERO engine GroupID in a non-PE 10.1.0.0 file,
  POSITIVE realism evidence for the GroupID field (the run's gid==0
  invariant is PE-scoped by design: PE NumGroups=0) — the former "SDK
  samples fail ONLY at types absent from the Entropia corpus" wording was
  FALSE for that sample; (d) HANDOFF QC/PE-MASTER verdict lines updated
  to the factual post-adjudication state (G16/G17 closure explicitly left
  to PE-MASTER); (e) completes the AMEND-009 parser-audit tally in
  HANDOFF (7 -> 8 PARSER_MATCHES_STANDARD rows after the row-7 inversion).
- BOUNDED EDITS (PRE_EDIT snapshots at 00_CONTROL/PRE_EDIT/*.AMEND-012.pre;
  OLD -> NEW SHA256):
  06_REPORT/STAGE_ACCEPTANCE_GATES.csv 10B0BDCB9A5B58EB904869D850BAEBA7AB9E7757F5FC33B3DFCC46C53BA6D228 -> E86945F7CF161F7ED69148B573C65C8C112D8A2BB7CCD2A1A98C41AD356E00DE (G6 + G7 evidence notes; statuses unchanged)
  06_REPORT/REPORT.md             020032DF88E71756BEB48622D4F91018E9BEF1F2792C945C04AF907CA17A1182 -> 4D1425803CAC9FD0F418D56045FE4B89B8D6000B08FCA703D7234C4051E04106 (headline 3 search-dependence; headline 4 BABYLENGUIN; §7 gates note)
  06_REPORT/HANDOFF.md            6CF4815ACEBC9A6EEE0A70A18A0A87579088AA025AB9485A7F8B0C727919A7DF -> 1DE9A951CEDEA501DE570A8037C68B4EF69683FB7561EF2FF26547357188E6FC (holdout disclosure; MATCHES tally; QC/PE-MASTER verdict lines)
  01_RAW/FIELD_VALIDATION_RAW.md  92FAAB6930E966BC2F57DB89E45B58C5EE345A020F60EF7B8935F8ED056E778E -> ADD931EF5772F02A34CCC9EE85BD72D7D9696C3C701C02F22FFA1BD30D667E42 (cross-publisher row + PARSE_BLOCKED denominators note)
- IMPACT ON MEASUREMENTS: NONE (disclosures; all closure/blocked counts
  unchanged).

## AMEND-013 (2026-09-15, executor, PE-MASTER-adjudicated correction
  batch — F-QC-8 counting-mode clarifications)
- AUTHORITY: PE-MASTER adjudication of QC F-QC-8 (ACCEPTED clarification).
- WHAT: (a) G12 counting mode stated: "23 type rows" = the 23
  STANDARD_10_1_CONFIRMED types per NIF_10_1_STANDARD_COVERAGE.csv, while
  the WORLD_VIEWER table has 24 capability rows naming 28 distinct types
  (family-aggregating rows) — construction difference, not discrepancy;
  (b) 442-vs-423/425 reconciled: BASELINE_GEN_SUMMARY schema-level
  hist_types_applying_to_10_1=442 includes 19 zero-field types not
  materialized as BASELINE_TYPE_TABLE rows (442−19=423); +2 observed
  UNDEFINED_IN_SCHEMA placeholders = 425 table type names; algebra
  425−76=349 holds with the 2 undefined canceling; (c) "7 MindArk" rollup
  framing cleaned in MINDARK_NIF_EXTENSION_MATRIX.csv — per-type
  structural_status now explicit (6 MINDARK_EXTENSION_STRONGLY_SUPPORTED
  + NiVertexMorphExtraData UNKNOWN/deferred); that matrix rebuild was
  performed under AMEND-009 (same file, same snapshot pair — see
  AMEND-009 for its SHA pair and the s09 column-defect disclosure).
- BOUNDED EDITS (PRE_EDIT snapshots at 00_CONTROL/PRE_EDIT/*.AMEND-013.pre;
  OLD -> NEW SHA256):
  06_REPORT/STAGE_ACCEPTANCE_GATES.csv E86945F7CF161F7ED69148B573C65C8C112D8A2BB7CCD2A1A98C41AD356E00DE -> 8436011278A557A37DF4FA2F290B8546655A8F6907EE7CFEE89DFA0B69CE2980 (G4 reconciliation note; G12 counting-mode note; statuses unchanged)
  06_REPORT/REPORT.md             4D1425803CAC9FD0F418D56045FE4B89B8D6000B08FCA703D7234C4051E04106 -> A13BF24DC329AA9E88E4B6AF99D8D8ED341395505963AD538E9FF9F47C8AFFE5 (§3 counting-mode note)
  02_ANALYSIS/WORLD_VIEWER_MINIMUM_NIF_SLICE.md 1C618F2ACD83414C3414B7B595F872354A12F31E2009D316FDA9020231A56D47 -> 5CE1AEDEA7243ADDC67C8BCEB783FA2E928EB91B729275C320B678211648FB2C (counting-mode note in the intro)
- IMPACT ON MEASUREMENTS: NONE (counting-mode notes; all counts
  pre-existing and unchanged).

## AMEND-014 (2026-09-15, executor, PE-MASTER-adjudicated correction
  batch — residual stale-claim sweep + final §21 provenance regeneration)
- WHAT (residual fixes found by the post-edit stale-claim sweep):
  (a) NIF_10_1_BASELINE_SPEC.md baseline-conflicts paragraph still said
  "C-08 (ArkTexture count 99.0%)" — corrected to the F-14 verdict
  (100% in-slice; corpus-wide outside the slice OPEN);
  (b) FINDINGS_LOG F-17 appended (F-12 cross-publisher wording
  correction: BABYLENGUIN.NIF fails at block 7 GroupID=479309 — a
  NONZERO engine GroupID in a non-PE 10.1.0.0 file, positive realism
  evidence for the GroupID field; the run's gid==0 closure invariant is
  PE-scoped BY DESIGN; F-12 historical text byte-unchanged);
  (c) REPORT.md §8 provenance section updated for the correction batch
  (12 scripts after s11+s12; two new evidence CSVs; per-file PRE_EDIT
  snapshots; census CSV byte-unchanged and now byte-reproducible from
  the packaged s03‖s11 pipeline; no measurement rows changed).
- BOUNDED EDITS (PRE_EDIT snapshots at 00_CONTROL/PRE_EDIT/*.AMEND-014.pre;
  OLD -> NEW SHA256):
  02_ANALYSIS/NIF_10_1_BASELINE_SPEC.md 61C912A251F106420628BCB21804813726B299E4FA707A1FD1BAE69F7178F322 -> 8FBE024DCA596DE5392CC0D78D04A39820DB44DD11F4B96F1F3B494CC4F02F4E
  00_CONTROL/FINDINGS_LOG.md      34EAFBB610427888523334DF80787D04F7976A152159464D98E3DC0DF34B01F0 -> 548A80D33D3214F9D0E3C4DBDE12D4701C2B7BE3481991570D00D6B974FF4B4F (append F-17; F-12 bytes unchanged)
  06_REPORT/REPORT.md             A13BF24DC329AA9E88E4B6AF99D8D8ED341395505963AD538E9FF9F47C8AFFE5 -> 7E8A94B2E55D80DD8AE8F9FC868C30BED44042F081812C65CDF856198A5284D1 (§8 correction-batch note)
- WHAT (provenance): final §21 pass executed AFTER this entry:
  s10_provenance.py (updated README template per AMEND-011) regenerates
  SCRIPT_SHA256.csv (now 12 script rows: s01-s12 incl. s11_census_labels,
  s12_arktexture_zero_count_rederivation), 03_EVIDENCE/README.md,
  03_EVIDENCE/EVIDENCE_INDEX.csv and 06_REPORT/MANIFEST_SHA256.csv in the
  canonical order; self-exclusion L12 held (MANIFEST does not hash
  itself); rehash verification: zero missing rows, zero stale hashes;
  zero __pycache__/.pyc in the package. This log entry and all AMEND-009
  ..013 PRE_EDIT snapshots are themselves covered by the regenerated
  manifests.
- IMPACT ON MEASUREMENTS: NONE.

### AMEND-014 ADDENDUM (2026-09-15, executor — cosmetic indent alignment)
- REPORT.md item 7 ArkTexture-count bullet realigned to the list's 3-space
  indent (the AMEND-009 replacement had used 4; no content change).
  OLD -> NEW SHA256:
  7E8A94B2E55D80DD8AE8F9FC868C30BED44042F081812C65CDF856198A5284D1 ->
  576E30FFE99F40721AFCC346C0847651ED347796F206AB384E936A59894E2093
- Provenance regenerated AFTER this addendum (final s10 pass below);
  this addendum is itself covered by the regenerated manifests.
## AMEND-015 (2026-09-15, pe-master-auditor, persistence — gates G16/G17/G18 closure + PE_MASTER_REVIEW.md addition)
- AUTHORITY: PE-MASTER PERSIST_PUBLISH dispatch (ORDERED_WORK per the PE-MASTER review below); no science content.
- WHAT (review addition): NEW FILE 06_REPORT/PE_MASTER_REVIEW.md (SHA256 906A674C306F6B129DC91F5E454BB19FB5101481FC9A323E654E0DB29D3DCB40, 18,935B) — the PE-MASTER review of this run persisted VERBATIM (UTF-8, LF); VERDICT MASTER_ACCEPTED; AUTHORITY_STATUS ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT NONE; HARD_STOP per contract S28 step 12.
- WHAT (gate closures per the review's GATE_PREDICATES): G16 PASS — fresh QC QC_PASS_WITH_FINDINGS (QC_AUDIT.md); findings F-QC-1/2/3 adjudicated ACCEPTED by PE-MASTER on own bytes; correction batch AMEND-009..014 executed + PE-MASTER targeted re-audit passed. G17 PASS — PE_MASTER_REVIEW.md persisted verbatim. G18 PASS — single path-limited commit + AUDIT_ENTRYPOINT row + push + HEAD==origin/master==ls-remote verification; evidence = this commit, discover via `git log -1 -- docs/audits/PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915`.
- BOUNDED EDITS (PRE_EDIT snapshot 00_CONTROL/PRE_EDIT/06_REPORT__STAGE_ACCEPTANCE_GATES.csv.AMEND-015.pre, SHA256 8436011278A557A37DF4FA2F290B8546655A8F6907EE7CFEE89DFA0B69CE2980, 6421B; OLD -> NEW SHA256):
  06_REPORT/STAGE_ACCEPTANCE_GATES.csv 8436011278A557A37DF4FA2F290B8546655A8F6907EE7CFEE89DFA0B69CE2980 -> F2CDD195E7883DCA20E8FA7889C90ADE559FC9CFAD901DCDF7F9222B3FC9F63E (G16/G17/G18 PENDING_LATER_PHASE -> PASS with the review's evidence; no other row touched)
- IMPACT ON MEASUREMENTS: NONE (control/report layer only; no science evidence file touched; no src/, docs/nif/* or runtime change).
- PROVENANCE: s10_provenance.py regenerated AFTER this entry in the canonical §21 order (SCRIPT_SHA256 -> EVIDENCE README -> EVIDENCE_INDEX -> MANIFEST; self-exclusion L12); this entry, PE_MASTER_REVIEW.md and the PRE_EDIT snapshot are covered by the regenerated manifests. PERSISTENCE = the single path-limited commit carrying the package + AUDIT_ENTRYPOINT.md.
