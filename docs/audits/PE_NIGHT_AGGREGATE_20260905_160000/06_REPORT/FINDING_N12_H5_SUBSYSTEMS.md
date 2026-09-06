# FINDING N-12 (H5) — THE SUBSYSTEM FOREST MAPPED + THE PROTECTION SUBSYSTEM DECODED

**RUN**: H5 of the hourly loop — the DisplaySubsystem vtable + the orchestrator's ctor forest.

## THE FINDINGS

1. **THE DisplaySubsystem VTABLE** @0x00A7B988 (3 methods; the 4th dword = 1.0f data):
   VT[0] = 0x0048B0A0 (the DESTRUCTOR: the vtable restore + FUN_0048AF30 member teardown
   + the conditional delete); VT[1] = 0x0048B520 (49 B, 1 call — a small accessor);
   VT[2] = 0x0048B0E0 (807 B, 17 calls = the REGISTRATION method: pushes the callback code
   pointers 0x9A6408-0x9A6580 + the register helpers). The DisplaySubsystem = a SETTINGS
   HOLDER; the ctor does flags + the OS-version probe — NOT the display query.
2. **THE PROTECTION SUBSYSTEM DECODED (a canon find)**: FUN_00419390 = the OBFUSCATED
   API RESOLVER: the cipher = **`s[i] ^= i + 0x51`**; the decoded strings:
   **"kernel32.dll"** + **"CreateMutexA"** + "CloseHandle" + **"IsDebuggerPresent"** +
   "CreateFileMappingA" + "FindWindowA" — the client's ANTI-DEBUG/PROTECTION init
   (the obfuscation explains the missing strings in every census!). The mutex-gate
   (FUN_00407270 = the single-instance check) + IsDebuggerPresent + FindWindowA = the
   triple protection. The protection = NOT the -1 cause in the no-debugger trace runs.
3. **THE SUBSYSTEM CLASSES (the orchestrator's forest, all identified)**:
   DisplaySubsystem (FUN_0048aef0), **WorldSubsystem** (FUN_0048e170!),
   ArkObjectService/ArkClientObjectManagerImpl (FUN_004a9ba0), the PhysX init
   (FUN_00857c90 + the MessageBox string), the string-config holder (FUN_00418630
   inside the 0x160-object), the protection (FUN_00419390), + the ~10-gate chain.
4. **THE DISPLAY QUERY = IN THE GATE CHAIN** (the timing: the orchestrator runs after
   the log rotation; the DEVICEMAP reads = the last activity). The gates (0048e7c0,
   00415d70, 0041b4b0, 00416390, 00467e60, 00459270, 0044c8e0, 004736c0, 00984610,
   0043f060, 00418010) = the small check functions; the real display init = what the
   failing gate calls. THE NEXT PROBE (H6): the GATE BINARY-SEARCH DEBUG — DR0/DR1/DR2
   on the first/middle/last gates -> the last-hit gate brackets the failure -> decompile
   its callees = THE PREDICATE.

## THE HONEST STATE

The display query remains unlocated after H5 (the subsystem ctors = holders, not the
query owner). The hunt's efficiency decision: the live gate-progression probe (2-3
debug runs) over the continued static forest-walk.
