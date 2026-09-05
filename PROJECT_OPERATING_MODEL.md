# PE / EUDORIA RECONSTRUCTION — PROJECT OPERATING MODEL (TWO-TIER EXTERNAL, PE-MASTER INSIDE)

**Status:** ADOPTED (2026-09-06, human directives a-d; supersedes the
three-tier browser-audit model — the browser ChatGPT tier is REMOVED from
the mandatory loop and redefined by the architect review (d) as OPTIONAL
CONSULTATION / BACKUP ARCHITECT, out-of-band, on demand only)
**Complements:** `CHATGPT_ARCHITECT_INSTRUCTIONS.md` (still binding)
**Refines:** the OPENCODE -> GITHUB -> EXTERNAL AUDIT CONTRACT (evidence,
provenance, hygiene, no-original-payload rules UNCHANGED and binding).
**Agent charters:** `pe-master.md` (the auditor) and `pe-master-auditor.md`
(the execution orchestrator) in `.opencode/agents/`.

---

## 1. PARTIES AND COMPETENCES

| Party | Role | Cadence |
|---|---|---|
| **HUMAN** | Strategic decisions, milestone authorization, relay to Desktop, FINAL closure (`MILESTONE_CLOSED` / `NEXT_MILESTONE_AUTHORIZED`), `EARLY_DESKTOP_ESCALATION` | always |
| **PE-MASTER** (OpenCode agent, GLM 5.3 max, ChatGPT-Desktop-calibrated DEEP auditor, read-only, no subagents) | INDEPENDENT deep adversarial run-level auditor: audits every completed run COMPLETELY — reads every code file the run touched (full commit-range diff), every evidence file it analyzed, cross-compares against the prior canonical record, checks consistency and errors at line level, verifies physical provenance (file identities, SHAs, target bytes); verdicts; designs the next experiment; pre-checks the milestone gate package; verifies Desktop findings and orders corrections. Never executes. Coverage honesty mandatory (states what was NOT checked). | every significant run (launched by pe-master-auditor via Task, or directly by the human) |
| **pe-master-auditor + pe-reconstruction** (execution team) | ALL execution: forensics, Ghidra, RE, scripts, experiments, implementation, tests, regression; the auto loop; internal pre-push QC; commits + pushes; package writing; `AUDIT_ENTRYPOINT.md` maintenance; persists PE-MASTER verdicts; implements ordered corrections | continuous inside the milestone |
| **ChatGPT Desktop** | MILESTONE-LEVEL deep auditor (cross-engine independent check; reads `D:\Eudoria_Reconstruction` physical evidence + GitHub): full milestone post-audit, focused revalidation, designs the next milestone charter; recommendations get implemented and verified by PE-MASTER | milestone ends only (token-expensive by design) |
| **ChatGPT (browser)** | OPTIONAL CONSULTATION / BACKUP ARCHITECT — out-of-band second opinion: suspicious PE-MASTER behavior, a second verdict, GLM loop detection, comparing two audits, Desktop token exhaustion, governance design. NOT a mandatory gate in any loop. | on demand only |

**Deliberate trade-off (recorded):** run-level auditing moved from the
browser ChatGPT (different engine) to PE-MASTER (same engine family as the
executors). Mitigations: PE-MASTER audits from raw artifacts in a fresh
context, its charter mandates extra adversarial discipline against
same-engine error classes, and the cross-engine independence check is
PRESERVED at the milestone gate by ChatGPT Desktop. One human decision can
restore the browser tier at any time.

## 2. THE FLOW

