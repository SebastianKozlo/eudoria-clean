# 00_FINAL_REPORT — PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913

- RUN_ID: `PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913` (RUN_CLASS: MATERIAL)
- Mission (human order §5): verify the external sources cited in the ChatGPT audits; every claim = a check-list item, NEVER a source of truth. Bounded to the A–F list; the internet part closes after the listed claims.
- MAIN ARTIFACT: `02_ANALYSIS/CLAIMS_MATRIX.md` (+ machine `claims_matrix.csv` / `claims_matrix.json` — G4 PASS: 24 == 24 rows, identical ID sets).
- Full verbatim quotes/code: `01_RAW/` (10 evidence files). Procedures: `00_CONTROL/VERIFY_PROCEDURES.md`. Provenance: `03_EVIDENCE/MANIFEST.md` + `Z1_MATRIX_CONSISTENCY.json`.

## 1. Matrix summary (24 rows / 23 contract claims; D2 split into D2a+D2b)

| Status | Count | Rows |
|---|---|---|
| CONFIRMED | 21 | A1, A2, B1, B3, B4, B5, B6, C1, C2, C3, D1, D2a, D3, E1, E2, E3, F1, F2, F4, F5, F6 |
| STRONGLY_SUPPORTED | 1 | B2 (substance confirmed; zone-offset composition order corrected) |
| PLAUSIBLE | 0 | — |
| UNVERIFIED | 2 | D2b (RoR post not quotable — 7 documented attempts), F3 (elitepvpers PEBNTView blocked — 8 documented attempts) |
| REJECTED | 0 | — |

Every CONFIRMED/STRONGLY_SUPPORTED row carries a verbatim quote or code with file+lines (+commit SHA for all repositories — see the matrix and `01_RAW/`). Both UNVERIFIED rows carry documented, reproducible attempts (HTTP status codes, archive-API results, CDX census).

## 2. Key resolutions (one sentence each, per handoff requirement)

- **A (MindArk world editor)**: CONFIRMED — the 2002 MindArk newsletter (via Worthplaying) presents Kajsa Högberg as World Creator placing heightfield/textures/vegetation "including the cities" in a world editor (claim's "Kaja" = source's "Kajsa"), and CGW 2003 confirms separate "static objects and environments" artists (LightWave for SOME major-city buildings; 3ds Max for creatures) — with the MANDATED limitation that a world editor proves the authoring PROCESS, not the client/server storage location of its output.
- **B (DAoC static world)**: CONFIRMED — four parser lineages read the DAoC client's nifs.csv + fixtures.csv exactly as claimed (all field indices verified in code), with three precision corrections: (B2) DaocNavMesh composes the fixture world matrix as T×R×S with the zone offset applied as an OUTERMOST traversal pre-multiplication (not a trailing factor) and scale-Y negated; (B6) tree/cluster data files are separate but clusters are still placed via fixture rows; (B5) OpenDAoC-BuildNav is a declared fork of the Uthgard buildnav (one lineage with it), so the four repos are three independent lineages + one fork lineage corroborating the DAoC format — a RESEARCH PATTERN only, never a format transfer to Entropia.
- **C (OpenMW/MWSE)**: CONFIRMED — OpenMW/MWSE/openmw-trav document, verbatim, the base-record-without-location vs instance-with-position/rotation/scale separation (0/1/N instances per base) — ONE engine family's schema, explicitly NOT a mandatory Gamebryo-era standard (contract C-LIMITATION recorded).
- **D (network create-object)**: CONFIRMED WITH THE TRAP RESOLVED — DoL's NPCCreate (0xDA) carries Heading→Z→X→Y→Model exactly as claimed and WarEmu's F_CREATE_STATIC(0x71)/F_CREATE_MONSTER(0x72) compositions are verbatim-confirmed, BUT (D3, from code) F_CREATE_STATIC creates DB-driven INTERACTIVE objects (loot/quest logic; the embedded example is a door) and DoL's create-family covers NPCs/players/doors/items/housing — in BOTH emulators the authored static city world is NOT network-placed (DAoC's cities live in the client's own fixtures.csv — group B); the RoR methodology post itself is NOT QUOTABLE (D2b, 7 attempts).
- **E (EU 10.4)**: CONFIRMED — the forum post exists, is authored by player "Wody" (NOT MindArk), and lists exactly templates.vfs=610,576 B, Sectors.xbc=129 B, ResourcePaths.xbc, the pak family and the vfs family; the mandated limitations stand: 129 B cannot hold a placement table, filename continuity ≠ format continuity, a user CRC manifest ≠ a specification; EU1030 untouched (E3).
- **F (BNT/NiArk history)**: CONFIRMED except F3 — PerlMonks 2005-12-02 (FC /B byte-diffing of Models.bnt/50.bnt/Textures.bnt, pure Perl I/O, zero BNT semantics), xennex 2007-01-24/25 (verbatim BNT2 index structure; int64-unknown; crash-after-replace experiment), sinkillerj 2020-01 (verbatim "decode the game enough to recreate the old world"; ends at NIF viewing + unresolved TDF/TEZ), PyFFI (verbatim "Unknown node." NiArk classes = STRUCTURAL oracle only) — while the elitepvpers PEBNTView thread is unreachable from this environment (F3, 8 attempts) and its create-BNT capability remains UNVERIFIED.

