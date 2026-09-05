// PEFoliageCore.js — M1 ITER 049 (ledger ITER_035, the FLOAT64 operand lock).
// PE Runtime Core: the vegetation INSTANCE GENERATOR, implementing the 9.3.5
// chain EXACTLY as the binary computes it — every constant BYTE-LOCKED as
// FLOAT64 and every float32 store replicated at the binary's own rounding
// points (the human audit's ENTRY #10 correction; the iter032/033 f32
// misreads are SUPERSEDED).
//
// =========== THE FLOAT64 OPERAND LOCK (iter035, FRESH Ghidra ITER049_FLOAT64) ===========
// Binary: Entropia.exe 9.3.5.6746 sandbox copy, SHA256 E7785430E81DFFE648CE8F5312414B17
// BC9FCE61389689A22F753765D5280F31 (verified before import). Image base 0x00400000;
// .rdata VA 0x00A75000 = raw 0x675000 (VA -> file offset = VA - 0x400000).
//
// THE THREE CONSTANTS (byte-exact, QWORD f64 operands — the prior f32 reads were
// the LOW DWORD of these 8-byte doubles):
//   _DAT_00a7d7a8 @ VA 0x00A7D7A8, file 0x67D7A8, bytes 00 00 00 00 C0 FF DF 40
//     = 32767.0 f64 — FDIV QWORD @ 0x0098CE5A (FUN_0098ce30). [was read as 0.0f
//     low dword + ASSUMED 32768.0 — WRONG]
//   _DAT_00a8c758 @ VA 0x00A8C758, file 0x68C758, bytes 00 00 00 00 E0 FF EF 40
//     = 65535.0 f64 — FLD QWORD @ 0x0095B2BC + 0x0095B3DB (FUN_0095b180). [was
//     read as 0.0f low dword + ASSUMED 2.0 — WRONG]
//   _DAT_00a980d0 @ VA 0x00A980D0, file 0x6980D0, bytes 00 00 00 40 E1 7A 14 3F
//     = 0.00007812499825377017 f64 — FMUL QWORD @ 0x0095B347 (FUN_0095b180).
//     BYTE-EXACT ROLE: C = float32(1/12800) widened to f64 (mantissa
//     0x47AE140000000 = 2348810 * 2^29; the binary stores the f32-rounded
//     decimal 0.000078125 = 1/12800 = 2^-7/100 in a QWORD slot). [was read as
//     the low dword 0x40000000 = 2.0f and called "MEASURED 2.0f" — WRONG]
//
// THE SIX FLOAT32 STORE/ROUNDING POINTS (the census, iter035_operand_table.json;
// the chain computes in 80-bit x87 and rounds to f32 AT THESE STORES ONLY):
//   P1 @0x0098CE60  rand01 = f32(r / 32767.0)         (FUN_0098ce30, before return)
//   P2 @0x0095ACF0  value  = f32(rand01*(max-min)+min) (FUN_0095ac30, before return)
//   P3 @0x0095B318  nodeX  = f32(A / 65535.0)          (FUN_0095b180 -> node+0x5C)
//   P4 @0x0095B322  nodeY  = f32(B / 65535.0)         (FUN_0095b180 -> node+0x60)
//   P5 @0x0095B353  f32(value * C)                    (FUN_0095b180, pre-FABS)
//   P6 @0x0095B365  nodeScale = f32(|value*C|)        (FUN_0095b180 -> node+0x68)
// The lerp min/max are FLOAT32 FIELDS (FLD DWORD [impl+0x44]/[impl+0x40]) — the
// lerp OPERANDS are f32 values whatever their source.
// EXACTNESS (proven exhaustively, exact-rational, iter035): the JS formula
// (f64 arithmetic + Math.fround at the same points) is BIT-EXACT vs the
// binary's 80-bit-then-FSTP-DWORD double rounding over the COMPLETE input
// domains (32768/32768 rand01 values, 65536/65536 u16 positions,
// 1245184+1245184 lerp/scale combinations — 0 mismatches).
//
// ============ THE CONFIRMED CHAIN (address-cited; unchanged parts from iter032) ============
// (1) .vcl TSV -> 12-value records (FUN_0083a7d0; decoded upstream by
//     VegetationClimateDecoder). The parser's 12-value copy is a raw REP MOVSD
//     (4-byte values, no conversion) — per-column int/float types UNVERIFIED.
// (2) The per-cell procedural grid: subdivision switch on settings+4,
//     case 0/1/2/3/4 -> step 1/2/4/8/16 (FUN_0098fe00 @ 0x0098FE00; INTEGER-ONLY
//     — 0 FPU instructions in the census). The spawn loop builds
//     ArkVegetationSpawnSettings with value 1 at +4 -> default subdivision 2.
// (3) The per-cell records: 8-byte triples {u16 x, u16 y, u32 model_id}
//     (FUN_00990810 @ 0x00990810; the FPU usage there = exact 4-byte moves).
//     [P-CELLSTREAM] the historical cell byte-stream ORIGIN is NOT closed —
//     the record CONTENT here is the labeled deterministic stand-in.
// (4) The position-keyed RNG (FUN_0098cdf0 seed + FUN_0098ce30 next +
//     FUN_0095ac30 sampler):
//       seed: x = ((p4*16 + p5)*16 + p1 + p2 + p3) * 0x5CC7 + 0x6D7  (uint32)
//             state = x*8 ^ x                                     (uint32)
//       next:  state = state*0x343FD + 0x269EC3 (uint32);
//             r = (state>>16) & 0x7FFF;  rand01 = f32(r / 32767.0)
//             (the FADD dword [2^32f] @0x0098CE54 is the compiler's generic
//             unsigned-conversion idiom — DEAD CODE here: r >= 0 always)
//       sampler: min/max = the f32 fields impl+0x44/impl+0x40;
//             value = f32(rand01 * (max - min) + min)
//       POSITION-KEYED DETERMINISM (the same u16 pair -> the same scale).
// (5) The instance spawn (FUN_0095b180): per record {A = u16 x, B = u16 y,
//     id = u32}:
//       node+0x5C = f32(A / 65535.0)   (the NiNode local translate X — a [0,1]
//                                   NODE-LOCAL FRACTION: 65535.0 = the u16 max)
//       node+0x60 = f32(B / 65535.0)   (local translate Y — same)
//       node+0x64 = id                (THE MODEL BIND; the raw bits move
//                                   exactly through the FPU roundtrip)
//       node+0x68 = f32(|value * 0.00007812499825377017|)  (the local scale)
//     ROTATION/variant: NOT FOUND in the spawn loop (identity = RE-faithful).
//     THE [0,1]-node-position -> WORLD mapping lives in the visualizer path
//     (FUN_0095ae20/FUN_0095b4f0 — NOT decompiled; iter032 bound 5 stands) —
//     it is UNVERIFIED, and this module leaves it to the caller as an explicit
//     labeled reconstruction calibration (windowWorld below).
//
// ================== HONEST BOUNDS (all labeled; NO historical-truth claims) ==================
// [P-CLIMATE]     RECONSTRUCTION-ONLY: which .vcl chunk applies to a region —
//                 the per-location climate input is PLAUSIBLE-UNVERIFIED (the
//                 shared-selector hypothesis, iter032); the CALLER passes the
//                 explicit index.
// [P-CELLSTREAM]  RECONSTRUCTION-ONLY: the per-cell record CONTENT (positions +
//                 model selection + counts) — the historical stream origin is
//                 NOT closed; this module generates it deterministically
//                 (placementHash + count = max(0, round(col1 density)) per
//                 record per sub-cell). NEVER claimed historical.
// [P-RNG-P3]      p3 = *(impl+0x24) UNVERIFIED -> 0 (documented constant).
// [P-SCALE-FIELDS] the lerp bounds impl+0x44 (min) / impl+0x40 (max) ARE f32
//                 fields (FLD DWORD, census-locked); the VCL col2/col3 -> field
//                 mapping = the census min/max reading (STRONGLY_SUPPORTED,
//                 NOT byte-pinned), and the ABSOLUTE world-size meaning of the
//                 resulting node scale depends on those field VALUES — bounded.
// [P-WINDOW]      RECONSTRUCTION-ONLY: the generation window (the u16 record
//                 space handed to the grid) and its world box — the historical
//                 grid extents are settings-scaled (FUN_0098fe00 extent getters
//                 read runtime settings) and the visualizer's [0,1]->world
//                 transform is NOT decompiled; the caller supplies windowWorld
//                 as an explicit CURRENT_RUNTIME_CALIBRATION.

