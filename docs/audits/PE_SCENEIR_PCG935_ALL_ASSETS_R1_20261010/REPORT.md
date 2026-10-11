# PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 — REPORT

**Run**: PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 · 2026-10-11
**Contract**: OPENCODE_PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010.md (33060 B, SHA256 12183200…7F31E, identity verified)
**Base**: e9bb1f5120444f8bafd7d90c426f9e64d6b9bf2c (source branch codex/pe-city-asset-map-r1-20261010)
**Worktree**: pe-sceneir-pcg935-all-r1 (branch codex/pe-sceneir-pcg935-all-assets-r1-20261010)
**Inputs**: Models.bnt (395,412,868 B, c950a8c2…, SHA-verified at server startup) · Textures.bnt (973,942,771 B, 61acd13b…) · donor DdsDecoder.js (7535 B, 12323655…, byte-exact reuse)

## What was built

A complete PCG-9.3.5 full-asset SceneIR viewer with the entire Models.bnt corpus:

1. **Census** — all 5,596 entries enumerated from the physical BNT2 index, payload-hashed, header-version-identified: 4,838 × NIF 10.1.0.0, 757 × 4.1.0.12, 1 × 4.0.0.2 (matches the pinned denominators; no hardcoding — re-measured).
2. **Three version-aware corpus readers** on the src/pecompat architecture (fail-closed, closure + EOF-exact with recorded-tail fallback, memoized backtracking):
   - NIF 10.1.0.0: 4,832/4,838 PASS (99.88%) — 7 honest FAILs recorded with reasons.
   - NIF 4.1.0.12: **757/757 PASS** — the v4 lineage extended against real PCG payloads (layout corrections measured this run: the NiProperty double-flags trap, the ArkTexture unnamed i32, the light version-split).
   - NIF 4.0.0.2: **1/1 PASS** (52555.nif, 37 blocks, EOF-exact; 4-byte booleans, hasUv, no z-function, raw-ptr lights + trailing f32).
3. **Catalog with composed bounds** (parentWorld × local, FILE_SCENE_SPACE): default ranking maxAxis extent largest→smallest, UNKNOWN (1,843 genuinely mesh-less assets) LAST with stable id-ASC ties, plus bytes/tris/verts/diagonal/vertical alternate sorts with per-metric coverage.
4. **Texture chain — the actual era binding**: mesh → texturing property → ArkTexture entry (joined by texturingPropertyRef) → 9-byte tail → **dual controls (byte-shape + same-era reference)** → Textures.bnt id → decode (strict DDS DXT1/DXT5 donor decoder; TGA2 24/32-bpp). States separated: 3,678 TEXTURED_EXACT · 73 PARTIAL (RENDER_RECONSTRUCTION fallback only) · 28 UNRESOLVED · 2 DECODE_FAIL · 1,808 SOURCE_UNTEXTURED. Checkerboard = visible PARTIAL, never TEXTURED_EXACT. The 218757 universal tail interpretation stays RETRACTED.
5. **Original animations**: keyframe controllers → per-node quaternion/position/scale tracks with ORIGINAL keys (duration from real key times); text keys preserved; skins with bind pose/inverse-bind/weights; UV/vis/flip/material-color/alpha emitted with original keys (inventoried; property application partial); PSys DETECTION_UNRESOLVED; morphs recorded-RAW. Browser playback: clip selector, play/pause/stop, scrub, speed, once/repeat, **>2-duration repeat without drift** (wrapped cleanly to 1.44/3.33). No invented/simulated clips.
6. **Viewer app** (compat/pcg935-viewer.html/js/css): main canvas dominant, drawers closed by default, search/filter/sort/deep-links (#asset/<id>), old-SceneIR orbit feel with stable AABB fit (updateMatrixWorld first), latest-wins generation identity, whole/parts with per-part visibility, wireframe/textures/axes/grid/bounds toggles, reset/fit, truthful failure display.
7. **Server** (compat/server-pcg935-viewer.mjs, 127.0.0.1:8164): loopback-only, static allowlist, pinned Three.js 0.185.0 (version-verified at startup), bounded routes with truthful errors (verified by 17 negative probes), LRU-bounded caches (assets 6 / textures 128, held at 6 during the full sweep).

## Acceptance gates — ALL 11 PASS

See STAGE_ACCEPTANCE_GATES.csv + TEST_RESULTS.json for the full records:
corpus bijection · parser fixtures pos/neg · cache/status negatives · ranking spot checks · texture controls · animation controls (incl. browser loop/pause/scrub) · API negatives · real-browser LOAD/PIXEL/INTERACTION (raw CDP on 8164; asset-discriminating pixel census) · **per-entry runtime coverage sweep 5,589 OK + 7 SKIPPED_KNOWN_FAIL with bounded unload** · lifecycle A/B/A memory · regression batteries (218757 + 457485 witnesses PASS; protected reader files byte-identical).

## Honest residuals (never hidden)

- 7 parse failures (0.125%) — MODEL_DATA_REF_TYPE_MISMATCH ×4, NiSkinData/NiSkinPartition/EOF-region closure ×4 (see KNOWLEDGE_GAPS.md).
- ALL_TEXTURE_BINDINGS_RESOLVED = NO (28 UNRESOLVED + 2 DECODE_FAIL + 73 fallback-PARTIAL).
- ALL_ANIMATIONS_PLAYABLE = NO (PSys 130 assets DETECTION_UNRESOLVED; morph semantics unresolved; property controllers inventoried but not applied live).
- JPEG (19) and TGA types 1/3/10 (30) textures UNSUPPORTED_FORMAT (truthful 415).

## Claims discipline

ALL_CATALOGUED = YES (5,596/5,596) · ALL_ATTEMPTED = YES (5,596) · ALL_RENDERABLE = PARTIAL (5,589 runtime responses built; browser render verified on witnesses — no per-entry screenshot claims) · publication and 8140 handoff per contract order.

**This package is SELF_REVIEW + machine gates. INDEPENDENT_DESKTOP_POST_AUDIT = PENDING.**
