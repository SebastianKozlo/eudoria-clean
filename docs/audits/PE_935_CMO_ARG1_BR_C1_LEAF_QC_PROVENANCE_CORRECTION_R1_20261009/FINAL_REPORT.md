# FINAL_REPORT — PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009

```text
RUN_ID      = PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009
RUN_CLASS   = BOUNDED_MACHINERY_AND_RECORDS_CORRECTION
BASE_SHA    = a7b1dc0317af6a33b185481cd9559160188cfb24 (EXPECTED == LOCAL_HEAD
              == origin/master == live remote at preflight, 2026-10-09T15:48:16Z)
SCOPE       = close the two BR-C1 residuals (leaf-field handling; QC coverage
              provenance) + records-only model continuity; NO new RE; the
              client never ran (STATIC_ONLY); EXE reads limited to hashing,
              PE mapping and the two existing windows (replay/verify only)
OUTCOME     = BR_C1_R1_LEAF_FIELD_HANDLING = CORRECTED_IN_TESTED_SCOPE
              BR_C1_R2_QC_COVERAGE_PROVENANCE = ERRATUM_RECORDS_ONLY
              BR_C1_DESKTOP_CLOSURE = PENDING_POST_AUDIT
```

## 1. Identity and authorization

- Authoritative contract: `C:\Users\User\Documents\ChatGPT\PE\PE_BR_C1_LEAF_MODEL_CONTINUITY_PROMPT_20261009\OPENCODE_BR_C1_LEAF_QC_MODEL_CONTINUITY_R1_20261009.md`
  (19467 B / SHA256 B5D378F4BF7FC0160F3D9643284C87DB858E48759D1D1621629D508774E78820
  — measured MATCH before any action; read in full, 200 lines).
- Execution authorization: the separate human start message (2026-10-09)
  naming this exact frozen contract and authorizing this correction run.
  NEXT_EXPERIMENT_AUTHORIZED = NO.
- Executor: OpenCode agent pe-reconstruction (model nask-glm/glm-5-3),
  single session, NO_NESTED_TASKS. This executor did NOT commit, push or
  edit AUDIT_ENTRYPOINT.md; the prepared package is returned to
  PE-MASTER before publication. Fresh-context QC of this package =
  PENDING (arranged by the orchestrator; QC_RESULTS.json / QC_REPORT.md
  and PE_MASTER_REVIEW.md are NOT fabricated here; MANIFEST_SHA256.csv is
  generated LAST at persistence over the final scope).
- PREREGISTRATION.md was written BEFORE any science (identity, expected
  PRE observations, LF matrix, erratum bound, scope fences).

## 2. Preflight (measured)

- Git triple: LOCAL_HEAD == origin/master == live remote master ==
  `a7b1dc0317af6a33b185481cd9559160188cfb24` == EXPECTED_BASE_SHA
  (commands + UTC recorded in INPUT_IDENTITIES.json). Tracked
  worktree/index clean; the six foreign untracked paths (5x PE_935_*
  packages + experiments/) inventoried and left untouched.
- OUTPUT_ROOT and OUTPUT_REPO_PATH ABSENT before the run (created fresh).
- All pinned inputs re-measured MATCH: the contract (19467 B / B5D378F4...),
  predecessor correction contract (18566 B / B30E807B...), Desktop
  REPORT.md (11811 B / 5CC64F1A...), MINIMAL_SECOND_PASS.json (2070 B /
  ABA59BB4...), QC_RECORD_FRESH_CONTEXT... (19614 B / 0C6B6912...), model
  research REPORT.md (14029 B / AE4F6A93...), the five pinned source
  correction package files (MANIFEST 5674 B / DEA0F8F8...; run_frame_bridge
  123758 B / 1B11B3A1...; qc_frame_bridge 102397 B / 1D6E168C...;
  run_br_c1_controls 51514 B / 55F952A5...; BRIDGE_PROVENANCE.json
  32219 B / ADBA8BF8...), and Entropia.exe (8015872 B / E7785430...).
- Both historical packages verified against the Git blobs at BASE with
  complete before-inventories: source correction package 20/20
  byte-identical; original bridge package 35/35 byte-identical. Each old
  manifest's entrypoint row was judged against that package's original
  commit state (source correction: BASE a7b1dc0; bridge: its own recorded
  ce75b7b era), never against the later updated entrypoint.
