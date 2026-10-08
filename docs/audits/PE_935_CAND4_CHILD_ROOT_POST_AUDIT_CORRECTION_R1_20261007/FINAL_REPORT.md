# FINAL_REPORT — PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007

RUN_CLASS: RECORDS_AND_QC_MACHINERY_CORRECTION · Era: PCG 9.3.5 · Executor:
pe-reconstruction (PE-MASTER direct dispatch, NO_NESTED_TASKS). BASE_SHA
790e83735b439e2d76a250868a47a599c2c10184 (== LOCAL_HEAD == origin/master == actual
remote master, verified at preflight 2026-10-07T18:37Z; re-verified at package close).
SOURCE_RUN (audited, READ-ONLY): PE_935_CAND4_CHILD_ROOT_PROVENANCE_R1_20261007 at
790e837 (38 files; BASE git-blob identity 38/38 before AND after the work —
SOURCE_PACKAGE_UNCHANGED). AUTHORITY: Desktop post-audit C4-C1/C4-C2 of 790e837,
verdict REQUIRE_CORRECTIONS (all three inputs read in full; identities MATCH).
THIS PHASE: records/QC-machinery corrections + fresh internal QC (SELF-REVIEW) +
package. NO AUDIT_ENTRYPOINT edit, NO commit/push (the proposed newest-first row is in
HANDOFF.md; persistence belongs to PE-MASTER after its own audit). RESULTING_SHA = NONE
(this phase).

---

## 1. Dispositions (contract §1–§7 — actual results)

### C4-C1 EDGE ACCOUNTING — CORRECTED (records); historical compliance FAIL stands

- RETRACTED (superseded; SUPERSESSION.md S-1..S-4): "ACCOUNTED_EDGE_COUNT = 24" as a
  complete total; "INDEPENDENT_RECONSTRUCTED_EDGE_COUNT = 24" as a complete-census proof;
  "exceedance exactly 24/+16"; "zero semantic analysis hidden under RAW_VISIBLE".
- CORRECTED_EDGE_ACCOUNTING_LEDGER.csv: full re-adjudication of all 69 source rows by
  ROW CONTENT (the original columns preserved VERBATIM — 69 rows x 9 fields
  byte-identical; never retyped). Counted set = 32 (24 historical ANALYZED_NEW with
  recorded interpretations + RV-01..RV-07 + NEIGH-09, whose NOT_COUNTED_REASON content
  records interpretations: argument construction; temp init x2; cleanup x4; receiver
  esi + result as argument of FUN_006C9F30). Non-counted: 11 PRIOR_REPIN_EXEMPTION_
  UNREVERIFIED (exemptions retained; prior-record citations NOT re-verified here),
  17 NOT_COUNTED_CLEAN (no callsite interpretation in the row content), 9
  CANDIDATE_UNADJUDICATED (annotations that MAY constitute §3 interpretations —
  e.g. NEIGH-15's receiver [esp+0x40], NEIGH-04's new(0x68), NEIGH-07's body-role label
  — whose counting was NOT adjudicated by the authoritative post-audit nor by this
  correction; no new interpretive science in a records correction).
- Conservative status (proven floor): MINIMUM_NEW_ANALYZED_EDGE_COUNT = 32 (>= 32).
  EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED (the candidates + the repin exemptions are
  not exhaustively adjudicated; the exact total is not provable from existing records).
- ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL (historical; 32 > MAX 8; exceedance >= +24,
  not exact). RETROACTIVE_PRIOR_AUTHORIZATION = NO. ORIGINAL_SCOPE_COMPLIANCE = FAIL.

### C4-C1 FUNCTION BODY ACCOUNTING — CORRECTED (records); historical compliance FAIL stands

