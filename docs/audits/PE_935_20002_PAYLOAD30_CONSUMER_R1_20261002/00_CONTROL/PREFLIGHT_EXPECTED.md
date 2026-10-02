# PREFLIGHT_EXPECTED — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Expected input identities for GATE S0 (PREFLIGHT). The executor measures the ACTUAL
values at execution start, BEFORE any science, and records them in
00_CONTROL\PREFLIGHT.md (+ 00_CONTROL\SOURCE_IDENTITY.md) per RUN_CONTRACT.md §6.

## Expected identities

| FIELD | EXPECTED VALUE | SOURCE |
|---|---|---|
| EXPECTED_HEAD | 9203b6d1ad5025f4158d5165863594132aaac49f | human authorization + PE-MASTER preflight 2026-10-02 |
| EXPECTED_EXE_PATH | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | human authorization + PE-MASTER preflight 2026-10-02 |
| EXPECTED_EXE_SIZE_BYTES | 8015872 | human authorization + PE-MASTER preflight 2026-10-02 |
| EXPECTED_EXE_SHA256 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | human authorization + PE-MASTER preflight 2026-10-02 |
| EXPECTED_VFS_PATH | D:\Eudoria_Reconstruction\pcg_install\Data\Parameters\20002.vfs | human authorization + PE-MASTER preflight 2026-10-02 |
| EXPECTED_VFS_SIZE_BYTES | 174864 | human authorization + PE-MASTER preflight 2026-10-02 |
| EXPECTED_VFS_SHA256 | C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4 | human authorization + PE-MASTER preflight 2026-10-02 |

## Formalizer verification (independent re-measurement, 2026-10-02, before package creation)

Measured by the pe-master-auditor formalizer session (read-only; PowerShell 5.1;
git rev-parse / Get-Item / Get-FileHash -Algorithm SHA256):

- ACTUAL_HEAD = 9203b6d1ad5025f4158d5165863594132aaac49f — MATCH (== EXPECTED_HEAD; local origin/master tracking ref identical, not re-fetched — read-only discipline)
- ACTUAL_EXE_SIZE_BYTES = 8015872 — MATCH
- ACTUAL_EXE_SHA256 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — MATCH
- ACTUAL_VFS_SIZE_BYTES = 174864 — MATCH
- ACTUAL_VFS_SHA256 = C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4 — MATCH
- git status --short (pre-creation) = exactly the 5 pre-existing untracked groups (per RUN_CONTRACT.md §0 DIRTY_TREE_INVENTORY) — MATCH
- OUTPUT_ROOT did not exist before package creation — NO COLLISION
- Prior-evidence inputs exist: JOIN R1 04_TOOLS\vfs_common.py; 03_COUNTERCHECKS\AMEND_R2\AMEND_R2_ID2_MEMBERSHIP_20002_48.json; 01_RAW\ (dir) — CONFIRMED PRESENT

FORMALIZER_VERIFICATION = ALL_EXPECTED_IDENTITIES_MATCH.

NOTE: this block is the formalizer's pre-package verification. It does NOT replace the
executor's own S0 preflight — the executor re-measures at execution start and records
ACTUAL values itself (fail-closed against drift after formalization).

## EXECUTOR FILL — measure at execution start, BEFORE any science

ACTUAL_HEAD = 9203b6d1ad5025f4158d5165863594132aaac49f
ACTUAL_EXE_SIZE_BYTES = 8015872
ACTUAL_EXE_SHA256 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31
ACTUAL_VFS_SIZE_BYTES = 174864
ACTUAL_VFS_SHA256 = C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4
ERA = EU 9.3.5 / PCG 9.3.5 (pcg_install corpus)
BUILD = Entropia Universe 9.3.5.6746 (FileVersion from the pinned EXE; 2008-09-17)
READ_ONLY_STATUS = CONFIRMED (all source accesses read-only; scripts ran only from OUTPUT_ROOT\03_SCRIPTS; originals never modified; the client was never launched)
measured_at_utc = 2026-10-02 (executor session; details in 00_CONTROL\PREFLIGHT.md)

(The executor also writes these into 00_CONTROL\PREFLIGHT.md and 00_CONTROL\SOURCE_IDENTITY.md per RUN_CONTRACT.md §6.)

## Mismatch rule (binding)

If HEAD or either physical identity differs: RUN_STATUS = BLOCKED_INPUT_IDENTITY_MISMATCH, HARD_STOP = YES; preserve evidence; do NOT reset the repository; do NOT substitute another executable or VFS; do NOT silently continue on drift.

## Historical / cross-build corpus rule

CD_2003 / JUL_2003 / EU10.x corpora may be used only explicitly labeled HISTORICAL_OR_CROSS_BUILD_ORACLE.

## Ghidra binary-identity requirement (authorization §6)

Prove the analyzed binary is the pinned physical Entropia.exe; for every load-bearing instruction preserve IMAGE_BASE/VA/RVA/FILE_OFFSET/ORIGINAL_BYTES; static conclusions labeled STATIC_ONLY; runtime execution and runtime reachability remain NOT_TESTED.
