# FINAL_REPORT — PE_935_PLACEMENT_PROBE_PREFLIGHT_CORRECTION_R1_20261011

STATUS LABEL: FINAL

## Verdict
**CORRECTION_STATUS = PARTIAL.** The planned correction set and both allowed fix rounds are complete; every §6 observation and both §7 cases are implemented, measured and PASS; the §8 budget semantics are enforced and measured PASS for the covered scenarios, with ONE residual P2 defect class (R2-5, below) and five P3 residuals disclosed in INTERNAL_REVIEW.md. Per contract §8 the two fix rounds are exhausted, so the residuals are persisted honestly instead of being fixed by a third round.

## Scope actually executed (correction-only, synthetic inputs)
- Corrected Placement Probe Kit R1 in `tools/placement_probe/` (placement_probe.mjs, ids_from_export.mjs, README.md, tests/**).
- No PCG placement pilot, no original-game payload reads for placement, no EXE/Gamebryo RE, no Viewer changes, no master merge, no standing-science status changes. PLACEMENT_DISCOVERY = NOT_EXECUTED.

## Measured results (all generated from executed artifacts; commands, exit codes and code/fixture identities in POST/)
- Original 7 kit tests: **7/7 pass** on the corrected tool (originalSevenNamesPass=true), suite total 27/27 pass / 0 fail, exit 0.
- §6 matrix: O1..O7 all PASS with predicate-computed outcomes (POST_MEASUREMENTS.json).
- §7: S7a LAYOUT_ATTEMPTS=126, LAYOUTS_ADMITTED=0 (PRE R1: layoutsTested=0; independently recomputed by two fresh QC contexts); S7b joint XYZ_FINITE_RATE=56/80=0.7 (PRE R1 xyzRate=0.9 stays labeled the legacy per-axis column mean).
- O3: sample 1200/1200 (rate 1.0) vs FULL_CENSUS 4800 rows (ID rate 0.25) — the sample never impersonates the table.
- §8 budgets: B1..B7 + CX1..CX4 all PASS. LAYOUT_ATTEMPTS charged (not LAYOUTS_ADMITTED); reservation before read with verified size; refund on decode failure; ceilings never raisable (B6); RETAINED_CANDIDATES enforced on the GLOBAL peak (adversarial QC probes: peak 256/256 at 9 and 20 inputs; caps 4, 10, 12 all respected).
- Budget consumption of the run itself: MAX_FIX_ROUNDS=2 used (AMENDMENT_LOG.md); no invocation approached the canonical ceilings except by deliberate lowered-threshold tests.

## Residual findings (disclosed, NOT fixed — rounds exhausted)
- **R2-5 (P2):** in a multi-entry container whose shared budget is exhausted mid-scan by an earlier payload, only the FIRST subsequent unanalyzed payload gets its admission-level disposition corrected to OVER_BUDGET; later entries of the same container can remain dispositioned SCANNED despite zero analysis (QC measurement: 4 entries, cap 100 → [SCANNED, OVER_BUDGET, SCANNED, SCANNED]). Bounded to the pre-exhaustion skip path; does not affect budget charging or the B3/CX scenarios. Revalidation gate for any future authorized fix: a 4-entry container under a deliberately early-exhausted budget must end with dispositionTotal == declaredEntryCount and no SCANNED for unanalyzed payloads.
- **R2-1 (P3):** an admitted payload skipped due to earlier budget exhaustion keeps its SCANNED_BYTES/SYNTHETIC_INPUTS admission charged (no refund) — now documented as admission-time accounting (AMENDMENT_LOG, BUDGET_ACCOUNTING).
- **R2-2 (P3):** bounded transient copy overlaps (ranked candidate list vs emitted row copies; csvRows materialization) exist outside the tracked retained-candidate peak; worst case bounded by cap+top.
- **R2-3 (P3):** budget.test B5's two-input case degenerates (the second input is never opened at cap 4); the two-input property is still proven by the QC adversarial probes (9/20-input peak 256).
- **R2-4 (P3):** containerReadBytes accounts input-file sizes at admission-check time, including raw inputs refused before their read; the refused payload itself is never read (B2: scannedBytes=2576 only).
- **R2-6 (P3):** resolved — AMENDMENT_LOG draft inconsistencies corrected before publication (Rounds used: 2; stale ROUND 2 placeholder superseded note; QC path corrected).

## Standing science (unchanged, PROHIBITED_IN_THIS_RUN to change)
MODEL_218757_TO_CMO_JOIN = NOT_ESTABLISHED; WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED; HISTORICAL_PLACEMENT = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO; CANONICAL_GATE_EFFECT = NONE. J3 preserved (PHYSICAL_TRANSFORM_MEASUREMENTS=PRESERVED; SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN=NOT_QUALIFIED_BY_ORIGINAL_SCOPE). The 4057→218757 relation stays definition/resource, not world instance. 0xA4 not a confirmed instance stream; 24007.vfs not a confirmed world-anchor source; FUN_00567770 not an established placement builder. Historical PCG Models.bnt inventory (5596 <id>.nif incl. 218757.nif, earlier measurement) preserved, not re-opened. Era discipline: PCG_9_3_5 vs CD_2003 vs JUL_2003 vs EU_RUNTIME kept separate; synthetic IDs in this run belong to NO era.

## Terminal state
- EXTERNAL_DESKTOP_POST_AUDIT = PENDING (fresh internal QC + round-2 re-QC are internal to this run, not independent Desktop post-audits).
- NEXT_EXPERIMENT_AUTHORIZED = NO. NEXT_MILESTONE_AUTHORIZED = NO. PILOT_SCAN = AWAITING_HUMAN_AUTHORIZATION. HARD_STOP = YES after publication.