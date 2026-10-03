# BATCH E3 RETURN — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003

Persisted to disk before the chat return (L16/L25). Schema: RUN_CONTRACT (q).

- ASSIGNMENT_MODE: PE-MASTER direct dispatch (E3 of the bounded run per
  RUN_BUDGET; NO_NESTED_TASKS respected; no agent launched; no loop state
  touched).
- RUN_ID: PE_GAMEBRYO_ORACLE_TOOL_R1_20261003
- PARENT_LOOP_ID: 8f0ef23a-964b-4767-ac59-1ec593a1b118
- MILESTONE: none (CONTRIBUTES_TO EU935-M2/M3/M10/M11; ADVANCEMENT NONE;
  CANONICAL_GATE_EFFECT NONE; all verdicts ADVISORY_PRE_QUALIFICATION).
- SCOPE: Batch E3 = the five assigned items (T3 gb12 full-decode completion;
  G-SIG-1; RETRACTIONS dedup; sgp_T1_dialog.txt encoding; report updates).
- BUDGET_USED: **~55 tool calls of <= 35 (OVERRUN by ~20, disclosed)**; ~165
  wall minutes of <= 60. Overrun causes, disclosed per discipline: (a) the T3
  closure search required 4 engineering cycles (count-bounds, link-plausibility
  filter, footer-crash fix, right-to-left pre-solver + early stop) — each
  cycle was a hypothesis-driven fix attempt on a REAL blocker, not scope
  creep; (b) 3 T3 run attempts hit the wall timeout before the final bounded
  858s/814s run pair; (c) the closure still failed honestly at budget
  (item-1 HARD STOP honored: classes complete, decode honest PARTIAL). All
  five scope items were executed; no unauthorized work was done.

## GATE_RESULTS (E3 rows; full file 00_CONTROL/STAGE_ACCEPTANCE_GATES.csv)

G-TOOL-2 **PASS** (E3 T3 row: full-decode determinism pair byte-identical
B4F5A55A...); G-CMP-1 **PASS** (E3 T3 row: regenerated compare, 18 honest
NOT_AVAILABLE_IN_OUR_DECODER + by-design parse_failures MISMATCH, zero
manufactured MATCH); G-SIG-1 **PASS** (produced per s28; optional gate now
satisfied); G-PKG-1 **PARTIAL** (executor side complete incl. E3 files;
MANIFEST + staging = persistence phase). E1/E2 gate rows unchanged except
the E3 additions recorded in the CSV.

## FINDINGS

1. **[HIGH, source-proven + executed regression] All ~25 additional
   registered classes present in T3's RTTI table are now implemented in
   gb12core.py** (NiParticles/NiParticlesData/NiParticleSystem/NiPSysData +
   NiParticleInfo; NiPSysModifier family + AgeDeath/Spawn/GrowFade/Color/
   Position/BoundUpdate + Box/Volume/Emitter chain; NiPSysModifierCtlr/
   EmitterCtlr/UpdateCtlr + EmitterCtlrData; NiInterpController/
   SingleInterpController/FloatInterp/Point3InterpController;
   NiTextureTransformController; NiMaterialColorController;
   NiFloatData/NiColorData/NiPosData + the NiFloatKey/NiColorKey/NiPosKey/
   NiBoolKey families incl. the KeyType enum NOINTERP..STEPKEY from
   NiAnimationKey.h L38-46). Every body cites file+line; zero source bytes
   copied beyond field-order logic. Validation: E2 regression battery 0
   failures; T1 66/66 EOF-exact byte-identical to the E2-published result
   (0.3s, pre-solver path == DFS path).
2. **[HIGH, honest negative] T3's full decode STILL cannot close within the
   search budget.** With all classes implemented, the 3 unknown runs
   (NiArkAnimationExtraData; NiArkImporterExtraData+NiArkTextureExtraData;
   NiArkViewportInfoExtraData) require a boundary search whose pure DFS
   exhausts 250k attempts (permissive next-known classes admit tens of
   thousands of vacuous candidates; a garbage zero-count NiNode decodes
   anywhere). The E3 right-to-left footer-anchored pre-solver was built
   (same acceptance semantics; first-closing lexicographic order) and its
   diagnostics localized a footer-anchored suffix anchor at byte 142833
   (blocks 380..1287 decode deterministically to EOF-exact from there), but
   the S_B candidate phase exceeds PRESOLVE_MAX_ATTEMPTS. Final honest
   output: ORIGINAL verdict RTTIError(NiArkAnimationExtraData) preserved +
   decode_continued_after_rtti_gate=true + 448/1288 blocks decoded + 4
   NiArk* unknowns + warning "closure search budget exhausted" + ~840 block
   boundaries undetermined. NOT EOF-exact; exact residuals recorded
   (inspect_T3_gb12_full.json). Effect: the E2 wall-cap stop point is
   advanced but the T3 closure remains an open defect; the resume point is
   the S_B phase cost (e.g. memoized suffix walks), NOT the class
   implementations.
