// PEFoliageCore.js — M1 ITER 047 (ledger ITER_033, Gate C wiring).
// PE Runtime Core: the CONFIRMED 9.3.5 vegetation INSTANCE GENERATOR.
// Implements the source-graph stages recovered in iter032 (Gate C, ledger
// ITER_032) EXACTLY as decompiled, with every stage address-cited. This
// module owns the foliage WORLD semantics; the renderer (Three.js r185)
// receives plain instance records — NO format knowledge.
//
// ============ THE CONFIRMED CHAIN (Entropia.exe 9.3.5.6746, iter032) ============
// (1) .vcl TSV -> 12-value records (FUN_0083a7d0; decoded upstream by
//     VegetationClimateDecoder — the 0x30/48-byte engine row stride).
// (2) The per-cell procedural grid: subdivision switch on settings+4,
//     case 0/1/2/3/4 -> step 1/2/4/8/16 (FUN_0098fe00 @ 0x0098FE00).
//     The spawn loop FUN_0095b180 builds ArkVegetationSpawnSettings with
//     value 1 at +4 -> the RE-derived default subdivision = step 2.
// (3) The per-cell records: 8-byte triples {u16 x, u16 y, u32 model_id}
//     (FUN_00990810 @ 0x00990810 writes u16@0, u16@2, u32@4 per record,
//     count per cell from the cell stream; density = *(cell+8) >> 3 in
//     FUN_0098fe00). ERA BOUND (iter032 bound 3): the historical cell byte
//     stream's ORIGIN is NOT closed (local file vs server content) — the
//     record CONTENT is therefore generated locally as a labeled stand-in
//     [P-CELLSTREAM]; the record FORMAT and the spawn semantics below are
//     the CONFIRMED parts.
// (4) The position-keyed RNG (FUN_0098cdf0 @ 0x0098CDF0 + FUN_0098ce30 @
//     0x0098CE30 + the sampler FUN_0095ac30 @ 0x0095AC30):
//       seed: x = ((p4*16 + p5)*16 + p1 + p2 + p3) * 0x5CC7 + 0x6D7  (uint32)
//             state = x*8 ^ x                                     (uint32)
//       next: state = state*0x343FD + 0x269EC3; out = (state>>16) & 0x7FFF
//             -> the classic MSVC rand() LCG (214013 / 2531011)
//       sampler: value = rand01 * (max - min) + min  (lerp of the per-model
//             scale fields impl+0x40/impl+0x44 read in FUN_0095ac30)
//     The SEED INPUTS (from the FUN_0095ac30 decompile):
//       p4 = record u16 x & 0xFFFF, p5 = record u16 y & 0xFFFF
//         -> POSITION-KEYED DETERMINISM (CONFIRMED: the same u16 position
//            always yields the same scale; no global seed, no server RNG)
//       p1 = the packed 32-bit query position (FUN_007ce1e0 = *(obj+8),
//            consumed as one u32; FUN_0098f3a0 splits it >>16 / &0xFFFF)
//       p2 = *(obj+0x2c) (FUN_007ad080) — by the +0x2c field pattern in the
//            spawn loop this is the VIEW BAND 10/20/30 (FUN_0095b180 reads
//            *(...+0x2c) and tests 10/0x14/0x1e) — STRONGLY_SUPPORTED
//       p3 = *(impl+0x24) (FUN_0098cfe0 object) — UNVERIFIED
// (5) The instance spawn (FUN_0095b180 @ 0x0095B180): per record triple
//     {A = u16 x, B = u16 y, id = u32}:
//       node[pos].x = A / _DAT_00a8c758      (POSITION X — divisor runtime-init)
//       node[pos].y = B / _DAT_00a8c758      (POSITION Y — same divisor)
//       node+0x19    = id                    (THE MODEL BIND)
//       node+0x1a    = |sampler_value * _DAT_00a980d0|  (SCALE; the constant
//                      is MEASURED 2.0f in the binary bytes)
//     ROTATION/variant: NOT FOUND in the spawn loop (position + scale +
//     model id only — iter032 bound 5); identity rotation is therefore the
//     RE-faithful choice, not a placeholder.
//
// ================= ERA-BOUNDED PLACEHOLDERS (ALL LABELED) =================
// [P-CLIMATE]    which .vcl chunk applies to a world region — the per-location
//                climate input is PLAUSIBLE-UNVERIFIED (the shared-selector
//                hypothesis, iter032); the CALLER passes the explicit index.
// [P-CELLSTREAM] the per-cell record CONTENT (positions + model selection +
//                counts) — the historical stream origin is NOT closed; this
//                module generates it deterministically (placement hash +
//                count = max(0, round(col1 density)) per record per sub-cell).
//                RECONSTRUCTION-ONLY, never claimed historical.
// [P-RNG-DIV]    _DAT_00a7d7a8 (the rand01 divisor) is runtime-initialized and
//                reads 0.0 from the file (iter032 bound 2) -> 32768.0 (the
//                MSVC rand() full range; rand01 in [0,1)).
// [P-RNG-P3]     p3 = *(impl+0x24) UNVERIFIED -> 0 (documented constant).
// [P-POS-SCALE]  _DAT_00a8c758 (the u16 -> world position divisor) is
//                runtime-initialized and not statically recoverable
//                (iter032 bound 2) -> 2.0 (the u16 position space then covers
//                65,536 half-units = a world up to 32,768 units, which admits
//                both deployed calibrations AND the historical client
//                coordinates, e.g. Fort Zeus 22,467 < 32,768).
// [P-SCALE-FIELDS] the lerp bounds impl+0x44 (min) / impl+0x40 (max) are the
//                per-model scale pair; the VCL col2/col3 mapping = the census
//                min/max reading (col2 -> min, col3 -> max), field-level
//                direction STRONGLY_SUPPORTED, not byte-pinned.

