# PREFLIGHT — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003

Performed by: pe-master-auditor FORMALIZER-1 worker (no science, no git
mutations). Date: 2026-10-03. Environment: Windows, PowerShell 5.1, workdir
`D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`. All values below are
ACTUAL command outputs recorded verbatim (fail-closed), not assumptions.
Full SHA256 of multi-GB archives is deliberately NOT computed here — that
is executor Phase A duty per the dispatch; only existence + size are
recorded here.

## 1. GIT VERIFICATION (re-run by the formalizer, not assumed)

Commands executed and their actual outputs:

```
PS> git fetch origin
(no output; FETCH_EXIT=0)

PS> git rev-parse HEAD
f33c7b9c201b02b8e0f8c7010275b6217475b5a4

PS> git rev-parse origin/master
f33c7b9c201b02b8e0f8c7010275b6217475b5a4

PS> git ls-remote origin refs/heads/master
f33c7b9c201b02b8e0f8c7010275b6217475b5a4	refs/heads/master
(LSREMOTE_EXIT=0)

PS> git status --short
?? docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/
?? docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
?? docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/
?? docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/
?? experiments/
```

ASSERTION: HEAD == origin/master == live remote ==
`f33c7b9c201b02b8e0f8c7010275b6217475b5a4` — CONFIRMED by the three
independent measurements above (fetch exited 0; both rev-parses and the
live ls-remote return the identical SHA).

Anomaly note (honesty record): the formalizer's FIRST combined invocation
(`git fetch origin 2>&1; ...; git ls-remote ...`) produced one
`fatal: unable to access 'https://github.com/SebastianKozlo/eudoria-clean.git/': Empty reply from server`
line with ambiguous attribution (PowerShell 5.1 can reorder native stderr
records relative to stdout). The commands were therefore RE-RUN
individually (above); fetch and ls-remote both then succeeded cleanly with
exit 0. The transient network error is recorded and does not affect the
assertion. Staged changes: NONE (`git status --short` shows untracked-only;
no `M `/`A `/`D ` entries).

BASE_SHA (pinned by the parent dispatch) ==
`f33c7b9c201b02b8e0f8c7010275b6217475b5a4` == observed HEAD. MATCH.

## 2. UNTRACKED INVENTORY + OUT_OF_SCOPE (verbatim)

The worktree dirty state is UNTRACKED ONLY — exactly the six entries
above, matching the parent's preflight claim verbatim. ALL of them are
OUT_OF_SCOPE for this run:

| Untracked path | Status in this run |
|---|---|
| `docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/` | OUT_OF_SCOPE — NEVER_STAGE, NEVER_COMMIT, never modify |
| `docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/` | OUT_OF_SCOPE — READ-ONLY reference (its sandbox payload + raw evidence only); NEVER_STAGE, NEVER_COMMIT |
| `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/` | OUT_OF_SCOPE — NEVER_STAGE, NEVER_COMMIT |
| `docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/` | OUT_OF_SCOPE — NEVER_STAGE, NEVER_COMMIT |
| `docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/` | OUT_OF_SCOPE — NEVER_STAGE, NEVER_COMMIT |
| `experiments/` | OUT_OF_SCOPE (foreign EU1030 workstream) — NEVER_STAGE, NEVER_COMMIT |

RULE: NEVER_STAGE_NEVER_COMMIT applies to all six entries for every worker
in this run. The fresh package `docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/`
(00_CONTROL created by this formalization; the rest created by the
executor) and the tool `tools/gamebryo_oracle/` are the ONLY new repo
paths this run may ever stage, in the separate persistence phase.

## 3. FRESH-PACKAGE COLLISION CHECK

- `docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/` did NOT exist before
  this formalization (verified: `Test-Path` = False; now contains only
  `00_CONTROL/`). No output-root collision.
- `tools/gamebryo_oracle/` did NOT exist before this run (verified:
  `Test-Path` = False). `tools/` exists and currently contains 16 loose
  forensic script files (`era_validation*.js`, `iter020_*.py/js`,
  `p0_byte_audit.js`, etc.) — none named gamebryo_oracle; no collision.

