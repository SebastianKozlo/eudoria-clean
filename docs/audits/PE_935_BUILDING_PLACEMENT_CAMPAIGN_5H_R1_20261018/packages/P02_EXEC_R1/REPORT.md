# P02 REPORT — Front A1 continuation: 006B1C80 walker tail (P01 FIRST_MISSING_EDGE priority 1)

RUN_ID: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | PACKAGE: P02 | FRONT: A
Worker: pe-reconstruction | Started UTC: 2026-10-18T21:31:17Z (RUN_STARTED.json) | Region: 0x006B1E00-0x006B1FAC (Admission A0f2d2522b464)
Source: GHIDRA_H5_VTABLE2.txt, SHA256 642CC29A01B8AD6F783E82E14DA4A61FA00BA6A3EC6DF98EDFF28AC25CC1D8DB (verified 21:31:09Z and re-verified 21:34:47Z, 50,780,146 B, unchanged)
Context cited (not re-analyzed): P01 REPORT.md, P01 QC_REPORT.md.

## SCOPED RESULT (headline)

**NO resource-ID/element/receiver binding in the walker tail — pure processing plus ONE constant class-keyed element SELECTION; the exact missing link is now fully localized to 007b6c30.** The 136-row region (bodies/blocks 0x006B1E0B, 0x006B1E2F) completes the 006B1C80 walker (epilogue `RET 0x4` @006b1fa7). Full store census: **7 explicit stores** (1 worklist deque insert, 4 frame stores, 1 SEH restore, 1 result-flag clear) — **no [elem+8] store** (the only +8 access is the list-head LOAD @006b1ec8), **no receiver-pointer store, no registration-key store, no global store, no resource-ID value** (no 0x42/66, no 296445 anywhere in the region).

