# PREFLIGHT — PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z

All measurements performed by this executor, 2026-10-03, from
CANONICAL_REPO_ROOT = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean unless noted.

## Git baseline (contract §2)

| Query | Command | UTC | Exit code | Returned SHA |
|---|---|---|---|---|
| Fetch | `git fetch origin` | 2026-10-03T07:14:00Z | 0 | n/a |
| Local HEAD | `git rev-parse HEAD` | 2026-10-03T07:14:00Z | 0 | 743f9fac2dd5c9e94eaba074b46903b4d3686b46 |
| origin/master | `git rev-parse origin/master` | 2026-10-03T07:14:00Z | 0 | 743f9fac2dd5c9e94eaba074b46903b4d3686b46 |
| Live remote | `git ls-remote --exit-code origin refs/heads/master` | 2026-10-03T07:14:00Z | 0 | 743f9fac2dd5c9e94eaba074b46903b4d3686b46 |

- EXPECTED_BASE_SHA = 743f9fac2dd5c9e94eaba074b46903b4d3686b46
- All three measurements MATCH EXPECTED_BASE_SHA → BASELINE PASS.
- REMOTE_STATE_AT_START: live remote master = 743f9fac2dd5c9e94eaba074b46903b4d3686b46
  (equal to BASE_SHA; no observed remote change at start of run).

## Working tree

- `git status --porcelain`: ZERO tracked changes (no `M`/`A`/`D` rows).
- Foreign untracked groups (present, NOT touched, NOT staged — matches dispatch list):
  - `docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/`
  - `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`
  - `docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/`
  - `docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/`
  - `experiments/`
- Result: WORKING_TREE PASS.

## Physical source identities

| Source | Physical path | Size (B) | SHA256 | Status |
|---|---|---|---|---|
| Client EXE | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8015872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | MATCH (contract: same) |
| 20002.vfs | D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs | 174864 | C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4 | PINNED (this run's copy) |
| NiMain.lib (Gb 1.1.2 Eval) | D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\SDK\Win32\Lib\VC71\ReleaseLib\NiMain.lib | 3073590 | FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597 | MATCH (contract: same) |
| Gb12 source root | D:\gamebyroengine\extracted\Gb12_Source\ | dir | not hashed (tree) | EXISTS (10 top dirs: AppFrameworks, Build, CoreLibs, Documentation, PSX2Viewer, Samples, SDK, ThirdPartyCode, ToolLibs, Tools) |

Note: Entropia.exe (8,015,872 B) is the PCG 9.3.5 client build — this is the input build
for this run (INPUT_BUILD_SHA256 = E7785430...F31). The historical PE2_unpacked_out.exe
(2.2 MB, 56178993...) is a DIFFERENT binary from a different era/track and is NOT the
input build for this run; it is referenced only where historical audit packages did so.

## Lead packages (contract §2) — existence verified

- docs/audits/PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002/ — EXISTS (00_CONTROL, 01_RAW, 02_ANALYSIS, 03_SCRIPTS, 04_QC, 06_REPORT)
- docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/ — EXISTS (00_CONTROL, 01_RAW, 02_ANALYSIS, 03_EVIDENCE, 06_REPORT)
- docs/audits/PE_935_STATIC_INSTANCE_TRACE_R1_20260913/ — EXISTS (00_CONTROL, 01_RAW, 02_ANALYSIS, 03_EVIDENCE, 06_REPORT)

## Run package

- docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/ — verified NOT
  to exist before creation; created fresh at run start.

## PREFLIGHT VERDICT: PASS — RE may proceed.
