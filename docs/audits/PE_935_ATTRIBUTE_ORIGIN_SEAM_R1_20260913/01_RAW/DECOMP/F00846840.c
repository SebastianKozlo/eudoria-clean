
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

bool FUN_00846840(undefined4 param_1,float *param_2)

{
  uint uVar1;
  int iVar2;
  int *piVar3;
  bool bVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  bool bVar7;
  bool bVar8;
  float10 fVar9;
  char local_65;
  float local_64;
  float fStack_60;
  float fStack_5c;
  int local_58;
  float local_54;
  float local_50;
  float local_4c;
  undefined4 uStack_48;
  float fStack_44;
  undefined4 uStack_40;
  undefined4 local_3c;
  undefined4 local_38;
  undefined4 local_34;
  float fStack_30;
  float fStack_2c;
  float fStack_28;
  float fStack_24;
  float fStack_20;
  float fStack_1c;
  float fStack_18;
  float fStack_14;
  float fStack_10;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a27eb0;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&stack0xffffff8c;
  ExceptionList = &local_c;
  local_54 = 0.0;
  local_50 = 0.0;
  local_4c = 0.0;
  uVar6 = 0;
  local_34 = 0;
  uVar5 = 0;
  local_65 = '\0';
  FUN_0085b840(param_1);
  local_4 = 0;
  iVar2 = FUN_004123d0(uVar1);
  if (iVar2 != 0) {
    FUN_0085b860(&local_58);
    local_4._0_1_ = 1;
    uVar5 = FUN_0085acb0();
    local_4._0_1_ = 0;
    FUN_0085b1a0();
    piVar3 = (int *)FUN_0085b860(&local_58);
    iVar2 = *piVar3;
    local_54 = *(float *)(iVar2 + 0x44);
    local_50 = *(float *)(iVar2 + 0x48);
    local_4c = *(float *)(iVar2 + 0x4c);
    FUN_0085b1a0();
    piVar3 = (int *)FUN_0085b860(&local_58);
    iVar2 = *piVar3;
    local_3c = *(undefined4 *)(iVar2 + 0x5c);
    local_38 = *(undefined4 *)(iVar2 + 0x60);
    local_34 = *(undefined4 *)(iVar2 + 100);
    FUN_0085b1a0();
    FUN_0085b860(&local_58);
    local_4._0_1_ = 2;
    local_65 = FUN_0085b050();
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_0085b1a0();
  }
  iVar2 = FUN_004123d0(uVar1);
  bVar7 = iVar2 != 0;
  local_4 = 0xffffffff;
  FUN_008e0110();
  bVar4 = bVar7;
  if (bVar7) {
    local_64 = (float)FUN_007103c0();
    fStack_60 = (float)uVar5;
    FUN_00703b80(&local_64);
    bVar8 = local_58 == 0;
    local_4 = 3;
    if (!bVar8) {
      uVar6 = FUN_00714740();
      fVar9 = (float10)FUN_00710740();
      local_64 = (float)fVar9;
      bVar8 = local_58 == 0;
    }
    bVar4 = bVar7 && !bVar8;
    local_4 = 0xffffffff;
    FUN_00703bc0();
    if (bVar7 && !bVar8) {
      if (local_65 == '\0') {
        switch(uVar6) {
        case 0x6a4:
          fStack_44 = (float)_DAT_00a7b260 * local_64;
          fStack_5c = local_64 * (float)_DAT_00a91c78;
          break;
        case 0x6a5:
          fStack_44 = (float)_DAT_00a7b3e8 * local_64;
          fStack_5c = local_64 * (float)_DAT_00a7af78;
          break;
        default:
          fStack_44 = 0.0;
          fStack_5c = local_64;
          break;
        case 0x6a8:
          fStack_44 = (float)_DAT_00a79a08 * local_64;
          fStack_5c = local_64 * (float)_DAT_00a7af80;
          break;
        case 0x6a9:
          fStack_44 = 0.0;
          fStack_5c = _DAT_00a7ae90;
        }
      }
      else {
        fStack_44 = -local_64 * (float)_DAT_00a7b3e8;
        fStack_5c = local_64 * (float)_DAT_00a7b308;
      }
      fStack_60 = fStack_44;
      uStack_48 = 0;
      fStack_44 = 0.0;
      local_64 = 0.0;
      uStack_40 = local_34;
      FUN_0096cdd0(&uStack_48);
      *param_2 = fStack_60 * fStack_24 + local_64 * fStack_30 + fStack_5c * fStack_18 + local_54;
      param_2[1] = fStack_14 * fStack_5c + fStack_2c * local_64 + fStack_20 * fStack_60 + local_50;
      param_2[2] = fStack_5c * fStack_10 + fStack_1c * fStack_60 + fStack_28 * local_64 + local_4c;
    }
  }
  ExceptionList = local_c;
  return bVar4;
}