export const FOLIAGE_RE = {
  binary: 'Entropia.exe 9.3.5.6746 (iter032, ledger ITER_032)',
  vclParser: 'FUN_0083a7d0 (12 values -> 0x30 records)',
  gridGen: 'FUN_0098fe00 (subdivision switch settings+4: 0/1/2/3/4 -> 1/2/4/8/16)',
  cellRecords: 'FUN_00990810 ({u16 x, u16 y, u32 model_id} 8-byte triples)',
  spawnLoop: 'FUN_0095b180 (pos = u16/K; scale = |lerp*2.0|; model id bind)',
  rngSeed: 'FUN_0098cdf0 (x = ((p4*16+p5)*16+p1+p2+p3)*0x5CC7+0x6D7; state = x*8^x)',
  rngNext: 'FUN_0098ce30 (MSVC rand(): state*0x343FD+0x269EC3, >>16 &0x7FFF)',
  rngSampler: 'FUN_0095ac30 (lerp impl+0x44..impl+0x40; p4/p5 = record u16 x/y)',
  spawnSettings: 'FUN_0095b180 builds ArkVegetationSpawnSettings {vtable, 1@+4, ...} -> default level 1',
  scaleConstant: '_DAT_00a980d0 = 2.0f (MEASURED in the binary bytes)',
  bounds: 'iter032_findings.json honest_bounds (1)-(5)',
};

export const FOLIAGE_PLACEHOLDERS = {
  'P-CLIMATE': 'per-location climate input PLAUSIBLE-UNVERIFIED (shared-selector hypothesis); explicit index passed by the caller',
  'P-CELLSTREAM': 'per-cell record content = local deterministic stand-in (historical stream origin NOT closed, iter032 bound 3)',
  'P-RNG-DIV': '_DAT_00a7d7a8 = 32768.0 (runtime-initialized; not statically recoverable, iter032 bound 2)',
  'P-RNG-P3': 'seed p3 = *(impl+0x24) UNVERIFIED -> 0',
  'P-POS-SCALE': '_DAT_00a8c758 = 2.0 (runtime-initialized; not statically recoverable, iter032 bound 2)',
  'P-SCALE-FIELDS': 'lerp min/max = VCL col2/col3 (census min/max reading; field-level direction STRONGLY_SUPPORTED)',
};

/** The MSVC rand() LCG constants (CONFIRMED in the binary bytes). */
export const MSVC_RAND_MUL = 0x343FD;    // 214013
export const MSVC_RAND_INC = 0x269EC3;   // 2531011

/**
 * VegetationRNG — the CONFIRMED vegetation RNG (FUN_0098cdf0 + FUN_0098ce30).
 * One instance = one seed + one draw (the sampler draws once per record).
 */
export class VegetationRNG {
  /** rand01 divisor — [P-RNG-DIV] era-bounded (see module header). */
  static DIVISOR = 32768.0;

