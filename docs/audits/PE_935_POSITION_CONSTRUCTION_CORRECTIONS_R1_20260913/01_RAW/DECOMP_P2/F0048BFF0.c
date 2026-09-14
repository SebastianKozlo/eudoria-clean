// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x48bff0L (requested via site 0x48c05b)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0048bff0(void)

{
  float10 fVar1;
  float10 fVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  int iVar6;
  allocator<char> *paVar7;
  undefined uVar8;
  int iVar9;
  float10 fVar10;
  float10 fVar11;
  float10 fVar12;
  float10 fVar13;
  float10 fVar14;
  float fVar15;
  float fVar16;
  undefined4 uVar17;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbVar18;
  float *pfVar19;
  undefined4 uVar20;
  allocator<char> local_56;
  allocator<char> aStack_55;
  float local_54;
  float local_50 [3];
  float local_44;
  float local_40;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_3c [24];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_24 [24];
  void *local_c;
  undefined *puStack_8;
  int iStack_4;
  
  iStack_4 = 0xffffffff;
  puStack_8 = &LAB_009a6742;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  pfVar19 = local_50 + 2;
  FUN_004143f0(pfVar19,DAT_00b9d8d0 ^ (uint)&stack0xffffff9c);
  FUN_0042bdb0(pfVar19);
  if (local_40 < (float)_DAT_00a7b9f8 != (NAN(local_40) || NAN((float)_DAT_00a7b9f8))) {
    uVar20 = 0;
    uVar17 = 0;
    fVar15 = local_50[2];
    fVar16 = local_44;
    FUN_004154f0(local_50[2],local_44,0,0);
    fVar10 = (float10)FUN_00853a80(fVar15,fVar16,uVar17,uVar20);
    if (fVar10 < (float10)_DAT_00a7b128 == (fVar10 == (float10)_DAT_00a7b128)) {
      iVar9 = 0;
    }
    else {
      iVar9 = 8;
    }
    uVar20 = 0;
    uVar17 = 0;
    fVar15 = local_44 + (float)_DAT_00a7b9f0;
    fVar16 = (float)_DAT_00a7b9f0 + local_50[2];
    local_54 = fVar16;
    FUN_004154f0(fVar16,fVar15,0,0);
    fVar10 = (float10)FUN_00853a80(fVar16,fVar15,uVar17,uVar20);
    if (fVar10 < (float10)_DAT_00a7b128 == (fVar10 == (float10)_DAT_00a7b128)) {
      iVar3 = 0;
    }
    else {
      iVar3 = 2;
    }
    uVar20 = 0;
    uVar17 = 0;
    fVar15 = local_44 + (float)_DAT_00a7b9f0;
    fVar16 = local_50[2] - (float)_DAT_00a7b9f0;
    local_54 = fVar16;
    FUN_004154f0(fVar16,fVar15,0,0);
    fVar10 = (float10)FUN_00853a80(fVar16,fVar15,uVar17,uVar20);
    if (fVar10 < (float10)_DAT_00a7b128 == (fVar10 == (float10)_DAT_00a7b128)) {
      iVar4 = 0;
    }
    else {
      iVar4 = 2;
    }
    uVar20 = 0;
    uVar17 = 0;
    fVar15 = local_44 - (float)_DAT_00a7b9f0;
    fVar16 = (float)_DAT_00a7b9f0 + local_50[2];
    local_54 = fVar16;
    FUN_004154f0(fVar16,fVar15,0,0);
    fVar10 = (float10)FUN_00853a80(fVar16,fVar15,uVar17,uVar20);
    if (fVar10 < (float10)_DAT_00a7b128 == (fVar10 == (float10)_DAT_00a7b128)) {
      iVar5 = 0;
    }
    else {
      iVar5 = 2;
    }
    uVar20 = 0;
    uVar17 = 0;
    fVar15 = local_44 - (float)_DAT_00a7b9f0;
    fVar16 = local_50[2] - (float)_DAT_00a7b9f0;
    local_54 = fVar16;
    FUN_004154f0(fVar16,fVar15,0,0);
    fVar10 = (float10)FUN_00853a80(fVar16,fVar15,uVar17,uVar20);
    if (fVar10 < (float10)_DAT_00a7b128 == (fVar10 == (float10)_DAT_00a7b128)) {
      iVar6 = 0;
    }
    else {
      iVar6 = 2;
    }
    uVar20 = 0;
    uVar17 = 0;
    fVar15 = local_50[2] + (float)_DAT_00a7af88;
    fVar16 = local_44;
    local_54 = fVar15;
    FUN_004154f0(fVar15,local_44,0,0);
    fVar11 = (float10)FUN_00853a80(fVar15,fVar16,uVar17,uVar20);
    fVar10 = (float10)_DAT_00a7b128;
    uVar20 = 0;
    uVar17 = 0;
    fVar15 = local_50[2] - (float)_DAT_00a7af88;
    fVar16 = local_44;
    local_54 = fVar15;
    FUN_004154f0(fVar15,local_44,0,0);
    fVar12 = (float10)FUN_00853a80(fVar15,fVar16,uVar17,uVar20);
    fVar1 = (float10)_DAT_00a7b128;
    uVar20 = 0;
    fVar15 = local_44 + (float)_DAT_00a7af88;
    uVar17 = 0;
    fVar16 = local_50[2];
    local_54 = fVar15;
    FUN_004154f0(local_50[2],fVar15,0,0);
    fVar13 = (float10)FUN_00853a80(fVar16,fVar15,uVar17,uVar20);
    fVar2 = (float10)_DAT_00a7b128;
    uVar20 = 0;
    fVar15 = local_44 - (float)_DAT_00a7af88;
    uVar17 = 0;
    local_54 = fVar15;
    FUN_004154f0(local_50[2],fVar15,0,0);
    fVar14 = (float10)FUN_00853a80(local_50[2],fVar15,uVar17,uVar20);
    local_54 = (float)(iVar9 + iVar3 + iVar4 + iVar5 + iVar6 +
                       (uint)(fVar11 < fVar10 != (fVar11 == fVar10)) +
                       (uint)(fVar12 < fVar1 != (fVar12 == fVar1)) +
                       (uint)(fVar13 < fVar2 != (fVar13 == fVar2)) +
                      (uint)(fVar14 <= (float10)_DAT_00a7b128));
    if (local_54 != 0.0) {
      fVar10 = (float10)FUN_0041c740(0x3f800000,0,local_40,_DAT_00a7b128,_DAT_00a7b9e8);
      local_54 = (float)(fVar10 * (float10)(((float)(int)local_54 * (float)_DAT_00a7af78) /
                                            (float)_DAT_00a7b9e0 + (float)_DAT_00a7b2d0));
      FUN_0048bbc0();
      fVar10 = (float10)FUN_00861240();
      local_50[0] = (float)fVar10;
      if (local_50[0] < _DAT_00a7b9d8 == (NAN(local_50[0]) || NAN(_DAT_00a7b9d8))) {
        if (local_50[0] < _DAT_00a7b9d4 == (NAN(local_50[0]) || NAN(_DAT_00a7b9d4))) {
          paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_56);
          iStack_4 = 0xc;
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_3c,"WAVES_01",paVar7);
          pbVar18 = abStack_3c;
          uVar17 = 1000;
          iStack_4._0_1_ = 0xd;
          FUN_004150f0(pbVar18,1000);
          FUN_008b6510(pbVar18,uVar17);
          iStack_4 = CONCAT31(iStack_4._1_3_,0xc);
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_3c);
          stlp_std::allocator<char>::~allocator<char>(&local_56);
          paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_56);
          iStack_4 = 0xe;
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_3c,"WAVES_02",paVar7);
          pbVar18 = abStack_3c;
          uVar17 = 1000;
          iStack_4._0_1_ = 0xf;
          FUN_004150f0(pbVar18,1000);
          FUN_008b6510(pbVar18,uVar17);
          iStack_4 = CONCAT31(iStack_4._1_3_,0xe);
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_3c);
          iStack_4 = 0xffffffff;
          stlp_std::allocator<char>::~allocator<char>(&local_56);
          pfVar19 = local_50;
          uVar20 = 0x97;
          uVar17 = 0;
          local_50[0] = 0.0;
          local_50[1] = 0.0;
          FUN_00414770(0,0x97,pfVar19);
          FUN_00446800(uVar17,uVar20,pfVar19);
          paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_55);
          iStack_4 = 0x10;
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_24,"WAVES_03",paVar7);
          pbVar18 = abStack_24;
          iStack_4._0_1_ = 0x11;
          fVar15 = local_54;
          FUN_004150f0(pbVar18,local_54);
          FUN_008b6550(pbVar18,fVar15);
          iStack_4 = CONCAT31(iStack_4._1_3_,0x10);
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_24);
          stlp_std::allocator<char>::~allocator<char>(&aStack_55);
          ExceptionList = local_c;
          return;
        }
        paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_56);
        iStack_4 = 6;
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_3c,"WAVES_01",paVar7);
        pbVar18 = abStack_3c;
        uVar17 = 1000;
        iStack_4._0_1_ = 7;
        FUN_004150f0(pbVar18,1000);
        FUN_008b6510(pbVar18,uVar17);
        iStack_4 = CONCAT31(iStack_4._1_3_,6);
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_3c);
        stlp_std::allocator<char>::~allocator<char>(&local_56);
        paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_56);
        iStack_4 = 8;
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_3c,"WAVES_03",paVar7);
        pbVar18 = abStack_3c;
        uVar17 = 1000;
        iStack_4._0_1_ = 9;
        FUN_004150f0(pbVar18,1000);
        FUN_008b6510(pbVar18,uVar17);
        iStack_4 = CONCAT31(iStack_4._1_3_,8);
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_3c);
        iStack_4 = 0xffffffff;
        stlp_std::allocator<char>::~allocator<char>(&local_56);
        pfVar19 = local_50;
        uVar20 = 0x96;
        uVar17 = 0;
        local_50[0] = 0.0;
        local_50[1] = 0.0;
        FUN_00414770(0,0x96,pfVar19);
        FUN_00446800(uVar17,uVar20,pfVar19);
        paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_56);
        uVar8 = 10;
        iStack_4 = 10;
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_3c,"WAVES_02",paVar7);
        iStack_4._0_1_ = 0xb;
      }
      else {
        paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_56);
        iStack_4 = 0;
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_3c,"WAVES_02",paVar7);
        pbVar18 = abStack_3c;
        uVar17 = 1000;
        iStack_4._0_1_ = 1;
        FUN_004150f0(pbVar18,1000);
        FUN_008b6510(pbVar18,uVar17);
        iStack_4 = (uint)iStack_4._1_3_ << 8;
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_3c);
        stlp_std::allocator<char>::~allocator<char>(&local_56);
        paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_56);
        iStack_4 = 2;
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_3c,"WAVES_03",paVar7);
        pbVar18 = abStack_3c;
        uVar17 = 1000;
        iStack_4._0_1_ = 3;
        FUN_004150f0(pbVar18,1000);
        FUN_008b6510(pbVar18,uVar17);
        iStack_4 = CONCAT31(iStack_4._1_3_,2);
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_3c);
        iStack_4 = 0xffffffff;
        stlp_std::allocator<char>::~allocator<char>(&local_56);
        pfVar19 = local_50;
        uVar20 = 0x95;
        uVar17 = 0;
        local_50[0] = 0.0;
        local_50[1] = 0.0;
        FUN_00414770(0,0x95,pfVar19);
        FUN_00446800(uVar17,uVar20,pfVar19);
        paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_56);
        uVar8 = 4;
        iStack_4 = 4;
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_3c,"WAVES_01",paVar7);
        iStack_4._0_1_ = 5;
      }
      pbVar18 = abStack_3c;
      fVar15 = local_54;
      FUN_004150f0(pbVar18,local_54);
      FUN_008b6550(pbVar18,fVar15);
      iStack_4 = CONCAT31(iStack_4._1_3_,uVar8);
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                (abStack_3c);
      stlp_std::allocator<char>::~allocator<char>(&local_56);
      ExceptionList = local_c;
      return;
    }
    local_54 = 0.0;
  }
  FUN_0048be10();
  ExceptionList = local_c;
  return;
}

