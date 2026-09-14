
undefined FUN_00752640(int *param_1,undefined4 *param_2,undefined4 *param_3,undefined *param_4)

{
  if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U)) {
    *param_2 = 0;
    if (*(char *)((int)param_1 + 0x11) != '\0') {
      *(undefined *)((int)param_1 + 0x11) = 0;
      goto LAB_00752680;
    }
LAB_007526a7:
    *param_3 = 0;
    if (*(char *)((int)param_1 + 0x11) == '\0') goto LAB_007526e6;
    *(undefined *)((int)param_1 + 0x11) = 0;
  }
  else {
    *param_2 = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
LAB_00752680:
    if ((*(char *)((int)param_1 + 0x11) == '\0') || ((uint)param_1[2] < param_1[3] + 4U))
    goto LAB_007526a7;
    *param_3 = *(undefined4 *)(param_1[3] + *param_1);
    FUN_0040de60(4);
  }
  if ((*(char *)((int)param_1 + 0x11) != '\0') && (param_1[3] + 1U <= (uint)param_1[2])) {
    *param_4 = *(undefined *)(param_1[3] + *param_1);
    FUN_0040de60(1);
    return *(undefined *)((int)param_1 + 0x11);
  }
LAB_007526e6:
  *param_4 = 0;
  if (*(char *)((int)param_1 + 0x11) != '\0') {
    *(undefined *)((int)param_1 + 0x11) = 0;
  }
  return *(undefined *)((int)param_1 + 0x11);
}

