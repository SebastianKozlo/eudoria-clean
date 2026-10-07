# QC_REPORT_INTERNAL — INDEPENDENT INTERNAL QC — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006

**QC_VERDICT = QC_PASS_WITH_FINDINGS.**

- RUN_ID (of the audited package) = PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006
- QC_RUN_ID = PE_935_MODEL_CHILD_SF_JOIN_INTERNAL_QC_R1_20261006
- QC_SCOPE = INDEPENDENT_INTERNAL_QC_MODEL_CHILD_SF (LOAD_BEARING depth, fresh context)
- CLASSIFICATION: this is the PE-MASTER-dispatched fresh-context INTERNAL QC of the
  executor package. It is NOT an external Desktop post-audit, NOT PE-MASTER qualification
  and NOT milestone closure. The executor's own QC_REPORT.md + qc_reverify_results.json
  are a SELF_CHECK; this report is the INDEPENDENT internal QC layer over the same package.
- MODE: STATIC-ONLY, zero runtime. No executor evidence was modified anywhere; all QC
  writes are under 00_CONTROL_INTERNAL_QC/ only. No commit, no push (HEAD == BASE
  24f45e0108b922c26ff584fee9ef7749de0390b6 unchanged throughout).

## 1. Identity preflight (my own measurements)

| input | measured | expected | verdict |
|---|---|---|---|
| EXE D:\Eudoria_Reconstruction\pcg_install\Entropia.exe | 8,015,872 B / E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31 | same | MATCH |
| Contract OPENCODE_MODEL_CHILD_JOIN_REVIEWED.md | 15,348 B / F929D2C0…F3C8 | same | MATCH |
| HANDOFF_NOTES.md (anchor constraints) | 1,641 B / D531B56A…4355 | same | MATCH |
| repo HEAD | 24f45e0108b922c26ff584fee9ef7749de0390b6 | BASE | MATCH; zero tracked modifications; package untracked (persistence phase pending — consistent with GOVERNANCE_DECISION §2 phase split) |

## 2. Own byte re-pins (dispatch items a–g) — 61/61 checks PASS

All from my own tooling (own PE mapper; raw byte reads; OWN subset x86 decoder for
instruction boundaries — capstone NOT available in the QC environment, which makes the
decode layer independent of the executor's tooling; every load-bearing pin additionally
verified as raw-byte equality, which is decoder-independent):

- **(a) JOIN SITE @0x0050A3E9..0x0050A3F7 — CONFIRMED.** Bytes
  `8B 4E 30 / 8B 01 / 8B 90 A4 00 00 00 / 6A 00 / 57 / FF D2` = mov ECX,[ESI+0x30];
  mov EAX,[ECX]; mov EDX,[EAX+0xA4]; push 0; push EDI; call EDX. My boundary-true linear
  decode from entry 0x0050A310 confirms all six sites are real instruction boundaries.
  Receiver arithmetic verified: ECX loaded once at 0x0050A3E9 from [ESI+0x30] (mod=01
  rm=110 disp8=0x30 → [ESI+0x30], ESI=SF per mov ESI,ECX @0x0050A313); the only ECX use
  before the call is the vtable READ; no ECX write. Slot arithmetic: 0xA4/4 = slot 41;
  my data read [0x00A8CCF4+0xA4] = 0x007B5810 (slot 42 = 0x007B5A00; slots 17/19/45 =
  0x007B5390/0x007B47D0/0x007B4550 — all match the recorded canon dump).
- **(b) [SF+0x20] INSTALL @0x0050A3AC — CONFIRMED.** `89 7E 20` = mov [ESI+0x20],EDI at a
  true boundary, between mov ECX,EDI @0x0050A3AA and the getter call @0x0050A3AF; EDI =
  the manager argument loaded at 0x0050A38F (mov EDI,[ESP+0x14]).
- **(c) FUN_006C66D0 GETTER CALL @0x0050A3AF — CONFIRMED.** rel32 recompute:
  0x0050A3AF+5+0x001BC31C = 0x006C66D0; receiver ECX = EDI (the manager) set at
  0x0050A3AA; result → EAX → EDI @0x0050A3B7 (`8B F8`), the child value pushed at
  0x0050A3F6.
