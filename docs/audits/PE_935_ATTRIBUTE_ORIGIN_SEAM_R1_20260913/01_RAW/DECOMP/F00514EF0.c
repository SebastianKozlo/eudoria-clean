
void FUN_00514ef0(undefined4 param_1,undefined4 param_2,undefined4 param_3,int *param_4)

{
  uint3 uVar1;
  char cVar2;
  uint uVar3;
  int *piVar4;
  undefined4 *puVar5;
  int iVar6;
  undefined4 uVar7;
  int *piVar8;
  undefined4 *puVar9;
  undefined4 uVar10;
  undefined4 uVar11;
  int **ppiVar12;
  char *pcVar13;
  int local_184;
  int local_180;
  int local_17c;
  undefined4 local_178;
  char local_171;
  undefined4 local_170;
  undefined4 local_16c;
  int *local_164;
  int *local_160;
  undefined4 local_15c;
  undefined4 local_158;
  undefined4 local_154;
  undefined4 *local_150;
  undefined4 *local_14c;
  undefined4 local_148;
  char local_144;
  undefined4 local_13c;
  undefined4 local_138;
  undefined4 local_134;
  undefined4 local_130;
  undefined local_12c [8];
  undefined4 local_124;
  undefined4 local_120;
  undefined4 local_11c;
  undefined4 local_118;
  undefined4 local_114;
  undefined4 local_110;
  undefined local_10c [4];
  undefined local_108 [76];
  undefined local_bc [4];
  undefined local_b8 [172];
  void *local_c;
  undefined *puStack_8;
  uint local_4;
  
  local_4 = 0xffffffff;
  puStack_8 = &LAB_009bc65e;
  local_c = ExceptionList;
  uVar3 = DAT_00b9d8d0 ^ (uint)&stack0xfffffe6c;
  ExceptionList = &local_c;
  FUN_004da170(param_1);
  local_4 = 0;
  local_4._1_3_ = 0;
  uVar1 = local_4._1_3_;
  local_4._1_3_ = 0;
  switch(param_3) {
  case 0x2b:
    uVar7 = FUN_00423c10(param_4,&local_178,&local_170,uVar3);
    FUN_00423c10(uVar7);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_00511b00(local_178,local_170);
    }
    break;
  case 0x2c:
    FUN_00727a20();
    local_4 = CONCAT31(local_4._1_3_,1);
    FUN_007278c0(param_4,local_bc);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_007160e0(local_bc);
      uVar7 = 0x3f800000;
      FUN_00414a70(0x3f800000);
      FUN_00460070(uVar7);
      FUN_00414470();
      FUN_0042e2f0();
      FUN_00414470();
      FUN_0042d850();
      FUN_004ac570(local_b8);
    }
    local_4 = local_4 & 0xffffff00;
    FUN_00727ac0();
    break;
  case 0x2d:
    local_164 = (int *)0x0;
    local_160 = (int *)0x0;
    local_15c = 0;
    local_4 = 2;
    FUN_00512fd0(&local_164);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      ppiVar12 = &local_164;
      FUN_004310f0(ppiVar12);
      FUN_004f50f0(ppiVar12);
    }
    local_4 = local_4 & 0xffffff00;
    FUN_004759f0();
    break;
  case 0x2e:
    local_184 = 0;
    local_180 = 0;
    uVar7 = FUN_00423c10(param_4,&local_178,&local_170,uVar3);
    piVar4 = (int *)FUN_00423c10(uVar7);
    if ((*(char *)((int)piVar4 + 0x11) == '\0') || ((uint)piVar4[2] < piVar4[3] + 8U)) {
      local_184 = 0;
      local_180 = 0;
      if (*(char *)((int)piVar4 + 0x11) != '\0') {
        *(undefined *)((int)piVar4 + 0x11) = 0;
      }
    }
    else {
      piVar4 = (int *)(*piVar4 + piVar4[3]);
      local_184 = *piVar4;
      local_180 = piVar4[1];
      FUN_0040de60(8);
    }
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      piVar4 = &local_184;
      uVar7 = local_178;
      uVar10 = local_170;
      FUN_004641f0(local_178,local_170,piVar4);
      FUN_00565900(uVar7,uVar10,piVar4);
    }
    break;
  case 0x2f:
    uVar7 = FUN_00423c10(param_4,&local_178,&local_170,uVar3);
    FUN_004c32f0(uVar7);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_004ec180(local_178,local_170);
    }
    break;
  case 0x30:
    local_13c = 0;
    local_138 = 0;
    local_134 = 0;
    local_130 = 0;
    uVar7 = FUN_004b08e0(param_4,&local_170);
    FUN_00412430(&local_13c);
    uVar7 = FUN_00423c10(uVar7,&local_130,local_12c,uVar3);
    FUN_00423c10(uVar7);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      uVar7 = FUN_0075ff20();
      uVar11 = 4;
      uVar10 = 0x23a;
      local_4._0_1_ = 3;
      FUN_00414b70(0x23a,uVar7,4);
      FUN_0046a520(uVar10,uVar7,uVar11);
      local_4._0_1_ = 0;
      FUN_008e0110();
      FUN_004310f0();
      uVar7 = FUN_004f4d90();
      FUN_00843d60(uVar7);
      local_4 = CONCAT31(local_4._1_3_,4);
      uVar7 = FUN_00843da0();
      uVar10 = 0x2d;
      FUN_004151f0(0x2d,uVar7);
      iVar6 = FUN_00866140(uVar10,uVar7);
      if (iVar6 != 0) {
        FUN_005c29d0(&local_13c,local_170);
      }
      local_4 = local_4 & 0xffffff00;
      FUN_008e0110();
    }
    break;
  case 0x31:
    local_184 = 0;
    local_180 = 0;
    uVar7 = FUN_00423c10(param_4,&local_170,&local_178,uVar3);
    piVar4 = (int *)FUN_00423c10(uVar7);
    if ((*(char *)((int)piVar4 + 0x11) == '\0') || ((uint)piVar4[2] < piVar4[3] + 8U)) {
      local_184 = 0;
      local_180 = 0;
      if (*(char *)((int)piVar4 + 0x11) != '\0') {
        *(undefined *)((int)piVar4 + 0x11) = 0;
      }
    }
    else {
      piVar4 = (int *)(*piVar4 + piVar4[3]);
      local_184 = *piVar4;
      local_180 = piVar4[1];
      FUN_0040de60(8);
    }
    if (*(char *)((int)param_4 + 0x11) == '\0') break;
    FUN_00843d60(local_170);
    local_4 = CONCAT31(local_4._1_3_,5);
    cVar2 = FUN_004da190();
    if (cVar2 == '\0') {
LAB_005152f7:
      FUN_0075ff20();
      local_4._0_1_ = 6;
      local_124 = 0;
      FUN_00719e30(local_178,&local_184,0,0,&local_124);
      uVar10 = 0;
      puVar5 = &local_13c;
      puVar9 = &local_158;
      uVar7 = FUN_00726490(puVar9,puVar5,0);
      FUN_004641f0(uVar7);
      FUN_00567c50(uVar7,puVar9,puVar5,uVar10);
      local_4 = CONCAT31(local_4._1_3_,5);
      FUN_008e0110();
    }
    else {
      uVar7 = FUN_00843dd0(local_10c);
      cVar2 = FUN_0072a580(uVar7);
      if (cVar2 == '\0') goto LAB_005152f7;
    }
    local_4 = local_4 & 0xffffff00;
    FUN_008e0110();
    break;
  case 0x32:
    local_150 = &local_158;
    local_158 = 0;
    local_154 = 0;
    local_148 = 0;
    local_144 = local_171;
    local_4._0_1_ = 7;
    local_178 = 0;
    local_14c = local_150;
    FUN_005134d0(local_150);
    puVar5 = &local_170;
    piVar4 = &local_184;
    uVar7 = FUN_00423c10(param_4,&local_178,piVar4,puVar5);
    uVar7 = FUN_00423c10(uVar7,piVar4,puVar5,uVar3);
    FUN_00423c10(uVar7);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      local_164 = (int *)0x0;
      local_160 = (int *)0x0;
      local_15c = 0;
      ppiVar12 = &local_164;
      uVar7 = 0x2e;
      local_4 = CONCAT31(local_4._1_3_,8);
      FUN_004151f0(0x2e,ppiVar12);
      FUN_00866700(uVar7,ppiVar12);
      if (local_164 != local_160) {
        FUN_004f37d0(&local_158,&local_178,local_184,local_170);
      }
      local_4._0_1_ = 7;
      FUN_006adf00();
    }
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_0098aa20();
    break;
  case 0x33:
    uVar7 = FUN_00423c10(param_4,&local_170,&local_184,uVar3);
    FUN_00423c10(uVar7);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_00512b30(local_170,local_184);
    }
    break;
  default:
    pcVar13 = &local_171;
    piVar4 = &local_17c;
    FUN_00414370(piVar4,param_3,param_4,pcVar13);
    FUN_0042b7f0(piVar4,param_3,param_4,pcVar13);
    break;
  case 0x36:
    local_164 = (int *)0x0;
    local_160 = (int *)0x0;
    local_15c = 0;
    local_4 = 9;
    FUN_00513ca0(&local_164);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      ppiVar12 = &local_164;
      FUN_00423b10(ppiVar12);
      FUN_004bb3e0(ppiVar12);
    }
    local_4 = local_4 & 0xffffff00;
    FUN_004ba8a0();
    break;
  case 0x37:
    local_158 = 0;
    local_154 = 0;
    local_150 = (undefined4 *)0x0;
    local_13c = 0;
    local_138 = 0;
    local_134 = 0;
    local_120 = 0;
    local_11c = 0;
    local_118 = 0;
    local_164 = (int *)0x0;
    local_160 = (int *)0x0;
    local_15c = 0;
    local_4._0_1_ = 0xd;
    local_4._1_3_ = 0;
    if ((*(char *)((int)param_4 + 0x11) == '\0') || ((uint)param_4[2] < param_4[3] + 8U)) {
      local_170 = 0;
      local_16c = 0;
      if (*(char *)((int)param_4 + 0x11) != '\0') {
        *(undefined *)((int)param_4 + 0x11) = 0;
        uVar1 = local_4._1_3_;
      }
    }
    else {
      puVar5 = (undefined4 *)(*param_4 + param_4[3]);
      local_170 = *puVar5;
      local_16c = puVar5[1];
      local_4._1_3_ = uVar1;
      FUN_0040de60(8);
      uVar1 = local_4._1_3_;
    }
    local_4._1_3_ = uVar1;
    FUN_00423c10(param_4,&local_184);
    FUN_00514db0(&local_158);
    FUN_00514db0(&local_13c);
    FUN_00514db0(&local_120);
    FUN_005130e0(&local_164);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_0049dcc0(local_184);
      local_4 = CONCAT31(local_4._1_3_,0xe);
      cVar2 = FUN_008df290();
      if (cVar2 != '\0') {
        FUN_004a0ba0(&local_170,&local_158,&local_13c,&local_120,&local_164);
      }
      local_4._0_1_ = 0xd;
      FUN_008df670();
    }
    local_4._0_1_ = 0xc;
    FUN_004e45f0();
    local_4._0_1_ = 0xb;
    FUN_005129c0();
    local_4._0_1_ = 10;
    FUN_005129c0();
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_005129c0();
    break;
  case 0x38:
    FUN_00423c10(param_4,&local_184);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_00514470(&local_17c,local_184);
    }
    break;
  case 0x39:
    local_158 = 0;
    local_154 = 0;
    local_150 = (undefined4 *)0x0;
    FUN_0052a260();
    local_4 = CONCAT31(local_4._1_3_,0x10);
    FUN_00514db0(&local_158);
    FUN_00514c60(&local_13c);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_0088c090(&local_158,&local_13c);
    }
    local_4._0_1_ = 0xf;
    FUN_00513590();
    local_4 = (uint)local_4._1_3_ << 8;
    FUN_005129c0();
    break;
  case 0x3e:
    FUN_00973500();
    FUN_004099c0(&local_184);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_00511de0(0x13,&local_184);
      piVar4 = &local_184;
      FUN_00414470(piVar4);
      FUN_0042dc30(piVar4);
    }
    break;
  case 0x3f:
    FUN_0074bb80();
    local_4 = CONCAT31(local_4._1_3_,0x11);
    FUN_0074bbb0(param_4,&local_158);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_00513b60(&local_17c,&local_158);
    }
    local_4 = local_4 & 0xffffff00;
    FUN_008e0110();
    break;
  case 0x40:
    FUN_00423c10(param_4,&local_178);
    uVar7 = local_178;
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_00843d60(local_178);
      local_4._0_1_ = 0x12;
      cVar2 = FUN_0042bc20();
      if (cVar2 != '\0') {
        local_184 = 0;
        local_180 = 0;
        cVar2 = FUN_00715100(uVar7);
        if (cVar2 != '\0') {
          FUN_007434d0();
          local_158 = *(undefined4 *)(local_17c + 0x2c);
          local_4._0_1_ = 0x13;
          FUN_0042ead0(&local_178);
          puVar5 = &local_158;
          uVar10 = 1;
          FUN_004310f0(1,uVar7,puVar5);
          FUN_004f6fc0(uVar10,uVar7,puVar5);
          local_4._0_1_ = 0x12;
          FUN_004b1180();
        }
        piVar4 = &local_184;
        uVar7 = FUN_004123d0(piVar4);
        FUN_004310f0(uVar7);
        cVar2 = FUN_004f6e60(uVar7,piVar4);
        if (cVar2 != '\0') {
          FUN_004c3580(&local_184);
          local_4._0_1_ = 0x14;
          uVar7 = FUN_004123d0();
          FUN_004c3940(uVar7);
          local_4._0_1_ = 0x12;
          FUN_004c43e0();
        }
        uVar7 = FUN_00843f20(local_108);
        FUN_004c3580(uVar7);
        local_4._0_1_ = 0x15;
        uVar7 = FUN_004123d0();
        FUN_004c3940(uVar7);
        local_4._0_1_ = 0x12;
        FUN_004c43e0();
        FUN_00844980();
      }
      local_4 = (uint)local_4._1_3_ << 8;
      FUN_008e0110();
    }
    break;
  case 0x41:
    local_164 = (int *)0x0;
    local_160 = (int *)0x0;
    local_15c = 0;
    local_4 = 0x16;
    FUN_00505710(&local_164);
    piVar4 = local_160;
    for (piVar8 = local_164; piVar8 != piVar4; piVar8 = piVar8 + 1) {
      iVar6 = *piVar8;
      local_184 = iVar6;
      FUN_007434f0(*(undefined4 *)(local_17c + 0x2c));
      local_4._0_1_ = 0x17;
      FUN_0042ead0(&local_184);
      puVar5 = &local_158;
      uVar7 = 1;
      FUN_004310f0(1,iVar6,puVar5);
      FUN_004f8950(uVar7,iVar6,puVar5);
      local_4 = CONCAT31(local_4._1_3_,0x16);
      FUN_004b1180();
    }
    puVar5 = &local_114;
    uVar10 = 0x89;
    local_114 = 0;
    local_110 = 0;
    uVar7 = FUN_00726490(0x89,puVar5);
    FUN_00414770(uVar7);
    FUN_00446800(uVar7,uVar10,puVar5);
    FUN_00401360();
    FUN_00417880();
    local_4 = local_4 & 0xffffff00;
    FUN_006adf00();
    break;
  case 0x42:
    FUN_00423c10(param_4,&local_170);
    FUN_00423c10(param_4,&local_184);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      uVar7 = *(undefined4 *)(local_17c + 0x2c);
      uVar10 = local_170;
      iVar6 = local_184;
      FUN_00414bf0(uVar7,local_170,local_184);
      FUN_0046c2a0(uVar7,uVar10,iVar6);
    }
    break;
  case 0x43:
    FUN_00423c10(param_4,&local_184);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      uVar7 = *(undefined4 *)(local_17c + 0x2c);
      iVar6 = local_184;
      FUN_00414bf0(uVar7,local_184);
      FUN_0046e790(uVar7,iVar6);
    }
    break;
  case 0x44:
    local_158 = 0;
    local_154 = 0;
    local_150 = (undefined4 *)0x0;
    local_4 = 0x18;
    FUN_005131c0(&local_158);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      uVar7 = *(undefined4 *)(local_17c + 0x2c);
      puVar5 = &local_158;
      FUN_00414ff0(uVar7,puVar5);
      FUN_00486530(uVar7,puVar5);
    }
    local_4 = local_4 & 0xffffff00;
    FUN_005c55d0();
    break;
  case 0x45:
    puVar5 = &local_170;
    puVar9 = &local_178;
    local_178 = 0;
    local_170 = 0;
    uVar7 = FUN_00423c10(param_4,&local_184,puVar9,puVar5);
    uVar7 = FUN_00423c10(uVar7,puVar9,puVar5,uVar3);
    FUN_00423c10(uVar7);
    iVar6 = local_184;
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_00843d60(local_184);
      local_4._0_1_ = 0x19;
      FUN_00845f70(0x2b,local_178);
      FUN_00845f70(0x2c,local_170);
      uVar7 = *(undefined4 *)(local_17c + 0x2c);
      FUN_00414ff0(uVar7,iVar6);
      FUN_00487060(uVar7,iVar6);
      FUN_005c4ba0(&local_158,3);
      local_4 = (uint)local_4._1_3_ << 8;
      FUN_008e0110();
    }
    break;
  case 0x46:
    FUN_004b08e0(param_4,&local_184);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      iVar6 = local_184;
      FUN_00414ff0(local_184);
      FUN_00488010(iVar6);
    }
    break;
  case 0x47:
    uVar7 = FUN_00423c10(param_4,&local_184,&local_184,uVar3);
    FUN_00423c10(uVar7);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      iVar6 = local_184;
      FUN_00414ff0(local_184);
      FUN_00487750(iVar6);
    }
    break;
  case 0x48:
    uVar7 = FUN_00423c10(param_4,&local_170,&local_184,uVar3);
    FUN_00423c10(uVar7);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_004143f0();
      iVar6 = FUN_00746550();
      if (local_184 == iVar6) {
        uVar7 = local_170;
        iVar6 = local_184;
        FUN_00414ff0(local_170);
        FUN_004882e0(uVar7,iVar6);
      }
      else {
        iVar6 = local_184;
        FUN_00414ff0(local_184);
        FUN_00488480(iVar6);
      }
    }
    break;
  case 0x49:
    uVar7 = FUN_004b08e0(param_4,&local_171,&local_170);
    FUN_00423c10(uVar7);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      if (local_171 == '\0') {
        FUN_00843d60(local_170);
        local_4._0_1_ = 0x1a;
        FUN_00845f70(0x3f1,0);
        FUN_0050dd60(&local_158,0);
        uVar7 = FUN_00726490();
        FUN_00843d60(uVar7);
        local_4._0_1_ = 0x1b;
        FUN_00845f70(0x3f5,0);
        local_4._0_1_ = 0x1a;
        FUN_008e0110();
        local_4 = (uint)local_4._1_3_ << 8;
        FUN_008e0110();
      }
      else {
        uVar7 = *(undefined4 *)(local_17c + 0x2c);
        uVar10 = local_170;
        FUN_004145f0(uVar7,local_170);
        FUN_004387a0(uVar7,uVar10);
      }
    }
    break;
  case 0x4a:
    piVar4 = &local_184;
    puVar5 = &local_170;
    uVar7 = FUN_004b08e0(param_4,&local_178,puVar5,piVar4);
    uVar7 = FUN_00423c10(uVar7,puVar5,piVar4,uVar3);
    FUN_00423c10(uVar7);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      uVar7 = local_178;
      uVar10 = local_170;
      iVar6 = local_184;
      FUN_004145f0(local_178,local_170,local_184);
      FUN_00437ee0(uVar7,uVar10,iVar6);
    }
    break;
  case 0x4b:
    uVar7 = FUN_00423c10(param_4,&local_170,&local_184,uVar3);
    FUN_004b08e0(uVar7);
    if (*(char *)((int)param_4 + 0x11) != '\0') {
      FUN_005146b0(*(undefined4 *)(local_17c + 0x2c),local_170,local_184);
    }
  }
  local_4 = 0xffffffff;
  thunk_FUN_00703bc0();
  ExceptionList = local_c;
  return;
}

