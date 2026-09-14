// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x96de00L (requested via site 0x96de27)

bool __fastcall FUN_0096de00(int param_1)

{
  char cVar1;
  float local_30;
  float local_2c;
  float local_28;
  float local_24;
  float local_20;
  float local_1c;
  float local_18;
  float local_14;
  float local_10;
  float local_c;
  float local_8;
  float local_4;
  
  local_30 = *(float *)(param_1 + 0xc);
  local_2c = *(float *)(param_1 + 0x10);
  local_28 = *(float *)(param_1 + 0x14);
  cVar1 = FUN_00755f90(&local_30);
  if (cVar1 != '\0') {
    local_10 = *(float *)(param_1 + 0x3c);
    local_18 = local_10 * *(float *)(param_1 + 0x18);
    local_14 = *(float *)(param_1 + 0x1c) * local_10;
    local_10 = local_10 * *(float *)(param_1 + 0x20);
    local_30 = local_30 + local_18;
    local_2c = local_2c + local_14;
    local_28 = local_28 + local_10;
    cVar1 = FUN_00755f90(&local_30);
    if (cVar1 != '\0') {
      local_1c = *(float *)(param_1 + 0x40);
      local_24 = local_1c * *(float *)(param_1 + 0x24);
      local_20 = *(float *)(param_1 + 0x28) * local_1c;
      local_1c = local_1c * *(float *)(param_1 + 0x2c);
      local_30 = local_24 + local_30;
      local_2c = local_20 + local_2c;
      local_28 = local_1c + local_28;
      cVar1 = FUN_00755f90(&local_30);
      if (cVar1 != '\0') {
        local_4 = *(float *)(param_1 + 0x44);
        local_c = local_4 * *(float *)(param_1 + 0x30);
        local_8 = *(float *)(param_1 + 0x34) * local_4;
        local_4 = local_4 * *(float *)(param_1 + 0x38);
        local_30 = local_c + local_30;
        local_2c = local_8 + local_2c;
        local_28 = local_4 + local_28;
        cVar1 = FUN_00755f90(&local_30);
        if (cVar1 != '\0') {
          local_30 = local_30 - local_24;
          local_2c = local_2c - local_20;
          local_28 = local_28 - local_1c;
          cVar1 = FUN_00755f90(&local_30);
          if (cVar1 != '\0') {
            local_30 = local_30 - local_18;
            local_2c = local_2c - local_14;
            local_28 = local_28 - local_10;
            cVar1 = FUN_00755f90(&local_30);
            if (cVar1 != '\0') {
              local_30 = local_24 + local_30;
              local_2c = local_20 + local_2c;
              local_28 = local_1c + local_28;
              cVar1 = FUN_00755f90(&local_30);
              if (cVar1 != '\0') {
                local_30 = local_30 - local_c;
                local_2c = local_2c - local_8;
                local_28 = local_28 - local_4;
                cVar1 = FUN_00755f90(&local_30);
                return cVar1 != '\0';
              }
            }
          }
        }
      }
    }
  }
  return false;
}

