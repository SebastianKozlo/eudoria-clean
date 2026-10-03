// source: C7_LISTS_AND_ATTACH.json :: Z09_emitter_caller_006c4020

void FUN_006c4020(undefined4 *param_1,undefined4 param_2)

{
  undefined4 *puVar1;
  int iVar2;
  
  iVar2 = 2;
  do {
    puVar1 = param_1 + 1;
    for (; param_1 != puVar1; param_1 = param_1 + 1) {
      FUN_006c3f50(*param_1,param_2);
    }
    iVar2 = iVar2 + -1;
    param_1 = puVar1;
  } while (iVar2 != 0);
  return;
}

