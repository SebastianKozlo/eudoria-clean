# NOT_CHECKED — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003 (E1 draft; E2 completes)

Everything E1 deliberately did NOT check, with the reason and the batch that
owns it. Statuses from the closed set; no silent omissions.

## E2-owned (contract Phase D)

1. **Executed-loader behavior for ANY tool/loader** — no loader was run in E1
   (MODE: static; BUILDS/RUNS = NOT_TESTED for all 49 TOOLCHAIN_MATRIX rows).
   Includes: SceneViewer (all versions), SceneGraphPrinter, NifConvert,
   AnimationTool, AssetViewer, SceneDesigner, PhysXNifViewer, NSFParserUtility,
   DeveloperTools. NOT_TESTED.
2. **GB_1_1_2 / GB_2_3 ms_uiNifMinVersion & ms_uiNifMaxVersion VALUES** —
   compiled into binary NiMain.lib / NIMAIN23VC71R.lib; not source-visible.
   UNKNOWN until an executed-loader test (or lib RE, separate authorization).
3. **Executed confirmation of GB_1_2 NIF 10.1.0.0 load** (including the
   NiArk*-class prediction in VERSION_SUPPORT.md section 5) — source-derived
   only; NOT_TESTED.
4. **G-VER-2 FULL vs PARTIAL executed verdicts** — E1 delivered the
   source-level verdicts only.
5. **218757_NIF_RESULT.md (G-218757-1/2)** — requires the oracle run.
6. **GAMEBRYO_COMPATIBILITY_MATRIX.csv (G-MATRIX-1)** — requires runs.
7. **P7 (prior NifViewer 2.6 launch failure blocker class)** — E1 performed no
   execution; still UNVERIFIED. E2 must establish the exact blocker class or
   achieve a working original-tool run.
8. **GAMEBRYO_ORACLE_TOOL build + controls (G-TOOL-1..4) + comparison
   (G-CMP-1/2)** — E2.
9. **Optional GAMEBRYO_SEMANTIC_SIGNATURES.json (G-SIG-1)** — not produced in
   E1 (non-gating).

## E1 scope boundaries (not required by the E1 contract; recorded honestly)

10. **Deep contents of extracted\ subdirs beyond census** — Gb112_eval,
    gb112_known_good, Gb112_docs_html, Gb112_tools_setup, gb12_build (beyond
    NiVersion.h + lib identities + tool exe census), Gb26 (installer tree) were
    counted/hashed at top level only. NOT_CHECKED (not load-bearing for the
    version-gate question).
11. **Full archive listings** — recorded to sandbox\listings\ (7z l -ba, 6
    files); only summaries/counts entered the package CSVs. Full-listing
    analysis NOT_CHECKED.
12. **GbEvaluationSetup.ini full contents** — component/label fields extracted
    (sandbox phaseBC_result.json gb23.metadata_contents); full installer-table
    semantics NOT_CHECKED.
13. **Manifest block_histogram per-T analysis vs GB class registries** (exact
    object-coverage per T file) — E2 input for G-VER-2 executed verdicts.
14. **KF/KFM animation containers, NiControllerSequence/NiKeyframeController
    payload maps** — indexed (SOURCE_ORACLE_INDEX.csv functions_present) but
    not semantically mapped in E1.
15. **Volumes.bnt / .bvi (P5)** — context only per contract; NOT decoded
   (MindArk volume format out of scope for the Gamebryo-oracle question).
16. **NIF_VERSION_CENSUS.csv** (declared cross-check basis) — not used by the
    executed selection and NOT re-hashed in E1 (recorded in SELECTION_LOCK.json).
17. **The single NIF 4.0.0.2 corpus file** — counted in the census; not
    selected by any T rule; not individually examined.
18. **gb12_build OUR_TOOL scripts** (crosscheck_E.mjs, niark_strip.mjs, etc.)
    — catalogued, not read (not oracle-relevant).
19. **PE metadata of the 419 exes beyond the census fields** — all exes hashed
    (sandbox exe_census.csv + inventory_data.json); per-exe deeper PE analysis
    NOT_CHECKED.


## E2 additions (Batch E2, 2026-10-03)

1. G-SIG-1 GAMEBRYO_SEMANTIC_SIGNATURES.json (optional gate) — NOT_TESTED:
   budget exhausted before the optional phase. TRANSFORM_SEMANTICS.md (E1)
   remains the semantic signature source. **[E3: CLOSED — produced, see the
   E3 section below.]**
