// source: C7_LISTS_AND_ATTACH.json :: Z04_attach_impl_e20_00779e20

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined __fastcall FUN_00779e20(int param_1)

{
  float fVar1;
  
  if (*(int *)(param_1 + 0x60) != 2) {
    return 0;
  }
  FUN_00779d60(1);
  *(float *)(param_1 + 0x68) = -_DAT_00a8e188;
  *(float *)(param_1 + 0x6c) = -_DAT_00a8e188;
  fVar1 = _DAT_00a8e188;
  *(undefined *)(param_1 + 0x74) = 0;
  *(float *)(param_1 + 0x70) = -fVar1;
  FUN_00779160();
  FUN_00778ef0(0);
  return 1;
}

