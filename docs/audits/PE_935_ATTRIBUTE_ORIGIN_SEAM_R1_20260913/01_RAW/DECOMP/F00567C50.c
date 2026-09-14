
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00567c50(int param_1,undefined4 param_2,int *param_3,char param_4)

{
  void *pvVar1;
  char cVar2;
  short sVar3;
  uint uVar4;
  int iVar5;
  undefined4 uVar6;
  allocator<char> *paVar7;
  int *piVar8;
  char *pcVar9;
  undefined4 uVar10;
  undefined4 uVar11;
  int *piVar12;
  float10 fVar13;
  undefined4 uVar14;
  undefined4 uVar15;
  undefined4 uVar16;
  undefined4 uVar17;
  float *pfVar18;
  undefined4 uVar19;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbVar20;
  int **ppiVar21;
  float *pfVar22;
  undefined auStack_cc [3];
  undefined local_c9;
  uint local_c8 [2];
  int *local_c0;
  undefined4 uStack_bc;
  allocator<char> local_b6;
  allocator<char> aStack_b5;
  int *piStack_b4;
  undefined4 local_b0;
  float fStack_ac;
  float fStack_a8;
  float fStack_a4;
  float fStack_a0;
  undefined local_9c [12];
  int *piStack_90;
  int *piStack_8c;
  int iStack_88;
  void *pvStack_84;
  void *pvStack_80;
  int iStack_7c;
  float fStack_78;
  float fStack_74;
  float fStack_70;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_60 [80];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  uint local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009c9e76;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_cc;
  uVar4 = DAT_00b9d8d0 ^ (uint)&stack0xffffff24;
  ExceptionList = &local_c;
  local_c0 = param_3;
  FUN_00843d60(param_1);
  local_4 = 0;
  FUN_004143f0(uVar4);
  iVar5 = FUN_007ce1e0();
  local_b0 = CONCAT31(local_b0._1_3_,param_1 == iVar5);
  local_c9 = 1;
  FUN_00843dd0(local_c8);
  cVar2 = FUN_009768d0(0x175);
  if ((cVar2 == '\0') || ((char)local_b0 != '\0')) {
    cVar2 = FUN_009768d0(0x1b2b);
    if (cVar2 != '\0') {
      uVar6 = FUN_0048ada0();
      FUN_00567b40(local_9c,param_2,uVar6);
    }
  }
  else {
    cVar2 = FUN_004436f0();
    local_c9 = cVar2 == '\0';
    if (!(bool)local_c9) goto LAB_00568375;
    uVar6 = FUN_0048ada0();
    FUN_00567b40(local_9c,param_2,uVar6);
    FUN_00443740();
  }
  paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_b6);
  local_4._0_1_ = 1;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_60,"",paVar7);
  pbVar20 = abStack_60;
  local_4._0_1_ = 2;
  uVar6 = FUN_00844130(pbVar20);
  FUN_0050a690(uVar6,pbVar20);
  local_4._0_1_ = 4;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(abStack_60)
  ;
  local_4._0_1_ = 5;
  stlp_std::allocator<char>::~allocator<char>(&local_b6);
  iVar5 = FUN_0050a7d0();
  if (iVar5 != 0) {
    piStack_90 = (int *)0x0;
    piStack_8c = (int *)0x0;
    iStack_88 = 0;
    ppiVar21 = &piStack_90;
    uVar6 = 1;
    local_4._0_1_ = 6;
    FUN_0050a7d0(1,ppiVar21);
    FUN_006c8cb0(uVar6,ppiVar21);
    if ((char)local_b0 != '\0') {
      paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_b5);
      local_4._0_1_ = 7;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)&fStack_78,"",paVar7);
      pfVar22 = &fStack_78;
      local_4._0_1_ = 8;
      FUN_00414670(pfVar22);
      uVar6 = FUN_007d8f90();
      FUN_0050a690(uVar6,pfVar22);
      local_4._0_1_ = 10;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)&fStack_78);
      local_4 = CONCAT31(local_4._1_3_,0xb);
      stlp_std::allocator<char>::~allocator<char>(&aStack_b5);
      iVar5 = FUN_0050a7d0();
      if (iVar5 != 0) {
        ppiVar21 = &piStack_90;
        uVar6 = 1;
        FUN_0050a7d0(1,ppiVar21);
        FUN_006c8cb0(uVar6,ppiVar21);
      }
      local_4._0_1_ = 6;
      FUN_0059f0d0();
    }
    pvStack_84 = (void *)0x0;
    pvStack_80 = (void *)0x0;
    iStack_7c = 0;
    local_4 = CONCAT31(local_4._1_3_,0xc);
    piStack_b4 = piStack_8c;
    for (piVar12 = piStack_90; pvVar1 = pvStack_84, piVar12 != piStack_b4; piVar12 = piVar12 + 1) {
      if (((*(int *)(*piVar12 + 0x4c) == 3) && (iVar5 = FUN_007e0e40(), iVar5 != 0)) &&
         (iVar5 = FUN_006c66d0(), iVar5 != 0)) {
        piVar8 = (int *)FUN_006c66d0();
        iVar5 = *piVar8;
        pcVar9 = stlp_std::
                 basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 ::c_str((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                          *)&DAT_00ba2e44);
        fStack_a0 = (float)(**(code **)(iVar5 + 0x44))(pcVar9);
        if (fStack_a0 != 0.0) {
          FUN_00566ce0(&fStack_a0);
        }
      }
    }
    if (pvStack_84 != pvStack_80) {
      fStack_78 = 0.0;
      fStack_74 = 0.0;
      fStack_70 = 0.0;
      fStack_ac = 0.0;
      fStack_a8 = 0.0;
      fStack_a4 = 0.0;
      iVar5 = FUN_0048ada0();
      if (iVar5 == param_1) {
        iVar5 = 0;
      }
      pfVar22 = &fStack_ac;
      piStack_b4 = _DAT_00a7b7ec;
      pfVar18 = &fStack_78;
      uVar6 = param_2;
      uVar10 = FUN_00844130(param_2,iVar5,pfVar18,pfVar22);
      cVar2 = FUN_00566100(uVar10,uVar6,iVar5,pfVar18,pfVar22);
      if (cVar2 != '\0') {
        pfVar22 = &fStack_ac;
        fStack_ac = 0.0;
        fStack_a8 = 0.0;
        fStack_a4 = 0.0;
        uVar6 = local_b0;
        uVar10 = param_2;
        uVar11 = FUN_00844130(local_b0,param_2,pfVar22);
        FUN_00565ab0(uVar11,uVar6,uVar10,pfVar22);
        fStack_a0 = fStack_a8 - fStack_74;
        piStack_b4 = (int *)(fStack_a4 - fStack_70);
        local_c0 = (int *)((float)piStack_b4 * (float)piStack_b4 +
                          fStack_a0 * fStack_a0 + (fStack_ac - fStack_78) * (fStack_ac - fStack_78))
        ;
        fVar13 = (float10)_CIsqrt();
        local_c0 = (int *)(float)fVar13;
        piStack_b4 = local_c0;
      }
      fStack_ac = 0.0;
      fStack_a8 = -(float)piStack_b4 * (float)_PTR_00a7a618;
      fStack_a4 = 0.0;
      FUN_00566d20(&pvStack_84,&LAB_0048baa0,0,fStack_a8,0);
    }
    local_4._0_1_ = 6;
    if (pvVar1 != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(pvVar1,(iStack_7c - (int)pvVar1 >> 2) * 4);
    }
    local_4._0_1_ = 5;
    if (piStack_90 != (int *)0x0) {
      stlp_std::__node_alloc::deallocate(piStack_90,(iStack_88 - (int)piStack_90 >> 2) * 4);
    }
  }
  local_4._0_1_ = 0;
  FUN_0059f0d0();
  uVar6 = FUN_00844130();
  FUN_0085b840(uVar6);
  local_4 = CONCAT31(local_4._1_3_,0xd);
  iVar5 = FUN_004123d0();
  if (iVar5 != 0) {
    FUN_004123d0();
    iVar5 = FUN_0085acb0();
    if (iVar5 == 0) {
      cVar2 = FUN_00844020(0x27b);
      if (cVar2 == '\0') {
        iVar5 = FUN_004123d0();
        uVar6 = *(undefined4 *)(iVar5 + 0x74);
        uVar10 = FUN_00401260(0,0x100);
        FUN_005b6890(uVar6,0x39,uVar10);
      }
      else {
        uVar6 = FUN_00843dd0(&local_c0);
        uVar10 = FUN_00729eb0(uVar6);
        iVar5 = FUN_004123d0();
        uVar6 = *(undefined4 *)(iVar5 + 0x74);
        uVar19 = 0xffffffff;
        uVar17 = 0;
        uVar16 = 0x6ac;
        uVar15 = 1;
        uVar14 = 0;
        uVar11 = 0x39;
        FUN_00414670(uVar6,0x39,0,1,0x6ac,0,0xffffffff,uVar10);
        FUN_0043f4b0(uVar6,uVar11,uVar14,uVar15,uVar16,uVar17,uVar19,uVar10);
      }
    }
    else {
      uVar6 = FUN_00401260(0,0x100);
      FUN_005146b0(iVar5,0x39,uVar6);
    }
    iVar5 = FUN_00401360();
    local_c0 = (int *)(*(float *)(iVar5 + 100) + (float)_DAT_00a79a08);
    iVar5 = FUN_004123d0();
    *(int **)(iVar5 + 0xac) = local_c0;
  }
  local_4 = local_4 & 0xffffff00;
  FUN_008e0110();
  if (param_4 != '\0') {
    FUN_0050b770(param_1,1);
  }
  cVar2 = FUN_00844020(0x27b);
  if ((cVar2 == '\0') ||
     (((cVar2 = FUN_009768d0(0x173), cVar2 == '\0' && (cVar2 = FUN_009768d0(0x1fa4), cVar2 == '\0'))
      && ((sVar3 = (short)(local_c8[0] >> 0x10), sVar3 != 0x1595 &&
          ((sVar3 != 0x1b48 && (cVar2 = FUN_009768d0(0x2ac5), cVar2 == '\0')))))))) {
    FUN_005666e0(param_1,param_2,local_c8,local_b0);
  }
  cVar2 = FUN_009768d0(0x170d);
  if (cVar2 == '\0') {
    cVar2 = FUN_009768d0(0x1bdc);
    if (cVar2 != '\0') {
      uVar6 = FUN_004123d0(param_2);
      local_c9 = FUN_00567770(uVar6,param_2);
    }
  }
  else {
    cVar2 = FUN_00844020(0xdd0);
    ppiVar21 = &local_c0;
    iVar5 = 0x74 - (uint)(cVar2 != '\0');
    local_c0 = (int *)0x0;
    uStack_bc = 0;
    uVar6 = FUN_00844130(iVar5,ppiVar21);
    FUN_00414770(uVar6);
    FUN_00446800(uVar6,iVar5,ppiVar21);
    if ((char)local_b0 != '\0') {
      uVar4 = local_c8[0] >> 0x10;
      uVar6 = 0x2d;
      FUN_004151f0(0x2d,uVar4);
      iVar5 = FUN_00866140(uVar6,uVar4);
      if (iVar5 == 0) {
        uVar4 = local_c8[0] >> 0x10;
        uVar6 = 0x2d;
        FUN_004151f0(0x2d,uVar4);
        FUN_00866e50(uVar6,uVar4);
      }
      else {
        FUN_005c2760();
      }
      pfVar22 = &fStack_78;
      FUN_004143f0(pfVar22);
      uVar6 = FUN_0042bdb0(pfVar22);
      iVar5 = FUN_0072d9f0(uVar6);
      if (iVar5 == 5) {
        FUN_004ac4b0(0x4f,0);
      }
    }
  }
LAB_00568375:
  local_4 = 0xffffffff;
  FUN_008e0110();
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

