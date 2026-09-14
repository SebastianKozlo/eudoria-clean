// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x413590L (requested via site 0x413590)

LPCRITICAL_SECTION __fastcall FUN_00413590(LPCRITICAL_SECTION param_1)

{
  if (DAT_00ba1200 == '\0') {
    FUN_00413460();
  }
  InitializeCriticalSection(param_1);
  param_1[1].LockCount = 0x1fe319ba;
  *(undefined *)&param_1[1].DebugInfo = 0;
  return param_1;
}