export const FOLIAGE_OPERAND_LOCK = {
  source: 'Entropia.exe 9.3.5.6746 sandbox copy (SHA256 E7785430E81DFFE648CE8F5312414B17BC9FCE61389689A22F753765D5280F31), FRESH Ghidra project ITER049_FLOAT64, iter035 (ledger ITER_035)',
  operandTable: '99_Audits/PE_MILESTONE_1_WORLD_SURFACE_R1/03_EVIDENCE/iter035_operand_table.json',
  rand01Divisor: { symbol: '_DAT_00a7d7a8', va: '0x00A7D7A8', fileOffset: '0x67D7A8',
    bytes: '00 00 00 00 C0 FF DF 40', f64: 32767.0, operand: 'FDIV QWORD @0x0098CE5A' },
  nodePosDivisor: { symbol: '_DAT_00a8c758', va: '0x00A8C758', fileOffset: '0x68C758',
    bytes: '00 00 00 00 E0 FF EF 40', f64: 65535.0, operand: 'FLD QWORD @0x0095B2BC/0x0095B3DB' },
  nodeScaleMul: { symbol: '_DAT_00a980d0', va: '0x00A980D0', fileOffset: '0x6980D0',
    bytes: '00 00 00 40 E1 7A 14 3F', f64: 0.00007812499825377017,
    operand: 'FMUL QWORD @0x0095B347',
    derivation: 'C = float32(1/12800) widened to f64 = 10737418/2^37 exactly (the f32-rounded decimal 0.000078125 stored in a QWORD slot); role: nodeScale = |lerp| / 12800 (2^-7/100)' },
  f32RoundingPoints: [
    'P1 @0x0098CE60 rand01 = f32(r/32767.0)',
    'P2 @0x0095ACF0 value = f32(rand01*(max-min)+min)',
    'P3 @0x0095B318 nodeX = f32(A/65535.0)',
    'P4 @0x0095B322 nodeY = f32(B/65535.0)',
    'P5 @0x0095B353 f32(value*C)',
    'P6 @0x0095B365 nodeScale = f32(|value*C|)',
  ],
  exactness: 'exhaustive exact-rational proof: the f64+Math.fround replication is BIT-EXACT vs 80-bit+FSTP DWORD over the complete input domains (0 mismatches; iter035_operand_table.json exactness_proofs)',
};

