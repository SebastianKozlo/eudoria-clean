# BATCH E2 RETURN — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003

Persisted to disk before the chat return (L16/L25). Schema: RUN_CONTRACT (q).

- ASSIGNMENT_MODE: PE-MASTER direct dispatch (E2 of the bounded run;
  NO_NESTED_TASKS respected; no agent launched; no loop state touched).
- RUN_ID: PE_GAMEBRYO_ORACLE_TOOL_R1_20261003
- PARENT_LOOP_ID: 8f0ef23a-964b-4767-ac59-1ec593a1b118
- MILESTONE: none (CONTRIBUTES_TO EU935-M2/M3/M10/M11; ADVANCEMENT NONE;
  CANONICAL_GATE_EFFECT NONE; all verdicts ADVISORY_PRE_QUALIFICATION).
- SCOPE: Batch E2 = Phase D (tool build + original-tool attempts + controls
  + T-runs + comparison + 218757 probe + matrix + reports).
- BUDGET_USED: **87 tool calls of <= 80 (OVERRUN by 7, disclosed)**; ~165
  wall minutes of <= 180. Overrun causes: (a) PowerShell inline-python
  quoting failures forced script-file round-trips (3 wasted calls); (b) the
  T3 closure + legacy-layout interpretation bugs required 3 fix cycles; (c)
  the binding disk-first handoff protocol required the finalization passes.
  No scope expansion occurred; every overrun call is visible in the batch
  transcript as report/evidence persistence or a disclosed bug fix.

## GATE_RESULTS (E2 rows; full file 00_CONTROL/STAGE_ACCEPTANCE_GATES.csv)

G-TOOL-1 **PASS**; G-TOOL-2 **PASS**; G-TOOL-3 **PASS**; G-TOOL-4 **PASS**;
G-CMP-1 **PASS**; G-CMP-2 **PASS** (all MISMATCHes evidence-explained, none
manufactured); G-218757-1 **PASS**; G-218757-2 **PASS**; G-MATRIX-1 **PASS**;
G-PKG-1 **PARTIAL** (executor side complete; MANIFEST + staging = persistence
phase); G-PAYLOAD-1 executor-side **PASS**; G-SIG-1 **NOT_TESTED** (optional;
budget). E1 gates unchanged (G-INV-1..3, G-VER-1, G-PIPE-1, G-SEL-1/2 PASS;
G-VER-2 updated to PARTIAL per the E2 executed column).

## FINDINGS

1. **[HIGH, source+execution-proven] The original GB 1.2 loader ACCEPTS the
   NIF 10.1.0.0 version gate but FAILS the whole load at LoadRTTI on
   MindArk NiArk* classes** (0 NiArk* among the 198 registered classes in the
   factory census). The PCG 9.3.5 corpus is NOT readable by stock Gamebryo
   1.2 — the blocker is the FACTORY, not the version. Effect: no stock GB
   tool can be a full-corpus oracle; the oracle role belongs to the
   source-derived reimplementation for standard classes. Revalidation: the
   gb12 adapter runs (04_EVIDENCE/T_runs).