  /**
   * The seed hash, VERBATIM FUN_0098cdf0:
   *   x = ((p4*0x10 + p5)*0x10 + p1 + p2 + p3) * 0x5CC7 + 0x6D7  (uint32)
   *   state = x*8 ^ x                                            (uint32)
   * p4/p5 = the record's u16 position components (POSITION-KEYED);
   * p1 = the packed query position; p2 = the view band (STRONGLY_SUPPORTED);
   * p3 = *(impl+0x24) [P-RNG-P3] = 0.
   * All arithmetic is uint32 (>>> 0), exactly as the decompile reads.
   */
  seed(p1, p2, p3, p4, p5) {
    const x =
      ((((p4 >>> 0) * 0x10 + (p5 >>> 0)) * 0x10) + (p1 >>> 0) + (p2 >>> 0) + (p3 >>> 0)) >>> 0;
    const hashed = (x * 0x5CC7 + 0x6D7) >>> 0;
    this.state = ((hashed * 8) ^ hashed) >>> 0;   // FUN_0098cdf0: state = x*8 ^ x
    return this.state;
  }

  /**
   * The next value, VERBATIM FUN_0098ce30:
   *   state = state*0x343FD + 0x269EC3 (uint32)
   *   return ((state >> 16) & 0x7FFF) / _DAT_00a7d7a8
   * The divisor is [P-RNG-DIV] 32768.0 -> rand01 in [0, 1).
   */
  next01() {
    this.state = (this.state * MSVC_RAND_MUL + MSVC_RAND_INC) >>> 0;
    return ((this.state >>> 16) & 0x7FFF) / VegetationRNG.DIVISOR;
  }
}

/**
 * The sampler, VERBATIM FUN_0095ac30 + the FUN_0095b180 scale field:
 *   value = rand01 * (max - min) + min     (lerp of impl+0x40/impl+0x44)
 *   scale = |value * 2.0|                  (spawn loop; _DAT_00a980d0 = 2.0f)
 * min/max = the per-model VCL col2/col3 [P-SCALE-FIELDS].
 */
export function sampleModelScale(rng, min, max) {
  const value = rng.next01() * (max - min) + min;
  return { value, scale: Math.abs(value * 2.0) };
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
 * generateInstances — the full CONFIRMED chain over one generation window.
 *
 * @param {object} opts
 *   records       the 12-value VCL climate records (decoded upstream)
 *   windowU16      {x0, y0, x1, y1} — the generation window in u16 position
 *                  space (world * posScale); the caller derives it from the
 *                  world region (era-bounded [P-WINDOW]: the historical grid
 *                  extents are settings-scaled and not statically pinneable).
 *   posScale       K = _DAT_00a8c758 [P-POS-SCALE] (world = u16 / K)
 *   level          the subdivision level 0..4 (FUN_0098fe00 switch input)
 *   viewBand       the p2 seed input (STRONGLY_SUPPORTED: 10/20/30)
 *   p3             the p3 seed input [P-RNG-P3] (default 0)
 * @returns {{instances: object[], census: object}}
 */
export function generateInstances({ records, windowU16, posScale, level, viewBand, p3 = 0 }) {
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
  const step = subdivisionStep(level);
  const cells = step * step;

  // The query position (p1): the window origin packed as the historical
  // component pair (FUN_007ce1e0 / FUN_0098f3a0 semantics).
  const p1 = packedQueryPosition(x0, y0);

  const cellW = (x1 - x0) / step;
  const cellH = (y1 - y0) / step;

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

          // The CONFIRMED spawn semantics (FUN_0095ac30 + FUN_0095b180):
          const rng = new VegetationRNG();
          const state0 = rng.seed(p1, viewBand, p3, ux, uy);
          const { value, scale } = sampleModelScale(rng, rec[2], rec[3]);
          const wx = ux / posScale;   // FUN_0095b180: pos.x = A / _DAT_00a8c758
          const wy = uy / posScale;   // pos.y = B / _DAT_00a8c758 (same divisor)

          instances.push({
            cell: [cx, cy], recIndex, modelId,
            u16: { x: ux, y: uy }, world: { x: wx, y: wy },
            scale, samplerValue: value,
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
    placeholders: FOLIAGE_PLACEHOLDERS,
    inputs: {
      recordCount: records.length,
      windowU16, posScale, level, step, cells,
      viewBand, p3, p1,
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
