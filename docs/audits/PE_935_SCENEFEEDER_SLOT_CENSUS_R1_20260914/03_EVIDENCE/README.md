# 03_EVIDENCE — PE_935_SCENEFEEDER_SLOT_CENSUS_R1_20260914

All run evidence for this small census lives in the sibling directories and is fully
reproducible from the physical EXE alone:

- `../01_RAW/VTABLE_AND_SLOTS.txt` — the physical vtable dump (raw .rdata bytes hexdump +
  per-slot entries), the executor's own RTTI chain walk (vtable -> COL -> TD -> name), and
  the slot-index map of the six contract functions.
- `../01_RAW/VTABLE_SLOT_MAP.json` — machine-readable sidecar of the same walk.
- `../01_RAW/SLOT_DISASSEMBLY.txt` — THE primary evidence: full capstone x86-32 listing of
  all six slot bodies with addresses, raw bytes and mnemonics, body-end derivation
  (padding/terminal/next-entry evidence), script-flagged window-field access candidates, and
  the call census per slot, plus the one-hop identification block (thunk resolution +
  function-start caller counts used for boundary validation).
- `../01_RAW/POSITIVE_CONTROL_005094C0.txt` — the FUN_005094C0 window: raw hexdump,
  byte-exact comparison against the contract-expected pattern, own decode, 9/9 semantic
  checks, verdict PASS.
- `../02_ANALYSIS/SLOT_ACCESS_CENSUS.json` — machine-readable per-slot access/call census.
- `../02_ANALYSIS/SCENEFEEDER_SLOT_CENSUS.csv` — the mandatory 6/6 census table.
- `../02_ANALYSIS/ONE_HOP_FLOW.md` — the minimal dataflow documentation (stops at first
  call) and the boundary-validation notes.
- `../00_CONTROL/` — the binding contract, the measured input identities, and the four
  run-local scripts (independently written; SHA256-hashed in `SCRIPT_SHA256.csv`).

No separate additional evidence artifacts were needed for this run: the six functions total
159 bytes of code, so the complete disassembly listing above IS the raw evidence, and no
callees were decoded (dataflow-stop rule), so no callee dumps exist by design.
