# FINAL_REPORT — PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009

**STATUS LABEL: FINAL** — the complete report for the WHOLE run (Packages
A+B+C). Fresh internal QC (pe-master-auditor fresh session; FRESH_INTERNAL_QC,
internal to PE-MASTER — NOT an independent Desktop post-audit) = **PASS_WITH_
FINDINGS** (0 P0, 0 P1, 6 P2, 4 P3; the five §9 SHA transcription defects are
corrected at this persistence finalization; the P2-6 COUNTERMODEL JSON repair
is adjudicated REPAIR_ACCEPTED by PE-MASTER). PE-MASTER verdict = **MASTER_
ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT =
NONE)**. DESKTOP_POST_AUDIT = PENDING. Publication (commit/push,
AUDIT_ENTRYPOINT row, final manifest) is executed by the separately-authorized
persistence phase; this finalization is part of that phase (summary: section
11).

## 0. Human-decision block (read this first)

1. The three work packages of the human-authorized run are executed to their
   bounded ends: (A) the three f99febe record defects are corrected with
   explicit supersessions and 5/5 countermodels reproduced; (B) the stock
   Gamebryo 1.2.2 SceneGraphPrinter is qualified headlessly on SDK/synthetic
   controls (gate PASS with scope; specificity FAIL preserved honestly);
   (C) the qualified methods were applied to the pinned PE container: a full
   metadata census (5,596 indexed NIF entries), a frozen mechanical selection
   (4 of max 5 deep inputs), native execution of every selected PE input on
   the stock printer, the ONE disclosed helper, the parser/native comparison,
   typed scene-structure analysis and the bounded 218757 comparison.
2. **The single most important measured result:** EVERY one of the 4,838
   NIF 10.1.0.0 files in the pinned Models.bnt declares at least one NiArk*
   class in its type table (NiArkTextureExtraData, NiArkAnimationExtraData and
   NiArkImporterExtraData are declared by ALL 4,838), and the stock GB 1.2
   registry (198 classes, zero NiArk*) therefore rejects them ALL. Measured
   natively: all 4 selected inputs exit 1 `Error loading stream.`
   (NATIVE_LOAD_REJECTED, generic); the qualified helper OBSERVED the specific
   native error `NiArkAnimationExtraData: cannot find create function.`
   (NO_CREATE_FUNCTION, enum 5) for all four — matching the source-predicted
   table-order first miss exactly, while remaining a SEPARATE evidence layer.
   No PE 10.1 asset in this container can EVER be loaded by the unmodified
   stock Gamebryo 1.2.2 toolchain — this is now a corpus-proven fact, not a
   single-file anecdote.
3. No PE world placement, instance, axis/unit or coordinate claim was made or
   is supportable from this run's evidence (section 14 ceiling preserved:
   MODEL_218757_TO_CMO_JOIN / HISTORICAL_WORLD_INSTANCE /
   PE_WORLD_ROOT_IDENTITY = NOT_ESTABLISHED; PE_AXES_AND_UNITS = UNVERIFIED;
   WORLD_XYZ_RECOVERED = NO). All reported transforms/bounds are
   FILE_SCENE_SPACE.
4. No commit/push occurred during the executor, QC or PE-MASTER audit
   phases; BASE f99febe was verified unchanged at every phase boundary; no
   original asset, SDK file or historical package was modified (all
   re-verified unchanged after each phase). The fresh internal QC and the
   PE-MASTER audit are COMPLETE (summary: section 11); the
   publication/persistence phase (this finalization — one path-limited
   commit + fast-forward push, one AUDIT_ENTRYPOINT row, EVIDENCE_INDEX +
   final manifest LAST, under its own authorization) completes the run.
   DESKTOP_POST_AUDIT remains PENDING.

```text
RUN_ID = PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009
RUN_CLASS = STAGED_RECORDS_CORRECTION_AND_ENGINE_ASSISTED_ASSET_INSPECTION
BASE_SHA = f99febeca9498011fc49f3aef932ecfac4244475 (unchanged, verified)
DATE = 2026-10-09
PCG_CLIENT_EXECUTION = NO
NEW_PCG_EXE_FUNCTION_BODIES = 0
CANONICAL_GATE_EFFECT = NONE
```

## 1. Identity and preflight (verified by this executor where re-measured)

- Governing contract verified: 32,125 B, SHA256
  63E093D22E6DA1A339F953977A21D4808300724FB6A91999A53C271E3D1A5753.
- Models.bnt: 395,412,868 B, SHA256
  C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0 —
  re-verified unchanged BEFORE and AFTER the phase.
- 218757 pin
  (…\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox\payloads\218757.nif):
  57,316 B, 3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36
  — re-verified unchanged after the phase.
- Stock printer FD693AF2D713C021B959FC7506200173435307C8FCCC24CCD5851DFCEB241C7C
  (663,552 B), MSVCP71.DLL DF96156F…23B, MSVCR71.DLL 8094AF5E…FEFE —
  re-verified unchanged after all runs. Optional helper gb12_oracle.exe
  DD7112A4…046C (594,944 B) + its source oracle.cpp AD1F5DED…E591A — verified
  before helper use, unchanged after.