export const FOLIAGE_RE = {
  binary: 'Entropia.exe 9.3.5.6746 (iter032 source graph + iter035 FLOAT64 operand lock, ledger ITER_035)',
  vclParser: 'FUN_0083a7d0 (12 values -> 0x30 records; raw REP MOVSD copy)',
  gridGen: 'FUN_0098fe00 (subdivision switch settings+4: 0/1/2/3/4 -> 1/2/4/8/16; INTEGER-ONLY per the iter035 census)',
  cellRecords: 'FUN_00990810 ({u16 x, u16 y, u32 model_id} 8-byte triples)',
  spawnLoop: 'FUN_0095b180 (nodeX/Y = f32(u16/65535.0); nodeScale = f32(|lerp*C|); model id bind at node+0x64)',
  rngSeed: 'FUN_0098cdf0 (x = ((p4*16+p5)*16+p1+p2+p3)*0x5CC7+0x6D7; state = x*8^x)',
  rngNext: 'FUN_0098ce30 (MSVC rand(): state*0x343FD+0x269EC3, >>16 &0x7FFF, /32767.0 f64 -> FSTP DWORD)',
  rngSampler: 'FUN_0095ac30 (f32 fields impl+0x44/impl+0x40; value = f32(rand01*(max-min)+min) -> FSTP DWORD)',
  spawnSettings: 'FUN_0095b180 builds ArkVegetationSpawnSettings {vtable, 1@+4, ...} -> default level 1',
  constants: '_DAT_00a7d7a8 = 32767.0 f64; _DAT_00a8c758 = 65535.0 f64; _DAT_00a980d0 = 0.00007812499825377017 f64 (all BYTE-LOCKED iter035)',
  bounds: 'iter032 honest bounds (1)-(7) + the iter035 lock (see FOLIAGE_OPERAND_LOCK + the module header)',
};

