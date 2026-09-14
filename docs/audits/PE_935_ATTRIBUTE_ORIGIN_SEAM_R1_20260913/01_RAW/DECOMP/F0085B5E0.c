
void __thiscall FUN_0085b5e0(int param_1_00,undefined4 *param_1)

{
  undefined4 uVar1;
  undefined4 local_c;
  undefined4 local_8;
  
  local_8 = param_1[1];
  local_c = *param_1;
  uVar1 = param_1[2];
  if (*(int *)(param_1_00 + 8) == 3) {
    local_c = 0;
    local_8 = 0;
  }
  FUN_0096b760();
  *(undefined4 *)(param_1_00 + 0x5c) = local_c;
  *(undefined4 *)(param_1_00 + 0x60) = local_8;
  *(undefined4 *)(param_1_00 + 100) = uVar1;
  return;
}

