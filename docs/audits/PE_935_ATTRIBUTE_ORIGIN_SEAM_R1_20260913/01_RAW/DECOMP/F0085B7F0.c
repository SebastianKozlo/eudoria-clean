
undefined4 * __thiscall FUN_0085b7f0(undefined4 *param_1_00,byte param_1)

{
  void *pvVar1;
  
  pvVar1 = (void *)param_1_00[0xf];
  *param_1_00 = MovableObject::vftable;
  if (pvVar1 != (void *)0x0) {
    thunk_FUN_008e0110();
    operator_delete(pvVar1);
  }
  pvVar1 = (void *)param_1_00[0x10];
  if (pvVar1 != (void *)0x0) {
    thunk_FUN_008e0110();
    operator_delete(pvVar1);
  }
  if ((param_1 & 1) != 0) {
    operator_delete(param_1_00);
  }
  return param_1_00;
}

