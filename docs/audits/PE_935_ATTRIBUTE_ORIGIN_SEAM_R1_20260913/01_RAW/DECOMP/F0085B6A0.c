
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN_0085b6a0(int param_1_00,undefined4 *param_1)

{
  int iVar1;
  float10 fVar2;
  float local_4;
  
  FUN_00976770(*(undefined4 *)(param_1_00 + 0x78),0);
  iVar1 = *(int *)(param_1_00 + 8);
  if ((((iVar1 != 3) && (iVar1 != 6)) && (iVar1 != 5)) &&
     (((iVar1 != 4 && (iVar1 != 7)) &&
      ((*(int *)(param_1_00 + 0x7c) != 0 || (*(int *)(param_1_00 + 0x78) == 0)))))) {
    *param_1 = 0;
    param_1[1] = 0;
    param_1[2] = 0;
    return;
  }
  if (*(int *)(param_1_00 + 0x10) == 0) {
    *param_1 = 0;
    param_1[1] = 0;
    param_1[2] = _DAT_00a81d40;
    return;
  }
  fVar2 = (float10)FUN_00861320();
  local_4 = (float)fVar2;
  if (_DAT_00a81d40 < local_4 != (NAN(_DAT_00a81d40) || NAN(local_4))) {
    local_4 = _DAT_00a81d40;
  }
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = (float)_DAT_00a7b508 + (local_4 - (float)_DAT_00a7b508);
  return;
}

