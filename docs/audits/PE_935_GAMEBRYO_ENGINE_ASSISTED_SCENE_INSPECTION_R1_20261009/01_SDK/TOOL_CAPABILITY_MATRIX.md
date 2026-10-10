# TOOL_CAPABILITY_MATRIX — SDK_QUALIFICATION (Work Package B)

RUN_ID = PE_935_GAMEBRYO_ENGINE_ASSISTED_SCENE_INSPECTION_R1_20261009
BASE_SHA = f99febeca9498011fc49f3aef932ecfac4244475 (unchanged)

Tool under qualification: the ORIGINAL vendor binary
`D:\gamebyroengine\extracted\Gb12_Source\Tools\DeveloperTools\SceneGraphPrinter\Win32\VC71\SceneGraphPrinter.exe`
(663552 B, SHA256 fd693af2d713c021b959fc7506200173435307c8fccc24ccd5851dfceb241c7c;
 identity valid against the contract pin and re-verified unchanged AFTER all runs by an
independent process).

Evidence layers used in this matrix (kept distinct):
- **SRC** = inspected SDK source (file:line locators in SOURCE_AND_BUILD_IDENTITIES.json).
- **RT** = runtime observations of THIS phase (01_SDK/SDK_EXECUTION_RESULTS.json,
  01_SDK/SYNTHETIC_AND_NEGATIVE_CONTROLS.json, raw logs under 01_SDK/raw/).
- **DESK** = pinned Desktop reports, used as COMPARISON inputs only (identity-verified).

Verdicts used: PASS / FAIL / NOT_TESTED / SOURCE_ONLY. **No universal TOOL_PASS is
assigned.** A capability verdict applies to THIS pinned executable on THESE inputs.

---

## Part 1 — Capabilities

### C1. Headless execution — **PASS** (RT)
16 native executions in total this phase: 4 positives, 4 mutated negatives,
1 missing-file, 1 empty scene (probe_sdk_tools_r1.py) + 6 synthetic
(probe_native_transforms_r1.py). All with `CREATE_NO_WINDOW`, no GUI, no renderer.
All exited normally (no timeout, no crash, no hang at the 30 s per-process
timeout). No installer, no global PATH change, no registry change, no
SDK-original patch; DLL exposure was child-process PATH only (see INTERVENTION_LEDGER
entry 2).

### C2. Flag effects (measured on the pinned binary; each = a separate capability)

| Flag | Real effect (SRC + RT) | Verdict |
|---|---|---|
| `-in` | required input path; missing `-in` → usage on stderr + exit 1 (SceneGraphPrinter.cpp:101-105) | PASS |
| `-trans` | prints the object's LOCAL Rotate rows / Translate / Scale via `GetRotate/GetTranslate/GetScale` (NiSceneGraphPrinter.cpp:100-125) — **LOCAL getters, not world translate**. RT: in every synthetic case the camera's `-trans` Translate stayed the serialized local (1,2,3) while its composed world translation was different (e.g. TRANSLATED_PARENT: local `<1,2,3>` vs world `(101,202,303)`, raw log `TRANSLATED_PARENT.stdout.txt`). | PASS |
| `-bs` | prints `World Bound: C <x,y,z>, R r` from `GetWorldBound()` — a **WORLD BOUNDING SPHERE**, not a building pivot and not a position getter (NiSceneGraphPrinter.cpp:127-138). For NiCamera ONLY this SDK sets bound center = world translation (NiCamera.cpp:267-270) — used as the synthetic probe; this equivalence is NOT generalized to arbitrary geometry. | PASS |
| `-extra` | prints each ExtraData's **CLASS NAME only** (`GetExtraDataAt(i)->GetRTTI()->GetName()`, NiSceneGraphPrinter.cpp:163-178) — no values, no fields. (Values are exposed via `GetViewerStrings` in SceneViewer's ExtraDataDlg — SOURCE_ONLY, see C15.) | PASS |
| `-prop` | prints property **class names** from the object's property list (NiSceneGraphPrinter.cpp:140-161); no values, no recursion into properties. | PASS |
| `-geom` | prints per-geometry model-data summary: vertex count (active), NORMALS/COLORS/UVS flags, SKINNED marker, triangle count; plus TriShape/TriStrips aggregate summary (NiSceneGraphPrinter.cpp:180-277, 349-378). | PASS |
| `-mem` | prints the SDK-process address of each visited native object (` <0x...>`, NiSceneGraphPrinter.cpp:77-78). **These are SDK-process heap addresses — NOT PCG pointers, block IDs or asset IDs**; they are per-run values (compare DT run `0x00D5E648`-style addresses) and cannot be treated as serialized identity. | PASS |
| `-ac` | shows AppCulled status (source-supported; not part of the required flag set this phase) | NOT_TESTED |
| `-ts N` | tab-stop width (source-supported) | NOT_TESTED |