```text
                 HUMAN
                    |
        authorize milestone / trigger loop / close milestone
                    v
   pe-master-auditor (orchestrator) + pe-reconstruction (worker)
        continuous bounded runs inside the milestone
                    |  every significant run: package + commit + PUSH
                    v
        SebastianKozlo/eudoria-clean  (full audit trail)
                    |
                    v
        PE-MASTER — per-run adversarial audit
        (raw evidence on disk + repo; verdict + next experiment)
                    |
        verdict -> ordered work -> back to the execution team
                    |
   ... runs repeat until PE-MASTER honestly states
       MILESTONE_CANDIDATE_FOR_DEEP_AUDIT ...
                    v
        MILESTONE GATE: execution team builds the complete gate
        package + FULL_MILESTONE_AUDIT -> PUSH -> HARD STOP
                    v
        HUMAN relays to CHATGPT DESKTOP (rare, token-expensive)
        deep milestone post-audit: every claim, every line, local
        physical evidence -> recommendations
                    v
        PE-MASTER verifies each finding -> orders correction runs
        -> execution team fixes -> PE-MASTER re-checks
        -> Desktop FOCUSED re-audit -> PASS -> HUMAN closes Mx
                    v
        DESKTOP designs Mx+1 charter (from full local context)
        -> execution resumes under PE-MASTER audits
```

## 3. RUN LIFECYCLE

1. **Direction**: PE-MASTER sets the P0 direction (its last
   NEXT_EXPERIMENT / ORDERED_WORK; a Desktop charter when the human
   relays one). One main P0 question per significant run.
2. **Formalization**: pe-master-auditor converts the direction into an
   executable `NEXT_PROMPT.md` (RUN_ID, exact paths, PASS/FAIL gates,
   hard-stops, denominators, forbidden-to-modify list, handoff block).
   `CHARTER_BLOCKED` allowed for provenance/safety/frozen-baseline
   violations — never silent "improvement".
3. **Execution**: pe-reconstruction works inside the bounded scope.
4. **Internal pre-push QC**: pe-master-auditor checks report vs raw
   evidence, package completeness, JSON validity, regressions.
5. **Push**: code/scripts + REPORT + HANDOFF + GATES + evidence index +
   commit + push (original payloads NEVER; identity metadata only).
6. **Per-run audit**: pe-master-auditor launches PE-MASTER via the Task
   tool (or the human talks to PE-MASTER directly). PE-MASTER audits from
   disk + repo, issues the verdict + corrected checkpoint fragment + the
   next experiment design + ORDERED_WORK.
7. **Persistence**: pe-master-auditor saves the PE-MASTER verdict as
   `PE_MASTER_REVIEW.md` under `docs/audits/<RUN_ID>/`, commits + pushes.
8. **Act**: implement ORDERED_WORK as the next bounded run (fix, revalidate,
   or proceed). DEPENDENCY_GATE per section 5.

## 4. VERDICT LEVELS — MANDATORY EXACT STRINGS

**Level 1 — RUN (PE-MASTER):**
`MASTER_ACCEPTED` | `MASTER_PARTIAL_PASS` | `MASTER_REJECTED` |
`MASTER_REVALIDATION_REQUIRED`

**Level 2 — MILESTONE READINESS (PE-MASTER):**
`MILESTONE_CANDIDATE_FOR_DEEP_AUDIT` — NOT a PASS; never closes anything.

**Level 3 — DEEP AUDIT (ChatGPT Desktop):**
`MILESTONE_POST_AUDIT_PASS` | `MILESTONE_POST_AUDIT_PARTIAL` |
`MILESTONE_POST_AUDIT_REJECTED` (+ recommendations)

**Level 4 — FINAL (human only):**
`MILESTONE_CLOSED` | `NEXT_MILESTONE_AUTHORIZED`

**Never conflated with:** internal stage verdicts and the evidence taxonomy
(`CONFIRMED`/`STRONGLY_SUPPORTED`/`PLAUSIBLE`/`UNVERIFIED`/`REJECTED`),
which stay unchanged inside the audit layer.

## 5. LOOP SEMANTICS + DEPENDENCY_GATE (default ON)

- The auto loop runs continuously inside the authorized milestone; every
  significant run ends with push + handoff + `AUDIT_ENTRYPOINT.md` update.
- The per-run PE-MASTER audit is launched by pe-master-auditor WITHOUT
  human relay (async from the human's perspective; the human can read
  `PE_MASTER_REVIEW.md` files anytime).
- **DEPENDENCY_GATE**: when a run's conclusions are LOAD-BEARING for
  subsequent runs (new semantic role / format-field meaning / era-canon
  change / rewrite of a claim cited by 2+ other runs), the loop marks the
  run `GATED_PENDING_PE_MASTER_VERDICT` and does NOT build on its
  conclusions until PE-MASTER issues the verdict. While gated and no human
  is present, the loop switches to independent backlog work instead of
  stopping. (With PE-MASTER internal this gate is fast — use it liberally.)
