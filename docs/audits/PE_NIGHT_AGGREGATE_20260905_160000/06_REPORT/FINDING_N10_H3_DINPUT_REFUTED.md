# FINDING N-10 (H3) — THE PREDICATE HUNT: THE DINPUT ROUTE REFUTED EMPIRICALLY

**RUN**: H3 of the hourly loop — the instruction-level hunt for the display-enum predicate.

## THE HUNT THIS HOUR

1. **The DInput chain decoded (Ghidra)**: the exe's ONLY DINPUT8 import = DirectInput8Create;
   its ONLY call site = FUN_00864ae0 (the input-init):
   ```c
   if (di == NULL && DirectInput8Create(hInst, 0x800, IID@0xA9BED4, &di, 0) < 0) {
       msg = "DirectInput8Create : " + hr_string;   // FUN_00408c10 + FUN_00864a30
       *caller_msg = msg;                             // -> the abort
   } else {
       hr = di->vtable[+0xC](...);   // = IDirectInput8::CreateDevice (NOT EnumDevices — the
                                     //   vtable order lesson: QI/AddRef/Release/CreateDevice@+0xC)
       if (hr < 0) { ...the same error path... }
   }
   ```
2. **THE IID ground truth**: the client's IID @0xA9BED4 (.rdata) = **{BF798030-483A-4DA2-AA99-5D64ED369700}**
   (IID_IDirectInput8A — read VERBATIM from the binary after my two hand-typed GUID attempts failed).
3. **THE EMPIRICAL TEST** (the 32-bit python, the client's exact calls + GUIDs):
   ```
   DirectInput8Create      = 0x00000000  OK
   CreateDevice(SysMouse)  = 0x00000000  OK
   CreateDevice(SysKeyboard)= 0x00000000 OK
   EnumDevices(ALL)        = 0x00000000  OK (2 devices)
   ```
   **THE ENTIRE DINPUT ROUTE SUCCEEDS ON THIS MACHINE** → the input-init hypothesis
   (the InputHost/CoreMessaging display queries) = **REFUTED**.

## THE INSTRUMENT LESSONS (recorded honestly)

1. My hand-typed IDirectInput8A GUID was WRONG TWICE (a hallucinated GUID -> E_NOINTERFACE);
   the fix = read the IID VERBATIM from the binary (0xA9BED4).
2. The vtable offset +0xC = CreateDevice (the DInput8 vtable order), NOT EnumDevices
   (my first probe mis-called it -> E_POINTER as MY bug, not the machine's).
3. VA != RVA (the IID lookup first failed by treating the VA as an RVA).

## THE HONEST STATE OF THE PREDICATE

REFUTED: the DInput init (all its calls succeed here). THE DEVICEMAP/HardwareInformation.MemorySize
reads in the death trace come from ANOTHER in-process display query. The remaining candidates
(priority order): (a) the WMV reader init (WMVCore imports GetDC; WMCreateReader = the exe's import;
the death precedes any media file open — consistent), (b) the Bink display-surface pre-init
(binkw32: GetDC/GetDeviceCaps/ChangeDisplaySettingsA; no .bik open needed for the surface init),
(c) another DLL display query. THE NEXT PROBE (H4): the GetDC/GetDeviceCaps-family empirical
tests on this machine (a 32-bit probe: GetDC(NULL)+GetDeviceCaps+EnumDisplayDevices — replicate
what each candidate does + check which one performs the registry reads via a simultaneous ProcMon).

THE GROUND TRUTH (unchanged): the client dies right after the display enumeration;
the exact predicate = still UNVERIFIED; the environment = degenerate (measured).
