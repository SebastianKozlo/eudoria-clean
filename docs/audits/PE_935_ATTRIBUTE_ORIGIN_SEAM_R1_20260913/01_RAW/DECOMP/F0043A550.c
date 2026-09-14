
void FUN_0043a550(void)

{
  uint uVar1;
  void *local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_0099c68b;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&local_10;
  ExceptionList = &local_c;
  if (DAT_00ba1824 == 0) {
    local_10 = operator_new(0x18);
    local_4 = 0;
    if (local_10 != (void *)0x0) {
      DAT_00ba1824 = FUN_0052a260(uVar1);
      ExceptionList = local_c;
      return;
    }
    DAT_00ba1824 = 0;
  }
  ExceptionList = local_c;
  return;
}

