// source: C7_LISTS_AND_ATTACH.json :: Z02_list2_init_00730970

/* WARNING: Removing unreachable block (ram,0x0073098a) */

void __thiscall FUN_00730970(int *param_1_00,int *param_1)

{
  undefined4 *puVar1;
  int *piVar2;
  uint uVar3;
  uint uVar4;
  
  piVar2 = param_1;
  if (*param_1 != param_1[1]) {
    param_1[1] = *param_1;
  }
  uVar3 = 0;
  if ((*(char *)((int)param_1_00 + 0x11) == '\0') || ((uint)param_1_00[2] < param_1_00[3] + 2U)) {
    uVar4 = 0;
    if (*(char *)((int)param_1_00 + 0x11) != '\0') {
      *(undefined *)((int)param_1_00 + 0x11) = 0;
    }
  }
  else {
    uVar4 = (uint)*(ushort *)(param_1_00[3] + *param_1_00);
    FUN_0040de60(2);
  }
  if (uVar4 != 0) {
    do {
      if (*(char *)((int)param_1_00 + 0x11) == '\0') {
        return;
      }
      if ((uint)param_1_00[2] < param_1_00[3] + 4U) {
        *(undefined *)((int)param_1_00 + 0x11) = 0;
        param_1 = (int *)0x0;
      }
      else {
        param_1 = *(int **)(param_1_00[3] + *param_1_00);
        FUN_0040de60(4);
      }
      puVar1 = (undefined4 *)piVar2[1];
      if (puVar1 == (undefined4 *)piVar2[2]) {
        FUN_00445780(puVar1,&param_1,&param_1,1,1);
      }
      else {
        if (puVar1 != (undefined4 *)0x0) {
          *puVar1 = param_1;
        }
        piVar2[1] = piVar2[1] + 4;
      }
      uVar3 = uVar3 + 1;
    } while (uVar3 < uVar4);
  }
  return;
}

