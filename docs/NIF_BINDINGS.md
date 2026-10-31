# NIF_BINDINGS — what the NIF side of the pipeline actually does

Scope note: everything below is **NIF 10.1.0.0 witness-scope** plus (since W09)
the **dedicated NIF 4.1.0.12 adapter**, cross-checked against a headless stock
**Gamebryo 1.2 engine oracle** (built from 32-bit SDK libs, SHA-pinned).
Nothing here claims a full Gamebryo reimplementation.

## What works (with evidence IDs)

| Capability | Evidence |
|---|---|
| **Block graph traversal** (type/name/children/depth, ref lines; NULL child refs `-1` in `NiNode.children` are legal v10 data and are skipped) | W07 unit test 46/46; all 10 climate-0 witness ids parse FULL-OK |
| **Local TRS per node** | W07 IR cross-check vs engine oracle: 457485 → 31/32 fields match (census, all per-type counts, TRS, bounds, sample vertices/triangles, material colors, alpha) |
| **World TRS** (parent-composed via NiTransform `operator*`: `(P∘C).s = Ps·Cs`, `.R = P·C`, `.t = Pt + P·R(Ps·Ct)`) — parity with the frozen `niTransformAdapter.mjs compose()`, 8/8 adapter gates incl. the wrong-transpose mutant negative control | W01/W07 adapter + registry suites |
| **Materials** (NiMaterialProperty ambient/diffuse/specular/glossiness/alpha; NiTexturingProperty slots; era Ark texture binding displayed as textureId) | W07 materials panel + W08 compare (material fields all exact) |
| **Engine-oracle census equality** (block counts, per-type counts, shape multisets, bounds) | 457485: 31/32; 218757 (4.1, via frozen R61 reader): **22/22** |
| **Camera semantics** (look=col 0, up=col 1, right=col 2; row-vector view with −(basis·translate); NDC [−1,1] both axes; matches Three `Matrix4.lookAt` convention) | W08 source-backed paraphrase of pinned `NiCamera.cpp` (SHA `752CDFA8…`); adapter `camera_eye_to_origin` + live `three_engine_math_crosscheck` gates |
| **Geometry samples** (vertex/triangle counts, bounds, sample vertices/triangles) | W08 COMPARE_457485 / COMPARE_218757 — exact |

### The one documented non-match (a registry rule, not a bug)

- `texture.baseTextureIndex`: our IR records `baseSlot.source = -1` (NULL source ref);
  the engine's `GetBaseTextureIndex()` returns **0** (the texture *stage index* of the
  BASE slot). **Different fields.** For an engine BASE slot, index 0 with `source=-1` is
  normal and must not be read as a texture ref. Folded into the Rosetta registry as
  `KNOWLEDGE_RECORDS_CAMPAIGN_R1.json` record KR-W08-a.

## Unsupported / opaque in this runtime

| Block / feature | State |
|---|---|
| **NiArk\* blocks** (ArkAnimationExtraData etc.) | Stock `NiStream` cannot create them — engine load of the original FAILS verbatim (`cannot find create function`, recorded negative control L0). Oracle comparisons use Ark-stripped adapted copies with per-file lossmap sidecars; every strip loss is documented. |
| **Controllers** | v10: IR records refs only, honestly marked OPAQUE — no controller block decoding in the witness scope. **4.1 (W09): NiUVController + NiUVData are DECODED** in the reader41 IR (engine-exact on 296445). Other controller types remain census/REFERENCE only (engine oracle: NiBoneLODController, NiPSysUpdateCtlr, NiFlipController). |
| **Animation** | NOT claimed from controller presence. Oracle probes at t0/t1 measured actual world-TRS deltas; both probed assets were static in [0, 0.5] (`false_controllers_static_in_0_t1`). No true animated-TRS fixture has been demonstrated yet. |
| **Skinning / skin partition** | Census-level only (oracle saw NiSkinInstance/SkinData/SkinPartition ×2 in BABYLENGUIN); no skin decode. |
| **Particles** | Census-level only (2 NiParticleSystems in BABYLENGUIN); no decode. |
| **Era textures in 3D viewport** | Deliberately not mounted (mounting the ~1 GB era texture archive for a reference-stage render is disproportionate); the Ark textureId is shown in the materials panel with an honest label. |

## Loss policy

