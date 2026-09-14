
undefined4 * __thiscall
FUN_0050a690(undefined4 *param_1_00,undefined4 param_1,
            basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            *param_2)

{
  uint uVar1;
  undefined4 uVar2;
  void *local_c;
  undefined *puStack_8;
  undefined4 uStack_4;
  
  uStack_4 = 0xffffffff;
  puStack_8 = &LAB_009baccc;
  local_c = ExceptionList;
  uVar1 = DAT_00b9d8d0 ^ (uint)&stack0xffffffec;
  ExceptionList = &local_c;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)(param_1_00 + 1),param_2);
  uStack_4 = 0;
  uVar2 = FUN_005091c0(param_1,uVar1);
  *param_1_00 = uVar2;
  ExceptionList = local_c;
  return param_1_00;
}

