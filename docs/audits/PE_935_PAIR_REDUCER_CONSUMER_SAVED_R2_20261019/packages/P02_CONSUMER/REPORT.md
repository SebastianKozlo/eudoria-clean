# P02 — Etap B: consumer 006C4060 continuation + first real use of global 0x00BA45E8 (SAVED-ONLY)

RUN_ID = PE_935_PAIR_REDUCER_CONSUMER_SAVED_R2_20261019 | PACKAGE = P02 | WORKER = pe-reconstruction
Admission: Ad4f041c2ce70 (EVENTS/000003_ADMIT.json). Extract: P02_EXTRACT, 62 rows, region [006C4160,006C4220) (first listed VA 006C4166), sha256 CBFAB8283853F3833EC36E498CA15502AE3465BEF29867C50ACBFA8754B23AE5 (verified by worker, Get-FileHash).
Corrections C1..C8 assimilated before analysis (run-root CORRECTIONS_APPLIED.json). Closed priors used read-only: QUALIFICATION_SAVED_R1 P04/P05 (extracts in P04_CALLER2_R1), P06/P07 (extracts in P06_CONSUMER_R1), P08 (WINDOW_006C3D40), P09 (WINDOW_006C2C90), P10 (WINDOW_006C36B0), P03 (WINDOW_006C3F50); DEEP_POSTAUDIT_R1 REPORT.md + STACK_REDERIVATION.json; sibling P01_ADAPTER (this run).

RUN_STATUS = COMPLETE_WITHIN_ASSIGNED_SCOPE (HARD STOP at assignment boundary; parent run not closed)

## 0. Executive result

The continuation closes the body of **006C4060**: it is **domknięte** at RET @006C41F0 (single normal exit; no branch escapes the combined windows). After the projection loop 006C36B0 fills the global container, 006C4060 does NOT interpret the collected DWORDs as ids/pointers anywhere in the admitted windows. It performs **container maintenance**: it hands the global range (begin,tail) to an opaque callee **0x008D6D90**, then — based on the returned position — executes an **in-place compaction that erases the returned position and drops every ZERO element after it** (@006C4180-4190), relocates any block the callee appended (memmove-like fix-up through [0x00A753B4]), rewrites the global tail M32[0x00BA45EC] (@006C41AE), and finally deallocates the local container C's buffer through [0x00A759FC]. The **first PROVEN element-VALUE consumer** of the global in the whole admitted chain is `TEST EDX,EDX @006C4182` — a zero-vs-nonzero test only. No resource/world/transform edge appears; DATA_DOMAIN is not advanced by this window (negative result within scope).

## 1. Q1 — Full normal path and closure (CONFIRMED)

Combined listing = P06 WINDOW_006C4057 (rows 650268-650308), P06 WINDOW_006C40E0 (rows 650309-650349), P02_EXTRACT (rows 650350-650411): **144 rows, listing row numbers strictly continuous, 143 inter-row VA deltas all equal to the x86 encoding length of the preceding instruction** (programmatic delta extraction + manual encoding check; the two cross-window seams verified: 006C40DF `CALL 0x006c2c90` → 006C40E4 delta 5 = E8 rel32; 006C415E `MOV dword ptr [ESP+0x50],0x0` → 006C4166 delta 8 = C7 44 24 50 +imm32). Note `JMP 0x006c4180` @006C417B is 5 bytes (E9 rel32, rel=0): compiler loop-head alignment at the 16-byte-aligned 006C4180.

**Normal path (single entry @006C4060, single normal exit RET @006C41F0):**

