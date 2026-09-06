# PE_HOURLY_LOOP — the hourly loop ledger (started by the human's order 2026-09-06)

The discipline: each hour = bounded work units -> package -> commit -> checkpoint ->
continue. The state file = this ledger + the repo commits.

## HOUR 1 — the intro-video config-hunt (the x87 CW unblock test prep)

**STATUS: COMPLETED (the honest negative — all the cheap unblock routes exhausted)**

1. The CLI switch census: NO classic switches (-nologo/-windowed/etc. ABSENT; only
   word-fragment noise) — the switch route DEAD.
2. `wd\Data\Data.ini` = `[Export] Version=9030501` ONLY (no display/video options).
3. The MindArk registry keys EXIST on this machine (HKLM\SOFTWARE\WOW6432Node\MindArk\
   Project Entropia: Installer=NX4NMX8E, the install path, the start-menu folder, the
   installer language; HKCU\Software\MindArk\Project Entropia: the [Language] subkey) —
   the client's lazy registry reads would find real values; NO display options there.
4. 30 .bik files exist (`wd\Data\Video\NNNNN.bik`); the RTTI class
   `.?AVArkDiscipleIntroductionUI@@` @0x77FF44 = the intro UI; the ".bik" string
   @0x67A70C = the extension-format string.
5. **THE DECISIVE NEGATIVE: ZERO .bik opens in the death trace** — the client dies
   BEFORE any BinkOpen file call (the display enum = pure CPU, no file I/O) —
   the missing-intro-video trick = DEAD (nothing video-file-related was reached).
6. CONSEQUENCE: the cheap unblock routes are exhausted; the x87 CW unblock =
   (a) a real display environment (the human's environment decision), or
   (b) the exact-predicate identification via a bounded DIAGNOSTIC DEBUG of the
   death run (H2: the qualified Backend-E harness + a breakpoint at the DPVS-exit
   FUN_007c5310 -> the call stack at the exit = the exact failing path).

## HOUR 2 — the death-run diagnostic debug (PLANNED)

The bounded diagnostic: spawn Entropia.exe under DEBUG_ONLY_THIS_PROCESS (the
qualified harness pattern), breakpoint at FUN_007c5310 @0x007C5310 (the ONLY exit()
caller) + optionally at the display-API boundaries; capture the call stack + the
register state at the breakpoint -> the exact failing call chain. ZERO code patches;
observation only; the kill + the orphan census per the standing discipline.

## HOUR 2 — COMPLETED: the death-run diagnostic debug (the instrument + the findings)

N-9 (06_REPORT\FINDING_N9_DEATH_DIAG.md): the SUEF neutralizer canon fact (FUN_00406da0
patches SetUnhandledExceptionFilter with xor eax,eax; ret 4); the boot registry chain =
LAZY (zero client-registry I/O in the death trace); a routine C++ (STL) exception in
the "Installer"-read chain (first-chance captured; NOT the fatal event); the -1-exit
EAX-residue theory WITHDRAWN (a parsing artifact — the 64-bit DEBUG_EVENT union at +16);
the debug-run divergence documented (the no-debugger trace = the ground truth).
The display predicate: the trace conclusion stands (the display enum -> the -1);
the exact in-module check = the remaining bound (the ProcMon-on-debug-run or the
instruction-level trace = the H3 candidates).

## HOUR 3 — COMPLETED: the DInput route REFUTED (the honest negative)

N-10 (06_REPORT\FINDING_N10_H3_DINPUT_REFUTED.md): the DInput chain decoded (FUN_00864ae0:
DirectInput8Create < 0 -> the abort; the IID {BF798030-483A-4DA2-AA99-5D64ED369700} verbatim
from the binary); the empirical 32-bit probe: ALL the client's DInput calls SUCCEED on this
machine (create S_OK; CreateDevice mouse/keyboard S_OK; EnumDevices S_OK) => the input
hypothesis REFUTED. The instrument lessons (the hallucinated-GUID trap; the vtable +0xC =
CreateDevice; VA-vs-RVA). The predicate hunt continues (the WMV reader / the Bink surface
pre-init = the H4 candidates; the GetDC/GetDeviceCaps empirical probes).

## HOUR 4 — COMPLETED: the display trail mapped (N-11)

The display-API probe (GetDC/GetDeviceCaps/GetSystemMetrics/EnumDisplayDevices all OK;
the v1 CreateDCA-fail claim RETRACTED as my marshaling artifact); the Bink route =
DirectDraw (found the runtime strings) BUT ddraw NEVER loaded => the death PRECEDES all
the graphics-DLL routes; the orchestrator decoded (FUN_004172a0: the ctor sequence incl.
PhysX-with-MessageBox + the ~10-gate chain, any FALSE = the abort); THE DisplaySubsystem
CLASS FOUND (FUN_0048aef0 ctor + vtable + the OS-probe); dpvs.dll = UPX-PACKED (unpacked
cleanly; KERNEL32-only imports + a user32 string => the ordinal-resolution suspect).
THE H5 LEADS: the DisplaySubsystem vtable methods; the DPVS Library init (the 0x7C5xxx
cluster); dpvs's ordinal-resolved user32 call.

## HOUR 5 — COMPLETED: the subsystem forest mapped + the PROTECTION decoded (N-12)

The DisplaySubsystem vtable (3 methods: the dtor/accessor/registration; the class =
a settings holder, NOT the query owner); THE PROTECTION SUBSYSTEM DECODED: FUN_00419390
= the obfuscated API resolver (the cipher s[i] ^= i+0x51; the decoded strings:
kernel32.dll + CreateMutexA + CloseHandle + IsDebuggerPresent + CreateFileMappingA +
FindWindowA => the client anti-debug/protection canon; explains the missing strings!);
the subsystem classes all identified (DisplaySubsystem, WorldSubsystem [FUN_0048e170],
ArkObjectService/ArkClientObjectManagerImpl, PhysX, the string-config holder, the
protection); THE DISPLAY QUERY = IN THE GATE CHAIN (the timing); the H6 plan = the
GATE BINARY-SEARCH DEBUG (DR0/1/2 on the first/mid/last gates -> the last-hit gate ->
decompile its callees = THE PREDICATE).
