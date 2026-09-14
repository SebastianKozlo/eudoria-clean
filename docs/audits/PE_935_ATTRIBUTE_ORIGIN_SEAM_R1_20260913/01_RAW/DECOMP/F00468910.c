
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall
FUN_00468910(int param_1_00,int *****param_1,int ****param_2,undefined4 param_3,undefined4 param_4,
            undefined4 param_5,undefined4 param_6,undefined4 param_7,int *****param_8)

{
  char cVar1;
  byte bVar2;
  undefined4 *puVar3;
  int *****pppppiVar4;
  int *****pppppiVar5;
  int *piVar6;
  int iVar7;
  int iVar8;
  undefined4 uVar9;
  int ****ppppiVar10;
  undefined4 *puVar11;
  bool bVar12;
  int ***apppiStack_190 [2];
  int ****ppppiStack_188;
  int ****ppppiStack_184;
  int ****ppppiStack_180;
  int ****ppppiStack_17c;
  int ****local_178;
  int ****local_174;
  uint uStack_170;
  undefined auStack_15c [3];
  byte local_159;
  int ***local_154;
  undefined4 local_150;
  undefined4 local_14c;
  undefined4 local_148;
  undefined4 local_144;
  undefined4 local_140;
  int ****local_13c [2];
  int ****local_134;
  int ****local_130;
  int ****local_12c;
  undefined4 local_128;
  int ****local_124;
  undefined4 local_120 [4];
  undefined4 local_110;
  undefined4 local_10c;
  undefined4 local_108;
  uint local_104;
  undefined local_100 [40];
  undefined local_d8 [84];
  int ***local_84 [29];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  puStack_8 = &LAB_009a1911;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_15c;
  uStack_170 = DAT_00b9d8d0 ^ (uint)&stack0xfffffe94;
  ExceptionList = &local_c;
  local_4 = 0;
  local_174 = (int ****)0x46895f;
  FUN_004ad820();
  pppppiVar4 = param_1;
  local_154 = (int ***)param_2;
  local_150 = param_3;
  local_14c = param_4;
  local_124 = (int ****)param_1;
  local_148 = param_5;
  local_144 = param_6;
  local_140 = param_7;
  local_4._0_1_ = 2;
  if (((uint)param_8 >> 7 & 1) == 0) {
    if (((uint)param_8 >> 8 & 1) != 0) goto LAB_00468a1e;
  }
  else {
    local_174 = (int ****)local_100;
    local_178 = (int ****)0x4689cf;
    FUN_00414af0();
    local_178 = (int ****)0x4689d6;
    puVar3 = (undefined4 *)FUN_004604d0();
    local_154 = (int ***)*puVar3;
    local_150 = puVar3[1];
    local_14c = puVar3[2];
    local_148 = puVar3[3];
    local_144 = puVar3[4];
    local_140 = puVar3[5];
    local_174 = (int ****)0x468a08;
    FUN_008e0110();
    local_174 = (int ****)0x468a11;
    cVar1 = FUN_00719dc0();
    if (cVar1 == '\0') {
LAB_00468a1e:
      local_174 = (int ****)pppppiVar4;
      local_178 = (int ****)0x468a26;
      cVar1 = FUN_004648b0();
      if (cVar1 != '\0') {
        local_178 = (int ****)local_100;
        local_174 = (int ****)_DAT_00a7b420;
        ppppiStack_17c = (int ****)0x468a3e;
        FUN_00414af0();
        ppppiStack_17c = (int ****)0x468a45;
        puVar3 = (undefined4 *)FUN_00460900();
        local_154 = (int ***)*puVar3;
        local_150 = puVar3[1];
        local_14c = puVar3[2];
        local_148 = puVar3[3];
        local_144 = puVar3[4];
        local_140 = puVar3[5];
        local_174 = (int ****)0x468a77;
        FUN_008e0110();
      }
    }
  }
  local_174 = (int ****)0x468a83;
  FUN_00511530();
  local_174 = &local_154;
  local_4 = CONCAT31(local_4._1_3_,3);
  local_178 = (int ****)0x468a9c;
  local_159 = FUN_00511750();
  if (pppppiVar4 == (int *****)0xa) {
    local_174 = local_84;
    if (local_159 != 0) {
      local_178 = &local_154;
      ppppiStack_17c = (int ****)0x468ac1;
      pppppiVar4 = (int *****)FUN_00464ab0();
      local_124 = (int ****)pppppiVar4;
      goto LAB_00468ac7;
    }
LAB_00468cbd:
    local_4._0_1_ = 2;
    local_174 = (int ****)0x468cca;
    FUN_00460430();
    local_4._0_1_ = 1;
    local_174 = (int ****)0x468cdb;
    FUN_008e0110();
    local_4 = (uint)local_4._1_3_ << 8;
    local_174 = (int ****)0x468ceb;
    thunk_FUN_00703bc0();
    local_4 = 0xffffffff;
    local_174 = (int ****)0x468d02;
    FUN_008e0110();
    goto LAB_00468d04;
  }
LAB_00468ac7:
  if (pppppiVar4 == (int *****)0x21c) {
    local_174 = (int ****)0x468ad4;
    FUN_004310f0();
    local_174 = (int ****)0x468adb;
    local_174 = (int ****)FUN_004f4d90();
    local_178 = (int ****)0x468ae3;
    pppppiVar4 = (int *****)FUN_00464000();
    local_124 = (int ****)pppppiVar4;
  }
  local_178 = (int ****)0x468aef;
  local_174 = (int ****)pppppiVar4;
  FUN_00423b90();
  local_178 = (int ****)0x468af6;
  pppppiVar5 = (int *****)FUN_0071a670();
  local_174 = (int ****)0x468b03;
  local_12c = (int ****)pppppiVar5;
  cVar1 = FUN_006c4200();
  if (cVar1 == '\0') goto LAB_00468cbd;
  local_13c[0] = *pppppiVar5;
  if (*(char *)(param_1_00 + 0x2c) != '\0') {
    local_174 = (int ****)local_13c;
    local_178 = (int ****)&local_134;
    ppppiStack_17c = (int ****)0x468b28;
    FUN_004d1430();
    if ((int *****)local_134 == (int *****)(param_1_00 + 0x30)) goto LAB_00468cbd;
  }
  if ((((uint)pppppiVar5[6] & 0x40000000) != 0) && (((uint)param_8 >> 6 & 1) == 0)) {
    local_174 = (int ****)0xd19;
    local_178 = (int ****)param_8;
    ppppiStack_17c = *pppppiVar5;
LAB_00468caf:
    ppppiStack_180 = (int ****)0x468cb6;
    param_8 = (int *****)local_178;
    FUN_00467c60();
    goto LAB_00468cbd;
  }
  local_13c[0] = (int ****)(param_1_00 + 0x48);
  local_174 = (int ****)0x468b69;
  cVar1 = FUN_009733d0();
  if ((cVar1 != '\0') && (((uint)pppppiVar5[6] & 0x8000000) == 0)) {
    local_174 = (int ****)0x468b7f;
    FUN_00973390();
    local_174 = (int ****)0x468b88;
    FUN_009734d0();
  }
  local_174 = (int ****)0x468b8d;
  FUN_004310f0();
  local_174 = (int ****)0x468b94;
  cVar1 = FUN_004f4e10();
  if ((cVar1 != '\0') && (((uint)pppppiVar5[6] & 0x800000) == 0x800000)) {
    if (((uint)pppppiVar5[6] & 0x40000) != 0) {
      local_174 = (int ****)0x12;
      local_178 = (int ****)0x468bbe;
      FUN_00415170();
      local_178 = (int ****)0x468bc5;
      cVar1 = FUN_006fff20();
      if (cVar1 == '\0') goto LAB_00468bde;
    }
    local_174 = (int ****)&param_1;
    local_178 = (int ****)0x468bd9;
    FUN_00464850();
    goto LAB_00468cbd;
  }
LAB_00468bde:
  if (((uint)pppppiVar5[6] & 0x8000000) == 0) {
    local_174 = (int ****)0x468bf0;
    local_174 = (int ****)FUN_004634a0();
    local_178 = (int ****)0x468bf9;
    FUN_00464850();
    local_174 = (int ****)0x468c02;
    FUN_008e0110();
  }
  local_174 = (int ****)0x468c0b;
  cVar1 = FUN_00719dc0();
  if (((cVar1 != '\0') && (local_159 == 0)) && (((uint)pppppiVar5[6] & 0x8000) == 0))
  goto LAB_00468cbd;
  local_174 = (int ****)&local_128;
  local_178 = local_84;
  ppppiStack_17c = &local_154;
  local_128 = 0x670;
  ppppiStack_184 = (int ****)0x468c44;
  ppppiStack_180 = (int ****)pppppiVar5;
  local_159 = FUN_00464e30();
  if (local_159 == 0) {
    if (((uint)pppppiVar5[6] & 0x4000) != 0) {
      local_174 = (int ****)local_100;
      local_178 = (int ****)0x468c63;
      local_174 = (int ****)FUN_004da390();
      local_178 = (int ****)0x468c6d;
      FUN_004602f0();
      local_174 = (int ****)0x468c76;
      FUN_008e0110();
      local_159 = 1;
      goto LAB_00468c7b;
    }
LAB_00468ca1:
    local_174 = (int ****)local_128;
    ppppiStack_17c = (int ****)pppppiVar4;
    local_178 = (int ****)param_8;
    goto LAB_00468caf;
  }
LAB_00468c7b:
  local_174 = (int ****)&local_128;
  local_178 = local_84;
  ppppiStack_17c = &local_154;
  ppppiStack_184 = (int ****)0x468c95;
  ppppiStack_180 = (int ****)pppppiVar5;
  bVar2 = FUN_00466a00();
  if ((local_159 & bVar2) == 0) goto LAB_00468ca1;
  if ((((uint)param_8 >> 4 & 1) == 0) && (pppppiVar4 == (int *****)0x13b)) {
    *(undefined4 *)(param_1_00 + 0x28) = 0;
    local_174 = (int ****)0x468d50;
    piVar6 = (int *)FUN_004926e0();
    if (*piVar6 == 0x4e46) {
      local_174 = (int ****)0x1;
      local_178 = (int ****)&local_134;
      local_134 = (int ****)0x0;
      ppppiStack_17c = (int ****)0x468d6c;
      ppppiStack_17c = (int ****)FUN_004926e0();
      ppppiStack_180 = (int ****)0x468d72;
      FUN_00414570();
      ppppiStack_180 = (int ****)0x468d79;
      FUN_00437d20();
      if ((int *****)local_134 != (int *****)0x0) {
        *(int *****)(param_1_00 + 0x28) = local_134;
      }
    }
  }
  local_174 = (int ****)0x468d8d;
  iVar7 = FUN_0048ada0();
  if (iVar7 != 0) {
    local_174 = (int ****)0x468d9e;
    iVar7 = FUN_00726490();
    local_174 = (int ****)0x468da9;
    iVar8 = FUN_0048ada0();
    pppppiVar5 = (int *****)local_12c;
    if (((iVar8 == iVar7) || (((uint)param_8 >> 4 & 1) != 0)) ||
       (((uint)local_12c[6] & 0x108000) != 0)) goto LAB_0046902c;
    local_174 = (int ****)&local_130;
    local_178 = (int ****)&local_134;
    ppppiStack_17c = local_84;
    ppppiStack_180 = (int ****)param_8;
    ppppiStack_184 = &local_154;
    ppppiStack_188 = local_12c;
    apppiStack_190[1] = (int ***)0x468df7;
    cVar1 = FUN_00464bb0();
    if (cVar1 == '\0') goto LAB_00468cbd;
    if (((uint)param_8 & 1) == 0) {
LAB_00468fc7:
      local_178 = &local_154;
      local_174 = local_130;
      ppppiStack_17c = (int ****)0x468fdb;
      cVar1 = FUN_00465300();
      if ((((uint)((int ****)pppppiVar5)[6] & 1) == 0) && (cVar1 == '\0')) {
        local_174 = (int ****)0x6d1;
        ppppiStack_17c = (int ****)pppppiVar4;
        local_178 = (int ****)param_8;
        goto LAB_00468caf;
      }
      if ((((uint)((int ****)pppppiVar5)[6] & 0x200000) == 0) || (cVar1 == '\0')) goto LAB_0046902c;
      local_178 = local_130;
      local_174 = local_130;
    }
    else {
      local_174 = (int ****)0x468e12;
      FUN_004143f0();
      local_174 = (int ****)0x468e19;
      cVar1 = FUN_0042c1e0();
      if (cVar1 == '\0') goto LAB_00468fc7;
      local_178 = &local_154;
      local_174 = local_134;
      ppppiStack_17c = (int ****)0x468e35;
      cVar1 = FUN_00465300();
      if (cVar1 != '\0') {
        local_174 = (int ****)0x468e40;
        iVar7 = FUN_00465580();
        if ((iVar7 != 0x6ac) && (((uint)((int ****)pppppiVar5)[6] & 0x10000) != 0x10000))
        goto LAB_0046902c;
      }
      local_174 = (int ****)0x6ac;
      local_178 = (int ****)0x468e6d;
      FUN_00467a00();
      if ((((uint)((int ****)pppppiVar5)[6] & 0x40000) == 0) && (pppppiVar4 != (int *****)0x140)) {
        local_174 = (int ****)0x468e8f;
        puVar3 = (undefined4 *)FUN_0075ff20();
        local_120[1] = *puVar3;
        local_120[2] = puVar3[1];
        local_120[3] = puVar3[2];
        local_120[0] = 0x23a;
        local_110 = puVar3[3];
        local_10c = puVar3[4];
        local_108 = puVar3[5];
        local_104 = 4;
        puVar3 = local_120;
        ppppiVar10 = apppiStack_190;
        for (iVar7 = 8; iVar7 != 0; iVar7 = iVar7 + -1) {
          *ppppiVar10 = (int ***)*puVar3;
          puVar3 = puVar3 + 1;
          ppppiVar10 = ppppiVar10 + 1;
        }
        local_4._0_1_ = 5;
        FUN_00468910();
        local_4._0_1_ = 4;
        local_174 = (int ****)0x468ef8;
        FUN_008e0110();
        local_4 = CONCAT31(local_4._1_3_,3);
        local_174 = (int ****)0x468f09;
        FUN_008e0110();
        pppppiVar4 = (int *****)local_124;
        pppppiVar5 = (int *****)local_12c;
      }
      if (((uint)pppppiVar5[6] & 0x200000) != 0) {
        local_134 = local_130;
        local_178 = &local_154;
        local_174 = local_130;
        ppppiStack_17c = (int ****)0x468f32;
        cVar1 = FUN_00465300();
        if (cVar1 == '\0') {
          local_174 = (int ****)0x468f3f;
          cVar1 = FUN_004da500();
          if (cVar1 == '\0') {
            local_174 = (int ****)0x6d1;
            ppppiStack_17c = (int ****)pppppiVar4;
            local_178 = (int ****)param_8;
            goto LAB_00468caf;
          }
        }
      }
      local_178 = local_134;
      local_174 = local_130;
    }
    ppppiStack_180 = &local_154;
    ppppiStack_188 = (int ****)0x468f74;
    ppppiStack_184 = (int ****)pppppiVar5;
    ppppiStack_17c = (int ****)param_8;
    FUN_00466ce0();
    goto LAB_00468f74;
  }
LAB_0046902c:
  if (pppppiVar4 != (int *****)0x140) {
    if (((uint)pppppiVar5[6] & 0x40000) == 0) {
      if (((uint)pppppiVar5[6] & 0x80000000) == 0x80000000) {
        local_174 = (int ****)0x46918b;
        cVar1 = FUN_004da260();
        if (cVar1 != '\0') {
          local_174 = (int ****)0x469198;
          uVar9 = FUN_0075ff20();
          local_13c[0] = apppiStack_190;
          local_4._0_1_ = 10;
          FUN_004634c0(0x23a,uVar9,0);
          cVar1 = FUN_00468910();
          local_159 = cVar1 == '\0';
          local_4 = CONCAT31(local_4._1_3_,3);
          local_174 = (int ****)0x4691d4;
          FUN_008e0110();
          if (local_159 != 0) goto LAB_00468cbd;
        }
      }
    }
    else {
      local_174 = (int ****)0x469050;
      cVar1 = FUN_004da260();
      if (cVar1 == '\0') {
        local_174 = (int ****)0x469061;
        uVar9 = FUN_0075ff20();
        local_134 = apppiStack_190;
        local_4._0_1_ = 6;
        FUN_004634c0(0x230,uVar9,0);
        cVar1 = FUN_00468910();
        local_159 = cVar1 == '\0';
        local_4 = CONCAT31(local_4._1_3_,3);
        local_174 = (int ****)0x46909d;
        FUN_008e0110();
        if (local_159 != 0) goto LAB_00468cbd;
        puVar3 = &param_1;
        puVar11 = local_120;
        for (iVar7 = 8; iVar7 != 0; iVar7 = iVar7 + -1) {
          *puVar11 = *puVar3;
          puVar3 = puVar3 + 1;
          puVar11 = puVar11 + 1;
        }
        local_104 = (uint)param_8 | 0x200;
        puVar3 = local_120;
        ppppiVar10 = apppiStack_190;
        for (iVar7 = 8; iVar7 != 0; iVar7 = iVar7 + -1) {
          *ppppiVar10 = (int ***)*puVar3;
          puVar3 = puVar3 + 1;
          ppppiVar10 = ppppiVar10 + 1;
        }
        local_4._0_1_ = 7;
        local_174 = (int ****)FUN_00466530(local_d8,FUN_00468910,param_1_00);
        local_4._0_1_ = 8;
        local_178 = (int ****)0x46910c;
        local_174 = (int ****)FUN_004688e0();
        local_4._0_1_ = 9;
        local_178 = (int ****)0x469120;
        FUN_004669e0();
        local_4._0_1_ = 8;
        local_174 = (int ****)0x469131;
        FUN_00662d00();
        local_4._0_1_ = 7;
        local_174 = (int ****)0x469145;
        FUN_008e0110();
        local_174 = (int ****)0x2;
        local_178 = (int ****)0x0;
        ppppiStack_17c = (int ****)0x12c;
        ppppiStack_180 = (int ****)0x469156;
        local_174 = (int ****)FUN_0040bfe0();
        local_178 = (int ****)0x46915e;
        FUN_00973430();
        local_4 = CONCAT31(local_4._1_3_,3);
        local_174 = (int ****)0x46916f;
        FUN_008e0110();
        goto LAB_00468f74;
      }
    }
  }
  if (pppppiVar5[1] == (int ****)0x5) {
    local_178 = (int ****)0x4691f8;
    local_174 = (int ****)pppppiVar5;
    local_159 = FUN_00465430();
    goto LAB_004691fc;
  }
  if (pppppiVar5[2] == (int ****)0x13) {
    local_174 = &local_154;
    ppppiStack_17c = (int ****)0x469264;
    local_178 = (int ****)pppppiVar5;
    local_159 = FUN_004654e0();
    goto LAB_004691fc;
  }
  if (pppppiVar4 < (int *****)0x119) {
    if (pppppiVar4 == (int *****)0x118) {
      local_174 = (int ****)0x4693d0;
      iVar7 = FUN_004926e0();
      local_178 = *(int *****)(iVar7 + 4);
      local_174 = (int ****)0x2;
      ppppiStack_17c = (int ****)0x4693dd;
      local_159 = FUN_00468090();
    }
    else {
      switch(pppppiVar4) {
      case (int *****)0x15:
        local_174 = &local_154;
        local_178 = (int ****)0x46929e;
        local_159 = FUN_0058db50();
        break;
      case (int *****)0x16:
switchD_0046928d_caseD_16:
        local_174 = &local_154;
        local_178 = (int ****)0x46941e;
        local_159 = FUN_0058db50();
        break;
      case (int *****)0x17:
        local_174 = &local_154;
        local_178 = (int ****)0x4692b0;
        local_159 = FUN_0058db50();
        break;
      default:
        goto switchD_0046928d_caseD_18;
      case (int *****)0x32:
        local_174 = (int ****)0x1;
        local_178 = (int ****)0x4693bb;
        FUN_004149f0();
        local_178 = (int ****)0x4693c2;
        local_159 = FUN_0045b300();
        break;
      case (int *****)0xc8:
        local_174 = (int ****)0x4692c1;
        local_174 = (int ****)FUN_0048ada0();
        local_178 = (int ****)0x4692c7;
        FUN_004145f0();
        local_178 = (int ****)0x4692ce;
        local_159 = FUN_00439580();
        break;
      case (int *****)0xd2:
        local_174 = (int ****)0x469312;
        local_174 = (int ****)FUN_0048ada0();
        local_178 = (int ****)0x469318;
        FUN_0041b3a0();
        local_178 = (int ****)0x46931f;
        local_159 = FUN_004b6070();
        break;
      case (int *****)0xdc:
        local_174 = (int ****)0x4692dc;
        local_174 = (int ****)FUN_0048ada0();
        local_178 = (int ****)0x4692e2;
        FUN_004145f0();
        local_178 = (int ****)0x4692e9;
        local_159 = FUN_00438310();
        break;
      case (int *****)0xe6:
        local_174 = (int ****)0x4692f7;
        local_174 = (int ****)FUN_0048ada0();
        local_178 = (int ****)0x4692fd;
        FUN_004145f0();
        local_178 = (int ****)0x469304;
        local_159 = FUN_00439f00();
        break;
      case (int *****)0xf0:
        local_174 = (int ****)0x46932d;
        iVar7 = FUN_004926e0();
        local_174 = *(int *****)(iVar7 + 4);
        local_178 = (int ****)0x469336;
        FUN_00414370();
        local_178 = (int ****)0x46933d;
        local_159 = FUN_00428aa0();
        break;
      case (int *****)0xfa:
        local_174 = (int ****)0x46934b;
        iVar7 = FUN_004926e0();
        local_178 = *(int *****)(iVar7 + 4);
        local_174 = (int ****)0x4;
        ppppiStack_17c = (int ****)0x469358;
        local_159 = FUN_00468090();
        break;
      case (int *****)0x104:
        local_174 = (int ****)0x469366;
        iVar7 = FUN_004926e0();
        local_178 = *(int *****)(iVar7 + 4);
        local_174 = (int ****)0x5;
        ppppiStack_17c = (int ****)0x469373;
        local_159 = FUN_00468090();
        break;
      case (int *****)0x10e:
        local_174 = (int ****)0x469381;
        iVar7 = FUN_004926e0();
        local_174 = *(int *****)(iVar7 + 4);
        local_178 = (int ****)0x46938a;
        FUN_00464270();
        local_178 = (int ****)0x469391;
        local_159 = FUN_005687c0();
        break;
      case (int *****)0x10f:
        local_174 = (int ****)0x46939f;
        iVar7 = FUN_004926e0();
        local_174 = *(int *****)(iVar7 + 4);
        local_178 = (int ****)0x4693a8;
        FUN_00464270();
        local_178 = (int ****)0x4693af;
        local_159 = FUN_00568a10();
      }
    }
    goto LAB_004691fc;
  }
  if (pppppiVar4 < (int *****)0x227) {
    if (pppppiVar4 == (int *****)0x226) {
      local_174 = (int ****)0x4696b8;
      FUN_004310f0();
      local_174 = (int ****)0x4696bf;
      local_159 = FUN_004fbef0();
    }
    else {
      switch(pppppiVar4) {
      case (int *****)0x122:
        local_174 = (int ****)0x46949e;
        iVar7 = FUN_004926e0();
        local_178 = *(int *****)(iVar7 + 4);
        local_174 = (int ****)0x3;
        ppppiStack_17c = (int ****)0x4694ab;
        local_159 = FUN_00468090();
        break;
      default:
        goto switchD_0046928d_caseD_18;
      case (int *****)0x12c:
        local_174 = (int ****)_DAT_00a7b430;
        local_178 = (int ****)0x4694c3;
        local_178 = (int ****)FUN_0048ada0();
        ppppiStack_17c = (int ****)0x4694c9;
        FUN_004149f0();
        ppppiStack_17c = (int ****)0x4694d0;
        local_159 = FUN_0045aa80();
        break;
      case (int *****)0x136:
        local_174 = (int ****)0x4696ae;
        local_159 = FUN_00465d20();
        break;
      case (int *****)0x13b:
        local_174 = &local_154;
        local_178 = (int ****)0x469432;
        local_159 = FUN_00465520();
        break;
      case (int *****)0x13c:
        local_174 = (int ****)0x469440;
        local_174 = (int ****)FUN_004926e0();
        local_178 = (int ****)0x469446;
        local_174 = (int ****)FUN_0049eb40();
        local_178 = (int ****)0x469456;
        FUN_0049dcc0();
        local_4._0_1_ = 0xb;
        local_174 = (int ****)0x469465;
        local_174 = (int ****)FUN_008df6b0();
        local_178 = (int ****)0x46946f;
        local_178 = (int ****)FUN_00746560();
        ppppiStack_17c = (int ****)0x469475;
        FUN_00464370();
        ppppiStack_17c = (int ****)0x46947c;
        FUN_0056ea60();
        local_4 = CONCAT31(local_4._1_3_,3);
        local_174 = (int ****)0x469490;
        FUN_008df670();
        goto LAB_00468f74;
      case (int *****)0x140:
        local_174 = (int ****)0x4694de;
        local_174 = (int ****)FUN_0048ada0();
        local_178 = (int ****)0x4694e4;
        local_159 = FUN_0058d800();
        break;
      case (int *****)0x14a:
switchD_0046940d_caseD_14a:
        local_174 = (int ****)0x4694f5;
        local_174 = (int ****)FUN_0048ada0();
        ppppiStack_17c = (int ****)0x4694fc;
        local_178 = (int ****)pppppiVar4;
        FUN_004642f0();
        ppppiStack_17c = (int ****)0x469503;
        local_159 = FUN_0056ad60();
        break;
      case (int *****)0x154:
        local_174 = &local_154;
        local_178 = (int ****)0x469524;
        local_159 = FUN_00580020();
        break;
      case (int *****)0x15e:
        local_174 = &local_154;
        local_178 = (int ****)0x469536;
        local_159 = FUN_0057e9e0();
        break;
      case (int *****)0x168:
        local_174 = &local_154;
        local_178 = (int ****)0x469512;
        local_159 = FUN_0057f820();
        break;
      case (int *****)0x172:
        local_174 = (int ****)0x0;
        local_178 = (int ****)0x469548;
        local_178 = (int ****)FUN_006b22d0();
        ppppiStack_17c = (int ****)0x46954e;
        local_159 = FUN_00580450();
        break;
      case (int *****)0x1f4:
        local_174 = (int ****)0x6a4;
        local_178 = (int ****)0x469562;
        local_159 = FUN_00467a00();
        break;
      case (int *****)0x1fe:
        local_174 = (int ****)0x6a8;
        local_178 = (int ****)0x469573;
        local_159 = FUN_00467a00();
        break;
      case (int *****)0x208:
        local_174 = (int ****)0x6ac;
        local_178 = (int ****)0x469584;
        local_159 = FUN_00467a00();
        break;
      case (int *****)0x209:
        local_174 = (int ****)0x1;
        local_178 = (int ****)0x469590;
        FUN_004149f0();
        local_178 = (int ****)0x469597;
        local_159 = FUN_0045b210();
        break;
      case (int *****)0x20a:
        local_13c[0] = (int ****)
                       (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
        local_174 = local_13c[0];
        local_178 = (int ****)0x1;
        ppppiStack_17c = (int ****)0x4695b1;
        FUN_004149f0();
        ppppiStack_17c = (int ****)0x4695b8;
        local_159 = FUN_00459c40();
        break;
      case (int *****)0x20b:
        local_13c[0] = (int ****)
                       (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
        local_174 = local_13c[0];
        local_178 = (int ****)0x2;
        ppppiStack_17c = (int ****)0x4695d2;
        FUN_004149f0();
        ppppiStack_17c = (int ****)0x4695d9;
        local_159 = FUN_00459c40();
        break;
      case (int *****)0x20c:
        local_13c[0] = (int ****)
                       (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
        local_174 = local_13c[0];
        local_178 = (int ****)0x4;
        ppppiStack_17c = (int ****)0x4695f3;
        FUN_004149f0();
        ppppiStack_17c = (int ****)0x4695fa;
        local_159 = FUN_00459c40();
        break;
      case (int *****)0x20d:
        local_13c[0] = (int ****)
                       (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
        local_174 = local_13c[0];
        local_178 = (int ****)0x20;
        ppppiStack_17c = (int ****)0x469614;
        FUN_004149f0();
        ppppiStack_17c = (int ****)0x46961b;
        local_159 = FUN_00459c40();
        break;
      case (int *****)0x20e:
        local_13c[0] = (int ****)
                       (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
        local_174 = local_13c[0];
        local_178 = (int ****)0x8;
        ppppiStack_17c = (int ****)0x469635;
        FUN_004149f0();
        ppppiStack_17c = (int ****)0x46963c;
        local_159 = FUN_00459c40();
        break;
      case (int *****)0x20f:
        local_13c[0] = (int ****)
                       (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
        local_174 = local_13c[0];
        local_178 = (int ****)&DAT_00000010;
        ppppiStack_17c = (int ****)0x469656;
        FUN_004149f0();
        ppppiStack_17c = (int ****)0x46965d;
        local_159 = FUN_00459c40();
        break;
      case (int *****)0x210:
        local_13c[0] = (int ****)
                       (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
        local_174 = local_13c[0];
        local_178 = (int ****)0x40;
        ppppiStack_17c = (int ****)0x469677;
        FUN_004149f0();
        ppppiStack_17c = (int ****)0x46967e;
        local_159 = FUN_00459c40();
        break;
      case (int *****)0x211:
        local_13c[0] = (int ****)
                       (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
        local_174 = local_13c[0];
        local_178 = (int ****)0x80;
        ppppiStack_17c = (int ****)0x46969b;
        FUN_004149f0();
        ppppiStack_17c = (int ****)0x4696a2;
        local_159 = FUN_00459c40();
        break;
      case (int *****)0x21c:
        goto switchD_0046928d_caseD_16;
      }
    }
    goto LAB_004691fc;
  }
  if (pppppiVar4 < (int *****)0x367) {
    if (pppppiVar4 == (int *****)0x366) {
      local_174 = (int ****)0x1;
      local_178 = (int ****)0x46980c;
      FUN_00414c70();
      local_178 = (int ****)0x469813;
      local_159 = FUN_00472bd0();
      goto LAB_004691fc;
    }
    switch(pppppiVar4) {
    case (int *****)0x230:
      local_174 = (int ****)0x1;
      local_178 = (int ****)0x4696fa;
      FUN_004641f0();
      local_178 = (int ****)0x469701;
      local_159 = FUN_00565cb0();
      goto LAB_004691fc;
    default:
      goto switchD_0046928d_caseD_18;
    case (int *****)0x23a:
      local_174 = (int ****)0x0;
      local_178 = (int ****)0x46970c;
      FUN_004641f0();
      local_178 = (int ****)0x469713;
      local_159 = FUN_00565cb0();
      goto LAB_004691fc;
    case (int *****)0x240:
      local_174 = (int ****)0x46971d;
      FUN_00414af0();
      local_174 = (int ****)0x469724;
      local_159 = FUN_004620b0();
      goto LAB_004691fc;
    case (int *****)0x242:
      local_13c[0] = (int ****)
                     (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
      local_174 = local_13c[0];
      local_178 = (int ****)0x46973c;
      FUN_00414af0();
      local_178 = (int ****)0x469743;
      FUN_00461470();
      break;
    case (int *****)0x244:
      local_174 = (int ****)0x46974d;
      FUN_00414af0();
      local_174 = (int ****)0x469754;
      local_159 = FUN_00460fe0();
      goto LAB_004691fc;
    case (int *****)0x24e:
      local_174 = (int ****)0x46975e;
      FUN_00414a70();
      local_174 = (int ****)0x469765;
      local_159 = FUN_0045eb70();
      goto LAB_004691fc;
    case (int *****)0x24f:
      local_13c[0] = (int ****)
                     (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
      local_174 = local_13c[0];
      local_178 = (int ****)0x46977d;
      FUN_00414a70();
      local_178 = (int ****)0x469784;
      FUN_0045b430();
      break;
    case (int *****)0x250:
      local_13c[0] = (int ****)
                     (CONCAT31(local_13c[0]._1_3_,(char)((uint)param_8 >> 5)) & 0xffffff01);
      local_174 = local_13c[0];
      local_178 = (int ****)0x46979c;
      FUN_00414a70();
      local_178 = (int ****)0x4697a3;
      FUN_0045b450();
      break;
    case (int *****)0x251:
      local_174 = (int ****)0x0;
      local_178 = (int ****)0x4697ae;
      FUN_00414a70();
      local_178 = (int ****)0x4697b5;
      FUN_0045b960();
      break;
    case (int *****)0x252:
      local_174 = (int ****)0x0;
      goto LAB_004697bb;
    case (int *****)0x253:
      local_178 = &local_154;
      local_174 = (int ****)0x1;
      ppppiStack_17c = (int ****)0x4697dd;
      FUN_00414a70();
      ppppiStack_17c = (int ****)0x4697e4;
      FUN_00460000();
      break;
    case (int *****)0x254:
      local_178 = &local_154;
      local_174 = (int ****)0x3;
      ppppiStack_17c = (int ****)0x4697f5;
      FUN_00414a70();
      ppppiStack_17c = (int ****)0x4697fc;
      FUN_00460000();
      break;
    case (int *****)0x255:
      local_174 = (int ****)0x4;
LAB_004697bb:
      local_178 = &local_154;
      ppppiStack_17c = (int ****)0x4697c5;
      FUN_00414a70();
      ppppiStack_17c = (int ****)0x4697cc;
      FUN_00460000();
    }
    goto LAB_00468f74;
  }
  if ((int *****)0x47f < pppppiVar4) {
    if (pppppiVar4 < (int *****)0x583) {
      if (pppppiVar4 != (int *****)0x582) {
        switch(pppppiVar4) {
        case (int *****)0x480:
          local_174 = (int ****)0x1;
          local_178 = (int ****)0x469a08;
          FUN_00875460();
          break;
        case (int *****)0x481:
          local_174 = (int ****)0x2;
          local_178 = (int ****)0x469a17;
          FUN_00875460();
          break;
        case (int *****)0x482:
          local_174 = (int ****)0x3;
          local_178 = (int ****)0x469a26;
          FUN_00875460();
          break;
        case (int *****)0x483:
          local_174 = (int ****)0x4;
          local_178 = (int ****)0x469a35;
          FUN_00875460();
          break;
        case (int *****)0x484:
          local_174 = (int ****)0x5;
          local_178 = (int ****)0x469a44;
          FUN_00875460();
          break;
        case (int *****)0x485:
          local_174 = (int ****)0x6;
          local_178 = (int ****)0x469a53;
          FUN_00875460();
          break;
        case (int *****)0x486:
          local_174 = (int ****)0x7;
          local_178 = (int ****)0x469a62;
          FUN_00875460();
          break;
        case (int *****)0x487:
          local_174 = (int ****)0x8;
          local_178 = (int ****)0x469a71;
          FUN_00875460();
          break;
        default:
          goto switchD_0046928d_caseD_18;
        case (int *****)0x51e:
        case (int *****)0x528:
        case (int *****)0x532:
        case (int *****)0x53c:
        case (int *****)0x546:
        case (int *****)0x550:
          goto switchD_0046940d_caseD_14a;
        }
        goto LAB_00468f74;
      }
      local_174 = (int ****)0x469a82;
      local_174 = (int ****)FUN_0048ada0();
      local_178 = (int ****)0x0;
      ppppiStack_17c = (int ****)0x469a89;
      FUN_004642f0();
      ppppiStack_17c = (int ****)0x469a90;
      local_159 = FUN_00568ee0();
      goto LAB_004691fc;
    }
    if (pppppiVar4 < (int *****)0xfa1) {
      if (pppppiVar4 == (int *****)0xfa0) {
switchD_00469bb4_caseD_fa1:
        local_174 = (int ****)0x469bc2;
        local_159 = FUN_00467bd0();
      }
      else if (pppppiVar4 < (int *****)0xd53) {
        if (pppppiVar4 == (int *****)0xd52) {
          local_174 = (int ****)0x469b2f;
          iVar7 = FUN_004926e0();
          local_174 = *(int *****)(iVar7 + 4);
          local_178 = (int ****)0x469b38;
          FUN_00414370();
          local_178 = (int ****)0x469b3f;
          local_159 = FUN_00426f00();
        }
        else if (pppppiVar4 == (int *****)0x58c) {
          local_174 = (int ****)0x469b12;
          local_174 = (int ****)FUN_0048ada0();
          local_178 = (int ****)0x1;
          ppppiStack_17c = (int ****)0x469b1a;
          FUN_004642f0();
          ppppiStack_17c = (int ****)0x469b21;
          local_159 = FUN_00568ee0();
        }
        else {
          if (pppppiVar4 != (int *****)0x596) {
            bVar12 = pppppiVar4 == (int *****)0xd48;
            goto LAB_00469ac8;
          }
          local_174 = (int ****)0x469af5;
          local_174 = (int ****)FUN_0048ada0();
          local_178 = (int ****)0x2;
          ppppiStack_17c = (int ****)0x469afd;
          FUN_004642f0();
          ppppiStack_17c = (int ****)0x469b04;
          local_159 = FUN_00568ee0();
        }
      }
      else if (pppppiVar4 == (int *****)0xd5c) {
        local_174 = (int ****)0x469b86;
        iVar7 = FUN_004926e0();
        local_174 = *(int *****)(iVar7 + 4);
        local_178 = (int ****)0x469b8f;
        FUN_00414370();
        local_178 = (int ****)0x469b96;
        local_159 = FUN_00428c20();
      }
      else {
        if (pppppiVar4 != (int *****)0xed8) {
          bVar12 = pppppiVar4 == (int *****)0xed9;
LAB_00469ac8:
          if (!bVar12) goto switchD_0046928d_caseD_18;
          local_174 = (int ****)0x469ad7;
          iVar7 = FUN_004926e0();
          local_174 = *(int *****)(iVar7 + 4);
          local_178 = (int ****)0x469ae0;
          FUN_00414370();
          local_178 = (int ****)0x469ae7;
          FUN_0042b5a0();
          goto LAB_00468f74;
        }
        local_174 = (int ****)0x469b65;
        iVar7 = FUN_004926e0();
        local_174 = *(int *****)(iVar7 + 4);
        local_178 = (int ****)0x469b6e;
        iVar7 = FUN_00582650();
        local_159 = iVar7 != 0;
      }
      goto LAB_004691fc;
    }
    if (pppppiVar4 < (int *****)0x1389) {
      if (pppppiVar4 == (int *****)0x1388) {
        local_174 = (int ****)0x1;
        local_178 = (int ****)0x469bde;
        local_178 = (int ****)FUN_006b22d0();
        ppppiStack_17c = (int ****)0x469be4;
        FUN_004310f0();
        ppppiStack_17c = (int ****)0x469beb;
        local_159 = FUN_004fb090();
      }
      else {
        switch(pppppiVar4) {
        case (int *****)0xfa1:
        case (int *****)0xfa2:
        case (int *****)0xfa3:
        case (int *****)0xfa4:
        case (int *****)0xfa5:
          goto switchD_00469bb4_caseD_fa1;
        case (int *****)0xfa6:
          local_174 = (int ****)0x469bce;
          local_159 = FUN_004655e0();
          break;
        default:
          goto switchD_0046928d_caseD_18;
        }
      }
      goto LAB_004691fc;
    }
    switch(pppppiVar4) {
    case (int *****)0x1392:
      local_174 = (int ****)0x1;
      local_178 = (int ****)0x469c4e;
      local_178 = (int ****)FUN_006b22d0();
      ppppiStack_17c = (int ****)0x469c54;
      FUN_004310f0();
      ppppiStack_17c = (int ****)0x469c5b;
      local_159 = FUN_004fb450();
      break;
    default:
switchD_0046928d_caseD_18:
      local_174 = (int ****)local_13c;
      ppppiStack_17c = (int ****)0x469ceb;
      local_178 = (int ****)pppppiVar4;
      cVar1 = FUN_004636f0();
      ppppiVar10 = local_13c[0];
      if (cVar1 == '\0') goto LAB_00468cbd;
      local_174 = (int ****)0x0;
      local_178 = local_13c[0];
      ppppiStack_17c = (int ****)0x469cfe;
      FUN_004151f0();
      ppppiStack_17c = (int ****)0x469d05;
      cVar1 = FUN_008660f0();
      local_174 = (int ****)0x0;
      local_178 = ppppiVar10;
      if (cVar1 != '\0') {
        ppppiStack_17c = (int ****)0x469d10;
        FUN_004151f0();
        ppppiStack_17c = (int ****)0x469d17;
        FUN_008665e0();
        goto LAB_00468f74;
      }
      ppppiStack_17c = (int ****)0x469d21;
      FUN_004151f0();
      ppppiStack_17c = (int ****)0x469d28;
      iVar7 = FUN_00866e50();
      local_159 = iVar7 != 0;
      break;
    case (int *****)0x139c:
      local_174 = (int ****)0x469c16;
      local_174 = (int ****)FUN_006b22d0();
      local_178 = (int ****)0x469c1c;
      FUN_00414570();
      local_178 = (int ****)0x469c23;
      local_159 = FUN_004358f0();
      break;
    case (int *****)0x13a6:
      local_174 = &local_154;
      local_178 = (int ****)0x469c88;
      local_159 = FUN_00463680();
      break;
    case (int *****)0x13b0:
      local_174 = (int ****)0x469c65;
      FUN_004310f0();
      local_174 = (int ****)0x469c6e;
      local_174 = (int ****)FUN_006b22d0();
      local_178 = (int ****)0x469c74;
      FUN_004fab70();
      goto LAB_00468f74;
    case (int *****)0x13ba:
      local_174 = (int ****)0x469c31;
      local_174 = (int ****)FUN_006b22d0();
      local_178 = (int ****)0x469c37;
      FUN_004310f0();
      local_178 = (int ****)0x469c3e;
      local_159 = FUN_004fc1a0();
      break;
    case (int *****)0x13c4:
      local_174 = (int ****)0x469cb1;
      local_174 = (int ****)FUN_006b22d0();
      local_178 = (int ****)0x469cb7;
      FUN_004310f0();
      local_178 = (int ****)0x469cbe;
      FUN_004faa80();
      goto LAB_00468f74;
    case (int *****)0x13ce:
      local_174 = (int ****)0x469ccc;
      local_174 = (int ****)FUN_006b22d0();
      local_178 = (int ****)0x469cd2;
      FUN_00414570();
      local_178 = (int ****)0x469cd9;
      local_159 = FUN_00435070();
      break;
    case (int *****)0x13d8:
      local_174 = (int ****)0x469c96;
      local_174 = (int ****)FUN_006b22d0();
      local_178 = (int ****)0x469c9c;
      FUN_004642f0();
      local_178 = (int ****)0x469ca3;
      FUN_0056a1c0();
      goto LAB_00468f74;
    }
    goto LAB_004691fc;
  }
  if (pppppiVar4 == (int *****)0x47f) {
    local_174 = (int ****)0x0;
    local_178 = (int ****)0x4699c8;
    FUN_00875460();
    goto LAB_00468f74;
  }
  switch(pppppiVar4) {
  case (int *****)0x370:
    local_174 = (int ****)0x2;
    local_178 = (int ****)0x469974;
    FUN_00414c70();
    local_178 = (int ****)0x46997b;
    local_159 = FUN_00472bd0();
    goto LAB_004691fc;
  default:
    goto switchD_0046928d_caseD_18;
  case (int *****)0x37a:
    local_174 = (int ****)0x469985;
    FUN_00414c70();
    local_174 = (int ****)0x46998c;
    local_159 = FUN_00472e70();
    goto LAB_004691fc;
  case (int *****)0x384:
    local_174 = (int ****)0x46985f;
    FUN_004bc9b0();
    break;
  case (int *****)0x3a2:
    local_174 = (int ****)0x46986b;
    local_159 = FUN_00466410();
    goto LAB_004691fc;
  case (int *****)0x3a3:
    local_174 = (int ****)0x469875;
    local_159 = FUN_0088dc70();
    goto LAB_004691fc;
  case (int *****)0x3ac:
    local_174 = (int ****)0x46987f;
    FUN_004d9de0();
    break;
  case (int *****)0x3b0:
    local_174 = (int ****)0x469889;
    FUN_0058d6f0();
    break;
  case (int *****)0x3b1:
    local_174 = (int ****)0x469893;
    local_159 = FUN_0087e820();
    goto LAB_004691fc;
  case (int *****)0x3b6:
    local_174 = (int ****)0x46989d;
    FUN_00875410();
    break;
  case (int *****)0x3c0:
    local_174 = (int ****)0x469996;
    local_159 = FUN_0087a580();
    goto LAB_004691fc;
  case (int *****)0x3ca:
    local_174 = (int ****)0x4699a2;
    local_159 = FUN_00468370();
    goto LAB_004691fc;
  case (int *****)0x3de:
    local_174 = (int ****)0x4699ac;
    local_159 = FUN_0087e5d0();
    goto LAB_004691fc;
  case (int *****)0x3e3:
    local_174 = (int ****)0x4699b6;
    FUN_00414470();
    local_174 = (int ****)0x4699bd;
    FUN_0042f1c0();
    break;
  case (int *****)0x3e8:
    local_174 = (int ****)0x46995c;
    FUN_004b9250();
    break;
  case (int *****)0x3ed:
    local_174 = (int ****)0x46984e;
    FUN_00414a70();
    local_174 = (int ****)0x469855;
    FUN_0045e6d0();
    break;
  case (int *****)0x3f2:
    local_174 = (int ****)0x4698a7;
    FUN_00414470();
    local_174 = (int ****)0x4698ae;
    FUN_0042eab0();
    break;
  case (int *****)0x3f7:
    local_174 = (int ****)0x4698da;
    FUN_004145f0();
    local_174 = (int ****)0x4698e1;
    FUN_00438240();
    break;
  case (int *****)0x3fc:
    local_174 = (int ****)0x4698c9;
    FUN_004145f0();
    local_174 = (int ****)0x4698d0;
    FUN_004399e0();
    break;
  case (int *****)0x401:
    local_174 = (int ****)0x1;
    local_178 = (int ****)0x4698ed;
    FUN_005833f0();
    break;
  case (int *****)0x403:
    local_174 = (int ****)0x4698fa;
    FUN_00414ff0();
    local_174 = (int ****)0x469901;
    FUN_00484f50();
    break;
  case (int *****)0x404:
    local_174 = (int ****)0x46990f;
    iVar7 = FUN_004926e0();
    local_174 = *(int *****)(iVar7 + 4);
    local_178 = (int ****)0x469918;
    FUN_00414ff0();
    local_178 = (int ****)0x46991f;
    FUN_00488690();
    break;
  case (int *****)0x405:
    local_174 = (int ****)0x469929;
    FUN_00414ff0();
    local_174 = (int ****)0x469930;
    FUN_00486710();
    break;
  case (int *****)0x406:
    local_174 = (int ****)0x4698b8;
    FUN_004145f0();
    local_174 = (int ****)0x4698bf;
    FUN_004399c0();
    break;
  case (int *****)0x40b:
    local_174 = (int ****)0x469968;
    local_159 = FUN_004664b0();
LAB_004691fc:
    local_4._0_1_ = 2;
    local_174 = (int ****)0x469210;
    FUN_00460430();
    local_4._0_1_ = 1;
    local_174 = (int ****)0x469221;
    FUN_008e0110();
    local_4 = (uint)local_4._1_3_ << 8;
    local_174 = (int ****)0x469231;
    thunk_FUN_00703bc0();
    local_4 = 0xffffffff;
    local_174 = (int ****)0x469248;
    FUN_008e0110();
    goto LAB_00468d04;
  case (int *****)0x410:
    local_174 = (int ****)0x46994b;
    FUN_00414ff0();
    local_174 = (int ****)0x469952;
    FUN_00487230();
    break;
  case (int *****)0x411:
    local_174 = (int ****)0x46993a;
    FUN_00414ff0();
    local_174 = (int ****)0x469941;
    FUN_00487280();
  }
LAB_00468f74:
  local_4._0_1_ = 2;
  local_174 = (int ****)0x468f88;
  FUN_00460430();
  local_4._0_1_ = 1;
  local_174 = (int ****)0x468f99;
  FUN_008e0110();
  local_4 = (uint)local_4._1_3_ << 8;
  local_174 = (int ****)0x468fa9;
  thunk_FUN_00703bc0();
  local_4 = 0xffffffff;
  local_174 = (int ****)0x468fc0;
  FUN_008e0110();
LAB_00468d04:
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

