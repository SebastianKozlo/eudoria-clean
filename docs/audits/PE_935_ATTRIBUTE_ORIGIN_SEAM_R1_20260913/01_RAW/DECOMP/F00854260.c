
void FUN_00854260(undefined4 *param_1)

{
  undefined4 *puVar1;
  uint local_4;
  
  local_4 = 0xc;
  puVar1 = (undefined4 *)stlp_std::__node_alloc::allocate(&local_4);
  if (puVar1 + 1 != (undefined4 *)0x0) {
    puVar1[1] = *param_1;
    puVar1[2] = param_1[1];
  }
  *puVar1 = 0;
  return;
}

