// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x84a090L (requested via site 0x84a129)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_0084a090(int *param_1,int param_2,undefined4 *param_3)

{
  bool bVar1;
  char cVar2;
  uint uVar3;
  int *piVar4;
  int iVar5;
  float10 fVar6;
  uint *puVar7;
  float *pfVar8;
  float local_5c;
  uint local_58;
  float local_54;
  float local_50;
  int local_4c;
  int local_48;
  float local_44;
  float local_40;
  float local_3c;
  float local_38;
  float local_34;
  float local_30;
  undefined auStack_2c [32];
  void *local_c;
  undefined *puStack_8;
  undefined4 uStack_4;
  
  uStack_4 = 0xffffffff;
  puStack_8 = &LAB_00a284f8;
  local_c = ExceptionList;
  uVar3 = DAT_00b9d8d0 ^ (uint)&stack0xffffff98;
  ExceptionList = &local_c;
  iVar5 = param_1[1];
  FUN_004154f0(iVar5,uVar3);
  local_58 = FUN_00854520(iVar5);
  if (local_58 == 0) {
    ExceptionList = local_c;
    return 0;
  }
  local_38 = *(float *)(local_58 + 0x44);
  local_34 = *(float *)(local_58 + 0x48);
  local_30 = *(float *)(local_58 + 0x4c);
  piVar4 = (int *)FUN_0085ad50();
  local_4c = *piVar4;
  local_48 = piVar4[1];
  puVar7 = &local_58;
  FUN_004154f0(puVar7,uVar3);
  FUN_00853a60(puVar7);
  iVar5 = param_1[3];
  local_44 = 0.0;
  pfVar8 = &local_44;
  local_40 = 0.0;
  local_3c = 0.0;
  FUN_004154f0(iVar5,pfVar8);
  cVar2 = FUN_00854620(iVar5,pfVar8);
  if (cVar2 == '\0') {
    ExceptionList = local_c;
    return 0;
  }
  if (*(char *)(param_1 + 8) == '\0') {
    local_54 = local_44 - local_38;
    local_5c = local_40 - local_34;
    local_50 = (local_3c - local_30) * (local_3c - local_30) +
               local_54 * local_54 + local_5c * local_5c;
    fVar6 = (float10)_CIsqrt();
    local_50 = (float)fVar6;
    if (_DAT_00a7b128 < local_50) {
      *param_3 = 0x29c;
      ExceptionList = local_c;
      return 0;
    }
  }
  if (local_4c == 0x4e34) {
    ExceptionList = local_c;
    return 1;
  }
  if (param_1[4] == 1) {
    if ((param_1[1] != 0) && ((uint)param_1[1] < 4000000)) {
      *param_3 = 0x277;
      ExceptionList = local_c;
      return 0;
    }
    cVar2 = FUN_009768d0(0x159);
    if ((cVar2 == '\0') && (local_4c != 0x4e37)) {
      *param_3 = 0x277;
      ExceptionList = local_c;
      return 0;
    }
  }
  if (local_4c == 0x5dc9) {
    FUN_00439080(local_48);
    uStack_4 = 0;
    if ((local_5c != 0.0) && (cVar2 = FUN_0072d390(), cVar2 != '\0')) goto LAB_0084a445;
LAB_0084a2a9:
    uStack_4 = 0xffffffff;
    FUN_00703bc0();
  }
  else if (local_4c == 0x4e24) {
    FUN_00608ea0(local_48);
    uStack_4 = 1;
    iVar5 = FUN_00726450();
    if (iVar5 == *param_1) goto LAB_0084a445;
    goto LAB_0084a2a9;
  }
  FUN_00849d40(&local_38,param_2);
  if (*(int *)(param_2 + 4) == 0) {
    ExceptionList = local_c;
    return 1;
  }
  FUN_0057b140(*(int *)(param_2 + 4));
  uStack_4 = 2;
  if (param_1 != (int *)0x0) {
    if (((param_1[4] == 3) || (param_1[4] == 1)) && (iVar5 = FUN_00726450(), iVar5 != *param_1)) {
      *param_3 = 0xae;
    }
    else {
      if (((local_4c == 0x4e46) || (local_4c == 0x2b7b)) && (param_1[4] == 0)) {
        bVar1 = true;
      }
      else {
        bVar1 = false;
      }
      cVar2 = FUN_00751640(*param_1);
      if ((cVar2 != '\0') || (bVar1)) {
        FUN_00750fb0(auStack_2c);
        uStack_4._0_1_ = 3;
        cVar2 = FUN_00751850();
        uStack_4 = CONCAT31(uStack_4._1_3_,2);
        FUN_008e0110();
        if (cVar2 == '\0') {
          if ((*(char *)((int)param_1 + 0x21) == '\0') || (cVar2 = FUN_00751190(), cVar2 != '\0')) {
            if (local_4c == 0x4e46) {
              FUN_004b0c90(&local_4c);
              uStack_4._0_1_ = 4;
              if ((((param_2 != 0) && (cVar2 = FUN_0072f3d0(), cVar2 != '\0')) && (param_1[4] == 0))
                 && (cVar2 = FUN_00751140(), cVar2 == '\0')) {
                *param_3 = 0xe4f;
                uStack_4 = CONCAT31(uStack_4._1_3_,2);
                FUN_00703bc0();
                goto LAB_0084a310;
              }
              uStack_4 = CONCAT31(uStack_4._1_3_,2);
              FUN_00703bc0();
            }
LAB_0084a445:
            uStack_4 = 0xffffffff;
            FUN_00703bc0();
            ExceptionList = local_c;
            return 1;
          }
          *param_3 = 0x7d6;
        }
        else {
          *param_3 = 0x9ea;
        }
      }
      else {
        *param_3 = 0xb23;
      }
    }
  }
LAB_0084a310:
  uStack_4 = 0xffffffff;
  FUN_00703bc0();
  ExceptionList = local_c;
  return 0;
}

