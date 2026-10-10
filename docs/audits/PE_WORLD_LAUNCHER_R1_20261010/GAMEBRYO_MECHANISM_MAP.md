# GAMEBRYO_MECHANISM_MAP — PE_WORLD_LAUNCHER_R1_20261010

RUN_ID = PE_WORLD_LAUNCHER_R1_20261010
PHASE = ETAP_B_MECHANISM_RESEARCH (research in service of implementation; NO launcher code written in this phase)
WRITTEN_AT = 2026-10-10 (this phase; measured identities recorded fresh at write time)
CONTRACT § = OPENCODE_PE_WORLD_LAUNCHER_R1_20261010.md §3 (Etap B)

## 0. Method and standing rules

- For each mechanism: **SOURCE+VERSION+SHA → OBSERVED SDK BEHAVIOR → PE EVIDENCE OR
  GAP → ADAPTER DECISION → CONTROL (EXECUTED vs PLANNED)**. Controls marked PLANNED
  are pointed at their later phase (C/D/E) — they are NOT claimed as executed.
- SDK sources/docs are READ_ONLY; **no SDK source, documentation or binary text is
  copied into this repo** — only this original summary with reproducible identities.
- SDK generation identity (measured, not assumed):
  - `Gb12_Source` = Gamebryo **1.x** sources — `CoreLibs\NiSystem\NiVersion.h`
    `#define GAMEBRYO_MAJOR_VERSION 1` (measured); copyright 1996-2005 Numerical
    Design Limited. The prior-run stock tools were "Gamebryo 1.2.2".
  - `Gb26_src` = **Emergent** Gamebryo 2.6-generation sources (copyright 1996-2008
    Emergent Game Technologies) — used ONLY as a separately-described later-generation
    comparison, never as a 1.x/PE trace.
  - `Gb112_docs_html` = Gamebryo **1.1** compiled HTML help (Gamebryo_1_1.hhc).
- **SDK knowledge is NOT PE knowledge.** MOUT/BackgroundLoad/SceneAttachment are
  OTHER APPLICATIONS' examples — behavioral references, never proof of the Entropia
  terrain format, the PE streaming design, or any PE world semantics.

## 1. SDK file identities read this phase (all measured fresh; READ_ONLY)

