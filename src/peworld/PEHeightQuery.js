// PEHeightQuery.js — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §3.2)
// THE ONE SHARED HEIGHT QUERY for rendering, trees and walking: triangle-
// exact on EXACTLY the triangles the near layer renders, with a HALO of real
// neighboring original samples beyond the rendered window edge (the
// 256-samples/0..510 vs generator-0..512 boundary resolution), and explicit
// per-instance surface status.
//
// DESIGN CONTRACT (binding):
//   - the query reproduces the quad split of PETerrainRegion.buildGeometry
//     VERBATIM: per quad (x0,z0): indices (a,c,b),(b,c,d) with a=(x0,z0),
//     b=(x0+1,z0), c=(x0,z0+1), d=(x0+1,z0+1); the split diagonal runs from
//     (x0+1,z0) to (x0,z0+1) (the anti-diagonal fx+fz=1). A height queried
//     here IS the height of the rendered triangle plane at that point —
//     measured equal by the WL-2 POST gate.
//   - calibration: worldHeightMeters (the SAME conversion the near mesh
//     applies — applied EXACTLY ONCE here; raw u16 preserved; NO smoothing,
//     NO scaling to hide steep terrain, NO re-normalization).
//   - HALO: the sampling field is a block of ORIGINAL tiles that MAY extend
//     beyond the rendered window (the caller fetches a 1-tile ring). The
//     query accepts positions anywhere on the FIELD where real samples exist;
//     positions whose quad touches a MISSING tile return null (NEVER a
//     duplicated last height, NEVER interpolation through an unknown tile,
//     NEVER y=0).
//   - missing tiles are explicit: a null return means "no real surface data
//     at this point" — the CALLER decides (stop movement / defer the
//     instance); this module never invents a surface.
'use strict';

import { worldHeightMeters, PE_TERRAIN_METER_PER_SAMPLE, PE_TERRAIN_TILE_SIZE } from './PETerrainCore.js';

export const HEIGHT_QUERY_VERSION = 'peheight-query-triangle-v1';

/** The per-instance surface status vocabulary (contract §3.2 — one instance
 * has an explicit status, never an automatic "rendered"). */
export const SURFACE_STATUS = Object.freeze({
  PLACED_ON_AVAILABLE_SURFACE: 'PLACED_ON_AVAILABLE_SURFACE',
  DEFERRED_NO_SURFACE: 'DEFERRED_NO_SURFACE',
  UNSUPPORTED_MODEL: 'UNSUPPORTED_MODEL',
  LOD_LIMITED: 'LOD_LIMITED',
});

/** The in-tile decimated sample indices of the distant LOD levels (REAL
 * original samples — decimation ONLY, never averaging; documented renderer
 * LOD policy, contract §4). */
export const LOD_DECIMATION = Object.freeze({
  mid: { perTile: 8, indices: [0, 4, 9, 13, 18, 22, 27, 31], label: 'MID_LOD_DECIMATION_8 (every ~4th ORIGINAL sample; positions are the samples’ own)' },
  far: { perTile: 4, indices: [0, 10, 21, 31], label: 'FAR_LOD_DECIMATION_4 (every ~10th ORIGINAL sample; positions are the samples’ own)' },
});

/**
 * PEHeightField — one contiguous block of ORIGINAL tiles with the shared
 * triangle query.
 */
export class PEHeightField {
  /**
   * @param {TerrainTile[][]} tiles 2D [y][x]; null entries = MISSING tiles
   *        (the query refuses to cross them — honest null, never a fill).
   * @param {object} opts { tileWorldMeters = 64 } the adapter tile size.
   */
  constructor(tiles, { tileWorldMeters = 64 } = {}) {
    if (!Array.isArray(tiles) || tiles.length < 1 || !Array.isArray(tiles[0])) {
      throw new Error('[PEHeightField] tiles must be a 2D array');
    }
    this.tilesX = tiles[0].length;
    this.tilesY = tiles.length;
    this.tileWorldMeters = tileWorldMeters;
    // the block origin derived from ANY present tile (the caller may pass a
    // field whose edge tiles are MISSING — e.g. the halo ring at the map
    // borders; every present tile implies the same block origin)
    let o = null;
    for (let y = 0; y < tiles.length && !o; y++) {
      for (let x = 0; x < tiles[y].length; x++) {
        if (tiles[y][x]) { o = { t: tiles[y][x], x, y }; break; }
      }
    }
    if (!o) throw new Error('[PEHeightField] the field has no present tiles');
    this.originGridX = o.t.gridX - o.x;
    this.originGridY = o.t.gridY - o.y;
    this.samplesX = this.tilesX * PE_TERRAIN_TILE_SIZE;
    this.samplesY = this.tilesY * PE_TERRAIN_TILE_SIZE;
    this.tilePresent = new Uint8Array(this.tilesX * this.tilesY);
    for (let y = 0; y < this.tilesY; y++) {
      for (let x = 0; x < this.tilesX; x++) {
        const t = tiles[y][x];
        if (t) {
          if (t.gridX !== this.originGridX + x || t.gridY !== this.originGridY + y) {
            throw new Error(`[PEHeightField] tile grid mismatch at ${x},${y}`);
          }
          this.tilePresent[y * this.tilesX + x] = 1;
        }
      }
    }
    this.tiles = tiles;
    this.version = HEIGHT_QUERY_VERSION;
  }

