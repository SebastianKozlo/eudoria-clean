# P01 REPORT — Front A, priorities A1+A2/A2b

RUN_ID: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | PACKAGE: P01 | FRONT: A
Worker: pe-reconstruction | Started UTC: 2026-10-18T21:14:37Z | Regions: 0x006B1C60-0x006B1E00 (Adc52ad119303), 0x007D27B0-0x007D291E (Ab6ebb24f3a07)
Source: GHIDRA_H5_VTABLE2.txt, SHA256 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB (re-verified 2026-10-18T21:15:12Z)

## SCOPED RESULT (headline)

**Identity bridge: NOT FOUND in the admitted windows — and the missing link is now exactly identified.** Region 0x006B1C60-0x006B1E00 contains NO registration key, NO receiver-pointer store, NO [elem+8] store, and NO (type,id)-keyed lookup. What it actually contains: (a) a 4-row factory class-bootstrap stub 006B1C60 (`[ECX]=0xA85454` vtable install + `[0x00BA7220]=1` flag), and (b) a worklist type-directed scene walker 006B1C80 (partial in window). **Type66+ID A → 296445: NOT_ESTABLISHED — this region contains no keyed logic at all, so it neither supports nor refutes the join.** The exact remaining unknown: where the resource-ID→element→receiver binding is stored (see FIRST_MISSING_EDGE).

**A2 (006B1C80 write-set/alias):** explicit-store channel to outslot/V CLOSED at STRONGLY_SUPPORTED. The previously-open `[EDI]=EAX` store is now pinned: EDI is the insert cursor of a locally-constructed deque (`[ESP+0x2c]`), EAX is the single by-value stack argument; the store writes into the walker's own worklist storage. Residual opacity is honestly enumerated (container helpers 0043ba10/0043ca60; two virtual elem→vtable+8 calls receiving only ECX=elem; indirect free [0x00A759FC]) — all premise-level countermodels preserved.

**A2b (007D27B0):** identified as the NiStream teardown/destructor-class body (installs vptr 0x00A8EC24 — the same vptr the postaudit observed on the NiStream in 0082E750). It CANNOT write the outslot or V through any explicit store or argument (only ECX=this; all stores this-relative). **But it DOES free the [this+0x148] holder — the exact holder of the post-load V read (V=M32[M32[obj+0x148]]).** New premise refinement: the V-holder is dangling after this call; *out/Q survival depends on the retain (refcount), not holder liveness. Q-preservation arguments must drop any holder-liveness assumption.

## EVIDENCE MAP

| Claim | Statement (short) | Level | Resolution |
|---|---|---|---|
| P01-C1 | No identity bridge in region 1 window (full store census, 126 rows) | CONFIRMED | REJECTED_WITH_EVIDENCE (bridge absent in window) |
| P01-C2 | Region 1 = factory vtable/flag stub + type-directed deque walker | CONFIRMED (mechanics) | factual |
| P01-C3 | type66+ID A join unaddressed; no keyed logic in either window | CONFIRMED (absence) | NOT_ESTABLISHED (global) |
| P01-C4 | 006B1C80 explicit stores cannot reach outslot/V; [EDI] origin pinned | STRONGLY_SUPPORTED | REJECTED_WITH_EVIDENCE (explicit-store channel) |
| P01-C5 | 007D27B0 = NiStream teardown (vptr 0xA8EC24, member release/free-all, sub-vptr resets) | CONFIRMED | factual |
| P01-C6 | 007D27B0 cannot write outslot/V (explicit stores/arguments) | STRONGLY_SUPPORTED | REJECTED_WITH_EVIDENCE |
| P01-C7 | 007D27B0 frees +0x148 holder → lifetime premise refinement for Q | STRONGLY_SUPPORTED | CONDITIONAL refinement |
| P01-C8 | Body-entry map correction: 006B1D15/D49/DC6 are branch targets of 006B1C80 | CONFIRMED | factual correction |

Full statements, premises, countermodels: CLAIMS.json. Working dataflow/frame/CFG analysis: ANALYSIS_NOTES.md.

## PRESERVED DISTINCTIONS (contract compliance)

- V_first @006B201A / V_reload @006B206C / Q0 / Q1 / VT kept distinct; no equality assumed across opaque calls. This package adds no claim about their equality.
- No direct caller ≠ exclusively virtual (not used as evidence).
- vtable match ≠ runtime receiver identity: 0xA85454 install is class identity only; the walker's vtable+8 dispatch is type identity only.
- Explicit CFG store ≠ final memory value after opaque calls: both A2 and A2b conclusions are explicit-store-scoped with opaque residuals enumerated.
- Heap/stack disjointness treated as premise, not runtime fact (explicitly listed as the excluding premise for the [EDI]=EAX and this-relative-store countermodels).
- NiTArray +C8/+CC/+D4 premise independently cross-confirmed on branch elements in 006B1C80 ([EBX+0xCC] data, [EBX+0xD4] count, 4-byte stride).

## COUNTERS: actual vs reserved

- Bodies: **3 actual** (006B1C60 complete, 006B1C80 partial-window, 007D27B0 complete) vs 6 reserved. Contract's listed entries 006B1D15/006B1D49/006B1DC6 are branch targets inside 006B1C80, not functions (P01-C8).
- Instruction rows: **236 actual** (126 + 110, all read rows analyzed) vs 236 reserved.
- CALL sites: **19 actual** (region1: 0043ba10, 0043ca60, [0x00A759FC], virtual EDX, virtual EAX; region2: 6 virtual releases/destroys + 007d1d70 + 007d16b0 + 6× 0095db40 + 2× 0095dd6c) vs 19 reserved.
- Candidates: **4 actual** (CAND-R1a factory-flag registration; CAND-R1b type-node table; CAND-R1c typeinfo-walk join; CAND-R2a outslot/V hazard) vs 4 reserved.
- Front A total caps consumption: 3/16 bodies, 236/1800 rows, 19/64 CALL, 4/12 candidates.

## GATES

See GATES.json. RUN_STATUS: COMPLETED (all contract-required outputs materialized; wall cap respected; no new regions read; no forbidden access).

## HONEST LIMITS

1. All absence claims are scoped to the two admitted windows. The un-admitted tail of 006B1C80 (0x006B1E00 onward, exits 006b1f28/006b1f34, leaf path 006b1e2f) was NOT read — jump-target addresses were recorded from in-window instructions only.
2. P01-C7's bearing on V/Q uses the postaudit's +0x148 dataflow premise (same-class vptr match 0xA8EC24); it is not an independent re-derivation of that dataflow.
3. "Scene-graph walker" and "NiStream dtor" are semantics-level namings backed by explicit dataflow + cited premises, not RTTI name dumps; deque/dtor class naming is STRONGLY_SUPPORTED/PLAUSIBLE where marked in CLAIMS.json.
4. This package did not verify the retain ordering in 0082E750 (region not admitted); P01-B3 backlog item tracks it.
