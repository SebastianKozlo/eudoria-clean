# 11 — Open problems and REJECTED claims

## Byte-level UNKNOWNs (parse-safe, semantics open — all raw-kept + SHA256)

| Item | What is known | What is open |
|---|---|---|
| NiArkAnimationExtraData extension | full grammar (FIXED/BINARY/TEXT_CRLF variants, trailers 6/35/39 B) | per-field semantics of node records; u1..u4 header meanings |
| NiArkImporterExtraData trailing 38 B (v10) | always 38 B (Mode1+Mode2) | field meanings |
| NiArkTextureExtraData num_tex (=3), field1, field2-low8 | entry structure + counts decoded | semantics; low-8 flags |
| NiArkViewportInfoExtraData extension | ≤121 B, boundary-exact | full internal layout |
| NiVertexMorphExtraData payload | 15..59,027 B, first byte always 0x01 | morph/weight field layout |
| NiArkShaderExtraData unknownInt/unknownString | int + string layout | shader config semantics |
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
