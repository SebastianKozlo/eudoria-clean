// source: C3_DECOMP.json :: R16_attach_006cb4c0

void __fastcall FUN_006cb4c0(int param_1)

{
  int *piVar1;
  int *piVar2;
  
  piVar1 = *(int **)(param_1 + 0x14);
  for (piVar2 = *(int **)(param_1 + 0x10); piVar2 != piVar1; piVar2 = piVar2 + 1) {
    if (*(int *)(*piVar2 + 0x5c) != 0) {
      FUN_006cb3c0(*piVar2);
    }
  }
  return;
}

