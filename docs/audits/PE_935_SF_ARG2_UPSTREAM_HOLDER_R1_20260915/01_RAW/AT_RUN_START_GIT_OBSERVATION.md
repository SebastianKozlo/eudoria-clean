# AT_RUN_START_GIT_OBSERVATION — PE_935_SF_ARG2_UPSTREAM_HOLDER_R1_20260915

Measured: 2026-09-15T05:25:54Z (executor-local 2026-09-14 22:25:54 Pacific Daylight Time; R2 note per QC_AUDIT.md P3-5: the R1 label said "Pacific Standard Time" - September is PDT (UTC-7); the numeric pair was already internally consistent)
Measurer: pe-reconstruction executor (read-only git commands only; ZERO mutations performed in this observation)
Command context: `git -C D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean <cmd>` (PowerShell 5.1)

## rev-parse HEAD
```
895bbc8baa2d002c562b7e5b43212e38c2abb16f
```

## rev-parse --abbrev-ref HEAD
```
master
```

## rev-parse origin/master
```
895bbc8baa2d002c562b7e5b43212e38c2abb16f
```

## ls-remote origin master
```
895bbc8baa2d002c562b7e5b43212e38c2abb16f	refs/heads/master
LSREMOTE_EXIT=0
```

## status --porcelain=v1 (full output)
```
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
?? experiments/
```

Interpretation (G1 start check):
- HEAD == origin/master == ls-remote == contract BASE_SHA `895bbc8baa2d002c562b7e5b43212e38c2abb16f` → MATCH.
- Dirty set at run start == exactly the two pre-existing untracked directories declared in the contract:
  `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/` and `experiments/`.
- Everything tracked is clean (no modified/staged entries in porcelain output).

## worktree list
```
D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean                              895bbc8 [master]
D:/Eudoria_Reconstruction/worktrees/PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1 5290e79 [audit/pe935-ninode-slot17-gb-oracle-minicheck-r1]
D:/Eudoria_Reconstruction/worktrees/WORK_AUDIT_REPORTS                          1312f89 [audit/work-audit-reports]
```

Notes:
- The main worktree (this run's workspace) is at BASE_SHA 895bbc8 on master.
- `audit/work-audit-reports` worktree = independent auditor workspace, NEVER touched by this run (contract §11 WORK-AUDITOR SEPARATION).
- The `PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1` worktree is a foreign worktree on a different branch/commit (5290e79); not part of this run's scope; not touched.

## Commit identity of BASE_SHA (read-only inspection)
`git -C ... show -s --format='%H %ci %an' 895bbc8`:
(recorded in 00_CONTROL/AMEND_LOG_R1.md entry A8; R2 correction per QC_AUDIT.md P3-6: the R1 note pointed at "01_RAW/GIT_OBSERVATION_COMMANDS.txt", a file that was never created - the command transcript has always lived in AMEND_LOG_R1.md A8)
