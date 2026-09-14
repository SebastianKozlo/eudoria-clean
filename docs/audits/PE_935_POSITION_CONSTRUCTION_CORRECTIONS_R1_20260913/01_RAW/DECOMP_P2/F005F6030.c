// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x5f6030L (requested via site 0x5f603a)

void __fastcall FUN_005f6030(int *param_1)

{
  int iVar1;
  
  iVar1 = *param_1;
  if (iVar1 != 0) {
    FUN_004154f0(iVar1);
    FUN_00855dc0(iVar1);
  }
  iVar1 = param_1[1];
  *param_1 = 0;
  *(undefined *)(param_1 + 0xb) = 0;
  if (iVar1 != 0) {
    FUN_00401360(iVar1);
    FUN_00485050();
    FUN_0048cc20(iVar1);
  }
  if ((undefined4 *)param_1[4] != (undefined4 *)0x0) {
    (*(code *)**(undefined4 **)param_1[4])(1);
  }
  return;
}

