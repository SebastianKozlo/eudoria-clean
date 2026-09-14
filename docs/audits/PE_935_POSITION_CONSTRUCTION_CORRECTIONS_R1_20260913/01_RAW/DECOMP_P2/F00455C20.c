// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x455c20L (requested via site 0x455cb3)

void __fastcall FUN_00455c20(int *param_1)

{
  int iVar1;
  void *pvVar2;
  undefined4 *puVar3;
  undefined4 *puVar4;
  undefined4 uVar5;
  undefined4 local_38 [2];
  undefined4 *local_30;
  undefined4 *local_2c;
  int local_28;
  undefined local_24 [4];
  void *local_20;
  undefined *local_1c;
  undefined *local_18;
  int local_14;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_0099f940;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  FUN_00453cf0(DAT_00b9d8d0 ^ (uint)&stack0xffffffb8);
  local_30 = (undefined4 *)0x0;
  local_2c = (undefined4 *)0x0;
  local_28 = 0;
  iVar1 = *param_1;
  local_4 = 0;
  FUN_00413440();
  FUN_0070cd50(local_38,*(undefined4 *)(iVar1 + 0x20),iVar1 + 0x18,&local_30,local_38[0]);
  FUN_00413450();
  puVar3 = local_2c;
  for (puVar4 = local_30; puVar4 != puVar3; puVar4 = puVar4 + 1) {
    uVar5 = *puVar4;
    FUN_004154f0(uVar5);
    FUN_00855dc0(uVar5);
  }
  FUN_004555b0(param_1 + 0x54);
  local_4._0_1_ = 1;
  FUN_00453bc0(local_38,local_1c,local_24,FUN_004544a0,param_1);
  local_4 = (uint)local_4._1_3_ << 8;
  if (local_14 != 0) {
    while (local_20 != (void *)0x0) {
      FUN_00857f50(*(undefined4 *)((int)local_20 + 0xc));
      pvVar2 = *(void **)((int)local_20 + 8);
      stlp_std::__node_alloc::deallocate(local_20,0x14);
      local_20 = pvVar2;
    }
    local_1c = local_24;
    local_20 = (void *)0x0;
    local_14 = 0;
    local_18 = local_1c;
  }
  local_4 = 0xffffffff;
  if (local_30 != (undefined4 *)0x0) {
    stlp_std::__node_alloc::deallocate(local_30,(local_28 - (int)local_30 >> 2) * 4);
  }
  ExceptionList = local_c;
  return;
}

