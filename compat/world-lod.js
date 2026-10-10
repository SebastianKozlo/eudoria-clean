// world-lod.js — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §4)
// THE distant-LOD client: the whole available map as a CONTINUOUS WORLD.
//
//   MID  — a 40x40-tile ring of 8x8-decimated REAL samples per tile around
//          the near window (hole cut EXACTLY at the near mesh's own last real
//          samples — the boundary grid lines MATCH the near mesh edge, so
//          there is NO crack and NO skirt between near and mid BY
//          CONSTRUCTION: both levels share the same ORIGINAL samples on the
//          cut lines).
//   FAR  — the whole 220x236 regular grid at 4x4-decimated REAL samples per
//          tile (one ~1.6 MB binary fetch; the SAME census pass collects the
//          decimated samples server-side). The far mesh vertex buffer is
//          STATIC; the mid-window-shaped HOLE is cut through the INDEX only
//          (rebuilt when the mid window moves — the hole boundary grid lines
//          again MATCH the mid ring edge: no crack, no skirt).
//
//   HONEST HOLES: a tile whose per-tile status is not MEASURED (missing entry
//   / decode failure / outside the regular grid) contributes NO surface —
//   its quads are skipped (explicit holes; "missing" is NAMED in the
//   coverage census, never masked by a zero surface). The decimation is of
//   ORIGINAL SAMPLES (never averaging; the sample keeps its own world
//   position). This is a RENDERER LOD policy with explicit coverage — NOT a
//   new source format, NOT a stock-PE paging recovery.
//
//   CALIBRATION: worldHeightMeters is applied EXACTLY ONCE on both levels
//   (the same conversion as the near mesh — never twice, never smoothed).
'use strict';

import * as THREE from 'three';
import { worldHeightMeters, PE_TERRAIN_METER_PER_SAMPLE } from '../src/peworld/PETerrainCore.js';
import { LOD_DECIMATION } from '../src/peworld/PEHeightQuery.js';

export const WORLD_LOD_VERSION = 'world-lod-r2-v1';
export const TILE_M = 64;                 // adapter tile meters (CURRENT_RUNTIME_CALIBRATION)
export const MID_WINDOW_T = 40;           // the mid ring window (tiles)
export const MID_BLOCK_T = 8;             // one served block = 8x8 tiles
const MID_IDX = LOD_DECIMATION.mid.indices;
const FAR_IDX = LOD_DECIMATION.far.indices;

function tileLinePos(tileIdx, k, idx) {
  return tileIdx * TILE_M + idx[k] * PE_TERRAIN_METER_PER_SAMPLE; // the sample's OWN position
}

/**
 * WorldLod — the distant terrain layers (mid + far).
 * deps: { scene, fetchBinary(url)->{payload,headers}, fetchJson(url) }
 */
export class WorldLod {
  constructor({ scene, fetchBinary, fetchJson }) {
    if (!scene || typeof fetchBinary !== 'function' || typeof fetchJson !== 'function') {
      throw new Error('[WorldLod] scene, fetchBinary and fetchJson are required');
    }
    this.scene = scene;
    this.fetchBinary = fetchBinary;
    this.fetchJson = fetchJson;
    this.gridW = 220; this.gridH = 236; // refreshed from /api/world/status (measured, not trusted blindly)
    this.midGroup = new THREE.Group();
    this.midGroup.name = 'lod-mid-ring';
    this.farGroup = new THREE.Group();
    this.farGroup.name = 'lod-far-world';
    this.midGroup.visible = true;
    this.farGroup.visible = true;
    scene.add(this.farGroup);
    scene.add(this.midGroup);
    // far state
    this.far = { status: 'PENDING', mesh: null, xPos: null, zPos: null, gridW: null, gridH: null, tileStatus: null, samples: null, holeOrigin: null, tris: 0, verts: 0 };
    // mid state
    this.mid = { status: 'IDLE', mesh: null, origin: null, blocksCache: new Map(), blocksOrder: [], blocksMax: 96, tris: 0, verts: 0, fetches: 0 };
    this.materialMid = new THREE.MeshLambertMaterial({ color: 0x7d8a96, side: THREE.DoubleSide }); // neutral distant LOD surface (RECONSTRUCTION preview aid)
    this.materialFar = new THREE.MeshLambertMaterial({ color: 0x5f6c78, side: THREE.DoubleSide });
    this.coverage = {
      farTilesRepresented: 0, farTilesMissing: 0,
      midTilesRepresented: 0, midTilesMissing: 0,
      midOrigin: null, farReady: false,
    };
  }

