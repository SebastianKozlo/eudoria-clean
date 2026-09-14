// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x85b780L (requested via site 0x85b783)

undefined4 __fastcall FUN_0085b780(int param_1)

{
  short sVar1;
  short sVar2;
  int iVar3;
  bool bVar4;
  bool bVar5;
  
  FUN_004154f0();
  iVar3 = FUN_007ce1e0();
  if (iVar3 != 1) {
    iVar3 = *(int *)(param_1 + 8);
    if (iVar3 == 3) {
      *(short *)(param_1 + 0xa0) = *(short *)(param_1 + 0xa0) + 1;
      sVar1 = *(short *)(param_1 + 0xa0);
      bVar5 = SBORROW2(sVar1,5);
      sVar2 = sVar1 + -5;
      bVar4 = sVar1 == 5;
    }
    else {
      if ((((iVar3 != 6) && (iVar3 != 5)) && (iVar3 != 4)) && (iVar3 != 7)) {
        return 1;
      }
      *(short *)(param_1 + 0xa0) = *(short *)(param_1 + 0xa0) + 1;
      bVar5 = SBORROW2(*(short *)(param_1 + 0xa0),0x14);
      sVar2 = *(short *)(param_1 + 0xa0) + -0x14;
      bVar4 = sVar2 == 0;
    }
    if (bVar4 || bVar5 != sVar2 < 0) {
      return 0;
    }
    *(undefined2 *)(param_1 + 0xa0) = 0;
  }
  return 1;
}

