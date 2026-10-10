# AUTHORIZATION_AND_PREFLIGHT — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009

Phase: SETUP_PREFLIGHT_AND_CONTROLS (worktree setup, preflight artifacts, engine
source inspection, Controls A/B). No adapter/app implementation in this phase.

## 1. Human authorization summary

- ONE human-authorized run: `PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009`
  (RUN_CLASS = BOUNDED_ENGINE_REFERENCE_AND_BROWSER_IMPLEMENTATION).
- Scope authorized: implementation + LOCAL viewer testing + commit/push of the
  feature branch `codex/pe-sceneir-218757-r1-20261009` ONLY.
- NOT authorized: master changes, Entropia.exe / original client execution,
  historical placement claims, network producer trace, new corpus search, new EXE
  bodies, semantic derivation of the nine-byte Ark texture tail.
- `NEXT_EXPERIMENT_AUTHORIZED = NO`, `HARD_STOP = YES` (standing).

## 2. Governing contract identity (re-verified by this executor)

- Path: `C:\Users\User\Documents\ChatGPT\PE\OPENCODE_SCENEIR_218757_BROWSER_R1_20261009\OPENCODE_SCENEIR_218757_BROWSER_R1.md`
- Size: 18739 bytes (measured), SHA256:
  `1c7fc42f3023b9a2f37fe6e6f3830b217e35df35d91a48f0455f57cd06d14db3`
  (re-measured by this executor — MATCHES the launcher-pinned value
  1C7FC42F3023B9A2F37FE6E6F3830B217E35DF35D91A48F0455F57CD06D14DB3).
- The launcher instruction identifying this contract is the ONLY authorization
  for this run; the older SKILL_ROSETTA_RUNTIME contract was NOT launched.

## 3. BASE verification (measured in this phase, before any write)

- EXPECTED_BASE_SHA = `3fbe93eec04759395223e6677b5040273d29222a`
- Canonical checkout `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`:
  `git rev-parse HEAD` = `3fbe93eec04759395223e6677b5040273d29222a` (on `master`).
- `origin/master` = `3fbe93eec04759395223e6677b5040273d29222a`.
- Fresh remote (`git ls-remote origin master`) = `3fbe93eec04759395223e6677b5040273d29222a`.
- Conclusion: LOCAL == origin/master == fresh remote master == BASE. BASE is in
  remote master's ancestry (it IS remote master) — no BLOCKED_BASELINE.
- Canonical untracked foreign paths observed (NOT absorbed, NOT modified):
  `docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/`,
  `docs/audits/PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/`,
  `docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/`,
  `docs/audits/PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/`,
  `docs/audits/PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/`,
  `experiments/` (6 untracked groups). The worktree was created FROM THE PINNED
  COMMIT, so none of these follow it.

## 4. Worktree / branch collision checks (before creation)

- WORKTREE `D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1` did NOT
  exist (Test-Path = False) — no collision.
- BRANCH `codex/pe-sceneir-218757-r1-20261009` did NOT exist locally or on
  remote (`git branch -a --list "*sceneir*"` empty; not present in ls-remote)
  — no collision.
- PRIVATE_ROOT `D:\Eudoria_Reconstruction\99_Audits\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009`
  did NOT exist — created (append-only).

## 5. Worktree creation and verification

- Command (the single authorized write in the canonical checkout):
  `git worktree add "D:\Eudoria_Reconstruction\12_WebGame\pe-sceneir-218757-r1" -b codex/pe-sceneir-218757-r1-20261009 3fbe93eec04759395223e6677b5040273d29222a`
- Worktree HEAD = `3fbe93eec04759395223e6677b5040273d29222a` (== BASE),
  `git status` clean, branch = `codex/pe-sceneir-218757-r1-20261009`.
- Canonical master HEAD re-verified AFTER creation: still
  `3fbe93eec04759395223e6677b5040273d29222a` on `master` — untouched.
- Other worktrees present and NOT touched:
  `worktrees\PE_935_NINODE_SLOT17_GB_ORACLE_MINICHECK_R1`
  (audit/pe935-ninode-slot17-gb-oracle-minicheck-r1),
  `worktrees\WORK_AUDIT_REPORTS` (audit/work-audit-reports).

## 6. Standing limits preserved (contract §1 — unchanged)

- 5596 Models.bnt entries; 4838 NIF 10.1 files declare NiArk classes.
- Original stock printer rejects selected PE files (measured: 218757/423020
  exit 1 `Error loading stream.` in the predecessor + post-audit); a
  PE-specific adapter is required.
- Model 218757: 66 accounted blocks, 62-supported/4-opaque ceiling — NOT
  silently promoted; all 14 NiTriShape/NiTriShapeData associations preserved
  in the imported representation, including helper candidates.
- 423020 exact-array negative = one selected comparison only.
- FC-C1/C2/C3 supersessions ACTIVE: growth-path equality and alias identity
  unresolved; placement participation not excluded by a generic container
  mechanism.
- MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
- HISTORICAL_WORLD_INSTANCE = NOT_ESTABLISHED
- WORLD_XYZ_RECOVERED = NO
- CANONICAL_GATE_EFFECT = NONE
- PE_AXES_AND_UNITS = UNVERIFIED_FROM_ENGINE (any render conversion is a
  labeled RENDER_ADAPTER_CHOICE applied once).

## 7. Input identity pins re-measured this phase

- Models.bnt: 395412868 B, SHA256 `c950a8c26f2063f4dd748d88c95bd769aac77a2f5f76face7e969be0b3d3bee0` — MATCH.
- 218757.nif pin copy: 57316 B, SHA256 `3e8a22c2213202207e374b55cd65b2c3be039ccdd1e8d01a07fcaf44de12cf36` — MATCH.
- SceneGraphPrinter.exe (GB 1.2 VC71): 663552 B, SHA256 `fd693af2d713c021b959fc7506200173435307c8fccc24ccd5851dfceb241c7c` — MATCH.
- MSVCP71.DLL `df96156f6a548fd6fe5672918de5ae4509d3c810a57bffd2a91de45a3ed5b23b`,
  MSVCR71.DLL `8094af5ee310714caebccaeee7769ffb08048503ba478b879edfef5f1a24fefe` (Gb112_tools_setup).
- Fixtures: ROTATED_SCALED_PARENT.nif 327 B `56fe7fec78c229acc9919735078b4f48b1c44b74bce01bca7814db023f4d5a19`;
  THREE_LEVEL_SOCKET.nif 430 B `0c71d5fdd4a70dd17b38ee49c3279747c772a0f96fe02a02c90aac716b441873`.
- terrain.gsa 61015 B `188a3a66f2fa719f0e0c82ae5bcb0e35952683d48b8df6a825de9a2a30665ba7`;
  TerrainSample.pal 22542 B `6a8539977b988e38e86e4b088f969f3f639796465167f23fc6ae5756682d283c`.
- smallpillar.nif: header `Gamebryo File Format, Version 20.5.0.4`, 29422 B,
  SHA256 `bcc97bf3d102f33188a771045aca198ee63b14db811404f5a178a55638f0f796`
  (fact recorded; NO NIF 20.5 reader attempted).
- Full table: INPUT_IDENTITIES.json. INPUT_HASH_MISMATCHES = NONE.

## 8. Read-only application references inspected (details in INPUT_IDENTITIES.json + PLAN_AND_PATH_ALLOWLIST.md)

- `D:\Eudoria_Reconstruction\12_WebGame\eudoria-compat-threejs-r1` — the old
  compat app (three 0.185.0, entry-by-entry API + provenance + hash cross-check,
  model 457485 mode). Reusable patterns identified; not wholesale-reused.
- `D:\Eudoria_Reconstruction\12_WebGame\tools\pe_asset_viewer_v4` — GLB/catalog
  forensic viewer (vendored r169). Its GLB exports are NOT treated as
  PCG-byte-equivalent; 218757 will come from pinned Models.bnt bytes.
- `D:\Eudoria_Reconstruction\12_WebGame\eudoria-web` — legacy r169 game runtime;
  NOT compatible with the base's three 0.185.0 stack without broad work;
  terrain integration will NOT be forced (authored grid instead).

## 9. Base repo test setup (inspected, for the plan)

- `package.json`: `{"type":"module","dependencies":{"three":"0.185.0"}}` — no
  test runner dependency, no scripts. RETAINED unchanged this phase.
- Existing test patterns in the repo: Python self-tests
  (`tools/gamebryo_oracle/tests/test_gb12.py --self` battery style, printing
  MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH / WHY_NON_CIRCULAR /
  FAILURE_CASE_DETECTED per control) and Node-based probe tools
  (`tools/*.js` executed directly with `node`). The new tests/pecompat/ suite
  will follow the zero-dependency Node-script + Python-control style so no new
  package dependency is introduced.
- NifModelReader.js (src/pesource/) is the 457485 SINGLE-WITNESS reader
  (v10.1.0.0 only, first-mesh render path). Its path does NOT support 218757;
  the adapter extends via NEW code under src/pecompat/ (regression of the
  witness preserved if its code path is ever touched).

## 10. Original asset / proprietary content policy (this phase and onward)

- All original models, SDK scenes/source, decoded arrays, texture payloads and
  screenshots with original assets: PRIVATE_ROOT / local-only, never committed.
- Report package carries ONLY bounded control values, counts, names, hashes and
  printer stdout/stderr (not proprietary).
- Originals (Models.bnt, SDK trees, fixtures, printer, historical audit
  packages, client installation) are READ_ONLY — never modified.

## 11. Preflight conclusion

WORKTREE_COLLISION = NONE. BASELINE = VERIFIED (local == origin == remote == pin).
BRANCH = `codex/pe-sceneir-218757-r1-20261009` (created from the pin).
INPUT_HASH_MISMATCHES = NONE. CONTROLS: A captured (CONTROLS_A.json), B native
ground truth captured (CONTROLS_B.json). READY for the implementation phases
per PLAN_AND_PATH_ALLOWLIST.md.
