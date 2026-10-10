# PREREGISTRATION — SDK QUALIFICATION PHASE (Work Package B)

RUN_ID = PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009
BASE_SHA = f99febeca9498011fc49f3aef932ecfac4244475 (verified before this phase; unchanged)

**This document is written and frozen BEFORE any native execution of this
phase.** Source inspection (contract section 5) is complete and is recorded
separately in SOURCE_AND_BUILD_IDENTITIES.json + TOOL_CAPABILITY_MATRIX.md;
every expected value below is derived from the inspected SDK SOURCE
(version gates in NiStream.cpp, transform composition in
NiTransform.inl/NiAVObject_Win32.cpp, traversal rules in
NiSceneGraphPrinter.cpp) and/or from the pinned Desktop reports used as
COMPARISON references (PE_GAMEBRYO_SCENE_TOOLS_DEEP_CHECK_20261009,
PE_GAMEBRYO_PLACEMENT_MECHANISMS_LOCAL_RESEARCH_20261009 — both
identity-verified MATCH in this run's INPUT_IDENTITIES.json phase 1).
No printer output of this phase has been observed at the time of writing.

## 1. Execution environment registered before the runs

- Executable (unchanged original, run IN PLACE, read-only):
  `D:\gamebyroengine\extracted\Gb12_Source\Tools\DeveloperTools\SceneGraphPrinter\Win32\VC71\SceneGraphPrinter.exe`
  663552 B, SHA256 fd693af2d713c021b959fc7506200173435307c8fccc24ccd5851dfceb241c7c
  (re-verified this phase; matches contract pin and Desktop identity).
- DLL exposure class: **CHILD_PROCESS_PATH_DLL_EXPOSURE** only. The child
  process PATH gets `D:\gamebyroengine\extracted\Gb112_tools_setup` prepended
  (MSVCP71.DLL df96156f…, MSVCR71.DLL 8094af5e… — re-verified this phase).
  Effectiveness evidence recorded before execution: the printer imports
  MSVCP71.dll and MSVCR71.dll (ASCII import strings present in the exe), and
  NEITHER DLL exists in C:\Windows\System32 or C:\Windows\SysWOW64 → the child
  PATH prepend is the effective resolution mechanism. No installer, no global
  PATH change, no file association, no registry change, no SDK patch.
- Operational controls: per-process timeout 30 s (hang detection; timeout is a
  measured result); SetErrorMode(SEM_FAILCRITICALERRORS|SEM_NOOPENFILEERRORBOX|
  SEM_NOGPFAULTERRORBOX) on the launching python process (inherited by child;
  prevents GUI error dialogs, keeping the run headless); cwd = fixture
  directory (writable LOCAL_ONLY root); stdout/stderr captured as raw files.
- No GUI tool is executed (SceneViewer/SceneDesigner: SOURCE_ONLY).
- No PE asset is opened in this phase (Package C is a later dispatch; SDK
  materials only here).

## 2. Positive SDK controls — expected BEFORE running

All four are run with argv `SceneGraphPrinter.exe -in <input> -trans -extra
-prop -geom -bs -mem` (all six flags exist in the inspected CLI source,
SceneGraphPrinter.cpp:26-36).

| Case | Input (path + SHA measured this phase) | Expected (source-derived) | Desktop comparison (NOT forced) |
|---|---|---|---|
| SDK_DESERT_TOWN | MOUT\Data\DesertTown\DT.NIF 92452794… | exit 0; stderr empty; >=1 numbered visits; Total Object Count >= 1; header version 10.1.0.0 (0x0a010000); user version 0; serialized block count 1226 (own header parse, predicted = Desktop) | visits 388, unique printed addresses 388, depth 6 |
| SDK_DESERT_GROUND | MOUT\Data\DesertTown\DT_Ground.NIF b91cd416… | exit 0; header 10.1.0.0; block count 977 | visits 561, unique 561, depth 7 |
| SDK_TUTORIAL_WORLD | Tutorials\Data\Win32\WORLD.nif 7268f44b… | exit 0; header 10.0.1.18 (0x0a000112); block count 396 | visits 131, unique printed addresses 130, depth 7 |
| SDK_TUTORIAL_OBJECT | Tutorials\Data\Win32\OBJECT.NIF 1eaeef36… | exit 0; header 10.0.1.18; block count 60 | visits 17, unique 16, depth 5 |

Preregistered rules:
- The printer's "Total Object Count" is the count of PrintID calls
  (traversal visits), NOT the serialized block count and NOT unique pointers
  (NiSceneGraphPrinter.cpp:82). Both other counts are measured independently
  (own header parse for serialized blocks; -mem addresses deduplicated for
  unique native pointers).
- Traversal-visits prediction for the same pinned exe + same SHA inputs:
  identical to Desktop (388/561/131/17). Any difference must be explained by
  measured evidence (different input, different flags, or loader nondeterminism
  the difference is evidence of), never forced.
- The parser used for visit summaries must account for ALL numbered visit
  lines. PrintID prints `:<name>` ONLY for NiObjectNET-derived objects
  (NiSceneGraphPrinter.cpp:63-75); NiTimeController derives from NiObject, NOT
  NiObjectNET (NiTimeController.h:26) → controller visit lines have NO
  `:<name>` token. The parser must accept BOTH forms (this is the defect class
  Desktop disclosed for its first parser).

## 3. Six synthetic transform controls — expected BEFORE running

Generated as fresh synthetic NIF 10.1.0.0 graphs by the adapted copy of the
Desktop generator (REUSED CODE, lineage recorded in the script header).
Observation probe: NiCamera ONLY — in this SDK,
NiCamera::UpdateWorldBound sets the world-bound CENTER to the world
TRANSLATION (NiCamera.cpp:267-270); this equivalence is a property of
NiCamera in this source, NOT of arbitrary geometry. The observed value is
therefore the camera's COMPOSED WORLD TRANSLATION after Update(0) (the
printer calls Update(0.0f), SceneGraphPrinter.cpp:146, with
bUpdateControllers=true default, NiAVObject.h:56).