- LOCAL HEAD == BASE f99febe; foreign untracked paths preserved untouched
  (6 foreign groups + this run's untracked package + experiments/).

## 2. Work Package A — records correction (COMPLETE; disposition summary)

Adjudicated against the Desktop post-audit (identity-verified inputs) and the
historical f99febe package (READ_ONLY; 22/22 manifest rows re-verified MATCH
by phase 1). Full dispositions in 00_RECORDS_CORRECTION/SUPERSESSION.md +
CORRECTED_CLAIM_MATRIX.json; headline:

- **FC-C1 SUPERSEDED (split):** initial local = getter return and fast-path
  equality stay VALID BYTE_OBSERVATIONS; growth-path equality of the later
  arg6 to the initial [P+8] = NOT_ESTABLISHED_WITHIN_BOUND (nonvolatile-register
  preservation does not preserve escaped memory); the subject's direct
  arg6-slot non-use RETAINED as a separate valid fact; the subject's late
  arg1 re-read ≠ proof the initial out-pointer survived the helper
  (NOT_ESTABLISHED on the growth path).
- **FC-C2 SUPERSEDED:** producing chains stay byte-proven distinct, but
  CONTAINER_VS_P_ALIAS_RELATION = UNRESOLVED (distinct chains can alias); the
  callback return can alias its receiver — the direct-EDI-operand census
  stays valid as a DIRECT-operand count while the absolute "never
  dereferenced" is NARROWED (indirect read through EAX NOT EXCLUDED). F2/F8
  and the G4/G5 cells corrected accordingly.
- **FC-C3 SUPERSEDED:** generic range/callback/container mechanism
  CONFIRMED_IN_EXAMINED_WINDOW, but DIRECT_TRANSFORM_OPERATION =
  NOT_ESTABLISHED and ROLE_IN_PLACEMENT_PIPELINE = UNRESOLVED;
  PLACEMENT_BRANCH_EXCLUDED = NO (absence of FPU/SSE excludes neither float
  bit copies nor placement-pipeline participation).
- **P3 sentence corrected:** direct slot usage is arg1–arg5 (arg6 slot has
  ZERO direct accesses); "all six" superseded; register part stays valid.
- Falsifier classes honestly re-labeled (F1/F5/F7 COUNTERCHECKS, F2/F3/F6
  METHODOLOGICAL, F4 CONDITION RECORD, F8 NEGATIVE CONTROL with a superseded
  interpretation) — none of the 8 was a mutation test on an actual body.
- Countermodels: 5/5 REPRODUCED (CM-1 3/3 cases, CM-2, CM-3 2/2, CM-4, CM-5
  preregistered prose case), NONE forced, NONE failed; raw outputs captured;
  every one labeled LOGICAL_COUNTERMODEL_REPRODUCTION (NOT execution of
  FUN_006C2E00; no closed body opened).
- Internal consistency of the corrected matrix verified in phase 1; no
  material contradiction remained, authorizing Package B under this contract.

## 3. Work Package B — SDK qualification (COMPLETE; scope-limited PASS)

Full detail in 01_SDK/ (TOOL_CAPABILITY_MATRIX.md,
SDK_EXECUTION_RESULTS.json, SYNTHETIC_AND_NEGATIVE_CONTROLS.json,
SOURCE_AND_BUILD_IDENTITIES.json, PREREGISTRATION_SDK_PHASE.md). Summary:

- 16 native executions of the ORIGINAL vendor printer
  (fd693af2…41c7c): 4 SDK positives (DT.NIF 388 visits/6 depth,
  DT_Ground.NIF 561/7, WORLD.nif 131/7 — 130 unique addresses,
  OBJECT.NIF 17/5 — 16 unique; counts identical to the pinned Desktop
  comparison values — deterministic same-exe/same-input reproduction), 4
  negative mutations, 1 missing file, 1 own empty scene, 6 synthetic
  transform controls (6/6 expected-vs-observed PASS, incl.
  TWO_PARENTS_LAST_LINK_WINS diagnostic).
- Capability matrix: C1 headless PASS; flags -trans LOCAL getters,
  -bs WORLD bound, -extra CLASS NAMES only, -prop names, -geom counts,
  -mem SDK-process addresses (PASS each, with scope); C3 serialized-field
  exposure FAIL (by design — zero serialized fields); C4 native-object
  exposure PASS with scope; C5 post-Update PASS with per-value-mutation
  NOT_MEASURED; C6 traversal edges PASS (indentation ≠ scene-child;
  controller edges measured); C7 three DISTINCT count namespaces PASS
  (serialized blocks vs visits vs unique pointers); C8 local-vs-world PASS
  (6/6 synthetic); C9 bounds-as-bounds PASS; C10 version range
  [3.3.0.11..10.2.0.0], user version 0, loader aliases measured PASS
  (NiKeyframeController→NiTransformController 9→9 and 2→2 runtime-observed);
  C11 error specificity **FAIL** (one generic `Error loading stream.` for
  every failure — honest scope limit); C12 zero on-disk mutation PASS
  (7/7 identities re-verified); C13 Update(0) runs controllers PASS
  (per-value NOT_MEASURED); C14 negative/empty classification PASS (empty +
  exit 0 is NOT a populated inspection — preregistered rule); C15
  SceneViewer SOURCE_ONLY (GUI not executed).
- TOOL_QUALIFICATION_GATE = **PASS** (scope: this pinned binary, headless
  structural inspection, SDK/synthetic inputs; does NOT qualify GUI tools,
  serialized-field parsing, or any PE-world capability).

## 4. Work Package C — PE census, selection, native inspection, comparison

### 4.1 Corpus metadata census (contract section 8)

Produced with a VERBATIM byte-identical COPY of the documented BNT2 walker
(TOOLS/s01_bnt2_walk_r1.py; canonical s01 SHA256
60EBC604F3645C839F56D163E6DA6C873DC7CF2E5BE1CA2D2955D430C39FF65F) + the
s02/s03-lineage census logic (adapted copy, lineage disclosed in the script).
Negative-control battery 4/4 PASS (synthetic archives only) BEFORE the real
walk; calibration fail-closed (index_start 395,262,727, count 5,596, anchor
name offset 395,268,773; 218757 = entry 781 @ offset 116,223,520, 57,316 B,
name offset 395,283,797 — all reproduced from the pinned bytes).

- **Denominators: 5,596 indexed NIF entries (all .nif, all raw, no zlib);
  header line + version u32 readable 5,596/5,596; failures 0; text-version
  mismatches 0.**
- Version census: 4,838 × 10.1.0.0 (type tables + object histograms SCANNED,
  0 scan failures), 757 × 4.1.0.12 (num_blocks readable per the demonstrated
  nif_parser_v2 header layout; type histogram HEADER_UNSUPPORTED — inline
  per-block type names are block-body decoding, beyond a metadata census),
  1 × 4.0.0.2 (HEADER_UNSUPPORTED beyond the version field).
- Independently reproduces the historical Rosetta BNT2_WALK_SUMMARY numbers
  (4,838/757/1, raw 5,596, 0 failures).
- Artifact: 02_PE/CORPUS_METADATA_CENSUS.csv (5,596 rows: name, ordinal,
  offset/length, compression, SHA256, header line, version, user version,
  block counts, compact type histogram, status) + CENSUS_SUMMARY.json; full
  per-entry tables LOCAL_ONLY (02_PE_work/per_entry_full.json).

### 4.2 Mechanical selection (frozen BEFORE native/deep inspection)

02_PE/SELECTION_AND_EXTRACTION_PROVENANCE.json (rules preregistered in
02_PE/PREREGISTRATION_PE_PHASE.md §3):

- **(a) MANDATORY 218757.nif** — fresh extraction from the pinned BNT at the
  index-proven range; byte identity with the contract pin REQUIRED and
  TRUE (fail-closed).
- **(b) STOCK-ONLY candidate = NO_STOCK_ONLY_CANDIDATE.** Pool evidence
  (measured over the fresh census): **0 of 4,838** NIF 10.1.0.0 files have a
  COMPLETE declared type table contained in the measured stock registry
  (198 classes). NiArkTextureExtraData, NiArkAnimationExtraData and
  NiArkImporterExtraData are declared by ALL 4,838 files; NiArkViewportInfoExtraData
  by 4,062; NiArkShaderExtraData by 1,293; NiVertexMorphExtraData by 118;
  NiArkBillboardNode by 12. No NiArk class was removed to manufacture a
  candidate. 757+1 4.x entries are excluded from this pool (their class
  tables are not header-readable at the metadata level).
- **(c) COMPOUND candidates (top 3 of a 1,135-file pool; ranked by NiNode
  object count desc, then NiTriShape desc, size desc, name asc — ranks
  compound STRUCTURE, not proven world scenes):** 496633.nif (166 NiNode /
  163 NiTriShape / 2,068,670 B, SHA 4DBCC731…B736), 512126.nif (122/129,
  673,746 B, E37C7D29…B2BA), 423020.nif (119/102, 882,570 B, C46D9DF2…917).
  218757 excluded from pools (b)/(c) by dedup; 4 distinct inputs ≤ hard max 5.
- All four extracted fresh into LOCAL_ONLY (02_PE_payloads/), each with
  container/index/range/size/SHA256 provenance and census byte-identity
  checks; 496633 additionally byte-identical to the historical oracle-run
  payload (cross-run extraction fidelity).

### 4.3 Native execution on the stock printer (contract section 9)

All four (full provenance in 02_PE/NATIVE_EXECUTION_RESULTS.json; raw logs in
02_PE/raw/; DLL exposure class CHILD_PROCESS_PATH_DLL_EXPOSURE, same as
Package B; printer/DLL/container/payload identities re-verified unchanged
after the runs):

| input | exit | verbatim stderr | visits | outcome |
|---|---|---|---|---|
| 218757.nif | 1 | `Error loading stream.` | 0 | NATIVE_LOAD_REJECTED |
| 496633.nif | 1 | `Error loading stream.` | 0 | NATIVE_LOAD_REJECTED |
| 512126.nif | 1 | `Error loading stream.` | 0 | NATIVE_LOAD_REJECTED |
| 423020.nif | 1 | `Error loading stream.` | 0 | NATIVE_LOAD_REJECTED |

The binary's specificity limit (Package B C11 FAIL) holds on PE inputs too:
the stock output alone cannot identify the failing class. The PE assets are
NOT declared corrupt — the rejection is a missing-factory gate on
MindArk-custom classes.

### 4.4 The ONE optional native helper (contract section 11)

**Used (not built):** the EXISTING gb12_oracle.exe (identity re-verified
against the contract pin; its source oracle.cpp inspected BEFORE invocation;
provenance + interface recorded; behavior differences from the unmodified
printer DISCLOSED — 6 items, incl. prints the SPECIFIC NiStream last error,
Update(0,false) skips controllers, OracleStream snapshot hook via the PUBLIC
RegisterPostProcessFunction, zero engine changes, no NiArk loaders, no dummy
factories). Qualification controls 3/3 PASS (SDK positive OBJECT.NIF: exit 0,
60 blocks/2 top objects; missing-factory QzNode: exit 1 with the SPECIFIC
message; empty scene: exit 0 with 0/0). PE results (all four):

```text
exit=1, load=FAIL, lastError=5 (NO_CREATE_FUNCTION),
lastErrorMessage = "NiArkAnimationExtraData: cannot find create function."
```

This upgrades the failing-class identification from SOURCE-PREDICTED to
OBSERVED NATIVE (through a disclosed helper using the SAME stock factory
registry) — while the comparison artifacts keep the two evidence layers
SEPARATE (SOURCE_PREDICTED from the pinned SDK source table-order scan vs
the observed native reports).

### 4.5 Parser/native comparison (contract section 10)

Full four-namespace separation per input in 02_PE/PARSER_NATIVE_COMPARISON.json
(ORIGINAL_NATIVE_EXECUTION | OBSERVED_NATIVE_ERROR_HELPER |
SOURCE_PREDICTED_ORIGINAL_VERDICT | OUR_PARSER_RESULT |
OUR_EXTENSION_CONTINUATION). Highlights:

- probe-version: all 4 ACCEPTED by the version gate (10.1.0.0 in
  [3.3.0.11, 10.2.0.0], user version 0) — the gate is NOT the rejection point.
- ordinary inspect: all 4 SOURCE_PREDICTED_ORIGINAL_VERDICT = REJECTED,
  RTTIError(NiArkAnimationExtraData), first miss at table index 1 (fail-closed:
  nothing past the first table miss).
- --full-decode (OUR extension; never stock acceptance):
  - **218757.nif: coverage INCOMPLETE = 62 semantic + 4 boundary-only
    (unregistered) = 66 accounted; structural closure PASS; top-level root
    [0].** The prior ceiling (66 = 62 semantic + 4 opaque) is PRESERVED and
    INDEPENDENTLY REPRODUCED by this fresh run — NOT promoted to 66 semantic
    decodes.
  - **423020.nif: coverage INCOMPLETE = 432 semantic + 5 boundary-only
    (4 NiArk + 1 registered-but-not-decoded NiTextureEffect) = 437 accounted;
    structural closure PASS; root [0].**
  - **496633.nif: closure search budget exhausted** (measured; 1,011 s
    long-bounded run; ADAPTER_INTEGRITY=FAIL structural closure; counters
    NOT_MEASURED with reasons — honest, not zero).
  - **512126.nif: CLOSURE_SEARCH_FAILED — no boundary assignment closes the
    file to EOF within the tool's budgets** (measured; 16 LOADERS-runs incl.
    an 83-block registered-but-not-decoded run).
  - Both failures are RETAINED measured outcomes; no candidate replacement
    was attempted; no general hardening was performed (the ONE repair-cycle
    allowance was NOT spent). Historical cross-reference labeled: the
    pre-F2 core version closed 496633 (1,288 objects) — different tool
    version, comparison evidence only.
