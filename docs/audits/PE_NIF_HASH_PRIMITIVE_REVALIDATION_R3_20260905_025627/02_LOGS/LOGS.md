# LOGS — PE-NIF-HASH-PRIMITIVE-REVALIDATION-R3

Generated 2026-09-05 03:25:25 by 00_CONTROL/revalidate_r3.py.

## Execution order (enforced)

1. Phase 0 identity pins (prompt SHA, R2 source pin, R34 pin).
2. Phase 1 KAT suites via `run_kats.py` subprocesses (corrected / oracle self-vectors /
   R2-literal / wrong-value / three-state controls) — the corrected set MUST pass before
   aggregation; negative controls MUST exit nonzero (actual exit codes recorded in
   02_LOGS/kat_*.json and TEST_RESULTS.json).
3. Phase 1b Node probe (literal R2 declarations executed from the hash-pinned source;
   counterexamples tested against actual executed bytes).
4. Phase 2 corpus aggregation (only after Phase 1 PASS): per-entry identity pass,
   R2-vs-corrected value census, match-count tables, R2/R36 agreement.
5. Phase 3 historical re-sums (R34 / R35 / R2 state) — kept separate from physical
   recomputation.
6. Phase 4 sidecar byte reconstruction + R39 bare-CR dual-policy comparison.
7. Phase 5 gate assembly (three-state) + TEST_RESULTS.json emission.

## Command log

```
03:24:32 PHASE 0 identity pins
03:24:32 PHASE 1 known-answer tests (before any corpus aggregation)
03:24:32 KAT set corrected exit=0 all_pass=True
03:24:32 KAT set oracle_self_vectors exit=0 all_pass=True
03:24:32 KAT set r2_literal_python exit=1 all_pass=False
03:24:32 KAT set wrong_value_controls exit=1 all_pass=False
03:24:33 KAT set three_state_corrected exit=0 all_pass=True
03:24:33 KAT set three_state_r2_coercion exit=1 all_pass=False
03:24:33 PHASE 1b Node probe (actual R2 literal declarations executed, hash-pinned source)
03:24:40 probe exit=0
03:24:40 PHASE 1 PASS — aggregation authorized
03:24:40 PHASE 2 corpus parse + per-entry value comparison
03:24:41 parsed both containers in 0.6s
03:25:24 per-entry python legs computed in 43.4s (iterative sample: 6335 entries / 247.0 MB)
03:25:24 R2-vs-corrected adler32(name)            mismatches 11022/11022
03:25:24 R2-vs-corrected adler32(payload)         mismatches 11022/11022
03:25:24 R2-vs-corrected fnv1a(name)              mismatches 11016/11022
03:25:24 R2-vs-corrected crc32(name)              mismatches 0/11022
03:25:24 R2-vs-corrected crc32(name+0x0A)         mismatches 0/11022
03:25:24 R2-vs-corrected crc32(name+u32size_le)   mismatches 0/11022
03:25:24 R2-vs-corrected crc32(u32size_le+name)   mismatches 0/11022
03:25:24 R2-vs-corrected crc32(payload)           mismatches 0/11022
03:25:25 WROTE 01_RAW/PRIMITIVE_VALUE_CENSUS_FULL.json (11253830 B)
03:25:25 WROTE 01_RAW/PRIMITIVE_VALUE_COMPARISON.json (919217 B)
03:25:25 WROTE 01_RAW/CENSUS_RECOUNT_R3.json (1492 B)
03:25:25 PHASE 3 historical re-sums (R34 / R35 / R2 state)
03:25:25 WROTE 01_RAW/R34_RESUM.json (2176 B)
03:25:25 WROTE 01_RAW/R35_CLAIM_TABLE_PRESERVED.json (7797 B)
03:25:25 WROTE 01_RAW/R2_STATE_RESUM.json (1066 B)
03:25:25 PHASE 4 sidecars
03:25:25 WROTE 01_RAW/SIDECAR_BARE_CR_ANALYSIS.json (7561 B)
03:25:25 PHASE 5 gates assembly (three-state)
03:25:25 WROTE 02_LOGS/TEST_RESULTS.json (21336 B)
```

## Invocations

```
python 00_CONTROL/run_kats.py --set <set> --out 02_LOGS/kat_<set>.json   (x6 sets)
node   00_CONTROL/probe_r2_helpers.cjs 01_RAW/R2_HELPER_PROBE.json
python 00_CONTROL/revalidate_r3.py
python 00_CONTROL/emit_r3_outputs.py
```
