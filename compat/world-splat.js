// world-splat.js — PE_WORLD_LAUNCHER_R1_20261010, ETAP D (contract §5)
// PURE client-side module (no DOM, no THREE import — importable by the
// browser app AND by the Node gates): builds the region splat data for the
// terrain-texture shader from the per-tile material payloads served by
// /api/world/tile/<gx>/<gy>/materials.
//
// THE CHAIN (per used layer, contract §5):
//   TDF entry+record -> material identifier (id@+16) + name -> the engine-RE
//   CONFIRMED relation id@+16 -> '<id>.dat' in the pinned PCG Textures.bnt ->
//   the payload (fetched bounded, one entry) -> decodeTga2 (the PRODUCTION
//   decoder, strict TGA2 24bpp subset) -> RGBA -> GPU sampler (DataArrayTexture
//   + splat shader) -> visible material.
//
// RAW WEIGHTS: the per-layer 16x16 masks are carried bit-exact from the
// served base64; NOTHING normalizes them (layer sums > 255 are ORIGINAL
// DATA — the 9.3.5 engine census and the 2003 census both measured them).
// The shader blends sequentially by RAW mask/255 in RECORD ORDER.
//
// BLEND FORM provenance (era-matched, engine RE — NOT this run's invention):
//   the 9.3.5 TDF masks drive the LOD vertex-color bake
//   `vertexColor = lerp(vertexColor, materialTexture(u,v), mask/255)`
//   (FUN_00940de0; M1_TSFS_BINARY_FORENSICS iter015/iter030 consolidated
//   spec; EU935_WORLD_DATA_CENSUS GROUND_TEXTURES §2, 838/838 consumer
//   census). THIS preview applies the SAME sequential-lerp form to the
//   terrain ALBEDO — the ROLE, the UV repeat and the cell sampling are
//   labeled RENDER_RECONSTRUCTION choices (no PE evidence pins them);
//   the raw weights are unchanged.
//
// DIAGNOSTIC MODE (contract §5): a layer whose material id has NO resolved
// '<id>.dat' entry (server marked texture.resolved=false, or the client
// fetch/decode FAILED) is SKIPPED — counted, listed, never blended with a
// random/fallback texture. A texture that fetches but fails the strict
// decodeTga2 subset is likewise UNRESOLVED (decode failure is LOUD).
'use strict';

export const WORLD_SPLAT_SCHEMA_VERSION = 'world-splat-v1';

/** The RENDER_RECONSTRUCTION preset descriptor (surfaced to the UI/evidence
 * panel verbatim — the honest label of every choice that has NO PE
 * evidence; the raw weights and the blend FORM are NOT part of the
 * reconstruction label: the form is era-evidenced, the weights are original
 * data). */
export const RENDER_RECONSTRUCTION_PRESET = Object.freeze({
  label: 'RENDER_RECONSTRUCTION',
  schemaVersion: WORLD_SPLAT_SCHEMA_VERSION,
  blendForm: 'sequential lerp per layer by RAW mask/255 in RECORD ORDER (base first) — era-evidenced FORM (9.3.5 LOD vertex-color bake lerp(vertexColor, materialTexture(u,v), mask/255), iter030); applied here to albedo',
  albedoRole: 'RECONSTRUCTION: the 9.3.5 ground albedo was the climate palette pipeline (base+factor+detail; its per-location inputs 432502/459344 are MISSING locally) — the engine used the material textures for the vertex tint bake, NOT the base albedo',
  uv: 'world-space GLOBAL uv = worldPos.xz / 32 m (u along +X, v along +Z/south; no per-tile or per-window reset); the repeat value is a RECONSTRUCTION choice (the era-evidenced detail-texture density is 32/32/16 world units — iter024 — applied to material textures BY ANALOGY, not as a pinned material repeat)',
  rowOrder: 'decodeTga2 IMAGE order (row 0 = visual TOP; the TGA bottom-up storage is flipped ONCE by the decoder) + THREE.DataTexture flipY=false — v=0 samples the image TOP; the A32 climate-palette FILE-row convention (decodeTga2A32) is a DIFFERENT decoder/convention and is not used here',
  cellSampling: 'nearest 16x16 material cell per tile (2x2 samples = 4x4 m per cell; mask row = grid-y, col = grid-x, the same axes as the height grid); flat within a cell (the 9.3.5 "edge-extended at load" mask semantics are NOT pinned — nearest is the documented choice)',
  colorSpace: 'SRGB_PASSTHROUGH — the original TGA bytes are display-referred; the GPU blend happens on the raw values (no sRGB decode), matching the historical fixed-function D3D8 framebuffer-space blending; the shader outputs sRGB directly (no output colorspace chunk)',
  caps: 'MAX_LAYERS_PER_CELL=16 / MAX_TEXTURE_SLOTS=48 — cells/tiles exceeding a cap keep the FIRST layers in record order and the dropped count is REPORTED (a render approximation, labeled; the served raw weights are unchanged)',
  unresolved: 'a material id without a resolved <id>.dat entry (or a failed strict decode) is SKIPPED with an explicit diagnostic — never a fallback texture, never cross-era substitution',
});

