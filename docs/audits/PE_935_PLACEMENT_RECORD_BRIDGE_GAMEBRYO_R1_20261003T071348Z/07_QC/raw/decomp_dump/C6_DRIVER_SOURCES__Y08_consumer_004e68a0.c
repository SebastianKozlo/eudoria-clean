// source: C6_DRIVER_SOURCES.json :: Y08_consumer_004e68a0

void FUN_004e68a0(void)

{
  bool bVar1;
  char cVar2;
  int *piVar3;
  type_info *this;
  undefined4 uVar4;
  int *piVar5;
  int iVar6;
  int *piVar7;
  TypeDescriptor *pTVar8;
  int iStack_dc;
  int iStack_cc;
  int iStack_c8;
  undefined auStack_c4 [12];
  undefined auStack_b8 [44];
  undefined **ppuStack_8c;
  undefined auStack_38 [44];
  void *local_c;
  undefined *puStack_8;
  int iStack_4;
  
  iStack_4 = 0xffffffff;
  puStack_8 = &LAB_009b4d9c;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  piVar3 = (int *)FUN_008df1e0(DAT_00b9d8d0 ^ (uint)&stack0xffffff0c);
  iVar6 = 0;
  if (piVar3 != (int *)0x0) {
    pTVar8 = &ArkColoringUI_Impl::RTTI_Type_Descriptor;
    this = (type_info *)(**(code **)(*piVar3 + 100))();
    bVar1 = type_info::operator!=(this,(type_info *)pTVar8);
    if (!bVar1) {
      iStack_dc = 0;
      if (piVar3[0x9a] != 0) {
        FUN_00843d60(piVar3[0x9a]);
        iStack_4 = 0;
        uVar4 = FUN_004e4a40(auStack_b8);
        iStack_4._0_1_ = 1;
        cVar2 = FUN_008493f0(auStack_c4,uVar4,&DAT_00ba27e0);
        iStack_4 = (uint)iStack_4._1_3_ << 8;
        FUN_00745840();
        if (cVar2 != '\0') {
          uVar4 = FUN_00844660();
          FUN_0043a550(uVar4);
          FUN_0072f580(uVar4);
          cVar2 = FUN_0072fce0();
          if (cVar2 != '\0') {
            iStack_dc = FUN_007ad080();
          }
        }
        iStack_4 = 0xffffffff;
        FUN_008e0110();
      }
      piVar5 = piVar3 + 0xa8;
      piVar7 = piVar3 + 0xa2;
      do {
        iStack_c8 = piVar7[1];
        iStack_cc = *piVar7;
        bVar1 = iVar6 < iStack_dc;
        FUN_008df860(0x406);
        ppuStack_8c = ArkUI::WindowImpl<class_ArkUIWindow>::vftable;
        iStack_4 = 2;
        uVar4 = FUN_008dfae0(auStack_38,(-0x293 - (int)piVar3) + (int)piVar5);
        iStack_4._0_1_ = 3;
        FUN_009119b0(uVar4);
        iStack_4._0_1_ = 5;
        FUN_008df670();
        iStack_4._0_1_ = 6;
        FUN_008df670();
        FUN_008df430(!bVar1);
        FUN_004fca20(bVar1);
        *(bool *)piVar5 = bVar1;
        if (!bVar1) {
          FUN_004c3580(&iStack_cc);
          iStack_4._0_1_ = 7;
          FUN_004c3ed0();
          iStack_4._0_1_ = 6;
          FUN_004c43e0();
        }
        FUN_004e5e70(iVar6);
        iStack_4 = 0xffffffff;
        FUN_008df670();
        iVar6 = iVar6 + 1;
        piVar7 = piVar7 + 2;
        piVar5 = (int *)((int)piVar5 + 1);
      } while (iVar6 < 3);
    }
  }
  ExceptionList = local_c;
  return;
}