### C3. Serialized-field exposure — **FAIL** (as a capability of this tool; honest scope)
The printer never prints serialized fields. Everything printed is post-load NATIVE
state: the loader has already run factory creation, LoadBinary, LinkObject,
PostLinkObject, registered post-process converters (NiOldAnimationConverter for
version < 10.1.0.104, NiAnimationSDM.cpp:105) and selective-update flag fixups
(NiStream.cpp:821-841) before the first line is printed. Serialized state is
recoverable only by an independent parser (OUR_PARSER layer, Package C) or by
diffing against raw bytes. The stock printer alone exposes ZERO serialized fields.

### C4. Native-object exposure — **PASS** (with scope)
Prints, per visited object: runtime RTTI class name, NiObjectNET name (if any),
-process address (-mem), local TRS (-trans), world bound (-bs), property class
names (-prop), ExtraData class names (-extra), geometry summary (-geom).
Scope limits (measured + source): no field-level introspection, no serialized
block index (the printer never prints the block ordinal — a block-index↔visit
mapping requires an independent parser), no pre-Update state.

### C5. Post-Update state — **PASS** (with one honest sub-limit)
The printer calls `Update(0.0f)` on every top-level NiAVObject before printing
(SceneGraphPrinter.cpp:146). `Update` defaults to `bUpdateControllers=true`
(NiAVObject.h:56), so controllers RUN at time 0 (source-CONFIRMED);
`UpdateWorldData` recomputes `m_kWorld = parent.m_kWorld * m_kLocal`
(NiAVObject_Win32.cpp:22-31) and `UpdateWorldBound` recomputes bounds.
RT: all four positives contain live controllers (e.g. DT.NIF printed 9
NiTransformController, 13 NiGeomMorpherController) and completed with composed
bounds; the six synthetic controls show composed world state consistent with the
composition source.
Sub-limit: whether a SPECIFIC controller changed a SPECIFIC value at Update(0) is
NOT_MEASURED — the stock printer cannot show pre-Update state, so PRE/POST value
comparison is impossible with this tool (would require the optional inspector of
contract section 11).

### C6. Traversal edges — **PASS** (measured; indentation is NOT always scene-child)
Edges followed (SRC, NiSceneGraphPrinter.cpp:279-336): (a) all TOP-LEVEL objects
of the stream (`GetObjectAt(i)`, SceneGraphPrinter.cpp:141-149 — ANY NiObject class,
not only NiAVObject; non-NiAVObject roots are printed without Update);
(b) CONTROLLERS — for every visited NiObjectNET, the full `GetControllers()` chain
is recursed at indent+1 (305-312); (c) SCENE CHILDREN — for every visited NiNode,
all children via `GetAt(i)` at indent+1 (321-335). Edges NOT followed: properties
(only names listed inline), ExtraData (only class names listed inline), other
references (geometry model data is summarized but not traversed; controller
targets/interpolators are not traversed).
RT concretely: DT.NIF printed controllers WITHOUT `:<name>` tokens (NiTimeController
derives from NiObject, NOT NiObjectNET — NiTimeController.h:26), and the visit
histogram contains pure controller classes (NiGeomMorpherController=13,
NiLightColorController=5, NiPSys*Ctlr classes). A nested indented line is a
controller edge OR a scene-child edge; text indentation alone does not establish
SCENE_CHILD.
RT bonus: in WORLD.nif and OBJECT.NIF the SAME NiCamera object appears BOTH as a
top-level root (depth 0) AND as a scene child (depth 2) — 131 visits vs 130 unique
addresses (WORLD, camera "Camera" 0x00C26920) and 17 vs 16 (OBJECT, "HeliCam"
0x024292B0).

