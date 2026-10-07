# QC_REPORT — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006

SELF-CLASSIFICATION: this is the executor's own TARGETED / FRESH-CONTEXT INTERNAL QC
(SELF_CHECK). It is NOT independent external Desktop post-audit and NOT PE-MASTER
qualification. Machine measurements: 03_SCRIPTS/qc_reverify.py ->
03_SCRIPTS/qc_reverify_results.json (OVERALL = QC_PASS, 14/14 checks).
Qualification-gate machine results: 03_SCRIPTS/qualification_gate.py ->
03_SCRIPTS/qualification_results.json (OVERALL = PASS).

## 1. What was re-verified independently (fresh reads from the hash-pinned EXE)

- S1 EXE identity: size 8,015,872 / SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 — MATCH (fail-closed inside the QC tool).
- S2 25 load-bearing byte pins re-read at their exact VAs (PA1/PA2/PA3/PA4 re-pins,
  the CH1 emitter sites, the FUN_008BD720 body, the three CMO-ctor SF-method callsites,
  the transform-write site, the [SF+0x20] store, the child-getter callsite, the join-site
  parent load + virtual call, the AttachChild fingerprint instructions: refcount-inc
  01 5E 04, children-object LEA +0xC8, used/alloc field reads, the set-at call, the
  dec/destroy site) — ALL MATCH.
- S3 17 rel32 call targets recomputed independently (the SF factory, FUN_0050A310,
  FUN_006C66D0, FUN_0050A1E0, FUN_007BF900/0x7BF630/0x7BF500, FUN_007BF470,
  FUN_007B55E0, FUN_00788570, FUN_007790D0, the scheduler entry FUN_006C3640, the
  registry getter/lookup chain) — ALL MATCH.
- S4 Join-site receiver preservation: the window 0x0050A3E9..0x0050A3F8 decodes as
  `8B 4E 30 / 8B 01 / 8B 90 A4 00 00 00 / 6A 00 / 57 / FF D2` — ECX is loaded from
  [SF+0x30] at 0x0050A3E9 and the ONLY intermediate ECX use is the vtable READ
  (MOV EAX,[ECX]); no ECX write occurs before CALL EDX at 0x0050A3F7 — the receiver
  of the join call is byte-proven to be the exact SF+0x30 NiNode value. ARGUMENT
  PRESERVATION: EDI (the child) is pushed at 0x0050A3F6 unchanged from the
  FUN_006C66D0 result at 0x0050A3B7 (no EDI write in between — verified in
  01_RAW/FUN_0050A310_DECODE.txt).
- S5/S6/S7 Receiver/source chains re-read: FUN_0050A310 head (ESI=ECX=this=SF);
  the SF creation chain in FUN_006A3930 (FUN_005247C0 @0x006A39ED -> [ACLD+0x18]
  @0x006A39F6); the manager chain (new 0x130 -> FUN_006C0D50 @0x006A3A77 ->
  FUN_006C8B20/BB0 -> [ACLD+0x18] receiver -> FUN_0050A310 @0x006A3A9D) — ALL MATCH.
- S8 NiNode vtable data: slot 41 (+0xA4) = 0x007B5810, slot 42 (+0xA8) = 0x007B5A00
  (the detach-shaped call at 0x0050A35A uses slot 42) — MATCH.

## 2. Budgets, ledgers, statuses

- S9 budgets: NEW_DETAILED_FUNCTIONS 8/8 (max 8), NEW_INTERPROCEDURAL_EDGES 6/6
  (max 6), JOIN_CANDIDATES_DETAILED 4/4 (max 4), ORACLE_MECHANISMS 1/1
  (AttachChild + its AttachParent step), WRAPPER_DEPTH traversed 2 of max 2
  (FUN_006A3930 -> FUN_0050A310 -> the slot-41 edge; the child's next wrapper
  FUN_006C66D0 NOT traversed). NO budget was exceeded; analysis STOPPED at the
  boundary (see §4).
- S10 Ledger schemas: header/order/width/duplicate/null validation PASS for all four
  ledgers (csv.DictWriter + validator; build_ledgers.py).
- S11 Overclaim sweep of the ledgers: no "INSTANCE_MODEL_NODE_JOIN=CONFIRMED",
  no "CONFIRMED_MODEL_DERIVED" child claim, no runtime-observation claim, no
  transform-to-model promotion — CLEAN.
- S14 Status algebra: CAND-4 carries A=UNRESOLVED, B=CONFIRMED (scoped),
  C=STRONGLY_SUPPORTED, D=UNRESOLVED -> INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED
  (no averaging up; CONFIRMED_STATIC_CONDITIONAL NOT claimed).