- **(d) FUN_0050A310 <- FUN_006A3930 @0x006A3A9D — CONFIRMED.** rel32 recompute =
  0x0050A310; args: mov ECX,[ESI+0x18] @0x006A3A99 (the [ACLD+0x18] SF; [ACLD+0x18]
  store `89 46 18` @0x006A39F6 re-pinned; FUN_005247C0 factory call @0x006A39ED recompute
  = 0x005247C0); push EBP (manager) @0x006A3A9C. Manager creation: push 0x130 @0x006A3A48;
  allocator call @0x006A3A4D → 0x0095D3C4; FUN_006C0D50 (ArkModelManagerMain ctor, prior
  bridge W02 canon) @0x006A3A77 recompute = 0x006C0D50. All 8 chain sites verified as
  true boundaries in my own full-function linear decode of FUN_006A3930.
- **(e) FUN_007B5810 FINGERPRINT — CONFIRMED as STRONGLY_SUPPORTED, NOT CONFIRMED.** My
  256-byte read at 0x007B5810 is byte-identical to 01_RAW/FUN_007B5810_ORACLE_BYTE_PROOF
  .txt (E1 check). Independently re-measured: F1 child NULL-guard (ESI=[ESP+0x20] arg1;
  test ESI,ESI; je early-return); F2 refcount inc [child+4] ×2 (`01 5E 04` @0x007B5846 and
  @0x007B5851); F3 AttachParent-shaped direct call @0x007B584C → 0x007BF470 (push EDI =
  parent; mov ECX,ESI = child receiver; body UNDECODED — honestly not claimed beyond
  shape); F4 children-array ops (bFirstAvail byte gate `80 7C 24 24 00`; lea ECX,[EDI+0xC8]
  @0x007B5864 → FUN_007B55E0; append branch: add EDI,0xC8; EBX=[EDI+0xC] (= NiNode+0xD4
  used) vs [EDI+8] (= NiNode+0xD0 alloc); grow FUN_00788570 @0x007B58A8; set-at-index
  FUN_007790D0 @0x007B58B5 — all rel32 recomputed and MATCH); F5 refcount dec ×2 with
  zero-destroy via child vtable slot 1 (`01 7E 04` decs + `8B 06 8B 50 04 8B CE FF D2`
  destroy). My own extent decode: 0x007B5810..0x007B58F2 (TERMINAL_RET_PADDING) = the
  ledger extent. Children-array offsets in the claims are tied to the PCG slot-17 canon
  (NiNode+0xC8/+0xCC/+0xD0/+0xD4), NOT to SDK/ABI transfer — verified in the oracle proof
  text (F4 prediction cites PE_935_NINODE_SLOT17_GAMEBRYO_ORACLE_MINICHECK_R1_20260914).
  **The fingerprint was NOT promoted to CONFIRMED anywhere** (CL-11 and CAND-4
  JOIN_OPERATION_STATUS both say STRONGLY_SUPPORTED with explicit NOT CONFIRMED and the
  era-exactness ceiling disclosed).
- **(f) TRANSFORM (SAME_INSTANCE_TRANSFORM_RELATION) — full pins CONFIRMED.** In
  FUN_00509850 (my full extent decode 0x00509850..0x005099BB = the ledger extent):
  flags window [SF+0x24..0x27] (@0x00509857..0x0050986E); transform gate cmp byte
  [EBP+0x28],1 / jne @0x0050989F/0x005098A3; offset-add gate [EBP+0x2C]>>4 bit0
  @0x005098B6; translate: EAX=[EBP+0x30]+0x5C with stores [EAX]/[EAX+4]/[EAX+8]
  @0x00509913/0x0050991F/0x0050992E; **the ×100 constant [0x00A7A618] = 100.0 (qword
  double, my own data read)** loaded by fld qword @0x005098F4; rotation: rep movsd of 9
  dwords from [EBP+0x4C] to [EBP+0x30]+0x38 @0x00509931..0x0050993C; scale: fld
  [EBP+0x70]; fabs; fstp [EDX+0x68] with EDX=[EBP+0x30] @0x0050993E..0x00509950. Callsite
  0x00529050 rel32 → 0x00509850 with receiver ECX=[ESI+0xC0] (SF) @0x00529047. The
  relation is correctly recorded as CONFIRMED_STATIC, path-conditional, CMO-ctor-path SF
  instance, SEPARATE from any join claim (CAND-2 REJECTED as transform≠child).