- Predecessor records read IN FULL before implementation: predecessor
  contract (225 lines), source FINAL_REPORT / QC_REPORT /
  PE_MASTER_REVIEW / HANDOFF / SUPERSESSION, coverage, PRE/POST/
  regression results, the driver, and both gates; Desktop post-audit
  REPORT.md, MINIMAL_SECOND_PASS.json, the fresh-QC record, and the model
  research report.

## 3. PRE — the residual reproduced through the ACTUAL gates

The ACTUAL unmodified ordinary gates of the source correction package at
BASE (module hashes recorded in PRE_LEAF_RESULTS.json:
run_frame_bridge.py `1b11b3a1...`, qc_frame_bridge.py `1d6e168c...`),
deep-copied JSON loaded through their ordinary provenance override, all
temporary writes redirected to SCRATCH, no historical CLI main invoked.
Four PRE cases / eight outcomes (preregistered expectations met exactly;
matching the Desktop MINIMAL_SECOND_PASS.json 8/8):

| Case | Mutation (only the indicated leaf) | Production | QC |
|---|---|---|---|
| PRE-CLEAN | none | **PASS** (50/50 checks) | **PASS** (50/50 checks) |
| PRE-FLOAT | slot_delta_from_E: JSON 4 -> 4.0 | **PASS** (false-PASS; Python 4.0 == 4) | **PASS** (false-PASS) |
| PRE-DELETE-EXPR | delete slot_expr_from_E | **EXCEPTION** `KeyError('slot_expr_from_E')` | **EXCEPTION** `KeyError('slot_expr_from_E')` |
| PRE-DELETE-DELTA | delete slot_delta_from_E | **EXCEPTION** `KeyError('slot_delta_from_E')` | **EXCEPTION** `KeyError('slot_delta_from_E')` |

PRE residual reproduction = TRUE (raw tracebacks preserved verbatim in
PRE_LEAF_RESULTS.json). The numeric 4.0 does NOT demonstrate a different
offset — it violates the declared integer schema; and a caught exception
is EXCEPTION, not a successful semantic rejection. PRE was recorded as
measured and NEVER rewritten to match POST.

## 4. POST — the corrected two-leaf checks

Corrected COPIES under the new package 03_SCRIPTS/ (corrected module
SHA256s: run_frame_bridge.py `d5f42c1d0ff219d2cd6ec1f12e690269186c05c4ac3e5257bb6f217bf0ca464b`,
qc_frame_bridge.py `dadf1c41420f759340059f13e9ffd4598fcea666232a6707421818d8bb7ccf80`;
run_br_c1_controls.py preserved byte-identical `55f952a5...`).

- Production `gate_artifacts()`: expression leaf via the EXISTING
  `check_slot_expr` (E base vs bytes-derived `src_delta_rederived`);
  delta leaf via the EXISTING `check_int` (native JSON integer; JSON
  booleans/floats rejected). Named checks `PROV-A-SLOT-EXPR` /
  `PROV-A-SLOT-DELTA` with per-leaf named diagnostics; aggregate
  `PROV-A-SLOT` preserved as the conjunction of BOTH typed leaf
  comparisons; both leaves evaluated even if one fails; no direct
  indexing of a tested leaf can raise.
- QC `gate()`: its OWN safe helpers — new QC-local `qc_eslot_expr` /
  `qc_check_eslot_expr` for the E-based expression (expected constructed
  from independently derived `my_src`; the old hardcoded "[E+0x4]"
  string comparison removed) and the existing `qc_check_int` for the
  delta. Named checks `QC-A-SLOT-EXPR` / `QC-A-SLOT-DELTA` + the
  preserved aggregate. No production verdict import; no copied claim as
  source of truth.
- Minimality PROVEN: AST comparison — production: only `gate_artifacts`
  changed; QC: only `gate` changed + `qc_eslot_expr`/`qc_check_eslot_expr`
  added; zero added/removed/changed top-level assignments in both files.
  CODE_DIFF.patch (129 lines; both hunks inside the gate sections +
  the two new QC helpers) — mechanical apply test reproduces BOTH
  corrected files exactly. Regression preservation checks: production
  EXPECTED/MUTATIONS/CASE_ORDER and QC EXP/MUT/CASE_ORDER all IDENTICAL
  to the predecessor. No eval; no catch-and-pass; no coercion; no
  silent defaults; no universal schema engine.

