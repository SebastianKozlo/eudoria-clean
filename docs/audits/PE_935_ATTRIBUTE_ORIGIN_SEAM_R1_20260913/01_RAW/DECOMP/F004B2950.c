
void FUN_004b2950(undefined4 param_1,int param_2,int param_3)

{
  undefined4 uVar1;
  char cVar2;
  int local_c;
  undefined4 local_8;
  undefined4 local_4;
  
  if (param_2 == 0xac) {
    FUN_004b2270(param_3);
    return;
  }
  if (param_2 == 0xb2) {
    FUN_004b1c70(param_3);
    return;
  }
  FUN_004143f0();
  cVar2 = FUN_0042bc20();
  if (cVar2 != '\0') {
    FUN_004b18d0(param_2,param_3);
    return;
  }
  uVar1 = *(undefined4 *)(param_3 + 8);
  local_c = param_2;
  local_8 = FUN_0040e0d0();
  local_4 = uVar1;
  FUN_004b1890(&local_c);
  return;
}

