# RETRACTIONS_SUPERSESSIONS — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (E1 draft)

Corrections of prior canon are RECORDED AS PROPOSALS ONLY (G-PKG-1: the executor
does not edit other runs' or canonical files). Every item carries evidence and a
revalidation predicate.

## R1. PROPOSAL — P1 wording supersession (pin location precision)

- **Prior claim (P1, from the interrupted 218757 run's SELECTION.md):** "Gb12
  reader accepts NIF up to 10.2.0.0 (PE-MASTER-verified NiVersion.h)" — pinning
  `ms_uiNifMaxVersion` to NiVersion.h.
- **E1 evidence:** the VALUE 10.2.0.0 reproduces exactly, but the constant
  `ms_uiNifMaxVersion` is DEFINED in `Gb12_Source\CoreLibs\NiMain\NiStream.cpp`
  lines 44-46 (sha256 E955C36E...) from the `NIF_MAJOR/MINOR/PATCH/INTERNAL`
  macros that NiVersion.h carries (NiVersion.h lines 41-44). Declaration:
  NiStream.h line 288 (sha256 0EF7F74F...).
- **Proposed correction:** pin the value to "GB 1.2.2 ms_uiNifMaxVersion =
  10.2.0.0 (defined NiStream.cpp:44-46 from NiVersion.h macros)".
- **Revalidation predicate:** any future reader quotes NiStream.cpp L42-46.

## R2. PROPOSAL — "Gamebryo 1.2" corpus identity precision

- **Prior framing:** the corpus item is "Gamebryo 1.2".
- **E1 evidence:** Gb12_Source carries TWO patch levels of the 1.2.2 lineage:
  SDK\Win32\Include\NiVersion.h = 1.2.2.0 build 2005-06-08 (sha 0F4734C1...) and
  CoreLibs\NiSystem\NiVersion.h (+PS2 mirror) = 1.2.2.6 build 2006-06-19 (sha
  326D0136...). Both define NIF written = 10.2.0.0.
- **Proposed correction:** catalog the tree as "Gamebryo 1.2.2 (mixed .0/.6
  patch snapshots)"; version gates are unaffected (identical NIF values).
- **Revalidation predicate:** the two NiVersion.h variants remain in-tree.

## R3. PROPOSAL — v10 parser "dummy uint32" supersession candidate

- **Prior project observation (nif_parser_v10.py lineage):** NIF 10.1.0.0 files
  have "a dummy uint32 before each block".
- **E1 evidence:** the u32 is the per-block NiObjectGroup ID, read by
  `NiObject::LoadBinary` when `5.0.0.6 <= fileVersion < 10.1.0.114` (GB 1.2,
  NiObject.cpp L134-143, sha B137FE42...; = P2 EXACT MATCH). For NIF 10.1.0.0
  the condition is true, so the "dummy" u32 is structured engine data, not
  padding.
- **Proposed correction:** rename the field in decoder documentation to
  "GroupID (NiObjectGroup index, per NiObject::LoadBinary)".
- **Revalidation predicate:** E2 executed-loader run on T1/T2/T3/T5 showing the
  same 4-byte read at the same stream position (this remains a SOURCE-DERIVED
  prediction until executed).

## R4. NON-RETRACTION records (claims that SURVIVED E1 testing)

- **P4** (GB112 NiMain.lib VC71 ReleaseLib = FF4519AF prefix, 3,073,590 B):
  CONFIRMED by re-hash (FF4519AFD2475D9A...).
- **P5 reference values** (T1 index entry 781, name_file_offset 395,283,797,
  payload offset 116,223,520, size 57,316, stored SHA256 3E8A22C2..., header
  "Gamebryo File Format, Version 10.1.0.0", 66 blocks): **ALL MATCH** by this
  run's own re-extraction (04_EVIDENCE/EXTRACT_PROVENANCE.json) — the
  UNVERIFIED_REFERENCE class upgrades to REPRODUCED_THIS_RUN for these fields.
- **P3** (Models.bnt census 5,596 = 4,838x10.1.0.0 + 757x4.1.0.12 + 1x4.0.0.2):
  reproduced with a real CSV parser (5,596 logical rows; identical distribution);
  the "5,611 files" alternate wording is a physical-line-count artifact
  (PREFLIGHT section 5 already records both claims; E1 confirms the parser side).
- **P6 decoder-lineage pins** (s13_schema_field_identity_v2.py etc.): not used,
  not re-hashed in E1 — no change, recorded for completeness.
- **P7** (NifViewer 2.6 launch failure): NOT retracted, NOT explained — no
  execution in E1 (see NOT_CHECKED.md item 7).

## R5. E1 self-corrections (process, no canon impact)

- phaseBC_gb23_fix.py first run mis-parsed the 7z -slt listing (broken key
  match) → GB23 "absent" false negative; fixed and re-run (25 files extracted).
  Recorded so QC re-runs the FIXED script (04_EVIDENCE/scripts/).
- A fabricated-look SHA256 for GbEvaluationSDKSetup.exe in an early draft of
  VERSION_SUPPORT.md was caught and replaced with the actually computed value
  (69F84692D8BF857D607B30C6748F18B8FDEA857D43B63C56B4E63619E74C015E) before
  finalization; lesson: never cite a hash not printed by a tool in this run.
- PowerShell 5.1 `Get-ChildItem -LiteralPath -Include -Recurse` ignored the
  -Include filter (full-tree listing instead of the key-file subset) in the
  first discovery call — harmless (more data), recorded for script discipline.


## Batch E2 additions (2026-10-03) — RECORDED AS PROPOSALS (executor does not
edit other runs' or canonical files)

- **R6 (MANDATORY erratum, order s12/M6):** SELECTION.md T4 row says "no
  tie"; the pinned manifest actually has a 3-way 948 B tie among 223739.nif /
  223754.nif / 223534.nif (all num_blocks 10); the preregistered tie-break
  (lexicographically smallest name) selects the same file 223534.nif;
  selection OUTCOME unchanged; PE-MASTER-verified from the pinned manifest;
  SELECTION.md itself is lock-immutable so this erratum lives here.
- **R7 (P7 resolution, executed evidence):** the earlier interrupted-run
  screen_error.png was an ENVIRONMENT/CONFIG failure class, not the NIF
  version gate: fresh executed GB 2.6 PhysXNifViewer on T1 shows (1) startup
  Settings dialog, (2) after OK: "EGB_SHADER_LIBRARY_PATH environment
  variable not found", (3) with the env var set (fresh SDK_DLL_PC.cab
  extraction): "Failed to load shader library!" — the NiStream version gate
  is never reached in this environment. The GB 2.6 REJECTED verdict for NIF
  10.1.0.0 remains SOURCE-proven (NiStream.cpp sha 72781EEB, min 10.1.0.114).
  NOTE: the screen_error.png itself could not be re-viewed in this session
  (no image input available); the reconciliation relies on the FRESH executed
  observations, not on the old image.
- **R8 (execution-environment finding):** GB 1.1.2 Evaluation original tools
  are BLOCKED_EVALUATION_TIMELOCK_EXPIRED today (verbatim: "The supplied
  Gamebryo timelock (8469DD85B0554A49, Internal) has expired") — any prior
  assumption that the installed GB 1.1.2 tools could serve as a runnable
  oracle without addressing the timelock is superseded; the runtime-DLL
  blocker (MSVCR71/MSVCP71/MFC71) was SOLVED sandbox-locally (the exes
  launch), the timelock is the actual execution blocker.

(E3 process fix: the E2 additions block was accidentally appended 3x by the E2 finalization script; duplicates removed in E3, content unchanged — PE-MASTER-found.)
