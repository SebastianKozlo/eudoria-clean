// source: C3_DECOMP.json :: R03_lookup2x_006c2bb0

void __fastcall FUN_006c2bb0(int param_1)

{
  int iVar1;
  undefined4 uVar2;
  
  iVar1 = *(int *)(param_1 + 0x14);
  if (iVar1 != 0) {
    FUN_0043a550(iVar1);
    FUN_0072f580(iVar1);
    return;
  }
  iVar1 = FUN_006b22d0();
  if (iVar1 == 0xd) {
    FUN_006c2700();
    return;
  }
  iVar1 = FUN_006b22d0();
  if (iVar1 == 0) {
    FUN_006c2750();
    return;
  }
  iVar1 = FUN_006b22d0();
  uVar2 = *(undefined4 *)("ClickTargetNode" + iVar1 * 0x10);
  FUN_0043a550(uVar2);
  FUN_0072f580(uVar2);
  return;
}

