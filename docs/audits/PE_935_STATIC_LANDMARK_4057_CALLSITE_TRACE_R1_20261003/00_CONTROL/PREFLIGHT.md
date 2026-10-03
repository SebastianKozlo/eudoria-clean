# PREFLIGHT — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

Executor: pe-reconstruction. Mode: STATIC_ONLY. All measurements below were
executed by this executor in its own session before any science phase
(contract §5). Times UTC-local (Windows local clock, 2026-10-03).

## 1. GIT STATE (measured this session)

```text
git fetch origin            : completed (no errors)
git rev-parse HEAD          : a4992788982f8ff7f59866fa46aad1176897c69d
git rev-parse origin/master : a4992788982f8ff7f59866fa46aad1176897c69d
git ls-remote origin master : a4992788982f8ff7f59866fa46aad1176897c69d (refs/heads/master)
BASE_MISMATCH               : NO  (HEAD == origin/master == live remote == EXPECTED_BASE_SHA)
NON-UNTRACKED STATUS        : EMPTY (0 tracked modifications, 0 staged changes)
UNTRACKED (5, foreign, untouched):
  ?? docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/
  ?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
  ?? docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/
  ?? docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/
  ?? experiments/
```

FAIL-CLOSED RESULT: BASE verified; no HARD_STOP. The five foreign untracked
groups are read-only input; this run does not touch, modify or stage them.

## 2. INPUT PHYSICAL IDENTITIES (re-hashed this session, PowerShell Get-FileHash)

| Input | Path | Size (B) | SHA256 (measured) | Pin match |
|---|---|---|---|---|
| Client EXE (PCG 9.3.5) | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8,015,872 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | YES |
| templates.vfs | D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\templates.vfs | 560,788 | BE57818C7516F8C6C8A68DF427591567DD0E5A421934AC24ADA57E8261F65B77 | YES |
| Models.bnt (9.3.5) | D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt | 395,412,868 | C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0 | YES |
| Volumes.bnt | D:\Eudoria_Reconstruction\pcg_install\Data\Volumes\Volumes.bnt | 3,746,375 | 6AD8BA3C5AD6F7534F91C1956A0E36485A49BBEF3FFA918CBDDC0C68EDBABC09 | YES |

```text
WRONG_TARGET_BUILD = NO (EXE hash+size match the pinned 9.3.5 build)
ERA DISCIPLINE = PCG 9.3.5 ONLY (pcg_install paths).
  The 2003-era corpus at D:\Eudoria_Reconstruction\01_Original_Files
  (Models.bnt 1322ADF2..., EntropiaUniverse_Runtime exe E706C715...,
  VFS\templates.vfs DDE352A9...) is the WRONG ERA for this run and was NOT used.
```

## 3. CANON/CONTEXT READS (contract §5.6 minimum — all read this session)

```text
AUDIT_ENTRYPOINT.md (repo root; CURRENT STATE + LATEST RUNS)
docs/audits/PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003/
  01_ANALYSIS/CURRENT_CLAIM_STATE.md
  01_ANALYSIS/DEFERRED_PLACEMENT_LEADS.md
  03_REPORT/FINAL_REPORT.md (sections 1-4 read in full session context)
  03_REPORT/PE_MASTER_REVIEW.md
docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/
  02_ANALYSIS/TRACE_EDGE_BLOCKS.md (E1-E12)
  02_ANALYSIS/CLAIM_MATRIX.csv
  05_ORACLE/ORACLE_RECORDS.md
  06_REPORT/FINAL_REPORT.md
plus (adaptation reference, own bounded re-implementation):
  03_SCRIPTS/c1_census.py (VFS walk + BNT2 index implementation)
```

Canon facts reused as CONTEXT only (leads/canon, not evidence for this
call-site): templates.vfs record layout (magic ArkVFS02, base u32@8, records
from file offset 16, header {id,size,ver,crc32} 16 B, stride
ceil((16+size)/base)*base, 5,438 records, 0 CRC-fail, record id2=4508 @96,496
A=296445); registry lookup chain FUN_0072FA30 -> parse -> RB-tree ->
FUN_0072F580 (ABI registry_this.FUN_0072F580(id2), ECX=registry_this, id2 =
stack argument) -> A-read getter FUN_007CE1E0 ([this+8]) -> request pair
{0x66=MODEL, A} + scheduler callback 0x008BD720; Models.bnt BNT2 trailer index
(5,596 entries, index_start 395,262,727, "296445.nif" @395,268,773); B ->
Volumes.bnt .bvi (1,666/1,666 B-join, JOIN R1 canon). The 4057 chain is measured
independently by this run.

## 4. ENVIRONMENT INVENTORY (measured this session)

```text
OS            : Windows (win32), PowerShell 5.1
Python        : 3.12.10 (local, python.exe) — used for all own scripts
capstone      : NOT INSTALLED locally (ModuleNotFoundError) — not used; no
                packages installed this run (no user approval sought/needed:
                Ghidra 11.2.1 is the authorized disassembler/decompiler)
Ghidra        : D:\ghidra_11.2.1_PUBLIC (11.2.1 PUBLIC, build 2024-11-05)
                headless: D:\ghidra_11.2.1_PUBLIC\support\analyzeHeadless.bat
                skill recipes: pe-ghidra-re (fresh project rule, sandbox copy,
                hash-after-final-edit, isCall() filter, measured/interpreted/
                errors JSON)
JDK           : C:\Program Files\Microsoft\jdk-21.0.12.8-hotspot (per skill)
```

## 5. RUN-LOCAL SCRATCH / LOCAL-ONLY DISCIPLINE

```text
Repo package (NEW, only new directory): docs/audits/
  PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003/  (created fresh;
  verified NOT pre-existing by PE-MASTER preflight and by this executor's own
  directory listing of docs/audits at BOOT)
LOCAL-ONLY run scratch (OUTSIDE the repo, never committed):
  D:\Eudoria_Reconstruction\99_Audits\PE_935_LANDMARK4057_GHIDRA_SCRATCH_20261003\
    - sandbox copy of Entropia.exe (hash-verified vs pin before Ghidra import)
    - fresh Ghidra project LANDMARK4057 (auto-analysis + postscript dumps)
    - raw analyzeHeadless logs
Proprietary payloads (Entropia.exe, templates.vfs, Models.bnt, Volumes.bnt,
NIF/BVI payloads) stay LOCAL_ONLY; to the repo go ONLY identity metadata,
hashes, sizes, offsets, bounded byte windows, own scripts, reports, derived
evidence (contract §7).
No client launch. No dynamic instrumentation. No network capture. No runtime
work. STATIC_ONLY enforced for all phases.
```

## 6. PREFLIGHT VERDICT

```text
BOOT_PASS = YES
HARD_STOP = NONE
```