### C7. Count semantics — **PASS** (three DISTINCT namespaces, all measured)
- **Serialized block count**: from the file header (own header parse, reused
  bounded parser): DT=1226, DT_Ground=977, WORLD=396, OBJECT=60. The stock printer
  NEVER prints this number.
- **Traversal visits ("Total Object Count")**: ms_uiObjectCount increments on every
  PrintID call with NO deduplication and no block-count relation
  (NiSceneGraphPrinter.cpp:82): DT=388, DT_Ground=561, WORLD=131, OBJECT=17 —
  identical to the Desktop comparison values (same pinned exe + same SHA inputs →
  deterministic reproduction; differences = 0, nothing to explain beyond
  determinism).
- **Unique native pointers**: deduplicated `-mem` addresses: DT=388, DT_Ground=561,
  WORLD=130, OBJECT=16. The visit>unique deltas are revisits (same object reached
  as top-level root AND as child, see C6) — NOT missing objects and NOT errors.
- **"Tree Depth"** = max indent + 1 (NiSceneGraphPrinter.cpp:83-84, 340-341): 6/7/7/5 —
  matches Desktop.
A class-table ENTRY (e.g. `NiNode=113` in DT's serialized census) is a type
declaration count, not an object-reference count; the printed census is the
VISIT census (DT printed NiNode=113 visits, equal here by coincidence of
structure — never assumed).

### C8. Local vs composed world transforms — **PASS** (measured, both directions)
`-trans` = LOCAL member getters (C2). Composed world transforms are NOT printed by
the stock printer (no GetWorldTranslate output; that exists in SceneViewer's
WorldTransformsDlg — SOURCE_ONLY). For NiCamera ONLY, `-bs` center = world
translation (source fact). Six synthetic controls measured expected-vs-observed:
IDENTITY_PARENT (1,2,3); TRANSLATED_PARENT (101,202,303);
ROTATED_SCALED_PARENT (96,202,306); THREE_LEVEL_SOCKET (58,221,363);
LEAF_SCALE_SEPARATE (101,202,303); TWO_PARENTS_LAST_LINK_WINS (1,202,3) — **6/6
PASS**, all visit-count predictions (2/2/2/3/2/4) also matched. The composition
math is understood from source (NiTransform.inl:15-24: `T_res = T_a +
s_a·(R_a·T_b)`) and confirmed by runtime.

### C9. Bounds — **PASS** (as bounds only)
`-bs` prints the WORLD bounding sphere (center+radius) of each visited NiAVObject.
A bounds center is NOT a pivot, NOT a placement, NOT a world position of the
object's origin (NiNode bounds are merges of visual children, NiNode.cpp:243-272;
NiCamera bounds center is its world translation by class-specific source behavior).
Bounds may be zero-radius (e.g. pure transform nodes: synthetic raw logs show
`R 0` on NiNodes without visual children) — `IsVisualObject` = radius != 0
(NiAVObject.inl:232-235).

### C10. Version/class knowledge + rejection specificity — **PASS** (measured)
Accepted NIF version range of this binary: [GetVersion(3,3,0,11) …
GetVersion(10,2,0,0)] (NiStream.cpp:42-46 + NiVersion.h: GAMEBRYO 1.2.2.6 → NIF
10.2.0.0). User-defined version must be exactly 0 for files ≥ 10.0.1.8 (bounds are
both GetVersion(0,0,0,0), NiStream.cpp:47-50) — measured: all four positives have
user version 0; the user-version-1 mutant was rejected. PE NIF 10.1.0.0 with user
version 0 is INSIDE this range (relevant for Package C).
Loader aliases (source) with RUNTIME CONFIRMATION: `NiKeyframeController` →
`NiTransformController`, `NiKeyframeData` → `NiTransformData`, `NiVisData` →
`NiBoolData` (NiAnimationSDM.cpp:65-72, 100-103). RT: DT.NIF's serialized type
table contains NiKeyframeController=9 (own header parse) and the printed census
shows NiTransformController=9; OBJECT.NIF 2→2. **File class ≠ native runtime
class** — a printed class name is NOT the serialized class name.
Rejection points (source): header text gate (NOT_NIF_FILE), version gates
(OLDER/LATER), user-version gate, missing-factory at LoadRTTI (NO_CREATE_FUNCTION),
file-open failure (FILE_NOT_LOADED). All five were exercised this phase (see C14).

