# P03 PUMP REPORT - 0x00823C10 (producer of adapter return value)

ATTRIBUTION: DIRECT_ANALYST_FALLBACK_BY_PE_MASTER (two empty worker attempts; see RUN_STARTED.json).
SCOPE: admitted window [0x00823C10,0x00823E58) from pinned H5 listing (sha 642CC29A...D8DB), 185 rows, 20 CALL sites. Read-only context: P01_ADAPTER, P02_CONSUMER, closed priors. No original/runtime/Ghidra operations.

## 1. ABI (CONFIRMED)

thiscall: ECX=this(receiver); 4 stack args (callee cleans RET 0x10 @00823E57); returns 32-bit EAX; full SEH frame (handler literal 0xA236F8 @00823C12, cookie @00823C25-2C, FS:[0] install @00823C31, restore @00823E44-48).
Entry stack after prologue (ESP0 = entry ESP, frame depth 0x3C+arg slots):
- arg1 @ESP+0x40 = pair_ptr (from adapter: deref of arg3 holder, current pair address)
- arg2 @ESP+0x44 = &local (adapter local D)
- arg3 @ESP+0x48 = &local (adapter local B)
- arg4 @ESP+0x4C = context cursor word (S+10h low byte patched to 1)
EBP = arg1 = pair_ptr (@00823C3D). arg4 is NEVER READ in-window (arg4_dead_in_window, claim P03-K12).

## 2. Receiver handling (CONFIRMED)

EDI=ECX=this @00823C37. CALL 0x004D1430(this=EDI+4, &arg1_slot_addr, &local) @00823C57 — pair[0]=M32[EBP] read @00823C41 and stored into the ARG1 SLOT @00823C53 before this call; 004D1430 receives a pointer to that slot. EDI then advances to a sub-object: EAX=M32[ESP+0x18] (local); if EAX==EDI+4 then EDI+=0x1C else EDI=EAX+0x14 (@00823C5C-6C). After this point the window operates on receiver sub-object EDI with fields: [EDI+0x18]/[EDI+0x1C] list bounds (stride 0x10 loop), [EDI+0x24] resolver object, byte [EDI+0x38] flag.

## 3. Normal return paths (CONFIRMED)

The pump is an object RESOLVER. Returned EAX on every normal path is either an OBJECT POINTER or 0:

PATH-FAST (non-null): [EDI+0x24] present → virtual EAX=[ [EDI+0x24] ]vtable+0x4 @00823C7A (no args captured in window) → virtual [[EDI+0x24]]vtable+0x38 with arg EBP=pair_ptr @00823C84-84; ESI=EAX; if ESI!=0 → 00823E11: TLS flag [TLS[M32[0x00BA8E6C]]+8]=0 @00823E11-21; virtual [[EDI+0x24]]vtable+0x8 @00823E27-2F; CALL 0x00826760(this=ESI, arg2, arg3) @00823E31-3D; EAX=ESI @00823E42. RETURN ORIGIN (fast): the vtable+0x38 call on [EDI+0x24] with pair_ptr.

PATH-NULL-A: [EDI+0x24]==0 → XOR EAX,EAX @00823CAE → epilog (returns 0).
PATH-NULL-B: vtable+0x38 returned 0; optional fallbacks (byte [EDI+0x38] flag → CALL 0x00822970(this=saved_this, EBP) TEST AL; if true one more virtual vtable+0x8) then XOR EAX,EAX @00823CAE.
PATH-LOOP: iterates entries ESI in [EDI+0x18],[EDI+0x1C) stride 0x10:
  - if M32[ESI]!=0: virtual [[ESI]]vtable+0x8 with (EBP=pair_ptr, &local) @00823DA2-AD; if AL!=0 → 00823E03 → 00823D13.
  - 00823D13 (also directly when M32[ESI]==0 and M32[ESI+8]!=0): ECX=M32[ESI+8]; EAX=M32[EBP+4]=pair[1] @00823D16; virtual [[ESI+8]]vtable+0x4 with (pair[1], &local) @00823D21-24; ESI=EAX;
    - if ESI==0 → abort loop to 00823DBF (post-loop null-out path, returns 0 via 00823DFF).
    - else: CALL 0x00826840(this=ESI, EBP=pair_ptr) @00823D30-33; virtual [[EDI+0x24]]vtable+0x3C with (&[ESP+0x24], ESI) @00823D38-46; optional [saved_this+0x58] vtable+0x4 with (ESI) @00823D48-5A; TLS flag [...]+8=1 @00823D5C-74; EH-scope (0040E180 @00823D83, state -1 @00823D7B) with dealloc 0x0095DB40(local) @00823D90-9D; JMP 00823E27 (same finish as fast path).
  - loop increment @00823DB3; on exhaustion → 00823DBF: optional CALL 0x008237D0(this=saved_this, EBP); virtual [[EDI+0x24]]vtable+0x8; EH-scope close; XOR EAX,EAX @00823DFF (returns 0).

