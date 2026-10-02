
void __thiscall FUN_00971780(int param_1_00,undefined4 *param_1,uint *param_2)

{
  undefined4 *puVar1;
  undefined4 *puVar2;
  
  puVar1 = (undefined4 *)
           (*(int *)(param_1_00 + 8) +
           (*param_2 % ((*(int *)(param_1_00 + 0xc) - *(int *)(param_1_00 + 8) >> 2) - 1U)) * 4);
  puVar2 = (undefined4 *)puVar1[1];
  for (puVar1 = (undefined4 *)*puVar1; (puVar1 != puVar2 && (puVar1[1] != *param_2));
      puVar1 = (undefined4 *)*puVar1) {
  }
  if (puVar1 != puVar2) {
    *param_1 = puVar1;
    return;
  }
  *param_1 = 0;
  return;
}

