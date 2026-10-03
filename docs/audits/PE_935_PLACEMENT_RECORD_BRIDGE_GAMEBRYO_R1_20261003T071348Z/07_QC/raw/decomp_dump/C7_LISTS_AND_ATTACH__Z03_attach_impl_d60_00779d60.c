// source: C7_LISTS_AND_ATTACH.json :: Z03_attach_impl_d60_00779d60

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN_00779d60(int param_1_00,char param_1)

{
  int iVar1;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined local_24 [36];
  
  if (*(int *)(param_1_00 + 0x60) != 0) {
    if ((*(char *)(param_1_00 + 0x98) != '\0') && (param_1 != '\0')) {
      iVar1 = *(int *)(param_1_00 + 0xac);
      local_30 = *(undefined4 *)(iVar1 + 0x5c);
      local_2c = *(undefined4 *)(iVar1 + 0x60);
      local_28 = *(undefined4 *)(iVar1 + 100);
      FUN_007c4040(local_24,*(undefined4 *)(iVar1 + 0x68));
      FUN_0077c220(local_24,&local_30);
    }
    iVar1 = *(int *)(*(int *)(param_1_00 + 0x30) + *(int *)(param_1_00 + 0x9c) * 4);
    if ((NAN(-_DAT_00a8e188) || NAN(*(float *)(iVar1 + 0x24))) ==
        (-_DAT_00a8e188 == *(float *)(iVar1 + 0x24))) {
      *(float *)(param_1_00 + 100) =
           (*(float *)(iVar1 + 0x28) / *(float *)(iVar1 + 0x10) - *(float *)(iVar1 + 0x24)) +
           *(float *)(param_1_00 + 100);
    }
    *(undefined4 *)(param_1_00 + 0x60) = 0;
    FUN_00778860();
  }
  return;
}

