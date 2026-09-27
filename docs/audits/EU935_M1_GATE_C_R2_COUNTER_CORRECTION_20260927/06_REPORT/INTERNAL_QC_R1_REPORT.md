<!-- PROVENANCE: worker = pe-master-auditor (persistence phase of PE-MASTER loop dc98463f-f199-4a1a-8b96-c33a59ab6ecb); date = 2026-09-27; -->
<!-- SOURCE (verbatim copy): C:\Users\User\AppData\Local\Temp\opencode\EU935_M1_R2_20260927\QC_WORKSPACE\QC_REPORT.md — source sha256 = 249a5b47bbf01679db4acdd1634719d2ecffe64e9b2a30af23d9af2f5b3c83b0, 26812 bytes -->
<!-- NOTE: the bytes below this 3-line header are the source report copied VERBATIM (node fs byte copy); nothing below was added, removed or edited. -->
# QC REPORT — FRESH-CONTEXT READ-ONLY INTERNAL_QC
# RUN_ID: EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927 (QC phase)
# Executor: pe-reconstruction | QC: pe-master-auditor (fresh context) | Dispatcher: PE-MASTER
# Date: 2026-09-27 | READ-ONLY over D:\Eudoria_Reconstruction — ZERO repo mutations by this QC.
# All QC scripts live ONLY in C:\Users\User\AppData\Local\Temp\opencode\EU935_M1_R2_20260927\QC_WORKSPACE\

ASSIGNMENT_MODE: INTERNAL_QC (fresh-context, read-only, NO_NESTED_TASKS)
RUN_ID (audited package): EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
PARENT_LOOP_ID: EU935_M1_GATE_C_R2_CORRECTION_PERSISTENCE_NIGHTLOOP_20260927 (PE-MASTER loop dc98463f-f199-4a1a-8b96-c33a59ab6ecb)
MILESTONE: EU935-M1 (World Surface Fidelity); TARGET ERA PCG_9_3_5.

## VERDICT

**QC_PASS_WITH_FINDINGS** — 0 open P0 / 0 open P1 / 0 open P2; 5 bounded P3 findings
(3 newly found by this QC, 2 executor-disclosed and adjudicated correctly handled).
All 22 contract items PASS. Every load-bearing number was independently re-derived
from primary sources by this QC (own BNT2 parser, own census re-sums, own arithmetic,
own hash walks, own diff re-derivation, own blast-radius searches); nothing was taken
from the package's printed numbers.

---

## 0. QC METHOD + INDEPENDENCE STATEMENT

