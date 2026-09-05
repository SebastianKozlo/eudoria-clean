# PE / EUDORIA RECONSTRUCTION — PROJECT OPERATING MODEL (THREE-TIER AUDIT)

**Status:** ADOPTED (proposed by the human + browser ChatGPT, 2026-09-05/06)
**Complements:** `CHATGPT_ARCHITECT_INSTRUCTIONS.md` (still binding)
**Refines:** the OPENCODE -> GITHUB -> EXTERNAL AUDIT CONTRACT (run-level cadence,
verdict levels, who-designs-what). The contract's evidence, provenance, hygiene
and no-original-payload rules are UNCHANGED and remain binding on all tiers.
**Supersedes:** the implicit "one external ChatGPT does everything" reading.

---

## 1. PARTIES AND COMPETENCES

| Party | Role | Cadence |
|---|---|---|
| **HUMAN** | Strategic decisions, relay between tiers, FINAL milestone closure (`MILESTONE_CLOSED` / `NEXT_MILESTONE_AUTHORIZED`), may summon Desktop early (`EARLY_DESKTOP_ESCALATION`) on foundational contradictions | always |
| **OpenCode + GLM 5.3 MAX** (`pe-reconstruction` worker + `pe-master-auditor` internal orchestrator) | ALL execution: forensics, Ghidra, RE, scripts, experiments, implementation, tests, evidence, regression; internal adversarial pre-push audit; loop state + ledgers; commits + pushes; emits the EXTERNAL AUDIT HANDOFF block after each significant run | every run |
| **ChatGPT (browser)** | RUN-LEVEL external post-auditor + technical pilot: audits every significant run from LIVE GitHub; issues run verdicts; designs the next run direction; NEVER closes milestones | every significant run |
| **ChatGPT Desktop** | MILESTONE-LEVEL deep auditor: reads `D:\Eudoria_Reconstruction` (original bytes, local evidence, Ghidra artifacts) + GitHub; full milestone deep post-audit; focused revalidation after fixes; designs the next milestone charter | milestone ends only |

## 2. THE FLOW

```text
                 HUMAN
                    |
                    v
        CHATGPT DESKTOP — RARE
     ARCHITECT / DEEP MILESTONE AUDITOR
                    |
         direction / milestone charter
                    v
        CHATGPT IN BROWSER — OFTEN
      RUN AUDITOR / TECHNICAL PILOT
                    |
          correction / next run direction
                    v
          OpenCode + GLM 5.3 MAX
          FORENSICS / RE / CODE
                    |
             commit + PUSH
                    v
        SebastianKozlo/eudoria-clean
                    |
                    +----> back to the browser auditor
```

## 3. RUN LIFECYCLE

1. **Direction**: browser ChatGPT designs the next run direction (or the human
   relays a Desktop charter). One main P0 question per significant run.
2. **Formalization**: OpenCode's master-auditor converts the direction into a
   concrete executable `NEXT_PROMPT.md` (RUN_ID, exact input/output paths,
   PASS/FAIL gates, hard-stop conditions, denominators, forbidden-to-modify
   list, handoff block). The technical INTENT is the browser's; the forensic
   FORM (paths, gates, provenance discipline) is the master-auditor's.
   The master-auditor may return `CHARTER_BLOCKED` with reasons instead of
   executing a direction that would violate frozen baselines, provenance
   rules, or evidence hygiene — never silently "improve" it.
3. **Execution**: `pe-reconstruction` executes inside the bounded run scope
   (internal iterations allowed). Evidence discipline as per the contract.
4. **Internal pre-push audit**: master-auditor checks report vs raw evidence,
   provenance, denominators, overclaims, regressions before the push.
5. **Push**: code/scripts + REPORT.md + HANDOFF.md + GATES + evidence index +
   commit + push (original game payloads NEVER committed; identity metadata
   only).
6. **Handoff**: the OpenCode final chat response ends with the EXTERNAL AUDIT
   HANDOFF block (pasteable by the human directly to the browser auditor).
