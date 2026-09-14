
int FUN_006cb6f0(int param_1,int param_2)

{
  int iVar1;
  int iVar2;
  allocator<char> *paVar3;
  undefined4 uVar4;
  allocator<char> local_41;
  void *local_40;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_3c [24];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_24 [24];
  void *local_c;
  undefined *puStack_8;
  int iStack_4;
  
  uVar4 = param_2;
  iVar1 = param_1;
  iStack_4 = 0xffffffff;
  puStack_8 = &LAB_00a05bef;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  FUN_00971780(&local_40,&param_1);
  if (local_40 == (void *)0x0) {
    iVar2 = FUN_006cb370(iVar1);
    if (iVar2 == 0) {
      paVar3 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_41);
      iStack_4 = iVar2;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                (abStack_24,"",paVar3);
      paVar3 = (allocator<char> *)
               stlp_std::allocator<char>::allocator<char>((allocator<char> *)&param_1);
      iStack_4._0_1_ = 2;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                (abStack_3c,"",paVar3);
      iStack_4._0_1_ = 3;
      iVar1 = FUN_006c9700(iVar1,abStack_3c,abStack_24,0);
      iStack_4._0_1_ = 2;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                (abStack_3c);
      stlp_std::allocator<char>::~allocator<char>((allocator<char> *)&param_1);
      iStack_4 = (uint)iStack_4._1_3_ << 8;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                (abStack_24);
      iStack_4 = 0xffffffff;
      stlp_std::allocator<char>::~allocator<char>(&local_41);
      if (iVar1 == 0) goto LAB_006cb768;
      local_40 = operator_new(0xc);
      iStack_4 = 4;
      if (local_40 == (void *)0x0) {
        iVar2 = 0;
      }
      else {
        iVar2 = FUN_006fa8b0(iVar1);
      }
      iStack_4 = 0xffffffff;
      uVar4 = param_2;
    }
    iVar1 = FUN_006cb020(iVar2,uVar4,0);
    if (iVar1 != 0) {
      FUN_006f33a0(iVar2,iVar1);
    }
  }
  else {
    param_2 = iVar1;
    FUN_00971780(&param_1,&param_2);
    if (param_1 != 0) {
      ExceptionList = local_c;
      return *(int *)(*(int *)(param_1 + 8) + 8);
    }
LAB_006cb768:
    iVar1 = 0;
  }
  ExceptionList = local_c;
  return iVar1;
}

