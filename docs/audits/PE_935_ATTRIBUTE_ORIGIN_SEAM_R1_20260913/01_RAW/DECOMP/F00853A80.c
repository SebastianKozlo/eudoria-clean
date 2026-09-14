
float10 __thiscall
FUN_00853a80(int *param_1_00,undefined4 param_1,undefined4 param_2,int param_3,undefined4 param_4)

{
  char cVar1;
  float10 fVar2;
  undefined4 local_c;
  undefined4 local_8;
  float local_4;
  
  local_c = param_1;
  local_8 = param_2;
  local_4 = 0.0;
  cVar1 = FUN_00755f90(&local_c);
  if (cVar1 == '\0') {
    return (float10)0;
  }
  if (param_1_00[0x13] != 0) {
    local_c = param_1;
    local_8 = param_2;
    (**(code **)(*(int *)param_1_00[0x13] + 4))(&local_c,param_4);
  }
  if (*param_1_00 != 0) {
    FUN_00413440();
    local_c = param_1;
    local_8 = param_2;
    if (param_3 != 0) {
      fVar2 = (float10)(**(code **)(*(int *)*param_1_00 + 4))(&local_c,param_3);
      local_4 = (float)fVar2;
      FUN_00413450();
      return (float10)local_4;
    }
    fVar2 = (float10)(**(code **)(*(int *)*param_1_00 + 4))(&local_c,0);
    local_4 = (float)fVar2;
    FUN_00413450();
    return (float10)local_4;
  }
  return (float10)0.0;
}

