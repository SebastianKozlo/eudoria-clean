# PE_M1_GEOREF_P_DATUM_R1 — 00_FINAL_REPORT

**RUN_ID**: PE_M1_GEOREF_P_DATUM_R1_20260905_154841
**QUEUE**: M1 execution queue item #3 (georef/P-DATUM) — the night order, OFFLINE (zero client runtime)
**ERA**: PCG 9.3.5 (primary); cross-era bounds explicitly labeled
**EXECUTION**: direct by pe-master-auditor (Task endpoint unavailable); read-only on originals
**CONFLICT-AVOIDANCE**: the runtime track (#1/#2) is owned this night by the second
executor session (its artifacts observed live: live_test 15:46:56, death-trace 15:49:43,
trace scripts 15:53); this run touched ZERO runtime assets.

## P0

Where does the runtime take the world georeference from (datum/origin/anchoring)?

## THE ANSWER (composed, evidence-graded)

### CONFIRMED — the world datum is the GLOBAL HEIGHT FIELD, not the TDF tiles

1. **Origin/spatial frame**: the world frame = the 257×257 global height texture
   (Textures.bnt entry 429259, `.dat`, 198,191 B, SHA256
   `0BADB42EC131EE53C49E63EADEE529AA18A68A31D0CF16A57694488FF3333412`):
   origin corner (-65,536,-65,536), 512-unit texels, world span **131,072 units (2^17)**
   [prior iter023/028 evidence, tonight independently re-verified].
   The ArkHeightTree quadtree (root half 65,536) indexes THIS frame; its leaves
   carry NO tile references [iter028].
2. **Height datum**: texel t = 16-bit fixed-point in (B<<8|G) channels (R = a separate
   field, role unresolved); **height = (t-128)×5 m**. INDEPENDENTLY RECOMPUTED tonight
   over all 66,049 texels: land >0m = **79.6%** (prior iter029: 79.2% — consistent),
   height range **-639.43..+638.91 m** (theoretical (t-128)×5 bounds fit).
3. **The +50.0 slot datum — BYTE-LOCKED at instruction level** (resolves the iter028
   honest-bound #4 "the slot format's +50.0 datum intent — unverified"):
   - the slot packer `FUN_00991a20` = `{dst, value, format}` storing **2×f32:
     dst[0]=value, dst[4]=format** (decoded from the raw bytes tonight);
   - BOTH slot-fill callers (call sites `0x009482E9`, `0x0094839A`, `0x00949181`)
     execute **`FADD qword [0x00A81D20]`** — the f64 constant 50.0 (the census
     singleton) — i.e. **the height value gets +50.0 ADDED before slotting**;
   - the format field value = **50.0f from `0x00A7AFA8`** (f32 50.0; loaded by the
     callers right before the packer call);
   - the engine water level **10.0f @`0x00A7B128`** re-verified byte-exact (f32).
   - REMAINING BOUND (honest): the SEMANTIC DIRECTION of the +50.0 (which two frames
     it converts between) needs the caller-of-caller dataflow — bounded out of this
     run (no Ghidra session tonight; the instruction-level fact is closed).
4. **Era-stability of the TDF-header conclusion**: the 9.3.5 terrain.bnt
   (`pcg_install\Data\Terrain\terrain.bnt`, 125,064,817 B, trailer `BNT2`,
   58,451 entries) — ALL headers parsed (58,451/58,451, 0 bad): 58,450 standard
   tiles (data_size=2100, dim=32) + 1 overview (56221/237) — the SAME class
   structure as the 2003 50.bnt. The header x/y fields = **zone/layer IDs, NOT
   grid coordinates** (x: 39 unique in [1..44]; y: 6,200 unique in [1..45,216];
   **6,747 duplicate (x,y) pairs**) — a grid coordinate would be unique per tile.
   CONFIRMS the 2003-era conclusion ("zone/layer ID") as era-stable.

### BLOCKED-UNKNOWN — the per-tile placement key (the cell-stream class)

The 9.3.5 terrain tiles are SEQUENTIALLY named (00000000.tdf..) and their headers
do NOT carry the world placement → the tile→world key must come from the runtime's
zone/cell tables (FUN_0093f800's RB-tree keys) whose data source is NOT in the
locally-decodable corpus (the same class as P-CELLSTREAM/#4: the 65×65 climate /
129×129 detail grids are patcher-delivered, non-local per the 178-container census).
Consequence: the INTRA-era field-vs-tile pin cannot be computed from local data
tonight; the cross-era pin [P3b] remains at r=0.527 (iter028) — unchanged.

### The frames inventory (recorded, relationships honest)

| Frame | Extent | Source | Relation to the field frame |
|---|---|---|---|
| Global height field | (-65,536..+65,536)² = 131,072 units | 429259 + quadtree | THE datum |
| Historical locations (24007.vfs) | X -30,693..+25,070; Z -28,980..+27,705 | prior-verified | INSIDE the field ✓ |
| TEZ edit rects | 0..524,287 (2^19) | prior-verified + tonight's name-space check | 4× the field — relationship NOT established |
| 2003 tile grid | 220×236 (filename-XY) | prior-verified | era-local; cross-era unpinned (r=0.527) |
| Runtime reconstruction (2003) | 14,336×15,360 | prior-verified | local geometry, NOT the PE world system |

The TEZ .tez entry IDs are hierarchical (0xY000X page+index — e.g. 1048585=0x100009),
NOT world coordinates; the world-space data is in the TEZ payloads (prior-verified
48-byte records), unchanged.

## MILESTONE_PROGRESS vector

```
georef: the world datum = the global field (CONFIRMED chain, independently
        recomputed); +50.0 slot datum byte-locked instruction-level (iter028
        open item #4 resolved to byte-level); per-tile keying = BLOCKED-UNKNOWN
        (cell-stream class, non-local)
files:  terrain.bnt 58,451/58,451 headers; Textures.bnt 429259 extracted
        (LOCAL-ONLY derivative; identity metadata published); the binary
        constant census (f64/f32 50.0 + 10.0: 12 VA hits byte-located)
excluded: NO client runtime; NO Ghidra session (byte-level reads only);
          NO wiki edits; NO M2 advancement; era-primary 9.3.5
NOT_CHECKED: the +50.0 semantic direction (caller-of-caller); the TEZ<->field
          frame relationship; the R-channel role in 429259; the cell-stream
          contents (non-local); the 129x129 grids
```

## STAGE_ACCEPTANCE_GATES: see STAGE_ACCEPTANCE_GATES.csv (8/8 PASS)
RUN_STATUS = COMPLETED
HARD_STOP_REASON = NONE
