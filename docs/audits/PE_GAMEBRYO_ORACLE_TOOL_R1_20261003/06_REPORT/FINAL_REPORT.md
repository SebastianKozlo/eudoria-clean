# FINAL_REPORT — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (Batch E2)

All verdicts ADVISORY_PRE_QUALIFICATION (RUN_CONTRACT (a); Q1 absent; no
milestone/governance effect). Era categories used throughout; the oracle and
our decoder are never conflated (ORACLE_MODE on every output).

**Q1. Jakie wersje Gamebryo fizycznie posiadamy?** — GB_1_1_2 (installed tree
+ zip + iso), GB_1_2 (source rar + extracted tree + gamebryo_1.2.7z), GB_2_3
(GB_2.3.iso), GB_2_6 (GameBryo2.6.7z + extracted Gb26_src). Evidence: 01_INVENTORY/
GAMEBRYO_CORPUS_INVENTORY.csv (E1 gate G-INV-1 PASS). [CONFIRMED]

**Q2. Jakie wersje mają source?** — GB_1_2: FULL CoreLibs+SDK source (1.2.2,
NiVersion.h 326D0136 build 2006-06-19); GB_2_6: FULL flat source (2.6.0,
2008-10-20); GB_1_1_2: BINARY SDK (0 cpp); GB_2_3: BINARY SDK (0 NI*.cpp in
the Wise table). [CONFIRMED]

**Q3. Jakie oryginalne narzędzia fizycznie posiadamy?** — per TOOLCHAIN_MATRIX:
SceneViewer DX8/DX9, SceneGraphPrinter, NifConvert, AnimationTool,
AssetViewer, SceneDesigner, PhysXNifViewer, DeveloperTools (all era-separated,
with SHA256 census). [CONFIRMED]

**Q4. Które można zbudować?** — GB_1_2 tool MFC sources are complete in-tree;
no build was required because prebuilt exes exist; build NOT_TESTED (order
s19: original unmodified FIRST). [NOT_TESTED — honest]

