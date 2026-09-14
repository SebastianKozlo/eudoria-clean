// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x521990L (requested via site 0x5219e7)

void __fastcall FUN_00521990(undefined4 *param_1)

{
  void *pvVar1;
  uint uVar2;
  int iVar3;
  undefined4 uVar4;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  puStack_8 = &LAB_009be7f0;
  local_c = ExceptionList;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xffffffdc;
  ExceptionList = &local_c;
  *param_1 = ArkEquippedInventoryUI_Impl::vftable;
  iVar3 = param_1[0x9b];
  local_4 = 0;
  if (iVar3 != 0) {
    FUN_00414670(iVar3,uVar2);
    FUN_0043e450(iVar3);
    uVar4 = param_1[0x9b];
    FUN_004154f0(uVar4);
    FUN_00855dc0(uVar4);
    FUN_00843d60(param_1[0x9b]);
    local_4._0_1_ = 1;
    FUN_00844980();
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_008e0110();
  }
  pvVar1 = (void *)param_1[0x9a];
  if (pvVar1 != (void *)0x0) {
    FUN_005f6030();
    operator_delete(pvVar1);
  }
  local_4 = 0xffffffff;
  FUN_008ee120();
  ExceptionList = local_c;
  return;
}

