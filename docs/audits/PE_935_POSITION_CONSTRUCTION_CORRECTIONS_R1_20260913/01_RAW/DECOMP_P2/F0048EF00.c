// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x48ef00L (requested via site 0x48ef8f)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 * __fastcall FUN_0048ef00(undefined4 *param_1)

{
  uint uVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 local_58;
  undefined4 local_54;
  undefined4 local_50;
  undefined4 local_4c;
  undefined4 local_48;
  undefined4 local_44;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  puStack_8 = &LAB_009a6a48;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&stack0xffffffa0;
  ExceptionList = &local_c;
  param_1[1] = 0;
  local_4 = 0;
  *param_1 = ArkMoveSubsystem::vftable;
  FUN_0040b980(uVar1);
  FUN_0085bf20(0x1e);
  local_58 = _DAT_00a7ba3c;
  uVar5 = 1;
  local_54 = _DAT_00a7ba3c;
  local_50 = _DAT_00a7ba3c;
  local_4c = _DAT_00a7ba38;
  local_48 = _DAT_00a7ba38;
  local_44 = _DAT_00a7ba38;
  uVar2 = FUN_0048bf90(&local_4c,&local_58);
  uVar4 = 60000;
  puVar3 = param_1;
  FUN_004154f0(param_1,60000,uVar2,uVar5);
  FUN_00855340(puVar3,uVar4,uVar2,uVar5);
  ExceptionList = local_c;
  return param_1;
}

