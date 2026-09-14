// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x5f71e0L (requested via site 0x5f7232)

int * __thiscall
FUN_005f71e0(int *param_1_00,int *param_1,undefined4 param_2,int *param_3,undefined4 param_4)

{
  int *piVar1;
  int *piVar2;
  uint uVar3;
  int *piVar4;
  int iVar5;
  undefined4 uVar6;
  undefined4 local_14;
  undefined4 local_10;
  void *local_c;
  undefined *puStack_8;
  uint local_4;
  
  puStack_8 = &LAB_009e0cc1;
  local_c = ExceptionList;
  uVar3 = DAT_00b9d8d0 ^ (uint)&stack0xffffffdc;
  ExceptionList = &local_c;
  local_4 = 0;
  local_14 = 0;
  local_10 = 0;
  FUN_005f58a0(&local_14,param_3);
  iVar5 = *param_1_00;
  if (iVar5 != 0) {
    FUN_004154f0(iVar5,uVar3);
    FUN_00855dc0(iVar5);
  }
  *param_1_00 = 0;
  *(undefined *)(param_1_00 + 0xb) = 0;
  FUN_005f6de0(param_2,1);
  iVar5 = param_1_00[1];
  uVar6 = 0;
  FUN_00401360(iVar5,0);
  FUN_00485050();
  FUN_0048cbb0(iVar5);
  FUN_00525ae0(uVar6);
  FUN_008ddf90(param_1,param_4,2);
  local_4 = 0;
  if (*param_1 == 0) {
    piVar4 = (int *)FUN_006ba150(&param_3,0x84996);
    piVar2 = (int *)*param_1;
    local_4 = 1;
    if (piVar2 != (int *)*piVar4) {
      if (piVar2 != (int *)0x0) {
        piVar1 = piVar2 + 1;
        *piVar1 = *piVar1 + -1;
        if (*piVar1 == 0) {
          (**(code **)(*piVar2 + 4))();
        }
      }
      iVar5 = *piVar4;
      *param_1 = iVar5;
      if (iVar5 != 0) {
        *(int *)(iVar5 + 4) = *(int *)(iVar5 + 4) + 1;
      }
    }
    local_4 = local_4 & 0xffffff00;
    if ((param_3 != (int *)0x0) && (param_3[1] = param_3[1] + -1, param_3[1] == 0)) {
      (**(code **)(*param_3 + 4))();
    }
  }
  ExceptionList = local_c;
  return param_1;
}

