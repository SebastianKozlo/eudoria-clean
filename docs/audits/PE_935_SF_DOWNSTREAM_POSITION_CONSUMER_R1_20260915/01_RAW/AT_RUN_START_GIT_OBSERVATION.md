# AT_RUN_START_GIT_OBSERVATION — PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915

Purpose: formalize-time git/identity baseline of the run package, recorded by pe-master-auditor (the formalizer) when creating this package.
SECTION 1 below is the formalizer's measurement and is IMMUTABLE. SECTION 2 is reserved for the executor's own run-start observation per RUN_CONTRACT.md GIT FAIL-CLOSED: the executor APPENDS its timestamped measurement below the SECTION 2 marker and does NOT modify SECTION 1.

## SECTION 1 — FORMALIZE-TIME OBSERVATION (pe-master-auditor; immutable)

Measurement environment: Windows PowerShell 5.1, repo D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (branch master). All timestamps local (-07:00).

### git rev-parse HEAD — 2026-09-15T06:10:08.4973097-07:00
```
3068f31ad8db7e993a72365dc28cc03066095afd
```

### git rev-parse --abbrev-ref HEAD
```
master
```

### git rev-parse origin/master (local remote-tracking ref)
```
3068f31ad8db7e993a72365dc28cc03066095afd
```

### git ls-remote origin master — 2026-09-15T06:10:08.7160624-07:00 (network; EXIT 0)
```
3068f31ad8db7e993a72365dc28cc03066095afd	refs/heads/master
```

### git status --short
```
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
?? experiments/
```

### git worktree list
```
D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean                              3068f31 [master]
D:/Eudoria_Reconstruction/worktrees/PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1 5290e79 [audit/pe935-ninode-slot17-gb-oracle-minicheck-r1]
D:/Eudoria_Reconstruction/worktrees/WORK_AUDIT_REPORTS                          1312f89 [audit/work-audit-reports]
```

### Evaluation vs the pinned expectations (parent order + RUN_CONTRACT GIT FAIL-CLOSED)
- HEAD == BASE_SHA (3068f31ad8db7e993a72365dc28cc03066095afd) == origin/master == ls-remote: MATCH. No new commit on master between the parent's 2026-09-15T06:03 measurement and this formalize-time measurement.
- Pre-existing untracked inventory == exactly the two declared paths (docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ and experiments/): MATCH. Everything tracked clean.
- Worktrees: main 3068f31 [master]; PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1 5290e79; WORK_AUDIT_REPORTS 1312f89 — all three match the parent's declaration. The WORK_AUDIT_REPORTS worktree/branch audit/work-audit-reports is FORBIDDEN (WORK AUDITOR separation): not read, not merged, not modified by the formalizer.
- Output-root collision check: `docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/` did NOT exist before this formalization (Test-Path = False, 2026-09-15T06:10:35.3225309-07:00); the package was created fresh. (The dir appears in git status only AFTER this formalization created it — expected, it is the new run package.)

### Source identity re-measurement at formalize time (S0 pre-verification by the formalizer)
Measured 2026-09-15T06:10:09.1698119-07:00 (Get-FileHash) and 06:10:35.3225309-07:00 (own PE parse, python 3.12.7):
- Entropia.exe: Length 8015872 (PIN 8015872 — MATCH); SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (PIN — MATCH); LastWriteTime 2008-09-17 18:56:16.
- Own PE parse: e_lfanew 0x120; SIG 'PE\0\0'; Machine 0x14c (i386); NSections 5; SizeOptHdr 224; OptMagic 0x10b (PE32); ImageBase 0x400000; sections: .text vsize 0x6735e5 vaddr 0x1000 rawsize 0x674000 rawptr 0x1000; .rdata vsize 0xf6569 vaddr 0x675000 rawsize 0xf7000 rawptr 0x675000; .data vsize 0x3d6e4 vaddr 0x76c000 rawsize 0x34000 rawptr 0x76c000; .tls vsize 0xa vaddr 0x7aa000; .rsrc vsize 0x3c54 vaddr 0x7ab000 — ALL MATCH the S0 pin in RUN_CONTRACT.md.
- Environment measured at formalize time: python 3.12.7 (D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe); capstone 5.0.7 (capstone.cs_version() = (5, 0, 1280)). The executor MUST re-measure both at run time and print measured versions in every raw file header (the 1a490ee lesson).
- Formalizer scope note: this was the ordered pin verification (identity/PE layout only). The formalizer did NOT decode or re-verify any disassembly pin; the executor re-measures every pin in-run (G2).

