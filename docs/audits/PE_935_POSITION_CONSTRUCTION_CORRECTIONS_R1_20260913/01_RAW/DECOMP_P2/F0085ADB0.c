// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x85adb0L (requested via site 0x85adb0)

void __thiscall FUN_0085adb0(int *param_1_00,undefined4 param_1)

{
  undefined4 *puVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined local_64 [12];
  undefined4 local_58 [18];
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  undefined4 local_4;
  
  if (param_1_00[3] != 0) {
    if (*(int *)(param_1_00[3] + 0x20) == 3) {
      local_58[0] = 0x3f800000;
      local_58[1] = 0;
      local_58[2] = 0;
      local_58[3] = 0;
      local_58[5] = 0;
      local_58[6] = 0;
      local_58[7] = 0;
      local_58[4] = 0x3f800000;
      local_58[8] = 0x3f800000;
    }
    else {
      FUN_0096cdd0(param_1);
    }
    puVar1 = (undefined4 *)FUN_0085c0c0(local_64);
    puVar3 = local_58;
    puVar4 = local_58 + 9;
    for (iVar2 = 9; iVar2 != 0; iVar2 = iVar2 + -1) {
      *puVar4 = *puVar3;
      puVar3 = puVar3 + 1;
      puVar4 = puVar4 + 1;
    }
    local_10 = *puVar1;
    local_c = puVar1[1];
    local_8 = puVar1[2];
    local_4 = 0x3f800000;
    if (*(int *)(param_1_00[3] + 0x20) != 0) {
      FUN_0085cde0(local_58 + 9,1);
      (**(code **)(*param_1_00 + 0x2c))(param_1);
    }
  }
  return;
}

