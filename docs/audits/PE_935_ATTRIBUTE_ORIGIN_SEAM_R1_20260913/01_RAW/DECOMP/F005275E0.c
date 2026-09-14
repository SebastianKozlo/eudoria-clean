
void __thiscall FUN_005275e0(int param_1_00,undefined4 param_1,int *param_2)

{
  int iVar1;
  int iVar2;
  int *piVar3;
  int *piVar4;
  int iVar5;
  undefined2 local_34 [4];
  undefined4 local_2c;
  int local_24;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009bf2e8;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  piVar4 = (int *)FUN_00977780(DAT_00b9d8d0 ^ (uint)&stack0xffffffbc);
  piVar3 = param_2;
  iVar2 = *param_2;
  iVar1 = *piVar4;
  iVar5 = FUN_00747c30(param_1);
  if (iVar5 == *(int *)(param_1_00 + 0x24)) {
    if (iVar2 != iVar1) {
      local_24 = *piVar3;
      local_34[0] = (undefined2)param_1;
      local_2c = 0;
      local_4 = 0;
      iVar1 = *(int *)(param_1_00 + 0x24);
      if (iVar1 == *(int *)(param_1_00 + 0x28)) {
        FUN_00527410(iVar1,local_34,&param_2,1,1);
      }
      else {
        FUN_00526c80(iVar1,local_34);
        *(int *)(param_1_00 + 0x24) = *(int *)(param_1_00 + 0x24) + 0x28;
      }
      local_4 = 0xffffffff;
      FUN_00526c40();
    }
  }
  else if (iVar2 == iVar1) {
    FUN_00527570(iVar5,&param_2);
  }
  else {
    FUN_00526b80(piVar3);
  }
  ExceptionList = local_c;
  return;
}

