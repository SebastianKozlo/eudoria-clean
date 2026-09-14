// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x4124b0L (requested via site 0x4124b0)

void __thiscall FUN_004124b0(int *param_1_00,undefined4 *param_1)

{
  undefined4 *puVar1;
  
  if ((*(char *)((int)param_1_00 + 0x11) != '\0') && (param_1_00[3] + 8U <= (uint)param_1_00[2])) {
    puVar1 = (undefined4 *)(*param_1_00 + param_1_00[3]);
    *param_1 = *puVar1;
    param_1[1] = puVar1[1];
    FUN_0040de60();
    return;
  }
  *param_1 = 0;
  param_1[1] = 0;
  if (*(char *)((int)param_1_00 + 0x11) != '\0') {
    *(undefined *)((int)param_1_00 + 0x11) = 0;
  }
  return;
}

