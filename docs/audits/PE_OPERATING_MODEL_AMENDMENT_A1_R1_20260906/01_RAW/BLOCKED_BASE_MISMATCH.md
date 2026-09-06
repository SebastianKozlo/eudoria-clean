# BLOCKED_BASE_MISMATCH — pre-start base verification FAILED (HARD_STOP, fail-closed)

- **RUN_ID**: PE_OPERATING_MODEL_AMENDMENT_A1_R1_20260906
- **RUN_CLASS**: MATERIAL (governance-only; declared by PE-MASTER in the run contract)
- **PARENT**: PE-MASTER (standalone order relayed verbatim by the human, 2026-09-06)
- **CURRENT_MILESTONE**: EU935-M1 (governance-only run; M1 technical state NOT touched — and it was not touched)
- **BLOCK TIMESTAMP (physical clock)**: 2026-09-06 00:35:27 -07:00 (verification) / 00:36:49 -07:00 (raw transcript capture)
- **BLOCKING CLAUSE (verbatim from the run contract, HARD_STOP)**:
  > "Jeśli BASE_SHA przy starcie != 34a2eeba56c97648b1e4fae858221cd03e3890dd lub drzewo brudne w ścieżkach spoza scope → zapisz BLOCKED_BASE_MISMATCH w 01_RAW i zakończ bez commitowania."

---

## 1. Contract-declared base vs physical state at start

| Field | Contract (declared) | Physical (observed at start) | Match |
|---|---|---|---|
| BASE_SHA / HEAD | `34a2eeba56c97648b1e4fae858221cd03e3890dd` | HEAD = `8c95438245b3f75b8d90bd3f86a573dd8fab4c54` | **NO — 4 commits ahead** |
| HEAD == origin/master | (claimed in contract) | TRUE — origin/master = `8c95438245b3f75b8d90bd3f86a573dd8fab4c54` | holds (at the newer SHA) |
| remote master (ls-verify) | — | TRUE — `git ls-remote origin master` = `8c95438245b3f75b8d90bd3f86a573dd8fab4c54` (post-fetch) | holds |
| worktree CLEAN | (claimed in contract) | TRUE — `git status --porcelain` empty for tracked paths; `git diff --cached` empty | holds |

The worktree-cleanliness and sync conditions hold — but at a **newer commit than the declared BASE_SHA**. The declared base `34a2eeba...` exists in history (ancestor of HEAD; commit date `2026-09-05 22:41:15 -0700`), it is simply **not the current HEAD**. The blocking disjunct "BASE_SHA przy starcie != 34a2eeba..." is MET.

## 2. The four intervening commits (landed AFTER the declared base)

| # | SHA | Commit date (-0700) | Subject (short) |
|---|---|---|---|
| 1 | `1d91374efef0e9a9550596b4e6bec251dea501c9` | 2026-09-06 00:20:12 | audits: FINDING N-5 — display predicate static RE (Ghidra boot chain) |
| 2 | `063713b061c11a46aac83f2cf60cea3f0decda85` | 2026-09-06 00:22:12 | audits: FINDING N-6 — TEZ<->FIELD frame relation + TEZ layout canon correction |
| 3 | `550ea226d420283674ec9f5e8d42232bc191d56f` | 2026-09-06 00:23:18 | audits: FINDING N-7 — R-channel of the global height texture decoded |
| 4 | `8c95438245b3f75b8d90bd3f86a573dd8fab4c54` | 2026-09-06 00:24:12 | audits: FINDING N-8 — expanded cellstream negatives (full-corpus scan) |

All four are audit-tree commits by the parallel session(s). **All 42 changed paths** of
`git diff --name-status 34a2eeba..HEAD` fall under `docs/audits/PE_NIGHT_AGGREGATE_20260905_160000/**`
— i.e. **another run's audit tree, a FORBIDDEN path class for this run** ("wszystkie docs/audits/<inne runy>/").
Full per-commit path lists: `01_RAW/GIT_STATE_AT_BLOCK.txt`.

## 3. Why proceeding was impossible under the contract as written