export const FOLIAGE_PLACEHOLDERS = {
  'P-CLIMATE': 'RECONSTRUCTION-ONLY: per-location climate input PLAUSIBLE-UNVERIFIED (shared-selector hypothesis); explicit index passed by the caller',
  'P-CELLSTREAM': 'RECONSTRUCTION-ONLY: per-cell record content = local deterministic stand-in (historical stream origin NOT closed, iter032 bound 3); the record FORMAT {u16,u16,u32} + the spawn arithmetic are the CONFIRMED parts',
  'P-RNG-P3': 'seed p3 = *(impl+0x24) UNVERIFIED -> 0',
  'P-SCALE-FIELDS': 'lerp min/max = the f32 fields impl+0x44/impl+0x40 (FLD DWORD, census-locked); the VCL col2/col3 mapping = the census min/max reading (STRONGLY_SUPPORTED, NOT byte-pinned); the node-scale world-size meaning depends on the field VALUES (bounded)',
  'P-WINDOW': 'RECONSTRUCTION-ONLY: the generation window + its world box = the caller-supplied CURRENT_RUNTIME_CALIBRATION (the historical grid extents are settings-scaled; the visualizer [0,1]->world transform NOT decompiled)',
};

/** The MSVC rand() LCG constants (CONFIRMED in the binary bytes). */
export const MSVC_RAND_MUL = 0x343FD;    // 214013
export const MSVC_RAND_INC = 0x269EC3;   // 2531011

/** THE LOCKED CONSTANTS (f64, byte-exact — see FOLIAGE_OPERAND_LOCK). */
export const RAND01_DIVISOR = 32767.0;                 // _DAT_00a7d7a8
export const NODE_POS_DIVISOR = 65535.0;               // _DAT_00a8c758
export const NODE_SCALE_MUL = 0.00007812499825377017;  // _DAT_00a980d0

/**
 * VegetationRNG — the CONFIRMED vegetation RNG (FUN_0098cdf0 + FUN_0098ce30),
 * with the FLOAT64 divisor and the FLOAT32 return rounding LOCKED from the
 * binary (iter035). One instance = one seed + one draw (the sampler draws once).
 */
export class VegetationRNG {
  /**
   * The seed hash, VERBATIM FUN_0098cdf0 (uint32):
   *   x = ((p4*0x10 + p5)*0x10 + p1 + p2 + p3) * 0x5CC7 + 0x6D7
   *   state = x*8 ^ x
   * p4/p5 = the record's u16 position components (POSITION-KEYED);
   * p1 = the packed query position; p2 = the view band (STRONGLY_SUPPORTED);
   * p3 = *(impl+0x24) [P-RNG-P3] = 0.
   */
  seed(p1, p2, p3, p4, p5) {
    const x =
      ((((p4 >>> 0) * 0x10 + (p5 >>> 0)) * 0x10) + (p1 >>> 0) + (p2 >>> 0) + (p3 >>> 0)) >>> 0;
    const hashed = (x * 0x5CC7 + 0x6D7) >>> 0;
    this.state = ((hashed * 8) ^ hashed) >>> 0;   // FUN_0098cdf0: state = x*8 ^ x
    return this.state;
  }