### LF matrix (new; 8 cases x 2 gates = 16/16 correct)

| Case | Mutation | Production | QC | Diagnostics (both gates, verbatim class) |
|---|---|---|---|---|
| LF-CLEAN | none | PASS (52/52) | PASS (52/52) | — |
| LF-FLOAT | delta=4.0 | REJECTED | REJECTED | WRONG_TYPE delta (got float) |
| LF-BOOL | delta=true | REJECTED | REJECTED | WRONG_TYPE delta (got bool) |
| LF-MISSING-DELTA | delete delta | REJECTED | REJECTED | MISSING_FIELD delta |
| LF-MISSING-EXPR | delete expr | REJECTED | REJECTED | MISSING_FIELD expr |
| LF-NULL-EXPR | expr=null | REJECTED | REJECTED | WRONG_TYPE expr (got NoneType) |
| LF-WRONG-DELTA | delta=5 | REJECTED | REJECTED | VALUE_MISMATCH delta (derived 4, got 5) |
| LF-WRONG-EXPR | expr="[E+0x8]" | REJECTED | REJECTED | VALUE_MISMATCH expr (derived [E+0x4], got [E+0x8]) |

Every rejection: the correct named typed-leaf predicate among the failing
checks, the correct diagnostic naming the exact leaf path, failing checks
confined to the slot path (leaf + aggregate), ZERO hash/manifest-side
failures, ZERO unrelated failures, ZERO exceptions. CLEAN went through
the same final corrected ordinary gates. Mutated copies stayed in
SCRATCH (hash bypass confined to them, as in the predecessor).

### Re-executed existing matrices (unchanged case definitions, through the
            corrected copies, all writes SCRATCH, python3 -B)

- **Fixed artifact matrix = 14/14** (CLEAN PASS both; AC1/AC2 REJECTED both
  with the preserved expected predicates; BR1-BR4 REJECTED both with the
  expected named predicates, zero hash-side failures, zero exceptions).
- **Published additional controls = 43 cases / 86 outcomes, 86/86 correct**
  (32 single-field + 4 missing-field + 5 wrong-native-type + 2
  malformed-expression; definitions imported unchanged from the preserved
  run_br_c1_controls.py; SF-C2-8/SF-C2-9 still satisfy the preserved
  expected aggregate predicate and now also fail the typed leaf checks).
- **Byte regression = 24/24 CONTROL_PASS** (production 12/12 + QC 12/12
  through the corrected copies' PRESERVED helpers; GNU objdump 2.44, rc 0;
  M5 arg1 kind/expr/slot UNCHANGED while arg3/arg4 swapped and M7 arg1
  UNCHANGED while receiver changed — verified on BOTH sides;
  ADDRESS(T+8) vs MEM(T+8), exact call/slot/null-path checks preserved).
- **Clean final validation through the SAME corrected gates: production
  PASS 52/52 checks, QC PASS 52/52 checks** (measured; the count rose from
  the predecessor's 50 per gate by exactly the two new typed leaf checks
  — no check hidden to force an old count).

### In-run defects and repairs (honestly disclosed; retained attempts)

- **DEF-1 (POST evaluator; repair round 1 of max 1 used)**: the first POST
  execution recorded LF-MISSING-DELTA / LF-MISSING-EXPR as
  REJECTED_UNEXPECTED_DETAIL in both gates. The GATES were correct (failing
  checks = the exact typed leaf predicate + the aggregate; diagnostic
  MISSING_FIELD on the exact leaf; zero unrelated failures); the defect was
  in the DRIVER's evaluator — it required the diagnostic to carry a trailing
  `:<detail>` suffix, which the helpers' documented MISSING_FIELD format
  (`MISSING_FIELD:<dotted>`, no suffix) does not have. Fixed the evaluator's
  expected-format logic (gates untouched); the failed attempt's result files
  retained in SCRATCH (retained_failed_attempt_post_leaf_v1.json /
  _coverage_v1.csv); the ENTIRE POST phase was re-executed from scratch
  with the final driver bytes (identical gate outcomes; 16/16 correct after
  the fix).
