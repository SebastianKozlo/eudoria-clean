// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x509330L (requested via site 0x509330)

undefined4 * __thiscall FUN_00509330(undefined4 *param_1_00,undefined4 param_1,undefined4 param_2)

{
  uint uVar1;
  void *pvVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  undefined4 *puVar6;
  undefined4 local_30 [9];
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  puStack_8 = &LAB_009bac39;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&stack0xffffffbc;
  ExceptionList = &local_c;
  local_4 = 0;
  *param_1_00 = SceneFeederObject::vftable;
  FUN_0040b980(uVar1);
  *(undefined *)(param_1_00 + 4) = 0;
  param_1_00[5] = param_2;
  param_1_00[6] = 0;
  param_1_00[7] = 0;
  param_1_00[8] = 0;
  *(undefined *)(param_1_00 + 9) = 0;
  *(undefined *)((int)param_1_00 + 0x25) = 0;
  *(undefined *)((int)param_1_00 + 0x26) = 0;
  *(undefined *)((int)param_1_00 + 0x27) = 0;
  *(undefined *)(param_1_00 + 10) = 0;
  *(undefined *)((int)param_1_00 + 0x29) = 1;
  param_1_00[0xb] = 0;
  pvVar2 = operator_new(0x118);
  local_4._0_1_ = 1;
  if (pvVar2 == (void *)0x0) {
    iVar3 = 0;
  }
  else {
    iVar3 = FUN_007b6000(0);
  }
  param_1_00[0xc] = iVar3;
  if (iVar3 != 0) {
    *(int *)(iVar3 + 4) = *(int *)(iVar3 + 4) + 1;
  }
  param_1_00[0xd] = 0;
  param_1_00[0xe] = 0;
  param_1_00[0xf] = 0;
  param_1_00[0x10] = 0;
  param_1_00[0x11] = 0;
  local_4._0_1_ = 2;
  param_1_00[0x12] = 0;
  param_1_00[0x1d] = 0;
  param_1_00[0x1e] = 0;
  param_1_00[0x1f] = 0;
  param_1_00[0x20] = 0;
  param_1_00[0x21] = 0;
  param_1_00[0x22] = 0;
  param_1_00[0x23] = param_1;
  *(undefined *)(param_1_00 + 0x24) = 1;
  *(undefined *)((int)param_1_00 + 0x91) = 0;
  param_1_00[0xd] = DAT_00ba921c;
  param_1_00[0xe] = DAT_00ba9220;
  param_1_00[0xf] = DAT_00ba9224;
  param_1_00[0x10] = DAT_00ba921c;
  param_1_00[0x11] = DAT_00ba9220;
  param_1_00[0x12] = DAT_00ba9224;
  puVar5 = &DAT_00b93c80;
  puVar6 = local_30;
  for (iVar3 = 9; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar6 = *puVar5;
    puVar5 = puVar5 + 1;
    puVar6 = puVar6 + 1;
  }
  param_1_00[0x1c] = 0x3f800000;
  puVar5 = local_30;
  puVar6 = param_1_00 + 0x13;
  for (iVar3 = 9; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar6 = *puVar5;
    puVar5 = puVar5 + 1;
    puVar6 = puVar6 + 1;
  }
  pvVar2 = operator_new(0x14);
  local_4._0_1_ = 3;
  if (pvVar2 == (void *)0x0) {
    uVar4 = 0;
  }
  else {
    uVar4 = FUN_0064b1e0(param_1_00[5]);
  }
  local_4 = CONCAT31(local_4._1_3_,2);
  FUN_007b6a80("ArkSceneFeeder",uVar4);
  ExceptionList = local_c;
  return param_1_00;
}

