# FINDING N-9 (H2) — THE DEATH-RUN DIAGNOSTIC DEBUG: the results + the honest state

**RUN**: PE_M1_DEATH_DIAG (H2 of the hourly loop): the bounded diagnostic debug of the
-1 death — the qualified Backend-E pattern (DEBUG_ONLY_THIS_PROCESS; the x64 DR-write
route per the FACT2 lesson; armed on all 6 threads; the DR0/DR1/DR2 = the message
loop/LOOP-STEP/DPVS-exit entries; zero code patches; kill + death proof + orphans clean).

## THE INSTRUMENT LESSONS (my own bugs, caught + fixed in-flight)

1. The 64-bit-python DEBUG_EVENT = the union at offset **16** (4 bytes padding) — my
   v1/v2 read the padding as the exit code ("0") — **my "EAX residue" theory of the
   -1 is WITHDRAWN** (a parsing artifact).
2. GetThreadContext from 64-bit python on the WOW64 thread needs **Wow64GetThreadContext**
   (the v3-harness lesson applied).
3. The LOAD_DLL base = lpBaseOfImage @union+8 (not +16).

## THE FINDINGS

1. **THE SUEF NEUTRALIZER DISCOVERED (a canon fact)**: FUN_00406da0 = the client's
   anti-crash component: it locates `SetUnhandledExceptionFilter` in kernel32 and
   **patches it in-process via WriteProcessMemory with `33 C0 C2 04 00`
   (xor eax,eax; ret 4)** — neutralizing any external crash-dump handler installation
   (and interacting with debugger-driven second-chance handling — explains the weird
   exit codes under debug).
2. **The boot's registry-read chain is LAZY**: the full trace census = 1,496 registry
   rows, ZERO client-registry opens (no MindArk/Entropia paths ever opened before the
   death); the ArkRegistryHandler reads return 0 on a not-yet-opened key (no I/O).
   The deep-init's "Installer" read + the registry-path store = in-memory only.
3. **A C++ exception (0xE06D7363) in the boot**: first-chance-captured under the
   debugger: the chain = FUN_00409400 (the registry-value reader, 0x40943f) ->
   stlport.5.1.dll (0x37ba160) -> MSVCR80 _CxxThrowException — an STL exception in
   the "Installer"-read chain. Its boot position (debug-slowed ~2.9s ~ the ~30ms
   real-time point) = the pre-log-rotation "Installer" read. **PLAUSIBLY ROUTINE**
   (a caught exception; the client continues; the no-debugger trace shows no anomaly
   there) — NOT established as the fatal event.
4. **The debug-run divergence**: under the debugger the flow + the exit code differ
   (the throw visible; the SUEF neutralization + the NOT_HANDLED propagation interplay;
   the exit 0xE0710003 vs the no-debugger -1). THE NO-DEBUGGER TRACE REMAINS THE
   GROUND TRUTH: the fatal event = the display enumeration -> the -1 exit.

## THE HONEST STATE OF THE DISPLAY PREDICATE

CONFIRMED (the trace, N-2/N-3/N-5): the client dies right after the display
enumeration (the DEVICEMAP/Class-key reads; HardwareInformation.MemorySize MISSING
on the RDP adapter), before any D3D9 creation, before any .bik open, in the
deep-init/loop-entry region. UNVERIFIED: the exact in-module predicate (which call's
result the client rejects). The candidates: the binkw32 display-surface route (the
only display-capable loaded module) or the OS internals behind a display query.
The next bounded step: the ProcMon-on-debug-run discriminator or the deep-init
instruction-level trace of the display-enum moment.
