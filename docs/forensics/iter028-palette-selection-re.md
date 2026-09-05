# Terrain Climate Palette Selection — Reverse Engineering (ITER-28 / session ITER_042)

Era: PCG_9_3_5 (Entropia.exe 9.3.5.6746, SHA256 `E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31`).
Evidence: `99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter028_findings.json`, manifest `iter028_manifest.json` (67 entries). Ledger: `M1_LEDGER.md` ITER_028.

## Question

Where does per-location palette selection come from — which climate palette (and which palette ROW) applies to a given terrain location, and what source data drives it?

## Result (CONFIRMED, address-anchored)

### The palette index chain

```
world position
  -> gridX/gridY = (worldPos - origin) / 1024        [FUN_00939a30]
     origin = -(root half / 2) = -32768; world 0 <-> climate cell 32
  -> climate byte = grid[gridX * 65 + gridY]         [65x65 byte grid = bank[3]]
  -> table A[byte]                                    [mgr+0x40, 256-entry id table]
     entries 0..16  = the 17 climate palettes (0x66dc6, 0x66dc7, 0x68cd1, 0x68cd2,
                       0x6a423, 0x6a424, 0x6a425, 0x6a426, 0x6a427, 0x6a428,
                       0x6a438, 0x6a434, 0x6a435, 0x6a436, 0x6a437, 0x854a1, 0x85527)
     entries 17..255 = DEFAULT 0x66dc7
  -> FUN_00938e30 fetch (resource type 100) -> cache mgr+0x440[byte]
  -> the 64x256x32bpp RGBA palette
```

The climate byte is sampled at the 4 corners of the containing 1024-unit cell; up to 4 palettes are fetched and bilinear-blended per RGBA byte with the corner weights (`FUN_00938900`).

### The climate grid source — a global world-data texture set

`FUN_0044d360` (the terrain system creation) -> `FUN_00938f50(id1, id2, id3)` fetches **three global world-data textures** by id (resource type 100) and validates dims 257x257 / 65x65 / 129x129, then splits them into a 9-buffer grid bank (`FUN_0094a9e0`):

| texture id | dims | fill | bank |
|---|---|---|---|
| 0x68CCB (429259) | 257x257x24 | `(t[0]-128)*5` = **heights (m)**; `t[1]/255`; `(t[2]/255)*1.25-0.25` | bank[0..2] float |
| 0x698F6 (432502) | 65x65 | R = **palette climate byte**, G = detail texture id, B = third selector | bank[3..5] byte |
| 0x70060 (459344) | 129x129 | three more byte grids | bank[6..8] byte |

`FUN_00416390` hardcodes the three ids; id[0] (a 4th, runtime-configured current-world id) comes from a singleton.

**Local availability (exhaustive negative):** id 429259 is shipped in both-era `Textures.bnt` (decoded this session, range [-640, +635] m). **Ids 432502 / 459344 are in none of the 49 scanned BNT containers of either corpus**; the plausible second provider `Data\Textures\Terrain.bnt` is a **12-byte BNT2 stub** locally — the climate bytes arrive via the patcher/server channel. The fetch (`FUN_00823c10`) is a provider-ordered container walk; a total miss aborts terrain init, so the runtime data must come from a non-local source.

### The palette ROW = the altitude axis (bound #2 closed)

```
ROW = 255.0 * (1 - ((leafSlot[corner] + leafSlot[4])/2 - 2.0)/512.0 - noise2[cursor])
row = clamp(ftol(ROW), 0, 254)      # FUN_0095da40 = the MSVC ftol helper (confirmed)
col = clamp(ftol(63.0*(noise1[cursor] + acc)), 0, 62)
texel = palette[(row * 64 + col) * 4]   # quad +0x100 (row+1) / +4 (col+1)
```

Constants measured from the binary: 255.0 @0x00a7d748, 2.0 @0x00a7af9c, 512.0 @0x00a7b0b8, 63.0 @0x00a97cb0, the fallback gate 10.0 @0x00a7b128, 0.25 @0x00a7dce8.