### C11. Error specificity (stock binary) — **FAIL** (measured, honest)
The stream records SPECIFIC causes (`m_uiLastError` + `m_acLastErrorMessage`,
e.g. `"<class>: cannot find create function."`, NiStream.cpp:387-400) — but the
stock printer main NEVER calls GetLastErrorMessage; it prints ONLY
`"Error loading stream."` on stderr and exits 1 for EVERY load failure
(SceneGraphPrinter.cpp:127-131). RT: all five negative inputs (unknown class,
user version, too-new version, bad header text, missing file) produced the
IDENTICAL generic message + exit 1. The missing-factory identification is
SOURCE_PREDICTED (RTTIError path), not observed in the stock output. Specific
error surfacing exists in SceneViewer's NifDoc (GetLastErrorMessage in a message
box, NifDoc.cpp:574-583) — SOURCE_ONLY, GUI not executed.

### C12. In-memory / on-disk mutation — **PASS** (measured: nothing on disk; in-memory load conversion understood)
On disk: ZERO writes by the tool. Verified: printer exe + both DLLs + all four SDK
samples re-hashed UNCHANGED after all 16 executions (independent process). The
code path that could write a log (`NiSceneGraphPrinter::OpenLog` →
NiSceneGraph.txt) is never called by this main.
In memory (within the tool's own process, which then exits): load-time
representation conversions — factory creation, legacy loader aliases
(NiKeyframeController→NiTransformController), version-conditional reconstruction
(NiTransformController::LinkObject creates a NiTransformInterpolator for files
< 10.1.0.104, NiTransformController.cpp:165-178), the registered
NiOldAnimationConverter::Convert post-process for files < 10.1.0.104 (creates new
runtime controller objects), selective-update flag fixups for files < 4.1.0.12
(NiStream.cpp:821-841), and Update(0) recomputing world transforms/bounds. None of
this modifies the input file or any persistent state.

### C13. Update(0) controller behavior — **PASS** (execution) + NOT_MEASURED (per-value mutation)
Source: Update(0.0f) with bUpdateControllers=true runs property controllers and
the GetControllers() chain at time 0 (NiAVObject.h:56; NiAVObject.inl:237-253).
Execution: confirmed the printer performs this Update on every NiAVObject root
(all runs exited 0 with controller-populated scenes). Per-value PRE/POST mutation
measurement is NOT possible with the stock tool (no pre-state access) — recorded
as NOT_MEASURED, not as "no mutation". Note for PE work: printed `-trans` values
are therefore POST-Update(0) local state — a controller COULD have changed them;
they are not guaranteed raw serialized local TRS.

### C14. Negative/empty behavior classification — **PASS** (all 6 measured, honestly classified)
| Case | Mutation (offsets/bytes in SYNTHETIC_AND_NEGATIVE_CONTROLS.json) | Intended (source-predicted) | Actual |
|---|---|---|---|
| Unknown class (QzNode) | 2 bytes in OBJECT.NIF type-table copy | missing factory at LoadRTTI | exit 1, `Error loading stream.`, stdout empty |
| User version 1 | 1 byte | user-version gate | exit 1, same message |
| Version 20.2.0.7 | 4 bytes | LATER_VERSION gate | exit 1, same message |
| Bad header text | 39 bytes overwritten with `X` | NOT_NIF_FILE gate | exit 1, same message |
| Missing file | no file | FILE_NOT_LOADED | exit 1, same message |
| Empty scene | own minimal NIF, 0 objects/0 roots | empty top-level list | **exit 0**, stdout empty, stderr `No top-level file objects.` |
**Empty scene + exit 0 does NOT count as a populated scene inspection** (preregistered
gate rule: populated requires exit 0 AND ≥1 numbered visit AND nonzero Total Object
Count; the empty case has none of these). The stock binary's identical generic
message for all five failures is a measured specificity limit (see C11).

### C15. SceneViewer/SceneDesigner capabilities — **SOURCE_ONLY** (not executed, per contract)
SceneViewer source contains: world-transform display (WorldTransformsDlg.cpp:64-118,
GetWorldTranslate/Scale/Rotate), ExtraData VALUE display via GetViewerStrings
(ExtraDataDlg.cpp:51-105; NiStringExtraData.cpp:125-132 exposes m_pString), general
viewer strings (ViewerStringsDlg.cpp:76-84), and SPECIFIC load-error display via
GetLastErrorMessage (NifDoc.cpp:574-583). NONE of this was executed; it is NOT
called a runtime test and NOT a render. SceneDesigner 2.6 was NOT qualified (no
execution, not the default reader for older NIFs; Gb26 files serve as optional
architecture reference only — NiSceneGraphComponent entity-property mechanism and
NiExternalAssetNIFHandler original-or-clone retrieval recorded as 2.6-era
hypothesis classes, NOT PCG facts).

---

## Part 2 — The eight contract questions (source locators + separately measured runtime)

**5.1 Does the tool expose serialized fields, native objects or post-Update state?**
Native objects and post-Update state only (C3/C4/C5). Serialized fields: no —
representation is already converted by the loader (aliases confirmed at runtime,
C10); serialized block counts require an independent header parse (this phase used
the reused bounded parser; Package C uses our own parser as a separate layer).

**5.2 Which edges does traversal follow?**
Top-level roots (all classes), controllers (NiObjectNET chains), scene children
(NiNode arrays). Not properties, not ExtraData contents, not other references (C6).
Measured: controller classes appear in DT/OBJECT visit censuses; cameras appear as
both top-level root and child in WORLD/OBJECT (131/130, 17/16).

**5.3 Is a count serialized block count, traversal visits or unique native pointers?**
Three distinct namespaces, all measured separately (C7): 1226/977/396/60 serialized
blocks; 388/561/131/17 visits; 388/561/130/16 unique addresses. Desktop comparison:
identical (0 differences; deterministic same-exe/same-input reproduction).

**5.4 Which values are local transforms, composed world transforms or bounds?**
`-trans` local; `-bs` world bounds; composed world TRS not printed by the stock
printer; NiCamera bound center = world translation (camera-specific). 6/6 synthetic
controls confirm composition math (C8/C9).

**5.5 Which versions/classes/loader aliases are known, and where does rejection happen?**
Version window [3.3.0.11 … 10.2.0.0], user version must be 0 (≥10.0.1.8 files);
aliases NiKeyframeController→NiTransformController, NiKeyframeData→NiTransformData,
NiVisData→NiBoolData (runtime-observed 9→9 and 2→2); rejection points: file open,
header text, version gates, user-version gate, missing factory (C10).

**5.6 Are errors specific enough to identify a missing factory?**
The stream object is; the STOCK BINARY is not — one generic message for every load
failure (C11, C14 measured). Missing-factory identification from this binary alone:
impossible; from source: deterministic (LoadRTTI lookup order, first missing name
fails the load).

**5.7 What does the tool mutate in memory or on disk? Does Update(0) run controllers?**
Disk: nothing (verified post-run, 7/7 identities unchanged). Memory: load-time
conversions + Update(0) recomputations inside the tool's process. Update(0) runs
controllers (source + executed; per-value mutation NOT_MEASURED) (C5/C12/C13).

**5.8 What additional evidence would be needed to identify a PE world root, instance or source record?**
This SDK toolset alone cannot establish any PE-world identity. What would be
needed (all beyond this phase): (a) a PE container census of compound-scene
candidates (Package C: NIF 10.1.0.0 metadata with multi-NiNode/NiTriShape
structure — note PE 10.1.0.0/user-0 is INSIDE this binary's accepted range, so
native load can reach the RTTI/factory layer); (b) a PE-side instance source
(CMO-class or equivalent placement record) tying an instance identity to a model
and transform — the SDK's demonstrated mechanisms (world-file anchors via
SceneAttachment, named transform nodes like MOUT's "start", 2.6 entity properties,
baked-into-vertex transforms via NiOptimization, clone-shared geometry via
NiGeometry::CopyMembers) are HYPOTHESIS CLASSES for where such a record could
live, not evidence that PE uses them; (c) an identity-preserving chain
instance→model→transform in PE's own data. Per contract section 14 defaults:
MODEL_218757_TO_CMO_JOIN / HISTORICAL_WORLD_INSTANCE / PE_WORLD_ROOT_IDENTITY =
NOT_ESTABLISHED; PE_AXES_AND_UNITS = UNVERIFIED; WORLD_XYZ_RECOVERED = NO.

