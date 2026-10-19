# STACK_MAP - 0085BFA0 (ESP0 = entry ESP; [ESP0]=ret, [ESP0+4]=out-pointer)

SUB ESP,0xA0 => locals 0xA0. PUSH ESI (-4), PUSH EDI (-4). ESP_now = ESP0-0xA8.
Out-pointer arg read at [ESP+0xAC] @0085C06A = ESP0-0xA8+0xAC = ESP0+4 = arg slot. CONFIRMED single stack arg (RET 0x4).
Virtual call @0085BFB5: after PUSH ESI,EDI,EDX: [ESP]=ret,[ESP+4]=EDX(&local buffer @pre-push ESP+0x78 => one stack arg to the virtual), ECX=this2. Callee-clean assumption NOT needed (no visible ADD ESP; cleanup inside callees unopened - flagged as premise).
Epilogue: POP EDI, POP ESI, ADD ESP,0xA0, RET 0x4 => restores 0x8+0xA0 = 0xA8 = exact frame depth. BALANCE=CONSISTENT.
0085C0C0: SUB ESP,0xC; LEA EDX,[ESP]; PUSH EDX (arg=&3-float local); CALL EAX; copies to ECX=[ESP+0x10] (= out arg); ADD ESP,0xC; RET 0x4. BALANCE=CONSISTENT.
