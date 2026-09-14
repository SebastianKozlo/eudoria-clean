// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x58e230L (requested via site 0x58e253)

uint __thiscall FUN_0058e230(int *param_1_00,undefined4 param_1)

{
  uint in_EAX;
  uint uVar1;
  
  if (*param_1_00 != 0) {
    in_EAX = FUN_00726490();
    if (in_EAX != 0) {
      in_EAX = FUN_00726490();
      if (in_EAX != 0) {
        FUN_004154f0(in_EAX,param_1);
        uVar1 = FUN_00854620(in_EAX,param_1);
        return uVar1;
      }
    }
  }
  return in_EAX & 0xffffff00;
}

