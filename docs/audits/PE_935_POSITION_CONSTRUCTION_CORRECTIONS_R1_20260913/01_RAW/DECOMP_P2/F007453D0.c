// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x7453d0L (requested via site 0x7453d0)

undefined __thiscall FUN_007453d0(undefined4 *param_1_00,int *param_1)

{
  int *piVar1;
  
  if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U)) {
    *param_1_00 = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
    }
  }
  else {
    *param_1_00 = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
  }
  FUN_004124b0(param_1_00 + 1);
  piVar1 = (int *)FUN_007343e0(param_1,param_1_00 + 3);
  if ((*(char *)((int)piVar1 + 0x11) == '\0') || ((uint)piVar1[2] < piVar1[3] + 2U)) {
    *(undefined2 *)(param_1_00 + 0xd) = 0;
    if (*(char *)((int)piVar1 + 0x11) != '\0') {
      *(undefined *)((int)piVar1 + 0x11) = 0;
    }
  }
  else {
    *(undefined2 *)(param_1_00 + 0xd) = *(undefined2 *)(piVar1[3] + *piVar1);
    FUN_0040de60(2);
  }
  FUN_00412430(param_1_00 + 0xe);
  FUN_00412430(param_1_00 + 0x11);
  if ((*(char *)((int)piVar1 + 0x11) == '\0') || ((uint)piVar1[2] < piVar1[3] + 4U)) {
    param_1_00[0x14] = 0;
    if (*(char *)((int)piVar1 + 0x11) != '\0') {
      *(undefined *)((int)piVar1 + 0x11) = 0;
      goto LAB_00745498;
    }
LAB_007454bb:
    param_1_00[0x15] = 0;
    if (*(char *)((int)piVar1 + 0x11) != '\0') {
      *(undefined *)((int)piVar1 + 0x11) = 0;
      goto LAB_007454c6;
    }
LAB_007454e9:
    param_1_00[0x16] = 0;
    if (*(char *)((int)piVar1 + 0x11) == '\0') goto LAB_00745522;
    *(undefined *)((int)piVar1 + 0x11) = 0;
  }
  else {
    param_1_00[0x14] = *(undefined4 *)(piVar1[3] + *piVar1);
    FUN_0040de60(4);
LAB_00745498:
    if ((*(char *)((int)piVar1 + 0x11) == '\0') || ((uint)piVar1[2] < piVar1[3] + 4U))
    goto LAB_007454bb;
    param_1_00[0x15] = *(undefined4 *)(piVar1[3] + *piVar1);
    FUN_0040de60(4);
LAB_007454c6:
    if ((*(char *)((int)piVar1 + 0x11) == '\0') || ((uint)piVar1[2] < piVar1[3] + 4U))
    goto LAB_007454e9;
    param_1_00[0x16] = *(undefined4 *)(piVar1[3] + *piVar1);
    FUN_0040de60(4);
  }
  if ((*(char *)((int)piVar1 + 0x11) != '\0') && (piVar1[3] + 1U <= (uint)piVar1[2])) {
    *(undefined *)(param_1_00 + 0x17) = *(undefined *)(piVar1[3] + *piVar1);
    FUN_0040de60(1);
    return *(undefined *)((int)param_1 + 0x11);
  }
LAB_00745522:
  *(undefined *)(param_1_00 + 0x17) = 0;
  if (*(char *)((int)piVar1 + 0x11) != '\0') {
    *(undefined *)((int)piVar1 + 0x11) = 0;
  }
  return *(undefined *)((int)param_1 + 0x11);
}

