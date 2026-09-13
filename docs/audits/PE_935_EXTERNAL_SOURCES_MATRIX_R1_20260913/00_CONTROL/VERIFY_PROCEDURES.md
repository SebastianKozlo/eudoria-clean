# VERIFY_PROCEDURES — PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913

Run date: 2026-09-13. Executor: pe-reconstruction (direct PE-MASTER dispatch, human order §5).
Scope: EXACTLY the A–F claim list; no scope beyond it (the XeNTaX backup thread "Entropia Universe .PAK files_6041.md" was found during backup retrieval but deliberately NOT analyzed — out of list).

## 1. Repository state (contract verification)

- Repo: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`, remote `origin = https://github.com/SebastianKozlo/eudoria-clean.git`
- Pre-run: `HEAD = d1a036d86a1db59c7662dac988369892280129ec` == BASE_SHA (verified); after `git fetch origin`: `origin/master = d1a036d86a1db59c7662dac988369892280129ec` → HEAD == origin (verified).
- Dirty state pre-run: only `?? experiments/` (foreign session) — untouched throughout; not added, not committed.
- No repository initialization, no history rewrite, no foreign staged changes absorbed.

## 2. Web sources (articles/docs/forums)

Tool: platform `webfetch` (HTTP GET, markdown/text). Every claim's primary URL was fetched directly; search-engine snippets were NOT accepted as substitute (contract rule). Dead/blocked primary pages were retried via:

- **Wayback Machine** (web.archive.org): direct year-anchored captures (`/web/2024/…`, `/web/2/…`, `/web/2009/…`), availability API (`archive.org/wayback/available`), CDX API (`web.archive.org/cdx/search/cdx?url=…`) to enumerate captures.
- **archive.today** (`archive.ph/newest/…`) as a secondary archive.
- **Bing** web search only to locate alternative entry points (RoR thread, PEBNTView) — returned no usable results for either.
- **Playwright real-browser fetch** attempted for the RoR forum (bot-protected 403) — failed: no browser endpoint (`ECONNREFUSED ::1:9222`); recorded as a documented attempt.

Archive/attempt outcomes per claim are recorded in `01_RAW/` files and the D2b/F3 matrix rows.

## 3. GitHub repositories (code claims B1–B6, D1, D2a, D3)

Procedure: **read-only shallow clones** (`git clone --depth 1`) into the pre-approved temp workspace `C:\Users\User\AppData\Local\Temp\opencode\pe_935_ext_sources\repos\`. Code was READ ONLY — never compiled, never executed (contract HARD STOP on running historical programs applies to PEBNTView-class tools; the DAoC/DoL/WarEmu code was likewise only read).

| Repo | Clone SHA (branch HEAD) | Commit date |
|---|---|---|
| Merec/DAoC-MapCreator | 073a5940128be0e3f3bb57df0468d946b560c7f1 (master) | 2020-05-02 |
| jeremv42/DaocNavMesh | 206c3287770eb55ad56d3477a052375c49393281 (master) | 2025-08-04 |
| OpenDAoC/OpenDAoC-BuildNav | 291149188c0a67db00357f84518cf7b0309ffbb9 (master) | 2026-07-18 |
| mharj/daoctocrysis | 3e98846c51ba6ee8e065fb4b27c03c6f2adcec6e (master) | 2010-05-30 |
| Dawn-of-Light/DOLSharp | 776619f88d2d5ce52f09ab956194fd519a41f985 (master) | 2026-06-04 |
| WarEmu/WarEmu | 3e69ff657325e93cbe0a3955c56cdba6bdac5c5e (update = default) | 2014-08-26 |
| XeNTaXBackup/XeNTaXBackup.github.io | 2c6074a1bcb085e77f527fcf620620a4ee1e76da (main) | (backup repo) |

Repo discovery: GitHub REST search API (`api.github.com/search/repositories?q=…`) for DaocNavMesh / OpenDAoC-BuildNav / daoctocrysis / Dawn of Light / WarEmu / xentax; upstream verification via `api.github.com/repos/thekroko/uthgard-opensource`.

XeNTaX backup retrieval: `git clone --depth 1 --filter=blob:none --sparse` of XeNTaXBackup.github.io; thread located via `git ls-tree -r` name filter "Entropia" (3 thread files) and read from the working tree. PostIndex.md (2.9 MB) fetched raw and grepped for Entropia/BNT/sinkillerj/xennex (4 Entropia threads found; 3 read: 2446, 21558, 6041-located-only).

Line numbers: cited line numbers are from the `Read` tool over the cloned working tree at the recorded SHAs (1-based file lines).

## 4. Local generation & gates

- `00_CONTROL/z1_matrix_consistency.ps1` — G4 gate: RFC4180-tolerant CSV parser; converts `claims_matrix.csv` → `claims_matrix.json`; checks CSV rows == MD table rows == 24, ID sets equal, 7 fields/row, census coverage of the 23 contract claims (D2 split → D2a/D2b), status taxonomy validity; writes `03_EVIDENCE/Z1_MATRIX_CONSISTENCY.json`. Result: **G4 PASS** (24/24, tally CONFIRMED 21 / STRONGLY_SUPPORTED 1 / PLAUSIBLE 0 / UNVERIFIED 2 / REJECTED 0).
- Manifest hashes: `03_EVIDENCE/MANIFEST_SHA256.csv` (SHA256 over every produced artifact; generated last, after all other files finalized).

## 5. Boundary compliance

- NO historical binaries executed (PEBNTView never fetched, never run; DAoC/DoL/WarEmu/XeNTaX code only read).
- NO EU1030 interaction (E3): no local 10.x/EU1030 files read or touched.
- NO source files modified anywhere; NO game data touched; all work in `99_Audits` workspace + pre-approved temp dir.
- NO scope creep: only the A–F list was investigated (the off-list XeNTaX PAK thread was located but not analyzed; no follow-up on WarDB/PAK contents).
- Spawned processes: all webfetch/git/powershell invocations were synchronous, bounded, and terminated with the tool call; no background writers remain.
