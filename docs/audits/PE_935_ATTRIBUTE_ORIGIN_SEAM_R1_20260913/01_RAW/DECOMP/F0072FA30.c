
void FUN_0072fa30(void)

{
  byte bVar1;
  byte bVar2;
  char cVar3;
  undefined4 uVar4;
  undefined4 *puVar5;
  undefined4 *local_150;
  undefined4 *local_14c;
  int local_148;
  void *local_144;
  undefined4 uStack_140;
  undefined4 uStack_13c;
  undefined4 uStack_138;
  byte bStack_133;
  undefined4 *puStack_128;
  undefined4 local_124;
  undefined4 local_120;
  undefined4 local_11c;
  undefined auStack_118 [48];
  undefined4 auStack_e8 [54];
  uint local_10;
  void *local_c;
  undefined *puStack_8;
  uint local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_00a12223;
  local_c = ExceptionList;
  local_10 = DAT_00b9d8d0 ^ (uint)&local_150;
  ExceptionList = &local_c;
  FUN_00972380(DAT_00b9d8d0 ^ (uint)&stack0xfffffea0);
  local_150 = (undefined4 *)0x0;
  local_14c = (undefined4 *)0x0;
  local_148 = 0;
  local_4._0_1_ = 1;
  local_4._1_3_ = 0;
  FUN_004023c0(&DAT_00b9ff44,FUN_00404c30);
  uVar4 = FUN_00401e70(&local_144,DAT_00b6c3d8,"Parameters\\templates.vfs");
  local_4._0_1_ = 2;
  local_124 = 1;
  local_120 = 0x80;
  local_11c = 8;
  bVar1 = FUN_00972df0(uVar4,&local_124,&local_150);
  bVar1 = bVar1 & 1;
  local_4 = CONCAT31(local_4._1_3_,1);
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)&local_144);
  puStack_128 = local_14c;
  puVar5 = local_150;
  do {
    if (puVar5 == puStack_128) {
LAB_0072fc69:
      local_4 = local_4 & 0xffffff00;
      if (local_150 != (undefined4 *)0x0) {
        stlp_std::__node_alloc::deallocate(local_150,(local_148 - (int)local_150 >> 2) * 4);
      }
      local_4 = 0xffffffff;
      FUN_00972050();
      ExceptionList = local_c;
      ___security_check_cookie_4();
      return;
    }
    uVar4 = *puVar5;
    uStack_13c = 0;
    uStack_138 = 0;
    FUN_0040e160(0x80,1);
    uStack_140 = 0x80;
    local_144 = operator_new(0x80);
    bStack_133 = 1;
    local_4._0_1_ = 3;
    bVar2 = FUN_00971ad0(uVar4,&local_144,&DAT_00ba57ec);
    if ((bVar1 & bVar2) == 0) {
LAB_0072fc42:
      local_4 = CONCAT31(local_4._1_3_,1);
      cVar3 = FUN_0040e180(0x80);
      if (cVar3 != '\0') {
        operator_delete__(local_144);
      }
      goto LAB_0072fc69;
    }
    FUN_00730700();
    local_4._0_1_ = 4;
    FUN_00730c90(&local_144,auStack_118);
    bVar1 = bVar1 & bVar2 & bStack_133;
    auStack_e8[0] = FUN_004123d0();
    FUN_005670a0(auStack_118);
    local_4._0_1_ = 5;
    FUN_0072f8d0(&local_124,auStack_e8);
    local_4._0_1_ = 4;
    FUN_00730730();
    local_4._0_1_ = 3;
    FUN_00730730();
    if (bVar1 == 0) goto LAB_0072fc42;
    local_4 = CONCAT31(local_4._1_3_,1);
    cVar3 = FUN_0040e180(0x80);
    if (cVar3 != '\0') {
      operator_delete__(local_144);
    }
    puVar5 = puVar5 + 1;
  } while( true );
}

