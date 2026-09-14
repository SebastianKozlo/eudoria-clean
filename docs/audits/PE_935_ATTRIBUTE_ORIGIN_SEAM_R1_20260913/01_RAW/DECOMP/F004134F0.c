
LPCRITICAL_SECTION __fastcall FUN_004134f0(LPCRITICAL_SECTION param_1)

{
  uint uVar1;
  allocator<char> *paVar2;
  allocator<char> local_25;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_24 [24];
  void *local_c;
  undefined *puStack_8;
  int iStack_4;
  
  iStack_4 = 0xffffffff;
  puStack_8 = &LAB_00995b12;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&stack0xffffffd4;
  ExceptionList = &local_c;
  paVar2 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_25);
  iStack_4 = 0;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_24,"",paVar2);
  iStack_4._0_1_ = 1;
  if (DAT_00ba1200 == '\0') {
    FUN_00413460(uVar1);
  }
  InitializeCriticalSection(param_1);
  param_1[1].LockCount = 0x1fe319ba;
  *(undefined *)&param_1[1].DebugInfo = 0;
  iStack_4 = (uint)iStack_4._1_3_ << 8;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(abStack_24)
  ;
  stlp_std::allocator<char>::~allocator<char>(&local_25);
  ExceptionList = local_c;
  return param_1;
}

