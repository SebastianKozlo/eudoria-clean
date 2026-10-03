// source: C11_ORACLE_COUNTERPARTS.json :: O04_emitter_caller_006c4060

void FUN_006c4060(void)

{
  int *_Src;
  int iVar1;
  int *piVar2;
  int iVar3;
  undefined4 uVar4;
  int *_Dst;
  void *pvVar5;
  int *piVar6;
  size_t _Size;
  undefined local_2d;
  undefined4 local_2c;
  void *local_28;
  int local_24;
  int local_20;
  undefined4 local_10;
  void *local_c;
  undefined *puStack_8;
  undefined4 local_4;
  
  puStack_8 = &LAB_00a04968;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  local_28 = (void *)0x0;
  local_24 = 0;
  local_20 = 0;
  local_4 = 0;
  FUN_006c3fe0(&DAT_00a855f0,&local_28,DAT_00b9d8d0 ^ (uint)&stack0xffffffc0);
  FUN_006c4020(&DAT_00a858b8,&local_28);
  FUN_006c4020(&DAT_00a858c0,&local_28);
  FUN_006c3d40(local_28,local_24);
  iVar1 = local_24;
  iVar3 = FUN_006c2c90(local_28,local_24);
  if (iVar3 != iVar1) {
    FUN_006c2c50(iVar3,iVar1,&local_2d);
  }
  uVar4 = FUN_00415670();
  local_10 = CONCAT31(local_10._1_3_,1);
  FUN_006c36b0(&local_2c,local_28,local_24,&DAT_00ba45e8,FUN_00823c10,0,uVar4,&DAT_00a7957b,
               &DAT_00a7957b,local_10);
  _Src = DAT_00ba45ec;
  local_2c = 0;
  _Dst = (int *)FUN_008d6d90(DAT_00ba45e8,DAT_00ba45ec,&local_2c,&local_2d);
  piVar6 = _Src;
  piVar2 = _Dst;
  if (_Dst != _Src) {
    while (piVar2 = piVar2 + 1, piVar2 != _Src) {
      piVar6 = DAT_00ba45ec;
      if (*piVar2 != 0) {
        *_Dst = *piVar2;
        _Dst = _Dst + 1;
        piVar6 = DAT_00ba45ec;
      }
    }
  }
  piVar2 = DAT_00ba45ec;
  if ((_Dst != _Src) && (_Size = (int)piVar6 - (int)_Src, piVar2 = _Dst, _Size != 0)) {
    pvVar5 = memmove(_Dst,_Src,_Size);
    piVar2 = (int *)((int)pvVar5 + _Size);
  }
  DAT_00ba45ec = piVar2;
  local_4 = 0xffffffff;
  if (local_28 != (void *)0x0) {
    stlp_std::__node_alloc::deallocate(local_28,(local_20 - (int)local_28 >> 3) * 8);
  }
  ExceptionList = local_c;
  return;
}

