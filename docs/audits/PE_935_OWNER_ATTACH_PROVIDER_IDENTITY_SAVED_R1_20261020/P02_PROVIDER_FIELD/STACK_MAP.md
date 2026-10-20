# P02 STACK_MAP (ESP trace)

Entry E0. SUB ESP,0x18 -> frame F. PUSH EBX/EBP/ESI/EDI (4 saves). ARG1=ESI read at [ESP+0x28] (=E+4).
Locals: float L_PI=[0x00A7ADC8] stored via FST [ESP+0xC], FST [ESP+0x18], FSTP [ESP+0x20] (same value, 3 slots, after pushes).
Pointers staged: [ESP+0x10]=EDI+0x24, [ESP+0x18]=EDI+0x20 (overwrite of a float local slot after FST).
CALL 00864360 args (push order ESI, EDI, EDX=&float-locals, ECX=&[ESP+0x1C], EAX=&ptr-pair; 6th slot [ESP+0x34]=EBP=EDI+0x1C written directly). ADD ESP,0x8 after.
Then: PUSH EAX; CALL 0085BD20; ADD ESP,0x8 (x3, chain on EAX). Then byte ops, no net stack change until 0085BE48/0085BE50 path: PUSH EDX, PUSH ESI, CALL 0085BC10, ADD ESP,0x8.
Final: MOV [EDI+0x34],BL; POP EDI/ESI/EBP/EBX; ADD ESP,0x18; RET 0x4 (E to E+4 arg cleaned).
Observed exits: RET 0085BEDB and tail FLDZ at 0085BEDE (window end 0085BEE0; tail body outside window, not admitted).
ESP balanced on RET path; no leak observed on listed rows; FPU: 3 FST/FSTP of one FLD, FCHS groups balanced FLD/FSTP pairs, FLDZ at tail - depth 0 at RET path within window.
Callee bodies 00864360/0085BD20/0040DE60/0085BC10 NOT opened; ESP-clean assumptions about them are NOT made; the ADD ESP,0x8 cleanups listed are caller-side facts only.
