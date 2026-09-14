// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x853bd0L (requested via site 0x853c3a)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float10 __thiscall FUN_00853bd0(int param_1_00,float *param_1,float *param_2,undefined4 param_3)

{
  float *pfVar1;
  char cVar2;
  float10 fVar3;
  float local_1c;
  float local_18;
  float local_14;
  float local_10;
  float local_c;
  float local_8;
  float local_4;
  
  pfVar1 = param_2;
  fVar3 = (float10)1;
  local_1c = (float)fVar3;
  local_18 = 0.0;
  local_14 = 0.0;
  local_10 = 0.0;
  local_c = *param_2;
  local_8 = param_2[1];
  param_2 = (float *)(local_8 * local_8 + local_c * local_c + 0.0);
  if ((float)param_2 <= _DAT_00a91d28) {
    cVar2 = FUN_00755f90(param_1);
    if (cVar2 != '\0') {
      local_c = *param_1 + *pfVar1;
      local_8 = pfVar1[1] + param_1[1];
      local_4 = pfVar1[2] + param_1[2];
      cVar2 = FUN_00755f90(&local_c);
      if ((cVar2 != '\0') && (*(int *)(param_1_00 + 4) != 0)) {
        FUN_00413440();
        cVar2 = (**(code **)(**(int **)(param_1_00 + 4) + 4))
                          (param_1,pfVar1,&local_18,&param_2,param_3);
        FUN_00413450();
        if (cVar2 != '\0') {
          local_c = *param_1 - local_18;
          local_8 = param_1[1] - local_14;
          local_4 = param_1[2] - local_10;
          fVar3 = (float10)FUN_00444940();
          param_2 = (float *)(float)fVar3;
          fVar3 = (float10)FUN_00444940();
          local_1c = (float)((float10)(float)param_2 / fVar3);
        }
      }
    }
    fVar3 = (float10)local_1c;
  }
  return fVar3;
}