- The 300 s runner timeouts that preceded the two long-bounded reruns are
  recorded as measured events in ORACLE_RUN_PROVENANCE.json.

### 4.6 Scene/asset structure (contract section 12)

02_PE/SCENE_STRUCTURE_RESULTS.json — typed graphs with explicit namespaces
(serialized block ID; native pointer / traversal ID = NOT_AVAILABLE_NO_
NATIVE_LOAD for every selected PE input — honest, never fabricated), edge
kinds TOP_LEVEL_ROOT / SCENE_CHILD / CONTROLLER / PROPERTY / EXTRA_DATA /
RESOURCE_REFERENCE / UNKNOWN, and per-edge INDEPENDENCE labels:

- **218757.nif** (66 blocks: 62 semantic + 4 opaque NiArk): single top-level
  root NiNode "Scene Root"; 12 NiNode (B_Outpost_me01_Ext_sign / _main /
  bigdoors / smaldoor / vent03, __NDL_MultiMtl_Node, dPVS_occ01..05);
  14 NiTriShape + 14 NiTriShapeData; 9 NiTexturingProperty (ALL texture
  links NULL_LINKID — no standard external texture reference); 1
  NiZBufferProperty; 2 NiDirectionalLight attached via the root's effects
  array (UNKNOWN-kind edge, labeled); 0 controllers (Update could not change
  displayed state via controllers); 68 typed edges; composed FILE_SCENE_
  SPACE transforms computed for 28 blocks through complete chains ONLY,
  cross-checked 5/5 against the independent s2 parser's world transforms
  (e.g. B_Outpost_me01_Ext_sign:0 → world translate (0, −1030, 820));
  post-load/post-Update local transform NOT_MEASURED (no native load
  possible). NiArk payload analysis (fresh s2 Rosetta-lineage parse of the
  byte-identical payload, 66/66 EOF-exact): NiArkTextureExtraData carries the
  per-part texture NAME bindings (+ texturing-property refs; per-entry 9-byte
  tail semantics UNRESOLVED; the historical "BNT2 id" reading remains a
  RETRACTED prior claim), NiArkImporterExtraData + NiStringExtraData are
  EXPORTER METADATA (NDL 3ds Max settings dump), NiArkAnimationExtraData /
  NiArkViewportInfoExtraData are byte-derived-boundary opaque payloads.
  Model extents [2500, 3350, 1250] (game units, FILE_SCENE_SPACE bbox of
  world-composed vertices) are recorded as a SEPARATE bounds measurement —
  NO historical location derived from them, from native pointer values or
  from the zero root transform. Classification: SINGLE_MODEL (standalone
  outpost asset) with evidence + alternatives; world placement:
  NO_WORLD_PLACEMENT_EVIDENCE_FOUND.
- **423020.nif** (437 blocks: 432 semantic + 5 boundary-only): single root
  NiNode "Scene Root"; 119 NiNode incl. Portal01_01 and Bip01_item /
  Bip01_Camera_001..N rig-like sub-trees; 102 NiTriShape + 102
  NiTriShapeData; 92 NiTexturingProperty; 3 NiPointLight; 1 NiTextureEffect
  (registered-but-not-decoded, boundary-only); 0 controllers.
  Classification: COMPOUND-OBJECT / SCENE-CANDIDATE (mechanical structure
  rank — NOT a proven world scene).
- **496633.nif / 512126.nif:** NOT_AVAILABLE via the oracle full-decode
  (measured closure failures above); header-level metadata + RTTI table
  validation + native rejection evidence remain recorded. An unknown offset
  stops dependent parsing — no typed graph was fabricated for them.

### 4.7 Bounded 218757 comparison (contract section 13)

02_PE/MODEL_218757_RELATION_RESULTS.json:

- Scope: 1 of max 3 candidate comparisons (218757 vs 423020 — the only
  selected compound candidate with safe geometry decoding; 496633/512126
  provide no safe geometry, measured).
- Geometry fingerprints: exact serialized f32-LE vertex arrays and u16-LE
  triangle arrays, extracted from the payload bytes at closure-verified
  block ranges using the documented field layout, VALIDATED against BOTH
  parsers' measured counts and the adapter's model_bound values
  (14/14 + 102/102 EXTRACTED_VALIDATED; arrays stay LOCAL_ONLY — only
  SHA256 fingerprints, counts, names and transforms are published).
