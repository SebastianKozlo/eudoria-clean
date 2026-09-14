// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x42be30L (requested via site 0x42be44)

undefined4 * __thiscall FUN_0042be30(int param_1_00,undefined4 *param_1)

{
  char cVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  
  *param_1 = 0;
  param_1[1] = 0;
  param_1[2] = 0;
  uVar2 = *(undefined4 *)(param_1_00 + 8);
  puVar3 = param_1;
  FUN_004154f0(uVar2,param_1);
  cVar1 = FUN_008547a0(uVar2,puVar3);
  if (cVar1 == '\0') {
    *param_1 = DAT_00ba921c;
    param_1[1] = DAT_00ba9220;
    param_1[2] = DAT_00ba9224;
  }
  return param_1;
}

