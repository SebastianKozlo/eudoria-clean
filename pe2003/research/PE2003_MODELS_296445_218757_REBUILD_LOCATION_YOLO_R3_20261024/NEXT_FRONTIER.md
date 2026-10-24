# NEXT_FRONTIER — what comes next after R3

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Full roadmap: `docs/reconstruction-roadmap.md` (repo root). Priority order:

1. **(a) FIRST_MISSING_EDGE — dynamic capture of a real model open**
   (definition→open for a live instance; instrumentation of the open slots
   0x520EE0/0x520D80 / facade vtable 0x5E796C +8..+0x14). Static surface is
   exhausted (CONFIRMED-NEGATIVE; 0 direct callers ×3, 0 qualified virtual
   sites among 5776 indirect CALLs / 576 444 instructions). Do NOT re-run
   static censuses on build 56178993 for this edge.
2. **(b) live orientation source** (FUN_005030c0 param_5 supplier) —
   co-dependent with (a) on a running session.
3. **(c) server-side 0x7700xxxx execution model** (session capture /
   server-side analysis).
4. **(d) PCG demo NSIS payload recovery** (blocked at block #40) — corpus
   work, independent of a live session.
5. **(e) terrain 50.bnt era-split decode** (both versions; requires
   explicit authorization) — prerequisite for any future world-position
   calibration (the anchor problem).

Standing: ADVISORY_PENDING_EXTERNAL_POSTAUDIT; CANONICAL_GATE_EFFECT=NONE.
Locations of the two models are recoverable ONLY via (a)/(c) — no local-data
path exists (exhaustive negatives with denominators).
