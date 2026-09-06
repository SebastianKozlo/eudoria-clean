# FINDING N-12 (H5) — THE DEATH MECHANISM = AN ACCESS VIOLATION caught by the client's own SEH

**RUN**: H5 of the hourly loop — the DisplaySubsystem vtable + the gate-bisection + the AV capture.

## THE FINDINGS

1. **THE DisplaySubsystem VTABLE MAPPED**: @0x00A7B988 (from the ctor bytes `c7 06 88 b9 a7 00`):
   vtable[0]=0x0048B0A0 (the dtor: `mov [esi],vtable; call [FUN_0048afe0-ish]; ret 4`),
   vtable[1]=0x0048B520 (50 B), vtable[2]=0x0048B0E0 (30 B: a compact virtual
   dispatcher: `movzx ecx,[eax+0x60]; mov edx,[eax+0x5c]; call edx`) — + the data
   after (1.0f, a pointer 0x00A9FAA4, 0x0048B990, 0x007E19D0 ×2, the "WAVE_S03..."
   strings). The methods = small; the display query NOT in them.
2. **THE SEH-FRAME FUNCTION @0x48B110** (the cookie-protected ctor: FUN_00471060 +
   FUN_00725950) + the created functions at 0x48B520/0x48B0E0 — the DisplaySubsystem's
   construction neighborhood mapped.
3. **THE GATE-BISECTION RUN 1 (the first 4 gates @ DR0-3)**: NO gate hits — **the death
   precedes the orchestrator's gate chain** (or the DR arming under the changed harness
   config — recorded honestly as ambiguous; the run's exit = 0xC0000005!).
4. **THE DECISIVE DISCOVERY — THE DEATH IS AN ACCESS VIOLATION**: the debug runs
   consistently exit **-1073741819 = 0xC0000005 (ACCESS VIOLATION)** — NOT a clean -1!
   The mechanism: the display init on the degenerate display data (the RDP adapter's
   absent HardwareInformation.MemorySize / the empty structures) **crashes with an AV**;
   the client's OWN SEH catches it (with the SUEF-neutralized crash path) -> the
   controlled teardown -> the **-1 exit observed without the debugger**. THE -1 = the
   client's own crash-handler's exit code!
5. **THE LOADER-AV NOISE (the instrument lesson)**: 8+ IDENTICAL first-chance AVs at
   t≈0.063s (exc_addr=0x0, eip=KERNELBASE 0x754b71de) = the WOW64 loader's benign
   probing — NOT the crash. The real crash = LATER (t>2s debug-time). A working
   AV-capture needs the loader-window filter (ignore AVs before the main image runs).
6. **THE ALWAYS-CONTINUE DISCOVERY**: with ALL the AVs continued (DBG_CONTINUE), the
   client RUNS (>240s, not dying!) — the debugger-policy sensitivity documented (the
   no-debugger ground truth = the -1@40ms; under the debugger the flow diverges).

## THE HONEST STATE

THE PREDICATE NARROWED TO THE MECHANISM: **an AV inside the display-data path, caught
by the client's SEH, exiting -1**. The exact crashing instruction = STILL UNCAPTURED
(the harness iterations: the AV-noise filter + the last-AV-overwrite + the hang bugs —
all recorded; the working capture = the H6 item: filter the loader AVs (t<1s /
exc_addr=0), capture the first post-loader AV's EIP + the raw stack = the failing
instruction + the chain).
