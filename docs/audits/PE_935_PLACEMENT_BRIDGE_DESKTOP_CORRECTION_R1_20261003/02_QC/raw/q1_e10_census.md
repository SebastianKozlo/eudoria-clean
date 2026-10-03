# QC-F1 RAW — E10 retracted-vocabulary census (my own instrument)

DATE = 2026-10-03 (UTC) | INSTRUMENT = built-in content-search grep (case-sensitive patterns; one case-insensitive variant noted) + PowerShell substring extraction for AUDIT_ENTRYPOINT.md
SCOPE = all repo *.md + *.csv under D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (working tree at HEAD b151d428)

## Pattern 1 (case-sensitive): slot-position|slot position|payload-derived|payload derived|spatial vec3

### *.md hits — classification

(a) HISTORICAL PACKAGE (preserved historical artifacts, superseded — NOT live residue), 5 files / 15 lines (my count):
- docs/audits/PE_935_PLACEMENT_RECORD_BRIDGE_GAMEBRYO_R1_20261003T071348Z/02_ANALYSIS/TRACE_EDGE_BLOCKS.md — 7 lines: 349, 375, 379, 392, 456, 464, 465
- .../07_QC/QC_AUDIT_R1.md — 2 lines: 298, 299
- .../06_REPORT/DRAFT_FINAL_REPORT.md — 4 lines: 96, 97, 110, 166
- .../06_REPORT/AMEND_LOG_R1.md — 1 line: 113
- .../06_REPORT/PE_MASTER_REVIEW.md — 1 line: 79
→ EXACTLY MATCHES the executor's census claim "5 files, 15 lines: TRACE 7, AMEND 1, DRAFT 4, PE_MASTER_REVIEW 1, QC_AUDIT 2".

(b) NEW PACKAGE supersession/census/contract text (NOT promotions):
- 00_CONTROL/AUTHORIZATION.md lines 393-396 (order §4 forbidden-vocabulary list, verbatim order text), 2101 (order summary)
- 01_ANALYSIS/DESKTOP_FINDINGS.md lines 56, 62-73 (historical quotes + retraction context), 107 (forbidden vocabulary list)
- 01_ANALYSIS/CURRENT_CLAIM_STATE.md lines 45-48 (forbidden vocabulary list), 179/189/191-192 (census method/classification)
- 01_ANALYSIS/EXECUTION_LOG.md line 59 (census PATTERN definition)

