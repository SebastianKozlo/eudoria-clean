# INTERNAL_QC_R1.md — FRESH INTERNAL_QC, RUN B: PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500

- QC run: INTERNAL_QC_RUN_B (fresh independent QC context; the executor's report was NOT trusted a priori; every number below re-derived from disk/git by the QC session itself)
- Subject run: PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500 (RUN_CLASS MATERIAL; commits C1 14eda26, C2 0470985, C3 cdbbb53; BASE_SHA 90c86be9e52d00e4dd916ea75bc99ea93354c88f)
- Contract: D:\Eudoria_Reconstruction\99_Audits\PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500\00_CONTROL\CONTRACT.md
- QC scope per assignment: Q1-Q10 below; READ-ONLY everywhere except this file; NO_NESTED_TASKS; no commits made by QC.
- QC tooling: PowerShell 5.1 (Get-FileHash/byte loops), Python 3.12.10 (csv module — the standard RFC-4180 parser; hashlib; subprocess for git-blob hashing). All commands executed in-session 2026-09-06.

---

## Q1. Contract integrity — PASS

- Command: `Get-FileHash -Algorithm SHA256 00_CONTROL\CONTRACT.md`
- Re-derived: SHA256 = `8279C82707DF3DDC469B785AAB707D5FA1E36B469968D97645A75326FF6F6798`
- Expected: `8279C82707DF3DDC469B785AAB707D5FA1E36B469968D97645A75326FF6F6798` → MATCH.
- Contract read in full (59 lines): RUN_CLASS MATERIAL, executor pe-master-auditor (documentation/metadata corrections only), parent loop bd17344b-a054-4cf4-be8d-5f0b250e8509 iter 1, TARGET MAP TM-1..TM-8, gates G1-G5, forbidden set, required artifacts.

## Q2. Entrypoint (repo AUDIT_ENTRYPOINT.md) counts — PASS

File: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean\AUDIT_ENTRYPOINT.md (read in full, 88 lines).

- Commands: `[regex]::Matches($content,[regex]::Escape($phrase)).Count` per phrase; line-walk over the LATEST RUNS section.
- Re-derived phrase counts (whole file):
  - `1,796+33 v4` = **0** (expect 0) ✔
  - `both overfitting-control-validated` = **0** (expect 0) ✔
  - `ONE-WAY implication only` = **1** (expect 1) ✔
  - `SUPERSEDED IN PART` = **2** (expect 2) ✔
  - `K1 caveat` = **1** (expect 1) ✔
- New L30 row for `14eda26` present at the TOP of the LATEST RUNS table (first data row, file line 30), verdict cell = `PENDING (fresh INTERNAL_QC + PE-MASTER MASTER_AUDIT follow)` ✔
- Total table DATA rows between the `## LATEST RUNS` header and the next section = **31** (data rows L30-L60; counted as rows starting `| ` after the `|---|` separator). Note: raw `| `-prefixed lines including the column-header row = 32; the separator `|---|` does not start with `| `; data rows = 31 = the expected census.
- Rows `2d48831` (L31), `03b00cc` (L32), `eabf6cf` (L33) present and carrying the corrections:
  - 2d48831 purpose cell: `1,796 v10(class -256) + 26 v10(class 1) + 7 v4 = 1,829 = 5,596-3,767; ONE-WAY implication only (class -256 => zero entries; converse FALSE)`; verdict append `— SUPERSEDED IN PART (post-audit F2: ...)`.
  - 03b00cc purpose cell: `candidate grammars (deterministic OC = formal re-validation, not held-out validation; H7 37/37 was an arithmetic assignment — post-audit F1)`; verdict append `— SUPERSEDED IN PART (post-audit F1; +65/88.88% = CANDIDATE pending the grammar revalidation campaign)`.
  - eabf6cf verdict append: `— K1 caveat: physically-verified ID-membership (24,474/24,508) is not automatically proof of every mesh->texture association; recounting the same CSV is not a new independent source (post-audit)`.

## Q3. git diff 90c86be..HEAD -- AUDIT_ENTRYPOINT.md — PASS

- Commands: `git diff --stat 90c86be..HEAD -- AUDIT_ENTRYPOINT.md`; `git diff -U0 90c86be..HEAD -- AUDIT_ENTRYPOINT.md`
- Re-derived: `1 file changed, 4 insertions(+), 3 deletions(-)`; a single hunk `@@ -30,3 +30,4 @@` — exactly 3 replaced rows (2d48831, 03b00cc, eabf6cf) + 1 new row (14eda26). NO other row modified or deleted; the non-edited cell content of the three rows is byte-identical to BASE (verified by reading the full diff).
- Cross-check (independent method, byte-level, not line-diff): PRE_EDIT\AUDIT_ENTRYPOINT.pre.md (87 lines) == `git show 90c86be:AUDIT_ENTRYPOINT.md` byte-identical (True); PRE_EDIT vs `git show 14eda26:AUDIT_ENTRYPOINT.md` differs at EXACTLY lines 30, 31, 32 (line counts 87/87 — the C1 edit preserved the line count; C2 added the new row, current file = 88 lines).

## Q4. Ledger (repo docs\audits\CORRECTION_LEDGER.md) — PASS

(a) Byte-prefix proof:
- Commands: byte loop over `[System.IO.File]::ReadAllBytes(...)` of PRE_EDIT\CORRECTION_LEDGER.pre.md vs current ledger.
- Re-derived: BYTE-PREFIX = **True** (pre 22,728 B is an exact byte-prefix of current 28,227 B; +5,499 B appended; first mismatch: none). pre SHA256 `A03E7A51...C9BFBA7`; current SHA256 `357AB1C6...32A5C5F`. (Cross-consistency: 00_CONTROL\LEDGER_APPEND_BLOCK_B1.txt = 5,499 B = exactly the appended delta.)

(b) Six LED-ENTRY blocks F1..F6:
- Command: `[regex]::Matches` counts of `LED-ENTRY: F1..F6` over whole current file and whole pre file.
- Re-derived: each of F1..F6 = **exactly once** in the current ledger (1 each; 0 each in pre; total LED-ENTRY current = 11 = 5 pre-existing + 6 new ✔).
- Substance spot-verification (read in full, ledger lines 280-339):
  - F1 cites driver L1237-1250 (deterministic oc_eval cannot FAIL) and L1427-1429 (H7 validation_exact := h7_total_325//2) ✔ — matches the contract adjudication.
  - F2 gives the 1,796 + 26 + 7 partition (with one-way implication and converse-FALSE citing 26 class-1 zero-entry files in PROBE2_CONTINGENCY.json B1 row0) ✔.
  - F3 contains the forward-fix note ("Forward fix: RUN B TM-6 (21 files restored, per-path SHA verified); NO historical claim whether a mirror existed before") ✔.
  - F4 the manifest defects (K2 L2 unquoted comma, L17-18 symbolic rows; K3 L17 three records concatenated) ✔.
  - F5 the zero controller checkpoints (state checkpoint={}; events START+STOP only) ✔.
  - F6 the improper grading (MASTER_ACCEPTED at own NOT_CHECKED load-bearing items) ✔.

## Q5. Addenda — PASS

- Commands: `Get-FileHash` on repo addenda + 99_Audits SYNC copies; `git diff --name-status 90c86be..HEAD` on both package dirs; full reads of both addenda.
- Re-derived hashes:
  - repo docs\audits\PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209\PE_MASTER_REVIEW_ADDENDUM_R1.md = `FD0645E05BA8BA32CA588CE022C57CB25D053335AB878CFF482931B1BC8714C9` (expected fd0645e0... ✔); 99_Audits SYNC copy byte-identical (same hash) ✔.
  - repo docs\audits\PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200\PE_MASTER_REVIEW_ADDENDUM_R1.md = `543D2F00F61F09373BEE691BFAF0A6A57DEF12B6BCC39381DD9B81A1669763F5D` (expected 543d2f00... ✔); 99_Audits SYNC copy byte-identical ✔.
- Originals untouched vs 90c86be: `git diff --name-status 90c86be..HEAD -- <both package dirs>` = exactly `A .../PE_MASTER_REVIEW_ADDENDUM_R1.md` x2 (11 and 12 inserted lines respectively); ZERO modifications — PE_MASTER_REVIEW.md in both packages untouched ✔ (stronger than the minimum two-path check: the whole package trees show only the ADDENDUM additions).
- Content faithfulness (read in full):
  - K2 addendum: OC/H7 retraction (oc_eval driver L1237-1250 deterministic re-parse of already-selected successes — cannot FAIL; H7 37/37 = arithmetic assignment h7_total_325//2 at L1427-1429; H7 predicate L1414-1416 without denominator matching; OC teeth retained only for canonical-param grammars H3 2/5, H4 1/6) + CANDIDATE status (+65/88.88% pending PE_NIF_MORPH_GRAMMAR_REVALIDATION_R1) + F6 improper-grading note ✔ = the contract adjudication.
  - K3 addendum: partition 1,796 v10(class -256) + 26 v10(class 1) + 7 v4 = 1,829 = 5,596-3,767 ("the sum stands; the labels do not") + ONE-WAY implication only with converse FALSE (26 class-1 zero-entry files; PROBE2_CONTINGENCY.json B1_entry_count row0 = [26, 1313, 737, 462, 504]) + F6 note ✔ = the contract adjudication.

## Q6. K1 mirror FULL census — PASS

- Command: recursive Get-ChildItem over repo docs\audits\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\ + per-file Get-FileHash vs D:\Eudoria_Reconstruction\99_Audits\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\<same rel path>; then per-row re-verification of the executor census file.
- Re-derived: repo package = 22 files; mirror = 22 files; **total=22, match=22, mismatch=0, missing=0**; mirror files with no repo counterpart = 0. Every mirror SHA256 == repo source.
- Executor census (RB 00_CONTROL\K1_MIRROR_RESTORE_CENSUS.md, read in full): claims 22/22 (MATCH_OK_TOTAL=22, MIRROR_TOTAL=22, REPO_TOTAL=22, zero MISSING_IN_MIRROR, zero MISMATCH) — my INDEPENDENT per-row re-verification of all 22 census rows (relative_path + bytes + sha256 vs my own repo+mirror hashes): **OK=22, DISAGREE=0** ✔. Census claims match my measurements exactly (22/22).

## Q7. AGENTS.md (D:\Eudoria_Reconstruction\AGENTS.md) — PASS

- Commands: byte-loop prefix/suffix computation vs RB\00_CONTROL\PRE_EDIT\AGENTS.pre.md; regex counts; full read.
- Re-derived: pre 5,504 B / cur 5,785 B; common prefix = **1,301 B**; common suffix = **4,038 B** (byte-identical); pre differing window [1301,1466) = 165 B; cur differing window [1301,1747) = 446 B. The differing window lies entirely INSIDE the `## Cel` section body (the `## Cel` heading itself is in the common prefix; the common suffix begins at `## SRODOWISKO WYKONAWCZE — VM ONLY`) → ONLY the "## Cel" section differs; no other section touched.
- Phrase counts in the current file: `Rekonstrukcja Project Entropia 2003` = **0** (expect 0) ✔; `PRIMARY_RECONSTRUCTION_TARGET` = **1** (expect 1) ✔.
- Technical scope list preserved: `BNT/TDF, Terrain_patch, Patch Manager` = 1; `geometria terenu, materialy` = 1; `render packet registration, renderer DirectX` = 1; `lokalny login/world server` = 1 — all four items present, unchanged ✔.
- pre SHA256 `37298CF11626A822FD3232D09F17A96EB872AD404B7B0BB31641C02F1ABA1858` → cur SHA256 `4A93424FBBD0864188BFE2CF132565C3A3A525D626DDF617A0F48FACD7209C7B` (both independently re-derived; identical to the REPORT/manifest values).

## Q8. Manifest — PASS

- Command: my OWN independent validator (Python 3.12.10 csv module — standard RFC-4180 parser; NOT the executor's script): parse repo docs\audits\PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500\artifact_index.csv with section tracking behind `# external sources`, assert per MANIFEST_SCHEMA_SPEC.md.
- Re-derived:
  - Ordinary section header = `artifact,role,sha256` ✔; **13 ordinary data rows**; every row: exactly 3 fields ✔; sha256 = 64-hex ✔; artifact path exists in the package ✔; physical SHA256 == row hash for EVERY row (all 13 re-hashed by me) ✔; no duplicates ✔.
  - `# external sources` marker present before the external section ✔; external header = `source_id,kind,era,physical_path,sha256` ✔; **6 external rows**; each: 5 fields, kind=external_source, era non-empty, physical_path exists, hash matches physical file (all 6 re-hashed) ✔; no duplicate source_ids ✔.
  - Package file census: repo package = 15 files = 13 manifest-listed + artifact_index.csv + MANIFEST_VALIDATION.json — zero unlisted files; the disclosed self-exclusion set is respected ✔.
  - My result: **PASS** — matches RB 00_CONTROL\MANIFEST_VALIDATION.json (`result: PASS`, ordinary_rows_checked 13, external_source_rows_checked 6, negative tests 6/6 expected-FAIL-got-FAIL) ✔.
  - Pin consistency (independent): manifest@C1 blob SHA256 = `17105d0eda120f77f0e35d3709c4628d0f0771a21a13a8febee3e0bee536bf82` == the validation pin ✔; gates@C1 = `2d450e7c...` == the C1 manifest gates row ✔; C1→C3 manifest diff = exactly 1 line (gates-row hash 2d450e7c→495499db) ✔; current repo manifest == RB manifest byte-identical (`7C8B5A7B...`) ✔; current gates file hash `495499DB61CA2600E8A5FF62119328D0E5EDCAA2B970F535A675E9F4B62D8A39` == current manifest row ✔. Post-C3 manifest re-validation recorded in 00_CONTROL\B3_EXECUTION_LOG.md (PASS, 13+6) — consistent with my own independent PASS on the current (post-C3) manifest.
  - Minor metadata note (NOT a gate predicate): the file physically contains 4 `#`-prefixed lines (1, 2, 17, 18); MANIFEST_VALIDATION.json reports `comment_lines: 3` — the executor's validator counts the `# external sources` MARKER as a section switch, not a comment (lines 1, 2, 18 = 3). Purely interpretational; no gate assertion involves comment counts; all 8 assertions and their numbers match my independent re-derivation.

## Q9. Commits/remote — PASS

- Commands: `git log --oneline -5`; `git show --name-only --format=` per commit; `git fetch origin`; `git rev-parse HEAD`; `git rev-parse origin/master`; `git ls-remote origin refs/heads/master`; `git status --porcelain`.
- Re-derived:
  - git log -5: `cdbbb53` (C3) → `0470985` (C2) → `14eda26` (C1) → `90c86be` (BASE) → `2d48831` — order consistent with the run narrative.
  - C1 `14eda2648dd2c72d13c2827fe9cf8b42a178a193` path census = **19** (AUDIT_ENTRYPOINT.md; CORRECTION_LEDGER.md; the two addenda; the 15-path new package tree) ✔ (expect 19).
  - C2 `04709858937332925b7ab985dadda682b0f6e9d6` path census = **1** (AUDIT_ENTRYPOINT.md; numstat 1 insertion / 0 deletions) ✔ (expect 1).
  - C3 `cdbbb5388c1527a670e05fa7bce511f09490a3a7` path census = **2** (STAGE_ACCEPTANCE_GATES.csv + artifact_index.csv) ✔ (expect 2).
  - Full blast radius 90c86be..HEAD: exactly 19 paths = M AUDIT_ENTRYPOINT.md + M docs\audits\CORRECTION_LEDGER.md + 17 A (2 addenda + 15 package) — ZERO foreign/other paths ✔ (consistent with censuses 19/1/2 with path reuse entrypoint/gates/manifest).
  - Remote: after `git fetch origin`: HEAD = `cdbbb5388c1527a670e05fa7bce511f09490a3a7`; origin/master = same; DIRECT `git ls-remote origin refs/heads/master` = same → **origin/master == HEAD == cdbbb53...** (verified against the ACTUAL remote, not only the cached ref) ✔.
  - `git status --porcelain` = 0 lines → tree clean ✔.

## Q10. REPORT.md honesty — PASS (all claimed numbers re-derived; 2 minor disclosed/interpretational notes recorded in DISCREPANCIES)

File: docs\audits\PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500\REPORT.md (read in full, 55 lines). Every number checked against my Q2-Q9 results:

- Header: RUN_CLASS MATERIAL ✔; loop bd17344b ✔; BASE_SHA 90c86be9... ✔ (parent of C1 in git log).
- WHAT CHANGED 1 (entrypoint): 3 cells + 1 governance row ✔ (Q3: 4 ins/3 del); "row census 30 -> 31" ✔ (my 31 data rows; C2 numstat 1/0 — the 30 old rows byte-untouched in C2); "line-level diff vs PRE_EDIT touches EXACTLY lines 30,31,32" ✔ (my byte-level check: changed lines = [30,31,32]); "line count 87 = 87" ✔ (PRE_EDIT == BASE = 87 lines; post-C1 = 87; current = 88 after C2).
- WHAT CHANGED 2 (ledger): +6 entries each exactly-once ✔; byte-prefix 22,728 → 28,227 (+5,499, 0 rewritten) ✔ (Q4 — my numbers identical); evidence pointers F1..F6 ✔ (Q4b); LED-ENTRY total 11 = 5+6 ✔ (my counts: 11/5).
- WHAT CHANGED 3 (addenda): K2 SHA fd0645e0... ✔, **2067 B** ✔ (my measurement: 2067 B); K3 SHA 543d2f00... ✔, **1867 B** ✔ (my measurement: 1867 B); comma-form row0 ✔ (my count: comma form 1, space form 0); pre-copy 88c10f31... ✔ (== manifest row); SYNC copies byte-identical ✔; originals preserved ✔.
- WHAT CHANGED 4 (K1 mirror): 22/22 ✔ (my independent census 22/22/0/0); census file ✔ (my per-row re-verification 22/22); FORWARD FIX ONLY ✔.
- WHAT CHANGED 5 (AGENTS.md): pre 37298cf1 (5504 B) → post 4a93424f (5785 B) ✔ (my hashes byte-for-byte identical); common prefix 1301 B + suffix 4038 B ✔ (my numbers identical); scope list unchanged ✔; no other section touched ✔.
- WHAT CHANGED 6-8: MANIFEST_SCHEMA_SPEC ✔ (read; matches TM-8); adjudication persisted verbatim ✔ — my byte-level check: the adjudication file == the contract content between the `---BEGIN/END ADJUDICATION---` markers EXACTLY (2423 B; RB == repo; hash 4dc63339... == manifest row; the markers are the contract's delimiters, not part of the persisted text); package + repo mirror ✔ (15/15; manifest==RB byte-identical).
- GATES G1: my name-status = exactly M entrypoint + M ledger + A addenda (+ package additions); corpora 0 diffs ✔; AGENTS prefix/suffix proof ✔; ledger byte-prefix ✔.
- GATES G2: all fragment counts 0/0/1/2/1 ✔ (my Q2 — identical numbers); partition fragment = 1 ✔; OC fragment = 1 ✔; K3 comma 1 / space 0 ✔; LED-ENTRY 11 = 5+6 ✔; ledger run-id mentions = 6 ✔ (my count: 6).
- GATES G3: 22/22, MISSING=0, MISMATCH=0 ✔ (my Q6). Note on the "independently re-measured in B2 and re-hashed in B3" sequence wording → DISCREPANCIES item 1 (executor-disclosed).
- GATES G4: recorded post-push in C3 + B3 log ✔ (my Q9: HEAD == origin/master == ls-remote == cdbbb53; gates CSV G4 row = PASS with the C2-time verification text and the C3 re-verification pointer).
- GATES G5: staged censuses == authorized ✔ (my Q9: 19/1/2); zero payloads ✔ (all 19 paths are documentation/manifests/control records); artifact_index.csv self-validation PASS ✔ (my independent validator: PASS).
- NOT_CHECKED / STANDING: nothing scientific re-executed ✔ (consistent with the full 19-path diff — zero code/science files); K2 revalidation = RUN A (future) ✔; wiki HOLD ✔ (not in diff); plugin-owned files untouched ✔ (not in diff); zero payloads ✔; row verdict PENDING ✔; ADVISORY_PRE_QUALIFICATION ✔; loop aggregate MASTER_REVALIDATION_REQUIRED ✔ (matches the adjudication text).
- STAGE_ACCEPTANCE_GATES.csv (read in full, RFC-4180 quoted fields): G1-G5 all PASS with evidence; all evidence numbers cross-checked against my own measurements above — no mismatches.

## FULL_READ_LOG

Read to EOF in this QC session: CONTRACT.md; AUDIT_ENTRYPOINT.md (88 lines, full); CORRECTION_LEDGER.md tail (lines 280-339, the 6 new entries, full) + pre-file tail; both PE_MASTER_REVIEW_ADDENDUM_R1.md (full); K1_MIRROR_RESTORE_CENSUS.md (full, 38 lines); MANIFEST_SCHEMA_SPEC.md (full, 22 lines); MANIFEST_VALIDATION.json (full, 78 lines); B3_EXECUTION_LOG.md (full, 64 lines); AGENTS.md current (full, 148 lines); REPORT.md (full, 55 lines); STAGE_ACCEPTANCE_GATES.csv (full, 6 lines); artifact_index.csv (full, 25 lines); full C1-time manifest via git show; the full entrypoint unified diff (90c86be..HEAD); full name-status list (90c86be..HEAD).

## NOT_CHECKED (this QC)

- The scientific substance of the K1/K2/K3 runs and the PE-MASTER re-derivations behind the adjudication (PROBE2_RAW.csv partition; the 24,508-row re-derivation; oc_eval/H7 driver code) — out of RUN B scope (contract: documentation corrections only; the executor did NOT re-execute science either; the adjudication is PE-MASTER's and was READ-ONLY here).
- 00_CONTROL\B2_EXECUTION_LOG.md, HANDOFF.md, LEDGER_APPEND_BLOCK_B1.txt — hash-verified (manifest rows + my independent manifest re-hashes) but not read line-by-line (not load-bearing for the Q1-Q10 predicates).
- The 2003/9.3.5 corpora, wiki (docs\nif), PE_MASTER_LOOP_STATE.json / PE_MASTER_LOOP_EVENTS\ — untouched by the run per the diff (absent from the 19-path name-status); not further inspected (nothing in scope requires it).
- The negative-test FIXTURES of the manifest validator (synthetic; their results are recorded in MANIFEST_VALIDATION.json and the validator logic was re-implemented independently by me — the gate predicates themselves were re-executed on the real manifest with PASS).

---

## DISCREPANCIES

No numeric predicate of the QC checklist Q1-Q10 failed. Two minor observations recorded (neither invalidates a gate; both are disclosed/interpretational):

1. **[P3, executor-disclosed] REPORT.md G3 sequence wording was imprecise at C1-commit time.** REPORT.md (committed at C1) says the K1 mirror census was "independently re-measured in B2 and re-hashed in B3"; the executor's own 00_CONTROL\B3_EXECUTION_LOG.md §SELF-CAUGHT FINDING (P2) discloses that at C1-commit time only ONE of the 22 census hashes had been re-measured in B3 (the repo-side K1 PE_MASTER_REVIEW.md), with the full 22/22 re-hash completed later in the same batch (post-C3). Substance TRUE at batch end (my independent 22/22 census concurs); the committed SEQUENCE wording was premature. The executor disclosed it, returned it to PE-MASTER, and did not improvise a C4 (per the parent's exactly-C1/C2/C3 order). No further action by QC; PE-MASTER holds the disposition.
2. **[P3, interpretational] MANIFEST_VALIDATION.json `comment_lines: 3` vs 4 physical `#`-prefixed lines in artifact_index.csv.** The validator counts the `# external sources` line as a section marker, not a comment (3 = lines 1, 2, 18). No gate assertion involves comment counts; my independent parse confirms all counted row denominators (13 ordinary + 6 external) and PASS.

QC_VERDICT = QC_PASS