| # | Path (under `D:\gamebyroengine\extracted\`) | Size B | SHA256 | Examined content |
|---|---|---:|---|---|
| F1 | `Gb12_Source\CoreLibs\NiMain\NiStream.cpp` | 38458 | e955c36ebbb442029e00be8a154726741b8454a607f2dc043f1fd542b009dc25 | LoadHeader L303-360; RTTIError L387-400; CreateObjectByRTTI L402-410; LoadRTTI L412-449; LoadObject L451-468; LoadStream L506-635; LoadTopLevelObjects L362-385; ResolveLinkID L226-243; RegisterLoader L755-766; FreeLoadData L1059-1117; constructor/registry L56-139 |
| F2 | `Gb12_Source\CoreLibs\NiMain\Win32\NiAVObject_Win32.cpp` | 999 | 75e452680d4b52d469ec69ef33c79cf94bf0f3e334250b8fab3892077bf23fd4 | UpdateWorldData L22-31 (whole file) |
| F3 | `Gb12_Source\CoreLibs\NiMain\Win32\NiTransform.inl` | 1067 | 92e8acf6d94940344adca654e3a3344656ca3cbb4ba0b4d19b028a08e6c56b7b | operator* L15-24; point transform L26-29 (whole file) |
| F4 | `Gb12_Source\CoreLibs\NiMain\NiAVObject.inl` | 10672 | 09e1a5a5c88af503d9566b487941305307cba5cb1513147fb49e5a4dbdc91c3b | setters L82-143 (local), world setters L145-158, accessors L165-198, property list L200-224 (whole file) |
| F5 | `Gb12_Source\CoreLibs\NiMain\NiAVObject.cpp` | 33215 | 72e0837149b03ccda171bdf5e68e1e1f8c2712b2f10e7957ac3ec26344ca5ea7 | AttachParent L62-69; Update/UpdateDownwardPass L110-136; UpdateSelected/UpdateRigidDownwardPass L138-188 |
| F6 | `Gb12_Source\CoreLibs\NiMain\NiNode.cpp` | 33897 | 38c7a1de1e166345068d296f70f34b1adae27c694e19ead8fa0fbd8b62e0e016 | AttachChild L52-72; DetachChildAt L74-90; DetachChild L92-106; SetAt L108-130; UpdateDownwardPass L228-276; UpdateSelectedDownwardPass L278-328; UpdateRigidDownwardPass L330-364; UpdateUpwardPass L379-392; UpdateWorldBound L394-407 |
| F7 | `Gb12_Source\CoreLibs\NiMain\NiTexturingProperty.cpp` | 32194 | 2bc36c08e8b9e0ab624569ff098f1cd60b8242b737c0eb7b3e4dd3a6615ba106 | map slots L61-97; SetMultiTexture L99-115; SetMap/SetDecalMap L117-151; LoadBinary L238-349; LinkObject L351-387; Map::LoadBinary L838-867; Map::SaveBinary L869-887 |
| F8 | `Gb12_Source\CoreLibs\NiMain\NiSourceTexture.cpp` | 14704 | b5d0bb026b812ca4d022e110d7cfe0b98eca181c06f78c62a999512c0927e70e | Create L35-81; LoadBinary L162-314 (external/pixel-data + palette dedup via ChangeObject); LinkObject L316-322; PostLinkObject L324-338 |
| F9 | `Gb12_Source\CoreLibs\NiMain\NiGeometry.cpp` | 14679 | fde29a81fbd5b7f8df34320dcf9dc91fe32d7d9f2e6e5f70b30b976953eaf335 | SetModelData L80-93; UpdateWorldBound L100-110; UpdatePropertiesDownward L112-115; CopyMembers L275-280; LoadBinary/LinkObject L351-393 (whole file) |
| F10 | `Gb12_Source\Samples\Tutorials\04 - Scene Attachment\SceneAttachment.cpp` | 4140 | 8b2ec4feddff58f0a0a807e2fe20bf976b79539d590d283e46c5a93e071b9ee9 | CreateScene L37-96 (world NIF + object NIF + AttachChild at named node); whole file |
| F11 | `Gb12_Source\Samples\Demos\BackgroundLoad\BackgroundLoad.cpp` | 5746 | 8287a6aecb058d71978c7c6a1f3db382447c764b15cfae082078615d152475b1 | CreateScene L49-78; OnIdle L91-143; Terminate L145-151 (whole file) |
| F12 | `Gb12_Source\Samples\Demos\BackgroundLoad\BackgroundLoad.h` | 1051 | 9a0c21c245fac886d31bc9506bc6ff37284f72038eb47d6e1c470389972b2b74 | class shape (whole file) |
| F13 | `Gb12_Source\Samples\Demos\BackgroundLoad\CallbackStream.cpp` | 3740 | 6c4a299891268f39f5a9965892c57444a235e59f9cdb1136b7d5755a488d1659 | BackgroundLoadOnExit L23-48; Precache L51-121 (whole file) |
| F14 | `Gb12_Source\Samples\Demos\BackgroundLoad\CallbackStream.h` | 787 | bae28ef033fd0eb179851ebd604e4ead6c1168f84eef3d445517629af80c033a | class shape (whole file) |
| F15 | `Gb12_Source\Samples\ST_Applications\MOUT\TerrainManager.cpp` | 7148 | cdad77bab6e448ac36cb88a3df5867cda8f9e30a1d8d874d76b4fed34abac63e | Initialize L38-59; GetHeight L66-81; GetHeightAndNormal L83-106; TransformModelToWorldInPlace L125-156; TransformPointsBasicInPlace L158-187 (whole file) |
| F16 | `Gb12_Source\Samples\ST_Applications\MOUT\TerrainManager.h` | 2314 | d9ead2d207bd7478bc5c91fce1b0753682bc8c53496c6dee8e9fe65773e75089 | class shape (whole file) |
| F17 | `Gb12_Source\Samples\ST_Applications\MOUT\TerrainManager.inl` | 731 | 628c353cdc5685bc2ee72ac50dae6753dfcfae11eae945b210b3f675236535b1 | inline accessors (whole file) |
| F18 | `Gb12_Source\Samples\ST_Applications\MOUT\WorldManager.cpp` | 27057 | e9eb4f45b4036e0ed29afb63e9f9aabdfbf1dabb7dbc96589607c993abd60c59 | LoadWorld L150-258; OpenNif L562-573; OpenNifAndPrepack L575-587; RecursivePrepack L589-645 |
| F19 | `Gb26_src\NiExternalAssetNIFHandler.cpp` | 12796 | 38e13c8a46e491784e4f6679efb0601587e0cbd75d68498d86568dcc76130580 | LoadAll/Load L98-153; LoadNIFFile L155-200; Retrieve L202-256; Unload L258-313; UnloadAllUnusedAssets L315-388 (whole file) |
| F20 | `Gb26_src\NiExternalAssetNIFHandler.h` | 3058 | 8d98263391100ca455c271f60b408c8f0a3dd26558fb0e47deded9c1d1101851 | class shape (whole file) |
| F21 | `Gb12_Source\CoreLibs\NiSystem\NiVersion.h` | (small) | not separately hashed — two `#define` lines quoted verbatim | version constants only |
| F22 | `Gb112_docs_html\Reference\CoreLibs\NiMain\Main_Class_Reference\NiTexturingProperty_Map.htm` | 8749 | e1ae44e2ecaf92ee44dded9dcfcb8cf8b1c3c40b2f11c7224a4879f3cd2e9a7a | Map semantics (texture + filter + clamp + texcoord index; UV sets on NiGeometryData) |
| F23 | `Gb112_docs_html\Reference\CoreLibs\NiMain\Main_Class_Reference\NiStream.htm` | 24006 | c197a1d3cd4c42b436ca357419f8008f45e1d7d19338e12bd23ab9a5753935ae | located + skimmed (API list; primary evidence remains the sources F1-F20) |

