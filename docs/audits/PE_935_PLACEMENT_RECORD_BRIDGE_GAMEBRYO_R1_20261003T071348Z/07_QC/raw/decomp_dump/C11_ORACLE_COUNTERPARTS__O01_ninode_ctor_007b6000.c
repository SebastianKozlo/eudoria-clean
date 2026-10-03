// source: C11_ORACLE_COUNTERPARTS.json :: O01_ninode_ctor_007b6000

undefined4 * __thiscall FUN_007b6000(undefined4 *param_1_00,undefined4 param_1)

{
  undefined4 uVar1;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a1df54;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  FUN_007c02d0(DAT_00b9d8d0 ^ (uint)&stack0xffffffe8);
  local_4 = 0;
  *param_1_00 = NiNode::vftable;
  FUN_00788480(param_1,1);
  param_1_00[0x3b] = 0;
  param_1_00[0x39] = 0;
  param_1_00[0x3a] = 0;
  param_1_00[0x38] = NiTPointerList<class_NiDynamicEffect*>::vftable;
  param_1_00[0x3c] = DAT_00ba73a0;
  param_1_00[0x3d] = DAT_00ba73a4;
  uVar1 = DAT_00ba73a8;
  param_1_00[0x3f] = 0;
  local_4 = CONCAT31(local_4._1_3_,2);
  param_1_00[0x3e] = uVar1;
  FUN_007de000();
  ExceptionList = local_c;
  return param_1_00;
}

