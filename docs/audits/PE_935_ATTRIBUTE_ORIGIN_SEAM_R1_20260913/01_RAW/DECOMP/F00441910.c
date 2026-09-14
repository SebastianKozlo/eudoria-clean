
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall
FUN_00441910(int param_1_00,undefined4 *param_1,int *param_2,undefined4 param_3,char param_5)

{
  int *piVar1;
  char cVar2;
  allocator<char> *paVar3;
  int iVar4;
  undefined4 uVar5;
  int *piVar6;
  void *pvVar7;
  undefined4 uStack_138;
  undefined4 *puStack_134;
  undefined4 *puStack_130;
  undefined **ppuStack_12c;
  undefined4 uStack_128;
  undefined4 *puStack_124;
  undefined auStack_104 [2];
  allocator<char> aStack_102;
  allocator<char> aStack_101;
  int *piStack_100;
  allocator<char> local_f9;
  void *pvStack_f8;
  uint local_f4;
  int *local_f0;
  undefined4 uStack_ec;
  undefined4 uStack_e8;
  undefined4 uStack_e4;
  undefined4 *local_e0;
  int *piStack_dc;
  undefined4 local_d8;
  undefined *puStack_d4;
  undefined4 uStack_d0;
  undefined4 uStack_cc;
  undefined4 uStack_c8;
  int *piStack_c4;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_c0 [32];
  undefined4 *puStack_a0;
  undefined auStack_98 [28];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_7c [76];
  undefined4 *puStack_30;
  undefined auStack_28 [24];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 uStack_4;
  
  uStack_4 = 0xffffffff;
  puStack_8 = &LAB_0099d5e9;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_104;
  ExceptionList = &local_c;
  local_d8 = param_3;
  local_e0 = param_1;
  local_f0 = param_2;
  local_f4 = 0;
  paVar3 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_f9);
  uStack_4 = 0;
  puStack_124 = (undefined4 *)0x441998;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_7c,"",paVar3);
  uStack_4._0_1_ = 1;
  puStack_124 = (undefined4 *)0x4419b8;
  FUN_0050a690();
  uStack_4._0_1_ = 3;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(abStack_7c)
  ;
  uStack_4._0_1_ = 4;
  stlp_std::allocator<char>::~allocator<char>(&local_f9);
  iVar4 = FUN_004123d0();
  if (iVar4 != 0) {
    piStack_100 = (int *)*param_1;
    iVar4 = FUN_0050a950();
    if (iVar4 == 0) {
      puStack_124 = (undefined4 *)0x441a38;
      FUN_004d1430();
      if ((pvStack_f8 == (void *)(param_1_00 + 0x18)) || (*(int *)((int)pvStack_f8 + 0x18) == 0)) {
        aStack_101 = (allocator<char>)FUN_0043a740();
        if (aStack_101 != (allocator<char>)0x0) {
          FUN_004123d0();
          FUN_00509180();
          uVar5 = FUN_00844ae0();
          *(undefined4 *)(param_1_00 + 0x40) = uVar5;
          FUN_004ad820();
          uStack_4._0_1_ = 5;
          iVar4 = FUN_006b22d0();
          piStack_100 = _DAT_00a7af50;
          if (iVar4 == 1) {
            piStack_100 = _DAT_00a7af54;
          }
          paVar3 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_102);
          uStack_4._0_1_ = 6;
          puStack_124 = (undefined4 *)0x441acf;
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_c0,"",paVar3);
          uStack_ec = 0;
          uStack_e8 = 0;
          puStack_124 = (undefined4 *)0x1;
          uStack_e4 = _DAT_00a7adc8;
          uStack_128 = 0;
          ppuStack_12c = &puStack_d4;
          uStack_cc = 0;
          uStack_c8 = 0;
          puStack_130 = &uStack_ec;
          piStack_c4 = piStack_100;
          puStack_134 = &uStack_cc;
          uStack_138 = 0;
          uStack_4._0_1_ = 7;
          puStack_d4 = (undefined *)0x0;
          uStack_d0 = 0;
          uStack_128 = FUN_00730f00(*(undefined4 *)(param_1_00 + 0x40));
          ppuStack_12c = (undefined **)0x441b33;
          cVar2 = FUN_004c46c0();
          uStack_4._0_1_ = 6;
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_c0);
          stlp_std::allocator<char>::~allocator<char>(&aStack_102);
          if (cVar2 != '\0') {
            paVar3 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_102);
            uStack_4._0_1_ = 8;
            puStack_124 = (undefined4 *)0x441b7e;
            stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                      (abStack_c0,"",paVar3);
            uStack_4._0_1_ = 9;
            puStack_124 = (undefined4 *)0x441b9b;
            FUN_0050a690();
            uStack_4._0_1_ = 0xb;
            stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                      (abStack_c0);
            uStack_4._0_1_ = 0xc;
            stlp_std::allocator<char>::~allocator<char>(&aStack_102);
            iVar4 = FUN_004123d0();
            FUN_00509180();
            *(uint *)(iVar4 + 0x2c) = *(uint *)(iVar4 + 0x2c) | 0x11;
            piStack_100 = (int *)operator_new(0x118);
            uStack_4._0_1_ = 0xd;
            if (piStack_100 == (int *)0x0) {
              piVar6 = (int *)0x0;
            }
            else {
              piVar6 = (int *)FUN_007b6000();
            }
            if (piVar6 != (int *)0x0) {
              piVar6[1] = piVar6[1] + 1;
            }
            uStack_4._0_1_ = 0xe;
            piStack_100 = piVar6;
            piStack_dc = (int *)operator_new(0x1ec);
            uStack_4._0_1_ = 0xf;
            if (piStack_dc == (int *)0x0) {
              uVar5 = 0;
            }
            else {
              puStack_124 = local_e0 + 1;
              uStack_128 = *(undefined4 *)(param_1_00 + 0x40);
              ppuStack_12c = (undefined **)0x441c59;
              FUN_006c9840();
              uStack_4 = CONCAT31(uStack_4._1_3_,0x10);
              local_f4 = 1;
              puStack_124 = (undefined4 *)0x441c72;
              uVar5 = FUN_006b9230();
            }
            *(undefined4 *)(param_1_00 + 0x3c) = uVar5;
            uStack_4 = 0xe;
            if ((local_f4 & 1) != 0) {
              FUN_0070f860();
            }
            uStack_4._0_1_ = 0xc;
            if (piVar6 != (int *)0x0) {
              piVar1 = piVar6 + 1;
              *piVar1 = *piVar1 + -1;
              if (*piVar1 == 0) {
                (**(code **)(*piVar6 + 4))();
              }
            }
            uStack_4._0_1_ = 5;
            FUN_0059f0d0();
          }
          uStack_4._0_1_ = 4;
          thunk_FUN_00703bc0();
        }
        pvVar7 = (void *)0x0;
        piStack_dc = (int *)operator_new(0x118);
        uStack_4._0_1_ = 0x12;
        if (piStack_dc == (int *)0x0) {
          piStack_100 = (int *)0x0;
        }
        else {
          piStack_100 = (int *)FUN_007b6000();
        }
        piVar6 = piStack_100;
        if (piStack_100 != (int *)0x0) {
          piStack_100[1] = piStack_100[1] + 1;
        }
        uStack_4._0_1_ = 0x13;
        aStack_102 = (allocator<char>)0x1;
        piStack_dc = piStack_100;
        pvStack_f8 = operator_new(0x1ec);
        uStack_4._0_1_ = 0x14;
        if (pvStack_f8 != (void *)0x0) {
          puStack_124 = (undefined4 *)0x441d48;
          pvVar7 = (void *)FUN_006b9230();
        }
        uStack_4 = CONCAT31(uStack_4._1_3_,0x13);
        cVar2 = FUN_006b29c0();
        if (cVar2 == '\0') {
          if (pvVar7 != (void *)0x0) {
            FUN_006b5cd0();
            operator_delete(pvVar7);
          }
          aStack_102 = (allocator<char>)0x0;
        }
        else {
          piVar6 = (int *)*local_f0;
          local_f0 = (int *)local_f0[1];
          if (piVar6 != local_f0) {
            do {
              FUN_00843d60();
              uStack_4._0_1_ = 0x15;
              FUN_00843dd0();
              cVar2 = FUN_00728bf0();
              if (cVar2 == '\0') {
                puStack_124 = (undefined4 *)0x441dd6;
                FUN_00843dd0();
                cVar2 = FUN_009768d0();
                if (cVar2 != '\0') goto LAB_00441e49;
                cVar2 = FUN_00844020();
                if (cVar2 != '\0') {
                  FUN_00843d60();
                  uStack_4 = CONCAT31(uStack_4._1_3_,0x16);
                  cVar2 = FUN_00844020();
                  if (cVar2 != '\0') {
                    FUN_004123d0();
                    puStack_124 = (undefined4 *)0x441e36;
                    FUN_00845f70();
                  }
                  uStack_4._0_1_ = 0x15;
                  FUN_008e0110();
                }
              }
              else {
LAB_00441e49:
                FUN_00843dd0();
                puStack_124 = (undefined4 *)*piVar6;
                uStack_128 = 0x441e6b;
                FUN_007199e0();
                puStack_124 = (undefined4 *)0x441e73;
                FUN_006b9810();
                if ((aStack_101 != (allocator<char>)0x0) && (*(int *)(param_1_00 + 0x3c) != 0)) {
                  FUN_00843dd0();
                  puStack_124 = (undefined4 *)*piVar6;
                  uStack_128 = 0x441e9f;
                  FUN_007199e0();
                  puStack_124 = (undefined4 *)0x441ea8;
                  FUN_006b9810();
                }
              }
              uStack_4 = CONCAT31(uStack_4._1_3_,0x13);
              FUN_008e0110();
              piVar6 = piVar6 + 1;
            } while (piVar6 != local_f0);
          }
          if ((param_5 == '\0') && (aStack_101 == (allocator<char>)0x0)) {
            puStack_d4 = (undefined *)&uStack_138;
            FUN_00584340(local_d8);
            FUN_0043be80(pvVar7);
            uStack_4._0_1_ = 0x17;
            puStack_124 = (undefined4 *)0x441f16;
            FUN_0043bfe0();
            uStack_4._0_1_ = 0x18;
            puStack_124 = (undefined4 *)0x441f2c;
            FUN_0043da90();
            uStack_4._0_1_ = 0x17;
            if (puStack_30 != (undefined4 *)0x0) {
              if ((code *)*puStack_30 != (code *)0x0) {
                puStack_124 = (undefined4 *)auStack_28;
                uStack_128 = 0x441f53;
                (*(code *)*puStack_30)();
              }
              puStack_30 = (undefined4 *)0x0;
            }
            uStack_4 = CONCAT31(uStack_4._1_3_,0x13);
            if ((puStack_a0 != (undefined4 *)0x0) && ((code *)*puStack_a0 != (code *)0x0)) {
              puStack_124 = (undefined4 *)auStack_98;
              uStack_128 = 0x441f8e;
              (*(code *)*puStack_a0)();
            }
          }
          else {
            cVar2 = FUN_0043b6d0();
            if (cVar2 == '\0') {
              aStack_102 = (allocator<char>)0x0;
              piVar6 = piStack_100;
              goto LAB_004420a3;
            }
            puStack_124 = (undefined4 *)0x441fb3;
            FUN_00441790();
            if (aStack_101 != (allocator<char>)0x0) {
              if (*(int *)(param_1_00 + 0x3c) != 0) {
                FUN_0043b6d0();
                FUN_0043cf50();
                puStack_124 = (undefined4 *)0x441fe8;
                FUN_00440e70();
                paVar3 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_101);
                uStack_4._0_1_ = 0x19;
                puStack_124 = (undefined4 *)0x44200a;
                stlp_std::
                basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ::
                basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                          (abStack_c0,"",paVar3);
                uStack_4._0_1_ = 0x1a;
                puStack_124 = (undefined4 *)0x442027;
                FUN_0050a690();
                uStack_4._0_1_ = 0x1c;
                stlp_std::
                basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ::
                ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                          (abStack_c0);
                uStack_4 = CONCAT31(uStack_4._1_3_,0x1d);
                stlp_std::allocator<char>::~allocator<char>(&aStack_101);
                iVar4 = FUN_0050a7d0();
                if (iVar4 != 0) {
                  puStack_124 = (undefined4 *)0x44206d;
                  FUN_0043e520();
                }
                uStack_4 = CONCAT31(uStack_4._1_3_,0x13);
                FUN_0059f0d0();
              }
              puStack_124 = (undefined4 *)0x442092;
              FUN_0043a7b0();
            }
          }
          puStack_124 = (undefined4 *)0x44209f;
          FUN_006a8980();
          piVar6 = piStack_100;
        }
LAB_004420a3:
        uStack_4 = CONCAT31(uStack_4._1_3_,4);
        if (piVar6 != (int *)0x0) {
          piVar1 = piVar6 + 1;
          *piVar1 = *piVar1 + -1;
          if (*piVar1 == 0) {
            (**(code **)(*piVar6 + 4))();
          }
        }
        uStack_4 = 0xffffffff;
        FUN_0059f0d0();
        goto LAB_004420d9;
      }
    }
  }
  uStack_4 = 0xffffffff;
  FUN_0059f0d0();
LAB_004420d9:
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

