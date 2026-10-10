// PEFoliageLabSeed.js — PE_WORLD_LAUNCHER_R1_20261010, ETAP E (contract §6.3/§6.4).
// THE DOCUMENTED LAB_SEED WRAPPER AROUND PEFoliageCore (the [P-CELLSTREAM]
// reconstruction cell-stream generator, LAB_SEED-keyed).
//
// =================== THE THREE-WAY SEPARATION (contract §6, BINDING) ===================
//   ORIGINAL_CLIMATE_RECORDS = the 12-value records decoded from the pinned
//       .vcl payloads by the STRICT VegetationClimateDecoder (Vegetation-
//       Climates.bnt pin 7B858401… verified at mount). This wrapper CONSUMES
//       them read-only; it never edits, converts or filters records (25.vcl
//       stays UNSUPPORTED upstream — comma tokens are never converted).
//   RECOVERED_RNG_ARITHMETIC = the EXISTING, scope-documented PE code in
//       PEFoliageCore.js: the byte-locked seed hash (FUN_0098cdf0), the MSVC
//       rand() LCG (FUN_0098ce30, constants 0x343FD/0x269EC3, /32767.0 f64),
//       the f32 lerp sampler (FUN_0095ac30) and the node-position division
//       (/65535.0, FUN_0095b180 P3/P4), with the FLOAT64 operand lock
//       (FOLIAGE_OPERAND_LOCK, iter035) and f32 rounding at the binary's own
//       FSTP points. THIS MODULE IMPORTS AND CALLS THOSE EXPORTS AS-IS.
//       PEFoliageCore.js is NEVER EDITED (verified byte-identical by the
//       WORLD_VEG_CORE_UNTOUCHED gate).
//   INSTANCE_DISTRIBUTION = RECONSTRUCTION-ONLY, until the historical
//       cell-stream source is proven (iter032 bound 3, [P-CELLSTREAM]):
//       the per-cell RECORD CONTENT (positions + which model lands where).
//       PEFoliageCore.generateInstances' own placementHash is the SEEDLESS
//       documented stand-in; THIS wrapper replaces that stand-in component
//       with a LAB_SEED-KEYED deterministic stand-in (labPlacementHash below)
//       while reusing every byte-locked piece. NEVER claimed historical.
//
// =================== WHY A WRAPPER (documented, contract §6.3) ===================
//   PEFoliageCore.generateInstances has NO LAB_SEED input — by design: its
//   byte-locked RNG chain must stay untouched, and its internal placement
//   hash is not seed-keyed. The contract requires the LAB_SEED to influence
//   the RECONSTRUCTION cell stream / distribution through a DOCUMENTED
//   wrapper while the byte-locked seed/RNG/float arithmetic stays as-is.
//   This module is that wrapper:
//     - the [P-CELLSTREAM] stand-in (WHERE instances land inside a cell) is
//       re-derived here, keyed on (labSeed, sub-cell u16 box origin, modelId,
//       j) — the SAME hash shape as PEFoliageCore.placementHash with the
//       LAB_SEED mixed in (a reconstruction knob over a reconstruction
//       component; the historical stream origin stays NOT_CLOSED);
//     - the byte-locked chain is called VERBATIM per generated record:
//       VegetationRNG.seed/next01 (via sampleModelScale) with the SAME
//       p1/p2/p3/p4/p5 inputs PEFoliageCore computes, and the node positions
//       node01 = f32(u16 / NODE_POS_DIVISOR) with the exported locked
//       constant;
//     - LAB_SEED is NEVER equated with the unestablished original p3:
//       p3 stays 0 ([P-RNG-P3], shown separately in the UI/census).
//
// =================== THE PER-TILE WINDOW CALIBRATION ([P-WINDOW], CURRENT_RUNTIME_CALIBRATION) ===================
//   The generation unit is ONE terrain tile (gx, gy) — the streaming window
//   key (determinism is per tileKey: the same tile regenerates the same set
//   regardless of load order). The [P-WINDOW] mapping of this launcher:
//     u16 record space  =  world meters x U16_PER_WORLD_METER (2.0 — the SAME
//                           documented page calibration as the deployed
//                           foliage page, terrain/foliage_system.js);
//     tile u16 box      =  [gx * TILE_U16, (gx+1) * TILE_U16) x
//                          [gy * TILE_U16, (gy+1) * TILE_U16),
//                           TILE_U16 = tileWorldMeters * U16_PER_WORLD_METER
//                           (= 128 for the 64 m launcher tile);
//     tile world box    =  [gx * tileWorldMeters, (gx+1) * tileWorldMeters)
//                           (the launcher adapter meters: 2 m/sample, 32
//                           samples per tile — CURRENT_RUNTIME_CALIBRATION,
//                           the SAME preset as the terrain view).
//   Edge ownership: every instance position is generated STRICTLY INSIDE its
//   tile's u16 half-open box, so no position can be claimed by two tiles —
//   the border-duplicate prevention is BY CONSTRUCTION (measured by the
//   WORLD_VEG_EDGE_OWNERSHIP gate). The instance key carries the tile key.
//
// =================== THE PREVIEW-DENSITY FILTER (contract §6.7, RECONSTRUCTION) ===================
//   count per record per sub-cell = max(0, round(col1 * densityPercent/100))
//   — the SAME count rule as PEFoliageCore ([P-CELLSTREAM]: count =
//   max(0, round(col1))) scaled by the preview-density percent. At 100% the
//   counts equal the PEFoliageCore rule exactly. The .vcl col1 values are
//   ORIGINAL DATA and are never modified; the filter is a labeled
//   reconstruction preview knob (never a claim about historical counts).
//   col4/col5 (the census "elevation band" candidates) are carried RAW on
//   each instance as elevationBand {min,max} — NO filtering is applied (the
//   band semantics are UNVERIFIED; the same no-filter discipline as the
//   deployed foliage page).

