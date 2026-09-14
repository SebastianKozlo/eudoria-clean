
undefined4 FUN_004c4a10(undefined4 param_1,int param_2)

{
  int iVar1;
  char cVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 *puVar7;
  void *local_c;
  undefined *puStack_8;
  uint local_4;
  
  puStack_8 = &LAB_009afc71;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  uVar6 = 0;
  local_4 = 0;
  FUN_0075ff20(DAT_00b9d8d0 ^ (uint)&stack0xffffffd4);
  iVar1 = param_2;
  local_4 = 0;
  if (param_2 != 0) {
    FUN_00843d60(param_2);
    local_4 = 1;
    FUN_00843dd0(&param_2);
    cVar2 = FUN_0042bc20();
    if (cVar2 != '\0') {
      uVar6 = FUN_004123d0();
    }
    iVar3 = iVar1;
    FUN_004154f0(iVar1);
    iVar3 = FUN_008544d0(iVar3);
    if (iVar3 != 0) {
      puVar7 = &param_2;
      uVar4 = FUN_00792b20(uVar6,puVar7);
      uVar5 = FUN_0085ad50(uVar4);
      FUN_00719e30(iVar1,uVar5,uVar4,uVar6,puVar7);
    }
    local_4 = local_4 & 0xffffff00;
    FUN_008e0110();
  }
  ExceptionList = local_c;
  return param_1;
}

