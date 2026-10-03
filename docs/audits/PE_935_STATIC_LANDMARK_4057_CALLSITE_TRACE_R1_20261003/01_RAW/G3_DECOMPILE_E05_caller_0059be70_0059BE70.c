// E05_caller_0059be70 decompile (Ghidra 11.2.1, fresh project, sandbox copy of pinned EXE)
// listing + callers + callees: 01_RAW/G3_FALSIFIER_PATH.json

void FUN_0059be70(void)

{
  char cVar1;
  bool bVar2;
  int *piVar3;
  type_info *this;
  TypeDescriptor *pTVar4;
  undefined local_3c [4];
  undefined **local_38;
  void *local_c;
  undefined *puStack_8;
  uint local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009d29d0;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  FUN_004ad820(DAT_00b9d8d0 ^ (uint)local_3c);
  local_4 = 0;
  cVar1 = FUN_00714630();
  if (cVar1 != '\0') {
    FUN_008df860(0x411);
    local_38 = ArkRepairUI::vftable;
    local_4 = CONCAT31(local_4._1_3_,1);
    cVar1 = FUN_008df290();
    if (cVar1 == '\0') {
      FUN_00595b40();
      piVar3 = (int *)FUN_008df1e0();
      if (piVar3 != (int *)0x0) {
        pTVar4 = &ArkRepairUI_Impl::RTTI_Type_Descriptor;
        this = (type_info *)(**(code **)(*piVar3 + 100))();
        bVar2 = type_info::operator!=(this,(type_info *)pTVar4);
        if (!bVar2) {
          FUN_00599d30();
          FUN_0059ba40();
          FUN_004d9dc0(1,1);
          FUN_004143f0();
          FUN_0042bc30();
        }
      }
    }
    local_4 = local_4 & 0xffffff00;
    local_38 = ArkRepairUI::vftable;
    FUN_008df670();
  }
  local_4 = 0xffffffff;
  thunk_FUN_00703bc0();
  ExceptionList = local_c;
  return;
}

