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

**Era drift (ITER-2 census, 2026-09-04):** of the 5,422 shared names,
**5,208 (96.05%) are byte-identical** across eras (same SHA256). Only 214
changed: 211 re-exported within v10.1.0.0 (content edits), 3 upgraded
v4.1.0.12 → v10.1.0.0. The 2003 model corpus survived into 9.3.5 essentially
untouched. Provenance: `99_Audits\PE_NIF_ERA_DRIFT_R2_20260904_115051\`.

## Canonical denominators (stable — do not redefine)

| Denominator | 2003 | 9.3.5 |
|---|---|---|
| NIF files (Models.bnt) | 5,426 | 5,596 |
| Total blocks parsed | 296,489 | 392,061 |
| NiTriShape (container blocks) | 21,190 | 21,914 |
| NiTriShapeData (geometry payloads = "renderable meshes") | 21,106 | 21,830 |
| NiMaterialProperty | ~11,185 | 11,563 |
| NiFlipController | 125 | 126 |
| NiTextureEffect | 1,646 | 1,694 |
| NiVertexMorphExtraData | 79 | 354 |

NOTE: NiTriShape vs NiTriShapeData differ by a counting method (container vs
payload); the delta (84 in 2003, 84 in 9.3.5) is NOT a data error.

## Document map

- [01 — File format: header, primitives, block framing, version gates](01-file-format.md)
- [02 — Block registry: all block types + inheritance chains](02-block-registry.md)
- [03 — Geometry blocks (NiTriShape / NiTriShapeData)](03-geometry.md)
- [04 — Property blocks (materials, texturing, render states)](04-properties.md)
- [05 — Controllers and animation data blocks](05-controllers-data.md)
- [06 — Lights, camera, collision, particle systems](06-lights-camera-particles.md)
- [07 — Skinning (NiSkinInstance / NiSkinData / NiSkinPartition)](07-skinning.md)
- [08 — MindArk proprietary blocks (NiArk*) — NOT in any public NIF doc](08-ark-proprietary.md)
- [09 — Semantics beyond parsing: transforms, units, texture binding, materials](09-semantics.md)
- [10 — Containers (BNT2) and corpus manifests](10-containers-corpus.md)
- [11 — Open problems and REJECTED claims](11-open-problems.md)
- [corpus/ — machine-readable manifest of every NIF (9.3.5)](corpus/)

## Sources (Tier 0/1)

- R61 frozen parser source: `99_Audits\PE_R61_FROZEN_BASELINE_20260828\` (10 .py, SHA256-locked)
- M1D final report + NIF compatibility matrix (same dir, `04_documentation\`)
- PCG_9_3_5 corpus audit: `99_Audits\PE_PCG935_NIF_CORPUS_AUDIT_R1_20260904_113907\`
- Deep dump (per-file inventory): `99_Audits\PE_PCG935_NIF_DEEP_DUMP_R1_20260904_114352\`
- External cross-references used during RE: niflib (BSD-3), nif.xml (GPL-3, historical), jnif (MIT), OpenMW niffile.cpp — for STANDARD blocks only; NiArk blocks have no external reference.
