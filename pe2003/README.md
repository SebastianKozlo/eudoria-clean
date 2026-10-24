# pe2003 — Project Entropia 2003 reconstruction research (public projection)

This directory is the sanitized public projection of the **PE2003** research
program: a reverse-engineering campaign on the January-2003 "Commercial Open
Trial" release of Project Entropia (MindArk), focused on two concrete game
models — `296445.nif` and `218757.nif` — their asset identity, references,
loader machinery, spawn/transform pipeline and historical placement.

## Program goal

Rebuild on the 2003 release what was previously researched on the 9.3.5-era
client: model asset identity, the resource/loader chain, the network-driven
instance spawn, the transform rules, and whether authentic historical
locations of the two models can be recovered from the local 2003 corpus.

## Selected build and corpus (physical provenance)

| Artifact | Identity |
|---|---|
| Client | **Project Entropia 4.02.0000 Commercial Open Trial**, `PE.exe` 753 664 B, SHA256 `53A6F341BF75E6F16439DD290DC14BECCFD294AB1AE520E2398428074DC1C01`, PE32 i386, UPX-packed, timestamp 2003-01-30 12:33:07 UTC |
| Primary corpus | **PE42_EN_80553A75** — installer `pe42_en.exe` (CAB MSZip, 525 581 323 B, SHA256 `80553A75EED5117B194BD3382727F993970336607F62DE8A3807427DCA99F27B`), 711 extracted files, 841 093 330 B uncompressed, every file hashed |
| Client binary lineage | `PE.exe` == `PE_CD.exe` (IDENTICAL_BYTES); `upx -d` product == `PE2_unpacked_out.exe` 2 207 744 B SHA256 `56178993692A7409C8963398089E482EDDF96177666BACB91A8CC1A638D9A0650` (all static RE ran on this build) |
| Game archives | Models.ark 128 742 137 B `F660D055…`; Textures.ark 289 585 581 B `D611D125…`; Scripts.ark 5 662 913 B `1701D696…`; Volumes.ark 416 728 B `68EFF073…` — byte-identical across 3 physical copies |
| Terrain | `50.bnt` in TWO versions (PE42 `8E43CD14…` 116 528 920 B vs other copy `A6E59EE0…` 118 016 977 B — era split, catalogued, NOT decoded) |

## What was established (campaign R3, 2026-10-24)

- Full loader chain CONFIRMED at VA level: archive mount → resource manager
  (vtable 0x5E7974, 4 open slots nif/bvi/tga/dds; member name =
  `sprintf("%d")`+extension) → shared member reader FUN_00464F30 → NIF 4.1.0.12
  deserializer (0x522010→0x5B7170 "NetI" branch) → root wrapper 0x5EBC1C.
- Definition binding CONFIRMED data-side: Scripts.ark definitions 4508.obj
  (IDs 296445+296446) and 4057.obj (IDs 218757+218758) carry the model IDs as
  u32 constants in an identical attach-resource-pair bytecode macro.
- Spawn/transform mechanism CONFIRMED: network frame type 0x06 → wire parser
  FUN_00528a40 (BE envelope, LE f32 ×3) → avatar (0x118 B, vtable 0x5E4628) →
  scene attach with ×100.0 storage multiplier; orientation = 3×3 row-major
  row-vector (v·M), consumers FUN_004193f0/FUN_00419090.
- Placement verdict: **TRANSFORM_SOURCE = NETWORK_RUNTIME_ONLY**. The local
  2003 corpus contains NO instance data (install/Volumes/Scripts/Models
  negatives, all with denominators); AUTHENTIC_INSTANCE_COUNT = 0 offline;
  verdict = MECHANISM_CONFIRMED_LOCATIONS_NOT_RECOVERABLE_FROM_LOCAL_2003_CORPUS.
- The one open science edge: definition→open has NO static consumer on the
  unpacked client build (censuses 5776 indirect CALL sites / 576 444
  instructions; dynamic capture is the only remaining static-side-free path).

## What is NOT established

- Authentic historical world locations of either model (network/runtime only).
- World-axis/meters calibration (no anchor in the local corpus).
- Terrain decode (both 50.bnt versions catalogued only).
- The 218757 cross-variant structural diff (4.1.0.12 vs 10.1.0.0 payloads).
- Live orientation source (who supplies the real 9 floats) — UNVERIFIED.
- Server-side execution model of the 0x7700xxxx bytecode tokens.

## Structure

- `docs/` — sanitized research documentation (provenance, formats, pipeline,
  world data, roadmap).
- `tools/` — the campaign's own parsers/inspectors (path-parameterized public
  copies; no secrets, no embedded game data).
- `cases/` — per-model case summaries + the two-model comparison.
- `research/<RUN_ID>/` — the sanitized run report package of campaign R3
  (REPORT, derived claims, QC/process summary, frontier, publication manifest).

Standing: **ADVISORY_PENDING_EXTERNAL_POSTAUDIT**. CANONICAL_GATE_EFFECT=NONE.
Game binaries and game data payloads are NOT and will NOT be published here;
only hashes, structural metadata and own code.
