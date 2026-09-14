// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x5f6e70L (requested via site 0x5f6e7a)

void __thiscall FUN_005f6e70(int *param_1_00,undefined4 param_1,undefined4 param_2)

{
  int iVar1;
  
  iVar1 = *param_1_00;
  if (iVar1 != 0) {
    FUN_004154f0(iVar1);
    FUN_00855dc0(iVar1);
  }
  *param_1_00 = 0;
  *(undefined *)(param_1_00 + 0xb) = 0;
  FUN_005f6de0(param_1,param_2);
  return;
}

