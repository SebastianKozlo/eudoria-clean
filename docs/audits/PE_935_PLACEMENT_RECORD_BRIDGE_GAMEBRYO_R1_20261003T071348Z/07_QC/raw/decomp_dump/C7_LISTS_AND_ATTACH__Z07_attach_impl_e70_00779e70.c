// source: C7_LISTS_AND_ATTACH.json :: Z07_attach_impl_e70_00779e70

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint __thiscall FUN_00779e70(int param_1_00,int param_1,undefined4 param_2,uint param_3)

{
  int *piVar1;
  int *piVar2;
  float fVar3;
  uint uVar4;
  int iVar5;
  int iVar6;
  
  uVar4 = FUN_00779c80(param_3,0);
  if (((char)uVar4 == '\0') || (uVar4 = FUN_00779c80(param_3,0), (char)uVar4 == '\0')) {
    return uVar4 & 0xffffff00;
  }
  param_3 = 0;
  if (*(int *)(param_1_00 + 0x38) == *(int *)(param_1 + 0x38)) {
    while( true ) {
      while( true ) {
        fVar3 = _DAT_00a8e188;
        if (*(uint *)(param_1_00 + 0x38) <= param_3) {
          *(undefined4 *)(param_1_00 + 0x60) = 3;
          *(float *)(param_1_00 + 0x68) = -fVar3;
          *(undefined4 *)(param_1_00 + 0x6c) = param_2;
          fVar3 = _DAT_00a8e188;
          *(undefined4 *)(param_1 + 0x60) = 4;
          *(float *)(param_1 + 100) = -fVar3;
          *(int *)(param_1_00 + 0x90) = param_1;
          *(int *)(param_1 + 0x90) = param_1_00;
          return CONCAT31((int3)(param_3 >> 8),1);
        }
        piVar1 = *(int **)(*(int *)(param_1_00 + 0x30) + param_3 * 4);
        piVar2 = *(int **)(*(int *)(param_1 + 0x30) + param_3 * 4);
        if (piVar1 != (int *)0x0) break;
        if (piVar2 != (int *)0x0) goto LAB_00779f11;
        param_3 = param_3 + 1;
      }
      if (piVar2 == (int *)0x0) break;
      iVar5 = (**(code **)(*piVar1 + 8))();
      iVar6 = (**(code **)(*piVar2 + 8))();
      if ((iVar5 != iVar6) || (piVar1[0xd] != piVar2[0xd])) break;
      param_3 = param_3 + 1;
    }
  }
LAB_00779f11:
  FUN_00779d60(0);
  uVar4 = FUN_00779d60(0);
  return uVar4 & 0xffffff00;
}

