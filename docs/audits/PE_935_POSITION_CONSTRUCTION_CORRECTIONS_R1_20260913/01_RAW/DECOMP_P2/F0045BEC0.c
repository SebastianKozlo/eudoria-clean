// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x45bec0L (requested via site 0x45bf90)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN_0045bec0(int param_1_00,float param_1,undefined4 *param_2,undefined4 *param_3)

{
  float *pfVar1;
  undefined4 *puVar2;
  float10 fVar3;
  float fVar4;
  float fVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 local_3c;
  undefined4 local_38;
  float local_34;
  float local_30;
  float local_2c;
  float local_28;
  float local_24;
  float local_20;
  float local_1c;
  float local_18;
  float local_14;
  float local_10;
  undefined local_c [12];
  
  local_38 = param_2[1];
  local_3c = *param_2;
  local_34 = *(float *)(param_1_00 + 0x30) + (float)param_2[2];
  FUN_0096c130(&local_3c);
  FUN_0096c170(&local_34);
  local_38 = 0;
  pfVar1 = (float *)FUN_0096c920(&local_30,&local_3c);
  local_18 = param_1 * *pfVar1;
  local_14 = pfVar1[1] * param_1;
  local_10 = param_1 * pfVar1[2];
  FUN_0045ba30(&local_24);
  uVar7 = 0;
  local_1c = *(float *)(param_1_00 + 0xbc) + local_1c;
  uVar6 = 0;
  fVar4 = local_24 - local_18;
  fVar5 = local_20 - local_14;
  local_28 = local_1c - local_10;
  local_30 = fVar4;
  local_2c = fVar5;
  FUN_004154f0(fVar4,fVar5,0,0);
  fVar3 = (float10)FUN_00853a80(fVar4,fVar5,uVar6,uVar7);
  param_2 = (undefined4 *)(float)fVar3;
  pfVar1 = &local_28;
  if (local_28 <= (float)param_2) {
    pfVar1 = (float *)&param_2;
  }
  local_28 = *pfVar1;
  FUN_0045ba30(&local_18);
  local_10 = *(float *)(param_1_00 + 0xbc) + local_10;
  local_24 = local_18 - local_30;
  local_20 = local_14 - local_2c;
  local_1c = local_10 - local_28;
  puVar2 = (undefined4 *)FUN_0096c630(local_c,&local_24);
  local_3c = *puVar2;
  local_38 = puVar2[1];
  local_34 = (float)puVar2[2] - (float)_DAT_00a7adc0;
  FUN_0096c130(&local_3c);
  FUN_0096c170(&local_34);
  *(float *)(param_1_00 + 0x138) = local_30;
  *(float *)(param_1_00 + 0x13c) = local_2c;
  *(undefined4 *)(param_1_00 + 0x144) = local_3c;
  *(float *)(param_1_00 + 0x140) = local_28;
  *(undefined4 *)(param_1_00 + 0x148) = 0;
  *(float *)(param_1_00 + 0x14c) = local_34;
  *(undefined4 *)(param_1_00 + 0x150) = *param_3;
  *(undefined4 *)(param_1_00 + 0x154) = param_3[1];
  *(undefined4 *)(param_1_00 + 0x158) = param_3[2];
  return;
}

