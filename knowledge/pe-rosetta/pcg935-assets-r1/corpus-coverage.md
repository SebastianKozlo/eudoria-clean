---
run_id: PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010
card: corpus-coverage
status: MEASURED_ON_CORPUS
sources:
  - catalog: PRIVATE_OUTPUT_ROOT/catalog/catalog.json (5596 entries)
  - checkpoints: batch10 (4838), batch41 (757), catalog checkpoint (5596)
classification: INTERNAL_QC_ONLY_PENDING_DESKTOP
created: 2026-10-11
---

# Corpus coverage — denominators, failures, UNKNOWN classification

## Denominators (re-measured from the physical BNT2 index; match the pinned set)

- 5,596 total Models.bnt entries (0 CRC mismatches, 0 overlaps/gaps/dup names)
- 4,838 × NIF 10.1.0.0 · 757 × NIF 4.1.0.12 · 1 × NIF 4.0.0.2 (52555.nif)

## Parse outcome (per-version corpus readers)

- 10.1.0.0: 4,832/4,838 PASS (99.88%) — 7 honest FAILs (below)
- 4.1.0.12: 757/757 PASS (100%)
- 4.0.0.2: 1/1 PASS (EOF-exact, 37 blocks)
- Union: 5,589/5,596 PASS (99.87%), 7 FAIL (0.125%)

## The 7 honest FAILs (recorded, not relabeled)

- 472836, 543836, 546348, 68336 — closure returns but a TriShape dataRef
  points at a NiNode (MODEL_DATA_REF_TYPE_MISMATCH family; candidate sets
  wrong-but-closing; recorded AMBIGUOUS).
- 592605, 591780 — CLOSURE_FAIL in the NiSkinData context (64K attempts;
  these files combine ArkViewportInfo + ArkShaderExtraData +
  VertexMorphExtraData boundary blocks + skins; candidate product explodes).
- 204828 — CLOSURE_FAIL in the NiSkinPartition context (block 160 region).
- 419159 — EOF-region misparse (last blocks 22-24 + tail bytes unresolved).

## Extent UNKNOWN (1,843 entries — NOT failures)

Genuinely mesh-less assets: lights (NiPointLight/NiAmbientLight holders),
empty viewport placeholders, controller/rig-only files (e.g. 462325: 50 kf
controllers, 0 meshes). Their mesh/tri/vert counts are measured ZERO and
extent stays UNKNOWN — never null->0 promotion, ranked LAST.

## Runtime sweep categories (gate 9)

OK / FAIL / SKIPPED_KNOWN_FAIL are recorded separately; known-fail entries
are not re-run in the sweep (their API behavior is verified separately via
the truthful 422 route probe).
