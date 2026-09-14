// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x861390L (requested via site 0x861491)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN_00861390(int param_1_00,undefined4 param_1,float param_2)

{
  float fVar1;
  float fVar2;
  double dVar3;
  char cVar4;
  int iVar5;
  uint uVar6;
  undefined4 *puVar7;
  undefined8 *puVar8;
  float *pfVar9;
  undefined4 *puVar10;
  bool bVar11;
  float10 fVar12;
  float10 fVar13;
  undefined4 uVar14;
  undefined *puVar15;
  undefined4 uVar16;
  undefined4 uVar17;
  float fVar18;
  char local_fe;
  char local_fd;
  float local_fc;
  float local_f8;
  float local_f4;
  undefined8 local_f0;
  float local_e8;
  float local_e4;
  float fStack_e0;
  float local_dc;
  char local_d5;
  float local_d4;
  float local_d0;
  float local_cc;
  float local_c8;
  float local_c4;
  float fStack_c0;
  float local_bc;
  float local_b8;
  float local_b4;
  float local_b0;
  float local_ac;
  float local_a8;
  float local_a4;
  float local_a0;
  float fStack_9c;
  float fStack_98;
  float fStack_94;
  undefined local_90 [4];
  undefined4 auStack_8c [9];
  undefined4 uStack_68;
  undefined4 uStack_64;
  undefined4 uStack_60;
  undefined4 uStack_5c;
  undefined4 auStack_58 [9];
  undefined4 auStack_34 [13];
  
  fVar12 = (float10)FUN_00734230();
  *(float *)(param_1_00 + 8) = (float)fVar12;
  fVar12 = (float10)FUN_00734250();
  *(float *)(param_1_00 + 0xc) = (float)fVar12;
  fVar12 = (float10)FUN_00734270();
  *(float *)(param_1_00 + 0x10) = (float)fVar12;
  local_e4 = *(float *)(param_1_00 + 0x24) - param_2;
  *(float *)(param_1_00 + 0x24) = local_e4;
  if (local_e4 < 0.0) {
    *(undefined4 *)(param_1_00 + 0x24) = 0;
  }
  *(bool *)(param_1_00 + 0x28) =
       0.0 < *(float *)(param_1_00 + 0x24) != NAN(*(float *)(param_1_00 + 0x24));
  local_fd = FUN_0085c330();
  local_fe = FUN_0085c310();
  local_d5 = FUN_00734180();
  if (local_d5 == '\0') {
    if ((local_fd != '\0') && (local_fe != '\0')) {
      *(undefined4 *)(param_1_00 + 0x14) = 0;
      *(undefined4 *)(param_1_00 + 0x18) = 0;
      *(undefined4 *)(param_1_00 + 0x1c) = 0;
      return;
    }
  }
  else if ((local_fd != '\0') || (local_fe != '\0')) {
    FUN_0085d290(0);
    local_fe = '\0';
    FUN_0085d2f0(0);
    local_fd = '\0';
    *(undefined4 *)(param_1_00 + 0x4c) = 0;
  }
  FUN_0085c0c0(&local_bc);
  FUN_0085c280(&local_a0);
  local_d4 = 0.0;
  local_d0 = 0.0;
  *(undefined *)(param_1_00 + 0x36) = 0;
  local_cc = 0.0;
  if (((local_d5 != '\0') || (local_fd == '\0')) || (local_fe == '\0')) {
    FUN_004154f0();
    iVar5 = FUN_007ce1e0();
    if ((iVar5 == 1) || (*(int *)(param_1_00 + 0x44) == 1)) {
      *(undefined4 *)(param_1_00 + 0x54) = 0;
      *(undefined4 *)(param_1_00 + 0x58) = 0;
      *(undefined4 *)(param_1_00 + 0x5c) = 0;
LAB_00861509:
      iVar5 = param_1_00 + 0x54;
      puVar7 = (undefined4 *)(param_1_00 + 0x60);
      *puVar7 = 0;
      uVar14 = _DAT_00a91f68;
      *(undefined4 *)(param_1_00 + 100) = 0;
      *(undefined4 *)(param_1_00 + 0x68) = 0;
      uVar17 = *(undefined4 *)(param_1_00 + 4);
      uVar16 = 2;
      puVar15 = local_90;
      pfVar9 = &local_bc;
      FUN_00415570(pfVar9,uVar14,iVar5,puVar7,puVar15,2,uVar17);
      cVar4 = FUN_00857370(pfVar9,uVar14,iVar5,puVar7,puVar15,uVar16,uVar17);
      if (cVar4 != '\0') {
        *(undefined *)(param_1_00 + 0x36) = 1;
      }
    }
    else {
      FUN_004154f0();
      iVar5 = FUN_007ce1e0();
      if (iVar5 == 0) {
        uVar6 = (int)*(short *)(param_1_00 + 0x50) + 1U & 0x80000003;
        if ((int)uVar6 < 0) {
          uVar6 = (uVar6 - 1 | 0xfffffffc) + 1;
        }
        *(short *)(param_1_00 + 0x50) = (short)uVar6;
        if ((short)uVar6 == 0) {
          *(undefined4 *)(param_1_00 + 0x54) = 0;
          *(undefined4 *)(param_1_00 + 0x58) = 0;
          *(undefined4 *)(param_1_00 + 0x5c) = 0;
          goto LAB_00861509;
        }
        local_e4 = (float)_DAT_00a91fc0 * 0.0;
        iVar5 = param_1_00 + 0x60;
        local_ac = local_bc;
        local_a8 = local_b8;
        local_a4 = local_b4;
        fVar18 = local_bc + local_e4;
        fVar1 = local_b8 + local_e4;
        fVar2 = local_b4 - (float)_DAT_00a91fc0;
        local_c8 = local_e4;
        local_c4 = local_e4;
        fVar12 = (float10)FUN_0043a1d0(iVar5);
        if ((float10)_DAT_00a79734 < fVar12) {
          fVar12 = (float10)FUN_0043a1d0(iVar5);
          local_dc = (float)fVar12;
          fVar12 = (float10)FUN_0043a1d0(iVar5);
          local_b0 = (float)(fVar12 - (float10)local_dc);
          fVar12 = (float10)FUN_0043a1d0(iVar5);
          local_e4 = (float)(fVar12 - (float10)local_dc);
          if (local_b0 * local_e4 < (float)_DAT_00a79db0 !=
              (NAN(local_b0 * local_e4) || NAN((float)_DAT_00a79db0))) {
            *(undefined *)(param_1_00 + 0x36) = 1;
            local_e4 = local_b0 / (local_b0 - local_e4);
            fVar18 = local_bc + local_e4 * (fVar18 - local_bc);
            *(float *)(param_1_00 + 0x54) = fVar18;
            fVar1 = (fVar1 - local_b8) * local_e4 + local_b8;
            local_f0 = (double)CONCAT44(fVar1,fVar18);
            *(float *)(param_1_00 + 0x58) = fVar1;
            local_e8 = local_b4 + local_e4 * (fVar2 - local_b4);
            *(float *)(param_1_00 + 0x5c) = local_e8;
          }
        }
      }
    }
  }
  *(undefined4 *)(param_1_00 + 0x40) = _DAT_00a91f68;
  if (*(char *)(param_1_00 + 0x36) != '\0') {
    fVar18 = *(float *)(param_1_00 + 0x54) - local_bc;
    fVar1 = *(float *)(param_1_00 + 0x58) - local_b8;
    fVar2 = *(float *)(param_1_00 + 0x5c) - local_b4;
    local_e4 = fVar2 * fVar2 + fVar1 * fVar1 + fVar18 * fVar18;
    fVar12 = (float10)_CIsqrt();
    local_e4 = (float)fVar12;
    *(float *)(param_1_00 + 0x40) = local_e4;
  }
  FUN_004154f0();
  iVar5 = FUN_007ce1e0();
  if (iVar5 == 0) {
    if ((local_d5 == '\0') && ((local_fd == '\0' || (local_fe == '\0')))) {
      local_e4 = fStack_98 * fStack_98 + fStack_9c * fStack_9c + local_a0 * local_a0;
      fVar12 = (float10)_CIsqrt();
      local_e4 = (float)fVar12;
      bVar11 = _DAT_00a7b280 < local_e4;
      if (((*(int *)(param_1_00 + 0x44) != 3) && (*(int *)(param_1_00 + 0x44) != 4)) ||
         (*(char *)(param_1_00 + 0x35) == '\0')) {
        if (((bVar11) || (*(char *)(param_1_00 + 0x36) == '\0')) ||
           (0.0 < *(float *)(param_1_00 + 0x24) != NAN(*(float *)(param_1_00 + 0x24)))) {
          bVar11 = true;
        }
        else {
          bVar11 = false;
        }
      }
      if (!bVar11) {
        *(int *)(param_1_00 + 0x4c) = *(int *)(param_1_00 + 0x4c) + 1;
        if (100 < *(int *)(param_1_00 + 0x4c)) {
          FUN_0085d290(1);
          local_fe = '\x01';
          FUN_0085d2f0(1);
          local_fd = '\x01';
          *(undefined4 *)(param_1_00 + 0x4c) = 100;
        }
        goto LAB_0086187e;
      }
    }
    *(undefined4 *)(param_1_00 + 0x4c) = 0;
  }
LAB_0086187e:
  FUN_0096ccb0(*(undefined4 *)(param_1_00 + 8));
  if ((*(char *)(param_1_00 + 0x48) == '\0') &&
     (((iVar5 = *(int *)(param_1_00 + 0x44), iVar5 != 1 || (*(char *)(param_1_00 + 0x34) == '\0'))
      || (local_b4 < _DAT_00a91f70 == (NAN(local_b4) || NAN(_DAT_00a91f70)))))) {
    if ((iVar5 == 3) || (iVar5 == 4)) {
      FUN_007c3bb0(*(undefined4 *)(param_1_00 + 0x10));
      goto LAB_00861912;
    }
  }
  else {
    FUN_007c3bb0(-*(float *)(param_1_00 + 0x10));
LAB_00861912:
    puVar7 = (undefined4 *)FUN_0096cbc0(auStack_8c,auStack_34);
    puVar10 = auStack_58;
    for (iVar5 = 9; iVar5 != 0; iVar5 = iVar5 + -1) {
      *puVar10 = *puVar7;
      puVar7 = puVar7 + 1;
      puVar10 = puVar10 + 1;
    }
  }
  fVar18 = _DAT_00a91f70;
  puVar7 = auStack_58;
  puVar10 = auStack_34;
  for (iVar5 = 9; iVar5 != 0; iVar5 = iVar5 + -1) {
    *puVar10 = *puVar7;
    puVar7 = puVar7 + 1;
    puVar10 = puVar10 + 1;
  }
  cVar4 = *(char *)(param_1_00 + 0x35);
  if ((cVar4 != '\0') && ((*(int *)(param_1_00 + 0x44) == 1 || (*(int *)(param_1_00 + 0x44) == 4))))
  {
    fVar1 = *(float *)(param_1_00 + 0x20);
    if (*(char *)(param_1_00 + 0x34) == '\0') {
      if (local_b4 < fVar1) {
        *(undefined *)(param_1_00 + 0x34) = 1;
      }
      if (*(char *)(param_1_00 + 0x34) != '\0') {
        *(undefined4 *)(param_1_00 + 0x20) = _DAT_00a91f6c;
      }
    }
    else {
      if (fVar1 < local_b4 != (fVar1 == local_b4)) {
        *(undefined *)(param_1_00 + 0x34) = 0;
      }
      if (*(char *)(param_1_00 + 0x34) != '\0') {
        if ((_DAT_00a7b114 < local_b4 == (NAN(_DAT_00a7b114) || NAN(local_b4))) ||
           (*(char *)(param_1_00 + 0x36) == '\0')) goto LAB_008619bb;
        *(undefined *)(param_1_00 + 0x34) = 0;
      }
      *(float *)(param_1_00 + 0x20) = fVar18;
    }
LAB_008619bb:
    if (((local_b4 < fVar18 != (NAN(local_b4) || NAN(fVar18))) && (local_fd == '\0')) &&
       (local_fe == '\0')) {
      local_e4 = local_b4 - (float)_DAT_00a91fb8;
      local_dc = 0.0;
      if (local_e4 <= 0.0) {
        if (local_e4 < (float)_DAT_00a91fb0 == (NAN(local_e4) || NAN((float)_DAT_00a91fb0))) {
          local_e4 = ABS(local_e4);
          local_dc = ((local_e4 - (float)_DAT_00a7af80) * (float)_DAT_00a79a08) /
                     (float)_DAT_00a7af80 + (float)_DAT_00a79818;
        }
        else {
          local_dc = 1.0;
        }
      }
      fStack_c0 = local_dc * (float)_DAT_00a91fa8 * (float)_PTR_00a7a618;
      local_d4 = local_d4 + 0.0;
      local_d0 = local_d0 + 0.0;
      local_cc = fStack_c0 + local_cc;
    }
  }
  if (cVar4 != '\0') {
    if ((local_d5 == '\0') || (*(char *)(param_1_00 + 0x48) != '\0')) {
      if ((cVar4 == '\0') || ((local_d5 == '\0' || (*(char *)(param_1_00 + 0x48) == '\0'))))
      goto LAB_00862070;
      local_dc = 0.0;
      fVar12 = (float10)FUN_00991a70();
      if (fVar12 <= (float10)_DAT_00a79734) {
        fVar12 = (float10)FUN_00861220();
        if ((float10)_DAT_00a79734 < fVar12) {
          fVar12 = (float10)FUN_00861220();
          fVar12 = fVar12 * (float10)_DAT_00a7a6e8;
          goto LAB_00861ed4;
        }
      }
      else {
        fVar12 = (float10)FUN_00991a70();
        fVar12 = fVar12 * (float10)_DAT_00a873a8;
LAB_00861ed4:
        local_dc = (float)fVar12;
      }
      fVar12 = (float10)FUN_00734210();
      fStack_e0 = (float)(fVar12 * (float10)_DAT_00a7a6e8);
      fVar12 = (float10)FUN_00861240();
      local_f0 = (double)fVar12;
      fVar12 = (float10)FUN_006c9910();
      local_ac = (float)(((float10)local_f0 - fVar12) * (float10)_DAT_00a7a6e8);
      local_c4 = -local_dc;
      local_dc = 0.0;
      local_f0 = (double)CONCAT44(local_c4 + fStack_e0 + 0.0,local_ac + 0.0);
      local_e8 = 0.0;
      fVar12 = (float10)FUN_00991a70();
      if (fVar12 <= (float10)_DAT_00a79734) {
        fVar12 = (float10)FUN_004b2a20();
        uVar17 = _DAT_00a7b1d0;
        if ((float10)_DAT_00a7a6e8 < fVar12) goto LAB_00861f9d;
      }
      else {
        fVar12 = (float10)FUN_004b2a20();
        uVar17 = _DAT_00a7b1bc;
        if ((float10)_DAT_00a873a8 < fVar12) {
LAB_00861f9d:
          pfVar9 = &local_c8;
          FUN_0045c290(&local_ac,0x3f800000);
          puVar8 = (undefined8 *)FUN_0045b380(pfVar9,uVar17);
          local_f0 = (double)*puVar8;
          local_e8 = *(float *)(puVar8 + 1);
        }
      }
      puVar7 = auStack_34;
      puVar10 = auStack_8c;
      for (iVar5 = 9; iVar5 != 0; iVar5 = iVar5 + -1) {
        *puVar10 = *puVar7;
        puVar7 = puVar7 + 1;
        puVar10 = puVar10 + 1;
      }
      uStack_5c = 0x3f800000;
      uStack_68 = 0;
      uStack_64 = 0;
      uStack_60 = 0;
      pfVar9 = (float *)FUN_008566a0(&local_c8,&local_f0);
      local_d4 = *pfVar9 + local_d4;
      local_d0 = pfVar9[1] + local_d0;
      local_cc = pfVar9[2] + local_cc;
    }
    else {
      fStack_e0 = *(float *)(param_1_00 + 0x38) / (float)_DAT_00a91fa0;
      local_e4 = fStack_e0 * (float)_DAT_00a7b298;
      local_b0 = (*(float *)(param_1_00 + 0x3c) / (float)_DAT_00a91fa0) * (float)_DAT_00a7b298;
      fStack_e0 = fStack_e0 * (float)_DAT_00a7b2a0;
      local_dc = 0.0;
      fStack_94 = fStack_e0;
      fVar12 = (float10)FUN_00991a70();
      if (fVar12 <= (float10)_DAT_00a79734) {
        fVar12 = (float10)FUN_00861220();
        if ((float10)_DAT_00a79734 < fVar12) {
          fVar12 = (float10)FUN_00861220();
          fVar12 = fVar12 * (float10)local_e4;
          goto LAB_00861b34;
        }
      }
      else {
        fVar12 = (float10)FUN_00991a70();
        fVar12 = fVar12 * (float10)local_b0;
LAB_00861b34:
        local_dc = (float)fVar12;
      }
      fVar12 = (float10)FUN_00734210();
      fStack_94 = (float)(fVar12 * (float10)fStack_94);
      fVar12 = (float10)FUN_00861240();
      local_f0 = (double)fVar12;
      fVar12 = (float10)FUN_006c9910();
      local_ac = (float)(((float10)local_f0 - fVar12) * (float10)fStack_e0);
      local_c4 = -local_dc;
      local_dc = 0.0;
      local_f0 = (double)CONCAT44(local_c4 + fStack_94 + 0.0,local_ac + 0.0);
      local_e8 = 0.0;
      fVar12 = (float10)FUN_00991a70();
      if (fVar12 <= (float10)_DAT_00a79734) {
        fVar12 = (float10)FUN_004b2a20();
        if ((float10)local_e4 < fVar12 != (NAN((float10)local_e4) || NAN(fVar12))) {
          pfVar9 = &local_c8;
          fVar18 = local_e4;
          FUN_0045c290(&local_ac,0x3f800000);
          puVar8 = (undefined8 *)FUN_0045b380(pfVar9,fVar18);
          local_f0 = (double)*puVar8;
          local_e8 = *(float *)(puVar8 + 1);
        }
      }
      else {
        fVar12 = (float10)FUN_004b2a20();
        if ((float10)local_b0 < fVar12 != (NAN((float10)local_b0) || NAN(fVar12))) {
          pfVar9 = &local_c8;
          fVar18 = local_b0;
          FUN_0045c290(&local_ac,0x3f800000);
          puVar8 = (undefined8 *)FUN_0045b380(pfVar9,fVar18);
          local_f0 = (double)*puVar8;
          local_e8 = *(float *)(puVar8 + 1);
        }
      }
      cVar4 = *(char *)(param_1_00 + 0x36);
      if (cVar4 != '\0') {
        local_fc = local_a0;
        local_f4 = 0.0;
        local_f8 = fStack_9c;
        fVar13 = (float10)FUN_004b2a20();
        fVar12 = (float10)1;
        if (fVar12 < fVar13 != (NAN(fVar12) || NAN(fVar13))) {
          pfVar9 = (float *)FUN_0045c290(&local_c8,(float)fVar12);
          local_fc = *pfVar9;
          local_f8 = pfVar9[1];
          local_f4 = pfVar9[2];
        }
        fStack_e0 = *(float *)(param_1_00 + 0x68) * local_f4 +
                    *(float *)(param_1_00 + 0x60) * local_fc +
                    *(float *)(param_1_00 + 100) * local_f8;
        local_e4 = 1.0;
        if (fStack_e0 < 0.0 != NAN(fStack_e0)) {
          local_e4 = fStack_e0 + (float)_DAT_00a79818;
        }
        local_f0 = (double)CONCAT44(local_f0._4_4_ * local_e4,local_e4 * (float)local_f0);
        local_e8 = local_e4 * local_e8;
      }
      dVar3 = _DAT_00a79a08;
      if ((*(char *)(param_1_00 + 0x34) != '\0') ||
         ((cVar4 == '\0' && (dVar3 = _DAT_00a7dcf0, *(int *)(param_1_00 + 0x44) != 3)))) {
        fVar18 = (float)dVar3;
        local_f0 = (double)CONCAT44(local_f0._4_4_ * fVar18,(float)local_f0 * fVar18);
        local_e8 = fVar18 * local_e8;
      }
      puVar7 = auStack_34;
      puVar10 = auStack_8c;
      for (iVar5 = 9; iVar5 != 0; iVar5 = iVar5 + -1) {
        *puVar10 = *puVar7;
        puVar7 = puVar7 + 1;
        puVar10 = puVar10 + 1;
      }
      uStack_5c = 0x3f800000;
      uStack_68 = 0;
      uStack_64 = 0;
      uStack_60 = 0;
      pfVar9 = (float *)FUN_008566a0(&local_c8,&local_f0);
      local_d4 = *pfVar9 + local_d4;
      local_d0 = pfVar9[1] + local_d0;
      local_cc = pfVar9[2] + local_cc;
      cVar4 = FUN_00734160(1);
      if ((((cVar4 != '\0') && (*(char *)(param_1_00 + 0x36) != '\0')) &&
          (NAN(*(float *)(param_1_00 + 0x24)) != (*(float *)(param_1_00 + 0x24) == 0.0))) &&
         (*(char *)(param_1_00 + 0x34) == '\0')) {
        local_c8 = 0.0;
        local_c4 = 0.0;
        fStack_c0 = _DAT_00a91f98;
        FUN_0085d180(&local_c8);
        *(undefined4 *)(param_1_00 + 0x24) = _DAT_00a7afd4;
      }
    }
  }
LAB_00862070:
  cVar4 = *(char *)(param_1_00 + 0x36);
  if (cVar4 == '\0') {
    if ((local_fd == '\0') && (local_fe == '\0')) goto LAB_0086224d;
  }
  else if ((local_fd == '\0') && (local_fe == '\0')) {
    fVar18 = local_bc - *(float *)(param_1_00 + 0x54);
    fVar1 = local_b8 - *(float *)(param_1_00 + 0x58);
    fVar2 = local_b4 - *(float *)(param_1_00 + 0x5c);
    fStack_e0 = 0.0;
    local_ac = 0.0;
    local_a8 = 0.0;
    local_a4 = fStack_98 - 0.0;
    local_e8 = fVar2;
    local_f0._0_4_ = fVar18;
    local_f0._4_4_ = fVar1;
    FUN_0043ae80(0x3f800000);
    local_c8 = -(float)local_f0;
    local_c4 = -local_f0._4_4_;
    fStack_c0 = -local_e8;
    fStack_e0 = fVar2 * fVar2 + fVar18 * fVar18 + fVar1 * fVar1;
    fVar12 = (float10)_CIsqrt();
    fStack_e0 = (local_a4 * fVar2 + local_ac * fVar18 + local_a8 * fVar1) * (float)_DAT_00a873a8 +
                ((float)fVar12 - (float)_DAT_00a91fc0) * (float)_DAT_00a91f90;
    local_fc = fStack_e0 * local_c8;
    local_f8 = local_c4 * fStack_e0;
    local_f4 = fStack_e0 * fStack_c0;
    if (_DAT_00a85af8 < param_2) {
      fStack_e0 = (float)_DAT_00a91f88 / param_2;
      local_fc = fStack_e0 * local_fc;
      local_f8 = local_f8 * fStack_e0;
      local_f4 = fStack_e0 * local_f4;
    }
    local_d4 = local_fc + local_d4;
    local_d0 = local_f8 + local_d0;
    local_cc = local_f4 + local_cc;
LAB_0086224d:
    fVar18 = -local_a0;
    local_f0._4_4_ = -fStack_9c;
    local_e8 = -fStack_98;
    dVar3 = _PTR_00a7a618;
    if ((*(char *)(param_1_00 + 0x48) == '\0') &&
       (((iVar5 = *(int *)(param_1_00 + 0x44), dVar3 = _DAT_00a7a6e8, iVar5 == 1 || (iVar5 == 2)) ||
        ((*(char *)(param_1_00 + 0x35) == '\0' && (iVar5 == 3)))))) {
      if (*(char *)(param_1_00 + 0x34) == '\0') {
        local_e8 = 0.0;
        if (cVar4 == '\0') {
          local_e8 = (float)_DAT_00a7dcf0;
          fVar18 = fVar18 * local_e8;
          local_f0._4_4_ = local_f0._4_4_ * local_e8;
          local_e8 = local_e8 * 0.0;
        }
      }
      else {
        local_e8 = local_e8 * (float)_DAT_00a7b0a0;
      }
    }
    fVar1 = (float)dVar3;
    local_f0._4_4_ = local_f0._4_4_ * fVar1;
    local_f0 = (double)CONCAT44(local_f0._4_4_,fVar18 * fVar1);
    local_e8 = fVar1 * local_e8;
    local_d4 = fVar18 * fVar1 + local_d4;
    local_d0 = local_f0._4_4_ + local_d0;
    local_cc = local_cc + local_e8;
  }
  if ((*(char *)(param_1_00 + 0x35) == '\0') ||
     ((*(char *)(param_1_00 + 0x48) == '\0' && (*(int *)(param_1_00 + 0x44) != 3)))) {
    if ((local_fd != '\0') || (local_fe != '\0')) goto LAB_008623a0;
  }
  else {
    if ((local_fd != '\0') || (local_fe != '\0')) goto LAB_008623a0;
    local_d4 = local_d4 + 0.0;
    local_d0 = local_d0 + 0.0;
    local_cc = local_cc + (float)_DAT_00a91f80;
  }
  FUN_0085d120(param_2,&local_d4);
LAB_008623a0:
  *(float *)(param_1_00 + 0x14) = local_a0;
  *(float *)(param_1_00 + 0x18) = fStack_9c;
  *(float *)(param_1_00 + 0x1c) = fStack_98;
  fVar18 = _DAT_00a797c8;
  if (ABS(*(float *)(param_1_00 + 0x14)) < _DAT_00a797c8) {
    *(undefined4 *)(param_1_00 + 0x14) = 0;
  }
  if (ABS(*(float *)(param_1_00 + 0x18)) < fVar18 !=
      (NAN(ABS(*(float *)(param_1_00 + 0x18))) || NAN(fVar18))) {
    *(undefined4 *)(param_1_00 + 0x18) = 0;
  }
  if (ABS(*(float *)(param_1_00 + 0x1c)) < fVar18) {
    *(undefined4 *)(param_1_00 + 0x1c) = 0;
    return;
  }
  return;
}