RETURN ORIGIN (loop): the vtable+0x4 call on [entry+8] with pair[1] — object pointer ESI, subsequently used as `this` in 00826840 and 00826760.

## 4. Consumption of the pair (CONFIRMED, in-window)

- pair[0]=M32[EBP] read @00823C41 (stored to arg1 slot, passed by address to 004D1430, and the local-vs-EDI+4 comparison selects the sub-object).
- pair[1]=M32[EBP+4] read @00823D16 (argument to the loop resolver vtable+0x4 call).
Both DWORDs are consumed as opaque values by resolver interfaces. No arithmetic interpretation, no id comparison against a constant, no world/resource semantic in-window.

## 5. Visible effects vs opaque (axes)

LOCAL_MECHANISM: CONFIRMED as above (SEH, TLS flag 0x00BA8E6C index, EH scopes with -1 state slots, alloc/free pair 0095D3BE(0x80)/0095DB40).
DATA_DOMAIN: NOT_ESTABLISHED — resolver object identity, [EDI+0x24] class, [ESI+8] interface, 00826840/00826760 semantics all opaque (unopened). The returned value is an OBJECT POINTER by use (this-arg in thiscalls @00823D31/00823E3B) or 0; pointer/handle/id distinction beyond object-pointer-use is not established.
OPAQUE_EFFECTS: UNKNOWN for all 20 unopened callees; nothing observable in-window excludes additional effects (C5 preserved).
WORLD_INSTANCE_RELATION: NOT_ESTABLISHED. No RTTI, no NiNode/NiTriShape evidence in-window; no transform write, no scene attach. The pump result being an object pointer does NOT promote the global vector to a world-instance registry.

## 6. Comparison with closed CAND4 claims (within their scope)

CAND4 claim "pump ABI has four DWORDs, not three" — CONFIRMED consistent (RET 0x10, 4 stack args). CAND4 receiver/slot3 claims were not re-verified beyond this window; no conflict found within compared scope.

## 7. Containment (CONFIRMED)

All 16 intra-window jump targets (00823c69,c6c,cae,cb5,d00,da2,db3,dbf,d13,d5c,df,dff,e11,e27,e03,e44) lie within [0x00823C10,0x00823E58); body ends RET 0x10 @00823E57; byte-contiguous instruction stream; no jump outside the window; no new admission needed for this body.

## 8. Value graph extension (pair -> pump -> returned EAX)

E-PAIR0: pair[0] @00823C41 -> arg1-slot -> 004D1430 + sub-object selection. CONFIRMED.
E-PAIR1: pair[1] @00823D16 -> loop resolver vtable+4 arg. CONFIRMED (loop path only; fast path passes pair_ptr itself to vtable+0x38).
E-RET-FAST: EAX = [[EDI+0x24]vtable+0x38](pair_ptr) @00823C84. CONFIRMED origin; value kind = object pointer or 0.
E-RET-LOOP: EAX = [[entry+8]vtable+0x4](pair[1], &local) @00823D24. CONFIRMED origin; value kind = object pointer or 0.
E-FINISH: both paths call 00826760(this=result, arg2, arg3) before return — the result object is ACTED ON before the adapter sees it (additional opaque effects on the result object, C5).

## 9. Budget counters

bodies 3/3 reserved+charged (1 unique owner 0x00823C10); candidates 3/3 charged (0 opened; nominations: 004D1430, 00826760, 00826840, [EDI+0x24] resolver class, [entry+8] interface, 00822970, 008237D0, 0095D3BE/0095DB40); rows 185/6000; calls 20/200; doc lines 0/1500; INCIDENT_DEBIT 0 (no unexpected body: containment proven).

RUN_STATUS = COMPLETE_WITHIN_ASSIGNED_SCOPE (DIRECT_ANALYST_FALLBACK attribution; parent run open).
