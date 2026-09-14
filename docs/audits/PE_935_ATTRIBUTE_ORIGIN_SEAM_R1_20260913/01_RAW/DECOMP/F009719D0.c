
void __thiscall FUN_009719d0(int param_1_00,undefined4 *param_1,undefined4 *param_2)

{
  undefined4 *puVar1;
  undefined4 uVar2;
  undefined4 local_30;
  undefined4 local_2c;
  uint local_28;
  uint uStack_24;
  int local_14;
  int local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a4a138;
  local_c = ExceptionList;
  uStack_24 = DAT_00b9d8d0 ^ (uint)&stack0xffffffe0;
  ExceptionList = &local_c;
  local_10 = param_1_00 + 0x1c;
  local_28 = 0x971a06;
  FUN_00413440();
  puVar1 = param_1;
  param_1 = (undefined4 *)((uint)param_1 & 0xffffff00);
  local_28 = (uint)param_1;
  *puVar1 = 0;
  *param_2 = 0;
  local_2c = 0;
  local_30 = *(undefined4 *)(param_1_00 + 0x54);
  param_1 = &local_30;
  local_4 = 0;
  FUN_009717e0(&local_14);
  param_1 = (undefined4 *)((uint)param_1 & 0xffffff00);
  local_28 = (uint)param_1;
  local_2c = 0;
  local_30 = *(undefined4 *)(param_1_00 + 0x54);
  param_1 = &local_30;
  FUN_00971880(&param_1);
  if (local_14 != 0) {
    local_28 = 0x971a93;
    uVar2 = FUN_007ce1e0();
    *puVar1 = uVar2;
  }
  if (param_1 != (undefined4 *)0x0) {
    local_28 = 0x971aa6;
    uVar2 = FUN_007ce1e0();
    *param_2 = uVar2;
  }
  local_4 = 0xffffffff;
  local_28 = 0x971abb;
  FUN_00413450();
  ExceptionList = local_c;
  return;
}

