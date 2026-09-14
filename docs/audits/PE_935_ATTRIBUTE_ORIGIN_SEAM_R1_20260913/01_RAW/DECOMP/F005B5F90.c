
void FUN_005b5f90(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                 undefined4 *param_5)

{
  char cVar1;
  undefined4 uVar2;
  allocator<char> *paVar3;
  int iVar4;
  int iVar5;
  float10 fVar6;
  undefined *puVar7;
  undefined *puVar8;
  code **ppcVar9;
  undefined4 uVar10;
  undefined4 uVar11;
  undefined auStack_ec [3];
  allocator<char> local_e9;
  float fStack_e8;
  code *local_e0;
  int iStack_dc;
  undefined4 uStack_d8;
  float fStack_d4;
  undefined4 uStack_d0;
  undefined4 *puStack_c8;
  undefined auStack_c0 [24];
  undefined4 uStack_a8;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_a0 [24];
  undefined local_88 [44];
  undefined local_5c [76];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009d69e1;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_ec;
  ExceptionList = &local_c;
  uVar2 = param_1;
  FUN_0043a550(param_1,DAT_00b9d8d0 ^ (uint)&stack0xffffff04);
  uVar2 = FUN_0072f580(uVar2);
  FUN_005670a0(uVar2);
  local_4 = 0;
  FUN_00730f60();
  FUN_00730f90(param_4);
  uVar2 = FUN_0096c630(&local_e0,param_5);
  FUN_00730fb0(uVar2);
  FUN_00797280(param_1);
  paVar3 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_e9);
  local_4._0_1_ = 1;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)&local_e0,"",paVar3);
  uVar11 = 1;
  uVar10 = 1;
  ppcVar9 = &local_e0;
  uVar2 = 2;
  puVar8 = local_5c;
  puVar7 = local_88;
  local_4._0_1_ = 2;
  FUN_004148f0(puVar7,puVar8,2,ppcVar9,1,1);
  iVar4 = FUN_00457930(puVar7,puVar8,uVar2,ppcVar9,uVar10,uVar11);
  local_4._0_1_ = 1;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)&local_e0);
  stlp_std::allocator<char>::~allocator<char>(&local_e9);
  if (iVar4 != 0) {
    paVar3 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_e9);
    local_4._0_1_ = 3;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (abStack_a0,"",paVar3);
    local_4._0_1_ = 4;
    FUN_0050a690(iVar4,abStack_a0);
    local_4._0_1_ = 6;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (abStack_a0);
    local_4._0_1_ = 7;
    stlp_std::allocator<char>::~allocator<char>(&local_e9);
    cVar1 = FUN_006c4200();
    if (cVar1 != '\0') {
      FUN_004123d0(param_2);
      FUN_00509570(param_2);
      iVar5 = FUN_0050a860();
      if (iVar5 != 0) {
        iVar5 = FUN_00401360();
        uVar2 = *(undefined4 *)(iVar5 + 100);
        uVar10 = 1;
        fStack_e8 = (float)uVar2;
        FUN_0050a860(1,uVar2);
        FUN_006d0990(uVar10,uVar2);
        iVar5 = FUN_00401360();
        fStack_e8 = *(float *)(iVar5 + 100);
        fVar6 = (float10)FUN_0040bdc0(3);
        fStack_e8 = (float)(fVar6 + (float10)fStack_e8);
        iStack_dc = FUN_0050a860();
        fStack_d4 = fStack_e8;
        uStack_d8 = 1;
        local_e0 = FUN_006d09b0;
        FUN_00567130(&local_e0);
        local_4._0_1_ = 8;
        FUN_00973430(param_3);
        local_4._0_1_ = 7;
        if ((puStack_c8 != (undefined4 *)0x0) && ((code *)*puStack_c8 != (code *)0x0)) {
          (*(code *)*puStack_c8)(auStack_c0,auStack_c0,1);
        }
      }
    }
    FUN_0043ae80(0x3f800000);
    uStack_d8 = *param_5;
    fStack_d4 = (float)param_5[1];
    uStack_d0 = param_5[2];
    local_e0 = FUN_005b5e20;
    iStack_dc = iVar4;
    FUN_005b5dd0(&local_e0);
    local_4._0_1_ = 9;
    uVar2 = FUN_0040bfe0(200,0,2);
    FUN_00973430(uVar2);
    local_4._0_1_ = 7;
    if ((puStack_c8 != (undefined4 *)0x0) && ((code *)*puStack_c8 != (code *)0x0)) {
      (*(code *)*puStack_c8)(auStack_c0,auStack_c0,1);
    }
    uVar2 = FUN_004154f0();
    FUN_00567030(FUN_00855dc0,uVar2,iVar4,0);
    uStack_a8 = 0;
    local_4._0_1_ = 10;
    uVar2 = FUN_0040bfe0(2,0,3);
    uVar2 = FUN_0040be60(&local_e0,uVar2);
    FUN_00973430(uVar2);
    local_4._0_1_ = 7;
    if (puStack_c8 != (undefined4 *)0x0) {
      if ((code *)*puStack_c8 != (code *)0x0) {
        (*(code *)*puStack_c8)(auStack_c0,auStack_c0,1);
      }
      puStack_c8 = (undefined4 *)0x0;
    }
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_0059f0d0();
  }
  local_4 = 0xffffffff;
  FUN_00730730();
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

