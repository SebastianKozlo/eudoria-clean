// source: C4_CONSTRUCTION_TRACE.json :: W04_template_out_0072fe30

undefined4 __thiscall
FUN_0072fe30(int param_1_00,undefined4 *param_1,undefined4 *param_2,undefined4 *param_3)

{
  undefined4 uVar1;
  undefined4 uVar2;
  undefined4 *puVar3;
  int iVar4;
  
  if ((*(int *)(param_1_00 + 0x24) - *(int *)(param_1_00 + 0x20) & 0xfffffffcU) == 0x24) {
    puVar3 = *(undefined4 **)(param_1_00 + 0x20);
    uVar1 = puVar3[1];
    uVar2 = puVar3[2];
    *param_1 = *puVar3;
    param_1[1] = uVar1;
    param_1[2] = uVar2;
    iVar4 = *(int *)(param_1_00 + 0x20);
    uVar1 = *(undefined4 *)(iVar4 + 0x10);
    uVar2 = *(undefined4 *)(iVar4 + 0x14);
    *param_2 = *(undefined4 *)(iVar4 + 0xc);
    param_2[1] = uVar1;
    param_2[2] = uVar2;
    iVar4 = *(int *)(param_1_00 + 0x20);
    uVar1 = *(undefined4 *)(iVar4 + 0x1c);
    uVar2 = *(undefined4 *)(iVar4 + 0x20);
    *param_3 = *(undefined4 *)(iVar4 + 0x18);
    param_3[1] = uVar1;
    param_3[2] = uVar2;
    return 1;
  }
  return 0;
}

