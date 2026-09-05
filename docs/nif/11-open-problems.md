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
| BNT2 field_d semantics | **RESOLVED (ITER-36)** — carried-forward registration CRC |
| NiArkImporter 38 B tail | **DECODED (ITER-10)** — model local bounding box |
| Importer header patterns | **DECODED (ITER-29)** — version-routed + exporter strings |
| Texture slot vocabulary | **CLOSED (ITER-32)** — 40 slots, f1 slot enum, 24,508/24,508 |
| Shader directive vocabulary | **CLOSED (ITER-32)** — 17 names, 623 configs |
| Viewport 43 B class | **DECODED (ITER-28)** — camera/viewport family |

## Byte-level UNKNOWNs (parse-safe, semantics open — all raw-kept + SHA256)

| Item | What is known | What is open |
|---|---|---|
| BNT2 index field_d | **RESOLVED (ITER-36, STRONGLY_SUPPORTED)**: carried-forward REGISTRATION CRC — the payload's CRC32 at its last registering event in the archive lineage; d==c ⇔ unchanged since registration (c_eq_d 3,435/5,596 = 61.42%; 2003 mirror 3,299/5,426 = 60.80%) | exact packer write-path mechanism (inferred from value patterns; the archive tool itself not observed) |
| NiArkAnimationExtraData TEXT records | **DECODED (ITER-5/16)**: per-node procedural behavior config — node name, mode (activeIdle/single/Single/active/activeIdle/single — STATE-BINDING
label DECODED in ITER-38: twin-record proof 41076.nif — byte-identical
params, only the mode differs; `active` = weapon fire-state family
(542418/542466/542520), `single` = one-shot (count=1 in 87%), `Single` =
one-file orthography (386359.nif), `activeIdle/single` = lone contaminated
compound (slash, not hyphen)), channels (derivatives/Controllers/cyclic/ParticleSystem/Texture/NodeUpdate), targets (position/rotation/velocity/All), axis+speed params, LOOP mode; 1,274 records censused with FULL field lists (`PE_NIF_G3CB_SCHEMA_R16_COR_20260904_142550`); param tail BRANCHED per channel (ParticleSystem 14-18, derivatives 7-10, Controllers 1-16, cyclic 8-10) | per-channel param SEMANTICS field-by-field (values readable, meaning unmapped) |
| NiArkAnimation binary records | **DECODED (ITER-6/7)**: G3B 33B record + embedded event-name registry (morph: left/right, sound:hit_01-03, start_usetool:*) connecting behaviors to vertex morphs BY NAME | G3D internal record SEMANTICS (role of class 01/02/03 flags — all target skeleton nodes, interleaved, Scene-Root-last invariant (ITER-37); exact 01/02/03 engine semantics UNVERIFIED; the size formula `u3_byte1×5` was RETRACTED-from-suspicion: CONFIRMED CORRECT 348/348 in ITER-27). RESOLVED: string framing — G3E 4/4, G9_RTTI 10/10 (2-byte lead; R7/R9 hexes were link-shifted, corrected), BINARY 4/4 (ITER-31) |
| NiArkAnimationExtraData extension | full grammar + variant census (9.3.5: V10_BASE_0B 2270, G3B 1685, G3D 348, FIXED_A 347, G3C 308, FIXED_B 190, TEXT_CRLF 172, V10_BASE_33B 125) | (none open — byte-exact closure by ITER-30/31: G3B 1,682/1,682; G3D 348/348; G3E/BINARY/G9_RTTI/SHORT28/G3A 59/59; remaining family items = G3D class-byte role + per-channel TEXT param labels) |
| NiArkImporterExtraData (v10) | 38 B tail = MODEL LOCAL BOUNDING BOX CONFIRMED (ITER-10: 3,020/3,020 mesh-bearing files); header = version-routed layout + exporter-version string; 14 exact / 10 masked patterns (ITER-29) | mode/flag-bit semantics; the 3-byte flag region (states 558/128/72 — UNVERIFIED) |
| NiArkTextureExtraData field1 / field2-low8 | two classes: {field1=1, low8=0} ×3,042 / {field1=-256, low8=255} ×1,796 | what the classes mean |
| NiArkViewportInfoExtraData ext > 13 B | structure DECODED (ITER-8/28): `[u8 class byte][flags][payload]`; 85 B / 121 B classes = per-file camera/viewport float parameter blocks (floats CONFIRMED); 43 B = two sub-classes (all-zero defaults vs camera floats) | exact per-field semantics (fov/near/far/position — PLAUSIBLE, not CONFIRMED) |
| NiVertexMorphExtraData payload | per-vertex record model CONFIRMED (ITER-4: N records × [tag][W×f32], W∈{10,11}, weight pairs sum to 1.0, 2⁻¹⁸ quantization); big spans MULTI-FORMAT (ITER-19/20/21): Family A entry-stream consumption model 9,272/10,274 = 90.25% upper bound (R18 run6 + R20 backtrack; NOT the true record grammar — R33), Family B H-KEY42 strict units 1,915 + 669 r19-only spans, 325 heterogeneous residual (3.16%, 56 files); REAL sparse records = 10.8% of entries (R33) with var-k grammar `[u16 idx][k×f32 Σ=1.0][9×f32]` byte-exact 2,093/2,427 real-record spans = 86.2% (ITER-34); artifact payload = quantized-f32 records (≤7-bit mantissas, 2⁻¹⁴..2⁻²¹ grids — ITER-34) | remaining open (post-ITER-34): exact head semantics in artifact regions; the 9-float triple grouping (3 morph states × XYZ?); the last-record extra float's meaning. RESOLVED along the way: big-span layout = MULTI-FORMAT (Family A entry-stream consumption model 90.25% upper bound incl. R20 backtrack; Family B H-KEY42 strict units +669 r19-only; 325 heterogeneous residual — R19/R20/R21); entry ids = greedy-walk artifacts except the 10.8% REAL sparse records (R33); artifact encoding = quantized f32 — the f16 pair candidate was TESTED and REJECTED (R34 T-F16) |
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
