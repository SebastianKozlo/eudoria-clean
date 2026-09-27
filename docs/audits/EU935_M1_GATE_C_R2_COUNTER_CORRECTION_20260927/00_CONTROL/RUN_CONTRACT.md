# RUN CONTRACT (VERBATIM) - EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927

- DISPATCHER: PE-MASTER (loop dc98463f-f199-4a1a-8b96-c33a59ab6ecb; orchestration EU935_M1_GATE_C_R2_CORRECTION_PERSISTENCE_NIGHTLOOP_20260927)
- EXECUTOR: pe-reconstruction. NO_NESTED_TASKS: this agent dispatches NO other agent; it returns to PE-MASTER when done or blocked.
- RUN_CLASS: LOAD_BEARING; RUN_TYPE: GATE_C_R2_BOUNDED_COUNTER_CORRECTION; STATIC-ONLY: the client never ran; no GPU; no new corpus; no new RE beyond the bounded reproductions defined in the contract.
- MILESTONE: EU935-M1 (World Surface Fidelity); TARGET ERA: PCG_9_3_5.
- CONTRACT VERBATIM SOURCE: C:\Users\User\AppData\Local\Temp\opencode\EU935_M1_R2_20260927\EXECUTE_CONTRACT_EU935_M1_GATE_C_R2_COUNTER_CORRECTION.md (SHA256 E0FFAB0C1BB8B5F4455948C2B52297A95D14026C02555BFD5A34F665F205A77F, 20165 B; re-hashed at run start = MATCH). The dispatch prompt text is identical to that file. The contract body below is materialized VERBATIM from it.

---

﻿# RUN CONTRACT (dispatcher: PE-MASTER; executor: pe-reconstruction; NO_NESTED_TASKS)

RUN_ID: EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927
ORCHESTRATION_ID: EU935_M1_GATE_C_R2_CORRECTION_PERSISTENCE_NIGHTLOOP_20260927 (PE-MASTER loop dc98463f-f199-4a1a-8b96-c33a59ab6ecb)
MILESTONE: EU935-M1 (World Surface Fidelity). TARGET ERA: PCG_9_3_5.
RUN_CLASS: LOAD_BEARING; RUN_TYPE: GATE_C_R2_BOUNDED_COUNTER_CORRECTION. STATIC-ONLY: the client never runs; no GPU; no new corpus; no new RE beyond the bounded reproductions defined here.
TIMEBOX: target <= 60 minutes of work. This is a bounded correction + package run, not a science run.

## S0 GIT / STATE PIN (fail-closed; re-verify yourself at start; ANY mismatch -> record + STOP, no edits)

- Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean; branch master.
- BASE_SHA = HEAD = origin/master = remote master = cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d.
- YOU perform NO git add/commit/push/stash/checkout/reset. Persistence is a LATER, separate phase (another worker). HEAD must remain cc747df at your handoff.
- Expected worktree (PE-MASTER-verified 2026-09-27 ~01:0xZ): staged = NONE; tracked modified EXACTLY 3: AUDIT_ENTRYPOINT.md (+1/-0), src/pesource/VegetationClimateDecoder.js (+30/-6), src/peworld/PEFoliageCore.js (+20/-5); untracked roots: docs/audits/EU935_M1_GATE_C_FINDINGS_REVALIDATION_R1_20260926/ (49 files), docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ (DO NOT TOUCH), experiments/ (DO NOT TOUCH).

## HASH PINS (PE-MASTER-fresh 2026-09-27; re-verify each before relying on it)

