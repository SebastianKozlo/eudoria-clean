
undefined4 __thiscall FUN_0094bd30(int param_1_00,int *param_1)

{
  char cVar1;
  
  FUN_00412430(param_1_00 + 4);
  if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U)) {
    *(undefined4 *)(param_1_00 + 0x10) = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
      goto LAB_0094bd76;
    }
  }
  else {
    *(undefined4 *)(param_1_00 + 0x10) = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
LAB_0094bd76:
    if ((*(char *)((int)param_1 + 0x11) != '\0') && (param_1[3] + 4U <= (uint)param_1[2])) {
      *(undefined4 *)(param_1_00 + 0x14) = *(undefined4 *)(param_1[3] + *param_1);
      FUN_0040de60(4);
      goto LAB_0094bda9;
    }
  }
  *(undefined4 *)(param_1_00 + 0x14) = 0;
  if (*(char *)((int)param_1 + 0x11) != '\0') {
    *(undefined *)((int)param_1 + 0x11) = 0;
  }
LAB_0094bda9:
  cVar1 = FUN_00959090(param_1);
  if ((cVar1 != '\0') && (*(char *)((int)param_1 + 0x11) != '\0')) {
    return 1;
  }
  return 0;
}

