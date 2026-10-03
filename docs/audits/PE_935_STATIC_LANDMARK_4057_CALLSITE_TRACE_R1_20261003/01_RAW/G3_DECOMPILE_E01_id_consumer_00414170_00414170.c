// E01_id_consumer_00414170 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G3_FALSIFIER_PATH.json

void FUN_00414170(void)

{
  uint uVar1;
  void *local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00995bab;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&local_10;
  ExceptionList = &local_c;
  if (DAT_00ba124c == 0) {
    local_10 = operator_new(0x1c);
    local_4 = 0;
    if (local_10 != (void *)0x0) {
      DAT_00ba124c = FUN_008221c0(uVar1);
      ExceptionList = local_c;
      return;
    }
    DAT_00ba124c = 0;
  }
  ExceptionList = local_c;
  return;
}

