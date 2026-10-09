# KEY REGION LISTINGS — own decoder (dual-verified vs GNU objdump 2.44; F8 gate 0 disagreements)
# Every line: VA, opcode bytes, mnemonic, operands. <CALL->target> / <JMP->target COND> annotations.
# Evidence class: BYTE_OBSERVATION (own decoder primary; objdump independent agreement in 01_RAW/OBJDUMP_LISTINGS/).

## W_A prologue (SEH frame, param loads)
0x511070  6A FF                      PUSH 0xffffffff
0x511072  68 5B BE 9B 00             PUSH 0x9bbe5b
0x511077  64 A1 00 00 00 00          MOV EAX, FS:[0x0]
0x51107d  50                         PUSH EAX
0x51107e  81 EC 44 01 00 00          SUB ESP, 0x144
0x511084  53                         PUSH EBX
0x511085  55                         PUSH EBP
0x511086  56                         PUSH ESI
0x511087  57                         PUSH EDI
0x511088  A1 D0 D8 B9 00             MOV EAX, [0xB9D8D0]
0x51108d  33 C4                      XOR EAX, ESP
0x51108f  50                         PUSH EAX
0x511090  8D 84 24 58 01 00 00       LEA EAX, [ESP+0x158]
0x511097  64 A3 00 00 00 00          MOV FS:[0x0], EAX
0x51109d  8B B4 24 68 01 00 00       MOV ESI, [ESP+0x168]

## W_A second FUN_007CE1E0 use @0x0051115B (receiver = FUN_0041B3A0 result, NOT template)
0x511141  84 C0                      TEST AL, AL
0x511143  8B CE                      MOV ECX, ESI
0x511145  0F 84 F8 01 00 00          JE 0x511343 <JMP->0x511343 JE
0x51114b  E8 10 33 33 00             CALL 0x844460 <CALL->0x844460
0x511150  84 C0                      TEST AL, AL
0x511152  74 1D                      JE 0x511171 <JMP->0x511171 JE
0x511154  E8 47 A2 F0 FF             CALL 0x41b3a0 <CALL->0x41b3a0
0x511159  8B C8                      MOV ECX, EAX
0x51115b  E8 80 D0 2B 00             CALL 0x7ce1e0 <CALL->0x7ce1e0
0x511160  8B CE                      MOV ECX, ESI
0x511162  8B D8                      MOV EBX, EAX
0x511164  E8 67 12 F0 FF             CALL 0x4123d0 <CALL->0x4123d0
0x511169  3B D8                      CMP EBX, EAX
0x51116b  0F 85 03 01 00 00          JNE 0x511274 <JMP->0x511274 JNE
0x511171  68 86 15 00 00             PUSH 0x1586