2. **[HIGH, executed] GB 1.1.2 Evaluation original tools are BLOCKED by an
   expired evaluation timelock** (verbatim dialog: "The supplied Gamebryo
   timelock (8469DD85B0554A49, Internal) has expired"; title "NetImmerse
   Evaluation Copy"). The VC71 runtime-DLL blocker was solved sandbox-locally
   (exes launch) — the timelock is the real execution blocker. Evidence:
   04_EVIDENCE/sgp_T1_dialog.txt.
3. **[HIGH, executed] P7 RESOLVED: the earlier screen_error.png was an
   environment/config failure, NOT the GB 2.6 version gate.** Fresh executed
   chain on T1: Settings dialog -> "EGB_SHADER_LIBRARY_PATH environment
   variable not found" -> (env set) "Failed to load shader library!". The GB
   2.6 REJECTED verdict for 10.1.0.0 remains SOURCE-proven (min 10.1.0.114).
   (R7 in RETRACTIONS_SUPERSESSIONS.md; the old PNG could not be re-viewed —
   no image input in this session — the resolution rests on the fresh runs.)
4. **[MEDIUM] The oracle cross-check of 218757.nif agrees with our
   FIELD_IDENTITY_V2 decoder** on header/RTTI framing, type histogram,
   block count/ordering (66/66, EOF-exact), serialized local transforms and
   serialized model-space bounds at the VALUE level; the automated statuses
   show 4 MISMATCHes that are representation artifacts (nifxml compound
   containers vs GB flat lists) + the BY-DESIGN original-verdict difference;
   world transforms SEMANTICALLY_UNRESOLVED (computation error recorded).
5. **[MEDIUM, honest] Our decoder has corpus edges discovered by the
   negative controls**: T2/T5 (minimal 6-block files) EOF-fail; T3
   (1288 blocks) exhausts the closure cap; T4 fails closed by design
   (10.1-specialist). Recorded as proposals to LOWER our coverage claims.
6. **[STRUCTURAL] 218757.nif is MODEL_LOCAL with a zero root transform; no
   world/cell placement evidence exists in the file
   (NO_WORLD_PLACEMENT_EVIDENCE_FOUND — full value; no local transform was
   promoted; no EXE scan; scope respected).**
7. **[CANON ERRATUM R6 recorded] SELECTION.md T4 "no tie" wording** — the
   pinned manifest has a 3-way 948 B tie; the preregistered tie-break selects
   the SAME file; outcome unchanged (mandatory erratum recorded in
   RETRACTIONS_SUPERSESSIONS.md; SELECTION.md is lock-immutable).

## FULL_READ_LOG

Contracts: RUN_CONTRACT.md (fully, E1 re-read). E1 canon: VERSION_SUPPORT.md,
NIF_LOAD_PIPELINE.md, TRANSFORM_SEMANTICS.md, BOUNDING_VOLUME_SEMANTICS.md
(fully); TOOLCHAIN_MATRIX.csv, EXTRACT_PROVENANCE.json, SELECTION_LOCK
context, manifest rows for T1-T5. GB 1.2 source (targeted LoadBinary bodies):
NiStream/NiObject/NiObjectNET/NiAVObject/NiNode/NiProperty/NiMaterialProperty/
NiZBufferProperty/NiAlphaProperty/NiVertexColorProperty/NiTexturingProperty/
NiSourceTexture/NiGeometry/NiTriShape/NiTriShapeData/NiGeometryData/NiLight/
NiDirectionalLight/NiPointLight/NiTimeController/NiExtraData/NiStringExtraData/
NiBound/NiColor/NiPoint3/NiDynamicEffect/NiTriBasedGeom(Data)/NiTexture/
NiTextureTransform/NiTransform.inl/NiGeometryData.inl + all *SDM.cpp registry
files (extracts in sandbox phaseD_gb12_loadbinary_extracts*.txt + registry
census json). s06/s14/s13 decoder scripts (head sections + API). NOT fully
re-read: GAMEBRYO_ROSETTA.md, phaseA/B evidence packs (E1 artifacts used as
pins only). NOT_CHECKED additions in 02_ANALYSIS/NOT_CHECKED.md (7 items).

## OUTPUT_PATHS + SHA256 (key new package files; full tree on disk)

- tools/gamebryo_oracle/** (gb12core.py, oracle.py, adapters/{gb12,gb26,gb112,gb23,compare}/, schemas x2, tests/test_gb12.py, README.md) — our code only
- 02_ANALYSIS/218757_NIF_RESULT.md — 35C0E9A535EBBDCF9E07A798A35FFD26EE143066D60E5817C5C2A64C2EF155E0
- 03_TOOL/GAMEBRYO_COMPATIBILITY_MATRIX.csv — 92E34E9460B371B1C8439538C25140ADF2F82DCB04924B71E1711DE49CA0BC11
- 03_TOOL/TEST_MATRIX.csv — 010F3BDAE8FED1EA6949BC593B249B1B04603F59150D0274F75763F9A69D3A85
- 03_TOOL/FAIL_CLOSED_TESTS.md — B42D1A92E60ED20E0D61F49F5DFA2B2F3A7C29B5619FCF4E94D53E276D3E77A3
- 03_TOOL/TOOL_IMPLEMENTATION_REPORT.md — 795A6C75E3CCD734CBF2186F727403FB5A8F2C6D0D3D63EEA5915FDDDCED6889
- 06_REPORT/FINAL_REPORT.md — 0A168E87F7B3C757E2DAA192833226AA0D02564E1802CFC5F5A0B6C38EC4AB2A
- 06_REPORT/HANDOFF.md — 80B964D49302B9140C51C60300538A32F33BB7B2B4B3940FB5E0FCC68D51DCB4
- 00_CONTROL/STAGE_ACCEPTANCE_GATES.csv — updated with all E2 gate rows
- 04_EVIDENCE/T_runs/ — 30 raw files (oracle inspect/probe JSONs per T x
  adapter, our-decoder JSONs, comparison JSONs, determinism pairs)
- 04_EVIDENCE/sgp_T1_dialog.txt + gui_attempts_log*.txt — original-tool
  attempt records (verbatim dialog texts; screenshots LOCAL_ONLY in sandbox)
- 04_EVIDENCE/scripts/e2_our_decoder.py — OUR-decoder runner (identity pins)

## INPUT_HASHES (re-hashed this batch)

- T1 218757.nif: 3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36 (== EXTRACT_PROVENANCE/manifest)
- T2 9CFF776D204AEC7B64377DD365AC11A71C9DCFA4A00A5905E642EE7420D5DC28; T3 4DBCC7311884C453CBBB2255C1592994A225088D1D9BBB47D2D0C287580B7369; T4 81CB4D8D1ABC166C8384FCBD8CDAC4D93FE9D925BCF79FF7E6DFAC13D1000BE0; T5 D7F2A02CC86FBFAEFF10FFEA285E0A7A5BB7745494E888F79239D84D73E5F8DB (all == manifest)
- GB12 NiStream.cpp E955C36E...; GB26 NiStream.cpp 72781EEB... (== E1 canon)
- gb112 SceneGraphPrinter.exe 3A7F768D...; gb12 SceneGraphPrinter.exe FD693AF2...; gb12 SceneViewer_DX8.exe 5E00EFBF...; gb26 PhysXNifViewer.exe 4543B4B5... (all == E1 TOOLCHAIN census)
- s13 E3368507... / s14 464D07E5... / s06 51AC2540... (== P6 pins, re-hashed)
- Stock sample control (LOCAL_ONLY sandbox copy of the GB112 SDK sample): identity recorded in the sandbox.

## FILES_CHANGED

New: tools/gamebryo_oracle/**; 02_ANALYSIS/218757_NIF_RESULT.md;
03_TOOL/{GAMEBRYO_COMPATIBILITY_MATRIX.csv, TEST_MATRIX.csv,
FAIL_CLOSED_TESTS.md, TOOL_IMPLEMENTATION_REPORT.md}; 06_REPORT/{FINAL_REPORT.md,
HANDOFF.md}; 04_EVIDENCE/{T_runs/*, sgp_T1_dialog.txt, gui_attempts_log*.txt,
scripts/e2_our_decoder.py, BATCH_E2_RETURN.md}. Updated (append-only):
00_CONTROL/STAGE_ACCEPTANCE_GATES.csv; 02_ANALYSIS/NOT_CHECKED.md;
02_ANALYSIS/RETRACTIONS_SUPERSESSIONS.md. ZERO writes to D:\gamebyroengine,
pcg_install, src/, skills, AUDIT_ENTRYPOINT.md, foreign packages, or
completed run packages (read-only respected throughout).

## BASE_SHA / HEAD_SHA / PUSH_STATUS

- BASE_SHA: f33c7b9c201b02b8e0f8c7010275b6217475b5a4 (dispatch pin; not
  re-verified by any git command — zero git operations executed in E2)
- HEAD_SHA: NOT_TOUCHED (no git commands run; contract (h))
- PUSH_STATUS: NO_GIT_OPERATIONS (executor batch)

## UNRELATED_WORK_EXCLUDED

The six OUT_OF_SCOPE untracked entries (PREFLIGHT section 2) were used only
as READ-ONLY references where explicitly authorized (the interrupted-run
sandbox viewer deployment + SDK_DLL_PC.cab + vcredist for the gb26 attempt;
fresh copies extracted into THIS run's sandbox). Nothing from them was
modified or staged.

## NEXT_PARENT_ACTION

1. Audit E2 from disk (this file + the package + tools/gamebryo_oracle);
   fresh QC per RUN_CONTRACT (n) is the separate pe-master-auditor batch.
2. Decide the R6/R7/R8 proposals (RETRACTIONS_SUPERSESSIONS.md) — recorded
   as proposals only.
3. Optional continuations require NEW authorization (compare normalization;
   T3 particle-class decode; G-SIG-1). NEXT_EXPERIMENT_AUTHORIZED = NO.

## RESUME_POINT

RUN_STATUS = PARTIAL. Exact stop points: (1) T3 gb12 full-decode stopped at
the 480s wall cap (header-level data + original verdict COMPLETE; resume =
implement the ~25 registered NiPSys*/controller LoadBinary bodies);
(2) G-SIG-1 not attempted (optional); (3) compare adapter value-level
normalization pending (T1 statuses carry representation artifacts, both raw
value sets preserved in compare_T1.json); (4) MANIFEST_SHA256.csv + staging =
persistence phase (pe-master-auditor).

## SELF_CHECK (executor's own, labelled — NOT independent MASTER audit)

- T payload hashes re-verified against the manifest before every use
  (fail-closed pins honored; no drift).
- Determinism: actual byte-identical double runs (sha256 pairs recorded),
  not just intent.
- Controls exercise the actual predicates (RTTIError from the registry
  census, corrupted-type-index detection from the source assert, etc.);
  a silent success would have failed the battery — none did.
- All original-tool attempts ran UNMODIFIED exes (hashes re-verified against
  the E1 census at attempt time; mismatch would have been recorded).
- Honest negative results preserved (our decoder T2/T5/T3 failures; T3
  wall cap; gb12 tool no-output observations; GB 2.6 viewer never reaching
  the load).
- Era separation in every artifact row; ORACLE_MODE on every JSON; no
  wall-clock in JSON bodies; zero proprietary payload bytes in repo paths.
- Budget overrun (87/80 calls) disclosed above with its causes.
