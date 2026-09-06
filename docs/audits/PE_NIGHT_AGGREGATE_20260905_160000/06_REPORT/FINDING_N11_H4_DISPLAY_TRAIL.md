# FINDING N-11 (H4) — THE DISPLAY-INIT TRAIL MAPPED: the DisplaySubsystem found; the trail narrows

**RUN**: H4 of the hourly loop — the display-API probes + the orchestrator/ctor hunt.

## THE FINDINGS

1. **THE DISPLAY-API EMPIRICAL PROBE (32-bit, the sequential call test)**: GetDC = OK;
   GetDeviceCaps = OK (32bpp, 1536px); GetSystemMetrics = OK (1536x864);
   **EnumDisplayDevices = OK (ok=1, StateFlags 0x04000005 — the SAME degenerate flags as
   N-3!)**; CreateDCA("DISPLAY") = **WORKS in the v3 probe** (the v1's hdc=0 = MY marshaling
   artifact [str-not-bytes] — the v1 "CreateDCA fails" claim RETRACTED; the v3 with bytes +
   SetLastError = a valid handle, err 0).
2. **THE DINPUT ROUTE = REFUTED** (H3, unchanged).
3. **THE BINK ROUTE = "DirectDraw"**: binkw32's runtime strings include DirectDraw /
   DirectDrawCreate / SetDirectDraw — **Bink's display route = DirectDraw** — BUT the trace
   shows **ddraw.dll was NEVER loaded/attempted** (0 rows; the full 77-module census
   re-verified: no ddraw/d3d8/d3d9) => **the death PRECEDES all the graphics-DLL routes**.
4. **THE ORCHESTRATOR DECODED (the decisive structure)**: FUN_004172a0 (the deep-init's
   tail call) = the subsystem-init orchestrator: the ctor sequence (0x10/0x1c/0x60/0x28/
   0x160-byte objects; FUN_004926e0/0048aef0/0048e170/00857c90=PhysX[with the MessageBox
   string "PhysX physics system can not be initialized..."]/0048ef00/00418c20/00418570/
   004a9ba0/00419390/004123d0) + **the ~10-gate chain** (0048e7c0→00415d70→0041b4b0→
   00416390→00467e60→00459270→0044c8e0→004736c0→00984610→0043f060→00418010 — each must
   return TRUE; ANY FALSE = the abort -> the -1).
5. **THE DisplaySubsystem CLASS FOUND**: FUN_0048aef0 = its ctor (**sets
   `DisplaySubsystem::vftable`** + FUN_007c5410(1,1,0)=flags + FUN_0048adf0()=the
   OS-version probe [FUN_005af250 queries; the 0x11/0x13 branches; DAT_00ba7348 = the
   OS class]). The ctor itself does NOT do the display query => **the query lives in the
   DisplaySubsystem vtable methods OR the DPVS Library init** (FUN_007c5410 sits in the
   same 0x7C5xxx DPVS cluster as the teardown-exit FUN_007c5310!).
6. **dpvs.dll = UPX-PACKED** (unpacked cleanly with UPX 4.2.4: 311,296 B from 159,744;
   the LOCAL-ONLY unpacked copy at 01_RAW\dpvs_unpacked.dll): its REAL import table =
   **KERNEL32 ONLY (73 imports)** + one "user32" string => dpvs loads user32 at RUNTIME
   and resolves BY ORDINAL (no name strings!) — **the display query could be dpvs's
   user32-by-ordinal call** (the H5 candidate).

## THE HONEST STATE

The display-enum caller = STILL UNLOCATED (the trail: the DisplaySubsystem vtable
methods + the DPVS Library init + dpvs's ordinal-resolved user32 call). The empirical
facts stand: the degenerate display environment (measured), the death AFTER the DEVICEMAP
reads (trace), the graphics-DLL routes never reached, the DisplaySubsystem class = the
owner of the display init (the class identity = a NEW canon anchor).