- FUNCTION_BODY_ACCOUNTING.csv: the historical CTRL_3 performed a REAL 8-byte EXE probe
  of FUN_006C0EE0 (`8B 81 20 01 00 00 C3 CC`) and interpreted it as the manager+0x120
  getter — an UNDECLARED real-body probe (Desktop C4-C1 counterexample; absent from both
  declared prior packages). Per the source-run contract §2 rule it is counted
  retroactively as a HISTORICAL consumption: MINIMUM_NEW_FUNCTION_BODIES_OPENED = 7
  (>= 7; the proven 7th). ORIGINAL_FUNCTION_BODY_BUDGET_COMPLIANCE = FAIL (supersedes
  the source run's "6/6 within, NOT exceeded"). EXACT_NEW_FUNCTION_BODIES_OPENED =
  UNRESOLVED (the bounded-window neighbor-body raw display question is recorded as
  CANDIDATE_UNADJUDICATED; a records-only scan of the audited run's scripts found ZERO
  other undeclared probes — 31 distinct read VAs all within the accounted scope — but
  the unrecorded execution history is not provable from records).
- THIS correction opens NO new body (NEW_PCG_FUNCTION_BODIES_ALLOWED = 0; zero EXE
  access of any kind).

### C4-C2 CTRL_4 EXACT ENDPOINT — REBUILT (machinery); the corrected checker verified

- CONTROL_RESULTS.json (CTRL_4_EXACT_ENDPOINT_REBUILT) + 03_SCRIPTS/
  ctrl4_exact_endpoint.py: the rebuilt checker requires SIMULTANEOUSLY — P1 exact head
  mov edi,eax @0x0050A3B7 (bytes 8B F8); P2 no caller-side EDI write in the required
  range; P3 exact final child argument push edi @0x0050A3F6 (byte 57); P4 exact join
  call endpoint call edx @0x0050A3F7 (bytes FF D2, no shift) — each verified as the
  instruction AT THE EXACT ADDRESS on correct decode boundaries (boundary-safe linear
  decode; a CALL mnemonic anywhere else in the window is never accepted; the earlier
  push edi @0x0050A3D7 does NOT satisfy P3).
- Required matrix (all executed, all SYNTHETIC/IN-MEMORY ONLY): REAL CLEAN = PASS;
  historical EDI-clobber mutant (@0x0050A3DD, 8B 3D D0 D8 B9 00) = FAIL; mutant
  @0x0050A3F6 push edi -> push esi (57->56) = FAIL; mutant @0x0050A3F6 push edi -> nop
  (57->90) = FAIL. Matches the Desktop own_exact_endpoint_predicate exactly. The old
  checker's LOGIC reproduction over the same buffers: clean PASS; clobber FAIL; FALSE
  PASS on both final-argument mutants (the two Desktop false PASS — reproduced, not
  rewritten history: the historical clean PASS / EDI-clobber FAIL results remain
  authentic measurements of the old checker; SUPERSESSION.md S-6).
- CTRL_4 semantic scope UNCHANGED: caller-side exact final-argument predicate ONLY —
  CHILD_TO_JOIN_IDENTITY is NOT promoted to CONFIRMED (the four intervening callee
  bodies FUN_006C0F90/FUN_006C10B0/FUN_0050A1E0/FUN_005246E0 remain unopened).
- CTRL_3 REBUILT (contract §2): same wrong-manager-field predicate over SYNTHETIC
  fixtures / persisted prior pins only — clean = the persisted getter pin
  (8B 41 68 C3 CC CC CC CC) PASS; mutated = the recorded historical probe constant
  (8B 81 20 01 00 00 C3 CC) FAIL (reads [ecx+0x120], not [ecx+0x68]); ZERO EXE access;
  no new real accessor discovery (CTRL3_SYNTHETIC_OR_PRIOR_PIN_STATUS =
  SYNTHETIC_FIXTURES_AND_PERSISTED_PRIOR_PINS_ONLY).

### WRAPPER / LINEAGE — TERMINOLOGY CORRECTED (semantics != budget consumption)

- CORRECTED_LINEAGE_STATUS.md: WRAPPER_DEPTH = UNRESOLVED (the source run's
  "WRAPPER_DEPTH = 2" semantic claim superseded — S-7); MODEL_ROOT_RELATION = UNKNOWN;
  POINTER_LINEAGE_TRANSITIONS_OBSERVED = 2 (the examined H-1/H-2 description, NOT a
  global census); H-2 RELATION_TYPE = UNRESOLVED.
- Historical budget consumption PRESERVED (contract §4): NEW_WRAPPER_HOPS = 2 (charged
  analysis units of the original run) / MAX_NEW_WRAPPER_HOPS = 3 (unchanged). The
  unresolved H-2 relation still consumed the budget — NOT zeroed, NOT reduced; the two
  charged units do NOT establish two model-wrapper layers.

## 2. Science preservation (contract §5 — nothing raised, nothing broken)

PRESERVED raw facts (byte measurements — NOT superseded; SUPERSESSION.md NOT-superseded
list): FUN_006C66D0 = DIRECT_FIELD_GETTER [manager+0x68] (8B 41 68 C3); the base-ctor
NULL-init of +0x68 (89 5E 68 @0x006C8FD3); the measured store [manager+0x68]=[instance+4]
(89 7E 68 @0x006C67E2 / 8B 78 04 @0x006C67BE with the refcount protocol); the lazy
producer chain byte/dataflow facts (FUN_006C8B20 trigger -> FUN_006C6F60 producer ->
FUN_006C6780 writer; validity FUN_0072FCE0; empty-string-key lookups; getter A =
FUN_007CE1E0; pump FUN_006C9700 -> [+0x6C]); the join-window bytes (8B F8 @0x0050A3B7;
57 @0x0050A3F6; FF D2 @0x0050A3F7); all 56 byte pins + 23 rel32 recomputes; the RTTI
names; the string constants; EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30
(carried, ACLD-scoped).

NOT promoted (standing statuses, verified by the QC): CHILD_RESOURCE_PROVENANCE =
STRONGLY_SUPPORTED_MODEL_DERIVED (ceiling unchanged — GAP-1 [instance+4] identity and
GAP-2 FUN_006C8BB0 stand); MODEL_ROOT_RELATION = UNKNOWN; CHILD_VISUAL_ROLE =
UNRESOLVED; CHILD_TO_JOIN_IDENTITY = STRONGLY_SUPPORTED (NOT CONFIRMED);
CAND4_CHILD_ROOT_CLOSURE = NOT_ESTABLISHED_WITHIN_BOUND. No new science interpretation
was created by this correction (the QC verified the 8 additionally counted units quote
ONLY recorded source content; the forbidden-ACTIVE-token sweep is clean).

## 3. Fresh internal QC (contract §6) — SELF-REVIEW

QC_ORIGIN = SELF-REVIEW — fresh internal QC by the SAME pe-reconstruction executor
session that produced this correction package (author: pe-reconstruction); NOT an
independent external Desktop post-audit; NOT a PE-MASTER qualification; the independent
Desktop post-audit of THIS correction's SHA remains NOT_PERFORMED (pending
persistence/publication). Machine record: 03_SCRIPTS/qc_correction.py ->
03_SCRIPTS/QC_CORRECTION_RESULTS.json — QC_PASS 21/21 (with ONE QC-tooling defect round
disclosed and fixed in the QC script only; QC_REPORT.md §6). Highlights: what
qc_correction.py check C2 actually does with the corrected-ledger classification
(this §3 wording corrected per the independent internal QC finding F-IND-2;
QC_REPORT.md §1 and §8 record the repair): the row's LEDGER_CLASS is used as the
BRANCH SELECTOR for the 24 E-rows (within that branch the row content IS checked —
counted iff NEW_INTERPRETATION is non-empty); the 8 mandatory rows RV-01..RV-07 +
NEIGH-09 are verified by CONTENT (the marker phrases in their NOT_COUNTED_REASON); the
remaining 37 rows are assigned not-counted DERIVATIONALLY, without per-row content
examination (C2 alone would not have caught a misclassified RP row; for those rows the
C4 agreement is structurally guaranteed); the corrected ledger's own CORRECTED_COUNTED
/ CORRECTED_CLASS columns were only compared, never trusted. The FULL per-row
independent content adjudication of ALL 69 rows (zero differences vs the corrected
ledger; the stricter reading could only RAISE the floor) was performed by the fresh
INDEPENDENT internal QC (00_CONTROL_INTERNAL_QC/QC_IND_REPORT.md §2 /
QC_IND_RESULTS.json check I6) — THAT adjudication, not C2, is the independence basis
of the 32/11/17/9 classification. The conservative minimums confirmed (>= 32 / >= 7);
the rebuilt controls re-executed from import; the clean CTRL_4 buffer re-derived from
the published window record (22 instructions, contiguous boundaries, 0x42 bytes,
branch arithmetic exact); the historical budget FAILs preserved.

