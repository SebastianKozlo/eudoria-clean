
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00456f40(int param_1,undefined4 *param_2,undefined4 param_3,char param_4,int param_5,
                 undefined4 param_6,int *param_7,char param_8,undefined4 param_9,int *param_10,
                 char param_11)

{
  undefined4 uVar1;
  char cVar2;
  allocator<char> *paVar3;
  int iVar4;
  undefined4 uVar5;
  undefined4 *puVar6;
  float10 fVar7;
  undefined4 local_1e8;
  allocator<char> local_1e2;
  allocator<char> aStack_1e1;
  float fStack_1e0;
  undefined4 local_1dc;
  undefined4 local_1d8;
  undefined4 uStack_1d4;
  int *local_1d0;
  undefined auStack_1cc [8];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_1c4 [56];
  undefined4 auStack_18c [42];
  undefined auStack_e4 [188];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_28 [24];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 uStack_4;
  
  uStack_4 = 0xffffffff;
  puStack_8 = &LAB_0099fbf1;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)&local_1e8;
  ExceptionList = &local_c;
  local_1d8 = param_9;
  local_1d0 = param_7;
  local_1dc = FUN_004123d0(DAT_00b9d8d0 ^ (uint)&stack0xfffffe08);
  local_1e8 = FUN_006c64d0();
  paVar3 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_1e2);
  uStack_4 = 0;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_28,paVar3);
  uStack_4 = CONCAT31(uStack_4._1_3_,2);
  stlp_std::allocator<char>::~allocator<char>(&local_1e2);
  fStack_1e0 = _DAT_00a7b128;
  if (param_8 != '\0') {
    FUN_006a8980(auStack_1cc,&local_1dc);
    cVar2 = FUN_004c46c0(param_1,param_3,abStack_28,param_5);
    if (cVar2 == '\0') goto LAB_0045735d;
    if (param_5 == 1) {
      FUN_004525b0(param_1,local_1e8,&fStack_1e0);
      FUN_00452540(param_1,local_1e8);
    }
  }
  fVar7 = (float10)FUN_00861240();
  if ((float10)_DAT_00a797c8 < fVar7) {
    fVar7 = (float10)FUN_00861240();
    fStack_1e0 = (float)fVar7;
  }
  iVar4 = FUN_007ce1e0();
  if (iVar4 == 0) goto LAB_0045735d;
  if (param_4 == '\0') {
    FUN_00453ed0(param_1,param_2,param_1 + 8,fStack_1e0,local_1d0,local_1d8,param_10);
    auStack_18c[0] = local_1dc;
    uStack_4._0_1_ = 10;
    FUN_00453aa0(auStack_e4);
    uStack_4._0_1_ = 0xb;
    FUN_004558e0(auStack_1cc,auStack_18c);
    uStack_4._0_1_ = 10;
    FUN_004534d0();
    uStack_4 = CONCAT31(uStack_4._1_3_,2);
    FUN_004534d0();
    goto LAB_0045735d;
  }
  paVar3 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_1e1);
  uStack_4._0_1_ = 3;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_1c4,"",paVar3);
  uVar1 = local_1dc;
  uStack_4._0_1_ = 4;
  FUN_0050a690(local_1dc,abStack_1c4);
  uStack_4._0_1_ = 6;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_1c4);
  uStack_4 = CONCAT31(uStack_4._1_3_,7);
  stlp_std::allocator<char>::~allocator<char>(&aStack_1e1);
  cVar2 = FUN_006c4200();
  if (cVar2 != '\0') {
    FUN_006c8830();
    if ((-(uint)(*param_10 != 0) & 0x8e0110) == 0) {
      cVar2 = FUN_006c8b20();
      if (cVar2 != '\0') {
        uVar5 = FUN_0040b0a0();
        FUN_00455310(local_1e8,uVar5);
        cVar2 = FUN_006c8bb0();
        if (cVar2 != '\0') {
          puVar6 = param_2;
          FUN_004123d0(param_2);
          cVar2 = FUN_0050a310(puVar6);
          goto LAB_004571a0;
        }
      }
    }
    else {
      cVar2 = FUN_004532a0();
      if (param_2 != (undefined4 *)0x0) {
        (**(code **)*param_2)(1);
      }
      param_2 = (undefined4 *)0x0;
LAB_004571a0:
      if (cVar2 != '\0') {
        if (param_11 == '\0') {
          cVar2 = FUN_00452750(uVar1);
          if (cVar2 != '\0') goto LAB_004571be;
        }
        else {
LAB_004571be:
          uVar5 = _DAT_00a7b238;
          FUN_004123d0(_DAT_00a7b238);
          FUN_00509720(uVar5);
        }
        uVar5 = uVar1;
        FUN_00452210(uVar1);
        FUN_00539970(uVar5);
        FUN_0085b840(uVar1);
        uStack_4 = CONCAT31(uStack_4._1_3_,8);
        iVar4 = FUN_004123d0();
        if (iVar4 != 0) {
          FUN_004123d0();
          puVar6 = (undefined4 *)FUN_0085ad50();
          local_1d8 = *puVar6;
          uStack_1d4 = puVar6[1];
          cVar2 = FUN_009789c0();
          if (cVar2 != '\0') {
            puVar6 = &local_1d8;
            FUN_00401360(puVar6);
            FUN_00414130();
            FUN_004a9850(puVar6);
          }
        }
        if ((-(uint)(*local_1d0 != 0) & 0x8e0110) != 0) {
          FUN_00584340(local_1d0);
          uStack_4._0_1_ = 9;
          FUN_004066d0();
          uStack_4 = CONCAT31(uStack_4._1_3_,8);
          FUN_00662d00();
        }
        uStack_4._0_1_ = 7;
        FUN_008e0110();
        uStack_4 = CONCAT31(uStack_4._1_3_,2);
        FUN_0059f0d0();
        goto LAB_0045735d;
      }
    }
    if (param_2 != (undefined4 *)0x0) {
      (**(code **)*param_2)(1);
    }
  }
  uStack_4 = CONCAT31(uStack_4._1_3_,2);
  FUN_0059f0d0();
LAB_0045735d:
  uStack_4 = 0xffffffff;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(abStack_28)
  ;
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

