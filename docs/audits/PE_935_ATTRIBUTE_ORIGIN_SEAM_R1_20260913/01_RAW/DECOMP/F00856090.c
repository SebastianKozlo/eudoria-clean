
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN_00856090(int param_1_00,uint param_1)

{
  float fVar1;
  float fVar2;
  uint *puVar3;
  uint uVar4;
  int iVar5;
  undefined2 in_FPUControlWord;
  uint local_c;
  longlong local_8;
  
  puVar3 = &local_c;
  fVar1 = (float)(int)param_1;
  if ((int)param_1 < 0) {
    fVar1 = fVar1 + _DAT_00a79d5c;
  }
  iVar5 = (*(int *)(param_1_00 + 0xc) - *(int *)(param_1_00 + 8) >> 2) + -1;
  local_8 = CONCAT44(local_8._4_4_,iVar5);
  fVar2 = (float)iVar5;
  if (iVar5 < 0) {
    fVar2 = fVar2 + _DAT_00a79d5c;
  }
  if (fVar1 / fVar2 <= *(float *)(param_1_00 + 0x18)) {
    fVar1 = (float)*(int *)(param_1_00 + 0x14);
    if (*(int *)(param_1_00 + 0x14) < 0) {
      fVar1 = fVar1 + _DAT_00a79d5c;
    }
    iVar5 = (*(int *)(param_1_00 + 0xc) - *(int *)(param_1_00 + 8) >> 2) + -1;
    local_8 = CONCAT44(local_8._4_4_,iVar5);
    fVar2 = (float)iVar5;
    if (iVar5 < 0) {
      fVar2 = fVar2 + _DAT_00a79d5c;
    }
    if (fVar1 / fVar2 < *(float *)(param_1_00 + 0x18) !=
        (fVar1 / fVar2 == *(float *)(param_1_00 + 0x18))) {
      return;
    }
  }
  local_c = *(uint *)(param_1_00 + 0x14);
  if (*(uint *)(param_1_00 + 0x14) <= param_1) {
    puVar3 = &param_1;
  }
  iVar5 = *puVar3;
  fVar1 = (float)iVar5;
  if (iVar5 < 0) {
    fVar1 = fVar1 + _DAT_00a79d5c;
  }
  param_1 = CONCAT22((short)((uint)iVar5 >> 0x10),in_FPUControlWord);
  local_8 = (longlong)ROUND(fVar1 / *(float *)(param_1_00 + 0x18));
  uVar4 = stlp_std::priv::_Stl_prime<bool>::_S_next_size((uint)local_8);
  FUN_00855ee0(uVar4);
  return;
}

