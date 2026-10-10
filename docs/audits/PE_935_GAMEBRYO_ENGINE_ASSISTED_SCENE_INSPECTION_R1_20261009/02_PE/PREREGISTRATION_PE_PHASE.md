# PREREGISTRATION — PE INPUT CENSUS, MECHANICAL SELECTION AND NATIVE INSPECTION (Work Package C)

RUN_ID = PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009
PHASE = 02_PE (contract sections 8–14)
BASE_SHA = f99febeca9498011fc49f3aef932ecfac4244475 (unchanged; verified by this executor before writing this file)

**This document is written and frozen BEFORE the Package C science (corpus census
execution, candidate selection, PE native execution, oracle comparison, scene
analysis).** Package A (records correction) and Package B (SDK qualification)
are already complete; their artifacts (00_RECORDS_CORRECTION/, 01_SDK/) are
READ_ONLY for this phase. TOOL_QUALIFICATION_GATE = PASS with scope (stock
SceneGraphPrinter fd693af2…41c7c, headless structural inspection, SDK/synthetic
inputs; specificity FAIL preserved: one generic load-error message; -trans local,
-bs world bound, -extra class names only, -mem SDK-process addresses).

## 1. Inputs and tools (pinned, re-verified by this executor before this file)

- Contract: SHA256 63E093D22E6DA1A339F953977A21D4808300724FB6A91999A53C271E3D1A5753, 32125 B. VERIFIED.
- Models.bnt: D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt, 395412868 B, SHA256 C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0. VERIFIED.
- 218757 pin: D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox\payloads\218757.nif, 57316 B, SHA256 3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36. VERIFIED.
- Stock printer: SceneGraphPrinter.exe fd693af2d713c021b959fc7506200173435307c8fccc24ccd5851dfceb241c7c (663552 B). To be re-hashed immediately before AND after the native runs.
- DLLs (child-PATH only): MSVCP71.DLL df96156f…23b, MSVCR71.DLL 8094af5e…fefe (D:\gamebyroengine\extracted\Gb112_tools_setup).
- Historical index cross-checks (NOT extraction authority): 218757.nif entry 781, payload offset 116223520, length 57316, name offset 395283797; index_start 395262727, count 5596; anchor "296445.nif" name@395268773.

## 2. Census method (contract section 8) — registered BEFORE execution

- Reader: COPIES of the existing documented BNT2 walker
  `docs/audits/PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915/00_CONTROL/scripts/s01_bnt2_walk.py`
  (verbatim byte-copy into this run's TOOLS/; canonical file READ_ONLY; SHA256 of
  the canonical and the copy recorded in SELECTION_AND_EXTRACTION_PROVENANCE.json).
  Its bounds/identity checks reviewed this phase: footer magic BNT2 at EOF-8;
  u32 dir_offset bounds; NumEntries sanity; per-entry ASCII-name (<=260 B,
  0x0A-terminated), no duplicate names; 16-byte entry {u32 size, u32 offset,
  u32 field_c, u32 field_d}; size>0; offset+size <= dir_offset; EOF-exact index
  closure; footer repeat check; payload overlap check.
- Calibration (fail-closed; must reproduce before any target trust): Models.bnt
  index_start 395262727, count 5596, anchor name offset 395268773; entry 781 =
  218757.nif size 57316 offset 116223520; entry name offset 395283797. Any
  mismatch aborts the census.
