<!-- PROVENANCE: worker = pe-master-auditor (persistence phase of PE-MASTER loop dc98463f-f199-4a1a-8b96-c33a59ab6ecb); date = 2026-09-27; -->
<!-- SOURCE (verbatim copy): C:\Users\User\AppData\Local\Temp\opencode\EU935_M1_R2_20260927\RE_QC_WORKSPACE\RE_QC_REPORT.md — source sha256 = d44f80aeeb1eb958a3aa1b1d68eff8bf7172359b6b5aa60241a59543b231c2e8, 25696 bytes -->
<!-- NOTE: the bytes below this 3-line header are the source report copied VERBATIM (node fs byte copy); nothing below was added, removed or edited. -->
# RE-QC REPORT — EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927 (post-fix-batch fresh-context re-QC)

- RUN_ID: EU935_M1_R2_RE_QC_POST_FIX_BATCH_20260927
- PARENT_LOOP_ID: PE-MASTER EU935-M1 Gate C R2 QC repeat (fresh-context INTERNAL_QC over the final state after the bounded P3 fix batch)
- ASSIGNMENT_MODE: INTERNAL_QC (READ-ONLY re-QC; NO_NESTED_TASKS; NO mutations inside D:\Eudoria_Reconstruction; NO git operations that change state)
- WORKER: pe-master-auditor (fresh session; had NOT seen this run before)
- DATE: 2026-09-27
- SCOPE: verify QC_P3_FIX_BATCH.md (FIX-1..FIX-6) + repeat the load-bearing QC invariants on the final state. Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (HEAD cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d).
- Skill used: pe-bnt-tdf (C:\Users\User\.opencode\skills\pe-bnt-tdf\SKILL.md) — BNT2 trailer layout for the independent terrain.bnt parse. Era scope checked (terrain.bnt 9.3.5 = 58,451 entries / 125,064,817 B matches the skill's control-plane census).
- All scripts/outputs of this re-QC live ONLY in C:\Users\User\AppData\Local\Temp\opencode\EU935_M1_R2_20260927\RE_QC_WORKSPACE\ (script_A_terrain.js, script_B_repo.js + script_B_results.json, script_C_package.js + script_C_results.json, script_D_reconstruct.js, script_D2_report.js, script_E_entrypoint.js, diff_foliage.patch, diff_vcl.patch, head.tar + head_tree/ extracted HEAD archive).

## VERDICT

**QC_PASS_WITH_FINDINGS** — OPEN_P0 = 0, OPEN_P1 = 0, OPEN_P2 = 0 (=> not QC_FAIL). All six dispatched fixes verified; all load-bearing invariants re-verified on the final state. ONE new bounded P3 (P3-RE-1, documentation self-consistency of the new batch record itself — same class as the original P3-QC-3) + one sub-P3 wording observation. Non-blocking; no scientific claim, measurement, gate, or milestone assertion is affected. The two carried residues (P3-QC-4, P3-QC-5) remain correctly disclosed and untouched.

---

## 1. PER-FIX VERIFICATION (each independently re-measured)

### FIX-1 — dir_off phrase (P3-QC-1): VERIFIED (CONFIRMED, re-derived from RAW BYTES)
- 02_ANALYSIS/R2_F01_TERRAIN_SAMPLE_COUNTER.md line 16 reads exactly `(dir_off = 123,369,726, recorded in the JSON; count = 58,451).` (file read in full).
- 03_EVIDENCE/R2_F01_TERRAIN_COUNTER.json: bnt2.dir_off = 123369726, count = 58451, index consumed exactly at filesize-8. Confirmed.
- INDEPENDENT RE-DERIVATION (own parser written fresh from the BNT2 trailer layout; NOT the run's generator):
  - terrain.bnt (D:/Eudoria_Reconstruction/pcg_install/Data/Terrain/terrain.bnt) SHA256 = 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990 (pin MATCH), size 125,064,817 B.
  - Trailer [dir_off u32]["BNT2"] at filesize-8 => dir_off = 123,369,726. At dir_off [count u32] => 58,451. Index consumed EXACTLY (parsed bytes == filesize-8-start, 0 structural errors).
  - Full census reproduced: 58,451 entries, all eight-hex .tdf; regular 51,920 (x: 220 distinct, contiguous 0..219; y: 236 distinct, contiguous 0..235); special 6,530 (y 0xff1a..0xffff; x-range 0..217); sentinel 1 (7ffe7ffe.tdf); duplicates 0; unclassified 0; 51,920+6,530+1 = 58,451.
- "24608" is absent from R2_F01 (and from every package file except the fix record's own OLD-span quote + its explicitly-not-re-derived attribution note). The garbled phrase is gone.

### FIX-2 — "9,916" typo (P3-QC-2): SUBSTANTIVE FIX VERIFIED; new P3 in the record (see 3.1)
- 02_ANALYSIS/SELF_ADVERSARIAL_PASS.md row 2 TEST cell reads `9,216/9,216 region-tile samples = 9 x 1,024 internal consistency` (file read in full). No "9,216/9,916" remains.
- Package grep "9,916": 0 occurrences in the 34 non-record package files (including SELF_ADVERSARIAL_PASS.md); "9916" bare: 0 anywhere.
- QC_P3_FIX_BATCH.md itself contains 4 quoted occurrences of "9,916" (lines 52 heading, 58 OLD-span, 70 and 71 grounds) — all unambiguous correction-documentation; see finding P3-RE-1 for the record's falsified absolute claim.

### FIX-3 — timing-explicit dual-phase dependent-search record: VERIFIED (CONFIRMED; every value re-measured)
- Both rewritten records in place and read in full: R2_F01 section 5 (phases (a)-(d)) and BLAST_RADIUS section 1 ((a)-(d) + per-item dispositions).
- (a) Phase-1: 133,463,531 B — re-derived: measured tracked total 133,465,692 B minus the R2 entrypoint row 2,161 B = 133,463,531 B. ZERO tracked hits in the pre-R2-row state: verified — every currently-tracked file except AUDIT_ENTRYPOINT.md line 30 has 0 matches for "1,664,000"/"1664000"/"1.664.000", and line 30 IS the R2 row.
- (b) Post-Phase-4: tracked total measured = 133,465,692 B (2,594 tracked files). Exactly ONE tracked hit = AUDIT_ENTRYPOINT.md line 30 ("1,664,000" at line 30, col 6206 — the R2 registration row, correction-describing text). HEAD (cc747df) = ZERO hits — verified by a full byte-level search over an extracted `git archive HEAD` tree (2,594 files, 133,457,093 B): 0 hits for all three old-counter literals AND all equation patterns. R1 registration row (line 31) = 0 (the only entrypoint hit is at line 30).
- (c) R1 package (49 files): exactly ONE occurrence = F03_TERRAIN_TEXTURE_SCOPE.md line 104 (inside the corrected statement, lines 102-112, quoting the superseded value; the record's "line 104" = the literal's location, consistent with BLAST_RADIUS's "line 102" = the statement start). Not a live dependent.
- (d) Worktree-wide (3,914 files excluding .git): 63 old-counter matches = 1 entrypoint + 1 R1-F03 + 61 in the R2 package — every one a correction description (package records, before-image, EDIT diffs, generator scripts, evidence JSONs); ZERO live dependents; ZERO matches in PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/, experiments/, or any other untracked location.
- Arithmetic closure of the record's batch-start census: 63 (now) - 20 (QC_P3_FIX_BATCH.md's own quoted occurrences) = 43 = 1 + 1 + 41 — EXACTLY the record's "43 occurrences at batch start". Worktree file census 3,914 = 3,913 (batch start) + 1 (the new record). Closes exactly.
- THE OLD FALSIFIABLE INCONSISTENCY IS GONE: every "133,463,531" occurrence in the package (24 sites listed and context-checked) is now Phase-1-scoped with 0 hits or the timing-clause text; every ONE-hit claim is paired with 133,465,692 B. No text pairs 133,463,531 B with a hit.

### FIX-4 — equation search-timing/self-hit clauses (P3-QC-3): VERIFIED (CONFIRMED; searches re-run)
- All 5 sites in place and read in full: R2_F02_VCL_REVIEW_ERRATUM section 5 (after "— 0 HITS."), BLAST_RADIUS section 2 (after "RESULT: 0 hits."), SELF_ADVERSARIAL_PASS row 9 TEST cell (appended), REPORT.md section 4 and section 7.
- Wording verified: each clause scopes Phase 1 to the pre-edit worktree (133,463,531 B; "the R2 entrypoint row and this package's own records did not yet exist") and scopes post-run occurrences to "this run's own quoted-as-false correction records — this package's own records and the new AUDIT_ENTRYPOINT.md R2 row — no repo file asserts it."
- Searches re-run (literals "491x12 + 24 + 252", "491*12 + 24 + 252", "491 × 12 + 24" + regex /491\s*[x*×]\s*12\s*\+\s*24/):
  - tracked worktree: literals = 0; regex = EXACTLY ONE = AUDIT_ENTRYPOINT.md line 30 (match "491x12+24" inside the row's quoted-as-false text "the pasted-review equation 491x12+24+252 actually equals 6,168"). Matches the executor's claim exactly.
  - HEAD (full 2,594-file archive): 0 literals, 0 regex.
  - worktree-wide: 36 regex matches = 1 entrypoint + 35 in the R2 package; 0 in the R1 package, NINODE root, experiments/, or any other location; all package occurrences are quoted-as-false correction records.
  - Arithmetic closure: 35 (package now) - 3 (the record's own quoted literals) = 32 = the record's batch-start package count; 36 = 1 + 32 + 3 closes with the record's "33 at batch start = 1 entrypoint + 32 in this package". The 5 inserted clauses added ZERO equation-string occurrences.

### FIX-5 — the batch record itself: VERIFIED (CONFIRMED — before-hashes mechanically reproduced)
- 00_CONTROL/QC_P3_FIX_BATCH.md exists (19,108 B; hash b7535db53677ea5760bcd39fe6a8a8ac241611734acd9476b6114812feb0d793 = its MANIFEST_SHA256.csv row; UTF-8 no BOM, LF-only, no U+FFFD).
- AFTER hashes vs current bytes: ALL MATCH — R2_F01 fc5cec19.../4,419; BLAST_RADIUS 34339b39.../5,368; SELF_ADVERSARIAL 0d64ec62.../6,772; R2_F02 f1c7dff5.../4,292; REPORT e7ebfb53.../15,221.
- BEFORE hashes: MECHANICALLY VERIFIED by reconstruction — reversing the record's exact OLD-span quotes (parsed from the record's own fenced blocks) on the current bytes reproduces each pre-batch file EXACTLY:
  - R2_F01: 3,993 B / 10e77ed1bb6038101d15de04b4a731d91801b564c101fcb50421c8bbb9b31a12 — MATCH
  - SELF_ADVERSARIAL: 6,673 B / aa810fb6c554c4bea0bd0f38ec6b2c70e7375d3647331bc92bb5504f0d268a46 — MATCH
  - BLAST_RADIUS: 4,463 B / 9fdd9d2b5e635b2d6051ccd89be4a9feeecd43fc940267f371dfbf071ab98f01 — MATCH
  - R2_F02: 3,848 B / 849c03658ec8bf3494d3ca14c1b387de6accef09286713a654cf5328f5fc252b — MATCH
  - REPORT: 14,543 B / 8d34dae617357798863441bf636341a9e71ddfea4990cffdda134dcc30ffeb65 — MATCH
  Therefore the record's before-hashes, OLD-span quotes and transformation descriptions are exactly consistent with reality. Negative controls: every OLD span is absent from the current files; every inserted clause occurs exactly once.
- The manifest's pre-batch hash (d6d302a7.../5,513 B) is NOT verifiable from disk (the file was regenerated; no history copy exists in the repo; the first QC's report is not in the repo). Per the dispatch's fallback, the after-verification applies; the pre-batch value is plausible (34 pre-batch files => 33 rows; +1 row growth consistent with +160 B).
- Observation (sub-P3 wording nit, no formal number): FIX-4's preamble "(add-only; the surrounding substance is byte-unchanged)" is word-level true but byte-level loose at site 4 — the insertion re-wrapped the following words ("NO repo edit was required" -> "NO repo edit was\n  required", +2 B). The record's own site-4 insertion-point quote documents the continuous pre-batch phrase and the before/after hashes pin the exact bytes, so the transformation is fully disclosed; no measurement depends on the parenthetical.

### FIX-6 — manifest refresh: VERIFIED (CONFIRMED; every row re-hashed)
- 06_REPORT/MANIFEST_SHA256.csv = header + 34 data rows (strict 3-field parse, 0 unbalanced quotes); R2 package = 35 files (walk) = 34 rows + 1 self-excluded.
- Full independent re-hash of ALL 34 rows against disk: 0 stale / 0 missing / 0 size mismatch / 0 unlisted / 0 phantom rows. Self-exclusion verified. All paths repo-relative (docs/audits/...). QC_P3_FIX_BATCH.md row present with the correct fresh hash.
- The generator (03_EVIDENCE/scripts/r2_manifest.mjs, read to EOF) computes exactly what the record claims (walk, sort, repo-relative, self-exclude, 3 columns, then a built-in re-hash pass); my independent re-hash (different code) confirms the output equals reality.

---

## 2. REGRESSION SWEEP (each re-measured)

a. FROZEN SOURCES: numstat = 30/6 (src/pesource/VegetationClimateDecoder.js) + 20/5 (src/peworld/PEFoliageCore.js). Live raw patch buffers via `git diff --output` to temp files (no PowerShell piping): 27DEE19810FDED98FBE37E2013B742DA500BCD107AD0C85FEAFBCCDBF1EA96DD / 3,377 B and 5978FF6B3CD9C787284B829E59D8CCCF18D14D0FA956B6D760D86C4278728723 / 3,389 B — BOTH EXACT MATCH to the pins. PASS.

b. GIT STATE: HEAD = cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d; `git diff --cached --name-status` EMPTY (no staging); `git status` shape = exactly 3 tracked modified (AUDIT_ENTRYPOINT.md, src/pesource/VegetationClimateDecoder.js, src/peworld/PEFoliageCore.js) + 4 untracked roots: R1 package (49 files, verified by walk), R2 package (35 files), docs/audits/PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/, experiments/. Tracked census 2,594. PASS.

c. ENTRYPOINT: numstat 2/0; the vs-HEAD diff is one hunk @@ -29,0 +30,2 @@ containing ONLY the 2 added rows (line 30 = R2 row, 2,161 B incl. LF; line 31 = R1 row, 3,269 B); zero deletions; ALL historical rows byte-preserved (verified line-by-line against the extracted HEAD tree). After-hash A0F21829B8440E5183AEDC6B16337BF5E971C005A3485C19442B22F07444E8F0 / 115,846 B = current bytes; before-pin 8EEC84E65C19B56705B023AADAB27B5AD0A05E03686E5992F4C47A4836BEE45E / 113,685 B reproduced EXACTLY by reconstructing HEAD-entrypoint + R1 row. R2 row gate language: "MILESTONE_POST_AUDIT_PASS" occurs exactly ONCE, inside the negation "(this run claims NO Gate C PASS, NO MILESTONE_POST_AUDIT_PASS)"; "MILESTONE_POST_AUDIT_PARTIAL" appears only as the verbatim historical Desktop verdict label; no positive gate claim anywhere in the row. PASS.

d. PREDECESSOR EDITS CONFINED: F03_TERRAIN_TEXTURE_SCOPE.md = 72e1e22149405f4921ca69d36c8adb2e5a776b4de3acba2db5f67f0e82662ffb / 10,534 B; EVIDENCE_INDEX.csv = 67bfee8c15fac242ec079bba85f752c5b47a80b64a764cf3b0e6f5dece910443 / 7,710 B; R1 MANIFEST_SHA256.csv = a57aa321bdbbb0baa704fe714843b9e418de44a91ced4ba53232c88642fe957f / 8,521 B — ALL MATCH. BEFORE_IMAGES: BEFORE_F03 = 5704d1c8f8166fe5bf1b88b0e8d0b13e7a0de3ac83463bdaf920831e863489df / 9,807 B; BEFORE_EVIDENCE_INDEX = 02e03b7d073e5579123a95b03383bac26cebff46e83a24b36a1693caedd05b08 / 7,536 B; BEFORE_MANIFEST = 3a91f3a3505f6f3d46edee246ff91e26b373586d32803e57e18d6da4d1c46462 / 8,520 B — ALL MATCH. PASS.

e. R1 MANIFEST FULL RE-HASH: 48 data rows + header over the 49-file R1 package; independent re-hash of every row: 0 stale / 0 missing / 0 unlisted; self-excluded. (This also PROVES the fix batch did not modify any R1 package file.) PASS.

f. ARITHMETIC SPOT RE-EXECUTION: 51920*1024 = 53166080; (220*32)*(236*32) = 7040*7552 = 53166080; 491*12+24+252 = 6168; (491+1+1)*12 = 5916; 472*12+252 = 5916; 6168-5916 = 252 = 240+12. ALL REPRODUCED. PASS.

g. PACKAGE HYGIENE: all 7 package CSVs strict-parse at consistent field counts with 0 unbalanced-quote fields (FINDINGS 13 fields x 3 rows; MODIFIED_PATHS 9 x 4; CORRECTION_EDGES 6 x 3; AFTER_IMAGE_HASHES 3 x 4; BEFORE_IMAGE_METADATA 6 x 3; MANIFEST_SHA256 3 x 34; STAGE_ACCEPTANCE_GATES 5 x 16). All 35 package files: valid UTF-8 (byte round-trip), no BOM, no U+FFFD; LF-only (CR count = 0) for 34/35 files — the single exception is 00_CONTROL/RUN_CONTRACT.md with exactly ONE CR at position size-2 (final-line CRLF), which is the pre-existing, disclosed, PE-MASTER-accepted P3-QC-5 (disclosed in BASELINE_PIN.md S0 deviation record and HANDOFF.md deviation 3; the fix batch's census did not touch RUN_CONTRACT.md; the 5 edited files + the batch record all have CR count = 0). PASS.

h. PENDING GATES: 06_REPORT/STAGE_ACCEPTANCE_GATES.csv: OPEN_P0P1P2 = PENDING_QC_PHASE; INTERNAL_QC = PENDING_QC_PHASE; PE_MASTER_VERDICT = PENDING_PERSIST_PHASE; FINAL_REVIEW_INVENTORY = PENDING_PERSIST_PHASE. NOT flipped by this re-QC (the gate flip belongs to PE-MASTER's process). PASS.

---

## 3. ADJUDICATION

### 3.1 New findings introduced by the fix batch

**P3-RE-1 (new, bounded): QC_P3_FIX_BATCH.md's FIX-2 grounds contain a falsifiable absolute claim contradicted by the record's own quoted documentation**
- Source: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/00_CONTROL/QC_P3_FIX_BATCH.md, line 71: `cell) and ZERO times post-fix; there is no 9,916 anywhere.`
- Effect/contradiction: the final package contains 4 occurrences of "9,916", all inside this same record (line 52 heading `"9,916" typo`, line 58 OLD-span quote `9,216/9,916 -> 9,216/9,216`, lines 70/71 the grounds quotes). The claim was true at its measurement moment (post-FIX-2, before the record was authored) but is unscoped and is now falsifiable against the final state. Additionally, the record's self-hit disclosure (lines 325-329) enumerates only "the old-counter literals and the equation string" as self-quoted, omitting its "9,916" (and "24608") quotes. This is the same defect class as the original P3-QC-3 (a measurement claim without self-hit timing scoping), now inside the correction record itself.
- Materiality: NONE beyond the record's self-consistency. The substantive P3-QC-2 fix is correct and verified (0 occurrences in every load-bearing file; the quoted occurrences are unambiguous correction documentation). No scientific claim, measurement, gate, count, or downstream artifact depends on the sentence. The dispatch's parenthetical expectation "no '9,916' anywhere in the package — grep to confirm 0 occurrences" therefore does NOT hold literally (4 quoted occurrences in the record), while the substantive fix does.
- Narrow correction (for PE-MASTER to dispatch if adjudicated): scope the sentence to its measurement moment (e.g., "as measured immediately post-fix, before this record was authored: 0 occurrences in the package; the only '9,916' strings in the final package are this record's own quoted-as-old documentation") and extend the self-hit disclosure enumeration to include the "9,916" and "24608" quotes.
- Revalidation predicate: package grep finds "9,916" ONLY inside QC_P3_FIX_BATCH.md quoted-documentation spans; the grounds sentence is time-scoped; the disclosure enumeration lists all self-quoted literals; re-hash of the record + manifest row refresh.

Sub-P3 observation (no formal number): FIX-4 preamble "(add-only; the surrounding substance is byte-unchanged)" is byte-level loose at site 4 (2-byte rewrap of the following words), while the record's exact quotes and before/after hashes fully disclose the transformation. No action required; noted for the record's precision standard.

NO P0 / P1 / P2 defects were introduced by the fix batch.

### 3.2 The five original P3s

- P3-QC-1 (garbled dir_off phrase): RESOLVED — FIX-1 verified, dir_off independently re-derived from the terrain.bnt raw bytes (123,369,726; count 58,451; full census reproduced).
- P3-QC-2 ("9,916" typo): RESOLVED in the load-bearing file — row 2 reads 9,216/9,216; 0 occurrences in all package files except the batch record's own quoted documentation (=> new P3-RE-1 on the record's absolute claim).
- P3-QC-3 (missing equation search-timing/self-hit disclosure): RESOLVED — all 5 clauses in place with verified wording; all searches re-run; the disclosed occurrence structure confirmed exactly (tracked regex = 1 = the entrypoint R2 row quoted-as-false; HEAD = 0; all other occurrences inside this run's own package records).
- P3-QC-4 (F05_EXACTNESS_ORIGIN_PRECISION.md:87 "comment-only" residue): still OPEN and CORRECTLY DISCLOSED, NOT edited — line 86-87 still carries the imprecise lead word; the R1 manifest 0-stale re-hash proves the file is byte-identical to its EDIT-C-era state (the fix batch did not touch it); disclosed in BLAST_RADIUS section 3, R2_P3_EVIDENCE_LABEL section 4, REPORT section 11, SELF_ADVERSARIAL residual-honesty block, HANDOFF deviation 2, and the R2_P3 gate notes. Out of authorized scope, as adjudicated.
- P3-QC-5 (RUN_CONTRACT.md final CRLF): still DISCLOSED-ACCEPTED, unchanged — exactly one CR at the final-line position (size-2), disclosed in BASELINE_PIN S0 deviation + HANDOFF deviation 3; not touched by the batch.

---

## 4. EVIDENCE STATUS VOCABULARY APPLIED

- FIX-1..FIX-6 substantive claims: CONFIRMED (independent re-measurement/re-derivation).
- The record's before-hash table: CONFIRMED (mechanical byte-level reconstruction).
- The record's batch-start census claims (43/33/3,913/2,161): CONFIRMED by exact arithmetic closure against the final state.
- The pre-batch manifest hash (d6d302a7.../5,513 B): UNVERIFIED (pre-batch state not reconstructible from disk; no contradiction).
- "24608 = VegetationClimates.bnt dir_off": UNVERIFIED and explicitly NOT re-derived by the record (not load-bearing for FIX-1; disclosed as such).
- P3-RE-1: CONFIRMED (direct byte-level contradiction inside the record).

## 5. FULL_READ_LOG

Read to EOF (Read tool): QC_P3_FIX_BATCH.md; 02_ANALYSIS/R2_F01_TERRAIN_SAMPLE_COUNTER.md; 02_ANALYSIS/BLAST_RADIUS.md; 02_ANALYSIS/SELF_ADVERSARIAL_PASS.md; 02_ANALYSIS/R2_F02_VCL_REVIEW_ERRATUM.md; 02_ANALYSIS/R2_P3_EVIDENCE_LABEL.md; 03_EVIDENCE/R2_F01_TERRAIN_COUNTER.json; 06_REPORT/REPORT.md; 06_REPORT/HANDOFF.md; 06_REPORT/MANIFEST_SHA256.csv; 06_REPORT/STAGE_ACCEPTANCE_GATES.csv; 00_CONTROL/BASELINE_PIN.md; 00_CONTROL/SOURCE_INDEX.md; 01_RAW/FINDINGS.csv (long lines display-truncated in the reader but fully parsed + grepped programmatically: 13 fields x 3 rows, balanced quotes); 01_RAW/CORRECTION_EDGES.csv; 01_RAW/MODIFIED_PATHS.csv; 03_EVIDENCE/AFTER_IMAGE_HASHES.csv; 03_EVIDENCE/scripts/r2_manifest.mjs. Partial (load-bearing spans + context): R1 F03_TERRAIN_TEXTURE_SCOPE.md lines 98-115 (the corrected statement); R1 F05_EXACTNESS_ORIGIN_PRECISION.md lines 82-91 (the residue); both files' full byte-identity independently proven via the R1 manifest re-hash. Skill pe-bnt-tdf SKILL.md loaded in full. All other package files (incl. all CSVs, JSONs, diffs, BEFORE_IMAGES, scripts) were hashed, byte-searched, encoding-checked and CSV-parsed programmatically.

## 6. NOT_CHECKED

- The pre-batch (batch-start) states not reconstructible from disk: the pre-batch MANIFEST_SHA256.csv bytes (hash d6d302a7... unverifiable; the record's before-SIZES are consistent and the after-state fully verified).
- The first fresh INTERNAL_QC's report (not present in the repo; its findings were adjudicated by PE-MASTER and are quoted by the fix record).
- The R2 run's other generator scripts (r2_f01_terrain_counter.mjs, r2_f02_vcl_arithmetic.mjs, r2_p3_patch_class.mjs, r2_before_images.mjs, r2_edit_diffs.mjs, r2_entrypoint_row.mjs, r2_package_verifications.mjs, r1_*.mjs): not re-run and not read line-by-line — this re-QC re-derived the load-bearing measurements with INDEPENDENT code (own BNT2 parser, own search/CSV/hash tooling), so the generators' internals are not load-bearing for these verdicts; r2_manifest.mjs (the one the batch re-ran) was read to EOF.
- The remote origin/github.com state (no outbound connectivity; the package records this as the S0 deviation; remote verification belongs to the persistence phase).
- VegetationClimates.bnt content re-derivation (hash-pinned only, per the package; not load-bearing for this re-QC).
- The untracked roots PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ and experiments/ contents (outside this re-QC's scope; searched for the correction literals/regex — 0 hits).
- The equation-literal quotation contexts in RUN_CONTRACT.md/FINDINGS.csv/CORRECTION_EDGES.csv were programmatically verified as quoted-as-false; the full RUN_CONTRACT.md body (the human's verbatim dispatcher contract) was hash/CR-checked but not re-adjudicated clause-by-clause (out of re-QC scope; P3-QC-5 covers its only known defect).

## 7. OPEN ITEM COUNTS

- OPEN_P0 = 0
- OPEN_P1 = 0
- OPEN_P2 = 0
- OPEN P3 (new, this re-QC) = 1 (P3-RE-1, bounded documentation self-consistency in 00_CONTROL/QC_P3_FIX_BATCH.md; PE-MASTER adjudication requested)
- Carried disclosed residues unchanged: P3-QC-4 (F05:87 label, open, out of authorized scope) and P3-QC-5 (RUN_CONTRACT.md final CRLF, disclosed-accepted).

## 8. HANDOFF BLOCK

ASSIGNMENT_MODE: INTERNAL_QC (fresh-context READ-ONLY re-QC)
RUN_ID: EU935_M1_R2_RE_QC_POST_FIX_BATCH_20260927
PARENT_LOOP_ID: PE-MASTER EU935-M1 Gate C R2 correction QC repeat
MILESTONE: EU935-M1 (World Surface Fidelity)
SCOPE: EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927 fix-batch verification + full load-bearing invariant repeat
QC_VERDICT: QC_PASS_WITH_FINDINGS
FINDINGS: 0xP0, 0xP1, 0xP2, 1x new bounded P3 (P3-RE-1: the batch record's own "no 9,916 anywhere" absolute claim vs its 4 self-quotes; +1 sub-P3 wording observation on FIX-4's "byte-unchanged" parenthetical)
FULL_READ_LOG_PATH: this file, section 5
NOT_CHECKED: this file, section 6
FINAL_REPORT_PATH: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/REPORT.md (the run's; this re-QC's record = this file)
GATES_PATH: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/STAGE_ACCEPTANCE_GATES.csv (4 PENDING gates NOT flipped by this worker)
MANIFEST_PATH: docs/audits/EU935_M1_GATE_C_R2_COUNTER_CORRECTION_20260927/06_REPORT/MANIFEST_SHA256.csv (34 rows, 0 stale / 0 missing / 0 unlisted, re-verified)
INPUT_AND_OUTPUT_HASHES: terrain.bnt 95841761CE4EA074C97930EC1CEF3FB57AAC7F7F4F3D9B751A9EE60510299990 / 125,064,817 B; entrypoint A0F21829.../115,846 (before-pin 8EEC84E6.../113,685 reconstructed MATCH); the 5 edited files' before-hashes reconstructed MATCH (10e77ed1/3993, aa810fb6/6673, 9fdd9d2b/4463, 849c0365/3848, 8d34dae6/14543); after-hashes MATCH (fc5cec19/4419, 34339b39/5368, 0d64ec62/6772, f1c7dff5/4292, e7ebfb53/15221); QC_P3_FIX_BATCH.md b7535db5.../19,108 = manifest row; frozen patches 27DEE198.../3,377 and 5978FF6B.../3,389 = live diffs
FILES_CHANGED (by this re-QC): NONE inside D:\Eudoria_Reconstruction (READ-ONLY); outputs only in C:\Users\User\AppData\Local\Temp\opencode\EU935_M1_R2_20260927\RE_QC_WORKSPACE\
BASE_SHA: cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d
HEAD_SHA: cc747dfbf75d3c89c80bd8cccd33d6546fbfa36d (unchanged; no staging; no commits)
PUSH_STATUS: NOT_PERFORMED (read-only re-QC; no git state operations)
UNRELATED_WORK_EXCLUDED: PE_935_NINODE_SLOT17_FIRSTCALL_R1_20260914/ and experiments/ roots untouched and out of scope (searched: 0 hits)
NEXT_PARENT_ACTION: PE-MASTER final audit of this run; adjudicate P3-RE-1 (accept as-is or dispatch a bounded one-sentence scoping fix to QC_P3_FIX_BATCH.md + manifest refresh + fresh QC repeat); then the persistence phase (human-authorized Commit 1) and the PE_MASTER_VERDICT / FINAL_REVIEW_INVENTORY gates. INTERNAL_QC gate remains PENDING for PE-MASTER's process; this re-QC is its evidence input.
