// phase3_renders.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 3 (W3, contract §3)
// PRIVATE renders for the four primary CD_2003 models: top-down projection
// (file x/z plane), top-down wireframe, and 3D isometric wireframe — all in
// FILE_SCENE_SPACE (the file's own serialized axes; NO axis swap, NO unit
// conversion). AXIS SEMANTICS (e.g. which axis is up) ARE NOT ESTABLISHED —
// the top-down projection is the file x/z plane (the footprint axes used by
// the rankings), labeled as such; it is NOT a claim about the world up-axis.
// Original origin/bounds preserved (no centering in the raster; the image
// maps the composed AABB 1:1).
//
// Own bounded PNG encoder (IHDR/IDAT/IEND + node:zlib deflate) — no new
// dependency. Output → PRIVATE_OUTPUT only.

import fs from 'node:fs';
import zlib from 'node:zlib';
import { readNif41, analyzeNif41Model, PEC_NIF41_READER_VERSION } from './nif41_deep.mjs';
import { buildAssetIR, composeWorldTransforms } from '../../src/pecompat/PecSceneIR.js';
import { applyTrsPoint } from '../../src/pecompat/PecTransform.js';

function pngEncode(width, height, rgba) {
  const raw = Buffer.alloc((width * 4 + 1) * height);
  for (let y = 0; y < height; y++) {
    raw[y * (width * 4 + 1)] = 0; // filter: None
    rgba.copy(raw, y * (width * 4 + 1) + 1, y * width * 4, (y + 1) * width * 4);
  }
  const idat = zlib.deflateSync(raw, { level: 6 });
  const chunk = (type, data) => {
    const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
    const body = Buffer.concat([Buffer.from(type, 'ascii'), data]);
    const crcBuf = Buffer.alloc(4); crcBuf.writeUInt32BE(crc32(body) >>> 0);
    return Buffer.concat([len, body, crcBuf]);
  };
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0); ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8; ihdr[9] = 6; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk('IHDR', ihdr), chunk('IDAT', idat), chunk('IEND', Buffer.alloc(0)),
  ]);
}
const CRC_TABLE = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = (c & 1) ? (0xedb88320 ^ (c >>> 1)) : (c >>> 1); t[n] = c >>> 0; }
  return t;
})();
function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

const MESH_COLORS = [
  [66, 133, 244], [219, 68, 55], [244, 180, 0], [15, 157, 88],
  [171, 71, 188], [0, 172, 193], [255, 112, 67], [142, 124, 195],
];

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) args[key] = true;
      else { args[key] = next; i++; }
    }
  }
  return args;
}

/** Rasterize a filled+wireframe view of triangles in image space with z-buffer. */
function renderTriangles(width, height, tris, wireframe) {
  const rgba = Buffer.alloc(width * height * 4, 0);
  const zbuf = new Float64Array(width * height).fill(-Infinity);
  const edge = (x0, y0, x1, y1, col) => {
    // Bresenham with thick AA-ish simple steps
    let dx = Math.abs(x1 - x0), dy = Math.abs(y1 - y0);
    const sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
    let err = dx - dy, guard = 0;
    for (;;) {
      if (x0 >= 0 && x0 < width && y0 >= 0 && y0 < height) {
        const o = (y0 * width + x0) * 4;
        rgba[o] = col[0]; rgba[o + 1] = col[1]; rgba[o + 2] = col[2]; rgba[o + 3] = 255;
      }
      if ((x0 === x1 && y0 === y1) || guard++ > 100000) break;
      const e2 = 2 * err;
      if (e2 > -dy) { err -= dy; x0 += sx; }
      if (e2 < dx) { err += dx; y0 += sy; }
    }
  };
  for (const t of tris) {
    const [x0, y0, z0, x1, y1, z1, x2, y2, z2, col] = t;
    if (wireframe) {
      edge(x0, y0, x1, y1, col); edge(x1, y1, x2, y2, col); edge(x2, y2, x0, y0, col);
    } else {
      const minX = Math.max(0, Math.floor(Math.min(x0, x1, x2)));
      const maxX = Math.min(width - 1, Math.ceil(Math.max(x0, x1, x2)));
      const minY = Math.max(0, Math.floor(Math.min(y0, y1, y2)));
      const maxY = Math.min(height - 1, Math.ceil(Math.max(y0, y1, y2)));
      for (let py = minY; py <= maxY; py++) {
        for (let px = minX; px <= maxX; px++) {
          const d = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2);
          if (d === 0) continue;
          const a = ((y1 - y2) * (px - x2) + (x2 - x1) * (py - y2)) / d;
          const b = ((y2 - y0) * (px - x2) + (x0 - x2) * (py - y2)) / d;
          const c = 1 - a - b;
          if (a < 0 || b < 0 || c < 0) continue;
          const z = a * z0 + b * z1 + c * z2;
          const o = (py * width + px);
          if (z > zbuf[o]) { zbuf[o] = z; const q = o * 4; rgba[q] = col[0]; rgba[q + 1] = col[1]; rgba[q + 2] = col[2]; rgba[q + 3] = 255; }
        }
      }
    }
  }
  return rgba;
}

