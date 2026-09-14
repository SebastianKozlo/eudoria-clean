// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x857830L (requested via site 0x857863)

undefined4
FUN_00857830(float *param_1,float param_2,float *param_3,undefined4 *param_4,float *param_5)

{
  float fVar1;
  float fVar2;
  float fVar3;
  float10 fVar4;
  float *pfVar5;
  float *pfVar6;
  undefined4 *puVar7;
  float local_24;
  float local_20;
  float local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  
  local_24 = 0.0;
  local_20 = 0.0;
  puVar7 = &local_18;
  local_1c = -param_2;
  pfVar6 = &local_24;
  local_18 = 0;
  local_14 = 0;
  local_10 = 0;
  pfVar5 = param_1;
  FUN_004154f0(param_1,pfVar6,puVar7);
  fVar4 = (float10)FUN_00853bd0(pfVar5,pfVar6,puVar7);
  fVar1 = (float)fVar4;
  if (fVar1 < 1.0 != NAN(fVar1)) {
    fVar2 = param_1[1];
    fVar3 = param_1[2];
    *param_3 = *param_1 + local_24 * fVar1;
    param_3[1] = fVar2 + local_20 * fVar1;
    param_3[2] = fVar3 + local_1c * fVar1;
    *param_4 = local_18;
    param_4[1] = local_14;
    param_4[2] = local_10;
    *param_5 = fVar1;
    return 1;
  }
  return 0;
}

