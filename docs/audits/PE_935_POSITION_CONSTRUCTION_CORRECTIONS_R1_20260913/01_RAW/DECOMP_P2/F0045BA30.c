// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x45ba30L (requested via site 0x45ba6f)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 * __thiscall FUN_0045ba30(int param_1_00,undefined4 *param_1)

{
  float *pfVar1;
  undefined4 *puVar2;
  float *pfVar3;
  float10 fVar4;
  undefined4 uVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  
  puVar2 = param_1;
  *param_1 = 0;
  param_1[1] = 0;
  pfVar1 = (float *)(param_1 + 2);
  *pfVar1 = 0.0;
  if ((*(int *)(param_1_00 + 0x7c) != 0) && ((*(uint *)(param_1_00 + 0xc) & 0x400) == 0)) {
    FUN_00846840(*(int *)(param_1_00 + 0x7c),param_1);
    uVar6 = puVar2[1];
    uVar8 = 0;
    uVar7 = 0;
    uVar5 = *puVar2;
    FUN_004154f0(uVar5,uVar6,0,0);
    fVar4 = (float10)FUN_00853a80(uVar5,uVar6,uVar7,uVar8);
    param_1 = (undefined4 *)(_DAT_00b6fc18 + (float)fVar4);
    pfVar3 = (float *)&param_1;
    if (_DAT_00b6fc18 + (float)fVar4 <= *pfVar1) {
      pfVar3 = pfVar1;
    }
    *pfVar1 = *pfVar3;
    return puVar2;
  }
  *param_1 = *(undefined4 *)(param_1_00 + 0x10);
  param_1[1] = *(undefined4 *)(param_1_00 + 0x14);
  param_1[2] = *(undefined4 *)(param_1_00 + 0x18);
  *pfVar1 = *pfVar1 + (float)_DAT_00a7b278;
  return param_1;
}

