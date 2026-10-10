# AUTHORIZATION_AND_PREFLIGHT — PE_WORLD_LAUNCHER_R1_20261010

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
PHASE (this document) = SETUP + PREFLIGHT + ETAP A + FOCUSED QC A
WRITTEN_AT = 2026-10-10, before the Etap A code changes (pre-work snapshot; post-work
results in CAM_C1_C2_C3_DISPOSITION.md and the final handoff).

## 1. Human authorization (scope of this run)

- ONE run, invoked by the human's order pointing at the governing contract file
  `C:\Users\User\Documents\ChatGPT\PE\PE_WORLD_LAUNCHER_R1_20261010\OPENCODE_PE_WORLD_LAUNCHER_R1_20261010.md`
  (27507 B, SHA256 30ACECDF063D7CBCF6BFC9FD2169236783BEA60052B850CE613BC6330C4C5B63 —
  re-verified by own measurement: MATCH).
- Authorized: implementation + commit/push of branch
  `codex/pe-world-launcher-r1-20261010` ONLY. NO merge to master. NO Entropia.exe, no
  original server, no new RE beyond the contract's implementation-scoped format
  inspection. NEXT_EXPERIMENT_AUTHORIZED = NO. HARD_STOP = YES at the end of the run.
- THIS PHASE additionally: NO commit/push yet (persistence is a later phase of the run;
  the phase ends with the worktree holding the corrections + artifacts, uncommitted).
- Do-not-touch list (verified untouched): master (3fbe93e), the other worktrees
  (`pe-sceneir-218757-r1` @ 59641ca READ_ONLY, `pe-city-asset-map-r1` @ e9bb1f5 foreign
  active state), the standing servers (8140/PID 21288 and 8161/PID 9588 — left alive,
  never bound over), AUDIT_ENTRYPOINT.md, historical docs/audits packages.

## 2. Contract identity

- SOURCE_BRANCH = codex/pe-city-asset-map-r1-20261010; contract EXPECTED_BASE_SHA =
  f71eb30ade05d26c4f71f11087a56f4891113680; RESULT_BRANCH = codex/pe-world-launcher-r1-20261010;
  WORKTREE_ROOT = D:\Eudoria_Reconstruction\12_WebGame\pe-world-launcher-r1;
  OUTPUT_REPO_PATH = docs/audits/PE_WORLD_LAUNCHER_R1_20261010/;
  PRIVATE_OUTPUT_ROOT = D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_LAUNCHER_R1_20261010\;
  DEFAULT_BIND = 127.0.0.1; DEFAULT_PORT = 8162 (verified free).

## 3. BASE_DECISION — EXPLICIT DISCLOSURE (PE-MASTER; recorded verbatim, never hidden)

> **BASE_DECISION (PE-MASTER, EXPLICIT DISCLOSURE — do not hide it anywhere)**: the remote
> source branch is at e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c, NOT f71eb30a. PE-MASTER
> verified: f71eb30a IS an ancestor of e9bb1f5; the delta f71eb30a..e9bb1f5 is EXACTLY ONE
> commit — the CAMERA_UX_FIX (compat/catalog-app.js + compat/catalog-preview.js) that the
> SAME human explicitly authorized in the previous turn ("popraw obracanie kamery"). The
> contract's BLOCKED_BASE_CHANGED clause guards against unauthorized foreign drift; this
> delta is the user's own authorized continuation. Building from f71eb30a would resurrect
> the broken camera the user asked to fix. DECISION: create RESULT_BRANCH from e9bb1f5 (the
> current authorized head, containing EXPECTED_BASE in ancestry). You MUST record this
> decision + the observed remote SHAs prominently in AUTHORIZATION_AND_PREFLIGHT.md and
> cite it in every later report — it is NEVER a silent adaptation.

My own independent verification of every element of this decision (fresh measurements,
2026-10-10):

- `git ls-remote origin`:
  - HEAD / refs/heads/master = `3fbe93eec04759395223e6677b5040273d29222a` (expected 3fbe93e —
    MATCH; observed, never written).
  - refs/heads/codex/pe-city-asset-map-r1-20261010 = `e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c`.
- `git merge-base --is-ancestor f71eb30ade05d26c4f71f11087a56f4891113680 e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c`
  → exit 0 (ANCESTRY CONFIRMED).
- `git log --oneline f71eb30a..e9bb1f5` → EXACTLY ONE commit: `e9bb1f5` "PE_CITY_ASSET_MAP_R1_20261010
  CAMERA_UX_FIX: /catalog preview camera … (human request: 'popraw obracanie kamery …')";
  `git diff --stat f71eb30a..e9bb1f5` → `compat/catalog-app.js` (+53 lines area) and
  `compat/catalog-preview.js` (+130) ONLY — 2 files, +169/−14. The delta content matches
  the disclosed CAMERA_UX_FIX exactly.
- CONSEQUENCE ADOPTED: RESULT_BRANCH was created from `e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c`
  (worktree HEAD == e9bb1f5, branch codex/pe-world-launcher-r1-20261010, status clean,
  full prior stack present: compat/, src/pesource, src/pecompat, src/peworld,
  tools/pecompat, tests/pecompat, docs/audits). The contract's EXPECTED_BASE_SHA
  f71eb30a is preserved in the branch ancestry. This decision is cited in every report of
  this run (see CAM_C1_C2_C3_DISPOSITION.md §0 and the final handoff).