```text
CORRECTION_RECORDS_QC = PASS  (the result of the NEW correction's records/machinery)
ORIGINAL_SCOPE_COMPLIANCE = FAIL  (the HISTORICAL state of the audited run; separated
  from CORRECTION_RECORDS_QC; never becomes PASS)
```

C4-C1 and C4-C2 are NOT declared closed by this self-review — closure belongs to the
PE-MASTER audit + persistence and (for the new SHA) an actually-executed independent
post-audit. No SCIENCE_PASS is issued anywhere.

## 4. Package + integrity

- Package (OUTPUT_ROOT; REPO_WRITE_ALLOWLIST honored): INPUT_IDENTITIES.md,
  GOVERNANCE_DECISION.md, CORRECTED_EDGE_ACCOUNTING_LEDGER.csv,
  FUNCTION_BODY_ACCOUNTING.csv, CORRECTED_LINEAGE_STATUS.md, CONTROL_RESULTS.json,
  QC_REPORT.md, SUPERSESSION.md, PE_MASTER_REVIEW.md (placeholder —
  NOT_PERFORMED-do-persistence), FINAL_REPORT.md, HANDOFF.md, MANIFEST_SHA256.csv
  (generated LAST) + 03_SCRIPTS/ (ctrl3_rebuilt.py, ctrl4_exact_endpoint.py,
  build_corrected_ledger.py, qc_correction.py, make_manifest.py, FIXTURES.md,
  QC_CORRECTION_RESULTS.json).
