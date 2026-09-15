# SOURCE_REGISTRY — PE_935_NIF_10_1_BASELINE_ROSETTA_R1_20260915

All external sources are pinned as local copies (no network fetch performed in
this run; snapshots pre-existed in the workspace). Status labels:
EXTERNAL_REFERENCE_ORACLE (never automatically ENTROPIA_CONFIRMED),
LOCAL_PHYSICAL_CORPUS (project data), ENGINE_REFERENCE (actual Gamebryo
engine source — highest external authority for this era).

| ID | SOURCE_NAME | LOCAL PATH | REVISION/TAG | FETCH_DATE (local pin) | LICENSE | SUPPORTED_NIF_VERSIONS | ROLE |
|---|---|---|---|---|---|---|---|
| SRC-01 | NifTools nif.xml (modern) | D:\Eudoria_Reconstruction\04_External_References\reference_only\nifxml\nif.xml | niftoolsxml 0.10.0.0; SHA256 D6B76A83EA5FBADD... (full hash in 06_REPORT/MANIFEST_SHA256.csv) | pinned pre-run | GPL-3 (historical) / niftools own | all incl. 10.1.0.0 (V10_1_0_0) | schema oracle A |
| SRC-02 | NifTools nif.xml (historical) | D:\Eudoria_Reconstruction\04_External_References\reference_only\nifxml_historical\nif.xml | niftoolsxml 0.7.1.1; SHA256 1D5C8E580B95D3EB... — byte-identical to pyffi's bundled copy | pinned pre-run | GPL-3 | all incl. 10.1.0.0 (explicitly lists Entropia Universe as a 10.1.0.0 title) | schema oracle B (era-closest) |
| SRC-03 | NifSkope 2.0 bundled nif.xml | D:\Eudoria_Reconstruction\04_External_References\diagnostic_tools\nifskope\NifSkope_2_0_2018-02-22-x64\nif.xml | NifSkope 2.0 2018-02-22 x64 build; SHA256 0DCE5092060E0CAB... | pinned pre-run | NifSkope license | all incl. 10.1.0.0 | schema oracle C |
| SRC-04 | NiflySharp (C# implementation) | D:\Eudoria_Reconstruction\04_External_References\separate_tools\niflysharp_extract\ousnius-NiflySharp-104d79f\ | commit 104d79f (ousnius/NiflySharp) incl. bundled nif.xml SHA256 752C79786CEB2176... | pinned pre-run | MIT | >= 20.x era focus; NiHeader.cs models 10.1 header (with the 1-u32 tail — see CONFLICT C-01) | implementation oracle A |
| SRC-05 | nifskope_fo76utils build nif.xml | D:\Eudoria_Reconstruction\04_External_References\reference_only\nifskope_fo76utils\build\nif.xml | SHA256 880C316787950299... | pinned pre-run | niftools | all incl. 10.1.0.0 | schema oracle D |
| SRC-06 | **Gamebryo 1.2 ENGINE SOURCE (Gb12_Source)** | D:\gamebyroengine\extracted\Gb12_Source\ (CoreLibs\NiMain\NiStream.cpp, NiObject.cpp, NiObjectNET.cpp, ...) | Gamebryo 1.2 full source tree (local archive Gamebryo 1.2 Source.rar) | pinned pre-run | NDL/Gamebryo proprietary — local analysis only, no redistribution | the actual reader for 5.x..10.1-era files (NIF_MAJOR from NiVersion.h; ms_uiNifMaxVersion from build) | **ENGINE_REFERENCE — primary framing truth** |
| SRC-07 | Gamebryo 1.1.2 Evaluation SDK | D:\gamebyroengine\Gamebryo 1.1.2 Evaluation\ + D:\gamebyroengine\extracted\Gb112_eval, gb112_known_good | Gamebryo 1.1.2 Evaluation (2004 ISO) | pinned pre-run | NDL eval license | 10.x era exporter/SDK of the era Entropia used ("Gamebryo_1_1" exporter string per docs/nif/09) | ENGINE_REFERENCE + era-native sample NIFs |
| SRC-08 | Gamebryo 1.1.2 SDK sample NIFs | D:\gamebyroengine\extracted\gb112_known_good\{BABYLENGUIN.NIF, BABYLENGUIN.KF, DESTROYERBOT.NIF, ROCKY.NIF (all 10.1.0.0), SOLDIER.NIF (10.0.1.18)} | shipped with SRC-07 | pinned pre-run | SDK samples | 10.1.0.0, 10.0.1.18 | non-MindArk 10.1.0.0 physical controls |
| SRC-09 | Empire Earth II sample NIFs | D:\Eudoria_Reconstruction\04_External_References\reference_only\blender_niftools\todo\old_nifs\ee2\{lodtest.nif, lodtest-skinned.nif} | niftools-blender_niftools_addon test corpus | pinned pre-run | upstream test files | 10.1.0.0 (verified: header version 0x0A010000) | non-MindArk 10.1.0.0 physical controls (EE2 = Civ-era Gamebryo title) |
| SRC-10 | Blender NIF tools addon | D:\Eudoria_Reconstruction\04_External_References\reference_only\blender_niftools_extract\niftools-blender_niftools_addon-0305c8d\ | commit 0305c8d | pinned pre-run | BSD-3 / GPL-3 mix | 4.x..20.x | implementation oracle B (parser code reading) |
| SRC-11 | PyFFI source | D:\Eudoria_Reconstruction\04_External_References\reference_only\pyffi\ | pyffi tree (bundled nif.xml == SRC-02, SHA-verified identical) | pinned pre-run | BSD-3 / GPL-3 | 4.x..20.x | implementation oracle C |
| SRC-12 | OpenMW 0.51.0 (niffile.cpp) | D:\Eudoria_Reconstruction\04_External_References\reference_only\openmw_0.51.0\openmw-openmw-0.51.0\ | tag 0.51.0 | pinned pre-run | GPL-3 | 4.0.0.2..10.x (Morrowind-focused reader) | implementation oracle D (older-version cross-check) |
| SRC-13 | pynifly / NiflyDLL | D:\Eudoria_Reconstruction\04_External_References\reference_only\pynifly\ | NiflyDLL wrapper tree | pinned pre-run | MIT | as NiflySharp | implementation oracle E |
| SRC-14 | ByroRedux (Gamebryo RE docs) | D:\Eudoria_Reconstruction\04_External_References\reference_only\byroredux\ (+docs/legacy/nif.xml == SRC-01 SHA-verified) | local snapshot | pinned pre-run | repo-specific | Gamebryo era docs | supplementary docs oracle |
| SRC-15 | PCG 9.3.5 Models.bnt | D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt | size=395412868, SHA256=C950A8C26F2063F4DD748D88C95BD769AAC77A2F5F76FACE7E969BE0B3D3BEE0 (re-measured S0) | corpus | MindArk permission (non-commercial, no distribution) | 10.1.0.0 ×4,838 / 4.1.0.12 ×757 / 4.0.0.2 ×1 (independent census, this run) | PRIMARY PHYSICAL CORPUS |
| SRC-16 | GECK NIF knowledge notes | D:\Eudoria_Reconstruction\04_External_References\GECK_NIF_KNOWLEDGE\ | local notes | pinned pre-run | mixed | 20.x-era mostly | tertiary reference only |

## Game-specific 10.1.0.0 oracles (contract §14)
- Actual version VERIFIED from bytes in this run: Empire Earth II lodtest.nif
  + lodtest-skinned.nif = 10.1.0.0 (SRC-09); Gamebryo SDK samples
  BABYLENGUIN.NIF/DESTROYERBOT.NIF/ROCKY.NIF/BABYLENGUIN.KF = 10.1.0.0
  (SRC-08); SOLDIER.NIF = 10.0.1.18 (NOT a 10.1 oracle — cross-version only).
- Schema-listed 10.1.0.0 titles (SRC-02 version table): DAoC, Civilization IV,
  Freedom Force vs. the 3rd Reich, Axis and Allies, Kohan 2, Entropia
  Universe, Wildlife Park 2, The Guild 2, NeoSteam, Empire Earth II.
  NO local sample for the other titles — do NOT assume their version; only
  EE2/SDK samples have byte-verified 10.1.0.0 status here.

## Identified baseline conflicts (full matrix in 02_ANALYSIS/BASELINE_CONFLICT_MATRIX.csv)
- C-01: per-block GroupID u32 for 10.1.0.0 — present in ENGINE (SRC-06:
  5.0.0.6 <= v < 10.1.0.114) + physical (SRC-08/09/15); modern schema models
  "Group ID" only since 10.1.0.114; historical schema lacks it entirely;
  NiflySharp syncs the per-block u32 correctly for 10.1.0.0 (NiObject.cs
  L61-62 — F-16/AMEND-010 corrects the former "misalign" wording; its
  range differs from the engine only for 5.0.0.6–9.x files).
- C-02: schema tail naming (historical "Unknown Int 2" vs modern "Num
  Groups") — same u32 slot, different label; engine source names it
  NumGroups + group size list (matches modern).
