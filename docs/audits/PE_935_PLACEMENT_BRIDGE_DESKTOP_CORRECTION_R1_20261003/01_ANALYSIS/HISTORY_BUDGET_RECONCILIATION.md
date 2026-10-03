# HISTORY BUDGET RECONCILIATION — F-D4 (HONEST PROCESS RECORD, NOT A HISTORY REPAIR)

```text
RUN_ID = PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003
FINDING = F-D4 (ORIGINAL SEVERITY P2)
PURPOSE = honest process record + retraction of any full-conformance claim + preservation of NOT_ESTABLISHED
RULE = no retroactive PASS; no invented denominators; no fake measurements
HISTORICAL PACKAGE (READ-ONLY INPUT) = docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/
```

## 1. Historical preregistered executor budgets — PRESERVED verbatim

Source location: historical `00_CONTROL/RUN_PLAN.md`, section "## Budget (fixed BEFORE analysis; NOT expandable after results)", lines 28-32. Verbatim:

```text
- ENUMERATION budget (census + shortlist + selection): max 30 tool invocations
- DEEP_TRACE budget (re-pins + new traces + Ghidra rounds): max 90 tool invocations
- CONTROLS + ORACLE budget: max 30 tool invocations
```

Preserved status strings:

```text
EXECUTOR_ENUM_BUDGET = PREREGISTERED_MAX_30
EXECUTOR_DEEP_TRACE_BUDGET = PREREGISTERED_MAX_90
EXECUTOR_CONTROLS_ORACLE_BUDGET = PREREGISTERED_MAX_30
```

Historical hard limits (same source, lines 33-36) also preserved as historical fact: SHORTLIST_FAMILIES_MAX=3, DEEP_TRACE_FAMILIES_MAX=1, ORACLE_MECHANISMS_MAX=3, NEW_PCG_FUNCTIONS_DETAILED_MAX=120, NEW_PHYSICAL_RECORDS_DETAILED_MAX=3, QC_REPAIR_ROUNDS_MAX=1.

## 2. HISTORICAL_QC_BUDGET_PRE_REGISTERED = NOT_ESTABLISHED (package-content observation)

```text
HISTORICAL_QC_BUDGET_PRE_REGISTERED = NOT_ESTABLISHED
```

This value MUST NOT be changed to YES (order §3/§7). It is a PACKAGE-CONTENT OBSERVATION, re-verified by this correction (bounded greps, 2026-10-03): the historical package contains NO preregistered QC budget.

Files checked (existence + budget mentions):
- `00_CONTROL/AUTHORIZATION.md` (2,957 B), `00_CONTROL/PREFLIGHT.md` (3,460 B), `00_CONTROL/RUN_PLAN.md` (4,994 B) — only the executor budgets of section 1 appear (RUN_PLAN.md:28-38; grep 'budget|BUDGET' over 00_Control hits only RUN_PLAN lines 28/30/31/32/38). No QC budget is preregistered anywhere in 00_CONTROL.
- `07_QC/QC_AUDIT_R1.md` — discusses the RUN_PLAN budgets: line 322-324 "Budget: pre-registered in RUN_PLAN.md (ENUM ≤30 / TRACE ≤90 / CONTROLS+ORACLE ≤30) before analysis; declared usage ~14/~27/~10 — QC cannot re-count tool invocations from artifacts (noted as UNVERIFIED, not contradicted)"; line 390 "Budget usage counts (~14/~27/~10): UNVERIFIED (not re-countable from …)". No pre-set QC budget is recorded.
- `07_QC/QC_RECHECK_R1.md` — budget-related mentions are recount-method references only (e.g., lines 51, 67, 392); no pre-set QC budget.

The QC report itself records no pre-set budget → the observation stands: NOT_ESTABLISHED. NEVER write YES.

## 3. Desktop post-audit tool-call census — four values with provenance

Bounded session-store census attempt: performed 2026-10-03, exactly 5 tool calls (the preregistered cap in 00_CONTROL/CORRECTION_BUDGET.md §3.3). Calls spent: (1) AppData\.opencode / AppData\Local\opencode / AppData\Roaming\opencode listing; (2) config + additional standard store locations; (3) store structure inspection; (4) SQLite schema probe (read-only, python 3.12.10); (5) per-session tool-part census (read-only). Store found: `C:\Users\User\.local\share\opencode\opencode.db` (SQLite; read-only URI mode used; never written). The three dispatch-prechecked candidate roots (`C:\Users\User\.opencode` = {agents, agents_removed_backup_2026-09-05, node_modules, skills} — NO storage dir; `C:\Users\User\AppData\Local\opencode` = single config file only; `C:\Users\User\AppData\Roaming\opencode` = single config file only) contain NO per-session records; the actual store was found at `.local\share\opencode` within the same bounded attempt.

### 3.1 executor initial phase = 125

