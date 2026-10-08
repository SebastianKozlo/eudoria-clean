# EVIDENCE_INDEX — PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008

Index of every evidence file in the package with its role (which finding /
control it supports). All files are under
`docs/audits/PE_935_CAND4_006C9700_PLUS4_POST_AUDIT_CORRECTION_R1_20261008/`
unless prefixed otherwise. Sizes/SHA256 of every file at final persistence are
in MANIFEST_SHA256.csv (generated LAST; every-write-after-the-manifest rule).

## §1. Executor records + machinery (13 files)

| file | role |
|---|---|
| AUTHORIZATION_RECORD.md | run/contract identity + the real authorization source; records the phase split (executor vs parent persistence phases) and the authorization predicates honored |
| INPUT_IDENTITIES.md | preflight evidence: triple-BASE check (command/timestamp/exit/SHA), foreign untracked census, all 7 pinned inputs SIZE+SHA256, the physical EXE access census (contract §2 classes used and NOT accessed), the READ_ONLY source-package 28/28 blob-identity census, and the REC-W own physical measurement (headers, section table, 5 bytes @0x2CB836) |
| SOURCE_STATE_AND_FINDINGS.md | the complete REC-W occurrence census (A1-A3 contradictory active records; T1-T4 true descriptions; C1-C6 correct records), the five Desktop findings' dispositions, the preserved open findings F-1..F-5, the standing ceilings preserved verbatim, and the write-scope/phase-boundary record |
| ACTIVE_CORRECTED_PINS.json | REC-W: the SINGLE ACTIVE W-ctor record (CALLSITE_VA 0x006CB836; BYTES E8 75 F0 02 00; SIGNED_REL32 +0x2F075; NEXT_VA 0x006CB83B; TARGET_VA 0x006FA8B0; TARGET_FORMULA) with the own physical read basis, the prior-record agreement citation (path + Git blob SHA1 eea2876a… + SHA256 + verbatim quote) and the three superseded contradictory records enumerated |
| HISTORICAL_SCOPE_REASSESSMENT.csv | FD-C1: the callsite-unit floor re-adjudicated from the RECORDED CONTENT — 21 rows (E1..E12 + R-3/R-6/R-7/R-8/R-9 charged + R-1/R-2/R-4/R-5 NOT_ADJUDICATED_FOR_EXACT_COUNT), exact quotes per unit, floor MINIMUM_NEW_ANALYZED_CALLSITE_UNITS = 17, EXACT = UNRESOLVED, EDGE_BUDGET = FAIL |
| BODY_SCOPE_REASSESSMENT.csv | FD-C1 body scope: B-1..B-4 + NB-5 (the 0x006C9820 neighbor DESCRIBED in the RAW pump; NOT read from the EXE this run) — MINIMUM_NEW_FUNCTION_BODIES_OPENED = 5, EXACT = UNRESOLVED, EXCEEDANCE NOT established |
| CORRECTED_CLAIM_MATRIX.csv | FD-C2/FD-C3/name-taking/REC-W/scope: the corrected active claim statuses (T_EQUALS_FIRST_INITIAL_P = NOT_ESTABLISHED_WITHIN_BOUND; R_PLUS4_VALUE_PRESERVED_TO_LATER_USE = NOT_ESTABLISHED; ACTUAL_LATER_OVERWRITE_OBSERVED = NO; P_HEAP_ORIGIN = NOT_ESTABLISHED; P_ALLOCATION_OR_STORAGE_ORIGIN = NOT_ESTABLISHED_WITHIN_BOUND; P_VALUE_SOURCE_AT_FIRST_INIT = FUN_007B79B0_RETURN; P_NAME_TAKING_VIRTUAL_CALL = CONFIRMED_IN_RECORDED_STATIC_SCOPE; LOOKUP_SEMANTIC = UNRESOLVED; preserved core; RESEARCH_GUARDRAILS = GUARDRAILS_ONLY; SCOPE_BUDGET_RECORDS) |
| SUPERSESSION_LEDGER.csv | the 31-row supersession ledger (FD-C1 SL-1..8; FD-C2 SL-9..19; FD-C3 SL-20..24; REC-W SL-25..27; TOOL-MAP SL-28; ACC SL-29/30; STATUS SL-31): exact old claims, corrected active claims, bases, ceilings, dependent-record impact; HISTORICAL_MECHANICAL_PIN_RESULTS = PRESERVED; HISTORICAL_OVERALL_ACCEPTANCE = SUPERSEDED_IN_AFFECTED_SCOPE |
| MAPPER_RESULTS.json | TOOL-MAP: the production mapper controls (MAP1..MAP7, 102/102 case-PASS), the MC1–MC5 exact-anchor mutant results, the MC6 direct-physical-offset control (86/86 anchor gates PASS), the W-record mutation gates (JSON drives the record gates), and the implementation identity (successor + controls script SHA256; EXE identity before/after) |
| REGRESSION_RESULTS.json | TOOL-MAP: the historical 80-ID regression — required ID set (80 unique IDs, read-only AST parse of the historical checker, SHA verified), successor table identity 4/4, clean baseline 80/80 PASS + the RECW record gates on their separate 6-gate denominator; MC1–MC6 summary; regression verdict PASS |
| LOGICAL_CONTROL_RESULTS.json | FD-C2 controls: the synthetic countermodel (first-init P → opaque helper [this-4]:=Q → T=Q≠P) and the field-preserving model (T=P), both with all premises true — LOGICAL_CONTROLS_SCOPE = SYNTHETIC_ONLY; neither resolves the real FUN_006B2310; verdict keeps T_EQUALS_FIRST_INITIAL_P = NOT_ESTABLISHED_WITHIN_BOUND |
| 03_SCRIPTS/checker_plus4_successor.py | TOOL-MAP: the successor checker (the single range-safe read API; classification separated from physical read; RECW record gates validating ACTIVE_CORRECTED_PINS.json against the physical bytes and own arithmetic; the historical 80-check semantics preserved) — production machinery of the correction run |
| 03_SCRIPTS/run_correction_controls.py | TOOL-MAP: the controls driver that executed the 7 mapper control classes, MC1–MC6 and the W-record mutation gates; the implementation whose measured outputs are MAPPER_RESULTS.json / REGRESSION_RESULTS.json |