Scope discipline held: no whole-SDK read, no new atlas, no new EXE RE (0 native
executions this phase — see INTERVENTION_LEDGER).

---

## 2. Mechanism 1 — Stream / register / load / link + custom NiArk handling

**SOURCE**: F1 `NiStream.cpp` (Gamebryo 1.x, SHA e955c36e…) + F21 `NiVersion.h`.

**OBSERVED SDK BEHAVIOR** (from source, lines cited per file table):
1. `NiStream::LoadStream` (L506-635) is a fixed pipeline: `LoadHeader` → (NIF ≥
   5.0.0.1) `LoadRTTI` → (≥ 5.0.0.6) `LoadObjectGroups` → per-object `LoadBinary`
   loop → `LoadTopLevelObjects` → `LinkObject` loop → `PostLinkObject` loop →
   registered post-process functions → `SetSelectiveUpdateFlagsForOldVersions`
   → `FreeLoadData`.
2. `LoadHeader` (L303-360) rejects: not-"File Format" line; version < min ("too
   old") or > max ("Unknown NIF version") — the max is the SDK's own version.
3. `LoadRTTI` (L412-449) reads a `usRTTICount` type-name table and looks each
   name up in the static `ms_pkLoaders` registry (populated by `RegisterLoader`,
   L755-766). A missing entry → `RTTIError` (L387-400): error `NO_CREATE_FUNCTION`,
   message "`<ClassName>: cannot find create function.`" and the LOAD FAILS.
4. Linking: `ReadLinkID` stores link IDs during `LoadBinary`; `LinkObject` resolves
   them (`GetObjectFromLinkID`); ≥ 5.0.0.1 `ResolveLinkID` resolves immediately.
5. Texture palette dedup exists INSIDE the stream: `NiSourceTexture::LoadBinary`
   may replace the just-created object with a shared one via `ChangeObject`
   (F8 L215-275).

**PE EVIDENCE OR GAP** (all from prior executed runs, cited):
- Measured (PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1 + sceneir
  lineage): stock GB 1.2.2 tools REJECT PE NIF-10.1 content with the generic
  "Error loading stream."; a helper observed the specific
  "`NiArkAnimationExtraData: cannot find create function.`" — which is EXACTLY
  the `RTTIError` text of F1 L387-400 (two separate evidence layers).
- Corpus-proven: ALL 4,838 NIF-10.1 entries in PCG Models.bnt declare `NiArk*`
  blocks → NO stock-only reader can load them. The stock rejection is a REGISTRY
  GAP (no registered NiArk CreateFunctions in stock libs), NOT corruption and NOT
  permission to skip custom blocks.
- GAP: PE's own registration of NiArk factories (the client-side `RegisterLoader`
  equivalents) is NOT recovered — we do not know which NiArk semantics the
  original engine attached.

