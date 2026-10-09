# HANDOFF — PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009

Contract §10 terminal handoff, populated from REAL measurements only. If a check had
not passed, its actual result would be reported here instead of the expected value.

```text
RUN_ID = PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009
BASE_SHA = e687eb1360cc0f6f4c4d7c8db7587bb5d357bc6b
RESULTING_SHA = recorded at the terminal handoff per contract §9 — not embedded in this commit's files
REMOTE_SHA = recorded at the terminal handoff per contract §9 — not embedded in this commit's files

CALLSITE_VA = 0x00528E8D
CALLSITE_BYTES = E8 1E 23 33 00
CALLEE_TARGET = 0x0085B1B0
WINDOW_SIZE_BYTES = 28
WINDOW_SHA256 = 64102BC06987D31B9610B43602B7F777A73219FF9209F554241EE52080B923A2

THIS_REGISTER = THIS = ECX (callee thiscall receiver, set from ESI @0x00528E8B; separate from arg1)
THIS_SOURCE = ESI (defined @0x00528E76 from the symbolic entry ECX)
ESP_AT_WINDOW_START = SYMBOLIC_S
ESP_DELTA_BY_INSTRUCTION = see STACK_LEDGER.csv (0,0,0,0,0,-4,-4,-4,0,-4)
ESP_BEFORE_CALL = S-0x0C
ESP_AT_CALLEE_ENTRY = S-0x10

ARG1_CALLSITE_SLOT = [S-0xC] (written by push edi @0x00528E8A)
ARG1_ENTRY_SLOT = [ESP_AT_CALLEE_ENTRY+4] = [S-0xC]
ARG1_PUSH_INSTRUCTION_VA = 0x00528E8A
ARG1_PUSH_SOURCE = EDI (defined @0x00528E84)
ARG1_IMMEDIATE_PRODUCER_VA = 0x00528E84
ARG1_IMMEDIATE_SOURCE_OPERAND = DWORD [S+0x3C]
REACHING_DEFINITION_STATUS = IN_WINDOW_REACHING_DEFINITION_ESTABLISHED
UPSTREAM_BOUNDARY = UNRESOLVED_UPSTREAM
PATH_SCOPE = the examined straight-line path entering 0x00528E76 normally reaching the CALL
ABI_ASSUMPTIONS = 32-bit push/call; right-to-left push order => last push = arg1; thiscall
  receiver in ECX; callee entry conventions from prior-pinned committed evidence

CONTROL_CASE_COUNT = 6
EXECUTOR_CONTROL_OUTCOMES = BASELINE_QUALIFIED + 5x CONTROL_PASS
QC_CONTROL_OUTCOMES = BASELINE_QUALIFIED + 5x CONTROL_PASS (12 total, cases != outcomes)

SCIENCE_OUTCOME = ARG1_DIRECT_SOURCE_ESTABLISHED
UPSTREAM_PROVENANCE = UNRESOLVED_UPSTREAM

QC_ORIGIN = pe-master-auditor fresh-context internal QC (internal to PE-MASTER; not a Desktop post-audit)
QC_VERDICT = QC_PASS
RUN_VERDICT = MASTER_ACCEPTED (advisory; ADVISORY_PRE_QUALIFICATION)

MANIFEST_ROWS = 16
PHYSICAL_PACKAGE_FILE_COUNT = 16
MANIFEST_BIJECTION = PASS (measured)
CHANGED_PATH_CENSUS = 17 (16 package files incl. the manifest + AUDIT_ENTRYPOINT.md; measured at staging)
HISTORICAL_PACKAGES_UNCHANGED = YES

OPEN_FINDINGS = F-QC-1 (P3), F-QC-2 (P3), UPSTREAM_BOUNDARY by design

INDEPENDENT_DESKTOP_POST_AUDIT = NOT_PERFORMED
FIELD_SEMANTICS = UNVERIFIED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
HARD_STOP = YES
```

## Value provenance (each terminal value -> its evidence)

- `CALLSITE_VA` / `CALLSITE_BYTES` / `CALLEE_TARGET` / `WINDOW_SIZE_BYTES` /
  `WINDOW_SHA256`: fresh physical re-pin, triple-verified independently (executor
  `01_EVIDENCE/WINDOW_IDENTITY.json`; QC `QC_RESULTS.json` duty 1 — own PE mapping,
  own read of exactly 28 bytes at offset 1216118, own SHA == pin; PE-MASTER
  `PE_MASTER_REVIEW.md` own re-pin ALL MATCH). rel32 0x0033231E recompute
  0x00528E92 + 0x0033231E = 0x0085B1B0 == objdump target; falsifier liveness proven by
  QC NC2 (one rel32 byte mutated => the pinned-target check FAILED as designed).
- `THIS_REGISTER` / `THIS_SOURCE`: `mov ecx,esi` @0x00528E8B after
  `mov esi,ecx` @0x00528E76 (executor + QC ledgers agree; PE-MASTER manual
  verification consistent); the receiver channel is separate from the arg1 stack slot.
- `ESP_*` fields: `STACK_LEDGER.csv` rows 1..10 (ESP delta 0,0,0,0,0,-4,-4,-4,0,-4;
  ESP_AFTER S, S, S, S, S, S-0x4, S-0x8, S-0xC, S-0xC, S-0x10); machine-parsed by the
  QC — exact match; M2 mutant shows the ledger responds to an ESP perturbation
  (loads at S-4 => source [S+0x38]; entry S-0x14).
