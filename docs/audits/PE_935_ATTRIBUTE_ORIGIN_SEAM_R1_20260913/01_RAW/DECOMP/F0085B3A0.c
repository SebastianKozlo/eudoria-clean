
void __fastcall FUN_0085b3a0(undefined4 *param_1)

{
  void *pvVar1;
  
  pvVar1 = (void *)param_1[0xf];
  *param_1 = MovableObject::vftable;
  if (pvVar1 != (void *)0x0) {
    thunk_FUN_008e0110();
    operator_delete(pvVar1);
  }
  pvVar1 = (void *)param_1[0x10];
  if (pvVar1 != (void *)0x0) {
    thunk_FUN_008e0110();
    operator_delete(pvVar1);
  }
  return;
}