1. Prolog: SEH frame (state −1 @006C4060, handler **0x00A04968** data-pushed @006C4062, FS chain @006C4067/406D/4081), `SUB ESP,0x24` locals, save EBX/EBP/ESI/EDI, cookie `[0x00B9D8D0]^ESP` pushed @006C407C. Base depth **B = E1−0x44** (E1 = entry ESP).
2. `XOR EDI,EDI` @006C4087; shared container **C = B+0x1C** zero-initialized (3 stores @006C4089/408D/4091; C1).
3. SEH state := 0 @006C409F.
4. Collect (closed priors P04/P03): 006C3FE0(0xA855F0, C) @006C40A3; 006C4020(0xA858B8, C) @006C40B2; 006C4020(0xA858C0, C) @006C40C1 — each appends 8-byte pairs into C.
5. `ADD ESP,0x28` @006C40E4 (deferred cdecl cleanup, see §7).
6. Sort-shaped wrapper 006C3D40(M32[C], M32[C+4]) @006C40D0 (prior P08).
7. Adjacent-equality scan 006C2C90(M32[C], M32[C+4]) @006C40DF → EAX (prior P09).
8. If EAX != M32[C+4]: fix-up **006C2C50** (ECX receiver = C; args (EAX, end, &wrapper-byte)) @006C40F6 — opaque; **presumed callee-clean RET 0xC** (premise P4, §7).
9. Context build (closed priors P06/P07 + C2/C3): ESI := 0x00823C10 @006C40FB; CALL 00415670 @006C4100 → EBX; `SUB ESP,0x18` ctx = {0x823C10, EDI=0, EBX, 0xA7957B, 0xA7957B, partial DWORD low byte 1}.
10. Projection call **006C36B0(&out, M32[C], M32[C+4], 0x00BA45E8)** @006C4141 (P10 + P01): per-pair adapter 006C29D0 → pump 00823C10 → EAX DWORD appended to global.
11. Read global: ESI := M32[0x00BA45EC] @006C4146, ECX := M32[0x00BA45E8] @006C414C.
12. Prepare + call **008D6D90(begin, tail, &out_slot, &wrapper)** @006C4168; out_slot zeroed @006C415E; EDI := ESI (tail snapshot) @006C4166.
13. `ADD ESP,0x38` @006C416D (deferred cleanup: ctx + 006C36B0 args + 008D6D90 args, §7).
14. **Global fix-up** (§3): three cases on EAX = 008D6D90's return; possibly CALL [0x00A753B4] @006C41A3; write M32[0x00BA45EC] @006C41AE.
15. Local C cleanup: EAX := M32[C] @006C41B3; SEH state := −1 @006C41B9; if begin != 0: **[0x00A759FC](begin, byte size (M32[C+8]−begin) rounded to 8)** @006C41D4.
16. Epilog: FS restore @006C41DD/41E1; POP ECX(cookie)/EDI/ESI/EBP/EBX; `ADD ESP,0x30`; **RET @006C41F0**.

**Closure verdict**: every JMP/Jcc target in the combined body is inside [006C4060, 006C41F1] (all 9 branch instructions — JZ @006C40E9, JZ @006C4172, JZ @006C4179, JMP @006C417B, JZ @006C4184, JNZ @006C4190, JZ @006C419A, JZ @006C419E, JZ @006C41C1 — census complete; targets 006C40FB/006C4198/006C4180/006C418B/006C41B3/006C41AE/006C41DD). The only RET of the body is @006C41F0. The unlisted intervals [006C41F1, 006C4200) (15 B) and [006C4208, 006C4210) (8 B) contain no instruction start per the pinned listing and are unreachable by fall-through (both follow a RET). **No exit escapes the windows** on the normal path. Exceptional path: SEH handler 0x00A04968 is DATA (PUSH imm @006C4062), never called in normal flow; unwind semantics outside window (opaque, states −1/0/−1 visible). Caveats: (a) callee bodies are separate admissions; (b) **006C36B0's own epilogue/empty-case (@006C3725) remains outside all admitted windows** — a prior-run open edge, not a new escape of THIS body; the balance of 006C4060 depends on 006C36B0 returning normally with args left in place (§7).

## 2. Q2 — Global pair 0x00BA45E8/0x00BA45EC: vector semantics (CONFIRMED)

The three globals form a **12-byte vector header in .data at 0x00BA45E8**: begin = M32[0x00BA45E8], tail = M32[0x00BA45EC], limit = M32[0x00BA45F0]. Elements are 4-byte DWORDs (stride 4 everywhere).