Expected values below are derived BY THIS EXECUTOR from the source transform
composition (NiTransform::operator*, Win32\NiTransform.inl:15-24:
`Tres = Ta + sa*(Ra*Tb); Rres = Ra*Rb; sres = sa*sb`; world = parent.world *
local, NiAVObject_Win32.cpp:22-31), with Rz90 = [[0,-1,0],[1,0,0],[0,0,1]]:

| # | Case | Graph | Expected camera world translation (derived) | Derivation |
|---|---|---|---|---|
| 1 | IDENTITY_PARENT | Root(identity) -> Probe(1,2,3) | (1,2,3) | I*(1,2,3) + 0 |
| 2 | TRANSLATED_PARENT | Root t=(100,200,300) -> Probe | (101,202,303) | (100,200,300) + I*(1,2,3) |
| 3 | ROTATED_SCALED_PARENT | Root t=(100,200,300) R=Rz90 s=2 -> Probe | (96,202,306) | (100,200,300) + 2*(Rz90*(1,2,3)) = (100,200,300)+2*(-2,1,3) |
| 4 | THREE_LEVEL_SOCKET | WorldRoot(t100,200,300,Rz90,s2) -> Socket(t10,20,30,s0.5) -> Probe | (58,221,363) | Socket world=(60,220,360); Probe=(60,220,360)+1*(Rz90*(1,2,3)) |
| 5 | LEAF_SCALE_SEPARATE | Root t=(100,200,300) -> Probe s=9 | (101,202,303) | leaf scale does not enter its own translate composition |
| 6 | TWO_PARENTS_LAST_LINK_WINS | Root -> ParentA(t100,0,0)->Probe AND Root -> ParentB(t0,200,0)->Probe | (1,202,3) | last link detaches from ParentA (NiAVObject::AttachParent, NiAVObject.cpp:62-69) → parent = ParentB |

- These six expected values are additionally consistent with the pinned
  Desktop PLACEMENT_MECHANISMS report table (comparison input; not the source
  of the derivation).
- Case 6 is a deliberately conflicting-graph DIAGNOSTIC, not a claim of valid
  authoring practice (registered label). Preregistered traversal prediction
  for case 6: 4 visits (Root, ParentA, ParentB, Probe-under-ParentB), because
  the second AttachChild removes the child from ParentA's runtime array.
- PASS rule per case: exit 0 AND observed -bs camera world-bound center equals
  the expected triple (float compare after text parse).

## 4. Negative SDK-copy inputs + missing file + empty scene — expected BEFORE running

