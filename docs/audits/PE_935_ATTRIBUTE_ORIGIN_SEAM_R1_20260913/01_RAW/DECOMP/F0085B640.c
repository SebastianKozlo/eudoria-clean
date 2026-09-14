
void __thiscall FUN_0085b640(int param_1_00,undefined4 *param_1)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined4 local_8;
  
  local_8 = param_1[1];
  uVar1 = *param_1;
  uVar2 = param_1[2];
  if ((*(int *)(param_1_00 + 8) == 3) || (*(int *)(param_1_00 + 8) == 4)) {
    local_8 = 0;
  }
  FUN_0096b760();
  *(undefined4 *)(param_1_00 + 0x68) = uVar1;
  *(undefined4 *)(param_1_00 + 0x6c) = local_8;
  *(undefined4 *)(param_1_00 + 0x70) = uVar2;
  return;
}