- **Result: 0 exact geometry fingerprint matches →
  NO_MATCH_IN_SELECTED_INPUTS** (14 vs 102 mesh fingerprints compared; no
  shared mesh found). This does NOT exclude baked/re-exported models,
  different asset IDs, other containers, nonlocal instance sources or
  network-delivered instances; the candidate set was NOT expanded. No fuzzy
  threshold, texture/name-only identity or plausible-coordinate acceptance
  was used.

## 5. Placement qualification ceiling (contract section 14) — preserved

```text
MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
HISTORICAL_WORLD_INSTANCE = NOT_ESTABLISHED
PE_WORLD_ROOT_IDENTITY = NOT_ESTABLISHED
PE_AXES_AND_UNITS = UNVERIFIED
WORLD_XYZ_RECOVERED = NO
```

No edge in any artifact of this run was promoted to a PE world relation; SDK
mechanisms (world attachment anchors, per-instance properties, clone-shared
geometry, vertex-baked transforms) remain hypothesis classes, not PCG facts.

## 6. Intervention ledger summary

INTERVENTION_LEDGER.md (append-only) now carries three entries:
(1) Package A records phase — no runtime interventions;
(2) Package B — CHILD_PROCESS_PATH_DLL_EXPOSURE over 16 native executions,
non-mutation verified 7/7, one disclosed launcher defect;
(3) Package C — (3a) CHILD_PROCESS_PATH_DLL_EXPOSURE over the 4 stock-printer
PE executions; (3b) CUSTOM_SDK_SOURCE_HELPER_EXECUTION over the ONE helper
(3 qualification controls + 4 PE runs; identity/provenance/differences
disclosed); (3c) non-native copy executions (oracle copy, census/selection
scripts, s2 parse copy — no exposure class); (3d) four executor tooling
defects disclosed (census 4-byte shift caught before any use; helper-hash
transcription abort before any invocation; two s17 extraction/cross-check
cursor bugs caught by built-in validation and fixed before any conclusion;
two failed launch attempts with no process). The one run-local repair-cycle
allowance was NOT spent.

## 7. Open findings / NOT_CHECKED (honest)

- **NOT_CHECKED / NOT_MEASURED:**
  - Post-load/post-Update native state for ANY PE input (natively
    impossible: missing-factory rejection at LoadRTTI; a positive native
    load would require dummy factories or guessed NiArk loaders — both
    forbidden).
  - Per-value controller mutation at Update(0) — no controllers exist in
    the closure-verified PE inputs anyway (0 in all four).
  - Type histograms for the 757 4.1.0.12 + 1 4.0.0.2 entries
    (HEADER_UNSUPPORTED — inline block-type layout = full decode, beyond
    this metadata census).
  - NiArk semantic layout beyond the s2 byte-derived boundaries
    (NiArkAnimationExtraData/NiArkViewportInfoExtraData contents remain
    UNDETERMINED beyond the boundary; NiArkTextureExtraData per-entry 9-byte
    tail semantics UNRESOLVED).
  - Native pointer/traversal namespaces for PE inputs (no native load).
- **Measured capability gaps (retained, not chased):** the current pinned
  gb12 copy's closure search cannot close 496633.nif (budget exhausted) or
  512126.nif (no closing assignment) within its budgets; the pre-F2 core
  version closed 496633 historically — a version-difference observation.
- **DESIGNED_NOT_EXECUTED (next hypotheses, NOT run):** (1) a bounded
  closure-search improvement for the oracle copy (memoization/screening
  limits) to close 496633/512126 under the existing acceptance semantics —
  needs its own authorization; (2) geometry-fingerprint comparison of
  218757 against the OTHER 1,132 compound-pool files (candidate-set
  expansion — explicitly out of scope here); (3) a PE-side instance source
  search (CMO-class record tying instance→model→transform) — needs a new
  bounded contract; (4) resolution of the NiArkTextureExtraData 9-byte tail
  semantics.

## 8. Measured fields (contract section 19 — what exists now; QC/persistence finalize)

```text
RUN_ID = PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009
BASE_SHA = f99febeca9498011fc49f3aef932ecfac4244475
RESULTING_SHA = discover with: git log -1 -- docs/audits/PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009 (this run's single allowlisted publication commit; a file cannot contain its own commit SHA)
REMOTE_SHA = the same single publication commit; LOCAL_HEAD == origin/master == actual remote master == RESULTING_SHA verified at push (result in the persistence-phase return)
RUN_STATUS = COMPLETED_WITH_MASTER_ACCEPTED_ADVISORY (Packages A+B+C to their bounded ends; fresh internal QC PASS_WITH_FINDINGS; PE-MASTER MASTER_ACCEPTED advisory; DESKTOP_POST_AUDIT = PENDING)
FC_C1_DISPOSITION = SUPERSEDED (split; growth-path arg6 equality NOT_ESTABLISHED_WITHIN_BOUND; arg6-slot non-use retained)
FC_C2_DISPOSITION = SUPERSEDED (CONTAINER_VS_P_ALIAS_RELATION=UNRESOLVED; dereference absolute narrowed; F2/F8/G4/G5 corrected)
FC_C3_DISPOSITION = SUPERSEDED (DIRECT_TRANSFORM_OPERATION=NOT_ESTABLISHED; ROLE_IN_PLACEMENT_PIPELINE=UNRESOLVED; PLACEMENT_BRANCH_EXCLUDED=NO)
SDK_TOOL_QUALIFICATION = PASS_WITH_SCOPE (stock printer; headless; specificity FAIL preserved)
SDK_POSITIVE_CASES_EXECUTED = 4
SYNTHETIC_TRANSFORM_CASES_EXECUTED = 6
NEGATIVE_AND_EMPTY_CASES_EXECUTED = 6
PE_METADATA_CENSUS_COUNT = 5596 indexed; 5596 header-readable (0 failures); type-table histograms 4838 (10.1.0.0); num-blocks-only 757 (4.1.0.12); HEADER_UNSUPPORTED 758 (757+1); failures 0
PE_DEEP_INPUT_COUNT = 4/5 (218757.nif 3E8A22C2…CF36; 496633.nif 4DBCC731…B736; 512126.nif E37C7D29…B2BA; 423020.nif C46D9DF2…917)
STOCK_ONLY_CANDIDATE = NO_STOCK_ONLY_CANDIDATE (0/4838 fully-registered tables; all-file NiArk declarations measured)
COMPOUND_CANDIDATES = pool 1135; selected 496633 (166/163), 512126 (122/129), 423020 (119/102)
MODEL_218757_NATIVE_RESULT = exit 1 "Error loading stream." (NATIVE_LOAD_REJECTED, raw log 02_PE/raw/PE_218757.stderr.txt); helper-observed "NiArkAnimationExtraData: cannot find create function."
MODEL_218757_CUSTOM_PARSE_COVERAGE = 62+4/66 ceiling PRESERVED (independently reproduced this run)
NATIVE_HELPER_BUILT_OR_USED = used_gb12_oracle.exe DD7112A4…046C (existing custom SDK-source build; controls 3/3 PASS; 6 disclosed behavior differences; NOT the vendor printer)
COMPOUND_SCENE_CANDIDATES_INSPECTED = 1/3 fully (423020 closure-verified) + 2/3 attempted with measured closure failure (496633 budget exhausted; 512126 no closing assignment)
MODEL_GEOMETRY_MATCHES = 0; NO_MATCH_IN_SELECTED_INPUTS (1 comparison of max 3; 14 vs 102 validated mesh fingerprints)
PE_WORLD_ROOT_IDENTITY = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
QC_ORIGIN = FRESH_INTERNAL_QC (pe-master-auditor fresh session; internal to PE-MASTER; NOT an independent Desktop post-audit; summary: section 11)
QC_VERDICT = PASS_WITH_FINDINGS (6 P2 + 4 P3, 0 P0/P1; dispositions: section 11)
OPEN_FINDINGS = see section 7 (measured closure gaps; NiArk tail semantics; 4.x tables; post-Update state natively unavailable)
MANIFEST_ROWS = 169 total data rows in MANIFEST_SHA256.csv = 168 package-file rows (every physical package file except the manifest itself, including EVIDENCE_INDEX.md and PE_MASTER_REVIEW.md) + 1 changed AUDIT_ENTRYPOINT.md row (contract §18)
MANIFEST_PACKAGE_FILE_ROWS = 168
PACKAGE_PHYSICAL_FILES = 169 at final persistence (132 draft-time files + 31 fresh-QC control files under 00_CONTROL_INTERNAL_QC\ + QC_REPORT.md + QC_RESULTS.json + AMEND_LOG.md + PE_MASTER_REVIEW.md + EVIDENCE_INDEX.md + MANIFEST_SHA256.csv)
MANIFEST_BIJECTION = GATED_COMMIT_PREREQUISITE (predicate: MANIFEST_SHA256.csv data rows == the physical files enumerated from disk, 1:1 — zero duplicate, zero missing, zero extra, zero size mismatch, zero SHA mismatch, every row re-read from disk; the manifest is generated LAST after every package edit; the check executes immediately after generation by an independent code path and the commit proceeds ONLY on PASS; the executed result is reported in the persistence-phase return — any FAIL blocks the commit and forces regeneration)
PROPRIETARY_PAYLOADS_COMMITTED = NO (all payloads LOCAL_ONLY; manifest in LOCAL_ONLY_ROOT)
CANONICAL_GATE_EFFECT = NONE
DESKTOP_POST_AUDIT = PENDING
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES (this draft ends the executor's Package C work; QC/PE-MASTER follow)
```

