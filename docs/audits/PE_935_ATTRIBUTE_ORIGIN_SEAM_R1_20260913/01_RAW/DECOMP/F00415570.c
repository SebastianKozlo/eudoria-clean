
void FUN_00415570(void)

{
  uint uVar1;
  void *local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_0099632b;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&local_10;
  ExceptionList = &local_c;
  if (DAT_00ba12ec == 0) {
    local_10 = operator_new(0xcc);
    local_4 = 0;
    if (local_10 != (void *)0x0) {
      DAT_00ba12ec = FUN_00858a40(uVar1);
      ExceptionList = local_c;
      return;
    }
    DAT_00ba12ec = 0;
  }
  ExceptionList = local_c;
  return;
}

