
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_00567770(undefined4 param_1,undefined4 param_2)

{
  byte bVar1;
  byte bVar2;
  char cVar3;
  float *pfVar4;
  undefined3 uVar9;
  undefined4 uVar5;
  undefined4 uVar6;
  allocator<char> *paVar7;
  int iVar8;
  undefined *puVar10;
  undefined *puVar11;
  undefined4 uVar12;
  undefined4 uVar13;
  allocator<char> local_119;
  float local_118;
  float local_114;
  float local_110;
  float local_10c [9];
  undefined4 local_e8;
  undefined4 local_e4;
  float local_e0;
  float fStack_dc;
  float fStack_d8;
  float local_c8;
  float local_c4;
  float local_c0;
  float local_bc;
  float fStack_b8;
  float fStack_b4;
  undefined local_b0 [48];
  undefined local_80 [44];
  undefined4 *local_54;
  undefined auStack_4c [24];
  undefined4 uStack_34;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009c9de6;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  local_10c[5] = 0.0;
  local_10c[6] = 0.0;
  local_10c[7] = 0.0;
  local_10c[2] = 0.0;
  local_10c[3] = 0.0;
  local_10c[4] = 0.0;
  bVar1 = FUN_00846840(param_1,local_10c + 5,DAT_00b9d8d0 ^ (uint)&stack0xfffffed4);
  pfVar4 = local_10c + 2;
  FUN_004154f0(param_1,pfVar4);
  bVar2 = FUN_00854720(param_1,pfVar4);
  bVar2 = bVar1 & 1 & bVar2;
  local_10c[8] = local_10c[2];
  local_e8 = local_10c[3];
  local_e4 = local_10c[4];
  FUN_0096c920(&local_bc,local_10c + 8);
  pfVar4 = (float *)FUN_0096c920(&local_e0,local_10c + 2);
  uVar9 = (undefined3)((uint)pfVar4 >> 8);
  local_118 = *pfVar4 + local_10c[5];
  local_114 = local_10c[6] + pfVar4[1];
  local_110 = local_10c[7] + pfVar4[2];
  local_10c[8] = -local_10c[8];
  if (bVar2 != 0) {
    local_c8 = local_118;
    local_c4 = local_114;
    local_c0 = local_110;
    FUN_00730700();
    local_4 = 0;
    uVar5 = FUN_00733340();
    FUN_004c5580(param_2,local_b0,uVar5);
    uVar6 = FUN_00746550();
    FUN_00853a50(0x1bdc);
    FUN_00797280(0);
    FUN_00730f60();
    FUN_00730f90(&local_c8);
    FUN_00730fb0(local_10c + 8);
    local_10c[0] = 9.99406e-42;
    local_10c[1] = 0.0;
    FUN_00730fd0(local_10c);
    paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_119);
    local_4._0_1_ = 1;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)&local_e0,"",paVar7);
    uVar13 = 1;
    uVar12 = 1;
    pfVar4 = &local_e0;
    uVar5 = 2;
    puVar11 = local_b0;
    puVar10 = local_80;
    local_4._0_1_ = 2;
    FUN_004148f0(puVar10,puVar11,2,pfVar4,1,1);
    uVar12 = FUN_00457930(puVar10,puVar11,uVar5,pfVar4,uVar12,uVar13);
    local_4._0_1_ = 1;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)&local_e0);
    local_4._0_1_ = 0;
    stlp_std::allocator<char>::~allocator<char>(&local_119);
    uVar5 = uVar12;
    FUN_004154f0(uVar12,uVar6);
    FUN_008553d0(uVar5,uVar6);
    FUN_0085b840(uVar12);
    local_4._0_1_ = 3;
    iVar8 = FUN_004123d0();
    if (iVar8 != 0) {
      pfVar4 = &local_e0;
      local_10c[0] = (float)_DAT_00a7ae68;
      local_110 = local_bc * local_10c[0];
      local_114 = fStack_b8 * local_10c[0];
      local_10c[0] = local_10c[0] * fStack_b4;
      local_e0 = local_110;
      fStack_dc = local_114;
      fStack_d8 = local_10c[0];
      FUN_004123d0(pfVar4);
      FUN_0085ac50(pfVar4);
      pfVar4 = local_10c;
      local_10c[0] = 0.0;
      local_10c[1] = 0.0;
      cVar3 = FUN_00844020(0x1bde);
      iVar8 = (cVar3 != '\0') + 0x85;
      uVar5 = uVar12;
      FUN_00414770(uVar12,iVar8,pfVar4);
      FUN_00446800(uVar5,iVar8,pfVar4);
      uVar5 = FUN_004154f0();
      FUN_00567030(FUN_00855dc0,uVar5,uVar12,0);
      uStack_34 = 0;
      local_4._0_1_ = 4;
      uVar5 = FUN_0040bfe0(0xe10,0,2);
      FUN_00973430(uVar5);
      local_4._0_1_ = 3;
      if (local_54 != (undefined4 *)0x0) {
        if ((code *)*local_54 != (code *)0x0) {
          (*(code *)*local_54)(auStack_4c,auStack_4c,1);
        }
        local_54 = (undefined4 *)0x0;
      }
    }
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_008e0110();
    local_4 = 0xffffffff;
    uVar5 = FUN_00730730();
    uVar9 = (undefined3)((uint)uVar5 >> 8);
  }
  ExceptionList = local_c;
  return CONCAT31(uVar9,bVar2);
}