- SOURCE_PACKAGE_UNCHANGED: 38/38 BASE git-blob identity verified BEFORE the work and
  re-verified AFTER the work (zero mismatches, zero missing); zero writes into any
  historical package; old scripts with top-level writes into SOURCE_PACKAGE were NOT
  executed (needed logic re-implemented with pinned provenance in this package).
- Repo state at package close: HEAD == BASE 790e837…; zero tracked modifications; the 6
  foreign untracked roots untouched; changed-path census = exclusively
  docs/audits/PE_935_CAND4_CHILD_ROOT_POST_AUDIT_CORRECTION_R1_20261007/** (created by
  this run); AUDIT_ENTRYPOINT.md NOT edited; no commit/push by this executor
  (RESULTING_SHA = NONE this phase).
- Manifest: generated LAST over the physical package files minus itself; entrypoint
  EXCLUDED pending persistence (noted in the header); generator bijection self-check
  PASS; independent post-generation re-hash by a separate implementation (.NET SHA-256
  via PowerShell) reported in the terminal response — not persisted as a package file
  (any write after the manifest requires regeneration + re-verification).
- Process: every package file UTF-8 no-BOM with LF line endings; no __pycache__; scratch
  outside the repo.

## 5. Open findings / unresolved (honest)

1. EXACT_NEW_ANALYZED_EDGE_COUNT = UNRESOLVED — the 9 CANDIDATE_UNADJUDICATED rows
   (NEIGH annotations: receiver [esp+0x40]; new(0x68); body-role labels; topology
   notes) and the 11 repin exemptions were NOT adjudicated; adjudicating them would
   raise the floor and requires a decision of the human/PE-MASTER, not this correction.
2. EXACT_NEW_FUNCTION_BODIES_OPENED = UNRESOLVED — the bounded-window neighbor-body
   raw display question (CANDIDATE row C1 of FUNCTION_BODY_ACCOUNTING.csv).
3. The historical scope-compliance FAILs are permanent process facts (edge >= 32 vs
   MAX 8; bodies >= 7 vs MAX 6); no retroactive authorization exists or is claimed.
4. GAP-1 ([instance+4] identity via FUN_006C9700) and GAP-2 (FUN_006C8BB0) remain the
   recorded next-input candidates of the SOURCE run — NOT opened, NOT authorized here.

## 6. Governance statuses (unchanged)

WORLD_XYZ_RECOVERED = NO · HISTORICAL_INSTANCE_DATA_RECOVERED = NO ·
STATIC_BUILDING_CHANNEL = NOT_ESTABLISHED · RUNTIME_JOIN_OBSERVED = NO ·
CANONICAL_GATE_EFFECT = NONE · REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED ·
NEXT_EXPERIMENT_AUTHORIZED = NO. NEXT_EXPERIMENT_AUTHORIZED stays NO after this
correction; no FUN_006C9700, FUN_006C8BB0, historical XYZ or any other science run was
started. HARD STOP after the package + manifest + bijection verification.
