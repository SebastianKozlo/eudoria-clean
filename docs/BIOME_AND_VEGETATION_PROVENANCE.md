# BIOME_AND_VEGETATION_PROVENANCE — what is source, what is stand-in (era PCG_9_3_5)

Public implementation doc · campaign PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031.
**This is the honesty-critical document of the campaign.** Read it before quoting any tree position.

## 1. VERIFIED source: .vcl species palettes

- `VegetationClimates.bnt` (pcg_install, SHA256 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4, 25,346 B, BNT2, 32 entries) contains **32 text profiles `.vcl` (0.vcl … 31.vcl)** — 12-column whitespace records (5,916 tokens = 493 groups of 12).
- col0 = model id (246 distinct across the 31 decodable files; the GetModel 0x66 fetch-id space, NOT Models.bnt indices), col1 density 0..330, col2/col3 scale min/max, col4/col5 elevation band 0..1000 — **cols 6..11 UNVERIFIED raw**.
- **31/32 files DECODE_OK; 25.vcl = UNSUPPORTED (6 COMMA_TOKENS)** — the strict decoder fails honestly; the tokens are NOT normalized (locale of the original parser is unknown).
- Per-bone record counts, raw values and per-file SHAs: SCI W2_BIOME_VEGETATION\VCL_CENSUS.json. Species/model palettes are **VERIFIED source data**.

## 2. ENGINEERING stand-in: biome assignment

- **The runtime's region→biome assignment is an ENGINEERING stand-in, NOT recovered game logic**: `region = tile >> 5 → profile` (a coarse deterministic mapping with an explicit LAB/stand-in badge).
- The historical assignment mechanism was NOT recovered:
  - climate grid **resource 432502** (65×65 climate byte grid) = **NOT_FOUND_LOCALLY** — searched scope: **178 containers** (iter029) + INVENTORY.csv 1,856 files (0 hits) + ClientFiles.txt + Data.ini + raw-byte scan + no cache/patch directories. Classification NOT_FOUND_LOCALLY—LOCAL_SOURCE_EXHAUSTED (a missing physical input, not proof of nonexistence).
  - client vegetation path (VA-evidenced decompiles, W2-2): the client contains **NO per-position .vcl selector**. Everything per-position arrives through ONE position-keyed provider fetch `provider->vtable[1](x16,y16)` (packed 16/16 world-position pair) at FUN_0098f3a0. The which-.vcl decision happens **UPSTREAM_ORIGIN_UNKNOWN** — server content or patcher-delivered 432502 (HYPOTHESIS, shared-selector). P-CLIMATE remains OPEN.
- **P-CELLSTREAM open**: the per-cell record producer candidate is the same position-keyed provider fetch; boundary = provider object `queryobj+0x4→+0x20→+0x54` (not traced further).

## 3. CONFIRMED binary facts (what we do know)

- Per-cell record format: 8-byte triples {u16 x, u16 y, u32 model_id} — FUN_00990810, address-cited.
- **node-local u16 / 65535 = [0,1] CONFIRMED** (FUN_0095b180: node+0x5C/0x60 = f32(A/65535), f32(B/65535)); node scale = |lerp(min,max)|/12800; rotation/variant = identity (RE-faithful, not found in spawn loop — later decode of FUN_0095ae20/0095b4f0 shows a 12-float basis lerp as the node-local→world mechanism, VA-evidenced).
- Position-keyed RNG seed = ((p4*16+p5)*16+p1+p2+p3)*0x5CC7 + 0x6D7; MSVC rand() LCG — same u16 pair → same scale, DETERMINISTIC.

## 4. What we render, honestly labeled

- Runtime vegetation uses `compat/world-vegetation.js` + `PEFoliageLabSeed.js` — a **deterministic LAB_SEED stand-in wrapper** (`NODE_SCALE_RENDER_BRIDGE` calibration), explicitly **NOT a historical layout**. `ORIGINAL_REGION_TO_CLIMATE_JOIN = NOT_ESTABLISHED` is a named constant in the code.
- **ZERO claims about "original placement"** are made anywhere in this project (grep-verified 0 hits in the audit tree). Species come from the real .vcl palettes; positions/assignment do not.

## Sources (file + SHA256)

- VCL_CENSUS.md/.json — SCI W2_BIOME_VEGETATION\ (full raw records, comma offsets).
- W2_3_432502_LOCAL_CHECK_REPORT.md (SCI W2_BIOME_VEGETATION\W2_3_432502_LOCAL_CHECK_R1_20261031\) — 178-container search scope.
- CLIMATE_SELECTOR_MECHANISM.md + 01_RAW/dec_*.c — SCI W2_BIOME_VEGETATION\W2_CLIMATE_SELECTOR_R1_20261031\ (VA-evidenced decompiles).
- FRAME_FACTS.md, VEGETATION_PROVENANCE_GRAPH.json — SCI W2_BIOME_VEGETATION\ (per-field status labels).
- QC_ROLLING_R1/QC_REPORT.md — SHA256 76F2DB60CB88EE2363840A3C18D188D4EACD1CAF655083F1291495D351574ED8.
