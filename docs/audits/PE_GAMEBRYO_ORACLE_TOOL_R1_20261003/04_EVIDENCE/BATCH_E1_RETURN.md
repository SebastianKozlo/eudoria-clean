# BATCH E1 RETURN — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003

Persisted to disk before the chat return (L16/L25 discipline). Schema per
RUN_CONTRACT (q).

- **ASSIGNMENT_MODE:** PE-MASTER direct dispatch (batch E1 of the bounded run;
  NO_NESTED_TASKS respected — no agent launched, no loop state touched).
- **RUN_ID:** PE_GAMEBRYO_ORACLE_TOOL_R1_20261003
- **PARENT_LOOP_ID:** 8f0ef23a-964b-4767-ac59-1ec593a1b118
- **MILESTONE:** none (CONTRIBUTES_TO EU935-M2/M3/M10/M11; MILESTONE_ADVANCEMENT
  = NONE; CANONICAL_GATE_EFFECT = NONE; all verdicts ADVISORY_PRE_QUALIFICATION).
- **SCOPE:** Batch E1 = Phase A forensic inventory + Phase B version support +
  Phase C NIF load pipeline + T-corpus selection + SELECTION lock. NO tool
  building, NO oracle runs (E2).
- **BUDGET_USED:** 58 tool calls of <= 60; ~40 wall minutes of <= 150.
- **RUN_STATUS: COMPLETE_FOR_SCOPE** (all E1 gates resolved, none waived).

## GATE_RESULTS

G-INV-1 **PASS**; G-INV-2 **PASS**; G-INV-3 **PASS**; G-VER-1 **PASS**;
G-VER-2 **PARTIAL** (source-level complete; executed column is E2 by design);
G-PIPE-1 **PASS**; G-SEL-1 **PASS** (locked before any oracle run — none exist);
G-SEL-2 **PASS**; G-TOOL-1..4 / G-CMP-1/2 / G-218757-1/2 / G-MATRIX-1 /
G-PKG-1 / G-PAYLOAD-1 / G-SIG-1 **NOT_TESTED** (E2 or persistence phases).
Full rows: 00_CONTROL/STAGE_ACCEPTANCE_GATES.csv.

## FINDINGS

1. **[HIGH, source-proven] GB 2.6 REJECTS the PCG corpus.** GB 2.6
   `ms_uiNifMinVersion = 10.1.0.114` (Gb26_src\NiStream.cpp L48-49, sha256
   72781EEB...) — NIF 10.1.0.0 and 4.1.0.12 are below the floor ("NIF version is
   too old.", OLDER_VERSION). **Effect:** the 2.6 toolchain (SceneDesigner,
   AssetViewer, PhysXNifViewer...) is NOT an oracle for the T-corpus;
   **correction:** E2 oracle adapters must center on GB 1.2 (and test GB 1.1.2
   via its binary libs); **revalidation predicate:** E2 executed-loader
   negative control on GB 2.6 (expected explicit rejection).
2. **[HIGH, source-proven] GB 1.2 reads NIF 3.3.0.11..10.2.0.0** — 10.1.0.0 and
   4.1.0.12 both in range (NiStream.cpp L42-46, L303-336, sha E955C36E...).
   Unknown class names FAIL the whole load (LoadRTTI RTTIError, L427-433) —
   fail-closed by construction. **Prediction for E2 (not executed evidence):**
   T-corpus files containing MindArk NiArk* blocks will fail GB 1.2 LoadRTTI
   unless NiArk loaders are registered. **Revalidation predicate:** E2 runs.
3. **[MEDIUM] GB 1.1.2 writes/identifies NIF 10.1.0.0** (installed SDK
   NiVersion.h L18-21, sha 67C9C745) — same version string as the PCG 9.3.5
   corpus headers; but its read range is compiled into NiMain.lib (binary) →
   UNKNOWN from source; P4 lib pin CONFIRMED (FF4519AF..., 3,073,590 B).
4. **[MEDIUM] GB 2.3 evaluation is a binary SDK** (Wise installer; 0 NI*.cpp in
   its 4,642-entry file table); version 2.3.0.0 / NIF 20.3.0.9 proven from the
   recovered NiVersion.h (sha DFCCD6EC) + disk label "Gamebryo 2.3 Evaluation
   Disk 1". Read range = UNKNOWN (binary).
5. **[CANON] P1 value CONFIRMED (10.2.0.0), location superseded** — the constant
   lives in NiStream.cpp L44-46, fed by NiVersion.h macros (proposal R1 in
   RETRACTIONS_SUPERSESSIONS.md). P2 CONFIRMED EXACTLY (NiObject.cpp L134-143,
   5.0.0.6 <= v < 10.1.0.114; the v10-parser "dummy uint32" is the GroupID —
   proposal R3). P5 T1 reference values: ALL MATCH by fresh re-extraction.
