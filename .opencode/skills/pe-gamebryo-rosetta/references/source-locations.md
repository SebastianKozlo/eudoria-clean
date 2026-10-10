# Local source routes

Resolve these locations on the execution host; record current identities
before relying on them. Source code may be proprietary: keep full excerpts
and originals local. Public references must be original summaries with
reproducible source identities.

## Gamebryo SDK (architectural references only — never copied into committed code)

- SDK 1.2: `D:\gamebyroengine\extracted\Gb12_Source`. The composition law
  lives in `CoreLibs\NiMain\Win32\NiAVObject_Win32.cpp` (UpdateWorldData:
  `m_kWorld = parent->m_kWorld * m_kLocal`, else `= m_kLocal`) and
  `CoreLibs\NiMain\Win32\NiTransform.inl` (compose + point operators).
  Setters in `NiAVObject.inl` write LOCAL state only; reparenting does no
  compensation (`NiNode.cpp` AttachChild/SetAt). Geometry HOLDS a shared
  NiGeometryData reference (`NiGeometry.cpp` SetModelData).
  MEASURED identities (SHA256) of the five files read for
  PE_935_SCENEIR_MODEL_218757_BROWSER_R1: see that run's
  `docs/audits/.../SOURCE_IDENTITIES.json` (gb12_source_files).
- SDK docs: `D:\gamebyroengine\extracted\Gb112_docs_html`.
- Samples: SDK `Samples\Tutorials\04 - Scene Attachment`,
  `Samples\Demos\BackgroundLoad`. SDK behavior, not proof of PE's world source.
- SDK 2.6: `D:\gamebyroengine\extracted\Gb26_src`
  (NiTransformationComponent, NiSceneGraphComponent, NiExternalAssetNIFHandler
  — definition-vs-instance inheritance, retrieved-root TRS application,
  pristine-root/clone separation). Later-generation comparisons, not a
  substitute for a 1.x/PE trace.

## PE reconstruction (the executed lineage)

- Canonical client sources: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`
  (`src/pesource`, `src/peworld`). `NifModelReader.js` is single-witness
  (457485); inspect its actual implementation before widening use.
- THIS RUN's worktree (feature branch codex/pe-sceneir-218757-r1-20261009):
  `D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1` —
  `src/pecompat/` (adapter), `compat/` (app + loopback server),
  `tools/pecompat/`, `tests/pecompat/`, report package under
  `docs/audits/PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009/`.
- Pinned original container (READ_ONLY):
  `D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt`
  (395412868 B / SHA256 c950a8c2…d3bee0); model 218757 entry `218757.nif`
  (ordinal 781 / offset 116223520 cross-checks; 57316 B / SHA256
  3e8a22c2…12cf36 — the payload hash is the extraction authority).
- Integration prototype (patterns only):
  `D:\Eudoria_Reconstruction\12_WebGame\eudoria-compat-threejs-r1\compat` —
  entry-API + provenance-header + client-SHA cross-check pattern; its model
  mode renders the SINGLE witness mesh only.
- Viewer examples: `D:\Eudoria_Reconstruction\12_WebGame\tools\pe_asset_viewer_v4\src`
  (GLB/playback paths are implementation examples, not original NIF loader
  acceptance). `D:\Eudoria_Reconstruction\12_WebGame\eudoria-web\src` (legacy
  r169 runtime — NOT compatible with the 0.185.0 stack without broad work).
- The pinned three package (configured private root for the app server):
  `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\node_modules\three`
  (0.185.0; version-verified at every server start).