- PE-MASTER's verdict may authorize bounded chained fixes in one execution.
- The **milestone gate remains the HARD STOP**: Desktop deep audit happens
  there; the loop never authorizes the next milestone.

## 6. CORRECTION CYCLE AFTER A DESKTOP PARTIAL/REJECTED

```text
Desktop deep audit (findings A/B/C) -> saved in full as
FULL_EXTERNAL_MILESTONE_POST_AUDIT.md (committed by pe-master-auditor)
   -> PE-MASTER verifies each finding against evidence INDEPENDENTLY
      (never blindly executing Desktop's recommendations — Desktop can
      also be wrong); classifies every finding:
      ACCEPTED_FINDING / PARTIALLY_ACCEPTED / REJECTED_WITH_EVIDENCE
   -> PE-MASTER orders correction runs (bounded, one finding class each)
   -> execution team fixes + pushes; PE-MASTER audits each fix
   -> ... until every finding is FIXED / REVALIDATED / honestly
      BLOCKED-UNKNOWN
   -> PE-MASTER declares ready -> Desktop FOCUSED revalidation
   -> MILESTONE_POST_AUDIT_PASS -> human: MILESTONE_CLOSED
```

Desktop is NOT summoned per fix; only at revalidation points.
`EARLY_DESKTOP_ESCALATION` (exception): on a mid-milestone foundational
contradiction the human may summon Desktop early; it rules on that
contradiction only.

## 7. MILESTONE CYCLE (OFFICIAL MODEL)

```text
DESKTOP defines direction / Mx charter (or human + PE-MASTER for the first)
   -> HUMAN AUTHORIZE
   -> execution team runs (bounded runs, pushes)
   -> PE-MASTER audits every run (disk + repo)
   -> fix / next run ... repeat
   -> PE-MASTER: MILESTONE_CANDIDATE_FOR_DEEP_AUDIT
   -> execution team: FULL_MILESTONE_AUDIT + complete gate package
      + PUSH + HARD STOP
   -> HUMAN relays to DESKTOP deep post-audit
   -> PASS  -> human closes Mx
     PARTIAL -> section 6 cycle
   -> DESKTOP designs Mx+1 charter -> browser-free resume
```

## 8. WHAT GETS PERSISTED IN THE REPO

**Every significant run:** code/scripts (if changed) + REPORT.md +
HANDOFF.md + GATES + evidence index + provenance/SHAs + denominators +
unresolved/rejected/superseded claims. Local-only originals = identity
metadata (era, path, size, SHA256, reproduction method) — payloads never.

**Every PE-MASTER run audit:** `PE_MASTER_REVIEW.md` under
`docs/audits/<RUN_ID>/` (committed by pe-master-auditor).

**Every Desktop milestone audit:** ALWAYS in full:
`FULL_EXTERNAL_MILESTONE_POST_AUDIT.md` + its correction prompt.

**Every significant run end:** `AUDIT_ENTRYPOINT.md` updated
(current milestone/gate state, latest runs + SHAs + package paths, pending
verdicts, open P0s).

## 9. HONESTY RULES (COMPETENCE SEPARATION)

PE-MASTER reads BOTH the repo AND `D:\Eudoria_Reconstruction` (raw evidence
trees, Ghidra projects, sandboxes) — its run-level audit is therefore
STRONGER than the removed browser tier (which saw repo-only). PE-MASTER's
audit depth is COMPLETE within the run's scope: every touched code file,
every analyzed evidence file, prior-canon cross-comparison, line-level
machine-readable validation (JSONL line-parse, CSV schema vs generator,
SHA re-hash), file-identity verification by metadata, and target-address/
byte verification for runtime claims. PE-MASTER still must never claim
verification of bytes it did not read — its verdict carries an explicit
COVERAGE section (checked fully / census-level / NOT checked). ChatGPT
Desktop owns the milestone-end physical revalidation + the cross-engine
check.

