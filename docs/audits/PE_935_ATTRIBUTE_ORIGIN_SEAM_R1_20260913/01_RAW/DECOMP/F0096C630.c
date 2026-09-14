
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

float * FUN_0096c630(float *param_1,float *param_2)

{
  float fVar1;
  float fVar2;
  float10 fVar3;
  
  *param_1 = DAT_00ba921c;
  param_1[1] = DAT_00ba9220;
  param_1[2] = DAT_00ba9224;
  if (ABS(*param_2) <= _DAT_00a797c8) {
    if (0.0 < param_2[1] == NAN(param_2[1])) {
      param_1[2] = _DAT_00a91ec4;
    }
    else {
      param_1[2] = _DAT_00a7ae30;
    }
  }
  else {
    fVar3 = (float10)_CIatan();
    param_1[2] = (float)fVar3;
    if (*param_2 < 0.0) {
      param_1[2] = (float)fVar3 + (float)_DAT_00a7aeb0;
    }
  }
  _CIsqrt();
  fVar3 = (float10)_CIatan();
  fVar1 = (float)fVar3;
  *param_1 = fVar1;
  fVar2 = _DAT_00a9c490;
  if (((float)_DAT_00a9c498 < fVar1) ||
     (fVar2 = _DAT_00a9c480,
     fVar1 < (float)_DAT_00a9c488 != (NAN(fVar1) || NAN((float)_DAT_00a9c488)))) {
    *param_1 = fVar2;
  }
  fVar1 = param_1[2];
  if (param_1[2] <= (float)_DAT_00a7aeb0) {
    if (fVar1 < (float)_DAT_00a9c450 != (NAN(fVar1) || NAN((float)_DAT_00a9c450))) {
      param_1[2] = param_1[2] + (float)_DAT_00a79820;
    }
    return param_1;
  }
  param_1[2] = fVar1 - (float)_DAT_00a79820;
  return param_1;
}