- S12 Repo state: HEAD == 24f45e0108b922c26ff584fee9ef7749de0390b6 (BASE unchanged);
  ZERO tracked modifications; foreign untracked roots untouched
  (docs/audits/… 5 foreign packages + experiments/; this run's own package dir is the
  only new untracked content under docs/audits/ belonging to this run).

## 3. Qualification gate (structure-reading, not status-string-reading)

- The gate (03_SCRIPTS/qualification_gate.py) reads a typed PROOF-CHAIN structure:
  sf_creation -> sf_store -> parent_identity_access(field=+0x30) -> parent_receiver ->
  child_provenance(physically_established_model_resource_op) -> join_operation
  (children_array_insert_on_parent) -> visual_role, and verifies every byte claim of
  non-synthetic chains against the EXE.
- BASELINE = SYNTHETIC_GATE_TEST_ONLY fixture -> PASS (the gate can pass; the fixture
  is NOT PCG finding/evidence and does NOT promote INSTANCE_MODEL_NODE_JOIN — its
  edges are marked synthetic=True and it is named SYNTHETIC_GATE_TEST_ONLY).
- CTRL-A (parent -> other-node) -> FAIL, primary rejection by the PARENT predicate
  (a downstream operation-parent consistency failure is a legitimate cascade of the
  same mutation — the operation must bind THE receiver node).
- CTRL-B (child model-provenance removed) -> FAIL by the CHILD predicate.
- CTRL-C (identity edge +0x30 -> +0x34) -> FAIL by the PARENT-IDENTITY predicate.
- REAL CAND-4 chain evaluation -> FAIL on P_CHILD and P_VISUAL (its 5 byte claims
  r1/r2/r3/r4/r6 all verified MATCH against the EXE) — the gate does NOT
  rubber-stamp the real candidate; consistent with INSTANCE_MODEL_NODE_JOIN =
  NOT_ESTABLISHED.
- Not checker-always-FAIL: proven by the baseline PASS.

## 4. Honest QC findings (recorded, not repaired in evidence)

1. QC ROUND-1 DEFECT (QC tooling, fixed in the QC script itself; evidence NOT
   touched): the first qc_reverify.py run had 2 check-specification errors:
   (a) S2 PA2 pin expected a 13-byte string for a 14-byte read (the 14th byte 02 of
   the true window made the comparison fail although the actual bytes were correct
   and identical to 01_RAW/REPIN_ANCHOR_WINDOWS.txt PA2c); (b) S14 used string
   equality against a longer annotated status cell instead of a prefix test. Both
   were fixed in the QC script; the re-run is QC_PASS 14/14. No executor evidence
   file was modified by QC.
2. The fun_00509670 call at 0x0050A31B inside FUN_0050A310 (before the join section,
   on the [SF+0x24]==1 branch) was NOT decoded — recorded as NOT_CHECKED (budget).
3. FUN_007BF470 (the AttachParent-shaped direct call inside FUN_007B5810),
   FUN_007B5A00 (the detach-shaped slot 42 target), FUN_006C0EC0/ED0/FA0/FB0/F90/
   10B0/66D0, FUN_0050A1E0, FUN_005246E0, FUN_0096CDD0, FUN_0048BAC0 — all NOT
   decoded (budget boundary; recorded in the ledgers as unresolved boundaries).
4. The slow one-instruction-at-a-time capstone census attempt
   (scan_sf20_ext.py) TIMED OUT and was superseded by the fast byte-pattern census
   (scan_sf20_fast.py) — recorded; no results from the aborted scan were used.
5. The SF20_EXTERNAL_WRITER_SCAN (+0xC0-load -> +0x20-store window pattern) found
   ZERO hits — a true negative: no such direct pattern exists; the actual [SF+0x20]
   writer was found inside FUN_0050A310 (an SF-class method) after all.

## 5. QC verdict

QC_VERDICT = QC_PASS (SELF_CHECK) — with the explicit classification note above.
The strongest candidate (CAND-4) has byte-proven parent identity and an
AttachChild-shaped operation (STRONGLY_SUPPORTED), but its child's model/resource
provenance and visual role are UNRESOLVED at the budget boundary; the science outcome
PARENT_FOUND_CHILD_UNRESOLVED is consistent with every measurement.

## 6. RECORD-REPAIR (records-only dispatch executed 2026-10-06T23:36:20-07:00, PE-MASTER adjudication of the independent internal QC)

