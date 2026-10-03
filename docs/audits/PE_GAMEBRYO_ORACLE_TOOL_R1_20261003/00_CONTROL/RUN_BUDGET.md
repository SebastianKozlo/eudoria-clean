# RUN_BUDGET — PE_GAMEBRYO_ORACLE_TOOL_R1_20261003

Preregistered budgets (fixed by the PE-MASTER dispatch BEFORE any
execution). The deadline frame comes from the parent loop:
started 2026-10-03T15:13:15Z, deadline 2026-10-03T23:13:15Z (8h), drain
deadline 2026-10-03T23:23:15Z. All verdicts in this run are
ADVISORY_PRE_QUALIFICATION (Q1 absent).

## Batch budgets

| Batch | Worker | Tool calls | Wall minutes | Scope |
|---|---|---|---|---|
| E1 | pe-reconstruction (executor) | <= 60 | <= 150 | Phase A forensic inventory + Phase B version support + Phase C pipeline + T-corpus selection (incl. SELECTION.md fill + hash-lock) |
| E2 | pe-reconstruction (executor) | <= 80 | <= 180 | Phase D tool build + positive/negative controls + T-runs + original-vs-our-decoder comparison + 218757.nif probe + compatibility matrix + optional signatures + FINAL_REPORT |
| E3 (OPTIONAL) | pe-reconstruction (executor) | <= 50 | <= 120 | Only if PE-MASTER explicitly authorizes a continuation batch (e.g. original-tool execution attempts that E2 could not finish); without explicit PE-MASTER dispatch this batch DOES NOT EXIST |
| FRESH QC | pe-master-auditor (fresh context, NOT the formalizer) | <= 40 | <= 90 | Order section 29 / RUN_CONTRACT section (n) |
| PERSIST | pe-master-auditor (persistence worker) | <= 30 | <= 60 | Order section 30 / RUN_CONTRACT section (o) |

## Reserved time

- **>= 30 minutes are RESERVED for the PE-MASTER full audit + loop drain
  before the 8h deadline.** No executor/QC/persistence batch may consume
  this reserve. The persistence phase must be able to complete (ONE commit
  + push + three-way verify) before the drain deadline 23:23:15Z.

## Budget rules (binding)

1. **Budget exhaustion = honest PARTIAL with the exact stop point
   recorded, NEVER scope-faking.** A batch that hits its call or minute
   budget stops, writes its HANDOFF return with RUN_STATUS = PARTIAL (or
   the exact gate states reached), and returns to PE-MASTER. It is
   FORBIDDEN to compress the remaining scope into unverified claims, to
   mark unexecuted gates as anything other than NOT_TESTED/UNKNOWN, or to
   silently drop controls to save calls.
2. Every batch return records BUDGET_USED = {calls used, wall minutes
   used} against its preregistered cap (part of the final handoff schema,
   RUN_CONTRACT section (q)).
3. Calls spent re-reading one's own outputs do not extend the budget; the
   budget is a hard stop, and asking PE-MASTER for more budget is a
   CORRECTION_REQUEST, not self-service.
4. If E1 cannot finish Phase A+B+C+selection within budget, it returns
   PARTIAL with per-gate states; PE-MASTER (not the executor) decides
   whether E2 proceeds on the partial base or a continuation batch is
   dispatched.
5. The QC and PERSIST budgets belong to their respective workers; the
   executor may not borrow them.
6. Any deviation (overrun, underrun with idle capacity, mid-batch
   blocker) is recorded honestly in the batch return; underrun is NOT a
   failure — inflating scope to "use up" budget is forbidden (HARD STOP H5:
   scope creep).
