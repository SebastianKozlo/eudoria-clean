// source: C11_ORACLE_COUNTERPARTS.json :: O02_setname_007b67e0

void __thiscall FUN_007b67e0(int param_1_00,char *param_1)

{
  char cVar1;
  char *pcVar2;
  
  operator_delete__(*(void **)(param_1_00 + 0xc));
  if (param_1 != (char *)0x0) {
    pcVar2 = param_1;
    do {
      cVar1 = *pcVar2;
      pcVar2 = pcVar2 + 1;
    } while (cVar1 != '\0');
    pcVar2 = (char *)operator_new((uint)(pcVar2 + (1 - (int)(param_1 + 1))));
    *(char **)(param_1_00 + 0xc) = pcVar2;
    do {
      cVar1 = *param_1;
      *pcVar2 = cVar1;
      param_1 = param_1 + 1;
      pcVar2 = pcVar2 + 1;
    } while (cVar1 != '\0');
    return;
  }
  *(undefined4 *)(param_1_00 + 0xc) = 0;
  return;
}