'use strict';

import {
  VegetationRNG, sampleModelScale, subdivisionStep, packedQueryPosition,
  NODE_POS_DIVISOR, FOLIAGE_OPERAND_LOCK, FOLIAGE_RE, FOLIAGE_PLACEHOLDERS,
} from './PEFoliageCore.js';

export const LABSEED_WRAPPER_VERSION = 'peworld-foliage-labseed-v2';

// PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 — THE v2 CHANGES (both RECONSTRUCTION
// wrapper policy, versioned; the byte-locked PEFoliageCore chain is untouched):
//   (a) RECINDEX IDENTITY (contract §6.1): the LAB placement hash now mixes
//       recIndex in. Duplicate model rows (the 0x30 row vectors — e.g. profile
//       0 records 8 and 9, both model 166878) are SEPARATE climate records;
//       pre-v2 they generated IDENTICAL positions. A true random collision is
//       a different (honest) phenomenon from this wrapper defect — measured
//       by the PRE/POST WL-5 gates.
//   (b) FRACTIONAL DENSITY (contract §6.3): the per-tile/per-cell count is now
//       floor + a DETERMINISTIC fractional extra (a stable hash test against
//       the fractional part), replacing the identical per-tile Math.round
//       that vanished small positive records everywhere at 50% (R1 measured:
//       3 of 10 IDs instantiated). Monotonicity: floor(v) is non-decreasing in
//       density and the fractional test fires once and stays fired within a
//       bucket (hash < frac(d) and frac grows) — increasing density never
//       flips earlier identities; density=0 gives exactly zero; the count
//       stays LINEAR in the source weight col1 (expected value = col1*d% —
//       the source weights are preserved rather than forcing every model
//       into every tile).
export const LAB_DENSITY_POLICY = Object.freeze({
  version: 'labseed-density-v2-fractional',
  rule: 'count(record, cell, tile) = floor(v) + (densityHash01(labSeed, gx, gy, cellX, cellY, recIndex, modelId) < frac(v) ? 1 : 0), v = col1 * densityPercent / 100',
  monotoneInDensity: 'floor(v) non-decreasing + the fractional test, once fired within a bucket, stays fired (hash < frac grows monotonically within the bucket)',
  densityZero: 'v = 0 → count = 0 (exactly zero)',
  note: 'RECONSTRUCTION preview policy (the .vcl col1 values are ORIGINAL DATA, never modified); at 100% the expected count equals PEFoliageCore’s round(col1) in expectation but no longer clamps small records to whole tiles identically',
});