Proof anchors:
- **begin/tail consumed as a range pair**: MOV ESI,[0x00BA45EC] @006C4146 and MOV ECX,[0x00BA45E8] @006C414C → pushed as arg2/arg1 of 008D6D90 (PUSH ESI @006C415C, PUSH ECX @006C415D).
- **tail used as one-past-end bound**: CMP EAX,ESI @006C4170; LEA ECX,[EAX+4] / CMP ECX,ESI @006C4174/4177; loop bound CMP ECX,ESI @006C418E + JNZ @006C4190 — the loop walks 4-byte elements up to the tail VALUE.
- **tail is write-cursor bookkeeping** (closed prior P10): append writes M32[M32[0x00BA45EC]] = value @006C36F6 and advances M32[0x00BA45EC] += 4 @006C36F8, under the capacity guard CMP ECX,[ESI+8] (limit) @006C36E9. The literal 0x00BA45E8 is passed as 006C36B0's arg4 (PUSH @006C412E) and loaded into its ESI (C2).
- **tail reload @006C4192** (`MOV ESI,[0x00ba45ec]`): re-reads the CURRENT tail after 008D6D90 and the compaction loop; only the loop path executes it. It exists because the tail is **shared mutable state** that the opaque callee may have advanced (the code must not assume the pre-call snapshot is still valid). SUB ESI,EDI @006C419C computes the growth = current tail − snapshot; if non-zero, the appended block is relocated (§4).
- **tail write @006C41AE** (`MOV [0x00ba45ec],EAX`): new tail after compaction (+relocation). On the loop path EAX = write cursor (+ moved-block size); on the erase-last path EAX = snapshot−4.
- begin (0x00BA45E8) and limit (0xBA45F0) are **never written** in this window (census: the only global store is @006C41AE).

**GLOBAL_ELEMENT_KIND**: elements are 32-bit DWORDs; the ONLY in-window value interpretation is **zero vs non-zero** (TEST EDX,EDX @006C4182). Element values are never dereferenced as pointers, never compared as ids, never ordered, in this window (store census: EDX loaded from [ECX] is only TESTed and stored). Therefore kind (pointer / handle / id / bit-pattern) = **NOT_ESTABLISHED**; what IS established: zero is a *removable/empty* value at the LOCAL_MECHANISM level (the compaction drops it); the semantic meaning of zero (null handle? failed pump result? tombstone?) is **NOT established** — note the projection appends pump EAX unconditionally (P01 A09: single return path; a 0 return would be appended as 0).

## 3. Q3 — The loop @006C4180-4190 (CONFIRMED)

```
006C4174  LEA ECX,[EAX+4]        ; read cursor = ret+4
006C4177  CMP ECX,ESI            ; ret+4 == tail ?
006C4179  JZ 006C4198            ; (last-element case: no loop)
006C417B  JMP 006C4180           ; E9 rel32 rel=0 (loop-head alignment @006C4180, 16B-aligned)
006C4180  MOV EDX,[ECX]          ; EDX = *read_cursor
006C4182  TEST EDX,EDX
006C4184  JZ 006C418B            ; zero element -> NOT copied (dropped)
006C4186  MOV [EAX],EDX          ; *write_cursor = *read_cursor
006C4188  ADD EAX,4              ; write cursor advances ONLY after a copy
006C418B  ADD ECX,4              ; read cursor advances every iteration
006C418E  CMP ECX,ESI            ; bound = tail SNAPSHOT (pre-008D6D90 value)
006C4190  JNZ 006C4180
```

