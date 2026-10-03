// F01_id_to_string_00821760 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G4_TERMINAL_CONSUMER.json

undefined4
FUN_00821760(undefined4 param_1,undefined4 param_2,
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            *param_3)

{
  uint uVar1;
  allocator<char> *paVar2;
  int iVar3;
  undefined4 *puVar4;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbVar5;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbVar6;
  undefined4 uVar7;
  allocator<char> aStack_5e;
  allocator<char> local_5d;
  undefined4 uStack_5c;
  undefined4 uStack_58;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_54 [24];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_3c [24];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_24 [24];
  void *local_c;
  undefined *puStack_8;
  int iStack_4;
  
  iStack_4 = 0xffffffff;
  puStack_8 = &LAB_00a22ec6;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&stack0xffffff98;
  ExceptionList = &local_c;
  paVar2 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_5d);
  iStack_4 = 0;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_3c,"",paVar2);
  paVar2 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&aStack_5e);
  iStack_4._0_1_ = 2;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_54,"",paVar2);
  iStack_4._0_1_ = 3;
  uStack_5c = FUN_00826a50(param_1,uVar1);
  uVar7 = 1;
  pbVar6 = abStack_3c;
  pbVar5 = abStack_54;
  uStack_58 = param_2;
  puVar4 = &uStack_5c;
  FUN_00415670(puVar4,pbVar5,pbVar6,1);
  iVar3 = FUN_00823c10(puVar4,pbVar5,pbVar6,uVar7);
  iStack_4._0_1_ = 2;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(abStack_54)
  ;
  stlp_std::allocator<char>::~allocator<char>(&aStack_5e);
  iStack_4 = (uint)iStack_4._1_3_ << 8;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(abStack_3c)
  ;
  iStack_4 = 0xffffffff;
  stlp_std::allocator<char>::~allocator<char>(&local_5d);
  if (iVar3 != 0) {
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::operator=(param_3,(basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                         *)(iVar3 + 0x10));
    paVar2 = (allocator<char> *)
             stlp_std::allocator<char>::allocator<char>((allocator<char> *)&param_1);
    iStack_4 = 4;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (abStack_24,"",paVar2);
    iStack_4._0_1_ = 5;
    FUN_008268a0(abStack_24);
    iStack_4 = CONCAT31(iStack_4._1_3_,4);
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (abStack_24);
    stlp_std::allocator<char>::~allocator<char>((allocator<char> *)&param_1);
    ExceptionList = local_c;
    return 1;
  }
  ExceptionList = local_c;
  return 0;
}

