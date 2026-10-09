# AMEND_LOG — Records-Correction Round for PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009

- **AMENDMENT_CLASS**: BOUNDED RECORDS-ONLY CORRECTION, in place, package NOT yet published (single authorized round; max this one).
- **EXECUTOR**: pe-reconstruction (own not-yet-published package), dispatched by PE-MASTER 2026-10-09.
- **WORKLIST SOURCE**: fresh internal QC `PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_QC_R1_20261009` (QC_RESULTS.json / QC_REPORT.md, verdict QC_PASS_WITH_FINDINGS; findings P2-1, P2-2, P2-3, P3-1, P3-2).
- **RULES OBEYED**: no commit/push; AUDIT_ENTRYPOINT.md untouched; no MANIFEST; QC artifacts (QC_RESULTS.json / QC_REPORT.md) and SCRATCH untouched — their quotes of pre-correction strings remain as historical evidence; no new science, no binary analysis, no EXE reads; **no science value changed** (no pins, no VAs, no slot table, no dispositions, no gate results, no claim limits, no falsifier verdicts).
- **AMEND_LOG.md itself is NOT added to EVIDENCE_INDEX.md**: like the QC outputs, it is a post-run supervision/records artifact, outside the index's declared scope ("every package file ... hashed from disk AFTER the run's final write" — the 18 run artifacts; the index self-excludes itself and does not list QC_RESULTS.json/QC_REPORT.md either).

## P2-1 — BODY_CFG_AND_ACCESS_CENSUS.json (RESOLVED)

- **Change**: `cfg.blocks[8]` (BB_exit, range 0x006C3691-0x006C369B) — `"insns": 6` -> `"insns": 7`.
  - OLD: `{"id": "BB_exit", "range": "0x006C3691-0x006C369B", "insns": 6, "role": "EAX:=arg1; *arg1:=ESI (vector); pop esi/ebx/edi/ebp; RET"},`
  - NEW: `{"id": "BB_exit", "range": "0x006C3691-0x006C369B", "insns": 7, "role": "EAX:=arg1; *arg1:=ESI (vector); pop esi/ebx/edi/ebp; RET"},`
- **No other field changed**; no instruction record changed (BB_empty legitimately keeps `insns`: 6; BB0 keeps 6; the access_census rows are byte-identical).
- **Verification**: block counts re-summed from the corrected artifact: 6+4+5+2+4+2+8+3+7+6 = **47** == window instruction count (auditor decode). BB_exit's 7 instructions confirmed from the dual-verified listing: 0x006C3691 mov / 0x006C3695 mov / 0x006C3697 pop esi / 0x006C3698 pop ebx / 0x006C3699 pop edi / 0x006C369A pop ebp / 0x006C369B ret.
- **Pre SHA256**: 529ff1513d86aeb6a6b1edbe27c18a0d33f4269804c842aa82724b836c2f4412 (11128 B)
- **Post SHA256**: 3d6903142d2c5e2cb75b744a2f5a11717b51c5216e9cccd30466acefd8bf4222 (11128 B)
- **EVIDENCE_INDEX row re-hashed** (see EVIDENCE_INDEX.md section below).

## P2-2 — FALSIFIER_RESULTS.json F1 itemization (RESOLVED)

- **Change**: `falsifiers[0].measured_quantity` multiset corrected to the true 8-element multiset.
  - OLD: `... 8 callee esp-relative operations resolving to entry_offsets {arg1 x3, arg2 x1, arg3 x1, arg4 x2, arg5 x1, &arg1 x1}; arg6: 0 accesses; ...`
  - NEW: `... 8 callee esp-relative operations resolving to entry_offsets {arg1 x2, &arg1 x1, arg2 x1, arg3 x1, arg4 x2, arg5 x1}; arg6: 0 accesses; ...`
