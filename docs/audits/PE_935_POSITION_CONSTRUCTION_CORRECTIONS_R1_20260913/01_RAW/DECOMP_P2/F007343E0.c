// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x7343e0L (requested via site 0x7343e0)

int * FUN_007343e0(int *param_1,undefined4 *param_2)

{
  ushort uVar1;
  
  if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 2U)) {
    uVar1 = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
    }
  }
  else {
    uVar1 = *(ushort *)(param_1[3] + *param_1);
    FUN_0040de60(2);
  }
  if ((uVar1 & 2) == 0) {
    if ((uVar1 & 4) == 0) {
      FUN_004c32f0(param_1,param_2);
    }
    else {
      uVar1 = uVar1 & 0xfffb;
      *param_2 = 0x3f800000;
    }
  }
  else {
    uVar1 = uVar1 & 0xfffd;
    *param_2 = 0;
  }
  if ((uVar1 & 8) == 0) {
    if ((uVar1 & 0x10) == 0) {
      FUN_004c32f0(param_1,param_2 + 2);
    }
    else {
      uVar1 = uVar1 & 0xffef;
      param_2[2] = 0x3f800000;
    }
  }
  else {
    uVar1 = uVar1 & 0xfff7;
    param_2[2] = 0;
  }
  if ((uVar1 & 0x20) == 0) {
    if ((uVar1 & 0x40) == 0) {
      FUN_004c32f0(param_1,param_2 + 3);
    }
    else {
      uVar1 = uVar1 & 0xffbf;
      param_2[3] = 0x3f800000;
    }
  }
  else {
    uVar1 = uVar1 & 0xffdf;
    param_2[3] = 0;
  }
  if ((char)uVar1 < '\0') {
    uVar1 = uVar1 & 0xff7f;
    param_2[4] = 0;
  }
  else if ((uVar1 & 0x100) == 0) {
    FUN_004c32f0(param_1,param_2 + 4);
  }
  else {
    uVar1 = uVar1 & 0xfeff;
    param_2[4] = 0x3f800000;
  }
  if ((uVar1 & 0x200) == 0) {
    if ((uVar1 & 0x400) == 0) {
      FUN_004c32f0(param_1,param_2 + 5);
    }
    else {
      uVar1 = uVar1 & 0xfbff;
      param_2[5] = 0x3f800000;
    }
  }
  else {
    uVar1 = uVar1 & 0xfdff;
    param_2[5] = 0;
  }
  if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U)) {
    param_2[6] = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
      goto LAB_00734542;
    }
LAB_00734566:
    param_2[7] = 0;
    if (*(char *)((int)param_1 + 0x11) == '\0') goto LAB_007345a1;
    *(undefined *)((int)param_1 + 0x11) = 0;
  }
  else {
    param_2[6] = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
LAB_00734542:
    if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U))
    goto LAB_00734566;
    param_2[7] = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
  }
  if ((*(char *)((int)param_1 + 0x11) != '\0') && (param_1[3] + 4U <= (uint)param_1[2])) {
    param_2[8] = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
    *(ushort *)(param_2 + 9) = uVar1;
    return param_1;
  }
LAB_007345a1:
  param_2[8] = 0;
  if (*(char *)((int)param_1 + 0x11) != '\0') {
    *(undefined *)((int)param_1 + 0x11) = 0;
  }
  *(ushort *)(param_2 + 9) = uVar1;
  return param_1;
}

