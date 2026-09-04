// PETerrainCore.js — MILESTONE 1-E ITER 019 (CLEAN_RUNTIME_FOUNDATION)
// PE Runtime Core: canonical terrain REGION assembly from canonical TerrainTile
// objects (produced by PESourceMount.getTerrainTile — the ONLY sanctioned input;
// ZERO legacy runtime input). This module owns PE terrain WORLD semantics:
// grid placement, world height mapping, region vertex/index construction.
// The renderer (Three.js r185) receives plain arrays — NO format knowledge.
//
// HEIGHT SEMANTICS (audited, iter015 evidence — FUN_0047fb20 @ 0x0047FB20):
//   height = min + (max - min) * u16 * (1/65535)
//   FUNCTION_IDENTITY = CONFIRMED; OBSERVED_OPERATION = CONFIRMED;
//   FINAL_SEMANTIC_ROLE = STRONGLY_SUPPORTED (the terrain height query path).
//   The runtime per-tile min/max (tile_obj+0x24/+0x28 floats) source is
//   UNRESOLVED — TDF sub-header (payload 52..63) reads ZERO on all sampled
//   content tiles (iter019 probe). Until resolved, this module uses the
//   IDENTITY lerp (min=0, max=65535 in u16 space) — equivalent to raw u16 —
//   scaled to meters by the deployed runtime calibration heightScale = 1/128
//   (HEIGHT_SCALE_CALIBRATION, CURRENT_RUNTIME_CALIBRATION,
//   STRONGLY_SUPPORTED, NOT a proven historical engine fact). The lerp form is
//   kept EXPLICIT so a resolved per-tile min/max plugs in without restructure.

import { HEIGHT_SCALE_CALIBRATION } from '../pesource/TerrainTile.js';

export const PE_TERRAIN_TILE_SIZE = 32;           // TDF tile edge in height samples
export const PE_TERRAIN_METER_PER_SAMPLE = 2;     // CURRENT_RUNTIME_CALIBRATION (legacy
                                                  // runtime world scale=2, EudoriaWorldTransform
                                                  // MODE_CONFIGS.legacy.scale) — NOT a proven
                                                  // historical engine fact
export const HEIGHT_QUERY = {
  function: 'FUN_0047fb20',
  identity: 'CONFIRMED',
  observedOperation: 'min + (max - min) * u16 * (1/65535)',
  minSource: 'UNRESOLVED (identity lerp min=0 used; sub-header reads zero on samples)',
  maxSource: 'UNRESOLVED (identity lerp max=65535 used; sub-header reads zero on samples)',
  heightScale: HEIGHT_SCALE_CALIBRATION,
  finalSemanticRole: 'STRONGLY_SUPPORTED (terrain height query path)',
};

/** World height in meters for one raw u16 sample (FUN_0047fb20 form, identity lerp). */
export function worldHeightMeters(u16) {
  const min = 0, max = 65535; // identity lerp — see HEIGHT_QUERY.minSource/maxSource
  const normalized = min + (max - min) * u16 * (1 / 65535); // = u16 (explicit lerp form)
  return normalized * HEIGHT_SCALE_CALIBRATION.u16PerMeter ** -1; // u16 / 128 -> meters
}

/**
 * PETerrainRegion — canonical region assembled from an NxN block of
 * TerrainTile objects. Tiles are DISJOINT 32x32 sample blocks; the region
 * sample grid is the direct concatenation (no overlap, no averaging, no
 * repair). Tile-border sample differences are ORIGINAL DATA and are recorded
 * as a diagnostic (see _recordTileSeams).
 */
export class PETerrainRegion {
  /**
   * @param {TerrainTile[][]} tiles 2D array [row=y][col=x] of canonical tiles,
   *        each .length = regionTilesX; regionTilesY = tiles.length.
   */
  constructor(tiles) {
    if (!Array.isArray(tiles) || tiles.length < 1 || !Array.isArray(tiles[0])) {
      throw new Error('[PETerrainRegion] tiles must be a 2D array');
    }
    this.regionTilesX = tiles[0].length;
    this.regionTilesY = tiles.length;
    for (let y = 0; y < tiles.length; y++) {
      if (tiles[y].length !== this.regionTilesX) throw new Error('[PETerrainRegion] ragged tile block');
      for (let x = 0; x < this.regionTilesX; x++) {
        const t = tiles[y][x];
        if (!t || !t.heights || t.heights.length !== 1024) {
          throw new Error(`[PETerrainRegion] invalid tile at ${x},${y}`);
        }
        if (t.gridX !== tiles[0][0].gridX + x || t.gridY !== tiles[0][0].gridY + y) {
          throw new Error(`[PETerrainRegion] tile grid mismatch at ${x},${y}`);
        }
      }
    }
    this.tiles = tiles;
    this.originGridX = tiles[0][0].gridX;
    this.originGridY = tiles[0][0].gridY;
    this._recordTileSeams();
  }