## 4. LOCAL CORPUS RECORDS (existence + size only; SHA256 = executor Phase A)

### 4.1 D:\gamebyroengine — top-level physical census (recounted)

EXACTLY 8 top-level items = 2 directories + 6 archives (matches the
expected count in G-INV-1):

| Item | Size (bytes) |
|---|---|
| `extracted\` (directory) | census fields = executor Phase A |
| `Gamebryo 1.1.2 Evaluation\` (directory) | census fields = executor Phase A |
| `Gamebryo 1.1.2 Evaluation.zip` | 427,384,562 |
| `Gamebryo 1.2 Source.rar` | 450,424,793 |
| `GameBryo2.6.7z` | 3,005,063,726 |
| `gamebryo_1.2.7z` | 221,882,912 |
| `Gamebryo_Version_1.1.2_Gamebryo_2004.iso` | 494,020,608 |
| `GB_2.3.iso` | 2,093,645,824 |

Archive sizes MATCH the PE-MASTER loop-state preflight record verbatim
(427384562 / 450424793 / 3005063726 / 221882912 / 494020608 / 2093645824).

### 4.2 D:\gamebyroengine\extracted\ — subdirectory names (8)

`Gb112_docs_html`, `Gb112_eval`, `gb112_known_good`, `Gb112_tools_setup`,
`gb12_build`, `Gb12_Source`, `Gb26`, `Gb26_src`.

### 4.3 "Gamebryo 1.1.2 Evaluation" — top-level (12 items)

Directories: `AppFrameworks`, `Build`, `Documentation`, `Samples`, `SDK`,
`Tools`. Files: `GamebryoVideo.mpg` (9,419,172), `GbEvaluationSetup.dat`
(2,467), `GbEvaluationUninstaller.exe` (124,886), `license.txt` (286),
`Unwise32.exe` (164,864).

### 4.4 gb_tools_inventory (temp, read-only reference)

`C:\Users\User\AppData\Local\Temp\opencode\gb_tools_inventory\`:

| File | Size (bytes) | Matches parent claim |
|---|---|---|
| `AssetViewer_PC.cab` | 6,914,841 | YES (6914841) |
| `Dev_Tools_PC.cab` | 50,290,417 | YES (50290417) |
| `SceneDesigner_PC.cab` | 33,689,309 | YES (33689309) |

### 4.5 Interrupted-run sandbox payload (READ-ONLY reference)

`D:\Eudoria_Reconstruction\99_Audits\PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003\sandbox\`:
`218757.nif` (57,316 B — MATCHES pin), `218758.bvi` (652 B — MATCHES pin),
`viewer\` (dir), `SDK_DLL_PC.cab` (28,112,104), `vcredist2008_x86.exe`
(1,862,664), `screen_error.png` (61,742 — the P7 evidence), `dbg_probe.py`
(2,944), `dbg_probe2.py` (7,521), `dbg_probe3.py` (7,710),
`s3_dialog_text.ps1` (3,298), `s3_launch.ps1` (2,732), `s3_launch_only.ps1`
(4,179).

### 4.6 PCG corpus (read-only originals)

- `D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt` — EXISTS,
  395,412,868 B (MATCHES the G-SEL-2 pin size). SHA256 re-hash = executor
  Phase A duty, fail-closed against
  `C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0`.
- `D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt` —
  EXISTS, 3,746,375 B (context for P5; this run does NOT decode .bvi).

### 4.7 Run sandbox (to be created by the EXECUTOR, not by the formalizer)

`D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\`
does NOT exist yet (verified). The executor creates
`...\sandbox\` there. All extracted payloads stay LOCAL_ONLY in that
sandbox.

### 4.8 P1/P4 physical spot-checks (existence only; content = executor)

- P1 target EXISTS: `D:\gamebyroengine\extracted\Gb12_Source\SDK\Win32\Include\NiVersion.h`
  (2,503 B). The formalizer did NOT read its content (executor re-derives
  ms_uiNifMaxVersion from source and quotes exact lines + file SHA256).
- P4 candidate located (formalizer did NOT hash it): the GB112 Evaluation
  installed SDK lib
  `D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib`
  = 3,073,590 B — EXACT match with the P4 size pin (~3,073,590 B). The
  executor re-hashes it during inventory and verifies the SHA256 prefix
  `FF4519AF`. (Note: many other NiMain.lib copies exist across Gb12_Source
  SDK configs, gb12_build, and Gb26_src — the P4 pin is the GB112
  Evaluation VC71 ReleaseLib one; the executor records the full lib census
  per G-INV-1.)

## 5. SELECTION-BASIS INPUT ARTIFACT VERIFICATION (mechanical, oracle-independent)

The T-corpus preregistration basis (see SELECTION.md) was mechanically
validated by the formalizer with a proper CSV parser (Import-Csv), NOT by
naive line counting:

- `docs/nif/corpus/pcg953_nif_manifest.csv` — 2,827,906 B;
  SHA256 (formalizer-computed 2026-10-03):
  `2BE0DEFC9C09FF26371528A4601C10216AC3013717A244EB0652169123989B59`.
  Logical DATA_ROWS (Import-Csv) = **5,596**. Version distribution:
  `10.1.0.0 = 4838`, `4.1.0.12 = 757`, `4.0.0.2 = 1` — EXACT match with the
  P3 Models.bnt census claim (4,838 + 757 + 1 = 5,596). Row `218757.nif`
  IS PRESENT. Schema includes the columns needed for mechanical selection:
  `name, size, sha256, version, parse_status, num_blocks, ...`.
- `docs/audits/PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915/01_RAW/NIF_VERSION_CENSUS.csv`
  — SHA256 (formalizer-computed):
  `962B10ABCB38F98A14F18950E66E30E65B835648D810B62979DFA8517960585D`;
  5,597 physical lines = 1 header + 5,596 per-entry rows (per-entry:
  name, size_stored, offset, sha256_stored, version, scan_status).

**P3 discrepancy record (H4 discipline — both claims recorded, no silent
pick):** the parent dispatch's P3 wording says the manifest is "the 9.3.5
manifest (5,611 files) — different container; never conflate the two",
while the formalizer's proper-CSV measurement gives 5,596 logical rows
whose version distribution EXACTLY matches the Models.bnt census, and the
manifest's own README (`docs/nif/corpus/README.md`) states it IS the
Models.bnt inventory ("every NIF (5,596 rows) in the PCG_9_3_5 corpus
(pc_install\Data\Models\Models.bnt, SHA256 c950a8c2...)"). The value
5,611 reproduces as a NAIVE PHYSICAL-LINE artifact: the file has 5,612
physical lines (header + 5,596 logical rows + 16 extra physical lines from
quoted fields containing embedded newlines), so "5,612 - 1 header = 5,611"
is a line-count artifact, not a file count. The executor must reconcile
this during Phase A with proper CSV parsing (G-INV-1/G-VER-1 lineage) and
record the resolution; until then BOTH claims stand recorded here. The
"never conflate the two denominators" instruction itself remains binding:
the Models.bnt census (5,596 entries) and any other-container manifest are
distinct denominators and must never be merged in a claim.

Machine-readability note (L10): any census of this manifest MUST use a
real CSV parser (embedded newlines inside quoted fields make physical-line
counts wrong by 16 in this file).

## 6. PRIOR CANON PINS TO RECONCILE (recorded verbatim from the parent dispatch; executor re-verifies each from source)

- **P1**: Gb12 `NiVersion.h` `ms_uiNifMaxVersion` = 10.2.0.0 (claimed path
  `D:\gamebyroengine\extracted\Gb12_Source\SDK\Win32\Include\NiVersion.h`;
  source: interrupted 218757 run `00_CONTROL/SELECTION.md` — "Gb12 reader
  accepts NIF up to 10.2.0.0 (PE-MASTER-verified NiVersion.h)" — citing an
  earlier PE-MASTER verification). Executor: re-derive from source, quote
  exact lines + file SHA256. [Formalizer: path EXISTS, 2,503 B; content not
  read by the formalizer.]
- **P2**: Gb12 `NiObject.cpp` per-block GroupID u32 engine range
  5.0.0.6 <= v < 10.1.0.114 (source: audited run
  PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915). Executor: re-derive.
- **P3**: Models.bnt 9.3.5 census: 5,596 entries = 4,838 x 10.1.0.0 +
  757 x 4.1.0.12 + 1 x 4.0.0.2 (audited canon; Models.bnt SHA
  C950A8C2...). Distinct denominator: `docs/nif/corpus/pcg953_nif_manifest.csv`
  = the 9.3.5 manifest (parent wording: "5,611 files — different
  container"; see the discrepancy record in section 5 above). Executor:
  reconcile with proper CSV parsing; never conflate denominators.
- **P4**: GB112 Evaluation SDK NiMain.lib identity: SHA256 prefix
  `FF4519AF`, ~3,073,590 B (source: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914
  F5). Executor: re-hash the installed evaluation SDK lib during inventory.
  [Formalizer: size-matching candidate located — see 4.8.]
- **P5**: The 218757 pair data-side pins (templates.vfs record 4057
  {A=218757, B=218758}; "218757.nif" @Models.bnt 395,283,797; sandbox copy
  57,316 B; "218758.bvi" @Volumes.bnt 3,712,726) — CONTEXT ONLY; this run
  does NOT decode .bvi (record NOT_CHECKED; MindArk volume format is out
  of scope for the Gamebryo-oracle question). Reference cross-check values
  from the interrupted run's `01_RAW/EXTRACT_PROVENANCE.json` (SHA256
  B8EF44CA84714D9B94BBE10FAF66FBFEF087F11F464B0ECED4EF01019F7FF595,
  read-only): Models.bnt index_start 395,262,727 / entry_count 5,596;
  "218757.nif" entry_index 781, name_file_offset 395,283,797, payload
  offset 116,223,520, size 57,316, stored payload SHA256
  3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36,
  header "Gamebryo File Format, Version 10.1.0.0", num_blocks 66;
  "218758.bvi" entry_index 608, name_file_offset 3,712,726, payload offset
  1,672,904, size 652. These reference values are UNVERIFIED_REFERENCE
  (cross-check only); this run re-extracts T1 fresh from Models.bnt.
- **P6**: Prior runs used Gb12/Gb112 as oracle
  (NIF_10_1_BASELINE_ROSETTA s15 engine-transcribed walker; NINODE_SLOT17
  minicheck: GB112 NiNode slot17=SetSelectiveUpdateFlags, GB12
  slot17=ApplyTransform) — the new inventory must reconcile file identities
  with those runs' citations. Decoder-lineage reference pins (from the
  ROSETTA package's `00_CONTROL/SCRIPT_SHA256.csv`, read-only):
  `s13_schema_field_identity_v2.py` =
  E3368507FCA5E9FDAE2AEADC1F9A55137DAEE242FBBDB5F410027C64455B4893 (12,487 B);
  `s14_world_slice_validator_fieldidentity_v2.py` =
  464D07E5203A8BA1D95ED1B3A5B94C6A932A8AABF979903490C893DD94293C04 (3,458 B);
  `s06_world_slice_validator.py` =
  51AC25406DF00F3A1EED79E6573C779733FC1F95696EE045CE1C27202767BBC0 (31,291 B).
- **P7**: Prior NifViewer 2.6 launch attempt on 218757.nif FAILED
  (`screen_error.png`, 61,742 B, in the interrupted run sandbox — EXISTS,
  verified) — missing-deps class suspected but unproven. The tool phase
  must either establish the exact blocker class or achieve a working
  original-tool run; record honestly.

## 7. FILES READ BY THE FORMALIZER (with hashes where load-bearing)

| File | Role | SHA256 |
|---|---|---|
| `00_PROJECT_CONTEXT\PE_MASTER_LOOP_STATE.json` | parent contract verification (loop id, mission, authorization_quote, checkpoint, allowed_paths, deadline 2026-10-03T23:13:15Z / drain 23:23:15Z) | 93DE11B540F8C8F485C7278C63045EE3299E886CA7DDE4B2A38030A55DA347BC |
| `00_PROJECT_CONTEXT\PE_MASTER_LOOP_EVENTS\8f0ef23a-...-1-c4f783ef....json` | START event (mission/authorization cross-check) | read; consistent with LOOP_STATE |
| `docs\nif\corpus\pcg953_nif_manifest.csv` | selection-basis verification (section 5) | 2BE0DEFC9C09FF26371528A4601C10216AC3013717A244EB0652169123989B59 |
| `docs\nif\corpus\README.md` | manifest provenance (section 5 discrepancy record) | read in full (32 lines) |
| `docs\audits\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\01_RAW\NIF_VERSION_CENSUS.csv` | census artifact pin (head 30 lines of 5,597; schema verified) | 962B10ABCB38F98A14F18950E66E30E65B835648D810B62979DFA8517960585D |
| `docs\audits\PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915\00_CONTROL\SCRIPT_SHA256.csv` | decoder-lineage pins (P6) | read in full (20 lines) |
| `docs\audits\PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003\00_CONTROL\SELECTION.md` | P1 citation source (read-only) | 30EA69F9A29F1554D2984415110C5B64CE1F57E8F31822D3D40A702106FD70D9 |
| `docs\audits\PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003\01_RAW\EXTRACT_PROVENANCE.json` | P5 reference values (read-only) | B8EF44CA84714D9B94BBE10FAF66FBFEF087F11F464B0ECED4EF01019F7FF595 |
| `AUDIT_ENTRYPOINT.md` | persistence target (row format; first 54 lines read) | 009272136ACA01DB84D359FAA3A2AA483248470AE34E13536043D449EA039877 |
| `00_PROJECT_CONTEXT\PE_MASTER_ACTIVE_ORDER.md` | historical context only (v4/v7 2026-09-06 order; superseded by LOOP_STATE for the current mission) | read head (40 lines) |

FORMALIZER FULL_READ_LOG: LOOP_STATE (all 42 lines), README.md (all 32),
interrupted SELECTION.md (all 37), EXTRACT_PROVENANCE.json (all 122),
SCRIPT_SHA256.csv (all 20), ACTIVE_ORDER (head 40/175 — historical only),
census CSV (head 30/5,597 — schema-level verification, NOT a full read),
manifest CSV (header + 2 sample rows via parser + aggregate stats — NOT a
full read), AUDIT_ENTRYPOINT (head 54 — row-format verification only).

FORMALIZER NOT_CHECKED (deliberately — executor duties): archive interiors
(listing only = executor Phase A); SHA256 of the 6 archives, Models.bnt,
Volumes.bnt, NiVersion.h content, NiMain.lib hashes; the ROSETTA census
full body; the manifest full body; any NIF payload content; any Gamebryo
source content. The formalizer performed NO scientific analysis.

## 8. OBSERVATIONS FOR THE EXECUTOR (binding notes)

1. The manifest's `parse_status` is PASS for the audited census (per its
   README: 5596/5596 PASS by the frozen R61 parser). The manifest is a
   PRIOR audited project artifact — using it for mechanical selection is
   oracle-independent (it is NOT an output of the new GAMEBRYO_ORACLE_TOOL).
2. Embedded newlines exist in quoted manifest fields (16 extra physical
   lines) — parse with a real CSV parser (see section 5).
3. `tools/` contains 16 loose existing forensic scripts; the new tool must
   go into its own `tools/gamebryo_oracle/` subtree without touching them.
4. The interrupted-run sandbox (`PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003\sandbox\`)
   is READ-ONLY reference for T1 cross-check only; this run re-extracts
   T1 fresh from Models.bnt into THIS run's sandbox (G-SEL-2).
