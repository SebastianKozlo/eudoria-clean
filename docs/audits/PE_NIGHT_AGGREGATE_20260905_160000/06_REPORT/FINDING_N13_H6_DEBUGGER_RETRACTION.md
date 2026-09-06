# FINDING N-13 (H6) — THE DEBUGGER-ROUTE RETRACTION + the final honest state of the predicate

**RUN**: H6 — the clean AV-capture harness (the lessons applied: the window check every
iteration; the eip-in-image filter; the AV budget; NO DR breakpoints).

## THE RESULT (decisive + humbling)

- **ZERO AVs** under the plain debugger (105 events, 1 routine C++ throw, exit
  **0x4000001F** @3.2s). NO loader-AV noise either (the earlier "8 identical AVs" =
  the H5 harness's DR-interaction artifacts!).
- **THE H5 "the death = an AV" INTERPRETATION = RETRACTED AS MY INSTRUMENT'S ARTIFACT**:
  the AV exits (0xC0000005) appeared ONLY in the runs with the DR breakpoints armed;
  the plain-debug run = no AV, a different exit class.
- **THE CLIENT'S DEATH UNDER THE DEBUGGER = NON-DETERMINISTIC**: across the session's
  runs: -1, 0xE0710003, 0xC0000005 (with DR), 0x4000001F (no DR) — different classes
  per configuration. The debugger (any form) perturbs the client's protected boot
  (the SUEF neutralizer + the protection interplay).
- **THE ONLY RELIABLE GROUND TRUTH = THE NO-DEBUGGER TRACE**: the DEVICEMAP display
  query (Video0/Video1 + HardwareInformation.MemorySize MISSING on the RDP adapter)
  -> the silent -1 exit @~40ms.

## THE FINAL HONEST STATE OF THE DISPLAY PREDICATE (the H1-H6 arc)

CONFIRMED: the client dies after the display enumeration on the degenerate RDP
environment (6x Remote Display Adapter, ZERO PRIMARY_DEVICE, empty DeviceKeys,
single-mode lists, HardwareInformation.MemorySize absent); the death precedes every
graphics-DLL route (ddraw/d3d8/d3d9 never loaded); the DInput route works (refuted);
the cheap unblock routes are all dead (no switches/config/registry/intro-file); the
boot chain + the orchestrator + the DisplaySubsystem class mapped (the static RE
assets committed).

REFUTED (my artifacts, retracted): the EAX-residue theory (a parse artifact); the
AV mechanism (the DR-interaction artifact); the CreateDCA-fails claim (a marshaling
artifact).

THE REMAINING BOUND: the exact in-module predicate (which call's result the client
rejects) — the debugger route is CLOSED as contaminating; the paths:
(a) the human's display environment (GPU-P / physical console -> the client runs,
    the question dissolves -> the x87 CW measurement becomes possible),
(b) the deep static RE walk of the deep-init 0x405150 to the display query (a fresh
    focused session; the reusable Ghidra project retained),
(c) the conditional-PC model acceptance with the explicit environment bound.

THE INSTRUMENT LESSONS (the H1-H6 ledger): 64-bit DEBUG_EVENT union +16;
Wow64GetThreadContext; the VA-vs-RVA; the hallucinated-GUID trap (×2); the vtable
order (CreateDevice@+0xC); str-vs-bytes marshaling; the window-check-every-iteration
(the event-storm hang); the DR-vs-the-client interaction (the AV artifacts) —
ALL recorded in the findings N-9..N-13 for the QC ledger.