- **Fail-closed, loud**: unknown block types, unsupported versions and witness-chain
  violations produce terminal verbatim errors (see inspector's honest terminal states) —
  no partial IR, no silent skips, no default-success fallback.
- **Strip losses documented**: every Ark-strip has a `*.stripmap.json` sidecar (removed
  blocks, remapped links, orphaned kept blocks).
- **Known provenance quirk (recorded, not silently fixed)**: the adapted-copy stripmap's
  `source_sha256` derives from a byte-variant lab source, not the fixture original; both
  SHAs are separately pinned.

## NIF 4.1.0.12 — SUPPORTED (dedicated adapter, W09)

- Module: `src/pesource/NifModelReader41.js` (NEW, W09_a1). A SEPARATE format
  module — **not** an extension of the v10 witness reader. The v10 gate stays
  untouched and 4.1 still LOUD-FAILs inside `NifModelReader` by design
  (negative control N1 of the W09 unit test re-proves it verbatim).
- Method basis: the frozen R61 corpus (`pe_header/pe_block_reader/
  pe_standard_blocks` semantics ported to JS; block boundaries re-validated
  per fixture: every block's `blockEnd == next rttiStart`, 0 opaque, both
  fixtures). Engine-oracle cross-check: **43/43 W09 unit gates** — 218757:
  census 59 blocks + all per-type counts, 26 AV graph nodes, engine-walk
  shape order, TRS/bounds/sample vertices/material exact, and all **22/22
  COMPARE_218757 rows re-derived**; 296445: census 145 blocks + 11 type
  counts, 30-shape vertex-count multiset, graph walk 50 nodes == engine
  (incl. the NiTextureEffect attached via children), maxDepth 3.
- 4.1 format facts (documented differences vs 10.1, proven on the fixtures):
  inline RTTI per block (no type table), no block preamble, 1-byte booleans,
  NiObjectNET carries a **single** extraData link (not the v10 count array),
  NiAVObject has velocity + optional bounding box (no collisionObject),
  NiTriShape has NO hasShader, NiTriShapeData reads numUvSets **late** (after
  colors) with **unconditional** triangles (no keepFlags/compressFlags/
  consistencyFlags), NiMaterialProperty HAS flags, TexDesc slots carry
  ps2_l/ps2_k/unk1, NiTextureEffect has the unknownShort tail, NiStringExtraData
  is link-based (no name). Both fixtures end with an **identical 8-byte
  trailing `01 00 00 00 00 00 00 00`** recorded raw (semantics UNVERIFIED —
  era observation, not interpreted).
- Controllers in 4.1: **NiUVController + NiUVData are DECODED** in the IR
  (NiTimeController fields + data ref; 4 x float key groups) — 296445's
  controller targets NiTriShape `GeoTexanim01:0` (freq 1.0, end 3.333333,
  engine-exact). No animation is claimed from controller presence (the W08
  oracle probe showed world TRS static in [0, 0.5] for both fixtures).
- Unknown block policy: **OPAQUE with offset + span** — boundary found only
  by a known-RTTI-anchored search (exact byte match on known type names,
  never printable-string guessing); with no anchor the parse records
  `STOPPED_OPAQUE_NO_BOUNDARY` and stops. Synthetic negative controls cover
  both paths (N3a–d).
- Inspector: format dispatch on the header version (0x0401000C → reader41,
  0x0A010000 → witness reader, both gates re-verified internally). 218757 /
  296445 render as REFERENCE asset stage (multi-shape, cm→m x0.01, Z-up→Y-up
  (x,z,-y) CURRENT_RUNTIME_CALIBRATION — NOT world instance positions).
- **Adapter coverage = 12 decoded 4.1 block types** (fixture-validated set):
  NiNode, NiTriShape, NiTriShapeData, NiTexturingProperty, NiMaterialProperty,
  NiAlphaProperty, NiZBufferProperty, NiVertexColorProperty, NiStringExtraData,
  NiTextureEffect, NiUVController, NiUVData. Everything else goes OPAQUE.
- **Real-member extension census (W18)**: on actual 2003 Models.ark members the
  adapter additionally hit — and honestly censused as OPAQUE — new types beyond
  the fixture set: **NiKeyframeController / NiKeyframeData** (70 + 70 in avatar
  208861, known-RTTI-anchored), **NiArkAnimationExtraData /
  NiArkTextureExtraData / NiArkImporterExtraData** (1 each), and
  **NiSkinInstance / NiSkinData** in the hair meshes 32498/32509 — these end the
  file with **no known-RTTI anchor after them**, so the parse records
  `STOPPED_OPAQUE_NO_BOUNDARY` and the rendered IR is exactly what was parsed
  (geometry + UV shown, stop displayed, never hidden). All of these are
  **backlog adapters** (skinning + head attachment need them); none is decoded.
- Avatar 208861 (549/549 blocks: NiNode 137, NiTriShape/Data 89+89,
  NiMaterialProperty 89, 89 shapes, 91 Bip01-named nodes) and pair sibling
  208860 (543/543) parse PASS under the census; the avatar is **per-bone
  morph-part chunks, not a skinned body mesh** (that is what the file contains,
  not a parser limitation).
- Backlog (not started): per-shape UV/vertex-color oracle dump to settle the
  v-down UV convention; a kfm/keyframe fixture to demonstrate true animated
  TRS; **NiKeyframeController/NiKeyframeData/NiSkinInstance/NiSkinData
  adapters** (real fixtures now exist — W18 census); more 4.1 block types
  beyond the fixture-validated set on demand.

Cross-check totals summary: **46/46** v10 IR unit checks, **31/32** engine-vs-IR
on 457485 (1 documented different-field), **22/22** on 218757 (R61 lineage, W08),
**43/43** W09 adapter unit gates, browser proof **all gates PASS** (both 4.1
fixtures IR_READY, REVISION 187, 0 fatal; v10 witness regression intact).