7. **External run audit**: human pastes the handoff + "zaudytuj". Browser
   walks LIVE GitHub: HEAD -> commit range -> REPORT -> HANDOFF -> GATES ->
   EVIDENCE -> CODE -> dependencies -> blast radius.
8. **Verdict + findings** (see section 4) + the next run direction.
9. **Persistence**: browser verdicts/findings with project impact are saved by
   the NEXT OpenCode session as `EXTERNAL_REVIEW.md` (or referenced in the
   next HANDOFF). Full technical audits with material findings are kept.
10. **Repeat** until the browser can honestly state
    `MILESTONE_CANDIDATE_FOR_DEEP_AUDIT`.

## 4. VERDICT LEVELS — MANDATORY EXACT STRINGS

**Level 1 — RUN (browser ChatGPT):**
`RUN_ACCEPTED` | `RUN_PARTIAL_PASS` | `RUN_REJECTED` | `REVALIDATION_REQUIRED`

**Level 2 — MILESTONE READINESS (browser ChatGPT):**
`MILESTONE_CANDIDATE_FOR_DEEP_AUDIT` — this is NOT a PASS and never closes
anything. Maximum honest wording: "from the run level I no longer see an open
P0; the milestone is a candidate for the full Desktop audit."

**Level 3 — DEEP AUDIT (Desktop ChatGPT):**
`MILESTONE_POST_AUDIT_PASS` | `MILESTONE_POST_AUDIT_PARTIAL` |
`MILESTONE_POST_AUDIT_REJECTED` (+ detailed repair instructions)

**Level 4 — FINAL (human only):**
`MILESTONE_CLOSED` | `NEXT_MILESTONE_AUTHORIZED`

**Never conflated with:** internal stage verdicts
(`PASS`/`PARTIAL_PASS`/`FAIL`/`BLOCKED`) and the evidence taxonomy
(`CONFIRMED`/`STRONGLY_SUPPORTED`/`PLAUSIBLE`/`UNVERIFIED`/`REJECTED`),
which remain unchanged and internal to OpenCode's audit layer.

## 5. AUTO LOOP SEMANTICS (AMENDMENT)