**ADAPTER DECISION**: byte-range reading of the pinned containers + our own IR
(`src/pecompat/PecNif10Reader → PecSceneIR`); NO fabricated NiArk factories; NO
SDK loader invocation for PE assets (loud version gate, OPAQUE custom blocks
preserved). This is the executed 218757 lineage — REUSED, not re-derived.

**CONTROL**:
- EXECUTED (prior runs, cited): stock printer positive/negative battery (16
  native executions; capability matrix with preserved FAILs) + 218757 adapter
  battery (14/14 NiTriShape↔NiTriShapeData associations with recomputed
  fingerprints). See the sceneir run package.
- PLANNED (Etap E): regression battery through `PecNif10Reader` when the
  launcher consumes vegetation model IDs; unsupported models surface explicit
  counts/status, never silent skips.

---

## 3. Mechanism 2 — Local/world transforms + hierarchy

**SOURCE**: F3 `NiTransform.inl`, F2 `NiAVObject_Win32.cpp`, F4 `NiAVObject.inl`,
F5 `NiAVObject.cpp`, F6 `NiNode.cpp`.

**OBSERVED SDK BEHAVIOR**:
1. Composition law (F2 L22-31): `m_kWorld = parent->m_kWorld * m_kLocal`, else
   root `m_kWorld = m_kLocal`. Transform product (F3 L15-24):
   `s = s1·s2; R = R1·R2; t = t1 + s1·(R1·t2)`; point (F3 L26-29):
   `p → (R·p)·s + t`.
2. LAZY setters (F4 L82-143): `SetTranslate/SetRotate/SetScale` write **m_kLocal
   ONLY** — no world recompute, no parent notification. World is recomputed on
   demand in `Update()`/`UpdateDownwardPass()` (`UpdateWorldData`); world-only
   setters exist separately (F4 L145-158). Bounds merge upward in the same pass
   (F6 L228-276, L379-392).
3. `AttachChild` (F6 L52-72): refcount guard → `AttachParent` (which detaches the
   old parent first, F5 L62-69) → array add. **NO local-transform compensation**
   — the child's world position changes purely by composition. Same for `SetAt`
   (F6 L108-130) and `DetachChild*` (F6 L74-106).

**PE EVIDENCE OR GAP**: the SAME contracts are ALREADY implemented and verified
in `src/pecompat` (PecTransform/PecSceneIR): composition law reproduced against
NATIVE controls (probe world bound centers (96,202,306)/(58,221,363), tolerance
1e-4, both IR math and THREE.Matrix4 independent); reparenting-no-compensation
is a MEASURED native trait. This phase REUSES that — nothing re-derived blindly.
GAP: PE's own per-root transform application during load remains NOT traced
(that is a PE-side question, not an SDK one).

**ADAPTER DECISION**: reuse `PecSceneIR`/`PecTransform` + the viewer instance
wrapper policy for any NIF-sourced objects in the launcher world; the TERRAIN
world grid is a SEPARATE documented convention (`PETerrainRegion`: +X = grid x
meters, +Y = height meters, +Z = grid y south; `PE_TERRAIN_METER_PER_SAMPLE = 2`
labeled CURRENT_RUNTIME_CALIBRATION) — never conflated with NIF scene space.