export const MAX_LAYERS_PER_CELL = 16;
export const MAX_TEXTURE_SLOTS = 48;
export const MATERIAL_CELLS_PER_TILE = 16;          // 16x16 mask per 32x32-sample tile
export const REGION_TILES = 8;                     // the 8x8 window
export const REGION_CELLS = REGION_TILES * MATERIAL_CELLS_PER_TILE; // 128
export const EMPTY_SLOT_INDEX = 255;

function maskEquals(a, b) {
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
  return true;
}

/**
 * buildRegionSplatData — the pure region splat builder.
 * @param {Array<Array<object>>} materialsGrid 2D array [row=gy][col=gx] (8x8)
 *   of per-tile materials payloads ({materials: [{position,id,name,maskBase64,
 *   texture:{resolved,...}}], ...} — the server JSON). Row-major like the
 *   region tile grid.
 * @param {object} [opts] {atobFn} (Node tests pass a base64 decoder; the
 *   browser uses the global atob by default).
 * @returns {{ok, wireVersion, idxTextures: Uint8Array[4], wTextures: Uint8Array[4],
 *   textureIds: number[], slotById: Map, unresolved: object[], duplicates: number,
 *   cappedCells: number, cellsWithNoActiveLayers: number, activeLayersHist: object,
 *   layersTotal: number, appliedLayers: number, resolvedLayers: number,
 *   textureSlotOverflow: number, diagnostic: object}}
 *   idxTextures/wTextures: 4 RGBA u8 textures each, 128x128 (REGION_CELLS^2),
 *   cell (cx,cy) at row cy*128... layout: row = cy (grid-y), col = cx —
 *   texelFetch-compatible with the shader's cell math. Empty slots carry
 *   idx=255 (EMPTY_SLOT_INDEX), w=0.
 */