  setGrid(gridW, gridH) {
    this.gridW = gridW; this.gridH = gridH;
  }

  // ---------------- FAR ----------------

  /** Fetch + build the whole-world far mesh (idempotent; safe to retry). The
   *  expected NOT-READY 503 (the census is still measuring) keeps the status
   *  PENDING for the caller's poll loop — never a permanent failure. */
  async ensureFar() {
    if (this.far.status === 'READY') return true;
    if (this.far.status === 'LOADING') return false;
    this.far.status = 'LOADING';
    try {
      const { payload } = await this.fetchBinary('/api/world/far');
      const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
      const gridW = dv.getUint16(0, true), gridH = dv.getUint16(2, true), perTileEdge = dv.getUint16(4, true);
      if (perTileEdge !== FAR_IDX.length) throw new Error(`far per-tile edge ${perTileEdge} != client decimation ${FAR_IDX.length}`);
      const N = gridW * gridH;
      if (payload.byteLength !== 8 + N + N * perTileEdge * perTileEdge * 2) {
        throw new Error(`far payload ${payload.byteLength} B malformed (expected ${8 + N + N * perTileEdge * perTileEdge * 2})`);
      }
      const tileStatus = new Uint8Array(payload.buffer, payload.byteOffset + 8, N);
      const samples = new Uint16Array(payload.buffer, payload.byteOffset + 8 + N, N * perTileEdge * perTileEdge);
      // the STATIC vertex grid (uneven but REAL sample positions)
      const linesX = gridW * perTileEdge, linesZ = gridH * perTileEdge;
      const xPos = new Float32Array(linesX), zPos = new Float32Array(linesZ);
      for (let i = 0; i < linesX; i++) xPos[i] = tileLinePos(i >> 2, i & 3, FAR_IDX);
      for (let i = 0; i < linesZ; i++) zPos[i] = tileLinePos(i >> 2, i & 3, FAR_IDX);
      const positions = new Float32Array(linesX * linesZ * 3);
      let missing = 0, present = 0;
      for (let z = 0; z < linesZ; z++) {
        for (let x = 0; x < linesX; x++) {
          const tileX = x >> 2, tileZ = z >> 2;
          const ok = tileStatus[tileZ * gridW + tileX] === 1;
          const i = (z * linesX + x) * 3;
          positions[i] = xPos[x];
          positions[i + 1] = ok ? worldHeightMeters(samples[(tileZ * gridW + tileX) * 16 + (z & 3) * 4 + (x & 3)]) : 0; // placeholder — masked by the INDEX (never surface)
          positions[i + 2] = zPos[z];
        }
      }
      for (let t = 0; t < N; t++) { if (tileStatus[t] === 1) present++; else missing++; }
      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
      // the index is REBUILT per mid window (hole cut) — ONE preallocated max
      // buffer + setDrawRange (NO per-move allocation churn; the positions are
      // STATIC so the normals are computed ONCE here — never re-computed per
      // move; the hole only changes WHICH quads are drawn)
      const maxQuads = (linesX - 1) * (linesZ - 1);
      this.far.indexBuffer = new Uint32Array(maxQuads * 6);
      geometry.setIndex(new THREE.BufferAttribute(this.far.indexBuffer, 1));
      geometry.setDrawRange(0, 0);
      geometry.computeVertexNormals();
      const mesh = new THREE.Mesh(geometry, this.materialFar);
      mesh.frustumCulled = false; // one static world mesh (culling is per-quad in the shader budget sense — documented)
      this.farGroup.add(mesh);
      this.far.mesh = mesh;
      this.far.xPos = xPos; this.far.zPos = zPos;
      this.far.gridW = gridW; this.far.gridH = gridH;
      this.far.tileStatus = tileStatus; this.far.samples = samples;
      this.far.linesX = linesX; this.far.linesZ = linesZ;
      this.coverage.farTilesRepresented = present;
      this.coverage.farTilesMissing = missing;
      this.coverage.farReady = true;
      this.far.status = 'READY';
      return true;
    } catch (e) {
      const msg = String(e?.message ?? e);
      if (/FAR_LOD_NOT_READY|HTTP 503/.test(msg)) {
        // the census is still measuring — the EXPECTED transient: stay PENDING
        this.far.status = 'PENDING';
        this.far.error = null;
        return false;
      }
      this.far.status = 'FAILED';
      this.far.error = msg;
      return false;
    }
  }