(c) UNRELATED_SENSE (vtable slot alignment — different claim families, not E10):
- PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914: 06_REPORT/HANDOFF.md:20, 02_ANALYSIS/ENTROPIA_SLOT17_FINGERPRINT.md:167, 06_REPORT/REPORT.md:82 (3 lines — "slot-position alignment" = vtable slot alignment)
- PE_935_SF_ARG2_PROVENANCE_R1_20260914/06_REPORT/QC_AUDIT.md:260, 265 (2 lines — "slot positions across its 10 vtables" / "a single slot position")
- PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914/00_CONTROL/RUN_CONTRACT.md:105 — verified by me with case-insensitive pattern (?i)slot.position: line 105 = "A: at least one slot POSITION_TO_CALL -> give NEXT_SEAM = exactly ONE most direct call target" — vtable-slot naming; case-insensitive-only hit (matches executor's classification)

(d) OTHER LIVE DOC PROMOTING E10 POSITION/TRANSFORM SEMANTICS: **NONE FOUND**

### *.csv hits (pattern 1): 2 matches
- new package 01_ANALYSIS/CORRECTION_MATRIX.csv line 2 — historical quotes + corrected statuses (supersession record)
- historical 02_ANALYSIS/CLAIM_MATRIX.csv line 11 — historical artifact (preserved)
→ no other CSV promotes E10 semantics.

## Pattern 2 (case-sensitive): world transform — 29 matches, classified:
- historical package: ORACLE_RECORDS.md:87 ("local->world transforms", Mechanism 3 record), RUN_PLAN.md:71 — PRESERVED historical artifacts
- new package contract/supersession/deferred-lead text: AUTHORIZATION.md:397 (forbidden vocabulary), 1200 (§12 ladder), 2101; EXECUTION_LOG.md:35; DEFERRED_PLACEMENT_LEADS.md:212 (§12 ladder quote); DESKTOP_FINDINGS.md:107; CURRENT_CLAIM_STATE.md:49 (forbidden vocabulary), 88 (F-D3 locator description — Gamebryo local→world propagation, oracle context, not an E10 promotion)
- UNRELATED_SENSE (other claim families, not E10): docs/nif/11-open-problems.md:59 (REJECTED NIF material-object note); docs/forensics/iter037-model-witness.md:86,121 (foliage/NIF visualizer); PE_935_STATIC_PLACEMENT_ROUND1_20260913:68,153 + PE_935_STATIC_INSTANCE_TRACE_R1_20260913:123, Z4:97,110 (separate historical SF/setter-consumer claim families, statuses UNVERIFIED); PE_935_SF_DOWNSTREAM_POSITION_CONSUMER_R1_20260915/02_ANALYSIS/POSITION_SEMANTICS.md:11 (SF position-consumer family — placement-record setters, NOT templates.vfs list2/E10); PE_935_EXTERNAL_SOURCES_MATRIX_R1_20260913 (DAoC/WarEmu packet grammar); PE_935_CONSUMER_TRACE_CLAIMS_JOIN_R1_20260913 (claim E UNVERIFIED); PE_935_ATTRIBUTE_ORIGIN_SEAM_R1_20260913/RUN_CONTRACT.md:27 (transform-discipline rule); PE_935_PLACEMENT_INSTANCE_RESOURCE_JOIN_R1_20260928/RUN_CONTRACT.md:393 + PE_MASTER_REVIEW.md:22 (WORLD_TRANSFORM_CONSUMER for record→instance→SceneFeeder copies — separate family, its own package)
→ no live doc promotes E10 world-transform semantics.

## Pattern 3 (case-sensitive): positions — 100+ raw substring matches, dominated by "dispositions" (superstring) and non-E10 senses (byte positions, camera positions, foliage node positions, "the 296445 positions NOT recovered" negative statements, rand01/positions PC24 etc.).
E10-context "positions" hits:
- historical package TRACE_EDGE_BLOCKS.md:375 ("(positions)") — preserved artifact
- new package contract/supersession text (AUTHORIZATION.md:392, 2101; DESKTOP_FINDINGS.md:56, 62; CURRENT_CLAIM_STATE.md:44)
- AUDIT_ENTRYPOINT.md — verified by my own substring extraction (PowerShell): ALL its "positions" occurrences are inside "dispositions" (lines 31, 43, 87) or the negative statements "the 296445 positions NOT recovered" (lines 48, 50, 51) → 0 E10 promotions in the live entrypoint.
→ no live E10 "positions" promotion found.

## Required statuses check (CURRENT_CLAIM_STATE.md + DESKTOP_FINDINGS.md — full reads):
E10_OBSERVED_OPERATION = CONFIRMED (chain verbatim per order §4) ✓
E10_FINAL_SEMANTIC_ROLE = UNVERIFIED ✓
E10_SPATIAL_POSITION_OR_TRANSFORM = NOT_ESTABLISHED ✓
E10_SLOT_CLASS = UNKNOWN ✓
COLOR_VECTOR_HYPOTHESIS = PLAUSIBLE_ALTERNATIVE_ONLY ✓
WORLD_INSTANCE_IDENTITY = NOT_ESTABLISHED ✓ / WORLD_INSTANCE_EDGE = NOT_ESTABLISHED ✓
PERSISTENT_PLACEMENT_EDGE = NOT_ESTABLISHED ✓ / PLACEMENT_XYZ_RECOVERED = NO ✓
Supersession statement present verbatim: "Historical E10 position/transform wording from b151d428 is SUPERSEDED by this correction." (CURRENT_CLAIM_STATE.md:14) ✓
NO text asserting E10 = COLOR (both files explicitly record the negative) ✓
No color decoders (package tree = 9 md/csv files only) ✓
No consumer trace added (no new trace artifacts; EXECUTION_LOG §3 negatives) ✓

## Historical package integrity (this QC):
- git status --porcelain on the historical package path: EMPTY (clean) ✓
- 06_REPORT/FINAL_REPORT.md: SIZE=27,690 B SHA256=EDC245EFE76CB774FA2F65863AF9E14531BCBC9AFAB9EA8B84EB251764E048B0 (matches Phase-A pin) ✓
- 06_REPORT/PE_MASTER_REVIEW.md: SIZE=12,901 B SHA256=4BE5A85497EB2BFB9083A02BDC0080DEC5E946691B8FD9E3D758BE6835836E2D (matches Phase-A pin) ✓

## CONCLUSION

ACTIVE E10 POSITION/TRANSFORM SEMANTIC PROMOTIONS = 0
(outside supersession/retraction records; historical quotes preserved; contract text is not promotion; unrelated-sense hits classified)
