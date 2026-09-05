# AUDIT_ENTRYPOINT.md — THE EXTERNAL AUDITOR'S SINGLE ENTRY FILE

> **MAINTENANCE CONTRACT**: this file is updated by OpenCode's master-auditor
> at the end of EVERY significant run. It must never claim more than the repo
> actually contains. Repo: `SebastianKozlo/eudoria-clean`, branch `master`.
>
> **HOW TO AUDIT (PE-MASTER)**: read this file -> walk the referenced run
> package -> verify every load-bearing claim against the raw artifacts on
> disk (`D:\Eudoria_Reconstruction`) and the repo code/evidence -> issue the
> verdict using the exact strings in `PROJECT_OPERATING_MODEL.md` section 4,
> saved by pe-master-auditor as `PE_MASTER_REVIEW.md`. Do not trust this
> summary over the physical evidence; if they conflict, the evidence wins and
> you report the conflict.

## CURRENT STATE (as of this file's last update)

| Field | Value |
|---|---|
| HEAD | Discover via `git log` (this file cannot self-reference its own commit SHA); the LATEST RUNS table below is authoritative for work runs |
| Current milestone | **EU935-M1 World Surface Fidelity** |
| Milestone state | **HARD_STOPPED_AT_GATE** — V1 gate verdict REJECTED by the human (byte-proven FLOAT64 operand misread, decisions-ledger ENTRY #10); correction series done (ledger ITER_035/036/037); **V2 rejudgment = PARTIAL_PASS_CORRECTED (PROPOSED — the human + external review DECIDE)**. Nothing authorizes M2. |
| IMMEDIATE BLOCKER | **The M1 gate remote audit package (ITER_052 / ledger ITER_038) is INCOMPLETE and UNTRACKED**: of the files promised by its `GATE_INDEX.md`, five were never built — `EVIDENCE_MANIFEST.json`, `RETRACTIONS.md`, `UNRESOLVED.md`, `ROADMAP_MAPPING.md`, `HANDOFF.md` (verified missing in BOTH the repo copy and the local canonical audit tree). The packaging session was interrupted. **A bounded completion run (consolidation from existing records only — no new forensics, no new claims) is pending human authorization.** Until then the M1 gate package is NOT ready for external audit. |
| PE-MASTER status | **PROVISIONAL_UNTIL_QUALIFIED** — the agent exists with the full deep-audit charter, but is NOT the canonical run auditor until it passes benchmark Q1 (a human-graded deep audit of the historical WP1 MODE3 run, with the known-trap list held OUT of its context). Until qualification, PE-MASTER verdicts are advisory, not gates. |
| Open P0s | 1) M1 gate package completion (mechanical). 2) The 27 known-open M1 items + 5 honest limits (to be exported in `UNRESOLVED.md` by the completion run). |

## LATEST RUNS (newest first — work runs; governance commits excluded from the audit queue)

| Commit | RUN_ID / ITER | Package path (docs/audits/) | One-line purpose | PE-MASTER verdict |
|---|---|---|---|---|
| `97ed5e5` | PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054 | `PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/` | NIF claim-evidence correction package (EU935-M2 prep): Areas A-E corrected, 18/18 executable gates PASS | PENDING |
| `c0c2f2f` | PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119 (ITER-41) | `PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119/` | 23/23 external-audit allegations re-derived; CLAIM_MATRIX 43 atomic claims; doc corrections P1-P7 (proposals) | PENDING |
| `c97ed73` | iter37 (ITER-37) | (forensics under local tree; repo carries code+`docs/forensics/iter037-*`) | ORIGINAL-DIRECT single-model witness 457485: model->geometry->material->texture->render from original PCG_9_3_5 bytes, anti-circular vs frozen R61 python oracle (0 mismatches) | PENDING |
| `47f6ab4` | iter36 (ITER-36) | (local audit tree) | Float-constant lock sweep, all chains; FLOAT64/FLOAT32 error class CLOSED milestone-wide; materials_confirmed regenerated (EA4411B5...) | PENDING |
| `b3fe74b` | iter35 (ITER-35) | (local audit tree) | Foliage FLOAT64 operand lock (32767.0/65535.0/1/12800); 76/76 anti-circular RNG revalidation; foliage render superseded (8770AAA0...) | PENDING |
| `8cd0bc3` | iter34 (ITER-34) | (local audit tree) | M1 gate regression sweep record: 5/5 deterministic render hashes reproduce exactly; the 19-row gate matrix deliverable | PENDING |

> Historical runs before this table are reachable via `git log` (English
> commit messages carry the full claims trail) and `docs/forensics/iter0NN-*.md`.

## MILESTONE-GATE EXPECTATIONS (ChatGPT Desktop)

When the human summons Desktop for the M1 deep post-audit, Desktop should
expect: (a) the COMPLETE M1 gate package at
`docs/audits/PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/` (complete ONLY after the
completion run — see blocker above), including the consolidated
`EVIDENCE_MANIFEST.json` with per-claim sources, generators, SHAs,
denominators, why_non_circular, and the identity metadata of LOCAL-ONLY
original sources (era, path, size, SHA256, reproduction method — payloads
never committed); (b) `REPORT_V1_SUPERSEDED.md` vs `REPORT_V2_REJUDGMENT.md`
(the diff IS the correction story); (c) the physical corpora on
`D:\Eudoria_Reconstruction` (Desktop may read them directly). Deep-audit
verdict strings: `MILESTONE_POST_AUDIT_PASS / _PARTIAL / _REJECTED`
(+ repair recommendations, which get implemented and re-audited).

## CANONICAL GOVERNANCE FILES (always-current contracts)

- `PROJECT_OPERATING_MODEL.md` — the three-tier operating model (parties,
  run lifecycle, verdict strings, async loop semantics, DEPENDENCY_GATE,
  persistence + honesty rules).
- `CHATGPT_ARCHITECT_INSTRUCTIONS.md` — the standing instruction set for
  the external architect/post-auditor (evidence hierarchy, anti-success-
  theater, EU935 roadmap, audit style).
- This file — the always-current state pointer.
