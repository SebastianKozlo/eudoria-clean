// H03_extract_00823c10 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G5_LOOKUP_CLOSURE.json

int __thiscall
FUN_00823c10(int param_1_00,undefined4 *param_1,undefined4 param_3,undefined4 param_4)

{
  undefined4 *puVar1;
  char cVar2;
  uint uVar3;
  int iVar4;
  int unaff_EBX;
  int *piVar5;
  void *local_24;
  void *pvStack_20;
  undefined4 uStack_1c;
  undefined4 uStack_18;
  undefined uStack_13;
  void *local_c;
  undefined *puStack_8;
  undefined4 uStack_4;
  
  puVar1 = param_1;
  uStack_4 = 0xffffffff;
  puStack_8 = &LAB_00a236f8;
  local_c = ExceptionList;
  uVar3 = DAT_00b9d8d0 ^ (uint)&stack0xffffffc8;
  ExceptionList = &local_c;
  param_1 = (undefined4 *)*param_1;
  FUN_004d1430(&local_24,&param_1);
  if (local_24 == (void *)(param_1_00 + 4)) {
    param_1_00 = param_1_00 + 0x1c;
  }
  else {
    param_1_00 = (int)local_24 + 0x14;
  }
  if (*(int **)(param_1_00 + 0x24) != (int *)0x0) {
    (**(code **)(**(int **)(param_1_00 + 0x24) + 4))(uVar3);
    iVar4 = (**(code **)(**(int **)(param_1_00 + 0x24) + 0x38))(puVar1);
    if (iVar4 != 0) {
      *(undefined *)(*(int *)((int)ThreadLocalStoragePointer + _tls_index * 4) + 8) = 0;
LAB_00823e27:
      (**(code **)(**(int **)(param_1_00 + 0x24) + 8))();
      FUN_00826760(param_3,param_4);
      ExceptionList = local_c;
      return iVar4;
    }
    if ((*(char *)(param_1_00 + 0x38) == '\0') || (cVar2 = FUN_00822970(puVar1), cVar2 == '\0')) {
      uStack_1c = 0;
      uStack_18 = 0;
      FUN_0040e160(0x80,1);
      pvStack_20 = (void *)0x80;
      local_24 = operator_new(0x80);
      uStack_13 = 1;
      piVar5 = *(int **)(param_1_00 + 0x18);
      puStack_8 = (undefined *)0x0;
      if (piVar5 != *(int **)(param_1_00 + 0x1c)) {
        do {
          if ((int *)*piVar5 == (int *)0x0) {
            if (piVar5[2] != 0) {
LAB_00823d13:
              iVar4 = (**(code **)(*(int *)piVar5[2] + 4))(puVar1[1],&local_24);
              if (iVar4 != 0) {
                FUN_00826840(puVar1);
                (**(code **)(**(int **)(param_1_00 + 0x24) + 0x3c))(iVar4,uStack_1c);
                if (*(int *)(unaff_EBX + 0x58) != 0) {
                  (**(code **)(**(int **)(unaff_EBX + 0x58) + 4))(iVar4);
                }
                *(undefined *)(*(int *)((int)ThreadLocalStoragePointer + _tls_index * 4) + 8) = 1;
                puStack_8 = (undefined *)0xffffffff;
                cVar2 = FUN_0040e180(0x80);
                if (cVar2 != '\0') {
                  operator_delete__(local_24);
                }
                goto LAB_00823e27;
              }
              break;
            }
          }
          else {
            cVar2 = (**(code **)(*(int *)*piVar5 + 8))(puVar1,&local_24);
            if (cVar2 != '\0') {
              uStack_18 = 0;
              uStack_13 = 1;
              goto LAB_00823d13;
            }
          }
          piVar5 = piVar5 + 4;
        } while (piVar5 != *(int **)(param_1_00 + 0x1c));
      }
      if (*(char *)(param_1_00 + 0x38) != '\0') {
        FUN_008237d0(puVar1);
      }
      (**(code **)(**(int **)(param_1_00 + 0x24) + 8))();
      uStack_4 = 0xffffffff;
      cVar2 = FUN_0040e180(0x80);
      if (cVar2 != '\0') {
        operator_delete__(pvStack_20);
      }
      ExceptionList = local_c;
      return 0;
    }
    (**(code **)(**(int **)(param_1_00 + 0x24) + 8))();
  }
  ExceptionList = local_c;
  return 0;
}