- **DEF-2 (PRE comparison label; found by the executor SELF_CHECK; fixed,
  PRE re-measured)**: the PRE record's derived per-row
  `matches_preregistration` boolean was computed False for the PRE-FLOAT
  rows although the observed verdict (PASS — the preregistered false-PASS
  expectation) MATCHES the preregistration. Cause: the driver's comparison
  logic only treated the exact string "PASS" as the PASS class, so the
  preregistered "PASS (false-PASS: ...)" string fell into the
  exception-class branch. The raw PRE observations (verdicts, counts, raw
  tracebacks, module hashes, residual_reproduced flag) were correct and
  verbatim throughout; only the derived label was wrong. Fixed the PASS-class
  comparison (`startswith("PASS")`), retained the attempt
  (SCRATCH/retained_attempt_pre_leaf_v1.json) and re-measured the PRE phase
  with the final driver bytes — identical raw observations
  (PASS/PASS/KeyError/KeyError, residual_reproduced = true), truthful
  labels. This is PRE-phase harness/record-quality handling within the
  contract's PRE section ("troubleshoot only harness/setup within scope");
  it did NOT touch the gates and did NOT rewrite any raw observation. The
  POST repair budget (1 of max 1) was consumed by DEF-1 only.

## 5. QC provenance erratum (records-only)

ERRATUM_QC_PROVENANCE.md records the direct measurement of the original
later fresh-QC record (read IN FULL): re-executed = 14 (fixed) + 18
(9 selected additional cases x 2 gates) + 24 (byte regression) = **56
outcomes**; all 86 additional outcomes machine-parsed from raw rows
(68 not documented as re-executed there); no double counting; the
Desktop post-audit's full 14+86+24 re-execution is independently
attributable to Desktop, never retroactively credited to the earlier
fresh QC. Superseded: ONLY the predecessor final response's overbroad
"14+86+24 re-executed" claim. Kept:
ORIGINAL_FRESH_QC_BEFORE_PUBLICATION = NOT_MET;
RETROACTIVE_ORDER_COMPLIANCE = NO; publication integrity passed
independently of that process deviation; no automatic science/governance
retraction; the frozen historical records unchanged. The fresh-QC record
matched the contract's section-4 expectation table (verified against the
direct record, not copied as fact).

## 6. Model continuity (records-only)

MODEL_218757_CONTINUITY.md maps the prior pinned Desktop report
(PE_MODEL_218757_PLACEMENT_CASE_RESEARCH_20261009\REPORT.md, 14029 B /
AE4F6A93...) and the preserved bridge records ONLY. No asset, function,
model or instance was opened this run; every fact is labeled
ERA/BUILD/EVIDENCE_ORIGIN/SOURCE_PATH+HASH/status/REEXECUTED_THIS_RUN=no;
prior external findings stay
PRIOR_DESKTOP_MEASUREMENT_NOT_REEXECUTED_THIS_RUN. Distinctions preserved:
definition/resource relation (4057 -> 218757/218758) vs world instance;
GLB tied to 2003 ARK NIF 4.1.0.12 (C13D0873...) vs PCG NIF 10.1.0.0
(3E8A22C2...) with no build/identity transfer; Viewer Bounds
~[2500,1250,3350] = model extent, not world XYZ; the literal-u32-bounded
27-file Parameters scan whose negative proves no absence; SID 4057 =
different namespace; the AS1-AS5 + EAX!=0 chain ADDRESS(T+8) -> arg1
FUN_00528E50 -> arg1 FUN_0085B1B0 with prior ctor evidence [arg1+8] ->
MovableObject+0x44 (same-pointer substitution gives load address T+0x10 at
load time), contents/producer/type/semantics unresolved, T = ESP at
0x004C47AF (not the older R/P/T/W).

```text
MODEL_CONTINUITY_ORIGIN = PRIOR_EVIDENCE_RECORDS_ONLY
MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
```

Design-only handoff (NOT executed): the preferred subsequent question is
which existing, exactly pinned writer/source supplies that value on this
call path; a model-side consumer question may be chosen separately if it
has a stronger physical anchor; no merge into a broad run; the answer
need not be a coordinate/building; OpenMW/Gamebryo/NIF remain background
reference only.

## 7. Scope census (measured)

