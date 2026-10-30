# NIF_BINDINGS — what the NIF side of the pipeline actually does

Scope note: everything below is **NIF 10.1.0.0 witness-scope**, cross-checked against a
headless stock **Gamebryo 1.2 engine oracle** (built from 32-bit SDK libs, SHA-pinned).
NIF 4.1.0.12 is gated (see bottom). Nothing here claims a full Gamebryo reimplementation.

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
| **Controllers** | IR records refs only, honestly marked OPAQUE — no controller block decoding in the witness scope. Engine-oracle censuses exist as REFERENCE (NiBoneLODController, NiPSysUpdateCtlr, NiUVController+NiUVData, NiFlipController). |
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

## NIF 4.1.0.12 — gated, adapter pending

- The version gate loud-fails by design (`NifModelReader: version 0x0401000c NOT
  implemented`). **No 4.1 IR is faked.**
- The engine oracle *has* validated a 4.1 reader lineage (frozen R61 `peReader.js`):
  22/22 field match on 218757_stripped — but that is reference evidence, not this
  runtime's adapter.
- Backlog (not started): dedicated 4.1 adapter reusing the R61 lineage + oracle
  cross-check; per-shape UV/vertex-color oracle dump to settle the v-down UV convention;
  a kfm/keyframe fixture to demonstrate true animated TRS.

Cross-check totals summary: **46/46** IR unit checks, **31/32** engine-vs-IR on 457485
(1 documented different-field), **22/22** on 218757.
