// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x5f5870L (requested via site 0x5f587a)

void __fastcall FUN_005f5870(int *param_1)

{
  int iVar1;
  
  iVar1 = *param_1;
  if (iVar1 != 0) {
    FUN_004154f0(iVar1);
    FUN_00855dc0(iVar1);
  }
  *(undefined *)(param_1 + 0xb) = 0;
  *param_1 = 0;
  return;
}

