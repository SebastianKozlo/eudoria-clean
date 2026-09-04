// TerrainTile.js — PE MILESTONE 1 ITER 001 (PE_WORLD_SURFACE_FIDELITY_R1)
// Canonical terrain tile with provenance (charter §7). Units: heights are the
// RAW uint16 values from the original TDF bytes. NO unit conversion, NO
// normalization, NO 8-bit intermediate happens here — the consumer decides.
// heightScale (u16 -> meters) is carried as CALIBRATION metadata, labeled per
// the control plane (C-RUNTIME-002: CURRENT_RUNTIME_CALIBRATION, not a
// historical engine fact).

export const HEIGHT_SCALE_CALIBRATION = {
  u16PerMeter: 128, // CURRENT_RUNTIME_CALIBRATION (deployed runtime heightScale = 1/128)
  label: 'CURRENT_RUNTIME_CALIBRATION',
  evidenceStatus: 'STRONGLY_SUPPORTED',
};

export class TerrainTile {
  constructor({ gridX, gridY, name, heights, provenance, header, subheader, tail }) {
    if (!(heights instanceof Uint16Array) || heights.length !== 1024) {
      throw new Error('[TerrainTile] heights must be Uint16Array(1024)');
    }
    if (!provenance || !provenance.era || !provenance.evidenceStatus) {
      throw new Error('[TerrainTile] provenance with era + evidenceStatus required');
    }
    this.gridX = gridX;
    this.gridY = gridY;
    this.name = name;
    this.heights = heights;      // raw uint16, row-major 32x32
    this.provenance = provenance;
    this.header = header ?? null;
    this.subheader = subheader ?? null;
    this.tail = tail ?? null;    // raw tail (Gate B scope), NOT interpreted
  }

  /** Raw uint16 at local (x,y), 0..31. NO interpolation. */
  heightAt(x, y) {
    return this.heights[y * 32 + x];
  }
}