- **(g) FUN_008BD720 ACCESSOR + IMM — CONFIRMED.** `8D 41 18 C3` @0x008BD720 = lea
  EAX,[ECX+0x18]; ret (4-byte accessor; int3 padding after — my read) and
  `BB 20 D7 8B 00` @0x006C3FB0 = mov EBX,0x008BD720 (the bridge-E3 "callback" immediate;
  scheduler-entry call @0x006C3FCD rel32 → 0x006C3640 recompute MATCH).
- **Additional identity re-pins:** SF ctor FUN_00509330 stores the class vtable 0x00A7D458
  at [EBP+0x00] @0x00509366 (`C7 45 00 58 D4 A7 00`) — confirms CAND-4's "same class
  (vtable 0x00A7D458)" scope note; NiNode ctor FUN_007B6000 stores 0x00A8CCF4 at
  **0x007B6041** (my boundary-true decode from entry 0x007B6000 — the prior PA1 pin's VA
  is exact); [SF+0x30] store `89 45 30` @0x005093C3; NiNode ctor call @0x005093B8 →
  0x007B6000; refcount inc `83 40 04 01` @0x005093C8.
- **Raw-evidence integrity:** all 23 raw windows in 01_RAW re-read from the EXE and
  compared byte-for-byte with their BYTES records: ZERO mismatches.

## 3. Qualification gate (dispatch item 4) — PASS, incl. my own falsifiers

- The gate READS THE PROOF-CHAIN STRUCTURE (typed edges sf_creation → sf_store →
  parent_identity_access(field=+0x30) → parent_receiver → child_provenance(op,
  identity_preserved) → join_operation(mechanism, parent/child binding) → visual_role) and
  byte-verifies every non-synthetic edge's byte claim against the hash-pinned EXE
  (fail-closed EXE identity inside the script). It is NOT a four-typed-status rubber stamp.
- BASELINE = SYNTHETIC_GATE_TEST_ONLY fixture → PASS (gate can pass; not checker-always-FAIL);
  the fixture is explicitly marked synthetic/is_synthetic=True and is NOT recorded in any
  ledger or claim as PCG evidence — verified by full read of CANDIDATE_LEDGER/CLAIM_MATRIX.
- CTRL-A (parent→other-node): FAIL, primary P_PARENT_FAIL + a legitimate disclosed
  operation-parent consistency cascade; CTRL-B (child provenance removed): FAIL exactly by
  P_CHILD_FAIL; CTRL-C (identity edge +0x30→+0x34): FAIL exactly by P_PARENT_FAIL
  (parent_identity_access(+0x30) missing). None fail via manifest/Git — the gate never
  touches either.
- REAL CAND-4 chain: FAIL exactly on P_CHILD_FAIL + P_VISUAL_FAIL while ALL 5 real byte
  claims (r1 0x006A39ED `E8 CE 0D E8 FF`, r2 0x006A39F6 `89 46 18`, r3 0x0050A3E9
  `8B 4E 30`, r4 0x0050A3F7 `FF D2`, r6 0x007B5846 `01 5E 04`) match=True against the
  EXE — the gate does not rubber-stamp the real candidate. Consistent with
  INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED.