  farProgressNote() {
    return this.far.status === 'READY' ? 'READY' : `${this.far.status}${this.far.error ? `: ${this.far.error.slice(0, 140)}` : ''}`;
  }

  /** Rebuild the far INDEX with the mid-window hole (called when the mid
   *  window moves). The hole = EXACTLY the mid mesh coverage: the far quads
   *  fully inside the mid line range are skipped; the boundary quads remain
   *  (their far lines MATCH the mid ring's edge lines — same ORIGINAL
   *  samples on the cut lines: no crack, no overlap). Writes into the ONE
   *  preallocated index buffer + setDrawRange (bounded: no per-move
   *  allocation; the vertex positions/normals are STATIC — never touched). */
  rebuildFarIndex(midOrigin) {
    const f = this.far;
    if (f.status !== 'READY' || !f.mesh) return false;
    const lineHole0 = midOrigin.gx * 4;
    const lineHole1 = (midOrigin.gx + MID_WINDOW_T) * 4 - 1; // inclusive
    const lineHoleZ0 = midOrigin.gy * 4;
    const lineHoleZ1 = (midOrigin.gy + MID_WINDOW_T) * 4 - 1;
    const { linesX, linesZ, tileStatus, gridW } = f;
    const buf = f.indexBuffer;
    let n = 0, tris = 0;
    for (let qz = 0; qz < linesZ - 1; qz++) {
      for (let qx = 0; qx < linesX - 1; qx++) {
        // hole skip: quads FULLY inside the mid mesh coverage
        if (qx >= lineHole0 && qx + 1 <= lineHole1 && qz >= lineHoleZ0 && qz + 1 <= lineHoleZ1) continue;
        // honest holes: any corner vertex on a non-MEASURED tile → skip
        const tx0 = qx >> 2, tx1 = (qx + 1) >> 2, tz0 = qz >> 2, tz1 = (qz + 1) >> 2;
        if (tileStatus[tz0 * gridW + tx0] !== 1 || tileStatus[tz0 * gridW + tx1] !== 1 ||
            tileStatus[tz1 * gridW + tx0] !== 1 || tileStatus[tz1 * gridW + tx1] !== 1) continue;
        const a = qz * linesX + qx, b = a + 1, c = a + linesX, d = c + 1;
        // the SAME quad split as the near layer (PETerrainRegion.buildGeometry)
        buf[n++] = a; buf[n++] = c; buf[n++] = b;
        buf[n++] = b; buf[n++] = c; buf[n++] = d;
        tris += 2;
      }
    }
    f.mesh.geometry.setDrawRange(0, n);
    f.mesh.geometry.index.needsUpdate = true;
    f.tris = tris;
    f.holeOrigin = { ...midOrigin };
    return true;
  }

  // ---------------- MID ----------------

  async _block(bx, by) {
    const key = `${bx},${by}`;
    if (this.mid.blocksCache.has(key)) return this.mid.blocksCache.get(key);
    this.mid.fetches++;
    const { payload } = await this.fetchBinary(`/api/world/lod8/${bx}/${by}`);
    if (payload.byteLength !== 64 + 64 * 64 * 2) throw new Error(`lod8 block ${key}: ${payload.byteLength} B malformed`);
    const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
    const status = new Uint8Array(64);
    for (let i = 0; i < 64; i++) status[i] = dv.getUint8(i);
    const samples = new Uint16Array(64 * 64);
    for (let i = 0; i < 64 * 64; i++) samples[i] = dv.getUint16(64 + i * 2, true);
    const rec = { status, samples };
    this.mid.blocksCache.set(key, rec);
    this.mid.blocksOrder.push(key);
    while (this.mid.blocksOrder.length > this.mid.blocksMax) {
      const old = this.mid.blocksOrder.shift();
      this.mid.blocksCache.delete(old);
    }
    return rec;
  }

