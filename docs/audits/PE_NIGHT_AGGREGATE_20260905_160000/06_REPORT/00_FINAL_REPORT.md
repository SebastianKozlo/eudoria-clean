# PE_NIGHT_AGGREGATE_20260905_160000 — 00_FINAL_REPORT
## (the display-enum canon run + the manifest-contradiction settlement + the night reports)

**RUN_ID**: PE_NIGHT_AGGREGATE_20260905_160000 (the night continuation run — the queue items'
leftovers that SHOULD have been worked all night; started after the human's 13-minute
challenge; OFFLINE, read-only, zero client runtime)
**ERA**: PCG 9.3.5. **NO CONFLICT** with the second session (its turn ended 15:55:35;
its artifacts read-only by me).

## FINDING N-1 — THE MANIFEST CONTRADICTION SETTLED (byte-level)

Two sessions' claims conflicted: night-child: "No embedded XML manifest in .rsrc";
night-2: "resolved via the exe's embedded VC80.CRT manifest".

**MY BYTE CHECK (the .rsrc resource-directory walk)**: the sandbox Entropia.exe
(SHA E7785430...) .rsrc contains ONLY types **3 (RT_ICON), 14 (RT_GROUP_ICON),
16 (RT_VERSION) — NO type 24 (RT_MANIFEST)**. **The night-child's static evidence is
CORRECT; the night-2 mechanism label ("embedded VC80.CRT manifest") is FALSIFIED at
the byte level.**

**The ACTUAL mechanism (empirical, the ProcMon trace)**: MSVCR80.dll resolved via
`Load Image C:\Windows\WinSxS\x86_microsoft.vc80.crt_1fc8b3b9a1e18e3b_8.0.50727.9680_none_d090cb7c44278b28\msvcr80.dll` = SUCCESS — **the WinSxS-store direct resolution** (the
modern-Windows fallback for VC80 CRT when no manifest exists; ledger label:
WIN_SXS_STORE_FALLBACK). The night-2 EMPIRICAL claim (the imports all load) STANDS;
only its mechanism label is corrected.

## FINDING N-2 — THE DEATH WINDOW DECODED (the -1@40ms class; independent trace read)

