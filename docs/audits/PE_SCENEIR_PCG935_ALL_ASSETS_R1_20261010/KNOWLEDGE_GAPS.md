# Knowledge gaps — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

Honest open items (all era-labelled PCG 9.3.5, measured this run; updated in
CORRECTION_ROUND1 per QC_ROUND2):

1. **7 parse failures (0.125%, all v10)** — MODEL_DATA_REF_TYPE_MISMATCH x3
   (472836, 543836, 546348), closure x4: 2 NiSkinData-context (592605,
   591780), 1 NiSkinPartition context (204828), 1 EOF-region (419159).
   Recorded as FAIL with reasons (non-pass); API returns truthful 422.
   (68336 is NOT a failure — PASS, 37 blocks, 2 meshes, TEXTURED_EXACT.)
2. **NiLight 4.0.0.2 trailing f32 semantics** — measured values 1.0/1.0/0.0
   after specular; UNRESOLVED (dimmer-like).
3. **Morph target semantics** — NiVertexMorphExtraData regions recorded RAW;
   target application UNRESOLVED (116 assets).
4. **Particle systems** — DETECTION_UNRESOLVED, both denominators recorded:
   127 assets by the NiPSysData-only census (MODEL_STATUS_INDEX psys column,
   252 blocks) vs 130 assets by the 7-type decoder family (256 family
   blocks); no simulated particles emitted.
5. **Property-controller runtime application** — UV/vis/flip/material-color/
   alpha decoded + inventoried; not yet applied as live property animation.
6. **JPEG textures (19 entries)** + TGA types 1/3/10 (30 entries) —
   UNSUPPORTED_FORMAT (truthful 415).
7. **ArkTexture v4 unnamed i32 semantics** — consumed byte-exact, meaning
   UNRESOLVED (value 0 measured on the witness).
8. **Textured meshes with failed controls** — 28 UNRESOLVED + 2 DECODE_FAIL +
   73 PARTIAL(RENDER_RECONSTRUCTION) assets; never promoted to TEXTURED_EXACT.
9. **18 mesh-bearing assets without measurable geometry** — e.g. 591813 (1
   mesh, 38,912 tris) has non-finite FILE_SCENE_SPACE bounds; kept UNKNOWN
   (not mesh-less, not failed).

HISTORICAL_WORLD_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
INDEPENDENT_DESKTOP_POST_AUDIT = PENDING (this package is SELF_REVIEW +
machine gates; independent QC by PE-MASTER remains).
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