**CONTROL**:
- EXECUTED (prior): synthetic control-graph battery T1-T6 (sceneir run),
  including world-vs-local hierarchy checks and the no-compensation trait.
- PLANNED (Etap E + §8): the launcher scene battery repeats the same control
  class (local/world hierarchy on a synthetic control graph; shared resource
  with two different transforms; conversion applied exactly once).

---

## 4. Mechanism 3 — Textures / UV / material bindings

**SOURCE**: F7 `NiTexturingProperty.cpp`, F8 `NiSourceTexture.cpp`,
F9 `NiGeometry.cpp` (property-state push L112-115), F22 (docs: Map semantics),
F1 (palette/ChangeObject context).

**OBSERVED SDK BEHAVIOR**:
1. `NiTexturingProperty` holds a map ARRAY with fixed slots (F7 L61-97): BASE,
   DARK, DETAIL, GLOSS, GLOW, BUMP, then DECAL_BASE+ (m_uiDecals), plus ShaderMaps
   (≥ 5.0.0.17). Each `Map` = {texture link, clamp enum, filter enum, texCoord
   index, PS2 L/K, optional NiTextureTransform (≥ 10.0.1.10)} (F7 L838-867).
   Per F22: the Map references a TEXTURE-COORDINATE SET INDEX — the UV sets
   themselves live on NiGeometryData, not in the property.
2. `LoadBinary` (F7 L238-349) reads per-slot has-map flags + the Map bodies;
   `LinkObject` (F7 L351-387) binds textures from link IDs.
3. `NiSourceTexture` (F8): filename-keyed sharing through the stream texture
   palette (`ChangeObject` dedup); renderer data created in `PostLinkObject`
   (L324-338) — AFTER all links; image reading itself is delegated to the
   NiImageConverter subsystem (outside the NIF stream).

**PE EVIDENCE OR GAP**:
- MODELS (catalog + sceneir runs, measured): the four CD_2003 primaries carry
  `NiArkTextureExtraData` (numTex=0) and the stock NiTexturingProperty chain is
  ENTIRELY ABSENT; PCG_9_3_5 batch: 3,357 ArkTexture name edges ALL
  NAME_NOT_FOUND (the same-era Textures.bnt is numeric-named `<id>.dat`);
  218757: 9 TEXTURE_NAME_BOUND / 5 UNTEXTURED_NO_TEXPROP; container resolution
  NOT_ESTABLISHED; per-entry 9-byte Ark tail semantics UNRESOLVED.
