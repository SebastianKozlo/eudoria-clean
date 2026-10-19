# P03 HANDOFF — pe-reconstruction → PE-MASTER

RUN_STATUS: **COMPLETED** (all contract-required outputs materialized before wall; no forbidden access; MANIFEST written last, self-excluded).

## Scoped result (A1 final / P02-B1)

- **0x007B6C30 = entry guard + in-function dispatch of ONE larger function.** The admitted 14 rows: thiscall (ECX=this), single by-value DWORD key stack arg, unconditional read of M[this+0x18] (register-decrement −1, no store back), null-key fast path returning EAX=0 via RET 0x4, and a conditional JNZ into the continuation for any non-null key.
- **Zero memory writes in-region** ⇒ the admitted rows CANNOT themselves write a binding (pure guard, key passed by value, NULL-on-null-key).
- **Lookup vs get-or-create/register: NOT_ESTABLISHED for the full function** — both candidates (CAND-P3a pure keyed lookup; CAND-P3b get-or-create/register) remain live; the decision lives entirely in the unadmitted continuation.
- **For the P02 leaf action specifically:** key 0x00A85460 is a non-null constant ⇒ the JNZ is ALWAYS taken at both callsites (006b1e36, 006b1e49) ⇒ both calls always enter the continuation; the in-region fast path is dead for them. If CAND-P3b holds, the leaf action writes the binding THROUGH this call — still open, now precisely localized.
- **Receivers [elem]/[elem+0x24]:** dereferenced at +0x18 unconditionally (valid-object requirement; consistent with P02 sentinel guards); read-only in-region; receiver class/layout identity UNKNOWN; no identity inference from the vtable-derived key (premise preserved).

## JUMP TARGET VA (for parent admission — NOT read)

- **JNZ @0x007b6c41 → 0x007B6C4B** — continuation of the SAME logical function (entry 0x007B6C30; single body; do not count a second body per §6). Live-in state: EBP=this, EDI=M[this+0x18]−1, EBX=0, key at [ESP+0x10], 3 callee-saved regs already pushed.

## Precise remaining edge (P03-B1, sharpens P02-B1)

Admit 0x007B6C4B+ (same source, SHA 642CC29A...C1D8DB) and decide by the continuation's MISS-path store census: insert/write (+ possible count update at [this+0x18]) ⇒ CAND-P3b register (leaf action writes binding); return NULL with no stores ⇒ CAND-P3a pure lookup. Also record: matched entry structure, any further jump/call targets (report, do not read), exit paths, return-value provenance. Continuation size unknown from the admitted window — reserve conservatively.

## Actual counters

1 body / 14 rows / 2 edges / **0 CALL sites** / 2 candidates (reserve was 1/14/2 edges/2; the dispatch prompt's "2 CALL" rendering of the edges reserve does not correspond to any CALL instruction — actual CALL contribution to Front A = 0; ledger reservation stands per §6 no-refund).
Front A after P03: **6/16 bodies, 386/1800 rows, 42/64 CALL, 8/12 candidates**. Campaign: 6/96, 386/12000, 42/320, 8/48.

## Disclosure for parent QC

Incidental navigation exposure: the region-locating Grep address search returned 3 boundary/continuation rows (0x007b6c4b, 0x007b6c4d, 0x007b6c4e) because the JNZ target sits at the end-exclusive boundary. Not analyzed, no claim depends on them; jump-target report derives from the in-region JNZ operand. Details: COUNTERS.json / REPORT.md Honest Limits §3.

## Paths

- FINAL_REPORT_PATH: D:\Eudoria_Reconstruction\99_Audits\PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018\packages\P03_EXEC_R1\REPORT.md
- PRIMARY_EVIDENCE_PATHS: EXTRACT_007B6C30_REGION.txt (SHA 40516D35FF4945149C1562C837ED74944A3A965F78AEAA6172A0D8CCCC637A3C, 1455 B); CLAIMS.json; MEMORY_AND_IDENTITY.json; COUNTERS.json; BARRIER_BACKLOG.json; SOURCE_PINS.json; CONTRACT.json (copy of CONTROL\CONTRACTS\P03.json, SHA BFF9E307...7D171); GATES.json; artifact_index.csv; RUN_STARTED.json
- Source pin re-verified: GHIDRA_H5_VTABLE2.txt SHA256 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB @ 2026-10-18T21:37:49Z (unchanged).

HARD_STOP_REASON: none (package completed within wall 2026-10-18T21:58:31Z).
