# PREREGISTRATION — PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009

Written BEFORE any science/correction execution in this run. Scope, expected
observations and pass criteria are fixed here first; measured results are
recorded verbatim afterwards and are never rewritten to match expectations.

## 0. Identity and authorization

```text
RUN_ID            = PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009
RUN_CLASS         = BOUNDED_MACHINERY_AND_RECORDS_CORRECTION
CONTRACT          = C:\Users\User\Documents\ChatGPT\PE\PE_BR_C1_LEAF_MODEL_CONTINUITY_PROMPT_20261009\
                    OPENCODE_BR_C1_LEAF_QC_MODEL_CONTINUITY_R1_20261009.md
                    (19467 B / SHA256 B5D378F4BF7FC0160F3D9643284C87DB858E48759D1D1621629D508774E78820
                    — measured MATCH before any action; read in full, 200 lines)
EXPECTED_BASE_SHA = a7b1dc0317af6a33b185481cd9559160188cfb24
CANONICAL_REPO    = SebastianKozlo/eudoria-clean (master)
REPO_ROOT         = D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean
SOURCE_REPO_PATH  = docs/audits/PE_935_CMO_ARG1_BR_C1_ARTIFACT_VALIDATION_CORRECTION_R1_20261009/
ORIGINAL_BRIDGE_PATH = docs/audits/PE_935_CMO_ARG1_ENTRY_CALLER_BRIDGE_R1_20261009/
OUTPUT_ROOT       = D:\Eudoria_Reconstruction\99_Audits\PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009\
PACKAGE_ROOT      = OUTPUT_ROOT\PACKAGE\
SCRATCH_ROOT      = OUTPUT_ROOT\SCRATCH\   (local-only; never published)
OUTPUT_REPO_PATH  = docs/audits/PE_935_CMO_ARG1_BR_C1_LEAF_QC_PROVENANCE_CORRECTION_R1_20261009/
EXECUTION         = separate human start message (this run); executor
                    pe-reconstruction, single session, NO_NESTED_TASKS
NEXT_EXPERIMENT_AUTHORIZED = NO
```

## 1. Mission (pre-registered, narrow)

1. Close the two documented BR-C1 residuals (Desktop post-audit
   BR-C1-R1 leaf-field handling = OPEN_P2; BR-C1-R2 QC coverage provenance
   overstatement = OPEN_P2) through a small machinery + records correction:
   the two `phase_a.source_slot` leaves (`slot_expr_from_E`,
   `slot_delta_from_E`) must be checked individually by safe typed helpers
   in BOTH ordinary gates, with named diagnostics, no uncaught exception on
   a missing tested leaf, and no acceptance of a wrong native JSON type.
2. Correct the QC-provenance record: an ERRATUM separates what the earlier
   fresh-context internal QC actually re-executed from what it machine-parsed
   from raw rows; no double counting; no retroactive credit of Desktop
   execution to the earlier fresh QC; historical records unchanged.
3. Record the building-placement continuity map (MODEL_218757_CONTINUITY.md)
   from PRIOR pinned evidence ONLY — records-only; no new asset, function,
   model or instance is opened in this run.

## 2. Pinned inputs (all re-measured before implementation; see INPUT_IDENTITIES.json)

- Contract (19467 B / B5D378F4...), predecessor correction contract
  (18566 B / B30E807B...), Desktop post-audit REPORT.md (11811 B /
  5CC64F1A...), MINIMAL_SECOND_PASS.json (2070 B / ABA59BB4...),
  QC_RECORD_FRESH_CONTEXT_INTERNAL_QC_20261009.md (19614 B / 0C6B6912...),
  model research REPORT.md (14029 B / AE4F6A93...).
- Source correction package at BASE (20 files, 20/20 byte-identical to the
  Git blobs at a7b1dc0, verified before work): MANIFEST_SHA256.csv (5674 B /
  DEA0F8F8...), 03_SCRIPTS/run_frame_bridge.py (123758 B / 1B11B3A1...),
  03_SCRIPTS/qc_frame_bridge.py (102397 B / 1D6E168C...),
  03_SCRIPTS/run_br_c1_controls.py (51514 B / 55F952A5...),
  01_INPUTS/BRIDGE_PROVENANCE.json (32219 B / ADBA8BF8...).
