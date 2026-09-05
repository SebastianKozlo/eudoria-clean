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
| Milestone state | **RE-JUDGMENT ACCEPTED (2026-09-05, PE-MASTER relayed by the human; basis = the byte-stable `3491d79` package): `CORRECTION_DELIVERY_ACCEPTED` — M1 = `MILESTONE_CANDIDATE_FOR_DEEP_AUDIT`.** The V4.1 gate package (the V4 matrix `003056AC`/`EC04FC47` + the manifest `9944925D`) is the ACCEPTED deliverable; the historical chain (V1 REJECTED -> the correction series -> V2 -> the external DIRECT -> the repair -> V3 FROZEN -> V4 -> V4.1, double-verified by two PE-MASTER sessions + the pre-relay check PASS) is complete. THE LOOP HAS RESUMED on the M1 execution queue (the P0 order: x87 CW -> witness matrix + scrambled-texture falsification -> georef/P-DATUM -> P-CELLSTREAM/P-CLIMATE); the closure hard gate A/B/C/D (PROJECT_OPERATING_MODEL §13) governs the endgame; the Desktop deep audit is MANDATORY before the human's closure decision. Nothing authorizes M2. |
| IMMEDIATE BLOCKER | **RE-JUDGMENT ACCEPTED (2026-09-05, PE-MASTER relayed by the human; basis = the byte-stable `3491d79` package): `CORRECTION_DELIVERY_ACCEPTED` — the V4.1 gate package is ACCEPTED; M1 = `MILESTONE_CANDIDATE_FOR_DEEP_AUDIT`.** THE M1 EXECUTION QUEUE IS NOW THE BLOCKER (not the relay): (1) P0-1 x87 CW experiment design (RUN-3, offline prep — the runtime execution awaits the PE-MASTER design review + the human's GO), then the loop calibration (RUN-4); the queue order: x87 CW -> witness matrix + scrambled-texture falsification -> georef/P-DATUM -> P-CELLSTREAM/P-CLIMATE. The closure hard gate A/B/C/D (PROJECT_OPERATING_MODEL §13) governs the endgame; the Desktop deep audit is MANDATORY before the human's closure decision. |
| PE-MASTER status | **PROVISIONAL_UNTIL_QUALIFIED** — the agent exists with the full deep-audit charter, but is NOT the canonical run auditor until it passes benchmark Q1 (a human-graded deep audit of the historical WP1 MODE3 run, with the known-trap list held OUT of its context). Until qualification, PE-MASTER verdicts are advisory, not gates. |
| Open P0s | 1) **The M1 execution queue (the current blocker)**: P0-1 x87 CW experiment design (RUN-3 offline prep — the execution gated on the PE-MASTER design review + the human's GO), then the loop calibration (RUN-4); then witness matrix + scrambled-texture falsification -> georef/P-DATUM -> P-CELLSTREAM/P-CLIMATE. 2) The PE-MASTER qualification Q1 (human-graded). 3) The open M1 items — exported in the package `UNRESOLVED.md`: 27 known-open + 5 honest limits + the 7-item V3 open set (consumed by the queue above). |

## LATEST RUNS (newest first — work runs; governance commits excluded from the audit queue)

| Commit | RUN_ID / ITER | Package path (docs/audits/) | One-line purpose | PE-MASTER verdict |
|---|---|---|---|---|
| `2653662` | PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528 | `PE_M1_GATE_V4_1_REGISTRY_RESIDUAL_R1_20260905_110528/` + the live gate files | The bounded registry-residual fix (the R2 post-audit P1): the P-RNG-DIV/P-POS-SCALE missing/why composed per the byte-locks; the extended full-document semantic gate (N1-N6 fail-closed-proven + the PE-MASTER poisoning counter-check); the manifest rebuilt; the 100% final payload scan | MASTER_ACCEPTED (advisory) — **double-verified: the parallel PE-MASTER session's independent QC CONCURS (persisted as `PE_MASTER_CONCURRENCE.md`, incl. the cross-session PC24 103,073 + byte-lock confirmations)**; package READY for the external re-judgment |
| `6ca508c` | PE_M1_GATE_V4_CORRECTION_R2_20260905_101327 (R1 = `PE_M1_GATE_V4_CORRECTION_R1_20260905_100405`, BLOCKED on a prompt pin typo — preserved) | `PE_M1_GATE_V4_CORRECTION_R2_20260905_101327/` + the live gate files | The V4 correction per the external 12-point mandate (PE-MASTER-refined): the 19x9-field matrix in both formats; the six old gaps composed; the no-copy set; the semantic gate N1-N5; the counter split 443,141+20,000=463,141; the PC24 synthetic re-measurement 103,073/1,245,184 (TRIPLE-confirmed) | MASTER_PARTIAL_PASS (advisory; one P1 registry residual -> closed by V4.1) |
| `b34dd76` | PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816 | `PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/` (the completed gate package; the run's own records = local audit tree `D:\Eudoria_Reconstruction\99_Audits\PE_M1_GATE_PACKAGE_COMPLETION_R1_20260905_041816\`) | The mechanical M1 gate-package completion: the 5 missing files built from V3 + evidence indexes (19 fully-provenanced claims; zero payloads); V3 matrix copied hash-identical into `GATES\`; 4+1 hygiene correction-notes; fail-closed consistency PASS (226 re-hashes); pushed at `b34dd76` (the parallel-session sweep — byte-verified, see `01_PUSH_RECORD.md`) | MASTER_ACCEPTED (advisory; pre-check PASS — package READY) |
| `d20e15d` | PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203 (ITER-45) | `PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1_20260905_101203/` (incl. committed PE_MASTER_REVIEW.md) | NIF governance-only corrective (MASTER_PARTIAL_PASS follow-up): R3 entry-point row RESTORED with corrected claim status (14 CONFIRMED + 1 REJECTED-as-worded R3C-08); gate-weakness addendum W-1..W-4 code-confirmed (R3 package unmodified 33/33); TARGET_MAP 5 proposals/16 edits with 13/13 old fragments exactly-once machine-verified; P2/P3 wording fixes evidence-bounded; contradiction census 11 occurrences (incl. 2 uncited found); PATH-LIMITED commit with staged-index verification (b34dd76 incident lesson applied) | **MASTER_ACCEPTED** (advisory) — 13/13 claims independently confirmed from disk; PE-MASTER self-audit lesson: ENTRYPOINT_ROW_SURVIVAL control added; HR-R1-1/2 PENDING; HR-R3-3 HOLD (proposals ready: TARGET_MAP + P2/P3-fixed, wording-only, awaiting human consent) |
| `c47fe01` | PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627 (NIF R3) | `PE_NIF_HASH_PRIMITIVE_REVALIDATION_R3_20260905_025627/` (incl. committed PE_MASTER_REVIEW.md) | NIF R2-helper hash-primitive revalidation (EU935-M2 contribution; no advancement). CLAIM STATUS (corrected, superseding the earlier "15 CONFIRMED" summary): **14 CONFIRMED + 1 REJECTED (as worded — R3C-08)**; all 15 dispositions judged. Aggregate physical result unchanged (nine exact-zero; d==crc32(payload) 3,435/5,596 + 3,299/5,426; c==CRC32 11,022/11,022 — independently re-derived from container bytes by the post-review). 3 gate weaknesses documented by addendum (R3G6c empty-vector coverage label; R3G10 partial predicate; implementation-count overstatement); STAGE_ACCEPTANCE_GATES.csv missing from artifact_index (minor). Proposals P1R2-5-R3/P2R2-2-R3/P3R3/P4R3/P5R3 NOT applied — P2/P3 wording fixes + proposal→target map pending | R3 technical package **ACCEPTED**; persistence/materialization **MASTER_PARTIAL_PASS** (b34dd76 mixed-commit incident disclosed; row restored by PE_NIF_R3_PERSISTENCE_AND_TARGETMAP_R1). HR-R3-1 PARTIAL / HR-R3-2 ACCEPTED / HR-R3-3 **HOLD** (no application consent) / HR-R3-4 PASS. Wiki HOLD; M2 blocked |
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