## 3. Research patterns for EU935 — what is supported, and with what limits

### 3.1 Pattern: fixture-separation (model catalogue + placement record)

**Supported as a RESEARCH PATTERN — the strongest of the three, but zero format transfer.**
Mutually corroborating evidence: three independent DAoC lineages (2010 daoctocrysis / 2014-17 MapCreator / 2024 DaocNavMesh, plus the Uthgard-BuildNav fork lineage) parse the same nifs.csv(ID→NIF) + fixtures.csv(id, nif, name, XYZ, angle, scale, collision, unique-id, on-ground, flip, axis-angle) grammar and compose a world transform per instance (T×R×S variants; scale/100; Y-negation); the NetImmerse-family OpenMW/MWSE docs independently document base-record-vs-instance separation; MindArk's own 2002 world-editor interview (A1) shows cities were AUTHORED in an editor. LIMITS: all of this describes DAoC/Morrowind data, NOT Entropia's; the correct EU935 use is as a SEARCH GRAMMAR for candidate records (repeatable record + ID enrichment + transform plausibility + spatial clustering), never as a template to impose, per the contract LIMITATION recorded on every B row.

### 3.2 Pattern: network create-object

**Supported ONLY for dynamic/interactive entities — the static-building reading is REFUTED BY THE PRECEDENT'S OWN CODE (D3).**
DoL and WarEmu both demonstrate that a NetImmerse-era MMO protocol CAN deliver {OID + world transform + model/display ID} at runtime — that grammar exists (D1, D2a). But the same evidence shows what it is FOR: NPCs, players, moving objects, interactive GameObjects (doors/loot/quest objects), and player HOUSING; in both ecosystems the authored static world is client-local (DAoC: fixtures.csv — group B). Therefore the network-create precedent motivates an EU935 runtime decoder track for DYNAMIC objects, and explicitly does NOT justify network-first for static city placement. The RoR "RE from packet logs" narrative remains UNVERIFIED (D2b).

### 3.3 Pattern: MindArk world editor (client-side authored statics)

**Supported as HISTORICAL CONTEXT with a hard ceiling.**
A1 CONFIRMED that MindArk authored heightfield/textures/vegetation/CITIES in a world editor in 2002, and A2 confirms dedicated statics artists. The MANDATED LIMITATION bounds both: this proves the authoring process, NOT whether the world editor's placement output shipped in the client, the server, or both. Combined with 3.1 and 3.2 it sustains the ERRATA_R2 research direction (H_CLIENT priority for statics as a SEARCH HYPOTHESIS, network as competing hypothesis) — as a direction, not as a conclusion; EU935 placement remains NOT_FOUND_IN_SEARCHED_SCOPE with no new corpus search performed in this run (this run verified sources only).

