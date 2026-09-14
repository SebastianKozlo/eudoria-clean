// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x567170L (requested via site 0x567662)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00567170(undefined4 param_1,undefined4 param_2,undefined4 param_3,float param_4,
                 undefined4 param_5)

{
  char cVar1;
  uint uVar2;
  undefined4 *puVar3;
  allocator<char> *paVar4;
  int iVar5;
  float *pfVar6;
  int iVar7;
  undefined4 uVar8;
  float10 fVar9;
  undefined *puVar10;
  undefined *puVar11;
  undefined4 uVar12;
  code **ppcVar13;
  undefined4 uVar14;
  float fVar15;
  undefined auStack_134 [4];
  undefined4 local_130;
  allocator<char> local_12a;
  char local_129;
  float local_128 [2];
  float local_120;
  undefined local_11c [4];
  undefined local_118 [4];
  undefined4 local_114;
  undefined local_110 [8];
  int local_108;
  code *local_100;
  undefined4 uStack_fc;
  undefined4 uStack_f8;
  float fStack_f4;
  undefined4 local_e4;
  undefined4 local_e0;
  undefined local_dc [4];
  undefined4 *puStack_d8;
  undefined auStack_d0 [24];
  undefined4 uStack_b8;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_ac [24];
  undefined local_94 [44];
  undefined local_68 [76];
  uint local_1c;
  void *local_14;
  undefined *puStack_10;
  int local_c;
  
  local_c = 0xffffffff;
  puStack_10 = &LAB_009c9d81;
  local_14 = ExceptionList;
  local_1c = DAT_00b9d8d0 ^ (uint)auStack_134;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xfffffec0;
  ExceptionList = &local_14;
  local_120 = param_4;
  FUN_00843dd0(local_11c);
  local_130 = 1.0;
  uVar8 = 0x3bdb;
  FUN_0040bfe0(200,0,2);
  local_114 = 0;
  puVar3 = (undefined4 *)FUN_00843dd0(local_dc);
  local_e0 = *puVar3;
  local_e4 = 0x4e31;
  FUN_00703b80(&local_e4);
  local_c = 0;
  if (local_108 != 0) {
    local_114 = FUN_00727ed0(uVar2);
  }
  uVar12 = local_114;
  FUN_00719f70(0x3c,0x46,0xfa,0xff);
  local_129 = '\0';
  cVar1 = FUN_009768d0(0x180b);
  if (cVar1 == '\0') {
    cVar1 = FUN_00729de0(local_11c);
    if (cVar1 != '\0') {
      local_130 = (float)FUN_00729450(local_11c);
      cVar1 = FUN_00728aa0(local_11c);
      if (cVar1 == '\0') {
        cVar1 = FUN_00728ab0(local_11c);
        if (cVar1 == '\0') goto LAB_00567725;
        uVar8 = 0x3a47;
        local_130 = (float)(int)local_130 * (float)_DAT_00a7af80 + (float)_DAT_00a79a08;
        goto LAB_00567277;
      }
      uVar14 = 2;
      uVar8 = 0x3a40;
      uVar12 = 0x5dc;
      local_130 = (float)(int)local_130 * (float)_DAT_00a7b500 + (float)_DAT_00a79a08;
      goto LAB_0056727d;
    }
    switch(uVar12) {
    case 0:
    case 3:
      local_130 = _DAT_00a7af9c;
      break;
    case 1:
      local_130 = _DAT_00a7fa24;
      break;
    case 2:
      local_130 = _DAT_00a7d688;
      uVar8 = 0x3bda;
      uVar12 = FUN_0040bfe0(2,0,3);
      FUN_0040bd20(uVar12);
      local_129 = '\x01';
    }
  }
  else {
    uVar8 = 0x3bd9;
    local_130 = _DAT_00a7b128;
LAB_00567277:
    uVar14 = 3;
    uVar12 = 2;
LAB_0056727d:
    uVar12 = FUN_0040bfe0(uVar12,0,uVar14);
    FUN_0040bd20(uVar12);
  }
  uVar12 = uVar8;
  FUN_0043a550(uVar8);
  uVar12 = FUN_0072f580(uVar12);
  FUN_005670a0(uVar12);
  local_c._0_1_ = 1;
  FUN_00730f60();
  FUN_00730f90(param_3);
  uVar12 = FUN_0096c630(&local_100,local_120);
  FUN_00730fb0(uVar12);
  FUN_00797280(uVar8);
  paVar4 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_12a);
  local_c._0_1_ = 2;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)&local_100,"",paVar4);
  uVar14 = 1;
  uVar12 = 1;
  ppcVar13 = &local_100;
  uVar8 = 2;
  puVar11 = local_68;
  puVar10 = local_94;
  local_c._0_1_ = 3;
  FUN_004148f0(puVar10,puVar11,2,ppcVar13,1,1);
  iVar5 = FUN_00457930(puVar10,puVar11,uVar8,ppcVar13,uVar12,uVar14);
  local_c._0_1_ = 2;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)&local_100);
  stlp_std::allocator<char>::~allocator<char>(&local_12a);
  if (iVar5 != 0) {
    paVar4 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_12a);
    local_c._0_1_ = 4;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (abStack_ac,"",paVar4);
    local_c._0_1_ = 5;
    FUN_0050a690(iVar5,abStack_ac);
    local_c._0_1_ = 7;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (abStack_ac);
    local_c = CONCAT31(local_c._1_3_,8);
    stlp_std::allocator<char>::~allocator<char>(&local_12a);
    cVar1 = FUN_006c4200();
    if (cVar1 != '\0') {
      fVar15 = local_130;
      FUN_004123d0(local_130);
      FUN_00509570(fVar15);
      if (local_129 != '\0') {
        FUN_00719f90(local_118);
        local_120 = (float)((uint)local_130 & 0xff);
        local_128[0] = 3.57331e-43;
        local_120 = (float)FUN_0095da40();
        pfVar6 = local_128;
        if ((int)local_120 < 0x100) {
          pfVar6 = &local_120;
        }
        local_128[0] = (float)((uint)local_130 >> 8 & 0xff);
        local_130 = (float)CONCAT31(local_130._1_3_,*(undefined *)pfVar6);
        local_120 = 3.57331e-43;
        local_128[0] = (float)FUN_0095da40();
        pfVar6 = &local_120;
        if ((int)local_128[0] < 0x100) {
          pfVar6 = local_128;
        }
        local_128[0] = (float)((uint)local_130 >> 0x10 & 0xff);
        local_130._0_2_ = CONCAT11(*(undefined *)pfVar6,(undefined)local_130);
        local_120 = 3.57331e-43;
        local_128[0] = (float)FUN_0095da40();
        pfVar6 = &local_120;
        if ((int)local_128[0] < 0x100) {
          pfVar6 = local_128;
        }
        local_130._0_3_ = CONCAT12(*(undefined *)pfVar6,(undefined2)local_130);
        FUN_0050acc0(&local_130,local_118,local_118);
      }
      iVar7 = FUN_0050a860();
      if (iVar7 != 0) {
        iVar7 = FUN_00401360();
        fVar15 = *(float *)(iVar7 + 100);
        uVar8 = 1;
        local_128[0] = fVar15;
        FUN_0050a860(1,fVar15);
        FUN_006d0990(uVar8,fVar15);
        iVar7 = FUN_00401360();
        local_128[0] = *(float *)(iVar7 + 100);
        fVar9 = (float10)FUN_0040bdc0(3);
        local_128[0] = (float)(fVar9 + (float10)local_128[0]);
        uStack_fc = FUN_0050a860();
        uStack_f8 = 1;
        local_100 = FUN_006d09b0;
        fStack_f4 = local_128[0];
        FUN_00567130(&local_100);
        local_c._0_1_ = 9;
        FUN_00973430(local_110);
        local_c = CONCAT31(local_c._1_3_,8);
        FUN_00662d00();
      }
    }
    uVar8 = FUN_004154f0();
    FUN_00567030(FUN_00855dc0,uVar8,iVar5,0);
    uStack_b8 = 0;
    local_c._0_1_ = 10;
    uVar8 = FUN_0040bfe0(3,0,3);
    uVar8 = FUN_0040be60(&local_100,uVar8);
    FUN_00973430(uVar8);
    local_c._0_1_ = 8;
    if (puStack_d8 != (undefined4 *)0x0) {
      if ((code *)*puStack_d8 != (code *)0x0) {
        (*(code *)*puStack_d8)(auStack_d0,auStack_d0,1);
      }
      puStack_d8 = (undefined4 *)0x0;
    }
    FUN_00566480(iVar5,local_11c,local_114,param_5);
    local_c._0_1_ = 1;
    FUN_0059f0d0();
  }
  local_c = (uint)local_c._1_3_ << 8;
  FUN_00730730();
LAB_00567725:
  local_c = 0xffffffff;
  FUN_00703bc0();
  ExceptionList = local_14;
  ___security_check_cookie_4();
  return;
}