The full last-40-operations window of the live-test death (ProcMon CSV, 282,059 rows,
2,193 Entropia.exe rows — my independent read, not the night-2 session's summary):

1. WinMain RUNS: locale/MUI init, WinSock catalog reads, 77 modules Load Image
   (ALL static imports resolve: stlport, wmvcore, d3dx9_30 x2, dsound, dpvs x2,
   dinput8, binkw32, mac3r x2, NxCooking x2, ijl15, PhysXLoader x2, wmasf, msvcp80,
   comctl32...).
2. **The display enumeration** (the classic EnumDisplayDevices signature):
   `HKLM\HARDWARE\DEVICEMAP\VIDEO` → `\Device\Video0` (the adapter key
   `...\Control\Video\{53C87C01-4A58-11EF-AE96-806E6F6E6963}\0000`) → the driver
   class key `HKLM\System\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\00NN`
   → **RegQueryValue = NAME NOT FOUND (Length: 16)** → `\Device\Video1` (the
   BasicDisplay service key) → close.
3. **6x clean Thread Exit → Process Exit: Exit Status = -1.**
4. **d3d8.dll = NEVER LOADED (0 rows); d3d9.dll = NEVER LOADED (0 rows)** — the death
   is BEFORE any D3D route. The exe's only display-adjacent string:
   **"Direct3DCreate9" @0x00A87CC0** (unused before death). **The exe imports ZERO
   display APIs** (the full import-table census: no EnumDisplayDevices/GetDeviceCaps/
   GetSystemMetrics/ChangeDisplaySettings/Direct3DCreate8/9 in any of the 24 DLLs) —
   **ExitProcess is NOT imported** → the -1 exit = **return -1 from WinMain** (the CRT
   path). The enum caller = an in-process DLL or a runtime-resolved route (the
   remaining static-RE bound; candidate: dinput8's device init; needs Ghidra).

## FINDING N-3 — THE DISPLAY ENVIRONMENT IS DEGENERATE (the canon-gap environment side CLOSED)

**THE MEASUREMENT (read-only ctypes/winreg, zero game client, reproducible on any
machine — `display_env_measurement.py`)**:

```
EnumDisplayDevicesA(NULL, iDev, 0) on THIS machine:
  iDev=0 \\.\DISPLAY1 "Microsoft Remote Display Adapter" (RdpIdd_IndirectDisplay)
          StateFlags = 0x04000005  ATTACHED=1, PRIMARY=0, MODESPRUNED=0
          DeviceKey = EMPTY;  modes = EXACTLY 1 (1920x1080@32Hz, 32bpp)
  iDev=1..5: the same RDP adapter, StateFlags = 0x04000000 (NOT ATTACHED, NOT PRIMARY)
          DeviceKey = EMPTY;  modes = EXACTLY 1 (800x600@60Hz)
  => NO adapter carries DISPLAY_DEVICE_PRIMARY_DEVICE (0x2) ANYWHERE.
  HKLM\HARDWARE\DEVICEMAP\VIDEO: Video0 = the {53C87C01...} GUID key;
                                  Video1 = ...\Services\BasicDisplay
```

A 2008-era client's display init (primary-device search + fullscreen mode selection)
operates on: a PRIMARY device, real driver keys (DeviceKey), a mode LIST. This VM
offers **none of the three**: 6 synthetic RDP adapters, zero PRIMARY flags, empty
DeviceKeys, single-mode lists (and the attached one reports **32 Hz**).

**CONCLUSION (evidence-graded)**: the client's display-enum check fails LEGITIMATELY
on this environment — the -1 exit class is now UNDERSTOOD (not mysterious): **the
x87 CW measurement blocker = the degenerate RDP display environment, NOT the client,
NOT the sandbox, NOT anti-debug.** STRONGLY_SUPPORTED (the exact client-side
predicate stays UNVERIFIED — the remaining static-RE bound).

## THE UNBLOCK OPTIONS (for the human's morning decision)

1. **A real display environment** for the runtime VM (GPU-P passthrough / a physical
   console session / a proper non-RDP display config) — then the live test + the x87 CW
   measurement (the harness v3 discipline is ready).
2. **The bounded static RE of the -1 return path** (find the enum consumer + the exact
   predicate; Ghidra; the next-session item) — may reveal a config/env workaround
   (e.g., a registry/ini override) without new hardware.
3. Accept the conditional PC model with the explicit bound (the last-resort M1 option).

## CORRECTIONS TO MY OWN NIGHT REPORT (honesty)

- My earlier `MatchingDeviceID` check was a FALSE NEGATIVE (case-sensitive): the
  class keys DO carry `MatchingDeviceId` (lowercase d). The trace's NAME NOT FOUND
  (Length: 16) value name remains ambiguous in the ProcMon CSV (recorded as-is).
- My 13-minute night report violated the night order's intent (the checklist-vs-night
  error the human caught); this run is the corrected continuation.

## MILESTONE_PROGRESS vector

```
display_enum: the environment side CLOSED (the degenerate RDP adapter set measured,
              zero PRIMARY_DEVICE, 1-mode lists); the client side narrowed to
              "return -1 from WinMain after the enum; caller = a DLL/runtime route;
              exact predicate UNVERIFIED (needs Ghidra)"
manifest:     the contradiction settled byte-level (.rsrc: 3/14/16 only; no 24);
              the MSVCR80 mechanism = WIN_SXS_STORE_FALLBACK (empirical)
files:        the trace CSV independently read (2,193 rows; the full Load Image
              census 77); the exe import census (24 DLLs, zero display APIs);
              the string census ("Direct3DCreate9" @0xA87CC0 only)
excluded:     zero client runtime; zero wiki edits; NO M2; era 9.3.5
NOT_CHECKED:  the exact -1 predicate; the enum's in-process caller; the R-channel;
              the +50.0 semantic direction; the TEZ<->field relation
```

RUN_STATUS = COMPLETED
HARD_STOP_REASON = NONE (the night continues to the next bounded item per the human's challenge)
