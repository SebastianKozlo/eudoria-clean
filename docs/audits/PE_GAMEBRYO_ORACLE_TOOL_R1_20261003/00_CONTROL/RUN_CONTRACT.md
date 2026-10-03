# RUN_CONTRACT — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003

The binding execution contract. The human order (AUTHORIZATION.md) is the
contract's authority; this file makes it executable: identity, the ONE
primary question, phases, gates with exact predicates, controls, classes,
stops, paths, discipline and the persistence/terminal protocol. Where the
reconstructed order wording and this contract could diverge, the
SCIENTIFIC content pinned here (gates, budgets, selection rules, pins) is
normative, and PE-MASTER verifies both before release.

## (a) Identity block

| Field | Value |
|---|---|
| RUN_ID | PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 |
| PARENT_LOOP | PE-MASTER supervisory loop `8f0ef23a-964b-4767-ac59-1ec593a1b118` (owner win32:16328); NO_NESTED_TASKS |
| BASE_SHA | `f33c7b9c201b02b8e0f8c7010275b6217475b5a4` (== HEAD == origin/master == live remote; PREFLIGHT.md section 1) |
| RUN_CLASS | LOAD_BEARING (human-declared) |
| RUN_TYPE | GAMEBRYO_TOOLCHAIN_FORENSICS_AND_ORACLE_TOOL_BUILD |
| MODE | STATIC / LOCAL TOOL EXECUTION ONLY — the game client is NEVER launched; no dynamic instrumentation; no network (git fetch/ls-remote/push during preflight/persistence are the ONLY authorized network operations, by their respective workers) |
| PRIMARY_TARGET | PCG_9_3_5 / Entropia Universe 9.3.5 |
| CONTRIBUTES_TO | EU935-M2, EU935-M3, EU935-M10, EU935-M11 — **NO advancement**: MILESTONE_ADVANCEMENT = NONE; NEXT_MILESTONE_AUTHORIZED = NO; CANONICAL_GATE_EFFECT = NONE; Q1 absent → every verdict of this run is ADVISORY_PRE_QUALIFICATION |
| ROLES | executor = pe-reconstruction; fresh-context QC = pe-master-auditor (NOT this run's formalizer); persistence = pe-master-auditor; PE-MASTER = supervisor/auditor; human = orderer + post-publication adjudicator |

## (b) THE ONE primary question (order section 2)

> Which versions of the locally held original Gamebryo engine and
> toolchain (GB 1.1.2, GB 1.2, GB 2.3, GB 2.6 — `D:\gamebyroengine`)
> actually load Project Entropia / Entropia Universe 9.3.5 NIF files — in
> particular NIF version 10.1.0.0 — FULLY or PARTIALLY, with exactly what
> version-gate logic and failure behavior, proven from original Gamebryo
> source and/or executed original loaders — such that the original engine
> can serve as an INDEPENDENT semantic oracle for our own NIF decoder on
> asset 218757.nif and the preregistered test corpus T1-T5?

Everything not serving this question is out of scope (see (g) hard stops,
(h) forbidden paths). The run's two goals (forensic inventory; oracle tool)
are the two halves of answering it.

## (c) Phases A-D mapped to the human order sections

| Phase | Order sections | Batch | Produces |
|---|---|---|---|
| A — Forensic inventory of D:\gamebyroengine | s4 (+s22 policy) | E1 | `01_INVENTORY/GAMEBRYO_CORPUS_INVENTORY.csv` (G-INV-1), `TOOLCHAIN_MATRIX.csv` (G-INV-2), `SOURCE_ORACLE_INDEX.csv` (G-INV-3) |
| B — Version support from source (NIE ZGADUJ) | s5 (+P1/P2 reconciliation) | E1 | `02_ANALYSIS/VERSION_SUPPORT.md` (G-VER-1, G-VER-2) |
| C — Original NIF load pipeline | s6 (+s14, s15) | E1 | `02_ANALYSIS/NIF_LOAD_PIPELINE.md`, `GAMEBRYO_ROSETTA.md`, `TRANSFORM_SEMANTICS.md`, `BOUNDING_VOLUME_SEMANTICS.md` (G-PIPE-1) |
| T-corpus selection | s12 | E1 (end) | `00_CONTROL/SELECTION.md` filled + locked (G-SEL-1); extraction provenance (G-SEL-2) may complete in E2 before first oracle run |
| D — Build + run GAMEBRYO_ORACLE_TOOL | s7-s11, s13-s21, s23 | E2 (E3 optional) | `tools/gamebryo_oracle/**` (G-TOOL-1), raw outputs + controls in `04_EVIDENCE` (G-TOOL-2/3/4, G-CMP-1/2, G-218757-1/2), `02_ANALYSIS/218757_NIF_RESULT.md`, `03_TOOL/GAMEBRYO_COMPATIBILITY_MATRIX.csv` (G-MATRIX-1), optional `GAMEBRYO_SEMANTIC_SIGNATURES.json` (G-SIG-1), `06_REPORT/FINAL_REPORT.md` |

## (d) THE GATE LIST (exact predicates; verbatim from the PE-MASTER conversion)

G-INV-1 INVENTORY_CENSUS: 01_INVENTORY/GAMEBRYO_CORPUS_INVENTORY.csv has
EXACTLY one row per physical top-level item of D:\gamebyroengine (expected
8: 2 directories + 6 archives; recount physically and use the actual
count), each row carrying: relative path, size, SHA256 (files) OR census
fields (directories: recursive file_count + total_bytes + structure
summary), version_category in
{GB_1_1_2,GB_1_2,GB_2_3,GB_2_6,UNKNOWN_GAMEBRYO,THIRD_PARTY,OUR_TOOL},
version_evidence (concrete artifact: archive label / installer metadata /
source file+line / PE metadata), classification
(SOURCE/BINARY/DOCS/MIXED). FAIL if any physical item is absent or any
required field is vacuous. Archive interior = content LISTING (7z/rar/iso
listing; extract only what Phase B/C/D needs, into the sandbox, never into
D:\gamebyroengine and never into the repo).

G-INV-2 TOOLCHAIN_MATRIX: 01_INVENTORY/TOOLCHAIN_MATRIX.csv lists every
identified original tool (SceneViewer, NifViewer, SceneGraphPrinter,
NifConvert, AnimationTool, DeveloperTools, others found) with physical
location, identity (exe SHA256 or source path+SHA256), per-version NIF
support fields, BUILDS/RUNS status or NOT_TESTED+reason.

G-INV-3 SOURCE_ORACLE_INDEX: 01_INVENTORY/SOURCE_ORACLE_INDEX.csv indexes
every source file cited as oracle evidence
(NiStream/NiBinaryStream/NiObject/NiObjectNET/NiAVObject/NiNode/NiGeometry/NiGeometryData/NiTexturingProperty/NiSourceTexture/NiPixelData/NiTimeController/NiControllerSequence/NiKeyframeController/NiTransformController/NiBound/NiBoxBV/NiSphereBV/NiMain
+ LoadBinary/SaveBinary/RegisterLoader/RegisterStreamables/CreateObject/LinkObject/PostLinkObject/Load/Link/Stream/Read)
with per-file path + SHA256 + version.

G-VER-1 VERSION_EVIDENCE: 02_ANALYSIS/VERSION_SUPPORT.md gives per GB
version: MIN_NIF_VERSION_SUPPORTED, MAX_NIF_VERSION_SUPPORTED, SUPPORTED
VERSION TABLE, VERSION COMPARISON LOGIC, FAILURE BEHAVIOR — each backed by
source citation (file+line+SHA) or executed-loader observation; statuses
only SUPPORTED/REJECTED/PARTIAL/UNKNOWN with evidence; "should support"
without evidence = FAIL; reconciliation with pins P1/P2 recorded
explicitly.

G-VER-2 NIF_10_1_QUESTION: which GB versions read NIF 10.1.0.0 and FULL vs
PARTIAL, per version, with evidence (version-gate source +
object-coverage statement for the types present in the T-corpus + executed
loader test if a tool runs).

G-PIPE-1 PIPELINE: 02_ANALYSIS/NIF_LOAD_PIPELINE.md documents the load
pipeline per version family with class/function/source file/line/version
per step, 1.x vs 2.x differences explicit;
02_ANALYSIS/GAMEBRYO_ROSETTA.md maps ORIGINAL BYTE -> GAMEBRYO LOADER ->
RUNTIME FIELD -> RUNTIME OBJECT -> CONSUMER for the covered steps;
TRANSFORM_SEMANTICS.md covers
SetTranslate/SetRotate/SetScale/UpdateWorldData/AttachChild/DetachChild/SetAt
contracts; BOUNDING_VOLUME_SEMANTICS.md answers the order section 15
questions (serialized vs recomputed, stage, coordinate system, root bound
scope).

G-TOOL-1 TOOL_BUILT: tools/gamebryo_oracle/ exists with ONE entrypoint CLI
supporting inspect/compare/capabilities/probe-version; schemas
oracle_result.schema.json + comparison_result.schema.json; adapters
gb112/gb12/gb23/gb26 containing ONLY build instructions/local path
discovery/invocation/output parser/hash verification (zero proprietary
source in repo); output JSON matches the order section 8 minimum.

G-TOOL-2 DETERMINISM: for each T-file x each used adapter: two runs
produce byte-identical JSON (SHA256 equal). No wall-clock timestamps in
the JSON body.

G-TOOL-3 FAIL_CLOSED: wrong-version control -> REJECTED/UNSUPPORTED
(explicit, nonzero exit or accepted=false+reason); corrupted-copy control
-> FAIL (not silent success); unknown-class control -> unknown_type
reported (not skipped); partial-load case -> PARTIAL. Raw outputs of all
controls stored in 04_EVIDENCE. A control that silently succeeds = GATE
FAIL.

G-TOOL-4 ORACLE_LABELING: every JSON carries oracle.gamebryo_version,
loader_identity, loader_source_identity, tool_version, and ORACLE_MODE in
{ORIGINAL_TOOL_EXECUTION, SOURCE_DERIVED_REIMPLEMENTATION, MIXED};
SOURCE_DERIVED output is never phrased as original execution.

G-SEL-1 PREREGISTRATION: 00_CONTROL/SELECTION.md final T1-T5 rows
(container, id, offset+size, extracted SHA256, header NIF version,
mechanical reason) recorded and hash-locked BEFORE the first oracle run
on any T; the raw evidence creation order in 04_EVIDENCE must be consistent
with it.

G-SEL-2 PROVENANCE: each T re-extracted from the pinned container into THIS
run's sandbox with EXTRACT_PROVENANCE (T1 = 218757.nif re-extracted fresh
from Models.bnt; the old interrupted-run sandbox copy may be used ONLY as
a cross-check); Models.bnt pin:
D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt, 395,412,868
B, SHA256 C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0
(re-hash before use, fail-closed); "218757.nif" index offset 395,283,797.