  /** Rebuild the mid ring for the CURRENT near window origin (mid origin =
   *  the near window origin shifted -16 tiles, clamped to the grid). Fetches
   *  only missing blocks (bounded LRU); the hole is cut EXACTLY at the near
   *  mesh coverage (see the header). Returns the honest rebuild record. */
  async rebuildMid(nearOrigin) {
    const midOrigin = {
      gx: Math.min(Math.max(nearOrigin.gx - (MID_WINDOW_T - 8) / 2, 0), this.gridW - MID_WINDOW_T),
      gy: Math.min(Math.max(nearOrigin.gy - (MID_WINDOW_T - 8) / 2, 0), this.gridH - MID_WINDOW_T),
    };
    // fetch the covering blocks (5x5 blocks for a 40-tile window)
    const bx0 = Math.floor(midOrigin.gx / MID_BLOCK_T), by0 = Math.floor(midOrigin.gy / MID_BLOCK_T);
    const bx1 = Math.floor((midOrigin.gx + MID_WINDOW_T - 1) / MID_BLOCK_T);
    const by1 = Math.floor((midOrigin.gy + MID_WINDOW_T - 1) / MID_BLOCK_T);
    const blocks = new Map(); // "bx,by" (LOCAL block coords) -> record
    for (let by = by0; by <= by1; by++) {
      for (let bx = bx0; bx <= bx1; bx++) {
        blocks.set(`${bx},${by}`, await this._block(bx, by));
      }
    }
    // the mid sample field: 40x8 lines per axis (REAL decimated samples at their OWN positions)
    const lines = MID_WINDOW_T * MID_IDX.length; // 320
    // ONE preallocated position/index buffer (bounded: no per-move allocation
    // churn across window moves — the SAME buffers are rewritten + drawRange)
    if (!this.mid.positionBuffer) {
      this.mid.positionBuffer = new Float32Array(lines * lines * 3);
      this.mid.indexBuffer = new Uint32Array((lines - 1) * (lines - 1) * 6);
    }
    const positions = this.mid.positionBuffer;
    const holeLine0 = (nearOrigin.gx - midOrigin.gx) * MID_IDX.length;      // first near line (inclusive)
    const holeLine1 = holeLine0 + 8 * MID_IDX.length - 1;                     // last near line (inclusive)
    const holeLineZ0 = (nearOrigin.gy - midOrigin.gy) * MID_IDX.length;
    const holeLineZ1 = holeLineZ0 + 8 * MID_IDX.length - 1;
    const tileStatusAt = (lx, lz) => {
      const wgx = midOrigin.gx + (lx >> 3), wgy = midOrigin.gy + (lz >> 3);
      if (wgx >= this.gridW || wgy >= this.gridH) return 4;
      const rec = blocks.get(`${Math.floor(wgx / MID_BLOCK_T)},${Math.floor(wgy / MID_BLOCK_T)}`);
      if (!rec) return 4;
      return rec.status[(wgy % MID_BLOCK_T) * MID_BLOCK_T + (wgx % MID_BLOCK_T)];
    };
    const sampleAt = (lx, lz) => {
      const wgx = midOrigin.gx + (lx >> 3), wgy = midOrigin.gy + (lz >> 3);
      const rec = blocks.get(`${Math.floor(wgx / MID_BLOCK_T)},${Math.floor(wgy / MID_BLOCK_T)}`);
      const localTileX = wgx % MID_BLOCK_T, localTileZ = wgy % MID_BLOCK_T;
      const inTileLx = localTileX * 8 + (lx & 7); // block-local SAMPLE line
      const inTileLz = localTileZ * 8 + (lz & 7);
      return rec.samples[inTileLz * 64 + inTileLx];
    };
    // (the positions buffer is the PREALLOCATED this.mid.positionBuffer above)
    for (let lz = 0; lz < lines; lz++) {
      for (let lx = 0; lx < lines; lx++) {
        const tileX = midOrigin.gx + (lx >> 3), tileZ = midOrigin.gy + (lz >> 3);
        if (tileX >= this.gridW || tileZ >= this.gridH) continue; // outside the regular grid (never surface)
        const i = (lz * lines + lx) * 3;
        positions[i] = tileLinePos(tileX, lx & 7, MID_IDX);
        positions[i + 1] = tileStatusAt(lx, lz) === 0 ? worldHeightMeters(sampleAt(lx, lz)) : 0; // masked by the index below
        positions[i + 2] = tileLinePos(tileZ, lz & 7, MID_IDX);
      }
    }
    const indices = this.mid.indexBuffer;
    let n = 0, tris = 0, missing = 0, present = 0;
    for (let qz = 0; qz < lines - 1; qz++) {
      for (let qx = 0; qx < lines - 1; qx++) {
        if (qx >= holeLine0 && qx + 1 <= holeLine1 && qz >= holeLineZ0 && qz + 1 <= holeLineZ1) continue; // the near mesh covers this area
        const s00 = tileStatusAt(qx, qz), s10 = tileStatusAt(qx + 1, qz), s01 = tileStatusAt(qx, qz + 1), s11 = tileStatusAt(qx + 1, qz + 1);
        if (s00 !== 0 || s10 !== 0 || s01 !== 0 || s11 !== 0) { missing++; continue; } // honest hole (missing/failed/outside)
        present++;
        const a = qz * lines + qx, b = a + 1, c = a + lines, d = c + 1;
        indices[n++] = a; indices[n++] = c; indices[n++] = b; // the SAME quad split as the near layer
        indices[n++] = b; indices[n++] = c; indices[n++] = d;
        tris += 2;
      }
    }
    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setIndex(new THREE.BufferAttribute(indices, 1));
    geometry.setDrawRange(0, n);
    geometry.computeVertexNormals();
    if (this.mid.mesh) {
      this.mid.mesh.geometry.dispose();
      this.mid.mesh.geometry = geometry;
    } else {
      this.mid.mesh = new THREE.Mesh(geometry, this.materialMid);
      this.mid.mesh.frustumCulled = false;
      this.midGroup.add(this.mid.mesh);
    }
    this.mid.origin = midOrigin;
    this.mid.tris = tris;
    this.mid.verts = lines * lines;
    this.mid.status = 'READY';
    this.coverage.midTilesRepresented = present;
    this.coverage.midTilesMissing = missing;
    this.coverage.midOrigin = midOrigin;
    // the far hole follows the mid window (INDEX-only rebuild; static verts)
    this.rebuildFarIndex(midOrigin);
    return { midOrigin, tris, blocks: blocks.size, missing };
  }

