// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x846bb0L (requested via site 0x846bec)

byte FUN_00846bb0(undefined4 param_1,float param_2,int *param_3,float *param_4,undefined4 param_5,
                 char param_6)

{
  byte bVar1;
  byte bVar2;
  float *pfVar3;
  float10 fVar4;
  undefined4 uVar5;
  undefined4 *puVar6;
  undefined4 uVar7;
  int *piVar8;
  float *pfVar9;
  float local_34;
  float local_30;
  float local_2c;
  float local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined local_c [12];
  
  local_18 = 0;
  local_14 = 0;
  local_10 = 0;
  local_24 = 0;
  local_20 = 0;
  local_1c = 0;
  bVar1 = FUN_00846840(param_1,&local_18);
  puVar6 = &local_24;
  uVar5 = param_1;
  FUN_004154f0(param_1,puVar6);
  bVar2 = FUN_00854720(uVar5,puVar6);
  bVar2 = bVar1 & 1 & bVar2;
  if (bVar2 != 0) {
    pfVar3 = (float *)FUN_0096c920(local_c,&local_24);
    local_2c = param_2 * pfVar3[1];
    pfVar9 = &local_34;
    local_28 = pfVar3[2] * param_2;
    uVar7 = 2;
    puVar6 = &local_18;
    local_30 = param_2 * *pfVar3;
    pfVar3 = &local_30;
    uVar5 = 1;
    piVar8 = param_3;
    FUN_004154f0(1,puVar6,pfVar3,2,param_1,param_3,param_5,pfVar9);
    bVar1 = FUN_00853d00(uVar5,puVar6,pfVar3,uVar7,param_1,piVar8,param_5,pfVar9);
    bVar2 = bVar2 & bVar1;
    if (param_6 == '\0') {
      if (*param_3 == 0) {
        *param_3 = -1;
      }
    }
    else {
      bVar2 = bVar2 & *param_3 != 0;
    }
    if (bVar2 != 0) {
      fVar4 = (float10)_CIsqrt();
      *param_4 = (float)fVar4 * local_34;
    }
  }
  return bVar2;
}

