
int * FUN_00730c90(int *param_1,undefined4 *param_2)

{
  if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U)) {
    *param_2 = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
      goto LAB_00730ccd;
    }
LAB_00730cf0:
    param_2[2] = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
      goto LAB_00730cfb;
    }
LAB_00730d1e:
    param_2[1] = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
      goto LAB_00730d29;
    }
LAB_00730d4c:
    param_2[3] = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
      goto LAB_00730d57;
    }
  }
  else {
    *param_2 = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
LAB_00730ccd:
    if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U))
    goto LAB_00730cf0;
    param_2[2] = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
LAB_00730cfb:
    if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U))
    goto LAB_00730d1e;
    param_2[1] = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
LAB_00730d29:
    if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U))
    goto LAB_00730d4c;
    param_2[3] = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
LAB_00730d57:
    if ((*(char *)((int)param_1 + 0x11) != '\0') && (param_1[3] + 4U <= (uint)param_1[2])) {
      param_2[4] = *(undefined4 *)(param_1[3] + *param_1);
      FUN_0040de60(4);
      goto LAB_00730d87;
    }
  }
  param_2[4] = 0;
  if (*(char *)((int)param_1 + 0x11) != '\0') {
    *(undefined *)((int)param_1 + 0x11) = 0;
  }
LAB_00730d87:
  FUN_00730b70(param_2 + 5);
  FUN_00730970(param_2 + 8);
  if ((*(char *)((int)param_1 + 0x11) != '\0') && (param_1[3] + 4U <= (uint)param_1[2])) {
    param_2[0xb] = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
    return param_1;
  }
  param_2[0xb] = 0;
  if (*(char *)((int)param_1 + 0x11) != '\0') {
    *(undefined *)((int)param_1 + 0x11) = 0;
  }
  return param_1;
}

