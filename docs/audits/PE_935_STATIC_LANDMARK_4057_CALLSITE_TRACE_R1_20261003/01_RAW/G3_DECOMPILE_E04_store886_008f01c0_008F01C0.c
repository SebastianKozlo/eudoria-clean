// E04_store886_008f01c0 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G3_FALSIFIER_PATH.json

void FUN_008f01c0(basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *param_1)

{
  int iVar1;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbVar2;
  bool bVar3;
  int *piVar4;
  type_info *this;
  int *piVar5;
  allocator<char> *paVar6;
  undefined4 uVar7;
  undefined4 uVar8;
  undefined4 uVar9;
  TypeDescriptor *pTVar10;
  undefined4 uVar11;
  int iStack_30;
  int iStack_2c;
  int iStack_28;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_24 [24];
  void *local_c;
  undefined *puStack_8;
  int iStack_4;
  
  iStack_4 = 0xffffffff;
  puStack_8 = &LAB_00a3db62;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  piVar4 = (int *)FUN_008df1e0(DAT_00b9d8d0 ^ (uint)&stack0xffffffc8);
  if (piVar4 != (int *)0x0) {
    pTVar10 = &ArkUITextField::RTTI_Type_Descriptor;
    this = (type_info *)(**(code **)(*piVar4 + 100))();
    bVar3 = type_info::operator!=(this,(type_info *)pTVar10);
    if (!bVar3) {
      FUN_008df2d0(&iStack_2c,1);
      iVar1 = piVar4[0x65];
      if ((iStack_2c < iVar1) || (iStack_28 < iVar1)) {
        iStack_30 = iVar1;
        piVar5 = &iStack_2c;
        if (iStack_2c <= iVar1) {
          piVar5 = &iStack_30;
        }
        iStack_2c = *piVar5;
        iStack_30 = piVar4[0x65];
        piVar5 = &iStack_28;
        if (iStack_28 <= piVar4[0x65]) {
          piVar5 = &iStack_30;
        }
        iStack_28 = *piVar5;
        FUN_008df310(&iStack_2c,1);
      }
      FUN_008eccf0();
      pbVar2 = param_1;
      bVar3 = stlp_std::
              basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              ::empty(param_1);
      if (!bVar3) {
        paVar6 = (allocator<char> *)
                 stlp_std::allocator<char>::allocator<char>((allocator<char> *)&param_1);
        iStack_4 = 0;
        uVar7 = stlp_std::
                basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ::
                basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                          (abStack_24,paVar6);
        uVar11 = 0xe;
        uVar9 = 0;
        iStack_4._0_1_ = 1;
        uVar8 = FUN_00719f70(0xff,0xff,0xff,0xff);
        FUN_008ecb60(pbVar2,0,0,uVar8,uVar7,uVar9,uVar11);
        iStack_4 = (uint)iStack_4._1_3_ << 8;
        stlp_std::
        basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
        ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  (abStack_24);
        stlp_std::allocator<char>::~allocator<char>((allocator<char> *)&param_1);
      }
    }
  }
  ExceptionList = local_c;
  return;
}