## 9. EVIDENCE_INDEX (all package files; path | bytes | sha256)

See the full per-file index in HANDOFF.md (OUTPUT_FILES) and the machine-
readable index below (relative to the package root):

```text
00_RECORDS_CORRECTION\CORRECTED_CLAIM_MATRIX.json|26567|e33704ffc688534e2b09ecb2f81e415bcf5b6cc2acceff4e2b18c1efdf701d52
00_RECORDS_CORRECTION\COUNTERMODEL_RESULTS.json|13269|2e159900137c14faefcbf910d0025769891cef8cc6f739573a6996fdf3346ed1
00_RECORDS_CORRECTION\countermodels\cm1_escaped_local.py|5312|ac2d0af33f62586d3a12d174c53fc8ef319ca0575c336d5e0fbd2d5005e0ef84
00_RECORDS_CORRECTION\countermodels\cm2_alias_model.py|4329|5e5f4fbd162d33c950da695884b6561155bd086d20b7a356ba2ccf160e5bacc2
00_RECORDS_CORRECTION\countermodels\cm3_dword_float_copy.py|3356|0cfcd5c0356321a3def2ae377134009ecb208357cbc708eb8331f20bdbb7c293
00_RECORDS_CORRECTION\countermodels\cm4_escaped_subject_outslot.py|4557|8d8cdd5717f9cd8efaaf954c9937524884d657deb91a1b7cc983281b8eff8857
00_RECORDS_CORRECTION\countermodels\cm5_callback_return_alias.py|4033|1498fcec54a11fe65fb1b2aee0a9b1ab11fb1cbc3f02559f1aa0c3a6513b8c2f
00_RECORDS_CORRECTION\countermodels\raw\cm1_escaped_local_output.json|1262|1a609fb164cf3c92f984909ebcdda413d9328c429f66f9a1c95524b00ba6a099
00_RECORDS_CORRECTION\countermodels\raw\cm2_alias_model_output.json|844|dfe28dc1e1b686553d0b5a79eaabeead550ffb2c46c5cad7dd67243b2bc1c24e
00_RECORDS_CORRECTION\countermodels\raw\cm3_dword_float_copy_output.json|921|2eb21d4f97c282f3993270c5c72188979c1711ff1f7fa2c992eafa1c517004dc
00_RECORDS_CORRECTION\countermodels\raw\cm4_escaped_subject_outslot_output.json|833|d1cf8977520f256a597ef8ba291f13616f41eed98cbf8fad316898bc44466aa4
00_RECORDS_CORRECTION\countermodels\raw\cm5_callback_return_alias_output.json|1023|8250e8c6d6196180e4c09bf53167d754d07fd598dfa5a133ef3e121af9429b12
00_RECORDS_CORRECTION\SUPERSESSION.md|24017|a3f96365c8539f7f83c8634dc12621acdb8b714b68270c0b7f08c20a6b8fb69b
01_SDK\negative_control_details_internal.json|26261|4f806504810762e775aabd20684522ae77791946817a8c1c8978485d5a55432d
01_SDK\PREREGISTRATION_SDK_PHASE.md|11448|32913d50cd42a1c75682d684f7962c6ddc9396db729a1d71e252ad672bfd3aa3
01_SDK\raw\IDENTITY_PARENT.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\IDENTITY_PARENT.stdout.txt|685|2be854741b9b491a5468a90b1e65d4c7d253cf844994a1eaaff46be9950bfbf9
01_SDK\raw\LEAF_SCALE_SEPARATE.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\LEAF_SCALE_SEPARATE.stdout.txt|705|565c9cf9909291db5d71e025dacd90087a60cb0cce2b86185cf142be7fd871bb
01_SDK\raw\MISSING_INPUT.stderr.txt|23|74495fc82b8b38ff37746ffe732bbd08ff55674dfc6e3c83060edc3c3185abc4
01_SDK\raw\MISSING_INPUT.stdout.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\ROTATED_SCALED_PARENT.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\ROTATED_SCALED_PARENT.stdout.txt|709|80da071d62d12ca990ebacf6e39d675c01f3ddaec15275e5e98705ec5663292e
01_SDK\raw\SDK_DESERT_GROUND.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\SDK_DESERT_GROUND.stdout.txt|201266|ce02c34f49a6a27f04dfd8ad1908c2d1f3b1916acb3cbfa590dab1206589d9f9
01_SDK\raw\SDK_DESERT_TOWN.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\SDK_DESERT_TOWN.stdout.txt|157325|0ff9ce1e4c6f3de0c5c74d376c06aea1e7d15cadcdbc2d553c6d131195a5b59a
01_SDK\raw\SDK_TUTORIAL_OBJECT.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\SDK_TUTORIAL_OBJECT.stdout.txt|6594|96b305b27e9040409f89a0df6accb70b823c075fc42700f313da31a95d10c13a
01_SDK\raw\SDK_TUTORIAL_WORLD.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\SDK_TUTORIAL_WORLD.stdout.txt|62912|84f48609865daa405795e2542e72744d12ac8c724beb6a9418f591c4fd866d1e
01_SDK\raw\SYNTH_BAD_HEADER_TEXT.stderr.txt|23|74495fc82b8b38ff37746ffe732bbd08ff55674dfc6e3c83060edc3c3185abc4
01_SDK\raw\SYNTH_BAD_HEADER_TEXT.stdout.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\SYNTH_EMPTY_SCENE.stderr.txt|28|acf89a863661c6262d69b31fa49c8171abc998ccb4af5782216d7432609770d8
01_SDK\raw\SYNTH_EMPTY_SCENE.stdout.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\SYNTH_TOO_NEW_BINARY_VERSION.stderr.txt|23|74495fc82b8b38ff37746ffe732bbd08ff55674dfc6e3c83060edc3c3185abc4
01_SDK\raw\SYNTH_TOO_NEW_BINARY_VERSION.stdout.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\SYNTH_UNKNOWN_CLASS.stderr.txt|23|74495fc82b8b38ff37746ffe732bbd08ff55674dfc6e3c83060edc3c3185abc4
01_SDK\raw\SYNTH_UNKNOWN_CLASS.stdout.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\SYNTH_USER_VERSION_1.stderr.txt|23|74495fc82b8b38ff37746ffe732bbd08ff55674dfc6e3c83060edc3c3185abc4
01_SDK\raw\SYNTH_USER_VERSION_1.stdout.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\THREE_LEVEL_SOCKET.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\THREE_LEVEL_SOCKET.stdout.txt|909|3d650963043c4f0d60a1c6aee9cf8cc9d5d09d0d6e5b193d8104e94a3ef838fd
01_SDK\raw\TRANSLATED_PARENT.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\TRANSLATED_PARENT.stdout.txt|701|682aa63022c68f88d8f98530a00c9d77cbb4e50ff6604847c1e14cb9ea17cd5f
01_SDK\raw\TWO_PARENTS_LAST_LINK_WINS.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
01_SDK\raw\TWO_PARENTS_LAST_LINK_WINS.stdout.txt|1093|769d1a478d4a436b1b754324c86adf70e388b918c8807041b2f550d70cc9a2c7
01_SDK\SDK_EXECUTION_RESULTS.json|62344|2400f8454f24280699439fd50d0d923b5d5fea618868dfa4e801535762692657
01_SDK\SOURCE_AND_BUILD_IDENTITIES.json|26174|b9f8b7b183cd52e02d2c99afd0b8b8869edd7bb8966ccda9b998b86b7ad0d19b
01_SDK\SYNTHETIC_AND_NEGATIVE_CONTROLS.json|34167|fb813c64ef47f9b5569b1f3bc474ded32ad6afe75ffdafa74bc806abc8b2df56
01_SDK\synthetic_control_details_internal.json|16583|64cd1ed46e7d5b247e1cb4ba43c3ca8f23ce10a2b3e10dcf52f4a36a6d35dafe
01_SDK\TOOL_CAPABILITY_MATRIX.md|23530|c55e5644382d97b4a9871d5e74230657b2286aa50c667de2f63ff8a4e39a6f39
02_PE\CENSUS_SUMMARY.json|2605|78d8a737842ca12ffe11cf0099e95e42da454cb157a0a4a1ce5a18a1e63cc6f5
02_PE\CORPUS_METADATA_CENSUS.csv|2415783|ea66400faa91829474b0195222884e84e4695aa15f8281dbf0457418a5d6ebd6
02_PE\MODEL_218757_RELATION_RESULTS.json|9055|ffbfae00e6b069c6777adb49d226216c80934bf61a2040e14efcc92d712a803f
02_PE\NATIVE_EXECUTION_RESULTS.json|18490|c068d2ab2e414cd7c62925243fe4d38642e88eb0af7037215577bf9b6143f123
02_PE\NATIVE_HELPER_RESULTS.json|28636|70ffd56634fb2033c50c5b05d8b6883f3379562ef3b377d80609119f28469003
02_PE\ORACLE_RUN_PROVENANCE.json|21681|8d9d7cc26d6e4d39dd69aa76647ec431ac6312524c00b411bdab6ffefdcdfac2
02_PE\PARSER_NATIVE_COMPARISON.json|36615|dba55b8ef752db3007ae9140d047a3a1f21bcc70dd873b7aa5cd0cc4ade5d1f5
02_PE\PREREGISTRATION_PE_PHASE.md|13793|cba483f4c3036fcad4167b87032039e52181208851f61cd5af819f5847005bba
02_PE\raw\PE_218757.inspect.json|6181|497640be5f1664026a11d4dde9800e52f2e9d8bb4fdc4794c005aa26474d7866
02_PE\raw\PE_218757.inspect_full.json|76238|500df714889b847f06fdf5ac62ae4267c7f6a5cd2ea6049e6bbbef691efeb443
02_PE\raw\PE_218757.probe.json|1064|4df21d02727f74fbb26899b9b7713de615bb39cfd19db149e17279be01770af7
02_PE\raw\PE_218757.stderr.txt|23|74495fc82b8b38ff37746ffe732bbd08ff55674dfc6e3c83060edc3c3185abc4
02_PE\raw\PE_218757.stdout.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\raw\PE_218757_HELPER.oracle.json|445|bbc8ac66d2aaff943f2fc9925b5dddcf6a49b2f6f2696b34ddcdbf8595d25d30
02_PE\raw\PE_218757_HELPER.oracle.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\raw\PE_423020.inspect.json|6184|6ac6890086b492d9393927ace4ae1d386b1cd4ca962cb0b1ba17a44d62efff16
02_PE\raw\PE_423020.inspect_full.json|506118|695804fe8ce22853136f433b5051d57ce8d176f80bc2bf3657e228de3f0769d1
02_PE\raw\PE_423020.probe.json|1065|c45509b8d79bb8e2938f8b67aacaf44e344b20680381dc956040c42e5bb9f0f9
02_PE\raw\PE_423020.stderr.txt|23|74495fc82b8b38ff37746ffe732bbd08ff55674dfc6e3c83060edc3c3185abc4
02_PE\raw\PE_423020.stdout.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\raw\PE_423020_HELPER.oracle.json|445|38f9a967a49d9e4d0617886cea90ac95fc0dc565afc2dd6e5078163c2e8fb24a
02_PE\raw\PE_423020_HELPER.oracle.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\raw\PE_496633.inspect.json|6187|2a7b7691e955a8bc107d5d22fabe2048fe8599348331a7be44417be51f2df954
02_PE\raw\PE_496633.inspect_full.json|589473|a8f18dee51d5e23c650d3db9923e892a6c2b174120d9db6d2559fe8d063baa68
02_PE\raw\PE_496633.probe.json|1066|23c1153b5d0e0fea991bc1ccfe17dc59851a8396e47e2cee90d2f0ea85e9a70a
02_PE\raw\PE_496633.stderr.txt|23|74495fc82b8b38ff37746ffe732bbd08ff55674dfc6e3c83060edc3c3185abc4
02_PE\raw\PE_496633.stdout.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\raw\PE_496633_HELPER.oracle.json|445|9c78dbb344b1630b6979ccf1487e8d59781b971141cc99ce41dd7d598d5680ab
02_PE\raw\PE_496633_HELPER.oracle.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\raw\PE_512126.inspect.json|6184|358b03d51afc3a77a146b4c15e5c15f8b7350b94e76c6097551e68a3ef1ed1b6
02_PE\raw\PE_512126.inspect_full.json|15207|a15731a6094e82645b66a03a24cdc561b1a4e216c2439e8342b0476988a1f9df
02_PE\raw\PE_512126.probe.json|1065|4f6f781f3f26750cf06f30a2f58ae0a953813272a6023cbb5c64d229ab479f05
02_PE\raw\PE_512126.stderr.txt|23|74495fc82b8b38ff37746ffe732bbd08ff55674dfc6e3c83060edc3c3185abc4
02_PE\raw\PE_512126.stdout.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\raw\PE_512126_HELPER.oracle.json|445|72a2896543c2cb08b7d22be286c40f1232346f312492196b7349edfc6eb6f942
02_PE\raw\PE_512126_HELPER.oracle.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\raw\QC1_SDK_POSITIVE_OBJECT.oracle.json|4496|25ba38188f463d895f202522bc2032d8004cf081114830137a6d7fea8d16d51c
02_PE\raw\QC1_SDK_POSITIVE_OBJECT.oracle.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\raw\QC2_MISSING_FACTORY_QZNODE.oracle.json|443|a2e0fd98ac2f7011acc9f5b1a7880020b6f6819f768c65df3663b86667a02a01
02_PE\raw\QC2_MISSING_FACTORY_QZNODE.oracle.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\raw\QC3_EMPTY_SCENE.oracle.json|477|2ad9f8f3a1cc070690d78f69a6f4f0d5efd62a4b825e00a7a10f58006efc37b8
02_PE\raw\QC3_EMPTY_SCENE.oracle.stderr.txt|0|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
02_PE\SCENE_STRUCTURE_RESULTS.json|469580|333854c4b4fe39454bd2830ca141cea0548a6aecd04eb813066874e25ef77d3d
02_PE\SELECTION_AND_EXTRACTION_PROVENANCE.json|16049|73b44293dec55e2b39bb514aff7d0426e9fd6e4fedfac8eb7fdfe4569f22e29b
AUTHORIZATION_AND_PREFLIGHT.md|8745|62f71ce41c7ece6809c0ebe8bda896ea2e5898c4e46f74c7739efd13a299405a
INPUT_IDENTITIES.json|14935|bc7275e0b43ea570e71f7db720c2267e08660472830940bfabb1f26f1bbcf26a
INTERVENTION_LEDGER.md|12801|a674affae79b1b3baf2b9440b3045c864a6c5db30cd561bde3a6322c0cf9713b
PREREGISTRATION.md|16327|bf3af53af9ee99a7e8eec856580bc78e973b8002683c32cdd4e9bc1ffafc6106
TOOLS\combine_controls_r1.py|6858|68dbd7b5eaa675a52c20595fbd667afc6b523acfcb02f978818278ad8e884d55
TOOLS\gamebryo_oracle_r1\.gitignore|19|862263fa1f46c20f0d1e4dac5ffcc75abd55c08211b2c3864c5f8764b9d87793
TOOLS\gamebryo_oracle_r1\adapters\compare\__init__.py|22|90411c8175cfa13874bf03a506b2366a92620957ef844370b38bd5c9247cdf32
TOOLS\gamebryo_oracle_r1\adapters\compare\adapter.py|20041|05fb695af4e835e805867a84fe4395f9990de6491ff1362a810c714a6ef1c8a4
TOOLS\gamebryo_oracle_r1\adapters\gb112\__init__.py|22|90411c8175cfa13874bf03a506b2366a92620957ef844370b38bd5c9247cdf32
TOOLS\gamebryo_oracle_r1\adapters\gb112\adapter.py|10931|e54f6425151ed48405e4cee2ffee2c3a9f8ff50c82f81927d96c31ec0f9ab335
TOOLS\gamebryo_oracle_r1\adapters\gb12\__init__.py|22|90411c8175cfa13874bf03a506b2366a92620957ef844370b38bd5c9247cdf32
TOOLS\gamebryo_oracle_r1\adapters\gb12\adapter.py|4640|46fce9a1969e036f60d48bf05fea9355aa0e1992f1a48feee590d7e2d99b503c
TOOLS\gamebryo_oracle_r1\adapters\gb12\registry.py|6521|8849d55dd1b71ccd08a4b74edd35e4f8c32cc63d51428139e6c4c6855de61d57
TOOLS\gamebryo_oracle_r1\adapters\gb23\__init__.py|22|90411c8175cfa13874bf03a506b2366a92620957ef844370b38bd5c9247cdf32
TOOLS\gamebryo_oracle_r1\adapters\gb23\adapter.py|4934|3bcda25764deaa6d33677e41c1a5242b5006b0410b5dbd29b7bb9def11069453
TOOLS\gamebryo_oracle_r1\adapters\gb26\__init__.py|22|90411c8175cfa13874bf03a506b2366a92620957ef844370b38bd5c9247cdf32
TOOLS\gamebryo_oracle_r1\adapters\gb26\adapter.py|5834|e9b5dc0818ccae52cb0c100512185aa5eb2e66baabdddc17354c873db8cfdc4b
TOOLS\gamebryo_oracle_r1\gb12core.py|146945|9e06eeb5dd8c8f7ef20186b9cadaf7400137752c2c3709f9b61e99f53e48213a
TOOLS\gamebryo_oracle_r1\oracle.py|5409|1d420c57de2f3a6619e3978fc98966605184ae34ef009bb2c538e73ac8d80716
TOOLS\gamebryo_oracle_r1\README.md|17227|1474a09ff737ef04113f6b9b90fcb0694229bda8f785673ea7000b7dad730978
TOOLS\gamebryo_oracle_r1\schemas\comparison_result.schema.json|2368|a95cc1bb8fd88fc20773aa90d966152536d960c821dc1814b2b9fd146f1bfc19
TOOLS\gamebryo_oracle_r1\schemas\oracle_result.schema.json|6797|860c7bd9342507ddaffce39a5252c6671c63cd5074d63aea8178a78d4054d2fb
TOOLS\gamebryo_oracle_r1\tests\test_gb12.py|60479|b1f3fa9097e423978d0df790d4a5120627807b90e86d4c5402fffbf1b992bca7
TOOLS\probe_gb12_oracle_r1.py|14584|cb9602e9db428213c2539d223b617cfe259e807ee2bd2e93c5018ed55df0a0e4
TOOLS\probe_native_transforms_r1.py|11831|093f5d19c6eb1964e3783dd90eb86b7d61fee7eea77cd7fc29a8c91fa814182c
TOOLS\probe_pe_native_r1.py|13824|e03d3e458f7bcd21f1681d48750d729db2d7857f15e69938cb63f480cbe83163
TOOLS\probe_sdk_tools_r1.py|15002|6e43ddbd75f6ed85afa89b8f66628b1727e782c3f881c26335315bcfee203ccf
TOOLS\run_oracle_copy_r1.py|5538|febbf7db9c1a5ed474bba98af13e4c57dddc03b727d6c66bfdde324ccdfd6b13
TOOLS\s01_bnt2_walk_r1.py|10339|60ebc604f3645c839f56d163e6da6c873dc7cf2e5be1ca2d2955d430c39ff65f
TOOLS\s12_corpus_metadata_census_r1.py|20075|483aa7fdca4d4c774a8a904c06036c9d1fbb1b8b6acff8b58fd1c6f1dcb69c1f
TOOLS\s13_selection_extraction_r1.py|15393|6078649ec1d10f7f291bee45b023f8277694d55109e3ee95a07ce0219d1bb60a
TOOLS\s16_parser_native_comparison_r1.py|12872|3ef7e7895be7ee599581bd48c94476fcf0329cf15d13487836c05a6fa4ca482b
TOOLS\s17_scene_structure_and_relations_r1.py|36222|c00ed7326f2f645e0921455c4fdfd556b0b9392a7ecab50daea742d598aa7487
TOOLS\s2_parse_nif101_r1.py|27414|bf45c699b00eefae44ed325c421e7abfa7c1457d7309f443a28ed5631c554b2a
```