- predecessor/02_ANALYSIS/F03_TERRAIN_TEXTURE_SCOPE.md = 5704D1C8F8166FE5BF1B88B0E8D0B13E7A0DE3AC83463BDAF920831E863489DF, 9807 B  (EDIT TARGET A)
- predecessor/03_EVIDENCE/EVIDENCE_INDEX.csv = 02E03B7D073E5579123A95B03383BAC26CEBFF46E83A24B36A1693CAEDD05B08, 7536 B  (EDIT TARGET B)
- predecessor/06_REPORT/MANIFEST_SHA256.csv = 3A91F3A3505F6F3D46EDEE246FF91E26B373586D32803E57E18D6DA4D1C46462, 8520 B  (EDIT TARGET C)
- AUDIT_ENTRYPOINT.md = 8EEC84E65C19B56705B023AADAB27B5AD0A05E03686E5992F4C47A4836BEE45E, 113685 B  (add ONE row; all existing rows byte-preserved)
- predecessor/03_EVIDENCE/DIFF_PEFoliageCore.js.patch = 27DEE19810FDED98FBE37E2013B742DA500BCD107AD0C85FEAFBCCDBF1EA96DD, 3377 B (live "git diff -- src/peworld/PEFoliageCore.js" is byte-identical to it - PE-MASTER-verified; do NOT regenerate or modify this patch)
- predecessor/03_EVIDENCE/DIFF_VegetationClimateDecoder.js.patch = 5978FF6B3CD9C787284B829E59D8CCCF18D14D0FA956B6D760D86C4278728723, 3389 B (live diff byte-identical - PE-MASTER-verified)
- D:/Eudoria_Reconstruction/pcg_install/Data/Terrain/terrain.bnt = 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990, 125064817 B (PCG_9_3_5; == the M1-audit fresh pin)
- D:/Eudoria_Reconstruction/pcg_install/Data/VegetationClimates/VegetationClimates.bnt = 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4, 25346 B
- FROZEN SOURCES (DO NOT MODIFY): src/pesource/VegetationClimateDecoder.js and src/peworld/PEFoliageCore.js must remain byte-identical to BASE+patch for the whole run (verify: your fresh git diff hash == the patch hashes above; numstat 30/6 and 20/5 at handoff).
- Desktop R2 inputs (READ-ONLY claims): C:\Users\User\Documents\ChatGPT\PE\GATEC_REAUDIT_R2_REPORT_20260927.md; GATEC_REAUDIT_R2_CORRECTIVE_PROMPT_20260927.txt; gatec_reaudit_r2_* results. Treat every Desktop finding as falsifiable; your OWN reproduction is the basis; do not execute a correction merely because Desktop requested it.

## ONE PRIMARY QUESTION

Are Desktop R2's three bounded package-quality findings independently reproducible, and can the three bounded predecessor corrections be applied byte-safely with full before-image preservation, inside the authorized path set?

## PHASE 1 - INDEPENDENT REPRODUCTION (before any edit; scripts write ONLY into the R2 package)

1a. R2-F01 TERRAIN SAMPLE COUNTER. Write 03_EVIDENCE/scripts/r2_f01_terrain_counter.mjs (node v22.22.0; READ-ONLY on the BNT): BNT2 trailer parse of the pinned terrain.bnt (trailer [dir_off u32]["BNT2"]; at dir_off [count u32]; entries [name 0x0A-terminated][size u32][offset u32][crc u32][flags u32]; verify index consumed exactly p == filesize-8). Census ALL names: total, eight-hex .tdf names, REGULAR (x = first 4 hex chars in [0..219] AND y = second 4 hex chars in [0..235]), special (y in [0xff1a..0xffff]), sentinel 7ffe7ffe.tdf, duplicates, distinct x/y values + ranges. EXPECTED (independently established by PE-MASTER own walk): total 58451; regular 51920 (distinct x = exactly 220 values 0..219; distinct y = exactly 236 values 0..235); special 6530; sentinel 1; duplicates 0. Record MEASURED_QUANTITY / SOURCE / SOURCE_HASH / METHOD / EXCLUSION_SET / RESULT (exclusion set = 6530 special + 1 sentinel).
1b. TWO INDEPENDENT ARITHMETIC PATHS, machine-executed (never hand-typed): 51920*1024 = 53166080 AND (220*32)*(236*32) = 7040*7552 = 53166080. Record the additional falsifier: 51920*32 = 1661440 != 1664000 (the old printed total is derivable from NO valid arithmetic over these denominators). Also verify the per-tile denominator 32x32 = 1024 sample slots from the existing format evidence (R1 F03 section 7.2 B: "32x32 uint16 LE at payload offset 64"; the same file 9216/9216 samples for 9 region tiles = 9*1024 internal consistency; committed canon: M1 gate matrix "220x236 = 51,920 regular" + CORRECTION_LEDGER.md PE-MASTER physical name census). Output JSON to 03_EVIDENCE.
1c. R2-F02 VCL REVIEW ERRATUM. Write 03_EVIDENCE/scripts/r2_f02_vcl_arithmetic.mjs: recompute the BAD equation LHS 491*12+24+252 = 6168; re-derive the valid relations from the R1 census artifact per_file rows (parse predecessor/03_EVIDENCE/F02_VCL_CENSUS.json raw rows - do NOT trust its totals block): sum lines = 492, sum tokens = 5916, sum groups = 493, sum success records = 472, 25.vcl = 21 lines / 252 tokens / 21 groups; verify (491+1+1)*12 = 5916 (group-level: 491 numeric lines + 1 continuation extra group + 1 comma group = 493 groups); 493-21 = 472; 472*12+252 = 5916 (file-level); and the exact double-count decomposition: 6168-5916 = 252 = 240 (25.vcl 20 numeric lines x 12, already inside 491x12) + 12 (the 9.vcl continuation line FIRST group, already inside 491x12; the +24 term re-adds BOTH its groups). Verify numeric_rows_12cols = 491 from predecessor/03_EVIDENCE/F02_ITER032K_RERUN_vcl_columns.json. DO NOT modify: original payloads, the decoder, the census JSON, comma behavior. DO NOT infer original-client comma semantics. Bounded repo check: search tracked repo files for the bad-equation text variants ("491x12 + 24 + 252", "491*12 + 24 + 252", "491 × 12 + 24") - expected 0 hits (the defect existed only in the human-pasted PE_MASTER_REVIEW relay, never in a repo file); record the search space + result.
1d. R2-P3 EVIDENCE LABEL. Read predecessor/03_EVIDENCE/DIFF_PEFoliageCore.js.patch in full + your fresh live git diff; classify: comment lines + ONE documentation-metadata string (FOLIAGE_OPERAND_LOCK.exactness); NO arithmetic change; NO parser change; NO control-flow change; NO placement change. Verify the mislabel site: EVIDENCE_INDEX.csv row for DIFF_PEFoliageCore.js.patch (line 10) currently reads "Byte-exact git diff of the authorized comment-only exactness-wording correction". Bounded scan: confirm no OTHER live R1-package file mislabels the PEFoliageCore change as comment-only (PE-MASTER grep found the remaining "comment-only" hits are either VegetationClimateDecoder-scoped-accurate or already-precise "comment-only (PEFoliageCore.js additionally: ...)" phrasings); record the scan.

