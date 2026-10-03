// source: C3_DECOMP.json :: R08_other_00848ea0

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_00848ea0(void)

{
  char cVar1;
  byte bVar2;
  uint uVar3;
  int iVar4;
  undefined4 uVar5;
  undefined4 *puVar6;
  ushort *puVar7;
  byte bVar8;
  uint uVar9;
  uint uVar10;
  float10 fVar11;
  float local_68;
  undefined local_64 [4];
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  undefined4 local_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  undefined local_18 [12];
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a28300;
  local_c = ExceptionList;
  uVar3 = DAT_00b9d8d0 ^ (uint)&stack0xffffff88;
  ExceptionList = &local_c;
  bVar8 = 1;
  uVar10 = 0;
  do {
    cVar1 = FUN_00745540(1);
    if (cVar1 == '\0') {
      cVar1 = FUN_00745540(2);
      if (cVar1 != '\0') {
        local_68 = 0.0;
        uVar9 = 0;
        iVar4 = FUN_00745bf0(uVar10);
        if (iVar4 != 0) {
          FUN_00843d60(iVar4);
          local_4 = 1;
          puVar7 = (ushort *)FUN_00843dd0(local_64);
          uVar9 = (uint)*puVar7;
          fVar11 = (float10)FUN_00745690(uVar10);
          local_68 = (float)fVar11;
          bVar2 = FUN_00843d90();
          bVar8 = bVar8 & bVar2;
          local_4 = 0xffffffff;
          FUN_008e0110();
        }
        iVar4 = FUN_007333e0(uVar10);
        *(uint *)(iVar4 + 0xc) = uVar9;
        iVar4 = FUN_007333e0(uVar10);
        *(float *)(iVar4 + 0x10) = local_68;
      }
    }
    else {
      local_60 = _DAT_00a7b25c;
      local_5c = _DAT_00a7b25c;
      local_58 = _DAT_00a7b25c;
      iVar4 = FUN_00745bf0(uVar10);
      if (iVar4 != 0) {
        FUN_00843d60(iVar4);
        local_4 = 0;
        uVar5 = FUN_00844660(uVar3);
        FUN_0043a550(uVar5);
        FUN_0072f580(uVar5);
        local_4 = 0xffffffff;
        FUN_008e0110();
        cVar1 = FUN_0072fce0();
        if (cVar1 == '\0') {
          bVar8 = 0;
        }
        else {
          local_54 = 0;
          local_50 = 0;
          local_4c = 0;
          local_48 = 0;
          local_44 = 0;
          local_40 = 0;
          FUN_0072fe30(&local_60,&local_48,&local_54);
          local_3c = _DAT_00a7b25c;
          local_38 = _DAT_00a7b25c;
          local_34 = _DAT_00a7b25c;
          fVar11 = (float10)FUN_00745690(uVar10);
          puVar6 = (undefined4 *)FUN_006c1f90(local_18,&local_3c,&local_60,(float)fVar11);
          local_60 = *puVar6;
          local_5c = puVar6[1];
          local_58 = puVar6[2];
        }
      }
      puVar6 = (undefined4 *)FUN_007333e0(uVar10);
      *puVar6 = local_60;
      puVar6[1] = local_5c;
      puVar6[2] = local_58;
    }
    uVar10 = uVar10 + 1;
  } while (uVar10 < 3);
  ExceptionList = local_c;
  return bVar8;
}