**Required distinctions (contract section 5) — all enforced and measured:**
`-trans` = LOCAL getters ✔ (C2, C8); `-bs` = bounding sphere, not a building
pivot ✔ (C2, C9); `-extra` = class names in the stock printer ✔ (C2);
`-mem` = SDK-process addresses, not PCG pointers/block IDs/asset IDs ✔ (C2);
file class ≠ native runtime class via legacy loader conversion ✔ (C10, runtime
alias 9→9, 2→2).

---

## Part 3 — QUALIFICATION GATE VERDICT (contract section 7)

**GATE = PASS** (scope: this pinned SceneGraphPrinter.exe, on SDK and synthetic
inputs, for headless structural inspection; the gate does NOT qualify GUI tools,
does NOT qualify the printer as a serialized-field parser, and does NOT qualify
any PE-world placement capability).

Gate criteria (preregistered in 01_SDK/PREREGISTRATION_SDK_PHASE.md section 5):

1. **Executable identity valid — PASS.** Size+SHA256 match the pin; re-verified
   unchanged after all runs (independent process).
2. **Required SDK positive controls reproducible — PASS.** 4/4 exit 0, populated
   traversals (388/561/131/17 visits, depths 6/7/7/5), block/header counts measured
   (1226/977/396/60 at 10.1.0.0/10.1.0.0/10.0.1.18/10.0.1.18, user version 0);
   identical to the Desktop comparison values (deterministic reproduction, zero
   differences to explain).