- Original bridge package (35 files, 35/35 byte-identical to the Git blobs
  at BASE, verified before work).
- EXE (read-only): D:\Eudoria_Reconstruction\pcg_install\Entropia.exe
  (8015872 B / E7785430...). Allowed reads: whole-file hashing, PE headers
  for the existing mapping, and ONLY the two previously inspected windows
  A [0x00528E50,0x00528E92) (66 B, raw 1216080, SHA F8735567...) and
  B [0x004C4792,0x004C47C6) (52 B, raw 804754, SHA B59E16DC...),
  replay/verification only. No new bodies, xrefs, pointees. STATIC_ONLY.

## 3. Pre-registered PRE observation (the actual residual, through the
       ACTUAL UNMODIFIED ordinary gates of the source correction package)

Four cases x two gates = eight outcomes, deep-copied JSON loaded through the
ordinary provenance override, all temporary writes in SCRATCH:

| Case | Mutation (only the indicated field) | Expected PRE observation |
|---|---|---|
| PRE-CLEAN | none | PASS in both gates (50/50 checks each) |
| PRE-FLOAT | `phase_a.source_slot.slot_delta_from_E`: JSON 4 -> 4.0 | PASS in both gates despite the wrong declared integer type (Python `4.0 == 4`; `check_int` is not applied to this leaf in the predecessor gate) — a false-PASS on the declared schema type, NOT a different measured offset |
| PRE-DELETE-EXPR | delete only `slot_expr_from_E` | KeyError in both gates — an EXCEPTION is not a successful semantic rejection |
| PRE-DELETE-DELTA | delete only `slot_delta_from_E` | KeyError in both gates |

Numeric 4.0 does not demonstrate a different offset; it violates the declared
integer schema. A caught exception is EXCEPTION, not a semantic rejection. If
reproduction differs from the above, the record stays NOT_REPRODUCED /
REQUIRE_CORRECTIONS; PRE is never rewritten to match POST.

## 4. Pre-registered POST (the narrow repair and its controls)

Corrected COPIES under the new package 03_SCRIPTS/. ONLY the two leaf-field
checks change (production `gate_artifacts()`; QC `gate()`), plus a QC-local
E-based slot-expression helper and narrow driver routing. Everything else —
byte decoders, symbolic replay, ESP derivations, window definitions,
CASE_ORDER, byte mutations, MUTATIONS/EXPECTED/EXP definitions and all
unrelated predicates — stays unchanged, proven by AST comparison +
regression preservation checks + CODE_DIFF.patch.

Design (pre-registered):
- Production: the expression leaf via the existing `check_slot_expr`
  (E base, bytes-derived `src_delta_rederived`), the delta leaf via the
  existing `check_int` (native JSON integer; booleans/floats rejected).
- QC: its OWN safe string helper for the E-based expression (expected
  constructed from independently derived `my_src`, never from a copied
  claim or the production verdict) and `qc_check_int` for the delta.
- Each leaf: its own named check with a named diagnostic
  (MISSING_FIELD / WRONG_TYPE / MALFORMED_EXPR / VALUE_MISMATCH as
  applicable) and actual/expected value. Aggregate `PROV-A-SLOT` is
  preserved as the conjunction of BOTH typed leaf comparisons; both leaves
  are evaluated even if one fails; no direct indexing of a tested leaf can
  raise; no catch-and-pass, no coercion, no silent defaults, no eval, no
  universal schema engine.
- Check counts are measured; adding typed leaf checks may raise the clean
  count above 50 — no check is hidden to force an old count.

### LF matrix (new; 8 cases x 2 gates = 16 outcomes; only the indicated
            mutation, all other evidence clean)

