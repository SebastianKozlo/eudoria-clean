
void FUN_00457930(undefined4 *param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                 undefined4 param_5,undefined4 param_6)

{
  char cVar1;
  uint uVar2;
  int iVar3;
  undefined4 uVar4;
  allocator<char> *paVar5;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbVar6;
  undefined auStack_120 [3];
  allocator<char> aStack_11d;
  undefined4 local_11c;
  undefined4 local_118;
  undefined4 local_114;
  undefined4 local_110;
  undefined4 local_10c;
  undefined4 local_108;
  undefined4 local_104;
  undefined4 local_100;
  undefined4 local_fc;
  undefined4 local_f8;
  undefined4 local_f4;
  void *local_f0;
  undefined4 *local_ec [2];
  undefined local_e4 [24];
  undefined4 *local_cc [2];
  undefined auStack_c4 [24];
  undefined4 *local_ac [2];
  undefined auStack_a4 [24];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_8c [124];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_0099fd9f;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_120;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xfffffed0;
  ExceptionList = &local_c;
  local_11c = *param_1;
  local_114 = param_1[2];
  local_118 = param_1[1];
  local_10c = param_1[4];
  local_110 = param_1[3];
  local_100 = param_1[7];
  local_108 = param_1[5];
  local_104 = param_1[6];
  local_f4 = param_1[10];
  local_fc = param_1[8];
  local_f8 = param_1[9];
  iVar3 = FUN_004123d0(uVar2);
  if (iVar3 == 0) {
    uVar4 = FUN_00844ae0(param_1[1]);
    FUN_00853a50(uVar4);
  }
  uVar4 = FUN_004123d0(uVar2);
  FUN_00797280(uVar4);
  local_f0 = operator_new(0x130);
  local_4 = 0;
  if (local_f0 == (void *)0x0) {
    uVar4 = 0;
  }
  else {
    uVar4 = FUN_00733340();
    uVar4 = FUN_006c0d50(param_2,4,uVar4);
  }
  local_ac[0] = (undefined4 *)0x0;
  local_cc[0] = (undefined4 *)0x0;
  local_ec[0] = (undefined4 *)0x0;
  local_4._0_1_ = 3;
  local_4._1_3_ = 0;
  FUN_00456f40(&local_11c,uVar4,param_3,param_5,param_6,param_4,local_ec,1,local_cc,local_ac,0);
  local_4._0_1_ = 2;
  if (local_ec[0] != (undefined4 *)0x0) {
    if ((code *)*local_ec[0] != (code *)0x0) {
      (*(code *)*local_ec[0])(local_e4,local_e4,1);
    }
    local_ec[0] = (undefined4 *)0x0;
  }
  local_4 = CONCAT31(local_4._1_3_,1);
  if (local_cc[0] != (undefined4 *)0x0) {
    if ((code *)*local_cc[0] != (code *)0x0) {
      (*(code *)*local_cc[0])(auStack_c4,auStack_c4,1);
    }
    local_cc[0] = (undefined4 *)0x0;
  }
  local_4 = 0xffffffff;
  if ((local_ac[0] != (undefined4 *)0x0) && ((code *)*local_ac[0] != (code *)0x0)) {
    (*(code *)*local_ac[0])(auStack_a4,auStack_a4,1);
  }
  paVar5 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_11d);
  local_4 = 4;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_8c,"",paVar5);
  pbVar6 = abStack_8c;
  local_4._0_1_ = 5;
  uVar4 = FUN_004123d0(pbVar6);
  FUN_0050a690(uVar4,pbVar6);
  local_4._0_1_ = 7;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(abStack_8c)
  ;
  local_4 = CONCAT31(local_4._1_3_,8);
  stlp_std::allocator<char>::~allocator<char>(&aStack_11d);
  cVar1 = FUN_006c4200();
  if (cVar1 != '\0') {
    uVar4 = 0;
    FUN_004123d0(0);
    FUN_00509190(uVar4);
  }
  FUN_004123d0();
  local_4 = 0xffffffff;
  FUN_0059f0d0();
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

