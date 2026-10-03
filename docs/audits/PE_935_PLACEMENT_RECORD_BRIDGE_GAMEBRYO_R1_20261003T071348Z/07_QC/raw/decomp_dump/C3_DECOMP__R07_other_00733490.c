// source: C3_DECOMP.json :: R07_other_00733490

undefined __fastcall FUN_00733490(int param_1)

{
  char cVar1;
  uint uVar2;
  undefined4 uVar3;
  int iVar4;
  int iVar5;
  int *piVar6;
  undefined local_1d;
  int local_1c;
  undefined4 local_14 [2];
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a129b8;
  local_c = ExceptionList;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xffffffd0;
  ExceptionList = &local_c;
  local_1d = 1;
  piVar6 = (int *)(param_1 + 0x14);
  iVar5 = 3;
  do {
    if ((*piVar6 == 0) && (piVar6[-2] != 0)) {
      FUN_00976770(0x3d35,piVar6[-2]);
      local_14[0] = 0x4e26;
      FUN_00703b80(local_14);
      local_4 = 0;
      if (local_1c == 0) {
LAB_0073352d:
        local_1d = 0;
      }
      else {
        uVar3 = FUN_007376a0(uVar2);
        FUN_0043a550(uVar3);
        iVar4 = FUN_0072f580(uVar3);
        cVar1 = FUN_0072fce0();
        if (cVar1 == '\0') goto LAB_0073352d;
        *piVar6 = iVar4;
      }
      local_4 = 0xffffffff;
      FUN_00703bc0();
    }
    piVar6 = piVar6 + 6;
    iVar5 = iVar5 + -1;
    if (iVar5 == 0) {
      ExceptionList = local_c;
      return local_1d;
    }
  } while( true );
}