| Case | Mutation | Required POST in each ordinary gate |
|---|---|---|
| LF-CLEAN | none | PASS |
| LF-FLOAT | delta = 4.0 | REJECTED / WRONG_TYPE on the exact delta leaf path |
| LF-BOOL | delta = true | REJECTED / WRONG_TYPE on the exact delta leaf path |
| LF-MISSING-DELTA | delete delta leaf | REJECTED / MISSING_FIELD on the delta path |
| LF-MISSING-EXPR | delete expression leaf | REJECTED / MISSING_FIELD on the expression path |
| LF-NULL-EXPR | expression = null | REJECTED / WRONG_TYPE on the expression path |
| LF-WRONG-DELTA | delta = 5 | REJECTED / VALUE_MISMATCH on the delta path |
| LF-WRONG-EXPR | expression = "[E+0x8]" | REJECTED / VALUE_MISMATCH on the expression path |

Required per rejection: the correct leaf diagnostic AND named predicate, no
uncaught exception, no hash/manifest-side failure and no unrelated failure as
the sole reason. CLEAN goes through the same final corrected ordinary gates.
Mutated copies may bypass hash/manifest checks only to exercise the fact
predicate (as in the predecessor); a synthetic CONTROL_PASS is not
falsification of unchanged client behavior. All mutated copies stay in
SCRATCH.

### Re-executed existing matrices (unchanged case definitions, through the
                                corrected copies, all writes SCRATCH)

- Fixed artifact matrix 7 cases x 2 gates = 14 outcomes: 14/14 required
  (CLEAN PASS; AC1/AC2 REJECTED for value provenance / entry slot; BR1-BR4
  REJECTED for persisted CALL identity / slot identity / contradictory
  bridge value / null-path facts).
- Published additional controls 43 cases x 2 gates = 86 outcomes: 86/86
  correct rejections through the same gates (32 single-field + 4
  missing-field + 5 wrong-native-type + 2 malformed-expression).
