# NIF Format Wiki — Project Entropia (MindArk / Gamebryo NetImmerse)

This is the complete, evidence-based documentation of the NIF binary format as
used by Project Entropia — reverse-engineered from the physical game files, so
that **nobody ever has to re-do this work**. Every claim is labeled with an
evidence status and a source.

## Evidence model (used everywhere in these docs)

| Label | Meaning |
|---|---|
| CONFIRMED | Byte-level proof on the full corpus + cross-validation (niflib/nif.xml/jnif + independent decoder) |
| STRONGLY_SUPPORTED | Strong multi-source evidence, minor residue |
| PLAUSIBLE | Reasonable interpretation, not yet proven |
| UNKNOWN | Bytes are consumed correctly but semantics are not understood |
| REJECTED | Tested and disproven — do not resurrect |

Key provenance rule: **physical evidence outranks documentation**. The frozen
R61 parser (SHA256-locked, 5426/5426 PASS on 2003 corpus; 5596/5596 PASS on the
PCG_9_3_5 corpus, 2026-09-04 audit) is the executable embodiment of this wiki.

## Corpus eras (never mix denominators)

| Era | Container | NIF count | Versions | Status |
|---|---|---|---|---|
| EU runtime 2003 | `Models.bnt` (BNT2) | 5,426 | v10.1.0.0 × 4,665 / v4.1.0.12 × 760 / v4.0.0.2 × 1 | R61 parse closure 100% (M1D, FROZEN) |
| PCG 9.3.5 (primary) | `pcg_install\Data\Models\Models.bnt` (BNT2) | 5,596 | v10.1.0.0 × 4,838 / v4.1.0.12 × 757 / v4.0.0.2 × 1 (52555.nif!) | R61 parse closure 100% (2026-09-04, no parser change) |
| CD Jan 2003 | `Models.ark` (ARK/VFS) | 2,492 | mixed | different corpus; 70 CD-only models fail R61 (17 unsupported block types + 53 dialect divergences) |

Continuity 2003 → 9.3.5 (name-level): 5,422 shared names, 4 removed
(13563/261922/38579/524174), 174 added (all post-2003 ID range 59xxxx).