## PHASE 2 - BEFORE-IMAGE PRESERVATION (MANDATORY before any edit)

2a. Create the R2 package skeleton: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/ with 00_CONTROL, 01_RAW, 02_ANALYSIS, 03_EVIDENCE/BEFORE_IMAGES, 03_EVIDENCE/scripts, 06_REPORT.
2b. Binary-copy (fs.copyFileSync - byte-for-byte) the three EDIT TARGETS into 03_EVIDENCE/BEFORE_IMAGES/: BEFORE_F03_TERRAIN_TEXTURE_SCOPE.md, BEFORE_EVIDENCE_INDEX.csv, BEFORE_MANIFEST_SHA256.csv.
2c. Record for each: ORIGINAL_REPOSITORY_PATH, PRESERVED_COPY_PATH, ORIGINAL_SIZE, ORIGINAL_SHA256, PRESERVED_COPY_SHA256, BYTE_IDENTITY (YES/NO). BYTE_IDENTITY = YES (hash + size + byte-compare) required for ALL THREE before any edit. Any failure -> STOP, no edits.

## PHASE 3 - THE THREE AUTHORIZED PREDECESSOR EDITS (only after 2c passes; ONLY these three)

3a. EDIT A - predecessor/02_ANALYSIS/F03_TERRAIN_TEXTURE_SCOPE.md, ONLY the incorrect sample-total statement (line 102).
    OLD exact span: "- SAMPLE DIMENSIONS: 32x32 u16 per tile (1,664,000 samples over 51,920 tiles)."
    NEW text (semantic requirements; wrap to the file hard-line style; this statement only; NOTHING else in the file changes): the total is 53,166,080 u16 SAMPLE SLOTS across the 51,920 regular 32x32 tile blocks; explicitly label: sample slots, NOT unique height values, NOT unique world points, NOT historical rendering coverage, NOT terrain-texture coverage, NOT original-client parity, NOT proof of the RGB-TDF bridge; include the correction attribution EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927 and the two arithmetic paths (51920 x 1024 and (220x32) x (236x32), both = 53,166,080). PRESERVE untouched: BRIDGE_STATUS = UNKNOWN (line ~115) and every calibration/unknown label elsewhere in the file.
