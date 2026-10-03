// F02_singleton_ctor_008221c0 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G4_TERMINAL_CONSUMER.json

undefined4 * __fastcall FUN_008221c0(undefined4 *param_1)

{
  undefined4 *puVar1;
  uint uVar2;
  undefined local_11;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  puStack_8 = &LAB_00a2316b;
  local_c = ExceptionList;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xffffffe8;
  ExceptionList = &local_c;
  puVar1 = param_1 + 1;
  *param_1 = 0;
  *puVar1 = 0;
  *(undefined *)puVar1 = 0;
  param_1[2] = 0;
  param_1[3] = puVar1;
  param_1[4] = puVar1;
  param_1[5] = 0;
  *(undefined *)(param_1 + 6) = local_11;
  local_4 = 0;
  FUN_00821fb0(uVar2);
  ExceptionList = local_c;
  return param_1;
}