## W_A id selection + lookup chain + subject CALL @0x00511259
0x5111a0  E8 2B 2C 33 00             CALL 0x843dd0 <CALL->0x843dd0
0x5111a5  8B 08                      MOV ECX, [EAX]
0x5111a7  51                         PUSH ECX
0x5111a8  8B CE                      MOV ECX, ESI
0x5111aa  E8 21 12 F0 FF             CALL 0x4123d0 <CALL->0x4123d0
0x5111af  50                         PUSH EAX
0x5111b0  8D 8C 24 B0 00 00 00       LEA ECX, [ESP+0xB0]
0x5111b7  E8 24 88 20 00             CALL 0x7199e0 <CALL->0x7199e0
0x5111bc  50                         PUSH EAX
0x5111bd  8D 8C 24 B4 00 00 00       LEA ECX, [ESP+0xB4]
0x5111c4  E8 57 98 1A 00             CALL 0x6baa20 <CALL->0x6baa20
0x5111c9  8D 8C 24 B0 00 00 00       LEA ECX, [ESP+0xB0]
0x5111d0  C6 84 24 60 01 00 00 03    MOV [ESP+0x160], 0x3
0x5111d8  E8 03 94 1A 00             CALL 0x6ba5e0 <CALL->0x6ba5e0
0x5111dd  84 C0                      TEST AL, AL
0x5111df  75 19                      JNE 0x5111fa <JMP->0x5111fa JNE
0x5111e1  8D 8C 24 B0 00 00 00       LEA ECX, [ESP+0xB0]
0x5111e8  C6 84 24 60 01 00 00 02    MOV [ESP+0x160], 0x2
0x5111f0  E8 1B EF 3C 00             CALL 0x8e0110 <CALL->0x8e0110
0x5111f5  E9 DF 02 00 00             JMP 0x5114d9 <JMP->0x5114d9 None
0x5111fa  6A 04                      PUSH 0x4
0x5111fc  E8 0F 96 1D 00             CALL 0x6ea810 <CALL->0x6ea810
0x511201  83 C4 04                   ADD ESP, 0x4
0x511204  50                         PUSH EAX
0x511205  8D 8C 24 B4 00 00 00       LEA ECX, [ESP+0xB4]
0x51120c  E8 8F 9B F7 FF             CALL 0x48ada0 <CALL->0x48ada0
0x511211  8B C8                      MOV ECX, EAX
0x511213  E8 08 6A 22 00             CALL 0x737c20 <CALL->0x737c20
0x511218  84 C0                      TEST AL, AL
0x51121a  74 07                      JE 0x511223 <JMP->0x511223 JE
0x51121c  B8 FA 2D 00 00             MOV EAX, 0x2dfa
0x511221  EB 27                      JMP 0x51124a <JMP->0x51124a None
0x511223  6A 09                      PUSH 0x9
0x511225  E8 E6 95 1D 00             CALL 0x6ea810 <CALL->0x6ea810
0x51122a  83 C4 04                   ADD ESP, 0x4
0x51122d  50                         PUSH EAX
0x51122e  8D 8C 24 B4 00 00 00       LEA ECX, [ESP+0xB4]
0x511235  E8 66 9B F7 FF             CALL 0x48ada0 <CALL->0x48ada0
0x51123a  8B C8                      MOV ECX, EAX
0x51123c  E8 DF 69 22 00             CALL 0x737c20 <CALL->0x737c20
0x511241  84 C0                      TEST AL, AL
0x511243  74 1B                      JE 0x511260 <JMP->0x511260 JE
0x511245  B8 F9 2D 00 00             MOV EAX, 0x2df9
0x51124a  50                         PUSH EAX
0x51124b  E8 00 93 F2 FF             CALL 0x43a550 <CALL->0x43a550
0x511250  8B C8                      MOV ECX, EAX
0x511252  E8 29 E3 21 00             CALL 0x72f580 <CALL->0x72f580
0x511257  8B C8                      MOV ECX, EAX
0x511259  E8 82 CF 2B 00             CALL 0x7ce1e0 <CALL->0x7ce1e0
0x51125e  8B F8                      MOV EDI, EAX
0x511260  8D 8C 24 B0 00 00 00       LEA ECX, [ESP+0xB0]

## W_A [P+8] forwards region 1 (CALL 0x00414670 args)
0x511260  8D 8C 24 B0 00 00 00       LEA ECX, [ESP+0xB0]
0x511267  C6 84 24 60 01 00 00 02    MOV [ESP+0x160], 0x2
0x51126f  E8 9C EE 3C 00             CALL 0x8e0110 <CALL->0x8e0110
0x511274  8B 5D 04                   MOV EBX, [EBP+0x4]
0x511277  85 DB                      TEST EBX, EBX
0x511279  75 17                      JNE 0x511292 <JMP->0x511292 JNE
0x51127b  8D 54 24 14                LEA EDX, [ESP+0x14]
0x51127f  52                         PUSH EDX
0x511280  8B CE                      MOV ECX, ESI
0x511282  E8 49 2B 33 00             CALL 0x843dd0 <CALL->0x843dd0
0x511287  50                         PUSH EAX
0x511288  E8 63 7F 21 00             CALL 0x7291f0 <CALL->0x7291f0
0x51128d  83 C4 04                   ADD ESP, 0x4
0x511290  8B D8                      MOV EBX, EAX
0x511292  53                         PUSH EBX
0x511293  57                         PUSH EDI
0x511294  8B CE                      MOV ECX, ESI
0x511296  E8 35 11 F0 FF             CALL 0x4123d0 <CALL->0x4123d0
0x51129b  50                         PUSH EAX
0x51129c  E8 CF 33 F0 FF             CALL 0x414670 <CALL->0x414670

## W_A [P+8] forwards region 2 (CALL 0x00414670 args)
0x5112db  0F B6 0D E4 2C BA 00       MOVZX ECX, [0xBA2CE4]
0x5112e2  51                         PUSH ECX
0x5112e3  53                         PUSH EBX
0x5112e4  57                         PUSH EDI
0x5112e5  8D 4C 24 44                LEA ECX, [ESP+0x44]
0x5112e9  E8 E2 10 F0 FF             CALL 0x4123d0 <CALL->0x4123d0
0x5112ee  50                         PUSH EAX
0x5112ef  8B CE                      MOV ECX, ESI
0x5112f1  E8 DA 10 F0 FF             CALL 0x4123d0 <CALL->0x4123d0
0x5112f6  50                         PUSH EAX
0x5112f7  E8 74 33 F0 FF             CALL 0x414670 <CALL->0x414670