### Formalized artifact identities (post-final-edit, measured by the formalizer 2026-09-15T06:17:27.9216558-07:00)
- 00_CONTROL/RUN_CONTRACT.md — SHA256 EEF4C8982FC49A1B3B2F051557ED7CCECDA4350690A3580809D4E67A410AAC3E — 28824 bytes.
- 00_CONTROL/SOURCE_IDENTITIES.json — SHA256 0A66902D738D5C6DB3FB8B6B6B99F8D08C41E63D11C55EA4D1DEEAA395DFE1E8 — 8945 bytes (JSON validated: 19 top-level keys, run_id/exe-sha/packages correct).
- This file (01_RAW/AT_RUN_START_GIT_OBSERVATION.md) cannot contain its own hash; its SECTION 1 hash after the executor's SECTION 2 append will be covered by the executor's MANIFEST_SHA256.csv (L12 self-exclusion rule respected).

### Formalizer NOT_CHECKED (disclosed)
- No disassembly/semantics decoding by the formalizer (formalize-only mode; PE-MASTER stated it independently verified the SF slot3 window bytes at BOOT).
- Boot packages A/B/C verified by existence + SHA256 identities + AUDIT_ENTRYPOINT.md headline consistency, NOT by full-content re-derivation.
- ACTIVE_WRITER.lock observed stale (heartbeat 2026-09-07, scope = an unrelated 99_Audits run dir, disjoint from this package); no takeover performed — single-writer ownership resolves by explicit PE-MASTER dispatch; loop control belongs to PE-MASTER.

## SECTION 2 — EXECUTOR RUN-START OBSERVATION (append below this line; do not modify SECTION 1)

### Executor: pe-reconstruction, measured 2026-09-15T06:20:14.8250484-07:00 (PowerShell 5.1, repo D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean)

#### git rev-parse HEAD
```
3068f31ad8db7e993a72365dc28cc03066095afd
```
EVALUATION: == BASE_SHA (expected 3068f31ad8db7e993a72365dc28cc03066095afd) — MATCH.

#### git rev-parse --abbrev-ref HEAD
```
master
```

#### git rev-parse origin/master
```
3068f31ad8db7e993a72365dc28cc03066095afd
```
EVALUATION: HEAD == origin/master — MATCH.

#### git ls-remote origin master
```
3068f31ad8db7e993a72365dc28cc03066095afd	refs/heads/master
```
EVALUATION: HEAD == origin/master == ls-remote — MATCH. master has NOT moved. No reset performed; no unknown/conflicting change.

#### git status --short
```
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
?? docs/audits/PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/
?? experiments/
```
EVALUATION: the two pre-existing untracked paths (docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ and experiments/) are present and UNTOUCHED; the third entry is THIS run package created by the formalizer (expected). Everything tracked is clean. MATCH.

#### git worktree list
```
D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean                              3068f31 [master]
D:/Eudoria_Reconstruction/worktrees/PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1 5290e79 [audit/pe935-ninode-slot17-gb-oracle-minicheck-r1]
D:/Eudoria_Reconstruction/worktrees/WORK_AUDIT_REPORTS                          1312f89 [audit/work-audit-reports]
```
EVALUATION: matches the declared three worktrees. WORK_AUDIT_REPORTS worktree/branch audit/work-audit-reports is FORBIDDEN — not read, not merged, not modified by the executor.

#### S0 fail-closed re-verification by the executor (measured 2026-09-15T06:20 local, BEFORE any decode)
- Entropia.exe SIZE = 8015872 (PIN 8015872 — MATCH); SHA256 = E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 (PIN — MATCH) via Get-FileHash.
- Executor own PE parse (python 3.12.7): e_lfanew 0x120; SIG 'PE\0\0'; Machine 0x14c (i386); NSections 5; SizeOptHdr 224; OptMagic 0x10b (PE32); ImageBase 0x400000; EntryPointRVA 0x55da11; sections .text vaddr 0x1000 vsize 0x6735e5 raw 0x1000 rawsize 0x674000; .rdata vaddr 0x675000 vsize 0xf6569 rawsize 0xf7000; .data vaddr 0x76c000 vsize 0x3d6e4 raw 0x76c000 rawsize 0x34000; .tls vaddr 0x7aa000; .rsrc vaddr 0x7ab000 — ALL MATCH the S0 pins. (Executor self-correction note: the executor's first quick parse script read ImageBase from the wrong offset e+28 — which returns SizeOfCode 0x674000 — and was immediately re-measured at the correct Optional-Header offset e+24+28 yielding the pinned 0x400000; recorded here for transparency, no AMEND needed because no run artifact had yet been written with the buggy value.)
- Environment measured at run time: python 3.12.7 (D:\Eudoria_Reconstruction\10_Scripts\python_env\python.exe); capstone 5.0.7, capstone.cs_version() = (5, 0, 1280) — matches the pinned environment. Both are printed in every raw file header generated this run.
- S0 VERDICT: PASS (fail-closed gate open). G1 VERDICT: PASS. ZERO git mutations will be performed by the executor.

