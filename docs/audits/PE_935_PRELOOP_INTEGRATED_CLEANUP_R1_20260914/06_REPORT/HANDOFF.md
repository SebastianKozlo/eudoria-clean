# HANDOFF — PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914

- RUN_ID: PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914
- BASE_SHA: a7a6c756bc35a5b28220236e9ac649131206aeb3
- OBSERVED_HEAD_SHA (at start AND end, unchanged): a7a6c756bc35a5b28220236e9ac649131206aeb3
- GIT MUTATIONS BY THE EXECUTOR: **NONE** (read-only git; all outputs are new untracked
  files inside docs/audits/PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914/ only)
- SLOT17 BRANCH (read-only verified start == end): tip
  5290e79e0dc469c70605f35c125d7b727f9f7a6b (local + live remote), parent
  3644e5ac9cbf7b5445861e7f5342fb8642741346, worktree clean (porcelain 0 entries).
- PER-WORK-ITEM STATUS:
  - W1 E1 revalidation: **COMPLETE** — historical fn attribution 0x007EAC00 DISPROVEN;
    real fn 0x007EA740; EBP := ARG3 @0x007EA76D; case NONE_PROVEN → **POSSIBLE_ALIAS**.
  - W2 E2 revalidation: **COMPLETE** — historical fn attribution 0x0082DAC0 DISPROVEN;
    real fn 0x0082DA80; EBP := ECX @0x0082DA82; both entry paths = stack-local
    ArkNiTGAReader (vtable 0x00A9189C → .?AVArkNiTGAReader@@) → case B proven →
    **REJECTED_STANDS_SOUND**.
  - W3 classifier rule V2 + tests: **COMPLETE** — negative → POSSIBLE_ALIAS (PASS),
    positive → REJECTED_ALIAS (PASS); raw outputs persisted.
  - W4 census recomputation: **COMPLETE** — derived 3643 = 2/620/3021/0 (TOTAL asserted);
    R3 sidecar DRAFTED inside 02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md §5.
  - W5 AUD-F1..F7: **COMPLETE** — F1 ACCEPTED / F2 ACCEPTED / F3 PARTIALLY_ACCEPTED /
    F4 REJECTED_WITH_EVIDENCE / F5 REJECTED_WITH_EVIDENCE / F6 ACCEPTED / F7 ACCEPTED.
  - W6 GB12 erratum + NiRTTI: **COMPLETE** — raw JSON slots 13-19 re-verified; prose
    defect confirmed; NiRTTI semantic identity UPGRADED to CONFIRMED (bounded probe).
  - W7 F5 disposition: **COMPLETE** — PARKED_UNAUTHORIZED_ATTEMPT; 7/7 hashes unchanged;
    supersession 6/6 consistent + 6/6 subsumed → SUPERSEDED_SCIENTIFICALLY_BY SLOT17 R1.
  - W8 matrix: **COMPLETE** — 15 standing rows preserved; changed rows recorded.
  - W9 package completion: **COMPLETE** — 01_RAW/02_ANALYSIS/03_EVIDENCE populated;
    06_REPORT drafted (G14/G15 PENDING).
- E1_FINAL_CLASS: **POSSIBLE_ALIAS** (case proven: NONE_PROVEN)
- E2_FINAL_CLASS: **REJECTED_ALIAS** (case proven: B, with class corroboration —
  ArkNiTGAReader, stack-local on both entry paths)
- DERIVED_CENSUS_COUNTS: **3643 = 2 PROVEN / 620 POSSIBLE / 3021 REJECTED / 0 UNRESOLVED**
- CLASSIFIER_TEST_RESULTS: negative → POSSIBLE_ALIAS (PASS); positive → REJECTED_ALIAS (PASS)
- F5_SCIENCE_STATUS: **SUPERSEDED_SCIENTIFICALLY_BY
  PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914** (commit
  5290e79e0dc469c70605f35c125d7b727f9f7a6b)
- NiRTTI semantic identity (0x00BA7270 = NiAVObject NiRTTI): **CONFIRMED** (upgraded
  from STRONGLY_SUPPORTED by the bounded probe; 0x00BA7218 = NiNode NiRTTI CONFIRMED;
  pointer value CONFIRMED)
- AUD-F1..F7 one-line dispositions: F1 ACCEPTED (temporal-scope erratum; REMOTE_HEAD_CHRONOLOGY
  UNRESOLVED; no science impact) · F2 ACCEPTED (03_EVIDENCE=16/06_REPORT=4; TOTAL 35) ·
  F3 PARTIALLY_ACCEPTED (5 carried control/locator files; evidence classes regenerated;
  REPORT overstates; no science downgrade) · F4 REJECTED_WITH_EVIDENCE (standard PE32
  optional-header layout confirmed; "+4 shifted" claim wrong) · F5 REJECTED_WITH_EVIDENCE
  (Gb112_eval = Documentation only; NiMain.lib = installed Evaluation SDK path, pins
  match) · F6 ACCEPTED (corrected temporal wording recorded; no verbatim reconstruction) ·
  F7 ACCEPTED (temporal scope; worktree HEAD pin unaffected)
- GATES G0-G12 (executor self-assessment): **ALL PASS** (G8 both REQUIRED classes
  returned; G0-G11 measured independently; G12 stability re-affirmed). G13 in-scope PASS.
  G14/G15: **PENDING** (closed by the fresh QC / PE-MASTER adjudication + persistence
  worker).
- P0/P1 FINDINGS: NONE. P2 FINDING: the LINK30 historical function-attribution layer
  produced non-function VAs for the E1/E2 rows (attribution method exposure on other
  rows UNKNOWN; a census-wide attribution re-derivation is RECOMMENDED for a future
  authorized run). P3: soft timebox exceeded (~70 min); START-record generator-revision
  provenance note (disclosed).
- RUN_STATUS: **PRELOOP_CLEANUP_PROPOSAL_READY** (proposal; awaits fresh QC +
  PE-MASTER adjudication; NOT a milestone closure)
- HARD_STOP_REASON: **NONE**
- REPORT_PATH: docs/audits/PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914/06_REPORT/REPORT.md
- EVIDENCE_PATHS: docs/audits/PE_935_PRELOOP_INTEGRATED_CLEANUP_R1_20260914/01_RAW/ (10
  raw files), 02_ANALYSIS/ (6 documents), 03_EVIDENCE/EVIDENCE_INDEX.csv (+ README.md);
  index inside 03_EVIDENCE/EVIDENCE_INDEX.csv lists every artifact with generator +
  generator SHA256.
- NEXT STEPS (for PE-MASTER): fresh QC (G14) → adjudication → if ACCEPTED, the persistence
  worker performs the cherry-pick of 5290e79 onto current master, applies the R3 sidecar
  draft (02_ANALYSIS/CANONICAL_STATE_RECONCILIATION.md §5) to the LINK30 package,
  commits, pushes, updates AUDIT_ENTRYPOINT and persists PE_MASTER_REVIEW (G15).