6. **[STRUCTURAL] The serialized world bound does not exist** — NiAVObject/
   NiNode LoadBinary read no bound; model-space spheres serialize only inside
   NiGeometryData (L618 GB12 / L279 GB26); world bounds are recomputed at update
   (UpdateWorldData: `m_kWorld = parent->m_kWorld * m_kLocal`, identical in
   GB12/GB26, NiAVObject_Win32.cpp L22-31). No serialized root bound in any
   version — 218757 dimensions in E2 must be derived from per-geometry model
   bounds + local transforms, in GAME_UNITS.

## FULL_READ_LOG (complete reads this run)

Contracts (100%): AUTHORIZATION.md, RUN_CONTRACT.md, PREFLIGHT.md, SELECTION.md,
RUN_BUDGET.md. Reference script: s1_template4057_repin.py (method reuse).
Evidence packs (complete): GB_1_1_2 (1,227 lines), GB_2_3 (436); targeted
sections of GB_1_2/GB_2_6 packs (NiVersion.h, NiViewerStrings, NiObject.cpp,
NiBinaryStream.cpp, NiStream.cpp Load* functions, NiStream.h version decls,
NiAVObject.cpp/inl, NiNode.cpp/inl, NiObjectNET.cpp, NiGeometryData.cpp,
NiTexturingProperty.cpp, NiSourceTexture.cpp, NiBound.*, NiBoxBV/NiSphereBV/
NiBoundingVolume bodies, NiAVObject_Win32.cpp full) — line-numbered extracts in
sandbox\phaseBC\evidence_*.txt. NOT_CHECKED items (19) listed in
02_ANALYSIS/NOT_CHECKED.md.

## OUTPUT_PATHS + SHA256 (package, all created by E1)

