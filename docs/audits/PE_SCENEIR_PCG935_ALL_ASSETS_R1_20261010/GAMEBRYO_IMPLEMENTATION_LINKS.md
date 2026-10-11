---
run_id: PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010
card: gamebryo-lifecycle-links
status: IMPLEMENTED_AND_MEASURED
sources:
  - module: src/pecompat/PecSceneIR.js (buildAssetIR/validateSceneGraph/composeWorldTransforms/computeSceneBounds)
  - module: src/pecompat/PecNif10CorpusReader.js + PecNif41Reader.js (stream/link phases)
classification: INTERNAL_QC_ONLY_PENDING_DESKTOP
created: 2026-10-11
---

# Gamebryo lifecycle discipline — implemented links

| Lifecycle phase | Implementation in this run | Evidence |
|---|---|---|
| Creation/Stream | Both readers stream blocks from the physical BNT2 index payloads with fail-closed identity (server verifies Models.bnt/Textures.bnt SHA256 at startup) | server boot logs; input SHAs |
| Link | readNif*Corpus validate all refs in-range before closure returns; validateSceneGraph counts errors; links: extraDataRef chains, controllerRef, propertyRefs, children, effects, dataRef/skinRef, controller dataRef/targetRef | gate2 positives; catalog `errors` counts |
| Post-link/Root | TopObjects footer = root set (measured: usually [0] single root); multi-root files preserved as-is | footers in reader results |
| Parenting/sharing | composeWorldTransforms walks parentWorld × local (FILE_SCENE_SPACE); shared geometry (TriShapeData referenced by multiple TriShapes) counted; instances not duplicated | world maps in asset JSON |
| Controllers | controllerRef on NET blocks + per-controller dataRef/targetRef; keyframe/UV/vis/flip/material-color/alpha families emitted with original keys | animation-decoder card |
| Bounds | computeSceneBounds over world-transformed geometry; empty assets stay UNKNOWN (no null->0) | RANKING_COVERAGE.json |

## Corrections inherited from CAM lessons (contract §2/§51)

- CAM-C2 (FAILED rows counted as measured complexity): FAILED rows keep
  `measured=false` semantics in the catalog (extent null, meshes 0, err kept)
  and the sweep records SKIPPED_KNOWN_FAIL separately.
- CAM-C3 (cache era/container identity): the server verifies the container
  SHAs at startup (fail-closed) and the parse cache is keyed by numeric entry
  id (the id bijects 1:1 with the container index; wrong-era/foreign ids are
  refused before any parse). Asset JSON carries payloadSha256 + version.
- CAM-C1 (CD-era GLB availability): out of scope for this PCG-only feature —
  NOT reported CLOSED (remains open in the old package).
