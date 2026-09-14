
void FUN_004574f0(int *param_1)

{
  short sVar1;
  int *piVar2;
  char cVar3;
  uint uVar4;
  undefined4 uVar5;
  undefined4 *puVar6;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  undefined local_24 [12];
  undefined local_18 [12];
  void *local_c;
  undefined *puStack_8;
  uint local_4;
  
  piVar2 = param_1;
  local_4 = 0xffffffff;
  puStack_8 = &LAB_0099fc68;
  local_c = ExceptionList;
  uVar4 = DAT_00b9d8d0 ^ (uint)&stack0xffffffc4;
  ExceptionList = &local_c;
  if (*(char *)((int)param_1 + 0x11) != '\0') {
    if ((uint)param_1[2] < param_1[3] + 4U) {
      if (*(char *)((int)param_1 + 0x11) != '\0') {
        *(undefined *)((int)param_1 + 0x11) = 0;
      }
    }
    else {
      FUN_0040de60(4);
    }
  }
  if (*(char *)((int)piVar2 + 0x11) != '\0') {
    if ((uint)piVar2[2] < piVar2[3] + 2U) {
      if (*(char *)((int)piVar2 + 0x11) != '\0') {
        *(undefined *)((int)piVar2 + 0x11) = 0;
      }
    }
    else {
      sVar1 = *(short *)(piVar2[3] + *piVar2);
      FUN_0040de60(2);
      if (sVar1 != 0) {
        if (sVar1 == 1) {
          uVar5 = FUN_00423c10(piVar2,&local_30,&param_1);
          FUN_00423c10(uVar5);
          if (*(char *)((int)piVar2 + 0x11) == '\0') {
            ExceptionList = local_c;
            return;
          }
          FUN_00452fe0(local_30,param_1);
          ExceptionList = local_c;
          return;
        }
        if ((((sVar1 != 2) && (sVar1 != 3)) && (sVar1 != 4)) && (sVar1 != 5)) {
          ExceptionList = local_c;
          return;
        }
        if ((*(char *)((int)piVar2 + 0x11) == '\0') || ((uint)piVar2[2] < piVar2[3] + 8U)) {
          local_2c = 0;
          local_28 = 0;
          if (*(char *)((int)piVar2 + 0x11) != '\0') {
            *(undefined *)((int)piVar2 + 0x11) = 0;
          }
        }
        else {
          puVar6 = (undefined4 *)(*piVar2 + piVar2[3]);
          local_2c = *puVar6;
          local_28 = puVar6[1];
          FUN_0040de60(8);
        }
        FUN_00843d40(uVar4);
        local_4 = 2;
        cVar3 = FUN_00525af0(piVar2);
        if (cVar3 != '\0') {
          FUN_00456c80(local_18,sVar1,&local_2c);
        }
        goto LAB_004576b3;
      }
    }
  }
  FUN_00843d40(uVar4);
  local_4 = 0;
  cVar3 = FUN_00525af0(piVar2);
  if (cVar3 != '\0') {
    FUN_00836a50();
    local_4 = CONCAT31(local_4._1_3_,1);
    cVar3 = FUN_004c47f0(piVar2);
    if (cVar3 != '\0') {
      FUN_00453ff0(local_24);
    }
    local_4 = local_4 & 0xffffff00;
    FUN_008e0110();
  }
LAB_004576b3:
  local_4 = 0xffffffff;
  FUN_008e0110();
  ExceptionList = local_c;
  return;
}

