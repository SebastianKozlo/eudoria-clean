# QC_REPORT — FRESH-CONTEXT INTERNAL QC — PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009

```text
QC_RECORD_ID   = QC_FRESH_CONTEXT_PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009
QC_ORIGIN      = pe-master-auditor fresh-context internal QC, internal to
                PE-MASTER — NOT an independent Desktop post-audit, NOT
                executor self-review
QC_PERFORMER   = OpenCode agent pe-master-auditor worker session
                (model nask-glm/glm-5-3), dispatched by PE-MASTER;
                NO_NESTED_TASKS honored
QC_DATE_UTC    = 2026-10-09
AUDITED_STATE  = HEAD a7b1dc0317af6a33b185481cd9559160188cfb24 == BASE ==
                local origin/master; tracked worktree clean; executor stage
                PREPARED_NOT_PERSISTED (QC performed BEFORE publication, per
                contract section 6 — the ordering requirement is MET for
                THIS run)
CONTRACT       = C:\Users\User\Documents\ChatGPT\PE\PE_BR_C1_LEAF_MODEL_
                CONTINUITY_PROMPT_20261009\OPENCODE_BR_C1_LEAF_QC_MODEL_
                CONTINUITY_R1_20261009.md (19467 B / SHA256 B5D378F4BF7F
                C0160F3D9643284C87DB858E48759D1D1621629D508774E78820 —
                re-measured MATCH by this QC; read in full, 200 lines)
INTERNAL_QC_VERDICT = QC_PASS
```

## 1. Implementation independence (stated precisely)

- **Own fixtures**: the PRE and LF mutated provenance copies were built by
  MY OWN builder (own dotted-path SET/DEL logic, own JSON round-trip deep
  copy, own serialization, own paths under SCRATCH\QC_FRESH). The executor's
  fixture files (SCRATCH\prov\*.json) were never read or copied.
- **Own harness and own evaluation**: own driver
  (`SCRATCH/QC_FRESH/qc_fresh_harness.py`, `qc_fresh_compare.py`), own
  gate-invocation wrappers (raw, untruncated tracebacks), own LF evaluation
  predicates implemented directly from contract section 3, own AST
  comparison, own patch-application test.
- **PRE gates**: the ACTUAL UNMODIFIED source-correction gates extracted from
  git blobs at BASE (`git cat-file`, byte-exact via cmd redirection), hashes
  re-verified `1b11b3a1...` / `1d6e168c...` BEFORE execution.
- **POST gates**: the corrected package copies (`d5f42c1d...` /
  `dadf1c41...`) — these ARE the artifacts under test; a machinery-correction
  QC re-executes through them, so verdict independence comes from my own
  fixtures/evaluation, not from a re-implemented gate.
- **Unchanged case definitions**: the fixed/additional matrices use the
  preserved published definitions imported from `run_br_c1_controls.py`
  (byte-identical to the published driver, `55f952a5...`) as the contract
  requires.
- **Shared tool lineage (honest)**: GNU objdump 2.44 (WSL PE-AI) is the SAME
  single disassembler the executor used — NOT two independent decoders.
- All my writes stayed under `SCRATCH\QC_FRESH` (local-only); no executor
  evidence was modified. WORKS != UNDERSTOOD.

## 2. Measured coverage of THIS QC (what I actually did)

```text
RE-EXECUTED (my own fixtures/invocations):
  PRE                      4 cases x 2 gates =  8 outcomes (BASE gates)
  LF matrix                8 cases x 2 gates = 16 outcomes (corrected gates)
  fixed matrix             7 cases x 2 gates = 14 outcomes
  additional controls     43 cases x 2 gates = 86 outcomes
  byte regression      12 prod + 12 QC cases = 24 outcomes
  TOTAL RE-EXECUTED                          = 148 outcomes
  clean final validation (same corrected gates, no override):
    production PASS 52/52 checks; QC PASS 52/52 checks (measured)
MECHANICAL PROOFS: CODE_DIFF.patch apply test (reproduces BOTH corrected
  files byte-exactly); own AST comparison; module-level
  EXPECTED/MUTATIONS/CASE_ORDER/EXP/MUT identity vs BASE; FIELD_CHECK_
  COVERAGE re-parse (34 rows); DEF-1/DEF-2 retained-attempt comparisons.
SEMANTIC DIFFERENCES vs the executor's recorded results: 0
  (programmatic row-by-row comparison of PRE, LF, fixed, additional,
  regression: verdicts, failing-check sets, leaf diagnostics, exception
  types/reprs, check counts, matrix totals, M5/M7 flags, preservation flags)
```