```text
VALUE = 125
SOURCE = the human-relayed independent Desktop post-audit census (order §7 of PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1, delivered 2026-10-03; the Desktop audit session is external to this workspace and its per-call logs are not on this machine's inspected stores)
SESSION_ID / SOURCE_IDENTIFIER = ses_eff63660cffeJE8ariHPxOW4KQ ("Execute bounded placement bridge run (@pe-reconstruction subagent)", created 2026-10-03T07:13:45Z, directory D:/TESTAI, parent session ses_eff65ce0dffehQR2H4VAoaJOIv "Eksperyment PE_935 Placement Record Bridge")
COUNT_SCOPE = the initial-phase portion of the executor session (up to the repair-round boundary; the boundary attribution is the Desktop census's, not recorded in any artifact)
COUNTING_METHOD = the Desktop post-audit's own per-call counting (not recorded as a reproducible rule in this workspace)
INDEPENDENTLY_RECOMPUTED = NO (the 125/23 split inside one session is not reconstructable from the store)
PROVENANCE_STATUS = INHERITED_FROM_DESKTOP_POST_AUDIT
SUM_CHECK (machine-verified this correction): the executor session's total tool parts = 148 = 125 + 23 EXACTLY
```

### 3.2 executor repair phase = 23

```text
VALUE = 23
SOURCE = the human-relayed independent Desktop post-audit census (order §7, delivered 2026-10-03; the Desktop audit session is external to this workspace and its per-call logs are not on this machine's inspected stores)
SESSION_ID / SOURCE_IDENTIFIER = ses_eff63660cffeJE8ariHPxOW4KQ (same executor session as 3.1)
COUNT_SCOPE = the repair-round portion of the same executor session (boundary attribution = Desktop census)
COUNTING_METHOD = the Desktop post-audit's own per-call counting (not recorded as a reproducible rule in this workspace)
INDEPENDENTLY_RECOMPUTED = NO (same-session split not reconstructable)
PROVENANCE_STATUS = INHERITED_FROM_DESKTOP_POST_AUDIT
SUM_CHECK (machine-verified this correction): 148 total tool parts = 125 + 23 EXACTLY
```

### 3.3 fresh QC = 109

```text
VALUE = 109
SOURCE = machine recount matches the Desktop census value exactly
SESSION_ID / SOURCE_IDENTIFIER = ses_eff4f9ba2ffe54l7YQDmBq294P ("Fresh internal QC of bridge run (@pe-master-auditor subagent)", created 2026-10-03T07:35:22Z, directory D:/TESTAI, parent ses_eff65ce0dffehQR2H4VAoaJOIv)
COUNT_SCOPE = all tool parts of that QC session (316 parts total; 109 with data JSON type="tool")
COUNTING_METHOD = machine count of part rows with data JSON type='tool' per session_id in C:\Users\User\.local\share\opencode\opencode.db (SQLite read-only URI mode; python 3.12.10 sqlite3; measured 2026-10-03T09:24:40Z)
INDEPENDENTLY_RECOMPUTED = YES (109 — exact match with the inherited Desktop value)
PROVENANCE_STATUS = RECOMPUTED_FROM_LOCAL_SESSION_STORE (matches the Desktop census value exactly)
```

### 3.4 focused re-QC = 69

```text
VALUE = 69
SOURCE = machine recount matches the Desktop census value exactly
SESSION_ID / SOURCE_IDENTIFIER = ses_eff40a7ffffex6TtoVQEAWrKmX ("Focused re-QC of repair round (@pe-master-auditor subagent)", created 2026-10-03T07:51:42Z, directory D:/TESTAI, parent ses_eff65ce0dffehQR2H4VAoaJOIv)
COUNT_SCOPE = all tool parts of that re-QC session (224 parts total; 69 with data JSON type="tool")
COUNTING_METHOD = machine count of part rows with data JSON type='tool' per session_id (same method as 3.3; measured 2026-10-03T09:24:40Z)
INDEPENDENTLY_RECOMPUTED = YES (69 — exact match with the inherited Desktop value)
PROVENANCE_STATUS = RECOMPUTED_FROM_LOCAL_SESSION_STORE (matches the Desktop census value exactly)
```

Honest completeness note: two further child sessions of the same historical parent were identified and are NOT part of the four census values: `ses_eff335334ffekauyuLGpNeRUxP` ("Persist verdict, commit and push", 2026-10-03T08:06:16Z, 55 tool parts) and `ses_eff20857cffeai93HfqGMdWPT8` ("Restore EU935 NIF viewer service", 2026-10-03T08:26:48Z, 112 tool parts). No census value is asserted for them.

Counting-rule observation: the store's per-session tool-part count (one part row per tool invocation, type='tool') exactly reproduces the two independently-recomputable Desktop values (109, 69) and the executor sum (148 = 125+23), so the Desktop counting unit is confirmed to be equivalent to tool invocations for these sessions. The 125/23 phase SPLIT remains inherited (its boundary is not marked in the store).

## 4. Earlier declarations inventory

### 4.1 "~41 analytical invocations"

