# AMEND_LOG — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009 (internal QC)

AMENDMENT AUTHORITY: this fresh-session internal QC (pe-master-auditor, FRESH_INTERNAL_REVIEW —
internal to PE-MASTER, NOT an independent Desktop post-audit), dispatched directly by PE-MASTER for
run PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009. The assignment authorizes at most ONE targeted
repair round on QC-scoped mechanical defects; exactly ONE such repair was performed and is recorded
here. No executor raw evidence, no measurement value, no claim status and no code file was altered.

## AMEND-1 — INPUT_IDENTITIES.json: stale self-tool SHA256 corrected (finding F-QC-1)

- TARGET FILE (report package, phase-1 provenance record):
  `docs/audits/PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009/INPUT_IDENTITIES.json`
- DEFECT CLASS (mechanical provenance defect, QC-scope of duty 2 "spot-verify INPUT_IDENTITIES
  hashes"): the `controls_own_tools` row for `parse_gsa_controlA.py` recorded
  `sha256 = 530c3cee8a0ccbe7fa95ed6a6278ca9a99239205bb2d2f3c89079229d967574d`, while the physical
  file `D:\Eudoria_Reconstruction\99_Audits\PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009\controlA_work\parse_gsa_controlA.py`
  (16,614 B) hashes to `d80a908a91da932e1a2054fc686a511b91cd78b6853cb5f438b9e7dd3c4168b4` — the value
  CONTROLS_A.json (the Control-A record itself) already recorded. Two artifacts of the same run
  therefore carried two different hashes for the same tool, with no documented edit between them.
  Mechanism (most consistent with mtimes): the parser was edited after INPUT_IDENTITIES.json was
  written (00:11:31) and before CONTROLS_A.json was finalized (00:13:00); the INPUT_IDENTITIES row
  was never refreshed.
- COUNTER-CHECK (QC, own measurement): `Get-FileHash` over the physical file =
  `d80a908a91da932e1a2054fc686a511b91cd78b6853cb5f438b9e7dd3c4168b4` == CONTROLS_A.json
  `parser.sha256` == the corrected row. MATCH.
- PRE-EDIT STATE: 13,101 B, SHA256 `00201BBCF65D2335C6BBB0785DEC26FA9CC0E172DD284CA001B37BA611F3FCCE`.
- POST-EDIT STATE: 13,527 B, SHA256 `CE2DD4E2F70CA4F14CC8164279186042A61150C840FD21612AE84B10D35B25CC`
  (JSON re-parsed OK by QC after the edit).
- SEMANTIC CHANGE: the erroneous hash value `530c3cee...` in the row was replaced by the true,
  physically re-measured hash `d80a908a...`; a `qc_provenance_correction` note was added to the row
  that PRESERVES the old (stale) value inline and names this finding, so nothing is erased from the
  audit trail. No other row, no measurement value and no claim was touched.
- REVALIDATION GATE: any later re-hash of `parse_gsa_controlA.py` must equal the corrected row;
  CONTROLS_A.json and INPUT_IDENTITIES.json must no longer disagree.
- NOT AMENDED (disclosed, executor/parent domain): the remaining QC findings (F-QC-2 duplicate
  NULL_CHILD_SLOTS warnings in src/pecompat/PecSceneIR.js; F-QC-3 "bytes" fields that are actually
  JS character counts; F-QC-4 scene-mode independence-line wording; F-QC-5 UTF-16 raw stdout
  artifacts; F-QC-6 foreign orphan process pid 13724 + missing pm_server_run.log) are NOT repaired
  here — they are recorded in REVIEW.md / QC_RESULTS.json for PE-MASTER disposition.

AMENDMENTS TOTAL: 1. No other file in the worktree was modified by this QC.
