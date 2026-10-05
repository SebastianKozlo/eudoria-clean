# INPUT IDENTITIES — PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005

Phase-1 (machinery-repair) run of a bounded correction-only package:
repair of the three P2 defects found by the independent Desktop post-audit
plus the two bounded decoder-hygiene items H1/H2. STATIC-ONLY: the client
never ran; every EXE access is a static byte read of the pinned file.

## Repository / baseline

- REPO: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`
- Remote: `origin = https://github.com/SebastianKozlo/eudoria-clean.git`
- EXPECTED_BASE_SHA (verified at this run's preflight BEFORE any write):
  `c4cb60f719b5bbab0b7549b1e9cc36d18430cdcd`
- BASE triple at preflight (measured via `git fetch origin` + rev-parse +
  ls-remote): LOCAL_HEAD == ORIGIN/master == ACTUAL_REMOTE_MASTER ==
  `c4cb60f719b5bbab0b7549b1e9cc36d18430cdcd` (all three equal; no hard
  stop fired).
- Working tree at preflight: exactly the six FOREIGN UNTRACKED paths
  (docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/,
  PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/,
  PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/, experiments/)
  untouched and unstaged throughout this run; no staged content; nothing
  committed or pushed in phase 1.
- PHASE 1 write allowlist honored: every file written by this run lives
  under OUTPUT_ROOT only.

## Pinned EXE (never launched; static byte reads only)

- Path: `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
- Size: 8,015,872 B
- SHA256: `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`
- Re-verified by every instrument (loader pins size+SHA; the QC battery
  re-hashes at both the clean and the mutated executions).

## The independent post-audit (authoritative definition of the three P2)

- Path: `C:\Users\User\Documents\ChatGPT\PE\PE_935_F84_C2_DESKTOP_POST_AUDIT_20261004\REPORT.md`
- Size: 16,130 B
- SHA256: `6EFA947F6B7FED2D6BBFE079655D79DFA27E0FF55F14EA12DAFFFE30AB320E3C`
- Verdict: REQUIRE_CORRECTIONS (three P2; it does NOT overturn the C2
  publication; it found two new P2 and extended the blast radius of
  PE-MASTER's P2-1 advisory).

## Packages

- OUTPUT_ROOT (this package; fresh at start, created by this run):
  `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005/`
- SOURCE_PACKAGE (READ ONLY; its 03_SCRIPTS were the starting points of the
  corrected copies): `docs/audits/PE_935_FACTORY_PLUS_84_ASSIGNMENT_OBJECT_
  C2_AF1_AF3_CORRECTION_R1_20261004/`
- SOURCE_SHA (commit carrying the source package): `c4cb60f719b5bbab0b7549b1e9cc36d18430cdcd`
- Historical C1 package (READ ONLY): `docs/audits/PE_935_FACTORY_PLUS_84_
  ASSIGNMENT_OBJECT_C1_FORENSIC_QC_CORRECTION_R1_20261004/`
- Historical packages C1/C2 are READ ONLY FOREVER; nothing under them was
  modified by this run (verified: the regenerated census CSV and AF3 ledger
  are byte-identical to the committed C2 files, and the only pin-CSV changes
  are the 8 measured boundary-field changes on the two declassified driver
  pins - see 01_RAW/CHANGED_FIELDS_VS_C2.json).

## Independent oracle (synthetic fixtures only)

- Tool: GNU objdump via WSL
- Version (measured): `GNU objdump (GNU Binutils for Debian) 2.44`
- Scope: SYNTHETIC fixtures only (NEW-G, NEW-F, A1/A2/B/C/D/E, the H1
  16-bit addressing rm table, the H2 grouped-opcode controls, the P2-2
  decoder unit vectors) - 71 fixtures, raw command lines and verbatim
  disassembly outputs persisted in
  `01_RAW/ORACLE_INDEPENDENT_RECORDS.json`.
- The production decoder is NEVER its own source of truth for the fixtures;
  expected boundaries were locked from objdump BEFORE the corrected decoder
  was written. The EXE re-derivations of the QC gates use the production
  decoder (the established Q2/Q3 pattern, disclosed honestly).

## Run environment

- Executor: pe-reconstruction worker session (OpenCode agent); dispatched by
  PE-MASTER under human authorization dated 2026-10-05 (verbatim in
  HANDOFF.md provenance section).
- QC labeling: QC_SCOPE = SELF_CHECK_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION
  (executor self-QC; author/origin explicit; the phase-1 package does NOT
  claim an independent review).
- Python: 3.12.10 (Windows); scripts run with `-B` and
  `sys.dont_write_bytecode = True`.
- NO_NESTED_TASKS = YES (absolute); CLIENT_EXECUTION = FORBIDDEN (none
  occurred); CANONICAL_GATE_EFFECT = NONE;
  NEXT_EXPERIMENT_AUTHORIZED = NO.

## Anchor provenance (unchanged policy)

- The 34 strong anchors (KNOWN_FUNCTION_ENTRY) are
  PRIOR_CANON_ANCHOR_INPUT: the prior-canon function-entry table carried by
  the F84 chain packages, re-verified this run only at the same-VA bytes.
  THIS RUN DOES NOT CLAIM to independently re-prove the 34 anchors (that
  work was not performed); preservation under the prior canon is not
  transformed into new independent evidence.