3b. EDIT B - predecessor/03_EVIDENCE/EVIDENCE_INDEX.csv, ONLY the description field of the DIFF_PEFoliageCore.js.patch row (line 10).
    OLD field value: "Byte-exact git diff of the authorized comment-only exactness-wording correction"
    NEW field value: "Byte-exact git diff of the authorized correction: comment lines + ONE documentation-metadata string (FOLIAGE_OPERAND_LOCK.exactness) - no arithmetic/parser/control-flow/placement change (label corrected by EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927)"
    The row stays ONE line, 5 fields, strict RFC4180 parse. The patch bytes are NOT regenerated or modified.
3c. EDIT C - predecessor/06_REPORT/MANIFEST_SHA256.csv, ONLY the rows of the two files edited in 3a/3b: update sha256 + size_bytes to your fresh post-edit values. Row order preserved; 48 data rows + header; self-excluded (the manifest is NOT listed in itself); repo-relative paths unchanged; NOTHING else in the manifest changes.
3d. Record per edited file: BEFORE_SHA256 / AFTER_SHA256 / BEFORE_SIZE / AFTER_SIZE / EXACT_CHANGE / WHY_AUTHORIZED / CORRECTION_EDGE. Produce exact unified diffs (before->after) of all three edits into 03_EVIDENCE (EDIT_A_F03.diff, EDIT_B_EVIDENCE_INDEX.diff, EDIT_C_MANIFEST.diff).

## PHASE 4 - AUDIT_ENTRYPOINT ROW (the ONLY tracked-file edit of this run)

4a. Add EXACTLY ONE row at the TOP of the LATEST RUNS table (above the R1 row; the table is newest-first), in the table existing format. ALL existing rows byte-preserved. Verify: "git diff --numstat AUDIT_ENTRYPOINT.md" becomes 2/0; the vs-HEAD diff contains ONLY the 2 added rows (the R1 row + your new R2 row); zero deletions.
4b. Row content (ONE table line, no embedded newlines; keep the 5-cell pipe structure). Required meaning: RUN_ID EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927 (RUN_CLASS LOAD_BEARING; RUN_TYPE GATE_C_R2_BOUNDED_COUNTER_CORRECTION; executor pe-reconstruction, PE-MASTER-dispatched correction run, dispatcher contract in the package 00_CONTROL/RUN_CONTRACT.md; STATIC-ONLY - the client never ran) | purpose: the bounded correction of the Desktop Gate-C R2 findings (GATEC_REAUDIT_R2_REPORT_20260927, verdict MILESTONE_POST_AUDIT_PARTIAL): R2-F01 the F03:102 terrain sample counter 1,664,000 -> 53,166,080 u16 SAMPLE SLOTS across the 51,920 regular 32x32 tile blocks (regular-tile census re-derived from the pinned terrain.bnt 95841761...; two independent arithmetic paths; sample slots, NOT unique heights / coverage / parity); R2-F02 the VCL review-arithmetic erratum (the pasted-review equation 491x12+24+252 actually equals 6,168; correct relations (491+1+1)x12 = 5,916 and 472x12+252 = 5,916; raw census 493/5,916 UNCHANGED and valid; no repo file contained the bad equation); R2-P3 the EVIDENCE_INDEX DIFF_PEFoliageCore label corrected to comments + ONE metadata string (no behavior change); predecessor edits A/B/C with byte-identical BEFORE_IMAGES preserved in the R2 package; the predecessor R1 successor package is persisted by this run human-authorized Commit 1 (supersedes the R1 row "uncommitted" label) | verdict cell: PE-MASTER final audit + fresh INTERNAL_QC recorded in the run package 06_REPORT (advisory; CANONICAL_GATE_EFFECT = NONE while Q1 absent); Desktop R2 historical verdict MILESTONE_POST_AUDIT_PARTIAL stands; Gate A = PASS per the independent Desktop R2 audit; Gate C = REQUIRES_INDEPENDENT_DESKTOP_REAUDIT (this run claims NO Gate C PASS, NO MILESTONE_POST_AUDIT_PASS); Q1 NOT executed; Gate B canonical authority = BLOCKED (Q1 absent); M1 = OPEN; M2 = NOT AUTHORIZED; Viewer = NOT AUTHORIZED.

## PHASE 5 - R2 PACKAGE CONTENT (bounded; the minimum list; no evidence duplication)

