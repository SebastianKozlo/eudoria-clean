# INPUT IDENTITIES — PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005

One bounded correction-only run for the TWO P2 defects (D1/D2) found by the
independent Desktop post-audit of the published THREE-P2 package. STATIC-ONLY:
the client never ran; every EXE access is a static byte read of the pinned
file. NO new science; machinery repair + fresh QC + honest records only.

## Repository / baseline

- REPO: `D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean`
- Remote: `origin = https://github.com/SebastianKozlo/eudoria-clean.git`
- EXPECTED_BASE_SHA (verified at this run's preflight BEFORE any write):
  `9d31a82b6589f46e9ca6c75c6e323b433c1ebf92`
- BASE triple at preflight (measured via `git rev-parse` + `git ls-remote
  origin master`): LOCAL_HEAD == ORIGIN/master == ACTUAL_REMOTE_MASTER ==
  `9d31a82b6589f46e9ca6c75c6e323b433c1ebf92` (all three equal; no hard stop
  fired).
- Working tree at preflight: clean for every tracked path; exactly the six
  FOREIGN UNTRACKED paths
  (docs/audits/PE_935_FC1_P2_CLOSURE_EXTERNAL_QC_20261001/,
  PE_935_MODEL_218757_PLACEMENT_SEARCH_R1_20261003/,
  PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/,
  PE_935_P1_CLOSURE_EXTERNAL_QC_20260930/,
  PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/, experiments/)
  untouched and unstaged throughout this run; nothing staged; NOTHING
  committed or pushed by THIS run (persistence is the separate PE-MASTER
  phase per the dispatch).
- Write allowlist honored: every file written by this run lives under
  OUTPUT_ROOT only; AUDIT_ENTRYPOINT.md NOT edited (a proposed row is
  provided in HANDOFF.md for the persistence phase).

## Pinned EXE (never launched; static byte reads only)

- Path: `D:\Eudoria_Reconstruction\pcg_install\Entropia.exe`
- Size: 8,015,872 B
- SHA256: `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`
- Re-verified by every instrument (loader pins size+SHA; the QC battery
  re-hashes at the clean and at every mutated execution).

## The independent post-audit (authoritative definition of D1/D2)

- Path: `C:\Users\User\Documents\ChatGPT\PE\PE_935_F84_C2_C1_DESKTOP_POST_AUDIT_20261005\REPORT.md`
- Size: 15,535 B
- SHA256: `31AA87BC7C38089C7F648B5C749E196D80C4C6ED37823A96D5379CF84E78E61E`
- Verdict: REQUIRE_CORRECTIONS (two confirmed P2: D1 = H2 still accepts the
  reserved `0F 73 /4` in both MMX and SSE2 forms; D2 = Q2 trusts the JSON to
  select and limit its own validation - relabelled kind, removed EA object,
  DELETED load-bearing pins and duplicated/extra claims all passed).
- The audit ALSO confirms (in its tested scope): the three original
  THREE-P2 counterexample repairs, H1, the seven required mutation controls,
  the 133 physical opcode pins, persistence and the preserved assignment
  core. This run does NOT reopen those repairs; it reproduces them as
  controls.

## Packages

- OUTPUT_ROOT (this package; fresh at start, created by this run):
  `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION_R1_20261005/`
- SOURCE_PACKAGE = the exact BASE package (READ ONLY; its committed scripts
  are the copy lineage of this run's corrected instruments; its PINS table is
  the separately pinned expected roster):
  `docs/audits/PE_935_FACTORY_PLUS_84_C2_C1_THREE_P2_CORRECTION_R1_20261005/`
- SOURCE package manifest identity (verified this run, fail-closed preflight):
  `COMMITTED_PACKAGE_MANIFEST_SHA256.csv` — 5,613 B / SHA256
  `A407694EC96BBDDE8A8CE2E1D5808BACF39762017EE80B9A8A03D5AC6125897E`;
  bijection verified 33/33 rows (0 missing, 0 extra, 0 duplicates, 0 size
  mismatches, 0 SHA256 mismatches) and every source file == its exact Git
  blob at BASE_SHA (git ls-tree -r --long comparison; AUDIT_ENTRYPOINT.md
  blob `6f28c045ae2fb2d0f0bd13e353a92df3ddbec0cd`).
- Historical packages (C1/C2/THREE-P2) are READ ONLY FOREVER; nothing under
  them was modified by this run (verified: the regenerated census CSV, pin
  CSV and AF3 ledger are BYTE-IDENTICAL to the committed BASE files, and
  the regenerated C1/C2/C3 JSONs differ from BASE ONLY in the declared
  `run` label — see REGRESSION_DIFF.json).
- The D2 expected roster source: the BASE-pinned
  `03_SCRIPTS/c1_pin_ledger.py::PINS` (Git blob
  `5a7b642f380c00217db6db921d2fdf99277a38a6`, file SHA256
  `757225FEBD2C3E7B13A779199C123CB664481B189672B3A007EBDC1B39222D47`),
  extracted by AST literal evaluation (no historical code executed; no
  module import); 133 claims; role tally bytes=38, mem=46, imm32=14,
  call=29, imm8=4, declassified=2; persisted as EXPECTED_PIN_REGISTRY.json
  and re-derived IN-RUN by gate Q2 from the same Git blob (never trusted
  from disk).

## Independent oracle (synthetic fixtures only)

- Tool: GNU objdump via WSL
- Version (measured): `GNU objdump (GNU Binutils for Debian) 2.44`
- Scope: SYNTHETIC fixtures only - the 71 carried fixtures (NEW-G, NEW-F,
  A1/A2/B/C/D/E, the complete H1 16-bit-addressing rm table, the H2
  grouped-opcode controls, the P2-2 decoder unit vectors) RECAPTURED this
  run + 9 NEW D1 fixtures (the two `0F 73 /4` negatives `0F 73 E0 02` /
  `66 0F 73 E0 02`, the six contract legal controls `0F 71 E0 02`,
  `0F 72 E0 02`, `0F 73 D0 02`, `0F 73 F0 02`, `66 0F 73 D8 02`,
  `66 0F 73 F8 02`, and the downstream falsifier stream) = 80 fixtures,
  raw command lines and verbatim disassembly outputs persisted in
  `01_RAW/D1_INDEPENDENT_ORACLE_RECORDS.json`.
- Oracle-first discipline: this run's D1 EXPECTED verdicts were locked from
  the D1 contract + the ISA reference BEFORE the corrected decoder's D1
  behaviour was evaluated (the fixture expectations are fixed in the capture
  script; objdump was run first; the corrected decoder was then checked
  against the records - never the reverse). The production decoder is NEVER
  its own source of truth for the fixtures. The EXE re-derivations of the QC
  gates use the production decoder (the established Q2/Q3 pattern, disclosed
  honestly). The BASE (THREE-P2) decoder defect is additionally MEASURED
  in-run through a READ-ONLY import of the committed BASE modules (file
  identities recorded in 01_RAW/D1_BOUNDARY_FALSIFIER.json; no historical
  file modified; bytecode writes disabled).

## Run environment

- Executor: pe-reconstruction worker session (OpenCode agent); dispatched by
  PE-MASTER under the direct dispatch of 2026-10-05 (contract:
  OPENCODE_F84_C2_C1_D1_D2_CORRECTION_COMPLETE_20261005.md, read in full
  from disk before any action).
- QC labeling: QC_SCOPE = SELF_CHECK_FACTORY_PLUS_84_C2_C1_D1_D2_CORRECTION
  (executor self-QC; author/origin explicit; this package does NOT claim an
  independent review; PE_MASTER_REVIEW.md is an explicit placeholder - the
  PE-MASTER persistence phase performs the review).
- Python: 3.12.10 (Windows); all scripts run with `-B` and
  `sys.dont_write_bytecode = True` (no __pycache__ anywhere, including the
  historical packages whose scripts were imported READ-ONLY).
- NO_NESTED_TASKS = YES (absolute); CLIENT_EXECUTION = FORBIDDEN (none
  occurred); CANONICAL_GATE_EFFECT = NONE; NEXT_EXPERIMENT_AUTHORIZED = NO.

## Anchor provenance (unchanged policy)

- The 34 strong anchors (KNOWN_FUNCTION_ENTRY) are
  PRIOR_CANON_ANCHOR_INPUT: the prior-canon function-entry table carried by
  the F84 chain packages, re-verified this run only at the same-VA bytes.
  THIS RUN DOES NOT CLAIM to independently re-prove the 34 anchors (that
  work was not performed); preservation under the prior canon is not
  transformed into new independent evidence.