- `ARG1_*` fields: `ARG1_PROVENANCE.json` (the machine-readable result), derived by
  the executor replay from the objdump decode, independently re-derived by the QC
  (`QC_RESULTS.json` duty 2, 0 semantic differences), manually verified by PE-MASTER.
  The load `mov edi,DWORD PTR [esp+0x3c]` @0x00528E84 is the sole in-window EDI
  definition; the only in-window memory write is [S+0x10] @0x00528E78 (no alias of
  [S+0x3C]); all three loads execute at ESP = S; push edi @0x00528E8A is the LAST
  push => [S-0xC] = [entry+4] = arg1 under the stated ABI. M3 (EDI def removed) flips
  the status to UNRESOLVED_UPSTREAM — the derivation is sensitive to exactly the
  perturbation it claims to measure.
- `CONTROL_CASE_COUNT` / `EXECUTOR_CONTROL_OUTCOMES` / `QC_CONTROL_OUTCOMES`:
  `CONTROLS_RESULTS.json` (executor 6 cases: BASELINE_QUALIFIED + 5x CONTROL_PASS,
  each through the REAL analysis — objdump + symbolic replay, fixtures byte-confined,
  baseline hash identity-only) + `QC_RESULTS.json` duty 3 (QC's own fixtures — SHA256s
  byte-identical by independent construction — own replay, 6/6 agreement; 12 analysis
  outcomes = 6 cases x 2 implementations; cases != outcomes; not 12 independent
  implementations).
- `SCIENCE_OUTCOME` / `UPSTREAM_PROVENANCE`: `ARG1_PROVENANCE.json` — the confirmed
  direct source coexists with the unresolved upstream boundary (both dimensions
  reported per contract §6); QC verified completeness; no field semantics, no
  world/coordinate interpretation anywhere in the package (QC token scans: 0).
- `QC_ORIGIN` / `QC_VERDICT`: `QC_REPORT.md` / `QC_RESULTS.json` (fresh-context
  internal QC inside PE-MASTER's delegation chain; NOT an independent Desktop
  post-audit; independence dimensions stated honestly — same disassembler =
  NOT cross-implementation disassembler QC).
- `RUN_VERDICT`: `PE_MASTER_REVIEW.md` (persisted verbatim; internal advisory
  MASTER_AUDIT; own window re-pin + manual ledger decomposition ALL MATCH;
  ADVISORY_PRE_QUALIFICATION — PE-MASTER remains PROVISIONAL_UNTIL_QUALIFIED).
- `MANIFEST_ROWS = 16` / `PHYSICAL_PACKAGE_FILE_COUNT = 16` / `MANIFEST_BIJECTION =
  PASS (measured)`: `MANIFEST_SHA256.csv` generated LAST over the final persistence
  scope (every physical file under this package except the manifest itself + the
  updated AUDIT_ENTRYPOINT.md; repo-relative; measured census 16 physical package
  files => 15 package rows + 1 entrypoint row = 16 rows; zero
  missing/extra/duplicate/size/SHA mismatches; LF, UTF-8 no BOM, lowercase hex;
  self-exclusion documented in the manifest header).
- `CHANGED_PATH_CENSUS = 17`: staged at persistence = exactly the 16 package files
  (11 frozen executor/QC + PE_MASTER_REVIEW.md + FINAL_REPORT.md + EVIDENCE_INDEX.md +
  HANDOFF.md + MANIFEST_SHA256.csv) + AUDIT_ENTRYPOINT.md; staged census clean (zero
  foreign, zero historical-package files, zero residue).
- `HISTORICAL_PACKAGES_UNCHANGED = YES`: `git diff e687eb1 -- <historical packages>`
  empty at persistence (all prior run packages byte-identical to BASE); foreign
  untracked paths (5x PE_935_* packages + experiments/) untouched and not staged.
- `OPEN_FINDINGS`: F-QC-1 (P3, cosmetic — executor register_definitions emission
  loses intermediate defs; no verdict/check/claim depends on it; a future correction
  needs a new human decision); F-QC-2 (P3 — two QC-side cosmetic notes);
  UPSTREAM_BOUNDARY by design (the producer/type of [S+0x3C] before the window is
  deliberately untraced; budget UPSTREAM_PROVIDER_TRACING = 0) — not a defect.

## Persistence facts (this phase)

- Persistence scope: OUTPUT_ROOT (`docs/audits/PE_935_CMO_ARG1_SINGLE_CALLSITE_PROVENANCE_R1_20261009/`)
  + ONE new newest-first LATEST RUNS row in `AUDIT_ENTRYPOINT.md` (existing 5-column
  format; no other row modified).
- Allowlist gates: git status/diff limited to OUTPUT_ROOT/** + AUDIT_ENTRYPOINT.md; no
  proprietary payload (no EXE bytes, no binary scratch windows; only bounded
  instruction text with source identity); no residue (`python -B`; no
  __pycache__/.pyc/temp); executor + QC evidence FROZEN (the 11 files untouched by
  this phase — re-hashed at persistence start).
- LOCAL_HEAD == origin/master == actual remote master == e687eb1… re-verified live
  (ls-remote) immediately before commit; ONE normal commit (RUN_ID-prefixed long
  message, repo style); normal fast-forward push; no amend, no rebase, no force, no
  history rewrite.
- Per contract §9: a push/remote-verification failure would be a persistence failure,
  not a scientific PASS — the actual local/remote state would be preserved and the run
  would HARD STOP without a follow-up run and without guard weakening. QC failure
  alone would not be permission to abandon the evidence or promote it — here QC_PASS
  and all technical gates hold.
- No self-referential SHA: RESULTING_SHA/REMOTE_SHA are recorded at the terminal
  handoff, not embedded in any file of this commit.

**WORKS != UNDERSTOOD. NO AUTOMATIC UPSTREAM CONTINUATION. HARD_STOP = YES.**