### 3.4 Era/history layer (F)

The 2005 PerlMonks byte-diffing, the 2007 xennex BNT2 structure, the 2010 cross-engine converter, the 2020 sinkillerj attempt, and the PyFFI structural oracle together show: community work on the PE/BNT/NIF corpus is 21 years old, reached asset extraction/viewing and partial BNT2 index knowledge, and never publicly reached placement/consumer semantics — consistent with, and NOT contradicting, the project's own (era-separated, independently verified) results. F3 (PEBNTView) stays UNVERIFIED.

## 4. METHODOLOGICAL NOTE (F6, mandated)

**No discovery-priority claims are made from absence of results.** The absence of public prior art (in this run's searches, in the XeNTaX backup, and in the audited attachments' own negative results) is NOT proof that none existed; private RE may have existed at any time. Nothing in this report asserts or implies first-discovery status for any project result; the "publicly undocumented" statements in the historical record (F2/F4-era threads ending at asset extraction) are recorded as OBSERVATIONS of the public record only. Likewise, this run's UNVERIFIED rows (D2b, F3) are statements about ACCESSIBILITY from this environment on 2026-09-13, not about the truth of the underlying claims.

## 5. Gates

- **G1 (census)**: PASS — 23/23 contract claims have matrix rows (24 rows; D2 split for honest sub-statusing; no claim omitted).
- **G2 (quotes for CONFIRMED/SS; documented attempts for UNVERIFIED)**: PASS — 22 CONFIRMED/SS rows each carry verbatim quote or code+file+lines(+commit); 2 UNVERIFIED rows carry 7/8 documented attempts each.
- **G3 (DAoC commits+files+lines; kinship resolved)**: PASS — B1:073a594/FixturesLoader.cs; B2:206c328/Zone.cpp; B3:2911491/Zone2Obj.cs; B4:3e98846/main_window.cpp; B6:073a594/FixturesLoader.cs (+DaocNavMesh TreeCluster.cpp); B5 resolved (BuildNav = declared Uthgard fork; 3 independent lineages).
- **G4 (machine matrix == report table)**: PASS — `Z1_MATRIX_CONSISTENCY.json`: CSV 24 == MD 24, IDs equal, 7 fields/row, taxonomy-valid statuses.
- **G5 (publication)**: recorded in HANDOFF.md — path-limited commit `docs/audits/PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913/` + AUDIT_ENTRYPOINT.md (+1 row, 0 deletions), push, HEAD==origin verification (see HANDOFF for the executed result).

## 6. NON_PASS classes checked

- GATE_FAIL: none.
- SOURCE_UNREACHABLE_BUT_UNDOCUMENTED: none — both unreachable sources have documented attempts (D2b, F3).
- SCOPE_CREEP: none — only the A–F list was investigated; the off-list XeNTaX PAK thread (6041) was located during retrieval but deliberately not analyzed; no WarDB/10.x corpus research.

## 7. What remains UNVERIFIED, and why

1. **D2b — RoR post** (viewtopic.php?p=15035): live 403 (bot protection), zero Wayback captures (CDX census), archive.ph 404, browser endpoint unavailable → the RoR team's "RE from packet logs, no original server code" narrative cannot be quoted. The WarEmu CODE claims (D2a) are independently confirmed from the repo and do not depend on it.
2. **F3 — Desy PEBNTView @ elitepvpers 2008**: live 403 (http+https), Wayback playback 403/empty (CDX shows no captures of thread 146172), archive.ph 404, search engines useless → the tool's unpack+create-BNT capability and C#-port provenance remain unverified. NOT RUN per contract (the tool itself was never fetched/executed).

Both are ACCESSIBILITY statements (see §4); a future run with browser access or an elitepvpers account could close them.