2. GB 1.1.2 evaluation-timelock bypass — NOT ATTEMPTED: the timelock dialog
   ("The supplied Gamebryo timelock (8469DD85B0554A49, Internal) has
   expired") is recorded as the EXACT blocker; no patching of original tools
   (s19 forbids it for the first-attempt discipline; bypass work would need
   a new authorization).
3. GB 2.6 viewer full NIF-load reach — NOT_REACHED in this environment:
   PhysXNifViewer startup chain (Settings dialog -> EGB_SHADER_LIBRARY_PATH
   -> 'Failed to load shader library!') never reaches NiStream::Load; the
   GB 2.6 10.1.0.0 verdict therefore stays SOURCE-derived only.
4. GB 1.2 prebuilt SceneGraphPrinter/SceneViewer observable load results —
   NOT_DETERMINED: SGP exits code 1 with no stdout/dialog; SceneViewer stays
   alive with an empty title; no load verdict observable without deeper UI
   automation (not attempted within budget).
5. T3 gb12 full-decode block fields — PARTIAL: the 480s wall cap fired
   (honest); header-level oracle data (block count 1288, type histogram,
   RTTI verdict) complete. **[E3: ADVANCED but still PARTIAL — see the E3
   section.]**
6. Comparison field-level statuses for T2/T3/T4/T5 — NOT_AVAILABLE_IN_OUR_
   DECODER: the FIELD_IDENTITY_V2 decoder failed on T2/T5 (EOF), T3
   (closure cap), T4 (10.1-specialist; by design); comparisons report this
   honestly instead of manufacturing values.
7. MANIFEST_SHA256.csv — persistence phase (pe-master-auditor), not E2.

(E3 process fix: this E2 additions block was accidentally appended 3x by the
E2 finalization script — same root cause as the RETRACTIONS_SUPERSESSIONS.md
triplification PE-MASTER found; duplicates removed in E3, content unchanged.)


## E3 additions (Batch E3, 2026-10-03)

1. **T3 gb12 closure assignment — REMAINS OPEN (honest PARTIAL).** All ~25
   registered classes present in T3's RTTI table are now implemented in
   gb12core.py from GB 1.2 source (file+line cited per body), the E2
   footer-read crash on b_new closure failures is FIXED, and the full-decode
   now decodes 448/1288 blocks (determinism pair byte-identical,
   sha256 B4F5A55A7FA9BDC769B24108FCE120CAB0FFCDC75FE00FFD2FB6F2F1F4A281E7),
   but the unknown-run boundary search (OUR extension; 3 runs:
   NiArkAnimationExtraData, NiArkImporterExtraData+NiArkTextureExtraData,
   NiArkViewportInfoExtraData) still exhausts its attempt budget
   (DFS 250k; right-to-left footer-anchored pre-solver PRESOLVE_MAX_ATTEMPTS)
   — "closure search budget exhausted" is reported; the 4 NiArk* blocks stay
   UNREGISTERED_IN_GB12_FACTORY unknowns and ~840 block boundaries remain
   undetermined. Diagnostics (sandbox e3_t3_diag3.py) localized a
   footer-anchored suffix anchor at byte 142833 (blocks 380..1287 decode
   deterministically to EOF-exact from there), so the remaining defect is
   the S_B scan phase cost, NOT the class implementations (validated: T1
   66/66 EOF-exact byte-identical to the E2 result, 0.3s). RESUME_POINT for
   a future batch: make the S_B candidate phase tractable (e.g. memoized
   suffix walks), then re-run the determinism pair.
2. **T3 EOF-exactness — NOT ACHIEVED** (consequence of 1): the honest
   residual unknowns are recorded in inspect_T3_gb12_full.json (warnings +
   null objects) per the E3 item-1 fallback.
3. **G-SIG-1 — CLOSED in E3** (02_ANALYSIS/GAMEBRYO_SEMANTIC_SIGNATURES.json
   produced per order s28; GB_1_2 + GB_2_6 + declaration-only GB_1_1_2/GB_2_3
   entries; NO Entropia.exe matching).
4. **sgp_T1_dialog.txt encoding — FIXED in E3** (was UTF-16LE+BOM from a
   PowerShell 5.1 redirect; converted verbatim to plain UTF-8 with a
   one-line conversion header; the verbatim timelock wording is preserved).
5. **RETRACTIONS_SUPERSESSIONS.md + NOT_CHECKED.md triplification — FIXED in
   E3** (the E2 finalization script appended the E2 additions block 3x in
   both files; one instance kept, content unchanged — PE-MASTER-found for
   RETRACTIONS; the same defect confirmed and fixed in NOT_CHECKED).
6. **E2 footer-crash defect (found + fixed in E3):** on a b_new file whose
   closure search fails, gb12core.decode crashed with a TypeError
   (footer read with fpos=None) instead of returning the honest DECODE_ERROR
   partial JSON. Fixed; the E2 regression battery + T1 remain byte-identical;
   a T3-class file now returns the honest partial result.
7. **PSys/animation-class semantic validation beyond T1/T3** — the new
   loaders are exercised by T3's 448 decoded blocks and T1's closure, but no
   executed-loader cross-check of the PARTICLE family exists (no original
   tool loads NIF 10.1.0.0 — factory blocker; source-derived only).
8. **Presolve-vs-DFS semantic equivalence — VERIFIED ON T1 ONLY**: T1's
   pre-solver output is byte-identical to the DFS output (both
   sha-identical to E2's published result); for files where the pre-solver
   is the deciding path and no DFS result exists (T3), the equivalence is
   by-construction (same acceptance rules) but not by-execution comparison.
