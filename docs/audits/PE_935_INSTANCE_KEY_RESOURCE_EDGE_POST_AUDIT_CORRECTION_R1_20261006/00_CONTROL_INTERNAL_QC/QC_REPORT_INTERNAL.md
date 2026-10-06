# QC_REPORT_INTERNAL — PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006

- **QC_RUN_ID:** PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_INTERNAL_QC_R1_20261006
- **QC_SCOPE:** INDEPENDENT_INTERNAL_QC_RECORDS_CORRECTION (LOAD_BEARING depth, fresh context)
- **Executor of the audited package:** pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS)
- **QC worker:** pe-master-auditor (fresh context; PE-MASTER direct dispatch; NO_NESTED_TASKS;
  RECORDS-ONLY — zero new science, zero EXE reads, zero payload opening, zero runtime)
- **Audited package:** `docs/audits/PE_935_INSTANCE_KEY_RESOURCE_EDGE_POST_AUDIT_CORRECTION_R1_20261006/`
  (13 physical files at QC start; phase-1 state, untracked, PERSISTENCE_STATUS = PREPARED_NOT_PERSISTED)
- **BASE / HEAD at QC:** `f129fd5aa8e30f0f19c8903fe0d97899b9fe6510` (LOCAL_HEAD == origin/master ==
  contract EXPECTED_BASE_SHA; HEAD unchanged; no commit/push and no AUDIT_ENTRYPOINT edit performed
  by the executor in this phase, and none by this QC)
- **Governing contract:** `OPENCODE_RECORDS_ONLY_CORRECTION_REVIEWED.md` — 24,218 B / SHA256
  `EA86AA0897695C100D89BD68438318F6DDC9BD50DE28C7A6EDCC59ACF4ED61ED` (verified by this QC before any
  work; read in full)
- **Authoritative external input:** Desktop post-audit REPORT.md — 14,545 B / SHA256
  `664579B1F0762C9CE6266CDDF75EF9DEDA426E702800FAA0F837EC07EEB19572` (verified; REQUIRE_CORRECTIONS;
  audited target == BASE)
- **QC verdict:** **QC_PASS_WITH_FINDINGS** — every contract predicate measured PASS by this QC's own
  instruments; six P3-class documentation-precision findings and two observations; **zero P0/P1/P2;
  no load-bearing claim falsified; no fabricated provenance; no silent neighbor-shift; no new science.**

Instruments (this QC's own engine; the executor's validator was re-executed only as the
mutation-falsifier target required by the dispatch): `qc_independent.py`, `qc_mutations.py`
(copied into this directory); machine measurements:
`QC_INDEPENDENT_MEASUREMENTS.json`, `QC_MUTATION_RESULTS_FRESH_QC.json`; gates: `QC_GATES.csv`;
reading record: `FULL_READ_LOG.txt`.

---

## 1. Verdict summary (own measurements vs the package's claims)

