# FORMAT_COVERAGE — formats touched by the campaign (sanitized)

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.

| Format | Coverage | Status |
|---|---|---|
| ARK (ZIP-clone, AK magic) — Models/Textures/Scripts/Volumes.ark | full member listings (2492/4833/1937/831), CRC verified per member, local chain == EOCD == central directory | ANSWERED (decoder ark_vfs_decoder_f1.py QUALIFIED_WITH_CAVEAT; negative tests 4/4) |
| NIF 4.1.0.12 (0x0401000C) — the two target models | full block census 155/155 + 62/62, strict field parse, hierarchy, transforms, materials, geometry, footer cross-check | ANSWERED for the two files (fitted NiArk effect/controller grammars labeled UNVERIFIED single-instance fits; no third-parser cross-check available) |
| NIF 10.1.0.0 (9.3.5 variant of 218757) | NOT touched this campaign (cross-variant structural diff deferred) | NOT EXECUTED |
| .bvi (Volumes.ark: 12×BE-f32 ×48 B records) | full structural dump 831 members / 7032 records; target paired members 296446.bvi (21 rec), 218758.bvi (18 rec) pinned; zero model ids inside | ANSWERED (local collision channel fully characterized; negative for instance data) |
| Scripts.ark members (Blowfish-CBC DLOB bytecode) | ingest chain code-pinned (FUN_005235E0); decoded-corpse canon 1936/1936 reused read-only; both target definitions parsed to EOF byte-exact; chunk-size = byte-length (W1 empirical) | ANSWERED (channel = behaviors/bytecode; CODE semantics undecoded; disjoint 1937-vs-1+10+1936 classification unresolved, CS14) |
| .obj DLOB definitions (4508/4057) | resource-ID constants byte-verified (E18); type-id→definition lookup CONFIRMED | ANSWERED data-side |
| 0x7700xxxx bytecode opcodes | client-side interpreter census NEGATIVE with denominators (5776 indirect CALLs / 576 444 instructions); 0x7fffec7x runtime opcodes ARE consumed (partial revision) | NEGATIVE (static); server-side model UNVERIFIED |
| Terrain BNT (50.bnt, two versions) | catalogued + hashed only | CATALOGUED ONLY (decode requires explicit authorization) |
| NSIS (PE_PCG.exe) | header + 40 data blocks parsed clean; extraction BLOCKED at block #40 | BLOCKED (frontier item d) |
| CAB MSZip (pe42_en.exe) | full extraction 711 files, all hashed | PASS |
| ISO 9660 (PC Gamer Nov 2003) | listing succeeded with container DEGRADED status; selected member ZIP PASS | DEGRADED container / PASS payload (separated) |
| TGA/DDS texture members | open paths code-pinned (slot2 0x520C20 → TGA parse; slot3 0x5209D0 → NiSourceTextureData); payload scan SKIPPED_SCOPE | PARTIAL (code chain only; member-level extraction not performed) |

Publication note: format knowledge is published as structure/offset facts
(docs/formats.md, tools/); no payload samples, member listings or dumps are
published.
