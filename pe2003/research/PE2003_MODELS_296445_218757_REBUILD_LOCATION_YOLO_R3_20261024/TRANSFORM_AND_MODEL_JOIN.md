# TRANSFORM_AND_MODEL_JOIN — per-model join + transform summary (sanitized)

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
Detailed chain: `docs/object-and-transform-pipeline.md` (repo root).
Rule honored: COMMON mechanism results do NOT close model-specific joins
(R3 0H — no cross-model promotion).

## COMMON chain (both models, same code/censuses) — CONFIRMED

archive mount → resource manager (vtable 0x5E7974; slots
open_nif 0x520EE0 / open_bvi 0x520D80 / open_tga 0x520C20 /
open_dds 0x5209D0; member name = `sprintf("%d")`+extension) → member reader
FUN_00464F30 (hash+CRC gate) → NIF deserializer 0x522010→0x5B7170
("NetI" branch) → root wrapper 0x5EBC1C. Spawn: frame 0x06 → FUN_005bc5a0 →
FUN_00528a40 → FUN_004688d0 → avatar 0x118 B (vtable 0x5E4628) →
FUN_005030c0 → scene attach. Position: 3× f32 LE inside BE envelope;
storage ×100.0 (0x42C80000). Orientation: 3×3 row-major row-vector (v·M) at
obj+0x2C; consumers FUN_004193f0 (world compose) + FUN_00419090 (dPVS).

## Per-model joins (tracked separately)

| Join | 296445 | 218757 |
|---|---|---|
| type-id → definition | CONFIRMED — def 4508.obj (IDs 296445+296446 in the E18 macro) | CONFIRMED — def 4057.obj (IDs 218757+218758 in the E18 macro) |
| definition → model open | CONFIRMED-NEGATIVE static (0 direct callers ×3; 0 qualified virtual sites of 5776 indirect CALLs / 576 444 instructions); OPEN dynamic | same COMMON negative tested with model-agnostic censuses; per-model edge remains OPEN dynamic |
| spawn packet → instance | CONFIRMED (frame 0x06 chain) | CONFIRMED (same COMMON chain) |
| paired volume | 296446.bvi present (21×48 B); pairing NOT PROVEN code-side | 218758.bvi present (18×48 B, W1 discovery); pairing NOT PROVEN code-side |
| SAME_MODEL vs 9.3.5 | IDENTICAL_BYTES (3-way) — NOT interchangeable with 218757's VARIANT_SAME_ID | VARIANT_SAME_ID (4.1.0.12 vs 10.1.0.0 payloads) |
| Role expectations (UNVERIFIED) | possibly effect-asset (instance roster may be flare/particle anchors) | possibly prefab (roster would be per-outpost instances) |

## Open transform edges (both models)

- Live orientation source (FUN_005030c0 param_5 supplier): UNVERIFIED (W3-11).
- Position-slot writer FUN_005a7b30 body: PLAUSIBLE (sibling FUN_005a7bd0
  proven for the target triple; own body not decompiled).
- Avatar +0x44 (object id) writer slot target: UNVERIFIED.
- Consumer-layer clone-vs-identity (one loaded root serving many placements):
  UNVERIFIED (no live consumer callsite).

## Class correction (applies to both)

Avatar class 0x5E4628 (0x118 B) ≠ camera-record class 0x5E49B8 (0x54 B);
transform consumers operate on the avatar class (W2→W3 correction, CLR-01;
original wrong rows preserved append-only).
