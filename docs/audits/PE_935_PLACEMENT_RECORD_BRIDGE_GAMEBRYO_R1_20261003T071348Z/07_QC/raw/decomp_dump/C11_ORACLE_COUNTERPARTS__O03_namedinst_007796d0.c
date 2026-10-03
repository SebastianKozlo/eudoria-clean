// source: C11_ORACLE_COUNTERPARTS.json :: O03_namedinst_007796d0

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 * __thiscall
FUN_007796d0(undefined4 *param_1_00,undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  float fVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a1972f;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  FUN_007b7580(DAT_00b9d8d0 ^ (uint)&stack0xffffffe0);
  *param_1_00 = NiControllerSequence::vftable;
  param_1_00[3] = 0;
  param_1_00[4] = 0;
  param_1_00[5] = NiTArray<char*>::vftable;
  param_1_00[7] = 0;
  param_1_00[10] = 1;
  param_1_00[8] = 0;
  param_1_00[9] = 0;
  param_1_00[6] = 0;
  param_1_00[0xb] = NiTArray<class_NiPointer<class_NiTimeController>_>::vftable;
  param_1_00[0xd] = 0;
  param_1_00[0x10] = 1;
  param_1_00[0xe] = 0;
  param_1_00[0xf] = 0;
  param_1_00[0xc] = 0;
  param_1_00[0x11] = NiTArray<class_NiObjectNET*>::vftable;
  param_1_00[0x13] = 0;
  param_1_00[0x16] = 1;
  param_1_00[0x14] = 0;
  param_1_00[0x15] = 0;
  param_1_00[0x12] = 0;
  param_1_00[0x17] = 0;
  param_1_00[0x18] = 0;
  param_1_00[0x19] = -_DAT_00a8e188;
  param_1_00[0x1a] = -_DAT_00a8e188;
  param_1_00[0x1b] = -_DAT_00a8e188;
  fVar1 = _DAT_00a8e188;
  *(undefined *)(param_1_00 + 0x1d) = 0;
  param_1_00[0x1c] = -fVar1;
  param_1_00[0x1e] = NiTArray<class_NiPointer<class_NiTimeController>_>::vftable;
  param_1_00[0x20] = 0;
  param_1_00[0x23] = 1;
  param_1_00[0x21] = 0;
  param_1_00[0x22] = 0;
  param_1_00[0x1f] = 0;
  param_1_00[0x24] = 0;
  fVar1 = _DAT_00a8e188;
  *(undefined *)(param_1_00 + 0x26) = 0;
  param_1_00[0x25] = -fVar1;
  param_1_00[0x27] = 0;
  *(undefined *)(param_1_00 + 0x28) = 0;
  fVar1 = _DAT_00a8e188;
  param_1_00[0x2a] = 0;
  param_1_00[0x29] = -fVar1;
  param_1_00[0x2b] = 0;
  puVar3 = &DAT_00b93c80;
  puVar4 = param_1_00 + 0x2c;
  for (iVar2 = 9; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = *puVar3;
    puVar3 = puVar3 + 1;
    puVar4 = puVar4 + 1;
  }
  param_1_00[0x35] = DAT_00ba73a0;
  param_1_00[0x36] = DAT_00ba73a4;
  param_1_00[0x37] = DAT_00ba73a8;
  puVar3 = &DAT_00b93c80;
  puVar4 = param_1_00 + 0x38;
  for (iVar2 = 9; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar4 = *puVar3;
    puVar3 = puVar3 + 1;
    puVar4 = puVar4 + 1;
  }
  local_4 = 7;
  param_1_00[0x41] = DAT_00ba73a0;
  param_1_00[0x42] = DAT_00ba73a4;
  param_1_00[0x43] = DAT_00ba73a8;
  FUN_00777e00(param_1);
  FUN_007a23d0(param_2);
  param_1_00[10] = param_3;
  FUN_00778ef0(param_2);
  param_1_00[0x10] = param_3;
  FUN_007a23d0(0);
  param_1_00[0x16] = param_3;
  ExceptionList = local_c;
  return param_1_00;
}

