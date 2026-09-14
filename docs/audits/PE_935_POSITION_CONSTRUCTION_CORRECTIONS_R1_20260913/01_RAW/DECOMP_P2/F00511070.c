// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x511070L (requested via site 0x511375)

void FUN_00511070(undefined4 *param_1,char *param_2,undefined4 param_3)

{
  char cVar1;
  int iVar2;
  int iVar3;
  undefined4 *puVar4;
  int *piVar5;
  void *pvVar6;
  undefined4 uVar7;
  undefined auStack_1a0 [24];
  undefined4 uStack_188;
  undefined *puStack_184;
  code *pcStack_180;
  undefined4 *local_17c;
  code *local_178;
  code *local_174;
  undefined4 *local_170;
  undefined4 *local_16c;
  undefined local_14c [32];
  undefined4 local_12c [12];
  undefined4 local_fc [8];
  undefined4 local_dc [52];
  void *local_c;
  undefined *puStack_8;
  int local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009bbe5b;
  local_c = ExceptionList;
  ExceptionList = &local_c;
  iVar2 = FUN_004123d0();
  if (iVar2 == 0) {
    ExceptionList = local_c;
    return;
  }
  cVar1 = FUN_00843d90();
  if (cVar1 == '\0') {
    ExceptionList = local_c;
    return;
  }
  local_16c = (undefined4 *)0x5110ce;
  cVar1 = FUN_00844020();
  if (cVar1 != '\0') {
    ExceptionList = local_c;
    return;
  }
  FUN_00730700();
  uVar7 = 0;
  local_4 = 0;
  FUN_00733340();
  local_16c = local_12c;
  local_170 = param_1;
  local_174 = (code *)0x511107;
  cVar1 = FUN_004c5580();
  if (cVar1 == '\0') goto LAB_005114fe;
  local_dc[0] = 0;
  local_fc[0] = 0;
  local_4 = CONCAT31(local_4._1_3_,2);
  local_16c = (undefined4 *)0x511131;
  FUN_00843dd0();
  local_16c = (undefined4 *)0x511137;
  cVar1 = FUN_00728bf0();
  if (cVar1 == '\0') {
    local_16c = (undefined4 *)0x51134d;
    cVar1 = FUN_00844020();
    if (((cVar1 == '\0') && (*param_2 != '\0')) && (iVar2 = FUN_00746550(), iVar2 != 0)) {
      FUN_00746550();
      local_16c = (undefined4 *)0x511374;
      local_16c = (undefined4 *)FUN_004123d0();
      local_170 = (undefined4 *)0x51137a;
      FUN_004154f0();
      local_170 = (undefined4 *)0x511381;
      FUN_008553d0();
    }
LAB_00511381:
    puVar4 = (undefined4 *)0x0;
    local_16c = (undefined4 *)0x51138b;
    pvVar6 = operator_new(0x130);
    local_4._0_1_ = 4;
    if (pvVar6 != (void *)0x0) {
      local_16c = (undefined4 *)0x4;
      local_170 = local_12c;
      local_174 = (code *)0x5113b4;
      puVar4 = (undefined4 *)FUN_006c0d50();
    }
    local_4._0_1_ = 2;
    uVar7 = FUN_00525be0();
    local_170 = (undefined4 *)FUN_004123d0();
    local_174 = FUN_00510f80;
    local_178 = (code *)0x5113ed;
    local_16c = (undefined4 *)uVar7;
    FUN_0050d900();
    local_4._0_1_ = 5;
    local_16c = (undefined4 *)0x511401;
    FUN_006c7650();
    local_4._0_1_ = 2;
    FUN_00662d00();
    local_16c = param_1;
    local_174 = (code *)0x51141e;
    local_170 = puVar4;
    cVar1 = FUN_0050cc70();
    if (cVar1 != '\0') {
      FUN_00584340(param_3);
      local_4._0_1_ = 6;
      uVar7 = FUN_004123d0(*(undefined4 *)param_2,*(undefined4 *)(param_2 + 4),
                           *(undefined4 *)(param_2 + 8));
      local_4._0_1_ = 2;
      FUN_0050d970(auStack_1a0,FUN_00510af0,uVar7);
      FUN_00510e00();
      local_174 = (code *)(uint)(byte)param_2[8];
      local_16c = local_fc;
      local_170 = local_dc;
      local_178 = (code *)local_14c;
      local_4._0_1_ = 7;
      pcStack_180 = (code *)0x5114bc;
      local_17c = puVar4;
      pcStack_180 = (code *)FUN_004123d0();
      puStack_184 = (undefined *)0x5114c2;
      FUN_004148f0();
      puStack_184 = (undefined *)0x5114c9;
      FUN_00457cd0();
      local_4._0_1_ = 2;
      FUN_00662d00();
    }
  }
  else {
    cVar1 = FUN_00844460();
    if (cVar1 != '\0') {
      FUN_0041b3a0();
      iVar2 = FUN_007ce1e0();
      iVar3 = FUN_004123d0();
      if (iVar2 == iVar3) goto LAB_00511171;
LAB_00511274:
      iVar2 = *(int *)(param_2 + 4);
      if (iVar2 == 0) {
        local_16c = (undefined4 *)0x511287;
        FUN_00843dd0();
        local_16c = (undefined4 *)0x51128d;
        iVar2 = FUN_007291f0();
      }
      local_170 = (undefined4 *)0x51129b;
      local_16c = (undefined4 *)uVar7;
      local_170 = (undefined4 *)FUN_004123d0();
      local_174 = (code *)0x5112a1;
      local_174 = (code *)FUN_00414670();
      local_17c = (undefined4 *)local_14c;
      local_178 = FUN_00441200;
      pcStack_180 = (code *)0x5112b1;
      puVar4 = (undefined4 *)FUN_0050caf0();
      local_178 = (code *)*puVar4;
      local_174 = (code *)puVar4[1];
      local_170 = (undefined4 *)puVar4[2];
      local_16c = (undefined4 *)puVar4[3];
      local_17c = (undefined4 *)0x5112db;
      FUN_0050e310();
      local_174 = (code *)0x5112ee;
      local_170 = (undefined4 *)uVar7;
      local_16c = (undefined4 *)iVar2;
      local_174 = (code *)FUN_004123d0();
      local_178 = (code *)0x5112f6;
      local_178 = (code *)FUN_004123d0();
      local_17c = (undefined4 *)0x5112fc;
      local_17c = (undefined4 *)FUN_00414670();
      puStack_184 = local_14c;
      pcStack_180 = FUN_0043eae0;
      uStack_188 = 0x51130c;
      piVar5 = (int *)FUN_0050d8c0();
      local_17c = (undefined4 *)*piVar5;
      local_178 = (code *)piVar5[1];
      local_174 = (code *)piVar5[2];
      local_170 = (undefined4 *)piVar5[3];
      local_16c = (undefined4 *)piVar5[4];
      pcStack_180 = (code *)0x51133f;
      FUN_0050e0c0();
      goto LAB_00511381;
    }
LAB_00511171:
    local_16c = (undefined4 *)0x51117d;
    cVar1 = FUN_00844020();
    if (cVar1 != '\0') goto LAB_00511274;
    local_16c = (undefined4 *)0x511191;
    cVar1 = FUN_00844020();
    if (cVar1 != '\0') goto LAB_00511274;
    local_16c = (undefined4 *)0x5111a5;
    FUN_00843dd0();
    local_16c = (undefined4 *)0x5111af;
    local_16c = (undefined4 *)FUN_004123d0();
    local_170 = (undefined4 *)0x5111bc;
    FUN_007199e0();
    local_16c = (undefined4 *)0x5111c9;
    FUN_006baa20();
    local_4._0_1_ = 3;
    cVar1 = thunk_FUN_006c4200();
    if (cVar1 != '\0') {
      local_16c = (undefined4 *)0x511201;
      FUN_006ea810();
      local_16c = (undefined4 *)0x511211;
      FUN_0048ada0();
      local_16c = (undefined4 *)0x511218;
      cVar1 = FUN_00737c20();
      if (cVar1 == '\0') {
        local_16c = (undefined4 *)0x51122a;
        FUN_006ea810();
        local_16c = (undefined4 *)0x51123a;
        FUN_0048ada0();
        local_16c = (undefined4 *)0x511241;
        cVar1 = FUN_00737c20();
        if (cVar1 != '\0') goto LAB_0051124a;
      }
      else {
LAB_0051124a:
        local_16c = (undefined4 *)0x511250;
        FUN_0043a550();
        local_16c = (undefined4 *)0x511257;
        FUN_0072f580();
        uVar7 = FUN_007ce1e0();
      }
      local_4 = CONCAT31(local_4._1_3_,2);
      FUN_008e0110();
      goto LAB_00511274;
    }
    local_4._0_1_ = 2;
    FUN_008e0110();
  }
  local_4._0_1_ = 1;
  FUN_00662d00();
  local_4 = (uint)local_4._1_3_ << 8;
  FUN_00662d00();
LAB_005114fe:
  local_4 = 0xffffffff;
  FUN_00730730();
  ExceptionList = local_c;
  return;
}

