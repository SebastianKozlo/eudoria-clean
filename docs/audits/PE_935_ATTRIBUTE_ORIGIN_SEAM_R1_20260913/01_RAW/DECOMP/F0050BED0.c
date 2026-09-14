
void FUN_0050bed0(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4)

{
  char cVar1;
  char cVar2;
  undefined4 uVar3;
  int iVar4;
  undefined4 uVar5;
  uint uVar6;
  allocator<char> *paVar7;
  undefined4 uVar8;
  undefined auStack_68 [2];
  char local_66;
  allocator<char> local_65;
  uint local_64;
  undefined4 local_60;
  uint local_5c;
  undefined4 local_58;
  undefined local_54 [44];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  abStack_28 [24];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009baf6a;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)auStack_68;
  ExceptionList = &local_c;
  local_58 = param_3;
  uVar3 = FUN_004123d0(DAT_00b9d8d0 ^ (uint)&stack0xffffff88);
  FUN_0085b840(uVar3);
  local_4 = 0;
  iVar4 = FUN_004123d0();
  local_4 = 0xffffffff;
  FUN_008e0110();
  if (iVar4 == 0) {
    uVar8 = 0;
    uVar5 = FUN_00843da0(0);
    FUN_00976770(uVar5,uVar8);
    cVar1 = FUN_009768d0(0x191);
    local_66 = '\0';
    uVar5 = FUN_00843dd0(&local_64);
    cVar2 = FUN_00728a40(uVar5);
    if (cVar2 != '\0') {
      local_66 = '\x01';
      cVar1 = '\0';
    }
    uVar6 = FUN_004123d0();
    if (0xf0000000 < uVar6) {
      cVar1 = '\0';
    }
    FUN_00730f60();
    FUN_00853a50(uVar3);
    local_60 = FUN_004123d0();
    local_64 = local_5c >> 0x10;
    FUN_00730fd0(&local_64);
    FUN_00730f90(param_2);
    FUN_00730fb0(local_58);
    uVar3 = FUN_00843da0();
    FUN_00797280(uVar3);
    paVar7 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_65);
    local_4 = 1;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (abStack_28,paVar7);
    local_4 = CONCAT31(local_4._1_3_,3);
    stlp_std::allocator<char>::~allocator<char>(&local_65);
    cVar1 = FUN_004c46c0(local_54,(cVar1 != '\0') + '\x01',abStack_28,param_4);
    if ((cVar1 != '\0') && (local_66 != '\0')) {
      uVar5 = 0;
      uVar3 = FUN_004123d0(0);
      FUN_004154f0(uVar3);
      FUN_008553d0(uVar3,uVar5);
    }
    local_4 = 0xffffffff;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (abStack_28);
  }
  ExceptionList = local_c;
  ___security_check_cookie_4();
  return;
}

