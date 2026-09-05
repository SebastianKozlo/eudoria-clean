# Audit Trails (Remote Evidence Packages)

This directory is the **remote audit trail** of significant completed work
units, per the project's OPENCODE -> GITHUB -> EXTERNAL AUDIT CONTRACT
(permanent project governance, adopted 2026-09-05; persisted in the
pe-master-auditor operating procedure §21).

## Purpose

External auditors must be able to independently verify
CLAIM -> SOURCE -> METHOD -> IMPLEMENTATION -> TEST -> EVIDENCE -> VERDICT
from this repository alone, without access to the OpenCode conversation.
The chat response is only a HANDOFF INDEX; this directory is the evidence.

## Convention

- One subdirectory per significant run: `docs/audits/<RUN_ID>/`
- Contents: the run's REPORT.md, HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv
  (gates), artifact_index.csv (evidence manifest equivalent — with REAL
  SHA-256, no placeholders), and the run's derived analysis artifacts
  (control scripts, claim matrices, denominators, counterexamples,
  proposed corrections, normalized manifests, quotes, logs).
- **Original proprietary game payloads are NEVER committed** (installers,
  .bnt containers, .exe, NIF/TGA corpora). Original physical evidence is
  represented by identity metadata: ERA/BUILD, description,
  LOCAL_CANONICAL_PATH, SIZE, SHA256, REPRODUCTION_METHOD.
- Local evidence root (not committed): `D:\Eudoria_Reconstruction\99_Audits\`
- Historical runs are not rewritten; supersessions/retractions are recorded
  as new evidence.

## Milestone mapping (roadmap namespace)

- EU935-M0 Forensic Foundation
- EU935-M1 World Surface Fidelity
- EU935-M2 NIF / Models / Materials / Animation
- EU935-M3 World Placement
- EU935-M4 Runtime Core / Events / ArkScript
- EU935-M5 Player / Avatar / Movement
- EU935-M6 Gameplay / Interactions
- EU935-M7 Network / Server Compatibility
- EU935-M8 UI / Audio / Effects / Environment
- EU935-M9 Full World Integration
- EU935-M10 Original Client Fidelity
- EU935-M11 PE Rosetta Completeness
- EU935-M12 Release / Preservation

## Local-only original sources used by the runs here

| Era / Build | Description | Local canonical path | Size | SHA256 |
|---|---|---|---|---|
| PCG 9.3.5 (Entropia Universe 9.3.5) | Models.bnt (BNT2 container, 5,596 NIF entries) | D:\Eudoria_Reconstruction\pcg_install\Data\Models\Models.bnt | 395,412,868 | c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0 |
| 2003 installer era | Models.bnt (original 2003 container, 5,426 entries) | D:\Eudoria_Reconstruction\01_Original_Files\BNT_Models\Models.bnt | 375,322,581 | 1322ADF2919B1B24A8B4FDA9618347E00C5A2B35DBB54516E353F1CEFD3524A6 |
| R61 frozen baseline | PE NIF parser (10 locked .py sources) | D:\Eudoria_Reconstruction\99_Audits\PE_R61_FROZEN_BASELINE_20260828\01_source\ | — | per SHA256_SOURCE.json (verified 10/10 in every run) |
| 2003 extracted corpus | 5,426 loose .nif files | D:\Eudoria_Reconstruction\99_Audits\PE_M1B3_REAL_PE_NIF_COMPATIBILITY_LAB_V1_20260819_010815\02_extraction\nif\ | — | per-file SHA256 in PE_NIF_CORPUS.csv / manifests |
