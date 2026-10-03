// E02_on_ret_00821bb0 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G3_FALSIFIER_PATH.json

void FUN_00821bb0(basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *param_1,undefined4 param_2)

{
  char cVar1;
  allocator<char> *paVar2;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_64 [12];
  undefined4 uStack_58;
  undefined4 uStack_54;
  undefined4 uStack_50;
  undefined auStack_38 [3];
  allocator<char> local_35;
  undefined4 local_34;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *local_30;
  undefined *puStack_2c;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_28 [24];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  uint uStack_4;
  
  uStack_4 = 0xffffffff;
  puStack_8 = &LAB_00a2303c;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_38;
  ExceptionList = &local_c;
  local_30 = param_1;
  local_34 = 0;
  paVar2 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_35);
  uStack_4 = 1;
  uStack_50 = 0x821c14;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (abStack_28,paVar2);
  uStack_4 = CONCAT31(uStack_4._1_3_,3);
  stlp_std::allocator<char>::~allocator<char>(&local_35);
  uStack_50 = param_2;
  uStack_54 = 0;
  uStack_58 = 0x821c36;
  cVar1 = FUN_00821760();
  if (cVar1 == '\0') {
    uStack_50 = 0x821c47;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (param_1,(basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                        *)&DAT_00ba8218);
  }
  else {
    puStack_2c = abStack_64;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (abStack_64,abStack_28);
    FUN_0082a2d0(param_1);
  }
  local_34 = 1;
  uStack_4 = uStack_4 & 0xffffff00;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(abStack_28)
  ;
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

