// source: C6_DRIVER_SOURCES.json :: Y04_dynfactory_006a34a0

void __fastcall FUN_006a34a0(int param_1)

{
  int iVar1;
  
  if (*(int *)(param_1 + 0x10) != 0) {
    iVar1 = 2;
    do {
      FUN_006a2f60();
      iVar1 = iVar1 + -1;
    } while (iVar1 != 0);
    *(int *)(param_1 + 0x10) = *(int *)(param_1 + 0x10) + -1;
  }
  return;
}

