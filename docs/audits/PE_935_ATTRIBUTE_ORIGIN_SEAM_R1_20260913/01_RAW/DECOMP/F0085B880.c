
int __thiscall FUN_0085b880(int param_1_00,undefined4 param_1,undefined4 param_2)

{
  FUN_0040bd20(param_1);
  FUN_0040bd20(param_2);
  QueryPerformanceCounter((LARGE_INTEGER *)(param_1_00 + 0x10));
  QueryPerformanceCounter((LARGE_INTEGER *)(param_1_00 + 0x18));
  *(undefined4 *)(param_1_00 + 0x20) = 0;
  return param_1_00;
}

