# IMPLEMENTATION_NOTES — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

Phase: IR_ADAPTER_UNIT_TESTS (SceneIR + PE adapter for 218757 + transform/
instance/association tests). Written after implementation; every reuse is
labeled and every boundary assumption is listed with its evidence.

## 1. What was implemented where

### src/pecompat/ (all NEW code; src/pesource/ untouched — witness verified)

| File | Bytes | Role |
|---|---|---|
| `PecTransform.js` | 6,426 | GB-contract transform math (world = parentWorld*local; s=ps*ls, R=pr*lr, t=pt+ps*(pr*lt); point=(R*p)*s+t), TRS↔column-major 4x4, tolerance compares, deep-equality proofs. Pure module (no THREE import). |
| `PecSceneIR.js` | 19,829 | The SceneIR: ASSET (era/build, container/entry/hash, block IDs, supported types, per-block decode status, source links, closure), NODE (serialized local TRS + bit-hex trace, children, SEPARATE resource/property/extra-data links), DIAGNOSTICS (opaque counts, unresolved bindings, unsupported features, NULL-child-slot notes), COMPUTED STATE (FILE_SCENE_SPACE world transforms per node, scene bounds — distinct from the instance scene transform and the render transform). Validation: cycles REJECTED, dangling REQUIRED links REJECTED, multi-parent REPORTED with the full claim list (never silently selected), footer top-objects as root authority with unclaimed-scene-block cross-check. Cache key = assetId:payloadSha256:adapterVersion:schemaVersion. Synthetic IR builder for authored tests. |
| `PecNif10Reader.js` | 37,483 | The EXTENDED NIF 10.1.0.0 reader (version gate exact, loud otherwise). Full closure contract: all blocks + TopObjects footer + EOF-exact, else LOUD. Boundary-search backtracking for variable-ext blocks with every decision recorded. Fingerprint helper (decoded-array SHA over exact serialized f32-LE vertices / u16-LE indices + byte-range round-trip proof). |
| `PecAssetAdapter.js` | 11,515 | Pinned Models.bnt → BNT2 index-derived extraction → container+payload SHA fail-closed pins (ordinal/offset/size cross-checks) → reader → SceneIR → fingerprints → texture binding resolution (names/property refs only) → validation/composition/bounds. Regenerates from the original container every load (no stale JSON). |
| `PecInstanceBuilder.js` | 10,501 | Authored instances: unique IDs (duplicates REJECTED), shared asset, wrapper-owned scene transform (VIEWER_INSTANCE_WRAPPER_POLICY labeled as NOT a reproduction of SDK 2.6 root-replacement branches or the PE placement mechanism), lazy local setter semantics, SetAt-style reparenting with NO compensation, attachment dependencies RECORDED but NOT auto-applied (separate from scene parents — no double application), scene-parent cycle rejection, missing-master/dangling-parent rejection, multi-parent rejection with report. |
| `PecRenderConvert.js` | 11,910 | THREE r185 conversion (THREE injected by the caller — see §3): render-axis/unit choice (x,z,-y)×0.01 labeled RENDER_ADAPTER_CHOICE / PE_UNITS_NOT_CONFIRMED, applied EXACTLY ONCE as a single matrix at the render-space root (counter-instrumentable); THREE tree composes serialized local TRS in scene space; shared BufferGeometry via caller-owned cache; plain LABELED materials only (no texture bytes bound in this run); bounds conversion via corner mapping through the SAME single law. |

### tools/pecompat/
- `extract_218757.mjs` — extraction identity print (container/payload pins + cross-checks); exit 1 on mismatch.
- `sceneir_dump.mjs` — SceneIR build + bounded diagnostics dump (NO payloads; block list with byte ranges + decode statuses, mesh associations with recomputed fingerprints, texture binding census, bounds, closure decisions); `--emit-file-scene-space` writes the bounded transform artifact.
- `controlB_compare.mjs` — fixture → reader → composed camera world translate vs native expected, tolerance-based full-vector compare.

### tests/pecompat/ (zero new dependencies; three 0.185.0 from the existing canonical checkout node_modules, version pin asserted)
- `run_tests.mjs` — harness; per-control MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED; `--models` enables the pinned-container tests, otherwise they report NOT_PERFORMED_CONTAINER_UNAVAILABLE loudly (negative control executed: 17 PASS / 1 NOT_PERFORMED, no silent skip).
- `transform_composition.test.mjs` — T1 (both Control B fixtures: IR + THREE dual-engine composition vs native values) + T2 (nonidentity root, parent rotate/scale/translate, reparent-without-compensation, conversion-applied-exactly-once with structural counter + double-conversion negative control + IR-intactness proof + THREE/IR full-matrix agreement).
- `instance_separation.test.mjs` — T3 (two instances: BufferGeometry object identity shared, underlying array identity, wrapper separation, mutation of A leaves B exactly unchanged, asset IR unmutated).
- `invalid_links.test.mjs` — T4 part 1 (cycle, dangling child, dangling model-data ref, multi-parent REPORT with both parents + composition refusal, missing master, dangling scene parent, duplicate instanceId, instance scene cycle).
- `missing_texture.test.mjs` — T4 part 2 (bound/no-entry/no-prop/material-only-ref cases; labeled untextured + diagnostic; no false binding; container NOT_ESTABLISHED everywhere).
- `model_218757.test.mjs` — T5 (extraction identity, census + 62+4 accounting, 14/14 associations + 28/28 fingerprints vs predecessor, hierarchy + closure decisions, bounds vs predecessor extents, texture binding census + ArkTexture entry-list comparison, FILE_SCENE_SPACE artifact).
- `witness_457485_regression.test.mjs` — T6 (working-tree SHA256 of src/pesource/NifModelReader.js vs the BASE blob + src/pesource/ cleanliness; WITNESS_UNTOUCHED).
- `_helpers.mjs` — shared test helpers (fixture paths/pins, three resolution, synthetic TRS conveniences).