The leaf slots (`leaf+0x1c+i*8`, packer `FUN_00991a20` = `{value, format 50.0}`) are **heights sampled from the 257x257 global field** (`FUN_00947a40`, stride 0x101, `*(sampler+8)` double-deref = bank[0] — disasm-pinned) plus position-keyed deterministic noise (`FUN_004059c0`) and slope modulation, clamped to **[-20, +512]** (constants 0x00a97dc8/0x00a97c88) — matching the row domain [2, 514].

Decode-test (18 proven tiles): region A mountains 21–624 m -> rows 22–245 (heights >514 m clamp to row 0); region B flat grass 11–56 m -> rows 236–250. The decoded palettes' row-color structure (0x66dc6 green lowlands -> dark rock highlands; 0x6a436 light sand at the lowest rows) is consistent with rows = altitude bands.

### The quadtree <-> TDF tile linkage (bound #1 closed as a negative)

The quadtree is **ArkHeightTree** (vtable-proven in `FUN_00990a20`), built over the 257x257 GLOBAL height texture — NOT over the TDF tiles. Nodes: 0x48 bytes, 4 children (+0/+4/+8/+0xC), position (+0x10/+0x14), slots, size key (+0x44 = `((size & 0x7fffff)*4 | flags)*8`, so the key >> 5 = the size). Root half = 65536 (world 131,072 units).

**The leaves carry no tile reference and no palette index** — only position, size, and the global-field height slots. The TDF tiles enter the bake only via (a) the tile key/bbox in `FUN_0093f800`'s RB-tree and (b) the 3 detail textures from the per-tile material list (`FUN_00939900`). The quadtree<->tile relationship is spatial overlap per bake, not a data linkage.

### Global field cross-era validation (honest bound)

The shipped 257x257 height texture vs the 2003-era TDF heights (225 anchor tiles + the 18 proven): the best alignment over all tested transforms (4 sign combos x 2 tile scales x full offsets, plus an 8-variant dihedral test) reaches Pearson r = 0.527 (slope 0.20); the coastline IoU max 0.031. The field is a height field of the **9.3.5-era planet state** (2010: both continents + 7 years of edits + a possibly different datum), not the 2003 map — the mechanism is code-confirmed, the cross-era georeferencing is an open bound.

## Honest bounds

1. The 65x65 climate bytes are not locally available (49-container negative + the 12-byte `Terrain.bnt` stub) — the palette-per-location cannot be computed from the local corpus alone.
2. The cross-era georeferencing of the global height field vs the 2003 map is unpinned (r saturates at ~0.53).
3. The runtime world-id (singleton+4) is per-planet runtime data — unresolved.
4. The corner-present flag / edge-marker closed form and the slot format's +50.0 datum intent remain unverified (inherited from ITER-27).
5. The 129x129 grids' semantics (water/biome mask candidates) are unresolved.

## Impact on the runtime

- `PESourceMount` needs the second texture provider (`Textures\Terrain.bnt`, BNT2, patcher-populated) for ids 432502/459344; the 257x257 height texture 429259 is available in the shipped `Textures.bnt`.
- The terrain base color / palette selection is **global-data-driven**, not TDF-driven; the TDF material records feed only the 3 detail slots and the geometry.
- Cross-lead (Gate C): the ArkHeightTree + the climate cells are the same global data the vegetation spawn path (`FUN_0093a990`) consumes — a shared terrain/foliage climate system.

## Process

Fresh Ghidra project ITER042_PALETTE (never TMF1_12H); sandbox SHA-verified; 5 postscript runs + 13 data scripts, all hashed after final edit before execution; measured/interpreted/errors separation in every artifact. Loud failures documented and fixed (Jython non-ASCII coding error; uint8 overflow; a malformed comprehension; wrong PNG paths) — zero evidence claimed from failed runs. All spawned processes verified dead.
