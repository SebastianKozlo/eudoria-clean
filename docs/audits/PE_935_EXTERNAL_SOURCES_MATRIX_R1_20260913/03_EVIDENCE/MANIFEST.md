# MANIFEST — PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913 (03_EVIDENCE)

## Evidence provenance summary

| Claim rows | Evidence file | Primary source |
|---|---|---|
| A1 | `01_RAW/A1_WORTHPLAYING_2002-04-08.md` | worthplaying.com (LIVE 2026-09-13) |
| A2 | `01_RAW/A2_CGW_2003-06_ECONOMY_OF_SCALE_WAYBACK.md` | web.archive.org capture 2025-10-05 of cgw.com (live 403) |
| B1, B6 | `01_RAW/B1_B6_DAOC_MAPCREATOR_CODE.md` | Merec/DAoC-MapCreator @ 073a5940128be0e3f3bb57df0468d946b560c7f1 (code read-only) |
| B2 | `01_RAW/B2_DAOCNAVMESH_CODE.md` | jeremv42/DaocNavMesh @ 206c3287770eb55ad56d3477a052375c49393281 |
| B3, B4, B5 | `01_RAW/B3_B4_B5_BUILDNAV_DAOCTOCRYSIS_KINSHIP.md` | OpenDAoC/OpenDAoC-BuildNav @ 291149188c0a67db00357f84518cf7b0309ffbb9; mharj/daoctocrysis @ 3e98846c51ba6ee8e065fb4b27c03c6f2adcec6e; thekroko/uthgard-opensource (GitHub API) |
| C1 | `01_RAW/C1_OPENMW_TABLES_WORLD.md` | openmw.readthedocs.io (LIVE) |
| C2 | `01_RAW/C2_MWSE_OBJECT_LIFETIMES.md` | mwse.github.io (LIVE; full page persisted to tool-output tool_09b415fdc001IQaaLVMeSLJ9Iy) |
| C3 | `01_RAW/C3_OPENMW_TRAV_LUA_OVERVIEW.md` | openmw-trav.readthedocs.io (LIVE) |
| D1, D2a, D2b, D3 | `01_RAW/D1_D2_D3_DOL_WAREMU_CODE.md` | Dawn-of-Light/DOLSharp @ 776619f88d2d5ce52f09ab956194fd519a41f985; WarEmu/WarEmu @ 3e69ff657325e93cbe0a3955c56cdba6bdac5c5e (branch update); RoR post — unreachable (7 attempts documented) |
| E1, E2, E3 | `01_RAW/E1_EU10_4_FORUM_POST.md` | forum.entropiauniverse.com/t/144631 (LIVE) |
| F1 | `01_RAW/F1_PERLMONKS_513557_WAYBACK.md` | web.archive.org capture 2017-03-07 of perlmonks.org node 513557 (live = JS challenge) |
| F2, F4 | `01_RAW/F2_F4_XENTAX_BACKUP_THREADS.md` | XeNTaXBackup/XeNTaXBackup.github.io @ 2c6074a1bcb085e77f527fcf620620a4ee1e76da, markdown/ threads 2446 + 21558 |
| F3 | (no readable evidence; 8 attempts documented in matrix row F3 + D-list) | elitepvpers.com thread 146172 — unreachable |
| F5 | `01_RAW/F5_NIFTOOLS_PYFFI_NIARK.md` | niftools.org/pyffi (LIVE; full page persisted to tool-output tool_09b50ad6b001KPNfVhjEgryn77) |

## Gate artifacts

- `03_EVIDENCE/Z1_MATRIX_CONSISTENCY.json` — G4 verification output: CSV 24 rows == MD 24 rows, IDs equal, census complete, tally CONFIRMED 21 / STRONGLY_SUPPORTED 1 / PLAUSIBLE 0 / UNVERIFIED 2 / REJECTED 0 → **G4 PASS**.
- `03_EVIDENCE/MANIFEST_SHA256.csv` — SHA256 of every artifact in this package (generated after all files finalized; the manifest itself and HANDOFF hashes are recorded in the commit but the CSV covers all package files except itself, per standard practice — see its self-note).

## Local-only/temporary artifacts (not part of the package, listed for provenance)

- Cloned repos + XeNTaX backup: `C:\Users\User\AppData\Local\Temp\opencode\pe_935_ext_sources\` (read-only clones; no execution; retained for PE-MASTER spot-checks until cleanup order).
- Tool-output persistence files referenced above live under `C:\Users\User\.local\share\opencode\tool-output\` (session-local).