## §2. Fresh-context internal QC (4 files)

| file | role |
|---|---|
| QC_REPORT.md | QC method/origin disclosure (pe-master-auditor fresh-context internal QC — internal to PE-MASTER; NOT an independent Desktop audit; NOT executor self-review), materials checked, per-duty results (9/9), verdict CORRECTION_RECORDS_QC = PASS, coverage/NOT_CHECKED, the 2 disclosed QC self-tooling fixes, no QC repair round used |
| QC_RESULTS.json | QC machine-readable results: duty2 W-record recheck (own read + own arithmetic); duty3 QCPE independent mapper implementation for all 7 required cases; duty4 production replay (clean 86/86; MC1–MC5 exact anchors; W-record JSON gates); duty5 scope re-adjudication (21 rows, 17=12+5, quotes 12/12+5/5, dedupe); duty6 active-claims sweep (ZERO active T==P/heap/WITHIN; entrypoint pending per SL-16); duty7 both logical models; duty8 zero SCIENCE_PASS; duty9 80-ID regression with own 80/80 re-execution |
| 00_CONTROL_INTERNAL_QC/QC_COUNTERCHECK_RAW.json | the QC's own raw execution records (mapper classes, mutants, logical models, 80-check re-execution) |
| 03_SCRIPTS/qc_countercheck.py | the QC's OWN independent counter-check tool (QCPE range-check/arithmetic implementation, own synthetic PE builder, own AST parse, own 80-check execution, own logical models) — the independence instrument of duty3/duty9 |

## §3. Parent persistence phase (5 files — this phase)

