// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x84a470L (requested via site 0x84a4b3)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

undefined4 FUN_0084a470(int *param_1,int param_2,undefined4 *param_3)

{
  char cVar1;
  int iVar2;
  float10 fVar3;
  int iVar4;
  undefined4 *puVar5;
  undefined4 local_38;
  undefined4 local_34;
  undefined4 local_30;
  undefined auStack_2c [32];
  void *local_c;
  undefined *puStack_8;
  int iStack_4;
  
  iStack_4 = 0xffffffff;
  puStack_8 = &LAB_00a28530;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  iVar4 = param_1[3];
  local_38 = 0;
  puVar5 = &local_38;
  local_34 = 0;
  local_30 = 0;
  FUN_004154f0(iVar4,puVar5,DAT_00b9d8d0 ^ (uint)&stack0xffffffb0);
  cVar1 = FUN_00854620(iVar4,puVar5);
  if (cVar1 == '\0') {
    ExceptionList = local_c;
    return 0;
  }
  if ((*(char *)(param_1 + 8) == '\0') && (fVar3 = (float10)_CIsqrt(), _DAT_00a91c80 < (float)fVar3)
     ) {
    *param_3 = 0x29d;
    ExceptionList = local_c;
    return 0;
  }
  FUN_00849d40(param_1 + 5,param_2);
  if (*(int *)(param_2 + 8) == 0x4e33) {
    *param_3 = 0x2b0;
    ExceptionList = local_c;
    return 0;
  }
  if (*(int *)(param_2 + 8) != 0x5dca) {
    if (*(int *)(param_2 + 4) == 0) {
      cVar1 = FUN_009768d0(0x2b7a);
      if (cVar1 == '\0') {
        *param_3 = 0;
        ExceptionList = local_c;
        return 1;
      }
      *param_3 = 0xb28;
      ExceptionList = local_c;
      return 0;
    }
    FUN_0057b140(*(int *)(param_2 + 4));
    iStack_4 = 0;
    if (param_1 != (int *)0x0) {
      iVar4 = *param_1;
      iVar2 = FUN_00726450();
      if (iVar2 == iVar4) {
        cVar1 = FUN_00751640(iVar4);
        if (cVar1 == '\0') {
          *param_3 = 0xb23;
        }
        else {
          FUN_00750fb0(auStack_2c);
          iStack_4._0_1_ = 1;
          cVar1 = FUN_00751850();
          iStack_4 = (uint)iStack_4._1_3_ << 8;
          FUN_008e0110();
          if (cVar1 == '\0') {
            cVar1 = FUN_009768d0(0x2bc5);
            if ((cVar1 == '\0') || (cVar1 = FUN_00751140(), cVar1 != '\0')) {
              *param_3 = 0;
              iStack_4 = 0xffffffff;
              FUN_00703bc0();
              ExceptionList = local_c;
              return 1;
            }
            *param_3 = 0xe4e;
          }
          else {
            *param_3 = 0x9ea;
          }
        }
      }
      else {
        *param_3 = 0xaf;
      }
    }
    iStack_4 = 0xffffffff;
    FUN_00703bc0();
    ExceptionList = local_c;
    return 0;
  }
  *param_3 = 0x2b0;
  ExceptionList = local_c;
  return 0;
}

