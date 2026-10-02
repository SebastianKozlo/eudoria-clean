
char __thiscall FUN_007046a0(int *param_1_00,int param_1,undefined4 *param_2)

{
  char cVar1;
  char cVar2;
  int iVar3;
  undefined4 uVar4;
  
  FUN_004124b0(param_2);
  cVar1 = *(char *)(param_1 + 0x11);
  if (cVar1 != '\0') {
    iVar3 = FUN_0073c870(*param_2,1);
    if (iVar3 == 0) {
      return '\0';
    }
    iVar3 = FUN_0070e100(param_2[1]);
    if (iVar3 == 0) {
      iVar3 = FUN_0070dc20(param_2[1],param_1,1);
      cVar1 = iVar3 != 0;
    }
    else {
      uVar4 = FUN_0075d8d0(param_1);
      cVar1 = FUN_00726900(uVar4,param_1);
    }
    if ((((cVar1 != '\0') && (*param_1_00 != 1)) && (*param_1_00 != 3)) &&
       (cVar2 = FUN_0070bf40(0x20), cVar2 != '\0')) {
      FUN_0070c2f0(iVar3,0xffff);
    }
  }
  return cVar1;
}

