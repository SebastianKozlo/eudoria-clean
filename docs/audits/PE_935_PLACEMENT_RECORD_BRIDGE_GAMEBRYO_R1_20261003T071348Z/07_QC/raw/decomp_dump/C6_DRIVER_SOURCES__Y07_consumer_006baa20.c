// source: C6_DRIVER_SOURCES.json :: Y07_consumer_006baa20

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 * __thiscall FUN_006baa20(undefined4 *param_1_00,undefined4 *param_1)

{
  char cVar1;
  uint uVar2;
  undefined4 *puVar3;
  int iVar4;
  undefined4 uVar5;
  bool bVar6;
  undefined4 uVar7;
  int local_24;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  void *local_c;
  undefined *puStack_8;
  uint local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a03a50;
  local_c = ExceptionList;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xffffffc8;
  ExceptionList = &local_c;
  *param_1_00 = DAT_00ba4618;
  param_1_00[1] = DAT_00ba461c;
  param_1_00[2] = 0;
  param_1_00[3] = 0;
  param_1_00[4] = 0;
  FUN_00733340(uVar2);
  param_1_00[0x17] = _DAT_00a7b334;
  bVar6 = true;
  puVar3 = (undefined4 *)FUN_00728150();
  local_18 = *puVar3;
  local_1c = 0x4e26;
  FUN_00703b80(&local_1c);
  local_4 = 0;
  if (local_24 != 0) {
    iVar4 = FUN_0070c180(2);
    if (((*(int *)(iVar4 + 4) == 0) || (*(int *)(iVar4 + 4) != 1)) ||
       ((*(byte *)(iVar4 + 0xc) & 1) != 0)) {
      puVar3 = (undefined4 *)FUN_00977780();
      local_20 = *puVar3;
    }
    else {
      puVar3 = (undefined4 *)FUN_004926e0();
      local_20 = *puVar3;
    }
    iVar4 = FUN_0070c180(6);
    if (((*(int *)(iVar4 + 4) == 0) || (*(int *)(iVar4 + 4) != 1)) ||
       ((*(byte *)(iVar4 + 0xc) & 1) != 0)) {
      puVar3 = (undefined4 *)FUN_00977780();
    }
    else {
      puVar3 = (undefined4 *)FUN_004926e0();
    }
    uVar5 = *puVar3;
    uVar7 = 0x3d1c;
    FUN_00728150(0x3d1c);
    cVar1 = FUN_009768d0(uVar7);
    if (cVar1 == '\0') {
      FUN_0043a550(uVar5);
      uVar5 = FUN_0072f580(uVar5);
      cVar1 = FUN_0072fce0();
      bVar6 = cVar1 != '\0';
      param_1_00[3] = uVar5;
      if (!bVar6) goto LAB_006babec;
    }
    uVar5 = FUN_00728150();
    local_10 = FUN_00738150(uVar5);
    local_14 = 0x4e48;
    FUN_00703b80(&local_14);
    local_4 = CONCAT31(local_4._1_3_,1);
    if (param_1 == (undefined4 *)0x0) {
LAB_006babc1:
      bVar6 = false;
    }
    else {
      uVar5 = FUN_006ea810(2);
      cVar1 = FUN_00737c20(uVar5);
      if (cVar1 != '\0') goto LAB_006babc1;
      param_1_00[4] = param_1;
    }
    local_4 = local_4 & 0xffffff00;
    FUN_00703bc0();
    if (bVar6) {
      *param_1_00 = *param_1;
      param_1_00[1] = param_1[1];
      param_1_00[2] = local_20;
      goto LAB_006babf2;
    }
  }
LAB_006babec:
  param_1_00[3] = 0;
  param_1_00[4] = 0;
LAB_006babf2:
  local_4 = 0xffffffff;
  FUN_00703bc0();
  ExceptionList = local_c;
  return param_1_00;
}

