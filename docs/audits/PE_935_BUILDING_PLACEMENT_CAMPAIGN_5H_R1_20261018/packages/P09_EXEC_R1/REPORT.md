# P09 REPORT — C1 transport close-out: 0x006C3640 (second enqueue path of the {0x66,A} request)

run_id: PE_935_BUILDING_PLACEMENT_CAMPAIGN_5H_R1_20261018 | package: P09 (Front C) | admission: A14f4207636e3
scope: saved-evidence only; sole admitted source GHIDRA_H5_VTABLE2.txt (SHA256 642CC29A...D8DB, re-hash MATCH), region 0x006C3640-0x006C3678 (end-exclusive), listing lines 649385-649407, 23 rows, 1 body prefix, 1 in-window CALL, 4 edges, 2 candidates. No EXE/payload/runtime/Ghidra/old-scripts/config/skills/frozen-root/repo actions.

## 1. Question and answer summary

**Q:** What is the queue object, the entry layout, and the enqueue semantics of 006C3640? Which queue-object fields does it write (entry pointer store, count update, tail/head)?

**A (mechanics CONFIRMED in-window; semantic identity labels are cited-P07 / arg-shape inference, labeled as such):**

- **Function shape.** 0x006C3640 is a generic per-element enqueue loop (prefix of one body; the body continues out-of-window past 006C3678). It loads four stack arguments: `stack_arg[1]->EDI` (element range begin), `stack_arg[2]->EBP` (element range end), `stack_arg[3]->ESI` (queue object), `stack_arg[4]->EBX` (per-element callback). `stack_arg[0]` is never read in-window; entry ECX is unused before being overwritten. The loop exits when EDI==EBP (entry check `CMP/JZ -> 0x006C369C`, out-of-window). Arg roles are ARG-SHAPE INFERENCE from downstream usage; exact arg count/ABI (RET width) is not determinable in-window (epilogue out-of-window).

- **Queue object.** The queue object is the 4th stack DWORD (in ESI), with in-window field census:
  - `[ESI+0x0]`: never touched in-window — role UNKNOWN (no in-window head/base evidence).
  - `[ESI+0x4]`: **write/tail cursor POINTER** into a dense entry array — read at 006c365c, and the **ONLY queue-object field written in-window**, at 006c3672 as `+= 8` per enqueued entry. Pointer-ness is proven by direct dereference (006c366a/006c366f).
  - `[ESI+0x8]`: **limit/end value compared for equality with the cursor** (006c365f, read-only in-window; interpreted as buffer end/limit — PLAUSIBLE, never dereferenced in-window).
  - **No count update, no head update, no entry-pointer store into object fields occur in-window.** The enqueue commits an entry purely by the cursor advance; the pair itself is written in-place at the cursor target.

- **Entry layout.** One entry = **8 bytes = 2 DWORDs**: `entry[+0] <- [EAX]`, `entry[+0x4] <- [EAX+4]`, where EAX is the callback's return value (the "derefed pair" per P07). No per-entry header/tag/size in-window. Whether these DWORDs are the {0x66,A} request pair is inherited from cited P07 caller context; the window itself contains no 0x66 literal and no identity data (scoped negative, P09-C8).

- **Enqueue semantics (per iteration).** (i) `ECX = EDI` (current element); `CALL EBX` — callback invoked thiscall-shaped with ECX=current element (ABI inference; callee out-of-window). (ii) `ECX = [ESI+4]` (cursor). (iii) If `[ESI+4] == [ESI+8]` → `JZ 0x006C3678`: **capacity-event path, out-of-window** (candidates CAND-A grow/extend vs CAND-B lazy-alloc/flush — both UNVERIFIED, not distinguishable in-window). (iv) Else if cursor == NULL → skip store, count-only advance. (v) Else copy the pair into `[cursor]`/`[cursor+4]`. (vi) `[ESI+4] += 8`; `JMP 0x006C368a` (loop tail, out-of-window; navigation confirms a back-edge `006c368f JNZ 0x006c3658` to the in-window loop head). Disclosed oddity: the NULL-skip path leaves `[+4]=8` after its ADD; without out-of-window repair a next iteration would dereference an invalid pointer — recorded as countermodel in P09-C3, not resolvable in-window.

