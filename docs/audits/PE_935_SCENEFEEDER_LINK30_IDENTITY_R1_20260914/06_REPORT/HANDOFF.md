# HANDOFF.md — PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914 (delivery notice)

FINAL_HANDOFF_SCHEMA (per contract):

- RUN_ID: PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914
- BASE_SHA: 1a490eed4ca2b295e78cd3cf851a08ac9c93930b
- OBSERVED_HEAD_SHA: 1a490eed4ca2b295e78cd3cf851a08ac9c93930b
  (== BASE; the executor made ZERO git mutations — no add/commit/push/stage;
  publication is the separate later step by pe-master-auditor)
- WRITER_COUNT: 3643 (total census candidates — the raw denominator over full .text,
  2,266,698 swept instructions; every candidate has a classified CSV row)
- PROVEN_WRITER_COUNT: 2
  - 0x005093C3 (SF ctor FUN_00509330): [SF+0x30] = newly allocated operator-new(0x118)
    block initialized by FUN_007B6000, refcount++ at block+4
  - 0x0050A2D1 (SF dtor body FUN_0050A240): [SF+0x30] = 0 after the refcount release
    protocol
  (residue: 3023 REJECTED_ALIAS with per-row reasons; 618 POSSIBLE_ALIAS = the
  documented static bound; 0 UNRESOLVED)
- SF30_SOURCE_PROVENANCE: RESOLVED for both writers (creation/receipt-level chains
  with VA+byte hop tables in 02_ANALYSIS/SF30_PROVENANCE.md; P1 allocation->ctor->
  stored->refcount++; P2 constant zero after release protocol; nothing followed past
  receipt)
- SF30_TYPE_IDENTITY: RTTI-IDENTIFIED (calibrated walker, byte-confirmed walk)
- RTTI_NAME: `.?AVNiNode@@` (verbatim, mangled MSVC RTTI name; vtable 0x00A8CCF4,
  COL 0x00AAEEC8, TD 0x00B936C8; supporting embedded member vtable 0x00A8CCE0 =
  `?$NiTPointerList@PAVNiDynamicEffect@@@@` at block+0xE0)
- FINAL_STATUS: A — IDENTIFIED
- NEXT_SEAM: SLOT17 (the NiNode vtable slot-17 dword at [0x00A8CCF4+0x44] =
  0x007B5390 — recorded VALUE only, NOT decoded, per contract; candidate for the
  next run under that run's own scope guards)
- REPORT_PATH: docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/06_REPORT/REPORT.md
- HANDOFF_PATH: docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/06_REPORT/HANDOFF.md
- MANIFEST_PATH: docs/audits/PE_935_SCENEFEEDER_LINK30_IDENTITY_R1_20260914/06_REPORT/MANIFEST_SHA256.csv
- RUN_STATUS: COMPLETE
- HARD_STOP_REASON: NONE
- NOT_CHECKED (short): NiNode vtable slot 17 decode (next seam); 0x437F70/0x82B5A0
  analyses; the other 46 NiNode slots; block-ctor callees (0x7C02D0/0x788480/0x7DE000);
  individual resolution of the 618 POSSIBLE_ALIAS rows; SF+0x30 value's later
  behavior (TRANSFORM_TO_MODEL remains NOT_DEMONSTRATED); slot callers/consumers;
  296445/4508/terrain/NIF/network/runtime work.

Gates: G0–G5 all PASS (06_REPORT/STAGE_ACCEPTANCE_GATES.csv, recomputed by
00_CONTROL/finalize.py from the artifacts; COUNTER_ARITHMETIC holds: raw file ==
CSV == state json == 3643 with counts 2/618/3023/0).

Era label: PCG_9_3_5. STATIC-ONLY: the client never ran; no game binary process was
launched; every claim is from physical-byte reading scripts (own PE walk + capstone
5.0.7).