## 4. Input pins (own measurements — all MATCH)

All 7 contract inputs re-measured (size + SHA256) by this executor before use: 7/7 MATCH.
Full table: INPUT_IDENTITIES.json (this directory). The 4 CAM-C1 GLB comparison inputs:
4/4 MATCH. The 2 private cache JSONLs (READ_ONLY attach targets): measured and pinned in
INPUT_IDENTITIES.json. The Desktop post-audit REPORT.md and the evidence files read from
its directory (RUNTIME_CHECKS.json, CACHE_IDENTITY_CONTROLS.json, the two control
scripts): measured before use — hashes in INPUT_IDENTITIES.json.

## 5. Standing servers / ports census (measured 2026-10-10)

| Port | State | Owner | Disposition |
|---|---|---|---|
| 8140 | LISTENING (127.0.0.1) | node.exe PID 21288 | foreign standing reference server — ALIVE, untouched |
| 8161 | LISTENING (127.0.0.1) | node.exe PID 9588 | foreign standing catalog server — ALIVE, untouched |
| 8000 | LISTENING | node.exe PID 6040 | pre-existing game server — untouched, not used by this phase |
| 8162 | FREE (bind-probed) | — | DEFAULT_PORT of this run (later phases) |
| 9222 | NOT LISTENING | — | playwright automation daemon DOWN → browser INTERACTION will be NOT_PERFORMED unless it comes up |

Node v22.22.0 (measured). Three.js pinned 0.185.0 (retention pin; kept; no dependency
changes). No package installs.

## 6. Era discipline statement

- Authoritative world profile of this run: **PCG_9_3_5**. CD_2003 exists for
  catalog/comparison only. In the PESourceMount layer the CD era label may be CD_JAN_2003
  — the mapping CD_2003 ↔ CD_JAN_2003 must stay explicit; never identified with JUL_2003.
- Never mix PCG heights with other eras' models/textures. Every catalog row carries an
  explicit era; identity = era + container SHA + entry name + payload SHA. The same entry
  name in both eras = TWO DISTINCT assets (measured 2,177+ overlap names, era-separated).
- Historical 2003-era terrain rules in the pe-reconstruction skill (50.bnt, 220x236 BUNT
  grid) are reference knowledge for THAT pipeline — NOT defaults for this run's
  terrain.bnt (PCG_9_3_5) handling in later phases.

## 7. Required reads (contract §1.1)

- The relevant AGENTS.md: `D:\Eudoria_Reconstruction\AGENTS.md` (VM-only execution
  environment, evidence tiers, PE-MASTER delegation model, no-external-writes) — READ
  (hash in INPUT_IDENTITIES.json).
- pe-reconstruction skill (the executing agent's skill): READ — era discipline, TDF layout,
  canonical sources, failure modes (hash in INPUT_IDENTITIES.json).
- **pe-gamebryo-rosetta skill: HONEST FINDING — NOT FOUND.** The contract §1.1/§3/§9
  refers to an existing skill at `.opencode/skills/pe-gamebryo-rosetta/SKILL.md`; it does
  not exist at ANY of the three .opencode skills roots (C:\Users\User\.opencode\skills,
  D:\TESTAI\.opencode\skills, D:\Eudoria_Reconstruction\.opencode\skills) at preflight
  time (verified by enumeration). Etap B must CREATE it (contract §9 lists it as an
  allowed change target; §3 says "extend the existing skill" — the extension target must
  first be created from the existing PE evidence + the verified Gamebryo sources listed in
  contract §3). Nearest existing analog read for orientation: the skill index shows
  `pe-nif-gamebryo-reference-stack`. This is recorded as a preflight observation; nothing
  was silently skipped and no SDK knowledge is claimed in this phase.

## 8. Worktree + branch setup (Task 1) — executed and verified

- Command (the ONLY write to the canonical repo D:\Eudoria_Reconstruction\12_WebGame\
  eudoria-clean — a `git worktree add`):
  `git worktree add "D:\Eudoria_Reconstruction\12_WebGame\pe-world-launcher-r1" -b codex/pe-world-launcher-r1-20261010 e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c`
  → exit 0.
- Verified: worktree HEAD == e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c; branch =
  codex/pe-world-launcher-r1-20261010; `git status` clean; the whole prior stack present
  (compat/, src/pesource, src/pecompat, src/peworld, tools/pecompat, tools/gamebryo_oracle,
  tests/, docs/audits).
- Observed git identities (fresh): remote master 3fbe93eec04759395223e6677b5040273d29222a;
  remote source branch e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c; worktree list shows
  pe-sceneir-218757-r1 @ 59641ca (READ_ONLY), pe-city-asset-map-r1 @ e9bb1f5 (foreign
  active state; its observed local modifications are that worktree's business — not copied
  into the new worktree, which was created purely from the committed e9bb1f5).
- The canonical worktree's own untracked files (docs/audits/PE_935_* etc.) were NOT
  touched and are NOT copied anywhere.

## 9. Preflight verdict

PREFLIGHT = GREEN. All pins verified; ports census as declared; the BASE_DECISION is
recorded and independently confirmed; the corrections (Etap A) proceed under the
preregistered gates in PREREGISTRATION.md.
