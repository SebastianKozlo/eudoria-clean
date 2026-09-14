
undefined4 __thiscall FUN_00856190(int param_1_00,undefined4 *param_1)

{
  undefined4 local_10;
  undefined4 *local_c;
  undefined local_8 [4];
  char local_4;
  
  if (param_1[0x1d] != 0) {
    FUN_00413440();
    local_10 = FUN_00414130();
    local_c = param_1;
    FUN_00856090(*(int *)(param_1_00 + 0x24) + 1);
    FUN_00854d90(local_8,&local_10);
    if (local_4 != '\0') {
      FUN_00413450();
      return 1;
    }
    (**(code **)*param_1)(1);
    FUN_00413450();
  }
  return 0;
}

