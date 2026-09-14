
undefined4 __fastcall FUN_004b3a00(int param_1)

{
  char cVar1;
  undefined4 uVar2;
  int iVar3;
  allocator<char> *paVar4;
  bool bVar5;
  allocator<char> local_91 [9];
  undefined local_88 [12];
  undefined4 local_7c;
  undefined4 local_78;
  undefined uStack_74;
  undefined uStack_73;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 *apuStack_58 [2];
  undefined auStack_50 [24];
  undefined local_38 [44];
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009ad066;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  if (*(int *)(param_1 + 4) != 0) {
    FUN_00843d40(DAT_00b9d8d0 ^ (uint)&stack0xffffff5c);
    local_4 = 0;
    uVar2 = FUN_00843d60(*(undefined4 *)(param_1 + 4));
    local_4._0_1_ = 1;
    FUN_004c5c70(uVar2,local_88);
    local_4._0_1_ = 0;
    FUN_008e0110();
    uVar2 = FUN_004123d0();
    local_64 = 0;
    local_60 = 0;
    *(undefined4 *)(param_1 + 8) = uVar2;
    local_5c = 0;
    FUN_0055b300();
    local_4._0_1_ = 2;
    iVar3 = FUN_004123d0();
    if (iVar3 != 0) {
      iVar3 = FUN_004123d0();
      local_64 = *(undefined4 *)(iVar3 + 0x44);
      local_60 = *(undefined4 *)(iVar3 + 0x48);
      local_5c = *(undefined4 *)(iVar3 + 0x4c);
      *(undefined4 *)(param_1 + 0x48) = 0;
      *(undefined4 *)(param_1 + 0x4c) = 0;
      *(undefined4 *)(param_1 + 0x50) = 0x3f800000;
      FUN_00730f60();
      FUN_00853a50(*(undefined4 *)(param_1 + 8));
      uVar2 = *(undefined4 *)(param_1 + 4);
      local_7c = FUN_00843da0();
      local_78 = uVar2;
      FUN_00730fd0(&local_7c);
      FUN_00730f90(&local_64);
      paVar4 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(local_91);
      local_4._0_1_ = 3;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)&local_7c,"",paVar4);
      local_4._0_1_ = 4;
      cVar1 = FUN_004c46c0(local_38,0,&local_7c,1);
      bVar5 = cVar1 == '\0';
      local_4._0_1_ = 3;
      stlp_std::
      basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
      ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
                  *)&local_7c);
      stlp_std::allocator<char>::~allocator<char>(local_91);
      uVar2 = local_7c;
      if (!bVar5) {
        apuStack_58[0] = (undefined4 *)0x0;
        local_4._0_1_ = 5;
        local_7c._3_1_ = SUB41(uVar2,3);
        local_7c._0_3_ = CONCAT12(1,CONCAT11(1,bVar5));
        local_78 = 0;
        uStack_74 = 1;
        uStack_73 = bVar5;
        FUN_00511070(local_88,&local_7c,apuStack_58);
        local_4._0_1_ = 2;
        if (apuStack_58[0] != (undefined4 *)0x0) {
          if ((code *)*apuStack_58[0] != (code *)0x0) {
            (*(code *)*apuStack_58[0])(auStack_50,auStack_50,1);
          }
          apuStack_58[0] = (undefined4 *)0x0;
        }
        FUN_0085b840(*(undefined4 *)(param_1 + 8));
        local_4._0_1_ = 6;
        iVar3 = FUN_004123d0();
        if (iVar3 != 0) {
          FUN_004123d0();
          iVar3 = FUN_007b7c70();
          *(uint *)(iVar3 + 0x2c) = *(uint *)(iVar3 + 0x2c) | 1;
          FUN_00509190(0);
          local_4._0_1_ = 2;
          FUN_008e0110();
          local_4 = (uint)local_4._1_3_ << 8;
          FUN_008e0110();
          local_4 = 0xffffffff;
          FUN_008e0110();
          ExceptionList = local_c;
          return 1;
        }
        local_4._0_1_ = 2;
        FUN_008e0110();
      }
    }
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_008e0110();
    local_4 = 0xffffffff;
    FUN_008e0110();
  }
  ExceptionList = local_c;
  return 0;
}

