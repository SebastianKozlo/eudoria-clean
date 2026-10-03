// E03_store_008dfb70 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G3_FALSIFIER_PATH.json

void __thiscall FUN_008dfb70(undefined4 param_1,undefined4 param_2)

{
  uint uVar1;
  int iVar2;
  undefined4 uVar3;
  undefined4 uStack_6c;
  undefined4 uStack_68;
  undefined **local_64;
  undefined4 uStack_54;
  int iStack_44;
  void *pvStack_40;
  int iStack_3c;
  undefined **local_38 [4];
  undefined4 local_28;
  int local_18;
  void *local_14;
  int local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a3b920;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&stack0xffffff90;
  ExceptionList = &local_c;
  iVar2 = FUN_008df1e0(uVar1);
  if (iVar2 != 0) {
    uVar3 = FUN_008dfae0(local_38,0x26b9);
    local_4 = 0;
    FUN_0092b490(uVar3);
    local_4 = CONCAT31(local_4._1_3_,2);
    local_38[0] = ArkUI::Component::vftable;
    if (local_14 != (void *)0x0) {
      FUN_00890d30(local_28,local_18 + 4);
      if (local_14 != (void *)0x0) {
        stlp_std::__node_alloc::deallocate(local_14,local_10 * 4);
      }
    }
    iVar2 = FUN_008df1e0(uVar1);
    if (iVar2 == 0) {
      FUN_008df9a0(param_1);
      iVar2 = FUN_008df1e0();
      if (iVar2 == 0) {
        uStack_6c = 0;
        uStack_68 = 0;
      }
      else {
        FUN_008e04e0(&uStack_6c,1);
      }
      iVar2 = FUN_008df1e0();
      if (iVar2 != 0) {
        FUN_008e2ab0(&uStack_6c,1);
      }
    }
    FUN_0092b390(param_2);
    local_4 = 0xffffffff;
    local_64 = ArkUI::Component::vftable;
    if (pvStack_40 != (void *)0x0) {
      FUN_00890d30(uStack_54,iStack_44 + 4);
      if (pvStack_40 != (void *)0x0) {
        stlp_std::__node_alloc::deallocate(pvStack_40,iStack_3c * 4);
      }
    }
  }
  ExceptionList = local_c;
  return;
}

