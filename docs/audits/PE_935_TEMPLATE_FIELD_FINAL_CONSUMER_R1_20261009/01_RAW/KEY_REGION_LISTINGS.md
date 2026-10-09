# KEY_REGION_LISTINGS — PE_935_TEMPLATE_FIELD_FINAL_CONSUMER_R1_20261009

Dual-verified listings (own decoder x86dec.py + GNU objdump; F7 gate = 0 disagreements
over all 105 instructions; every call/jump target recomputed from its own opcode bytes).
Annotations are the run's STRUCTURE-level reading of the dual-verified byte stream.

## W-SUBJ FUN_006C3640 (primary subject; body 0x006C3640-0x006C36A8 = 105 B; 47 insns)

  0x006C3640  55               push     ebp                      
  0x006C3641  8b6c2410         mov      ebp, [esp+16]            EBP := arg3 (= [P+0x18]) - loop END
  0x006C3645  57               push     edi                      
  0x006C3646  8b7c2410         mov      edi, [esp+16]            EDI := arg2 (= [P+0x14]) - loop BEGIN/current
  0x006C364A  3bfd             cmp      edi, ebp                 
  0x006C364C  744e             je       0x006C369C               
  0x006C364E  53               push     ebx                      
  0x006C364F  8b5c2420         mov      ebx, [esp+32]            EBX := arg5 (= 0x008BD720) - the indirect call target
  0x006C3653  56               push     esi                      
  0x006C3654  8b742420         mov      esi, [esp+32]            ESI := arg4 (caller-owned vector, = caller param_2)
  0x006C3658  8bcf             mov      ecx, edi                 ECX := current element (thiscall receiver for the callback)
  0x006C365A  ffd3             call     ebx                      CALL EBX - per-element callback dispatch (edge: -> 0x008BD720, CLOSED)
  0x006C365C  8b4e04           mov      ecx, [esi+4]             ECX := vector cursor (arg4+0x4)
  0x006C365F  3b4e08           cmp      ecx, [esi+8]             cursor vs vector end (arg4+0x8)
  0x006C3662  7414             je       0x006C3678               
  0x006C3664  85c9             test     ecx, ecx                 
  0x006C3666  740a             je       0x006C3672               
  0x006C3668  8b10             mov      edx, [eax]               read [EAX] - callback result dword 0
  0x006C366A  8911             mov      [ecx], edx               write [ECX] - pair store dst = cursor (container)
  0x006C366C  8b4004           mov      eax, [eax+4]             read [EAX+4] - callback result dword 1 (EAX overwritten - last-writer-wins)
  0x006C366F  894104           mov      [ecx+4], eax             write [ECX+4] - pair store dst = cursor+4
  0x006C3672  83460408         add      [esi+4], 8               vector cursor += 8 (container advance)
  0x006C3676  eb12             jmp      0x006C368A               
  0x006C3678  6a01             push     1                        
  0x006C367A  6a01             push     1                        
  0x006C367C  8d54241c         lea      edx, [esp+28]            EDX := &arg1 (slot address - growth helper arg3)
  0x006C3680  52               push     edx                      
  0x006C3681  50               push     eax                      push EAX - callback result ptr = growth helper arg2 (8-byte source)
  0x006C3682  51               push     ecx                      
  0x006C3683  8bce             mov      ecx, esi                 
  0x006C3685  e876f7ffff       call     0x006C2E00               CALL 0x006C2E00 - growth append (edge CLOSED; derived callee cleanup 20)
  0x006C368A  83c720           add      edi, 32                  current element += 0x20 (stride)
  0x006C368D  3bfd             cmp      edi, ebp                 
  0x006C368F  75c7             jne      0x006C3658               
  0x006C3691  8b442414         mov      eax, [esp+20]            EAX := arg1 (out slot = &caller param_2 slot)
  0x006C3695  8930             mov      [eax], esi               *arg1 := vector (output store)
  0x006C3697  5e               pop      esi                      
  0x006C3698  5b               pop      ebx                      
  0x006C3699  5f               pop      edi                      
  0x006C369A  5d               pop      ebp                      
  0x006C369B  c3               ret                               
  0x006C369C  8b44240c         mov      eax, [esp+12]            empty path: EAX := arg1
  0x006C36A0  8b4c2418         mov      ecx, [esp+24]            empty path: ECX := arg4 (vector)
  0x006C36A4  5f               pop      edi                      
  0x006C36A5  8908             mov      [eax], ecx               empty path: *arg1 := vector
  0x006C36A7  5d               pop      ebp                      
  0x006C36A8  c3               ret                               