- The unattended AUTO LOOP operates **INSIDE a single bounded RUN charter**
  (as many internal iterations as the run's P0 needs).
- A **significant run boundary is an EXTERNAL GATE**: push + handoff + WAIT
  for the browser verdict. The loop does NOT silently cross it.
- A browser verdict MAY authorize bounded chained fixes inside one next
  execution (e.g. "fix F1..F3, rerun the regression sweep") without a new
  external gate — only when explicitly stated in the verdict.
- The **milestone gate remains the HARD STOP** (unchanged): there the Desktop
  deep audit happens; the loop never authorizes the next milestone.

## 6. CORRECTION CYCLE AFTER A DESKTOP PARTIAL/REJECTED

```text
Desktop deep audit (findings A/B/C)
   -> human relays it to the browser ChatGPT and to OpenCode
   -> OpenCode commits the FULL audit to the repo
   -> OpenCode executes correction runs
   -> browser audits each correction run (run-level, as always)
   -> ... until browser states: all findings FIXED / REVALIDATED
      / honestly still BLOCKED or UNKNOWN
   -> browser: "EU935-Mx is again ready for DESKTOP RE-AUDIT"
   -> Desktop: FOCUSED revalidation (not from zero)
   -> MILESTONE_POST_AUDIT_PASS
   -> human: MILESTONE_CLOSED
```

Desktop is NOT summoned per fix; it returns only at revalidation points.

## 7. MILESTONE CYCLE (OFFICIAL MODEL)

```text
DESKTOP defines direction / Mx charter
   -> HUMAN AUTHORIZE
   -> browser pilots runs (design direction per run)
   -> OpenCode executes + PUSH
   -> browser audits each run
   -> fix / next run ... repeat
   -> MILESTONE_CANDIDATE_FOR_DEEP_AUDIT
   -> OpenCode FULL_MILESTONE_AUDIT + PUSH + HARD STOP
   -> DESKTOP DEEP MILESTONE POST-AUDIT
   -> PASS -> HUMAN CLOSES Mx
            | PARTIAL -> correction cycle (section 6)
   -> DESKTOP designs Mx+1 charter (from full local context)
   -> browser pilots Mx+1
```

`EARLY_DESKTOP_ESCALATION` (exception): if a foundational assumption is
contradicted mid-milestone (the FLOAT32/FLOAT64 class of event), the human
may summon Desktop early. Desktop then rules on the specific contradiction
only — it does not take over run-level piloting.

## 8. WHAT GETS PERSISTED IN THE REPO

**Every significant run:** code/scripts (if changed) + REPORT.md + HANDOFF.md
+ GATES + evidence index + provenance/SHAs + denominators +
unresolved/rejected/superseded claims. Local-only originals are represented by
identity metadata (era, path, size, SHA256, reproduction method) — payloads
never.

**Browser run-level audits:** not the whole chat, but every result with
project impact reaches durable history as `EXTERNAL_REVIEW.md` (committed by
the next OpenCode session), at minimum referenced in the next HANDOFF.

**Desktop audits:** ALWAYS in full:
`FULL_EXTERNAL_MILESTONE_POST_AUDIT.md` + its correction prompt.

Audit-trail location convention: `docs/audits/<RUN_ID>/`.

## 9. HONESTY RULES (COMPETENCE SEPARATION)

The browser auditor checks extremely well: repo, commits, code, reports,
evidence metadata, scripts, denominators, logic, contradictions. But when a
claim depends exclusively on a local-only physical source
(`D:\...\Entropia.exe`, `Models.bnt`, Ghidra database, runtime dumps) that is
not in the repo, the browser does NOT pretend to have verified the bytes. It
labels such claims:

```text
REPO_EVIDENCE = CONSISTENT
PHYSICAL_SOURCE_REVALIDATION = REQUIRED_AT_MILESTONE_AUDIT
```

Desktop owns the physical revalidation at the milestone deep audit.
OpenCode's internal audit and the evidence taxonomy remain the first
line of defense at run level.

## 10. STATE AT ADOPTION (2026-09-05/06, from disk evidence)

- **M1 (PE_WORLD_SURFACE_FIDELITY_R1)** is HARD-STOPPED at the gate.
  V1 gate audit verdict was REJECTED by the human independent audit
  (byte-proven FLOAT64 operand misread, decisions-ledger ENTRY #10);
  the correction series followed (ledger ITER_035/036/037 = the operand
  lock, the float-constant sweep, the original-direct single-model witness);
  V2 rejudgment = `PARTIAL_PASS_CORRECTED` PROPOSED — the human + the
  external review DECIDE. Nothing authorizes Milestone 2.
- **OPEN ITEM — the M1 gate remote audit package (ITER_052 / ledger
  ITER_038) is INCOMPLETE and UNTRACKED**: of the files promised by
  `docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/GATE_INDEX.md`,
  five were never built (neither in the repo copy nor in the local canonical
  audit tree): `EVIDENCE_MANIFEST.json`, `RETRACTIONS.md`,
  `UNRESOLVED.md`, `ROADMAP_MAPPING.md`, `HANDOFF.md`. The packaging
  session was interrupted. The package MUST NOT be pushed in this state;
  a bounded completion run (consolidation FROM EXISTING RECORDS, no new
  forensics, no new claims) is the FIRST RUN under this operating model.
- The committed-and-pushed state of master is otherwise in sync
  (`97ed5e5`).

## 11. OPEN DECISIONS (PENDING THE HUMAN)

1. Confirm the auto-loop amendment (section 5) -> then the pe-master-auditor
   profile is amended + synced (canonical -> runtime, SHA256-verified) and
   OpenCode restarted.
2. Authorize the M1 gate package completion run (bounded, mechanical
   consolidation; the first run piloted under this model).
3. Whether the run direction for that completion run comes from the browser
   ChatGPT (per section 3.1) or is formalized directly by the
   master-auditor (permitted for mechanical completion of an interrupted
   packaging session — no new forensics, no new claims).