export function buildRegionSplatData(materialsGrid, opts = {}) {
  const atobFn = opts.atobFn ?? ((s) => atob(s));
  const dec = (b64) => {
    const bin = atobFn(b64);
    const out = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  };
  if (!Array.isArray(materialsGrid) || materialsGrid.length !== REGION_TILES ||
      materialsGrid.some((r) => !Array.isArray(r) || r.length !== REGION_TILES)) {
    throw new Error('[world-splat] materialsGrid must be the 8x8 window grid');
  }
  const N = REGION_CELLS;
  const idxTextures = [0, 1, 2, 3].map(() => new Uint8Array(N * N * 4).fill(0));
  const wTextures = [0, 1, 2, 3].map(() => new Uint8Array(N * N * 4).fill(0));
  for (const t of idxTextures) t.fill(EMPTY_SLOT_INDEX);
  const slotById = new Map();
  const textureIds = [];
  const unresolved = [];
  const unresolvedKey = new Set();
  let duplicates = 0, cappedCells = 0, cellsWithNoActiveLayers = 0, layersTotal = 0, appliedLayers = 0, resolvedLayers = 0;
  const activeLayersHist = new Map();
  let textureSlotOverflow = 0;

  for (let ty = 0; ty < REGION_TILES; ty++) {
    for (let tx = 0; tx < REGION_TILES; tx++) {
      const tilePayload = materialsGrid[ty][tx];
      const records = [...(tilePayload?.materials ?? [])].sort((a, b) => a.position - b.position);
      // decode masks once per tile (record order = base first)
      const layers = [];
      let prevByIdMask = new Map();
      for (const r of records) {
        layersTotal++;
        let mask;
        try {
          mask = dec(r.maskBase64);
        } catch (e) {
          unresolved.push({ tile: `${tx}/${ty}`, id: r.id, name: r.name, reason: `MASK_BASE64_DECODE_FAILED: ${e?.message ?? e}` });
          continue;
        }
        if (mask.length !== MATERIAL_CELLS_PER_TILE * MATERIAL_CELLS_PER_TILE) {
          unresolved.push({ tile: `${tx}/${ty}`, id: r.id, name: r.name, reason: `MASK_LENGTH ${mask.length} != 256 (malformed — layer skipped, loud)` });
          continue;
        }
        // EXACT-duplicate dedupe (measured rule): same id + identical mask
        // bytes = one layer (the 2003 Sand10x4 pattern); different mask =
        // an independent layer (kept).
        const prev = prevByIdMask.get(r.id);
        if (prev && maskEquals(prev, mask)) { duplicates++; continue; }
        prevByIdMask.set(r.id, mask);
        // the id@+16 -> '<id>.dat' relation: unresolved bindings are SKIPPED
        // (explicit diagnostic — never a fallback texture)
        const resolved = r.texture?.resolved === true;
        if (!resolved) {
          const key = `${r.id}`;
          if (!unresolvedKey.has(key)) {
            unresolvedKey.add(key);
            unresolved.push({ tile: `${tx}/${ty}`, id: r.id, name: r.name, reason: r.texture?.reason ?? 'UNRESOLVED material->texture binding (no <id>.dat entry / failed fetch)' });
          }
          continue;
        }
        resolvedLayers++;
        if (!slotById.has(r.id)) {
          if (textureIds.length >= MAX_TEXTURE_SLOTS) {
            textureSlotOverflow++;
            const key = `${r.id}`;
            if (!unresolvedKey.has(key)) {
              unresolvedKey.add(key);
              unresolved.push({ tile: `${tx}/${ty}`, id: r.id, name: r.name, reason: `TEXTURE_SLOTS_EXCEEDED (cap ${MAX_TEXTURE_SLOTS} — layer skipped, counted, never silent)` });
            }
            continue;
          }
          slotById.set(r.id, textureIds.length);
          textureIds.push(r.id);
        }
        layers.push({ slot: slotById.get(r.id), mask });
      }
      // write the per-cell slots
      for (let cy = 0; cy < MATERIAL_CELLS_PER_TILE; cy++) {
        for (let cx = 0; cx < MATERIAL_CELLS_PER_TILE; cx++) {
          const cellCol = tx * MATERIAL_CELLS_PER_TILE + cx;
          const cellRow = ty * MATERIAL_CELLS_PER_TILE + cy;
          const texel = (cellRow * N + cellCol) * 4;
          let active = 0;
          for (const layer of layers) {
            const w = layer.mask[cy * MATERIAL_CELLS_PER_TILE + cx];
            if (w > 0) active++;
          }
          activeLayersHist.set(active, (activeLayersHist.get(active) ?? 0) + 1);
          if (active === 0) { cellsWithNoActiveLayers++; continue; }
          let slot = 0;
          for (const layer of layers) {
            if (slot >= MAX_LAYERS_PER_CELL) { cappedCells++; break; } // keep the FIRST layers in record order
            const w = layer.mask[cy * MATERIAL_CELLS_PER_TILE + cx];
            if (w === 0) continue;
            idxTextures[slot >> 2][texel + (slot & 3)] = layer.slot;
            wTextures[slot >> 2][texel + (slot & 3)] = w; // RAW weight — bit-exact, never normalized
            slot++;
            appliedLayers++;
          }
        }
      }
    }
  }
  return {
    ok: unresolved.length === 0,
    wireVersion: WORLD_SPLAT_SCHEMA_VERSION,
    preset: RENDER_RECONSTRUCTION_PRESET,
    idxTextures, wTextures,
    textureIds, slotById,
    unresolved, duplicates, cappedCells, cellsWithNoActiveLayers,
    activeLayersHist: Object.fromEntries([...activeLayersHist.entries()].sort((a, b) => a[0] - b[0])),
    layersTotal, resolvedLayers, appliedLayers, textureSlotOverflow,
    cells: N * N,
    diagnostic: {
      mode: unresolved.length > 0 ? 'DIAGNOSTIC: unresolved material->texture bindings present' : 'NONE',
      unresolvedCount: unresolved.length,
      unresolvedSample: unresolved.slice(0, 12),
      duplicates, cappedCells, cellsWithNoActiveLayers, textureSlotOverflow,
      note: 'unresolved layers are SKIPPED (no fallback texture); capped cells keep the FIRST layers in record order (labeled render approximation; served raw weights unchanged)',
    },
  };
}

/**
 * sampleTexelImageOrder — the DOCUMENTED GPU sampling convention of this
 * preview (single source of truth for the UV/flip control gates):
 * a THREE.DataTexture built from decodeTga2's IMAGE-ORDER rgba with
 * flipY=false samples uv (0,0) at the image TOP-LEFT; u grows along image
 * columns (X), v grows along image ROWS going DOWN (row 0 = top).
 * @returns [r,g,b] of the texel at normalized (u,v).
 */
export function sampleTexelImageOrder(rgba, width, height, u, v) {
  const x = Math.min(width - 1, Math.max(0, Math.floor(u * width)));
  const y = Math.min(height - 1, Math.max(0, Math.floor(v * height)));
  const i = (y * width + x) * 4;
  return [rgba[i], rgba[i + 1], rgba[i + 2]];
}

/** The world-uv convention of the preview (single source of truth; the shader
 * mirrors this math): GLOBAL world-space uv, u = worldX / repeatM, v =
 * worldZ / repeatM (v along +Z = south, the adapter grid-y axis); the
 * RepeatWrapping wrap makes the pattern global across tiles/windows. */
export function worldUV(worldX, worldZ, repeatM) {
  return [worldX / repeatM, worldZ / repeatM];
}
