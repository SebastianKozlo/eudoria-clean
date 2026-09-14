
void FUN_00442190(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                 undefined4 **param_5,int param_6,undefined4 param_7,int *param_8)

{
  int *piVar1;
  allocator<char> *paVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  int aiStack_15c [2];
  undefined auStack_154 [20];
  undefined4 uStack_140;
  undefined auStack_13c [28];
  undefined4 uStack_120;
  undefined4 uStack_11c;
  undefined *puStack_118;
  undefined4 **ppuStack_114;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbStack_110
  ;
  undefined auStack_f4 [3];
  allocator<char> local_f1;
  undefined4 *puStack_f0;
  undefined4 local_ec;
  undefined4 local_dc;
  int *local_d8;
  undefined4 local_c8;
  undefined4 local_c4;
  undefined4 *apuStack_bc [2];
  undefined4 *apuStack_b4 [6];
  undefined local_9c [84];
  undefined auStack_48 [32];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_28 [24];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_0099d671;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_f4;
  ExceptionList = &local_c;
  local_d8 = param_8;
  local_ec = param_2;
  FUN_00843d40();
  local_4 = 0;
  local_c8 = 0;
  local_c4 = 0;
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x44222c;
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)FUN_00973500();
  ppuStack_114 = (undefined4 **)0x0;
  puStack_118 = (undefined *)0xfde;
  uStack_11c = 0x44223d;
  ppuStack_114 = (undefined4 **)FUN_00976770();
  puStack_118 = (undefined *)0x0;
  uStack_11c = param_7;
  uStack_120 = 0x442254;
  FUN_007260e0();
  local_4._0_1_ = 1;
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x44226d;
  FUN_00845ec0();
  FUN_00730f60();
  FUN_004123d0();
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x442289;
  FUN_00853a50();
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x442293;
  FUN_00730fd0();
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x44229d;
  FUN_00730f90();
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x4422a7;
  FUN_00730fb0();
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x4422b5;
  FUN_00797280();
  paVar2 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_f1);
  local_4._0_1_ = 2;
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x4422d5;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_28,paVar2);
  local_4 = CONCAT31(local_4._1_3_,4);
  stlp_std::allocator<char>::~allocator<char>(&local_f1);
  pbStack_110 = abStack_28;
  puStack_118 = local_9c;
  ppuStack_114 = (undefined4 **)0x1;
  uStack_11c = 0x442303;
  FUN_004c46c0();
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)0x442311;
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)FUN_004123d0();
  ppuStack_114 = (undefined4 **)0x442317;
  FUN_004154f0();
  ppuStack_114 = (undefined4 **)0x44231e;
  FUN_008553d0();
  puStack_f0 = param_5[1];
  for (puVar5 = *param_5; puVar5 != puStack_f0; puVar5 = puVar5 + 1) {
    pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                   *)0x442339;
    FUN_00843d60();
    local_4 = CONCAT31(local_4._1_3_,5);
    iVar3 = FUN_00525be0();
    if (iVar3 != 0) {
      pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                     *)0x442359;
      FUN_00844050();
      pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                     *)0x442363;
      FUN_00843f00();
    }
    local_4 = CONCAT31(local_4._1_3_,4);
    FUN_008e0110();
  }
  puStack_f0 = aiStack_15c;
  aiStack_15c[0] = 0;
  piVar1 = aiStack_15c;
  if (*local_d8 != 0) {
    aiStack_15c[0] = *local_d8;
    (**(code **)*local_d8)(local_d8 + 2,auStack_154,0);
    piVar1 = puStack_f0;
  }
  puStack_f0 = piVar1;
  local_4._0_1_ = 6;
  uVar4 = FUN_004123d0();
  local_4._0_1_ = 4;
  FUN_0043d730(auStack_13c,FUN_0043bf10,local_dc,uVar4);
  uStack_140 = 0x4423ee;
  FUN_00440bb0();
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)(uint)(param_6 == 0);
  local_4._0_1_ = 7;
  ppuStack_114 = (undefined4 **)local_ec;
  puStack_118 = (undefined *)0x44240f;
  puStack_118 = (undefined *)FUN_004123d0();
  uStack_11c = 0x44241c;
  FUN_006c9840();
  local_ec = CONCAT31(local_ec._1_3_,param_6 != 0);
  pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)apuStack_bc;
  ppuStack_114 = param_5;
  puStack_118 = auStack_48;
  local_4._0_1_ = 8;
  uStack_11c = 0x442447;
  FUN_00441910();
  FUN_004123d0();
  local_4._0_1_ = 7;
  FUN_0070f860();
  local_4._0_1_ = 4;
  if (apuStack_bc[0] != (undefined4 *)0x0) {
    if ((code *)*apuStack_bc[0] != (code *)0x0) {
      ppuStack_114 = apuStack_b4;
      puStack_118 = (undefined *)0x442487;
      pbStack_110 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                     *)ppuStack_114;
      (*(code *)*apuStack_bc[0])();
    }
    apuStack_bc[0] = (undefined4 *)0x0;
  }
  local_4._0_1_ = 1;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(abStack_28)
  ;
  local_4 = (uint)local_4._1_3_ << 8;
  FUN_008e0110();
  local_4 = 0xffffffff;
  FUN_008e0110();
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

