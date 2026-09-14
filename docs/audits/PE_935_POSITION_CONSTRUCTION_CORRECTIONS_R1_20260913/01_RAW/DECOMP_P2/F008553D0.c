// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x8553d0L (requested via site 0x8553d0)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_008553d0(undefined4 param_1,float param_2)

{
  bool bVar1;
  int iVar2;
  char cVar3;
  char cVar4;
  uint uVar5;
  int iVar6;
  int *piVar7;
  undefined4 *puVar8;
  int *piVar9;
  float *pfVar10;
  int iVar11;
  float fVar12;
  undefined4 uVar13;
  float10 fVar14;
  int iVar15;
  int iVar16;
  undefined4 uVar17;
  undefined4 uVar18;
  undefined4 *puVar19;
  void *pvVar20;
  undefined4 uVar21;
  undefined4 *puVar22;
  int local_60;
  undefined4 uStack_5c;
  undefined4 uStack_58;
  float local_54;
  float fStack_50;
  int local_4c;
  int local_48;
  void *local_44;
  undefined local_40 [8];
  int local_38;
  int local_34;
  undefined4 uStack_30;
  undefined4 uStack_2c;
  undefined4 uStack_28;
  float fStack_24;
  void *pvStack_20;
  float fStack_1c;
  undefined local_18 [12];
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a2956d;
  local_c = ExceptionList;
  uVar5 = DAT_00b9d8d0 ^ (uint)&stack0xffffff88;
  ExceptionList = &local_c;
  local_54 = 0.0;
  FUN_0085b840(param_1);
  local_4 = 0;
  iVar6 = FUN_004123d0(uVar5);
  if (iVar6 == 0) {
    local_4 = 0xffffffff;
    FUN_008e0110();
    ExceptionList = local_c;
    return 0;
  }
  FUN_0085b860(&local_44);
  iVar2 = (int)param_2;
  local_4._0_1_ = 1;
  FUN_00417ef0(param_2);
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  FUN_0085b860(&param_2);
  local_4._0_1_ = 2;
  piVar7 = (int *)FUN_0085ad50();
  local_38 = *piVar7;
  local_34 = piVar7[1];
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  FUN_0085b860(&param_2);
  local_4._0_1_ = 3;
  local_48 = FUN_00792b20();
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  FUN_0085b860(&param_2);
  local_4._0_1_ = 4;
  fVar14 = (float10)FUN_0085b020();
  local_54 = (float)fVar14;
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  puVar8 = (undefined4 *)FUN_0085b860(local_40);
  piVar7 = (int *)*puVar8;
  local_4._0_1_ = 5;
  piVar9 = (int *)FUN_0085b860(&local_60);
  iVar6 = *piVar9;
  local_4._0_1_ = 6;
  pfVar10 = (float *)(**(code **)(*piVar7 + 0xc))(local_18);
  param_2 = *pfVar10 + *(float *)(iVar6 + 0x44);
  local_44 = (void *)(pfVar10[1] + *(float *)(iVar6 + 0x48));
  fStack_50 = pfVar10[2] + *(float *)(iVar6 + 0x4c);
  local_4._0_1_ = 5;
  fStack_24 = param_2;
  pvStack_20 = local_44;
  fStack_1c = fStack_50;
  FUN_0085b1a0();
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  piVar7 = (int *)FUN_0085b860(&param_2);
  iVar6 = *piVar7;
  uStack_30 = *(undefined4 *)(iVar6 + 0x5c);
  uStack_2c = *(undefined4 *)(iVar6 + 0x60);
  uStack_28 = *(undefined4 *)(iVar6 + 100);
  FUN_0085b1a0();
  FUN_0085b860(&param_2);
  local_4._0_1_ = 7;
  iVar6 = FUN_0085acb0();
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  FUN_0085b860(&param_2);
  local_4._0_1_ = 8;
  FUN_007ce1e0();
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  FUN_0085b860(&param_2);
  local_4._0_1_ = 9;
  cVar3 = FUN_0085b750();
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  FUN_0085b860(&param_2);
  local_4._0_1_ = 10;
  iVar11 = FUN_006b22d0();
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  FUN_0085b860(local_40);
  local_4._0_1_ = 0xb;
  FUN_00417ea0(0);
  local_4 = (uint)local_4._1_3_ << 8;
  FUN_0085b1a0();
  if (iVar11 != 0) {
    FUN_00415570(iVar11);
    FUN_00858ba0(iVar11);
  }
  uVar13 = 0;
  param_2 = (float)((uint)param_2 & 0xffffff00);
  FUN_0085b860(local_40);
  local_4._0_1_ = 0xc;
  fStack_50 = (float)FUN_0048ada0();
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  iVar11 = local_48;
  if (fStack_50 != 0.0) {
    param_2 = (float)CONCAT31(param_2._1_3_,1);
  }
  local_44 = (void *)0x0;
  uStack_58 = 0;
  local_60 = 0;
  uStack_5c = 0;
  if (local_38 == 0x4e34) {
    local_60 = 1;
    if ((*(int *)(local_4c + 8) == 0) ||
       ((*(int *)(local_4c + 8) == 1 && (iVar11 = FUN_007105f0(), iVar6 == iVar11)))) {
      iVar6 = 3;
    }
    else {
      iVar6 = 1;
    }
    iVar11 = local_48;
    iVar16 = 1;
LAB_00855773:
    puVar19 = &uStack_5c;
    puVar22 = &uStack_58;
    puVar8 = &uStack_30;
    pfVar10 = &fStack_24;
    uVar17 = 1;
    uVar13 = param_1;
    iVar15 = iVar2;
    fVar12 = local_54;
    FUN_00415570(param_1,iVar2,iVar11,local_54,iVar16,1,pfVar10,puVar8,iVar6,puVar22,puVar19);
    uVar13 = FUN_008599a0(uVar13,iVar15,iVar11,fVar12,iVar16,uVar17,pfVar10,puVar8,iVar6,puVar22,
                          puVar19);
  }
  else {
    if (local_48 == 0x38b0) {
      puVar8 = &uStack_5c;
      puVar22 = &uStack_58;
      uVar21 = 0;
      puVar19 = &uStack_30;
      pfVar10 = &fStack_24;
      uVar18 = 1;
      uVar17 = 2;
      local_60 = 2;
      uVar13 = param_1;
      iVar6 = iVar2;
      fVar12 = local_54;
      FUN_00415570(param_1,iVar2,0x38b0,local_54,2,1,pfVar10,puVar19,0,puVar22,puVar8);
      uVar13 = FUN_008599a0(uVar13,iVar6,iVar11,fVar12,uVar17,uVar18,pfVar10,puVar19,uVar21,puVar22,
                            puVar8);
      goto LAB_00855930;
    }
    if (local_38 == 0x4e38) {
      FUN_0085b860(&local_44);
      local_4._0_1_ = 0xd;
      uVar13 = FUN_007ce1e0();
      local_4._0_1_ = 0;
      FUN_0085b1a0();
      switch(uVar13) {
      case 4:
      case 5:
        local_60 = 2;
        break;
      case 6:
        local_60 = 3;
        break;
      case 7:
        local_60 = 4;
      }
      iVar6 = (uint)(*(int *)(local_4c + 8) == 0) * 2 + 1;
      iVar16 = local_60;
      goto LAB_00855773;
    }
    if (cVar3 == '\0') {
      cVar4 = FUN_00978a10(0x159);
      if (cVar4 == '\0') {
        if (iVar2 != 0) {
          uVar13 = 0;
          pvVar20 = (void *)0x0;
          goto LAB_00855922;
        }
      }
      else if (iVar2 != 0) {
        uVar13 = 1;
        pvVar20 = (void *)0x3f800000;
        goto LAB_00855922;
      }
    }
    else {
      cVar4 = FUN_00978a10(0x1bdc);
      if (cVar4 != '\0') {
        local_44 = _DAT_00a7b128;
      }
      uVar13 = 2;
      pvVar20 = local_44;
LAB_00855922:
      puVar19 = &uStack_5c;
      puVar22 = &uStack_58;
      puVar8 = &uStack_30;
      pfVar10 = &fStack_24;
      uVar17 = param_1;
      iVar6 = iVar2;
      FUN_00415570(param_1,iVar2,pfVar10,puVar8,pvVar20,uVar13,puVar22,puVar19);
      uVar13 = FUN_0085a9f0(uVar17,iVar6,pfVar10,puVar8,pvVar20,uVar13,puVar22,puVar19);
    }
  }
LAB_00855930:
  FUN_0085b860(&local_48);
  local_4 = CONCAT31(local_4._1_3_,0xe);
  local_54 = 1.4013e-45;
  cVar4 = FUN_0085b0a0();
  if (cVar4 == '\0') {
    FUN_0085b860(&local_44);
    local_4 = 0xf;
    local_54 = 4.2039e-45;
    cVar4 = FUN_0085b0b0();
    bVar1 = false;
    if (cVar4 == '\0') goto LAB_00855988;
  }
  bVar1 = true;
LAB_00855988:
  local_4 = 0xe;
  if (((uint)local_54 & 2) != 0) {
    local_54 = (float)((uint)local_54 & 0xfffffffd);
    FUN_0085b1a0();
  }
  local_4._0_1_ = 0;
  local_4._1_3_ = 0;
  if (((uint)local_54 & 1) != 0) {
    FUN_0085b1a0();
  }
  iVar6 = local_60;
  fVar12 = fStack_50;
  if (bVar1) {
    if (param_2._0_1_ == '\0') {
      if (local_60 != 0) {
        local_44 = operator_new(0x6c);
        local_4._0_1_ = 0x10;
        if (local_44 == (void *)0x0) {
          local_4._0_1_ = 0;
          fVar12 = (float)0;
        }
        else {
          fVar12 = (float)FUN_00860ee0(uVar13,iVar6);
          local_4._0_1_ = 0;
        }
      }
    }
    else {
      FUN_00797280(uVar13);
      fVar12 = fStack_50;
    }
  }
  if (fVar12 != 0.0) {
    FUN_00860f60();
    piVar7 = (int *)FUN_0085b860(&local_44);
    local_4._0_1_ = 0x11;
    FUN_00861210(*(undefined4 *)(*piVar7 + 100));
    local_4._0_1_ = 0;
    FUN_0085b1a0();
    piVar7 = (int *)FUN_0085b860(&local_44);
    local_4._0_1_ = 0x12;
    FUN_00861230(*(undefined4 *)(*piVar7 + 100));
    local_4._0_1_ = 0;
    FUN_0085b1a0();
    piVar7 = (int *)FUN_0085b860(&local_44);
    local_4._0_1_ = 0x13;
    FUN_0072fd10(*(undefined4 *)(*piVar7 + 0x5c));
    local_4._0_1_ = 0;
    FUN_0085b1a0();
  }
  FUN_0085b860(&local_44);
  local_4._0_1_ = 0x14;
  FUN_0085afd0(iVar2,uStack_58,uStack_5c);
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  FUN_0085b860(&local_44);
  local_4._0_1_ = 0x15;
  FUN_00417ea0(uVar13);
  local_4._0_1_ = 0;
  FUN_0085b1a0();
  if (param_2._0_1_ == '\0') {
    puVar8 = (undefined4 *)FUN_0085b860(&param_2);
    local_4._0_1_ = 0x16;
    (**(code **)(*(int *)*puVar8 + 8))(fVar12);
    local_4._0_1_ = 0;
    FUN_0085b1a0();
  }
  FUN_00788260();
  if (cVar3 != '\0') {
    FUN_00413440();
    FUN_006a8980(local_40,&param_1);
    FUN_00413450();
  }
  local_4 = 0xffffffff;
  FUN_008e0110();
  ExceptionList = local_c;
  return 1;
}