- **My own tests on the pinned gate** (gate_sha256 = EF2D8E1F…400AD = the manifest pin;
  copies with ONLY the OUT path and the declared mutation changed;
  gate_tests_summary.json OVERALL=PASS):
  - T1 GATE_REPLAY: results byte-identical to the package's qualification_results.json.
  - T2 BYTE_FALSIFIER (r3 expect mutated `8B 4E 30`→`8B 4E 31`): the REAL chain FAILs with
    `BYTE_MISMATCH[r3]` — the byte predicate is load-bearing, not decorative.
  - T3 ADD_A (a well-formed child_provenance QC-test edge added): the P_CHILD failure
    disappears while P_VISUAL remains — P_CHILD discriminates on structure.
  - T4 ADD_A_D (A + D QC-test edges added): the REAL chain PASSES with all 5 byte claims
    verified — the PASS barrier for the real chain was exactly A and D; no hidden
    predicate blocks it. (QC gate-logic probes only; the science statuses of A/D remain
    UNRESOLVED — no promotion.)

## 4. Budget census (dispatch item 5) — 8/8, 6/6, 4/4, 2/2, 1/1; NOT exceeded

- FUNCTION_BUDGET.csv: 8 rows = NEW_DETAIL_1_OF_8..8_OF_8 (FUN_008BD720, FUN_00528E50
  continuation, FUN_00509510, FUN_00509070, FUN_00509850, FUN_007BF500, FUN_0050A310,
  FUN_007B5810). MAX_NEW_DETAILED_FUNCTIONS = 8 → exhausted, not exceeded.
- EDGE_LEDGER.csv: 6 rows E1..E6 = NEW_EDGE_1_OF_6..6_OF_6. MAX = 6 → exhausted, not
  exceeded. Accounting interpretation verified as contract-compliant: an "interprocedural
  edge" is charged where the callee is ANALYZED (E1–E5 callees are the newly-decoded
  functions; E6's callee FUN_007B5810 = NEW #8). Callsite observations to undecoded
  callees inside an already-charged body (FUN_006C66D0, FUN_006C0EC0/ED0/FA0/FB0,
  FUN_0050A1E0, FUN_005246E0, FUN_007BF900/007BF630, FUN_00509670, FUN_006C3640) are
  recorded as open boundaries / NOT_CHECKED and are within the contract's allowance for
  local caller/callee/xref searches and byte censuses ("Census (byte-scan only, not
  detailed)" was pre-registered). The prior-pin re-reads (FUN_00509330, FUN_0064B1E0,
  FUN_007B6000, FUN_005094C0, FUN_00414130, FUN_006C3F50, FUN_006A3930 E8 census,
  FUN_006CB6F0 window) are within the declared prior-pin scopes — exempt per contract §3.
- CANDIDATE_LEDGER.csv: 4 candidates (CAND-1..CAND-4). MAX_JOIN_CANDIDATES_DETAILED = 4 →
  exhausted, not exceeded. WRAPPER_DEPTH traversed 2 of MAX_WRAPPER_LEVELS 2
  (FUN_006A3930 → FUN_0050A310 → slot-41 edge; the child's next wrapper FUN_006C66D0 NOT
  traversed — STOP honored at the boundary). ORACLE_MECHANISMS: 1 of 1
  (NiNode::AttachChild with its AttachParent step as ONE mechanism).
- **DA2 discipline: ZERO after-the-fact exceptions.** No function/edge/candidate carries
  an over-budget disclosure; the budget-stop events are recorded as honest open edges
  (FUN_006C66D0 undecoded = the primary open edge; HANDOFF NOT_CHECKED list).
- **Timing (mtime evidence):** PRE_REGISTERED_ANCHORS.md 22:55:44 was written BEFORE all
  detailed-decode raw files (earliest 22:55:57 = REPIN_ANCHOR_WINDOWS.txt; the eight NEW
  function decodes 22:56:28–23:07:36), which precede build_ledgers.py 23:09:38, ledgers
  23:09:42, gate 23:11:15/17, executor SELF-QC 23:11:56/58, QC_REPORT 23:12:15,
  FINAL_REPORT 23:12:51, EVIDENCE_INDEX 23:12:59, PE_MASTER_REVIEW (placeholder)
  23:13:04, HANDOFF 23:13:16, make_manifest.py 23:13:22, MANIFEST_SHA256.csv LAST
  23:14:05. Serial order matches the contract §7 pipeline.

## 5. CANDIDATE_LEDGER (dispatch item 6) — schema + algebra PASS

