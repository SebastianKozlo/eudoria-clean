# ITER-023 (Gate D, loop iter 37) — Water Forensics Start: Container Census + height==0 Hypothesis Test

Era: PCG_9_3_5 (primary) vs JUL_2003 (comparison oracle), both SHA-verified.
Method: bounded data-level census; no binary RE, no runtime changes.

## Water container census (denominator: all 2,217 files under pcg_install\Data, 53 containers)

- **No dedicated water container exists.** Zero water-named files (0/2,217; 0/53 containers).
- Water content lives inside general containers:
  - **Terrain material tails** (terrain.bnt TDF records): exactly **5 water material ids**, both eras:
    `Water01=203650, Water02=9088, Water03=9102, Water04=26950, Water05=26951`
    (name-derived census — no assumption; no other Water* names exist).
  - **Textures.bnt** (BNT2, PCG 8,381 / JUL 8,095 entries): all 5 water texture ids exist
    as `<id>.dat` entries, payloads TGA2 256x256x24. Payload SHA256s are **byte-identical
    across four eras** (CD_JAN_2003 = JUL_2003 = EU_LATER = PCG_9_3_5).
  - **MusDef.bnt 548119.amu** = "DeepWater Theme" ArkScript music definition
    (Segment "DeepWater_01" -> 548118.sgt).
  - **Entropia.exe strings**: `WaterPlane01` @0x697ce0 (adjacent to `TerrainClimates`),
    `ARK_WATER_WIND` @0x697f0c (environment-parameter family with ARK_SUN_ALPHA,
    ARK_WIND, TIME, ARK_FOG_COLOR/RANGE), `Geowater:0` @0x685da7 (semantics UNKNOWN).
    PE.exe: 0 hits. All 27 Parameters .vfs: 0 hits.
- The "203650+ id space" is a general mixed texture space (7,000 PCG ids >= 203650;
  TGA2 profile census: mixed types/dims incl. type-83 compressed variants), not a water block.

## height==0 hypothesis (data level)

Full dual-era walk: 51,920 regular filename-xy tiles per era, 0 decode failures;
water materials form **coherent lake/ocean-shaped components** (largest 3,805 tiles =
coastal ring; Water01 components 667/307/302/279... = inland lakes).

- Tile min==0 on 46.9% of tiles (24,363 PCG / 24,386 JUL); zero-sample tiles == min-0 tiles.
- **Dominant zero component = 23,760 tiles spanning the ENTIRE 220x236 map** — raw u16==0
  is the ubiquitous tile-local-minimum value, not a lake marker.
- Crosstab (PCG, 51,920 tiles): zero&water 4,328 / zero-only 20,035 / water-only 1,362.
  Of zero tiles only 17.8% carry water; 1,362 water tiles contain no zero sample.
- Water tiles concentrate at tile-min 0 (median 0, p75 0, mean 616 vs global median 768,
  mean 2432) — an honest observed correlation, NOT semantic proof.

**Verdict:** `raw u16 height==0 = water marker` is **REFUTED** at the data level;
water materials concentrate at min-0 terrain (**CONFIRMED correlation**); the world-space
water level and the water-surface consumer mechanism remain UNVERIFIED
(RE leads: WaterPlane01, ARK_WATER_WIND).

## Era compare (JUL vs PCG)

- Water material record counts identical both eras except **Water03: 1,848 JUL -> 2,015 PCG
  (+167 tiles)** — the single era divergence found in the water system.
- Heights: 51,147/51,920 tiles byte-identical across eras; 773 differ (1.5%).
- Water textures: byte-identical 5/5.
- JUL counts re-derived independently == frozen iter008b census exactly (cross-check PASS).

## Evidence

03_EVIDENCE: iter023_water_container_census.json, iter023_terrain_minheight_water.json,
iter023_terrain_minheight_grids.json, iter023_water_secondary.json,
iter023_water_vs_minheight_dist.json (SHAs in M1 ledger ITER_023).