- TERRAIN (the launcher's Etap D chain) is NOT a NIF property chain at all:
  `PESourceMount.getTerrainMaterials` → `TdfMaterialTailDecoder` (named records:
  mask @ record+56, fields 52..55 = extra4, NOT mask; raw/RLE; independent
  weights; sums>255 = original data, never renormalized) → material id/name →
  **texture entry relation** → PCG Textures.bnt payload → `TgaDecoder` → GPU
  sampler. GAP (contract §5, pinned): `materialId == textureId` is **NOT
  established** — a mapping table needs provenance+version, or the launcher
  must show an explicit unresolved-binding diagnostic (never a random green
  texture).
- GAP: the PE-side blend/UV-repeat convention for terrain is NOT evidenced;
  the Stone04-base + independent-alpha-overlay model is the data-supported
  candidate (JUL-era forensics, era-labeled) to re-validate on PCG samples.

**ADAPTER DECISION**: for the launcher's terrain textures follow the TDF chain
(never NIF property semantics); decode with the qualified TGA subsets
(`decodeTga2` 24bpp terrain textures — iter011 corpus-wide; `decodeTga2A32*`
32bpp climate-palette/model subsets with their documented file-row vs image-row
conventions); blend/UV = an explicitly labeled RENDER_RECONSTRUCTION preset;
wrong-era texture resolution REFUSED via PESourceMount era discipline.

**CONTROL**:
- EXECUTED (prior, cited): TGA decoder qualification (iter011/027/030);
  iter020 material audit with an INDEPENDENT second parser + JUL oracle + era
  byte-identity census.
- PLANNED (Etap D, contract §8): mask offset 56 verified on the used samples;
  malformed/RLE fail-loud; raw weights unchanged; explicit unresolved binding
  state; wrong-era texture refusal; UV/flip controlled with a real texture;
  resolved/decoded/applied/browser-observed reported SEPARATELY.

---

## 5. Mechanism 4 — Shared geometry + separate instances

**SOURCE**: F9 `NiGeometry.cpp`, F19 `NiExternalAssetNIFHandler.cpp` (Gb26 —
later-generation comparison ONLY), F10 `SceneAttachment.cpp` (attach sample).

**OBSERVED SDK BEHAVIOR**:
1. `NiGeometry` HOLDS its mesh by smart pointer (`m_spModelData`); `SetModelData`
   (F9 L80-93) is a pointer swap; streaming links it by ID (F9 L384-393).
2. SDK CLONES SHARE geometry: `NiGeometry::CopyMembers` (F9 L275-280) passes the
   SAME `m_spModelData` to the clone — separate NiAVObject/transforms, shared
   NiGeometryData.
3. Gb26 `NiExternalAssetNIFHandler` (F19): `LoadNIFFile` (L155-200) stores the
   loaded root as the PRISTINE original; `Retrieve` (L202-256) returns either the
   pristine root (first user) or a `NiCloningProcess` COPY_EXACT clone recorded
   in a per-asset clone set; `UnloadAllUnusedAssets` (L315-388) removes clones
   by refcount and unloads assets whose pristine root is no longer externally
   referenced. This is the DEFINITION-vs-INSTANCE separation, generation 2.6.
4. `SceneAttachment` (F10): the load-attach pattern — root = `GetObjectAt(0)`,
   `AttachChild` at a NAMED node.

**PE EVIDENCE OR GAP**: PE-side instance streaming/clone policy is NOT recovered
(this is a PE question; the SDK files only bound what the engine's library COULD
do). The launcher vegetation plan (contract §6) needs exactly the separation
above: ORIGINAL_CLIMATE_RECORDS (.vcl) + RECOVERED_RNG_ARITHMETIC (PEFoliageCore,
byte-locked) + INSTANCE_DISTRIBUTION (reconstruction-only). The 218757 lineage
already implements resource-identity vs instance-identity (VIEWER_INSTANCE_WRAPPER
_POLICY: geometry shared, transforms/instance IDs not; authored instanceId).

**ADAPTER DECISION**: vegetation = decode each model ID ONCE (shared geometry
resource); instances = separate objects with own transforms + instance keys
(edge ownership prevents duplicates on tile borders and camera returns);
`Shared geometry is NOT shared instance` (contract §6.5); the single-witness
`NifModelReader.js` (457485) is NEVER widened without its witness regression —
Etap E uses the qualified importers or a narrowly-added format WITH controls.

**CONTROL**:
- EXECUTED (prior): 218757 battery (resource/instance separation; shared
  BufferGeometry per NiTriShapeData).
- PLANNED (Etap E, contract §8): repeat-seed → identical instance-set hash;
  changed seed → different position hash; tile-load order independence; no
  duplicate instances; 5000-visible-instance cap enforced + requested/rendered/
  limited counts; unload/reload without doubling or destroying shared resources.

---

## 6. Mechanism 5 — Scene load/unload management

**SOURCE**: F11-F14 `BackgroundLoad` demo, F15-F18 MOUT app.

**OBSERVED SDK BEHAVIOR**:
1. BackgroundLoad (F11): synchronous load of the core scene, then
   `BackgroundLoadBegin(file)` for a secondary NIF; the main loop POLLS
   `BackgroundLoadPoll(LoadState)` showing read%/link% progress and attaches
   the loaded root to the scene only when the status returns IDLE (L91-143);
   `Terminate` explicitly `BackgroundLoadFinish` + `RemoveAllObjects` (L145-151).
2. CallbackStream (F13): the `BackgroundLoadOnExit` override performs renderer
   preparation (UpdateProperties/UpdateEffects/Precache with STATIC consistency)
   IN THE LOADING THREAD, so the main thread does not stall (L23-121). The SDK's
   own progress model separates READ phase from LINK phase (F1 L724-739).
3. MOUT TerrainManager (F15): ground height via `NiPick` raycast
   (FIND_FIRST + TRIANGLE_INTERSECT + MODEL_COORDINATES after an IN-PLACE
   world bake of the pick-graph vertices, L125-187); the pick graph is NOT
   rendered. WorldManager (F18): ONE whole-world NIF + named node lookups
   ("buildings", "start", "lights"); `OpenNif` = `NiStream::Load` +
   `GetObjectAt(0)`; `RecursivePrepack` sets STATIC consistency + PrecacheGeometry.
   **NO tile streaming exists anywhere in these samples.**

**PE EVIDENCE OR GAP**: PE's own terrain streaming design is NOT established —
MOUT/BackgroundLoad are OTHER APPS' examples (contract §3: "Sample MOUT is an
example of another application, not proof of Entropia's terrain format"). The
launcher's tile streaming (Etap C: ≤64 active tiles around the camera,
controlled memory, NODATA stops movement/shows boundary) is an ADAPTER DESIGN
that borrows only the PATTERN (phase-separated load with progress + deferred
renderer prep + explicit cleanup + loud failure), never a claim about PE.

