// source: C6_DRIVER_SOURCES.json :: Y05_driver2_00521770

void __thiscall FUN_00521770(int param_1_00,int param_1)

{
  char cVar1;
  uint uVar2;
  int iVar3;
  int iVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined *puVar7;
  undefined *puVar8;
  undefined4 uVar9;
  undefined4 local_34;
  undefined local_30 [12];
  undefined local_24 [24];
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009be7c0;
  local_c = ExceptionList;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xffffffc0;
  ExceptionList = &local_c;
  if (*(int *)(param_1_00 + 4) != 0) {
    iVar3 = param_1 + 0x28;
    cVar1 = FUN_00408b60(iVar3,"start_usetool: effect_01",uVar2);
    if (cVar1 != '\0') {
      FUN_0085b840(*(undefined4 *)(param_1_00 + 4));
      local_4 = 0;
      iVar3 = FUN_004123d0();
      if (iVar3 != 0) {
        FUN_004123d0();
        iVar3 = FUN_0085acb0();
        if (iVar3 == 0) {
          FUN_004123d0();
          iVar4 = FUN_007ce1e0();
          if (iVar4 != 4) goto LAB_0052190a;
        }
        FUN_00843d60(*(undefined4 *)(param_1_00 + 4));
        local_4._0_1_ = 1;
        iVar4 = FUN_008452d0(0x3f4);
        if (iVar4 != 0) {
          FUN_00843d60(iVar4);
          local_4._0_1_ = 2;
          FUN_004143f0();
          iVar4 = FUN_00746550();
          local_34 = CONCAT31(local_34._1_3_,iVar3 == iVar4);
          if ((iVar3 == iVar4) && (cVar1 = FUN_00844020(0x175), cVar1 != '\0')) {
            FUN_004143f0();
            uVar5 = FUN_007ce1e0();
            FUN_00843d60(uVar5);
            uVar5 = 0;
            puVar8 = local_30;
            puVar7 = local_24;
            local_4._0_1_ = 3;
            FUN_004641f0(puVar7,puVar8,0);
            FUN_00567b40(puVar7,puVar8,uVar5);
            local_4._0_1_ = 2;
            FUN_008e0110();
          }
          uVar9 = local_34;
          uVar6 = FUN_00843dd0(&local_34);
          uVar5 = *(undefined4 *)(param_1_00 + 4);
          puVar8 = local_30;
          FUN_004641f0(uVar5,puVar8,uVar6,uVar9);
          FUN_005666e0(uVar5,puVar8,uVar6,uVar9);
          FUN_0050b770(*(undefined4 *)(param_1_00 + 4),1);
          local_4._0_1_ = 1;
          FUN_008e0110();
        }
        local_4 = (uint)local_4._1_3_ << 8;
        FUN_008e0110();
      }
LAB_0052190a:
      local_4 = 0xffffffff;
      FUN_008e0110();
      ExceptionList = local_c;
      return;
    }
    cVar1 = FUN_00408b60(iVar3,"morph:left",uVar2);
    if ((cVar1 == '\0') && (cVar1 = FUN_00408b60(iVar3,"morph:right",uVar2), cVar1 == '\0')) {
      ExceptionList = local_c;
      return;
    }
    uVar5 = *(undefined4 *)(param_1 + 0x1c);
    uVar9 = *(undefined4 *)(param_1_00 + 4);
    FUN_004146f0(uVar9,uVar5);
    FUN_00443ca0(uVar9,uVar5);
  }
  ExceptionList = local_c;
  return;
}