3. **Synthetic transform calculations understood — PASS.** 6/6 expected-vs-observed
   matches, expectations derived from source BEFORE execution and preregistered;
   NiCamera-probe scope labeled (bound center = world translation is a camera
   class behavior; TWO_PARENTS case labeled as a diagnostic).
4. **Stdout parser accounts for all numbered visits — PASS.** Parser accepts BOTH
   PrintID forms (`:<name>` and bare); measured unaccounted numbered lines = 0 in
   all 16 runs.
5. **Negative/empty behavior honestly classified — PASS.** 5 negatives exit 1 with
   the generic message (recorded as the binary's specificity limit), missing file
   exit 1, empty scene exit 0 + "No top-level file objects." and NOT counted as a
   populated inspection; every mutation recorded with offsets + original/new bytes.

**Therefore: applying the printer to PE inputs (Package C, later dispatch) is
qualified for headless native inspection under the scope limits recorded above.**
In particular, for PE inputs the stdout parser must use the BOTH-forms rule
(controllers print without `:<name>`), must NOT equate the printed census with the
serialized block census, must NOT equate NiKeyframeController-era serialized names
with printed NiTransformController names (alias direction is serialized→runtime),
and must treat a bare `Error loading stream.` as REJECTED-with-unspecified-cause
(source-predicted cause labeled separately).

**Package C readiness note (no scope expansion here):** PE NIF 10.1.0.0 with user
version 0 is inside this binary's accepted version range; the KNOWN risk is the
missing-factory class (NiArk classes are not stock loaders — expectation from prior
work, to be measured as NATIVE_LOAD_REJECTED with the generic message, and analyzed
separately against the serialized type table and the SDK source registry).

---

## Part 4 — What is NOT qualified (explicit)

- SceneViewer/SceneDesigner: NOT_TESTED/SOURCE_ONLY (no GUI execution).
- Serialized-field / raw-byte semantics of the printer: FAIL-by-design (C3) — use
  OUR_PARSER as the separate layer.
- Load-error specificity of the stock binary: FAIL (C11) — generic message only.
- Per-value controller mutation at Update(0): NOT_MEASURED (no pre-state access).
- Any PE-world placement/instance/root capability: NOT_ESTABLISHED (contract
  section 14 defaults apply; see 5.8).
- The optional gb12_oracle.exe: NOT_USED this phase (custom executable; separate
  contract-section-11 matter).
