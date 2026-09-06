# FINDING N-5 — THE DISPLAY PREDICATE STATIC RE (the Ghidra run)

**RUN**: the Ghidra headless chain (fresh project `PE935_DISPLAY_ENUM_R1`, the sandbox
Entropia.exe E7785430..., 413s analysis, reusable: `-process -noanalysis` for future queries).
Zero runtime; zero originals touched. All addresses = the exe's VAs (base 0x400000, no relocation).

## THE CLIENT BOOT CHAIN (decompiled, byte-anchored)

```
entry @0x0095DA11 (CRT) -> ___tmainCRTStartup @0x0095D750
  -> WinMain = FUN_00401000 @0x00401000 (a 516-byte launcher stub):
     time/srand; command-line parse;
     FUN_00408850("Entropia");                       // the app-name init
     gate = FUN_00407270(0);                          // the SINGLE-INSTANCE MUTEX
     //   (CreateMutexA + ERROR_ALREADY_EXISTS 0xB7 -> skip-all -> exit)
     if (gate) {
        FUN_00406ec0();                               // a flag set
        FUN_00406a70("");                             // handle init
        FUN_00406560(0xffffffff);                     // SetThreadPriority(-1)
        new(0x48) + FUN_00402e90(...);                // the core object create
        FUN_00404e50(...); FUN_0055f0-chain...
     }
  -> RUN = FUN_004055f0 @0x004055f0:
       CHECK-1 = FUN_00402fd0()                       // the window "Entropia Universe" (CreateWindowExA)
       WSAStartup(0x202)                              // the trace: WinSock catalogs
       DEEP-INIT = FUN_00405150(name)                 // the config chain (below)
       if TRUE -> FUN_00402910()                      // the message loop
                    PeekMessageA || FUN_00401360(); FUN_00417030()  // the LOOP-STEP (the engine tick)
```

THE DEEP-INIT (FUN_00405150) sequence: new(0x90) + FUN_00417b50 -> "data" setup ->
FUN_00404d90 -> the param setters (FUN_00728140/797280/743fd0/92f7d0 = trivial field stores)
-> FUN_004061a0 = **the CRC32 file reader** (basic_ifstream + the table CRC:
`v = v>>8 ^ tbl[(b ^ v) & 0xff]` + a progress callback FUN_00406440) -> FUN_0070bf00
(field+0x80 store) -> **FUN_00409260(0) = the ArkRegistryHandler CONSTRUCTOR** ->
**FUN_00409310("Software\\MindArk\\Project Entropia", 1)** (the registry-path STORE —
the reads are lazy: the trace shows ZERO MindArk registry rows, consistent with a
store-only) -> FUN_00409400("Installer", buf, 0x100) (a value read, in-memory) ->
**the log rotation** (`if (obj->field_0x40 == 1) rotate("Entropia.log")` — the trace:
CreateFile Entropia.log/dmp = NAME NOT FOUND @9:40.3387 ✓) -> FUN_00746550 (a field+4
getter) -> the error-object helpers -> return.

## THE EXIT PATH (the -1 mechanism)

- **ExitProcess is NOT imported by the exe**; the CRT `exit` thunk has EXACTLY ONE
  caller: **FUN_007c5310** = the DPVS teardown-exit ("dPVS Unit Sphere Reference
  Count Before NiDPVS Release" + getStatistic(0x72..0x75) = Cameras/Cells/Models/Objects
  Left + DPVS::Library::exit() -> exit). 3 callers:
  - FUN_007b7d50 = **the device-state-bit watcher**: `old = obj->field_0x30;
    cur = obj->vtable[+0x80](); if ((old & 0x08000000) && !(cur & 0x08000000)) {…}
    if ((old & 0x04000000) && !(cur & 0x04000000)) { vtable+0x8c(); vtable+0x9c();
    FUN_007c5310(); }` — a STATE-BIT DROP => the teardown-exit.
  - FUN_007c63f0 (the camera/scene teardown), FUN_00805230 (the release+exit path).

## THE DISPLAY-ENUM CALLER (the evidence chain)

- The exe: **ZERO display-API imports/strings** (the census: no EnumDisplayDevices/
  GetDeviceCaps/GetSystemMetrics anywhere; the only display string = "Direct3DCreate9"
  @0x00A87CC0 + "d3d9"/"D3D9" @0x00A97B4D/@0x00A87CD0 — the runtime D3D9 route,
  never reached in the death run: d3d8 AND d3d9 = 0 trace rows).
- **mac3r.dll = NOT the renderer — the canon correction**: the exe imports
  CMassiveClientCore/CMassiveAdObjectSubscriber (MassiveAdClient3) from it:
  **mac3r = the Massive Inc. in-game ADVERTISING client SDK** (SetImpression,
  EnterZone, MPSessionCreate, SetMaxReceiveKBPS...), 36 exports.
- The exe imports from binkw32: **the Bink VIDEO PLAYBACK set** (BinkOpen,
  BinkDoFrame, BinkCopyToBuffer, BinkOpenDirectSound...).
- **binkw32.dll = the ONLY display-capable loaded module**: its IAT = USER32:
  {ChangeDisplaySettingsA, GetSystemMetrics, CreateWindowExA, GetDC} + GDI32:
  {GetDeviceCaps} (+ the runtime-resolved "GetDeviceCaps" string). WMVCore: GetDC.
- The trace: the 7.4ms gap after the log rotation = PURE CPU (zero I/O rows) ->
  the display enum (Video0 + the Class-key `HardwareInformation.MemorySize` =
  NAME NOT FOUND + Video1) -> 6 clean thread exits -> Process Exit -1.

## THE VERDICT (evidence-graded)

**STRONGLY_SUPPORTED**: the boot-time media/video init (the Bink intro-video route —
the client's standard boot: window -> WinSock -> config/log -> the Bink intro video ->
only THEN D3D9) performs the display query through binkw32's display-capable IAT
(GetDC/GetDeviceCaps/GetSystemMetrics/ChangeDisplaySettingsA — the OS-internal
enumeration on Win10/11 reads DEVICEMAP\VIDEO + the adapter driver key), and on the
degenerate RDP display (6x Microsoft Remote Display Adapter, ZERO PRIMARY_DEVICE,
empty DeviceKeys, single-mode lists, HardwareInformation.MemorySize MISSING) the
init fails -> the state-bit drop path (FUN_007b7d50-class) or the loop-step error ->
FUN_007c5310 -> exit(-1).

THE HONEST BOUND: the exact failing check INSIDE binkw32's chain (which API result it
rejects) = UNVERIFIED (needs a live debug of the death run or a binkw32 RE). The
client-side boot structure + the exit mechanism = CONFIRMED (decompiled, byte-anchored).

## THE UNBLOCK CONSEQUENCES (updated for the morning)

1. A real display environment (GPU-P / physical console / a proper RDP display config)
   remains the primary unblock for the x87 CW (harness v3 ready).
2. A possible cheaper test: an .ini/config that DISABLES the intro video (if the
   client supports it) would skip the Bink display path entirely -> worth a bounded
   config-hunt run (the deep-init's "Installer" value + the lazy registry reads are
   the candidates).
3. The DPVS-exit path (FUN_007c5310) gives a CANON ANCHOR for any future live debug:
   a breakpoint there = the exact failure moment.
