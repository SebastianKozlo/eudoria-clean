// source: C7_LISTS_AND_ATTACH.json :: Z05_attach_impl_f80_00779f80

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

uint __thiscall FUN_00779f80(int param_1_00,uint param_1)

{
  int iVar1;
  uint in_EAX;
  
  if ((((*(int *)(param_1_00 + 0x60) == 3) && (param_1 != 0)) &&
      (in_EAX = *(uint *)(param_1_00 + 0x90), in_EAX == param_1)) && (*(int *)(in_EAX + 0x60) == 4))
  {
    FUN_00779d60(0);
    FUN_00779d60(1);
    iVar1 = *(int *)(param_1_00 + 0x90);
    *(float *)(param_1_00 + 0x68) = -_DAT_00a8e188;
    *(float *)(param_1_00 + 0x6c) = -_DAT_00a8e188;
    *(undefined4 *)(iVar1 + 0x90) = 0;
    *(undefined4 *)(param_1_00 + 0x90) = 0;
    return CONCAT31((int3)((uint)iVar1 >> 8),1);
  }
  return in_EAX & 0xffffff00;
}