## W_A EDI zeroed @0x00511133F (liveness end of [P+8]) + redefinition @0x0051113B4
0x51133a  E8 81 CD FF FF             CALL 0x50e0c0 <CALL->0x50e0c0
0x51133f  33 FF                      XOR EDI, EDI
0x511341  EB 3E                      JMP 0x511381 <JMP->0x511381 None
0x511343  68 91 01 00 00             PUSH 0x191
0x511348  E8 D3 2C 33 00             CALL 0x844020 <CALL->0x844020
0x51134d  84 C0                      TEST AL, AL
0x51134f  75 30                      JNE 0x511381 <JMP->0x511381 JNE
0x511351  38 45 00                   CMP [EBP], AL
0x511354  74 2B                      JE 0x511381 <JMP->0x511381 JE
0x511356  8D 4C 24 38                LEA ECX, [ESP+0x38]
0x51135a  E8 F1 51 23 00             CALL 0x746550 <CALL->0x746550
0x51135f  85 C0                      TEST EAX, EAX
0x511361  74 1E                      JE 0x511381 <JMP->0x511381 JE
0x511363  8D 4C 24 38                LEA ECX, [ESP+0x38]
0x511367  E8 E4 51 23 00             CALL 0x746550 <CALL->0x746550
0x51136c  50                         PUSH EAX
0x51136d  8B CE                      MOV ECX, ESI
0x51136f  E8 5C 10 F0 FF             CALL 0x4123d0 <CALL->0x4123d0
0x511374  50                         PUSH EAX
0x511375  E8 76 41 F0 FF             CALL 0x4154f0 <CALL->0x4154f0
0x51137a  8B C8                      MOV ECX, EAX
0x51137c  E8 4F 40 34 00             CALL 0x8553d0 <CALL->0x8553d0
0x511381  68 30 01 00 00             PUSH 0x130
0x511386  E8 39 C0 44 00             CALL 0x95d3c4 <CALL->0x95d3c4
0x51138b  83 C4 04                   ADD ESP, 0x4
0x51138e  89 44 24 14                MOV [ESP+0x14], EAX
0x511392  3B C7                      CMP EAX, EDI
0x511394  C6 84 24 60 01 00 00 04    MOV [ESP+0x160], 0x4
0x51139c  74 18                      JE 0x5113b6 <JMP->0x5113b6 JE
0x51139e  8D 8C 24 10 01 00 00       LEA ECX, [ESP+0x110]
0x5113a5  51                         PUSH ECX
0x5113a6  6A 04                      PUSH 0x4
0x5113a8  8D 54 24 40                LEA EDX, [ESP+0x40]
0x5113ac  52                         PUSH EDX
0x5113ad  8B C8                      MOV ECX, EAX
0x5113af  E8 9C F9 1A 00             CALL 0x6c0d50 <CALL->0x6c0d50
0x5113b4  8B F8                      MOV EDI, EAX
0x5113b6  8B CE                      MOV ECX, ESI
0x5113b8  C6 84 24 60 01 00 00 02    MOV [ESP+0x160], 0x2
0x5113c0  E8 1B 48 01 00             CALL 0x525be0 <CALL->0x525be0
0x5113c5  8B CE                      MOV ECX, ESI
0x5113c7  8B D8                      MOV EBX, EAX

