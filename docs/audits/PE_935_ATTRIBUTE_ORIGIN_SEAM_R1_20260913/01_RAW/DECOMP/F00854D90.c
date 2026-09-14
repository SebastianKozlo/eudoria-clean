
undefined4 * __thiscall FUN_00854d90(int param_1_00,undefined4 *param_1,uint *param_2)

{
  int *piVar1;
  int *piVar2;
  undefined4 *puVar3;
  int *piVar4;
  uint uVar5;
  
  uVar5 = *param_2 % ((*(int *)(param_1_00 + 0xc) - *(int *)(param_1_00 + 8) >> 2) - 1U);
  piVar2 = *(int **)(*(int *)(param_1_00 + 8) + 4 + uVar5 * 4);
  piVar1 = *(int **)(*(int *)(param_1_00 + 8) + uVar5 * 4);
  piVar4 = piVar1;
  if (piVar1 == piVar2) {
    puVar3 = (undefined4 *)FUN_00851610(&param_2,uVar5,param_2);
    *param_1 = *puVar3;
    *(undefined *)(param_1 + 1) = 1;
    return param_1;
  }
  do {
    if (piVar4[1] == *param_2) {
      *param_1 = piVar4;
      *(undefined *)(param_1 + 1) = 0;
      return param_1;
    }
    piVar4 = (int *)*piVar4;
  } while (piVar4 != piVar2);
  piVar2 = (int *)FUN_00854260(param_2);
  *piVar2 = *piVar1;
  *piVar1 = (int)piVar2;
  *(int *)(param_1_00 + 0x14) = *(int *)(param_1_00 + 0x14) + 1;
  *param_1 = piVar2;
  *(undefined *)(param_1 + 1) = 1;
  return param_1;
}