**Q5. Które można uruchomić?** — EXECUTED THIS RUN: gb112 SceneGraphPrinter
(launches; BLOCKED_EVALUATION_TIMELOCK_EXPIRED); gb12 SceneGraphPrinter (exits
code 1, no observable output); gb12 SceneViewer_DX8 (alive, empty title, no
load result); gb26 PhysXNifViewer (runs; never reaches the NIF load:
Settings -> missing EGB_SHADER_LIBRARY_PATH -> "Failed to load shader
library!"). Evidence: 04_EVIDENCE/sgp_T1_dialog.txt + gui_attempts_log*.txt +
sandbox screenshots (LOCAL_ONLY). [CONFIRMED by execution]

**Q6. Które potrafią czytać NIF 4.1.0.12?** — GB_1_2: SUPPORTED at the version
gate (source) + the gb12 adapter decodes the legacy inline-RTTI layout of T4
(223534.nif) EOF-exact with 10/10 blocks [CONFIRMED]. GB_2_6: REJECTED (below
floor 10.1.0.114) [CONFIRMED from source]. GB_1_1_2: UNKNOWN (binary).
GB_2_3: UNKNOWN (binary).

**Q7. Które potrafią czytać NIF 10.1.0.0?** — GB_1_2: version gate ACCEPTS
(3.3.0.11..10.2.0.0); the full corpus load FAILS at LoadRTTI on MindArk
NiArk* classes (unregistered -> RTTIError -> Load() false) — 0 NiArk* among
the 198 registered classes (registry census). GB_2_6: REJECTED. GB_1_1_2:
UNKNOWN (binary; and its tools cannot execute: timelock). GB_2_3: UNKNOWN.
[CONFIRMED for GB_1_2/GB_2_6]

**Q8. Czy odczyt 10.1 jest FULL czy PARTIAL?** — ORIGINAL GB 1.2 behavior on
the PCG 9.3.5 corpus: **FAIL** (whole-load failure at the first NiArk* block
— the version gate is NOT the blocker; the factory is). With OUR
--full-decode extension: PARTIAL (known-class fields decode bit-clean; NiArk*
blocks remain unknown with closure-derived boundaries). For a hypothetical
10.1.0.0 file containing ONLY standard classes: the gate + registry accept it
(SOURCE-derived prediction; the stock sample at 10.0.1.18 with standard
classes LOADS — positive control PASS). [CONFIRMED]

**Q9. Jak original Gamebryo streamuje NIF?** — NiStream::Load -> LoadHeader
("File Format" test + packed-u32 gate + user version >= 10.0.1.8) ->
LoadRTTI (u16 table + per-type u32-length strings + factory) -> LoadBinary
loop (per-block GroupID iff 5.0.0.6 <= v < 10.1.0.114) -> TopObjects footer
-> link loop -> postlink. Evidence: 02_ANALYSIS/NIF_LOAD_PIPELINE.md
(G-PIPE-1). [CONFIRMED]

**Q10. Jak działa object factory?** — ms_pkLoaders string map populated by
per-lib *SDM.cpp NiRegisterStream/RegisterLoader calls; miss -> RTTIError ->
NO_CREATE_FUNCTION "<name>: cannot find create function." -> load fails.
Registry census: 198 classes, ZERO NiArk*. [CONFIRMED]

**Q11. Jak działa link/PostLink?** — link: per-object LinkObject pops
GetObjectFromLinkID (NULL_LINKID 0xFFFFFFFF; NiNode children via SetAt);
postlink: extra-data migration (NiObjectNET.cpp L656-693, no byte
consumption at load). [CONFIRMED]

**Q12. Jak przechowywana jest local transform?** — Serialized in every
NiAVObject: translate 3xf32, rotate 3x3 f32 (row order as file bytes), scale
f32 (NiAVObject.cpp L602-604) — bit-exact equal on both sides for the
decoded T blocks. [CONFIRMED]

**Q13. Jak wyliczana jest world transform?** — COMPUTED at update:
m_kWorld = parent ? parent->m_kWorld * m_kLocal : m_kLocal; NiTransform
operator*: scale=sa*sb, rotate=Ra*Rb, translate=ta+sa*(Ra*tb)
(NiAVObject_Win32.cpp L22-31; Win32 NiTransform.inl L15-24). Never a Eudoria
position. [CONFIRMED (source)]

**Q14. Jak działa AttachChild?** — IncRefCount/AttachParent/array add; NOT
called during load (children attach via NiNode::LinkObject -> SetAt).
[CONFIRMED]

**Q15. Jak działa bounding volume?** — serialized MODEL-space spheres only
inside NiGeometryData (center 3f + radius f); NO serialized world/root bound;
world bounds recomputed by UpdateWorldBound merge at update.
(BOUNDING_VOLUME_SEMANTICS.md). [CONFIRMED]

**Q16. Czy zbudowano GAMEBRYO_ORACLE_TOOL?** — YES. tools/gamebryo_oracle
(oracle.py; schemas x2; adapters gb12/gb26/gb112/gb23/compare; tests;
README). [CONFIRMED — G-TOOL-1 PASS]

**Q17. Czy tool działa deterministycznie?** — YES for every used adapter x
T: byte-identical double runs, no wall-clock in any JSON body.
[E3: the T3 gb12 FULL-DECODE determinism pair is now also produced —
byte-identical sha256 B4F5A55A... (inspect_T3_gb12_full.json +
_run2.json) — the E2 gap (T3-full pair absent, wall cap) is closed for
determinism even though the T3 closure assignment itself remains honest
PARTIAL (see NOT_CHECKED E3 section). G-TOOL-2 PASS]

**Q18. Czy jest fail-closed?** — YES: all s17 detectors implemented and
exercised (RTTIError, missing factory, unsupported block, link failure,
partial, exception, object-count); no silent success. [G-TOOL-3 PASS]

**Q19. Czy 218757.nif został poprawnie odczytany?** — YES with the declared
semantics: the ORIGINAL GB 1.2 verdict is RTTIError (NiArk*) — that IS the
correct original behavior; the full-decode extension accounted 66/66 blocks
EOF-exact; OUR FIELD_IDENTITY_V2 decoder also decoded 66/66.
[CONFIRMED]

**Q20. Jak wygląda jego scene graph?** — 1 root NiNode "Scene Root"
(zero local transform); 12 NiNode blocks (outpost walls/doors/vents,
__NDL_MultiMtl_Node, 5 dPVS occluder nodes); 14 NiTriShape geometries +
their data blocks; 19 properties; 2 directional lights; 4 MindArk extra-data
blocks; 27 parent-child edges; no controllers. [CONFIRMED]

**Q21. Jakie ma wymiary w GAME_UNITS?** — From serialized per-geometry
MODEL-space spheres + local transforms (no serialized world bound): sphere
radii 525..1795 GAME_UNITS; nonzero local translations up to ~1030 GAME
UNITS on y / 820 on z. GAME_UNITS ONLY (scale to meters UNCONFIRMED).
[PLAUSIBLE (derived)]

**Q22. Czy zawiera world/cell placement evidence?** —
NO_WORLD_PLACEMENT_EVIDENCE_FOUND (full-value result). No serialized
world/cell record; root transform zero; local transforms never promoted.
[G-218757-2 PASS]

**Q23. Czy wynik oryginalnego Gamebryo zgadza się z naszym parserem?** — For
the decoded known-class data: T1 comparison 13 MATCH / 4 MISMATCH / 1
NOT_AVAILABLE_IN_OUR / 1 SEMANTICALLY_UNRESOLVED (T-runs JSONs). [PARTIAL —
see Q24]

**Q24. Jakie różnice znaleziono?** — (a) BY DESIGN: the oracle reports the
ORIGINAL fail-closed RTTIError verdict vs our decoder accepting NiArk* files
(the primary finding of the whole run); (b) representation differences:
nifxml compound containers ({'Row 1'..'Row 3'} / {'x','y','z'}) vs GB flat
lists in local transforms/bounds/names comparisons — both raw value sets are
recorded in compare_T1.json; value-level equality is evident in the recorded
data but the automated status stays MISMATCH until a normalization pass
(honest; no tolerance widened); (c) our decoder failed on T2/T5 (EOF error)
and T3 (closure cap) — honest NOT_AVAILABLE_IN_OUR_DECODER, never faked;
(d) world_transforms computation error recorded SEMANTICALLY_UNRESOLVED.
[G-CMP-2 PASS]

**Q25. Które nasze NIF assumptions mogą zostać podniesione/obniżone?** —
RAISE (proposals, ADVISORY): (1) the per-block GroupID framing and the
RTTI-table layout of 10.1.0.0 are now ORACLE-CONFIRMED (independent GB 1.2
semantics agree with our schema decoder on 66/66 boundaries); (2) the
serialized NiGeometryData model-space sphere semantics agree bit-exact.
LOWER (proposals): (1) our FIELD_IDENTITY_V2 decoder has corpus edges
(T2/T5 minimal files EOF-fail; T3 fails the closure cap) — coverage claims
should be re-scoped; (2) any assumption that original GB tools could
validate our decode is now bounded by the executed blockers (GB 1.1.2
timelock; GB 2.6 viewer env). [PLAUSIBLE — recorded as proposals only]

**Q26. Co pozostaje UNKNOWN?** — GB 1.1.2 read range (binary); GB 2.3 read
range + execution (not installed); GB 1.2 prebuilt tools' observable load
behavior (no output observable); GB 2.6 executed path beyond the shader-
library blocker; the NiArk* block CONTENT semantics (both oracles bounded:
GB 1.2 fails closed; our decoder decodes bytes but their MEANING is not
source-proven); T3 field-level oracle decode — [E3: ADVANCED to 448/1288
blocks decoded (all ~25 T3 classes implemented from GB 1.2 source) but the
unknown-run closure assignment still exceeds the search budget — honest
PARTIAL, exact residual in inspect_T3_gb12_full.json + NOT_CHECKED.md E3
section]; 218757 dimensions in meters (scale UNCONFIRMED). [HONEST]

**Q27. Jakie nowe Rosetta edges uzyskaliśmy?** — GAMEBRYO_ROSETTA.md gains
executed confirmations: header/RTTI/group framing edges (byte->loader->field)
now validated against an INDEPENDENT source-derived reimplementation;
registry census edge (class name -> registered/unregistered -> original
verdict); timelock/dialog text -> blocker-class edges for the original
tools. [E3: G-SIG-1 now also delivers the machine-readable semantic
signature set (02_ANALYSIS/GAMEBRYO_SEMANTIC_SIGNATURES.json per order s28):
per-version function contracts + source identity (file+sha256) for
SetTranslate/SetRotate/SetScale/UpdateWorldData/AttachChild/DetachChild/
SetAt + the NiStream load/link/postlink orchestration — NO Entropia.exe
matching. CONFIRMED]

**Q28. Czy powstało cokolwiek, co realnie pomoże przyszłemu placement RE?** —
Indirect but real: the oracle now gives an INDEPENDENT second decoder for
standard-class field identity (transforms/bounds/counts) — placement RE
based on our decoder can be cross-checked without touching the game client;
the fail-closed factory finding explains WHY no stock Gamebryo tool can read
PCG 10.1.0.0 assets (placement evidence must come from the client itself or
from NiArk semantics, not from stock tools). NO placement data was produced
(by scope). [CONFIRMED]

**Q29. Czy jakikolwiek proprietary payload/source trafił do repo?** — NO
(executor-side): tools/gamebryo_oracle = our code only (registry = class
names, a factual census); package = md/csv/json + our scripts; T payloads,
corrupted copies, screenshots, DLLs, exes stayed LOCAL_ONLY in the sandbox;
staging census check is the persistence phase's step 7. [CONFIRMED]

**Q30. Czy milestone/governance pozostały bez zmian?** — YES: MILESTONE_
ADVANCEMENT = NONE; NEXT_MILESTONE_AUTHORIZED = NO; CANONICAL_GATE_EFFECT =
NONE; no Q1 changes; no canonical files edited (retractions are proposals);
no git operations by the executor. [CONFIRMED]

## Terminal section (order s27 anti-overclaim)

Root transform != world position; loader accepted != all understood;
"looks correct" screenshots are NOT PASS; source exists != Entropia uses it
(needs FUNCTION_IDENTITY + build correspondence); computed world transforms
are NEVER Eudoria positions; dimensions in GAME_UNITS until scale is
CONFIRMED; all GB-era claims carry their era category.
