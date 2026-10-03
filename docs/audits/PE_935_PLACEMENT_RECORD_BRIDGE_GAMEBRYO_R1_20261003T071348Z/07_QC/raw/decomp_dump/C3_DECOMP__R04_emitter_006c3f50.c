// source: C3_DECOMP.json :: R04_emitter_006c3f50

void FUN_006c3f50(undefined4 param_1,int param_2)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_8;
  undefined4 local_4;
  
  FUN_0043a550(param_1);
  FUN_0072f580(param_1);
  local_8 = 0x66;
  local_4 = FUN_007ce1e0();
  iVar1 = param_2;
  puVar2 = *(undefined4 **)(param_2 + 4);
  if (puVar2 == *(undefined4 **)(param_2 + 8)) {
    FUN_006c2e00(puVar2,&local_8,&param_2,1,1);
  }
  else {
    if (puVar2 != (undefined4 *)0x0) {
      *puVar2 = 0x66;
      puVar2[1] = local_4;
    }
    *(int *)(param_2 + 4) = *(int *)(param_2 + 4) + 8;
  }
  puVar2 = (undefined4 *)FUN_0040b070();
  FUN_006c3640(&param_2,*puVar2,puVar2[1],iVar1,FUN_008bd720,local_4);
  return;
}

