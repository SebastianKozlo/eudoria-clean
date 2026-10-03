// D03_eax_producer_008e7b80 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G2_CALLEE_DEEPDIVE.json

undefined4 __thiscall FUN_008e7b80(undefined4 param_1_00,undefined4 param_1)

{
  char cVar1;
  uint uVar2;
  undefined4 uVar3;
  undefined4 uVar4;
  undefined local_40 [8];
  undefined local_38 [44];
  void *local_c;
  undefined *puStack_8;
  uint local_4;
  
  puStack_8 = &LAB_00a3c981;
  local_c = ExceptionList;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xffffffb4;
  ExceptionList = &local_c;
  local_4 = 0;
  uVar3 = FUN_008dfae0(local_38,1);
  local_4 = 1;
  FUN_008f0820(uVar3);
  local_4 = local_4 & 0xffffff00;
  FUN_008df670(uVar2);
  cVar1 = FUN_008df290();
  if (cVar1 == '\0') {
    FUN_0045b790(param_1_00);
    FUN_008f0460(1);
    FUN_008f04a0(1);
    uVar4 = 1;
    uVar3 = FUN_008df2d0(local_40,1);
    FUN_008df310(uVar3,uVar4);
    FUN_008df470(0);
    FUN_008f0520(1);
  }
  ExceptionList = local_c;
  return param_1;
}