- WHERE WRITTEN: historical `02_ANALYSIS/NOT_CHECKED.md`, section "## Budget consumption (fixed at 00_CONTROL/RUN_PLAN.md)", lines 57-59: "Enumeration + census + trace + controls + oracle: ~41 analytical tool invocations total (2 identity/preflight, 1 C1, 9 Ghidra rounds C2-C9+C11, 4 python instruments C10/C10v2/C12 + array probe, remainder reads of this run's own artifacts)."
- WHAT IT CLAIMED TO COUNT: total "analytical" tool invocations of the historical run, with a partial decomposition (2 identity/preflight + 1 C1 + 9 Ghidra rounds + 4 python instruments + array probe + "remainder reads of this run's own artifacts").
- REPRODUCIBLE COUNTING RULE: NO — a "~" approximation with no per-call ledger and no defined boundary of "analytical" vs non-analytical calls.
- HISTORICAL QC'S OWN VERDICT: QC_AUDIT_R1.md:323-324 "QC cannot re-count tool invocations from artifacts (noted as UNVERIFIED, not contradicted)"; QC_AUDIT_R1.md:390 "UNVERIFIED".
- RECONCILES WITH STORE CENSUS: NO — different counting units (the executor session's store total is 148 tool parts of ALL kinds; "~41 analytical" excludes/blurrs non-analytical calls by its own ambiguous decomposition; the Desktop per-phase census (125+23) counts the same session differently). No exact reconciliation is possible.
- STATUS = UNVERIFIED / NON_RECONSTRUCTABLE

### 4.2 "~14 / ~27 / ~10"

- WHERE WRITTEN: historical `02_ANALYSIS/NOT_CHECKED.md` lines 60-61: "Budgets: ENUMERATION ≤30 (used ~14 before selection), DEEP_TRACE ≤90 (used ~27), CONTROLS+ORACLE ≤30 (used ~10)." and historical `06_REPORT/DRAFT_FINAL_REPORT.md` lines 55-56: "BUDGET_SET = ENUM ≤30 / TRACE ≤90 / CONTROLS+ORACLE ≤30 tool invocations" / "BUDGET_REACHED = NO (used ~14/~27/~10; no budget expansion after results)".
- WHAT THEY CLAIMED TO COUNT: tool invocations per budget phase (ENUM / DEEP_TRACE / CONTROLS+ORACLE), self-declared approximations.
- REPRODUCIBLE COUNTING RULE: NO — "~" estimates with no per-call ledger and no rule assigning each tool call to a phase.
- HISTORICAL QC'S OWN VERDICT: QC_AUDIT_R1.md:323-324 and :390 — cannot be re-counted from artifacts; UNVERIFIED.
- RECONCILES WITH STORE CENSUS: NO — the store has no phase attribution at all (the phase split exists only in these declarations).
- ARITHMETIC TENSION (recorded honestly, NO resolution invented): the declared per-phase sum ~14 + ~27 + ~10 ≈ ~51 coexists with the declared total "~41 analytical tool invocations" in the SAME historical section (NOT_CHECKED.md:57-61). These are approximations without a counting rule; the discrepancy is recorded as-is. Do NOT invent a denominator or a resolution after the fact.
- STATUS = UNVERIFIED / NON_RECONSTRUCTABLE

## 5. Why a total tool-call count alone proves nothing about phase limits

A session's TOTAL tool-call count alone CANNOT establish any of:

```text
ENUM > 30
DEEP_TRACE > 90
CONTROLS+ORACLE > 30
```

because NO historical rule assigned every tool call to those phases (order §7). Concretely: the executor session's machine-verified total of 148 tool parts spans all of its work (enumeration, tracing, controls, oracle, artifact reads/writes, reporting) with no recorded phase ledger; the "~14/~27/~10" split is precisely the non-reconstructable claim that would be needed. The fresh-QC and focused-re-QC sessions had NO preregistered budget at all (section 2: NOT_ESTABLISHED), so no limit breach is demonstrable for them either.

## 6. REQUIRED FINAL STATUS BLOCK (exact strings)

```text
HISTORICAL_QC_BUDGET_PRE_REGISTERED = NOT_ESTABLISHED
HISTORICAL_TOOL_CALL_CENSUS = MEASURED_OR_INHERITED_PER_PHASE_WITH_PROVENANCE
HARD_HISTORICAL_PHASE_LIMIT_BREACH = NOT_DEMONSTRATED
FULL_HISTORICAL_BUDGET_CONFORMANCE = NOT_PROVEN
```

## 7. F-D4 closure (never a retroactive PASS)

```text
F-D4 = CORRECTED_BY_HONEST_PROCESS_RECORD
```

Closure = honest process record (this file) + retraction of any full-conformance claim + preservation of NOT_ESTABLISHED. The new correction-cycle budgets (00_CONTROL/CORRECTION_BUDGET.md, written BEFORE any correction work) do NOT retroactively establish HISTORICAL_QC_BUDGET_PRE_REGISTERED = YES; the historical state remains a separate finding. This file changes no historical byte and asserts no retroactive PASS.