- Corrected multiset sums: 2+1+1+1+2+1 = **8** == the stated total (the old itemization summed to 9). Multiset verified against the artifact's own census rows (esp-based ops: arg1 @0x006C3691 + @0x006C369C, &arg1 LEA @0x006C367C, arg2 @0x006C3646, arg3 @0x006C3641, arg4 @0x006C3654 + @0x006C36A0, arg5 @0x006C364F).
- **F1 verdict NOT changed**: outcome remains `PASS (all 6 slots machine-verified from both sides; contract slot claims confirmed; VA annotation corrected)`; failure_case_detected / why_non_circular / independent_source_of_truth untouched.
- **Pre SHA256**: 22433e21a55f026b9c7e604d67ff96be946cd58ebfef6f3627f9dd80336a7f8e (12934 B)
- **Post SHA256**: ec8a8a1b7d283a1ea6e3b036454ca7d9797d21a4bcce83a36f3c780fabd1bad0 (12934 B)
- **EVIDENCE_INDEX row re-hashed** (see EVIDENCE_INDEX.md section below).

## P2-3 — HANDOFF.md arg6 bullet wording (RESOLVED)

- **Change** (PER-VALUE DISPOSITION, arg6 bullet; logical text, physical wrap changed 2 -> 3 lines, LF-only line endings preserved):
  - OLD: `... NEVER READ (machine-verified: 0 of 17 esp-relative operations resolve to entry offset 0x18); discarded by the caller's ADD ESP,0x18.`
  - NEW: `... NEVER READ (machine-verified: 0 of the window's 17 census rows (16 accesses + 1 LEA; 8 of them esp-relative) resolve to entry offset 0x18); discarded by the caller's ADD ESP,0x18.`
- Both numbers now stated correctly: 17 total census rows (16 accesses + 1 LEA), of which 8 are esp-relative; 0 of them resolve to entry offset 0x18. This matches BODY_CFG census_note and the QC's mandated wording.
- **The dead-argument claim itself remains verbatim**: "DEAD ARGUMENT in this consumer — NEVER READ ... discarded by the caller's ADD ESP,0x18." No other HANDOFF.md line changed.
- **Pre SHA256**: cd394773d1ecae196648b4a3240b9828c3c2e1a9739ccbe080ade9550a68dc24 (15148 B)
- **Post SHA256**: 5558b870b5c9ae808e834174bba357ff6d229cbe7beb4c013aacad60c7b3145a (15197 B)
- **EVIDENCE_INDEX row re-hashed** (see EVIDENCE_INDEX.md section below).

## P3-1 — CP1252 em-dash byte in two headers (RESOLVED)

- **Change 1 — 01_RAW/KEY_REGION_LISTINGS.md, line 1, byte offset 22**: single byte `0x97` (CP1252 em-dash) -> UTF-8 em-dash `E2 80 94`. Byte-exact splice: no other byte touched (size +2); CRLF line endings preserved (128 CRLF, 0 lone LF).
  - OLD header: `# KEY_REGION_LISTINGS<0x97> PE_935_...`
  - NEW header: `# KEY_REGION_LISTINGS — PE_935_...`
  - **Pre SHA256**: d87dabfaf4f0bd7038878e2fd97caf952cfde9fce6eae453b8033bca0920948e (10056 B)
  - **Post SHA256**: 25190273e65fb9a894ffd381e49816cff7c03fcc8f90da6c8a3a194c359a4b32 (10058 B)
  - **EVIDENCE_INDEX row for KEY_REGION_LISTINGS.md refreshed (re-hashed) as required** — see below.
- **Change 2 — EVIDENCE_INDEX.md, line 1, byte offset 17**: single byte `0x97` -> UTF-8 em-dash `E2 80 94` (byte-exact splice, no other byte affected).
  - OLD header: `# EVIDENCE_INDEX<0x97> PE_935_...`
  - NEW header: `# EVIDENCE_INDEX — PE_935_...`
  - EVIDENCE_INDEX.md is self-excluded from its own table, so no self-reference problem (per QC finding text).
- **Verification**: both files now decode as STRICT UTF-8 (decode with exception fallback passes); full-package byte scan: every package file decodes strictly as UTF-8 (0 failures; remaining 0x97 bytes anywhere are legitimate UTF-8 continuation bytes, e.g. U+00D7 `×` = C3 97).

## P3-2 — SCRATCH intermediates not pinned (OBSERVATION — NOTED, no defect)

- Optional sentence ADDED to EVIDENCE_INDEX.md Integrity notes (the QC-authorized optional action):
  - NEW (3-line bullet): `- SCRATCH intermediates (analysis outputs, raw_slices/) are intentionally NOT hash-pinned here (local-only, outside git); the final window slices ARE pinned by SHA256 in 01_RAW/OWN_DECODER_WINDOWS.json exe_slices (QC_R1 finding P3-2 note).`
  - OLD: none (addition).
