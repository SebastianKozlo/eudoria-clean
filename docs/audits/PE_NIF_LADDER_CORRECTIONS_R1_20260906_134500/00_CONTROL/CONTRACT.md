# CONTRACT — RUN B: PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500

- RUN_CLASS: MATERIAL (declared by PE-MASTER at FORMALIZE, per PROJECT_OPERATING_MODEL A1.1)
- EXECUTOR: pe-master-auditor (documentation/metadata corrections only; NO re-execution of any science)
- PARENT: PE-MASTER loop bd17344b-a054-4cf4-be8d-5f0b250e8509 (iteration 1)
- MILESTONE: EU935-M1 (NO crossing) | ERA: n/a (documentation corrections)
- BASE_SHA: 90c86be9e52d00e4dd916ea75bc99ea93354c88f (HEAD == origin/master at formalization; tree clean)
- Repo: D:\Eudoria_Reconstruction\12_WebGame\eudoria-clean (SebastianKozlo/eudoria-clean, master)

## 0. PURPOSE
Persist the external post-audit corrections (package PE_NIF_LADDER_POSTAUDIT_R1_20260906, findings F1-F6, all adjudicated ACCEPTED by PE-MASTER 2026-09-06) via NEW amendments + current-pointer updates. Old reports/reviews byte-preserved; no history rewrite; corrections are additions and pointer-cell updates only. Executor limitation-disclosure is NOT proof that executor predicates were correct.

## 1. VERBATIM PERSISTENCE (copy this block EXACTLY to 00_CONTROL\PE_MASTER_POSTAUDIT_ADJUDICATION.md in this run dir AND to repo docs\audits\PE_NIF_LADDER_CORRECTIONS_R1_20260906_134500\00_CONTROL\PE_MASTER_POSTAUDIT_ADJUDICATION.md)

