# FLOW — 006C29D0 (adapter, Etap A, P01)

Single basic block. Zero JMP/Jcc in the entire window [006C29D0,006C2AB0) — verified by mnemonic census over all 67 rows (66 deltas byte-contiguous; RET 0x10 @006C2AAC is the only exit).

## 1. Control flow (all 9 indirect CALLs marked opaque)

```
006C29D0 entry (ECX = this = &ctx[2] = S+0x1C; 4 stack args)
  ├─ prolog: SEH(-1, handler 0xA04804, FS), SUB 0x34, save ESI/EDI, cookie^ESP, FS:[0]←E0-0xC
  ├─ ESI = this                                (006C29F5)
  ├─ [OPAQUE-1] CALL [0x00A75A38](this=&local_A)            → result_A   (006C29FB)
  ├─ EDI = [0x00A75A44]                                     (006C2A01)
  ├─ ctx[4] = M32[this+8] → PUSH                            (006C2A08/0B)
  ├─ SEH state := 0                                          (006C2A10)
  ├─ [OPAQUE-2] CALL EDI(this=&local_B, ctx[4]=0xA7957B, result_A)          (006C2A18)
  ├─ [OPAQUE-3] CALL [0x00A75A38](this=&local_C)            → result_C   (006C2A1E)
  ├─ ctx[3] = M32[this+4] → PUSH                            (006C2A24/28)
  ├─ SEH state := 2                                         (006C2A2D)
  ├─ [OPAQUE-4] CALL EDI(this=&local_D, ctx[3]=0xA7957B, result_C)          (006C2A32)
  ├─ CL = M8[this+0xC] = ctx[5]&0xFF (=1 per C3)            (006C2A34)
  ├─ pair_ptr = M32[M32[arg3]] = M32[S+0x10]                (006C2A37/3B)
  ├─ ESI = M32[this] = ctx[2] = 00415670_result             (006C2A3D)
  ├─ M8[arg3-slot] = CL   (own arg3 low byte := 1)          (006C2A3F)
  ├─ patched_slot = M32[arg3-slot] = (S+0x10)&~0xFF | 1     (006C2A43)
  ├─ PUSH patched_slot; PUSH &local_B; PUSH &local_D; PUSH pair_ptr        (006C2A47..52)
  ├─ rec = M32[arg2] = &ctx[0] = S+0x14                     (006C2A53)
  ├─ ECX = M32[rec+4] = ctx[1]; EAX = M32[rec] = ctx[0]     (006C2A57/5A)
  ├─ ECX += ESI   → receiver = ctx[1] + ctx[2] = 0 + obj    (006C2A5C)
  ├─ SEH state := 3                                         (006C2A5E)
  ├─ [OPAQUE-5, VALUE PRODUCER] CALL EAX @006C2A63
  │     target  = ctx[0] = 0x00823C10
  │     this    = receiver = 00415670_result (+0)
  │     args    = (pair_ptr, &local_D, &local_B, patched_slot)
  │     → EAX = REDUCED VALUE (kind opaque)
  ├─ ESI = EAX (save result)                                (006C2A69)
  ├─ [OPAQUE-6] CALL [0x00A75A5C](this=&local_D) dtor       (006C2A70, state 2)
  ├─ [OPAQUE-7] CALL [0x00A75A40](this=&local_C) dtor      (006C2A7A)
  ├─ [OPAQUE-8] CALL [0x00A75A5C](this=&local_B) dtor      (006C2A89, state 0)
  ├─ [OPAQUE-9] CALL [0x00A75A40](this=&local_A) dtor      (006C2A93)
  ├─ EAX = ESI (restore result)                             (006C2A99)
  ├─ epilog: FS restore, POP cookie/EDI/ESI, ADD ESP,0x40, RET 0x10 (006C2A9B..AAC)
  └─ EXCEPTIONAL: SEH handler 0xA04804 (outside window) — unwind by state; no EAX contract
```

## 2. Value graph (source → sink, with provenance and label)