NOTE (persistence finalization): the rows above are the run's draft-time
index, CORRECTED at persistence: (1) the COUNTERMODEL_RESULTS.json row now
records the POST-REPAIR identity (13,269 B / 2e159900…), SUPERSEDING the
pre-repair draft row (13,234 B / e687c8f3…) per AMEND_LOG.md Entry 1a — the
QC's single authorized content-preserving line-131/132 JSON repair, adjudicated
REPAIR_ACCEPTED by PE-MASTER; (2) the cm1/cm2/cm3/cm4 raw-output and
gb23-adapter SHA values are the TRUE DISK HASHES re-measured at persistence,
correcting the five draft transcription defects (QC P2-1…P2-5; physical files
byte-unchanged; disk == QC == PE-MASTER independent measurements). The
INTERVENTION_LEDGER.md row above is the ledger state at draft time (its
post-draft identity is covered by the manifest); FINAL_REPORT.md and HANDOFF.md
rows cannot appear here (a file cannot contain its own hash) — all three are
covered by the final manifest. The AUTHORITATIVE full final index =
EVIDENCE_INDEX.md (fresh full-package disk census, this package root) +
MANIFEST_SHA256.csv (generated LAST; covers every physical package file
except the manifest itself — including the QC files under
00_CONTROL_INTERNAL_QC\, QC_REPORT.md, QC_RESULTS.json, AMEND_LOG.md,
PE_MASTER_REVIEW.md, EVIDENCE_INDEX.md and the changed AUDIT_ENTRYPOINT.md).
Local-only payloads are NOT in this index (LOCAL_ONLY_ROOT manifest in the
99_Audits README.md).