Gate G6 (SUCCESS_CRITERIA) requires: `git diff --name-only BASE..HEAD == lista dozwolona`
(allowed list = exactly: PROJECT_OPERATING_MODEL.md; PE_MASTER_HUMAN_AUDIT_CONTRACT_v1.md;
docs/audits/PE_OPERATING_MODEL_AMENDMENT_A1_R1_20260906/**; AUDIT_ENTRYPOINT.md).

With BASE = `34a2eeba...` and any HEAD descending from the current physical HEAD, that diff
**necessarily includes the 42 PE_NIGHT_AGGREGATE paths** — none of which are on the allowed list.
G6 would FAIL by construction before any work of mine is even added. The only ways to "pass" would be:
(a) silently re-basing the contract's BASE_SHA to the physical HEAD inside this run — an unauthorized
improvisation of a governance-contract field, or (b) rewriting/absorbing the intervening commits —
explicitly forbidden. Per the fail-closed discipline: **BLOCKED_BASE_MISMATCH**. No improvisation.

## 4. What was NOT done (blocked before any work)

- **PROJECT_OPERATING_MODEL.md**: NOT touched. SHA256 at block: `C5BAAD439764CF593F419BA8E62198B2A08465B627B77D6DD126A4DE42FC8F94`. No AMENDMENT A-1 written, no `.pre` copy made (no edit ever happened; instead a `state_at_block` copy is preserved in this 01_RAW).
- **PE_MASTER_HUMAN_AUDIT_CONTRACT_v1.md**: NOT created (verified absent before and after the block).
- **AUDIT_ENTRYPOINT.md**: NOT touched. SHA256 at block: `58ECFB09BB4120CB8986BC990489100F63A32F5ADD06C9831544EE87D6C7DBC4`. No governance row appended.
- **Gates G1–G6**: NOT RUN — the pre-start base verification failed before any stage.
- **Commit**: NOT performed. **Push**: NOT attempted (per the HARD_STOP clause "zakończ bez commitowania").
- **M1 technical state, gate matrices, other run dirs, wiki, skills, .opencode/, loop-state files, corpora**: all untouched.

## 5. Required action by PE-MASTER (re-issue parameters)

The governance assignment itself remains valid and executable — only the pinned base is stale. Re-issue the SAME assignment with a refreshed base, e.g.:

- **BASE_SHA**: `8c95438245b3f75b8d90bd3f86a573dd8fab4c54` (HEAD == origin/master == remote master at block time, `git ls-remote`-verified; worktree CLEAN) — or whatever HEAD is current at re-issue time, with the same pre-start verification requirement;
- everything else unchanged: the exact scope/allowed paths, FORBIDDEN_PATHS, the AMENDMENT A-1 content (A1.1–A1.9), CONTRACT_TEXT_VERBATIM, gates G1–G6, and the provenance requirements;
- a fresh RUN_ID per project discipline (e.g. ...R2 / timestamp suffix), or explicit parent confirmation that this blocked run dir is superseded.

This blocker record is intentionally **uncommitted on disk** (HARD_STOP). PE-MASTER reads it directly from the repo tree; no human relay required.

## 6. Evidence inventory (this directory)

- `01_RAW/BLOCKED_BASE_MISMATCH.md` — this record (primary).
- `01_RAW/GIT_STATE_AT_BLOCK.txt` — raw command transcript (HEAD/origin/ls-remote/status/cached/worktree/log/merge-base/diff/name-only count/clock). Note: the git-log *subject* lines contain a console-codepage artifact (em-dash mojibake) from the PowerShell 5.1 capture; the SHA/date/path fields are exact ASCII and authoritative.
- `01_RAW/TARGET_PATH_PRESENCE_AND_HASHES.txt` — target path presence + untouched SHA256 + state-copy hashes.
- `01_RAW/PROJECT_OPERATING_MODEL.md.state_at_block` — byte-exact copy of PROJECT_OPERATING_MODEL.md at block time.
- `01_RAW/AUDIT_ENTRYPOINT.md.state_at_block` — byte-exact copy of AUDIT_ENTRYPOINT.md at block time.
