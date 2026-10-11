# Knowledge gaps — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010

Honest open items (all era-labelled PCG 9.3.5, measured this run):

1. **7 parse failures (0.125%)** — 4 MODEL_DATA_REF_TYPE_MISMATCH (472836,
   543836, 546348, 68336), 2 NiSkinData-context closure fails (592605,
   591780), 1 NiSkinPartition context (204828), 1 EOF-region (419159).
   Recorded AMBIGUOUS/non-pass; API returns truthful 422.
2. **NiLight 4.0.0.2 trailing f32 semantics** — measured values 1.0/1.0/0.0
   after specular; UNRESOLVED (dimmer-like).
3. **Morph target semantics** — NiVertexMorphExtraData regions recorded RAW;
   target application UNRESOLVED (116 assets).
4. **Particle systems** — DETECTION_UNRESOLVED (130 assets with PSys blocks;
   no simulated particles emitted).
5. **Property-controller runtime application** — UV/vis/flip/material-color/
   alpha decoded + inventoried; not yet applied as live property animation.
6. **JPEG textures (19 entries)** + TGA types 1/3/10 (30 entries) —
   UNSUPPORTED_FORMAT (truthful 415).
7. **ArkTexture v4 unnamed i32 semantics** — consumed byte-exact, meaning
   UNRESOLVED (value 0 measured on the witness).
8. **Textured meshes with failed controls** — 28 UNRESOLVED + 2 DECODE_FAIL +
   73 PARTIAL(RENDER_RECONSTRUCTION) assets; never promoted to TEXTURED_EXACT.

INDEPENDENT_DESKTOP_POST_AUDIT = PENDING (this package is SELF_REVIEW +
machine gates; independent QC by PE-MASTER remains).
