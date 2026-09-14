
void __thiscall
FUN_00851610(undefined4 *param_1_00,undefined4 *param_1,int param_2,undefined4 param_3)

{
  int *piVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 *puVar5;
  undefined4 *local_4;
  
  iVar3 = param_2;
  piVar1 = param_1_00 + 2;
  local_4 = param_1_00;
  FUN_00704220(&local_4,param_1_00 + 1,piVar1,&param_2);
  puVar4 = (undefined4 *)FUN_00854260(param_3);
  *puVar4 = *local_4;
  *local_4 = puVar4;
  iVar2 = *piVar1;
  for (puVar5 = (undefined4 *)(iVar2 + param_2 * 4); puVar5 != (undefined4 *)(iVar2 + 4 + iVar3 * 4)
      ; puVar5 = puVar5 + 1) {
    *puVar5 = puVar4;
  }
  param_1_00[5] = param_1_00[5] + 1;
  *param_1 = *(undefined4 *)(*piVar1 + iVar3 * 4);
  return;
}