## W_B full body (both subject CALLs + Phase-3 reads)
0x6c3f50  83 EC 08                   SUB ESP, 0x8
0x6c3f53  8B 44 24 0C                MOV EAX, [ESP+0xC]
0x6c3f57  53                         PUSH EBX
0x6c3f58  56                         PUSH ESI
0x6c3f59  57                         PUSH EDI
0x6c3f5a  50                         PUSH EAX
0x6c3f5b  E8 F0 65 D7 FF             CALL 0x43a550 <CALL->0x43a550
0x6c3f60  8B C8                      MOV ECX, EAX
0x6c3f62  E8 19 B6 06 00             CALL 0x72f580 <CALL->0x72f580
0x6c3f67  8B F8                      MOV EDI, EAX
0x6c3f69  BB 66 00 00 00             MOV EBX, 0x66
0x6c3f6e  8B CF                      MOV ECX, EDI
0x6c3f70  89 5C 24 0C                MOV [ESP+0xC], EBX
0x6c3f74  E8 67 A2 10 00             CALL 0x7ce1e0 <CALL->0x7ce1e0
0x6c3f79  8B 74 24 1C                MOV ESI, [ESP+0x1C]
0x6c3f7d  8B 4E 04                   MOV ECX, [ESI+0x4]
0x6c3f80  3B 4E 08                   CMP ECX, [ESI+0x8]
0x6c3f83  89 44 24 10                MOV [ESP+0x10], EAX
0x6c3f87  74 0F                      JE 0x6c3f98 <JMP->0x6c3f98 JE
0x6c3f89  85 C9                      TEST ECX, ECX
0x6c3f8b  74 05                      JE 0x6c3f92 <JMP->0x6c3f92 JE
0x6c3f8d  89 19                      MOV [ECX], EBX
0x6c3f8f  89 41 04                   MOV [ECX+0x4], EAX
0x6c3f92  83 46 04 08                ADD [ESI+0x4], 0x8
0x6c3f96  EB 16                      JMP 0x6c3fae <JMP->0x6c3fae None
0x6c3f98  6A 01                      PUSH 0x1
0x6c3f9a  6A 01                      PUSH 0x1
0x6c3f9c  8D 54 24 24                LEA EDX, [ESP+0x24]
0x6c3fa0  52                         PUSH EDX
0x6c3fa1  8D 44 24 18                LEA EAX, [ESP+0x18]
0x6c3fa5  50                         PUSH EAX
0x6c3fa6  51                         PUSH ECX
0x6c3fa7  8B CE                      MOV ECX, ESI
0x6c3fa9  E8 52 EE FF FF             CALL 0x6c2e00 <CALL->0x6c2e00
0x6c3fae  8B CF                      MOV ECX, EDI
0x6c3fb0  BB 20 D7 8B 00             MOV EBX, 0x8bd720
0x6c3fb5  E8 B6 70 D4 FF             CALL 0x40b070 <CALL->0x40b070
0x6c3fba  8B 4C 24 10                MOV ECX, [ESP+0x10]
0x6c3fbe  8B 50 04                   MOV EDX, [EAX+0x4]
0x6c3fc1  8B 00                      MOV EAX, [EAX]
0x6c3fc3  51                         PUSH ECX
0x6c3fc4  53                         PUSH EBX
0x6c3fc5  56                         PUSH ESI
0x6c3fc6  52                         PUSH EDX
0x6c3fc7  50                         PUSH EAX
0x6c3fc8  8D 4C 24 30                LEA ECX, [ESP+0x30]
0x6c3fcc  51                         PUSH ECX
0x6c3fcd  E8 6E F6 FF FF             CALL 0x6c3640 <CALL->0x6c3640
0x6c3fd2  83 C4 18                   ADD ESP, 0x18
0x6c3fd5  5F                         POP EDI
0x6c3fd6  5E                         POP ESI
0x6c3fd7  5B                         POP EBX
0x6c3fd8  83 C4 08                   ADD ESP, 0x8
0x6c3fdb  C3                         RET  <RET>

## W_B post-body raw context: adjacent function 0x006C3FE0 calls FUN_006C3F50 cdecl(2 args) in a loop
0x6c3fe0  53                         PUSH EBX
0x6c3fe1  8B 5C 24 0C                MOV EBX, [ESP+0xC]
0x6c3fe5  55                         PUSH EBP
0x6c3fe6  56                         PUSH ESI
0x6c3fe7  8B 74 24 10                MOV ESI, [ESP+0x10]
0x6c3feb  57                         PUSH EDI
0x6c3fec  BD 02 00 00 00             MOV EBP, 0x2
0x6c3ff1  8D 7E 10                   LEA EDI, [ESI+0x10]
0x6c3ff4  3B F7                      CMP ESI, EDI
0x6c3ff6  74 13                      JE 0x6c400b <JMP->0x6c400b JE
0x6c3ff8  8B 06                      MOV EAX, [ESI]
0x6c3ffa  53                         PUSH EBX
0x6c3ffb  50                         PUSH EAX
0x6c3ffc  E8 4F FF FF FF             CALL 0x6c3f50 <CALL->0x6c3f50
0x6c4001  83 C6 04                   ADD ESI, 0x4
0x6c4004  83 C4 08                   ADD ESP, 0x8
0x6c4007  3B F7                      CMP ESI, EDI
0x6c4009  75 ED                      JNE 0x6c3ff8 <JMP->0x6c3ff8 JNE
0x6c400b  83 ED 01                   SUB EBP, 0x1
0x6c400e  8B F7                      MOV ESI, EDI
0x6c4010  75 DF                      JNE 0x6c3ff1 <JMP->0x6c3ff1 JNE
0x6c4012  5F                         POP EDI
0x6c4013  5E                         POP ESI
0x6c4014  5D                         POP EBP
0x6c4015  5B                         POP EBX
0x6c4016  C3                         RET  <RET>

