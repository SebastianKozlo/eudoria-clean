// source: C6_DRIVER_SOURCES.json :: Y06_lazygetter_007376a0

undefined4 FUN_007376a0(void)

{
  int iVar1;
  undefined4 *puVar2;
  
  iVar1 = FUN_0070c180(6);
  if (((*(int *)(iVar1 + 4) != 0) && (*(int *)(iVar1 + 4) == 1)) &&
     ((*(byte *)(iVar1 + 0xc) & 1) == 0)) {
    puVar2 = (undefined4 *)FUN_004926e0();
    return *puVar2;
  }
  puVar2 = (undefined4 *)FUN_00977780();
  return *puVar2;
}