  /**
   * The next value, VERBATIM FUN_0098ce30 with the LOCKED operands:
   *   state = state*0x343FD + 0x269EC3 (uint32)
   *   r = (state >> 16) & 0x7FFF                      (r in [0, 32767], always >= 0
   *                                                    -> the 2^32f FADD idiom is DEAD)
   *   rand01 = f32(r / 32767.0)                       (FDIV QWORD _DAT_00a7d7a8 @0x0098CE5A,
   *                                                    then FSTP DWORD @0x0098CE60 = F32
   *                                                    ROUNDING BEFORE RETURN)
   * rand01 in [0, 1] INCLUSIVE (r = 0x7FFF -> exactly 1.0).
   */
  next01() {
    this.state = (this.state * MSVC_RAND_MUL + MSVC_RAND_INC) >>> 0;
    const r = (this.state >>> 16) & 0x7FFF;
    return Math.fround(r / RAND01_DIVISOR);   // P1: the binary's f32 store point
  }
}

/**
 * The sampler + the spawn scale field, VERBATIM the locked chain:
 *   min/max  = the f32 fields (FLD DWORD [impl+0x44]/[impl+0x40]) — the operands
 *              are f32 VALUES, so the inputs are frounded first
 *   value    = f32(rand01 * (max - min) + min)   (FUN_0095ac30, 80-bit lerp ->
 *              FSTP DWORD @0x0095ACF0 = P2)
 *   scale    = f32(|value * NODE_SCALE_MUL|)    (FUN_0095b180 FMUL QWORD @0x0095B347
 *              + FABS + FSTP DWORD @0x0095B365 = P5/P6; |f32(x)| = f32(|x|))
 */
export function sampleModelScale(rng, min, max) {
  const fmin = Math.fround(min);   // the f32 field at impl+0x44
  const fmax = Math.fround(max);   // the f32 field at impl+0x40
  const value = Math.fround(rng.next01() * (fmax - fmin) + fmin);   // P2
  const scale = Math.fround(Math.abs(value * NODE_SCALE_MUL));      // P5+P6 (net)
  return { value, scale };
}

/**
 * The subdivision switch, VERBATIM FUN_0098fe00:
 *   switch(settings+4): default->1, 1->2, 2->4, 3->8, 4->16
 * (the spawn loop's settings carries 1 at +4 -> default step 2).
 */
export function subdivisionStep(level) {
  switch (level) {
    case 0: return 1;
    case 1: return 2;
    case 2: return 4;
    case 3: return 8;
    case 4: return 16;
    default:
      throw new Error(`[PEFoliageCore] subdivision level ${level} out of range 0..4 (FUN_0098fe00 switch)`);
  }
}

/**
 * The packed query position (FUN_007ce1e0 = *(obj+8); FUN_0098f3a0 consumes it
 * as (>>16, &0xFFFF sign-extended)) — the 32-bit packing of two u16
 * components: (qX << 16) | (qY & 0xFFFF).
 */
export function packedQueryPosition(qX, qY) {
  return (((qX & 0xFFFF) << 16) | (qY & 0xFFFF)) >>> 0;
}

/**
 * [P-CELLSTREAM] The placement hash — RECONSTRUCTION-ONLY (NOT historical):
 * a documented deterministic hash standing in for the historical per-cell
 * record positions (whose stream origin is NOT closed, iter032 bound 3).
 * splitmix-style finalize; two calls (j*2, j*2+1) give independent fractions.
 */
function placementHash(cellX, cellY, modelId, j) {
  let h = (((cellX >>> 0) * 0x9E3779B1) ^ ((cellY >>> 0) * 0x85EBCA77) ^
           ((modelId >>> 0) * 0xC2B2AE3D) ^ ((j >>> 0) * 0x27D4EB2F)) >>> 0;
  h = Math.imul(h ^ (h >>> 16), 0x21F0AAAD) >>> 0;
  h = Math.imul(h ^ (h >>> 15), 0x735A2D97) >>> 0;
  return (h ^ (h >>> 15)) >>> 0;
}

