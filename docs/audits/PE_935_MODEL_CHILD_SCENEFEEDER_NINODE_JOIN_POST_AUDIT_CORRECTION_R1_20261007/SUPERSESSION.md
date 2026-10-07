# SUPERSESSION — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_POST_AUDIT_CORRECTION_R1_20261007

An explicit supersession record per contract §7 of OPENCODE_J1_J3_CORRECTION_REVIEWED.md
(SHA256 8BDE42C762FC49D615731CE1572D50E523C05672D7BC1AFD4E53EFB20B09C94E). The audited
source run is PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006 at commit
064b7f4aa4f3961f1a44212b2423e298eb51c291. The historical source package — including its
ledgers, its MANIFEST_SHA256.csv and its PE_MASTER_REVIEW.md — remains IMMUTABLE: no
historical file is edited by this correction, and supersession is recorded ONLY in the new
records of THIS package.

## 1. SUPERSEDED active interpretations of 064b7f4

For each item: the superseded interpretation, where it was stated (for the record), and the
superseding status in the corrected lineage. The technical BYTE EVIDENCE and the preserved
partial science are NOT falsified by any entry below.

S-1. Whole-package advisory `MASTER_ACCEPTED`.
  - Stated at: source PE_MASTER_REVIEW.md ("RUN_VERDICT = MASTER_ACCEPTED (advisory)",
    2026-10-06) and the 064b7f4 commit message.
  - SUPERSEDED as a whole-package interpretation: the independent Desktop post-audit of the
    exact published SHA (PE_935_MODEL_CHILD_SF_JOIN_DESKTOP_POST_AUDIT_064B7F4_20261007)
    returned REQUIRE_CORRECTIONS with three P2 findings (J1/J2/J3). The historical advisory
    text is preserved immutably; it is no longer an active acceptance interpretation of the
    corrected lineage.