- No load-bearing content; scope/provenance note only.

## EVIDENCE_INDEX.md (rows re-hashed in the same round)

- **Why**: EVIDENCE_INDEX.md pins package-artifact SHA256s; the four corrected artifacts above required row refreshes (QC revalidation predicates P2-1/P2-2/P3 each state "EVIDENCE_INDEX row updated"; P3-1 explicitly requires the KEY_REGION_LISTINGS.md row refresh).
- **Pre SHA256**: 4ec208f4cfe311d708e5f1b3ee1434375c18105b12bd60c98f0c6953b3bc10bf (5303 B; intermediate state after only the em-dash byte fix: 8b5b308c2132d39c8b759253d2cfd06e30d3d9b7cc545e62c1de429f70529a96, 5305 B)
- **Post SHA256**: 6fe53eb6bcafc0e290428249622aef45ca680bbbc749ce708f05a2ddcb479c36 (5552 B)
- **Row changes (old -> new)**:
  - `| BODY_CFG_AND_ACCESS_CENSUS.json | 11128 | 529ff1513d86aeb6a6b1edbe27c18a0d33f4269804c842aa82724b836c2f4412 |` -> `| BODY_CFG_AND_ACCESS_CENSUS.json | 11128 | 3d6903142d2c5e2cb75b744a2f5a11717b51c5216e9cccd30466acefd8bf4222 |` (P2-1)
  - `| FALSIFIER_RESULTS.json | 12934 | 22433e21a55f026b9c7e604d67ff96be946cd58ebfef6f3627f9dd80336a7f8e |` -> `| FALSIFIER_RESULTS.json | 12934 | ec8a8a1b7d283a1ea6e3b036454ca7d9797d21a4bcce83a36f3c780fabd1bad0 |` (P2-2)
  - `| HANDOFF.md | 15148 | cd394773d1ecae196648b4a3240b9828c3c2e1a9739ccbe080ade9550a68dc24 |` -> `| HANDOFF.md | 15197 | 5558b870b5c9ae808e834174bba357ff6d229cbe7beb4c013aacad60c7b3145a |` (P2-3)
  - `| 01_RAW/KEY_REGION_LISTINGS.md | 10056 | d87dabfaf4f0bd7038878e2fd97caf952cfde9fce6eae453b8033bca0920948e |` -> `| 01_RAW/KEY_REGION_LISTINGS.md | 10058 | 25190273e65fb9a894ffd381e49816cff7c03fcc8f90da6c8a3a194c359a4b32 |` (P3-1)
- All other rows (14 remaining package artifacts + 10 tooling scripts) byte-unchanged.

## Post-amendment verification (executor self-check, re-measured)

1. BODY_CFG_AND_ACCESS_CENSUS.json: parses as JSON; 10 blocks; insns sum = 47; BB_exit insns = 7; access_census still 17 rows; census_note unchanged.
2. FALSIFIER_RESULTS.json: parses as JSON; 8 falsifiers; F1 multiset = {arg1 x2, &arg1 x1, arg2 x1, arg3 x1, arg4 x2, arg5 x1} sums to 8; F1 outcome verbatim PASS; claim_limits string byte-identical.
3. HANDOFF.md: corrected phrase present; old "0 of 17 esp-relative" phrasing absent; dead-argument claim verbatim present; LF-only line endings preserved (168 LF, 0 CRLF).
4. KEY_REGION_LISTINGS.md + EVIDENCE_INDEX.md: strict UTF-8 decode PASS; CRLF-only line endings preserved.
5. EVIDENCE_INDEX integrity: all 18 package-artifact rows re-hashed from disk AFTER the amendments — 18/18 MATCH, 0 mismatches.
6. Package-wide sweep: no defective count/label remains outside the QC artifacts and the AMEND_LOG quotes above ("arg1 x3", "0 of 17 esp-relative", BB_exit "insns": 6 each verified absent from the executor artifacts; remaining occurrences are only in QC_RESULTS.json/QC_REPORT.md findings quotes, which are historical QC evidence).
7. No file outside the five listed here was modified (18/18 row re-hash confirms; QC artifacts and SCRATCH untouched; AUDIT_ENTRYPOINT.md untouched; no git operations performed).
