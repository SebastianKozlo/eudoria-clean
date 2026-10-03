// I01_sids_parser_00821e70 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G6_SIDS_PARSER.json

void __thiscall FUN_00821e70(int *param_1_00,int param_1)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  undefined local_34 [8];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  local_2c [24];
  undefined4 local_14;
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a230d8;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)local_34;
  uVar1 = DAT_00b9d8d0 ^ (uint)&stack0xffffffbc;
  ExceptionList = &local_c;
  uVar2 = 0;
  if (*(int *)(param_1 + 0x10) != 0) {
    FUN_008c3580(*(undefined4 *)(param_1 + 4));
    *(int *)(param_1 + 8) = param_1;
    *(undefined4 *)(param_1 + 4) = 0;
    *(int *)(param_1 + 0xc) = param_1;
    *(undefined4 *)(param_1 + 0x10) = 0;
  }
  if ((*(char *)((int)param_1_00 + 0x11) == '\0') || ((uint)param_1_00[2] < param_1_00[3] + 2U)) {
    uVar3 = 0;
    if (*(char *)((int)param_1_00 + 0x11) != '\0') {
      *(undefined *)((int)param_1_00 + 0x11) = 0;
    }
  }
  else {
    uVar3 = (uint)*(ushort *)(param_1_00[3] + *param_1_00);
    FUN_0040de60(2);
  }
  if (uVar3 != 0) {
    do {
      if (*(char *)((int)param_1_00 + 0x11) == '\0') break;
      FUN_008216f0(uVar1);
      local_4 = 0;
      FUN_0040e020(local_2c);
      if ((*(char *)((int)param_1_00 + 0x11) == '\0') || ((uint)param_1_00[2] < param_1_00[3] + 4U))
      {
        local_14 = 0;
        if (*(char *)((int)param_1_00 + 0x11) != '\0') {
          *(undefined *)((int)param_1_00 + 0x11) = 0;
        }
      }
      else {
        local_14 = *(undefined4 *)(param_1_00[3] + *param_1_00);
        FUN_0040de60(4);
      }
      FUN_00413da0(local_34,local_2c);
      local_4 = 0xffffffff;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                (local_2c);
      uVar2 = uVar2 + 1;
    } while (uVar2 < uVar3);
  }
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