---BEGIN ADJUDICATION---
# PE-MASTER post-audit adjudication — loop 0132d23c (K1-K3) + external package PE_NIF_LADDER_POSTAUDIT_R1_20260906
VERDICT = MASTER_REVALIDATION_REQUIRED (loop aggregate; supersedes the loop report's "3/3 MASTER_ACCEPTED" summary). AUTHORITY_STATUS = ADVISORY_PRE_QUALIFICATION; CANONICAL_GATE_EFFECT = NONE.
DISPOSITIONS: 6/6 external findings ACCEPTED. The 2h stop was legitimate (bounded scope A).
K1 (eabf6cf) STANDS: 24,474/24,508 = 99.8613% ID-membership triple-confirmed (human physical parse; external auditor physical parse; PE-MASTER re-derivation of all 24,508 rows: 24,474 resolved / 34 dangling; 3,767 distinct entry-bearing files = 3,016 v10 + 751 v4; dangling 18 SuperSpray + 15 same-as-2003 + 1 new id 592148). CAVEAT ADDED: ID-membership is NOT automatically proof of every mesh->texture association; recounting the same CSV is NOT a new independent source.
K2 (03b00cc) downgraded to CANDIDATE: +65 fits (H5a 39 + H5c 26) and 2,158/2,427 = 88.88% are real-record arithmetic, but "overfitting-control-validated" is RETRACTED: oc_eval (driver L1237-1250) is a deterministic re-parse of already-selected successes (cannot FAIL); H7 "37/37 validation-exact" is an arithmetic assignment (L1427-1429: validation_exact := h7_total_325 // 2); the H7 predicate (L1414-1416) compares raw NC count (3, <=1 trial/file) vs half the positives without denominator matching. Executor report was honest (deterministic OC = "a formal re-validation"); the PE_MASTER_REVIEW and entrypoint inflated it.
K3 (2d48831) science stands (OBSERVED-level; executor disclosed the 26 exceptions); review-layer partition SUPERSEDED: 1,796 v10(class -256) + 26 v10(class 1) + 7 v4 = 1,829 = 5,596-3,767 (PE-MASTER re-derivation from PROBE2_RAW.csv: 1|0 -> 26 zero + 3,016 positive; -256|255 -> 1,796 zero + 0 positive; K1: 751 of 758 v4). One-way implication only: class -256 => zero entries (1,796/1,796); converse FALSE. The review's "1,796 v10 + 33 v4" and "classes partition entry-bearing vs zero-entry" are RETRACTED.
F3: K1 99_Audits mirror absent (1/22 files). Restoration = forward fix, no historical claim.
F4: manifest defects (K2 artifact_index L2 unquoted comma, L17-18 symbolic rows; K3 L17 three records concatenated).
F5: loop 0132d23c wrote zero controller checkpoints (state checkpoint={}; events START+STOP).
F6: K2/K3 reviews issued MASTER_ACCEPTED at own NOT_CHECKED load-bearing items; fresh internal QC mandatory.
---END ADJUDICATION---

## 2. TARGET MAP (each edit: record pre-edit SHA256 BEFORE; verify after; whitespace-normalized exactly-once check; .pre copy of each edited file)
- TM-1 AUDIT_ENTRYPOINT.md L30 (KROK 3 row, commit 2d48831), purpose cell: replace "1,796+33 v4 = 1,829 = 5,596-3,767" with "1,796 v10(class -256) + 26 v10(class 1) + 7 v4 = 1,829 = 5,596-3,767; ONE-WAY implication only (class -256 => zero entries; converse FALSE)"; verdict cell append: " — SUPERSEDED IN PART (post-audit F2; run science stands at OBSERVED; adjudication: PE_NIF_LADDER_POSTAUDIT_R1_20260906)".
- TM-2 AUDIT_ENTRYPOINT.md L31 (KROK 2 row, commit 03b00cc), purpose cell: replace "both overfitting-control-validated" with "candidate grammars (deterministic OC = formal re-validation, not held-out validation; H7 37/37 was an arithmetic assignment — post-audit F1)"; verdict cell append: " — SUPERSEDED IN PART (post-audit F1; +65/88.88% = CANDIDATE pending the grammar revalidation campaign)".
- TM-3 AUDIT_ENTRYPOINT.md L32 (KROK 1 row, commit eabf6cf), verdict cell append: " — K1 caveat: physically-verified ID-membership (24,474/24,508) is not automatically proof of every mesh->texture association; recounting the same CSV is not a new independent source (post-audit)".
- TM-4 repo CORRECTION_LEDGER.md: append six entries (F1..F6) with evidence pointers (PE_NIF_LADDER_POSTAUDIT_R1_20260906 REPORT.md; K2 driver L1237-1250/L1427-1429/L1414-1416; PROBE2_CONTINGENCY.json B1_entry_count row0=[26,1313,737,462,504]; checks.json mirror/hash records). Append-only; byte-prefix proof.
- TM-5 additive addenda (originals byte-preserved; pure additions): docs\audits\PE_NIF_MORPH_RESIDUAL_DEEPDIVE_R1_20260906_033209\PE_MASTER_REVIEW_ADDENDUM_R1.md and docs\audits\PE_NIF_935_SEMANTIC_CORRELATIONS_R1_20260906_041200\PE_MASTER_REVIEW_ADDENDUM_R1.md — content: the K2/K3 supersessions from Section 1 (+ byte-identical 99_Audits SYNC copies of the addenda).
- TM-6 K1 mirror restoration: copy the 21 missing package files from repo docs\audits\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\ to D:\Eudoria_Reconstruction\99_Audits\PE_M1_935_BINDING_CHAIN_REVALIDATION_R1_20260906_031021\; SHA256-verify each copied path vs the repo source; record the census (22/22 incl. the existing review), per-file hashes, timestamps, and the forward-fix note (NO historical claim whether a mirror existed before).
- TM-7 D:\Eudoria_Reconstruction\AGENTS.md (LOCAL file, NOT repo): "## Cel" section (lines 27-34) currently "Rekonstrukcja Project Entropia 2003, szczegolnie: BNT/TDF, Terrain_patch, Patch Manager, geometria terenu, materialy, render packet registration, renderer DirectX, lokalny login/world server" — bounded rewrite: era-primary PCG_9_3_5 / Entropia Universe 9.3.5 as the PRIMARY RECONSTRUCTION TARGET; the 2003 corpora = historical/cross-build reference oracles; technical scope list unchanged in substance; NO other section touched; pre/post SHA256 recorded.
- TM-8 manifest schema spec: write 00_CONTROL\MANIFEST_SCHEMA_SPEC.md (this run dir + repo copy): RFC-4180 CSV writer (quoted fields; one record per line; never concatenated records); ordinary rows artifact|role|sha256 with 64-hex sha256, every listed path exists in the package and hash-matches; symbolic external-source rows as an explicit sub-schema (source_id|kind=external_source|era|physical_path|sha256), never mixed into ordinary rows; the manifest self-excludes its own hash; validation gate: parse every row with a standard CSV parser, assert schema + 64-hex + path existence + hash match, detect duplicates and missing files; negative tests: comma-in-description, missing newline, missing file, malformed hash, unsupported symbolic path. RUN A must implement and dogfood this spec.

## 3. GATES (fail-closed; execute and assert each)
- G1 BYTE_PRESERVATION: every pre-existing file unchanged except TM-1..TM-4, TM-7 targets and the TM-5 additions (pre-edit SHAs recorded BEFORE edits, verified AFTER; ledger = append-only byte-prefix).
- G2 EXACTLY_ONCE: every new/edited fragment appears exactly once (whitespace-normalized matching).
- G3 MIRROR_CENSUS: K1 mirror 22/22 paths present, each SHA256-identical to the repo source.
- G4 REMOTE_VERIFY: git fetch; then origin/master == HEAD; recording only local refs is INSUFFICIENT.
- G5 SCOPE: zero payloads; committed path census == the authorized list exactly (path-limited commit; never commit pre-staged foreign paths); this run's OWN artifact_index.csv follows MANIFEST_SCHEMA_SPEC.md and its self-validation gate PASSES (dogfooding).

## 4. NON-PASS CLASSES / HARD STOPS / FORBIDDEN
- NON-PASS: TARGET_FRAGMENT_NOT_FOUND / DUPLICATE_FRAGMENT / MIRROR_HASH_MISMATCH / REMOTE_DIVERGENCE / PATH_CENSUS_MISMATCH.
- HARD STOPS: any pre-edit SHA mismatch; any write outside the allowed paths.
- FORBIDDEN: modifying any byte of pre-existing files inside old run packages (the two TM-5 addenda are the ONLY old-dir exceptions and must be pure additions); the post-audit package PE_NIF_LADDER_POSTAUDIT_R1_20260906 (READ-ONLY); PE_MASTER_LOOP_STATE.json + PE_MASTER_LOOP_EVENTS\ (plugin-owned); wiki (docs\nif) — HOLD; any M2/milestone action; history rewrite.

## 5. REQUIRED PACKAGE ARTIFACTS (this run)
REPORT.md (PROJECT_OPERATING_MODEL s15 20-point contract), HANDOFF.md, STAGE_ACCEPTANCE_GATES.csv (one row per gate G1-G5 + result), artifact_index.csv (per MANIFEST_SCHEMA_SPEC.md), 00_CONTROL\CONTRACT.md, 00_CONTROL\PE_MASTER_POSTAUDIT_ADJUDICATION.md, 00_CONTROL\MANIFEST_SCHEMA_SPEC.md, 99_Audits mirror byte-identical.

## 6. FINAL HANDOFF SCHEMA (end of execution)
AUDIT_OUTPUT_ROOT / FINAL_REPORT_PATH / PRIMARY_EVIDENCE_PATHS / RUN_STATUS / HARD_STOP_REASON.

## 7. INPUTS (READ-ONLY)
- D:\Eudoria_Reconstruction\99_Audits\PE_NIF_LADDER_POSTAUDIT_R1_20260906\ (REPORT.md, checks.json, HANDOFF.md)
- repo AUDIT_ENTRYPOINT.md (rows L30-L32), repo CORRECTION_LEDGER.md (tail), D:\Eudoria_Reconstruction\AGENTS.md
- K1/K2/K3 run packages (docs\audits\... — TM-5/TM-6 touch them additively/copy-only)
