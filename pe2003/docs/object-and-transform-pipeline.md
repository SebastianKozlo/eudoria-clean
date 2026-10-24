# Object and transform pipeline — definition → manager → reader → NIF → spawn → avatar → scene

RUN_ID: PE2003_MODELS_296445_218757_REBUILD_LOCATION_YOLO_R3_20261024.
The full statically-proven chain on the unpacked client build
(SHA256 56178993…). Every edge below is a row of the private
`RESOURCE_INSTANCE_JOIN_2003.csv` (E01-E21, W3-01..12, R3-01..06) with VA +
byte evidence; statuses use the exact taxonomy
(CONFIRMED / STRONGLY_SUPPORTED / PLAUSIBLE / UNVERIFIED / REJECTED).

## 1. Archive mount (E01) — CONFIRMED

Client init FUN_0045AD40 → FUN_00478950 → FUN_00520780 mounts
`\models\`+`.ark` (also `\textures\`, `\volumes\`).

## 2. Resource manager (E02) — CONFIRMED

Resource-manager object, ctor FUN_00520600, vtable **0x5E7974**, four open
slots by extension:

| Slot | Function | Extension |
|---|---|---|
| [0] | 0x520EE0 open_nif_by_id | .nif |
| [1] | 0x520D80 open_bvi_by_id | .bvi |
| [2] | 0x520C20 open_tga | .tga |
| [3] | 0x5209D0 open_dds | .dds |

Member name is constructed as `sprintf("%d", id)` + extension (byte-verified:
push format `"%d"` @0x610400, call sprintf via IAT, push `".nif"` @0x610368)
— e.g. model id 296445 → member `"296445.nif"`.

## 3. Member reader (E04) — CONFIRMED

Shared ark member reader FUN_00464F30: hash lookup + CRC gate + raw read;
call census 5 sites.

## 4. NIF deserializer (E06) — CONFIRMED

FUN_00522010 → FUN_005B7170 magic gate ("NetI" → FUN_005B71E0 NiStream load)
→ root wrapped 0x28 B, vtable **0x5EBC1C** (FUN_005B5110). NIF 4.1.0.12
payloads match the NetI branch. No ID-keyed cache in the open path (E12/E21:
fresh re-read + re-parse per call, fresh wrapper, SmartPtr refcount;
consumer-level clone-vs-identity UNVERIFIED).

## 5. Definitions and the binding edge

- 2003 definitions are ArkScript DLOB bytecode members in Scripts.ark (there
  is NO templates.vfs on the CD-trial corpus):
  `4508.obj` (IDs 296445+296446) and `4057.obj` (IDs 218757+218758).
- Type-id → definition lookup: FUN_00441230 (engine+0x10058 tree, 33-callsite
  census) — CONFIRMED (W3-08).
- Resource-ID constants byte-verified inside the definition CODE (E18): both
  definitions carry the identical attach-resource-pair macro
  `7700FEDE 00000014 <ID> 7700FDAC 00000014 7700FEEB 00000008`
  (4508: 0x000485FD @~664 / 0x000485FE @~580; 4057: 0x00035685 @456 /
  0x00035686 @~372).
- **THE OPEN EDGE (E08/E20/W3-09/R3-06): definition → open_nif has NO static
  consumer on build 56178993.** 0 direct callers (verified 3×), 0 qualified
  virtual dispatch sites (censuses 5776 indirect CALL sites / 576 444
  instructions, multiple pattern variants); holders reachable only via the
  WinMain stack client → facade → manager. The SFO/0x415xxx candidate was
  REJECTED-PRECISELY (scene-node bookkeeping, zero open calls). The client
  has no `0x7700xxxx` interpreter (E19). Best-supported model: bytecode-driven
  open executed server-side or via a non-token path; the next edge is
  DYNAMIC-ONLY.

## 6. Spawn (W3-01..W3-03) — CONFIRMED

Network frame type **0x06** → frame dispatcher FUN_005bc5a0 (switch over 12
frame types 0x05/0x06/0x14/0x17/0x33/0x34/0x50/0x51/0x60/0x71/0x82/0x90) →
wire parser FUN_00528a40 → engine vtable 0x5E4070 slot +0x18 =
FUN_004688d0 → `operator_new(0x118)` avatar, ctor FUN_004889c0, vtable
**0x5E4628** → init slot +0xAC FUN_00488b10 → position floats → avatar
slots → FUN_005030c0(scene, id, x, y, z) → scene attach.

## 7. Transform rules — CONFIRMED (mechanism)

- Wire: envelope u32/u16 BIG-ENDIAN; POSITION = 12 raw bytes = 3 × f32
  LITTLE-ENDIAN (sub-types 1/5 body, 2 array elements).
- Storage: scene obj+0x50/+0x54/+0x58 = position × **100.0** (0x42C80000 at
  VA 0x5E412C, referenced 9× inside FUN_005030C0).
- Orientation: 9-float block at obj+0x2C..+0x4C; format 3×3 **ROW-MAJOR
  ROW-VECTOR (v·M, DirectX-style)** proven from consumer math (FUN_0041a4d0:
  out[j] = Σ_k v[k]·M[k*3+j]); world-compose consumer FUN_004193f0 (node
  vtable slot +0x98), dPVS consumer FUN_00419090 (slot +0xB0).
- Live orientation source (who supplies the real 9 floats to FUN_005030c0
  param_5): UNVERIFIED — all traced static callsites pass 0/unresolved (W3-11,
  frontier item b).

## 8. Class correction (W2→W3)

The 0x488xxx transform consumers operate on the AVATAR class (0x118 B,
vtable 0x5E4628), NOT on the 0x54-B record class 0x5E49B8 — the latter is a
separate camera-record class (6 engine-init instances). Original wrong rows
preserved append-only; correction ledgered (CLR-01).

## 9. Renderer side (statically mapped)

Scene-graph node class 0x130 B (vtable 0x5E2A3C, ctor 0x405B50; 59+ slots
incl. +0x60 update / +0x94 bounds / +0x98 world compose / +0xB0 dPVS / +0xD0
render-list attach); NIF root wrapper 0x5EBC1C; camera child 0x38 B
(0x5E32F8). Which visual reaches the renderer for a given live instance is
the same OPEN dynamic edge as §5.

## 10. Where values come from (the standing result)

Instance values (position/orientation/identity) arrive only via network
frames at runtime. The client holds an id-hash runtime roster
(FUN_00503940 lookup / FUN_00502E80 insert) populated only from network
frames. The local 2003 corpus contains no instance data (see
world-data-and-placement.md). Consequently this pipeline is a MECHANISM
result; authentic historical placements are NOT recoverable from local data.
