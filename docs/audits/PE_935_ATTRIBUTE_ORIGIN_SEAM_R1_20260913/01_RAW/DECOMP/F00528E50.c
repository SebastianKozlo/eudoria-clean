
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 * __thiscall
FUN_00528e50(undefined4 *param_1_00,undefined4 param_1,undefined4 param_2,undefined4 param_3,
            undefined4 param_4)

{
  uint *puVar1;
  char cVar2;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  undefined4 uVar6;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  local_24 [24];
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009bf53f;
  local_c = ExceptionList;
  uVar3 = DAT_00b9d8d0 ^ (uint)&stack0xffffffcc;
  ExceptionList = &local_c;
  FUN_0085b1b0(param_1,param_2,param_3);
  param_1_00[0x2b] = 0;
  param_1_00[0x2d] = 0;
  *param_1_00 = ClientMovableObject::vftable;
  param_1_00[0x29] = 0;
  *(undefined *)(param_1_00 + 0x2a) = 0;
  *(undefined *)(param_1_00 + 0x2c) = 0;
  param_1_00[0x2f] = 0;
  param_1_00[0x30] = 0;
  param_1_00[0x31] = 0;
  param_1_00[0x32] = 0;
  param_1_00[0x33] = 0;
  *(undefined *)(param_1_00 + 0x34) = 0;
  *(undefined *)((int)param_1_00 + 0xd1) = 0;
  *(undefined *)((int)param_1_00 + 0xd2) = 0;
  param_1_00[0x35] = 0;
  param_1_00[0x36] = 0;
  param_1_00[0x37] = 0;
  local_4._0_1_ = 1;
  local_4._1_3_ = 0;
  param_1_00[0x38] = 0;
  param_1_00[0x39] = 0;
  cVar2 = FUN_0085b0a0(uVar3);
  uVar4 = _DAT_00a7b25c;
  if (cVar2 != '\0') {
    uVar4 = _DAT_00a7a16c;
  }
  param_1_00[0x3a] = uVar4;
  param_1_00[0x3b] = 0;
  param_1_00[0x3c] = 0;
  param_1_00[0x3d] = 0;
  param_1_00[0x3e] = 0;
  param_1_00[0x3f] = 0;
  param_1_00[0x40] = 0;
  param_1_00[0x41] = 0;
  param_1_00[0x42] = 0;
  param_1_00[0x43] = 0;
  param_1_00[0x44] = 0;
  param_1_00[0x45] = 0;
  param_1_00[0x46] = 0;
  param_1_00[0x47] = 0;
  param_1_00[0x48] = 0;
  param_1_00[0x49] = 0;
  uVar4 = FUN_00746570();
  FUN_0085ad60(uVar4);
  FUN_00401360(param_4);
  FUN_00485050();
  iVar5 = FUN_0048cbb0(param_4);
  if (iVar5 != 0) {
    uVar4 = FUN_0085b120(local_24);
    local_4._0_1_ = 2;
    uVar6 = FUN_00414130(uVar4);
    uVar4 = FUN_005247c0(uVar6,uVar4);
    param_1_00[0x30] = uVar4;
    local_4 = CONCAT31(local_4._1_3_,1);
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (local_24);
    cVar2 = FUN_0085b750();
    if (cVar2 == '\0') {
      puVar1 = (uint *)(param_1_00[0x30] + 0x2c);
      *puVar1 = *puVar1 & 0xfffffffe;
    }
    else {
      puVar1 = (uint *)(param_1_00[0x30] + 0x2c);
      *puVar1 = *puVar1 | 1;
    }
    FUN_005094c0(param_1_00 + 0x11);
    FUN_00509510(param_1_00 + 0x17);
    FUN_00509070(param_1_00 + 0x14);
    FUN_00509850(0,0);
    param_1_00[0x2d] = param_1_00[0x19];
  }
  ExceptionList = local_c;
  return param_1_00;
}