/** The three-way separation labels, surfaced verbatim in the UI + artifacts
 * (contract §6; the single source of truth for the Etap E labels). */
export const VEGETATION_THREE_WAY_SEPARATION = Object.freeze({
  ORIGINAL_CLIMATE_RECORDS: 'data from the pinned .vcl files (strict VegetationClimateDecoder; VegetationClimates.bnt pin 7B858401C3EEBDA574DF4B4517E7FB2A8149C283885F27187682AA1239C745F4 verified at mount); consumed READ-ONLY; 25.vcl stays UNSUPPORTED (comma tokens — never converted)',
  RECOVERED_RNG_ARITHMETIC: 'the existing PEFoliageCore byte-locked seed/RNG/float chain (FUN_0098cdf0/FUN_0098ce30/FUN_0095ac30 + node01=/65535.0 f32; FLOAT64 operand lock iter035) — imported UNTOUCHED and called AS-IS by the LAB_SEED wrapper',
  INSTANCE_DISTRIBUTION: 'reconstruction-only until the cell-stream source is proven (iter032 bound 3): the LAB_SEED-keyed deterministic cell-stream stand-in in this wrapper + the [P-WINDOW] per-tile calibration — NEVER claimed historical; placement 1:1 NOT claimed',
});

/** The [P-WINDOW] calibration descriptor (CURRENT_RUNTIME_CALIBRATION —
 * carried in every census; NOT a historical engine claim). */
export const LABSEED_WINDOW_CALIBRATION = Object.freeze({
  label: 'CURRENT_RUNTIME_CALIBRATION',
  u16PerWorldMeter: 2.0,
  tileU16: 128,            // = 64 m tile x 2.0 (the launcher tile preset)
  tileWorldMeters: 64,     // 32 samples x 2 adapter meters/sample
  note: 'the SAME documented page calibration family as the deployed foliage page (terrain/foliage_system.js: u16 = world x 2.0); the historical grid extents are settings-scaled and the visualizer [0,1]->world transform is NOT decompiled (iter032 bound 5)',
});

/** The per-tile u16 span for a tile of `tileWorldMeters` adapter meters. */
export function tileU16Span(tileWorldMeters = LABSEED_WINDOW_CALIBRATION.tileWorldMeters,
                            u16PerWorldMeter = LABSEED_WINDOW_CALIBRATION.u16PerWorldMeter) {
  return Math.round(tileWorldMeters * u16PerWorldMeter);
}

/** [P-CELLSTREAM] THE LAB_SEED-KEYED PLACEMENT HASH — RECONSTRUCTION-ONLY.
 * v2: the RECIDX MIX-IN (contract §6.1). The same splitmix-finalize shape as
 * PEFoliageCore's internal placementHash, with the LAB_SEED and the RECORD
 * INDEX mixed into the first xor stage: duplicate model rows are SEPARATE
 * climate records and get SEPARATE position streams (pre-v2 they generated
 * identical positions — the PRE/POST WL-5 gates measure the change). This
 * replaces the seedless [P-CELLSTREAM] stand-in INSIDE this wrapper only
 * (PEFoliageCore is never edited). Keyed on the sub-cell u16 box origin
 * (bx0, by0 — which encodes tile + sub-cell), recIndex, modelId and j: two
 * calls (j*2, j*2+1) give the two independent position fractions, exactly
 * like PEFoliageCore. */