Mutations are made ONLY on fresh LOCAL_ONLY copies of
`Samples\Tutorials\Data\Win32\OBJECT.NIF` (never on the SDK original; the SDK
tree stays read-only). For each mutation this phase records: changed offsets,
original bytes, new bytes, intended failure, actual outcome. Fixture bytes
stay LOCAL_ONLY (proprietary-derived); only metadata/logs enter the repo
package.

| # | Case | Mutation (registered before execution) | Intended failure | Expected observation (source-derived) |
|---|---|---|---|---|
| N1 | SYNTH_UNKNOWN_CLASS | equal-length class-name substitution in the type table: `NiNode` -> `QzNode` (2 bytes) | missing factory at LoadRTTI (NiStream.cpp:427-433 → RTTIError, NO_CREATE_FUNCTION) | exit 1; stderr `Error loading stream.`; stdout empty (stock printer never calls GetLastErrorMessage, SceneGraphPrinter.cpp:127-131) |
| N2 | SYNTH_USER_VERSION_1 | user-defined version field 0 -> 1 (1 byte; file is 10.0.1.18 >= 10.0.1.8 so the field is read) | header gate (NiStream.cpp:347-352, ms_uiNifMaxUserDefinedVersion = 0) | exit 1; stderr `Error loading stream.` |
| N3 | SYNTH_TOO_NEW_BINARY_VERSION | version field -> 0x14020007 (20.2.0.7 > 10.2.0.0) (4 bytes) | header gate LATER_VERSION (NiStream.cpp:327-332) | exit 1; stderr `Error loading stream.` |
| N4 | SYNTH_BAD_HEADER_TEXT | overwrite the first header line bytes with `X` (39 bytes) | LoadHeader "File Format" substring check fails (NiStream.cpp:311-316) | exit 1; stderr `Error loading stream.` |
| N5 | MISSING_INPUT | reference to a nonexistent file | NiFile open failure (NiStream.cpp:647-653 FILE_NOT_LOADED) | exit 1; stderr `Error loading stream.` |
| N6 | SYNTH_EMPTY_SCENE | own minimal NIF 10.1.0.0, 0 objects, 0 type entries, 0 groups payload, 0 top-level refs | empty top-level list (SceneGraphPrinter.cpp:135-139) | **exit 0**; stdout empty; stderr `No top-level file objects.` |

Preregistered classification rules:
- N1-N5 all print the same generic message in the stock binary. The
  source-predicted SPECIFIC cause (missing factory vs version gate vs open
  failure) is labeled SOURCE_PREDICTED and kept separate from the OBSERVED
  native output. The stock binary alone cannot distinguish them
  (GetLastErrorMessage is never printed by this main).
- N6 (empty scene + exit 0) must NOT count as a populated scene inspection.
  Preregistered gate rule: an inspection counts as populated only when exit 0
  AND at least one numbered visit line AND a nonzero Total Object Count are
  present. N6 is an honest empty-behavior classification, not a success.
- Timeout/crash of any run = measured result, recorded as such.

## 5. Qualification gate criteria (registered BEFORE execution, contract section 7)

The printer is qualified for application to PE inputs (Package C, later
phase) only if ALL of:
1. Executable identity valid (size + SHA256 match the pin; unchanged after
   all runs).
2. Required SDK positive controls reproducible (all 4 exit 0, populated
   traversals, counts measured and consistent with the same-exe/same-input
   expectation; differences explained by evidence).
3. Synthetic transform calculations understood (6/6 expected-vs-observed
   matches, with the NiCamera-only scope of the bound-center observation
   labeled).
4. Stdout parser accounts for ALL numbered visits (both PrintID forms;
   unaccounted numbered lines = parser gap = FAIL of this criterion).
5. Negative/empty behavior honestly classified (N1-N6 as registered, with
   empty-vs-populated distinction enforced).
If any criterion fails: record the blocker; Package C will not run.

No universal TOOL_PASS is assigned; per-capability verdicts live in
TOOL_CAPABILITY_MATRIX.md.

## 6. What is NOT executed / NOT claimed (registered)

- No SceneViewer/SceneDesigner GUI execution (SOURCE_ONLY capabilities).
- No renderer, registry, driver or environment repair loop.
- No PE NIF, Models.bnt or any PCG asset access in this phase.
- No commit, no push, no AUDIT_ENTRYPOINT edit (later phases).
- Traversal counts are measured, not forced; deviations from Desktop values
  get evidence-based explanations.
