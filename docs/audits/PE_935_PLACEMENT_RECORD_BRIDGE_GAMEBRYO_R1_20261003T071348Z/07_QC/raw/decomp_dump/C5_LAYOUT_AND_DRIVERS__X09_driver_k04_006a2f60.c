// source: C5_LAYOUT_AND_DRIVERS.json :: X09_driver_k04_006a2f60

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_006a2f60(int param_1)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float fVar4;
  int *piVar5;
  void *pvVar6;
  int iVar7;
  int *piVar8;
  float10 fVar9;
  float10 fVar10;
  int local_c8;
  int *local_c4;
  undefined4 *local_a4;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a00b12;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  FUN_007524d0();
  local_4 = 0;
  FUN_00751be0();
  local_4._0_1_ = 1;
  FUN_006a28c0();
  FUN_006a2a00();
  FUN_006a2b30();
  local_4._0_1_ = 0;
  FUN_00751c10();
  FUN_00752090();
  fVar1 = *(float *)(param_1 + 0x3c);
  fVar2 = *(float *)(param_1 + 0x38);
  DAT_00ba4160 = DAT_00ba4160 + 1;
  fVar9 = (float10)FUN_00405920();
  FUN_00405920();
  FUN_00405920();
  FUN_0043ae80();
  FUN_00405e60();
  FUN_0096cdd0();
  FUN_00401260();
  FUN_00401260();
  FUN_0040bfe0();
  FUN_00973500();
  FUN_0040bfe0();
  FUN_0040be80();
  FUN_0040be00();
  FUN_0040bd20();
  pvVar6 = operator_new(0x70);
  local_4._0_1_ = 2;
  if (pvVar6 != (void *)0x0) {
    FUN_006a3930();
  }
  local_4._0_1_ = 0;
  FUN_006a3560();
  local_4._0_1_ = 3;
  if (local_c8 != 0) {
    fVar3 = *(float *)(param_1 + 0x24);
    fVar4 = *(float *)(param_1 + 0x20);
    fVar10 = (float10)FUN_00405920();
    FUN_0043ae80();
    piVar5 = (int *)(((fVar3 - fVar4) * (float)fVar10 + fVar4) *
                    ((fVar1 - fVar2) * (float)fVar9 + fVar2));
    FUN_0085d180();
    FUN_00405e60();
    FUN_0085d1e0();
    if (local_c4 != (int *)0x0) {
      LOCK();
      local_c4[1] = local_c4[1] + 1;
      UNLOCK();
    }
    iVar7 = FUN_006a2c30();
    local_4._0_1_ = 4;
    if (*(int *)(iVar7 + 8) != 0) {
      piVar8 = (int *)(*(int *)(iVar7 + 8) + 4);
      LOCK();
      *piVar8 = *piVar8 + 1;
      UNLOCK();
    }
    FUN_006a2e70();
    local_4._0_1_ = 5;
    FUN_00973430();
    local_4._0_1_ = 4;
    if ((local_a4 != (undefined4 *)0x0) && ((code *)*local_a4 != (code *)0x0)) {
      (*(code *)*local_a4)();
    }
    local_4._0_1_ = 3;
    if (piVar5 != (int *)0x0) {
      LOCK();
      iVar7 = piVar5[1] + -1;
      piVar5[1] = iVar7;
      UNLOCK();
      if (iVar7 == 0) {
        (**(code **)(*piVar5 + 4))();
        LOCK();
        iVar7 = piVar5[2] + -1;
        piVar5[2] = iVar7;
        UNLOCK();
        if (iVar7 == 0) {
          (**(code **)(*piVar5 + 8))();
        }
      }
    }
  }
  local_4 = (uint)local_4._1_3_ << 8;
  if (local_c4 != (int *)0x0) {
    LOCK();
    iVar7 = local_c4[1] + -1;
    local_c4[1] = iVar7;
    UNLOCK();
    if (iVar7 == 0) {
      (**(code **)(*local_c4 + 4))();
      LOCK();
      iVar7 = local_c4[2] + -1;
      local_c4[2] = iVar7;
      UNLOCK();
      if (iVar7 == 0) {
        (**(code **)(*local_c4 + 8))();
      }
    }
  }
  local_4 = 0xffffffff;
  FUN_00751c10();
  ExceptionList = local_c;
  return;
}