function labPlacementHash(labSeed, bx0, by0, recIndex, modelId, j) {
  let h = (((labSeed >>> 0) * 0x9E3779B1) ^ ((bx0 >>> 0) * 0x85EBCA77) ^
           ((by0 >>> 0) * 0xC2B2AE3D) ^ ((recIndex >>> 0) * 0x94D0BB4B) ^
           ((modelId >>> 0) * 0x27D4EB2F) ^ ((j >>> 0) * 0x165667B1)) >>> 0;
  h = Math.imul(h ^ (h >>> 16), 0x21F0AAAD) >>> 0;
  h = Math.imul(h ^ (h >>> 15), 0x735A2D97) >>> 0;
  return (h ^ (h >>> 15)) >>> 0;
}

/** The DETERMINISTIC fractional-density extra (contract §6.3, v2): a stable
 *  hash test against the fractional part of v — the "stochastic" rounding is
 *  a pure function of (tile, cell, record, model) — NEVER the LAB_SEED and
 *  never a runtime RNG — so the seed moves POSITIONS only while DENSITY
 *  controls COUNTS (the R1 determinism semantics preserved; the same config
 *  always yields the same counts). */
function densityHash01(gx, gy, cellX, cellY, recIndex, modelId) {
  let h = (((gx >>> 0) * 0x85EBCA77) ^ ((gy >>> 0) * 0xC2B2AE3D) ^
           ((cellX >>> 0) * 0x27D4EB2F) ^ ((cellY >>> 0) * 0x165667B1) ^
           ((recIndex >>> 0) * 0x94D0BB4B) ^ ((modelId >>> 0) * 0x8E3D9D1B)) >>> 0;
  h = Math.imul(h ^ (h >>> 16), 0x21F0AAAD) >>> 0;
  h = Math.imul(h ^ (h >>> 15), 0x735A2D97) >>> 0;
  return ((h ^ (h >>> 15)) >>> 0) / 4294967296; // [0,1)
}

/**
 * generateTileInstances — the DOCUMENTED LAB_SEED wrapper over the
 * PEFoliageCore chain, for ONE terrain tile (the tileKey determinism unit).
 *
 * @param {object} opts
 *   records        the 12-value .vcl climate records (ORIGINAL_CLIMATE_RECORDS,
 *                  decoded upstream by the STRICT decoder; read-only)
 *   labSeed        the preview seed (LAB_SEED; NEVER the unestablished
 *                  original p3; influences the [P-CELLSTREAM] stand-in only)
 *   gx, gy         the tile grid key (0-based, filename-xy regular grid)
 *   level          the subdivision level 0..4 (default 1 = the engine default
 *                  settings+4=1 -> step 2, FUN_0098fe00)
 *   viewBand       the p2 seed input (default 10; STRONGLY_SUPPORTED 10/20/30)
 *   p3             the p3 seed input ([P-RNG-P3] UNVERIFIED -> 0; default 0;
 *                  shown SEPARATELY in the UI/census — never the LAB_SEED)
 *   densityPercent the preview-density filter 0..100 (default 100 = the exact
 *                  PEFoliageCore count rule round(col1) per record per
 *                  sub-cell; RECONSTRUCTION preview knob)
 *   tileWorldMeters the launcher tile size in adapter meters (default 64)
 *   u16PerWorldMeter the [P-WINDOW] u16-per-meter calibration (default 2.0)
 * @returns {{instances: object[], census: object}}
 */