**Era drift (ITER-2 census, refined by ITER-36):** of the 5,422 shared
names, **5,208 (96.05%) are byte-identical** across eras (same SHA256). Only
214 changed: 211 within v10.1.0.0 + 3 upgraded v4.1.0.12 → v10.1.0.0.
ITER-36's field_d lineage evidence decomposed the 211: **46 true
size-changing re-exports** (all Gamebryo_1_1; d rewritten 46/46) + 165
equal-size changes — mostly 1-ULP float32 reprocessing (134 files, every
changed byte exactly +1 ULP) with field_d STABLE in 161/165 (non-registering
touch-ups), only 4 real equal-size edits. The 2003 model corpus survived
into 9.3.5 essentially untouched. Provenance:
`99_Audits\PE_NIF_ERA_DRIFT_R2_20260904_115051\`,
`99_Audits\PE_NIF_FIELD_D_R36_20260904_171903\`.

## Canonical denominators (stable — do not redefine)

| Denominator | 2003 | 9.3.5 |
|---|---|---|
| NIF files (Models.bnt) | 5,426 | 5,596 |
| Total blocks parsed | 296,489 | 392,061 |
| NiTriShape (container blocks) | 21,190 | 21,914 |
| NiTriShapeData (geometry payloads = "renderable meshes") | 21,106 | 21,830 |
| NiMaterialProperty | 11,186 | 11,563 |
| NiFlipController | 125 | 126 |
| NiTextureEffect | 1,646 | 1,694 |
| NiVertexMorphExtraData | 286 blocks (79 files) | 354 blocks (118 files) |

NOTE: NiTriShape vs NiTriShapeData differ by a counting method (container vs
payload); the delta (84 in 2003, 84 in 9.3.5) is NOT a data error.

## State of documentation (2026-09-04, post-ITER-39 audit)

The whole wiki was audited against the on-disk run inventory by ITER-39
(45 gaps closed at commit 3e383ce); ITER-40 added this summary and the
ch09 semantic enrichment. Coverage: **parse closure 100% on BOTH eras**
(5,596/5,596 PCG 9.3.5 + 5,426/5,426 EU 2003, frozen R61, zero parser
changes); **byte coverage ~100%** (every byte parsed into a field or
raw-kept + hashed); semantic closure is per-family — the status table
below, the complete open-unknowns table in
[11-open-problems.md](11-open-problems.md).

| Family / block type | Documentation status | Where |
|---|---|---|
| Header, primitives, block framing, version gates | CONFIRMED (M1D-locked) | ch01 |
| Geometry (NiTriShape / NiTriShapeData) | CONFIRMED | ch03 |
| Standard property blocks | CONFIRMED | ch04 |
| Keyframe & controller data (C12-B layout) | CONFIRMED (byte-exact, independent decoder) | ch05 |
| Lights, camera, collision, particles | CONFIRMED | ch06 |
| Skinning (NiSkin*; LBS formula) | CONFIRMED (empirical; 20/20 trace) | ch07 |
| NiArkAnimationExtraData — all 14 variants | STRUCTURE closed byte-exact (ITER-30/31: G3B 1,682/1,682, rare families 59/59, G3D 348/348); SEMANTICS decoded (TEXT behavior records ITER-5/16; Controllers attachment ITER-24; viewport suite ITER-25; modes ITER-38; event registry ITER-7/30); G3D class 01/02/03 engine roles UNVERIFIED (ITER-37) | ch08, ch09 |
| NiArkShaderExtraData | CONFIRMED — 17-directive CRLF config grammar, two effect families (ITER-32; 16 directive names in 2003 — R35) | ch08, ch09 |
| NiArkTextureExtraData | CONFIRMED — 40-slot vocabulary, f1 = slot enum, packed field2 formula 4,838/4,838 (ITER-32) | ch08, ch09 |
| NiArkImporterExtraData | CONFIRMED — 38 B model-local bounding box (ITER-10, 3,020/3,020) + version-routed header, 14 exact / 10 masked patterns (ITER-29); 3 flag bytes' semantics UNVERIFIED | ch08, ch09 |
| NiArkViewportInfoExtraData | Structure + camera floats CONFIRMED (ITER-8/28); exact per-field semantics PLAUSIBLE | ch08, ch09 |
| NiVertexMorphExtraData | Record model + quantized-f32 encoding CONFIRMED (ITER-4/34); variable-k sparse grammar byte-exact on 86.2% of real-record spans; 325-span heterogeneous residual OPEN (ITER-21) | ch08, ch09 |
| BNT2 index field_c / field_d | field_c = CRC32(payload) CONFIRMED both eras; field_d = carried-forward registration CRC RESOLVED (ITER-36, STRONGLY_SUPPORTED) | ch09, ch10 |
| Cross-era grammar stability | 19 ERA-STABLE / 2 EVOLVED / 0 falsifications (R35) | ch10 |

The honest UNVERIFIED list (top open items — full rows in ch11):

- **Morph artifact head semantics** — the record-head bytes inside
  artifact regions, the 9-float triple grouping (3 morph states × XYZ?),
  and the last-record extra float (post-ITER-34 residue).
- **G3D class 01/02/03 roles** — structure CONFIRMED (interleaved
  per-file animated-node list; the Scene-Root reference is always LAST,
  348/348) but no tested property partitions the classes; the class byte
  is file-configuration dependent, NOT node-intrinsic (ITER-37).
- **TEXT numeric param labels** — per-position value distributions mapped
  (ITER-23); the per-channel amplitude/phase/period roles stay INFERRED
  (runtime consumer evidence required).
- **The 325-span morph sliver** — 3.16% heterogeneous residual fitting no
  single grammar (ITER-21); fully dumped for a future deep dive.
- **Importer flag bits** — the 3-byte flag region has exactly 3 states
  (558/128/72 in 9.3.5; 561/128/72 in 2003) with no derivable semantics
  (ITER-29).
- **Non-BASE material slot runtime semantics** — slot identity closed
  (ITER-32); what GLOSS/BUMP/DARK/etc. DO at runtime needs D3D8 evidence
  (M3-5B).
- Plus the milestone-open items (cross-file skeleton pairing closure,
  world placement origin, D3D8 trace blocker, CD-2003 dialect) — ch11.

## Document map

- [01 — File format: header, primitives, block framing, version gates](01-file-format.md)
- [02 — Block registry: all block types + inheritance chains](02-block-registry.md)
- [03 — Geometry blocks (NiTriShape / NiTriShapeData)](03-geometry.md)
- [04 — Property blocks (materials, texturing, render states)](04-properties.md)
- [05 — Controllers and animation data blocks](05-controllers-data.md)
- [06 — Lights, camera, collision, particle systems](06-lights-camera-particles.md)
- [07 — Skinning (NiSkinInstance / NiSkinData / NiSkinPartition)](07-skinning.md)
- [08 — MindArk proprietary blocks (NiArk*) — NOT in any public NIF doc](08-ark-proprietary.md)
- [09 — Semantics beyond parsing: transforms, units, texture binding, materials + shader directives, animation behaviors, morph precision, build lineage](09-semantics.md)
- [10 — Containers (BNT2) and corpus manifests](10-containers-corpus.md)
- [11 — Open problems and REJECTED claims](11-open-problems.md)
- [corpus/ — machine-readable per-file manifests, BOTH eras (9.3.5 + 2003)](corpus/)

## Sources (Tier 0/1)

- R61 frozen parser source: `99_Audits\PE_R61_FROZEN_BASELINE_20260828\` (10 .py, SHA256-locked)
- M1D final report + NIF compatibility matrix (same dir, `04_documentation\`)
- PCG_9_3_5 corpus audit: `99_Audits\PE_PCG935_NIF_CORPUS_AUDIT_R1_20260904_113907\`
- Deep dump (per-file inventory): `99_Audits\PE_PCG935_NIF_DEEP_DUMP_R1_20260904_114352\`
- External cross-references used during RE: niflib (BSD-3), nif.xml (GPL-3, historical), jnif (MIT), OpenMW niffile.cpp — for STANDARD blocks only; NiArk blocks have no external reference.
- NIF documentation loop runs (ITER-2..40): `99_Audits\PE_NIF_*` run dirs —
  per-iteration findings in `00_PROJECT_CONTEXT\PE_AUTO_LOOP.json`
  (nif_documentation_loop_2026_09_04). ITER-39 audited the entire wiki
  (45 gaps closed at commit 3e383ce); ITER-40 added the README
  state-of-documentation section and the ch09 semantic enrichment
  (R29-R38 results: material slots, shader directives, morph precision,
  field_d lineage, exporter provenance, attachment system, TEXT modes).
