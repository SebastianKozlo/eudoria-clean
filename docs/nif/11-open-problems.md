# 11 — Open problems and REJECTED claims

## Solved during the documentation loop (2026-09-04, ITER-3 census)

| Item | Status |
|---|---|
| BNT2 index field_c | **CONFIRMED = CRC32(payload), 5,596/5,596** |
| NiArkShaderExtraData unknownString | **DECODED** — CRLF shader config (`effectfile`, `CullMethod`, `AlphaTreshold`, `EnableAnimation`, `reflectionMapCube`/`EnvMapCube`); unknownInt = 0 always |
| NiArkViewportInfoExtraData ext len 13 | **DECODED** — `0x03 + 12×00` (2,304 files); length histogram quantized odd |
| NiVertexMorphExtraData header | **DECODED** — `0x01 + u32 vertex_count + u16 flags` |
| NiArkTextureExtraData entry names | `<material>_<SLOT>` convention decoded (BASE/BUMP/ENVIRONMENT) |
| NiArkAnimationExtraData u1 | constant 5 (v10) / 0 (v4) — era marker |

## Byte-level UNKNOWNs (parse-safe, semantics open — all raw-kept + SHA256)

| Item | What is known | What is open |
|---|---|---|
| BNT2 index field_d | == CRC32(payload) in 3,435/5,596 | the differing 2,161 (REJECTED: 2003-era crc, crc32c, name-concats, halves, cross-entry) |
| NiArkAnimationExtraData TEXT records | **DECODED (ITER-5/16)**: per-node procedural behavior config — node name, mode (activeIdle/single/Single/active/activeIdle-single), channels (derivatives/Controllers/cyclic/ParticleSystem/Texture/NodeUpdate), targets (position/rotation/velocity/All), axis+speed params, LOOP mode; 1,274 records censused with FULL field lists (`PE_NIF_G3CB_SCHEMA_R16_COR_20260904_142550`); param tail BRANCHED per channel (ParticleSystem 14-18, derivatives 7-10, Controllers 1-16, cyclic 8-10) | per-channel param SEMANTICS field-by-field (values readable, meaning unmapped) |
| NiArkAnimation binary records | **DECODED (ITER-6/7)**: G3B 33B record + embedded event-name registry (morph: left/right, sound:hit_01-03, start_usetool:*) connecting behaviors to vertex morphs BY NAME | G3D internal layout (348 blocks; index lists; the frozen parser's byte[1]×5 size formula is WRONG — correction = bounded R61 follow-up under frozen-baseline rules); G3D/G9 exact string framing |
| NiArkAnimationExtraData extension | full grammar + variant census (9.3.5: V10_BASE_0B 2270, G3B 1685, G3D 348, FIXED_A 347, G3C 308, FIXED_B 190, TEXT_CRLF 172, V10_BASE_33B 125) | binary-variant inner layouts |
| NiArkImporterExtraData trailing 38 B (v10) | first byte = Mode marker; `ffffff 00000000 ffffffff ffffff` + float-like ~20 B + 00; 4,017 distinct | field meanings |
| NiArkTextureExtraData field1 / field2-low8 | two classes: {field1=1, low8=0} ×3,042 / {field1=-256, low8=255} ×1,796 | what the classes mean |
| NiArkViewportInfoExtraData ext > 13 B | quantized odd lengths 21/85/49/45/121/35/39/43 | internal layout of longer exts |
| NiVertexMorphExtraData payload | per-vertex record model CONFIRMED (ITER-4: N records × [tag][W×f32], W∈{10,11}, weight pairs sum to 1.0, 2⁻¹⁸ quantization); exact-walk blocks: 15/354 uniform + 6,167/10,274 big spans fit the entry-stream model `[u16 id][4×f32]`+pad+2B tail (ITER-18 run6, 60.03% upper bound) | the 339 sparse blocks' inner layout; residual 4,107 spans show repeating `[u16 value][u16 0]` pairs (f16-like — untested candidate); the last-record extra float's meaning; entry id semantics |
| BNT2 index field_c / field_d | structure | semantics (hash? crc? flags?) |
| NiPixelData unknown3/unknown8 bytes | offsets fixed | meaning |
| NiVertexColorProperty unknown_pe_field | values 0/1 | meaning |
| TDF material tail dims (dim2/dim4 masks) | structure CONFIRMED | per-dim render semantics |
| Terrain blend op/order, UV scale, filtering/mip | data layer CONFIRMED | exact historical render behavior (needs D3D8 runtime RE) |

## Milestone-open items (need runtime or cross-file work)

- **M3-5B**: non-BASE material slot semantics (DARK/DETAIL/GLOSS/GLOW/BUMP)
  — runtime-gated.
- **Cross-file skeleton pairing**: mesh-NIF ↔ ANIMATION_SKELETON by bone
  name — the era's normal pattern; full-avatar assembly UNRESOLVED at
  closure level (iteration-29 work exists but unreported/frozen).
- **World placement origin**: SERVER_DELIVERED only STRONGLY_SUPPORTED;
  definitive test = runtime origin trace (emulator track, human-gated).
- **D3D8 trace**: PE2 exits at slot2 before D3D8 use — blocker documented;
  static-canon fallback in place.
- **CD-2003 dialect**: 70 CD-only models fail R61 (17 unsupported types +
  53 layout divergences) — separate bounded work package, not blocking.

## REJECTED claims — DO NOT RESURRECT (each byte-documented in audits)

- NIF local transforms = world placement — REJECTED
- 0x5C material object = world transform — REJECTED
- FUN_005040F0 = PropertyOwner world/bound writer — REJECTED
- SFO +0x24/+0x28/+0x2C = world XYZ — REJECTED
- 0x360 float triplets = world XYZ — REJECTED
- SceneContext+0x134 = world placement — REJECTED
- PropertyOwner aggregate bound center = instance origin — REJECTED
- DPVS = placement source — REJECTED
- 200xx fixed placement-table model — REJECTED (encoding census)
- 24007 direct model-link/static-placement — REJECTED (not proven; absent in tested corpus)
- World RTTI string families (EP_MODEL, RealWorldItem, ArkStatic, ArkClientWorld, ArkModelManager, ArkResource, ArkTeleport, ...) — NOT PRESENT in the verified binary corpus
- GLOSS=roughness / BUMP=normalMap — REJECTED as overclaim
- "NiArkBillboardNode is a distinct layout" — REJECTED (alias of NiNode)
- Weight normalization of terrain masks (sums>255 in 33,295 tiles) — REJECTED
- "hasX=true + numVertices=0 is corrupt" — REJECTED (niflib-legal)

## The honest 100% statement

- **PARSE closure = 100%** on both eras (5,426/5,426 and 5,596/5,596; every
  block of every file consumed exactly, zero failures).
- **BYTE coverage ≈ 100%** (every byte is accounted for structurally —
  either parsed into a field or preserved raw+hashed).
- **SEMANTIC closure = PARTIAL** — the table above is the complete honest
  list of what remains unknown; nothing outside that list is open.