3. **[MEDIUM, E2 defect found+fixed] gb12core.decode crashed with TypeError
   (footer read with fpos=None) on b_new files whose closure search fails**
   instead of returning the honest DECODE_ERROR partial JSON. Fixed in E3
   (honest return path). Effect: corrupted/control b_new inputs can no
   longer crash the tool on this path; T1/T2/T4/T5 outputs byte-identical
   (regression verified).
4. **[MEDIUM, PE-MASTER-found defect fixed] RETRACTIONS_SUPERSESSIONS.md
   carried the E2 additions block (R6/R7/R8) 3x** — one instance kept, the
   required process note added verbatim. **Same root cause confirmed and
   fixed in NOT_CHECKED.md** (the E2 finalization script appended the E2
   additions block 3x there too — E3 dedup + E3 section added).
5. **[LOW, PE-MASTER-found defect fixed] sgp_T1_dialog.txt was UTF-16LE+BOM**
   (PowerShell 5.1 redirect) — converted verbatim to plain UTF-8 with a
   one-line conversion header; the verbatim timelock message "The supplied
   Gamebryo timelock (8469DD85B0554A49, Internal) has expired" is present
   and readable.
6. **[PROCESS, budget overrun disclosed]** ~55/35 calls, ~165/60 min — see
   BUDGET_USED above. No scope expansion; every overrun call is visible in
   the transcript as a disclosed fix cycle or evidence persistence.

## FULL_READ_LOG

RUN_CONTRACT.md (binding; re-read E3 scope items). BATCH_E2_RETURN.md
(resume points). gb12core.py (fully re-read: header canon, all existing
LoadBinary bodies, decode/decode_rest/closure logic). GB 1.2 source
(targeted LoadBinary/LoadCString/CreateFromStream bodies + KeyType enum +
NiAnimationKeyMacros.h registration mechanism): NiParticleSystem.cpp,
NiPSysData.cpp, NiParticleInfo.cpp, NiParticles.cpp (NiMain), NiParticlesData.cpp
(NiMain), NiPSysModifier.cpp, NiPSysEmitter.cpp, NiPSysVolumeEmitter.cpp,
NiPSysBoxEmitter.cpp, NiPSysAgeDeathModifier.cpp, NiPSysSpawnModifier.cpp,
NiPSysGrowFadeModifier.cpp, NiPSysColorModifier.cpp, NiPSysPositionModifier.cpp,
NiPSysBoundUpdateModifier.cpp, NiPSysModifierCtlr.cpp, NiPSysEmitterCtlr.cpp,
NiPSysUpdateCtlr.cpp, NiPSysEmitterCtlrData.cpp, NiInterpController.cpp,
NiSingleInterpController.cpp, NiFloatInterpController.cpp,
NiPoint3InterpController.cpp, NiTextureTransformController.cpp,
NiMaterialColorController.cpp, NiFloatData.cpp, NiColorData.cpp, NiPosData.cpp,
NiAnimationKey.cpp/.h, NiAnimationKeyMacros.h, NiFloatKey.cpp,
NiBoolKey.cpp, NiColorKey.cpp, NiPosKey.cpp, NiLinFloatKey.cpp,
NiBezFloatKey.cpp, NiTCBFloatKey.cpp, NiStepFloatKey.cpp, NiLinColorKey.cpp,
NiStepColorKey.cpp, NiLinPosKey.cpp, NiBezPosKey.cpp, NiTCBPosKey.cpp,
NiStepPosKey.cpp, NiQuaternion.cpp (per-file SHA256 recorded in the
gb12core.py E3 citation block; extracts in sandbox
e3_niparticle_loadbinary.txt / e3_anim_loadbinary.txt / e3_anim2_loadbinary.txt).
TRANSFORM_SEMANTICS.md (fully — the s28 contract canon). SOURCE_ORACLE_INDEX.csv
(GB_1_2/GB_2_6/GB_1_1_2/GB_2_3 rows for the signature sources). compare_T3.json,
STAGE_ACCEPTANCE_GATES.csv, NOT_CHECKED.md, RETRACTIONS_SUPERSESSIONS.md,
HANDOFF.md, FINAL_REPORT.md (Q17/Q19/Q26/Q27 sections), oracle.py (CLI +
compare command), adapters/gb12/adapter.py, registry.py, tests/test_gb12.py.
NOT fully re-read: GAMEBRYO_ROSETTA.md, NIF_LOAD_PIPELINE.md,
VERSION_SUPPORT.md (E1/E2 canon used as pins only).

