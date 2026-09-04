// TdfDecoder.js — PE MILESTONE 1 ITER 001/002 (PE_WORLD_SURFACE_FIDELITY_R1)
// TDF (terrain tile) decoder with the TWO offset spaces kept explicitly
// separate, per charter §3 / FULL_SYNC §05 "THE 52/64 OFFSET QUESTION":
//
// OFFSET SPACE 1 — PAYLOAD-RELATIVE (the decompressed TDF payload, 3652 B):
//   header      0..51    (u32 tile_x, u32 tile_y, u32 data_size, u32 tile_dim, 36 B metadata)
//   sub-header  52..63    (6 x u16 — NOT height data; offset-52 height reads corrupt 6 values)
//   HEIGHTS     64..2111 (32x32 uint16 LE = 2048 B — THE canonical height offset)
//   TAIL        2112..   (material section: u32 308 @2112, u32 16 @2116, payload @2120)
//
// OFFSET SPACE 2 — MATERIAL-RECORD-RELATIVE (a 308-byte record nested in the tail):
//   header      0..15    <size=308, dim=16, unk=1, bps=2>
//   material_id 16..19
//   reserved    20..23   (always 0)
//   name        24..31   (7 chars + NUL)
//   counter     32       (instance counter or 0)
//   pad         33..51
//   MASK16      52..307  (16x16 uint8 — record-relative! NOT payload offset 52)
//
// These spaces MUST NOT be collapsed. The coincidental double "52" is the
// historical root of the chronic confusion (FULL_SYNC §05, row table).
//
// Gate A decodes HEIGHTS only. The tail is exposed RAW (no material
// interpretation) for Gate B; material semantics are NOT implemented here.

export const TDF_PAYLOAD_LAYOUT = Object.freeze({
  HEADER: { start: 0, end: 52 },
  SUBHEADER: { start: 52, end: 64 },       // 12 bytes, NOT heights
  HEIGHTS: { start: 64, end: 2112 },      // 32x32 uint16 LE — canonical
  TAIL: { start: 2112, end: null },       // material section (Gate B scope)
});

export const TDF_MATERIAL_RECORD_LAYOUT = Object.freeze({
  // RECORD-RELATIVE offsets inside a 308-byte material record (TMF1.7 CONFIRMED)
  RECORD_SIZE: 308,
  HEADER: { start: 0, end: 16 },
  MATERIAL_ID: { start: 16, end: 20 },
  RESERVED: { start: 20, end: 24 },
  NAME: { start: 24, end: 32 },
  COUNTER: 32,
  PAD: { start: 33, end: 52 },
  MASK16: { start: 52, end: 308 },         // 16x16 uint8 — record-relative
});

export const TDF_STANDARD = Object.freeze({
  DECOMPRESSED_SIZE: 3652,
  DATA_SIZE_FIELD: 2100,   // u32 @payload 8
  TILE_DIM_FIELD: 32,      // u32 @payload 12
  HEIGHT_SAMPLES: 1024,    // 32*32
});

export const TDF_SENTINEL_NAME = '7ffe7ffe.tdf'; // overview/sentinel tile — NOT a regular grid tile

export function isSentinelName(name) {
  return name === TDF_SENTINEL_NAME;
}

/** Grid coordinates from the BUNT entry filename (XXXXXXXX.tdf). */
export function gridFromName(name) {
  if (typeof name !== 'string' || !/^[0-9a-fA-F]{8}\.tdf$/.test(name)) {
    throw new Error(`[TdfDecoder] not a tile filename: ${JSON.stringify(name)}`);
  }
  const gridX = parseInt(name.slice(0, 4), 16);
  const gridY = parseInt(name.slice(4, 8), 16);
  return { gridX, gridY };
}

/**
 * Decodes a decompressed TDF payload.
 * @param {Uint8Array} payload 3652 bytes (standard tile)
 * @param {object} meta {name, gridX, gridY}
 * @returns object with raw slices + heights (Uint16Array 1024) + tail raw
 */
export function decodeTdfPayload(payload, meta = {}) {
  if (payload.byteLength < TDF_PAYLOAD_LAYOUT.HEIGHTS.end) {
    throw new Error(`[TdfDecoder] payload too small: ${payload.byteLength}`);
  }
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const dataSize = dv.getUint32(8, true);
  const tileDim = dv.getUint32(12, true);
  // Standard-tile validation. The sentinel/overview tile (dim=237, ds=56221)
  // is classified BEFORE decoding and must never reach this function as a
  // regular tile (see PESourceMount.getTerrainTile).
  if (dataSize !== TDF_STANDARD.DATA_SIZE_FIELD || tileDim !== TDF_STANDARD.TILE_DIM_FIELD) {
    throw new Error(
      `[TdfDecoder] ${meta.name}: not a standard 32x32 tile (data_size=${dataSize}, tile_dim=${tileDim})`);
  }
  const heights = new Uint16Array(TDF_STANDARD.HEIGHT_SAMPLES);
  for (let i = 0; i < TDF_STANDARD.HEIGHT_SAMPLES; i++) {
    heights[i] = dv.getUint16(TDF_PAYLOAD_LAYOUT.HEIGHTS.start + i * 2, true);
  }
  return {
    name: meta.name,
    gridX: meta.gridX,
    gridY: meta.gridY,
    // raw slices — the offset spaces stay visible in the object graph
    header: payload.subarray(TDF_PAYLOAD_LAYOUT.HEADER.start, TDF_PAYLOAD_LAYOUT.HEADER.end),
    subheader: payload.subarray(TDF_PAYLOAD_LAYOUT.SUBHEADER.start, TDF_PAYLOAD_LAYOUT.SUBHEADER.end),
    heights, // 1024 uint16, row-major 32x32
    tail: payload.subarray(TDF_PAYLOAD_LAYOUT.TAIL.start), // RAW — Gate B scope
    dataSize,
    tileDim,
  };
}
