// H02_mapfind_00415670 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G5_LOOKUP_CLOSURE.json

void FUN_00415670(void)

{
  uint uVar1;
  void *local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_0099638b;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&local_10;
  ExceptionList = &local_c;
  if (DAT_00ba12f4 == 0) {
    local_10 = operator_new(0x98);
    local_4 = 0;
    if (local_10 != (void *)0x0) {
      DAT_00ba12f4 = FUN_00824c70(uVar1);
      ExceptionList = local_c;
      return;
    }
    DAT_00ba12f4 = 0;
  }
  ExceptionList = local_c;
  return;
}

