// source: C4_CONSTRUCTION_TRACE.json :: W02_visual_ctor_006c0d50

undefined4 * __thiscall
FUN_006c0d50(undefined4 *param_1_00,undefined4 param_1,undefined4 param_2,undefined4 param_3)

{
  FUN_006c8f80(param_1,param_2,param_3);
  param_1_00[0x44] = 0;
  param_1_00[0x45] = 0;
  param_1_00[0x46] = 0;
  param_1_00[0x47] = 0;
  param_1_00[0x48] = 0;
  param_1_00[0x49] = 0;
  *(undefined *)(param_1_00 + 0x4a) = 0;
  *(undefined *)((int)param_1_00 + 0x12a) = 0;
  *param_1_00 = ArkModelManagerMain::vftable;
  *(undefined *)((int)param_1_00 + 0x129) = 1;
  return param_1_00;
}