## 10. Self-check (executor's OWN, labelled; NOT an independent audit)

- Census denominators: 4,838 + 757 + 1 + 0 = 5,596 ✓ (integrity_ok true;
  historical cross-check identical).
- Selection: 4 distinct ≤ 5 ✓; stock-only pool 0/4,838 with per-type
  evidence ✓; 218757 pin byte-identity ✓; frozen before native/deep
  inspection ✓ (PREREGISTRATION_PE_PHASE.md predates all executions).
- Native: 4/4 NATIVE_LOAD_REJECTED with verbatim logs ✓; populated-scene
  rule applied ✓; identities unchanged before/after ✓.
- Helper: pin match ✓; source inspected before invocation ✓; controls 3/3 ✓;
  behavior differences disclosed ✓; observed error matches source-predicted
  table-order first miss for all four ✓ (kept as separate layers).
- Comparison: four namespaces per input ✓; 218757 ceiling 62+4/66 preserved
  AND reproduced ✓; closure failures retained without replacement ✓.
- Scene structure: namespaces explicit; native pointer/traversal honestly
  NOT_AVAILABLE ✓; FILE_SCENE_SPACE discipline ✓; composed transforms
  cross-checked against an independent parser 5/5 ✓; geometry extraction
  validated against both parsers 14/14 + 102/102 ✓.