- **Semantics**: forward, in-place **compaction** of [ret+4, tail_snapshot) into the space starting at ret: zero elements are **removed**; non-zero elements are copied down. EAX = write cursor (init = 008D6D90's return; advances only on copy); ECX = read cursor (init = ret+4; advances always). The write cursor never passes the read cursor (EAX ≤ ECX−4 ⇒ overwrite-safe, single left-to-right pass).
- **The element AT the returned position is dropped UNCONDITIONALLY** (never tested): the write cursor starts on it; it is overwritten by the first copied element or left below the new tail. The TEST!=0 predicate applies only to elements AFTER the returned position.
- **What TEST!=0 means**: an element is kept iff its value ≠ 0 — the only property of element values used in this window.
- **What is NOT established**: (i) element values are not interpreted in ANY other way anywhere in the admitted windows (no pointer deref of a value, no id comparison — census B08); (ii) no bounds guard exists: if 008D6D90 returned EAX with EAX+4 > tail, the loop would read past the array and not terminate before wrap/fault — the code **assumes** (premise, not proof) the return is a valid position in [begin, tail]; (iii) the meaning of zero (§2); (iv) whether zeros before the returned position are ever removed (they are NOT removed here: elements before the returned position are untouched — net effect over the whole array is "erase returned position + all zeros strictly after it").

## 4. Q4 — CALL [0x00A753B4] @006C41A3 and the tail write (structural CONFIRMED; identity PLAUSIBLE)

Args (cdecl, push order @006C41A0/41A1/41A2 — first push = last arg): **arg1 = EAX (dst = write cursor), arg2 = EDI (src = tail snapshot), arg3 = ESI (count = current_tail − snapshot_tail)**; immediate `ADD ESP,0xC` @006C41A9.

- **Structural match to a memmove(dst,src,count)-class block copy**: 3 cdecl args in (dst,src,count) order; count in BYTES; **dst < src** always on this path (EAX < EDI because CMP EAX,EDI @006C4198 fell through); ranges may overlap (dst+count vs src — e.g. dst=src−4, count=8 overlap), so a copy routine safe on overlap (memmove-class) is the coherent candidate. Additional structural pin: the code then computes **EAX+ESI** and stores it as the new tail — this is only correct if **the callee returns dst** in EAX (memmove/strcpy-family return dst). Classification: **(dst,src,count) block-copy fix-up = STRONGLY_SUPPORTED; specific identity memmove = PLAUSIBLE, NOT CONFIRMED** (target = M32[0x00A753B4], indirect slot, body unopened; observation only: the slot lies in the same 0xA75xxx region as the wrapper ctor/dtor slots 0xA75A38/0xA75A44 seen by P01).
- **What the call does**: relocates the block [snapshot_tail, current_tail) — i.e., whatever 008D6D90 appended during its execution — down to [compacted_end, compacted_end+count), preserving appended elements across the compaction.
- **`ADD EAX,ESI` → `MOV [0x00BA45EC],EAX`**: **NOT allocation growth**. It is tail-pointer bookkeeping after in-place compaction + relocation: new tail = compacted_end + relocated_block_size (or = compacted_end when count == 0 via JZ @006C419E; or = snapshot−4 on the erase-last path @006C4179→4198). No allocation happens in-window; begin/limit are untouched. Relative to the pre-call tail the new tail can shrink (elements dropped) or grow (appended > dropped) — the write is "set tail to the correct end", not a capacity event.

## 5. Q5 — 008D6D90, [0x00A759FC], and the [ESP+0x40]=−1 store

- **CALL 0x008D6D90 @006C4168**: **OPAQUE** (direct target VA known; body never admitted). In-window contract (CONFIRMED): args (begin=M32[0x00BA45E8], tail=M32[0x00BA45EC], &out_slot (content 0, zeroed @006C415E), &wrapper_byte (uninitialized local @E1−0x2D)); return EAX is consumed as a **position in the global element array** (compared to tail @006C4170; EAX+4 dereferenced as element in the loop @006C4174/4180) or as a no-op marker (EAX == tail). Best-fit hypothesis (PLAUSIBLE only, falsifiable by opening the body): a position-returning query on the range — e.g. "find first element equal to M32[&out_slot]=0" — since the fix-up then erases that position and drops zeros; an alternative family (position of first predicate-match via the wrapper) is equally compatible. Side effects may include **appending to the global** (the reload @006C4192 exists precisely to pick up tail movement); whether it ever appends is UNKNOWN. Everything about its computation and its other effects remains UNKNOWN (C5).
- **CALL [0x00A759FC] @006C41D4**: **OPAQUE target, deallocation-class role STRONGLY_SUPPORTED**. Args: arg1 = EAX = M32[C] (local container buffer begin, loaded @006C41B3), arg2 = EDX = ((M32[C+8] − M32[C]) >> 3) << 3 (SAR EDX,3 @006C41C9 then three `ADD EDX,EDX` @006C41CC/41CE/41D0 = ×8) — the **byte size of the buffer measured from begin to C+8's value**. Since C's append mechanism (closed prior P03 WINDOW_006C3F50 @006C3F80-96: write cursor = M32[C+4], capacity bound = M32[C+8], growth via 006C2E00) proves **C+4 = end / C+8 = limit**, the size passed is (limit − begin) = the **allocated** size, not the logical size. Guard `TEST EAX,EAX` @006C41B7 / `JZ 006C41DD` = skip-if-null. Executed once, immediately before the epilog, after the last use of C. Candidate identities (PLAUSIBLE, not established): sized deallocation (operator delete[](void*,size_t)-class) or a custom free(ptr,size). NOT a release/COM-pattern call on the evidence available (single DWORD arg pair, buffer semantics).
- **`MOV [ESP+0x40],0xffffffff` @006C41B9**: writes the **SEH state slot** (E1−0x44+0x40 = E1−0x04 — the same slot as the prolog PUSH −1 @006C4060 and the state-0 store @006C409F). Standard MSVC epilog idiom: state −1 = "no further objects to unwind". NOT a data flag, NOT a status code, NOT related to the −1 in EDX arithmetic. Slot identity CONFIRMED by depth arithmetic; the MSVC-idiom reading is STRONGLY_SUPPORTED (same pattern family as the P01 adapter frame). Note the store is interleaved between TEST @006C41B7 and JZ @006C41C1 without disturbing the flags (MOV does not write flags).

## 6. Q6 — Incidental neighbors (marked, not interpreted)

- **006C4200** — complete small function (5 rows, ends RET @006C4207): `XOR EAX,EAX; CMP [ECX],EAX; SETNZ AL; RET` → returns EAX = ([ECX] != 0). Mechanism is fully visible in-window; **identity/domain/callers NOT established** (no in-window caller; what ECX points to at runtime unknown). Separate body; NOT part of 006C4060 (15 B of unlisted padding after RET @006C41F0).
- **006C4210** — **partial** function, cut at the window end (006C4220): `PUSH ESI; MOV ESI,ECX; MOV ECX,[ESP+8]; MOV [ESI+0x88],ECX; MOV EAX,[ECX]; MOV EDX,[EAX+0x44]` (then window ends). Mechanism prefix visible (thiscall-style receiver in ECX→ESI; stores arg1 at [this+0x88]; then two-level deref [arg1] → [+0x44]); **NO interpretation beyond the window** — the body is incomplete, its callers/semantics are outside scope. Marked as an unopened neighbor requiring its own admission if ever needed.

## 7. Q7 — Deferred cleanup balance of the whole body (CONFIRMED / STRONGLY_SUPPORTED where noted)

**cdecl CALLs and their cleanup (all 11 call sites of 006C4060):**

| Site | Target | Args pushed | Cleanup | Status |
|---|---|---|---|---|
| 006C40A3 | 006C3FE0 | 2 (0xA855F0, C) | deferred → ADD ESP,0x28 | CONFIRMED (prior P04: RET, no imm) |
| 006C40B2 | 006C4020 | 2 (0xA858B8, C) | deferred → ADD ESP,0x28 | CONFIRMED (prior P04/P05) |
| 006C40C1 | 006C4020 | 2 (0xA858C0, C) | deferred → ADD ESP,0x28 | CONFIRMED |
| 006C40D0 | 006C3D40 | 2 (begin, end of C) | deferred → ADD ESP,0x28 | CONFIRMED (prior P08: RET) |
| 006C40DF | 006C2C90 | 2 (begin, end of C) | deferred → ADD ESP,0x28 | CONFIRMED (prior P09: RET) |
| 006C40F6 | 006C2C50 | 3 (pos, end, &wrapper) + ECX this=C | **callee-clean RET 0xC inferred** (unopened) | STRONGLY_SUPPORTED (premise P4) |
| 006C4100 | 00415670 | 0 visible | none needed | — |
| 006C4141 | 006C36B0 | 4 (&out, begin, end, 0x00BA45E8) | deferred → ADD ESP,0x38 | STRONGLY_SUPPORTED (premise P3; its RET outside admitted windows) |
| 006C4168 | 008D6D90 | 4 (begin, tail, &out_slot, &wrapper) | deferred → ADD ESP,0x38 | STRONGLY_SUPPORTED (premise P3) |
| 006C41A3 | [0x00A753B4] | 3 (dst, src, count) | **immediate ADD ESP,0xC** @006C41A9 | CONFIRMED |
| 006C41D4 | [0x00A759FC] | 2 (buffer, size) | **immediate ADD ESP,0x8** @006C41DA | CONFIRMED |

- **ADD ESP,0x28 @006C40E4** = 5 calls × 2 args × 4 B = 0x28 **EXACT** (unconditional segment; both window paths).
- **ADD ESP,0x38 @006C416D** = ctx (SUB ESP,0x18 = 6 DWORDs) + 006C36B0 args (4) + 008D6D90 args (4) = 14 DWORDs = 0x38 **EXACT** — valid on BOTH paths **iff** 006C2C50 cleans its own 3 args on the taken branch. The cdecl-006C2C50 alternative is falsified by three independent fixed-offset facts that only cohere at one depth: (i) the 0x38 sum itself; (ii) the [ESP+0x38] reads @006C4121/006C4136 must resolve to C+4/C+0 (end/begin of the pair array — matching closed-prior C4/P01 map) and would otherwise read saved-EBX/locals; (iii) the [ESP+0x50] store @006C415E must resolve to the out-slot E1−0x2C and would otherwise clobber saved EBP. Hence: **006C2C50 = thiscall-style with callee-clean RET 0xC** (STRONGLY_SUPPORTED; body unopened — recorded as premise, not fact).
- **Epilog vs prolog** (exact mirror): prolog pushed [−1, handler, FS] (0xC) + SUB 0x24 + [EBX,EBP,ESI,EDI,cookie] (0x14) = frame 0x44 below the return address. Epilog: FS restore via [ESP+0x38] (=E1−0x0C) @006C41DD/41E1; POP ECX (cookie — **popped and discarded, NO /GS validation visible in-window**) @006C41E8; POP EDI/ESI/EBP/EBX (exact LIFO reversal of the prolog pushes); `ADD ESP,0x30` = locals 0x24 + SEH trio 0xC; RET @006C41F0 pops the return address. **0x14 + 0x30 = 0x44 = prolog frame — balanced, zero residual, on every path** (the dealloc branch's PUSH×2 is cleaned by its own ADD ESP,0x8 before the epilog).
- **Independent depth-model confirmation** (three SEH/known-slot writes at three different depths all resolving to their correct slots): [ESP+0x48] @006C409F (depth E1−0x4C) → E1−0x04 (state 0); [ESP+0x50] @006C415E (depth E1−0x7C) → E1−0x2C (out-slot); [ESP+0x40] @006C41B9 (depth E1−0x44) → E1−0x04 (state −1). Full [ESP+x] census in STACK_MAP.md; zero unexplained offsets.

## 8. First real consumer of the global (task goal)

- **Header-level consumption** (pointers, not element values): reads @006C4146/006C414C → args of 008D6D90 @006C4168; loop bound @006C418E; tail write @006C41AE.
- **First PROVEN element-VALUE consumer in the admitted chain**: `MOV EDX,[ECX]; TEST EDX,EDX` @006C4180/4182 (the compaction predicate). Everything before it (collect/sort/scan/projection/append) moves or appends DWORDs without interpreting them. A value-level consumer may exist INSIDE opaque 008D6D90 (it receives the range) — unproven; if it exists, it is earlier in program order but still opaque.
- **Consequence for the mission**: this window advances the container-lifecycle understanding (projection → post-processing/maintenance of the global list), NOT the MODEL_RESOURCE→WORLD_INSTANCE bridge: no element is interpreted as an id, handle or pointer here.

## 9. Axes (per C5)

- LOCAL_MECHANISM: **CONFIRMED** (full normal path, ABI of all 11 call sites, stack balance, compaction/fix-up/dealloc mechanics).
- DATA_DOMAIN: **NOT_ESTABLISHED, unchanged standing** — pairs come from static id tables (0xA855F0/0xA858B8/0xA858C0) and pump-produced DWORDs; "compile-time resource dependencies" remains a hypothesis; this window adds no domain evidence (elements only tested !=0).
- OPAQUE_EFFECTS: **UNKNOWN** — 008D6D90 (may append; computes the position), [0x00A753B4] (block copy; identity), [0x00A759FC] (dealloc; identity), 006C2C50 (fix-up after dedupe), 00415670 (receiver producer), 00823C10 pump + prior-run opaque set. C5 preserved; H1/H2 disjointness NOT asserted (the reload @006C4192 is positive evidence that the caller is written for a callee that may mutate the global — an H2-compatible shape, without proving any enqueue happens).
- WORLD_INSTANCE_RELATION: **NONE established in this window** (negative result within scope; no scene/attach/transform instruction; no element dereferenced as an object pointer).

## 10. Budgets and counters (actual)

| Resource | Reserved | Recognized/used | Charged (no refund) | Cap (run) |
|---|---|---|---|---|
| bodies | 4 (ADMIT) | 3 visible: 006C4060 continuation (same owner as prior P06/P07), 006C4200 (incidental, complete), 006C4210 (incidental, partial); 4th reservation unspent on the partial's unknown continuation | 4 | 32 |
| candidates | 3 | 0 opened; nominated: 008D6D90 (primary), [0xA753B4], [0xA759FC], 006C2C50 (premise falsifier), 00823C10 (P01), 006C36B0 epilogue [006C3720,006C3740) | 3 | 32 |
| listing rows | — | 62 (new extract); 82 prior-window rows (P06 ×2) + 67 P01 rows consulted read-only (charged to their own runs) | 62 | 6000 |
| CALL sites | — | 3 in-window (008D6D90, [0xA753B4], [0xA759FC]); 11 total for the whole body incl. priors | 3 | 200 |
| body document lines | — | 0 | 0 | 1500 |
| INCIDENT_DEBIT | 0 | — | 0 | — |

3 visible bodies ≤ 4 reserved ⇒ no PARTIAL_NONCOMPLIANT, no unexpected-body incident, no refund claimed. Extract sha256 verified; no new body read outside the extract + closed priors; no original-game/runtime/Ghidra operations; no nested tasks; no config changes; no Hermes.

## 11. Missing edges returned to the parent (for its next admission decision)

1. **0x008D6D90 body** (primary): what it computes over the global range; whether it derefs element values (would advance DATA_DOMAIN); its append behavior (resolves the reload/memmove purpose); falsifies/confirm the "find-first-zero" hypothesis.
2. **Targets of [0x00A753B4] / [0x00A759FC]**: memmove/sized-free identity (import-table class of the 0xA75xxx region).
3. **006C2C50 epilogue/RET**: closes premise P4 (callee-clean RET 0xC) into a fact; also its fix-up semantics after the dedupe scan.
4. **006C36B0 epilogue [006C3720,006C3740)**: closes its normal-exit/empty-case (prior-run open edge; also closes the "returns with args left" premise P3 for this callee).
5. **0x00823C10 pump body** (P01's primary nomination — still open; the producer of the element values).

## 12. SELF_CHECK (worker-level, not independent MASTER audit)

- [x] Extract SHA256 matches contract (CBFAB828…23AE5); admission header (Ad4f041c2ce70, 62 rows, 3 calls) consistent with contract and file.
- [x] Full raw census: 62/62 extract rows read and analyzed; 144 combined rows / 143 deltas verified byte-contiguous; both cross-window seams encoding-verified; 3/3 in-window CALL sites classified (11/11 body-wide with priors).
- [x] Every [ESP+x] reference in the extract accounted at its exact depth (STACK_MAP §3); the deferred-cleanup arithmetic closes to the byte on both paths; epilog mirrors prolog exactly; three independent depth-model confirmations recorded.
- [x] Negative controls: no-branch-escape census (all Jcc/JMP targets in-window); element-values-never-deref'd census (B08); only-global-write census (@006C41AE); begin/limit-untouched census.
- [x] C1..C8 preserved (C1 single container used throughout; C3 partial DWORD kept as-is in ctx[5]; C5 all opaque effects UNKNOWN; no domain naming without edges); no silent promotion — 006C2C50 callee-clean is a LABELLED premise with falsifiers, not a fact; memmove/dealloc identities stay PLAUSIBLE/STRONGLY_SUPPORTED-structural.
- [x] No default-success: GLOBAL_ELEMENT_KIND, DATA_DOMAIN, world relation, meaning of zero, 008D6D90 semantics all NOT_ESTABLISHED/UNKNOWN as applicable; PASS not written for package structure.
- [x] Counters honest: 4/4 bodies, 3/3 candidates charged without refund; 62 rows; 3 CALLs; 0 document lines; INCIDENT_DEBIT 0.
- [x] Scope: no body outside the assigned extract + explicitly authorized closed priors opened; priors read-only; HARD STOP at assignment boundary; parent run not closed; no seal by worker.