Counter-check discipline used (pe-master-audit §4): PHYSICAL_RECOMPUTATION_INDEPENDENT
for the terrain census (own BNT2 trailer parser from the hash-pinned bytes) and
RAW_ARTIFACT_REDERIVATION for the VCL sums (own re-summation of the per_file rows,
totals block not used); independent blast-radius searches over all 2,594 tracked files;
independent strict RFC4180 parser (own implementation, not the executor's); independent
manifest re-hash walks; independent diff re-derivation (BEFORE_IMAGES vs current bytes);
raw-byte live git diff capture via `git diff --output` (PowerShell Out-File was found to
corrupt bytes with CRLF — my own instrument error, caught and replaced before use).

QC scripts (AUDITOR counter-checks, NOT project evidence):
- qc_terrain_walk.mjs — own BNT2 census of terrain.bnt
- qc_edit_rederive.mjs — own line-level BEFORE→AFTER re-derivation of all three edits
- qc_manifests_csv.mjs — own manifest re-hash + strict CSV parse (both packages) + PRE_QC_SNAPSHOT drift
- qc_blast_search.mjs — own tracked-file searches (old counter + bad equation)
- qc_vcl_census.mjs — own census per_file re-derivation
- qc_runcontract_check.mjs — RUN_CONTRACT.md verbatim-materialization check
- qc_findings_fields.mjs — FINDINGS.csv field extraction

## 1. PER-ITEM RESULTS (all 22)

| # | Item | Verdict | My measured evidence |
|---|---|---|---|
| 1 | R2-F01 arithmetic | PASS | Machine-executed (node v22.22.0, my own process): 51920*1024=53166080; (220*32)*(236*32)=7040*7552=53166080 (both equal); falsifier 51920*32=1661440 != 1664000 (old total derivable from NO valid product over the denominator family). |
| 2 | Regular tile denominator | PASS | terrain.bnt SHA256 re-hashed FIRST = 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990, 125,064,817 B (pin MATCH). My OWN BNT2 walk: trailer dir_off=123369726, magic "BNT2", count=58,451; 58,451 entries parsed; index consumed EXACTLY p==filesize-8 (125064809). TOTAL 58,451; REGULAR 51,920 (distinct x=220 contiguous 0..219, distinct y=236 contiguous 0..235; every x row has 236 tiles and every y column 220 — full grid); SPECIAL 6,530; SENTINEL 7ffe7ffe.tdf = 1; DUPLICATES 0; 0 unclassified. R2_F01_TERRAIN_COUNTER.json matches every value including dir_off/index-end. |
| 3 | 32x32 denominator (1024) | PASS | R1 F03 §7.2 B line 99-100: "32x32 uint16 LE at payload offset 64" (HEIGHT_DATA_OFFSET=64, 64+2048=2112; 2048 B = 1024 x u16); 9216/9216 samples for 9 region tiles = 9*1024 (F03:119); committed canon verified on disk: "220x236" in PE_MILESTONE_1_WORLD_SURFACE_R1_GATE/EVIDENCE_MANIFEST.json L190, PE_M1_GATE_V4_CORRECTION_R2 v4_rows_a.py L29, FULL_MILESTONE_AUDIT CLAIM_LEDGER.csv L3; CORRECTION_LEDGER.md L254-255 carries the PE-MASTER physical name census (58,451 names; 51,920 regular; x[0..219], y[0..235]). |
| 4 | Semantic label of the corrected statement | PASS | F03:102-112 (my own read + my own diff): "TOTAL = 53,166,080 u16 SAMPLE SLOTS across the 51,920 regular 32x32 tile blocks"; NOT-list complete (NOT unique height values / NOT unique world points / NOT historical original-client parity / NOT historical rendering coverage / NOT terrain-texture coverage / NOT proof of the RGB-TDF bridge); attribution EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927 present; both arithmetic paths in the statement; BRIDGE_STATUS = UNKNOWN preserved at line 125; UNITS/CURRENT_RUNTIME_CALIBRATION labels at 113-117 byte-identical (my prefix/suffix re-derivation: 101 common-prefix lines + 27 common-suffix lines byte-identical; ONLY the statement span changed). |
| 5 | R2-F02 arithmetic | PASS | Machine-executed: 491*12+24+252=6168; (491+1+1)*12=5916; 493-21=472; 472*12+252=5916; 6168-5916=252=240+12. All five relations verified exactly. |
| 6 | Population overlap explanation | PASS | R2_F02_VCL_REVIEW_ERRATUM.md §4 names the exact overlaps: 240 = 25.vcl's 20 numeric lines x 12 ALREADY inside 491x12 (the +252 term re-adds ALL 21 groups/lines of 25.vcl, so only the comma group [12] is new); 12 = the 9.vcl continuation line's FIRST group ALREADY inside 491x12 (the +24 term re-adds BOTH its groups, so only the second is new). Populations (a) 25.vcl's 20 numeric lines ⊂ 491 numeric lines; (b) continuation-line first group ⊂ the 491 numeric rows' groups. I verified the underlying census myself (item 7) — the explanation is arithmetically exact, not waved at. |
| 7 | Raw VCL census validity | PASS | F02_VCL_CENSUS.json (21,151 B, SHA B67E1FC41820CDC165FB8033ABCA0A035CD23F7838623E166534527B6FE7093D == its UNCHANGED R1-manifest row — manifest re-hash 0 stale and EDIT C touched only rows 16/23). MY OWN re-summation of all 32 per_file rows: nonempty_lines=492, whitespace_tokens=5,916, groups12=493; success records re-summed from decoder fields (12+14+11+10+7+6+8+12+7+12+19+19+18+16+14+23+10+7+9+46+36+26+28+20+15+14+17+14+9+7+6, 25.vcl excluded) = 472; 25.vcl = 21 lines / 252 tokens / 21 groups / THROW / bad_tokens 6; 31 SUCCESS + 1 THROW; 9.vcl = 11 lines / 12 groups (the ONLY file with groups>lines). numeric_rows_12cols=491 read directly from F02_ITER032K_RERUN_vcl_columns.json (hash A62D9473... == its manifest row). VegetationClimates.bnt re-hashed = 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4, 25,346 B (pin MATCH — payloads untouched). Decoder source unchanged: live git diff == accepted patch (5978FF6B...) + numstat 30/6. The census/payloads/decoder were NOT modified by this run. |
| 8 | R2-P3 evidence label | PASS | EDIT B new description == contract 3b NEW value byte-exact. My OWN full read of DIFF_PEFoliageCore.js.patch: hunk 1 (@@ -35,11 +35,26 @@) = 4 removed + 19 added, ALL `//` comment lines; hunk 2 (@@ -120,7 +135,7 @@) = 1 removed + 1 added = the `exactness:` field value (ONE documentation-metadata string inside FOLIAGE_OPERAND_LOCK). No arithmetic/parser/control-flow/placement change — verified line-by-line. My src/ walk: FOLIAGE_OPERAND_LOCK/operandLock/.exactness referenced ONLY inside PEFoliageCore.js (definition L119 + self-references L152/L167/L386); ZERO consumers in any other src/ file; zero reads of .exactness. Patch bytes unchanged (re-hash = 27DEE19810FDED98FBE37E2013B742DA500BCD107AD0C85FEAFBCCDBF1EA96DD). |
| 9 | Predecessor modified paths (exactly 3, confined spans) | PASS | My own BEFORE→AFTER re-derivation (line-level, byte-exact): EDIT A = 1 removed (L102 old statement) + 11 added, common prefix 101 + suffix 27 lines byte-identical — everything outside the statement untouched; EDIT B = 1 line changed (L10), only the description field, other 26 rows byte-identical; EDIT C = only rows 16 (F03) and 23 (EVIDENCE_INDEX) changed — rows 17-22 byte-identical between BEFORE and AFTER versions (verified line-by-line). Package EDIT_A/B/C diffs match my re-derivation. BEFORE_F03 L102 == the contract's OLD span byte-exact. |
| 10 | Predecessor manifest | PASS | R1 MANIFEST_SHA256.csv: header + 48 data rows (49 rows x 3 fields). ONLY the F03 row (5704d1c8/9807 -> 72e1e221/10534) and EVIDENCE_INDEX.csv row (02e03b7d/7536 -> 67bfee8c/7710) changed vs BEFORE_MANIFEST_SHA256.csv (3A91F3A3.../8520). My full re-hash of ALL 48 rows over the 49-file R1 package: 0 stale / 0 missing; disk census 49 = 48 rows + self (self NOT listed). Both new row values == my fresh hashes. |
| 11 | Before-images byte identity | PASS x3 | My re-hash of all three copies: BEFORE_F03 = 5704D1C8.../9807; BEFORE_EVIDENCE_INDEX = 02E03B7D.../7536; BEFORE_MANIFEST = 3A91F3A3.../8520 — each == its before-pin == its ORIGINAL_SHA256 in BEFORE_IMAGE_METADATA.csv. BYTE_IDENTITY = YES x3 (hash + size; content identity re-derived in item 9). |
| 12 | Before-images manifest inclusion | PASS | All 3 BEFORE_IMAGES + BEFORE_IMAGE_METADATA.csv present as rows in the R2 package MANIFEST_SHA256.csv (rows verified by my re-hash: 02e03b7d/7536, 5704d1c8/9807, 3ed10b9a/1160, 3a91f3a3/8520 — all MATCH current disk). |
| 13 | New R2 package content | PASS (P3 findings below) | 34 files on disk == claimed. ALL 02_ANALYSIS + 00_CONTROL + 06_REPORT files read in FULL (REPORT.md 245 lines, HANDOFF.md 48, BASELINE_PIN.md 46, SOURCE_INDEX.md 32, all 5 analyses, FINDINGS/MODIFIED_PATHS/CORRECTION_EDGES/STAGE_GATES/AFTER/BEFORE_METADATA CSVs, the 3 evidence JSONs, the 3 edit diffs, both load-bearing probe scripts read for generator lineage). Package structure == contract Phase 5 list (all files present; fields per contract: FINDINGS 13 fields, MODIFIED_PATHS 9, CORRECTION_EDGES 6, STAGE_GATES 16 gate rows incl the 4 PENDING_*, AFTER_IMAGE_HASHES 4 rows, BEFORE_IMAGE_METADATA 6 fields). RUN_CONTRACT.md == 1005-byte header + the contract body BYTE-VERBATIM (offset 1005; 1005+20165=21170; contract SHA E0FFAB0C.../20165 re-hashed = pin). Every load-bearing number re-derived: census (item 2), both arithmetic paths (item 1), VCL sums + decomposition (items 5-7), patch class (item 8), before/after hashes (items 9-11), entrypoint numstat/diff (item 16), blast-radius searches (verified: "1,664,000" = exactly 1 tracked hit = the new entrypoint row; exactly 1 R1-package hit = the corrected F03 quote; bad-equation spaced variants = 0 hits; R1 package bad-equation = 0), mislabel scan 41 = my 40 current + 1 (the since-fixed EDIT B target; scan ran pre-edit — reconciled exactly). F05:87 residue disclosed in 5 places (REPORT §4/§8/§11, FINDINGS.csv open_residue, R2_P3 §4, BLAST_RADIUS §3, HANDOFF deviation 2) and NOT edited. "MILESTONE_POST_AUDIT_PASS" string occurs in exactly 4 package files — ALL as negations/contract text (RUN_CONTRACT L71 + r2_entrypoint_row.mjs L22 + STAGE_GATES L17: "this run claims NO ... PASS"; REPORT L24: "claims NO Gate C PASS and NO MILESTONE_POST_AUDIT_PASS") — ZERO occurrences assert a PASS. Report §14 discloses the caught-and-fixed transcription error (final values verified correct). |
| 14 | New R2 manifest | PASS | 33 data rows == 34 package files - 1; self NOT listed (explicit Select-String: no 06_REPORT/MANIFEST row); repo-relative paths; my re-hash of every row: 0 stale / 0 missing. |
| 15 | CSV schemas (both packages, strict RFC4180) | PASS | My own strict quote-aware parser, 0 malformed rows anywhere. R1 (9 CSVs, all == declared shapes): FINDINGS 7x18, GATE_REVALIDATION 6x8, MODIFIED_PATHS 5x6, RETRACTION_SUPERSESSION_DELTA 16x8, UNRESOLVED_DELTA 41x5, V4_1_DELTA 21x9, EVIDENCE_INDEX 27x5, STAGE_ACCEPTANCE_GATES 13x5, MANIFEST 49x3 — all re-verified AFTER the edits. R2 (9 CSVs): FINDINGS 4x13, MODIFIED_PATHS 5x9, CORRECTION_EDGES 4x6, STAGE_ACCEPTANCE_GATES 17x5, MANIFEST 34x3, BEFORE_IMAGE_METADATA 4x6, AFTER_IMAGE_HASHES 5x3, + BEFORE_EVIDENCE_INDEX 27x5 and BEFORE_MANIFEST 49x3 (copies). 0 errors, consistent field counts per file. |
| 16 | AUDIT_ENTRYPOINT row | PASS | git diff -U0 vs HEAD = exactly @@ -29,0 +30,2 @@ — 2 added lines / 0 deletions (R2 row at line 30 ABOVE the R1 row at line 31, newest-first as contracted); ALL historical rows byte-preserved (0 deletions). After-hash A0F21829.../115,846 B == pin (before 8EEC84E6/113,685). Row truthfulness verified against the Desktop R2 report (hash 80AFCF7D.../26,350 B == SOURCE_INDEX #15): Desktop R2 verdict = MILESTONE_POST_AUDIT_PARTIAL ✓ (report title + §22 + FINAL_VERDICT); Gate A = PASS per independent Desktop R2 audit ✓ (§20 + GATE_A_STATUS=PASS — scoped to M1-queue exhaustion with bounded terminal unknowns, exactly as the row says); Gate C = REQUIRES_INDEPENDENT_DESKTOP_REAUDIT ✓ (Desktop NEXT_ACTION: return to Desktop with the exact new SHA; the run claims NO Gate C PASS); Q1 NOT executed ✓ (Q1 absent); Gate B canonical authority = BLOCKED ✓; M1 = OPEN ✓; M2/Viewer NOT AUTHORIZED ✓. No MILESTONE_POST_AUDIT_PASS assertion anywhere in the entrypoint: the string occurs at L30 only inside the row's own negation ("claims NO Gate C PASS, NO MILESTONE_POST_AUDIT_PASS") and at L107 in the pre-existing verdict-vocabulary legend (present at HEAD; not one of the 2 added lines). |
| 17 | Source freeze | PASS | numstat 30/6 (VegetationClimateDecoder.js) + 20/5 (PEFoliageCore.js) re-measured at QC end. Live `git diff --output` raw buffers (byte-safe capture; my first Out-File attempt was instrument-corrupted by CRLF and discarded): PEFoliageCore = 27DEE19810FDED98FBE37E2013B742DA500BCD107AD0C85FEAFBCCDBF1EA96DD; VegetationClimateDecoder = 5978FF6B3CD9C787284B829E59D8CCCF18D14D0FA956B6D760D86C4278728723 — both BYTE-IDENTICAL to the accepted patches. The run did not touch the frozen sources. |
| 18 | Patch identity | PASS | Both DIFF_*.patch files re-hashed == pins == the R1 manifest rows (post-EDIT-C manifest rows 21/22 carry 27dee198.../3377 and 5978ff6b.../3389 — seen in the EDIT_C diff context and confirmed by my 0-stale manifest re-hash). Not regenerated (mtime-independent proof: byte identity to live diff + hash pins). |
| 19 | Path census | PASS | git status = EXACTLY 3 tracked modified (AUDIT_ENTRYPOINT.md, src/pesource/VegetationClimateDecoder.js, src/peworld/PEFoliageCore.js) + 4 untracked roots (R1 package, R2 package, docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/, experiments/) — NOTHING else (verified at QC start AND end; identical to GIT_INDEX_STATE.txt). NINODE root current top-level: 5 subdirs (00_CONTROL/01_RAW/02_ANALYSIS/03_EVIDENCE/06_REPORT), 7 files, 76,963 B. experiments root: 1 subdir (eu1030), 23 files, 285,745 B. Both untouched by this run (untracked, outside every manifest/snapshot of this run; no authorized reason to touch; contract forbids; no drift signal anywhere). |
| 20 | PRE_QC_SNAPSHOT | PASS | PRE_QC_SNAPSHOT.csv: 86 data rows + header (== claimed 86; == 49 R1 + 34 R2 + 1 entrypoint + 2 frozen sources exactly). My re-hash of ALL 86 rows vs current disk: 0 stale / 0 missing / 0 size drift → NO unexplained mutation since the executor's Phase 6 checkpoint; NO CONCURRENT_MUTATION signal. GIT_INDEX_STATE.txt == current git state (status/numstat/no-staged/HEAD cc747df). |
| 21 | No unrelated staged files | PASS | git diff --cached --name-status EMPTY (re-verified twice); HEAD == cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d == origin/master tracking ref; the executor performed NO git mutation (BASE_SHA == HEAD at QC end). |
| 22 | No open P0/P1/P2 | PASS | All defects I found are bounded P3 (see findings); the two executor-disclosed residues adjudicated correctly. Nothing in the delivered correction constitutes P0/P1/P2. |

## 2. FINDINGS (severity, exact location, falsifiable evidence, narrow correction)

**P3-QC-1 (HYGIENE) — garbled phrase "24608-independent"**
- Location: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/02_ANALYSIS/R2_F01_TERRAIN_SAMPLE_COUNTER.md line 16.
- Evidence: the line reads "(dir_off = 24608-independent value recorded in the JSON; count = 58,451)". The token "24608" is meaningless (dir_off is 123,369,726; the JSON carries the correct value; "24608" appears nowhere in the JSON).
- Skutek/Effect: none on any number — my own walk reproduces dir_off/count/index-end exactly; purely a wording corruption in a non-load-bearing description.
- Narrow correction: in a future bounded documentation pass, reword to "(dir_off and index-end recorded in the JSON; count = 58,451)". Do NOT edit the completed package in place (immutability); supersede or note in the persistence-phase review inventory.

**P3-QC-2 (HYGIENE) — in-cell editing artifact "9,216/9,916 -> 9,216/9,216"**
- Location: 02_ANALYSIS/SELF_ADVERSARIAL_PASS.md row 2 (TEST column).
- Evidence: the cell reads "9,216/9,916 -> 9,216/9,216 region-tile samples = 9 x 1,024". The correct value 9,216/9,216 (9 x 1,024) is stated; "9,916" appears nowhere else in either package (my grep: 1 hit total — this cell).
- Effect: none — the load-bearing value is correct and consistent with R1 F03:119 and R2_F01_TERRAIN_COUNTER.json ("9216/9216"); confusing notation only.
- Narrow correction: future pass — drop the "->" artifact, state "9,216/9,216 samples for 9 region tiles = 9 x 1,024".

**P3-QC-3 (CORRECTNESS-WORDING) — the 0-hit bad-equation repo-search claims are phase-1-time records; post-row the equation string exists in the correction's own registration row**
- Location: 02_ANALYSIS/BLAST_RADIUS.md §2 ("RESULT: 0 hits"), 02_ANALYSIS/R2_F02_VCL_REVIEW_ERRATUM.md §5 ("0 HITS ... never in a repo file"), 03_EVIDENCE/R2_F02_VCL_ARITHMETIC.json repo_search, AUDIT_ENTRYPOINT.md R2 row ("no repo file contained the bad equation — 0 hits over all 2,594 tracked files").
- Evidence (my own search): the spaced variants ("491x12 + 24 + 252" etc.) = 0 hits today; BUT the no-space form "491x12+24+252" now occurs once in the tracked worktree — inside the R2 row itself ("the pasted-review equation 491x12+24+252 actually equals 6,168"), and the executor's own flexible regex /491\s*[x*×]\s*12\s*\+\s*24/ would match it. The recorded byte total 133,463,531 proves the search ran BEFORE the row was added (my current tracked byte count 133,465,692 = 133,463,531 + 2,161 R2-row bytes).
- Effect: the SUBSTANCE is true (no repo file ASSERTS the equation; the only current occurrence quotes it as FALSE; no live dependent; the erratum is documentation-only). The unqualified present-tense "never in a repo file" is, read literally post-run, superseded by the correction's own quoted-false documentation.
- Narrow correction: no package edit needed (the timing is provable from the recorded byte counts); a persistence-phase note in the final review inventory stating "the equation string now appears in the entrypoint R2 row and this package only as quoted-FALSE documentation" would make the wording airtight. The analogous self-hit IS explicitly disclosed for the old-counter search (BLAST_RADIUS §1) — the equation search should have gotten the same one-line note.

**P3-QC-4 (CORRECTNESS-WORDING; executor-disclosed; adjudicated CORRECTLY HANDLED) — F05:87 "(comment-only; zero arithmetic change)"**
- Location: docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/02_ANALYSIS/F05_EXACTNESS_ORIGIN_PRECISION.md line 86-87.
- Evidence: reads "...corrected (comment-only; zero arithmetic change)"; the PEFoliageCore change also carried the exactness metadata string (item 8). The factual content "zero arithmetic change" is TRUE; the "comment-only" lead word is imprecise. OUTSIDE the authorized edit set (the 3 spans); editing it was contract-forbidden.
- Adjudication: correctly disclosed as an out-of-scope OPEN P3 residue in 5 places (REPORT §4/§8/§11, FINDINGS.csv R2-P3 open_residue, R2_P3 §4, BLAST_RADIUS §3, HANDOFF deviation 2) and NOT edited. This is the correct handling. Remains an open P3 for a future authorized pass.

**P3-QC-5 (HYGIENE; executor-disclosed; adjudicated CORRECTLY HANDLED) — RUN_CONTRACT.md single final CRLF**
- Location: 00_CONTROL/RUN_CONTRACT.md (the verbatim contract copy).
- Evidence: my byte-comparison: the file = 1005-byte header + the contract body byte-verbatim INCLUDING its final CRLF (bytes ...E. 0D 0A at 20164-20165 of the source). Every other package file is LF-only (my CR-scan: 0 CR-containing lines in the three edited R1 files; JSON outputs LF-terminated).
- Adjudication: verbatim materialization (contract Phase 5) vs LF-only discipline (FILE DISCIPLINE) conflict; the executor chose verbatim + explicit disclosure (BASELINE_PIN deviation record; HANDOFF deviation 3). Correct, bounded P3, non-blocking.

Also noted (not a finding against the delivered state): REPORT §14 discloses a caught-and-fixed transcription error in three DRAFT package files before finalization — the final values (a57aa321/8521 etc.) are verified correct by my own hashes; this is chain honesty, not a defect.

## 3. HARD-STOP CHECK

NONE. No unexplained mutation (PRE_QC_SNAPSHOT 0 drift, 86/86 rows identical); no source-byte drift (live diffs byte-identical to patches; numstats exact); no manifest/CSV corruption (both manifests 0 stale/0 missing; all 18 CSVs strict-parse clean); no contradiction between package claims and physical evidence undermining a correction (all three corrections independently reproduced from primary sources; all three applied to exactly the authorized spans).

## 4. NOT_CHECKED (QC coverage honesty)

- The client never ran in this QC either (STATIC-ONLY; no runtime experiments of any kind).
- The remote github.com state was not live-fetched (same environment limitation the executor disclosed; local tracking ref origin/master == cc747df == HEAD). Remote verification remains with the persistence phase.
- The interior bytes of the two DO-NOT-TOUCH untracked roots (NINODE audit, experiments) were NOT hash-verified (out of scope per the QC mandate; recorded top-level census only; no signal of touching).
- The R1 package's own historical scientific content (F01/F04/F05/F06 analyses, synthetic fixtures) was not re-audited here — this QC covered the R2 correction run and its three authorized edits per the 22-item mandate; the R1 package's internal science remains under the standing R1 QC + Desktop R2 record.
- The 8 R2 scripts were read for lineage on the two load-bearing probes; the 6 packaging utilities were verified by their OUTPUTS (my independent re-derivation of every diff/manifest/before-image they produced), not by full source reads.
- Milestone-level gate state (Gate A/B/C/D semantics) was verified only as REPORTED-CLAIM-consistency against the Desktop R2 report; this QC does not re-adjudicate the milestone.

## 5. INPUT AND OUTPUT HASHES (key chain)

Inputs (re-hashed by me):
- EXECUTE_CONTRACT_..._20260927.md = E0FFAB0C1BB8B5F4455948C2B52297A95D14026C02555BFD5A34F665F205A77F (20165 B) == BASELINE_PIN pin
- terrain.bnt = 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990 (125064817 B) == pin
- VegetationClimates.bnt = 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4 (25346 B) == pin
- GATEC_REAUDIT_R2_REPORT_20260927.md = 80AFCF7D9E8604B89D55DCF5F67BF02F07AAF85B515FCDFAC0AF712EDE19E02D (26350 B) == SOURCE_INDEX #15
- GATEC_REAUDIT_R2_CORRECTIVE_PROMPT_20260927.txt = 76C3B0301AA665BDEEF3B5C815413739548D3F1CD7D721C690FDCF470615744F (5356 B) == SOURCE_INDEX #16
- F02_VCL_CENSUS.json = B67E1FC41820CDC165FB8033ABCA0A035CD23F7838623E166534527B6FE7093D (21151 B) == its unchanged R1 manifest row
- DIFF_PEFoliageCore.js.patch = 27DEE19810FDED98FBE37E2013B742DA500BCD107AD0C85FEAFBCCDBF1EA96DD (3377 B) == pin == live diff
- DIFF_VegetationClimateDecoder.js.patch = 5978FF6B3CD9C787284B829E59D8CCCF18D14D0FA956B6D760D86C4278728723 (3389 B) == pin == live diff

Measured after-states (all == claims, all == current disk):
- F03_TERRAIN_TEXTURE_SCOPE.md = 72E1E22149405F4921CA69D36C8ADB2E5A776B4DE3ACBA2DB5F67F0E82662FFB (10534 B)
- EVIDENCE_INDEX.csv = 67BFEE8C15FAC242EC079BBA85F752C5B47A80B64A764CF3B0E6F5DECE910443 (7710 B)
- R1 MANIFEST_SHA256.csv = A57AA321BDBBB0BAA704FE714843B9E418DE44A91CED4BA53232C88642FE957F (8521 B)
- AUDIT_ENTRYPOINT.md = A0F21829B8440E5183AEDC6B16337BF5E971C005A3485C19442B22F07444E8F0 (115846 B)
- BEFORE_IMAGES: 5704D1C8.../9807, 02E03B7D.../7536, 3A91F3A3.../8520 (all == pins)

## 6. HANDOFF BLOCK

ASSIGNMENT_MODE: INTERNAL_QC (fresh-context, read-only)
RUN_ID: EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
PARENT_LOOP_ID: EU935_M1_GATE_C_R2_CORRECTION_PERSISTENCE_NIGHTLOOP_20260927 (dc98463f-f199-4a1a-8b96-c33a59ab6ecb)
MILESTONE: EU935-M1
SCOPE: the R2 counter-correction package (34 files) + the 3 authorized predecessor edits + the entrypoint R2 row + source/patch freeze + snapshot integrity
QC_VERDICT: QC_PASS_WITH_FINDINGS
FINDINGS: 5 bounded P3 (P3-QC-1, P3-QC-2, P3-QC-3 new; P3-QC-4, P3-QC-5 executor-disclosed and correctly handled). OPEN_P0 = 0, OPEN_P1 = 0, OPEN_P2 = 0.
FULL_READ_LOG_PATH: C:\Users\User\AppData\Local\Temp\opencode\EU935_M1_R2_20260927\QC_WORKSPACE\QC_REPORT.md (this file; full-read log in section 1: all package control/analysis/report files + both load-bearing probe scripts read in full; all CSVs strict-parsed; all manifests re-hashed)
NOT_CHECKED: remote state; NINODE/experiments interiors; R1 historical science internals; runtime anything (see §4)
FINAL_REPORT_PATH (audited run): docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/REPORT.md
GATES_PATH: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/STAGE_ACCEPTANCE_GATES.csv (OPEN_P0P1P2 + INTERNAL_QC remain PENDING_QC_PHASE — this QC report is the QC-phase input; gate-row updates belong to the persistence phase per the run contract)
MANIFEST_PATH: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/MANIFEST_SHA256.csv
FILES_CHANGED (by this QC): NONE inside the repo (READ-ONLY held); QC scripts + this report live only in the QC_WORKSPACE
BASE_SHA: cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d
HEAD_SHA: cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d (unchanged; no commits; staged = NONE)
PUSH_STATUS: NOT_APPLICABLE (QC performed no git operations; publication belongs to the persistence phase)
UNRELATED_WORK_EXCLUDED: docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ (7 files, 76,963 B) and experiments/ (23 files, 285,745 B) — untouched, out of scope; the two frozen sources — byte-frozen, verified
NEXT_PARENT_ACTION: PE-MASTER final audit of this run; then the human-authorized persistence (Commit 1: R1 + R2 packages + the 3 tracked modifications, path-limited), with STAGE_ACCEPTANCE_GATES rows OPEN_P0P1P2 + INTERNAL_QC resolved from this QC record and PE-MASTER's verdict; Gate C remains REQUIRES_INDEPENDENT_DESKTOP_REAUDIT; Q1 NOT executed; M1 OPEN; M2/Viewer NOT AUTHORIZED.