- Relations: 1 ≤ 3 comparisons ✓; NO_MATCH_IN_SELECTED_INPUTS non-vacuous ✓.
- Ceiling: all five defaults preserved; no forced positive ✓.
- Repo/base: BASE f99febe unchanged; no commit/push; foreign untracked
  preserved; no orphan processes left (verified).
- Known residual limits honestly listed in section 7.

**The fresh internal QC (PASS_WITH_FINDINGS, 6 P2 + 4 P3, 0 P0/P1) and the
PE-MASTER audit (MASTER_ACCEPTED advisory; P2-6 repair adjudicated
REPAIR_ACCEPTED) are COMPLETE — summary in section 11. This report is not a
qualification of Q1/PE-MASTER authority/M1 or any placement authorization;
CANONICAL_GATE_EFFECT = NONE; DESKTOP_POST_AUDIT = PENDING.**

## 11. Fresh internal QC + PE-MASTER audit summary (persistence finalization)

- **QC_ORIGIN = FRESH_INTERNAL_QC** — pe-master-auditor, fresh session,
  internal to PE-MASTER; NOT an independent Desktop post-audit
  (DESKTOP_POST_AUDIT = PENDING). Full text: QC_REPORT.md + QC_RESULTS.json;
  amendments: AMEND_LOG.md; QC controls and re-execution outputs under
  00_CONTROL_INTERNAL_QC\.
- **QC_VERDICT = PASS_WITH_FINDINGS** (0 × P0, 0 × P1, 6 × P2, 4 × P3).
  Every load-bearing measured claim re-measured by the QC reproduced
  exactly: 14/14 pinned identity re-hashes MATCH; independent BNT2 index
  derivation → UNIQUE_DERIVATION_OK (ordinal 781 / offset 116,223,520 /
  57,316 B / name offset 395,283,797; fresh extraction byte-identical to the
  pin); all 5 countermodel scripts independently re-executed 5/5 with exact
  expected values; own native re-runs of SDK positives, one synthetic
  transform control, PE inputs (218757, 423020) and the helper reproduce the
  executor's outcomes byte-identically; full 5,596-row census CSV re-parse →
  4,838/757/1 versions, 0/4,838 stock-only candidates, compound top-3 ranking
  exact; 62+4/66 ceiling independently reproduced from an own NIF 10.1
  header census; geometry extraction recount 116 = 14 + 102
  EXTRACTED_VALIDATED.
- **Findings and dispositions:**
  - **P2-1…P2-5 (REPORTED by QC → CORRECTED at this persistence
    finalization):** five SHA transcription defects in the §9 draft index
    (cm1 raw output 65-char SHA with an inserted '9'; cm2 one wrong
    character; cm3/cm4 raw outputs and the gb23-adapter copy 63-char SHAs
    with dropped characters). The physical files are byte-unchanged; the true
    hashes were re-measured FROM DISK at persistence and independently
    confirmed by PE-MASTER (disk == QC == PE-MASTER); the §9 rows now carry
    the true identities. Revalidation gate: the regenerated
    EVIDENCE_INDEX.md/MANIFEST_SHA256.csv bijection from fresh disk hashes
    (this file) — fails before the correction, passes after.
  - **P2-6 (REPAIRED by QC under the single authorized in-run repair round;
    adjudicated REPAIR_ACCEPTED by PE-MASTER):** COUNTERMODEL_RESULTS.json
    was not valid JSON (line 131: bare number + unquoted annotation).
    Content-preserving repair: value split into `"countermodels_supplied":
    5,` + a verbatim sibling note (AMEND_LOG.md Entry 1a). PRE 13,234 B /
    e687c8f3… → POST 13,269 B / 2e159900…; strict parse now passes; all 5
    countermodel records + summary intact; the §9 row records the POST-REPAIR
    identity.
  - **P3-1 (REPORTED, documented):** the five raw countermodel outputs
    under countermodels\raw\ carry a UTF-8 BOM (capture artifact); SHA-pinned,
    content valid after the BOM (json.loads with utf-8-sig passes); NOT
    modified (executor evidence; recorded hashes must not be silently
    invalidated).
  - **P3-2 (REPORTED, documented):** the LOCAL_ONLY_ROOT README manifest
    lacks an 01_SDK_fixtures section (fixtures ARE documented repo-side in
    SDK_EXECUTION_RESULTS.json with LOCAL_ONLY paths+SHAs); local-only
    manifest update deferred to a future authorized round.
  - **P3-3 (RESOLVED at persistence):** standalone EVIDENCE_INDEX.md
    generated from a fresh full-package disk census (never copied from the
    draft §9 rows).
  - **P3-4 (RESOLVED by QC):** transient __pycache__ residue created by the
    QC's own import removed immediately; package residue 0 at QC end.
- **PE-MASTER audit: VERDICT = MASTER_ACCEPTED (advisory;
  ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE).** PE-MASTER
  independently re-measured the load-bearing claims (governing-contract
  identity; the census denominators from the CSV columns; the 218757 pin and
  index relation; the five §9 transcription defects by own re-hash; the
  post-repair COUNTERMODEL identity on disk; countermodel scripts/outputs;
  the SDK/PE raw logs and execution records; the placement-ceiling defaults
  in every artifact) and adjudicated the P2-6 repair REPAIR_ACCEPTED. Full
  text: PE_MASTER_REVIEW.md (package root). Q1_STATUS =
  NO_CANONICAL_QUALIFICATION_RECORD per AUDIT_ENTRYPOINT — this verdict is
  advisory, NOT a canonical gate; no milestone effect (EU935-M1 unchanged,
  OPEN).
- No P0/P1 finding ended any capability or phase; no scientific claim was
  changed by any finding (all defects were mechanical/provenance defects
  confined to the draft index and one JSON-syntax record, repaired under the
  authorized round).