```text
AUTHORIZED_PARTIAL_CODE_WINDOWS = 2 (EXISTING A 66 B, B 52 B; replay/verify only)
NEW_CODE_REGIONS / CALLEES / XREF / POINTEES = 0 (0x004C47C8 unopened)
PHYSICAL NIF/GLB/ARK/VFS/BNT/SDK READS   = 0 (continuity map = records only)
NEW_MODEL_INSTANCE_RESEARCH              = 0
PRE_OUTCOMES                            = 8 (4 cases x 2 gates; residual reproduced)
LF_MATRIX                                = 16/16
FIXED_ARTIFACT_MATRIX                    = 14/14
ADDITIONAL_CONTROLS                      = 43 cases / 86 outcomes, 86/86
REQUIRED_BYTE_MATRIX                     = 24/24
CLEAN_GATE_CHECKS                        = 52/52 per gate (measured, not forced)
FIELD_CHECK_COVERAGE_ROWS                = 34 (leaf rows re-pointed at the
                                           typed-leaf predicates; F-C2-9 display
                                           artifact resolved by construction)
PREDECESSOR_SOURCE_PACKAGES_CHANGED       = 0 of 20 and 0 of 35 (re-verified
                                           before AND after all work)
EXE_CHANGED                              = NO (re-hashed every phase + final)
REPAIR_ROUNDS                            = 1 of max 1 (POST driver evaluator
                                           DEF-1) + 1 PRE harness-label fix
                                           (DEF-2, found by SELF_CHECK; PRE
                                           re-measured with the final driver
                                           bytes; retained attempts in SCRATCH)
RUNTIME / NETWORK / CLIENT LAUNCH        = 0 (STATIC_ONLY)
```

## 8. Terminal status (executor stage)

```text
RUN_ID                          = PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009
EXPECTED_BASE_SHA               = a7b1dc0317af6a33b185481cd9559160188cfb24
RESULTING_SHA                   = NOT_CREATED (no commit by this executor; the
                                  orchestrator publishes after the separate
                                  fresh-context QC)
REMOTE_SHA                      = a7b1dc0317af6a33b185481cd9559160188cfb24
                                  (unchanged at last check; no push by this run)
PERSISTENCE_STATUS               = PREPARED_NOT_PERSISTED (package returned to
                                  PE-MASTER; manifest/QC/review pending)
PRE_REPRODUCTION                 = REPRODUCED (8/8 exactly as preregistered)
BR_C1_R1_LEAF_FIELD_HANDLING    = CORRECTED_IN_TESTED_SCOPE
BR_C1_R2_QC_COVERAGE_PROVENANCE = ERRATUM_RECORDS_ONLY
BR_C1_DISPOSITIONS               = R1 corrected in tested scope; R2 erratum
                                  recorded; overall BR_C1_DESKTOP_CLOSURE =
                                  PENDING_POST_AUDIT (this run's internal
                                  acceptance is implementation-in-tested-
                                  scope only, NOT Desktop closure)
CLEAN_ARTIFACT_GATES             = PASS both corrected gates (52/52 checks
                                  each; the same gates used for every control)
NEW_LEAF_MATRIX                  = 16/16
FIXED_MATRIX / ADDITIONAL / BYTE= 14/14 ; 86/86 ; 24/24
FRESH_CONTEXT_QC (this package) = PENDING (orchestrator-arranged; executor
                                  self-review is NOT the fresh QC)
PE_MASTER_REVIEW                 = ABSENT (orchestrator supplies it)
INDEPENDENT_DESKTOP_POST_AUDIT  = NOT_PERFORMED
SCIENTIFIC_CLAIMS               = PRESERVED (no semantic promotion; J3 kept;
                                  no ACLD/CMO transfer; no CMO+0x44 -> X)
SOURCE_PACKAGES_UNCHANGED        = YES (20/20 and 35/35 before AND after)
MODEL_CONTINUITY_ORIGIN          = PRIOR_EVIDENCE_RECORDS_ONLY
MODEL_218757_TO_CMO_JOIN         = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED              = NO
CANONICAL_GATE_EFFECT            = NONE
NEXT_EXPERIMENT_AUTHORIZED       = NO
HARD_STOP                        = YES (at executor stage: package prepared,
                                  returned; nothing committed/pushed)
```

Publication (this package + one truthful AUDIT_ENTRYPOINT.md row, manifest
last, allowlisted normal commit + fast-forward push) is the ORCHESTRATOR's
terminal step after the separate fresh-context QC. WORKS != UNDERSTOOD; no
coverage beyond the measured outcomes above is claimed.
