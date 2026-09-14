
char __thiscall FUN_004c47f0(undefined4 *param_1_00,undefined4 param_1)

{
  bool bVar1;
  char cVar2;
  char cVar3;
  int *piVar4;
  int iVar5;
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_> *pbVar6;
  undefined4 uVar7;
  undefined4 local_b0;
  int local_ac [12];
  undefined2 local_7c;
  undefined local_78 [12];
  undefined local_6c [12];
  undefined4 local_60;
  undefined4 local_58;
  undefined local_50 [44];
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
  local_24 [24];
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009afc24;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  FUN_00745360(DAT_00b9d8d0 ^ (uint)&stack0xffffff44);
  local_4 = 0;
  cVar2 = FUN_007453d0(param_1);
  if (cVar2 == '\0') goto LAB_004c49d2;
  uVar7 = local_b0;
  FUN_004154f0(local_b0);
  piVar4 = (int *)FUN_008544d0(uVar7);
  *param_1_00 = piVar4;
  if (piVar4 == (int *)0x0) {
    FUN_00730f60();
    FUN_00853a50(local_b0);
    FUN_00730f90(local_78);
    FUN_00730fb0(local_6c);
    FUN_00730fd0(local_ac);
    FUN_00797280(local_60);
    pbVar6 = local_24;
    FUN_004c4640(pbVar6,local_60);
    uVar7 = FUN_00765930(pbVar6,local_60);
    local_4._0_1_ = 1;
    cVar3 = FUN_004c46c0(local_50,local_7c,uVar7,1);
    local_4 = (uint)local_4._1_3_ << 8;
    stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
    ::~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              (local_24);
    if (cVar3 == '\0') goto LAB_004c49d2;
    uVar7 = local_b0;
    FUN_004154f0(local_b0);
    piVar4 = (int *)FUN_008544d0(uVar7);
    *param_1_00 = piVar4;
    if (((local_ac[0] == 0x4e34) || (local_ac[0] == 0x4e38)) || (local_ac[0] == 0x5dc9)) {
      bVar1 = true;
    }
    else {
      bVar1 = false;
    }
    (**(code **)(*piVar4 + 0x14))(local_58);
    if (!bVar1) goto LAB_004c49d2;
  }
  else {
    (**(code **)(*piVar4 + 0x14))(local_58);
    cVar3 = FUN_0085b750();
    if (cVar3 != '\0') {
      FUN_0085b3e0(local_78,1);
      FUN_0085adb0(local_6c);
    }
    iVar5 = FUN_006b22d0();
    if ((iVar5 != 0) ||
       (((local_ac[0] != 0x4e34 && (local_ac[0] != 0x4e38)) && (local_ac[0] != 0x5dc9))))
    goto LAB_004c49d2;
  }
  uVar7 = 0;
  FUN_004154f0(local_b0,0);
  FUN_008553d0(local_b0,uVar7);
LAB_004c49d2:
  local_4 = 0xffffffff;
  FUN_008e0110();
  ExceptionList = local_c;
  return cVar2;
}

