// IsoPatchSelection.js — JOB W03 ISO_TERRAIN_VERTICAL_SLICE (2026-10-30)
// DYNAMIC tile-patch selection derived from the MOUNTED ARCHIVE INDEX (not
// hardcoded coordinates): enumerate the BUNT index of the ISO_5_1_0_0
// 50.bnt, build the filename-xy grid occupancy map, and scan row-major for
// the FIRST NxN patch whose tiles all decode as standard 32x32 TDF tiles
// AND carry real terrain (not an all-zero water/nodata patch).
//
// Explicit handling (contract req 4):
//   - SENTINEL (7ffe7ffe.tdf) and any out-of-grid names are excluded from
//     regular addressing (loudly counted, never silently used).
//   - NODATA/WATER: raw u16 == 0 samples are counted per patch; a patch that
//     is ALL zeros is REJECTED as nodata, not rendered as fake flat terrain.
//   - No interpolation/repair — heights stay RAW uint16 (IR numbers, no
//     conversion); display scale is the consumer's labeled calibration.
import { gridFromName, isSentinelName } from '../pesource/TdfDecoder.js';

export const ISO_GRID = { GRID_X: 220, GRID_Y: 236 }; // regular filename-xy extent

/**
 * Build the occupancy map from an enumerate() result (PESourceMount).
 * @returns {{occupancy: Set<string>, census: object}}
 */
export function buildGridCensus(entries) {
  const occupancy = new Set();
  let sentinel = 0, outOfGrid = 0, badNames = 0, duplicates = 0;
  const seen = new Set();
  for (const e of entries) {
    if (seen.has(e.name)) { duplicates++; continue; }
    seen.add(e.name);
    if (isSentinelName(e.name)) { sentinel++; continue; }
    if (!/^[0-9a-fA-F]{8}\.tdf$/.test(e.name)) { badNames++; continue; }
    const { gridX, gridY } = gridFromName(e.name);
    if (gridX >= ISO_GRID.GRID_X || gridY >= ISO_GRID.GRID_Y) { outOfGrid++; continue; }
    occupancy.add(`${gridX},${gridY}`);
  }
  return {
    occupancy,
    census: {
      indexEntries: entries.length,
      regularTiles: occupancy.size,
      sentinelEntries: sentinel,
      outOfGridEntries: outOfGrid,
      badNameEntries: badNames,
      duplicateEntries: duplicates,
    },
  };
}

/**
 * Find the FIRST working NxN patch, row-major over the filename-xy grid.
 * A patch "works" iff: all N*N tiles exist in the index, all decode through
 * getTerrainTile (standard 32x32 TDF), and the region carries real terrain
 * (maxRawHeight > 0 and nonZeroSamples >= minNonZero) — all-zero water/
 * nodata patches are skipped EXPLICITLY, never rendered as fake flat land.
 * @param {object} mount PESourceMount with ISO_5_1_0_0:Terrain/50.bnt mounted
 * @param {object} opts { era, n=3, minNonZero=102 }
 * @returns {{originGridX, originGridY, n, tiles, patchesTried, patchStats}}
 */
export async function findFirstWorkingPatch(mount, { era, n = 3, minNonZero = 102 }) {
  const entries = await mount.enumerate({ era, container: 'Terrain/50.bnt' });
  const { occupancy, census } = buildGridCensus(entries);
  let patchesTried = 0;
  const rejects = [];
  for (let gy = 0; gy + n <= ISO_GRID.GRID_Y; gy++) {
    for (let gx = 0; gx + n <= ISO_GRID.GRID_X; gx++) {
      // occupancy pre-check (cheap) before decode
      let allPresent = true;
      for (let y = 0; y < n && allPresent; y++) {
        for (let x = 0; x < n; x++) {
          if (!occupancy.has(`${gx + x},${gy + y}`)) { allPresent = false; break; }
        }
      }
      if (!allPresent) continue;
      patchesTried++;
      const tiles = [];
      let decodeOk = true;
      try {
        for (let y = 0; y < n; y++) {
          const row = [];
          for (let x = 0; x < n; x++) {
            row.push(await mount.getTerrainTile({ era, gridX: gx + x, gridY: gy + y }));
          }
          tiles.push(row);
        }
      } catch (err) {
        decodeOk = false;
        rejects.push({ originGridX: gx, originGridY: gy, reason: `DECODE_ERROR: ${err.message}` });
      }
      if (!decodeOk) continue;
      // explicit nodata/water accounting — RAW u16, no conversion
      let nonZero = 0, maxH = 0, minH = 65535, zeros = 0;
      for (const row of tiles) for (const t of row) for (const h of t.heights) {
        if (h === 0) zeros++;
        else nonZero++;
        if (h > maxH) maxH = h;
        if (h < minH) minH = h;
      }
      const stats = { nonZeroSamples: nonZero, zeroSamples: zeros, maxRawHeight: maxH, minRawHeight: minH };
      if (maxH === 0 || nonZero < minNonZero) {
        rejects.push({ originGridX: gx, originGridY: gy, reason: 'NODATA_WATER_ALL_ZERO', stats });
        continue;
      }
      return {
        originGridX: gx, originGridY: gy, n,
        tiles, patchesTried, rejects, census,
        patchStats: stats,
        selectionRule: `first row-major ${n}x${n} patch with all tiles decodable + maxRawHeight>0 + nonZero>=${minNonZero}`,
      };
    }
  }
  throw new Error(`[IsoPatchSelection] no working ${n}x${n} patch found (${patchesTried} tried; ${rejects.length} rejected)`);
}