## W_C full body (primary subject 1)
0x7ce1e0  8B 41 08                   MOV EAX, [ECX+0x8]
0x7ce1e3  C3                         RET  <RET>

## W_D full body (primary subject 2)
0x40b070  8D 41 14                   LEA EAX, [ECX+0x14]
0x40b073  C3                         RET  <RET>

## W_E1 full body (lookup anchor)
0x72f580  51                         PUSH ECX
0x72f581  56                         PUSH ESI
0x72f582  8B F1                      MOV ESI, ECX
0x72f584  8D 44 24 0C                LEA EAX, [ESP+0xC]
0x72f588  50                         PUSH EAX
0x72f589  8D 4C 24 08                LEA ECX, [ESP+0x8]
0x72f58d  51                         PUSH ECX
0x72f58e  8B CE                      MOV ECX, ESI
0x72f590  E8 9B 1E DA FF             CALL 0x4d1430 <CALL->0x4d1430
0x72f595  8B 44 24 04                MOV EAX, [ESP+0x4]
0x72f599  3B C6                      CMP EAX, ESI
0x72f59b  5E                         POP ESI
0x72f59c  74 07                      JE 0x72f5a5 <JMP->0x72f5a5 JE
0x72f59e  83 C0 14                   ADD EAX, 0x14
0x72f5a1  59                         POP ECX
0x72f5a2  C2 04 00                   RET 0x4 <RET>
0x72f5a5  B8 00 58 BA 00             MOV EAX, 0xba5800
0x72f5aa  59                         POP ECX
0x72f5ab  C2 04 00                   RET 0x4 <RET>

## W_E2 full body (getter anchor)
0x43a550  6A FF                      PUSH 0xffffffff
0x43a552  68 8B C6 99 00             PUSH 0x99c68b
0x43a557  64 A1 00 00 00 00          MOV EAX, FS:[0x0]
0x43a55d  50                         PUSH EAX
0x43a55e  51                         PUSH ECX
0x43a55f  A1 D0 D8 B9 00             MOV EAX, [0xB9D8D0]
0x43a564  33 C4                      XOR EAX, ESP
0x43a566  50                         PUSH EAX
0x43a567  8D 44 24 08                LEA EAX, [ESP+0x8]
0x43a56b  64 A3 00 00 00 00          MOV FS:[0x0], EAX
0x43a571  A1 24 18 BA 00             MOV EAX, [0xBA1824]
0x43a576  85 C0                      TEST EAX, EAX
0x43a578  75 3D                      JNE 0x43a5b7 <JMP->0x43a5b7 JNE
0x43a57a  6A 18                      PUSH 0x18
0x43a57c  E8 43 2E 52 00             CALL 0x95d3c4 <CALL->0x95d3c4
0x43a581  83 C4 04                   ADD ESP, 0x4
0x43a584  89 44 24 04                MOV [ESP+0x4], EAX
0x43a588  85 C0                      TEST EAX, EAX
0x43a58a  C7 44 24 10 00 00 00 00    MOV [ESP+0x10], 0x0
0x43a592  74 1C                      JE 0x43a5b0 <JMP->0x43a5b0 JE
0x43a594  8B C8                      MOV ECX, EAX
0x43a596  E8 C5 FC 0E 00             CALL 0x52a260 <CALL->0x52a260
0x43a59b  A3 24 18 BA 00             MOV [0xBA1824], EAX
0x43a5a0  8B 4C 24 08                MOV ECX, [ESP+0x8]
0x43a5a4  64 89 0D 00 00 00 00       MOV FS:[0x0], ECX
0x43a5ab  59                         POP ECX
0x43a5ac  83 C4 10                   ADD ESP, 0x10
0x43a5af  C3                         RET  <RET>
0x43a5b0  33 C0                      XOR EAX, EAX
0x43a5b2  A3 24 18 BA 00             MOV [0xBA1824], EAX
0x43a5b7  8B 4C 24 08                MOV ECX, [ESP+0x8]
0x43a5bb  64 89 0D 00 00 00 00       MOV FS:[0x0], ECX
0x43a5c2  59                         POP ECX
0x43a5c3  83 C4 10                   ADD ESP, 0x10
0x43a5c6  C3                         RET  <RET>