- 00_CONTROL/RUN_CONTRACT.md (materialize THIS contract verbatim + a short header: dispatcher PE-MASTER, NO_NESTED_TASKS, STATIC-ONLY)
- 00_CONTROL/SOURCE_INDEX.md (every input read: path, class/era, size, SHA256, role)
- 00_CONTROL/BASELINE_PIN.md (git pin at start; hash-pin table: expected vs YOUR fresh value, MATCH/DIFF per row)
- 01_RAW/FINDINGS.csv (header + rows R2-F01, R2-F02, R2-P3; fields at least: finding_id, desktop_claim, verification_method, measured_quantity, denominator, independent_source, why_non_circular, result, correction_edge, affected, unaffected, blast_radius, open_residue; strict CSV)
- 01_RAW/MODIFIED_PATHS.csv (the 3 predecessor edited paths + AUDIT_ENTRYPOINT.md; fields: path, change_class, authorization, before_sha256, after_sha256, before_size, after_size, exact_change, correction_edge)
- 01_RAW/CORRECTION_EDGES.csv (edge_id R2-F01-COUNTER / R2-F02-ERRATUM / R2-P3-LABEL; old_state, new_state, evidence_pointer, authorization, scope)
- 02_ANALYSIS/R2_F01_TERRAIN_SAMPLE_COUNTER.md (full record per 1a/1b + the SAFE SEMANTIC: 53,166,080 SAMPLE SLOTS ACROSS THE 51,920 REGULAR 32x32 TILE BLOCKS + the EXPLICIT NOT-list: NOT unique height values; NOT unique world points; NOT historical original-client parity; NOT historical rendering coverage; NOT terrain-texture coverage; NOT proof of the RGB-TDF bridge; BRIDGE_STATUS = UNKNOWN preserved; calibration labels preserved)
- 02_ANALYSIS/R2_F02_VCL_REVIEW_ERRATUM.md (OLD_STATEMENT = the human-pasted PE_MASTER_REVIEW equation "491x12 + 24 + 252 = 5916"; WHY_WRONG = the LHS is 6,168; CORRECT_ARITHMETIC = both valid relations + the population identities; POPULATION_OVERLAP = the exact 240 + 12 = 252 double-count decomposition and WHICH populations overlap (the 491 numeric lines already include 25.vcl 20 numeric lines and the continuation line first group); AFFECTED_CLAIMS = the pasted review arithmetic ONLY (repo-wide search record; expected 0 repo hits); UNAFFECTED_CLAIMS = the raw census 32/492/5,916/493/6/31/1/472 and all R1 package contents; BLAST_RADIUS; note the pasted review is a chat-relay artifact - no repo file contained the equation)
- 02_ANALYSIS/R2_P3_EVIDENCE_LABEL.md (the label-correction record with the patch class verification)
- 02_ANALYSIS/BLAST_RADIUS.md (dependency-census discipline: old counter 1,664,000 - bounded search of tracked repo files for dependents, expected NONE, record the search; review equation - pasted-review only; evidence label - descriptive metadata only; per-item dispositions PROVEN_AFFECTED / POTENTIALLY_AFFECTED / PROVEN_UNAFFECTED / DEPENDENCY_UNKNOWN)
- 02_ANALYSIS/SELF_ADVERSARIAL_PASS.md (rows CLAIM/FALSIFIER/TEST/INDEPENDENT_SOURCE/RESULT/IMPACT for: the tile census; the 1024 denominator; both arithmetic paths; the VCL sums; the double-count decomposition; the patch class; the before-image byte identity; the entrypoint row survival)
- 03_EVIDENCE/BEFORE_IMAGES/ (the 3 byte-exact copies + BEFORE_IMAGE_METADATA.csv with the 6 record fields per file)
- 03_EVIDENCE/scripts/ (r2_f01_terrain_counter.mjs, r2_f02_vcl_arithmetic.mjs, + any patch-class check script)
- 03_EVIDENCE/ (R2_F01_TERRAIN_COUNTER.json + R2_F02_VCL_ARITHMETIC.json outputs; EDIT_A_F03.diff, EDIT_B_EVIDENCE_INDEX.diff, EDIT_C_MANIFEST.diff; AFTER_IMAGE_HASHES.csv: path, after_sha256, after_size for the 3 edited files + AUDIT_ENTRYPOINT.md)
- 06_REPORT/REPORT.md (POM s15 20-point report for this bounded run: human-decision block first; RUN_ID + state delta; method; per-finding results; gates table; NOT_CHECKED; handoff block)
- 06_REPORT/HANDOFF.md (AUDIT_OUTPUT_ROOT / FINAL_REPORT_PATH / PRIMARY_EVIDENCE_PATHS / RUN_STATUS / HARD_STOP_REASON)
- 06_REPORT/STAGE_ACCEPTANCE_GATES.csv (rows: R2_F01_COUNTER, R2_F02_VCL_ERRATUM, R2_P3_LABEL, BEFORE_IMAGES, PREDECESSOR_MANIFEST, R2_MANIFEST, CSV_SCHEMAS, SOURCE_FREEZE, PATCH_IDENTITY, ENTRYPOINT_ROW_SURVIVAL, UNAUTHORIZED_CHANGED_PATHS, OPEN_P0P1P2[QC_PHASE], INTERNAL_QC[QC_PHASE], PE_MASTER_VERDICT[PERSIST_PHASE], FINAL_REVIEW_INVENTORY[PERSIST_PHASE], MILESTONE_STATE_ASSERTIONS; fields: stage_gate_id, check, result, evidence, notes; result vocabulary PASS / FAIL / PENDING_<PHASE>)
- 06_REPORT/MANIFEST_SHA256.csv (ALL R2 package files; repo-relative paths; sha256,size_bytes; self-excluded; computed LAST after every other file is final; 0 missing / 0 stale on re-hash)