## OUTPUT_PATHS + SHA256

- tools/gamebryo_oracle/gb12core.py — 93989D7294C16CAFC57D6910FB70171CC4D5A4F63F684D28DE84FDC19DA177B0 (E3 loaders + count bounds + link filter + pre-solver + footer-crash fix; our code only)
- 04_EVIDENCE/T_runs/inspect_T3_gb12_full.json — B4F5A55A7FA9BDC769B24108FCE120CAB0FFCDC75FE00FFD2FB6F2F1F4A281E7
- 04_EVIDENCE/T_runs/inspect_T3_gb12_full_run2.json — B4F5A55A... (byte-identical pair; 858s/814s wall each; no wall-clock in body)
- 04_EVIDENCE/T_runs/compare_T3.json — B810FA6A0B1DF1EC524E05BEAE109EBA3B0E5D14F956FAC8B9BD7CB44D36BFCF
- 02_ANALYSIS/GAMEBRYO_SEMANTIC_SIGNATURES.json — CE84F4857D50331443BCE8DA3AEE58C097213D01B6B382C4509E2ADE2356ECA1
- 02_ANALYSIS/RETRACTIONS_SUPERSESSIONS.md — 6177511FE39D7DCEA7E3D088B5151319274003E6CADAA4810F12F808756FED3D (dedup verified: exactly 1 "Batch E2 additions" block)
- 02_ANALYSIS/NOT_CHECKED.md — FE2C56EC29C2E1B574D2F71E13C29DC1C507E19D4C0F6441253AE2ADE3BD7ECE (dedup verified: exactly 1 "E2 additions" block; E3 section added)
- 06_REPORT/HANDOFF.md — B9D113FA6FA6968E606B4970EA0315D51FFFB18A2A2E978E3F962BC2C81E6727 (terminal block updated truthfully)
- 06_REPORT/FINAL_REPORT.md — DB7C9E7D03F29406A427387B94DE7470FDD73DD85E244248847423E18C82C019 (Q17/Q26/Q27 E3 notes)
- 00_CONTROL/STAGE_ACCEPTANCE_GATES.csv — 69540A42ADD991E81A8DF0C4E152FC9B973A2E1AAFF9AF5235EB48D6174F1F5C (5 E3 rows appended)
- 04_EVIDENCE/sgp_T1_dialog.txt — 180EB479BD87B310A946E3BBBE5876FB4D18E3E5A95735A6D497C72AF73A399A (plain UTF-8; timelock message verified present)
- 04_EVIDENCE/BATCH_E3_RETURN.md — this file
- Sandbox (LOCAL_ONLY, not repo): e3_t3_seqwalk.py / e3_t3_diag.py /
  e3_t3_diag2.py / e3_t3_diag3.py, e3_t1_revalidation{,2,3}.json,
  e3_niparticle_loadbinary.txt, e3_anim_loadbinary.txt,
  e3_anim2_loadbinary.txt

## INPUT_HASHES (re-hashed this batch)

- T3 496633.nif: 4DBCC7311884C453CBBB2255C1592994A225088D1D9BBB47D2D0C287580B7369 (== manifest pin; fail-closed check executed before every run)
- T1 218757.nif: 3E8A22C2213202207E374B55CD65B2C3BE039CCDD1E8D01A07FCAF44DE12CF36 (== manifest pin)
- NiStream.cpp (GB12): E955C36E... (== E1/E2 canon, via gb12core canon block)
- GB 1.2 class sources: per-file SHA256 recorded in the gb12core.py E3
  citation block (re-hashed during extraction this batch)

## FILES_CHANGED

