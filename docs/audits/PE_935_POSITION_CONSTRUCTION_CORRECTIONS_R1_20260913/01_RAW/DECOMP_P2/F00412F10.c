// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x412f10L (requested via site 0x412f10)

basic_ostream<char,class_stlp_std::char_traits<char>_> * __thiscall
FUN_00412f10(ushort *param_1_00,basic_ostream<char,class_stlp_std::char_traits<char>_> *param_1,
            int param_3)

{
  ushort uVar1;
  basic_ostream<char,class_stlp_std::char_traits<char>_> *pbVar2;
  uint uVar3;
  undefined4 uVar4;
  ios_base *piVar5;
  uint uVar6;
  code *pcVar7;
  undefined4 unaff_ESI;
  undefined4 unaff_EDI;
  undefined *puVar8;
  code *pcVar9;
  code **ppcVar10;
  undefined *puVar11;
  code **ppcVar12;
  code *apcStack_20 [2];
  undefined4 uStack_18;
  undefined4 uStack_14;
  code *pcStack_10;
  int *piStack_c;
  undefined4 uStack_8;
  int *piStack_4;
  
  if (*(char *)(param_1_00 + 8) == '\0') {
    stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::_M_put_nowiden(param_1,"");
    return param_1;
  }
  param_1[*(int *)(*(int *)param_1 + 4) + 0x70] =
       (basic_ostream<char,class_stlp_std::char_traits<char>_>)0x30;
  stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::operator<<(param_1,FUN_0040e6c0)
  ;
  pcVar7 = _M_put_nowiden_exref;
  pcVar9 = operator<<_exref;
  if (param_3 == 5) {
    puVar8 = (undefined *)(uint)param_1_00[1];
    pbVar2 = stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::operator<<
                       (param_1,(uint)*param_1_00);
    stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::_M_put_nowiden(pbVar2,"-");
    pcVar7 = pcVar9;
    if (pbVar2 == (basic_ostream<char,class_stlp_std::char_traits<char>_> *)0x0) {
      stlp_std::ios_base::width((ios_base *)0x0,2);
    }
    else {
      stlp_std::ios_base::width((ios_base *)(pbVar2 + *(int *)(*(int *)pbVar2 + 4)),2);
    }
  }
  else {
    if (param_3 == 6) {
      uVar3 = (uint)param_1_00[3];
      apcStack_20[0] = width_exref;
      uStack_18 = 2;
      uStack_14 = 0;
      pbVar2 = (basic_ostream<char,class_stlp_std::char_traits<char>_> *)
               FUN_004072d0(param_1,&DAT_00ba10e0 + (uint)param_1_00[1] * 0x18);
      pcVar7 = _M_put_nowiden_exref;
      stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::_M_put_nowiden(pbVar2," ");
      pbVar2[*(int *)(*(int *)pbVar2 + 4) + 0x70] =
           (basic_ostream<char,class_stlp_std::char_traits<char>_>)0x20;
      pbVar2 = (basic_ostream<char,class_stlp_std::char_traits<char>_> *)
               FUN_0040c020(pbVar2,apcStack_20);
      pcVar9 = operator<<_exref;
      pbVar2 = stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::operator<<
                         (pbVar2,uVar3);
      stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::_M_put_nowiden(pbVar2," ");
      pbVar2[*(int *)(*(int *)pbVar2 + 4) + 0x70] =
           (basic_ostream<char,class_stlp_std::char_traits<char>_>)0x30;
LAB_0041302f:
      uVar1 = param_1_00[4];
      stlp_std::ios_base::width((ios_base *)(param_1 + *(int *)(*(int *)param_1 + 4)),2);
      (*pcVar9)(uVar1);
      (*pcVar7)(&DAT_00a79d58);
      if (piStack_4 == (int *)0x0) {
        piVar5 = (ios_base *)0x0;
      }
      else {
        piVar5 = (ios_base *)(*(int *)(*piStack_4 + 4) + (int)piStack_4);
      }
      stlp_std::ios_base::width(piVar5,2);
      uStack_8 = (*pcVar9)(unaff_ESI);
      (*pcVar7)(&DAT_00a79d58);
      if (piStack_c == (int *)0x0) {
        piVar5 = (ios_base *)0x0;
      }
      else {
        piVar5 = (ios_base *)(*(int *)(*piStack_c + 4) + (int)piStack_c);
      }
      stlp_std::ios_base::width(piVar5,2);
      (*pcVar9)(unaff_EDI);
    }
    else {
      if ((((param_3 == 3) || (param_3 == 2)) || (param_3 == 4)) || (param_3 == 9)) {
        uVar3 = (uint)param_1_00[3];
        apcStack_20[0] = width_exref;
        uVar6 = (uint)param_1_00[1];
        uStack_14 = 0;
        piStack_4 = (int *)0x0;
        uStack_18 = 2;
        uStack_8 = 2;
        pcStack_10 = width_exref;
        pbVar2 = stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::operator<<
                           (param_1,(uint)*param_1_00);
        stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::_M_put_nowiden(pbVar2,"-")
        ;
        pbVar2 = (basic_ostream<char,class_stlp_std::char_traits<char>_> *)
                 FUN_0040c020(pbVar2,&pcStack_10);
        pbVar2 = stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::operator<<
                           (pbVar2,uVar6);
        stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::_M_put_nowiden(pbVar2,"-")
        ;
        ppcVar12 = apcStack_20;
LAB_004131bf:
        pbVar2 = (basic_ostream<char,class_stlp_std::char_traits<char>_> *)
                 FUN_0040c020(pbVar2,ppcVar12);
        stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::operator<<(pbVar2,uVar3);
      }
      else if ((param_3 == 7) || (param_3 == 8)) {
        uVar3 = (uint)param_1_00[3];
        uVar6 = (uint)param_1_00[1];
        ppcVar12 = apcStack_20;
        puVar11 = &DAT_00a79704;
        ppcVar10 = &pcStack_10;
        apcStack_20[0] = width_exref;
        pcStack_10 = width_exref;
        puVar8 = &DAT_00a79704;
        uStack_18 = 2;
        uStack_14 = 0;
        uStack_8 = 2;
        piStack_4 = (int *)0x0;
        pbVar2 = stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::operator<<
                           (param_1,(uint)*param_1_00);
        uVar4 = FUN_00401d60(pbVar2,puVar8,ppcVar10,uVar6,puVar11,ppcVar12);
        pbVar2 = (basic_ostream<char,class_stlp_std::char_traits<char>_> *)FUN_0040c020(uVar4);
        pbVar2 = stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::operator<<
                           (pbVar2,uVar6);
        pbVar2 = (basic_ostream<char,class_stlp_std::char_traits<char>_> *)FUN_00401d60(pbVar2);
        goto LAB_004131bf;
      }
      if (((param_3 == 3) || (param_3 == 4)) || (param_3 == 8)) {
        stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::_M_put_nowiden
                  (param_1," ");
      }
      else if (param_3 == 9) {
        FUN_00401d60(param_1,&DAT_00a79de4);
        goto LAB_0041302f;
      }
      if ((((param_3 == 3) || (param_3 == 1)) || (param_3 == 4)) || (param_3 == 9))
      goto LAB_0041302f;
      if (param_3 == 8) {
        uVar3 = (uint)param_1_00[5];
        piStack_4 = (int *)0x0;
        uStack_14 = 0;
        pcStack_10 = width_exref;
        uVar6 = (uint)param_1_00[4];
        uStack_8 = 2;
        apcStack_20[0] = width_exref;
        uStack_18 = 2;
        pbVar2 = (basic_ostream<char,class_stlp_std::char_traits<char>_> *)
                 FUN_0040c020(param_1,apcStack_20,uVar6,&DAT_00a79d58,&pcStack_10);
        pbVar2 = stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::operator<<
                           (pbVar2,uVar6);
        uVar4 = FUN_00401d60(pbVar2);
        pbVar2 = (basic_ostream<char,class_stlp_std::char_traits<char>_> *)FUN_0040c020(uVar4);
        stlp_std::basic_ostream<char,class_stlp_std::char_traits<char>_>::operator<<(pbVar2,uVar3);
        goto LAB_0041332d;
      }
    }
    if (param_3 == 4) {
      uVar1 = param_1_00[7];
      (*pcVar7)(&DAT_00a79704);
      stlp_std::ios_base::width((ios_base *)(param_1 + *(int *)(*(int *)param_1 + 4)),3);
      (*pcVar9)(uVar1);
      goto LAB_0041332d;
    }
    if (param_3 != 9) goto LAB_0041332d;
    puVar8 = &DAT_00a79e50;
  }
  (*pcVar7)(puVar8);
LAB_0041332d:
  param_1[*(int *)(*(int *)param_1 + 4) + 0x70] =
       (basic_ostream<char,class_stlp_std::char_traits<char>_>)0x20;
  return param_1;
}

