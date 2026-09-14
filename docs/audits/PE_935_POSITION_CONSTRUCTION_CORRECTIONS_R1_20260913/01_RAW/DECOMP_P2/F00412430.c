// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x412430L (requested via site 0x412430)

void __thiscall FUN_00412430(int *param_1_00,undefined4 *param_1)

{
  undefined4 *puVar1;
  
  if ((*(char *)((int)param_1_00 + 0x11) != '\0') && (param_1_00[3] + 0xcU <= (uint)param_1_00[2]))
  {
    puVar1 = (undefined4 *)(*param_1_00 + param_1_00[3]);
    *param_1 = *puVar1;
    param_1[1] = puVar1[1];
    param_1[2] = puVar1[2];
    FUN_0040de60();
    return;
  }
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  if (*(char *)((int)param_1_00 + 0x11) != '\0') {
    *(undefined *)((int)param_1_00 + 0x11) = 0;
  }
  return;
}