/**
 * generateInstances — the CONFIRMED chain over one generation window, with the
 * FLOAT64 constants + F32 rounding points LOCKED (iter035).
 *
 * @param {object} opts
 *   records       the 12-value VCL climate records (decoded upstream)
 *   windowU16     {x0, y0, x1, y1} — the generation window in u16 record space
 *                 ([P-WINDOW] RECONSTRUCTION-ONLY: the caller's calibration)
 *   windowWorld   {x0, y0, x1, y1} — the WORLD box corresponding to windowU16
 *                 ([P-WINDOW] RECONSTRUCTION-ONLY: the caller's CURRENT_RUNTIME_
 *                 CALIBRATION for the [0,1] node position -> world mapping; the
 *                 visualizer's own transform is NOT decompiled — iter032 bound 5)
 *   level         the subdivision level 0..4 (FUN_0098fe00 switch input)
 *   viewBand      the p2 seed input (STRONGLY_SUPPORTED: 10/20/30)
 *   p3            the p3 seed input [P-RNG-P3] (default 0)
 * @returns {{instances: object[], census: object}}
 */
export function generateInstances({ records, windowU16, windowWorld, level, viewBand, p3 = 0 }) {
  if (!Array.isArray(records) || records.length === 0) {
    throw new Error('[PEFoliageCore] no climate records (empty climate)');
  }
  for (const r of records) {
    if (!Array.isArray(r) || r.length !== 12) {
      throw new Error('[PEFoliageCore] climate record is not the 12-value layout (FUN_0083a7d0)');
    }
  }
  const { x0, y0, x1, y1 } = windowU16;
  if (!(0 <= x0 && x0 < x1 && x1 <= 0x10000 && 0 <= y0 && y0 < y1 && y1 <= 0x10000)) {
    throw new Error(`[PEFoliageCore] invalid u16 window ${JSON.stringify(windowU16)}`);
  }
  if (!windowWorld || !(windowWorld.x0 < windowWorld.x1 && windowWorld.y0 < windowWorld.y1)) {
    throw new Error(`[PEFoliageCore] invalid windowWorld ${JSON.stringify(windowWorld)} (the [P-WINDOW] calibration is REQUIRED and explicit)`);
  }
  const step = subdivisionStep(level);
  const cells = step * step;

  // The query position (p1): the window origin packed as the historical
  // component pair (FUN_007ce1e0 / FUN_0098f3a0 semantics).
  const p1 = packedQueryPosition(x0, y0);

  const cellW = (x1 - x0) / step;
  const cellH = (y1 - y0) / step;

  // The [P-WINDOW] linear calibration: u16 record space -> world box (the
  // CALLER's reconstruction choice; NOT a binary claim).
  const u16ToWorldX = (u) => windowWorld.x0 + (u - x0) / (x1 - x0) * (windowWorld.x1 - windowWorld.x0);
  const u16ToWorldY = (u) => windowWorld.y0 + (u - y0) / (y1 - y0) * (windowWorld.y1 - windowWorld.y0);

  const instances = [];
  const perCell = [];
  const perModel = new Map();   // modelId -> {count, scaleMin, scaleMax}
  const zeroCountRecords = [];  // records present in the climate, count 0

  for (let cy = 0; cy < step; cy++) {
    for (let cx = 0; cx < step; cx++) {
      const cell = { cellX: cx, cellY: cy, u16Box: null, counts: {}, total: 0 };
      const bx0 = Math.floor(x0 + cx * cellW), by0 = Math.floor(y0 + cy * cellH);
      const bx1 = Math.floor(x0 + (cx + 1) * cellW), by1 = Math.floor(y0 + (cy + 1) * cellH);
      cell.u16Box = { x0: bx0, y0: by0, x1: bx1, y1: by1 };
      const bw = Math.max(1, bx1 - bx0), bh = Math.max(1, by1 - by0);

      // Per climate record (the record IS the unit — duplicate model ids with
      // different bands are separate engine rows, per the 0x30 row vector):
      // [P-CELLSTREAM] count = max(0, round(col1 density)) per sub-cell.
      records.forEach((rec, recIndex) => {
        const modelId = rec[0] | 0;
        const density = rec[1];
        const count = Math.max(0, Math.round(density));
        cell.counts[`rec${recIndex}_m${modelId}`] = count;
        if (count === 0) {
          zeroCountRecords.push({ recIndex, modelId, density });
          return;
        }
        let m = perModel.get(modelId);
        if (!m) { m = { modelId, count: 0, scaleMin: Infinity, scaleMax: -Infinity }; perModel.set(modelId, m); }

        for (let j = 0; j < count; j++) {
          // [P-CELLSTREAM] The stand-in record: {u16 x, u16 y, u32 model_id}
          // (the FUN_00990810 triple layout), positions inside the sub-cell.
          const hA = placementHash(bx0, by0, modelId, j * 2);
          const hB = placementHash(bx0, by0, modelId, j * 2 + 1);
          const ux = bx0 + Math.min(bw - 1, Math.floor(((hA >>> 16) & 0xFFFF) / 65536 * bw));
          const uy = by0 + Math.min(bh - 1, Math.floor((hB & 0xFFFF) / 65536 * bh));

          // The CONFIRMED spawn arithmetic (FUN_0095ac30 + FUN_0095b180, the
          // iter035 FLOAT64 lock: every constant f64, f32 at the binary's own
          // FSTP points):
          const rng = new VegetationRNG();
          const state0 = rng.seed(p1, viewBand, p3, ux, uy);
          const { value, scale } = sampleModelScale(rng, rec[2], rec[3]);
          // P3/P4: the node-local [0,1] positions (the BINARY fields)
          const nodeX = Math.fround(ux / NODE_POS_DIVISOR);
          const nodeY = Math.fround(uy / NODE_POS_DIVISOR);
          // The [P-WINDOW] page calibration (NOT a binary claim):
          const wx = u16ToWorldX(ux);
          const wy = u16ToWorldY(uy);

          instances.push({
            cell: [cx, cy], recIndex, modelId,
            u16: { x: ux, y: uy },
            node01: { x: nodeX, y: nodeY },          // the BINARY node fields (f32)
            world: { x: wx, y: wy },                 // the caller's calibration
            scale, samplerValue: value,              // the BINARY node scale (f32) + lerp
            seedInputs: { p1, p2: viewBand, p3, p4: ux, p5: uy },
            rngState0: state0,
            elevationBand: { min: rec[4], max: rec[5] },
            rotation: 'IDENTITY (rotation/variant NOT FOUND in the spawn loop — iter032 bound 5)',
          });
          m.count++; m.scaleMin = Math.min(m.scaleMin, scale); m.scaleMax = Math.max(m.scaleMax, scale);
          cell.total++;
        }
      });
      perCell.push(cell);
    }
  }

  const census = {
    reChain: FOLIAGE_RE,
    operandLock: FOLIAGE_OPERAND_LOCK,
    placeholders: FOLIAGE_PLACEHOLDERS,
    inputs: {
      recordCount: records.length,
      windowU16, windowWorld, level, step, cells,
      viewBand, p3, p1,
      constants: {
        rand01Divisor: RAND01_DIVISOR,
        nodePosDivisor: NODE_POS_DIVISOR,
        nodeScaleMul: NODE_SCALE_MUL,
      },
    },
    totals: {
      instances: instances.length,
      distinctModelsInstantiated: perModel.size,
      zeroCountRecords: zeroCountRecords.length,
    },
    perCell,
    perModel: [...perModel.values()],
    zeroCountRecords,
  };
  return { instances, census };
}
