
basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *
FUN_0085b120(basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
             *param_1)

{
  allocator<char> *paVar1;
  allocator<char> local_11;
  undefined4 local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 uStack_4;
  
  uStack_4 = 0xffffffff;
  puStack_8 = &LAB_00a29eb9;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  local_10 = 0;
  paVar1 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_11);
  uStack_4 = 0;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            (param_1,"",paVar1);
  stlp_std::allocator<char>::~allocator<char>(&local_11);
  ExceptionList = local_c;
  return param_1;
}