## 3. Per-duty results

| # | Duty | Result | Key evidence |
|---|---|---|---|
| D1 | INPUT/PACKAGE IDENTITY | PASS | 18 package files re-hashed; package == repo mirror 18/18 byte-identical (re-verified again after all QC work); BRIDGE_PROVENANCE.json `ADBA8BF8...`/32219 B == pin; EXE `E7785430...`/8015872 B re-hashed before AND after all QC work; all four pinned Desktop records + model report re-hashed MATCH; no SCRATCH content in PACKAGE |
| D2 | PRE reproduction | PASS | My own mutations through the BASE-extracted predecessor gates: CLEAN PASS 50/50 both; PRE-FLOAT **PASS 50/50 both (the false-PASS residual reproduced)**; both deletions `KeyError('slot_expr_from_E'` / `KeyError('slot_delta_from_E')` in both gates with raw tracebacks (same predecessor source lines as the executor's record); residual_reproduced = true; matches PRE_LEAF_RESULTS.json exactly and Desktop MINIMAL_SECOND_PASS.json 8/8 |
| D3 | LF matrix re-execution | PASS | 16/16 through the corrected gates. Every rejection: REJECTED with the exact named typed predicate (PROV-A-SLOT-EXPR/-DELTA, QC-A-SLOT-EXPR/-DELTA), failing set confined to {leaf, PROV-A-SLOT}, correct diagnostic on the exact leaf path (`WRONG_TYPE:...expected JSON integer, got float/bool`, `MISSING_FIELD:phase_a.source_slot.<leaf>` exactly, `WRONG_TYPE:...expected JSON string, got NoneType`, `VALUE_MISMATCH:...derived 4, got 5`, `VALUE_MISMATCH:...derived [E+0x4], got '[E+0x8]'`), zero exceptions, zero hash-side failures, zero unrelated failures; LF-CLEAN PASS through the same final gates; matches POST_LEAF_RESULTS.json exactly |
| D4 | Regression re-execution | PASS | fixed 14/14; additional 43/86 -> 86/86 (SF-C2-8/9 still satisfy the preserved aggregate predicate AND now also fail the typed leaf predicates — verified in my run); byte regression 24/24 CONTROL_PASS (objdump 2.44, rc 0); M5/M7 arg1-retention verified on BOTH sides; ADDRESS(T+8) vs MEM(T+8) verified on the expected rows (prod: clean arg1_kind=ADDRESS/expr ADDRESS(T+0x8) vs M9 STACK_READ/MEM(T+0x8); QC: aslots a1 [ADDR,8] vs [MEM,8]); matches the executor's results exactly |
| D5 | Minimality audit | PASS | My own `patch -p1` application of CODE_DIFF.patch to the BASE-extracted originals reproduces BOTH corrected files byte-exactly; my own AST comparison: production ONLY `gate_artifacts` changed, QC ONLY `gate` changed + exactly `qc_eslot_expr`/`qc_check_eslot_expr` added, zero top-level assignment changes (matches the recorded ast_comparison); EXPECTED/MUTATIONS/CASE_ORDER/EXP/MUT module-identical to BASE; diff scope = the two gate hunks + the two QC helpers (+ one cosmetic whitespace line — F-QCF-1) |
| D6 | QC provenance erratum | PASS | The pinned record `0C6B6912...` read DIRECTLY in full; its coverage measured: re-executed 14 (fixed) + 18 (9 selected additional cases x 2) + 24 (byte regression) = **56 outcomes**; machine-parsed all 86 additional outcomes (68 not documented as re-executed there) — the contract section-4 expectation table MATCHES the direct record; ERRATUM_QC_PROVENANCE.md states exactly this bound with verbatim quotes (verified against the record); no double counting (18 subset of 86); no retroactive Desktop credit (Desktop's own 14+86+24 confirmed from its REPORT.md section 2, kept separately attributable); `ORIGINAL_FRESH_QC_BEFORE_PUBLICATION = NOT_MET` and `RETROACTIVE_ORDER_COMPLIANCE = NO` preserved; commit a7b1dc0 time verified == 14:01:51 UTC |
| D7 | Model continuity | PASS | All 9 facts of MODEL_218757_CONTINUITY.md verified against the pinned research report `AE4F6A93...` read in full (record 4057/218757/218758 fields, CRC 79E7AC62, float 0x41AA0F28; GLB 511452 B/D58D7534; NIF 4.1.0.12 56535 B/C13D0873 vs PCG 10.1.0.0 57316 B/3E8A22C2; ARK copies F660D055; ark_export_report numbers; Viewer Bounds [2500,1250,3350]; root transforms; outpost mesh names; 27-file scan 14825 records / 3 hits breakdown / sids namespace) — all EXACT; every fact labeled ERA/ORIGIN/SOURCE+HASH/REEXECUTED_THIS_RUN=no; all contract section-5 distinctions preserved; join NOT_ESTABLISHED; XYZ NOT_RECOVERED; no new asset/function/instance opened |
| D8 | Scope/hygiene | PASS | Only OUTPUT_ROOT + the untracked mirror written by the run; tracked paths: zero changes (git diff empty; AUDIT_ENTRYPOINT.md unchanged vs BASE); 6 foreign untracked paths untouched (newest mtimes 2026-09-11..2026-10-03, all before the run); BOTH source packages blob-identical to BASE (explicit-SHA git hash-object comparison: 20/20 and 35/35); zero .pyc/__pycache__; all 18 files UTF-8 no BOM, 17 text files pure LF (CSV CRLF = predecessor convention, F-QCF-2); no forbidden payload/credentials |
| D9 | Findings ledger | PASS | DEF-1 and DEF-2 both adjudicated **HONEST** (below); zero semantic differences vs the executor's results; no executor defect requires a correction round |

## 4. In-run defect adjudication (executor-disclosed)

**DEF-1 (POST driver evaluator; repair round 1 of max 1) — HONEST.**
The retained failed attempt
(`SCRATCH/retained_failed_attempt_post_leaf_v1.json`) exists and records
LF-MISSING-DELTA / LF-MISSING-EXPR as REJECTED_UNEXPECTED_DETAIL (attempt
lf_matrix 12/16) while ALL 16 gate outcomes (verdicts, failing checks,
diagnostics) are IDENTICAL to the final POST_LEAF_RESULTS.json — mechanical
proof that the defect was in the DRIVER's evaluator (it required a trailing
detail suffix the helpers' documented `MISSING_FIELD:<dotted>` format does
not have), not in the gates. The repair budget (1 of 1) was respected, the
failed attempt retained, the entire POST re-executed with the final driver
bytes, and my own evaluator reproduces 16/16.

**DEF-2 (PRE comparison label; harness fix under section 2) — HONEST.**
The retained attempt (`SCRATCH/retained_attempt_pre_leaf_v1.json`) exists;
its PRE-FLOAT rows carry `matches_preregistration = False` while ALL raw
observations (verdicts, exception types/reprs, check counts, pass counts,
`residual_reproduced = true`) are IDENTICAL to the final PRE record — exactly
the disclosed driver PASS-class comparison bug (`startswith("PASS")` fix).
No raw PRE observation was rewritten; PRE was re-measured with the final
driver bytes. This is PRE-phase harness/record-quality handling within the
contract's PRE section; the POST repair budget was consumed by DEF-1 only.

## 5. Findings (complete list; none blocks publication)

**F-QCF-1 (P3, cosmetic — one AST-invisible whitespace line in the diff).**
Location: CODE_DIFF.patch hunk 1, the `"little")` continuation line inside
`gate_artifacts` gains one leading space. Effect: none — the AST proof (only
`gate_artifacts`/`gate` changed) holds, the patch reproduces the corrected
file byte-exactly, no verdict/count/predicate is affected. Correction:
optional normalization in a future machinery pass; not required for this
run's validity.

**F-QCF-2 (P3, observation — CSV CRLF convention).**
FIELD_CHECK_COVERAGE.csv uses CRLF (csv.DictWriter with `newline=""`), unlike
the 17 pure-LF text documents. The published predecessor's coverage CSV at
BASE uses the SAME convention (35x CRLF, 0x bare LF), written by the same
preserved writer logic — a convention-consistent file, not a new deviation.
The persistence-phase manifest must simply hash the final bytes.

**F-QCF-0 (P3-informational, MY tooling — not an executor defect).**
My first BASE-blob extraction was transcoded to UTF-16 by PowerShell `>`
redirection; self-caught at the hash-verification step and re-extracted
byte-exactly via `cmd /c` before any gate execution. Recorded for instrument
transparency; no audit evidence affected.

No P0, no P1, no P2 findings. No executor artifact requires repair by
pe-reconstruction.

## 6. Standing (unchanged by this QC)

```text
CROSS_CALL_POINTER_VALUE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL
BRIDGE_STATUS = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL
CONDITIONS = AS1-AS5 plus EAX!=0, unchanged
POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM
FIELD_SEMANTICS = UNVERIFIED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
```

J3 supersessions kept; no ACLD/CMO identity transfer; no CMO+0x44 -> X
promotion; no semantic promotion of any recorded fact.

## 7. FULL_READ_LOG

Read IN FULL by this QC: the contract (200 lines); the pinned fresh-QC
record (314 lines); Desktop REPORT.md (118 lines); MINIMAL_SECOND_PASS.json
(98 lines); the model research report (163 lines); MODEL_218757_CONTINUITY.md
(83); ERRATUM_QC_PROVENANCE.md (137); SUPERSESSION_AND_STANDING.md (179);
EVIDENCE_INDEX.md (89); FINAL_REPORT.md (318); HANDOFF.md (191);
PREREGISTRATION.md (249); INPUT_IDENTITIES.json (104); PRE_LEAF_RESULTS.json
(1850); CODE_DIFF.patch (129); 03_SCRIPTS/run_leaf_controls.py (912);
03_SCRIPTS/run_br_c1_controls.py (1035); the corrected run_frame_bridge.py
in all load-bearing regions (full gate_artifacts, all field helpers, module
definitions, build_fixture/run_case; lines 63-222, 1115-1234, 1690-2299 plus
full function census); the corrected qc_frame_bridge.py in all load-bearing
regions (full gate(), all qc helpers incl. the two new ones, module
definitions; lines 40-259, 860-1469 plus full function census).

Machine-parsed IN FULL: POST_LEAF_RESULTS.json (every LF/fixed/additional/
clean-final/AST block compared row-by-row against my re-execution);
REGRESSION_RESULTS.json (all 24 case verdicts, M5/M7 blocks, preservation
flags); FIELD_CHECK_COVERAGE.csv (34 rows); the retained DEF-1/DEF-2 attempt
files.

## 8. NOT_CHECKED

- The unchanged byte-decoder/symbolic-replay middle sections of both gate
  files line-by-line (run_frame_bridge.py ~223-1115; qc_frame_bridge.py
  ~260-860): PROVEN unchanged vs BASE by my own AST comparison + module
  definition identity + the byte-exact patch apply test, and functionally
  exercised by my 24/24 byte-matrix re-execution through them.
- Executor scratch tooling sources (self_check.py, patchtest.sh): their
  retained outputs were programmatically verified; the sources not read.
- The predecessor package's non-input documents: out of this correction QC's
  scope; its load-bearing inputs were hash-verified vs BASE and functionally
  exercised.
- The live remote: NOT re-queried by this QC (local origin/master == HEAD ==
  BASE verified); the orchestrator re-verifies live at persistence per
  contract section 7.

## 9. Verdict

```text
INTERNAL_QC_VERDICT      = QC_PASS
P0/P1/P2 FINDINGS        = NONE
P3 OBSERVATIONS          = F-QCF-1 (diff whitespace), F-QCF-2 (CSV CRLF
                           convention), F-QCF-0 (QC tooling incident,
                           self-caught)
EXECUTOR DEFECTS         = DEF-1, DEF-2 — both HONEST (retained evidence
                           verified; raw outcomes identical)
CORRECTION ROUND NEEDED  = NONE for this package
BR_C1_R1                 = CORRECTED_IN_TESTED_SCOPE (independently
                           confirmed by re-execution; NOT Desktop closure)
BR_C1_R2                 = ERRATUM_RECORDS_ONLY (verified against the
                           direct record)
BR_C1_DESKTOP_CLOSURE    = PENDING_POST_AUDIT (this internal QC is NOT the
                           independent Desktop post-audit)
NEXT_EXPERIMENT_AUTHORIZED = NO
```

This QC wrote ONLY `QC_RESULTS.json` and `QC_REPORT.md` (byte-identical in
both the local PACKAGE and the repo mirror) plus its own scratch under
`SCRATCH\QC_FRESH` (local-only). No commit, no push, no entrypoint edit, no
manifest (generated LAST at persistence). The package is returned to
PE-MASTER for adjudication and the persistence phase.