New: 02_ANALYSIS/GAMEBRYO_SEMANTIC_SIGNATURES.json;
04_EVIDENCE/T_runs/{inspect_T3_gb12_full.json, inspect_T3_gb12_full_run2.json,
BATCH_E3_RETURN.md}. Updated: tools/gamebryo_oracle/gb12core.py;
04_EVIDENCE/T_runs/compare_T3.json; 06_REPORT/{HANDOFF.md, FINAL_REPORT.md};
00_CONTROL/STAGE_ACCEPTANCE_GATES.csv (append rows);
02_ANALYSIS/{NOT_CHECKED.md, RETRACTIONS_SUPERSESSIONS.md};
04_EVIDENCE/sgp_T1_dialog.txt (encoding fix, verbatim content). ZERO writes
to D:\gamebyroengine, pcg_install, src/, skills, AUDIT_ENTRYPOINT.md, foreign
packages, or completed run packages (read-only respected throughout).

## BASE_SHA / HEAD_SHA / PUSH_STATUS

- BASE_SHA: f33c7b9c201b02b8e0f8c7010275b6217475b5a4 (dispatch pin; not
  re-verified by any git command — zero git operations executed in E3)
- HEAD_SHA: NOT_TOUCHED (no git commands run; contract (h))
- PUSH_STATUS: NO_GIT_OPERATIONS (executor batch)

## UNRELATED_WORK_EXCLUDED

The OUT_OF_SCOPE untracked entries and all foreign packages were not
touched. Sandbox-only diagnostics stayed in the run sandbox (never staged).

## NEXT_PARENT_ACTION

1. Audit E3 from disk (this file + the package + tools/gamebryo_oracle);
   fresh QC per RUN_CONTRACT (n) remains the separate pe-master-auditor
   batch (T1 re-run after the E3 changes is the natural QC re-check: it is
   byte-identical to E2's published result).
2. Decide the T3 closure continuation: the remaining defect is bounded
   (S_B candidate-phase cost; suffix anchor at byte 142833 already
   localized) — a NEW authorization is required (NEXT_EXPERIMENT_
   AUTHORIZED = NO stands).
3. Persistence phase unchanged (MANIFEST must cover the new E3 files:
   GAMEBRYO_SEMANTIC_SIGNATURES.json, the T3 pair, the updated files).

## RESUME_POINT

RUN_STATUS = PARTIAL. Exact stop points: (1) T3 gb12 full decode — classes
COMPLETE (all ~25, T1-validated); determinism pair COMPLETE (byte-identical);
closure assignment OPEN (search budget; S_B phase of the right-to-left
footer-anchored pre-solver; suffix anchor byte 142833 localized; resume =
memoize/bound the S_B walk phase, re-run the pair); (2) G-SIG-1 COMPLETE;
(3) RETRACTIONS + NOT_CHECKED dedup COMPLETE; (4) dialog encoding COMPLETE;
(5) report updates COMPLETE (gates CSV, Q17/Q26/Q27, HANDOFF terminal block,
NOT_CHECKED E3 section).

## SELF_CHECK (executor's own, labelled — NOT independent MASTER audit)

- T payload hashes re-verified against the manifest before every run
  (fail-closed pins honored; no drift).
- T3 determinism: actual byte-identical double runs (sha256 pair recorded),
  not just intent; no wall-clock in the JSON body.
- T1 regression: the E3-changed tool reproduces the E2-published T1 result
  byte-identically (both the pre-solver and DFS paths) — the strongest
  available evidence that the new loaders + pre-solver preserve the E2
  semantics on real data.
- E2 regression battery: 0 failures after all E3 changes.
- Honest negatives preserved: T3 not EOF-exact (residuals recorded; no
  manufactured MATCH in compare_T3.json; 18 rows NOT_AVAILABLE_IN_OUR_
  DECODER because OUR decoder also fails on T3).
- Era separation in every artifact; ORACLE_MODE on every JSON; the
  ORIGINAL GB 1.2 verdict never merged with OUR extension; zero
  proprietary source bytes embedded (field-order logic + names + hashes
  only); payloads LOCAL_ONLY in the sandbox.
- Budget overrun (~55/35 calls, ~165/60 min) disclosed with its causes
  above; no scope expansion; no HARD_STOP condition fired (WORLD_PLACEMENT_
  RECOVERED stays NO; no unambiguous placement record appeared).
