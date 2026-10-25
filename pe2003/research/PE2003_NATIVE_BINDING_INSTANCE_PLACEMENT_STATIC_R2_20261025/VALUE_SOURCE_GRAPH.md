# VALUE SOURCE GRAPH — R2 synthesis (where every transform-relevant value comes from)

RUN_ID: PE2003_NATIVE_BINDING_INSTANCE_PLACEMENT_STATIC_R2_20261025 | Authoring: 2026-10-25T11:18:13Z
Sources: P01_TRANSFORM_FIELD_SOURCE.json, P02_NETWORK_JOIN_AUDIT.json, J01b, J02, B01/B02a. Coordinate-frame discipline: raw native vectors without calibration are candidates only; LOCAL vs WORLD kept separate.

## Node A — NIF file stream (LOCAL, definition data) — CONFIRMED

- Producer: <id>.nif block data → parse subsystem FUN_005b71e0/FUN_00404200/FUN_004045f0 (loader registry 0x619E78, create-fn table) → owner class 0x78 vt 0x5EBBEC via factory FUN_005b2f10 + block reader (vt slot 3, FUN_005b38c0 region).
- Values: owner+0x50..+0x70 floats (defaults −1.0f; final values file-derived), +0x74 gate byte.
- Consumer: FUN_005068f0 (record[0] targets, gate).
- Classification: **NIF_FILE_LOCAL** — definition data only; the two pinned NIF files additionally carry identity-only local transforms (31/31).

## Node B — network wire triplets (WORLD-candidate channel, values runtime-only) — STRONGLY_SUPPORTED

- Producer: FUN_005bbbd0 ntohl-reads wire triplets into the 0x48 record[6] struct (+0x14/+0x20/+0x2C) → FUN_005977b0 pass-2 (EBP=[EDI+0x18] = record[6]) → entity (0x118, vt 0x5E4628) vslots +0x4C/+0x50/+0x58 → FUN_00488b70/FUN_00488cb0 value computation → FUN_005030c0.
- Writer: FUN_005030c0(registry, id, x,y,z, matrix9f): node+0x50/54/58 = (x,y,z)×100.0f; node+0x2C..+0x4C = 9-float rotation matrix; target = 0x130 B vt-0x5E2A3C objects (ctor FUN_00405b50; registry-add FUN_00502e80; attach under registry+0x3C AddChild — J04 69/69).
- Values: NOT statically observable (wire data); representation known (float, ×100.0f scale for translation).
- Identity join to OUR models: **STILL_AMBIGUOUS** (family-level join established by the byte-identical installs 0x405bdf/0x407896; decisive edge registry+0x3C root identity).

## Node C — VM constants/literals (per-model identity data) — CONFIRMED

- Model ids 296445/296446/218757/218758: STOREI literals inside DYN getters of 4508/4057 (outside the attach chain); consumed only across the DYN dispatch boundary → MISSING_EDGE (no static consumer; 0 foreign literal hits in 1936 corpus files + EXE).
- Per-part mesh names + part ext ids: caller init literals → part-object properties (injected before attach).
- f1 property ids 1617 (watch) / 1611 (+1 sibling): semantics UNCHECKED (J02 honest limit).

## Node D — executors/callbacks (no value production) — CONFIRMED

- DAT_A FUN_005c27a0: no-op. DAT_B FUN_00561ee0 → FUN_005541e0: quaternion normalization only (sign flip + clamp) — transforms the values emitted in node A/B records, produces no placement of its own.

## Standing consequence

No edge in this graph yields authenticated world coordinates for models 296445/218757: node A is LOCAL definition data (identity transforms in the files), node B's values are runtime wire data whose object-identity join to our models is unproven, node C has no static consumer. Therefore **WORLD_XYZ_RECOVERED=NO; HISTORICAL_PLACEMENT=NOT_ESTABLISHED; SOURCE_UNKNOWN** — carried exactly, with the family-level join (vt 0x5E2A3C) as the strongest established link and the frontier edges (BLK-R2-01..10) as the only static paths that could change it.