export function generateTileInstances({
  records, labSeed, gx, gy,
  level = 1, viewBand = 10, p3 = 0,
  densityPercent = 100,
  tileWorldMeters = LABSEED_WINDOW_CALIBRATION.tileWorldMeters,
  u16PerWorldMeter = LABSEED_WINDOW_CALIBRATION.u16PerWorldMeter,
} = {}) {
  if (!Array.isArray(records) || records.length === 0) {
    throw new Error('[PEFoliageLabSeed] no climate records (empty climate — the caller must surface the profile decode state honestly)');
  }
  for (const r of records) {
    if (!Array.isArray(r) || r.length !== 12) {
      throw new Error('[PEFoliageLabSeed] climate record is not the 12-value layout (FUN_0083a7d0)');
    }
  }
  if (!Number.isInteger(gx) || !Number.isInteger(gy) || gx < 0 || gy < 0) {
    throw new Error(`[PEFoliageLabSeed] invalid tile key ${gx},${gy}`);
  }
  if (!Number.isInteger(labSeed) || labSeed < 0 || labSeed > 0xFFFFFFFF) {
    throw new Error(`[PEFoliageLabSeed] invalid labSeed ${labSeed} (uint32 preview seed)`);
  }
  const dp = Math.min(100, Math.max(0, densityPercent));
  if (!Number.isFinite(dp)) throw new Error('[PEFoliageLabSeed] invalid densityPercent');
  const tileU16 = tileU16Span(tileWorldMeters, u16PerWorldMeter);
  if (tileU16 <= 0) throw new Error(`[PEFoliageLabSeed] invalid tile u16 span ${tileU16}`);
  const x0 = gx * tileU16, y0 = gy * tileU16;
  const x1 = (gx + 1) * tileU16, y1 = (gy + 1) * tileU16;
  if (x1 > 0x10000 || y1 > 0x10000) {
    throw new Error(`[PEFoliageLabSeed] tile ${gx},${gy} u16 box [${x0},${y0}..${x1},${y1}] exceeds the u16 record space 0x10000`);
  }
  const windowU16 = { x0, y0, x1, y1 };
  // The [P-WINDOW] tile world box (adapter meters — CURRENT_RUNTIME_CALIBRATION).
  const windowWorld = {
    x0: gx * tileWorldMeters, y0: gy * tileWorldMeters,
    x1: (gx + 1) * tileWorldMeters, y1: (gy + 1) * tileWorldMeters,
  };
  // The [P-WINDOW] linear u16->world calibration (the CALLER's reconstruction
  // choice, the same rule as PEFoliageCore.generateInstances lines).
  const u16ToWorldX = (u) => windowWorld.x0 + (u - x0) / (x1 - x0) * (windowWorld.x1 - windowWorld.x0);
  const u16ToWorldY = (u) => windowWorld.y0 + (u - y0) / (y1 - y0) * (windowWorld.y1 - windowWorld.y0);

  const step = subdivisionStep(level);   // VERBATIM FUN_0098fe00 (imported, untouched)
  const cells = step * step;
  // p1: the packed query position of the TILE origin (the per-tileKey seed
  // input — the same window-origin packing PEFoliageCore uses; documented
  // reconstruction choice making determinism per-tileKey).
  const p1 = packedQueryPosition(x0, y0);

  const cellW = (x1 - x0) / step;
  const cellH = (y1 - y0) / step;

  const instances = [];
  const perCell = [];
  const perModel = new Map();
  const zeroCountRecords = [];

  for (let cy = 0; cy < step; cy++) {
    for (let cx = 0; cx < step; cx++) {
      const bx0 = Math.floor(x0 + cx * cellW), by0 = Math.floor(y0 + cy * cellH);
      const bx1 = Math.floor(x0 + (cx + 1) * cellW), by1 = Math.floor(y0 + (cy + 1) * cellH);
      const u16Box = { x0: bx0, y0: by0, x1: bx1, y1: by1 };
      const bw = Math.max(1, bx1 - bx0), bh = Math.max(1, by1 - by0);
      const cell = { cellX: cx, cellY: cy, u16Box, counts: {}, total: 0 };

      // Per climate record (the record IS the unit — duplicate model ids with
      // different bands are separate engine rows, per the 0x30 row vector).
      records.forEach((rec, recIndex) => {
        const modelId = rec[0] | 0;
        const density = rec[1];
        // The preview-density filter (RECONSTRUCTION, v2 FRACTIONAL — see
        // LAB_DENSITY_POLICY): floor(v) + a deterministic fractional extra
        // keyed on (labSeed, tile, cell, recIndex, modelId). Monotone in the
        // density; 0 → exactly 0; the source weights stay linear.
        const v = density * dp / 100;
        const base = Math.floor(Math.max(0, v));
        const frac = v - Math.floor(Math.max(0, v));
        const extra = frac > 0 && densityHash01(gx, gy, cx, cy, recIndex, modelId) < frac ? 1 : 0;
        const count = base + extra;
        cell.counts[`rec${recIndex}_m${modelId}`] = count;
        if (count === 0) {
          zeroCountRecords.push({ recIndex, modelId, density });
          return;
        }
        let m = perModel.get(modelId);
        if (!m) { m = { modelId, count: 0, scaleMin: Infinity, scaleMax: -Infinity }; perModel.set(modelId, m); }

        for (let j = 0; j < count; j++) {
          // [P-CELLSTREAM] THE LAB_SEED-KEYED STAND-IN RECORD {u16 x, u16 y,
          // u32 model_id} (the FUN_00990810 triple layout): the position lands
          // STRICTLY INSIDE the tile's half-open u16 box (edge ownership by
          // construction — WORLD_VEG_EDGE_OWNERSHIP). v2: recIndex is mixed in
          // (duplicate records get SEPARATE position streams).
          const hA = labPlacementHash(labSeed, bx0, by0, recIndex, modelId, j * 2);
          const hB = labPlacementHash(labSeed, bx0, by0, recIndex, modelId, j * 2 + 1);
          const ux = bx0 + Math.min(bw - 1, Math.floor(((hA >>> 16) & 0xFFFF) / 65536 * bw));
          const uy = by0 + Math.min(bh - 1, Math.floor((hB & 0xFFFF) / 65536 * bh));

          // ============ THE RECOVERED, BYTE-LOCKED CHAIN (imported, AS-IS) ============
          const rng = new VegetationRNG();
          const state0 = rng.seed(p1, viewBand, p3, ux, uy);       // FUN_0098cdf0 verbatim
          const { value, scale } = sampleModelScale(rng, rec[2], rec[3]); // FUN_0095ac30 + P5/P6 verbatim
          // P3/P4 verbatim: the node-local [0,1] positions with the LOCKED divisor.
          const nodeX = Math.fround(ux / NODE_POS_DIVISOR);
          const nodeY = Math.fround(uy / NODE_POS_DIVISOR);
          // ============================================================================

          // The [P-WINDOW] calibration (NOT a binary claim).
          const wx = u16ToWorldX(ux);
          const wy = u16ToWorldY(uy);

          instances.push({
            key: `${gx},${gy}|r${recIndex}m${modelId}|c${cx},${cy}|${j}`,
            tile: { gx, gy }, recIndex, modelId, cell: [cx, cy], j,
            u16: { x: ux, y: uy },
            node01: { x: nodeX, y: nodeY },   // the BINARY node fields (f32)
            world: { x: wx, y: wy },          // the caller's calibration
            scale,                            // the BINARY node scale (f32)
            samplerValue: value,              // the lerp value (f32)
            seedInputs: { p1, p2: viewBand, p3, p4: ux, p5: uy },
            rngState0: state0,
            elevationBand: { min: rec[4], max: rec[5] }, // carried RAW (cols UNVERIFIED — no filtering)
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
    wrapperVersion: LABSEED_WRAPPER_VERSION,
    densityPolicy: LAB_DENSITY_POLICY,
    threeWaySeparation: VEGETATION_THREE_WAY_SEPARATION,
    reChain: FOLIAGE_RE,
    operandLock: FOLIAGE_OPERAND_LOCK,
    placeholders: FOLIAGE_PLACEHOLDERS,
    windowCalibration: { ...LABSEED_WINDOW_CALIBRATION, tileU16, tileWorldMeters, u16PerWorldMeter },
    inputs: {
      labSeed, gx, gy, level, step, cells, viewBand, p3,
      densityPercent: dp,
      windowU16, windowWorld, p1,
      recordCount: records.length,
      constants: {
        nodePosDivisor: NODE_POS_DIVISOR,
        rand01Divisor: FOLIAGE_OPERAND_LOCK.rand01Divisor.f64,
        nodeScaleMul: FOLIAGE_OPERAND_LOCK.nodeScaleMul.f64,
      },
    },
    totals: {
      instances: instances.length,
      distinctModelsInstantiated: perModel.size,
      zeroCountRecords: zeroCountRecords.length,
    },
    perCell, perModel, zeroCountRecords,
  };
  return { instances, census };
}
