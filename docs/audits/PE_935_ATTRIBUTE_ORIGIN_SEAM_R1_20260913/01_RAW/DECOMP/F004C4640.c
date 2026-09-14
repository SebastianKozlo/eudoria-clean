
void FUN_004c4640(void)

{
  uint uVar1;
  void *local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009afbbb;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&local_10;
  ExceptionList = &local_c;
  if (DAT_00ba26b8 == 0) {
    local_10 = operator_new(0x1c);
    local_4 = 0;
    if (local_10 != (void *)0x0) {
      DAT_00ba26b8 = FUN_00766480(uVar1);
      ExceptionList = local_c;
      return;
    }
    DAT_00ba26b8 = 0;
  }
  ExceptionList = local_c;
  return;
}