**ADAPTER DECISION**: reuse `PETerrainRegion` (disjoint NxN tile assembly, seam
differences recorded as ORIGINAL_DATA, no repair) + a NEW bounded tile-stream
component (Etap C); height sampling for the walk controller comes from the SAME
terrain data (contract §7); data gaps = stop/boundary, never void-drop.

**CONTROL**:
- EXECUTED (prior): terrain clean-path gates (iter019 era validation on
  terrain.bnt; PETerrainRegion seam diagnostic; p0.js end-to-end region render
  with per-tile height SHA256 byte-faithfulness export).
- PLANNED (Etap C, contract §8): offset 64-vs-52 negative control; exact 1024
  raw heights per tile; sentinel/NODATA handling; reversed tile-load order
  stability; source bytes unmodified; borders/calibration; conversion applied
  exactly once; several physical samples re-read by an INDEPENDENT byte reader.

---

## 7. Cross-mechanism standing summary

| Mechanism | SDK source (SHA256 prefix) | PE evidence | Reuse vs new | Controls |
|---|---|---|---|---|
| 1 stream/link/NiArk | NiStream.cpp e955c3… | stock rejection measured; 4838/4838 NiArk | REUSE PecNif10Reader→SceneIR | executed (prior) + planned Etap E |
| 2 transforms/hierarchy | NiTransform.inl 92e8ac…, NiAVObject_Win32.cpp 75e452…, NiNode.cpp 38c7a1… | native-verified composition law | REUSE PecTransform/PecSceneIR | executed (prior) + planned §8 |
| 3 textures/UV/material | NiTexturingProperty.cpp 2bc36c…, NiSourceTexture.cpp b5d0bb…, NiGeometry.cpp fde29a… | Ark chains measured; terrain = TDF chain | REUSE TdfMaterialTailDecoder + TgaDecoder; NEW terrain-texture binding | planned Etap D (subset executed prior) |
| 4 shared geo/instances | NiGeometry.cpp fde29a…, Gb26 NiExternalAssetNIFHandler.cpp 38e13c… | PE policy not recovered (gap) | REUSE resource/instance contract; NEW vegetation wrapper | executed (prior) + planned Etap E |
| 5 load/unload mgmt | BackgroundLoad.cpp 8287a6…, MOUT TerrainManager.cpp cdad77…, WorldManager.cpp e9eb4f… | PE streaming NOT established (examples only) | REUSE PETerrainRegion; NEW tile-stream design | executed (prior, terrain gates) + planned Etap C |

**Standing honesty**: No mechanism here converts SDK behavior into a PE fact.
Every PE claim above cites its measured prior evidence; every gap is named; the
MOUT/BackgroundLoad/SceneAttachment samples are bounded as other apps' patterns.
No SDK sources/docs/binaries are copied into this repository.
