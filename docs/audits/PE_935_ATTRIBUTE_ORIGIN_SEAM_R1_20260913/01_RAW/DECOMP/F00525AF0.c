
undefined __thiscall FUN_00525af0(int *param_1_00,int param_1)

{
  char cVar1;
  undefined uVar2;
  int iVar3;
  undefined4 uVar4;
  undefined local_3c [48];
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009bf088;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  FUN_00747e20(DAT_00b9d8d0 ^ (uint)&stack0xffffffb8);
  local_4 = 0;
  FUN_00748480(param_1,local_3c);
  cVar1 = *(char *)(param_1 + 0x11);
  *(char *)(param_1_00 + 2) = cVar1;
  if (cVar1 == '\0') goto LAB_00525b63;
  if (*param_1_00 == 0) {
LAB_00525b5b:
    uVar2 = 1;
  }
  else {
    iVar3 = FUN_004123d0();
    if (*param_1_00 == iVar3) goto LAB_00525b5b;
    uVar2 = 0;
  }
  *(undefined *)(param_1_00 + 2) = uVar2;
LAB_00525b63:
  if (*(char *)(param_1_00 + 2) != '\0') {
    iVar3 = FUN_004123d0();
    *param_1_00 = iVar3;
    uVar4 = FUN_004123d0();
    iVar3 = FUN_00841920(uVar4);
    param_1_00[1] = iVar3;
    if (iVar3 == 0) {
      iVar3 = FUN_00842c30(local_3c);
      param_1_00[1] = iVar3;
      *(byte *)(param_1_00 + 2) = *(byte *)(param_1_00 + 2) & iVar3 != 0;
    }
    else {
      FUN_00842d40(iVar3,local_3c);
    }
  }
  uVar2 = *(undefined *)(param_1_00 + 2);
  local_4 = 0xffffffff;
  FUN_00747e40();
  ExceptionList = local_c;
  return uVar2;
}

