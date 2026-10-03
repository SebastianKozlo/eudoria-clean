// decompiled FUN_00599D30 (Ghidra 11.2.1, fresh project, sandbox copy of the pinned EXE)
// byte integrity: 01_RAW/RAW_BYTE_PINS.json g1_byte_crosscheck; listing: 01_RAW/G1_FUNCTION_DUMP.json

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_00599d30(int param_1)

{
  undefined **ppuVar1;
  char cVar2;
  int iVar3;
  allocator<char> *paVar4;
  undefined **ppuStack_190;
  undefined **ppuStack_18c;
  undefined **appuStack_188 [6];
  undefined4 uStack_170;
  undefined **ppuStack_16c;
  undefined **local_168;
  undefined **local_164;
  undefined **ppuStack_160;
  undefined **ppuStack_15c;
  undefined **appuStack_158 [7];
  undefined4 uStack_13c;
  undefined4 uStack_138;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbStack_134
  ;
  undefined *local_114;
  int iStack_110;
  allocator<char> aStack_101;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  local_100 [44];
  undefined4 *puStack_d4;
  undefined *apuStack_cc [6];
  undefined4 local_b4;
  undefined4 local_b0;
  undefined4 local_ac;
  undefined4 uStack_a8;
  undefined4 uStack_70;
  undefined4 uStack_6c;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009d2626;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x599d6b;
  FUN_008df310();
  local_b4 = 0;
  local_b0 = 0;
  local_ac = 0;
  pbStack_134 = local_100;
  local_4 = 0;
  uStack_138 = 0x599d94;
  FUN_00414170();
  uStack_138 = 0x599d9b;
  uStack_138 = FUN_00821bb0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x886b6;
  uStack_13c = 0x3c;
  local_114 = (undefined *)&local_168;
  ppuVar1 = (undefined **)(param_1 + 4);
  local_4._0_1_ = 1;
  local_168 = ArkUI::Component::vftable;
  uStack_170 = 0x599dcc;
  ppuStack_16c = ppuVar1;
  FUN_00426800();
  local_168 = ArkUI::WindowImpl<class_ArkUIWindow>::vftable;
  ppuStack_16c = (undefined **)0x599ddd;
  FUN_00904490();
  local_4 = (uint)local_4._1_3_ << 8;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(local_100);
  local_4 = 0xffffffff;
  FUN_00426620();
  iVar3 = FUN_008df1e0();
  if (iVar3 != 0) {
    local_114 = (undefined *)&ppuStack_15c;
    ppuStack_15c = ArkUI::Component::vftable;
    local_164 = (undefined **)0x599e33;
    ppuStack_160 = ppuVar1;
    FUN_00426800();
    ppuStack_15c = ArkUI::WindowImpl<class_ArkUIWindow>::vftable;
    ppuStack_160 = (undefined **)0x599e46;
    FUN_00906f30();
    local_114 = (undefined *)&ppuStack_15c;
    ppuStack_15c = ArkUI::Component::vftable;
    local_164 = (undefined **)0x599e6c;
    ppuStack_160 = ppuVar1;
    FUN_00426800();
    ppuStack_15c = ArkUI::WindowImpl<class_ArkUIWindow>::vftable;
    ppuStack_160 = (undefined **)0x599e7f;
    FUN_00906f30();
  }
  uStack_a8 = 0;
  local_b4 = 0;
  local_b0 = 0;
  local_ac = 0;
  iVar3 = FUN_008df1e0();
  if (iVar3 != 0) {
    cVar2 = FUN_008ed590();
    if (cVar2 == '\0') {
      pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                     *)&local_114;
      uStack_138 = 0x599ecd;
      FUN_008df4e0();
    }
    FUN_008ed540();
    FUN_008edaa0();
  }
  FUN_008eff60();
  local_4 = 2;
  FUN_0045b790();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x599f19;
  FUN_008df310();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&DAT_00ba342c;
  uStack_138 = 0x599f2b;
  FUN_008df3f0();
  paVar4 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_101);
  local_4._0_1_ = 3;
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x599f4d;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)&local_b4,"Steelfish Bold",paVar4);
  local_4._0_1_ = 4;
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x599f65;
  FUN_008eff80();
  local_4._0_1_ = 3;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)&local_b4);
  local_4 = CONCAT31(local_4._1_3_,2);
  stlp_std::allocator<char>::~allocator<char>(&aStack_101);
  FUN_008df590();
  FUN_008f0780();
  FUN_008f0460();
  local_4 = 0xffffffff;
  FUN_008df670();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&DAT_00b7dd58;
  local_114 = (undefined *)&ppuStack_160;
  ppuStack_160 = ArkUI::Component::vftable;
  local_168 = (undefined **)0x599fe2;
  local_164 = ppuVar1;
  FUN_00426800();
  ppuStack_160 = ArkUI::WindowImpl<class_ArkUIWindow>::vftable;
  local_164 = (undefined **)0x599ff5;
  FUN_00905dc0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&DAT_00b7dd70;
  local_114 = (undefined *)&ppuStack_160;
  ppuStack_160 = ArkUI::Component::vftable;
  local_168 = (undefined **)0x59a01d;
  local_164 = ppuVar1;
  FUN_00426800();
  ppuStack_160 = ArkUI::WindowImpl<class_ArkUIWindow>::vftable;
  local_164 = (undefined **)0x59a030;
  FUN_00905dc0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&DAT_00b7dd48;
  uStack_138 = 0x59a043;
  FUN_008df3f0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0xff;
  uStack_138 = 0xff;
  uStack_13c = 0x59a063;
  FUN_00719f70();
  uStack_70 = 0x140;
  uStack_6c = 2;
  FUN_008eff60();
  local_4 = 5;
  FUN_0045b790();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59a0b2;
  FUN_008df310();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&DAT_00b7dd88;
  uStack_138 = 0x59a0c7;
  FUN_008df3f0();
  FUN_008f05a0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x186a0;
  uStack_138 = 0x59a0ed;
  FUN_00409460();
  FUN_00493ac0();
  pbStack_134 = local_100;
  local_4._0_1_ = 6;
  uStack_138 = 0x59a113;
  FUN_00414170();
  uStack_138 = 0x59a11a;
  FUN_00821bb0();
  local_4._0_1_ = 7;
  FUN_008f01c0();
  local_4._0_1_ = 6;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(local_100);
  local_4 = CONCAT31(local_4._1_3_,5);
  FUN_00426620();
  local_4 = 0xffffffff;
  FUN_008df670();
  FUN_008eff60();
  local_4 = 8;
  FUN_0045b790();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59a19e;
  FUN_008df310();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&DAT_00b7dd90;
  uStack_138 = 0x59a1b3;
  FUN_008df3f0();
  FUN_008f05a0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x186a0;
  uStack_138 = 0x59a1d9;
  FUN_00409460();
  FUN_00493ac0();
  pbStack_134 = local_100;
  local_4._0_1_ = 9;
  uStack_138 = 0x59a1ff;
  FUN_00414170();
  uStack_138 = 0x59a206;
  FUN_00821bb0();
  local_4._0_1_ = 10;
  FUN_008f01c0();
  local_4._0_1_ = 9;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(local_100);
  local_4 = CONCAT31(local_4._1_3_,8);
  FUN_00426620();
  local_4 = 0xffffffff;
  FUN_008df670();
  FUN_008eff60();
  local_4 = 0xb;
  FUN_0045b790();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59a28a;
  FUN_008df310();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&DAT_00b7dd98;
  uStack_138 = 0x59a29f;
  FUN_008df3f0();
  FUN_008f05a0();
  local_114 = (undefined *)0x0;
  FUN_0045e1a0();
  pbStack_134 = local_100;
  local_4._0_1_ = 0xc;
  uStack_138 = 0x59a2e3;
  FUN_00414170();
  uStack_138 = 0x59a2ea;
  FUN_00821bb0();
  local_4._0_1_ = 0xd;
  FUN_008f01c0();
  local_4._0_1_ = 0xc;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(local_100);
  local_4 = CONCAT31(local_4._1_3_,0xb);
  FUN_00426620();
  local_4 = 0xffffffff;
  FUN_008df670();
  FUN_0091cfa0();
  local_4 = 0xe;
  FUN_004e3d10();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59a36e;
  FUN_008df310();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&DAT_00b7dda0;
  uStack_138 = 0x59a383;
  FUN_008df3f0();
  ppuStack_160 = (undefined **)(uint)DAT_00ba3419;
  local_114 = (undefined *)&ppuStack_18c;
  ppuStack_18c = ArkUI::Component::vftable;
  ppuStack_190 = ppuVar1;
  FUN_00426800();
  ppuStack_190 = (undefined **)FUN_00597680;
  ppuStack_18c = ArkRepairUI::vftable;
  FUN_00598210(&ppuStack_15c);
  ppuStack_160 = (undefined **)0x59a3de;
  FUN_00599920();
  local_4._0_1_ = 0xf;
  FUN_0091d090();
  local_4._0_1_ = 0xe;
  if ((puStack_d4 != (undefined4 *)0x0) && ((code *)*puStack_d4 != (code *)0x0)) {
    pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                   *)apuStack_cc;
    uStack_138 = 0x59a419;
    (*(code *)*puStack_d4)();
  }
  FUN_008e6fd0();
  local_4._0_1_ = 0x10;
  FUN_004910d0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59a44a;
  FUN_008df310();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&DAT_00b7ddb8;
  uStack_138 = 0x59a45c;
  FUN_008df3f0();
  FUN_008dfcd0();
  FUN_008e7b80();
  local_4._0_1_ = 0x11;
  FUN_008f0780();
  local_4._0_1_ = 0x10;
  FUN_008df670();
  local_164 = (undefined **)FUN_008df6b0();
  local_114 = (undefined *)&ppuStack_190;
  ppuStack_190 = ArkUI::Component::vftable;
  FUN_00426800(ppuVar1);
  ppuStack_190 = ArkRepairUI::vftable;
  FUN_00598300(&ppuStack_160,FUN_005976c0);
  local_164 = (undefined **)0x59a4ff;
  FUN_005999b0();
  local_4._0_1_ = 0x12;
  FUN_008e6ff0();
  local_4._0_1_ = 0x10;
  if ((puStack_d4 != (undefined4 *)0x0) && ((code *)*puStack_d4 != (code *)0x0)) {
    pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                   *)apuStack_cc;
    uStack_138 = 0x59a537;
    (*(code *)*puStack_d4)();
  }
  local_4._0_1_ = 0xe;
  FUN_008df670();
  FUN_008e6fd0();
  local_4._0_1_ = 0x13;
  FUN_004910d0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59a579;
  FUN_008df310();
  iStack_110 = DAT_00b7ddc4 + DAT_00b7ddbc;
  local_114 = (undefined *)(DAT_00b7ddc0 + DAT_00b7ddb8);
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&local_114;
  uStack_138 = 0x59a5ae;
  FUN_008df3f0();
  FUN_008dfcd0();
  FUN_008e7b80();
  local_4._0_1_ = 0x14;
  FUN_008f0780();
  local_4._0_1_ = 0x13;
  FUN_008df670();
  local_164 = (undefined **)FUN_008df6b0();
  local_114 = (undefined *)&ppuStack_190;
  ppuStack_190 = ArkUI::Component::vftable;
  FUN_00426800(ppuVar1);
  ppuStack_190 = ArkRepairUI::vftable;
  FUN_00598300(&ppuStack_160,FUN_005976c0);
  local_164 = (undefined **)0x59a651;
  FUN_005999b0();
  local_4._0_1_ = 0x15;
  FUN_008e6ff0();
  local_4._0_1_ = 0x13;
  if ((puStack_d4 != (undefined4 *)0x0) && ((code *)*puStack_d4 != (code *)0x0)) {
    pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                   *)apuStack_cc;
    uStack_138 = 0x59a689;
    (*(code *)*puStack_d4)();
  }
  local_4._0_1_ = 0xe;
  FUN_008df670();
  FUN_008e6fd0();
  local_4._0_1_ = 0x16;
  FUN_004910d0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59a6cb;
  FUN_008df310();
  iStack_110 = DAT_00b7ddbc + DAT_00b7ddc4 * 2;
  local_114 = (undefined *)(DAT_00b7ddb8 + DAT_00b7ddc0 * 2);
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&local_114;
  uStack_138 = 0x59a702;
  FUN_008df3f0();
  FUN_008dfcd0();
  FUN_008e7b80();
  local_4._0_1_ = 0x17;
  FUN_008f0780();
  local_4._0_1_ = 0x16;
  FUN_008df670();
  local_164 = (undefined **)FUN_008df6b0();
  local_114 = (undefined *)&ppuStack_190;
  ppuStack_190 = ArkUI::Component::vftable;
  FUN_00426800(ppuVar1);
  ppuStack_190 = ArkRepairUI::vftable;
  FUN_00598300(&ppuStack_160,FUN_005976c0);
  local_164 = (undefined **)0x59a7a5;
  FUN_005999b0();
  local_4._0_1_ = 0x18;
  FUN_008e6ff0();
  local_4._0_1_ = 0x16;
  if ((puStack_d4 != (undefined4 *)0x0) && ((code *)*puStack_d4 != (code *)0x0)) {
    pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                   *)apuStack_cc;
    uStack_138 = 0x59a7dd;
    (*(code *)*puStack_d4)();
  }
  local_4._0_1_ = 0xe;
  FUN_008df670();
  FUN_008e6fd0();
  local_4._0_1_ = 0x19;
  FUN_004910d0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59a81f;
  FUN_008df310();
  iStack_110 = DAT_00b7ddc4 * 3 + DAT_00b7ddbc;
  local_114 = (undefined *)(DAT_00b7ddc0 * 3 + DAT_00b7ddb8);
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&local_114;
  uStack_138 = 0x59a859;
  FUN_008df3f0();
  FUN_008dfcd0();
  FUN_008e7b80();
  local_4._0_1_ = 0x1a;
  FUN_008f0780();
  local_4._0_1_ = 0x19;
  FUN_008df670();
  local_164 = (undefined **)FUN_008df6b0();
  local_114 = (undefined *)&ppuStack_190;
  ppuStack_190 = ArkUI::Component::vftable;
  FUN_00426800(ppuVar1);
  ppuStack_190 = ArkRepairUI::vftable;
  FUN_00598300(&ppuStack_160,FUN_005976c0);
  local_164 = (undefined **)0x59a8fc;
  FUN_005999b0();
  local_4._0_1_ = 0x1b;
  FUN_008e6ff0();
  local_4._0_1_ = 0x19;
  if ((puStack_d4 != (undefined4 *)0x0) && ((code *)*puStack_d4 != (code *)0x0)) {
    pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                   *)apuStack_cc;
    uStack_138 = 0x59a934;
    (*(code *)*puStack_d4)();
  }
  local_4._0_1_ = 0xe;
  FUN_008df670();
  FUN_008e6fd0();
  local_4._0_1_ = 0x1c;
  FUN_004910d0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59a976;
  FUN_008df310();
  iStack_110 = DAT_00b7ddbc + DAT_00b7ddc4 * 4;
  local_114 = (undefined *)(DAT_00b7ddb8 + DAT_00b7ddc0 * 4);
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&local_114;
  uStack_138 = 0x59a9ad;
  FUN_008df3f0();
  FUN_008dfcd0();
  FUN_008e7b80();
  local_4._0_1_ = 0x1d;
  FUN_008f0780();
  local_4._0_1_ = 0x1c;
  FUN_008df670();
  local_164 = (undefined **)FUN_008df6b0();
  local_114 = (undefined *)&ppuStack_190;
  ppuStack_190 = ArkUI::Component::vftable;
  FUN_00426800(ppuVar1);
  ppuStack_190 = ArkRepairUI::vftable;
  FUN_00598300(&ppuStack_160,FUN_005976c0);
  local_164 = (undefined **)0x59aa50;
  FUN_005999b0();
  local_4._0_1_ = 0x1e;
  FUN_008e6ff0();
  local_4._0_1_ = 0x1c;
  if ((puStack_d4 != (undefined4 *)0x0) && ((code *)*puStack_d4 != (code *)0x0)) {
    pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                   *)apuStack_cc;
    uStack_138 = 0x59aa88;
    (*(code *)*puStack_d4)();
  }
  local_4._0_1_ = 0xe;
  FUN_008df670();
  FUN_008e6fd0();
  local_4._0_1_ = 0x1f;
  FUN_004910d0();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59aad3;
  FUN_008df310();
  local_114 = (undefined *)(DAT_00b7ddc0 * 5 + DAT_00b7ddb8);
  iStack_110 = DAT_00b7ddc4 * 5 + 0xc + DAT_00b7ddbc;
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)&local_114;
  uStack_138 = 0x59ab12;
  FUN_008df3f0();
  FUN_008dfcd0();
  FUN_008e7b80();
  local_4._0_1_ = 0x20;
  FUN_008f0780();
  local_4._0_1_ = 0x1f;
  FUN_008df670();
  local_114 = (undefined *)appuStack_188;
  appuStack_188[0] = ArkUI::Component::vftable;
  ppuStack_190 = (undefined **)0x59ab81;
  ppuStack_18c = ppuVar1;
  FUN_00426800();
  ppuStack_18c = (undefined **)FUN_00597a10;
  appuStack_188[0] = ArkRepairUI::vftable;
  ppuStack_190 = (undefined **)&ppuStack_15c;
  FUN_00597ac0();
  ppuStack_160 = (undefined **)0x59abad;
  FUN_00599680();
  local_4._0_1_ = 0x21;
  FUN_008e6ff0();
  local_4._0_1_ = 0x1f;
  if (puStack_d4 != (undefined4 *)0x0) {
    if ((code *)*puStack_d4 != (code *)0x0) {
      pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                     *)apuStack_cc;
      uStack_138 = 0x59abe7;
      (*(code *)*puStack_d4)();
    }
    puStack_d4 = (undefined4 *)0x0;
  }
  local_4 = CONCAT31(local_4._1_3_,0xe);
  FUN_008df670();
  FUN_00908df0();
  local_114 = (undefined *)appuStack_158;
  appuStack_158[0] = ArkUI::Component::vftable;
  ppuStack_160 = (undefined **)0x59ac29;
  ppuStack_15c = ppuVar1;
  FUN_00426800();
  appuStack_158[0] = ArkUI::WindowImpl<class_ArkUIWindow>::vftable;
  ppuStack_15c = (undefined **)0x59ac3a;
  FUN_00907670();
  pbStack_134 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x59ac58;
  FUN_0091d040();
  local_4 = 0xffffffff;
  FUN_008df670();
  ExceptionList = local_c;
  return;
}

