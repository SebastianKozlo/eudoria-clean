// source: C5_LAYOUT_AND_DRIVERS.json :: X04_list1_copy_00566f80

int * __thiscall FUN_00566f80(int *param_1_00,int *param_1)

{
  int *piVar1;
  uint uVar2;
  int iVar3;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  piVar1 = param_1;
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009c9cc8;
  local_c = ExceptionList;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xffffffe4;
  ExceptionList = &local_c;
  param_1 = (int *)(param_1[1] - *param_1 >> 5);
  *param_1_00 = 0;
  param_1_00[1] = 0;
  param_1_00[2] = 0;
  iVar3 = FUN_00565fd0(param_1,&param_1);
  *param_1_00 = iVar3;
  param_1_00[1] = iVar3;
  param_1_00[2] = (int)param_1 * 0x20 + iVar3;
  local_4 = 0;
  iVar3 = FUN_00566d60(*piVar1,piVar1[1],iVar3,&param_1,0,uVar2);
  param_1_00[1] = iVar3;
  ExceptionList = local_c;
  return param_1_00;
}

