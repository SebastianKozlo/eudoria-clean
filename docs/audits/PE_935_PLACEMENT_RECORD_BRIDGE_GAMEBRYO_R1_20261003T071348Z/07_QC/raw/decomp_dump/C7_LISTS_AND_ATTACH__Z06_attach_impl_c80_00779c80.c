// source: C7_LISTS_AND_ATTACH.json :: Z06_attach_impl_c80_00779c80

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 __thiscall FUN_00779c80(int param_1_00,undefined4 param_1,char param_2)

{
  int iVar1;
  char cVar2;
  uint uVar3;
  
  if (*(int *)(param_1_00 + 0x60) != 0) {
    return 0;
  }
  FUN_007787a0(param_1);
  *(undefined *)(param_1_00 + 0x98) = 0;
  *(undefined4 *)(param_1_00 + 0x9c) = 0;
  if (((*(int *)(param_1_00 + 0xac) != 0) && (*(char *)(*(int *)(param_1_00 + 0x5c) + 0x70) != '\0')
      ) && (uVar3 = 0, *(int *)(param_1_00 + 0x38) != 0)) {
    do {
      iVar1 = *(int *)(*(int *)(param_1_00 + 0x30) + uVar3 * 4);
      if (((iVar1 != 0) && (*(int *)(iVar1 + 0x34) == *(int *)(param_1_00 + 0xac))) &&
         (cVar2 = FUN_0043a6d0(&DAT_00ba6b0c,iVar1), cVar2 != '\0')) {
        *(undefined *)(param_1_00 + 0x98) = 1;
        *(uint *)(param_1_00 + 0x9c) = uVar3;
        break;
      }
      uVar3 = uVar3 + 1;
    } while (uVar3 < *(uint *)(param_1_00 + 0x38));
  }
  if (*(char *)(param_1_00 + 0x98) != '\0') {
    *(undefined *)(param_1_00 + 0xa0) = 1;
    *(float *)(param_1_00 + 0xa4) = -_DAT_00a8e188;
    FUN_0077c140(param_1_00 + 0xe0,param_1_00 + 0x104);
  }
  *(undefined4 *)(param_1_00 + 0x60) = 1;
  if (param_2 != '\0') {
    *(float *)(param_1_00 + 100) = -_DAT_00a8e188;
  }
  return 1;
}

