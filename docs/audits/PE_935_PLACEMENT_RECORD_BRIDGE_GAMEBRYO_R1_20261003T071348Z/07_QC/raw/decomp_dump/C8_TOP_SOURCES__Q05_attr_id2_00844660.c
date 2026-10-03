// source: C8_TOP_SOURCES.json :: Q05_attr_id2_00844660

undefined4 __fastcall FUN_00844660(int param_1)

{
  uint uVar1;
  int *piVar2;
  undefined4 uVar3;
  int local_1c;
  undefined local_18 [4];
  undefined4 local_14;
  int local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a27778;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&stack0xffffffe0;
  ExceptionList = &local_c;
  if (*(int *)(param_1 + 4) == 0) {
    local_1c = 0;
    piVar2 = &local_1c;
  }
  else {
    piVar2 = (int *)FUN_00747970(local_18);
  }
  local_10 = *piVar2;
  local_14 = 0x4e26;
  FUN_00703b80(&local_14);
  local_4 = 0;
  if (local_1c != 0) {
    uVar3 = FUN_007376a0();
    local_4 = 0xffffffff;
    FUN_00703bc0(uVar1);
    ExceptionList = local_c;
    return uVar3;
  }
  local_4 = 0xffffffff;
  FUN_00703bc0(uVar1);
  ExceptionList = local_c;
  return 0;
}

