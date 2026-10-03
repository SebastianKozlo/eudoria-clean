// D02_consumer886_008f0780 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G2_CALLEE_DEEPDIVE.json

void FUN_008f0780(undefined4 param_1)

{
  undefined4 uVar1;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbVar2;
  undefined4 *puVar3;
  undefined4 local_30;
  undefined4 local_2c;
  undefined4 local_28;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  local_24 [24];
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  puStack_8 = &LAB_00a3dbf1;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  local_30 = 0;
  local_2c = 0;
  local_28 = 0;
  puVar3 = &local_30;
  pbVar2 = local_24;
  local_4 = 0;
  FUN_00414170(pbVar2,param_1,puVar3,DAT_00b9d8d0 ^ (uint)&stack0xffffffc8);
  uVar1 = FUN_00821bb0(pbVar2,param_1,puVar3);
  local_4._0_1_ = 1;
  FUN_008f01c0(uVar1);
  local_4 = (uint)local_4._1_3_ << 8;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>(local_24);
  local_4 = 0xffffffff;
  FUN_00426620();
  ExceptionList = local_c;
  return;
}