- Byte regression 24/24 CONTROL_PASS (production 12-case + QC 12-case byte
  matrices through the corrected copies' preserved helpers), with M5/M7
  semantics preserved (arg1 retention + changed other channels),
  ADDRESS(T+8) vs MEM(T+8), exact call/slot/null-path checks.

If a required expectation fails, the actual failure is reported. At most ONE
focused repair/recheck round inside the two-leaf scope, retaining failed
attempts.

## 5. Pre-registered QC-provenance erratum (records-only)

The pinned original later fresh-QC record (QC_RECORD_FRESH_CONTEXT_INTERNAL_
QC_20261009.md, 19614 B / 0C6B6912...) is read DIRECTLY and its coverage is
measured by evidence type (re-executed vs machine-parsed) with
timestamp/session/source. The contract's section-4 table is recorded as
EXPECTATIONS and verified against the direct record; any discrepancy is
preserved, not smoothed over. Expected (to be verified against the record):
fixed 14 outcomes re-executed; additional 9 cases / 18 outcomes re-executed;
byte regression 24 outcomes re-executed; all 43 cases / 86 additional
outcomes machine-parsed from raw rows (68 outcomes not documented as
re-executed there). No double counting of parsed and re-executed outcomes as
unique tests. No retroactive crediting of the Desktop post-audit's
re-execution (86/86 + 14/14 + 24/24) to the earlier fresh QC — the Desktop
evidence is independently attributable to Desktop.

The corrected statement supersedes ONLY the overbroad QC coverage claim (the
final-response claim that the fresh QC re-executed the full 14+86+24). It
keeps `ORIGINAL_FRESH_QC_BEFORE_PUBLICATION = NOT_MET` and
`RETROACTIVE_ORDER_COMPLIANCE = NO`, states that publication integrity passed
independently of this process deviation, and follows no automatic
science/governance retraction. Historical final answers and QC records stay
unchanged. The new correction's own fresh-context QC coverage is measured
separately by that QC (not fabricated here).

## 6. Pre-registered records-only model continuity (no new reads)

MODEL_218757_CONTINUITY.md is a compact map from the pinned prior Desktop
report (PE_MODEL_218757_PLACEMENT_CASE_RESEARCH_20261009\REPORT.md, 14029 B /
AE4F6A93...) and preserved bridge records ONLY. No new asset, function,
model or instance is opened to populate it. Every fact is labeled with
ERA/BUILD, EVIDENCE_ORIGIN, SOURCE_PATH/HASH, status and
REEXECUTED_THIS_RUN=no. Prior external findings stay
PRIOR_DESKTOP_MEASUREMENT_NOT_REEXECUTED_THIS_RUN. The distinctions fixed
in contract section 5 are preserved: definition/resource relation vs world
instance; GLB tied to the older 2003 ARK NIF 4.1.0.12 (C13D0873...) vs the
PCG 10.1.0.0 NIF (3E8A22C2...) with no build/identity transfer; Viewer
Bounds ~[2500,1250,3350] = model extent, not world XYZ; the 27-file
Parameters scan bounded to literal u32 refs with a non-proving negative; SID
4057 = different namespace; the AS1-AS5 + EAX!=0 chain ADDRESS(T+8) -> arg1
FUN_00528E50 -> arg1 FUN_0085B1B0 with prior ctor evidence [arg1+8] ->
MovableObject+0x44 (substituting the same pointer gives load address T+0x10
at load time), contents/producer/type/semantics unresolved, T = ESP at
0x004C47AF (not the older R/P/T/W symbol). Connection between the chains =
NOT_ESTABLISHED; historical building XYZ = NOT_RECOVERED. Design-only
handoff: the preferred subsequent question is which existing, exactly
pinned writer/source supplies that value on this call path (DESIGN ONLY,
not executed; a model-side consumer question may be chosen separately if it
has a stronger physical anchor; no merge into a broad run; the answer need
not be a coordinate/building). OpenMW/Gamebryo/NIF = background reference
only; no new research, no ABI/offset transfer.

## 7. Scope fences (fail-closed)

No new features; no T+0x10 producer investigation; no assets; no
placement/XYZ work; no upstream producer trace; no new
caller/receiver/getter/transform RE; no client launch (STATIC_ONLY); no
qualification/milestone action; no next experiment; no edits to active
profiles, skills, other packages, milestone files or proprietary sources;
no physical NIF/GLB/ARK/VFS/BNT/SDK reads. This executor does NOT commit,
push or edit AUDIT_ENTRYPOINT.md; the prepared package is returned to the
orchestrator (PE-MASTER) before publication, and the separate fresh-context
QC (QC_RESULTS.json / QC_REPORT.md), PE_MASTER_REVIEW.md and
MANIFEST_SHA256.csv are left to the orchestrator/persistence phase
(mark PENDING; never fabricate).

## 8. Standing science (pre-registered as unchanged; no promotion)

```text
CROSS_CALL_POINTER_VALUE_IDENTITY = CONFIRMED_STATIC_CONDITIONAL
BRIDGE_STATUS = POINTER_VALUE_IDENTITY_ESTABLISHED_CONDITIONAL
CONDITIONS = AS1-AS5 plus EAX!=0, unchanged
POINTEE_CONTENTS_PROVENANCE = UNRESOLVED_UPSTREAM
FIELD_SEMANTICS = UNVERIFIED
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED
HISTORICAL_PLACEMENT = NOT_ESTABLISHED
WORLD_XYZ_RECOVERED = NO
CANONICAL_GATE_EFFECT = NONE
```

J3 supersessions kept; no ACLD/CMO identity transfer; no CMO+0x44 -> X
promotion. Supersession scope: ONLY adequacy/full-closure claims affected by
the two residuals and the overbroad QC coverage claim. Previous authentic
PRE/POST, required controls, clean conditional science and the actual
late-QC history are preserved.

## 9. Self-check plan (executor SELF_CHECK, not the fresh QC)

After all phases: full raw census of every recorded outcome; all gates
evaluated; negative controls meaningful (each LF rejection carries the
named leaf predicate + diagnostic class, zero hash-side failures, zero
exceptions); correct source/generator hashes recorded in the result files;
no default-success fallbacks; EXE re-hashed after every phase; both source
packages re-inventoried after all work; deviation list honest; WORKS !=
UNDERSTOOD.