My independent parse (L1): header is EXACTLY the contract §5 field list (15 columns:
CANDIDATE_ID, JOIN_SITE_VA, PARENT_SOURCE, PARENT_STATUS, CHILD_SOURCE, CHILD_PROVENANCE,
CHILD_ROLE, JOIN_OPERATION, JOIN_OPERATION_STATUS, PATH_CONDITIONS, WRAPPER_DEPTH,
IDENTITY_BREAK_FOUND, STATUS, REJECTION_REASON, PHYSICAL_EVIDENCE); 4 rows; width stable;
zero null/missing cells; zero duplicate IDs; zero extra cells. Built by csv.DictWriter
with a fixed header (build_ledgers.py read in full) and the on-disk CSVs are byte-identical
to the generator's regenerated output (my ledger_regeneration_check.py). Claims matrix is
consistent with A–D: CL-13 A=UNRESOLVED, CL-12 B=CONFIRMED (scoped), CL-11
C=STRONGLY_SUPPORTED (NOT CONFIRMED), CL-14 D=UNRESOLVED → CL-15
INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED with the explicit no-averaging rationale.
CAND-4 STATUS = EXAMINED_UNRESOLVED with REJECTION_REASON = NONE (not rejected; unresolved
within bound) — honest. The CAND-4 PARENT_STATUS carries the SCOPE NOTE (ACLD-path
instance; DIFFERENT INSTANCE from the SF-island CMO+0xC0 holder; for the CMO instance no
join was found in the examined chain).

## 6. HANDOFF_NOTES binding constraints (dispatch item 7) — ALL honored

1. FUN_006CB020 is NOT used as a visual-child anchor (appears only as prior-canon
   description + CH3 with "visual-child relation of ANY of these = NOT_ESTABLISHED").
2. FUN_006CB3C0 has NO label-derived priority (CH3: "returns to the shortlist ONLY on a
   physical pointer/dataflow edge"); no such edge was found and it is in NO candidate.
3. No GetObjectByName-derived child claim (slot 17 appears only as prior canon for the
   position path and for the children-array layout).
4. The attach operation was identified via the VTABLE SLOT DISPATCH ([0x00A8CCF4+0xA4]
   → FUN_007B5810), not by name; the observed set-at-index/grow pattern is consistent
   with the "SetAt/wrapper implementations allowed" constraint; nothing rests on a named
   AttachChild import.
5. VFX separation honored: CHILD_ROLE = UNRESOLVED with the explicit "resource-derived
   child may be VFX — separate proof required" note (HANDOFF_NOTES item 4).
6. Transform ≠ join honored: CAND-2 REJECTED (TRANSFORM_APPLICATION_NOT_CHILD_BINDING);
   SAME_INSTANCE_TRANSFORM_RELATION kept as a separate status with NO join promotion
   (HANDOFF_NOTES item 5).

## 7. Oracle discipline (dispatch item 8) — PASS

Exactly ONE mechanism (NiNode::AttachChild + its AttachParent step). ORACLE_SOURCE paths
+ SHA256 recorded (NiNode.cpp 38C7A1DE…/33,897; NiAVObject.cpp 72E08371…/33,215) and — my
own re-hash — BOTH files match those identities on disk today. The identity comparison
against the earlier research's SOURCE_IDENTITIES.json is recorded in the oracle proof
(MATCH). NO blind ABI/offset transfer: the children-array offsets in every claim are tied
to the PCG-measured slot-17 canon (+0xC8/+0xCC/+0xD0/+0xD4); the fingerprint prediction is
described "in own words, no source reproduction"; no Gamebryo source text appears in the
package. The era-exactness ceiling is disclosed (STRONGLY_SUPPORTED, NOT CONFIRMED).

## 8. Scope (dispatch item 9) — PASS

- STATIC-ONLY: no client launch, no runtime instrumentation, no network. Every
  measurement in the package is a byte read/decode; the QC itself also ran zero runtime
  targets.
- No VFS/BNT/NIF payload opened (templates.vfs record 4508/A is cited from prior canon
  only; the resource-island data join is declared inherited prior canon, not re-run).
- No new records-correction, no web research (INPUT_IDENTITIES lists only local pinned
  inputs + BASE git-show reads).
- AUDIT_ENTRYPOINT.md untouched: zero mentions of this RUN_ID; git diff vs HEAD empty.
- Prior packages read-only: both §2 source packages unmodified vs HEAD; their
  FINAL_REPORT.md hash-match their own committed manifests (my spot-check). The other
  foreign untracked roots match the executor's 6-root inventory (byte-level untouchedness
  not verifiable without baselines — see NOT_CHECKED).
