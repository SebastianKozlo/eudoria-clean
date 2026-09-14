// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x48d220L (requested via site 0x48d255)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN_0048d220(int param_1)

{
  int *piVar1;
  float fVar2;
  char cVar3;
  undefined4 uVar4;
  int iVar5;
  undefined4 *puVar6;
  undefined4 *puVar7;
  int *piVar8;
  undefined *puVar9;
  undefined *puVar10;
  undefined local_40 [12];
  undefined local_34 [12];
  undefined4 local_28 [5];
  float local_14;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009a67e8;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  FUN_004143f0();
  FUN_007ce1e0();
  FUN_004154f0();
  cVar3 = FUN_00854570();
  if (cVar3 != '\0') {
    FUN_00414a70();
    uVar4 = FUN_008dc5a0();
    FUN_00414a70();
    FUN_008dc540();
    FUN_00930020();
    FUN_004143f0();
    FUN_0042bdb0();
    iVar5 = FUN_00401360();
    piVar1 = *(int **)(iVar5 + 100);
    FUN_0048cda0(*(undefined4 *)(param_1 + 0x10));
    FUN_00415370();
    FUN_0092f8b0();
    local_4 = 0;
    FUN_0090cf80();
    puVar10 = local_40;
    puVar9 = local_34;
    piVar8 = piVar1;
    FUN_0045b880(piVar1,puVar9,puVar10,uVar4);
    FUN_0094eac0(piVar8,puVar9,puVar10,uVar4);
    local_4 = 0xffffffff;
    if ((piVar1 != (int *)0x0) && (piVar1[1] = piVar1[1] + -1, piVar1[1] == 0)) {
      (**(code **)(*piVar1 + 4))();
    }
    fVar2 = (float)_PTR_00a7a618 * 0.0;
    FUN_00523720();
    iVar5 = FUN_00746560();
    if ((NAN(fVar2) || NAN(*(float *)(iVar5 + 0x14))) == (fVar2 == *(float *)(iVar5 + 0x14))) {
      FUN_00523720();
      puVar6 = (undefined4 *)FUN_00746560();
      puVar7 = local_28;
      for (iVar5 = 7; iVar5 != 0; iVar5 = iVar5 + -1) {
        *puVar7 = *puVar6;
        puVar6 = puVar6 + 1;
        puVar7 = puVar7 + 1;
      }
      local_14 = fVar2;
      FUN_00523720();
      FUN_009330d0();
    }
    FUN_004147f0();
    FUN_0044cee0();
    if (*(char *)(param_1 + 0x5c) != '\0') {
      FUN_0048c700();
      FUN_0048ca20();
    }
  }
  ExceptionList = local_c;
  return;
}