## 10. STATE AT ADOPTION (2026-09-06, from disk evidence)

- **M1 (PE_WORLD_SURFACE_FIDELITY_R1)** is HARD-STOPPED at the gate.
  V1 gate verdict REJECTED by the human (byte-proven FLOAT64 operand
  misread, decisions-ledger ENTRY #10); correction series done (ledger
  ITER_035/036/037); V2 rejudgment = `PARTIAL_PASS_CORRECTED` PROPOSED —
  the human + external review DECIDE. Nothing authorizes M2.
- **OPEN ITEM — the M1 gate remote audit package (ITER_052 / ledger
  ITER_038) is INCOMPLETE and UNTRACKED**: five files promised by its
  `GATE_INDEX.md` were never built (verified missing in both the repo
  copy and the local canonical audit tree): `EVIDENCE_MANIFEST.json`,
  `RETRACTIONS.md`, `UNRESOLVED.md`, `ROADMAP_MAPPING.md`, `HANDOFF.md`.
  The packaging session was interrupted. **The bounded completion run
  (consolidation from existing records only — no new forensics, no new
  claims) is pending human authorization and is the FIRST RUN under this
  operating model.** Under the new model PE-MASTER pre-checks that
  package before it goes to Desktop.
- Before this adoption, several completed runs (iter35/36/37, NIF
  claim-evidence lock R1/R2) have NO independent PE-MASTER review yet;
  PE-MASTER may audit them retroactively when the human requests.

## 11. OPEN DECISIONS (PENDING THE HUMAN)

1. ~~Browser tier~~ — REMOVED from the mandatory loop (human directive
   2026-09-06; redefined as OPTIONAL CONSULTATION / BACKUP ARCHITECT,
   section 1).
2. Authorize the M1 gate package completion run (bounded, mechanical
   consolidation; the first run executed + PE-MASTER-audited under this
   operating model — after the qualification benchmark Q1).
3. DEPENDENCY_GATE default stays ON (now keyed to fast internal
   PE-MASTER verdicts).

## 12. PE-MASTER QUALIFICATION GATE (before canonical authority)

PE-MASTER_STATUS = PROVISIONAL_UNTIL_QUALIFIED. The agent exists with the
full deep-audit charter, but is NOT the canonical run auditor (its
verdicts are not gates, its ORDERED_WORK is not binding) until it passes
the historical benchmark:

1. **BENCHMARK Q1**: PE-MASTER deep-audits the historical WP1 MODE3
   runtime run
   (`D:\Eudoria_Reconstruction\99_Audits\PE_WORLD_WP1_PLACEMENT_BRIDGE_20260831_220000\`
   + the R47G sandbox
   `D:\Eudoria_Reconstruction\99_Audits\PE_R47G_D3D_WORLD_RUNTIME_20260901_000000\01_SANDBOX\`),
   given ONLY the executor's report + raw evidence paths — NO list of
   known errors. It must find the traps on its own, from the artifacts.
2. **SCORING** (human-graded; the trap list is held OUT of PE-MASTER's
   context): >=5/6 known traps + no fabricated findings + correct
   verdict strings + honest COVERAGE = PASS. Otherwise: profile
   correction and re-test on a second historical run.
3. **On PASS**: PE-MASTER_STATUS = QUALIFIED -> canonical run auditor;
   the per-run Task launches begin. The qualification record is
   committed as `PE_MASTER_QUALIFICATION_Q1.md` under `docs/audits/`.
4. **SKILLS**: pe-master-* skills are built ONLY from CONFIRMED lessons
   (run -> PE-MASTER finding -> correction -> revalidation -> LESSON
   CONFIRMED -> skill update — never from an unverified error, which
   would make a mistake a permanent bias). Target set, built gradually:
   pe-master-forensic-method, pe-master-claim-audit,
   pe-master-evidence-provenance, pe-master-x86-ghidra-review,
   pe-master-runtime-hook-audit, pe-master-binary-format-audit,
   pe-master-rendering-d3d-review, pe-master-nif-review,
   pe-master-terrain-review, pe-master-network-review,
   pe-master-counterexample-design, pe-master-blast-radius,
   pe-master-milestone-gate-review.