Origin = internal QC findings F-QC-1..F-QC-6 (00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md,
QC_RUN_ID PE_935_MODEL_CHILD_SF_JOIN_INTERNAL_QC_R1_20261006, QC_VERDICT =
QC_PASS_WITH_FINDINGS), adjudicated by PE-MASTER: F-QC-1..F-QC-4 CORRECT-AND-FIXED,
F-QC-5/F-QC-6 DISCLOSED_NO_ACTION. RECORDS-ONLY repair: no new decoding/RE, no byte-value
changes in any raw window, no status/claim changes; SCIENCE OUTCOME =
PARENT_FOUND_CHILD_UNRESOLVED unchanged; INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED
unchanged; all prior QC verdicts stand unchanged.

- F-QC-1 (P2) FIXED — 01_RAW/REPIN_ANCHOR_WINDOWS.txt: the CH2a caption was corrected. The
  window (VA 0x0064b1ec LEN 16) is the FUN_0064B1E0 body tail (a duplicate of the PA2b
  window), NOT "FUN_008BD720 first bytes". VA/BYTES unchanged (true EXE bytes,
  byte-verified by the internal QC); the real FUN_008BD720 accessor record (8D 41 18 C3
  @0x008BD720, 01_RAW/FUN_008BD720_DECODE.txt) untouched; no claim cites CH2a.
- F-QC-2 (P2) FIXED — INPUT_IDENTITIES.json: oracle_sources[].measured_at_use (was null,
  contradicting INPUT_IDENTITIES.md §5 and 01_RAW/FUN_007B5810_ORACLE_BYTE_PROOF.txt)
  filled with the actual at-use measurements — NiNode.cpp 33,897 B /
  38C7A1DE1E166345068D296F70F34B1ADAE27C694E19EAD8FA0FBD8B62E0E016 and NiAVObject.cpp
  33,215 B / 72E0837149B03CCDA171BDF5E68E1E1F8C2712B2F10E7957AC3EC26344CA5EA7, both MATCH
  vs expected — with the records-based measurement time (file mtime of
  01_RAW/FUN_007B5810_ORACLE_BYTE_PROOF.txt = the at-use measurement record; no in-record
  timestamp was saved) plus a repair-time re-hash annotated regenerated_at (MATCH).
  Substance was already verified by the internal QC (its own re-hash of both files
  MATCHed the recorded identities).
- F-QC-3 (P2) FIXED — FINAL_REPORT.md §2: the "FUN_0050A310 was fully decoded" wording
  replaced with the precise wording — the decoded window is 0x0050A310..0x0050A42F
  (LEN 288) while the function's true extent (internal QC measurement) is
  0x0050A310..0x0050A45C (terminal ret 0x4 @0x0050A459 + int3 padding); the undecoded
  tail 0x0050A42B..0x0050A45C contains NO join-bearing content; every join-bearing item
  lies inside the decoded window; explicitly reconciled with FUNCTION_BUDGET.csv's honest
  "0x0050A310..0x0050A453+" continuation notation. FUNCTION_BUDGET.csv itself was checked
  and intentionally NOT modified (its notation is honest per the QC; hand-editing the
  generated ledger would break the build_ledgers.py regeneration identity that the
  internal QC verified byte-for-byte).
- F-QC-4 (P3) FIXED — 01_RAW/SF20_WRITER_CENSUS.txt: the NiNode vtable dump legend
  corrected to "47 canonical slots" with the 48th listed row (slot 47, +0xBC, 0x65666665)
  marked as a PAST-THE-END ASCII artifact, not a vtable entry; all rows/values unchanged;
  slot 41 (the load-bearing entry) unaffected. EVIDENCE_INDEX.md's "FULL NiNode vtable
  dump (47 slots)" wording matches the corrected canonical slot count and was left
  untouched (outside the authorized repair census).
- F-QC-5/F-QC-6 (P3) DISCLOSED_NO_ACTION — mid-instruction window starts (PA1b/CH3a/the FUN_006A3930 window) and the EDI callee-saved convention across four undecoded intermediate callees: disclosed QC observations already recorded in 00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md §11 (F-QC-5/F-QC-6); no correction required.

Changed paths (5): 01_RAW/REPIN_ANCHOR_WINDOWS.txt, INPUT_IDENTITIES.json,
FINAL_REPORT.md, 01_RAW/SF20_WRITER_CENSUS.txt, QC_REPORT.md (this section).
00_CONTROL_INTERNAL_QC/ was read-only throughout; AUDIT_ENTRYPOINT.md NOT edited;
MANIFEST_SHA256.csv NOT regenerated (intentionally stale for the 5 changed paths — the
persistence phase regenerates the manifest LAST with full scope incl.
00_CONTROL_INTERNAL_QC and PE_MASTER_REVIEW.md); no commit, no push; BASE_SHA
24f45e0108b922c26ff584fee9ef7749de0390b6 unchanged.
