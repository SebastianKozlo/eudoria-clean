// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x7576a0L (requested via site 0x7576d4)

undefined4 __thiscall FUN_007576a0(int param_1_00,undefined4 param_1)

{
  int *piVar1;
  int *piVar2;
  int *piVar3;
  char cVar4;
  uint uVar5;
  int *piVar6;
  int *local_64;
  int *local_60;
  int local_5c;
  float local_58;
  float local_54;
  float local_50;
  float local_4c;
  float local_48;
  float local_44;
  float local_40;
  float local_3c;
  float local_38;
  float local_34;
  float local_30;
  float local_2c;
  undefined4 local_28;
  undefined4 local_24;
  undefined4 local_20;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a17188;
  local_c = ExceptionList;
  uVar5 = DAT_00b9d8d0 ^ (uint)&stack0xffffff80;
  ExceptionList = &local_c;
  cVar4 = FUN_00755f90(param_1);
  if (cVar4 != '\0') {
    local_64 = (int *)0x0;
    local_60 = (int *)0x0;
    local_5c = 0;
    local_4 = 0;
    FUN_00757390(param_1_00 + 100,param_1_00,&local_64,uVar5);
    piVar3 = local_60;
    piVar2 = local_64;
    if (local_64 != local_60) {
      piVar6 = local_64 + 5;
      do {
        local_4c = (float)piVar6[-2];
        local_48 = (float)piVar6[-1];
        local_44 = (float)*piVar6;
        local_58 = (float)piVar6[-5];
        local_54 = (float)piVar6[-4];
        local_50 = (float)piVar6[-3];
        local_28 = 0;
        local_24 = 0;
        local_20 = 0;
        local_1c = 0;
        local_18 = 0;
        local_14 = 0;
        local_40 = local_58;
        local_3c = local_54;
        local_38 = local_50;
        local_34 = local_4c;
        local_30 = local_48;
        local_2c = local_44;
        FUN_0048b9b0();
        cVar4 = FUN_00755f90(param_1);
        if (cVar4 != '\0') {
          local_4 = 0xffffffff;
          if (piVar2 != (int *)0x0) {
            stlp_std::__node_alloc::deallocate(piVar2,((local_5c - (int)piVar2) / 0x4c) * 0x4c);
          }
          ExceptionList = local_c;
          return 1;
        }
        piVar1 = piVar6 + 0xe;
        piVar6 = piVar6 + 0x13;
      } while (piVar1 != piVar3);
    }
    local_4 = 0xffffffff;
    if (piVar2 != (int *)0x0) {
      stlp_std::__node_alloc::deallocate(piVar2,((local_5c - (int)piVar2) / 0x4c) * 0x4c);
    }
  }
  ExceptionList = local_c;
  return 0;
}

