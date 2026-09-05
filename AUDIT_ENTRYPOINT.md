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
| Milestone state | **HARD_STOPPED_AT_GATE** — V1 gate verdict REJECTED by the human (ledger ENTRY #10); correction series done; V2 rejudgment = PARTIAL_PASS_CORRECTED (PROPOSED); external V2 audit verdict = DIRECT (do not close M1); the validation-proof repair run PE_M1_VALIDATOR_COVERAGE_REPAIR_R1 executed (all 19 allegations ACCEPTED; post-audit MASTER_ACCEPTED, advisory) with the V3 matrix = the LIVE matrix; **the M1 gate remote audit package is now COMPLETE and PUSHED (`b34dd76`) via PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816: all five GATE_INDEX-promised files built (EVIDENCE_MANIFEST.json with 19 fully-provenanced claims, RETRACTIONS.md, UNRESOLVED.md, ROADMAP_MAPPING.md, HANDOFF.md) + the V3 matrix copies (hash-identical) in `GATES\` with the old copies marked SUPERSEDED-BY-V3 + CORRECTION_NOTES.md; the fail-closed consistency check PASS (226 SHA re-hashes, 0 problems; 24 committed files payload-scanned = zero payloads). Awaiting the PE-MASTER pre-check of the package; the Desktop relay = the human's decision alone.** Nothing authorizes M2. |
| IMMEDIATE BLOCKER | **RESOLVED** (2026-09-05): the M1 gate remote audit package is complete and pushed. Remaining gates before M1 closure: (1) the PE-MASTER pre-check of the completed package (advisory — PROVISIONAL_UNTIL_QUALIFIED); (2) the human's decision on the Desktop relay / M1 closure. One governance note for the auditors: the package's commit attribution — a parallel pe-master-auditor session's commit (`b34dd76`, the NIF-R3 verdict persistence) swept this run's staged files into its own commit before this run's own commit executed; byte-integrity of all 24 package files at HEAD was verified against the run's records (full honest account: the run's `06_REPORT\01_PUSH_RECORD.md`). |
| PE-MASTER status | **PROVISIONAL_UNTIL_QUALIFIED** — the agent exists with the full deep-audit charter, but is NOT the canonical run auditor until it passes benchmark Q1 (a human-graded deep audit of the historical WP1 MODE3 run, with the known-trap list held OUT of its context). Until qualification, PE-MASTER verdicts are advisory, not gates. |
| Open P0s | 1) The PE-MASTER pre-check of the completed M1 gate package (IN FLIGHT). 2) The human's M1-closure decision (the Desktop relay is optional consultation per the 2026-09-06d governance). 3) The open M1 items — exported in the package `UNRESOLVED.md`: 27 known-open + 5 honest limits + the 7-item V3 open set (incl. x87 CW measurement, witness matrix, georef/P-DATUM, patcher grids, cell-content origin, original-client parity). |

## LATEST RUNS (newest first — work runs; governance commits excluded from the audit queue)

| Commit | RUN_ID / ITER | Package path (docs/audits/) | One-line purpose | PE-MASTER verdict |
|---|---|---|---|---|
| `b34dd76` | PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816 | `PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/` (the completed gate package; the run's own records = local audit tree `D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816\`) | The mechanical M1 gate-package completion: the 5 missing files built from V3 + evidence indexes (19 fully-provenanced claims; zero payloads); V3 matrix copied hash-identical into `GATES\`; 4+1 hygiene correction-notes; fail-closed consistency PASS (226 re-hashes); pushed at `b34dd76` (the parallel-session sweep — byte-verified, see `01_PUSH_RECORD.md`) | PENDING (pre-check) |
| `bc2e2df` | PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439 | `PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439/` (repo carries PE_MASTER_REVIEW.md; full run package = local audit tree `D:\Eudoria_Reconstruction\99_Audits\PE_M1_VALIDATOR_COVERAGE_REPAIR_R1_20260905_012439\`) | Validation-proof repair per the external V2 audit (DIRECT): all 19 allegations ACCEPTED; oracle+domain+gates+mapping repaired; V3 matrix = live; run OFFLINE (no own commits) | MASTER_ACCEPTED (advisory) |
| `97ed5e5` | PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054 | `PE_NIF_CLAIM_EVIDENCE_LOCK_R2_20260905_020054/` | NIF claim-evidence correction package (EU935-M2 prep): Areas A-E corrected, 18/18 executable gates PASS | **REVALIDATION_CLOSED-at-run-level** — external post-audit verdict REVALIDATION_REQUIRED fully satisfied by R3 (defects fixed, method claims superseded, physical results retained); R2 helper hash defects corrected in R3; proposals superseded by R3 versions pending human HR-R3-3 |
| `c0c2f2f` | PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119 (ITER-41) | `PE_NIF_CLAIM_EVIDENCE_LOCK_R1_20260904_233119/` | 23/23 external-audit allegations re-derived; CLAIM_MATRIX 43 atomic claims; doc corrections P1-P7 (proposals) | PENDING (retro PE-MASTER audit optional, low priority per R3 review) |
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