  /** The continuous-world coverage census (contract §4: explicitly separate
   *  indexed / valid / coarse-represented / near-resident / pending /
   *  missing). */
  census({ nearOrigin, nearTilesPresent, nearTilesMissing }) {
    return {
      version: WORLD_LOD_VERSION,
      grid: { width: this.gridW, height: this.gridH, tiles: this.gridW * this.gridH },
      near: {
        windowTiles: 8, origin: nearOrigin,
        tilesPresent: nearTilesPresent ?? null, tilesMissing: nearTilesMissing ?? null,
      },
      mid: {
        windowTiles: MID_WINDOW_T, origin: this.mid.origin,
        tris: this.mid.tris, verts: this.mid.verts, status: this.mid.status,
        blocksCached: this.mid.blocksCache.size, blockFetches: this.mid.fetches,
        quadsRepresented: this.coverage.midTilesRepresented, quadsMissing: this.coverage.midTilesMissing,
      },
      far: {
        status: this.far.status, tris: this.far.tris,
        tilesRepresented: this.coverage.farTilesRepresented, tilesMissing: this.coverage.farTilesMissing,
        holeOrigin: this.far.holeOrigin,
      },
      seamsPolicy: 'boundary grid lines MATCH the coarser/finer level edge (the SAME original samples on the cut lines) — no cracks BY CONSTRUCTION; no skirts are used (none needed); missing tiles are explicit holes, never zero surface',
    };
  }

  dispose() {
    if (this.mid.mesh) { this.mid.mesh.geometry.dispose(); this.midGroup.remove(this.mid.mesh); this.mid.mesh = null; }
    if (this.far.mesh) { this.far.mesh.geometry.dispose(); this.farGroup.remove(this.far.mesh); this.far.mesh = null; }
    this.materialMid.dispose();
    this.materialFar.dispose();
    this.scene.remove(this.midGroup);
    this.scene.remove(this.farGroup);
  }
}
