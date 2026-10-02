# PREFLIGHT (GATE S0) — PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002

Measured by the executor (pe-reconstruction) at execution start, BEFORE any science.
Method: PowerShell 5.1 — `git rev-parse HEAD`; `Get-Item` (size);
`Get-FileHash -Algorithm SHA256` (hashes); `git status --short` (tree census).
Contract SHA256 re-verified before measurement:
- RUN_CONTRACT.md = 27,270 bytes — SHA256 24B3A5599FA16FE1E465BB82462344B35362CA7E1185F712EBC7730065D28657 — MATCH CONTRACT_FREEZE.json (gate re-verification, measured before any science).

## Measured ACTUAL values (executor, 2026-10-02)

| FIELD | ACTUAL VALUE | EXPECTED (PREFLIGHT_EXPECTED.md) | VERDICT |
|---|---|---|---|
| ACTUAL_HEAD | 9203b6d1ad5025f4158d5165863594132aaac49f | 9203b6d1ad5025f4158d5165863594132aaac49f | MATCH |
| ACTUAL_EXE_SIZE_BYTES | 8015872 | 8015872 | MATCH |
| ACTUAL_EXE_SHA256 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | MATCH |
| ACTUAL_VFS_SIZE_BYTES | 174864 | 174864 | MATCH |
| ACTUAL_VFS_SHA256 | C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4 | C3899C3E88D72CE12CEF9B8A4F5E73B26632BB1A3207C950FF2BC40FD9C94AC4 | MATCH |

EXE file version metadata (read-only, `VersionInfo`): FileVersion=9.3.5.6746,
ProductVersion=9.3.5.6746, ProductName=Entropia Universe, FileDescription=Entropia Universe,
LastWriteTime=2008-09-17T18:56:16.

Git worktree location of HEAD measurement: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (canonical repo working copy; read-only repo ops: rev-parse + status only; no fetch performed — read-only discipline).

Git status --short at S0 (executor measurement, before writing any package file):
```
?? docs/audits/PE_935_20002_PAYLOAD30_CONSUMER_R1_20261002/
?? docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
?? docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/
?? docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/
?? experiments/
```
= the 5 pre-existing untracked groups per RUN_CONTRACT.md §0 DIRTY_TREE_INVENTORY
PLUS the new run package dir (expected; formalizer created it). No staged entries; no modified tracked entries.

READ_ONLY_STATUS = CONFIRMED (all source accesses read-only; scripts execute only from OUTPUT_ROOT\03_SCRIPTS; originals never modified).

## GATE S0 PREDICATE (RUN_CONTRACT.md §A S0_INPUT_IDENTITY, fail-closed)

ACTUAL_HEAD == 9203b6d1ad5025f4158d5165863594132aaac49f : TRUE
AND EXE size/SHA256 == pinned : TRUE
AND VFS size/SHA256 == pinned : TRUE

GATE_S0_INPUT_IDENTITY = PASS.
No mismatch => no BLOCKED_INPUT_IDENTITY_MISMATCH; science may start.

measured_at_utc = 2026-10-02 (executor session; PowerShell measurement block recorded above)