| Contract predicate | Package claim | This QC's independent measurement | Agreement |
|---|---|---|---|
| Q1_BASE_IDENTITY | PASS (HEAD == origin == remote == f129fd5, preflight) | HEAD == origin/master == f129fd5 (own rev-parse); remote re-verification deferred to persistence (no fetch by this QC) | YES |
| Q2_DESKTOP_REPORT_IDENTITY | PASS | 14,545 B / 664579B1...19572 — MATCH (own hash) | YES |
| Q3_SOURCE_PACKAGE_READ_ONLY | PASS | own full re-hash of all 36 files == INPUT_IDENTITIES baseline, zero size/SHA diffs | YES |
| Q4_FUNCTION_LEDGER_SCHEMA | PASS | own parser: 10 exact contract-§6 columns in order, 8 rows, all widths 10, zero extra/missing/null, ORD unique, no BOM/CRLF/blank lines, prose non-empty, no STATUS column | YES |
| Q5_EDGE_LEDGER_SCHEMA | PASS | own parser: 11 exact columns, 22 rows, all widths 11, zero extra/missing/null, EDGE_ID unique | YES |
| Q6_DICTREADER_EXTRA_NULL | ZERO | restkey sentinel `__EXTRA__` zero hits; zero None-valued fields (both tables) | YES |
| Q7_STATUS_SOURCE_SEPARATION | PASS | STATUS vocabulary 22/22 valid; no evidence path in any STATUS; no STATUS token in any CITED; STATUS != CITED on all rows; FUNCTION prose fields non-empty and no edge enum applied | YES |
| Q8_MUT_A | CAUSAL_FAIL | MY OWN replicas on DIFFERENT rows (FUNCTION ORD 5 + EDGE E-GB2, raw-text append — a different mutation mechanism than the executor's csv.writer append): both REJECTED rc=2 with ROW_WIDTH_EXACT + DICTREADER_NO_EXTRA_CELLS | YES |
| Q9_MUT_B | CAUSAL_FAIL | MY OWN replicas (FUNCTION ORD 8 + EDGE E-N4): both REJECTED rc=2 with ROW_WIDTH_EXACT + DICTREADER_NO_MISSING_CELLS | YES |
| Q10_MUT_C | CAUSAL_FAIL | MY OWN replica on E-N4 (executor used E-GETTER): REJECTED rc=2 with CITED_EXISTING_ARTIFACT + STATUS_VOCABULARY + STATUS_NOT_EVIDENCE_PATH + CITED_NOT_STATUS_TOKEN — the same 4-predicate class as the executor's MUT_C | YES |
| Q11_DPA2_HISTORY_PRESERVED | PASS | source Q7 "PASS WITH ONE DISCLOSED DEVIATION" + Q9 QC_PASS + FINAL_REPORT §6 6-COUNTED/7th-disclosed verified; new records FAIL + HUMAN_ADJUDICATED_NOW + RETROACTIVE_PRIOR_AUTHORIZATION = NO + TECHNICAL_QC/PROCESS_COMPLIANCE separated | YES (wording notes F-QC-5/F-QC-6) |
| Q12_DPA3_PROVENANCE | PASS | source attribution quote + verbatim block (authorizes commit/push + manifest LAST; no deferral inside) verified; corrected statuses + no never-existed claim; FINAL_PUBLICATION_AUTHORIZATION = PRESENT | YES |
| Q13_P3_PRECISION | PASS | all P3-1..P3-6 verified against persisted evidence (see §3) | YES |
| Q14_NO_UNINTENDED_SCIENCE_DIFF | PASS | 10/10 required-unchanged conclusions preserved; all content changes within the contract §15 allowed list | YES |
| Q15_SOURCE_PACKAGE_HASH_DIFF | ZERO | own re-hash of 36 files: zero diffs, zero extra files | YES |
| Q16_FORBIDDEN_WORK | ZERO | zero EXE reads/payloads/runtime/new RE in the package's derivations (every reconstructed cell traces to already-persisted evidence); forbidden status tokens appear only in explicit NOT-converted negations; allowlist respected | YES |

Re-execution of the pinned production validator (`03_SCRIPTS/ledger_schema_qc.py`, on-disk SHA256
`916AD3E19D941BAF6D55A6197537ACCFC606276D3168D2AF9B233B0468887CEE` == manifest pin, verified before and
unchanged after all runs): clean check mode rc=0, FUNCTION_LEDGER_SCHEMA = PASS,
EDGE_LEDGER_SCHEMA = PASS, OVERALL = PASS — reproducing the package's LEDGER_SCHEMA_QC.json. Clean
ledger hashes unchanged after all mutation runs (mutations ran on temp copies only; the executor's
claim "the clean corrected ledgers were never modified" is confirmed by hash).

## 2. DPA1 reconstruction audit (the core of this QC)

**Source defect census (own naive parse):** FUNCTION_LEDGER.csv header 10 cols; data rows: ORD1=13
cells, ORD2=10, ORD3..8=9 → **7/8 malformed**. EDGE_LEDGER.csv header 11 cols; E-C1-PUSH=12,
E-E1-CALL=10, E-GB1=10, E-GB2=10, E-XD=10 → **5/22 malformed**. Exactly the Desktop DPA1 numbers.

**Field-by-field verification (ALL rows, ALL fields, own engine):**
- FUNCTION: ORD 1 — EXTENT = byte-exact join c2+c3; IDENTITY_EVIDENCE = byte-exact join c6+c7;
  OBSERVED_OPERATION = byte-exact join c8+c9; FINAL_SEMANTIC_ROLE = disclosed P3-4 rewrite of c10
  (contains CONFIRMED/CONFIRMED/UNRESOLVED + STRONGLY_SUPPORTED-in-census-scope + in-cell marker);
  all other cells verbatim. ORD 2 — all 10 cells verbatim except FUNCTION_IDENTITY, which is the
  source cell with exactly the single disclosed P3-2 replacement (byte-exact transform verified).
  ORD 3–8 — ORD/FUNCTION_ID/BUDGET_ROLE/FUNCTION_IDENTITY/IDENTITY_EVIDENCE/HISTORICAL_INPUT_
  AVAILABILITY/CITED verbatim (ORD 5 EXTENT = exact P3-3 transform; ORD 5 FINAL_SEMANTIC_ROLE =
  exact P3-5 transform; both verified byte-exact); FINAL_SEMANTIC_ROLE = the source semantic-role
  cell (right-aligned reconstruction confirmed by content); OBSERVED_OPERATION = reconstruction.
- EDGE: 16 rows fully verbatim (all 11 cells byte-equal to source); E-M1-INSERT = 10 verbatim cells +
  1 disclosed P3-5 STATUS rewrite (byte-exact transform verified); E-C1-PUSH = 10 verbatim cells +
  RECEIVER_PROOF = join of the split cells **with a space inserted after the comma** (F-QC-3);
  E-E1-CALL / E-GB1 / E-GB2 / E-XD = verbatim cells + exactly one reconstructed field each
  (PATH_CONDITIONS / FIELD_REGISTER_VALUE / RECEIVER_PROOF / RECEIVER_PROOF).
- **Zero unexplained deltas.** Every one of the 10 reconstructed cells is ABSENT from its source row
  (mechanically: `in_source_row = False` for all 10) — these are genuine reconstructions, not silent
  neighbor-shifts. No field was invented: every factual element of every reconstructed cell was
  verified present in the cited persisted evidence:
  - OBSERVED_OPERATION ORD 3/4/5/6/7 == source FINAL_REPORT §7 table values (ORD 3/6/7 byte-equal;
    ORD 4/5 equal modulo the arrow glyph — F-QC-2);
  - OBSERVED_OPERATION ORD 8 == synthesis of FINAL_REPORT §6 phrase + BYTE_WINDOWS F004157B0_head
    (8B F1 @0x004157B2; C7 06 18 9F A7 00 @0x004157B8) + the row's own FUNCTION_IDENTITY/EXTENT
    cells (all fragments verified in the artifacts);
  - E-E1-CALL PATH_CONDITIONS == supported by FUNCTION ORD 3 IDENTITY_EVIDENCE ("alloc-fail JZ
    0x00524816"), sibling E-E1-ABI RECEIVER_PROOF ("JZ 0x00524816 skips ctor"), BYTE_WINDOWS
    (74 14 JZ at 0x00524800) and the conditional call in GHIDRA_DECOMPILES;
  - E-GB1 FIELD_REGISTER_VALUE == supported by BYTE_WINDOWS A1 5C FE B9 00 @0x00401381 + FUNCTION
    ORD 6 ([0x00B9FE5C], 0x88 B, vtable 0x00A79F18) + E-GB2 class proof;
  - E-GB2 RECEIVER_PROOF == supported by BYTE_WINDOWS F004157B0_head + FUNCTION ORD 6 miss-path
    decode (PUSH 0x88; new @0x0040138F; ctor FUN_004157B0 @0x004013A9);
  - E-XD RECEIVER_PROOF == supported by BYTE_WINDOWS F0064B1E0_head (56 8B F1 @0x0064B1E1) +
    E-E2-EXTRADATA (6A 14; new(0x14); JZ 0x00509492) + FUNCTION ORD 7.
- **Join-position ambiguity handled honestly:** the E-C1-PUSH comma join and the four one-field-absent
  EDGE rows were resolved by right-alignment + content-anchoring + sibling-row structural analogy,
  with the residual ambiguity explicitly disclosed in QC_REPORT's RECONSTRUCTION_MAP and FINAL_REPORT
  finding 3 — consistent with the evidence; no alternative mapping is silently asserted as certain.
- **rel32 arithmetic:** every claimed E8 target recomputed by this QC's own arithmetic — 18/18 MATCH
  (12 in-ledger "recomputed" claims incl. all six getter callsites == exactly the 6-census set
  {0x004569D3, 0x00456BEB, 0x0045723E, 0x0045A08B, 0x00528FD9, 0x008561AC}; plus window-derived
  checks: new-thunk 0x0095D3C4 ×2, base ctor 0x007C8780, back-ptr 0x005094E0, list-reg 0x006A8980,
  GameClient ctor 0x004157B0).

**Validator audit (L14):** the production validator genuinely implements header-exact+unique, row
width, duplicate primary IDs, DictReader extra/missing (restkey/restval), no-empty-required-cells,
identity/source separation, CITED non-empty-or-UNKNOWN/NOT_CHECKED + existing-artifact traceability,
EDGE STATUS vocabulary + evidence-path detection + swap detection, FUNCTION no-STATUS-column +
prose non-emptiness (the edge enum is NOT applied to FUNCTION prose — correct per contract §7). It
never consults manifest/Git (mutation rejections are causal — confirmed by my different-row,
different-mechanism replicas). Its scope is honestly disclosed as "CSV schema + artifact-existence
layer only". Limitations observed: (a) fully-empty CSV rows are silently skipped (`rows[1:] if r`) —
my blank-line probe PASSES the checker (O-QC-1); the actual tables contain no blank lines (measured);
(b) the CITED check verifies "≥1 known token whose file exists", not that every cited fragment is
real — acceptable within the disclosed schema layer, since this QC independently verified the
reconstructions row-by-row against the cited evidence.

## 3. P3-1..P3-6 / DPA2 / DPA3 / Q14 verification

- **P3-1** CONFIRMED: source AMENDMENT 1 State-A display = 61 chars (missing `239`);
  `01_RAW/GovernanceWriteTime.txt` = the full 64-char `A953107598F7553C8DE5926EE7FA690920117E34923977B728F065AC073741A6`;
  the correction quotes both correctly; no byte-recovery or +25-B-delta claim is made.
- **P3-2** CONFIRMED from persisted bytes: BYTE_WINDOWS row `0x00528EA0: 00 00 C7 06 B0 DC A7 00
  89 9E A4 00 00 00 88 9E` → `C7 06 B0 DC A7 00` @0x00528EA2; `89 9E A4 00 00 00` @0x00528EA8.
  Corrected FUNCTION row 2 uses EA2 with in-cell disclosure; the source row's own IDENTITY_EVIDENCE
  already said EA2 (the internal inconsistency the Desktop flagged is resolved, not repeated).
- **P3-3** CONFIRMED: window `F00856190_mapinsert_full` = 0x00856190..0x0085620F (ends 0F; the
  epilogue `83 C4 10 C2 04` is in-window, the final RET byte 00 at 0x00856210 is not); inclusive
  body 0x00856190..0x00856210 = **129 B**; the source run's own QC_REPORT Q5 already used body
  ..0x00856210 and its F3 text pins the falsifier at 0x0085620B over `83 C4 10 C2 04` — three
  independent persisted records agree. The corrected EXTENT discloses the window limitation in-cell.
- **P3-4** CONFIRMED: the source HANDOFF/FINAL_REPORT/PE_MASTER_REVIEW carry the "≥3 receiver kinds"
  claims; corrected FUNCTION row 1 states ClientMovableObject CONFIRMED / GameClient CONFIRMED /
  additional [EBX] receiver form UNRESOLVED + "SHARED +0x74 OFFSET READER — STRONGLY_SUPPORTED in
  examined census scope"; no active "receiver kinds proven" remains in the new package.
- **P3-5** CONFIRMED: the broad phrase exists in source FINAL_REPORT §1.3; in the new package it
  occurs exactly twice (GOVERNANCE P3-5, QC_REPORT P3-5), both inside explicit "superseded by"
  statements — i.e., only as quoted historical retraction, never as an active claim. The scoped
  replacement wording is present (FINAL_REPORT/GOVERNANCE) and the direct-E8 negative is scoped to
  the measured five-address predicate {FUN_0072F580, FUN_006C9700, FUN_006CB6F0, FUN_006CB020,
  FUN_0043A550} in E-M1-INSERT + FUNCTION row 5.
- **P3-6** CONFIRMED: source QC_GATES.csv header = 6 columns; the G2 row naive-parses to **8 cells**
  (unquoted commas in `8,015,872 B`); the limitation is recorded in the correction; the artifact was
  not rewritten; its valid physical-byte results stay scoped.
- **DPA2** CONFIRMED: historical truth recorded exactly (MAX=6; FUN_0064B1E0 = function #7 full
  27-B body observed; ORIGINAL_PROCESS_BUDGET_COMPLIANCE = FAIL; breach preserved; present
  adjudication recorded separately as HUMAN_ADJUDICATED_NOW with RETROACTIVE_PRIOR_AUTHORIZATION =
  NO; TECHNICAL_QC separated from PROCESS_COMPLIANCE). No active compliance claim exists in the
  package (see F-QC-5 for a wording-precision note on the QC_REPORT sentence itself).
- **DPA3** CONFIRMED: the source GOVERNANCE attributes "persistence zrobi osobna faza — NIE
  commituj..." to a direct human instruction; the preserved VERBATIM block instead authorizes
  commit/push + manifest LAST + remote verification and contains no deferral instruction (mechanically
  verified inside the block). The correction sets PERSISTENCE_PHASE_SPLIT_SOURCE =
  NOT_ESTABLISHED_IN_RECORDED_HUMAN_SOURCE + ORCHESTRATOR_PHASE_SPLIT + FINAL_PUBLICATION_
  AUTHORIZATION = PRESENT, fabricates no message, back-fills no chronology, and does not claim an
  unpreserved message never existed. Historical files untouched (Q15 zero diff).
- **Q14** CONFIRMED: all ten required-unchanged conclusions verified present and unchanged in the
  corrected records (details in the verdict table); RESOURCE_EDGE_CONFIRMED / RESOURCE_EDGE_REJECTED_
  GLOBAL appear only inside the explicit "NOT converted to" negation in FINAL_REPORT §4. All content
  changes fall within the contract §15 allowed list (schema repair; corrected metadata/provenance/
  addresses/sizes/wording; process-budget adjudication; supersession routing).

## 4. Findings (all P3; none falsifies a load-bearing claim; none blocks publication)

**P3 / F-QC-1 — RECONSTRUCTION_MAP's ORD 1 cross-check annotation "equals FINAL_REPORT §7 row 1
verbatim" is inexact.**
Source: `QC_REPORT.md` RECONSTRUCTION_MAP, row "ORD 1 | OBSERVED_OPERATION". Measured: source FINAL_REPORT
§7 row 1 OBSERVED_OPERATION = `mov eax,[ecx+0x74]; ret`; the corrected cell =
`mov eax,[ecx+0x74]; ret - returns the dword at receiver+0x74` (which is the byte-exact join of the
source row's own split cells — verified). §7's value is a strict PREFIX of the corrected cell, not equal.
Effect: annotation imprecision only; the ledger cell itself is correct and fully traceable.
Correction: reword to "extends the §7 row-1 value (prefix) with the preserved source-row continuation".
Revalidation: string comparison §7-row1-obs vs corrected ORD1 OBSERVED_OPERATION (prefix test).

**P3 / F-QC-2 — "reconstructed VERBATIM from FINAL_REPORT §7" is inexact for ORD 4 and ORD 5 (arrow
glyph normalization).**
Source: `QC_REPORT.md` RECONSTRUCTION_MAP, row "ORD 3-7 | OBSERVED_OPERATION". Measured: §7 uses
U+2192 (`key → FUN_0064B1E0`; `duplicate→deleting dtor`); the corrected CSV uses ASCII `->`. ORD 3/6/7
are byte-verbatim; ORD 4/5 are equal only after arrow normalization. Effect: semantic content identical;
the "VERBATIM" label overstates byte-identity for two cells. Correction: disclose the ASCII arrow
normalization in the map (or make the cells byte-equal). Revalidation: byte-compare §7 obs vs
corrected OBS for ORD 4/5 (exact = False, normalized = True — expected disclosed state).

**P3 / F-QC-3 — E-C1-PUSH RECEIVER_PROOF join inserted a space after the embedded comma.**
Source: `EDGE_LEDGER_CORRECTED.csv` row E-C1-PUSH, RECEIVER_PROOF = `...(no conversion), from E-C1:
EAX=key`. Measured: the byte-exact join of the source split cells is `...(no conversion),from E-C1:
EAX=key` (no space). The FUNCTION ORD 1 joins are byte-exact (no space) — inconsistent normalization.
Effect: typographic only; both constituent texts are preserved verbatim; no content invented or lost;
the map's "join of raw C7+C8" does not mention the inserted space. Correction: disclose the space (or
make the join byte-exact). Revalidation: join-comparison c7+","+c8 vs the corrected cell.

**P3 / F-QC-4 — RECONSTRUCTION_MAP EDGE header label "17 verbatim rows" lists 16 rows.**
Source: `QC_REPORT.md` RECONSTRUCTION_MAP, EDGE table first row. Measured: 16 rows are fully verbatim
(11/11 cells equal); the 17th well-formed source row (E-M1-INSERT) is verbatim except its P3-5-scoped
STATUS, which the map discloses as its own row. Effect: count/label imprecision only. Correction:
"16 fully verbatim rows + E-M1-INSERT (STATUS scoped per P3-5)". Revalidation: mechanical
full-table comparison (this QC's C section already produces it).

**P3 / F-QC-5 — QC_REPORT Q11's literal string-absence sentence is self-referentially inexact.**
Source: `QC_REPORT.md` Q11: "The string 'BUDGET RESPECTED' does NOT occur for the original run
anywhere in this package". Measured: the uppercase string occurs 3× in the package — QC_REPORT Q11
itself, FINAL_REPORT §2 (DPA2: "'BUDGET RESPECTED' is never written for the original run") and
GOVERNANCE DPA2 ("Never written for the original run") — and the lowercase quoted form once in
HANDOFF's proposed entrypoint row (as explicitly-superseded framing). **Substance verified TRUE:**
every occurrence is a rule statement or an explicitly-superseded quotation; NO occurrence asserts
budget compliance for the original run. Effect: the sentence conflates "no active compliance claim"
with literal string absence; a machine string-scan (like this QC's) reports non-zero. Correction:
reword to "no active budget-compliance claim for the original run appears anywhere in this package".
Revalidation: case-insensitive scan classifying each occurrence's context (this QC's
BUDGET_RESPECTED_SCAN does exactly this).

**P3 / F-QC-6 — HANDOFF's proposed AUDIT_ENTRYPOINT row conflates the edge-scoped "budget respected"
phrase with the superseded process framing.**
Source: `HANDOFF.md` proposed row: "the original run's 'budget respected'/QC_PASS process framing
superseded". Measured: in the source package the phrase "budget respected" occurs only in
edge-budget statements ("Further call edges traced…: 2 (budget respected)" — FINAL_REPORT §6 and
HANDOFF), which were true in their own scope; the process framing DPA2 supersedes is Q7's "PASS WITH
ONE DISCLOSED DEVIATION" + Q9 QC_PASS + MASTER_ACCEPTED. Effect: shorthand imprecision inside a
PROPOSED row (AUDIT_ENTRYPOINT is not yet edited); the DPA2 records in GOVERNANCE/QC_REPORT/
FINAL_REPORT/SUPERSESSION are precise. Correction: in the persistence phase, replace the
"'budget respected'" shorthand with the Q7/Q9 labels (or explicitly scope it to the edge budget).
Revalidation: context classification of every "budget respected" occurrence in source + row.

## 5. Observations (non-gating)

**O-QC-1 — validator leniency: fully-empty CSV rows are silently skipped.**
`03_SCRIPTS/ledger_schema_qc.py` builds `data = [r for r in rows[1:] if r]`; a fully blank line is
dropped without failing any predicate (my blank-line probe returned rc=0 PASS). The contract's
mandatory mutation set (§8 MUT-A/B/C) does not include this case, and both actual tables contain zero
blank lines (measured: NO_BLANK_LINES PASS on both), so no contract predicate is violated. Disclosed
for the persistence phase's awareness; an optional hardening is a blank-line check.

**O-QC-2 — manifest regeneration required at persistence (by design).**
The 12-row manifest covers the phase-1 package state (13 physical files, manifest self-excluded;
AUDIT_ENTRYPOINT.md exclusion documented in the manifest comment — verified). This QC adds new files
under `00_CONTROL_INTERNAL_QC/`; the persistence phase must regenerate the manifest LAST with the
full scope (every physical package file + the updated AUDIT_ENTRYPOINT row) per the package's own
HANDOFF persistence instruction, and repeat the bijection verification. My QC records are:
QC_REPORT_INTERNAL.md, QC_GATES.csv, QC_INDEPENDENT_MEASUREMENTS.json,
QC_MUTATION_RESULTS_FRESH_QC.json, FULL_READ_LOG.txt, qc_independent.py, qc_mutations.py.

## 6. Coverage / NOT_CHECKED (explicit; see FULL_READ_LOG.txt for the full record)

- FULL_READ: the contract (917 lines), the Desktop post-audit (256 lines), all 13 package files
  (including the 471-line validator read to EOF), the source ledgers, source FINAL_REPORT,
  GOVERNANCE_DECISION, HANDOFF, QC_REPORT, PE_MASTER_REVIEW, QC_GATES.csv, BYTE_WINDOWS.txt,
  GovernanceWriteTime.txt, the prompt-review REVIEW.md.
- FULL_PARSE: both corrected ledgers (all rows × all fields), both source ledgers (naive),
  INPUT_IDENTITIES baseline (36 rows), the manifest (12 rows), source FINAL_REPORT §7 table,
  source QC_GATES.csv.
- NOT_CHECKED (explicit): full byte-identity of the verbatim human block vs the original 2026-10-06
  message (outside this QC's evidence set; verified consistent with the dispatch-quoted prefix,
  contract §0 and the prompt-review context); actual remote master (no fetch by this QC — local
  origin/master verified; persistence re-verifies); any EXE/PCG measurement (records-only; zero EXE
  reads by this QC); the source run's technical science beyond the preserved-conclusion checks
  (independently verified by the Desktop post-audit; this QC re-verified arithmetic + reconstruction
  traceability from persisted evidence only); interiors of foreign untracked paths; runtime,
  payloads, ExtraData consumers, indirect readers (unchanged NOT_CHECKED from the source run).

## 7. QC verdict block

```text
QC_VERDICT = QC_PASS_WITH_FINDINGS
FINDINGS = F-QC-1..F-QC-6 (all P3, documentation precision) + O-QC-1/O-QC-2 (observations)
BLOCKERS = NONE
PUBLICATION_BLOCKERS = NONE
FUNCTION_LEDGER_ROWS_MEASURED = 8 (10 exact cols)
EDGE_LEDGER_ROWS_MEASURED = 22 (11 exact cols)
SOURCE_DEFECT_CENSUS_MEASURED = 7/8 FUNCTION + 5/22 EDGE (Desktop DPA1 reproduced)
RECONSTRUCTED_CELLS_VERIFIED = 10/10 absent-from-source + traceable-to-cited-evidence
REL32_RECOMPUTE = 18/18 MATCH
MUT_REPLICATIONS = 5/5 REJECTED by the pinned production validator (different rows + different
  mechanism for MUT-A; same predicate classes as the executor's MUTATION_RESULTS.json)
Q15_SOURCE_REHASH = 36/36 byte-identical (own engine)
MANIFEST_REHASH = 12/12 rows equal; 13 physical files pre-QC; self-exclusion + entrypoint
  exclusion verified
Q14 = 10/10 required-unchanged conclusions preserved
P3_1..P3_6 = ALL verified against persisted evidence
DPA2 = CORRECTED (historical FAIL preserved; present adjudication separate)
DPA3 = CORRECTED (provenance statuses verified; commit f129fd5 remains authorized)
NO_NEW_SCIENCE = YES (this QC: records-only; zero EXE reads)
CANONICAL_GATE_EFFECT = NONE
NEXT_EXPERIMENT_AUTHORIZED = NO
```

This verdict is an internal QC result for PE-MASTER. It is not MASTER_ACCEPTED, not a milestone
closure, and not a publication. The persistence phase (PE-MASTER) must regenerate the manifest LAST
including these QC records and the AUDIT_ENTRYPOINT row, then perform the path-limited commit/push
and remote verification per contract §17–§18. The P3 findings F-QC-1..F-QC-6 may be repaired by a
records-only follow-up (or accepted as disclosed imprecision by PE-MASTER's audit); none of them
blocks publication.
