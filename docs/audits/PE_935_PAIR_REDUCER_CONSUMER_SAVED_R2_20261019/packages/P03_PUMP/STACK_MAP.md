# STACK_MAP - 0x00823C10 (ESP0 = ESP at entry)

Entry: [ESP0]=ret; args: +4 arg1(pair_ptr), +8 arg2(&local_D), +C arg3(&local_B), +10 arg4(cursor word).

Frame layout below ESP0 (pushed first = highest):
- ESP0-0x04: -1 (SEH)
- ESP0-0x08: 0xA236F8 (SEH handler)
- ESP0-0x0C: FS_old (SEH FS:[0])
- ESP0-0x28..: locals (SUB ESP,0x1C)
- ESP0-0x38..-0x2C: EBX,EBP,ESI,EDI (PUSH order)
- ESP0-0x3C: cookie (PUSH EAX after XOR [0x00B9D8D0],ESP)
Total frame depth = 0x3C (60 bytes). ESP_now = ESP0 - 0x3C.
Arg slots from ESP_now: arg1=+0x40, arg2=+0x44, arg3=+0x48, arg4=+0x4C.

Key stack facts (anchors):
- [ESP+0x14]=this saved @00823C39.
- pair[0] stored over the ARG1 slot @00823C53 (ESP shifted by two PUSHes: net ESP_now_old+0x40) and passed BY ADDRESS (&arg1_slot) to 004D1430.
- FS restore value read from [ESP+0x30] = ESP0-0x0C (FS_old slot) @00823E31.
- TLS: index M32[0x00BA8E6C]; base FS:[0x2C]; flag byte [base+index*4 deref +8] @00823D5C-74 / 00823E11-21.

Epilogue balance (EXACT, both normal paths):
- MOV FS:[0],ECX (restore; no stack change) @00823E44-48
- POP ECX (cookie, 4), POP EDI/ESI/EBP/EBX (0x10) => ESP = ESP0-0x28
- ADD ESP,0x28 => ESP = ESP0 (removes locals 0x1C + SEH pushes 0xC)
- RET 0x10 => pops return + 4 args (callee-clean thiscall)
Balance check: 0x14 (pops) + 0x28 (ADD) = 0x3C = exact frame depth; RET imm 0x10 matches 4 stack args. BALANCE=CONSISTENT byte-exact on all normal paths (00823CAE, 00823DFF, both value paths via 00823E44).

Exceptional exits: SEH unwinding via handler 0xA236F8 (unopened; EAX contract on unwind NOT_ESTABLISHED).
