# X87 RUNTIME AUDIT - EU935-M1 (the x87 control word disposition)

PE-MASTER in-session audit content, persisted verbatim (formatted; no content
changes).

1. INTENDED MEASUREMENT: site-local CW read at FDIV @0x0098CE5A /
   FLD @0x0095B2BC, N=10/site + fallbacks (design run 57a8d96 - verdict
   PENDING design-review, superseded by execution attempts).
2. EXECUTION POINT: post-boot, foliage chain execution.
3. BLOCKER: the client exits -1 at display enumeration (imports all load;
   WinMain runs); the VM reports 6x Microsoft Remote Display Adapter, ZERO
   PRIMARY_DEVICE, empty DeviceKeys, single-mode lists,
   HardwareInformation.MemorySize missing.
4. PHYSICALLY EVIDENCED: ProcMon trace 2,193 rows (LOCAL-ONLY), the
   night-aggregate display-enum canon N-2/N-3, the boot chain fully
   decompiled, all cheap unblock routes measured negative.
5. LOAD-BEARING: YES - the PC condition carries the engine-parity arithmetic
   claims.
6. PC=24 WOULD BREAK 14,104/229,376 real lerp values (6.15%) - it CANNOT flip
   an accepted claim because the claims are already CONDITIONAL.
7. M1 CONTRACT: the V4 HONEST LIMITS carry the conditional model - the
   contract does NOT require the measurement, it requires the honest
   disposition.
8. Gate A permits the honest BLOCKED-UNKNOWN with the exhaustive-negative
   record - SATISFIED.
9. A real display / GPU-P / physical-console experiment is a HUMAN DECISION
   (paths: (a) real display env, (b) instruction-level Ghidra predicate trace
   H3, (c) conditional-PC acceptance) - NOT ordered by this audit, NOT
   performed.

## DISPOSITION

- X87_CW_STATUS = UNMEASURED / ENVIRONMENT_BLOCKED.
- X87_CW_M1_CLOSURE_BLOCKER = CONDITIONAL (the conditionality is documented
  and binding; acceptance is a human/Desktop decision).
- CONTRACT_BASIS = POM §13 Gate A + V4.1 HONEST LIMITS.

No patching of Entropia.exe was performed; no GPU experiments started.
