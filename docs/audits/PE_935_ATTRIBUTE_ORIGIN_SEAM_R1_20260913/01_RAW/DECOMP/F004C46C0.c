
void FUN_004c46c0(undefined4 *param_1,int param_2,undefined4 param_3,undefined4 param_4)

{
  void *pvVar1;
  undefined4 uVar2;
  float10 fVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined4 local_2c;
  float local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009afbeb;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  local_38 = *param_1;
  local_34 = param_1[1];
  uVar2 = param_1[2];
  uVar4 = param_1[3];
  local_28 = (float)param_1[4];
  local_24 = param_1[5];
  local_20 = param_1[6];
  local_1c = param_1[7];
  local_18 = param_1[8];
  local_14 = param_1[9];
  local_10 = param_1[10];
  local_30 = uVar2;
  local_2c = uVar4;
  if ((((param_2 == 3) || (param_2 == 6)) || (param_2 == 5)) || ((param_2 == 4 || (param_2 == 7))))
  {
    uVar6 = 0;
    uVar5 = 0;
    FUN_004154f0(uVar2,uVar4,0,0,DAT_00b9d8d0 ^ (uint)&stack0xffffffc4);
    fVar3 = (float10)FUN_00853a80(uVar2,uVar4,uVar5,uVar6);
    if (local_28 < (float)fVar3) {
      local_28 = (float)fVar3;
    }
  }
  pvVar1 = operator_new(0x128);
  local_4 = 0;
  if (pvVar1 == (void *)0x0) {
    uVar2 = 0;
  }
  else {
    uVar2 = FUN_00528e50(&local_38,param_2,param_3,param_4);
  }
  local_4 = 0xffffffff;
  FUN_004154f0(uVar2);
  FUN_00856190(uVar2);
  ExceptionList = local_c;
  return;
}

