# 04_RUNTIME — NOT RUN

Runtime/game execution is explicitly OUT OF SCOPE for PE-NIF-CLAIM-EVIDENCE-LOCK-R2
(per the binding prompt: "no runtime/game/Ghidra").

NOT executed in this run:
- no PE.exe / Entropia.exe / any game client,
- no emulator or compatibility layer,
- no Ghidra / x32dbg / Frida / apitrace session,
- no historical run driver (no R29-R40 driver, no R1 control script),
- no PE_AUTO_LOOP relaunch or modification (PE_AUTO_LOOP.json read-only; its hash
  difference vs older manifests is a mutable pointer, not corruption).

This run is a static evidence-correction package: physical container re-reads,
counter/normalization/wording corrections, lossless manifest sidecars, executable
gates, and a bounded documentation publication. Every claim it touches remains at
its run-derived evidence level; nothing here promotes any runtime-gated claim.
