
int __thiscall FUN_006cb370(int param_1_00,undefined4 param_1)

{
  int iVar1;
  int iVar2;
  undefined4 uVar3;
  int iVar4;
  int local_4;
  
  uVar3 = param_1;
  iVar1 = *(int *)(param_1_00 + 0x14);
  iVar4 = *(int *)(param_1_00 + 0x10);
  local_4 = param_1_00;
  while( true ) {
    if (iVar4 == iVar1) {
      return 0;
    }
    param_1 = uVar3;
    FUN_00971780(&local_4,&param_1);
    if ((local_4 != 0) && (iVar2 = *(int *)(*(int *)(local_4 + 8) + 4), iVar2 != 0)) break;
    iVar4 = iVar4 + 4;
  }
  return iVar2;
}

