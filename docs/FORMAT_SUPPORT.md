# FORMAT_SUPPORT — container and payload formats this codebase actually handles

All statements below are evidence-backed; "supported" always means *for the stated era
corpus*. Statuses come from `CAPABILITY_MATRIX.json`.

## Containers

| Format | Era corpus | Status | Notes |
|---|---|---|---|
| **BUNT** | ISO_5_1_0_0 `50.bnt` | **Implemented + tested** | Footer `BUNT`, index at offset 116,926,624; 51,921 entries × 21 B (13-byte name + `\n` + packed_size + offset). 51,920 regular filename-xy tiles (grid 0..219 × 0..235, name `XXXXXXXX.tdf`, first 4 hex = grid_x, next 4 = grid_y) + **1 sentinel** `7ffe7ffe.tdf`. 0 duplicates / 0 bad names / 0 out-of-grid (unit-tested census). |
| **BNT2_TERRAIN** | PCG 9.3.5 corpus (different era) | **Implemented (other corpus)** | Footer `BNT2`, 16-byte entries *with* crc32, 58,451 entries including **6,530 special rows** (y = 0xff1a..0xffff). Those special rows DO NOT EXIST in the ISO corpus — the two framings must never be mixed. |
| **BNT2** (generic) | Models.bnt lineage | **Implemented (reference stage)** | Used by the inspector's ORIGINAL-DIRECT model chain (`getModelResource`), SHA-verified container. |
| **ArkVFS (.ark)** | CD Jan-2003 (`Textures.ark`, `Models.ark`, `Scripts.ark`) | **Implemented (reference/scripts)** | ZIP-like with AK magic; used for REFERENCE texture join (4,833 members) and ArkScript `.obj` decode (1,937 members). |
| ISO-era **texture container** | — | **MISSING (documented missing edge)** | The ISO installer corpus ships *no* texture container; the 50.bnt index contains only `.tdf` payloads. All 12 distinct terrain TexIDs are therefore joined in REFERENCE mode from CD Jan-2003 `Textures.ark` (12/12, payload SHA re-verified). |

### BUNT record framing quirks (handled, do not "fix")

- Record: marker `02 00 00 FF` + u32 decompressed_size + zlib stream (`78da`).
- `packed_size` in the index **counts 8 trailing bytes over** the true zlib stream
  ("BUNT_TRAILING_BYTES") — the decoder slices the true stream; the browser re-verifies
  each entry with strict inflate.
- BUNT has **no crc32 field** (BNT2_TERRAIN does).

## Payloads

### TDF height tiles (era ISO_5_1_0_0)

- 32×32 **uint16 little-endian**, height data at **offset 64** (52-byte header +
  12-byte sub-header); `data_size` = 2100, dim = 32, payload 3652 B.
- Offsets come from the audited fixture — **not** blind ±4. (Historical note: an older
  pipeline reading offset 52 produced vertical grid artifacts; 64 is correct.)
- Tile assembly: stride 32, no overlap. All-zero tiles = water/nodata and are **rejected
  explicitly** by the patch selector (not silently rendered).

### TDF material tail (era ISO_5_1_0_0) — **offsetbase +56**

- Mask data begins **+56 bytes record-relative from the size field**. Legacy TMF1.7's
  `+52` is **falsified for this corpus** (it misassigned a per-record checksum-like field
  at bytes 52..55 to the mask). Byte evidence E1–E4: 18/18 RLE records decode exactly at
  +56 (0/18 at +52); overlay masks start with a smooth ramp at +56; base (position-0)
  layer is all-255 in 9/9 tiles; 72/72 strides of size+4 land on the next `[size][dim]`
  header.
- Splat model: base layer + independent alpha overlays, max 10 overlays/tile; 16×16
  weight masks per overlay; weight sums > 255 occur and are kept as ORIGINAL DATA
  (non-complementary model, **no renormalization**).
- The 24-byte field at record offset 32..55 has role **UNVERIFIED** and is never
  interpreted.

### Textures

- REFERENCE mode only: TGA 2.0, 256×256×24 (opaque) from CD Jan-2003 `Textures.ark`.
  Every asset carries the REFERENCE label; nothing is presented as ISO truth.

## NIF formats

| Version | Status |
|---|---|
| **NIF 10.1.0.0** | **Supported (witness scope)** — `NifModelReader.parseWitnessModel` parses the v10 witness class; all 10 climate-0 witness models parse FULL-OK; IR cross-check vs engine oracle 46/46. NiArk blocks: stock engine cannot load them (proven negative control) — Ark-stripped adapted copies exist for the oracle path, with lossmap sidecars. |
| **NIF 4.1.0.12** | **Gated — dedicated adapter pending.** The version gate LOUD-FAILS by design (`0x0401000c NOT implemented`). No 4.1 IR is faked; the frozen R61 reader lineage exists and was engine-validated (22/22 oracle match) but a JS adapter for this runtime is backlog. See `NIF_BINDINGS.md`. |

## Explicit boundaries / limitations

- **Terrain**: one deterministic 3×3-tile patch (grid origin (95,0)), 96×96 samples,
  RAW u16 max 767. Display scale `u16/128 → metres` is a **CURRENT_RUNTIME_CALIBRATION**
  (not a recovered unit), horizontal 2 m/sample. Edge seams (E 20/192, S 25/192) are kept
  as ORIGINAL DATA — no repairs. Full-continent assembly is NOT part of this runtime.
- **Materials/UV**: masks are era truth; the 8 m world-space UV repeat is a
  RECONSTRUCTION_CANDIDATE (query-param overridable), not recovered data.
- **Environment**: no sky/fog/light values recovered in the era corpus — see
  `ENVIRONMENT.md`.
- **Character creation**: schema/labels/layout recovered; ranges/palettes/defaults are
  engine-side and open — see `CHARACTER_CREATION.md`.
