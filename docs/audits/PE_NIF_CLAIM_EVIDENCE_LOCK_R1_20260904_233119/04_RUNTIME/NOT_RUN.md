# 04_RUNTIME — NOT RUN

Runtime analysis is OUT OF SCOPE for PE-NIF-CLAIM-EVIDENCE-LOCK-R1.

- No game execution (PE.exe / Project Entropia client was NOT started).
- No emulator, no D3D8 tracing, no Frida/x32dbg/ProcMon instrumentation.
- No Ghidra project opened or modified.
- No historical driver from runs R29-R40 (or any other run) was executed —
  all verifications in this round are NEW read-only controls (control_r1.cjs)
  over existing artifacts and the two original BNT2 containers.

Consequences for claim statuses (deliberate, not a failure):
- All engine/runtime semantics claims (G3D class roles, TEXT mode runtime
  behavior, material slot runtime meaning/M3-5B, morph delta-triple meaning)
  remain UNVERIFIED / STRONGLY_SUPPORTED / PLAUSIBLE at their current levels.
- The missing-for-stronger column of CLAIM_MATRIX.csv names runtime evidence
  where it is the natural upgrade path; obtaining it is future work, subject
  to a separate authorization.
