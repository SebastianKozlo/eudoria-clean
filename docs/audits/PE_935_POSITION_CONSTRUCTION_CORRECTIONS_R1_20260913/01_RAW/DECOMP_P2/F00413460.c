// DECOMPILED (Ghidra 11.2.1) from Entropia.exe
// function entry 0x413460L (requested via site 0x413460)

/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00413460(void)

{
  HMODULE hModule;
  undefined local_5;
  
  _DAT_00ba1204 = (undefined4 *)operator_new(0x18);
  if (_DAT_00ba1204 == (undefined4 *)0x0) {
    _DAT_00ba1204 = (undefined4 *)0x0;
  }
  else {
    *_DAT_00ba1204 = 0;
    *(undefined *)_DAT_00ba1204 = 0;
    _DAT_00ba1204[1] = 0;
    _DAT_00ba1204[4] = 0;
    _DAT_00ba1204[2] = _DAT_00ba1204;
    _DAT_00ba1204[3] = _DAT_00ba1204;
    *(undefined *)(_DAT_00ba1204 + 5) = local_5;
  }
  _DAT_00ba1208 = (LPCRITICAL_SECTION)operator_new(0x18);
  InitializeCriticalSection(_DAT_00ba1208);
  hModule = LoadLibraryA("kernel32.dll");
  if (hModule != (HMODULE)0x0) {
    _DAT_00ba120c = GetProcAddress(hModule,"TryEnterCriticalSection");
    FreeLibrary(hModule);
  }
  DAT_00ba1200 = 1;
  return;
}

