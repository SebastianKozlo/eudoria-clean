// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x67bc90L (requested via site 0x67be1e)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __thiscall FUN_0067bc90(int param_1,undefined4 param_2,char param_3)

{
  void *pvVar1;
  void *pvVar2;
  allocator<char> *paVar3;
  void **ppvVar4;
  int iVar5;
  void *pvVar6;
  bool bVar7;
  undefined *puVar8;
  undefined *puVar9;
  undefined4 uVar10;
  void **ppvStack_110;
  allocator<char> local_e9;
  undefined *local_e8;
  undefined4 local_e4;
  undefined4 local_dc;
  undefined4 local_d8;
  undefined4 local_d4;
  undefined4 uStack_d0;
  undefined4 uStack_cc;
  undefined4 uStack_c8;
  undefined4 uStack_c4;
  undefined4 uStack_c0;
  undefined4 uStack_bc;
  undefined local_b8 [12];
  undefined4 *puStack_ac;
  void *apvStack_a4 [6];
  void *pvStack_8c;
  int iStack_88;
  void *apvStack_84 [2];
  int iStack_7c;
  void *pvStack_6c;
  undefined local_68 [44];
  undefined local_3c [48];
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009f9625;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  FUN_0085c0c0();
  FUN_00730700();
  local_4 = 0;
  FUN_00853a50();
  FUN_00730f60();
  FUN_00730f90();
  local_dc = 0;
  local_d8 = 0;
  local_d4 = 0;
  FUN_00730fb0();
  local_e8 = (undefined *)0x1bdc;
  local_e4 = 0;
  FUN_00730fd0();
  paVar3 = (allocator<char> *)stlp_std::allocator<char>::allocator<char>(&local_e9);
  local_4._0_1_ = 1;
  ppvStack_110 = (void **)0x67bd74;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)apvStack_84,"",paVar3);
  ppvStack_110 = apvStack_84;
  uVar10 = 2;
  puVar9 = local_3c;
  puVar8 = local_68;
  local_4._0_1_ = 2;
  FUN_004148f0(puVar8,puVar9,2);
  ppvVar4 = (void **)FUN_00457930(puVar8,puVar9,uVar10);
  local_4._0_1_ = 1;
  stlp_std::basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>::
  ~basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
            ((basic_string<char,class_stlp_std::char_traits<char>,class_stlp_std::allocator<char>_>
              *)apvStack_84);
  local_4._0_1_ = 0;
  stlp_std::allocator<char>::~allocator<char>(&local_e9);
  FUN_0085b840();
  local_4._0_1_ = 3;
  iVar5 = FUN_004123d0();
  if (iVar5 != 0) {
    local_e8 = (undefined *)0x0;
    local_e4 = 0;
    ppvStack_110 = ppvVar4;
    FUN_00414770();
    FUN_00446800();
    ppvStack_110 = (void **)FUN_004154f0();
    FUN_00567030(FUN_00855dc0);
    pvStack_8c = (void *)0x0;
    ppvStack_110 = (void **)0xe10;
    local_4._0_1_ = 4;
    FUN_0040bfe0();
    FUN_00973430();
    local_4._0_1_ = 3;
    if ((puStack_ac != (undefined4 *)0x0) && ((code *)*puStack_ac != (code *)0x0)) {
      ppvStack_110 = apvStack_a4;
      (*(code *)*puStack_ac)();
    }
  }
  FUN_004150f0();
  FUN_008b7100();
  *(undefined4 *)(param_1 + 0xc) = 0;
  if (param_3 != '\0') {
    ppvStack_110 = _DAT_00a7af68;
    uVar10 = FUN_0040bfe0(500,0,2);
    FUN_00414a70(uVar10);
    FUN_0045b560(uVar10);
    pvStack_6c = operator_new(0x50);
    bVar7 = pvStack_6c == (void *)0x0;
    local_4._0_1_ = 5;
    if (bVar7) {
      pvVar6 = (void *)0x0;
    }
    else {
      ppvStack_110 = (void **)0x67bf1e;
      FUN_0045e000();
      local_4 = CONCAT31(local_4._1_3_,6);
      FUN_0045e2e0();
      local_e8 = (undefined *)&ppvStack_110;
      local_dc = 5;
      local_d8 = 5;
      ppvStack_110 = _DAT_00a7b25c;
      uStack_c8 = _DAT_00a7b1d0;
      uStack_c4 = _DAT_00a7b1bc;
      uStack_d0 = _DAT_00a7afa8;
      uStack_cc = _DAT_00a7ae70;
      local_4 = 7;
      uStack_c0 = 3000;
      uStack_bc = 5000;
      pvVar6 = (void *)FUN_006a2830(param_2,local_b8,&local_dc,&uStack_c0,&uStack_d0,&uStack_c8);
    }
    pvVar1 = *(void **)(param_1 + 8);
    local_4 = 9;
    if ((pvVar6 != pvVar1) && (pvVar1 != (void *)0x0)) {
      pvVar2 = *(void **)((int)pvVar1 + 0x40);
      if (pvVar2 != (void *)0x0) {
        ppvStack_110 = (void **)0x67c015;
        stlp_std::__node_alloc::deallocate
                  (pvVar2,(*(int *)((int)pvVar1 + 0x48) - (int)pvVar2 >> 2) * 4);
      }
      operator_delete(pvVar1);
    }
    *(void **)(param_1 + 8) = pvVar6;
    local_4 = 8;
    if (!bVar7) {
      if (apvStack_84[0] != (void *)0x0) {
        ppvStack_110 = (void **)0x67c061;
        stlp_std::__node_alloc::deallocate
                  (apvStack_84[0],(iStack_7c - (int)apvStack_84[0] >> 2) * 4);
      }
    }
    local_4._0_1_ = 3;
    local_4._1_3_ = 0;
    if ((!bVar7) && (pvStack_8c != (void *)0x0)) {
      ppvStack_110 = (void **)0x67c092;
      FUN_00890d30();
      if (pvStack_8c != (void *)0x0) {
        ppvStack_110 = (void **)0x67c0ad;
        stlp_std::__node_alloc::deallocate(pvStack_8c,iStack_88 * 4);
      }
    }
  }
  if (*(int *)(param_1 + 4) != 0) {
    ppvStack_110 = (void **)0x1;
    FUN_0050a0f0();
  }
  local_4 = (uint)local_4._1_3_ << 8;
  FUN_008e0110();
  local_4 = 0xffffffff;
  FUN_00730730();
  ExceptionList = local_c;
  return;
}

