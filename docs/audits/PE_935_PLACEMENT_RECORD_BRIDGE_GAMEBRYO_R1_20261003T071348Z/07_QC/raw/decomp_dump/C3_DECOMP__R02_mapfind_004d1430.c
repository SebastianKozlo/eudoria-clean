// source: C3_DECOMP.json :: R02_mapfind_004d1430

void __thiscall FUN_004d1430(int param_1_00,int *param_1,uint *param_2)

{
  int iVar1;
  int iVar2;
  int iVar3;
  
  if (*(int *)(param_1_00 + 4) == 0) {
    *param_1 = param_1_00;
    return;
  }
  iVar1 = *(int *)(param_1_00 + 4);
  iVar3 = param_1_00;
  do {
    if (*(uint *)(iVar1 + 0x10) < *param_2) {
      iVar2 = *(int *)(iVar1 + 0xc);
    }
    else {
      iVar2 = *(int *)(iVar1 + 8);
      iVar3 = iVar1;
    }
    iVar1 = iVar2;
  } while (iVar2 != 0);
  if ((iVar3 != param_1_00) && (*param_2 < *(uint *)(iVar3 + 0x10))) {
    *param_1 = param_1_00;
    return;
  }
  *param_1 = iVar3;
  return;
}

