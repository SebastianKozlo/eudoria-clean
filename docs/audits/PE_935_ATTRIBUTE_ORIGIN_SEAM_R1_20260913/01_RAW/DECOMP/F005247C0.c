
undefined4 __thiscall FUN_005247c0(int param_1_00,undefined4 param_1,undefined4 param_2)

{
  undefined4 uVar1;
  void *local_14 [2];
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009bee6b;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  local_14[0] = operator_new(0x98);
  uVar1 = 0;
  local_4 = 0;
  if (local_14[0] != (void *)0x0) {
    uVar1 = FUN_00509330(param_1_00,param_1,param_2);
  }
  local_4 = 0xffffffff;
  param_2 = uVar1;
  FUN_005094e0(param_1_00 + 0xc0);
  FUN_006a8980(local_14,&param_2);
  ExceptionList = local_c;
  return uVar1;
}

