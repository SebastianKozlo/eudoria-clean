# ARCHITECTURE — source → Rosetta → IR → Three

## Pipeline (ASCII)

```
 +-----------------------------+        +------------------------------+
 | ERA SOURCE FILES            |        | REFERENCE / ORACLE SOURCES    |
 |  ISO_5_1_0_0 50.bnt (BUNT)  |        |  CD_JAN_2003 Textures.ark     |
 |  Models.bnt (BNT2)          |        |  gb12 Gamebryo 1.2 source     |
 |  .ark scripts (1883, 635..) |        |  oracle_helper.exe (engine)   |
 |  SHA256-pinned, verified    |        |  PE2_unpacked_out.exe (static)|
 |  at mount boundary          |        +---------------+--------------+
 +--------------+--------------+                        |
                |                                        | (cross-check only,
                v                                         |  never substituted)
 +------------------------------- Rosetta layer (src/pesource) ------+
 | PEProvenance.js   ERAS + KNOWN_HASHES + EVIDENCE_STATUS           |
 | PESourceMount.js  era registry -> requires archive format,       |
 |                   hash-verify on mount, refuses on mismatch      |
 | BuntArchive.js    ISO_5_1_0_0 framing (51,921 entries)            |
 | Bnt2Archive / Bnt2TerrainArchive  PCG framing (different corpus) |
 | ArkArchive.js     ArkVFS (.ark) members                          |
 | TdfDecoder.js     32x32 u16 LE height tiles @ offset 64          |
 | TdfMaterialTailDecoder.js  material masks @ record+56            |
 | NifModelReader.js NIF 10.1.0.0 witness reader (4.1 LOUD-FAILs)   |
 +---------------+---------------------------------------------------+
                 |  IR (intermediate representation: JSON-ish objects:
                 |      block census, hierarchy, local/world TRS,
                 |      materials, slot refs, geometry samples)
                 v
 +------------------------------- World layer (src/peworld) -------+
 | IsoPatchSelection.js  shared (node+browser) tile selector        |
 | IsoEnvironment.js     sky/fog/light layers w/ per-layer mode    |
 | IsoMaterialsFixture.js generated cross-check fixture             |
 +---------------+---------------------------------------------------+
                 |
                 v
 +------------------------------- Browser (terrain/) ---------------+
 | world_iso.html/js    Three r187 terrain + splat + env HUD        |
 | inspector.html/js    NIF inspector: graph/TRS/materials/3D       |
 | server.mjs           loopback static server + exact data routes  |
 +------------------------------------------------------------------+
```

## Role of each runtime piece

| Piece | Role |
|---|---|
| **Node (`server.mjs`)** | Loopback-only static server (default 8140, fallback 8141) + exact-path allowlist routes for data files; writes a lease file (PID/port/stop command). No game logic. |
| **Browser (`world_iso`, `inspector`)** | The actual runtime: decodes happen client-side via the same Rosetta modules (browser io injection: fetch / inflate / sha), so Node is never a decode oracle. |
| **Engine oracle (`oracle_helper.exe`)** | Headless stock-Gamebryo-1.2 comparator, used *offline* as evidence: engine vs our JS IR field-by-field (31/32 and 22/22 matches). Never part of the live page; its outputs are shown in the inspector as REFERENCE records, clearly not JS parses. |
| **Rosetta registry (`src/pe2003/rosetta/…`)** | Frozen evidence namespace: transform adapter + tests + knowledge records (`CLAIM_CORRECTIONS.json`, `ROSETTA_INTEGRATION_MAP.json`, `KNOWLEDGE_RECORDS_CAMPAIGN_R1.json`). The J4 hash gate pins the three adapter modules. |

## Era registration flow (how a new era enters)

1. **Era + hash pins** — add `ERAS.<NAME>` and `KNOWN_HASHES['<NAME>:<container>']` in
   `src/pesource/PEProvenance.js`. Era = physical source + label; byte-coincidence with
   another era's file is recorded as such, never as an alias.
2. **Format requirement** — `PESourceMount._terrainArchive` maps the era to its required
   archive format (e.g. ISO_5_1_0_0 → BUNT framing → `BuntArchive`); mount verifies SHA256
   and refuses on mismatch.
3. **Decoder** — era-scoped decoders (`TdfDecoder`, `TdfMaterialTailDecoder`,
   `NifModelReader`) consume containers; unknown/unera'd data loud-fails.
4. **IR** — decoders emit intermediate representation (census, hierarchy, TRS, materials,
   geometry samples).
5. **Fixture + test** — generated fixtures (e.g. `IsoMaterialsFixture.js`) plus unit
   gates + browser proof gates (CDP) with negative controls.
6. **Consumer** — runtime pages consume the IR (never a second parser).
7. **Record** — findings fold back into the Rosetta registry as additive knowledge
   records (`KNOWLEDGE_RECORDS_CAMPAIGN_R1.json`).

See `DEVELOPMENT.md` for the step-by-step version with commands.