async function main() {
  const args = parseArgs(process.argv);
  const modelsDir = args['models-dir'];
  const outDir = args['out-dir'];
  const size = args.size ? parseInt(args.size, 10) : 1536;
  if (!modelsDir || !outDir) throw new Error('--models-dir <dir> --out-dir <dir> required');
  const models = (args.models ?? '192374.nif,193207.nif,193313.nif,193684.nif').split(',');
  fs.mkdirSync(outDir, { recursive: true });

  const manifest = [];
  for (const name of models) {
    const payload = new Uint8Array(fs.readFileSync(`${modelsDir}\\${name}`));
    const r = readNif41(payload, { sourceName: name });
    const ir = buildAssetIR(r, {
      assetId: parseInt(name.replace(/\.nif$/i, ''), 10) || name,
      era: 'CD_2003', build: 'CD_2003_Models_ark_primary_phase3_render',
      container: 'Models/Models.ark', entryName: name,
      payloadSha256: '0'.repeat(64), sizeBytes: payload.length,
      adapterVersion: PEC_NIF41_READER_VERSION,
    });
    const world = composeWorldTransforms(ir);
    const byIndex = new Map(ir.blocks.map((b) => [b.index, b]));
    // gather world-transformed triangles per mesh (world = parentWorld * local; identity TRS here — but applied fully)
    const meshes = [];
    let minB = [Infinity, Infinity, Infinity], maxB = [-Infinity, -Infinity, -Infinity];
    for (const b of ir.blocks) {
      if (b.type !== 'NiTriShape') continue;
      const data = b.dataRef != null ? byIndex.get(b.dataRef) : null;
      if (!data?.geometry?.positions || !data.geometry.indices) continue;
      const w = world.get(b.index);
      const pos = data.geometry.positions, idx = data.geometry.indices;
      const tris = [];
      for (let i = 0; i < idx.length; i += 3) {
        const p0 = applyTrsPoint(w, [pos[idx[i] * 3], pos[idx[i] * 3 + 1], pos[idx[i] * 3 + 2]]);
        const p1 = applyTrsPoint(w, [pos[idx[i + 1] * 3], pos[idx[i + 1] * 3 + 1], pos[idx[i + 1] * 3 + 2]]);
        const p2 = applyTrsPoint(w, [pos[idx[i + 2] * 3], pos[idx[i + 2] * 3 + 1], pos[idx[i + 2] * 3 + 2]]);
        for (const p of [p0, p1, p2]) for (let k = 0; k < 3; k++) { if (p[k] < minB[k]) minB[k] = p[k]; if (p[k] > maxB[k]) maxB[k] = p[k]; }
        tris.push([p0, p1, p2]);
      }
      meshes.push({ name: b.name, tris });
    }
    // ---- top-down (file x/z plane): image x = file x, image y = file z ----
    const spanX = maxB[0] - minB[0], spanZ = maxB[2] - minB[2];
    const top = (spanX >= spanZ) ? spanX : spanZ;
    const W = Math.max(8, Math.round(size * (spanX / top))), H = Math.max(8, Math.round(size * (spanZ / top)));
    const toImgX = (x) => ((x - minB[0]) / (spanX || 1)) * (W - 1);
    const toImgY = (z) => ((z - minB[2]) / (spanZ || 1)) * (H - 1);
    const topTris = [], topTrisWire = [];
    meshes.forEach((m, mi) => {
      const col = MESH_COLORS[mi % MESH_COLORS.length];
      for (const [p0, p1, p2] of m.tris) {
        topTris.push([toImgX(p0[0]), toImgY(p0[2]), p0[1], toImgX(p1[0]), toImgY(p1[2]), p1[1], toImgX(p2[0]), toImgY(p2[2]), p2[1], col]);
        topTrisWire.push([toImgX(p0[0]), toImgY(p0[2]), 0, toImgX(p1[0]), toImgY(p1[2]), 0, toImgX(p2[0]), toImgY(p2[2]), 0, [255, 255, 255]]);
      }
    });
    const pngTop = pngEncode(W, H, renderTriangles(W, H, topTris, false));
    const pngTopWire = pngEncode(W, H, renderTriangles(W, H, topTrisWire, true));
    const stem = name.replace('.nif', '');
    fs.writeFileSync(`${outDir}\\${stem}_topdown_xz_filled.png`, pngTop);
    fs.writeFileSync(`${outDir}\\${stem}_topdown_xz_wireframe.png`, pngTopWire);

    // ---- 3D isometric wireframe: rotate file (x,y,z) by yaw -30°, pitch 25° ----
    // Isometric projection of the FILE axes (not world semantics): a reading aid only.
    const yaw = -30 * Math.PI / 180, pitch = 25 * Math.PI / 180;
    const proj = (p) => {
      const [x, y, z] = p;
      const cx = Math.cos(yaw), sx = Math.sin(yaw);
      let x1 = x * cx - y * sx, y1 = x * sx + y * cx, z1 = z;
      const cy = Math.cos(pitch), sy = Math.sin(pitch);
      const y2 = y1 * cy - z1 * sy, z2 = y1 * sy + z1 * cy;
      return [x1, z2, y2]; // image x, depth, image y
    };
    let pMin = [Infinity, Infinity], pMax = [-Infinity, -Infinity];
    const projected = meshes.map((m) => m.tris.map(([p0, p1, p2]) => [proj(p0), proj(p1), proj(p2)]));
    for (const mm of projected) for (const [p0, p1, p2] of mm) for (const p of [p0, p1, p2]) {
      if (p[0] < pMin[0]) pMin[0] = p[0]; if (p[0] > pMax[0]) pMax[0] = p[0];
      if (p[2] < pMin[1]) pMin[1] = p[2]; if (p[2] > pMax[1]) pMax[1] = p[2];
    }
    const spX = pMax[0] - pMin[0] || 1, spY = pMax[1] - pMin[1] || 1;
    const W3 = Math.max(8, Math.round(size * (spX / Math.max(spX, spY)))), H3 = Math.max(8, Math.round(size * (spY / Math.max(spX, spY))));
    const isoTris = [];
    projected.forEach((mm, mi) => {
      const col = MESH_COLORS[mi % MESH_COLORS.length];
      for (const [p0, p1, p2] of mm) {
        const ix = (p) => ((p[0] - pMin[0]) / spX) * (W3 - 1);
        const iy = (p) => ((p[2] - pMin[1]) / spY) * (H3 - 1);
        isoTris.push([ix(p0), iy(p0), 0, ix(p1), iy(p1), 0, ix(p2), iy(p2), 0, col]);
      }
    });
    const pngIso = pngEncode(W3, H3, renderTriangles(W3, H3, isoTris, true));
    fs.writeFileSync(`${outDir}\\${stem}_iso3d_wireframe.png`, pngIso);

    manifest.push({
      model: name, era: 'CD_2003',
      renders: [
        { file: `${stem}_topdown_xz_filled.png`, view: 'file x/z plane (image x=file x, image y=file z), z-buffer over file y; axis semantics NOT established', width: W, height: H },
        { file: `${stem}_topdown_xz_wireframe.png`, view: 'same projection, triangle edges', width: W, height: H },
        { file: `${stem}_iso3d_wireframe.png`, view: 'isometric reading aid over file x/y/z (yaw -30deg pitch 25deg) — NOT a world-space claim', width: W3, height: H3 },
      ],
      composedBoundsFileSceneSpace: { min: minB, max: maxB },
      meshColorLegend: meshes.map((m, mi) => ({ mesh: m.name, colorRgb: MESH_COLORS[mi % MESH_COLORS.length], triangles: m.tris.length })),
      note: 'connected triangle components are NOT building counts; original origin preserved (image maps the composed AABB 1:1, no centering)',
    });
  }
  fs.writeFileSync(`${outDir}\\RENDER_MANIFEST.json`, JSON.stringify(manifest, null, 1), 'utf8');
  process.stdout.write(JSON.stringify({ artifact: 'PHASE3_RENDERS', models: manifest.map((m) => ({ model: m.model, renders: m.renders.map((r) => r.file) })) }, null, 1) + '\n');
}

main().catch((err) => {
  console.error('[phase3_renders] FATAL:', err?.stack ?? err);
  process.exitCode = 1;
});
