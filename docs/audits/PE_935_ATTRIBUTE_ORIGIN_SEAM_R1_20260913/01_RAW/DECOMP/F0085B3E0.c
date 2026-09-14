
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN_0085b3e0(int *param_1_00,float *param_1,undefined4 param_2)

{
  bool bVar1;
  char cVar2;
  float *pfVar3;
  int iVar4;
  float10 fVar5;
  float fVar6;
  float fVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  int iVar10;
  float local_3c;
  float local_38;
  float local_34;
  float local_30;
  float local_2c;
  float local_28;
  float fStack_24;
  float fStack_20;
  float fStack_1c;
  float local_18;
  float local_14;
  float local_10;
  undefined local_c [12];
  
  fVar7 = param_1[1];
  uVar9 = 0;
  fVar6 = *param_1;
  local_28 = param_1[2];
  uVar8 = 0;
  local_30 = fVar6;
  local_2c = fVar7;
  FUN_004154f0(fVar6,fVar7,0,0);
  fVar5 = (float10)FUN_00853a80(fVar6,fVar7,uVar8,uVar9);
  if (local_28 < (float)fVar5) {
    local_28 = (float)fVar5;
  }
  iVar4 = 0;
  bVar1 = false;
  local_3c = local_30;
  local_38 = local_2c;
  local_34 = local_28;
  if (param_1_00[2] == 3) {
    do {
      pfVar3 = (float *)(**(code **)(*param_1_00 + 0xc))(local_c);
      fStack_24 = *pfVar3 + local_3c;
      fStack_20 = pfVar3[1] + local_38;
      iVar10 = param_1_00[3];
      fStack_1c = pfVar3[2] + local_34;
      uVar9 = 2;
      pfVar3 = &local_18;
      local_18 = fStack_24 + 0.0;
      local_14 = fStack_20 + 0.0;
      local_10 = fStack_1c - (float)_DAT_00a7b2d0;
      uVar8 = _DAT_00a80594;
      FUN_00415570(pfVar3,_DAT_00a80594,2,iVar10);
      cVar2 = FUN_00856800(pfVar3,uVar8,uVar9,iVar10);
      if (cVar2 == '\0') goto LAB_0085b5a1;
      iVar4 = iVar4 + 1;
      local_3c = local_3c + 0.0;
      bVar1 = true;
      local_38 = local_38 + 0.0;
      local_34 = local_34 + (float)_DAT_00a7af80;
    } while (iVar4 < 100);
  }
  else {
    do {
      iVar10 = param_1_00[3];
      fVar7 = local_3c + 0.0;
      uVar9 = 2;
      pfVar3 = &local_18;
      fVar6 = local_38 + 0.0;
      local_10 = local_34 + (float)_DAT_00a79818;
      uVar8 = _DAT_00a7af9c;
      local_18 = fVar7;
      local_14 = fVar6;
      FUN_00415570(pfVar3,_DAT_00a7af9c,2,iVar10);
      cVar2 = FUN_00856800(pfVar3,uVar8,uVar9,iVar10);
      if (cVar2 == '\0') goto LAB_0085b5a1;
      iVar4 = iVar4 + 1;
      bVar1 = true;
      local_34 = local_34 + (float)_DAT_00a7af80;
      local_3c = fVar7;
      local_38 = fVar6;
    } while (iVar4 < 100);
  }
LAB_0085b5a5:
  local_30 = local_3c;
  local_2c = local_38;
  local_28 = local_34;
LAB_0085b5bd:
  (**(code **)(*param_1_00 + 4))(&local_30,param_2);
  return;
LAB_0085b5a1:
  if (!bVar1) goto LAB_0085b5bd;
  goto LAB_0085b5a5;
}

