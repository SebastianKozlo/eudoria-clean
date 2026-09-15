# GIT_OBSERVATIONS_AT_FORMALIZE.md — PE_935_SF_ARG2_PROVENANCE_R1_20260914

Recorded by pe-master-auditor (formalizer) on 2026-09-14, under PE-MASTER loop
`2ed038db-5d2e-4e7e-b679-2d29bf57501a` (EU935-M1, Phase 2). Read-only observation — the
formalizer performed ZERO git mutations (no add, no commit, no push, no stash, no
checkout, no reset, no branch). The only filesystem effect of formalization is the new
untracked package directory
`docs/audits/PE_935_SF_ARG2_PROVENANCE_R1_20260914/` (00_CONTROL with 3 files).

Repo: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean` · remote `origin` =
`https://github.com/SebastianKozlo/eudoria-clean.git` · expected HEAD (BASE_SHA) =
`f239eb85cd0f56ae10cee52d57833a49f225965c`.

---

## SNAPSHOT 1 — PRE-CREATION (before the package directory was created)

TIMESTAMP: `2026-09-14T16:38:54.198-07:00`

```
--- HEAD ---
f239eb85cd0f56ae10cee52d57833a49f225965c
--- BRANCH ---
master
--- origin/master (local cached ref) ---
f239eb85cd0f56ae10cee52d57833a49f225965c
--- remote -v ---
origin	https://github.com/SebastianKozlo/eudoria-clean.git (fetch)
origin	https://github.com/SebastianKozlo/eudoria-clean.git (push)
--- ls-remote origin refs/heads/master ---
f239eb85cd0f56ae10cee52d57833a49f225965c	refs/heads/master
--- status --short ---
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
?? experiments/
--- worktree list ---
D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean                              f239eb8 [master]
D:/Eudoria_Reconstruction/worktrees/PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1 5290e79 [audit/pe935-ninode-slot17-gb-oracle-minicheck-r1]
```

## SNAPSHOT 2 — POST-CREATION (after the package dir + RUN_CONTRACT.md + SOURCE_IDENTITIES.json were written)

TIMESTAMP: `2026-09-14T16:45:11.636-07:00`

```
--- HEAD ---
f239eb85cd0f56ae10cee52d57833a49f225965c
--- BRANCH ---
master
--- origin/master (local cached ref) ---
f239eb85cd0f56ae10cee52d57833a49f225965c
--- ls-remote origin refs/heads/master ---
f239eb85cd0f56ae10cee52d57833a49f225965c	refs/heads/master
--- status --short ---
?? docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/
?? docs/audits/PE_935_SF_ARG2_PROVENANCE_R1_20260914/
?? experiments/
--- status (summary) ---
On branch master
Your branch is up to date with 'origin/master'.
Untracked files: the three directories above; nothing added to commit.
--- worktree list ---
D:/Eudoria_Reconstruction/12_WebGame/eudoria-clean                              f239eb8 [master]
D:/Eudoria_Reconstruction/worktrees/PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1 5290e79 [audit/pe935-ninode-slot17-gb-oracle-minicheck-r1]
--- staged paths check ---
git diff --cached --name-only -> EMPTY (STAGED_COUNT: 0)
```

## EXPECTED vs OBSERVED

| Item | Expected | Observed | Verdict |
|---|---|---|---|
| HEAD | f239eb85cd0f56ae10cee52d57833a49f225965c | f239eb85cd0f56ae10cee52d57833a49f225965c (both snapshots) | MATCH |
| Branch | master | master | MATCH |
| origin/master (local ref) | == BASE_SHA | f239eb8... (equal) | MATCH |
| Live remote (ls-remote origin refs/heads/master) | == BASE_SHA | f239eb85cd0f56ae10cee52d57833a49f225965c | MATCH (local ref == live remote; no remote drift) |
| Untracked set (pre-creation) | exactly FIRSTCALL pkg + experiments/ | exactly those two | MATCH |
| Untracked set (post-creation) | FIRSTCALL pkg + experiments/ + this package dir | exactly those three | MATCH |
| Staged paths | none | none (STAGED_COUNT 0) | MATCH |
| Linked worktrees | main worktree @ master f239eb8 | + the SLOT17 GB_ORACLE verbatim-record worktree @ 5290e79 (branch audit/pe935-ninode-slot17-gb-oracle-minicheck-r1) — a pre-existing eternal record, untouched | OBSERVED (no conflict; read-only) |

**Discrepancies found at formalize time: NONE** in the git state. One discrepancy in the
dispatching prompt itself (recorded in SOURCE_IDENTITIES.json): the first supplied
SHA256 string for Entropia.exe was corrupted (75 hex chars, duplication artifact); the
formalizer's own Get-FileHash measurement (E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31,
size 8015872) matches the prompt's second, declared-correct 64-hex string exactly.
Trust-your-own-measurement applied.

## EXECUTOR INSTRUCTION (AT_RUN_START re-measurement)

The executor re-measures this observation at run start into
`01_RAW/AT_RUN_START_GIT_OBSERVATION.md` (timestamped; same commands: `git rev-parse HEAD`,
`git branch --show-current`, `git rev-parse origin/master`, `git ls-remote origin
refs/heads/master`, `git status --short`, `git worktree list`, staged-paths check).
Expected at run start: HEAD == BASE_SHA == origin/master == live ls-remote ==
`f239eb85cd0f56ae10cee52d57833a49f225965c`; untracked set == exactly the three
directories above; zero staged paths. Any other value = the armed HARD_STOPs
(BASE_DRIFT / FOREIGN_STAGED_PATH) — report only, no reset, no reconcile, no unstage.
The executor performs ZERO git mutations.

*This file is an IMMUTABLE INPUT for the executor (do not edit, do not append).*
