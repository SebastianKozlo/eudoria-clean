# P01_CALLER FLOW — 00527AA0 (short)

```
ENTRY (thiscall: ECX=this, [E+4]=ARG1, RET 0x4)
  │
  ├─ SUB ESP,0x34          frame = 13-dword out-buffer only
  ├─ PUSH EBX / MOV EBX,ECX  owner register = this
  ├─ PUSH EDI
  │
  ├─ EDI = [this+0xC]                ── receiver (single dereference)
  ├─ TEST EDI,EDI ──0──►──────────────► EXIT_EARLY (0x00527b18)
  ├─ CMP [this+0x10],0 ──0──►─────────► EXIT_EARLY
  │
  ├─ FPU block:
  │    field_E0 := +0.0
  │    if (float@0x00A797C8 < field_E4)  field_E8 := field_E4     [JP idiom]
  │    field_E4 := +0.0   (at join 0x00527aeb; FPU depth 0 after)
  │
  ├─ PUSH ESI
  ├─ EAX = LEA [ESP+0xC]  = &buffer (frame base, 0x34 bytes)
  ├─ PUSH EAX                          arg for 0085BFA0
  ├─ ECX = EDI (= [this+0xC])          receiver for 0085BFA0
  ├─ CALL 0085BFA0                     get-transform: writes 13-dword output
  │        {9 rot + 3 trans + 1.0f} into buffer; returns EAX=&buffer
  │        (frozen prior R2 P04-K01/K03; callee RET 0x4)
  ├─ EDI += 0x30                       dest = receiver+0x30
  ├─ ESI = EAX                         src = &buffer
  ├─ REP MOVSD, ECX=0xD                buffer → receiver+0x30 (13 dwords)
  │
  ├─ ECX = [ESP+0x44] = ARG1           this function's own arg
  ├─ PUSH ECX                          forwarded as sole arg
  ├─ ECX = [this+0x10]                 second object as receiver
  ├─ CALL 00861150                     semantics UNKNOWN (unopened)
  │
  └─ POP ESI
EXIT_EARLY:  POP EDI / POP EBX / ADD ESP,0x34 / RET 0x4
```

Two CALL sites total (0085BFA0 @0x00527af9; 00861150 @0x00527b12); no indirect/virtual dispatch in this window. One body (00527AA0), complete in-window. Guards make the method a no-op when either pointer field is null.
