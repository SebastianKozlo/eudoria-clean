// source: C7_LISTS_AND_ATTACH.json :: Z01_list1_init_00730b70

void __thiscall FUN_00730b70(int *param_1_00,int *param_1)

{
  int iVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  undefined auStack_34 [3];
  undefined local_31;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  local_30 [32];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a124a8;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_34;
  uVar2 = DAT_00b9d8d0 ^ (uint)&stack0xffffffbc;
  ExceptionList = &local_c;
  if (*param_1 != param_1[1]) {
    FUN_00730020(*param_1,param_1[1],&local_31);
  }
  uVar3 = 0;
  if ((*(char *)((int)param_1_00 + 0x11) == '\0') || ((uint)param_1_00[2] < param_1_00[3] + 2U)) {
    uVar4 = 0;
    if (*(char *)((int)param_1_00 + 0x11) != '\0') {
      *(undefined *)((int)param_1_00 + 0x11) = 0;
    }
  }
  else {
    uVar4 = (uint)*(ushort *)(param_1_00[3] + *param_1_00);
    FUN_0040de60(2);
  }
  if (uVar4 != 0) {
    do {
      if (*(char *)((int)param_1_00 + 0x11) == '\0') break;
      FUN_00730de0(uVar2);
      local_4 = 0;
      FUN_00730ed0(param_1_00,local_30);
      iVar1 = param_1[1];
      if (iVar1 == param_1[2]) {
        FUN_007307a0(iVar1,local_30,&local_31,1,1);
      }
      else {
        FUN_0072fd40(iVar1,local_30);
        param_1[1] = param_1[1] + 0x20;
      }
      local_4 = 0xffffffff;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                (local_30);
      uVar3 = uVar3 + 1;
    } while (uVar3 < uVar4);
  }
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

