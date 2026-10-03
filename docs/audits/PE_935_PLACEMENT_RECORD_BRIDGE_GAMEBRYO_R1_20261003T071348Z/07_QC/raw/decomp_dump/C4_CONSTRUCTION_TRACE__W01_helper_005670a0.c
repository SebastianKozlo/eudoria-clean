// source: C4_CONSTRUCTION_TRACE.json :: W01_helper_005670a0

undefined4 * __thiscall FUN_005670a0(undefined4 *param_1_00,undefined4 *param_1)

{
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009c9cfb;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  *param_1_00 = *param_1;
  param_1_00[1] = param_1[1];
  param_1_00[2] = param_1[2];
  param_1_00[3] = param_1[3];
  param_1_00[4] = param_1[4];
  FUN_00566f80(param_1 + 5);
  local_4 = 0;
  FUN_00525da0(param_1 + 8);
  param_1_00[0xb] = param_1[0xb];
  ExceptionList = local_c;
  return param_1_00;
}