## 2. Reuse labels (contract §7 — the documented parser lineage, labeled)

1. **BNT2 extraction chain**: `src/pesource/Bnt2Archive.js` is IMPORTED and used
   for the index-derived extraction (era-validated framing: footer magic,
   0x0A-terminated names, size/offset/crc32/pad). This is the base repo's
   existing extraction chain; it is NOT modified.
2. **NifStream conventions** (header line, u32 version gate, per-block u32==0
   preamble, SizedStrings, 1-byte v10 booleans, file-order f32 bit-hex, loud
   fail-closed unknown types): adopted from the documented conventions of
   `src/pesource/NifModelReader.js` (the R61 lineage). That reader itself is
   NOT imported, NOT modified; its first-mesh path does NOT support 218757 and
   is not pretended otherwise.
3. **218757-corpus field layouts** from the predecessor's s2 Rosetta-lineage
   parser (committed in the worktree BASE at
   `docs/audits/PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009/TOOLS/s2_parse_nif101_r1.py`,
   READ as reference): NiDirectionalLight (net+av+affected+dimmer+ambient/
   diffuse/specular — 218757 has 2 such blocks, absent from the witness
   reader's type set), NiTexturingProperty HIST 0.7.1.1 slot order
   (Base..Decal0 + conditionals, bump luma/matrix only when Has Bump),
   NiArkTextureExtraData entry-list layout (count=(field2>>8)&0xFFFFFF),
   the closure-constrained boundary candidate method (next-block preamble
   shapes + TopObjects footer shapes, (rank,pos) ordered), and the
   TopObjects footer + EOF-exact closure contract.
4. **Predecessor measurement files** (RELATION_RESULTS fingerprints,
   SCENE_STRUCTURE census/hierarchy/bounds/ArkTexture entries, q5 census) are
   used ONLY as independent COMPARISON evidence in tests — never as inputs;
   every value the adapter emits is derived from the pinned bytes.

## 3. Boundary assumptions (all closure-verified per file, decisions recorded)

- **NiArkTextureExtraData layout variants**: the 218757 corpus lineage reads
  `name SS` first; the 457485 witness lineage reads 3 raw bytes first. MY
  reader tries NOPREFIX then PREFIX3 as backtracking variants and records the
  chosen variant. FINDING (measured this phase): for 218757 the pair
  (importer-tail 38B + ArkTexture PREFIX3) is BYTE-EQUIVALENT to
  (41B + NOPREFIX) — the "3 prefix bytes" are the 41B tail's trailing
  00 00 00. Both attributions consume identical absolute bytes (all fields
  land at identical offsets; texture names/refs verified). The documented
  sizes are seeded FIRST so the corpus-documented attribution
  (41B + NOPREFIX, matching the predecessor's measurements) is chosen;
  the alternative is recorded in the decision log if the seeds fail.
- **NiArkImporterExtraData tail**: not a documented fixed size across the two
  lineages (41B corpus vs 38B witness); derived by closure with both
  documented sizes seeded first. 218757 measured 41B (matches predecessor).
- **NiArkAnimationExtraData / NiArkViewportInfoExtraData**: name + RAW ext to
  the closure-derived boundary (16B / 49B measured — both match the
  predecessor); content UNDETERMINED, never interpreted.
- **NiTriShapeData UV-set info bytes**: read as numUvSetsLo u8 +
  extraVectorsFlags u8 (s2 labels) with the witness lineage's tangent trigger
  (extraVectorsFlags & 0xF0, a superset of s2's & 0x10) and the raw u16 also
  recorded. 218757 measured extraVectorsFlags == 0 (no tangents anywhere).
- **NiTexturingProperty slots**: textureCount==7 for 218757 (7 base slots;
  no shader textures — loud fail otherwise). Both lineages consume identical
  bytes at tc==7.
- **NiVertexColorProperty**: witness/R61 convention (not present in this run's
  inputs).
- **Roots**: the TopObjects footer is the authority; unclaimed scene blocks
  (AV types not claimed as a child) are the fallback and cross-check
  (agree: true for 218757 and both fixtures).
- **NULL (-1) child slots are LEGAL** NIF null links (measured: block 0
  carries 19 of them alongside 12 real children — matching the predecessor's
  blockmap); recorded as diagnostics, skipped in composition, NOT errors.
- **NiCamera** (Control B fixtures only): net+av decoded (the probe TRS);
  frustum/viewport fields recorded RAW to the closure boundary — NOT decoded
  in this run (out of scope; the probe quantity is the TRS).

## 4. Honest deviations from the plan (all within the allowlist)

1. **THREE injected, not imported**: `PecRenderConvert.buildRenderModel(THREE,
   ...)` takes the three module as its first argument instead of a static
   `import * as THREE from 'three'`. Reason: the worktree carries no
   node_modules and no new dependencies were allowed; tests/tools resolve
   three 0.185.0 from the EXISTING canonical checkout
   (`eudoria-clean/node_modules`, version pin asserted at load), and the app
   phase will inject its importmap-resolved module. Same file, same purpose
   as planned — only the wiring differs. The render conversion itself is
   pure and testable without THREE.
2. **tests/pecompat/_helpers.mjs** added (shared fixture paths/pins, three
   resolution, synthetic TRS conveniences). All seven planned test files
   exist with the planned names; the helper is an implementation detail
   inside the allowed `tests/pecompat/` area.
3. **Test numbering mapping** (dispatch T1–T6 over the plan's T1–T8 classes):
   dispatch T1 = harness T1_*; T2 = T2a–T2d (+ plan reparenting class);
   T3 = T3; T4 = T4a–T4h + T4b_missing_texture; T5 = T5a–T5g; T6 =
   T6_witness_457485_untouched. TEST_RESULTS_UNIT.json carries both keys.
4. **FILE_SCENE_SPACE artifact location**: emitted to
   `raw/FILE_SCENE_SPACE_TRANSFORMS_218757.json` (bounded: 66 entries of
   index/type/name/decodeStatus/localTrs/worldTrs ONLY — verified to contain
   no positions/indices arrays; the same transform class the predecessor
   published in SCENE_STRUCTURE_RESULTS.json).
5. **A real bug found and fixed during testing** (honest record): the first
   implementation of `PecRenderConvert.conversionMatrix` produced z'=-u*x
   instead of z'=-u*y. The T2d conversion-once test caught it by disagreeing
   with the independent analytic value
   (THREE world (0.04,0.09,-0.04) vs analytic (0.04,0.09,-0.03)); the matrix
   row was corrected and the full suite re-run green. The failure was
   preserved in the first run's console output before the fix.

## 5. Decode ceiling preserved (contract §1)

66 accounted blocks = 62 SUPPORTED + 4 Ark blocks per ACTUAL field coverage:
- `NiArkTextureExtraData` (block 3): PARTIALLY_UNDERSTOOD (documented entry
  list decoded: 18 entries with names/f1/f2/texprop refs; per-entry 9-byte
  tails recorded RAW — semantics UNRESOLVED for 218757; NO textureId
  interpretation in this run; the 'BNT2 id' reading stays a RETRACTED prior
  claim for this model).
- `NiArkImporterExtraData` (block 2): PARTIALLY_UNDERSTOOD (name/int/version
  string decoded; 41B tail raw).
- `NiArkAnimationExtraData` (block 1): OPAQUE (name + 16B raw ext).
- `NiArkViewportInfoExtraData` (block 13): OPAQUE (name + 49B raw ext).
No silent Ark semantic decodes; the IR records `opaqueBlockCount: 4`.

## 6. Texture binding status (this phase's measured truth)

- 18 ArkTexture entries re-derived from bytes; entry names/f1/f2/texprop
  refs/9B-tail hex all match the predecessor's independent parse exactly.
- 9 meshes TEXTURE_NAME_BOUND (each 2 names: part BASE + DARK slots via
  texprops 4–12); 5 dPVS_occ meshes UNTEXTURED_NO_TEXPROP (material-only
  refs — matching the reference; NO false binding).
- Container resolution: NOT_ESTABLISHED everywhere (name/property bindings
  only; RESOURCE_NAME_REFERENCES_ONLY; no texture bytes resolved; no
  cross-era substitutions; geometry viewable with labeled plain materials).

## 7. Commands (this phase)

- `node tests/pecompat/run_tests.mjs --models "D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt" --json-out <path> --artifact-out <path>` — the full suite (24 PASS / 0 FAIL / 0 NOT_PERFORMED with --models; 17 PASS / 1 NOT_PERFORMED loud negative control without).
- `node tools/pecompat/extract_218757.mjs` — extraction identity (exit 0).
- `node tools/pecompat/sceneir_dump.mjs --models <Models.bnt> --json <path>` — bounded dump (exit 0).
- `node tools/pecompat/controlB_compare.mjs <fixture.nif> <x,y,z>` — PASS (maxDiff 0 for both fixtures).

No server, no browser execution, no commit/push in this phase (final
persistence phase later, per the dispatch).