The leaf action (0x006B1E2F) does contain **type-keyed logic of exactly one shape**: `PUSH 0x00A85460; MOV ECX,EBX; CALL 0x007b6c30` — a lookup with a **compile-time-constant key** (0x00A85460 = 0x00A85454+0xC, i.e. statically inside/adjacent to the P01-confirmed factory-class vtable), performed first on the leaf element, then on its **[+0x24] member** as fallback, both sentinel-guarded (bail JZ 006b1fb4, out-of-region). This is an element SELECTION by class key — **not a resource-ID**: no variable ID flows in the region, so the region **neither contains nor can refute the join to actualS or 296445** (MODEL_INSTANCE_BINDING remains NOT_ESTABLISHED, same shape as P01-C3, now covering the walker's ENTIRE body).

**Exact missing link:** (a) the lookup/registration semantics of **007b6c30** — what key 0x00A85460 matches and which code REGISTERED an element under that key into the leaf elem / [leaf+0x24] containers (if 007b6c30 is get-or-create/register rather than lookup, the leaf action itself WRITES the binding through the callee — in-region facts cannot distinguish); (b) the origin/identity of the 007b4170 receiver slot **M[steady+0x18]** (candidate channels: 0043ca60 byref @006B1E0B, or P01-window init — un-itemized in cited P01 outputs). See BARRIER_BACKLOG P02-B1/P02-B2.

## EVIDENCE MAP

| Claim | Statement (short) | Level | Resolution |
|---|---|---|---|
| P02-C1 | Store census: 7 explicit stores, no [elem+8]/receiver/registration/ID store (all 136 rows) | CONFIRMED | REJECTED_WITH_EVIDENCE (binding store absent in region) |
| P02-C2 | Leaf-path + exit mechanics incl. stack-balance derivation of slot identities | CONFIRMED (mechanics) | factual |
| P02-C3 | MAIN: no binding; processing + constant class-keyed selection; join NOT_ESTABLISHED; missing link = 007b6c30 + steady[0x18] | CONFIRMED (absence in region, scoped) | NOT_ESTABLISHED (global join) |
| P02-C4 | Key 0xA85460 = 0xA85454+0xC (arithmetic; factory vtable cited P01) | CONFIRMED (arithmetic) / PLAUSIBLE (interpretation) | CONDITIONAL |
| P02-C5 | RET 0x4 returns AL=steady[0x17]; only failure write in-region; 0x80-chunk array fully freed in-epilogue | CONFIRMED (in-region) / PLAUSIBLE (out-of-region continuation) | factual + CONDITIONAL |
| P02-C6a | CAND-P2a: 007b6c30 = keyed dictionary lookup (CANDIDATE) | STRONGLY_SUPPORTED (call shape) / PLAUSIBLE (semantics) | CONDITIONAL |
| P02-C6b | CAND-P2b: 007b4170 = conditional element hand-off to frame receiver M[steady+0x18] (CANDIDATE) | PLAUSIBLE | CONDITIONAL |

Full statements, premises, countermodels: CLAIMS.json. Register-role identity map and frame slot map: MEMORY_AND_IDENTITY.json.

## STRUCTURE OF THE TAIL (mechanics, CONFIRMED)

1. **006b1e00-006b1e2a (child-push loop tail):** `[EDI]=EAX` worklist insert continues P01's deque pinning (P01-C4); insert cursor spill `[ESP+0x2c]=EDI`; loop head `EAX=[EBX+0xD4]` (NiTArray count, premise-consistent), `ESI+=1`, `CMP/JA 006b1dda` back into P01's window (next child), else `JMP 006b1f28` (drain check). Block **006B1E0B** is the deque grow/insert-support block: `0043ca60(this=&steady[0x1c] container, arg=&steady[0x18])` — **callee receives a BYREF to the frame slot later used as 007b4170 receiver** — then reloads the cursor.
2. **006b1e2f-006b1ea7 (leaf keyed selection + derive chain):** two-receiver constant-key lookup (007b6c30, key 0x00A85460, sentinel EBP, bail 006b1fb4); derive chain 008bd720 → 004152f0 → 006ae840 → **EBP_L1**; null → failure flag. Bool gate 006eb320(EBP_L1); if false, upgrade chain 006c64d0 → **[result+0x4]** (P01 parent-chain pattern) → 004152f0 → 006aded0 → **[result]** → 004152f0 → 006ae310 → **EBP_L2**; null → failure flag. EBP_L1/EBP_L2 kept distinct.
3. **006b1eb1-006b1f22 (node-list walk):** retain-shaped 004152f0(EBP,EBX) → 006b0680; `007558a0(lookup result)` → list holder; walk from `[holder+0x8]` to holder-sentinel: per node, `[0x00A75A00](&steady[0x44], node+0x28)` local-container insert, `006f2940(EBP, node+0x10, &steady[0x40])`; **if result nonzero → `007b4170(ECX=M[steady+0x18], arg=result)`** — the only outbound element hand-off; then `[0x00A75A5C](&steady[0x44])` cleanup, `[0x00A75854](node)` → next.
4. **006b1f28-006b1fa7 (exit):** drain-check loop back 006b1d33; cleanup frees every non-null 0x80-byte chunk and the chunk-pointer array via `[0x00A759FC]`; SEH restore, cookie check 0095d3ca, `ADD ESP,0x58`, **`RET 0x4`** (one by-value stack arg — consistent with P01 QC frame arithmetic [ESP+0x70]=ARG1), returns `AL=steady[0x17]` (BOOL). Only the FAILURE write of that flag (0 @006b1faa) is in-region; the 006b1faa block's fall-through (starts 0x006b1faf) is out-of-region/unread.

## COUNTERS: actual vs reserved

- Bodies: **2 actual** (contract body-entries 0x006B1E0B, 0x006B1E2F; both are in-function branch-target blocks of 006B1C80 — P01-C8-class map note; 0 new logical functions) vs 2 reserved. Region completes walker 006B1C80's full body.
- Instruction rows: **136 actual** / 136 reserved (consecutive source lines 626546-626681; line parity exact).
- CALL sites: **23 actual** (18 direct incl. 4× 004152f0 + 2× 007b6c30; 5 indirect incl. 2× [0x00A759FC]) / 23 reserved.
- Candidates: **2 actual** (CAND-P2a keyed-lookup; CAND-P2b conditional hand-off) / 2 reserved.
- Front A running totals after P02: **5/16 bodies, 372/1800 rows, 42/64 CALL, 6/12 candidates** (P01 QC-confirmed 3/236/19/4 + P02 2/136/23/2); campaign totals 5/96, 372/12000, 42/320, 6/48.

## GATES

See GATES.json. RUN_STATUS: COMPLETED (all contract-required outputs materialized; wall respected; no new regions read; no forbidden access; no config/skills/frozen-root/repo changes).

## HONEST LIMITS

1. All absence claims are scoped to the admitted region (explicit-store level); callee-internal binding channels (all 23 CALLs, incl. the 007b6c30 get-or-create countermodel) remain open — this is exactly why P02-B1 is the missing link.
2. The stack-slot identity derivation (steady[0x68] flag, steady[0x18] receiver, &steady[0x40]/[0x44] args) rests on the callee-pops convention for [0x00A75A00], derived from per-iteration stack-balance necessity; the counter-convention is preserved in CLAIMS (it would shift slot names, not the VA-anchored census or the binding-absence result).
3. steady[0x18] origin and the success-write site of steady[0x17] are NOT established from the admitted corpus (P01 REPORT/QC do not itemize them; P02 is forbidden from re-reading P01's window) — both flagged in BARRIER_BACKLOG.
4. Out-of-region exit targets 0x006B1FB4 and 006b1faa's fall-through (0x006b1faf+) were recorded as addresses only, not read.
5. Semantics-level namings ("keyed lookup", "retain-shaped", "node list") are pattern-based and hedged in CLAIMS; no RTTI names were used; vtable proximity (0xA85460 vs 0xA85454) is class/type identity only, not instance identity.
