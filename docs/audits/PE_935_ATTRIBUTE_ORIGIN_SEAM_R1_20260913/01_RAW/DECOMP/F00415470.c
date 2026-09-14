
void FUN_00415470(void)

{
  uint uVar1;
  void *local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009962cb;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&local_10;
  ExceptionList = &local_c;
  if (DAT_00ba12e4 == 0) {
    local_10 = operator_new(0x100);
    local_4 = 0;
    if (local_10 != (void *)0x0) {
      DAT_00ba12e4 = FUN_00707e50(uVar1);
      ExceptionList = local_c;
      return;
    }
    DAT_00ba12e4 = 0;
  }
  ExceptionList = local_c;
  return;
}