  /** Raw u16 at field-local sample (vx, vy) — null when the owning tile is
   *  missing (never a fill). */
  rawSample(vx, vy) {
    if (vx < 0 || vy < 0 || vx >= this.samplesX || vy >= this.samplesY) return null;
    const tx = Math.floor(vx / PE_TERRAIN_TILE_SIZE), ty = Math.floor(vy / PE_TERRAIN_TILE_SIZE);
    if (!this.tilePresent[ty * this.tilesX + tx]) return null;
    const lx = vx % PE_TERRAIN_TILE_SIZE, ly = vy % PE_TERRAIN_TILE_SIZE;
    return this.tiles[ty][tx].heights[ly * PE_TERRAIN_TILE_SIZE + lx];
  }

  /** World meters of field-local sample coordinates. */
  worldX(vx) { return (this.originGridX * this.tileWorldMeters) + vx * PE_TERRAIN_METER_PER_SAMPLE; }
  worldZ(vy) { return (this.originGridY * this.tileWorldMeters) + vy * PE_TERRAIN_METER_PER_SAMPLE; }
  localSampleX(worldX_) { return (worldX_ - this.originGridX * this.tileWorldMeters) / PE_TERRAIN_METER_PER_SAMPLE; }
  localSampleZ(worldZ_) { return (worldZ_ - this.originGridY * this.tileWorldMeters) / PE_TERRAIN_METER_PER_SAMPLE; }

  /** The SHARED height query: the EXACT rendered-triangle plane height at a
   *  world point, in adapter meters (calibration applied EXACTLY ONCE).
   *  Returns null when the point is outside the field or its quad touches a
   *  missing tile (honest "no surface data"). */
  triangleHeightAtWorld(wx, wz) {
    const lx = this.localSampleX(wx), lz = this.localSampleZ(wz);
    return this.triangleHeightAtSample(lx, lz);
  }

  /** The same query on field-local SAMPLE coordinates (floats). */
  triangleHeightAtSample(lx, lz) {
    if (!Number.isFinite(lx) || !Number.isFinite(lz)) return null;
    if (lx < 0 || lz < 0 || lx > this.samplesX - 1 || lz > this.samplesY - 1) return null;
    // exact last-line vertex hits (closed domain [0, samples-1])
    if (lx === this.samplesX - 1 && lz === this.samplesY - 1) {
      const raw = this.rawSample(this.samplesX - 1, this.samplesY - 1);
      return raw === null ? null : worldHeightMeters(raw);
    }
    let x0, z0, fx, fz;
    if (lx === this.samplesX - 1) { x0 = this.samplesX - 2; fx = 1; }
    else { x0 = Math.floor(lx); fx = lx - x0; }
    if (lz === this.samplesY - 1) { z0 = this.samplesY - 2; fz = 1; }
    else { z0 = Math.floor(lz); fz = lz - z0; }
    const h00 = this.rawSample(x0, z0), h10 = this.rawSample(x0 + 1, z0);
    const h01 = this.rawSample(x0, z0 + 1), h11 = this.rawSample(x0 + 1, z0 + 1);
    if (h00 === null || h10 === null || h01 === null || h11 === null) return null; // quad touches a MISSING tile
    // the EXACT quad split of PETerrainRegion.buildGeometry: (a,c,b),(b,c,d)
    // → the anti-diagonal fx+fz=1; triangle 1 covers fx+fz<=1.
    const raw = (fx + fz <= 1)
      ? h00 + (h10 - h00) * fx + (h01 - h00) * fz
      : h01 * (1 - fx) + h10 * (1 - fz) + h11 * (fx + fz - 1);
    return worldHeightMeters(raw); // applied EXACTLY ONCE (the SAME conversion as the near mesh)
  }

  /** Census of the field: present/missing tiles (the honest coverage input). */
  census() {
    let present = 0;
    for (let i = 0; i < this.tilePresent.length; i++) if (this.tilePresent[i]) present++;
    return {
      version: this.version,
      origin: { gx: this.originGridX, gy: this.originGridY },
      tilesX: this.tilesX, tilesY: this.tilesY,
      tilesPresent: present,
      tilesMissing: this.tilePresent.length - present,
      sampleSpan: { x: [0, this.samplesX - 1], z: [0, this.samplesY - 1] },
      worldSpan: {
        x: [this.worldX(0), this.worldX(this.samplesX - 1)],
        z: [this.worldZ(0), this.worldZ(this.samplesY - 1)],
      },
    };
  }
}
