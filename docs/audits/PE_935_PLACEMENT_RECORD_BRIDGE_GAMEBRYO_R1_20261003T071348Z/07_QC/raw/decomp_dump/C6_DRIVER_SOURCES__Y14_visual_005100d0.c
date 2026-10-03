// source: C6_DRIVER_SOURCES.json :: Y14_visual_005100d0

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_005100d0(undefined4 param_1,char param_2,undefined4 param_3,int *param_4,float param_5)

{
  allocator<char> *paVar1;
  int iVar2;
  void *pvVar3;
  undefined *puStack_d4;
  undefined auStack_b4 [3];
  allocator<char> local_b1;
  int *local_b0;
  undefined4 uStack_ac;
  void *pvStack_a8;
  void *pvStack_a4;
  int iStack_a0;
  float fStack_9c;
  void *pvStack_98;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_94 [24];
  undefined4 *puStack_7c;
  undefined auStack_74 [32];
  undefined auStack_54 [68];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 uStack_4;
  
  uStack_4 = 0xffffffff;
  puStack_8 = &LAB_009bbb93;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_b4;
  ExceptionList = &local_c;
  local_b0 = param_4;
  paVar1 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_b1);
  uStack_4 = 0;
  puStack_d4 = (undefined *)0x510139;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_94,"",paVar1);
  uStack_4._0_1_ = 1;
  puStack_d4 = (undefined *)0x51015a;
  FUN_0050a690();
  uStack_4._0_1_ = 3;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(abStack_94)
  ;
  uStack_4._0_1_ = 4;
  stlp_std::allocator<char>::~allocator<char>(&local_b1);
  iVar2 = FUN_0050a7e0();
  if (iVar2 != 0) {
    pvStack_a8 = (void *)0x0;
    pvStack_a4 = (void *)0x0;
    iStack_a0 = 0;
    uStack_4._0_1_ = 5;
    puStack_d4 = (undefined *)0x5101bf;
    FUN_0050a7d0();
    puStack_d4 = (undefined *)0x5101c6;
    FUN_006c8cb0();
    iVar2 = FUN_00401360();
    uStack_ac = *(undefined4 *)(iVar2 + 100);
    pvStack_98 = pvStack_a4;
    pvVar3 = pvStack_a8;
LAB_005101e0:
    do {
      if (pvVar3 == pvStack_98) goto LAB_0051025f;
      if (NAN(param_5) == (param_5 == 0.0)) {
        iVar2 = FUN_006c6410();
        if (iVar2 != 0) {
          fStack_9c = param_5 * (float)_PTR_00a7a618;
          FUN_006e7460();
        }
      }
      iVar2 = FUN_007e0e40();
      if (iVar2 != 0) {
        if (param_2 != '\0') {
          puStack_d4 = (undefined *)0x510248;
          FUN_006d0990();
          pvVar3 = (void *)((int)pvVar3 + 4);
          param_4 = local_b0;
          goto LAB_005101e0;
        }
        puStack_d4 = (undefined *)0x510256;
        FUN_006d09b0();
      }
      pvVar3 = (void *)((int)pvVar3 + 4);
      param_4 = local_b0;
    } while( true );
  }
LAB_00510305:
  uStack_4 = 0xffffffff;
  FUN_0059f0d0();
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
LAB_0051025f:
  if (*param_4 != 0 || param_4[1] != 0) {
    local_b0 = (int *)&puStack_d4;
    FUN_00973500();
    FUN_0050cb20(auStack_54,FUN_005100d0,param_1,0,param_3);
    FUN_0050ff50();
    uStack_4._0_1_ = 6;
    FUN_00973430();
    uStack_4._0_1_ = 5;
    if ((puStack_7c != (undefined4 *)0x0) && ((code *)*puStack_7c != (code *)0x0)) {
      puStack_d4 = auStack_74;
      (*(code *)*puStack_7c)();
    }
  }
  uStack_4 = CONCAT31(uStack_4._1_3_,4);
  if (pvStack_a8 != (void *)0x0) {
    puStack_d4 = (undefined *)0x510302;
    stlp_std::__node_alloc::deallocate(pvStack_a8,(iStack_a0 - (int)pvStack_a8 >> 2) * 4);
  }
  goto LAB_00510305;
}

