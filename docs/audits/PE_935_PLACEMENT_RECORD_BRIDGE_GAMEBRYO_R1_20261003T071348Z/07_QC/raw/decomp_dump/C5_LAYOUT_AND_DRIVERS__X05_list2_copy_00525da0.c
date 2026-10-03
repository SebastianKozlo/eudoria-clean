// source: C5_LAYOUT_AND_DRIVERS.json :: X05_list2_copy_00525da0

undefined4 * __thiscall FUN_00525da0(undefined4 *param_1_00,int *param_1)

{
  void *pvVar1;
  void *_Src;
  int *piVar2;
  void *pvVar3;
  size_t _Size;
  
  piVar2 = param_1;
  param_1 = (int *)(param_1[1] - *param_1 >> 2);
  *param_1_00 = 0;
  param_1_00[1] = 0;
  param_1_00[2] = 0;
  pvVar3 = (void *)FUN_00444cf0(param_1,&param_1);
  *param_1_00 = pvVar3;
  param_1_00[1] = pvVar3;
  param_1_00[2] = (void *)((int)pvVar3 + (int)param_1 * 4);
  pvVar1 = (void *)piVar2[1];
  _Src = (void *)*piVar2;
  if (pvVar1 != _Src) {
    _Size = (int)pvVar1 - (int)_Src;
    pvVar3 = memcpy(pvVar3,_Src,_Size);
    pvVar3 = (void *)((int)pvVar3 + _Size);
  }
  param_1_00[1] = pvVar3;
  return param_1_00;
}

