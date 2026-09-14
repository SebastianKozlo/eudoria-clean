
undefined FUN_00752700(int *param_1,undefined4 *param_2,undefined4 *param_3,undefined *param_4,
                      undefined *param_5)

{
  if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U)) {
    *param_2 = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
      goto LAB_0075273c;
    }
LAB_00752762:
    *param_3 = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
      goto LAB_00752770;
    }
LAB_00752796:
    *param_4 = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
      goto LAB_007527a4;
    }
  }
  else {
    *param_2 = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
LAB_0075273c:
    if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U))
    goto LAB_00752762;
    *param_3 = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
LAB_00752770:
    if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 1U))
    goto LAB_00752796;
    *param_4 = *(undefined *)(param_1[3] + *param_1);
    FUN_0040de60(1);
LAB_007527a4:
    if ((*(char *)((int)param_1 + 0x11) != '\0') && (param_1[3] + 1U <= (uint)param_1[2])) {
      *param_5 = *(undefined *)(param_1[3] + *param_1);
      FUN_0040de60(1);
      goto LAB_007527c9;
    }
  }
  *param_5 = 0;
  if (*(char *)((int)param_1 + 0x11) != '\0') {
    *(undefined *)((int)param_1 + 0x11) = 0;
    return 0;
  }
LAB_007527c9:
  return *(undefined *)((int)param_1 + 0x11);
}

