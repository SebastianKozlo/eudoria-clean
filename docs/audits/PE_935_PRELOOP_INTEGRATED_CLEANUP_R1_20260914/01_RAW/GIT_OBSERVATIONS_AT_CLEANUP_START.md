# GIT OBSERVATIONS — AT_CLEANUP_START

- RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914
- OBSERVATION_LABEL: AT_CLEANUP_START
- OBSERVER: pe-reconstruction (cleanup executor; parent loop 2ed038db-5d2e-4e7e-b679-2d29bf57501a)
- REPO: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
- SNAPSHOT_TAKEN: 2026-09-14 15:55:38 -07:00 (local, PowerShell Get-Date)
- The executor performed ZERO git mutations (all commands below are read-only).
- This file is the timestamped G1 record required by RUN_CONTRACT.md section B.2 / W9.

## 1. HEAD / branch / local origin ref

```
$ git rev-parse HEAD
a7a6c756bc35a5b28220236e9ac649131206aeb3
$ git branch --show-current
master
$ git rev-parse origin/master
a7a6c756bc35a5b28220236e9ac649131206aeb3
```

- VERDICT: HEAD == BASE_SHA pin (a7a6c756bc35a5b28220236e9ac649131206aeb3) == local
  origin/master ref. No drift at cleanup start. G0 component PASS.

## 2. Live remote (git ls-remote origin, observed 2026-09-14 15:55 -07:00)

```
$ git ls-remote origin master
a7a6c756bc35a5b28220236e9ac649131206aeb3	refs/heads/master
$ git ls-remote origin audit/pe935-ninode-slot17-gb-oracle-minicheck-r1
5290e79e0dc469c70605f35c125d7b727f9f7a6b	refs/heads/audit/pe935-ninode-slot17-gb-oracle-minicheck-r1
```

- VERDICT: live remote master == local HEAD == BASE_SHA (no drift). The SLOT17 branch is
  present on the remote at the pinned tip 5290e79 (no force-push / rewrite observed).

## 3. git status --short (observed 2026-09-14 15:55:38 -07:00)

```
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
?? docs/audits/PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914/
?? experiments/
```

- Exactly 3 untracked entries, 0 modified, 0 staged. Matches the expected
  AT_CLEANUP_START set (RUN_CONTRACT.md B.2): FIRSTCALL + experiments/ + this cleanup
  package directory. G0 component PASS.

## 4. git worktree list

```
D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean                              a7a6c75 [master]
D:/Eudoria_Reconstruction/worktrees/PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1 5290e79 [audit/pe935-ninode-slot17-gb-oracle-minicheck-r1]
```

## 5. SLOT17 branch integrity

```
$ git rev-parse audit/pe935-ninode-slot17-gb-oracle-minicheck-r1
5290e79e0dc469c70605f35c125d7b727f9f7a6b      (== pinned tip)
$ git rev-parse 5290e79e0dc469c70605f35c125d7b727f9f7a6b^
3644e5ac9cbf7b5445861e7f5342fb8642741346      (== pinned parent)
$ git status --porcelain   (in the SLOT17 worktree)
(0 entries — clean)
```

- Worktree D:\Eudoria_Reconstruction\worktrees\PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1:
  clean; HEAD == pinned tip. G2 components PASS.

## 6. Commit timestamps (git log --format)

```
a7a6c756bc35a5b28220236e9ac649131206aeb3
  author 2026-09-14 14:40:54 -0700, commit 2026-09-14 14:40:54 -0700
  subject: audits: PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 (Desktop R2 post-audit
  amendment: F1 branch (b) — census row 0x0040525B REJECTED->POSSIBLE_ALIAS, canonical
  3643=2/619/3022/0, ... path-limited)
5290e79e0dc469c70605f35c125d7b727f9f7a6b
  author 2026-09-14 15:11:43 -0700, commit 2026-09-14 15:11:43 -0700
  subject: audits: NiNode slot17 Gamebryo oracle mini-check R1
```

## 7. master reflog chronology (git reflog master -n 6)

```
a7a6c756 master@{0} commit: audits: PE_935_SCENEFEEDER_LINK30_AMEND_R2_20260914 (...) | 2026-09-14 14:40:54 -0700
3644e5ac master@{1} commit: audits: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 (...) | 2026-09-14 10:12:52 -0700
1a490eed master@{2} commit: audits: PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914 (...) | 2026-09-14 06:33:29 -0700
```

