// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x447630L (requested via site 0x44a925)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00447630(float param_1,undefined4 param_2,undefined4 *param_3)

{
  char cVar1;
  byte bVar2;
  undefined uVar3;
  bool bVar4;
  int iVar5;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbVar6;
  int iVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  undefined4 uVar10;
  undefined4 uVar11;
  float *pfVar12;
  undefined4 uVar13;
  undefined4 uVar14;
  float fVar15;
  uint uVar16;
  uint uVar17;
  undefined *puVar18;
  allocator<char> *paVar19;
  undefined4 uVar20;
  undefined4 uVar21;
  int *piVar22;
  undefined4 *puVar23;
  undefined4 *puVar24;
  undefined4 uVar25;
  void *pvVar26;
  int iVar27;
  undefined4 *puVar28;
  undefined2 in_FPUControlWord;
  float10 fVar29;
  float fVar30;
  float fVar31;
  float fVar32;
  float fVar33;
  float fVar34;
  float fVar35;
  float fVar36;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbVar37;
  int **ppiVar38;
  float **ppfVar39;
  undefined4 uVar40;
  undefined auStack_78c [3];
  byte local_789;
  float fStack_788;
  float local_784;
  uint local_780;
  int local_77c;
  float local_778;
  undefined4 local_774;
  undefined4 *local_770;
  int local_76c;
  float fStack_768;
  float *local_764;
  float local_760;
  float local_75c;
  char local_755;
  uint local_754;
  void *pvStack_750;
  int local_74c;
  float *local_748;
  float local_744;
  float local_740;
  float local_73c;
  void *local_738;
  undefined4 uStack_734;
  float fStack_730;
  allocator<char> aStack_72a;
  allocator<char> local_729;
  allocator<char> aStack_728;
  allocator<char> aStack_727;
  allocator<char> aStack_726;
  allocator<char> aStack_725;
  void *pvStack_724;
  void *local_720;
  undefined4 uStack_71c;
  float fStack_718;
  undefined local_714 [8];
  void *local_70c;
  int iStack_708;
  int local_704;
  void *local_700 [2];
  int iStack_6f8;
  void *local_6f4 [2];
  int iStack_6ec;
  void *local_6e8 [2];
  int iStack_6e0;
  void *local_6dc [2];
  int iStack_6d4;
  void *local_6d0 [2];
  int iStack_6c8;
  void *local_6c4 [2];
  int iStack_6bc;
  void *local_6b8 [2];
  int iStack_6b0;
  void *local_6ac [2];
  int iStack_6a4;
  void *local_6a0 [2];
  int iStack_698;
  void *local_694 [2];
  int iStack_68c;
  void *local_688 [2];
  int iStack_680;
  void *local_67c [2];
  int iStack_674;
  void *local_670 [2];
  int iStack_668;
  void *local_664 [2];
  int iStack_65c;
  void *local_658 [2];
  int iStack_650;
  void *local_64c [2];
  int iStack_644;
  void *local_640 [2];
  int iStack_638;
  void *local_634 [2];
  int iStack_62c;
  void *local_628 [2];
  int iStack_620;
  int iStack_61c;
  undefined auStack_618 [4];
  undefined4 uStack_614;
  undefined4 uStack_610;
  undefined4 uStack_60c;
  undefined4 uStack_608;
  undefined4 uStack_604;
  undefined4 uStack_600;
  undefined4 uStack_5fc;
  undefined4 uStack_5f8;
  undefined4 uStack_5f4;
  undefined4 uStack_5f0;
  int iStack_5ec;
  undefined auStack_5e8 [4];
  undefined4 uStack_5e4;
  undefined4 uStack_5e0;
  undefined4 uStack_5dc;
  undefined4 local_5d8;
  undefined4 local_5d4;
  undefined4 local_5d0;
  undefined4 local_5cc;
  undefined4 local_5c8;
  undefined4 local_5c4;
  undefined4 local_5c0;
  undefined4 local_5bc;
  undefined4 local_5b8;
  undefined local_5a8 [12];
  undefined local_59c [12];
  undefined local_590 [24];
  undefined local_578 [12];
  undefined local_56c [12];
  undefined auStack_560 [12];
  undefined auStack_554 [12];
  undefined auStack_548 [28];
  undefined auStack_52c [32];
  undefined local_50c [40];
  undefined local_4e4 [8];
  undefined auStack_4dc [8];
  undefined auStack_4d4 [24];
  undefined auStack_4bc [24];
  undefined local_4a4 [8];
  undefined auStack_49c [24];
  undefined auStack_484 [8];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_47c [24];
  undefined auStack_464 [8];
  undefined local_45c [8];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_454 [32];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_434 [56];
  undefined local_3fc [24];
  undefined local_3e4 [24];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_3cc [36];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_3a8 [24];
  undefined auStack_390 [12];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_384 [36];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_360 [36];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_33c [272];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  local_22c [24];
  int *local_214 [2];
  int iStack_20c;
  void *local_1f0 [2];
  int iStack_1e8;
  void *local_1d8 [2];
  int iStack_1d0;
  undefined local_1b4 [104];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  local_14c [24];
  undefined local_134;
  undefined4 local_130;
  undefined4 local_12c;
  undefined4 local_128;
  float local_124;
  float local_120;
  basic_stringstream<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  local_f0 [16];
  undefined auStack_e0 [208];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  uint local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_0099e742;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_78c;
  ExceptionList = &local_c;
  local_774 = param_3;
  local_784 = 0.0;
  FUN_0052a490();
  FUN_00444800();
  iVar5 = FUN_0052ba20();
  if (iVar5 == 1) goto LAB_0044c041;
  FUN_0040b980();
  local_74c = FUN_0052a470();
  local_74c = local_74c + param_3[1];
  pbVar6 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *)
           FUN_0052a490();
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (local_22c,pbVar6);
  local_4._0_1_ = 0;
  local_4._1_3_ = 0;
  local_754 = 0;
  local_780 = 0;
  iVar7 = FUN_00401360();
  local_778 = *(float *)(iVar7 + 100);
  switch(iVar5) {
  case 2:
    uVar25 = FUN_0052a470();
    FUN_0085b840();
    local_4 = CONCAT31(local_4._1_3_,1);
    iVar5 = FUN_004123d0();
    if (iVar5 != 0) {
      FUN_004123d0();
      iVar5 = FUN_0085acb0();
      if (iVar5 != 0) {
        FUN_00401260(0);
        FUN_005146b0(iVar5,uVar25);
      }
    }
    local_4 = local_4 & 0xffffff00;
    FUN_008e0110();
    break;
  case 3:
    FUN_0052a470();
    FUN_0052a470();
    FUN_0052a470();
    FUN_0052a470();
    FUN_004445b0(param_1,&local_754);
    break;
  case 4:
    pbVar6 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)FUN_0052a490();
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)local_1f0,pbVar6);
    local_4._0_1_ = 0x54;
    pbVar6 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)FUN_0052a490();
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)local_1d8,pbVar6);
    local_4._0_1_ = 0x55;
    uVar25 = FUN_0052a470();
    fVar29 = (float10)FUN_0052a450();
    local_73c = (float)fVar29;
    FUN_0052a470();
    FUN_0052a6d0(local_590);
    local_4._0_1_ = 0x56;
    FUN_00444470();
    local_4._0_1_ = 0x55;
    FUN_006adf00();
    local_764 = (float *)-(float)local_764;
    local_760 = -local_760;
    FUN_0052a6d0(local_578);
    local_4._0_1_ = 0x57;
    FUN_00444470();
    local_4._0_1_ = 0x55;
    FUN_006adf00();
    local_789 = FUN_0052a590();
    local_755 = FUN_0052a590();
    stlp_std::
    basic_stringstream<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
    basic_stringstream<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (local_f0,0x18);
    local_4 = CONCAT31(local_4._1_3_,0x58);
    FUN_004072d0(auStack_e0);
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                   *)local_1f0);
    if (bVar4) {
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      operator=((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)local_1f0,"Scene Root");
    }
    FUN_00444650(uVar25,&local_770,local_1f0,&local_764);
    local_778 = (float)FUN_0052a470();
    if (local_778 == 0.0) {
LAB_0044a0e2:
      bVar4 = false;
    }
    else {
      pbVar6 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)stlp_std::
                  basic_stringstream<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  ::str(local_f0);
      local_4 = CONCAT31(local_4._1_3_,0x59);
      local_784 = 1.4013e-45;
      bVar4 = stlp_std::
              basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ::empty(pbVar6);
      if (bVar4) goto LAB_0044a0e2;
      bVar4 = true;
    }
    local_4 = 0x58;
    if (((uint)local_784 & 1) != 0) {
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                (abStack_3cc);
    }
    if (bVar4) {
      bVar4 = stlp_std::
              basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ::empty(local_22c);
      fVar15 = param_1;
      if (!bVar4) {
        fVar15 = (float)FUN_00529d90(param_1);
      }
      if (((fVar15 != 0.0) && (FUN_004445b0(fVar15,&local_754), local_780 != 0)) &&
         (iVar5 = FUN_006c9200(), iVar5 == 0)) {
        cVar1 = FUN_0052a590();
        bVar2 = local_789 != 0;
        if (cVar1 != '\0') {
          bVar2 = bVar2 | 4;
        }
        FUN_00730700();
        local_4._0_1_ = 0x5a;
        FUN_00743fd0();
        FUN_00853a50();
        local_770 = (undefined4 *)operator_new(0x110);
        local_4._0_1_ = 0x5b;
        if (local_770 == (undefined4 *)0x0) {
          iVar5 = 0;
        }
        else {
          FUN_00733340();
          iVar5 = FUN_006c8f80(local_1b4,bVar2);
        }
        local_4._0_1_ = 0x5a;
        *(undefined4 *)(iVar5 + 0x48) = 5;
        *(undefined4 *)(iVar5 + 0x4c) = 0;
        if (local_755 != '\0') {
          FUN_006c66c0();
        }
        FUN_006c9490(local_1f0,local_1d8,iVar5,1,local_73c,&local_764,local_214);
        local_4._0_1_ = 0x5c;
        FUN_006c9040();
        iVar5 = local_74c;
        if (0 < local_74c) {
          local_770 = (undefined4 *)operator_new(0x18);
          local_4._0_1_ = 0x5d;
          if (local_770 == (undefined4 *)0x0) {
            uVar25 = 0;
          }
          else {
            uVar25 = FUN_0052a260();
          }
          local_4._0_1_ = 0x5c;
          FUN_00444800();
          FUN_0052ba40();
          FUN_0052b5c0(2);
          stlp_std::
          basic_stringstream<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
          ::str(local_f0);
          local_4._0_1_ = 0x5e;
          FUN_0052b5c0(0x1b);
          local_4._0_1_ = 0x5c;
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_3a8);
          FUN_0052b5c0(9);
          pvVar26 = operator_new(0x14);
          if (pvVar26 == (void *)0x0) {
            local_73c = 0.0;
          }
          else {
            local_73c = (float)FUN_00444440(param_1,uVar25,*local_774,local_774[1]);
          }
          uVar25 = FUN_0040bfe0(iVar5,iVar5 >> 0x1f,2);
          uVar25 = FUN_0040b8f0(auStack_4bc,local_714,uVar25);
          FUN_00444880(uVar25);
          FUN_00446030(&local_770);
        }
        local_4._0_1_ = 0x5a;
        FUN_0043a290();
        local_4 = CONCAT31(local_4._1_3_,0x58);
        FUN_00730730();
      }
    }
    local_4._0_1_ = 0x55;
    stlp_std::
    basic_stringstream<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
    _vbase_destructor_(local_f0);
    local_4._0_1_ = 0x54;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)local_1d8);
    local_4 = (uint)local_4._1_3_ << 8;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)local_1f0);
    break;
  case 5:
    pbVar6 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)FUN_0052a490();
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)local_214,pbVar6);
    local_4 = CONCAT31(local_4._1_3_,0x5f);
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty(local_22c);
    if (!bVar4) {
      param_1 = (float)FUN_00529d90(param_1);
    }
    if ((param_1 != 0.0) && (FUN_004445b0(param_1,&local_754), local_780 != 0)) {
      FUN_006c9120();
    }
    local_4 = local_4 & 0xffffff00;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)local_214);
    break;
  case 6:
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty(local_22c);
    if ((!bVar4) && (iVar5 = FUN_00529d90(param_1), iVar5 == 0)) {
      fVar29 = (float10)FUN_0052a450();
      fStack_788 = (float)fVar29;
      bVar2 = FUN_0052a590();
      local_789 = bVar2;
      cVar1 = FUN_0052a590();
      if ((bVar2 == 0) || (cVar1 == '\0')) {
        bVar4 = false;
      }
      else {
        bVar4 = true;
      }
      FUN_0052a6d0(auStack_560);
      local_4._0_1_ = 0x60;
      FUN_00444470();
      local_4._0_1_ = 0;
      FUN_006adf00();
      local_764 = (float *)-(float)local_764;
      local_760 = -local_760;
      FUN_0052a6d0(auStack_548);
      local_4._0_1_ = 0x61;
      FUN_00444470();
      local_4 = (uint)local_4._1_3_ << 8;
      FUN_006adf00();
      if (bVar4) {
        FUN_00401360();
        FUN_00485050();
        FUN_0048bba0();
      }
      else if (local_789 != 0) {
        FUN_00401360();
        FUN_00485050();
        FUN_0074c6d0();
      }
      uVar3 = FUN_0052a590();
      local_780 = CONCAT31(local_780._1_3_,uVar3);
      local_755 = FUN_0052a590();
      uVar16 = FUN_0052a470();
      FUN_0052a6d0(&local_70c);
      local_748 = (float *)0x0;
      local_744 = 0.0;
      local_4._0_1_ = 0x62;
      local_740 = 0.0;
      local_738 = (void *)0x0;
      uStack_734 = 0;
      fStack_730 = 0.0;
      if (local_789 == 0) {
        FUN_0085b840();
        local_4 = CONCAT31(local_4._1_3_,99);
        iVar5 = FUN_004123d0();
        if (iVar5 != 0) {
          iVar5 = FUN_004123d0();
          local_748 = *(float **)(iVar5 + 0x44);
          local_744 = *(float *)(iVar5 + 0x48);
          local_740 = *(float *)(iVar5 + 0x4c);
          iVar5 = FUN_004123d0();
          local_738 = *(void **)(iVar5 + 0x5c);
          uStack_734 = *(undefined4 *)(iVar5 + 0x60);
          fStack_730 = *(float *)(iVar5 + 100);
          fVar29 = (float10)FUN_00444940();
          if ((float10)_DAT_00a797c8 < fVar29) {
            FUN_0096cdd0();
            puVar23 = (undefined4 *)FUN_004444d0(auStack_390);
            local_764 = (float *)*puVar23;
            local_760 = (float)puVar23[1];
            local_75c = (float)puVar23[2];
          }
          FUN_00444490();
          FUN_00444490();
        }
        local_4._0_1_ = 0x62;
        FUN_008e0110();
      }
      else {
        local_748 = local_764;
        local_744 = local_760;
        local_740 = local_75c;
        local_738 = local_720;
        uStack_734 = uStack_71c;
        fStack_730 = fStack_718;
      }
      pvVar26 = pvStack_750;
      if (local_755 != '\0') {
        fVar29 = (float10)FUN_0052a450();
        pvStack_750 = (void *)(float)fVar29;
        FUN_00414a70();
        FUN_008dc540();
        FUN_009300f0();
        fVar29 = (float10)FUN_004444b0(iStack_20c);
        local_778 = (float)fVar29;
        fVar29 = (float10)FUN_004444b0(fStack_730);
        local_784 = (float)fVar29;
        if (local_778 < 0.0 != NAN(local_778)) {
          local_778 = local_778 + (float)_DAT_00a7aeb0;
        }
        if (local_784 < 0.0 != NAN(local_784)) {
          local_784 = local_784 + (float)_DAT_00a7aeb0;
        }
        local_73c = ABS(local_778 - local_784);
        pvVar26 = (void *)ABS((float)pvStack_750);
        if (local_73c < (float)pvVar26) {
          local_784 = ((float)pvVar26 - local_778) + local_784;
          if ((float)pvStack_750 < 0.0 != NAN((float)pvStack_750)) {
            local_784 = -local_784;
          }
          fStack_730 = local_784 + fStack_730;
        }
      }
      pvStack_750 = pvVar26;
      if ((char)local_780 != '\0') {
        fVar29 = (float10)FUN_0052a450();
        local_784 = (float)fVar29;
        FUN_00411f80(0,-local_784);
        FUN_00411f80(0,0);
        FUN_0096cdd0();
        FUN_004444d0(local_1f0);
        FUN_006a7090(&local_770);
        uVar25 = 0;
        puVar23 = local_770;
        iVar5 = local_76c;
        FUN_004154f0(local_770,local_76c,0);
        fVar29 = (float10)FUN_00853a80(puVar23,iVar5,uVar25);
        fStack_768 = (float)fVar29;
        pvStack_750 = (void *)((fStack_768 - local_740) / ABS(local_784));
        fVar29 = (float10)FUN_00437e30();
        local_778 = (float)fVar29;
        if (local_784 < 0.0) {
          local_778 = -local_778;
        }
        local_738 = (void *)-local_778;
      }
      if (uVar16 != 0) {
        local_789 = (byte)uVar16 & 1;
        local_780 = CONCAT31(local_780._1_3_,(char)(uVar16 >> 1)) & 0xffffff01;
        if ((((uVar16 >> 1 & 1) != 0) || ((uVar16 >> 2 & 1) != 0)) || ((uVar16 & 1) != 0)) {
          local_770 = (undefined4 *)0x0;
          local_76c = 0;
          fStack_768 = 0.0;
          uVar17 = -(uint)((uVar16 & 1) != 0) & (uint)&local_770;
          pfVar12 = local_748;
          fVar15 = local_744;
          FUN_004154f0(local_748,local_744,uVar17);
          fVar29 = (float10)FUN_00853a80(pfVar12,fVar15,uVar17);
          local_784 = (float)fVar29;
          if ((uVar16 >> 2 & 1) == 0) {
            if ((char)local_780 != '\0') {
              local_740 = local_784;
            }
          }
          else {
            if (local_789 == 0) {
              local_740 = local_75c + local_784;
              goto LAB_0044aa92;
            }
            local_740 = local_784;
            FUN_0043ae80();
            FUN_00444490();
          }
          if (local_789 != 0) {
            FUN_00732fa0();
            FUN_00733080(&local_770);
            fStack_730 = 0.0;
            FUN_00444490();
          }
        }
      }
LAB_0044aa92:
      FUN_0052a470();
      FUN_00730700();
      local_4._0_1_ = 100;
      FUN_00743fd0();
      FUN_0072fd10();
      FUN_00853a50();
      FUN_00730f60();
      FUN_00730f90();
      FUN_00730fb0();
      paVar19 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_727);
      local_4._0_1_ = 0x65;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                (abStack_454,"",paVar19);
      uVar20 = 1;
      pbVar6 = abStack_454;
      uVar25 = 2;
      puVar18 = local_1b4;
      pbVar37 = local_14c;
      local_4._0_1_ = 0x66;
      FUN_004148f0(pbVar37,puVar18,2,pbVar6,1);
      iVar5 = FUN_00457930(pbVar37,puVar18,uVar25,pbVar6,uVar20);
      local_4._0_1_ = 0x65;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                (abStack_454);
      local_4._0_1_ = 100;
      stlp_std::allocator<char>::~allocator<char>(&aStack_727);
      if (iVar5 != 0) {
        FUN_0052a280(param_1,local_22c);
        if (0 < local_74c) {
          local_770 = (undefined4 *)operator_new(0x18);
          local_4._0_1_ = 0x67;
          if (local_770 == (undefined4 *)0x0) {
            uVar25 = 0;
          }
          else {
            uVar25 = FUN_0052a260();
          }
          local_4._0_1_ = 100;
          FUN_00444800();
          FUN_0052ba40();
          FUN_0052b5c0(2);
          FUN_0052b5c0(9);
          pvVar26 = operator_new(0x14);
          if (pvVar26 == (void *)0x0) {
            pvStack_750 = (void *)0x0;
          }
          else {
            pvStack_750 = (void *)FUN_00444440(param_1,uVar25,*local_774,local_774[1]);
          }
          uVar25 = FUN_0040bfe0(local_74c,local_74c >> 0x1f,2);
          uVar25 = FUN_0040b8f0(auStack_49c,local_714,uVar25);
          FUN_00444880(uVar25);
          FUN_00446030(&local_770);
        }
        FUN_004445b0(iVar5,&local_754);
        if (local_754 != 0) {
          if (2 < (uint)(iStack_708 - (int)local_70c >> 2)) {
            paVar19 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_728);
            local_4._0_1_ = 0x68;
            stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                      (abStack_434,"",paVar19);
            local_4._0_1_ = 0x69;
            FUN_0050a690(iVar5);
            local_4._0_1_ = 0x6b;
            stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                      (abStack_434);
            local_4._0_1_ = 0x6c;
            stlp_std::allocator<char>::~allocator<char>(&aStack_728);
            FUN_00719f70(0xff,0xff,0xff);
            uStack_5f8 = FUN_0095da40();
            uStack_60c = 0xff;
            uStack_604 = 0;
            uVar25 = FUN_004019c0(&uStack_60c);
            puVar18 = (undefined *)FUN_00401d40(&uStack_604,uVar25);
            local_774 = (undefined4 *)CONCAT31(local_774._1_3_,*puVar18);
            uStack_5fc = FUN_0095da40();
            uStack_610 = 0xff;
            uStack_5f0 = 0;
            uVar25 = FUN_004019c0(&uStack_610,&uStack_5fc);
            puVar18 = (undefined *)FUN_00401d40(&uStack_5f0,uVar25);
            local_774._0_2_ = CONCAT11(*puVar18,(undefined)local_774);
            uStack_608 = FUN_0095da40();
            uStack_5e4 = 0xff;
            uStack_600 = 0;
            uVar25 = FUN_004019c0(&uStack_5e4,&uStack_608);
            puVar18 = (undefined *)FUN_00401d40(&uStack_600,uVar25);
            local_774._0_3_ = CONCAT12(*puVar18,(undefined2)local_774);
            FUN_0050acc0(&DAT_00b8d124,&DAT_00b8d124);
            local_4._0_1_ = 100;
            FUN_0059f0d0();
          }
          FUN_00509570();
        }
      }
      local_4._0_1_ = 0x62;
      FUN_00730730();
      local_4 = (uint)local_4._1_3_ << 8;
      FUN_006adf00();
    }
    break;
  case 7:
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty(local_22c);
    if ((!bVar4) && (iVar5 = FUN_00529d90(param_1), iVar5 != 0)) {
      FUN_004154f0();
      FUN_00855dc0();
LAB_0044c024:
      FUN_0052a0b0(param_1);
    }
    break;
  case 8:
    uVar16 = FUN_0052a470();
    local_754 = uVar16;
    local_789 = FUN_0052a590();
    local_784 = (float)FUN_0052a470();
    if (uVar16 != 0) {
      switch(uVar16) {
      case 1:
        puVar23 = (undefined4 *)0x0;
        break;
      case 2:
      case 4:
      case 5:
        puVar23 = (undefined4 *)0x2;
        break;
      case 3:
        puVar23 = (undefined4 *)0x3;
        break;
      default:
        puVar23 = (undefined4 *)0xffffffff;
      }
      local_774 = puVar23;
      iVar5 = FUN_00414a70();
      puVar24 = *(undefined4 **)(iVar5 + 8);
      if ((puVar23 != (undefined4 *)0xffffffff) &&
         ((puVar24 != puVar23 || (local_784 == 1.4013e-45)))) {
        if (local_789 != 0) {
          if (puVar24 == (undefined4 *)0x0) {
            iVar5 = 1;
          }
          else if ((puVar24 == (undefined4 *)0x2) || (puVar24 == (undefined4 *)0x3)) {
            iVar5 = 4;
          }
          else {
            iVar5 = -1;
          }
          local_770 = (undefined4 *)operator_new(0x18);
          local_4._0_1_ = 0x4d;
          if (local_770 == (undefined4 *)0x0) {
            uVar25 = 0;
          }
          else {
            uVar25 = FUN_0052a260();
          }
          local_4._0_1_ = 0;
          FUN_00444800();
          FUN_0052ba40();
          FUN_0052b5c0(2);
          if (iVar5 == 4) {
            local_748 = (float *)0x0;
            ppfVar39 = &local_748;
            local_744 = 0.0;
            local_740 = 0.0;
            FUN_00414a70(ppfVar39);
            FUN_0045e850(ppfVar39);
            local_764 = (float *)0x0;
            local_760 = 0.0;
            local_75c = 0.0;
            FUN_0085b840();
            local_4 = CONCAT31(local_4._1_3_,0x4e);
            iVar5 = FUN_004123d0();
            if (iVar5 != 0) {
              FUN_004123d0();
              FUN_0045b5c0(local_3fc);
              puVar23 = (undefined4 *)FUN_00437e50(local_3e4);
              local_764 = (float *)*puVar23;
              local_760 = (float)puVar23[1];
              local_75c = (float)puVar23[2];
            }
            FUN_0096bb80();
            local_4._0_1_ = 0x4f;
            FUN_0052b280(0x27);
            local_4._0_1_ = 0x4e;
            FUN_006adf00();
            FUN_0052b460(0x28);
            local_4._0_1_ = 0;
            FUN_008e0110();
          }
          FUN_0052b4d0(0x29);
          FUN_0052b550(0x26);
          FUN_0052b550(0x25);
          pvVar26 = operator_new(0x14);
          if (pvVar26 == (void *)0x0) {
            local_784 = 0.0;
          }
          else {
            local_784 = (float)FUN_00444440(param_1,uVar25,*param_3,param_3[1]);
          }
          uVar25 = FUN_0040bfe0(local_74c,local_74c >> 0x1f,2);
          uVar25 = FUN_0040b8f0(local_45c,local_714,uVar25);
          FUN_00444880(uVar25);
          FUN_00446030(&local_770);
          uVar16 = local_754;
          puVar23 = local_774;
        }
        FUN_00414a70(puVar23);
        FUN_0045dac0(puVar23);
        if (uVar16 == 4) {
          fVar29 = (float10)FUN_0052a450();
          local_784 = (float)fVar29;
          FUN_0052a6d0(local_5a8);
          local_4._0_1_ = 0x50;
          FUN_00444470();
          local_4 = (uint)local_4._1_3_ << 8;
          FUN_006adf00();
          ppiVar38 = local_214;
          FUN_00414a70(ppiVar38);
          FUN_0045e800(ppiVar38);
        }
        else if (uVar16 == 5) {
          fVar29 = (float10)FUN_0052a450();
          local_784 = (float)fVar29;
          FUN_0052a6d0(local_59c);
          local_4._0_1_ = 0x51;
          FUN_00444470();
          local_4 = (uint)local_4._1_3_ << 8;
          FUN_006adf00();
          local_5d8 = _DAT_00a7ae30;
          local_5d4 = 0;
          ppiVar38 = local_214;
          local_5d0 = _DAT_00a7ae30;
          fVar15 = local_784;
          FUN_00414a70(local_784,ppiVar38);
          FUN_0045bec0(fVar15,ppiVar38);
          uVar25 = 1;
          FUN_00414a70(1);
          FUN_0045d1d0(uVar25);
        }
      }
    }
    break;
  case 9:
    local_784 = (float)FUN_0052a470();
    if ((int)local_784 < 1) {
      local_5cc = 0;
      puVar23 = &local_5cc;
      local_5c8 = 0;
      local_5c4 = 0;
      uVar20 = 0;
      uVar25 = FUN_00973500(0,puVar23);
      FUN_00414a70(uVar25);
      FUN_0045b560(uVar25,uVar20,puVar23);
    }
    else {
      local_5c0 = 0;
      puVar23 = &local_5c0;
      local_5bc = 0;
      local_5b8 = 0;
      fVar15 = (float)(int)local_784;
      uVar25 = FUN_0040bfe0(0x7fffffff,0,3);
      FUN_00414a70(uVar25,fVar15,puVar23);
      FUN_0045b560(uVar25,fVar15,puVar23);
      iVar5 = local_74c;
      if (local_74c != param_3[1] && -1 < local_74c - param_3[1]) {
        local_770 = (undefined4 *)operator_new(0x18);
        local_4._0_1_ = 0x52;
        if (local_770 == (undefined4 *)0x0) {
          uVar25 = 0;
        }
        else {
          uVar25 = FUN_0052a260();
        }
        local_4 = (uint)local_4._1_3_ << 8;
        FUN_00444800();
        FUN_0052ba40();
        FUN_0052b5c0(2);
        FUN_0052b550(0x2a);
        pvVar26 = operator_new(0x14);
        if (pvVar26 == (void *)0x0) {
          local_784 = 0.0;
        }
        else {
          local_784 = (float)FUN_00444440(param_1,uVar25,0,0);
        }
        uVar25 = FUN_0040bfe0(iVar5,iVar5 >> 0x1f,2);
        uVar25 = FUN_0040b8f0(local_50c,local_714,uVar25);
        goto LAB_00449f0e;
      }
    }
    break;
  case 10:
    fVar29 = (float10)FUN_0052a450();
    local_774 = (undefined4 *)(float)fVar29;
    fVar29 = (float10)FUN_0052a450();
    local_784 = (float)fVar29;
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty(local_22c);
    if (!bVar4) {
      param_1 = (float)FUN_00529d90(param_1);
    }
    FUN_004445b0(param_1,&local_754);
    if (local_780 != 0) {
      fVar15 = (float)local_74c / (float)_DAT_00a7a6e8;
      fVar36 = local_778;
      puVar23 = local_774;
      local_784 = fVar15;
      FUN_006c0f80(local_778,fVar15,local_774);
      FUN_006cf570(fVar36,fVar15,puVar23);
    }
    FUN_004143f0();
    fVar15 = (float)FUN_007ce1e0();
    if (param_1 == fVar15) {
      FUN_00414670(param_2);
      uVar25 = FUN_007d8f90();
      FUN_00447630(uVar25);
    }
    break;
  case 0xb:
    local_789 = FUN_0052a590();
    cVar1 = FUN_0052a590();
    local_784 = param_1;
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty(local_22c);
    fVar15 = param_1;
    if (!bVar4) {
      fVar15 = (float)FUN_00529d90(param_1);
      local_784 = fVar15;
    }
    FUN_004445b0(fVar15,&local_754);
    uVar16 = local_780;
    if (cVar1 == '\0') {
      if (local_754 != 0) {
        FUN_0050a1c0(local_789 == 0);
      }
    }
    else if ((local_780 == 0) || (iVar5 = FUN_006c0fc0(), iVar5 == 0)) {
      iVar5 = 0;
      if (uVar16 != 0) {
        iVar7 = FUN_006c12d0();
        if (iVar7 != 0) {
          FUN_006c12d0();
          iVar7 = FUN_00746550();
          iVar27 = FUN_006c66d0();
          do {
            iVar5 = iVar7;
            if (iVar5 == 0) break;
            iVar7 = *(int *)(iVar5 + 0x24);
          } while (*(int *)(iVar5 + 0x24) != iVar27);
        }
        iVar7 = FUN_006c66d0();
        uVar16 = 0;
        if (*(int *)(iVar7 + 0xd4) != 0) {
          do {
            iVar27 = FUN_0043a700();
            if ((iVar27 != 0) && (iVar27 = FUN_0043a700(), iVar27 != iVar5)) {
              uVar17 = (uint)(local_789 == 0);
              FUN_0043a700(uVar16);
              FUN_00444540(uVar17);
            }
            uVar16 = uVar16 + 1;
          } while (uVar16 < *(uint *)(iVar7 + 0xd4));
        }
      }
    }
    else {
      FUN_006c0fc0();
      iVar5 = FUN_006b22f0();
      if (iVar5 != 0) {
        FUN_00444540(local_789 == 0);
      }
    }
    FUN_004143f0();
    fVar15 = (float)FUN_007ce1e0();
    if (local_784 == fVar15) {
      FUN_00414670(param_2);
      uVar25 = FUN_007d8f90();
      FUN_00447630(uVar25);
    }
    cVar1 = FUN_0052a590();
    iVar5 = local_74c;
    if ((cVar1 != '\0') && (0 < local_74c)) {
      local_770 = (undefined4 *)operator_new(0x18);
      local_4._0_1_ = 0x53;
      if (local_770 == (undefined4 *)0x0) {
        uVar25 = 0;
      }
      else {
        uVar25 = FUN_0052b170();
      }
      local_4 = (uint)local_4._1_3_ << 8;
      FUN_0052b4d0(0x2d);
      FUN_0052b4d0(0x2f);
      FUN_0052b550(5);
      FUN_0052b550(6);
      pvVar26 = operator_new(0x14);
      if (pvVar26 == (void *)0x0) {
        local_784 = 0.0;
      }
      else {
        local_784 = (float)FUN_00444440(param_1,uVar25,0,0);
      }
      uVar25 = FUN_0040bfe0(iVar5,iVar5 >> 0x1f,2);
      uVar25 = FUN_0040b8f0(auStack_4dc,local_714,uVar25);
LAB_00449f0e:
      FUN_00444880(uVar25);
      FUN_00446030(&local_770);
    }
    break;
  case 0xc:
    uVar25 = FUN_0052a470();
    local_76c = local_74c;
    local_770 = (undefined4 *)0xfffffc18;
    FUN_00446800(param_1,uVar25);
    break;
  case 0xd:
    FUN_0052a470();
    uVar25 = FUN_0052a470(0x3e);
    uVar20 = FUN_0052a470(0x3d);
    uVar21 = FUN_0052a590(0x3c);
    uVar40 = FUN_0052a590(0x3b);
    fVar29 = (float10)FUN_0052a450(0x40);
    fVar15 = (float)fVar29;
    fVar29 = (float10)FUN_0052a450(0x3a);
    fVar36 = (float)fVar29;
    fVar29 = (float10)FUN_0052a450(0x39);
    fVar35 = (float)fVar29;
    fVar29 = (float10)FUN_0052a450(0x38);
    fVar34 = (float)fVar29;
    fVar29 = (float10)FUN_0052a450(0x37);
    fVar33 = (float)fVar29;
    uVar13 = FUN_0052a470(0x36);
    uVar14 = FUN_0052a470(0x35);
    uVar11 = FUN_0052a470(0x34);
    FUN_008b9c30(uVar11,uVar14,uVar13,fVar33,fVar34,fVar35,fVar36,fVar15,uVar40,uVar21,uVar20,uVar25
                );
    local_4 = CONCAT31(local_4._1_3_,2);
    FUN_004150f0();
    FUN_008b94d0();
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty(local_22c);
    if (!bVar4) {
      FUN_0052a0b0(param_1);
      FUN_0052a280(param_1,local_22c);
    }
    local_4 = local_4 & 0xffffff00;
    FUN_00445660();
    break;
  case 0xe:
    cVar1 = FUN_0052a590();
    fVar15 = param_1;
    if (cVar1 != '\0') {
      fVar15 = (float)FUN_00529d90(param_1);
    }
    if (fVar15 != 0.0) {
      FUN_0052a490();
      fVar29 = (float10)FUN_0052a450(0x45);
      fVar36 = (float)fVar29;
      uVar25 = FUN_0052a470(0x44);
      uVar20 = FUN_0052a470(0x43);
      fVar29 = (float10)FUN_0052a450(0x42);
      fVar35 = (float)fVar29;
      uVar21 = FUN_0052a470(0x3f);
      uVar40 = FUN_0052a470(0x3e);
      uVar13 = FUN_0052a470(0x3d);
      uVar14 = FUN_0052a590(0x3c);
      uVar11 = FUN_0052a590(0x3b);
      fVar29 = (float10)FUN_0052a450(0x3a);
      fVar34 = (float)fVar29;
      fVar29 = (float10)FUN_0052a450(0x39);
      fVar33 = (float)fVar29;
      fVar29 = (float10)FUN_0052a450(0x38);
      fVar32 = (float)fVar29;
      fVar29 = (float10)FUN_0052a450(0x37);
      fVar31 = (float)fVar29;
      fVar29 = (float10)FUN_0052a450(0x41);
      fVar30 = (float)fVar29;
      uVar8 = FUN_0052a470(0x36);
      uVar9 = FUN_0052a470(0x35);
      uVar10 = FUN_0052a470(0x34);
      FUN_008b9ad0(uVar10,uVar9,uVar8,fVar30,fVar31,fVar32,fVar33,fVar34,uVar11,uVar14,uVar13,uVar40
                   ,uVar21,fVar35,uVar20,uVar25,fVar36);
      local_4 = CONCAT31(local_4._1_3_,3);
      fVar36 = fVar15;
      FUN_004146f0(fVar15);
      FUN_00442c20(fVar36);
      if ((fVar15 == param_1) &&
         (bVar4 = stlp_std::
                  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  ::empty(local_22c), !bVar4)) {
        FUN_0052a0b0(param_1);
        FUN_0052a280(param_1,local_22c);
      }
      local_4 = local_4 & 0xffffff00;
      FUN_008b9a30();
    }
    break;
  case 0xf:
    FUN_0052a470();
    uVar25 = FUN_0052a470(0x3e);
    uVar20 = FUN_0052a470(0x3d);
    uVar21 = FUN_0052a590(0x3c);
    uVar40 = FUN_0052a590(0x3b);
    fVar29 = (float10)FUN_0052a450(0x3a);
    fVar15 = (float)fVar29;
    fVar29 = (float10)FUN_0052a450(0x39);
    fVar36 = (float)fVar29;
    fVar29 = (float10)FUN_0052a450(0x38);
    fVar35 = (float)fVar29;
    fVar29 = (float10)FUN_0052a450(0x37);
    fVar34 = (float)fVar29;
    fVar29 = (float10)FUN_0052a450(0x49);
    fVar33 = (float)fVar29;
    fVar29 = (float10)FUN_0052a450(0x48);
    fVar32 = (float)fVar29;
    uVar13 = FUN_0052a470(0x36);
    uVar14 = FUN_0052a470(0x35);
    uVar11 = FUN_0052a470(0x34);
    FUN_008b9d20(uVar11,uVar14,uVar13,fVar32,fVar33,fVar34,fVar35,fVar36,fVar15,uVar40,uVar21,uVar20
                 ,uVar25);
    local_4._0_1_ = 4;
    FUN_004146f0(param_1);
    FUN_00442c80(param_1);
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_00445660();
    break;
  case 0x10:
    FUN_0052a470();
    cVar1 = FUN_0052a590();
    if (cVar1 == '\0') {
      bVar4 = stlp_std::
              basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ::empty(local_22c);
      if ((!bVar4) && (iVar5 = FUN_00529d90(param_1), iVar5 != 0)) {
        FUN_004150f0(iVar5);
        FUN_008b7170(iVar5);
        goto LAB_0044c024;
      }
    }
    else {
      FUN_004146f0(param_1);
      FUN_00442e20(param_1);
    }
    break;
  case 0x11:
    FUN_004150f0();
    FUN_008b6460();
    break;
  case 0x12:
    FUN_00446a50();
    local_4._0_1_ = 5;
    FUN_0052a730(&local_748);
    local_4._0_1_ = 6;
    FUN_0052a730(local_214);
    local_4._0_1_ = 7;
    FUN_0052a730(local_1f0);
    local_4._0_1_ = 8;
    FUN_0052a730(local_1d8);
    local_4._0_1_ = 9;
    FUN_0052a730(local_67c);
    local_4._0_1_ = 10;
    FUN_0052a730(local_628);
    local_4._0_1_ = 0xb;
    FUN_0052a730(local_640);
    local_4._0_1_ = 0xc;
    FUN_0052a730(local_658);
    local_4._0_1_ = 0xd;
    FUN_0052a730(local_670);
    local_4._0_1_ = 0xe;
    FUN_0052a6d0(local_688);
    local_4._0_1_ = 0xf;
    FUN_0052a6d0(local_6a0);
    local_4._0_1_ = 0x10;
    FUN_0052a6d0(local_6e8);
    local_4._0_1_ = 0x11;
    FUN_0052a6d0(local_6f4);
    local_4._0_1_ = 0x12;
    FUN_0052a6d0(local_6b8);
    local_4._0_1_ = 0x13;
    FUN_0052a6d0(local_6d0);
    uVar16 = 0;
    pfVar12 = local_748;
    if ((int)local_744 - (int)local_748 >> 2 != 0) {
      do {
        local_4._0_1_ = 0x14;
        if (pfVar12[uVar16] != 0.0) {
          FUN_008b97e0(pfVar12[uVar16],local_214[0][uVar16],
                       *(int *)((int)local_670[0] + uVar16 * 4) == 1,
                       *(undefined4 *)((int)local_6e8[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_6f4[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_67c[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_628[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_6b8[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_6d0[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_640[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_658[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_688[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_6a0[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_1f0[0] + uVar16 * 4));
          local_4._0_1_ = 0x15;
          FUN_00446c20();
          pfVar12 = local_748;
        }
        uVar16 = uVar16 + 1;
      } while (uVar16 < (uint)((int)local_744 - (int)pfVar12 >> 2));
    }
    local_4._0_1_ = 0x14;
    FUN_0052a730(&local_764);
    local_4._0_1_ = 0x16;
    FUN_0052a730(local_6dc);
    local_4._0_1_ = 0x17;
    FUN_0052a730(local_634);
    local_4._0_1_ = 0x18;
    FUN_0052a6d0(local_694);
    local_4._0_1_ = 0x19;
    FUN_0052a6d0(local_664);
    local_4._0_1_ = 0x1a;
    FUN_0052a6d0(local_6ac);
    local_4._0_1_ = 0x1b;
    FUN_0052a6d0(local_64c);
    local_4._0_1_ = 0x1c;
    FUN_0052a730(local_700);
    local_4._0_1_ = 0x1d;
    FUN_0052a730(local_6c4);
    local_4._0_1_ = 0x1e;
    FUN_0052a6d0(&local_770);
    local_4._0_1_ = 0x1f;
    FUN_0052a6d0(&local_738);
    local_4._0_1_ = 0x20;
    FUN_0052a6d0(&local_720);
    local_4._0_1_ = 0x21;
    FUN_0052a6d0(&local_70c);
    uVar16 = 0;
    pfVar12 = local_764;
    if ((int)local_760 - (int)local_764 >> 2 != 0) {
      do {
        local_4._0_1_ = 0x22;
        if (pfVar12[uVar16] != 0.0) {
          FUN_008b9910(pfVar12[uVar16],*(undefined4 *)((int)local_6dc[0] + uVar16 * 4),
                       *(int *)((int)local_634[0] + uVar16 * 4) == 1,
                       *(undefined4 *)((int)local_694[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_664[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_6ac[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_64c[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_700[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_6c4[0] + uVar16 * 4),local_770[uVar16],
                       *(undefined4 *)((int)local_738 + uVar16 * 4),
                       *(undefined4 *)((int)local_720 + uVar16 * 4));
          local_4._0_1_ = 0x23;
          FUN_00446c60();
          pfVar12 = local_764;
        }
        uVar16 = uVar16 + 1;
      } while (uVar16 < (uint)((int)local_760 - (int)pfVar12 >> 2));
    }
    local_4._0_1_ = 0x22;
    FUN_004150f0();
    FUN_008b64a0();
    local_4._0_1_ = 0x21;
    if (local_70c != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_70c,(local_704 - (int)local_70c >> 2) * 4);
    }
    local_4._0_1_ = 0x20;
    if (local_720 != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_720,((int)fStack_718 - (int)local_720 >> 2) * 4);
    }
    local_4._0_1_ = 0x1f;
    if (local_738 != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_738,((int)fStack_730 - (int)local_738 >> 2) * 4);
    }
    local_4._0_1_ = 0x1e;
    if (local_770 != (undefined4 *)0x0) {
      stlp_std::__node_alloc::deallocate(local_770,((int)fStack_768 - (int)local_770 >> 2) * 4);
    }
    local_4._0_1_ = 0x1d;
    if (local_6c4[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6c4[0],(iStack_6bc - (int)local_6c4[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x1c;
    if (local_700[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_700[0],(iStack_6f8 - (int)local_700[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x1b;
    if (local_64c[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_64c[0],(iStack_644 - (int)local_64c[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x1a;
    if (local_6ac[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6ac[0],(iStack_6a4 - (int)local_6ac[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x19;
    if (local_664[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_664[0],(iStack_65c - (int)local_664[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x18;
    if (local_694[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_694[0],(iStack_68c - (int)local_694[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x17;
    if (local_634[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_634[0],(iStack_62c - (int)local_634[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x16;
    if (local_6dc[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6dc[0],(iStack_6d4 - (int)local_6dc[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x14;
    if (local_764 != (float *)0x0) {
      stlp_std::__node_alloc::deallocate(local_764,((int)local_75c - (int)local_764 >> 2) * 4);
    }
    local_4._0_1_ = 0x13;
    if (local_6d0[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6d0[0],(iStack_6c8 - (int)local_6d0[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x12;
    if (local_6b8[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6b8[0],(iStack_6b0 - (int)local_6b8[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x11;
    if (local_6f4[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6f4[0],(iStack_6ec - (int)local_6f4[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x10;
    if (local_6e8[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6e8[0],(iStack_6e0 - (int)local_6e8[0] >> 2) * 4);
    }
    local_4._0_1_ = 0xf;
    if (local_6a0[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6a0[0],(iStack_698 - (int)local_6a0[0] >> 2) * 4);
    }
    local_4._0_1_ = 0xe;
    if (local_688[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_688[0],(iStack_680 - (int)local_688[0] >> 2) * 4);
    }
    local_4._0_1_ = 0xd;
    if (local_670[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_670[0],(iStack_668 - (int)local_670[0] >> 2) * 4);
    }
    local_4._0_1_ = 0xc;
    if (local_658[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_658[0],(iStack_650 - (int)local_658[0] >> 2) * 4);
    }
    local_4._0_1_ = 0xb;
    if (local_640[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_640[0],(iStack_638 - (int)local_640[0] >> 2) * 4);
    }
    local_4._0_1_ = 10;
    if (local_628[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_628[0],(iStack_620 - (int)local_628[0] >> 2) * 4);
    }
    local_4._0_1_ = 9;
    if (local_67c[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_67c[0],(iStack_674 - (int)local_67c[0] >> 2) * 4);
    }
    local_4._0_1_ = 8;
    if (local_1d8[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_1d8[0],(iStack_1d0 - (int)local_1d8[0] >> 2) * 4);
    }
    local_4._0_1_ = 7;
    if (local_1f0[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_1f0[0],(iStack_1e8 - (int)local_1f0[0] >> 2) * 4);
    }
    local_4._0_1_ = 6;
    if (local_214[0] != (int *)0x0) {
      stlp_std::__node_alloc::deallocate(local_214[0],(iStack_20c - (int)local_214[0] >> 2) * 4);
    }
    local_4._0_1_ = 5;
    if (local_748 != (float *)0x0) {
      stlp_std::__node_alloc::deallocate(local_748,((int)local_740 - (int)local_748 >> 2) * 4);
    }
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_00446ad0();
    break;
  case 0x13:
    FUN_0052a470();
    FUN_004150f0();
    FUN_008b6480();
    break;
  case 0x14:
    FUN_00446a50();
    local_4._0_1_ = 0x24;
    FUN_0052a730(&local_748);
    local_4._0_1_ = 0x25;
    FUN_0052a730(&local_770);
    local_4._0_1_ = 0x26;
    FUN_0052a730(&local_738);
    local_4._0_1_ = 0x27;
    FUN_0052a730(&local_720);
    local_4._0_1_ = 0x28;
    FUN_0052a730(&local_70c);
    local_4._0_1_ = 0x29;
    FUN_0052a730(local_6c4);
    local_4._0_1_ = 0x2a;
    FUN_0052a730(local_700);
    local_4._0_1_ = 0x2b;
    FUN_0052a730(local_64c);
    local_4._0_1_ = 0x2c;
    FUN_0052a730(local_6ac);
    local_4._0_1_ = 0x2d;
    FUN_0052a6d0(local_664);
    local_4._0_1_ = 0x2e;
    FUN_0052a6d0(local_694);
    local_4._0_1_ = 0x2f;
    FUN_0052a6d0(local_634);
    local_4._0_1_ = 0x30;
    FUN_0052a6d0(local_6dc);
    local_4._0_1_ = 0x31;
    FUN_0052a6d0(local_6d0);
    local_4._0_1_ = 0x32;
    FUN_0052a6d0(local_6b8);
    uVar16 = 0;
    pfVar12 = local_748;
    if ((int)local_744 - (int)local_748 >> 2 != 0) {
      do {
        local_4._0_1_ = 0x33;
        if (pfVar12[uVar16] != 0.0) {
          FUN_008b97e0(pfVar12[uVar16],local_770[uVar16],
                       *(int *)((int)local_6ac[0] + uVar16 * 4) == 1,
                       *(undefined4 *)((int)local_634[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_6dc[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_70c + uVar16 * 4),
                       *(undefined4 *)((int)local_6c4[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_6d0[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_6b8[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_700[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_64c[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_664[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_694[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_738 + uVar16 * 4));
          local_4._0_1_ = 0x34;
          FUN_00446c20();
          pfVar12 = local_748;
        }
        uVar16 = uVar16 + 1;
      } while (uVar16 < (uint)((int)local_744 - (int)pfVar12 >> 2));
    }
    local_4._0_1_ = 0x33;
    FUN_0052a730(&local_764);
    local_4._0_1_ = 0x35;
    FUN_0052a730(local_6f4);
    local_4._0_1_ = 0x36;
    FUN_0052a730(local_6e8);
    local_4._0_1_ = 0x37;
    FUN_0052a6d0(local_6a0);
    local_4._0_1_ = 0x38;
    FUN_0052a6d0(local_688);
    local_4._0_1_ = 0x39;
    FUN_0052a6d0(local_670);
    local_4._0_1_ = 0x3a;
    FUN_0052a6d0(local_658);
    local_4._0_1_ = 0x3b;
    FUN_0052a730(local_640);
    local_4._0_1_ = 0x3c;
    FUN_0052a730(local_628);
    local_4._0_1_ = 0x3d;
    FUN_0052a6d0(local_67c);
    local_4._0_1_ = 0x3e;
    FUN_0052a6d0(local_1d8);
    local_4._0_1_ = 0x3f;
    FUN_0052a6d0(local_1f0);
    local_4._0_1_ = 0x40;
    FUN_0052a6d0(local_214);
    uVar16 = 0;
    pfVar12 = local_764;
    if ((int)local_760 - (int)local_764 >> 2 != 0) {
      do {
        local_4._0_1_ = 0x41;
        if (pfVar12[uVar16] != 0.0) {
          FUN_008b9910(pfVar12[uVar16],*(undefined4 *)((int)local_6f4[0] + uVar16 * 4),
                       *(int *)((int)local_6e8[0] + uVar16 * 4) == 1,
                       *(undefined4 *)((int)local_6a0[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_688[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_670[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_658[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_640[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_628[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_67c[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_1d8[0] + uVar16 * 4),
                       *(undefined4 *)((int)local_1f0[0] + uVar16 * 4));
          local_4._0_1_ = 0x42;
          FUN_00446c60();
          pfVar12 = local_764;
        }
        uVar16 = uVar16 + 1;
      } while (uVar16 < (uint)((int)local_760 - (int)pfVar12 >> 2));
    }
    local_4._0_1_ = 0x41;
    iVar5 = FUN_0052a470();
    local_134 = iVar5 != 0;
    fVar29 = (float10)FUN_0052a450();
    local_124 = (float)fVar29;
    fVar29 = (float10)FUN_0052a450();
    local_120 = (float)fVar29;
    FUN_0085b840();
    local_4 = CONCAT31(local_4._1_3_,0x43);
    iVar5 = FUN_004123d0();
    if (iVar5 != 0) {
      iVar5 = FUN_004123d0();
      local_130 = *(undefined4 *)(iVar5 + 0x44);
      local_12c = *(undefined4 *)(iVar5 + 0x48);
      local_128 = *(undefined4 *)(iVar5 + 0x4c);
    }
    pbVar6 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)FUN_0052a490();
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::operator=(local_14c,pbVar6);
    uVar25 = FUN_0052a470(0x6b);
    pbVar6 = local_14c;
    FUN_004150f0(pbVar6,uVar25);
    FUN_008b64c0(pbVar6,uVar25);
    local_4._0_1_ = 0x41;
    FUN_008e0110();
    local_4._0_1_ = 0x40;
    if (local_214[0] != (int *)0x0) {
      stlp_std::__node_alloc::deallocate(local_214[0],(iStack_20c - (int)local_214[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x3f;
    if (local_1f0[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_1f0[0],(iStack_1e8 - (int)local_1f0[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x3e;
    if (local_1d8[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_1d8[0],(iStack_1d0 - (int)local_1d8[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x3d;
    if (local_67c[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_67c[0],(iStack_674 - (int)local_67c[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x3c;
    if (local_628[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_628[0],(iStack_620 - (int)local_628[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x3b;
    if (local_640[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_640[0],(iStack_638 - (int)local_640[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x3a;
    if (local_658[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_658[0],(iStack_650 - (int)local_658[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x39;
    if (local_670[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_670[0],(iStack_668 - (int)local_670[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x38;
    if (local_688[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_688[0],(iStack_680 - (int)local_688[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x37;
    if (local_6a0[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6a0[0],(iStack_698 - (int)local_6a0[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x36;
    if (local_6e8[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6e8[0],(iStack_6e0 - (int)local_6e8[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x35;
    if (local_6f4[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6f4[0],(iStack_6ec - (int)local_6f4[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x33;
    if (local_764 != (float *)0x0) {
      stlp_std::__node_alloc::deallocate(local_764,((int)local_75c - (int)local_764 >> 2) * 4);
    }
    local_4._0_1_ = 0x32;
    if (local_6b8[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6b8[0],(iStack_6b0 - (int)local_6b8[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x31;
    if (local_6d0[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6d0[0],(iStack_6c8 - (int)local_6d0[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x30;
    if (local_6dc[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6dc[0],(iStack_6d4 - (int)local_6dc[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x2f;
    if (local_634[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_634[0],(iStack_62c - (int)local_634[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x2e;
    if (local_694[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_694[0],(iStack_68c - (int)local_694[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x2d;
    if (local_664[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_664[0],(iStack_65c - (int)local_664[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x2c;
    if (local_6ac[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6ac[0],(iStack_6a4 - (int)local_6ac[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x2b;
    if (local_64c[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_64c[0],(iStack_644 - (int)local_64c[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x2a;
    if (local_700[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_700[0],(iStack_6f8 - (int)local_700[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x29;
    if (local_6c4[0] != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_6c4[0],(iStack_6bc - (int)local_6c4[0] >> 2) * 4);
    }
    local_4._0_1_ = 0x28;
    if (local_70c != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_70c,(local_704 - (int)local_70c >> 2) * 4);
    }
    local_4._0_1_ = 0x27;
    if (local_720 != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_720,((int)fStack_718 - (int)local_720 >> 2) * 4);
    }
    local_4._0_1_ = 0x26;
    if (local_738 != (void *)0x0) {
      stlp_std::__node_alloc::deallocate(local_738,((int)fStack_730 - (int)local_738 >> 2) * 4);
    }
    local_4._0_1_ = 0x25;
    if (local_770 != (undefined4 *)0x0) {
      stlp_std::__node_alloc::deallocate(local_770,((int)fStack_768 - (int)local_770 >> 2) * 4);
    }
    local_4._0_1_ = 0x24;
    FUN_006adf00();
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_00446ad0();
    break;
  case 0x15:
    pbVar6 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)FUN_0052a490();
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)local_214,pbVar6);
    local_4._0_1_ = 0x44;
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                   *)local_214);
    if (bVar4) {
      FUN_0052a470();
      FUN_004150f0();
      FUN_008b64f0();
      local_4 = (uint)local_4._1_3_ << 8;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)local_214);
    }
    else {
      FUN_0052a470();
      ppiVar38 = local_214;
      FUN_004150f0(ppiVar38);
      FUN_008b6510(ppiVar38);
      local_4 = (uint)local_4._1_3_ << 8;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)local_214);
    }
    break;
  case 0x16:
    uVar25 = FUN_0052a730(local_56c);
    local_4._0_1_ = 0x45;
    uVar20 = FUN_0052a590(0x72);
    uVar21 = FUN_0052a470(0x71);
    uVar40 = FUN_0052a470(0x70);
    uVar13 = FUN_0052a470(0x6f);
    uVar14 = FUN_0052a490(9);
    FUN_00445fa0(uVar14,uVar25,uVar13,uVar40,uVar21,uVar20);
    local_4._0_1_ = 0x47;
    FUN_006adf00();
    uVar25 = FUN_0052a470(0x6d);
    FUN_004150f0(uVar25);
    FUN_008b6440(uVar25);
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_00445690();
    break;
  case 0x17:
    FUN_004150f0();
    FUN_008b72c0();
    break;
  case 0x18:
    FUN_004150f0();
    cVar1 = FUN_008b6420();
    iVar5 = local_74c;
    if ((cVar1 != '\0') && (0 < local_74c)) {
      local_770 = (undefined4 *)operator_new(0x18);
      local_4._0_1_ = 0x48;
      if (local_770 == (undefined4 *)0x0) {
        uVar25 = 0;
      }
      else {
        uVar25 = FUN_0052a260();
      }
      local_4._0_1_ = 0;
      FUN_00444800();
      FUN_0052ba40();
      FUN_0052b5c0(2);
      pvVar26 = operator_new(0x14);
      if (pvVar26 == (void *)0x0) {
        local_784 = 0.0;
      }
      else {
        local_784 = (float)FUN_00444440(param_1,uVar25,*param_3,param_3[1]);
      }
      uVar25 = FUN_0040bfe0(iVar5,iVar5 >> 0x1f,2);
      uVar25 = FUN_0040b8f0(local_4e4,local_714,uVar25);
      FUN_00444880(uVar25);
      FUN_00446030(&local_770);
    }
    FUN_0052a470();
    FUN_004150f0();
    FUN_008b63e0();
    break;
  case 0x19:
  case 0x1a:
  case 0x1b:
    local_784 = (float)FUN_0052a470();
    uVar25 = FUN_0052a470();
    paVar19 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_729);
    local_4._0_1_ = 0x49;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)local_214,paVar19);
    local_4 = CONCAT31(local_4._1_3_,0x4b);
    stlp_std::allocator<char>::~allocator<char>(&local_729);
    fVar15 = param_1;
    if (iVar5 == 0x1a) {
      bVar4 = stlp_std::
              basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ::empty(local_22c);
      if (!bVar4) {
        fVar15 = (float)FUN_00529d90(param_1);
      }
      pbVar6 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)FUN_0052a490();
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      operator=((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 *)local_214,pbVar6);
    }
    else if (iVar5 == 0x1b) {
      fVar15 = (float)FUN_00529d90(param_1);
    }
    FUN_004445b0(fVar15,&local_754);
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                   *)local_214);
    uVar16 = local_780;
    if (!bVar4) {
      if (local_780 != 0) {
        uVar16 = FUN_006c9200();
        goto LAB_00449497;
      }
      goto switchD_004494bb_caseD_2;
    }
LAB_00449497:
    if ((uVar16 == 0) || (iVar5 = FUN_007e0e40(), iVar5 == 0)) goto switchD_004494bb_caseD_2;
    switch(local_784) {
    case 0.0:
      FUN_007e0e40(uVar25);
      FUN_006d09d0(uVar25);
      local_4 = local_4 & 0xffffff00;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)local_214);
      break;
    case 1.4013e-45:
      FUN_007e0e40(uVar25);
      FUN_006d0990(uVar25);
      local_770 = (undefined4 *)operator_new(0x18);
      local_4._0_1_ = 0x4c;
      if (local_770 == (undefined4 *)0x0) {
        uVar25 = 0;
      }
      else {
        uVar25 = FUN_0052b170();
      }
      local_4 = CONCAT31(local_4._1_3_,0x4b);
      FUN_0052b550(0x31);
      pvVar26 = operator_new(0x14);
      if (pvVar26 == (void *)0x0) {
        local_784 = 0.0;
      }
      else {
        local_784 = (float)FUN_00444440(param_1,uVar25,*local_774,local_774[1]);
      }
      uVar25 = FUN_0040bfe0(local_74c,local_74c >> 0x1f,2);
      uVar25 = FUN_0040b8f0(auStack_4d4,local_714,uVar25);
      FUN_00444880(uVar25);
      FUN_00446030(&local_770);
    default:
switchD_004494bb_caseD_2:
      local_4 = local_4 & 0xffffff00;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)local_214);
      break;
    case 4.2039e-45:
      FUN_007e0e40(uVar25);
      FUN_006d0990(uVar25);
      local_4 = local_4 & 0xffffff00;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)local_214);
      break;
    case 5.60519e-45:
      FUN_007e0e40(uVar25);
      FUN_006d09b0(uVar25);
      local_4 = local_4 & 0xffffff00;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)local_214);
      break;
    case 7.00649e-45:
      FUN_007e0e40(uVar25);
      FUN_006d09f0(uVar25);
      local_4 = local_4 & 0xffffff00;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)local_214);
      break;
    case 8.40779e-45:
      FUN_007e0e40(uVar25);
      FUN_006d0a10(uVar25);
      local_4 = local_4 & 0xffffff00;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)local_214);
    }
    break;
  case 0x1c:
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty(local_22c);
    if ((!bVar4) && (iVar5 = FUN_00529d90(param_1), iVar5 == 0)) {
      FUN_0052a6d0(&local_720);
      fStack_788 = 1.0;
      local_4._0_1_ = 0x6d;
      FUN_00445990();
      FUN_00404e30();
      local_784 = (float)FUN_0095da40();
      FUN_00404e30();
      local_778 = (float)FUN_0095da40();
      FUN_0052a6d0(&local_70c);
      fStack_788 = 0.0;
      local_4._0_1_ = 0x6e;
      FUN_00445990();
      FUN_00404e30();
      pvStack_750 = (void *)FUN_0095da40();
      FUN_00404e30();
      local_73c = (float)FUN_0095da40();
      FUN_0052a730(local_214);
      local_4._0_1_ = 0x6f;
      fStack_788 = 0.0;
      FUN_00433860();
      iStack_5ec = *local_214[0];
      iStack_61c = local_214[0][1];
      if ((iStack_5ec != 0) || (local_754 = local_754 & 0xffffff00, iStack_61c != 0)) {
        local_754 = CONCAT31(local_754._1_3_,1);
      }
      FUN_0052a6d0(&local_748);
      fStack_788 = 1.0;
      local_4._0_1_ = 0x70;
      FUN_00445990();
      fStack_788 = 1.0;
      FUN_00445990();
      fStack_788 = 1.0;
      FUN_00445990();
      fVar15 = (float)_DAT_00a7b088;
      fStack_788 = (float)(int)ROUND(fVar15 * *local_748);
      FUN_00719f70((uint)fStack_788 & 0xff,(int)ROUND(local_748[1] * fVar15) & 0xff,
                   (int)ROUND(local_748[2] * fVar15) & 0xff);
      FUN_0052a6d0(&local_764);
      local_4._0_1_ = 0x71;
      fStack_788 = 1.0;
      FUN_00445990();
      fStack_788 = 1.0;
      FUN_00445990();
      fStack_788 = 1.0;
      FUN_00445990();
      fVar15 = (float)_DAT_00a7b088;
      local_780 = CONCAT22(local_780._2_2_,in_FPUControlWord);
      fStack_788 = (float)(int)ROUND(fVar15 * *local_764);
      FUN_00719f70((uint)fStack_788 & 0xff,(int)ROUND(local_764[1] * fVar15) & 0xff,
                   (int)ROUND(local_764[2] * fVar15) & 0xff);
      local_770 = (undefined4 *)FUN_0052a470();
      iVar5 = FUN_0052a470();
      fStack_788 = (float)FUN_0052a470();
      uStack_5f4 = FUN_0052a470();
      local_780 = FUN_0052a470();
      uStack_614 = FUN_0052a470();
      pbVar6 = (basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                *)FUN_0052a490();
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)local_1f0,pbVar6);
      local_4 = CONCAT31(local_4._1_3_,0x72);
      pvStack_724 = (void *)FUN_0052a470();
      iVar27 = 0;
      iVar7 = 0;
      if (iVar5 == 2) {
        iVar5 = FUN_00404e30();
        iVar27 = *(int *)(iVar5 + 0x30) - (int)local_784;
      }
      else if (iVar5 == 1) {
        iVar5 = FUN_00404e30();
        iVar27 = (*(int *)(iVar5 + 0x30) - (int)local_784) / 2;
      }
      if (fStack_788 == 2.8026e-45) {
        iVar5 = FUN_00404e30();
        iVar7 = *(int *)(iVar5 + 0x34) - (int)local_778;
      }
      else if (fStack_788 == 1.4013e-45) {
        iVar5 = FUN_00404e30();
        iVar7 = (*(int *)(iVar5 + 0x34) - (int)local_778) / 2;
      }
      iVar27 = iVar27 + (int)pvStack_750;
      iVar7 = iVar7 + (int)local_73c;
      fStack_788 = (float)CONCAT31(fStack_788._1_3_,local_780 != 0);
      FUN_00401360();
      FUN_006b22f0();
      uVar25 = FUN_0048ada0();
      pvStack_750 = operator_new(0x1f8);
      local_4._0_1_ = 0x73;
      if (pvStack_750 == (void *)0x0) {
        piVar22 = (int *)0x0;
      }
      else {
        piVar22 = (int *)FUN_008ebd90(uVar25,iVar27,iVar7,local_784,local_778,local_1f0,uStack_614,
                                      auStack_618,local_754,auStack_5e8,0,iStack_5ec,iStack_61c,
                                      uStack_5f4);
      }
      pvVar26 = pvStack_724;
      if (pvStack_724 == (void *)0x0) {
        paVar19 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_726);
        local_4._0_1_ = 0x78;
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_33c,paVar19);
        local_4._0_1_ = 0x79;
        uVar25 = FUN_00719f70(0xff,0xff,0xff,0xff);
        uVar40 = 0;
        uVar21 = 0;
        uVar20 = FUN_0052a490(0x75);
        FUN_008ecd10(uVar20,uVar21,uVar40,uVar25);
        local_4 = CONCAT31(local_4._1_3_,0x78);
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_33c);
        paVar19 = &aStack_726;
      }
      else {
        paVar19 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_72a);
        local_4._0_1_ = 0x74;
        uVar25 = stlp_std::
                 basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                 ::
                 basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                           (abStack_360,paVar19);
        local_4._0_1_ = 0x75;
        FUN_0052b110(auStack_554);
        pbVar6 = abStack_384;
        local_4._0_1_ = 0x76;
        FUN_00414170(pbVar6,pvVar26);
        uVar20 = FUN_00821bb0(pbVar6,pvVar26);
        uVar40 = 0;
        local_4._0_1_ = 0x77;
        uVar21 = FUN_00719f70(0xff,0xff,0xff,0xff);
        FUN_008ecb60(uVar20,0,0,uVar21,uVar25,uVar40);
        local_4._0_1_ = 0x76;
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_384);
        local_4._0_1_ = 0x75;
        FUN_00426620();
        local_4 = CONCAT31(local_4._1_3_,0x74);
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_360);
        paVar19 = &aStack_72a;
      }
      local_4._0_1_ = 0x72;
      stlp_std::allocator<char>::~allocator<char>(paVar19);
      if (local_780 == 1) {
        iVar5 = FUN_008e9e90();
        iVar5 = ((int)local_778 - iVar5) / 2;
        if (0 < iVar5) {
          paVar19 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_725);
          local_4._0_1_ = 0x7a;
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_47c," ",paVar19);
          local_4._0_1_ = 0x7b;
          FUN_00719f70(0xff,0xff,0xff);
          FUN_008ecd40(abStack_47c,iVar5,1,0);
          local_4._0_1_ = 0x7a;
          stlp_std::
          basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
          ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                    (abStack_47c);
          local_4._0_1_ = 0x72;
          stlp_std::allocator<char>::~allocator<char>(&aStack_725);
        }
      }
      (**(code **)(*piVar22 + 0x110))();
      FUN_008e03f0(0);
      FUN_0052a280(param_1,local_22c);
      if (local_74c != local_774[1] && -1 < local_74c - local_774[1]) {
        pvStack_724 = operator_new(0x18);
        local_4._0_1_ = 0x7c;
        if (pvStack_724 == (void *)0x0) {
          uVar25 = 0;
        }
        else {
          uVar25 = FUN_0052a260();
        }
        local_4._0_1_ = 0x72;
        FUN_00444800();
        FUN_0052ba40();
        FUN_0052b5c0(2);
        FUN_0052b5c0(9);
        FUN_0052a470();
        FUN_0052b550(0x82);
        pvVar26 = operator_new(0x14);
        if (pvVar26 == (void *)0x0) {
          pvStack_724 = (void *)0x0;
        }
        else {
          pvStack_724 = (void *)FUN_00444440(param_1,uVar25,0,0);
        }
        uVar25 = FUN_0040bfe0(local_74c,local_74c >> 0x1f,2);
        uVar25 = FUN_0040b8f0(auStack_464,local_714,uVar25);
        FUN_00444880(uVar25);
        FUN_00446030(&pvStack_724);
      }
      puVar23 = local_770;
      if (0 < (int)local_770) {
        FUN_008e0a30(0);
        FUN_0040bfe0(puVar23,(int)puVar23 >> 0x1f);
        FUN_008e0230(0x3f800000,0);
      }
      local_4._0_1_ = 0x71;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)local_1f0);
      local_4._0_1_ = 0x70;
      FUN_006adf00();
      local_4._0_1_ = 0x6f;
      FUN_006adf00();
      local_4._0_1_ = 0x6e;
      FUN_006adf00();
      local_4._0_1_ = 0x6d;
      FUN_006adf00();
      local_4 = (uint)local_4._1_3_ << 8;
      FUN_006adf00();
    }
    break;
  case 0x1d:
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty(local_22c);
    if ((!bVar4) && (iVar5 = FUN_00529d90(param_1), iVar5 != 0)) {
      iVar5 = FUN_0052a470();
      if (0 < iVar5) {
        FUN_0040bfe0(iVar5,iVar5 >> 0x1f);
        FUN_008e0230(0,0);
        local_770 = (undefined4 *)operator_new(0x18);
        local_4._0_1_ = 0x7d;
        if (local_770 == (undefined4 *)0x0) {
          uVar25 = 0;
        }
        else {
          uVar25 = FUN_0052a260();
        }
        local_4 = (uint)local_4._1_3_ << 8;
        FUN_00444800();
        FUN_0052ba40();
        FUN_0052b5c0(2);
        FUN_0052b5c0(9);
        FUN_0052b550(0x82);
        pvVar26 = operator_new(0x14);
        if (pvVar26 == (void *)0x0) {
          local_770 = (undefined4 *)0x0;
        }
        else {
          local_770 = (undefined4 *)FUN_00444440(param_1,uVar25,0,0);
        }
        uVar25 = FUN_0040bfe0(iVar5 + 100,iVar5 + 100 >> 0x1f,2);
        uVar25 = FUN_0040b8f0(auStack_484,local_714,uVar25);
        goto LAB_00449f0e;
      }
      FUN_00414ef0();
      FUN_008d9e90();
      goto LAB_0044c024;
    }
    break;
  case 0x1e:
    uVar3 = FUN_0052a590();
    local_770 = (undefined4 *)CONCAT31(local_770._1_3_,uVar3);
    FUN_00415370();
    FUN_0048ada0();
    FUN_0092fd00();
    iVar5 = local_74c;
    if (local_74c != local_774[1] && -1 < local_74c - local_774[1]) {
      local_770 = (undefined4 *)operator_new(0x18);
      local_4._0_1_ = 0x7e;
      if (local_770 == (undefined4 *)0x0) {
        uVar25 = 0;
      }
      else {
        uVar25 = FUN_0052a260();
      }
      local_4 = (uint)local_4._1_3_ << 8;
      FUN_00444800();
      FUN_0052ba40();
      FUN_0052b5c0(2);
      FUN_0052b4d0(0x83);
      pvVar26 = operator_new(0x14);
      if (pvVar26 == (void *)0x0) {
        local_770 = (undefined4 *)0x0;
      }
      else {
        local_770 = (undefined4 *)FUN_00444440(param_1,uVar25,0,0);
      }
      uVar25 = FUN_0040bfe0(iVar5,iVar5 >> 0x1f,2);
      uVar25 = FUN_0040b8f0(local_4a4,local_714,uVar25);
      goto LAB_00449f0e;
    }
    break;
  case 0x1f:
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty(local_22c);
    if ((!bVar4) && (iVar5 = FUN_00529d90(param_1), iVar5 == 0)) {
      local_770 = (undefined4 *)operator_new(0x80);
      local_4._0_1_ = 0x7f;
      if (local_770 == (undefined4 *)0x0) {
        piVar22 = (int *)0x0;
      }
      else {
        piVar22 = (int *)FUN_006a3c30();
      }
      local_4._0_1_ = 0;
      uStack_5dc = FUN_0052a470();
      uStack_5e0 = 0x65;
      FUN_006a4df0();
      local_4._0_1_ = 0x80;
      uVar3 = FUN_006a54d0();
      local_780 = CONCAT31(local_780._1_3_,uVar3);
      local_4 = (uint)local_4._1_3_ << 8;
      FUN_00444be0();
      if ((char)local_780 == '\0') {
        if (piVar22 != (int *)0x0) {
          (**(code **)*piVar22)();
        }
      }
      else {
        (**(code **)(*piVar22 + 0x10))();
        iVar5 = FUN_0040ed30();
        if (iVar5 != 0) {
          iVar7 = *piVar22;
          FUN_0040bfe0(iVar5,iVar5 >> 0x1f);
          (**(code **)(iVar7 + 0x1c))();
        }
        (**(code **)(*piVar22 + 4))();
        puVar23 = (undefined4 *)operator_new(0x30);
        local_4._0_1_ = 0x81;
        local_770 = puVar23;
        if (puVar23 == (undefined4 *)0x0) {
          puVar23 = (undefined4 *)0x0;
        }
        else {
          _vector_constructor_iterator_(puVar23,0xc,4,FUN_004926e0);
        }
        local_4._0_1_ = 0;
        puVar24 = (undefined4 *)operator_new(0x20);
        local_4._0_1_ = 0x82;
        if (puVar24 == (undefined4 *)0x0) {
          puVar28 = (undefined4 *)0x0;
          local_770 = puVar24;
        }
        else {
          local_770 = puVar24;
          _vector_constructor_iterator_(puVar24,8,4,FUN_004926e0);
          puVar28 = puVar24;
        }
        local_4._0_1_ = 0;
        puVar24 = (undefined4 *)FUN_00411f80(0,0);
        *puVar23 = *puVar24;
        puVar23[1] = puVar24[1];
        puVar23[2] = puVar24[2];
        puVar24 = (undefined4 *)FUN_00411f80(0x3f800000,0);
        puVar23[3] = *puVar24;
        puVar23[4] = puVar24[1];
        puVar23[5] = puVar24[2];
        puVar24 = (undefined4 *)FUN_00411f80(0x3f800000,0x3f800000);
        puVar23[6] = *puVar24;
        puVar23[7] = puVar24[1];
        puVar23[8] = puVar24[2];
        puVar24 = (undefined4 *)FUN_00411f80(0,0x3f800000);
        puVar23[9] = *puVar24;
        puVar23[10] = puVar24[1];
        puVar23[0xb] = puVar24[2];
        *puVar28 = 0;
        puVar28[1] = 0x3f800000;
        local_770 = (undefined4 *)0x0;
        puVar28[2] = 0x3f800000;
        local_76c = 0;
        puVar28[3] = 0x3f800000;
        puVar28[4] = 0x3f800000;
        puVar28[5] = 0;
        puVar28[6] = 0;
        puVar28[7] = 0;
        local_770 = (undefined4 *)operator_new(0x28);
        local_4._0_1_ = 0x83;
        if (local_770 == (undefined4 *)0x0) {
          uVar25 = 0;
        }
        else {
          uVar25 = FUN_007be510(4,puVar23,puVar28);
        }
        local_4._0_1_ = 0;
        operator_delete__(puVar23);
        operator_delete__(puVar28);
        local_770 = (undefined4 *)operator_new(0x48);
        local_4._0_1_ = 0x84;
        if (local_770 != (undefined4 *)0x0) {
          FUN_007b8230();
        }
        FUN_004448d0();
        local_4._0_1_ = 0x85;
        FUN_007ce1e0();
        FUN_00746550();
        fVar15 = local_784;
        FUN_004449d0();
        FUN_00444a80();
        *(undefined4 *)((int)fVar15 + 0x20) = 0;
        FUN_00444b60();
        local_770 = (undefined4 *)operator_new(0x28);
        local_4._0_1_ = 0x86;
        if (local_770 == (undefined4 *)0x0) {
          iVar5 = 0;
        }
        else {
          iVar5 = FUN_00444ba0();
        }
        *(ushort *)(iVar5 + 0x20) = *(ushort *)(iVar5 + 0x20) & 0xfffc;
        local_4._0_1_ = 0x85;
        FUN_00444b60();
        FUN_00401360();
        FUN_006b22f0();
        FUN_0048add0();
        FUN_00445700();
        DAT_00ba187c = DAT_00ba187c + 1;
        puVar23 = (undefined4 *)FUN_00446b40();
        *puVar23 = piVar22;
        puVar23[1] = uVar25;
        FUN_0052a280(param_1,local_22c);
        iVar5 = local_74c;
        if (local_74c != local_774[1] && -1 < local_74c - local_774[1]) {
          local_770 = (undefined4 *)operator_new(0x18);
          local_4._0_1_ = 0x87;
          if (local_770 == (undefined4 *)0x0) {
            uVar25 = 0;
          }
          else {
            uVar25 = FUN_0052a260();
          }
          local_4._0_1_ = 0x85;
          FUN_00444800();
          FUN_0052ba40();
          FUN_0052b5c0(2);
          FUN_0052b5c0(9);
          pvVar26 = operator_new(0x14);
          if (pvVar26 == (void *)0x0) {
            local_770 = (undefined4 *)0x0;
          }
          else {
            local_770 = (undefined4 *)FUN_00444440(param_1,uVar25,0,0);
          }
          uVar25 = FUN_0040bfe0(iVar5,iVar5 >> 0x1f,2);
          uVar25 = FUN_0040b8f0(auStack_52c,local_714,uVar25);
          FUN_00444880(uVar25);
          FUN_00446030(&local_770);
        }
        local_4 = (uint)local_4._1_3_ << 8;
        FUN_0079fc70();
      }
    }
    break;
  case 0x20:
    bVar4 = stlp_std::
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
            empty(local_22c);
    if ((!bVar4) &&
       (local_770 = (undefined4 *)FUN_00529d90(param_1), local_770 != (undefined4 *)0x0)) {
      FUN_00445220(&pvStack_724);
      if (pvStack_724 != (void *)(local_77c + 0x34)) {
        if (*(undefined4 **)((int)pvStack_724 + 0x14) != (undefined4 *)0x0) {
          (**(code **)**(undefined4 **)((int)pvStack_724 + 0x14))();
        }
        FUN_00401360();
        FUN_006b22f0();
        FUN_0048add0();
        FUN_007bd830();
        local_770 = (undefined4 *)&stack0xfffff85c;
        FUN_004539e0();
      }
      goto LAB_0044c024;
    }
  }
  local_4 = 0xffffffff;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(local_22c);
LAB_0044c041:
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