G-CMP-1 COMPARISON: compare output per T for the full order section 11
field list with statuses in {MATCH, MISMATCH, NOT_AVAILABLE_IN_ORACLE,
NOT_AVAILABLE_IN_OUR_DECODER, SEMANTICALLY_UNRESOLVED}; OUR decoder
identity pinned (path+SHA256+lineage; preference: the audited
FIELD_IDENTITY_V2 decoder lineage from
PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915; document whichever is used);
float tolerance explicitly declared where applied.

G-CMP-2 MISMATCH_HONESTY: every MISMATCH carries an evidence-based
explanation or SEMANTICALLY_UNRESOLVED; no fake equality; no tolerance
widened to manufacture MATCH.

G-218757-1 PROBE: 02_ANALYSIS/218757_NIF_RESULT.md delivers the full order
section 13 field list with per-field statuses; the order section 10
scene-graph-level classification
(MODEL_LOCAL/MULTI_OBJECT_LOCAL_SCENE/CELL_LIKE/WORLD_LIKE/UNKNOWN) + the
four explicit questions (IS_ROOT_TRANSFORM_ZERO?,
IS_ROOT_TRANSFORM_NONZERO?, DOES_FILE_CONTAIN_PARENT_ABOVE_BUILDING?,
DO_NODE_NAMES_SUGGEST_CELL/WORLD_CONTEXT?, IS_THIS_STANDALONE_ASSET?) each
with status CONFIRMED/STRONGLY_SUPPORTED/PLAUSIBLE/UNVERIFIED/REJECTED;
dimensions in GAME_UNITS only.

