// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x42c180L (requested via site 0x42c19b)

undefined4 __thiscall FUN_0042c180(int param_1_00,undefined4 *param_1)

{
  undefined uVar1;
  undefined4 *puVar2;
  undefined4 uVar3;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined local_c [12];
  
  puVar2 = &local_18;
  uVar3 = *(undefined4 *)(param_1_00 + 8);
  local_18 = 0;
  local_14 = 0;
  local_10 = 0;
  FUN_004154f0(uVar3,&local_18);
  uVar1 = FUN_00854720(uVar3,puVar2);
  puVar2 = (undefined4 *)FUN_0096c920(local_c,&local_18);
  *param_1 = *puVar2;
  param_1[1] = puVar2[1];
  uVar3 = puVar2[2];
  param_1[2] = uVar3;
  return CONCAT31((int3)((uint)uVar3 >> 8),uVar1);
}