// =====================================================================
// W06 — MULTIPATCH STREAMING expansion-window helpers (2026-10-30)
// =====================================================================
// Contract §7 streaming: expand the visible area from the fixture-pinned
// core 3x3 to a 5x5 window, streaming tiles ONE BY ONE with an explicit
// ocean/nodata skip. The per-tile heuristic is the SAME census heuristic
// the W03/W05 patch scan uses (minNonZero=102 of 1024 samples — i.e. a
// tile with >90% zero samples is ocean/nodata and is SKIPPED with an
// explicit log, never rendered as fake flat land).
// NOTE (explicit): the skip applies to STREAMED (ring) tiles only — the
// core 3x3 keeps its original all-9-tiles behavior (W05 material fixture
// + cross-check are pinned to those 9 tiles; fallback to 3x3 must work).
export const OCEAN_SKIP_MIN_NONZERO = 102; // nonZero <= 102 of 1024  <=>  zeros > 90%
export const OCEAN_SKIP_RULE = 'nonZero <= 102 of 1024 raw u16 samples (>90% zeros => OCEAN_NODATA skip; same census heuristic as findFirstWorkingPatch minNonZero=102)';

/** BUNT filename from grid coordinates (inverse of gridFromName). */
export function tileNameFromGrid(gridX, gridY) {
  if (!Number.isInteger(gridX) || !Number.isInteger(gridY) ||
      gridX < 0 || gridX > 219 || gridY < 0 || gridY > 235) {
    throw new Error(`[IsoPatchSelection] grid out of range 0..219/0..235: ${gridX},${gridY}`);
  }
  return gridX.toString(16).padStart(4, '0') + gridY.toString(16).padStart(4, '0') + '.tdf';
}

/** RAW u16 terrain stats for one tile — explicit nodata/water accounting. */
export function tileTerrainStats(heights) {
  let zeros = 0, nonZero = 0, maxH = 0, minH = 65535;
  for (const h of heights) {
    if (h === 0) zeros++; else nonZero++;
    if (h > maxH) maxH = h;
    if (h < minH) minH = h;
  }
  return {
    samples: heights.length, zeros, nonZero,
    zeroFraction: +(zeros / heights.length).toFixed(4),
    maxRawHeight: maxH, minRawHeight: minH,
  };
}

/** Ocean/nodata classification (W06 streaming skip heuristic). */
export function isOceanNodataTile(stats) {
  return stats.nonZero <= OCEAN_SKIP_MIN_NONZERO;
}

/**
 * NxN window CONTAINING the core patch, centered on the core when possible,
 * clamped to the regular 220x236 grid. For the W03/W05 core @(95,0) and
 * n=5 the desired center origin (94,-1) clamps to (94,0): y=0 is the grid
 * north edge, so the window extends x 94..98, y 0..4 (core at offset 1,1).
 */
export function windowContainingCore(core, n = 5) {
  if (n < core.n) throw new Error(`[IsoPatchSelection] window n=${n} smaller than core n=${core.n}`);
  const pad = (n - core.n) >> 1;
  const originX = Math.min(Math.max(core.originGridX - pad, 0), ISO_GRID.GRID_X - n);
  const originY = Math.min(Math.max(core.originGridY - pad, 0), ISO_GRID.GRID_Y - n);
  return {
    originX, originY, n,
    coreOffsetX: core.originGridX - originX,
    coreOffsetY: core.originGridY - originY,
    rule: `${n}x${n} window containing the ${core.n}x${core.n} core @${core.originGridX},${core.originGridY}, centered when possible, clamped to the ${ISO_GRID.GRID_X}x${ISO_GRID.GRID_Y} grid`,
  };
}

/**
 * Stream plan for the RING (window minus core), ordered NEAR-ORIGIN-FIRST:
 * ascending distance from the core patch center tile, row-major tie-break.
 * Each entry: { gridX, gridY, name, order }.
 */
export function streamRingPlan(core, win) {
  const cx = core.originGridX + (core.n - 1) / 2;
  const cy = core.originGridY + (core.n - 1) / 2;
  const inCore = (x, y) =>
    x >= core.originGridX && x < core.originGridX + core.n &&
    y >= core.originGridY && y < core.originGridY + core.n;
  const ring = [];
  for (let y = win.originY; y < win.originY + win.n; y++) {
    for (let x = win.originX; x < win.originX + win.n; x++) {
      if (!inCore(x, y)) ring.push({ gridX: x, gridY: y, name: tileNameFromGrid(x, y) });
    }
  }
  ring.sort((a, b) =>
    (((a.gridX - cx) ** 2 + (a.gridY - cy) ** 2) - ((b.gridX - cx) ** 2 + (b.gridY - cy) ** 2)) ||
    (a.gridY - b.gridY) || (a.gridX - b.gridX));
  ring.forEach((r, i) => { r.order = i; });
  return ring;
}