G-218757-2 PLACEMENT_SAFETY: WORLD_PLACEMENT_EVIDENCE verdict; a local
transform is NEVER promoted to world placement; NO_WORLD_PLACEMENT_EVIDENCE_FOUND
is an acceptable full-value result; no EXE-wide scan, no placement tracing,
no building-family search (out of scope by the order).

G-MATRIX-1 MATRIX: 01_INVENTORY or 03_TOOL/GAMEBRYO_COMPATIBILITY_MATRIX.csv
with the order section 16 columns; every cell in
{PASS,PARTIAL,FAIL,NOT_TESTED,UNKNOWN}; zero blank cells; one row per
GB_VERSION x TOOL. [Binding location pin for this run:
`03_TOOL/GAMEBRYO_COMPATIBILITY_MATRIX.csv` — the executor records the
chosen location in the manifest either way.]

G-PKG-1 PACKAGE: the section 24 tree exists with all required files;
FINAL_REPORT.md answers the 30 questions of section 25 separately and
numbered; NOT_CHECKED.md; RETRACTIONS_SUPERSESSIONS.md (corrections of
prior canon are RECORDED AS PROPOSALS in this run — the executor does not
edit other runs' or canonical files); MANIFEST_SHA256.csv covering every
package file except itself (bijection verified by census).

G-PAYLOAD-1 NO_PROPRIETARY: at staging time the committed path census =
run package + tools/gamebryo_oracle + AUDIT_ENTRYPOINT.md ONLY; zero
Gamebryo source/ISO/lib/binaries and zero original NIF/BNT/VFS/EXE payloads
in the commit; identity metadata only; modified proprietary payloads never
leave the sandbox.

G-SIG-1 (OPTIONAL, non-gating if absent; if produced it must satisfy):
GAMEBRYO_SEMANTIC_SIGNATURES.json per order section 28 with
version/source identity/function contract/relevant offsets/confidence; NO
Entropia EXE-wide matching attempted.

## (e) Negative controls (order section 18; binding for G-TOOL-3)

Every material control records: MEASURED_QUANTITY /
INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED.

| Control | Required outcome | Falsifier question |
|---|---|---|
| Positive | a known-good NIF (T-corpus member) loads (blocks read, accepted, scene graph populated) | would the test fail if the loader rejected valid input? |
| Wrong-version | wrong-version input (e.g. a 4.1.0.12 file against a version-gated adapter, or a synthetic out-of-range header) -> explicit REJECTED/UNSUPPORTED, nonzero exit or accepted=false+reason | would the test fail if the loader silently accepted an unsupported version? |
| Corrupted-copy | a corrupted copy of a T payload (sandbox-local) -> FAIL, not silent success | would the test fail if corruption was silently skipped? |
| Unknown-class | an input containing an unknown class/type id -> unknown_type REPORTED, not skipped | would the test fail if unknown classes were dropped silently? |
| Partial-load | a case loading only part of the scene -> PARTIAL, never PASS | would the test fail if partial loads were reported as PASS? |

A control that silently succeeds = GATE FAIL (G-TOOL-3). Raw outputs of all
controls are stored in 04_EVIDENCE with tool+input SHA256, stdout/stderr,
exit codes. Negative controls that do not exercise the actual predicate
validate nothing (L9).

## (f) Non-pass classes (canonical for every gate)

`PASS` / `PARTIAL` / `FAIL` / `BLOCKED_<REASON>` / `UNKNOWN` /
`NOT_TESTED` / `NOT_AVAILABLE`.

RUN_STATUS: `COMPLETE_FOR_SCOPE` / `PARTIAL` / `BLOCKED_EXTERNAL` +
HARD_STOP_REASON.

Gate results are recorded per gate in
`00_CONTROL/STAGE_ACCEPTANCE_GATES.csv` (executor; one row per gate:
gate_id, predicate_result, evidence pointer, timestamp). A gate that was
never attempted is NOT_TESTED — never PASS by silence.

## (g) Hard stops (executor)

- **H1** any step would require launching the game client, dynamic
  instrumentation, or network -> stop that step, record BLOCKED (not
  authorized);
- **H2** any write into D:\gamebyroengine or pcg_install originals ->
  FORBIDDEN (extraction only into the run sandbox);
- **H3** any proprietary payload about to be staged -> STOP, fix staging;
- **H4** version-evidence contradiction with prior audited canon that
  cannot be reconciled from source -> record BOTH claims with evidence as
  a finding, never silently pick one;
- **H5** scope creep into placement/EXE-wide/all-buildings -> STOP, record;
- **H6** budget exhaustion -> honest PARTIAL with exact stop point;
- **H7** a live writer/controller collision or irreconcilable repo state
  -> stop and report.

## (h) Forbidden paths (executor)

- All completed/committed run packages (read-only reference).
- The untracked foreign packages
  (`PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003` — read-only
  reference for its sandbox payload + raw evidence;
  `PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001`;
  `PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914`;
  `PE_935_P1_CLOSURE_EXTERNAL_QC_20260930`;
  `PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928`; `experiments/`) —
  never modify, never stage;
- `src/` (no game-runtime changes in this run);
- `AUDIT_ENTRYPOINT.md` (persistence phase only, by pe-master-auditor);
- `D:\gamebyroengine` and `pcg_install` (read-only; extraction to sandbox
  only);
- skills/agents/plugin files;
- git history (no rewrite, no force-push);
- NO git operations of any kind by the executor before the persistence
  phase (which is dispatched separately by PE-MASTER to pe-master-auditor).

## (i) Allowed inputs / outputs (executor)

Allowed INPUTS (read-only unless stated): `D:\gamebyroengine` (read-only);
`D:\Eudoria_Reconstruction\pcg_install` (read-only);
`C:\Users\User\AppData\Local\Temp\opencode\gb_tools_inventory\` (read-only
reference cabs); prior run packages (read-only reference); the repo's
committed corpus artifacts (`docs/nif/corpus/pcg953_nif_manifest.csv`,
ROSETTA census — see SELECTION.md pins); project skills; the run sandbox
(rw, executor-created).

Allowed OUTPUTS: `docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/**` (the
package); `tools/gamebryo_oracle/**` (the tool); the run sandbox
`D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox\**`
(local-only); NOTHING else. NO git operations before the persistence
phase.

## (j) Payload discipline

- Original executables, DLLs, ISOs, libs, archives, and original
  NIF/BNT/VFS payloads NEVER enter the repo (G-PAYLOAD-1). Identity
  metadata only (path/size/SHA256/version/provenance).
- External dependencies referenced as LOCAL_PATH_DESCRIPTION / VERSION /
  SIZE / SHA256 / REPRODUCTION_METHOD.
- Extracted T payloads, corrupted control copies and any screenshots stay
  LOCAL_ONLY in the sandbox; NifConvert-style derivatives are
  GENERATED_DIAGNOSTIC_ARTIFACT, never RECOVERED_ORIGINAL.
- At staging time (persistence phase): committed path census = run package
  + tools/gamebryo_oracle + AUDIT_ENTRYPOINT.md ONLY.

## (k) Era separation (ABSOLUTNA ZASADA, order section 3)

- Closed category set for every artifact/claim/output:
  `GB_1_1_2` / `GB_1_2` / `GB_2_3` / `GB_2_6` / `UNKNOWN_GAMEBRYO` /
  `THIRD_PARTY` / `OUR_TOOL`.
- NEVER "Gamebryo robi X" without the exact version; findings from
  different GB versions are never merged.
- PCG 9.3.5 corpus era vs 2003 corpus era: never conflated;
  `manifest_2003.csv` is the WRONG ERA for this run's T-corpus.
- The oracle and our decoder are likewise never conflated: every output
  carries ORACLE_MODE (G-TOOL-4).

## (l) Claim discipline (order sections 26-27)

- Separate FUNCTION_IDENTITY / OBSERVED_OPERATION /
  FINAL_SEMANTIC_ROLE (+ CAUSAL_ROLE where relevant). Evidence vocabulary:
  CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED.
- Coverage claims separate CLIENT_KNOWLEDGE_COVERAGE /
  RECONSTRUCTION_IMPLEMENTATION_COVERAGE /
  HISTORICAL_GAME_RECOVERY_COVERAGE.
- Gamebryo source alone CANNOT confirm MindArk placement, world
  coordinates, server values, or Ark custom semantics.
- Anti-overclaim: root transform != world position; SceneViewer renders !=
  parser correctness; loader accepted != all understood; source exists !=
  Entropia uses it (needs FUNCTION_IDENTITY + build correspondence).
- NEVER call a computed world transform a Eudoria position;
  SERIALIZED_LOCAL_TRANSFORM vs COMPUTED_WORLD_TRANSFORM always
  distinguished; dimensions in GAME_UNITS only until scale is CONFIRMED.
- A silent skip is never a pass (G-TOOL-3; QC treats any silent skip as
  QC_FAIL until reclassified PARTIAL with the exact residue).

## (m) Deliverables map (order section -> file; incl. the 30 FINAL_REPORT questions)

| Order section | Deliverable |
|---|---|
| s0 authorization | 00_CONTROL/AUTHORIZATION.md |
| s1 pre-flight | 00_CONTROL/PREFLIGHT.md |
| s2 primary question | RUN_CONTRACT.md (b); answered by FINAL_REPORT Q4/Q5 |
| s3 era separation | RUN_CONTRACT.md (k); version_category columns in all inventory/output files |
| s4 Phase A inventory | 01_INVENTORY/GAMEBRYO_CORPUS_INVENTORY.csv; TOOLCHAIN_MATRIX.csv; SOURCE_ORACLE_INDEX.csv |
| s5 Phase B version support | 02_ANALYSIS/VERSION_SUPPORT.md |
| s6 Phase C pipeline | 02_ANALYSIS/NIF_LOAD_PIPELINE.md; GAMEBRYO_ROSETTA.md; TRANSFORM_SEMANTICS.md; BOUNDING_VOLUME_SEMANTICS.md |
| s7 Phase D tool | tools/gamebryo_oracle/** (README, launcher, schemas oracle_result.schema.json + comparison_result.schema.json, adapters gb112/gb12/gb23/gb26/compare, tests) |
| s8 inspect output | 04_EVIDENCE raw inspect JSONs per T; schema in the tool |
| s9 object-level output | same raw JSONs; SERIALIZED_LOCAL_TRANSFORM vs COMPUTED_WORLD_TRANSFORM fields |
| s10 placement safety | 02_ANALYSIS/218757_NIF_RESULT.md; RUN_CONTRACT (e)/(p) |
| s11 comparison | 04_EVIDENCE per-T comparison raw outputs + summary in FINAL_REPORT; our-decoder identity pinned per G-CMP-1 |
| s12 test corpus | 00_CONTROL/SELECTION.md (+ lock in 04_EVIDENCE/SELECTION_LOCK.json); 04_EVIDENCE/EXTRACT_PROVENANCE.json |
| s13 test 218757 | 02_ANALYSIS/218757_NIF_RESULT.md |
| s14 source-as-oracle signatures | 01_INVENTORY/SOURCE_ORACLE_INDEX.csv + 02_ANALYSIS/GAMEBRYO_SEMANTIC_SIGNATURES.json (optional) |
| s15 bounding volumes | 02_ANALYSIS/BOUNDING_VOLUME_SEMANTICS.md |
| s16 compatibility matrix | 03_TOOL/GAMEBRYO_COMPATIBILITY_MATRIX.csv |
| s17 fail-closed | G-TOOL-3 controls in 04_EVIDENCE; STAGE_ACCEPTANCE_GATES.csv |
| s18 controls | 04_EVIDENCE control raw outputs (MEASURED_QUANTITY/INDEPENDENT_SOURCE_OF_TRUTH/WHY_NON_CIRCULAR/FAILURE_CASE_DETECTED records) |
| s19 SceneGraphPrinter | 04_EVIDENCE original-tool attempt records (stdout/stderr/exit/tool SHA/input SHA) |
| s20 SceneViewer/NifViewer | 04_EVIDENCE attempt records; screenshots LOCAL_ONLY (sandbox) |
| s21 NifConvert | derivatives classified GENERATED_DIAGNOSTIC_ARTIFACT in the records |
| s22 tool policy | tools/gamebryo_oracle/README.md + G-PAYLOAD-1 compliance |
| s23 tool structure | tools/gamebryo_oracle/ layout |
| s24 output artifacts | the package tree below + MANIFEST_SHA256.csv (package root) |
| s25 final questions | 06_REPORT/FINAL_REPORT.md — the 30 questions answered SEPARATELY and NUMBERED (list below) |
| s26 claim discipline | RUN_CONTRACT (l); applied in every analysis file |
| s27 anti-overclaim | RUN_CONTRACT (l); FINAL_REPORT terminal section |
| s28 signatures (optional) | 02_ANALYSIS/GAMEBRYO_SEMANTIC_SIGNATURES.json |
| s29 fresh QC | 05_QC/QC_REPORT.md (fresh pe-master-auditor context, NOT the formalizer) |
| s30 persistence | 06_REPORT/HANDOFF.md; AUDIT_ENTRYPOINT.md factual row; MANIFEST_SHA256.csv; RUN_CONTRACT (o) |
| s31 terminal | 06_REPORT/HANDOFF.md terminal block + FINAL_REPORT terminal section; RUN_CONTRACT (p) |

Package tree (order s24; 00_CONTROL..06_REPORT):

```
docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/
  MANIFEST_SHA256.csv                      (package root; every file except itself)
  00_CONTROL/  AUTHORIZATION.md, PREFLIGHT.md, RUN_BUDGET.md, SELECTION.md,
               RUN_CONTRACT.md (formalizer) + STAGE_ACCEPTANCE_GATES.csv (executor)
  01_INVENTORY/ GAMEBRYO_CORPUS_INVENTORY.csv, TOOLCHAIN_MATRIX.csv,
               SOURCE_ORACLE_INDEX.csv
  02_ANALYSIS/  VERSION_SUPPORT.md, NIF_LOAD_PIPELINE.md, GAMEBRYO_ROSETTA.md,
               TRANSFORM_SEMANTICS.md, BOUNDING_VOLUME_SEMANTICS.md,
               218757_NIF_RESULT.md, GAMEBRYO_SEMANTIC_SIGNATURES.json (optional)
  03_TOOL/      GAMEBRYO_COMPATIBILITY_MATRIX.csv, TOOL_IDENTITY.md
  04_EVIDENCE/  raw oracle outputs per T x adapter, determinism pairs,
               control raw outputs, EXTRACT_PROVENANCE.json, SELECTION_LOCK.json,
               original-tool attempt records (s19-s21)
  05_QC/        QC_REPORT.md (fresh QC worker)
  06_REPORT/    FINAL_REPORT.md, NOT_CHECKED.md, RETRACTIONS_SUPERSESSIONS.md,
               HANDOFF.md, PE_MASTER_REVIEW.md (persistence phase)
tools/gamebryo_oracle/                      (the tool; s22-s23)
```

THE 30 REQUIRED FINAL_REPORT QUESTIONS (order s25; answered separately,
numbered Q1..Q30; each answer carries its evidence status):

The order's section 25 questions govern FINAL_REPORT verbatim (each answer carries its evidence status and deliverable pointer); RUN_CONTRACT (b) is PE-MASTER's P0 narrowing of order s2 — the run's Phases A-D answer the full s2 breadth.

1. Jakie wersje Gamebryo fizycznie posiadamy?
2. Jakie wersje posiadają source?
3. Jakie oryginalne narzędzia fizycznie posiadamy?
4. Które można zbudować?
5. Które można uruchomić?
6. Które potrafią czytać NIF 4.1.0.12?
7. Które potrafią czytać NIF 10.1.0.0?
8. Czy odczyt 10.1 jest FULL czy PARTIAL?
9. Jak original Gamebryo streamuje NIF?
10. Jak działa object factory?
11. Jak działa link/PostLink?
12. Jak przechowywana jest local transform?
13. Jak wyliczana jest world transform?
14. Jak działa AttachChild?
15. Jak działa bounding volume?
16. Czy zbudowano GAMEBRYO_ORACLE_TOOL?
17. Czy tool działa deterministycznie?
18. Czy jest fail-closed?
19. Czy `218757.nif` został poprawnie odczytany?
20. Jak wygląda jego scene graph?
21. Jakie ma wymiary w GAME_UNITS?
22. Czy zawiera world/cell placement evidence?
23. Czy wynik oryginalnego Gamebryo zgadza się z naszym parserem?
24. Jakie różnice znaleziono?
25. Które nasze dotychczasowe NIF assumptions mogą zostać podniesione/obniżone?
26. Co pozostaje UNKNOWN?
27. Jakie nowe Rosetta edges uzyskaliśmy?
28. Czy powstało cokolwiek, co realnie pomoże przyszłemu placement RE?
29. Czy jakikolwiek proprietary payload/source trafił do repo?
30. Czy milestone/governance pozostały bez zmian?

Deliverable pointers: Q1-Q3 -> 01_INVENTORY/ (G-INV-1/2/3); Q4-Q8 ->
02_ANALYSIS/VERSION_SUPPORT.md (G-VER-1/2, pins P1/P2); Q9-Q11 ->
02_ANALYSIS/NIF_LOAD_PIPELINE.md (G-PIPE-1); Q12-Q13 ->
02_ANALYSIS/TRANSFORM_SEMANTICS.md; Q14 -> TRANSFORM_SEMANTICS.md
(AttachChild); Q15 -> BOUNDING_VOLUME_SEMANTICS.md; Q16-Q18 -> 03_TOOL/ +
04_EVIDENCE controls (G-TOOL-1/2/3); Q19-Q22 ->
02_ANALYSIS/218757_NIF_RESULT.md (G-218757-1/2); Q23-Q24 -> 04_EVIDENCE
comparison outputs (G-CMP-1/2); Q25-Q26 -> FINAL_REPORT assumptions section
+ 02_ANALYSIS/NOT_CHECKED.md; Q27 -> 02_ANALYSIS/GAMEBRYO_ROSETTA.md;
Q28 -> FINAL_REPORT placement-assistance section; Q29 -> G-PAYLOAD-1
staging census; Q30 -> terminal block RUN_CONTRACT (p).

## (n) Fresh QC requirements (order section 29; binding for the fresh QC worker)

The fresh QC (pe-master-auditor, NEW context — never this run's formalizer)
must, at minimum:
1. verify hashes INDEPENDENTLY (re-hash T payloads, tool files, basis
   artifacts; never trust the report's numbers);
2. confirm NIF versions from the extracted file headers (not from the
   manifest or the report);
3. re-run >= 3 oracle tests (at minimum: T1 + one 10.1.0.0 T + one
   non-10.1 T if available) and compare against the executor's raw
   outputs;
4. compare raw vs wrapper outputs (the raw 04_EVIDENCE JSONs vs the
   summarized claims — the summary may not exceed the raw);
5. execute or verify the corrupted-input control and the fail-closed
   check (a silent skip = QC_FAIL until reclassified PARTIAL with the
   exact residue);
6. verify NO proprietary file is in the staged set (path census);
7. verify deterministic repeatability (two runs, byte-identical, no
   wall-clock in the body);
8. verify the SELECTION lock order (SELECTION_LOCK.json precedes the
   first oracle output; SELECTION.md byte-identity vs the lock hash);
9. check gate predicates against the actual artifacts (claim -> input rows
   -> computation -> exact boolean predicate), with coverage algebra and
   explicit NOT_CHECKED (any unchecked load-bearing component forbids
   QC_PASS);
10. verify the P1-P7 pin reconciliations from source where load-bearing.
QC verdicts: QC_PASS / QC_PARTIAL / QC_FAIL / QC_BLOCKED (with findings).
The QC report goes to 05_QC/QC_REPORT.md. QC is internal QC — MASTER_ACCEPTED
and milestone closure remain PE-MASTER/human decisions; all verdicts are
ADVISORY_PRE_QUALIFICATION.

## (o) Persistence protocol (order section 30; persistence worker = pe-master-auditor, separately dispatched)

Order of operations (no step skipped, no force push):
1. FINAL REPORT (06_REPORT/FINAL_REPORT.md complete, 30 questions
   answered);
2. HANDOFF (06_REPORT/HANDOFF.md with the terminal block);
3. AUDIT_ENTRYPOINT.md — append ONE factual row to the LATEST RUNS table
   (format per the current file: Commit | RUN_ID/ITER | Package path |
   One-line purpose | PE-MASTER verdict; commit cell = discover via
   `git log -1 -- <package path>` per house convention);
4. MANIFEST LAST — MANIFEST_SHA256.csv at the package root covering EVERY
   package file EXCEPT itself;
5. VERIFY BIJECTION — census the package tree on disk vs the manifest:
   every file present is hashed in the manifest and every manifest row
   exists on disk (bijection, zero orphans both ways);
6. STAGE — path-limited staging of EXACTLY: the package
   (`docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/`),
   `tools/gamebryo_oracle/`, `AUDIT_ENTRYPOINT.md`. NEVER `git add -A`;
   never stage any of the six OUT_OF_SCOPE untracked entries (PREFLIGHT
   section 2);
7. VERIFY STAGED — `git status`/`git diff --cached --name-only`: the
   staged set MUST equal the authorized set (G-PAYLOAD-1 census) — zero
   Gamebryo source/ISO/lib/binaries, zero original NIF/BNT/VFS/EXE
   payloads; on any foreign staged path: STOP, report conflict, never
   unstage/absorb;
8. ONE COMMIT — a single path-limited commit (message in repo style:
   run id + one-line purpose); re-check HEAD before committing if any
   intervening commit appeared;
9. PUSH — normal push (no force push);
10. THREE-WAY VERIFY — HEAD == origin/master == live remote
    (`git ls-remote`); record the pushed SHA in HANDOFF.md. If the push
    fails: record REMOTE_SYNC_PENDING, NEVER claim published, return to
    PE-MASTER.
The persistence worker performs byte-identity verification of any
PE-MASTER review it persists; PE_MASTER_REVIEW.md goes to 06_REPORT/.

## (p) Terminal block (order section 31; filled at run end, in 06_REPORT/HANDOFF.md)

```
GAMEBRYO_ORACLE_TOOL_BUILT = YES | PARTIAL | NO
GB_NIF_10_1_SUPPORT        = CONFIRMED | PARTIAL | REJECTED | UNKNOWN   (per GB version, with per-version verdicts)
218757_ORACLE_RESULT       = <summary + status>
WORLD_PLACEMENT_RECOVERED  = NO   (unless an unambiguous, independently verified
                                    world/cell placement record appears IN THE NIF
                                    ITSELF; if it appears: HARD STOP immediately)
RUN_STATUS                 = COMPLETE_FOR_SCOPE | PARTIAL | BLOCKED_EXTERNAL + HARD_STOP_REASON
HARD_STOP                  = YES (after publication; pending Desktop post-audit of the exact pushed SHA)
NEXT_EXPERIMENT_AUTHORIZED = NO
AUTOMATIC_CONTINUATIONS    = NONE (no 218757 EXE scan, no placement tracing,
                                   no Ark insertion-edge RE, no building-family search,
                                   no runtime/network analysis, no milestone/Q1 changes)
```

All values are advisory (ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT
= NONE while Q1 is absent). The run ENDS at the HARD STOP; the human
decides everything after it.

## (q) Final handoff schema (EVERY child batch return to PE-MASTER)

Every batch (E1, E2, E3, fresh QC, PERSIST) returns compactly, never empty:

```
ASSIGNMENT_MODE / RUN_ID / PARENT_LOOP_ID / MILESTONE / SCOPE (batch id) /
BUDGET_USED (calls used / minutes used vs preregistered cap) /
GATE_RESULTS (per gate touched: PASS/PARTIAL/FAIL/BLOCKED/UNKNOWN/NOT_TESTED) /
FINDINGS (bold severity, exact source, effect, correction, revalidation predicate) /
FULL_READ_LOG / NOT_CHECKED / OUTPUT_PATHS + SHA256 / INPUT_HASHES (key inputs re-hashed) /
FILES_CHANGED / BASE_SHA / HEAD_SHA / PUSH_STATUS (executor batches: NO_GIT_OPERATIONS) /
UNRELATED_WORK_EXCLUDED / NEXT_PARENT_ACTION / RESUME_POINT (if PARTIAL or interrupted)
```

Rules: budget exhaustion -> honest PARTIAL with the exact stop point
(RUN_BUDGET.md); a failed experiment is a result; three similar failures
require a new method or a blocked branch, not a declaration that the run
is finished; CORRECTION_REQUESTs (scope, inputs, authorization) go to
PE-MASTER — no worker dispatches anything itself (NO_NESTED_TASKS); if
interrupted, persist a precise RESUME_POINT on disk before returning.