- **Transport position (cited P07 + navigation census, no re-derivation).** Exactly **2 call sites** target 0x006C3640 in the saved listing (006c3fcd, 006d4501), inside the caller clusters 006C3F98 / 006D44A4 that per P07 first call 40B070 (sites 006c3fb5 / 006d44ed by navigation) — the second enqueue path of the {0x66,A} request with callback 8BD720. The first path (pump 006B6C9D) enqueues via 43E5B0 per P07; equivalence of 43E5B0 to this helper is NOT claimed (identical shapes do not prove common semantics; 43E5B0 body is a data barrier).

## 2. Corpus-coverage data barrier (parent-verified, independently re-verified here)

0x0040B070, 0x0043E5B0, 0x0043C700 have **zero body rows** in GHIDRA_H5_VTABLE2.txt and appear only as CALL operands (17 / 1 / 10 sites). The three transport-chain callee bodies are a **data barrier** for this listing. Incidental navigation also matched a separate saved corpus file, `GHIDRA_GATE_00407270.txt`, containing a decompiled `FUN_0040b070` signature — recorded in BARRIER_BACKLOG (P09-B3) as a candidate to lift the 0040B070 half of the barrier; NOT read/analyzed in this package. A first `rg` census attempt failed (CommandNotFoundException); those outputs were discarded and all census results come from the working Grep tool.

## 3. Premises and honest limits (preserved)

- All register-role labels (begin/end/queue/callback) and the callback ECX-ABI note are labeled ARG-SHAPE/ABI INFERENCE; ESP-offset arithmetic itself is CONFIRMED from rows.
- Callback EAX-return is a premise (first iteration has no in-window EAX init); callback body out-of-window.
- Element stride NOT determinable in-window (stride arithmetic is in the out-of-window loop tail); range semantics rest on the entry equality check.
- Identical names/shapes do not prove common semantics: queue class identity UNKNOWN; 43E5B0≠006C3640 not asserted.
- Scoped negative bounded to the window: no float math, no coordinates, no identity data, no VFS access in the 23 rows.
- Boundary disclosure: a 42-line read block (listing lines 649378-649419) was displayed once to pin window boundaries; only lines 649385-649407 are used as evidence; adjacent rows are out-of-window and no claims are made on them (NAVIGATION_CENSUS N5).

## 4. Scoped result

CLOSED (in-window): queue-object field census and write set; 8-byte 2-DWORD entry layout; guarded append semantics (capacity-event / NULL-skip / store+advance); 2-site caller census of 0x006C3640. OPEN (barriers P09-B1..B4): capacity-event handler nature (CAND-A/B), element stride, callback body, transport callees 40B070/43E5B0/43C700 (absent from listing), queue consumer/identity. No new identity edge; MODEL_INSTANCE_BINDING unchanged (transport-side only).

## 5. Counters (actual vs reserved)

Reserved (CONTRACT.json): 1 body / 23 rows / 4 edges / 2 candidates. Actual: **1 body (prefix) / 23 rows / 1 CALL (006c365a CALL EBX, indirect) / 4 edges (JZ×3 + JMP×1; 3 of 4 targets out-of-window) / 2 candidates**. Discrepancy disclosure: dispatch prose said "4 CALL" while CONTRACT.json reserves "edges: 4" and the question itself says "1 call"; reconciled as edges=4, CALL=1. Unforeseen in-window bodies: 0. Incidents: 0. Union VA opened: 0x006C3640-0x006C3678 (0x38 bytes).

Process disclosure (timestamp discipline): during packaging, several non-load-bearing stamps in EXTRACT/NAVIGATION_CENSUS/SOURCE_PINS/GATES/MANIFEST were initially written as estimates rather than tool-clocked values. SELF_CHECK caught this; all invented stamps were replaced with real tool-clock anchors (23:07:05.746Z run start; 23:12:08.533Z first post-write clock check; 23:12:29.117Z stamped re-hash) or explicit bounded windows, and artifact_index.csv/MANIFEST.json were regenerated over the corrected files. No scientific content (extract rows, claims, censuses) was altered by this correction; only timestamp lines changed.

## 6. Standing

WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; CURSOR_SOURCE_MEDIUM=UNKNOWN; CANONICAL_GATE_EFFECT=NONE. QC_ORIGIN: this report is worker output; independent QC belongs to the parent's reviewer (no independent QC performed in this child, per role boundaries).