- FACTUAL READING (git evidence only): local master advanced 3644e5ac -> a7a6c756 at
  14:40:54 -0700, i.e. BEFORE the SLOT17 branch commit 5290e79 (15:11:43 -0700). At
  SLOT17 publication time local master was already a7a6c756. (Consistent with
  GIT_OBSERVATIONS_AT_FORMALIZE.md section 7; the AUD-F1 temporal-scope adjudication is
  in 02_ANALYSIS/SLOT17_AUDIT_FINDINGS_DISPOSITION.md.)

## 8. SLOT17 commit tree census (git ls-tree -r 5290e79 --name-only, AUD-F2 evidence)

Per-directory counts for docs/audits/PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914/
inside commit 5290e79 (executor's own count of the ls-tree output, observed 15:57 -07:00):

- 00_CONTROL: 6 (RUN_CONTRACT.md, SOURCE_IDENTITIES.json, coff_disasm_symbol.py,
  entropia_disasm_7b5390.py, entropia_rtti_probe.py, parse_coff_vtable.py)
- 01_RAW: 3 (ENTROPIA_007B5390_DISASM.txt, GB112_SOURCE_LOCATORS.md, GB12_SOURCE_LOCATORS.md)
- 02_ANALYSIS: 6 (CLASS_HIERARCHY_AND_VTABLE_MAP.md, CROSS_VERSION_COMPARISON.csv,
  ENTROPIA_SLOT17_FINGERPRINT.md, GETOBJECTBYNAME_FINGERPRINT.md, NEGATIVE_CONTROLS.md,
  OFFSET90_ORACLE.md)
- 03_EVIDENCE: 16 (ENTROPIA_NIRTTI_STATIC_INIT.txt, ENTROPIA_RTTI_CHAIN_PROBE.json,
  ENTROPIA_SLOT_NEIGHBORS_DISASM.txt, EVIDENCE_INDEX.csv, GB112_NIAVOBJECT_CTOR_DISASM.txt,
  GB112_NIAVOBJECT_GETOBJECTBYNAME_DISASM.txt, GB112_NIAVOBJECT_UPDATEWORLDDATA_DISASM.txt,
  GB112_NIMAIN_LIB_VTABLE_DUMP.json, GB112_NINODE_GETOBJECTBYNAME_DISASM.txt,
  GB12_CHAIN_OBJ_VTABLE_DUMP.json, GB12_NIAVOBJECT_CTOR_DISASM.txt,
  GB12_NIAVOBJECT_GETOBJECTBYNAME_DISASM.txt, GB12_NIAVOBJECT_UPDATEWORLDDATA_DISASM.txt,
  GB12_NINODE_GETOBJECTBYNAME_DISASM.txt, GB12_NINODE_OBJ_VTABLE_DUMP.json, README.md)
- 06_REPORT: 4 (HANDOFF.md, MANIFEST_SHA256.csv, REPORT.md, STAGE_ACCEPTANCE_GATES.csv)
- TOTAL: 35 == the pinned census (03_EVIDENCE=16, 06_REPORT=4).

## 9. SLOT17 worktree package file mtimes (AUD-F3 evidence, observed 15:58 -07:00)

PowerShell Get-ChildItem -Recurse -File LastWriteTime census (35 files), relative to the
package root, format "relpath | mtime | size":

```
00_CONTROL\coff_disasm_symbol.py                  | 2026-09-14 14:24:07 | 8482
00_CONTROL\entropia_disasm_7b5390.py               | 2026-09-14 14:18:25 | 4004
00_CONTROL\entropia_rtti_probe.py                  | 2026-09-14 14:11:34 | 7166   [CARRIED <14:31]
00_CONTROL\parse_coff_vtable.py                   | 2026-09-14 14:12:14 | 12158  [CARRIED <14:31]
00_CONTROL\RUN_CONTRACT.md                        | 2026-09-14 15:07:53 | 5098
00_CONTROL\SOURCE_IDENTITIES.json                 | 2026-09-14 15:08:27 | 8576
01_RAW\ENTROPIA_007B5390_DISASM.txt               | 2026-09-14 14:57:05 | 5890
01_RAW\GB112_SOURCE_LOCATORS.md                   | 2026-09-14 15:07:43 | 6047
01_RAW\GB12_SOURCE_LOCATORS.md                    | 2026-09-14 14:26:37 | 6355   [CARRIED <14:31]
02_ANALYSIS\CLASS_HIERARCHY_AND_VTABLE_MAP.md     | 2026-09-14 15:07:16 | 10373
02_ANALYSIS\CROSS_VERSION_COMPARISON.csv          | 2026-09-14 15:06:46 | 6925
02_ANALYSIS\ENTROPIA_SLOT17_FINGERPRINT.md        | 2026-09-14 15:04:16 | 9776
02_ANALYSIS\GETOBJECTBYNAME_FINGERPRINT.md        | 2026-09-14 15:07:19 | 5682
02_ANALYSIS\NEGATIVE_CONTROLS.md                  | 2026-09-14 15:06:22 | 7098
02_ANALYSIS\OFFSET90_ORACLE.md                    | 2026-09-14 15:05:56 | 7633
03_EVIDENCE\ENTROPIA_NIRTTI_STATIC_INIT.txt      | 2026-09-14 14:59:53 | 3596
03_EVIDENCE\ENTROPIA_RTTI_CHAIN_PROBE.json        | 2026-09-14 14:39:07 | 7111
03_EVIDENCE\ENTROPIA_SLOT_NEIGHBORS_DISASM.txt    | 2026-09-14 14:57:05 | 17126
03_EVIDENCE\EVIDENCE_INDEX.csv                    | 2026-09-14 15:09:02 | 3932
03_EVIDENCE\GB112_NIAVOBJECT_CTOR_DISASM.txt      | 2026-09-14 14:54:34 | 2487
03_EVIDENCE\GB112_NIAVOBJECT_GETOBJECTBYNAME_DISASM.txt | 2026-09-14 14:54:34 | 1912
03_EVIDENCE\GB112_NIAVOBJECT_UPDATEWORLDDATA_DISASM.txt | 2026-09-14 14:54:34 | 1623
03_EVIDENCE\GB112_NIMAIN_LIB_VTABLE_DUMP.json     | 2026-09-14 14:53:20 | 30110
03_EVIDENCE\GB112_NINODE_GETOBJECTBYNAME_DISASM.txt | 2026-09-14 14:54:33 | 1784
03_EVIDENCE\GB12_CHAIN_OBJ_VTABLE_DUMP.json       | 2026-09-14 14:53:21 | 78308
03_EVIDENCE\GB12_NIAVOBJECT_CTOR_DISASM.txt       | 2026-09-14 14:54:34 | 2476
03_EVIDENCE\GB12_NIAVOBJECT_GETOBJECTBYNAME_DISASM.txt | 2026-09-14 14:54:34 | 1610
03_EVIDENCE\GB12_NIAVOBJECT_UPDATEWORLDDATA_DISASM.txt | 2026-09-14 14:56:08 | 4961
03_EVIDENCE\GB12_NINODE_GETOBJECTBYNAME_DISASM.txt | 2026-09-14 14:54:34 | 1747
03_EVIDENCE\GB12_NINODE_OBJ_VTABLE_DUMP.json     | 2026-09-14 14:53:20 | 6418
03_EVIDENCE\README.md                            | 2026-09-14 15:08:55 | 2053
06_REPORT\HANDOFF.md                             | 2026-09-14 15:11:05 | 4933
06_REPORT\MANIFEST_SHA256.csv                    | 2026-09-14 15:11:31 | 3604
06_REPORT\REPORT.md                              | 2026-09-14 15:09:21 | 10325
06_REPORT\STAGE_ACCEPTANCE_GATES.csv             | 2026-09-14 15:09:43 | 8352
```

Note: the "[CARRIED <14:31]" annotations above mark the five files whose mtimes precede
the completing-session start (14:31 local) per the AUD-F3 pin — the raw mtime values are
the measurement; the classification is recorded in
02_ANALYSIS/SLOT17_AUDIT_FINDINGS_DISPOSITION.md.

## 10. Verdict

All AT_CLEANUP_START observations match the AT_FORMALIZE pins (RUN_CONTRACT.md section B):
HEAD == BASE_SHA; branch master; origin/master == BASE_SHA locally and on the live
remote; SLOT17 branch tip == 5290e79 locally and remotely; parent == 3644e5ac; worktree
clean; untracked set == exactly the three expected entries. NO git mutations performed.
