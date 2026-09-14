// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x42bdb0L (requested via site 0x42bdd6)

undefined4 * __thiscall FUN_0042bdb0(int param_1_00,undefined4 *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  
  *param_1 = DAT_00ba921c;
  param_1[1] = DAT_00ba9220;
  param_1[2] = DAT_00ba9224;
  iVar1 = *(int *)(param_1_00 + 8);
  if (iVar1 != 0) {
    puVar2 = param_1;
    FUN_004154f0(iVar1,param_1);
    FUN_00854620(iVar1,puVar2);
  }
  return param_1;
}

