
void FUN_004b0ab0(int param_1)

{
  int iVar1;
  char cVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_20;
  undefined4 local_1c;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  iVar1 = param_1;
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009ac998;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  puVar4 = &local_20;
  local_20 = 0;
  local_1c = 0;
  iVar3 = param_1;
  FUN_00415470(param_1,puVar4,DAT_00b9d8d0 ^ (uint)&stack0xffffffd8);
  cVar2 = FUN_007046a0(iVar3,puVar4);
  if (cVar2 != '\0') {
    FUN_00843d60(local_1c);
    local_4 = 0;
    cVar2 = FUN_0042bc20();
    if (cVar2 == '\0') {
      cVar2 = FUN_00525af0(iVar1);
      if (cVar2 != '\0') {
        FUN_00836a50();
        local_4._0_1_ = 1;
        cVar2 = FUN_004c47f0(iVar1);
        local_4._0_1_ = 0;
        FUN_008e0110();
        if (cVar2 != '\0') {
          FUN_004b0930(&local_20);
          local_4._0_1_ = 2;
          if (param_1 != 0) {
            puVar4 = &param_1;
            FUN_004642f0(puVar4);
            FUN_0056a560(puVar4);
          }
          local_4 = (uint)local_4._1_3_ << 8;
          FUN_00703bc0();
        }
      }
    }
    local_4 = 0xffffffff;
    FUN_008e0110();
  }
  ExceptionList = local_c;
  return;
}

