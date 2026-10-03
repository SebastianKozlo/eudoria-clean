// source: C5_LAYOUT_AND_DRIVERS.json :: X10_visual_helper_006c8f80

undefined4 * __thiscall
FUN_006c8f80(undefined4 *param_1_00,undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  void *local_c;
  undefined *puStack_8;
  undefined local_4;
  undefined3 uStack_3;
  
  puStack_8 = &LAB_00a055a7;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  *param_1_00 = ArkModelManager::vftable;
  param_1_00[2] = 0;
  param_1_00[10] = 0;
  param_1_00[0x12] = 0;
  param_1_00[0x13] = 0;
  param_1_00[0x14] = 0;
  param_1_00[0x15] = 0;
  param_1_00[0x16] = 0;
  param_1_00[0x17] = 0;
  param_1_00[0x18] = 0;
  param_1_00[0x19] = 0;
  param_1_00[0x1a] = 0;
  local_4 = 3;
  uStack_3 = 0;
  param_1_00[0x1b] = 0;
  FUN_005670a0(param_1);
  _local_4 = CONCAT31(uStack_3,4);
  FUN_0043a330(param_1_00 + 0x28,param_3,0x18,3,&LAB_0043a300);
  param_1_00[0x3a] = param_2;
  *(undefined *)(param_1_00 + 0x3b) = 0;
  param_1_00[0x3c] = 0;
  ExceptionList = local_c;
  return param_1_00;
}