| Edge | From → To | Mechanism / VA | Pointer level | Label |
|---|---|---|---|---|
| E1 | CALL 00415670 @006C4100 (006C4060, closed prior P06) → ctx[2] | MOV [EAX+8],EBX @006C4116; copy-by-value into 006C36B0 frame | L0 value → L1 slot | STRONGLY_SUPPORTED (closed prior + nonvolatile premise; producer opaque) |
| E2 | ctx[2] (S+0x1C) → callee this + ESI | ECX at CALL 006C36E1; MOV ESI,ECX @006C29F5; MOV ESI,[ESI] @006C2A3D | L1 | CONFIRMED (listing) |
| E3 | ctx[0] (S+0x14, = 0x00823C10 per closed prior) → pump target | MOV EAX,[ESP+0x64] @006C2A53 (rec); MOV EAX,[EAX] @006C2A5A; CALL EAX @006C2A63 | L1 (value from memory) | CONFIRMED mechanism; target VALUE 0x00823C10 STRONGLY_SUPPORTED (closed prior construction + no-writer census; opaque callees cannot be excluded a priori) |
| E4 | ctx[1] (S+0x18, = EDI=0 per closed prior) → receiver addend | MOV ECX,[EAX+4] @006C2A57; ADD ECX,ESI @006C2A5C | L1 | CONFIRMED mechanism; value 0 STRONGLY_SUPPORTED (nonvolatile premise) |
| E5 | receiver = ctx[1]+ctx[2] = 00415670_result → pump this | ECX at CALL EAX @006C2A63 | L0 | CONFIRMED (arithmetic) / object identity UNKNOWN |
| E6 | cursor slot [S+0x10] (caller EDI = current pair addr, C4) → pair_ptr | M32[M32[arg3]] @006C2A37/3B | **L2** (pointer-holder → slot → pair) | CONFIRMED |
| E7 | pair_ptr → pump arg1 | PUSH EAX @006C2A52 | L0 pass-through | CONFIRMED |
| E8 | ctx[5] low byte (=1, C3) → own-arg3 slot low byte | MOV CL,[ESI+0xC] @006C2A34; MOV [ESP+0x58],CL @006C2A3F | byte-granular | CONFIRMED; only byte 0 of ctx[5] consumed — C3's undefined upper 24 bits are NEVER READ by this body |
| E9 | patched_slot = (S+0x10)&~0xFF\|1 → pump arg4 | MOV EDX,[ESP+0x58] @006C2A43; PUSH EDX @006C2A47 | L1 (stack-address, low byte tagged 1) | CONFIRMED mechanism; SEMANTICS UNKNOWN (what the pump does with it) |
| E10 | ctx[3]/ctx[4] (both 0xA7957B) → ctor-D/ctor-B arg1 | @006C2A24/28 and @006C2A08/0B | L0 | CONFIRMED; 0xA7957B role opaque |
| E11 | ctor results (result_A/result_C) → ctor-B/ctor-D arg2 | PUSH EAX @006C2A07/27 | L0 | CONFIRMED (registers not redefined between CALL and PUSH — verified) |
| E12 | &local_D, &local_B → pump args 2/3 | LEA + PUSH @006C2A48..51 | L1 (callee-frame locals) | CONFIRMED |
| E13 | pump EAX → callee return EAX | MOV ESI,EAX @006C2A69; MOV EAX,ESI @006C2A99; RET 0x10 | L0 | CONFIRMED — **the ONLY normal return path** |
| E14 | callee EAX → caller fast-path append into global {0xBA45E8 begin, 0xBA45EC tail, 0xBA45F0 limit} | @006C36E6..FC (closed prior P10): ECX=M32[ESI+4]=M32[0xBA45EC]; M32[ECX]=EAX; tail+=4 | L0→L1 | CONFIRMED (closed prior; not re-derived in P01) |
| E15 | global element → first real consumer 006C4060 continuation @006C4146+ | M32[0xBA45EC], M32[0xBA45E8] read after return (closed prior P06 window, last row 006C415E mid-body) | L1 | OPEN EDGE — outside P01 scope; Etap B of parent plan |

## 3. Dead arguments (negative controls)

- callee arg1 = begin&0xFFFFFF00 (pushed @006C36D8): NO read at depth E0-0x4C offset 0x50 → dead.
- callee arg4 = 0 (pushed @006C36C3): NO read at offset 0x5C anywhere → dead.
- Consequence: the caller's low-byte-zeroing of begin @006C36CF has NO effect on the callee's behavior (dead transformation).

## 4. Axes (per C5)

- LOCAL_MECHANISM: CONFIRMED as above (functor invocation: build 2 wrapper objects from identical constant 0xA7957B, call ctx[0] on object ctx[2] with (pair, wrapper2, wrapper1, tagged-slot-ptr), return its result, destruct in reverse).
- DATA_DOMAIN: pair content = 8-byte elements of the shared C list (closed prior postaudit: collect from static ID arrays 0xA855F0/0xA858B8/0xA858C0 → sort → dedupe). "Compile-time resource dependencies" stays hypothesis (postaudit §4). Pump return kind (id/handle/pointer/bit-pattern): NOT_ESTABLISHED — pump body unopened.
- OPAQUE_EFFECTS: UNKNOWN — all 9 indirect callees unopened (targets: M32[0xA75A38], M32[0xA75A44], M32[0xA75A5C], M32[0xA75A40], 0x00823C10). C5 preserved.
- WORLD_INSTANCE_RELATION: NONE established in this window. No store to 0xBA45E8 inside 006C29D0 (byte-census). Transform/scene edge would have to live inside the pump — unopened.
