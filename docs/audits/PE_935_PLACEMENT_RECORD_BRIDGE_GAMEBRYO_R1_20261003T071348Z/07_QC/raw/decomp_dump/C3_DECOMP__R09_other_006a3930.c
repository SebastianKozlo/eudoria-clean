// source: C3_DECOMP.json :: R09_other_006a3930

undefined4 * __thiscall
FUN_006a3930(undefined4 *param_1_00,void *param_1,undefined4 param_2,int *param_4)

{
  int *piVar1;
  char cVar2;
  uint uVar3;
  allocator<char> *paVar4;
  int iVar5;
  undefined4 uVar6;
  undefined4 uVar7;
  undefined4 **ppuVar8;
  void *pvVar9;
  undefined4 *apuStack_54 [2];
  undefined auStack_4c [24];
  undefined4 uStack_34;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a00c1b;
  local_c = ExceptionList;
  uVar3 = DAT_00b9d8d0 ^ (uint)&stack0xffffff98;
  ExceptionList = &local_c;
  FUN_006a3bd0(param_1);
  *param_1_00 = ArkClientLocalDynamic::vftable;
  param_1_00[8] = 0;
  param_1_00[0x10] = 0;
  param_1_00[0x12] = 0;
  param_1_00[0x1a] = 0;
  local_4._0_1_ = 2;
  local_4._1_3_ = 0;
  uVar6 = param_2;
  FUN_0043a550(param_2,uVar3);
  param_2 = FUN_0072f580(uVar6);
  cVar2 = FUN_0072fce0();
  if (cVar2 == '\0') {
    param_1_00[6] = 0;
  }
  else {
    paVar4 = (allocator<char> *)
             stlp_std::allocator<char>::allocator<char>((allocator<char> *)&param_1);
    local_4._0_1_ = 3;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)apuStack_54,"",paVar4);
    ppuVar8 = apuStack_54;
    uVar7 = 0;
    uVar6 = 1;
    local_4._0_1_ = 4;
    FUN_00401360(1,0,ppuVar8);
    FUN_00485050();
    FUN_0048cbb0(uVar6);
    uVar6 = FUN_005247c0(uVar7,ppuVar8);
    param_1_00[6] = uVar6;
    local_4._0_1_ = 3;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)apuStack_54);
    local_4._0_1_ = 2;
    stlp_std::allocator<char>::~allocator<char>((allocator<char> *)&param_1);
    if (param_1_00[6] != 0) {
      uVar6 = FUN_0085c0c0(apuStack_54);
      FUN_005094c0(uVar6);
      uVar6 = FUN_0085c0f0(apuStack_54);
      FUN_00509510(uVar6);
      param_1 = operator_new(0x130);
      local_4._0_1_ = 5;
      if (param_1 == (void *)0x0) {
        iVar5 = 0;
      }
      else {
        uVar6 = FUN_00733340();
        iVar5 = FUN_006c0d50(param_2,4,uVar6);
      }
      local_4._0_1_ = 2;
      if (iVar5 != 0) {
        FUN_006c8b20();
        FUN_006c8bb0();
        FUN_0050a310(iVar5);
        iVar5 = FUN_007e0e40();
        if (iVar5 != 0) {
          iVar5 = FUN_00401360();
          param_1 = *(void **)(iVar5 + 100);
          uVar6 = 0;
          pvVar9 = param_1;
          FUN_007e0e40(0,param_1);
          FUN_006d0990(uVar6,pvVar9);
        }
      }
      piVar1 = param_4;
      if (*param_4 != 0 || param_4[1] != 0) {
        FUN_006a38d0(&LAB_006a3680,param_1_00,0);
        uStack_34 = 0;
        local_4._0_1_ = 6;
        FUN_00453800(apuStack_54);
        param_1_00[0x10] = uStack_34;
        local_4._0_1_ = 2;
        if ((apuStack_54[0] != (undefined4 *)0x0) && ((code *)*apuStack_54[0] != (code *)0x0)) {
          (*(code *)*apuStack_54[0])(auStack_4c,auStack_4c,1);
        }
        FUN_00973430(piVar1);
        FUN_006a38d0(&LAB_006a36a0,param_1_00,0);
        uStack_34 = 0;
        local_4._0_1_ = 7;
        FUN_00453800(apuStack_54);
        param_1_00[0x1a] = uStack_34;
        local_4 = CONCAT31(local_4._1_3_,2);
        if ((apuStack_54[0] != (undefined4 *)0x0) && ((code *)*apuStack_54[0] != (code *)0x0)) {
          (*(code *)*apuStack_54[0])(auStack_4c,auStack_4c,1);
        }
        uVar6 = FUN_0040bfe0(600,0,2);
        FUN_00973430(uVar6);
      }
    }
  }
  ExceptionList = local_c;
  return param_1_00;
}

