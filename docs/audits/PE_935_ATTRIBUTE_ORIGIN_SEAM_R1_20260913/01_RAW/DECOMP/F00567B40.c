
void __thiscall
FUN_00567b40(int param_1_00,undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  char cVar1;
  int iVar2;
  int iVar3;
  undefined4 uVar4;
  undefined4 uVar5;
  undefined4 *puVar6;
  undefined4 *puVar7;
  undefined4 local_1c;
  undefined4 local_18;
  undefined4 local_14;
  undefined4 local_10;
  undefined4 local_c;
  undefined4 local_8;
  int local_4;
  
  FUN_004143f0();
  iVar2 = FUN_007ce1e0();
  iVar3 = FUN_00844130();
  FUN_00443580();
  local_4 = *(int *)(param_1_00 + 0x50);
  local_c = *(undefined4 *)(param_1_00 + 0x48);
  if (((uint)((*(int *)(param_1_00 + 0x54) - *(int *)(param_1_00 + 0x58) >> 3) +
              ((*(int *)(param_1_00 + 0x60) - local_4 >> 2) + -1) * 0x10 +
             (*(int *)(param_1_00 + 0x4c) - *(int *)(param_1_00 + 0x44) >> 3)) <=
       *(uint *)(param_1_00 + 0x40)) || (iVar2 == iVar3)) {
    uVar4 = FUN_0040b980();
    if (*(int *)(param_1_00 + 0x54) == *(int *)(param_1_00 + 0x5c) + -8) {
      FUN_00443310(uVar4);
    }
    else {
      FUN_00442ba0(*(int *)(param_1_00 + 0x54));
      *(int *)(param_1_00 + 0x54) = *(int *)(param_1_00 + 0x54) + 8;
    }
    local_10 = 0;
    local_c = 0;
    puVar7 = &local_1c;
    local_8 = 0;
    local_1c = 0;
    puVar6 = &local_10;
    local_18 = 0;
    local_14 = 0;
    uVar4 = param_2;
    uVar5 = FUN_00844130(param_2,param_3,puVar6,puVar7);
    cVar1 = FUN_00566100(uVar5,uVar4,param_3,puVar6,puVar7);
    if (cVar1 != '\0') {
      FUN_00567170(param_2,param_1,&local_10,&local_1c,iVar2 == iVar3);
    }
  }
  return;
}