- 01_INVENTORY/GAMEBRYO_CORPUS_INVENTORY.csv — 80BCCE2B2C950F8D6665D6573F5A99014EB86C7BEC95734697999A1C89C7AB53
- 01_INVENTORY/TOOLCHAIN_MATRIX.csv — D5E814817E19B31178FBFFBE5FCA1FDCDC68108A268EC09C814DF1685B6F5E5D
- 01_INVENTORY/SOURCE_ORACLE_INDEX.csv — 25172B700BAA0DC9A0E8FDDD31D3064C3A754AC70CDED8327F37EF9A46E52C74
- 02_ANALYSIS/VERSION_SUPPORT.md — C4F971DDDF93698D1A16DBFB1DA9D7B948CF36624D2B1B6A0175FF44934819A2
- 02_ANALYSIS/NIF_LOAD_PIPELINE.md — 23FBC50F6D87821DEF906F19B7B73485C347B985A57751872DB9CB89BF378C07
- 02_ANALYSIS/GAMEBRYO_ROSETTA.md — 749A3B81E970AE711755552CEF10E36CC39F08F2D65A5221DE5FFEF3E381410E
- 02_ANALYSIS/TRANSFORM_SEMANTICS.md — EA5AE9746D8F3FFAAFD28BD5E3D8B3E537F8E93122A039F3DA48C0C256A2B341
- 02_ANALYSIS/BOUNDING_VOLUME_SEMANTICS.md — 5910A14D51A85390C892986D810C8B2DFAB7F69F1A60B84E73B04866B4001C40
- 02_ANALYSIS/NOT_CHECKED.md — 8FFBABA4699446287302A7A44DA72D3A2AFCE9E5F8A13BA6A27BF33AFF97EFB8
- 02_ANALYSIS/RETRACTIONS_SUPERSESSIONS.md — ABFF5D4198130E5908CB495DC35DBBAD986D4A5C4FEB8DC1427C393F2D0BFC9C
- 00_CONTROL/STAGE_ACCEPTANCE_GATES.csv — (this batch; hash computable at persistence; content = 21 gate rows)
- 00_CONTROL/SELECTION.md (EDITED: T1-T5 rows filled, then locked) — 4A67C6B844B6DA65DF403AA5B87B8012FECB7CBBF60051422E306E93C733381C (== SELECTION_LOCK_SHA256)
- 04_EVIDENCE/EXTRACT_PROVENANCE.json — 4472C84560B9E8314CE3EFB920323BFA4CF7BC0457D0EE6E9199B0C83064A466
- 04_EVIDENCE/SELECTION_LOCK.json — 11155D9FD770A6622AB756CA61B54774F53124688723156A9C12C837B50501BD
- 04_EVIDENCE/scripts/{phaseA_inventory.ps1, phaseBC_evidence.py, phaseBC_gb23_fix.py, phase_selection.py, gen_inventory_csvs.py} — hashes in the package census (this file's generation excluded only itself from hashing; scripts: 165C90B6..., 833F6F0B..., 36A6E52D..., 84C185D8..., F96DC072...)
- 04_EVIDENCE/BATCH_E1_RETURN.md — this file
- Sandbox (LOCAL_ONLY, never committed): 5 T payloads (sha256 = manifest values;
  218757.nif = 3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36),
  6 archive listings, exe census (BB4DC9E9...), inventory_data.json
  (7BBC26A3...), evidence packs (D593C4CD / D2796EE3 / C1E11589 / 2156DC68),
  source_oracle_index.json (451CD87B...), selection_report.json, GB23 SDK
  header extractions.

## INPUT_HASHES (re-hashed this run)

- Models.bnt: 395,412,868 B — C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0 (== pin, fail-closed gate PASS)
- pcg953_nif_manifest.csv: 2,827,906 B — 2BE0DEFC9C09FF26371528A4601C10216AC3013717A244EB0652169123989B59 (== pin, PASS; 5,596 logical rows via real CSV parser)
- 6 archives: 171E36A2... (GB112 zip) / 43088FD3... (GB12 rar) / 0ACE9FD8... (GB2.6 7z) / 9923569B... (GB1.2 7z) / 139783A9... (GB112 iso) / AF3391BF... (GB2.3 iso)
- GB112 NiMain.lib VC71 ReleaseLib: FF4519AFD2475D9A6E71A35E5DB6B0F5A0B7E9E86EC3662C6A340DA19BA06597 (P4 PASS)
- GB23 SDK setup exe: 69F84692D8BF857D607B30C6748F18B8FDEA857D43B63C56B4E63619E74C015E (187,899,445 B)

## FILES_CHANGED

Only inside docs/audits/PE_GAMEBRYO_ORACLE_TOOL_R1_20261003/** (the authorized
package root): all 01_INVENTORY/02_ANALYSIS/04_EVIDENCE files are NEW;
00_CONTROL/SELECTION.md is the only pre-existing file edited (T1-T5 rows + lock
per protocol); 00_CONTROL/STAGE_ACCEPTANCE_GATES.csv new (executor duty).
NO writes to D:\gamebyroengine, pcg_install, src/, AUDIT_ENTRYPOINT.md, skills,
or any OUT_OF_SCOPE untracked path. Sandbox writes confined to
D:\Eudoria_Reconstruction\99_Audits\PE_GAMEBRYO_ORACLE_TOOL_R1_20261003\sandbox\.

## BASE_SHA / HEAD_SHA / PUSH_STATUS

- BASE_SHA: f33c7b9c201b02b8e0f8c7010275b6217475b5a4 (dispatch pin; == HEAD ==
  origin/master per PREFLIGHT, formalizer-verified 2026-10-03)
- HEAD_SHA: NOT_TOUCHED — zero git commands executed in E1 (contract (h): no
  git operations of any kind before the persistence phase)
- PUSH_STATUS: NO_GIT_OPERATIONS (executor batch)

## UNRELATED_WORK_EXCLUDED

The six OUT_OF_SCOPE untracked entries (PREFLIGHT section 2) were neither read
for absorption, modified, nor staged; no foreign work is included in any E1
output. The interrupted-run sandbox was used read-only as a cross-check basis
only (values now REPRODUCED_THIS_RUN).

## NEXT_PARENT_ACTION

1. Audit E1 from disk (this file + the package); independent QC is the fresh
   pe-master-auditor batch per RUN_CONTRACT (n).
2. Decide the P1-wording and GroupID ("dummy uint32") supersession proposals
   (RETRACTIONS_SUPERSESSIONS.md R1/R3) — recorded as proposals only.
3. Dispatch Batch E2 (<= 80 calls / <= 180 min per RUN_BUDGET): build
   tools/gamebryo_oracle; adapters should center on **GB 1.2 (source-supported
   range) with GB 1.1.2 binary testing**; include the GB 2.6 wrong-version
   negative control (source-predicted explicit rejection); run the locked
   T1-T5; 218757 probe; compatibility matrix; comparison vs our decoder;
   FINAL_REPORT (30 questions).

## RESUME_POINT

None — batch complete for scope. For E2 continuity: all E2 inputs are on disk
(locked SELECTION.md; EXTRACT_PROVENANCE.json; payloads in sandbox\payloads\;
evidence packs + source_oracle_index.json in sandbox\phaseBC\; tool census in
sandbox\phaseA\). If E2 chooses to re-verify, re-run
04_EVIDENCE/scripts/phase_selection.py (fail-closed) and compare against
SELECTION_LOCK_SHA256.

## SELF_CHECK (executor's own, labelled — NOT independent MASTER audit)

- Re-hashes executed by scripts, not trusted from pins (Models.bnt, manifest,
  all 6 archives, P4 lib, all cited source files hashed by the evidence packer).
- G-INV-1 recount: 8 top-level items re-counted physically (TOPLEVEL_COUNT=8).
- Selection: mechanical rules + tie-breaks executed BEFORE any oracle run (no
  oracle output exists in the repo or sandbox); real CSV parser (5,596 rows;
  naive-line count explicitly avoided); own BNT2 walk calibrated on the
  296445.nif anchor + T1 reference (ALL MATCH) before any candidate was
  trusted; zero candidate exclusions; all extracted sha256 == manifest sha256.
- No default-success fallbacks: both fail-closed pins would have HARD_STOPped
  the run on mismatch; the one mid-run error (gb23 listing parse) produced an
  honest "absent" result that was fixed and re-run, and is disclosed in
  RETRACTIONS_SUPERSESSIONS.md R5.
- Era separation maintained in every artifact row (version_category columns;
  no cross-version claims without per-version citation).
- Zero proprietary payload bytes in the repo (package census = md/csv/json +
  scripts only); T payloads LOCAL_ONLY.