- git status clean outside the package: HEAD == BASE, zero tracked modifications, no
  staging, no commit, no push — the executor phase boundary (SCIENCE + SELF-QC + PACKAGE,
  persistence = PE-MASTER) was honored exactly as recorded in GOVERNANCE_DECISION §2.

## 9. Manifest (dispatch item 10) — PASS

MANIFEST_SHA256.csv: 31 data rows; my full independent re-hash of all 31 rows + sizes =
ZERO missing/extra/duplicate/size/SHA mismatch. Physical files = 32 (31 + the self-excluded
manifest itself) = the dispatch's census. The AUDIT_ENTRYPOINT.md exclusion is EXPLICITLY
recorded (make_manifest.py docstring, FINAL_REPORT §6, HANDOFF, EVIDENCE_INDEX) with the
persistence-phase regeneration obligation stated. MANIFEST generated LAST (mtime
evidence). NOTE: this QC's own records under 00_CONTROL_INTERNAL_QC/ are necessarily absent
from the current manifest — the persistence phase regenerates the manifest over the final
physical package (including this QC dir, per the POST_AUDIT_CORRECTION precedent) before
commit.

## 10. GOVERNANCE_DECISION verbatim instruction (dispatch item 2) — consistent

The verbatim block authorizes: ONE micro-run per the reviewed contract file; HANDOFF_NOTES
as binding anchor constraints; commit/push ONLY within the contract allowlist; keeping the
question/limits/evidence requirements; no client/extra experiment; return the commit SHA +
outcome + HARD STOP after final QC and publication. This matches the 2026-10-06
authorization as relayed in the QC dispatch (micro-run + HANDOFF_NOTES binding + commit/
push in allowlist). The executor correctly did NOT commit/push: the PE-MASTER dispatch
phase assignment ("NIE commituj, NIE pushuj — persistence = PE-MASTER po własnym audycie i
fresh internal QC") is preserved verbatim in §2 and classified ORCHESTRATOR_PHASE_SPLIT
(recorded from the dispatch text as received, not reconstructed) — consistent with the
observed repo state (package untracked, HEAD == BASE, entrypoint untouched) and with the
DPA3 methodology precedent. PE_MASTER_REVIEW.md is an honest PLACEHOLDER (explicitly NOT
review content; to be replaced by PE-MASTER in the persistence phase) — no fabricated
verdict anywhere in the package.

## 11. FINDINGS (bold titles; none falsifies a load-bearing claim)

**F-QC-1 (P2) — REPIN_ANCHOR_WINDOWS.txt window CH2a is mislabeled: the caption claims
"FUN_008BD720 first bytes (PIN existence check…)" but the window is VA 0x0064B1EC LEN 16
whose bytes (`89 46 10 C7 06 74 32 A8 00 8B C6 5E C2 04 00 CC`) are the FUN_0064B1E0 body
tail (a duplicate of the PA2b window), NOT the bytes at 0x008BD720.**
- Exact source: 01_RAW/REPIN_ANCHOR_WINDOWS.txt, section header "### CH2a: FUN_008BD720
  first bytes (PIN existence check; body decode charged separately)", "VA 0x0064b1ec LEN
  16" (file lines 280–288).
- Contradicted claim: the CH2a record's own caption; NOT any CLAIM_MATRIX row (CL-05
  rests on CH1a/CH1b — the 0x006C3FB0 immediate pin, which is correct — and CL-06 rests on
  01_RAW/FUN_008BD720_DECODE.txt, which is correct: my read at 0x008BD720 = `8D 41 18 C3`).