- Negative controls (s01's own battery, on synthetic archives only): NC_BASE
  valid synthetic must PASS; NC_TRUNCATE must FAIL; NC_CORRUPT_COUNT must FAIL;
  NC_WRONG_ENDIAN must FAIL. All four run before the Models.bnt census is trusted.
- Per entry: payload read at index-proven offset/size; zlib-magic check (78 xx)
  with decompress-or-record; header line (0x0A-terminated ASCII <=256) + version
  u32 (version field is demonstrated readable for ALL 5,596 entries by the
  historical s02 scan; re-demonstrated by this run — a parse failure is recorded
  as a failure, never zeroed).
- Type/object histogram: for NIF 10.1.0.0 (version u32 0x0A010000) via the
  documented s03 `scan_101_header` layout (user version u32, num blocks u32,
  num block types u16, SizedString type names with [1,256]-byte bounds, u16
  type indices with bounds check, num groups u32 + group sizes). Demonstrated
  support: historical s03 scanned the whole 10.1 subset with 0 failures; the
  layout is the same 10.1 header the SDK-qualified positive controls use.
- Versions 4.1.0.12 / 4.0.0.2 (and any other): header line + version u32
  readable; TYPE/OBJECT HISTOGRAM = HEADER_UNSUPPORTED (the 10.1 type-table
  layout does not apply; no demonstrated header-level type-table support for
  the 4.x inline layout in this lineage). Recorded as HEADER_UNSUPPORTED,
  never as zero counts.
- Census output: 02_PE/CORPUS_METADATA_CENSUS.csv — one row per INDEXED entry:
  name, index ordinal, payload offset/length, compression, header line,
  version u32 + label, user version (10.1 only), num blocks, num block types,
  compact type histogram (10.1 only), scan status (SCANNED / HEADER_UNSUPPORTED
  / FAILED+reason). Full per-file histograms stay LOCAL_ONLY. Denominator:
  SCANNED + HEADER_UNSUPPORTED + FAILED == 5596 required.

## 3. Mechanical selection rules (contract section 8) — FROZEN BEFORE any
native/deep inspection; the ranked shortlist and selected pins are written to
02_PE/SELECTION_AND_EXTRACTION_PROVENANCE.json before the first native run

- (a) MANDATORY: 218757.nif (fresh extraction from the pinned BNT; byte identity
  with the pin SHA256 3E8A22C2…CF36 REQUIRED — mismatch aborts the phase).
- (b) STOCK-ONLY candidate (at most one): pool = indexed entries whose version
  u32 is inside the SDK accepted range [0x0330000B .. 0x0A020000] (= 3.3.0.11 ..
  10.2.0.0), user version 0 where the field applies, AND whose COMPLETE declared
  type table (10.1 layout only — 4.x tables are not header-readable, so 4.x
  entries cannot demonstrate a complete registered table) is fully contained in
  the measured stock registry GB12_REGISTERED_CLASSES (198 names, from
  tools/gamebryo_oracle/adapters/gb12/registry.py; the same SDK-source-derived
  registry qualified in Package B; zero NiArk* present). Selection: smallest
  payload, then lexicographically smallest name. If the pool is empty:
  NO_STOCK_ONLY_CANDIDATE (no NiArk removal to manufacture one).
- (c) COMPOUND-SCENE candidates (up to three): pool = NIF 10.1.0.0 entries with
  >= 4 declared NiNode OBJECT references AND >= 2 NiTriShape OBJECT references
  (object counts from the header type-index histogram — NEVER type-table entry
  counts; the two are explicitly not equated). Rank: NiNode object count DESC,
  then NiTriShape count DESC, then payload size DESC, then name ASC. Top 3.
  LABEL: this ranks compound STRUCTURE, not proven world scenes.
- Deduplication: 218757 is removed from pools (b)/(c) if present; a payload
  selected in one category is not selected twice. HARD MAX = 5 distinct PE NIFs.
- If a chosen candidate fails at any later stage, the outcome is RETAINED — no
  replacement with the next-ranked candidate to chase a success.

## 4. Native execution rules (contract section 9) — registered BEFORE execution

- Tool: the qualified stock printer only, on UNCHANGED local copies of the
  fresh extractions (LOCAL_ONLY). argv: -in <payload> -trans -extra -prop
  -geom -bs -mem. cwd: this run's LOCAL_ONLY payload directory. DLL exposure:
  CHILD_PROCESS_PATH_DLL_EXPOSURE (child PATH prepend only, no global change).
  Per-process timeout 30 s; CREATE_NO_WINDOW; launcher SetErrorMode as in
  Package B. Provenance captured per run: argv, cwd, env delta, input SHA, exe
  SHA, exit code, raw stdout/stderr paths, timeout flag. Tool/DLL hashes
  re-verified after all runs; payload copies re-hashed before and after.
- POPULATED SCENE rule (from Package B, preregistered there and inherited):
  a populated native inspection requires exit 0 AND >= 1 numbered visit row AND
  nonzero reported Total Object Count. Empty output + exit 0 is NOT a populated
  inspection. Exit 0 alone is never sufficient.
- Expected results (HISTORICAL EXPECTATIONS, to be measured):
  - 218757.nif: four NiArk blocks in the serialized table
    (NiArkAnimationExtraData, NiArkImporterExtraData, NiArkTextureExtraData,
    NiArkViewportInfoExtraData — prior parse); the stock registry contains zero
    NiArk* classes, so the source-derived expectation is a missing-factory
    RTTIError with the generic "Error loading stream." on stderr + exit 1.
    Expected classification: NATIVE_LOAD_REJECTED with UNSPECIFIED cause from
    the binary alone (specificity FAIL, Package B C11). The source-predicted
    first missing factory (table order: NiArkAnimationExtraData) is labeled
    SEPARATELY as SOURCE_PREDICTED, never as an observed native report.
    A different native outcome (e.g. success) is recorded as measured, with the
    deviation explained.
  - Stock-only candidate: unknown until measured; class-table completeness +
    version gating make a successful load PLAUSIBLE, but LoadBinary/link
    failures remain possible and will be retained as measured.
  - Compound candidates: unknown; PE 10.1 exporter files commonly contain
    NiArk* blocks, making native rejection PLAUSIBLE for many. Retained as
    measured either way.

## 5. Parser/native comparison rules (contract section 10) — registered BEFORE execution

- Canonical tools/gamebryo_oracle is READ_ONLY; COPIES run from this run's
  TOOLS/gamebryo_oracle_r1/ with all output redirected to this run's paths.
  Copy identity vs canonical recorded (per-file SHA256).
- Four namespaces per input, per block/claim, kept DISTINCT:
  ORIGINAL_NATIVE_EXECUTION | SOURCE_PREDICTED_ORIGINAL_VERDICT |
  OUR_PARSER_RESULT | OUR_EXTENSION_CONTINUATION.
- For 218757: prior ceiling PRESERVED — 66 accounted blocks = 62 semantic +
  4 opaque (the 4 NiArk blocks). Boundary accounting is NOT promoted to
  semantic decodes unless new INDEPENDENTLY supported evidence changes a
  particular block (then documented exactly which and why).
- Known residual oracle defects F3–F7/O1/T3 or a new crash do NOT authorize
  general hardening: capture the exception + affected capability. At most ONE
  small run-local inspection-wrapper repair cycle (in this run's package,
  never canonical tools). An unknown offset stops dependent parsing.

## 6. Optional native inspector (contract section 11) — decision registered BEFORE execution

Default: NOT_BUILT. The required distinctions (specific load-error cause,
post-Update local TRS, ExtraData values) are either (i) already exposed by the
qualified stock printer + serialized parser combination, or (ii) not required
by the contract's PE-world default ceiling (section 14). A helper is built or
invoked ONLY if a REQUIRED distinction cannot be exposed otherwise; any helper
must first pass the relevant SDK/synthetic controls and disclose every behavior
difference. The optional gb12_oracle.exe (dd7112a4…046c) is NOT the unmodified
vendor printer; if invoked at all, its local source/build provenance and
actual interface are inspected FIRST and its class is recorded in
INTERVENTION_LEDGER.md.

## 7. Scene analysis and placement ceiling (contract sections 12–14)

- Typed graph per safely inspectable asset with namespaces: native pointer /
  traversal ID / serialized block ID — DISTINCT; a missing map entry stays
  UNMAPPED. Edge kinds: TOP_LEVEL_ROOT, SCENE_CHILD, CONTROLLER, PROPERTY,
  EXTRA_DATA, RESOURCE_REFERENCE, UNKNOWN. Text indentation alone does NOT
  establish SCENE_CHILD (controller edges print indented too — Package B C6).
- FILE_SCENE_SPACE discipline: the world coordinate system of an SDK-loaded
  scene is FILE_SCENE_SPACE until an independent PE world/root relation is
  established. NO PE axis swap, cm/m conversion or ×100 scale imported from
  any other engine/format/UI/source example. For 218757: NO historical
  location derived from dimensions [2500,1250,3350], native pointer values or
  a zero root transform.
- Default science ceiling (unless a genuinely new positive with exact physical
  instance/source identity, asset relation, complete transform chain and
  world-frame provenance appears — do NOT force it):
  MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED; HISTORICAL_WORLD_INSTANCE =
  NOT_ESTABLISHED; PE_WORLD_ROOT_IDENTITY = NOT_ESTABLISHED;
  PE_AXES_AND_UNITS = UNVERIFIED; WORLD_XYZ_RECOVERED = NO.

## 8. Bounded 218757 comparison (contract section 13) — registered BEFORE execution

- If safe decoding provides geometry for 218757 and a selected compound
  candidate: exact geometry fingerprints (documented fields + canonicalization):
  vertex positions, triangle indices, geometry counts, independently checked
  local structure. AT MOST THREE candidate comparisons. Original arrays and
  reconstructed meshes stay LOCAL_ONLY; published output = identities, counts,
  fingerprints, graph paths, evidence locators, concise transform summaries.
- PARTIAL_GEOMETRY_MATCH reported separately from complete asset-subtree
  correspondence. Exact shared geometry does NOT establish the same runtime
  instance or historical building. No fuzzy threshold widening, no
  texture/name-only identity, no plausible-coordinate acceptance. No match →
  NO_MATCH_IN_SELECTED_INPUTS (which does not exclude baked/re-exported models,
  different asset IDs, other containers, nonlocal instance sources,
  network-delivered instances; no candidate-set expansion).

## 9. Hard constraints reconfirmed (contract sections 9–14 bind)

No NIF version/user version alteration, no block removal, no class replacement,
no guessed-length padding, no Load-failure suppression, no NifConvert, no
convert/save of originals, no new PCG callgraph/RTTI/animation/CMO/network
experiment, no client launch, no renderer/registry/driver repair loop, no GUI
startup. Proprietary payloads never committed (LOCAL_ONLY + manifest in
LOCAL_ONLY_ROOT). Missing evidence = NOT_MEASURED. Timeout/crash = measured
result. Original PE container/SDK trees never modified (hash re-verification
after all runs).