## W-CALLER FUN_006C3F50 (anchor caller; body 0x006C3F50-0x006C3FDB = 140 B; 54 insns)

  0x006C3F50  83ec08           sub      esp, 8                   
  0x006C3F53  8b44240c         mov      eax, [esp+12]            EAX := param_1 (id; pushed @3F5A as lookup key)
  0x006C3F57  53               push     ebx                      
  0x006C3F58  56               push     esi                      
  0x006C3F59  57               push     edi                      
  0x006C3F5A  50               push     eax                      
  0x006C3F5B  e8f065d7ff       call     0x0043A550               getter call (edge; body CLOSED; never reads its stack arg - predecessor fact)
  0x006C3F60  8bc8             mov      ecx, eax                 
  0x006C3F62  e819b60600       call     0x0072F580               lookup call (edge; body CLOSED; RET 0x4 consumes the key - inherited context)
  0x006C3F67  8bf8             mov      edi, eax                 EDI := P (lookup result)
  0x006C3F69  bb66000000       mov      ebx, 0x00000066          EBX := 0x66
  0x006C3F6E  8bcf             mov      ecx, edi                 
  0x006C3F70  895c240c         mov      [esp+12], ebx            LOCAL_A := 0x66
  0x006C3F74  e867a21000       call     0x007CE1E0               getter2 call (W-DEP2; EAX := [P+8])
  0x006C3F79  8b74241c         mov      esi, [esp+28]            ESI := param_2 (the caller-owned vector)
  0x006C3F7D  8b4e04           mov      ecx, [esi+4]             
  0x006C3F80  3b4e08           cmp      ecx, [esi+8]             
  0x006C3F83  89442410         mov      [esp+16], eax            LOCAL_B := [P+8]
  0x006C3F87  740f             je       0x006C3F98               
  0x006C3F89  85c9             test     ecx, ecx                 
  0x006C3F8B  7405             je       0x006C3F92               
  0x006C3F8D  8919             mov      [ecx], ebx               vector insert pair dword 0: 0x66
  0x006C3F8F  894104           mov      [ecx+4], eax             vector insert pair dword 1: [P+8]
  0x006C3F92  83460408         add      [esi+4], 8               vector cursor += 8
  0x006C3F96  eb16             jmp      0x006C3FAE               
  0x006C3F98  6a01             push     1                        
  0x006C3F9A  6a01             push     1                        
  0x006C3F9C  8d542424         lea      edx, [esp+36]            EDX := &param_2 (growth arg3)
  0x006C3FA0  52               push     edx                      
  0x006C3FA1  8d442418         lea      eax, [esp+24]            EAX := &LOCAL_A = 8-byte source {0x66, [P+8]} (growth arg2)
  0x006C3FA5  50               push     eax                      
  0x006C3FA6  51               push     ecx                      
  0x006C3FA7  8bce             mov      ecx, esi                 
  0x006C3FA9  e852eeffff       call     0x006C2E00               growth call (edge CLOSED; derived callee cleanup 20)
  0x006C3FAE  8bcf             mov      ecx, edi                 ECX := P (receiver for interior-pointer thunk)
  0x006C3FB0  bb20d78b00       mov      ebx, 0x008BD720          EBX := 0x008BD720 (arg5 value)
  0x006C3FB5  e8b670d4ff       call     0x0040B070               CALL 0x0040B070 (W-DEP1; EAX := P+0x14 interior pointer)
  0x006C3FBA  8b4c2410         mov      ecx, [esp+16]            ECX := LOCAL_B = [P+8]
  0x006C3FBE  8b5004           mov      edx, [eax+4]             EDX := [EAX+4] = [P+0x18]
  0x006C3FC1  8b00             mov      eax, [eax]               EAX := [EAX] = [P+0x14]
  0x006C3FC3  51               push     ecx                      push ECX -> callee arg6 = [P+8]
  0x006C3FC4  53               push     ebx                      push EBX -> callee arg5 = 0x008BD720
  0x006C3FC5  56               push     esi                      push ESI -> callee arg4 = vector
  0x006C3FC6  52               push     edx                      push EDX -> callee arg3 = [P+0x18]
  0x006C3FC7  50               push     eax                      push EAX -> callee arg2 = [P+0x14]
  0x006C3FC8  8d4c2430         lea      ecx, [esp+48]            ECX := &param_2 slot
  0x006C3FCC  51               push     ecx                      push ECX -> callee arg1 = &caller param_2 slot
  0x006C3FCD  e86ef6ffff       call     0x006C3640               ANCHOR CALL -> FUN_006C3640 (rel32 E8 6E F6 FF FF recomputed = 0x006C3640)
  0x006C3FD2  83c418           add      esp, 24                  ADD ESP,0x18 - cdecl caller cleans 6 args (24 bytes)
  0x006C3FD5  5f               pop      edi                      
  0x006C3FD6  5e               pop      esi                      
  0x006C3FD7  5b               pop      ebx                      
  0x006C3FD8  83c408           add      esp, 8                   
  0x006C3FDB  c3               ret                               

## W-DEP1 FUN_0040B070 (bounded dependency; 4 B)

  0x0040B070  8d4114           lea      eax, [ecx+20]            
  0x0040B073  c3               ret                               

## W-DEP2 FUN_007CE1E0 (bounded dependency; 4 B)

  0x007CE1E0  8b4108           mov      eax, [ecx+8]             
  0x007CE1E3  c3               ret                               

## W-ANCHOR 0x008BD720 (16 B raw DATA read; NO decode per preregistration)

  bytes: 8d4118c3cccccccccccccccccccccccc
  section: .text (file-mapped at 0x4BD720); all_zero = False
  interpretation: quarantined hypothesis ONLY - see ANCHOR_008BD720_CLASSIFICATION.json