- Skutek: an orphaned defective raw window; a reader could mistake the PA2b duplicate for
  an FUN_008BD720 pin. No downstream claim cites CH2a.
- Correction (persistence-phase choice; evidence NOT edited in place by QC): PE-MASTER may
  disclose this defect in the entrypoint row / a follow-up note, or order a records
  correction run. The raw file stays as-is (evidence immutability).
- Revalidation predicate: a re-pinned window at VA 0x008BD720 would show `8D 41 18 C3 CC …`
  (my G1/G2 checks already provide the independent pin).

**F-QC-2 (P2) — INPUT_IDENTITIES.json records oracle_sources[].measured_at_use = null,
contradicting INPUT_IDENTITIES.md §5 ("Identities re-measured at use time and compared
against the earlier research's SOURCE_IDENTITIES.json") and the oracle byte proof
("measured size 33897 / SHA256 38C7A1DE… == earlier-research expectation MATCH").**
- Exact source: INPUT_IDENTITIES.json, `"oracle_sources": [ { … "measured_at_use": null …
  } ]` (lines 66–81 of the JSON).
- Skutek: a machine-readable field suggests the oracle identities were NOT re-measured at
  use, while the .md and the raw proof say they were. Substance: TRUE — my own independent
  re-hash today confirms both files match the expected identities (NiNode.cpp
  38C7A1DE…/33,897; NiAVObject.cpp 72E08371…/33,215). SOURCE_FILE_UNCHANGED = YES;
  MANIFEST/JSON-IDENTITY_CORRECT = for this field NO (L10 split).
- Correction: fill measured_at_use (e.g., "2026-10-06T23:0x-07:00 MATCH") in a
  records-correction, or disclose; no evidence re-measurement needed (already verified).
- Revalidation predicate: re-hash of both Gb12 files equals the recorded SHA256/size (my
  J1 check = PASS).

**F-QC-3 (P2) — FINAL_REPORT §2 says "FUN_0050A310 was fully decoded (NEW #7)", but the
raw decode window covers only 0x0050A310..0x0050A42F (LEN 288) while the function's true
extent is 0x0050A310..0x0050A45C (my own entry-aligned linear decode: terminal
`C2 04 00` ret 0x4 @0x0050A459 + int3 padding to 0x0050A45C).**
- Exact source: FINAL_REPORT.md line 99 ("FUN_0050A310 was fully decoded (NEW #7)") vs
  FUNCTION_BUDGET.csv row FUN_0050A310 VA_RANGE "0x0050A310..0x0050A453+" (honest "+"
  continuation notation) vs 01_RAW/FUN_0050A310_DECODE.txt WINDOW LEN 288.
- Contradicted claim: only the "fully decoded" wording. The undecoded tail
  (0x0050A42B..0x0050A45C) contains: mov byte [ESI+0x91],1; mov byte [ESI+0x28],1; jne
  0x0050A44A; mov ECX,ESI; call 0x005095C0; mov byte [ESI+0x24],1; mov byte [ESI+0x91],1;
  return-true epilogue (mov AL,1; ret 4) and return-false epilogue (xor AL,AL; ret 4) —
  NO join-bearing content; every load-bearing claim (join site, [SF+0x20] install, getter
  calls, detach path, path conditions to the join) lies inside the decoded window and was
  independently re-verified by me.
- Skutek: report/budget wording drift; a reader could believe the whole 332-byte function
  was decoded when the charge covered a 288-byte window with an honestly-marked open tail.
- Correction: persistence-phase wording note (or correction run); the budget's "+" notation
  and the raw file remain authoritative and honest.
- Revalidation predicate: boundary decode from 0x0050A310 ends at ret 0x4 @0x0050A459
  (my H7 check = PASS, with the tail bytes recorded in
  qc_independent_repins_results.json detail.fun_50a310_undecoded_tail_bytes).

**F-QC-4 (P3) — SF20_WRITER_CENSUS.txt vtable dump header says "47 slots" but lists 48
rows; slot 47 = 0x65666665 = ASCII past-the-end data (my u32 read confirms), i.e., the
display overran the NiNode vtable by one row.** Slot 41 (the load-bearing one) is
unaffected; EVIDENCE_INDEX.md propagates the same "FULL NiNode vtable dump (47 slots)"
wording. No claim affected (slot 47 is not cited anywhere). Display artifact disclosed by
its own content.

**F-QC-5 (P3) — three raw windows begin mid-instruction (PA1b: start VA 0x007B6038; CH3a:
start VA 0x006CB7C0; the FUN_006A3930 window around 0x006A3A9D: start VA 0x006A3A7D), so
their capstone decode columns start with garbage until re-sync.** The raw BYTES are
correct (all 23 windows byte-verified vs the EXE), and the boundary-sensitive claims were
independently re-derived by my own entry-aligned decodes (e.g., the 0x007B6041 vtable
store). Disclosed-by-content display artifacts; no correction required.

**F-QC-6 (P3) — the child-argument (EDI) identity preservation from 0x0050A3B7 (mov
EDI,EAX after FUN_006C66D0) to the push at 0x0050A3F6 crosses four undecoded intermediate
callees (FUN_006C0F90, FUN_006C10B0, FUN_0050A1E0, FUN_005246E0).** Within the decoded
caller body there is indeed no EDI write (verified), and preservation across the callees
holds under the standard MSVC 32-bit callee-saved-register convention (exemplified by
FUN_007B5810's own push/pop of EDI), but it is convention-backed rather than byte-proven
across those bodies. Since CHILD_PROVENANCE is UNRESOLVED anyway and nothing is promoted on
the EDI chain, this is an observation, not a correction demand. The PARENT (ECX) chain, in
contrast, contains NO calls between the [SF+0x30] load and the virtual dispatch and is
fully byte-proven.

**No P0/P1 findings.** Every load-bearing claim re-measured by this QC MATCHES its
physical evidence: the join-site receiver = the exact examined ACLD-path SF+0x30 NiNode
(byte-proven, no clobber); the operation = the slot-41 AttachChild counterpart
(STRONGLY_SUPPORTED, honestly capped); the child's provenance/role honestly UNRESOLVED at
the budget boundary; INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED with correct status
algebra (no averaging); the SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC with
complete pins and correct separation from any join claim; RUNTIME_JOIN_OBSERVED = NO;
governance statuses unchanged.

## 12. Coverage algebra (L11)

Package files = 32 = 31 manifest rows + 1 self-excluded manifest. My QC read = 32/32
FULL_READ (100%) + 31/31 manifest rows re-hashed + 23/23 raw windows byte-verified + 61
independent measurement checks + 4 gate tests + 1 ledger regeneration diff + 2 prior
package spot-checks. NOT_CHECKED items are enumerated in FULL_READ_LOG.md §NOT_CHECKED;
none of them gates a load-bearing claim of this package (the load-bearing pins were all
re-measured).

## 13. QC verdict and handoff

QC_VERDICT = **QC_PASS_WITH_FINDINGS** (F-QC-1/2/3 = P2 record/wording defects; F-QC-4/5/6
= P3 observations; zero load-bearing falsifications; 61/61 own checks PASS; gate + falsifier
suite PASS; budgets 8/8, 6/6, 4/4, 2/2, 1/1 exhausted-not-exceeded with zero after-the-fact
exceptions; manifest bijection zero-mismatch over the 31 pre-QC rows). This verdict is
INTERNAL QC only — not MASTER_ACCEPTED, not external Desktop post-audit, not PE-MASTER
qualification, not milestone closure. The three P2 findings need no science repair; they
are disclosed here for PE-MASTER's persistence decision (entrypoint row wording and/or a
records-correction run). My QC wrote ONLY under 00_CONTROL_INTERNAL_QC/ (14 files incl.
this report); executor evidence untouched; HEAD == BASE throughout; the persistence phase
must regenerate the manifest (the current one intentionally covers the 31 pre-QC package
files) and replace the PE_MASTER_REVIEW.md placeholder with the real PE-MASTER review.