| file | role |
|---|---|
| PE_MASTER_REVIEW.md | PE-MASTER MASTER_AUDIT verdict persisted VERBATIM per the parent dispatch: VERDICT = MASTER_ACCEPTED; AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE; preflight, finding dispositions, preserved core, gate predicates, findings, coverage, HARD_STOP = YES |
| FINAL_REPORT.md | this file — the consolidated correction report (run/contract identity, preflight, the five finding dispositions with measured evidence, preserved core, floor numbers, corrected claim statuses, mapper/MC/regression results, QC origin + PASS, PE-MASTER verdict, supersession summary, open findings, terminal governance) |
| EVIDENCE_INDEX.md | this index (role of every evidence file; Desktop inputs cited with SIZE/SHA) |
| HANDOFF.md | the contract §10 terminal fields filled with the ACTUAL measured values (RESULTING_SHA/REMOTE_SHA recorded at the terminal handoff per contract §9 — not embedded in this commit's files) |
| MANIFEST_SHA256.csv | the FINAL manifest, generated LAST: every physical file under OUTPUT_REPO_PATH except the manifest itself PLUS AUDIT_ENTRYPOINT.md; repo-relative paths; missing=0/extra=0/duplicate=0/size=0/SHA=0 required |

## §4. External evidence inputs (READ outside the repo; cited by identity)

| input | identity | role |
|---|---|---|
| DESKTOP_POST_AUDIT REPORT.md | C:\Users\User\Documents\ChatGPT\PE\PE_935_FUN006C9700_PLUS4_DESKTOP_POST_AUDIT_FD481C5_20261008\REPORT.md — 15346 B / SHA256 BF9C8C7903F984B0F3579B48A7EA5B9479BF4E9BE697F98EF0A6EFFAE6D2505B | the independent Desktop post-audit (verdict REQUIRE_CORRECTIONS on fd481c5) — the finding input of this correction run (FD-C1/FD-C2/FD-C3/REC-W/TOOL-MAP) |
| DESKTOP SCOPE_REASSESSMENT.csv | same directory — 7668 B / SHA256 C21DA7BA52F935D56FEE1864A283DC0DB8836A3AF58414C93C80CEA9EC78EF6B | the Desktop scope re-adjudication input (superseded in part by this package's own content-based floors) |
| DESKTOP COUNTERCHECKS.json | same directory — 38977 B / SHA256 A1F6A943E5A67C51F990126727C8A35CD0579CA9F70E5A7960911774210823AC | the Desktop counterchecks (incl. the independent W-ctor re-measure C6 of the REC-W agreement set) |
| ORIGINAL_MICRORUN_CONTRACT | C:\Users\User\Documents\ChatGPT\PE\PE_FUN006C9700_PLUS4_MICRORUN_PROMPT_R2_20261008\OPENCODE_FUN006C9700_PLUS4_MICRORUN_R2.md — 17487 B / SHA256 A6ABFE5E155F3FBAECDCC52E9D9A5E2B18D4286E67192C1C6717B3899EA2B20C | the source of the original budgets (12 edges / 6 bodies) — the FAIL-compliance baseline |
| DESKTOP_ENGINE_RESEARCH REPORT.md | C:\Users\User\Documents\ChatGPT\PE\PE_H4_P_GETTER_ENGINE_RESEARCH_20261008\REPORT.md — 17960 B / SHA256 D1B6B4A0F66D0BEAF65FBE7F9A97CC55BA7474A69DC51761E1B9DF500852E316 | INTERPRETIVE GUARDRAILS ONLY (not PCG byte proof) — recorded as GUARDRAILS_ONLY in CORRECTED_CLAIM_MATRIX.csv |
| EXE (local-only, NOT committed) | D:\Eudoria_Reconstruction\pcg_install\Entropia.exe — 8015872 B / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | the pinned 2003 client image; reads limited to the contract §2 policy; unchanged after all controls (re-verified before AND after); proprietary original stays local |

## §5. Referenced source package (READ_ONLY, unchanged)

`docs/audits/PE_935_CAND4_006C9700_PLUS4_PROVENANCE_R1_20261008/` — 28 files,
28/28 byte-identical to their BASE Git blobs (census in INPUT_IDENTITIES.md §4).
Load-bearing files cited by this correction: 01_RAW/MANUAL_ENCODING_CROSSCHECK.txt
(prior W-record, blob eea2876a…), 01_RAW/PINS_AND_REL32.txt,
SOURCE_STATE.md, EDGE_ACCOUNTING_LEDGER.csv, FUNCTION_BODY_ACCOUNTING.csv,
CLAIM_MATRIX.csv, POINTER_LINEAGE.csv, FINAL_REPORT.md, HANDOFF.md,
PE_MASTER_REVIEW.md, QC_REPORT.md, CONTROL_RESULTS.json,
00_CONTROL_INTERNAL_QC/QC_RESULTS.json, 03_SCRIPTS/checker_plus4.py — every
quote is inside the correction package's records; the source files themselves
were NOT edited.