  /**
   * Tile-border seam RECORDING (data diagnostic, non-fatal). Tiles are DISJOINT
   * 32x32 sample blocks (220x32 = 7040 — NO corner overlap), so adjacent tiles
   * carry INDEPENDENT border samples; the observed differences are ORIGINAL DATA
   * (iter019 probe: 191/192 east, 192/192 south borders differ in the P0 region).
   * The canonical chunk pipeline handled continuity at the 513x513 chunk level;
   * this region module performs NO seam averaging or repair (no aggressive
   * cleaning — FINAL_LOCKED discipline).
   */
  _recordTileSeams() {
    let eastPairs = 0, eastDiffs = 0, eastMaxAbs = 0;
    let southPairs = 0, southDiffs = 0, southMaxAbs = 0;
    for (let y = 0; y < this.regionTilesY; y++) {
      for (let x = 0; x < this.regionTilesX; x++) {
        const t = this.tiles[y][x];
        if (x + 1 < this.regionTilesX) {
          const right = this.tiles[y][x + 1];
          for (let r = 0; r < 32; r++) {
            eastPairs++;
            const d = t.heights[r * 32 + 31] - right.heights[r * 32 + 0];
            if (d !== 0) eastDiffs++;
            if (Math.abs(d) > eastMaxAbs) eastMaxAbs = Math.abs(d);
          }
        }
        if (y + 1 < this.regionTilesY) {
          const below = this.tiles[y + 1][x];
          for (let c = 0; c < 32; c++) {
            southPairs++;
            const d = t.heights[31 * 32 + c] - below.heights[0 * 32 + c];
            if (d !== 0) southDiffs++;
            if (Math.abs(d) > southMaxAbs) southMaxAbs = Math.abs(d);
          }
        }
      }
    }
    this.tileSeamDiagnostic = {
      east: { pairs: eastPairs, diffs: eastDiffs, maxAbs: eastMaxAbs },
      south: { pairs: southPairs, diffs: southDiffs, maxAbs: southMaxAbs },
      interpretation: 'ORIGINAL_DATA (disjoint tiles, no repair applied)',
    };
  }

  /** Raw u16 sample at region-local (vx, vy) — region vertex grid (tilesX*32+1)^2 NOT used;
   *  vertex grid here = SAMPLE grid (tilesX*32) with the region assembled by
   *  corner-sharing: value at (vx,vy) = tile(vx/32, vy/32).heights[vy%32][vx%32]. */
  rawSample(vx, vy) {
    const tx = Math.floor(vx / PE_TERRAIN_TILE_SIZE), ty = Math.floor(vy / PE_TERRAIN_TILE_SIZE);
    const lx = vx % PE_TERRAIN_TILE_SIZE, ly = vy % PE_TERRAIN_TILE_SIZE;
    return this.tiles[ty][tx].heights[ly * PE_TERRAIN_TILE_SIZE + lx];
  }

  /**
   * Canonical render geometry: sample-grid mesh (no extra border vertices).
   * World space: +X = grid x (meters), +Y = height (meters), +Z = grid y
   * (south). PE world axis conventions beyond this calibration are UNRESOLVED
   * and irrelevant to P0 byte-faithfulness.
   * @returns {{positions: Float32Array, indices: Uint32Array, sampleGridX: number, sampleGridY: number}}
   */
  buildGeometry() {
    const sx = this.regionTilesX * PE_TERRAIN_TILE_SIZE;
    const sy = this.regionTilesY * PE_TERRAIN_TILE_SIZE;
    const positions = new Float32Array(sx * sy * 3);
    for (let vy = 0; vy < sy; vy++) {
      for (let vx = 0; vx < sx; vx++) {
        const i = (vy * sx + vx) * 3;
        positions[i] = vx * PE_TERRAIN_METER_PER_SAMPLE;
        positions[i + 1] = worldHeightMeters(this.rawSample(vx, vy));
        positions[i + 2] = vy * PE_TERRAIN_METER_PER_SAMPLE;
      }
    }
    const quads = (sx - 1) * (sy - 1);
    const indices = new Uint32Array(quads * 6);
    let q = 0;
    for (let vy = 0; vy < sy - 1; vy++) {
      for (let vx = 0; vx < sx - 1; vx++) {
        const a = vy * sx + vx, b = a + 1, c = a + sx, d = c + 1;
        indices[q++] = a; indices[q++] = c; indices[q++] = b;
        indices[q++] = b; indices[q++] = c; indices[q++] = d;
      }
    }
    return { positions, indices, sampleGridX: sx, sampleGridY: sy };
  }

  /** Per-tile provenance of the region (the provenance chain, intact). */
  provenanceList() {
    const out = [];
    for (let y = 0; y < this.regionTilesY; y++) {
      for (let x = 0; x < this.regionTilesX; x++) out.push(this.tiles[y][x].provenance);
    }
    return out;
  }
}
