# HANDOFF_QC — terminal block — INDEPENDENT INTERNAL QC — PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006

```text
ASSIGNMENT_MODE = INTERNAL_QC (independent, fresh context; NO_NESTED_TASKS; STATIC-ONLY, zero runtime)
QC_RUN_ID = PE_935_MODEL_CHILD_SF_JOIN_INTERNAL_QC_R1_20261006
PARENT_LOOP_ID = PE-MASTER dispatch of 2026-10-06 (post-24f45e0 work queue)
MILESTONE = EU935 / PE 9.3.5 bounded static RE track (no Q1/Gate-B/M1/M2 change; CANONICAL_GATE_EFFECT=NONE)
SCOPE = INDEPENDENT_INTERNAL_QC_MODEL_CHILD_SF — verification of the executor package
        PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006 (32 files, FULL_READ)
QC_VERDICT = QC_PASS_WITH_FINDINGS
FINDINGS =
  F-QC-1 (P2): 01_RAW/REPIN_ANCHOR_WINDOWS.txt CH2a window mislabeled — caption says
      "FUN_008BD720 first bytes" but VA/bytes are 0x0064B1EC = FUN_0064B1E0 tail (PA2b
      duplicate); no claim rests on CH2a (CL-05 rests on CH1b; CL-06 on
      FUN_008BD720_DECODE.txt — both independently verified correct).
  F-QC-2 (P2): INPUT_IDENTITIES.json oracle_sources[].measured_at_use = null contradicts
      INPUT_IDENTITIES.md §5 and the oracle proof ("re-measured MATCH"); substance TRUE —
      my re-hash of NiNode.cpp (38C7A1DE…/33,897) and NiAVObject.cpp (72E08371…/33,215)
      both MATCH; JSON bookkeeping field inconsistent.
  F-QC-3 (P2): FINAL_REPORT §2 "FUN_0050A310 was fully decoded" — window covers only
      0x0050A310..0x0050A42F (LEN 288); true extent 0x0050A310..0x0050A45C (my decode:
      ret 0x4 @0x0050A459 + padding); the tail is flag-re-arm + call 0x005095C0 +
      epilogues — NO join-bearing content; budget honestly says "0x0050A453+".
  F-QC-4 (P3): SF20_WRITER_CENSUS vtable dump header "47 slots" vs 48 rows listed
      (slot 47 = 0x65666665 = past-end ASCII); slot 41 unaffected.
  F-QC-5 (P3): three raw windows start mid-instruction (PA1b/CH3a/one 006A3930 window) —
      decode columns begin with garbage until re-sync; raw BYTES all byte-verified vs EXE.
  F-QC-6 (P3): child-arg (EDI) preservation 0x0050A3B7→0x0050A3F6 crosses 4 undecoded
      callees — holds by the MSVC callee-saved ABI convention, not byte-proven across them
      (parent ECX chain has NO calls and is fully byte-proven); CHILD_PROVENANCE is
      UNRESOLVED anyway — observation only.
  ZERO P0/P1. No load-bearing claim falsified. No evidence repaired in place (contract §5);
  findings recorded for the PE-MASTER persistence decision.
OWN COUNTERS vs DECLARED:
  own checks 61/61 PASS (EXE id, a–g re-pins, boundary decodes, vtable data, x100=100.0,
  SF/NiNode vtable stores @0x00509366/0x007B6041, 23/23 raw windows byte-identical,
  31/31 manifest rows re-hash zero-mismatch, 32-file census, ledger schema+regeneration
  byte-identical, status algebra, oracle+contract+research hashes) — ALL MATCH the
  executor's declarations.
BYTE RE-PINS a–g (own engine):
  (a) join site 0x0050A3E9..0x0050A3F7 = 8B 4E 30 / 8B 01 / 8B 90 A4 00 00 00 / 6A 00 / 57 /
      FF D2; receiver [ESI+0x30] (ESI=SF), slot 41 = [0x00A8CCF4+0xA4] = 0x007B5810 — CONFIRMED
  (b) [SF+0x20] install 89 7E 20 @0x0050A3AC — CONFIRMED (true boundary; EDI=manager arg)
  (c) FUN_006C66D0 call @0x0050A3AF rel32→0x006C66D0; ECX=EDI; result→EDI @0x0050A3B7 — CONFIRMED
  (d) FUN_0050A310 <- FUN_006A3930 @0x006A3A9D (ECX=[ACLD+0x18] SF, push EBP manager);
      new 0x130 @0x006A3A48 → 0x0095D3C4; FUN_006C0D50 @0x006A3A77; [ACLD+0x18]=89 46 18
      @0x006A39F6 — CONFIRMED (all 8 sites true boundaries in own full-function decode)
  (e) FUN_007B5810: F1 guard/F2 inc ×2/F3 call→0x007BF470 (body undecoded)/F4 +0xC8
      children ops (FUN_007B55E0 / FUN_00788570 / FUN_007790D0)/F5 dec ×2 + slot-1
      zero-destroy; extent 0x007B5810..0x007B58F2; bytes byte-identical to the oracle
      proof file — CONFIRMED as STRONGLY_SUPPORTED (NOT promoted to CONFIRMED anywhere)
  (f) FUN_00509850: gates [SF+0x24..0x27]/[SF+0x28]==1/[SF+0x2C]>>4 bit0; translate ×100
      ([0x00A7A618]=100.0q) → NiNode+0x5C/+0x60/+0x64; rotation 9 dwords SF+0x4C→+0x38;
      scale |SF+0x70|→+0x68; callsite 0x00529050 (ECX=[CMO+0xC0]) — CONFIRMED
      (SAME_INSTANCE_TRANSFORM_RELATION has complete pins; separate from any join claim)
  (g) 8D 41 18 C3 @0x008BD720 (4-byte accessor) + BB 20 D7 8B 00 @0x006C3FB0 — CONFIRMED
BUDGET CENSUS = functions 8/8, edges 6/6, candidates 4/4, wrapper 2/2, oracle 1/1 —
  exhausted, NOT exceeded; zero after-the-fact exceptions (DA2 clean); PRE_REGISTERED_
  ANCHORS (22:55:44) written BEFORE all detailed decodes (earliest 22:55:57); MANIFEST LAST
GATE = structure-reading (proof-chain + EXE byte verification); baseline PASS; CTRL-A/B/C
  proper predicates; REAL CAND-4 FAIL exactly on P_CHILD+P_VISUAL with 5/5 byte MATCH; my
  falsifiers: byte-mutation → BYTE_MISMATCH[r3] fires; +A → P_CHILD disappears;
  +A+D → real chain PASSES (barrier was exactly A/D); replay byte-identical
SCIENCE (re-verified independently) = PARENT_FOUND_CHILD_UNRESOLVED;
  INSTANCE_MODEL_NODE_JOIN = NOT_ESTABLISHED (A=UNRESOLVED, B=CONFIRMED scoped to the
  ACLD-path instance, C=STRONGLY_SUPPORTED, D=UNRESOLVED; no averaging);
  RUNTIME_JOIN_OBSERVED = NO; SAME_INSTANCE_TRANSFORM_RELATION = CONFIRMED_STATIC
  (separate status, no join promotion); best candidate = CAND-4 @0x0050A3F7
FULL_READ_LOG_PATH = docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/00_CONTROL_INTERNAL_QC/FULL_READ_LOG.md
NOT_CHECKED = enumerated in FULL_READ_LOG.md (private-research report CONTENTS; prior-package
  file contents beyond the 2 spot-checks; foreign-untracked byte-level untouchedness — no
  baselines exist; the executor scratch dir; all undecoded callees (FUN_006C66D0,
  FUN_007BF470, FUN_0050A1E0, FUN_005246E0, FUN_00509670, FUN_005095C0, FUN_007B5A00,
  FUN_006C0EC0/ED0/FA0/FB0/F90/10B0, FUN_006C3640, FUN_007B55E0/788570/7790D0,
  FUN_006C8B20/BB0, FUN_006C0D50, FUN_0072FCE0, FUN_0048BAC0, FUN_0096CDD0,
  FUN_007BF900/7BF630, resource completion chain, FUN_007B68B0 storage); runtime anything)
FINAL_REPORT_PATH (QC) = docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/00_CONTROL_INTERNAL_QC/QC_REPORT_INTERNAL.md
GATES_PATH = docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/00_CONTROL_INTERNAL_QC/gate_tests_summary.json
            (package gates: 03_SCRIPTS/qualification_results.json — replayed identical)
MANIFEST_PATH = docs/audits/PE_935_MODEL_CHILD_SCENEFEEDER_NINODE_JOIN_R1_20261006/MANIFEST_SHA256.csv (31 rows, zero mismatch, pre-QC scope)
INPUT_AND_OUTPUT_HASHES = EXE E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31/8,015,872 B;
  contract F929D2C0…F3C8/15,348; HANDOFF_NOTES D531B56A…4355/1,641; oracle NiNode.cpp
  38C7A1DE…/33,897 + NiAVObject.cpp 72E08371…/33,215; 3 private reports 26CBF3AB…/17,914,
  D6B81792…/13,385, 598DA71A…/15,300 — ALL MATCH; gate under test EF2D8E1F…400AD (=
  manifest pin); full per-file SHA table = MANIFEST_SHA256.csv (my re-hash zero mismatch)
FILES_CHANGED (this QC) = ONLY 00_CONTROL_INTERNAL_QC/** (15 files: FULL_READ_LOG.md,
  QC_REPORT_INTERNAL.md, HANDOFF_QC.md, qc_independent_repins.py + _results.json,
  gate_falsifier_runner.py, gate_replay.py, gate_falsifier_byte.py, gate_add_A.py,
  gate_add_AD.py, results_gate_replay.json, results_gate_falsifier_byte.json,
  results_gate_add_A.json, results_gate_add_AD.json, gate_tests_summary.json,
  ledger_regeneration_check.py + .json) — executor evidence untouched; AUDIT_ENTRYPOINT
  untouched; no commit, no push, no staging by this QC
BASE_SHA = 24f45e0108b922c26ff584fee9ef7749de0390b6
HEAD_SHA = 24f45e0108b922c26ff584fee9ef7749de0390b6 (== BASE; package + QC records untracked)
PUSH_STATUS = NONE (QC does not publish; persistence belongs to PE-MASTER)
UNRELATED_WORK_EXCLUDED = 6 foreign untracked roots (5x PE_935_* packages + experiments/)
  inventoried, untouched by this QC; the 2 "NOT in BASE" foreign packages were correctly
  NOT used as evidence by the executor
NEXT_PARENT_ACTION = PE-MASTER decision: (1) accept this internal QC (QC_PASS_WITH_FINDINGS,
  no science repair needed); (2) adjudicate the 3x P2 + 3x P3 findings — minimal path =
  disclose F-QC-1/2/3 in the entrypoint row / persistence wording, no evidence re-edit;
  alternative = a small records-correction run for F-QC-1/2 (CH2a caption, JSON
  measured_at_use) + F-QC-3 wording; (3) write the real PE_MASTER_REVIEW.md (the current
  one is the honest placeholder), (4) regenerate the manifest LAST over the final package
  (including 00_CONTROL_INTERNAL_QC/), full bijection, then the authorized path-limited
  commit/push + entrypoint row. NEXT_EXPERIMENT_AUTHORIZED = NO (this QC adds no new RE).
HARD_STOP = YES (QC complete; return to PE-MASTER)
```
