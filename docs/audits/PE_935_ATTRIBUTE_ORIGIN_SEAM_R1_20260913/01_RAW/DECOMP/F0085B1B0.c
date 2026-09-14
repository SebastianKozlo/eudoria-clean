
undefined4 * __thiscall FUN_0085b1b0(undefined4 *param_1_00,undefined4 param_1,undefined4 param_2)

{
  undefined4 uVar1;
  undefined4 *puVar2;
  int iVar3;
  
  *param_1_00 = MovableObject::vftable;
  param_1_00[1] = 0;
  param_1_00[2] = param_2;
  param_1_00[3] = 0;
  param_1_00[4] = 0;
  FUN_007345c0();
  param_1_00[0xf] = 0;
  param_1_00[0x10] = 0;
  param_1_00[0x11] = 0;
  param_1_00[0x12] = 0;
  param_1_00[0x13] = 0;
  param_1_00[0x14] = 0;
  param_1_00[0x15] = 0;
  param_1_00[0x16] = 0;
  param_1_00[0x17] = 0;
  param_1_00[0x18] = 0;
  param_1_00[0x19] = 0;
  param_1_00[0x1a] = 0;
  param_1_00[0x1b] = 0;
  param_1_00[0x1c] = 0;
  uVar1 = FUN_004123d0();
  param_1_00[0x1d] = uVar1;
  uVar1 = FUN_00746550();
  param_1_00[0x1e] = uVar1;
  param_1_00[0x1f] = 0;
  param_1_00[0x20] = 0;
  param_1_00[0x21] = 0;
  puVar2 = (undefined4 *)FUN_00746570();
  param_1_00[0x22] = *puVar2;
  uVar1 = puVar2[1];
  param_1_00[0x24] = 0;
  param_1_00[0x25] = 0;
  param_1_00[0x23] = uVar1;
  param_1_00[0x26] = 0x3f800000;
  *(undefined *)(param_1_00 + 0x27) = 0;
  *(undefined *)((int)param_1_00 + 0x9d) = 0;
  *(undefined *)((int)param_1_00 + 0x9e) = 0;
  *(undefined *)((int)param_1_00 + 0x9f) = 0;
  *(undefined2 *)(param_1_00 + 0x28) = 0;
  puVar2 = (undefined4 *)FUN_00746560();
  param_1_00[0x11] = *puVar2;
  param_1_00[0x12] = puVar2[1];
  param_1_00[0x13] = puVar2[2];
  param_1_00[0x14] = DAT_00ba921c;
  param_1_00[0x15] = DAT_00ba9220;
  param_1_00[0x16] = DAT_00ba9224;
  puVar2 = (undefined4 *)FUN_0040b070();
  param_1_00[0x17] = *puVar2;
  param_1_00[0x18] = puVar2[1];
  param_1_00[0x19] = puVar2[2];
  puVar2 = (undefined4 *)FUN_0040b070();
  param_1_00[0x1a] = *puVar2;
  param_1_00[0x1b] = puVar2[1];
  param_1_00[0x1c] = puVar2[2];
  iVar3 = FUN_0040b070();
  FUN_00734220(*(undefined4 *)(iVar3 + 8));
  iVar3 = FUN_0040b070();
  FUN_00734240(*(undefined4 *)(iVar3 + 8));
  puVar2 = (undefined4 *)FUN_0040b070();
  FUN_00734260(*puVar2);
  return param_1_00;
}