FILE DISCIPLINE: all new text files UTF-8 WITHOUT BOM, LF-only, no U+FFFD; write text via node fs.writeFileSync (PowerShell 5.1 Set-Content adds a BOM - do not use it for package files); before-images via binary copy; no proprietary payloads into the repo (identity metadata only); package manifests exclude themselves; NO inventory -> manifest -> inventory hash cycles.

## PHASE 6 - PRELIMINARY DETACHED PRE-QC SNAPSHOT (CHECKPOINT_A; OUTSIDE the repo)

Create C:\Users\User\AppData\Local\Temp\opencode\EU935_M1_R2_20260927\PRE_QC_SNAPSHOT\PRE_QC_SNAPSHOT.csv: for EVERY file of the predecessor R1 package (49), the new R2 package (all), AUDIT_ENTRYPOINT.md, and both frozen sources: path, size, sha256, mtime_utc. Plus GIT_INDEX_STATE.txt (git status --porcelain + git diff --numstat + git diff --cached --name-status outputs). This snapshot detects mutation during review; it is NOT the final reviewed inventory; NO repo manifest may reference or hash it.

## PHASE 7 - SELF-VERIFY + HANDOFF

- Re-verify: each of the 3 predecessor edits changed EXACTLY the authorized span (your unified diffs show only that); frozen sources byte-untouched (fresh live git diff hashes == the patch hashes; numstat 30/6 + 20/5); AUDIT_ENTRYPOINT numstat 2/0, both rows added, zero deletions, all historical rows byte-preserved; git status shape unchanged except the new R2 untracked root; NO staging anywhere.
- R2 manifest census: rows = R2 package file count - 1 (self-excluded); re-hash every row: 0 stale / 0 missing.
- STRICT-parse every CSV you wrote (field count per header; RFC4180).
- Return a compact delivery notice: what was done; key measured values (regular tiles, both arithmetic paths, VCL sums, the 6,168 decomposition); BEFORE_IMAGES BYTE_IDENTITY results; the three after-hashes + entrypoint after-hash; entrypoint numstat; package path; snapshot path; any deviation. FULL details live in the package REPORT/HANDOFF.

## HARD STOPS (record + stop; do not edit beyond)

any hash-pin mismatch; byte-identity failure; unexpected git state; any need to touch a path outside the authorized set; source-byte drift; evidence contradicting a Desktop finding in a way that makes a correction unsafe (report - do NOT force the correction).

## FORBIDDEN

editing src/pesource/VegetationClimateDecoder.js or src/peworld/PEFoliageCore.js (FROZEN - byte-identical to the Desktop-R2-audited state); regenerating or modifying the accepted patch bytes; editing any historical package other than the three authorized spans; touching docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ or experiments/; Q1; POM edits; M2; Viewer; client/GPU; comma normalization; parser changes; broad cleanup or encoding normalization; git add/commit/push; editing anything under C:\Users\User\Documents\ChatGPT\PE.
