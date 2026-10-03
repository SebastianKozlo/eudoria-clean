// H04_singleton_init_00821fb0 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G5_LOOKUP_CLOSURE.json

void __fastcall FUN_00821fb0(int param_1)

{
  char cVar1;
  undefined4 uVar2;
  int iVar3;
  undefined auStack_ec [3];
  char local_e9;
  void *local_e8;
  undefined4 uStack_e4;
  undefined4 uStack_e0;
  undefined4 uStack_dc;
  char cStack_d7;
  void *local_d0;
  undefined4 local_cc;
  int local_c8;
  undefined4 local_c4;
  undefined4 local_c0;
  undefined4 local_bc;
  undefined auStack_b8 [168];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a2312d;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_ec;
  ExceptionList = &local_c;
  FUN_00972380(DAT_00b9d8d0 ^ (uint)&stack0xffffff0c);
  local_c4 = 1;
  local_c0 = 0x80;
  local_bc = 8;
  local_d0 = (void *)0x0;
  local_cc = 0;
  local_c8 = 0;
  local_4._0_1_ = 1;
  local_4._1_3_ = 0;
  FUN_004023c0(&DAT_00b9ff44,FUN_00404c30);
  uVar2 = FUN_00401e70(&local_e8,DAT_00b6c3d8,"parameters\\sids.vfs");
  local_4._0_1_ = 2;
  local_e9 = FUN_00972df0(uVar2,&local_c4,&local_d0);
  local_4._0_1_ = 1;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)&local_e8);
  if (local_e9 != '\0') {
    uStack_e0 = 0;
    uStack_dc = 0;
    FUN_0040e160(0x80,1);
    uStack_e4 = 0x80;
    local_e8 = operator_new(0x80);
    cStack_d7 = '\x01';
    local_4 = CONCAT31(local_4._1_3_,3);
    cVar1 = FUN_00971ad0(1,&local_e8,auStack_b8);
    if (cVar1 == '\0') {
      local_e9 = '\0';
    }
    else {
      iVar3 = param_1 + 4;
      if (*(int *)(param_1 + 0x14) != 0) {
        FUN_008c3580(*(undefined4 *)(param_1 + 8));
        *(int *)(param_1 + 0xc) = iVar3;
        *(undefined4 *)(param_1 + 8) = 0;
        *(int *)(param_1 + 0x10) = iVar3;
        *(undefined4 *)(param_1 + 0x14) = 0;
      }
      FUN_00821e70(iVar3);
      local_e9 = cStack_d7;
    }
    FUN_00971cd0();
    local_4._0_1_ = 1;
    cVar1 = FUN_0040e180(0x80);
    if (cVar1 != '\0') {
      operator_delete__(local_e8);
    }
  }
  local_4 = (uint)local_4._1_3_ << 8;
  if (local_d0 != (void *)0x0) {
    stlp_std::__node_alloc::deallocate(local_d0,(local_c8 - (int)local_d0 >> 2) * 4);
  }
  local_4 = 0xffffffff;
  FUN_00972050();
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