S-2. The production qualification gate as a trustworthy positive semantic qualifier.
  - Stated at: source PE_MASTER_REVIEW.md line 22 ("Qualification gate: reads proof-chain
    structure (not just 4 status strings); ... the gate's failure barrier is exactly A/D"),
    source HANDOFF.md CTRL block, source QC_REPORT.md §3, and the 064b7f4 commit message.
  - SUPERSEDED: the Desktop counterexamples M1–M5 (five false-positive PASSes on the original
    gate, replayed and confirmed by the Desktop on the exact BASE gate SHA EF2D8E1F…) show the
    gate accepted declarations without physical evidence. The corrected gate
    (QUALIFICATION_GATE_CORRECTED.py, this package) runs with
    REAL_SCIENCE_AUTO_QUALIFICATION = DISABLED, returns separate SCHEMA/PIN/STRUCTURAL checks
    whose PASS is never SCIENCE_PASS, and rejects M1–M5 (M4/M5 by mechanical predicates, M1–M3
    honestly by policy). ACTIVE status:
    QC_POSITIVE_CHAIN_QUALIFICATION = NOT_ESTABLISHED_AS_GENERAL_AUTHORITY.

S-3. `6/6 edges, exhausted not exceeded`.
  - Stated at: the 064b7f4 commit message ("budget EXACTLY exhausted 8/8 functions, 6/6 edges,
    ..."), source PE_MASTER_REVIEW.md line 18/22 ("Budget census: 8/8 functions, 6/6 edges,
    ... — exhausted NOT exceeded"), source FINAL_REPORT.md §2 header ("budgets: 8/8 functions,
    6/6 edges, 4/4 candidates, 1/1 oracle"), source HANDOFF.md ("BUDGET USED = functions 8/8,
    edges 6/6 ..."), source QC_REPORT.md §2 S9 ("NEW_INTERPROCEDURAL_EDGES 6/6 (max 6) ...
    NO budget was exceeded").
  - SUPERSEDED: the 6/6 figure measured the length of the ledger list, not the performed
    scope. The records-only census (EDGE_BUDGET_RECONSTRUCTION.csv, this package; amended
    per the internal QC of this package, finding F-QC-1) reconstructs 22 DISTINCT new
    (caller,callee) pairs whose semantic analysis is recorded in the source run's own
    records — including the mandated 0x0050A3AF -> FUN_006C66D0 child-getter edge
    (receiver = manager; return EAX -> EDI; used as the CAND-4 child argument; callee body not
    decoded, which does not remove the edge) and the two F-QC-1-counted manager-method pairs
    (FUN_006C0F90 / FUN_006C10B0). ACTIVE statuses:
    MINIMUM_ANALYZED_EDGE_COUNT = 22 (re-derived 20 -> 22 by the F-QC-1 amendment);
    MAX_NEW_INTERPROCEDURAL_EDGES = 6 (NOT retroactively changed);
    ORIGINAL_EDGE_BUDGET_COMPLIANCE = FAIL.

S-4. `ZERO after-the-fact exceptions`.
  - Stated at: the 064b7f4 commit message ("... 2/2 wrappers, 1/1 oracle — ZERO after-the-fact
    exceptions"), source PE_MASTER_REVIEW.md line 18/22 ("... ZERO after-the-fact exceptions"),
    source FINAL_REPORT.md §7 SELF_CHECK ("8/8 functions, 6/6 edges ... STOPPED at the
    boundary; no after-the-fact exceptions"), source HANDOFF.md BUDGET USED line.
  - SUPERSEDED: at least 16 distinct uncharged analyzed interprocedural pairs exist beyond
    the 6 charged edges (22 - 6; re-derived by the F-QC-1 amendment from the pre-amend 14;
    see S-3). No after-the-fact exception is adjudicated by this correction;
    no retroactive authorization is claimed; the exceedance is recorded as the honest process
    fact. ACTIVE statuses: RETROACTIVE_PRIOR_AUTHORIZATION = NO; every whole-run
    process-compliance interpretation depending on "6/6 exhausted" or "zero exceptions" is
    superseded with it.

S-5. Transform `CONFIRMED_STATIC` as an authorized result of the source run.
  - Stated at (historical source quotes): source PE_MASTER_REVIEW.md line 14 — "SAME_INSTANCE_TRANSFORM_RELATION =
    CONFIRMED_STATIC (SEPARATE status; full pins verified by internal QC; does NOT promote the join)" — plus source
    FINAL_REPORT.md §1.5/§3, source CLAIM_MATRIX.csv CL-08 — "CONFIRMED (NEW #5) — recorded as
    SAME_INSTANCE_TRANSFORM_RELATION=CONFIRMED_STATIC (path-conditional)" — plus source HANDOFF.md line 34, source
    FUNCTION_BUDGET.csv row #5 (PRIOR_SCOPE_NOTE=none; the ledger itself classifies the trace as NEW, not
    inherited/re-pinned).
  - SUPERSEDED as an ACTIVE run-qualified conclusion: the source contract permitted
    SAME_INSTANCE_TRANSFORM_RELATION only as an existing, re-pinned evidence note and excluded
    a separate new transform trace; the source run nevertheless promoted a full new
    FUN_00509850 transform semantic. ACTIVE statuses:
    PHYSICAL_TRANSFORM_MEASUREMENTS = PRESERVED (all raw windows/measurements unchanged;
    re-hashed == BASE blobs by this correction's QC);
    NEW_TRANSFORM_TRACE = MEASURED_INCIDENTAL_OUTSIDE_PERMITTED_PROMOTION;
    SAME_INSTANCE_TRANSFORM_RELATION_FROM_THIS_RUN = NOT_QUALIFIED_BY_ORIGINAL_SCOPE.
    NOT described as inherited/re-pinned; NO prior human authorization claimed; future
    acceptance requires a new explicit present human decision (none exists).

## 2. PRESERVED (NOT superseded; contract §7 "Preserve")

- The exact ACLD SF+0x30 parent: EXACT_PARENT = CONFIRMED_EXACT_SCENEFEEDER_PLUS_30, scoped to
  the examined ArkClientLocalDynamic+0x18 SF instance (PARENT_SCOPE =
  EXAMINED_ACLD_PLUS_18_SF_INSTANCE; the SF-island CMO+0xC0 instance is a different holder; no
  identity or CMO-transform transfer into the ACLD chain).
- The join callsite bytes: the 0x0050A3E9..0x0050A3F7 window
  (`8B 4E 30 / 8B 01 / 8B 90 A4 00 00 00 / 6A 00 / 57 / FF D2`), receiver = [SF+0x30], NiNode
  vtable slot 41 = FUN_007B5810 — CONFIRMED_IN_EXAMINED_ACLD_SCOPE.
- The STRONGLY_SUPPORTED AttachChild counterpart (JOIN_OPERATION): fingerprint
  F1/F2/F4/F5 byte-verified vs the pinned EXE; F3 call-through body undecoded; PCG
  engine-generation not era-exact with the Gb12 oracle — the status ceiling is unchanged; the
  operation is NOT promoted to CONFIRMED by this correction.
- A unresolved: CHILD_MODEL_PROVENANCE = UNRESOLVED (FUN_006C66D0 and the manager's
  model/resource provenance not traced).
- D unresolved: CHILD_VISUAL_ROLE = UNRESOLVED (no physical visual-role proof).
- SCIENCE_OUTCOME = PARENT_FOUND_CHILD_UNRESOLVED (the honest partial result stands).

## 3. Immutability and scope statements

- The historical source package at BASE 064b7f4 (49 files, re-hashed by this correction before
  and after work: 49/49 git-blob identity match, aggregate SHA256
  ab21cbc3991c91b19bd884f851e0fe24f1eba251b48e24643a71f6169be65b5b unchanged) is read-only and
  is not edited, rewritten, or re-manifested by this correction.
- The historical PE_MASTER_REVIEW.md is preserved VERBATIM as a historical record; the
  supersession of its ACTIVE interpretations (S-1, S-2, S-3, S-4, S-5) is recorded here and in
  CORRECTED_STATUS_ALGEBRA.md section B, per the no-in-place-rewrite rule.
- This supersession does not close the J1–J3 corrections: the independent PE-MASTER audit of
  THIS package is pending, and no correction is claimed closed merely by this execution.
