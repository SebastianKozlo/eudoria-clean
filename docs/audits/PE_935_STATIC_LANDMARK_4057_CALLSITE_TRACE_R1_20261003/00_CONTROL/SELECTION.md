# SELECTION — PE_935_STATIC_LANDMARK_4057_CALLSITE_TRACE_R1_20261003

## 1. Selected target (single, bounded)

```text
ANCHOR_VA        = 0x0059AB12
CANDIDATE_IMMEDIATE = 4057 (0x00000FD9) — lead, TO BE REPINNED
CANDIDATE_TEMPLATE_ID2 = 4057 — lead, TO BE REPINNED
CANDIDATE_MODEL_A = 218757 — lead, TO BE REPINNED
CANDIDATE_COLLISION_B = 218758 — lead, TO BE REPINNED
NEARBY_IMMEDIATE = 886 — UNKNOWN; only mechanical dataflow if needed for 4057
```

Source of the lead: the deferred lead recorded by
PE_935_PLACEMENT_BRIDGE_DESKTOP_CORRECTION_R1_20261003 (01_ANALYSIS/
DEFERRED_PLACEMENT_LEADS.md §1, preserved there as RECORD ONLY; explicitly
NOT repinned there). This run is the separately authorized execution of that
recorded candidate (its §6 "CANDIDATE NEXT EXPERIMENT — DESIGN ONLY").

## 2. Why this anchor was selected

- The correction cycle closed FAMILY-T (record 4508) to RESULT_LEVEL B and
  explicitly deferred the 4057/0x0059AB12 lead as the next bounded question.
- The human selected model 218757 as a probe object on HUMAN_HISTORICAL
  RECOLLECTION (characteristic static building/landmark, probably one world
  location) — a probe-selection criterion ONLY, not evidence (contract §2).
- The falsifier is sharp and cheap: either the immediate 4057 at this call-site
  reaches a proven template-id consumer (registry lookup FUN_0072F580 ABI or
  an independently proven consumer), or the numeric match with templates.vfs
  id2=4057 is coincidence/unresolved and the lead is rejected for this
  call-site (contract §4).

## 3. Starting epistemic state (contract §2 verbatim — unchanged at selection time)

```text
4057_EXISTS_AS_TEMPLATE_ID = LOCAL_LEAD / TO_BE_REPINNED
4057_TO_A218757_MAPPING = LOCAL_LEAD / TO_BE_REPINNED
B218758_COLLISION_MAPPING = LOCAL_LEAD / TO_BE_REPINNED
IMMEDIATE_4057_AT_0x0059AB12 = LOCAL_LEAD / TO_BE_REPINNED
IMMEDIATE_4057_IS_TEMPLATE_ID = UNVERIFIED
HARDCODED_TEMPLATE_REFERENCE_4057 = UNVERIFIED
CLIENT_CONSTRUCTS_MODEL_218757_HERE = UNVERIFIED
STATIC_BUILDING_INSTANCE = UNVERIFIED
STATIC_LANDMARK_CONSTRUCTION_PATH = UNVERIFIED
WORLD_TRANSFORM_SOURCE = UNKNOWN
PLACEMENT_XYZ = UNKNOWN
IMMEDIATE_886_SEMANTIC_ROLE = UNKNOWN
```

## 4. Non-goals (enforced)

No client launch; no dynamic instrumentation; no network capture; no runtime
packet analysis; no wide placement-subsystem sweep; no all-buildings search; no
automatic map reconstruction; no M1 closure; no M2/M3; no Q1; no PE-MASTER
qualification change; no next-experiment authorization; no history rewrite; no
force-push; no proprietary payload publication; no guessing 886; no accepting
4057 as template ID merely because the number matches; no separate 886 trace.

## 5. Method selection

- Phase 1 data side: own Python 3.12.10 walker of templates.vfs (format from
  canon; implementation independent; calibrated against canon anchors: 5,438
  records / 0 CRC-fail / exact EOF / record id2=4508 @96,496 A=296445), plus
  BNT2 trailer-index lookups for the two candidate names (Models.bnt ->
  "218757.nif"; Volumes.bnt -> "218758.bvi"), index metadata only.
- Phase 2+ code side: own PE-header mapper (pure Python struct) for raw byte
  windows; Ghidra 11.2.1 headless (fresh project, sandbox EXE copy,
  hash-verified) for function boundaries, listing, decompilation, callers/
  callees. Every load-bearing code claim byte-anchored (VA + raw bytes);
  decompiler prose alone is never sufficient (supervisory addition 5).
- Ghidra-derived listing bytes cross-checked byte-for-byte against the raw
  physical EXE via the own mapper (prior-run c10v2 method re-implemented).
