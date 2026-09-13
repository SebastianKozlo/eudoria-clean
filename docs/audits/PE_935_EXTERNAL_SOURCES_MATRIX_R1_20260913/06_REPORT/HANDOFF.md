# HANDOFF — PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913

- **AUDIT_OUTPUT_ROOT**: `D:\Eudoria_Reconstruction\99_Audits\PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913\`
- **FINAL_REPORT_PATH**: `06_REPORT/00_FINAL_REPORT.md` (matrix: `02_ANALYSIS/CLAIMS_MATRIX.md` + `claims_matrix.csv`/`.json`)
- **RUN_STATUS**: COMPLETE — all A–F claims verified or honestly unverified; gates G1–G4 PASS; G5 executed below.
- **HARD_STOP_REASON**: none (no historical binaries run; no EU1030 interaction; no sub-agents; no originals modified; list exhausted → STOP per contract).

## Gate results

- G1 census: PASS (23/23 claims → 24 rows; D2 split D2a/D2b)
- G2 quotes/attempts: PASS (22 CONFIRMED/SS with verbatim quotes/code+lines+commits; 2 UNVERIFIED with 7/8 documented attempts)
- G3 DAoC SHAs/files/lines + kinship: PASS (B5 resolved — BuildNav = declared fork of thekroko/uthgard-opensource buildnav)
- G4 machine==table: PASS (`03_EVIDENCE/Z1_MATRIX_CONSISTENCY.json` — 24==24, IDs equal)
- G5 publication: EXECUTED — see below.

## Matrix row counts per STATUS

CONFIRMED 21 / STRONGLY_SUPPORTED 1 (B2) / PLAUSIBLE 0 / UNVERIFIED 2 (D2b, F3) / REJECTED 0 — TOTAL 24 rows.

## Key resolutions (A–F, one sentence each)

- **A**: Kajsa Högberg = World Creator (2002, world editor: heightfield/textures/vegetation/cities) + CGW 2003 separate statics artists — CONFIRMED, with the mandated authoring-process-not-storage-location limitation.
- **B**: All fixture-field claims CONFIRMED in code across 3 independent DAoC lineages (+1 fork lineage); corrections: DaocNavMesh zone offset is an outermost traversal factor (not trailing), scale-Y negated; tree clusters placed via fixture rows; BuildNav = Uthgard fork — DAoC grammar is a search pattern only, no format transfer.
- **C**: OpenMW/MWSE base-record vs instance separation CONFIRMED verbatim — one engine family's schema, not a universal Gamebryo standard.
- **D**: DoL NPCCreate (0xDA) Heading→Z→X→Y→Model and WarEmu F_CREATE_STATIC(0x71)/F_CREATE_MONSTER(0x72) compositions CONFIRMED; D3 TRAP RESOLVED FROM CODE: F_CREATE_STATIC = DB-driven interactive objects (door/loot/quest), static cities are client-side in both ecosystems → network-create precedent covers dynamic entities (+housing), NOT static buildings; RoR post itself not quotable (D2b).
- **E**: EU 10.4 post CONFIRMED (author = player "Wody", 2009-11-25, NOT MindArk; templates.vfs=610,576 B, Sectors.xbc=129 B, all paks/vfs present); limitations recorded (129B ≠ placement table; filename ≠ format continuity; user post ≠ spec); EU1030 untouched.
- **F**: PerlMonks 2005 / xennex 2007 BNT2 / sinkillerj 2020 / PyFFI NiArk structural oracle all CONFIRMED (via Wayback + XeNTaXBackup.github.io @ 2c6074a + live docs); PEBNTView (F3) UNVERIFIED (elitepvpers unreachable, 8 attempts).

## What remains UNVERIFIED and why

- **D2b (RoR post)**: 403 live, zero Wayback captures (CDX), archive.ph 404, no browser endpoint → content not quotable; WarEmu code claims do not depend on it.
- **F3 (PEBNTView)**: elitepvpers 403 + no archive captures → tool capability unverified; never run (contract).

## Research-pattern verdict for EU935 (from the report §3)

- fixture-separation: SUPPORTED as a search pattern (3 independent DAoC lineages + OpenMW/MWSE + MindArk world-editor context) — no format transfer.
- network-create: SUPPORTED for dynamic/interactive entities only; REFUTED as a static-city precedent by the precedent's own code (D3) and by DAoC's client-side fixtures.
- world-editor: SUPPORTED as authoring context with the hard ceiling (process ≠ storage location) — sustains ERRATA_R2's H_CLIENT-priority-as-research-direction, NOT a conclusion.
- F6: no discovery-priority claims from absence — recorded as an explicit methodological note.

## Publication (G5)

- Package copied to repo: `docs/audits/PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913/` (22 paths: 00_CONTROL ×3, 01_RAW ×10, 02_ANALYSIS ×3, 03_EVIDENCE ×3, 06_REPORT ×3 — see artifact_index.csv).
- Commit: path-limited (package + AUDIT_ENTRYPOINT.md only), AUDIT_ENTRYPOINT.md +1 LATEST RUNS row / 0 deletions; pushed to origin/master; post-push `HEAD == origin/master` verified.
- Commit SHA + push verification: recorded below in §"Commit record" (filled at execution).

## Commit record (execution result)

(See git log at commit time; HEAD SHA discoverable via `git log -1 -- AUDIT_ENTRYPOINT.md`.)
