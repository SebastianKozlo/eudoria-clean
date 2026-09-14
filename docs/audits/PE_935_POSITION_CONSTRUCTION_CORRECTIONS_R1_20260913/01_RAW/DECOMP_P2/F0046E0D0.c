// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x46e0d0L (requested via site 0x46e604)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_0046e0d0(undefined4 param_1,undefined4 param_2,undefined4 param_3,float param_4,int param_5
                 )

{
  char cVar1;
  uint uVar2;
  int iVar3;
  float *pfVar4;
  allocator<char> *paVar5;
  code **ppcVar6;
  undefined4 *puVar7;
  undefined4 *puVar8;
  bool bVar9;
  float10 fVar10;
  undefined auStack_c8 [3];
  allocator<char> local_c5;
  float local_c4;
  float fStack_c0;
  float local_bc;
  float local_b8;
  float local_b4;
  float fStack_b0;
  float local_ac;
  float local_a8;
  float local_a4;
  undefined4 local_a0;
  undefined4 uStack_9c;
  undefined4 uStack_98;
  int local_94;
  float fStack_90;
  float fStack_8c;
  float fStack_88;
  undefined **appuStack_78 [2];
  undefined4 *apuStack_70 [6];
  undefined4 uStack_58;
  undefined4 auStack_50 [4];
  undefined4 uStack_40;
  undefined4 uStack_3c;
  undefined4 uStack_38;
  code *apcStack_30 [4];
  undefined4 uStack_20;
  undefined4 uStack_1c;
  float fStack_18;
  int iStack_14;
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009a244b;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_c8;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xffffff28;
  ExceptionList = &local_c;
  local_ac = 0.0;
  local_a8 = 0.0;
  local_a4 = 0.0;
  local_bc = 0.0;
  local_94 = param_5;
  local_b8 = 0.0;
  local_b4 = 0.0;
  FUN_004da140(param_1);
  local_4 = 0;
  if (local_c4 == 0.0) {
    bVar9 = false;
  }
  else {
    FUN_0058e230(&local_ac);
    local_a4 = local_a4 + param_4;
    iVar3 = FUN_0042c270(0xd);
    bVar9 = iVar3 != 1;
  }
  local_4 = 0xffffffff;
  thunk_FUN_00703bc0(uVar2);
  if (bVar9) {
    FUN_0085b840(param_2);
    local_4 = 1;
    iVar3 = FUN_004123d0();
    if (iVar3 == 0) {
      bVar9 = false;
    }
    else {
      puVar7 = &local_a0;
      FUN_004123d0(puVar7);
      pfVar4 = (float *)FUN_0085af90(puVar7);
      local_bc = *pfVar4;
      local_b8 = pfVar4[1];
      local_b4 = pfVar4[2];
      paVar5 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_c5);
      local_4._0_1_ = 2;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)&fStack_90,"",paVar5);
      local_4._0_1_ = 3;
      FUN_0050a700(&local_c4,&fStack_90);
      local_4._0_1_ = 5;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)&fStack_90);
      local_4 = CONCAT31(local_4._1_3_,6);
      stlp_std::allocator<char>::~allocator<char>(&local_c5);
      iVar3 = FUN_0050a840();
      if (iVar3 != 0) {
        FUN_0050a840();
        iVar3 = FUN_00746550();
        iVar3 = iVar3 + 0x90;
        puVar7 = &local_a0;
        FUN_00437f70(puVar7,iVar3);
        pfVar4 = (float *)FUN_0082b5a0(puVar7,iVar3);
        local_bc = *pfVar4;
        local_b8 = pfVar4[1];
        local_b4 = pfVar4[2];
        puVar7 = &local_a0;
        FUN_004123d0(puVar7);
        iVar3 = FUN_0085af70(puVar7);
        local_b4 = *(float *)(iVar3 + 8) + local_b4;
      }
      local_4 = CONCAT31(local_4._1_3_,1);
      FUN_0059f0d0();
    }
    local_4 = 0xffffffff;
    FUN_008e0110();
    if (bVar9) {
      paVar5 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_c5);
      local_4 = 7;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)appuStack_78,"",paVar5);
      local_4._0_1_ = 8;
      FUN_0050a690(param_3,appuStack_78);
      local_4._0_1_ = 10;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)appuStack_78);
      local_4 = CONCAT31(local_4._1_3_,0xb);
      stlp_std::allocator<char>::~allocator<char>(&local_c5);
      cVar1 = FUN_006c4200();
      if (cVar1 == '\0') {
        bVar9 = false;
      }
      else {
        pfVar4 = &local_ac;
        local_bc = local_bc - local_ac;
        local_c4 = local_b8 - local_a8;
        fStack_c0 = local_b4 - local_a4;
        local_b8 = local_c4;
        local_b4 = fStack_c0;
        fStack_b0 = local_bc;
        FUN_004123d0(pfVar4);
        FUN_005094c0(pfVar4);
        fStack_90 = local_bc;
        fStack_8c = local_b8;
        fStack_88 = local_b4;
        FUN_0043ae80(0x3f800000);
        FUN_00732fa0();
        FUN_00733080(&fStack_90,0);
        local_a0 = uStack_40;
        puVar7 = &local_a0;
        uStack_98 = uStack_38;
        uStack_9c = uStack_3c;
        FUN_004123d0(puVar7);
        FUN_00509510(puVar7);
        fStack_c0 = fStack_c0 * fStack_c0 + fStack_b0 * fStack_b0 + local_c4 * local_c4;
        fVar10 = (float10)_CIsqrt();
        fStack_c0 = (float)fVar10;
        iVar3 = FUN_004123d0();
        fStack_b0 = *(float *)(iVar3 + 0x70);
        local_bc = 0.0;
        local_b8 = (fStack_c0 * (float)_PTR_00a7a618) / fStack_b0;
        local_b4 = 0.0;
        *(undefined4 *)(param_5 + 0x5c) = 0;
        *(float *)(param_5 + 0x60) = local_b8;
        *(undefined4 *)(param_5 + 100) = 0;
      }
      local_4 = 0xffffffff;
      FUN_0059f0d0();
      if (bVar9) {
        apcStack_30[2] = (code *)FUN_00414bf0();
        fStack_c0 = param_4;
        apcStack_30[3] = (code *)param_1;
        fStack_18 = param_4;
        apcStack_30[0] = FUN_0046e0d0;
        apcStack_30[1] = (code *)0x0;
        uStack_20 = param_2;
        iStack_14 = local_94;
        uStack_1c = param_3;
        ppcVar6 = apcStack_30;
        puVar7 = auStack_50;
        for (iVar3 = 8; iVar3 != 0; iVar3 = iVar3 + -1) {
          *puVar7 = *ppcVar6;
          ppcVar6 = ppcVar6 + 1;
          puVar7 = puVar7 + 1;
        }
        appuStack_78[0] = (undefined **)0x0;
        cVar1 = FUN_007b0940(auStack_50);
        if (cVar1 == '\0') {
          fStack_c0 = 4.48416e-44;
          apuStack_70[0] = (undefined4 *)stlp_std::__node_alloc::allocate((uint *)&fStack_c0);
          if (apuStack_70[0] != (undefined4 *)0x0) {
            puVar7 = auStack_50;
            puVar8 = apuStack_70[0];
            for (iVar3 = 8; iVar3 != 0; iVar3 = iVar3 + -1) {
              *puVar8 = *puVar7;
              puVar7 = puVar7 + 1;
              puVar8 = puVar8 + 1;
            }
          }
          appuStack_78[0] = &PTR_FUN_00a7b510;
        }
        else {
          appuStack_78[0] = (undefined **)0x0;
        }
        uStack_58 = 0;
        local_4 = 0xc;
        FUN_00973410();
        local_4 = 0xffffffff;
        if ((appuStack_78[0] != (undefined **)0x0) && ((code *)*appuStack_78[0] != (code *)0x0)) {
          (*(code *)*appuStack_78[0])(apuStack_70,apuStack_70,1);
        }
        goto LAB_0046e610;
      }
    }
  }
  FUN_004154f0(param_3);
  FUN_00855dc0(param_3);
LAB_0046e610:
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

