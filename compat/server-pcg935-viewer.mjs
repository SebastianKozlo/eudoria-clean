#!/usr/bin/env node
// server-pcg935-viewer.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 7)
//
// Loopback-only viewer server for the PCG 9.3.5 full-asset SceneIR:
//   - static allowlist (the pcg935-viewer app files; no fs paths from URLs)
//   - pinned Three.js 0.185.0 serving (jail-checked subtree, version-verified)
//   - /api/catalog          — the full 5,596-entry ranked catalog (read-only)
//   - /api/asset/<id>       — per-entry REAL parse -> IR -> geometry/anim/
//                             texture-chain JSON (LRU-bounded, size-limited)
//   - /api/texture/<id>     — same-era Textures.bnt decode -> PNG (LRU-bounded)
//   - /api/status           — truthful runtime status
//   - everything else 404; traversal/foreign/malformed denied with real errors.
//
// START:  node compat/server-pcg935-viewer.mjs   (env PORT, default 8164)
// The 8140 old viewer (server-sceneir.mjs) stays untouched during development.
'use strict';

import http from 'node:http';
import net from 'node:net';
import path from 'node:path';
import fs from 'node:fs';
import zlib from 'node:zlib';
import crypto from 'node:crypto';

import { Bnt2Archive } from '../src/pesource/Bnt2Archive.js';
import { readNif10Corpus } from '../src/pecompat/PecNif10CorpusReader.js';
import { readNif41Corpus } from '../src/pecompat/PecNif41Reader.js';
import {
  buildAssetIR, validateSceneGraph, composeWorldTransforms, computeSceneBounds,
} from '../src/pecompat/PecSceneIR.js';
import { resolveAssetTextures } from '../src/pecompat/PecTextureChain.js';
import { decodeAssetAnimations } from '../src/pecompat/PecAnimDecoder.js';
import { sniffTextureFormat, decodeTexturePayload } from '../src/pecompat/PecTextureChain.js';

const CONFIG = {
  port: Number(process.env.PORT) || 8164,
  host: '127.0.0.1',
  repoRoot: process.cwd(),
  modelsPath: process.env.PECOMPAT_MODELS
    || 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt',
  texturesPath: process.env.PECOMPAT_TEXTURES
    || 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Textures\\Textures.bnt',
  catalogPath: process.env.PECOMPAT_CATALOG
    || 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010\\catalog\\catalog.json',
  threeRoot: process.env.PECOMPAT_THREE_ROOT
    || 'D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\node_modules\\three',
  threePinnedVersion: '0.185.0',
  // fail-closed pinned input SHAs (contract preflight values)
  modelsSha256: 'C950A8C2'.toLowerCase(),
  texturesSha256Prefix: '61acd13b',
  assetCacheMax: 6,      // LRU entries for parsed assets
  textureCacheMax: 128,  // LRU entries for decoded texture PNGs
  maxAssetJsonBytes: 96 * 1024 * 1024, // hard payload ceiling for one asset
  requestLineLimit: 512,
};

// ---------------------------------------------------------------- load inputs

function sha256(buf) {
  return crypto.createHash('sha256').update(buf).digest('hex');
}

function fail(msg) {
  console.error(`[server] FATAL: ${msg}`);
  process.exit(1);
}

const modelsBytes = new Uint8Array(fs.readFileSync(CONFIG.modelsPath));
const modelsSha = sha256(modelsBytes);
if (!modelsSha.startsWith(CONFIG.modelsSha256)) {
  fail(`Models.bnt sha256 ${modelsSha} does not match the pinned prefix ${CONFIG.modelsSha256}`);
}
const modelsArchive = new Bnt2Archive(modelsBytes);
const modelsEntries = modelsArchive.entries();
const modelsByName = new Map(modelsEntries.map((e) => [e.name, e]));
const entryIdByName = new Map(modelsEntries.map((e) => [e.name, parseInt(e.name, 10)]));
const entryById = new Map(modelsEntries.map((e) => [parseInt(e.name, 10), e]));

const texturesBytes = new Uint8Array(fs.readFileSync(CONFIG.texturesPath));
const texturesSha = sha256(texturesBytes);
if (!texturesSha.startsWith(CONFIG.texturesSha256Prefix)) {
  fail(`Textures.bnt sha256 ${texturesSha} does not match the pinned prefix ${CONFIG.texturesSha256Prefix}`);
}
const texturesArchive = new Bnt2Archive(texturesBytes);
const textureEntryById = new Map(texturesArchive.entries().map((e) => [parseInt(e.name, 10), e]));

const catalogBuffer = fs.readFileSync(CONFIG.catalogPath);
const catalog = JSON.parse(catalogBuffer.toString('utf8'));
if (!catalog || !Array.isArray(catalog.entries) || catalog.entries.length < 1000) {
  fail(`catalog at ${CONFIG.catalogPath} is missing/implausible`);
}
const catalogById = new Map(catalog.entries.map((e) => [e.id, e]));

// three pinned-version verification
{
  const pj = JSON.parse(fs.readFileSync(path.join(CONFIG.threeRoot, 'package.json'), 'utf8'));
  if (pj.version !== CONFIG.threePinnedVersion) {
    fail(`three package at ${CONFIG.threeRoot} is ${pj.version}, pinned version is ${CONFIG.threePinnedVersion}`);
  }
}

console.log(`[server] Models.bnt ${modelsBytes.length} B sha256 ${modelsSha.slice(0, 12)}…`);
console.log(`[server] Textures.bnt ${texturesBytes.length} B sha256 ${texturesSha.slice(0, 12)}…`);
console.log(`[server] catalog entries: ${catalog.entries.length} (pass ${catalog.stats.pass}, fail ${catalog.stats.fail})`);
console.log(`[server] three ${CONFIG.threePinnedVersion} verified at ${CONFIG.threeRoot}`);

// ---------------------------------------------------------------- LRU caches

function makeLru(max) {
  const map = new Map();
  return {
    get(k) {
      if (!map.has(k)) return undefined;
      const v = map.get(k);
      map.delete(k);
      map.set(k, v);
      return v;
    },
    set(k, v) {
      if (map.has(k)) map.delete(k);
      map.set(k, v);
      if (map.size > max) map.delete(map.keys().next().value);
    },
    size: () => map.size,
  };
}
const assetCache = makeLru(CONFIG.assetCacheMax);
const textureCache = makeLru(CONFIG.textureCacheMax);

// ---------------------------------------------------------------- PNG encoder

const CRC_TABLE = (() => {
  const t = new Int32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c;
  }
  return t;
})();
function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
function chunk(type, data) {
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length, 0);
  const typeBuf = Buffer.from(type, 'ascii');
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(Buffer.concat([typeBuf, data])), 0);
  return Buffer.concat([len, typeBuf, data, crc]);
}
/** Encode top-first RGBA as PNG (row 0 = top). No deps. */
export function encodePng(width, height, rgba) {
  const sig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(width, 0);
  ihdr.writeUInt32BE(height, 4);
  ihdr[8] = 8;  // bit depth
  ihdr[9] = 6;  // RGBA
  ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
  const stride = width * 4;
  const raw = Buffer.alloc((stride + 1) * height);
  for (let y = 0; y < height; y++) {
    raw[y * (stride + 1)] = 0; // filter: none
    Buffer.from(rgba.buffer, rgba.byteOffset + y * stride, stride).copy(raw, y * (stride + 1) + 1);
  }
  const idat = zlib.deflateSync(raw, { level: 6 });
  return Buffer.concat([sig, chunk('IHDR', ihdr), chunk('IDAT', idat), chunk('IEND', Buffer.alloc(0))]);
}

// ---------------------------------------------------------------- asset parse

function base64Of(typedArr) {
  return Buffer.from(typedArr.buffer, typedArr.byteOffset, typedArr.byteLength).toString('base64');
}

function parseEntry(id) {
  const e = entryById.get(id);
  if (!e) return null;
  const payload = modelsBytes.subarray(e.offset, e.offset + e.size);
  const dv = new DataView(modelsBytes.buffer, modelsBytes.byteOffset, modelsBytes.byteLength);
  const p = modelsBytes.subarray(e.offset, e.offset + 64);
  const nl = p.indexOf(0x0a);
  if (nl < 4 || nl + 8 > p.length) return null;
  const version = dv.getUint32(e.offset + nl + 1, true);
  const r = version >= 0x0a000000
    ? readNif10Corpus(payload, { sourceName: e.name })
    : readNif41Corpus(payload, { sourceName: e.name });
  return { r, payload, version, entry: e };
}

function buildAssetResponse(id) {
  return buildAssetResponseImpl(id);
}

export { buildAssetResponse, assetCache, textureCache, CONFIG };

function buildAssetResponseImpl(id) {
  const cached = assetCache.get(id);
  if (cached) return cached;
  const parsed = parseEntry(id);
  if (!parsed) return null;
  const { r, payload, version, entry } = parsed;
  const versionString = version >= 0x0a000000 ? '10.1.0.0' : (version === 0x04000002 ? '4.0.0.2' : '4.1.0.12');
  const ir = buildAssetIR(r, {
    assetId: id, era: 'PCG_9_3_5', build: 'PCG_9_3_5_Models_bnt_entry',
    container: 'Models/Models.bnt', entryName: entry.name, payloadSha256: sha256(payload),
    sizeBytes: entry.size, adapterVersion: 'pcg935-server-r1', physicalSource: 'Models.bnt',
  });
  const validation = validateSceneGraph(ir);
  const world = composeWorldTransforms(ir);
  const bounds = computeSceneBounds(ir, world);
  const anim = decodeAssetAnimations(ir);
  const tex = resolveAssetTextures(ir, (tid) => {
    const te = textureEntryById.get(tid);
    if (!te) return null;
    return { payload: texturesBytes.subarray(te.offset, te.offset + te.size) };
  }, null);

  const blocksSlim = ir.blocks.map((b) => ({
    i: b.index, t: b.type, n: b.name ?? null,
  }));
  const byIndex = new Map(ir.blocks.map((b) => [b.index, b]));
  const meshes = [];
  for (const b of ir.blocks) {
    if (b.type !== 'NiTriShape') continue;
    const dataB = byIndex.get(b.dataRef);
    const g = dataB?.geometry;
    if (!g) continue;
    const wf = world.get(b.index) ?? { elements: null };
    const mats = (b.fields?.propertyRefs ?? b.propertyRefs ?? [])
      .map((ref) => byIndex.get(ref)).filter((x) => x);
    const matProp = mats.find((x) => x.type === 'NiMaterialProperty');
    const alphaProp = mats.find((x) => x.type === 'NiAlphaProperty');
    const texProp = mats.find((x) => x.type === 'NiTexturingProperty');
    // texture binding for this mesh (per the resolved chain)
    const texRes = tex.results.find((m) => m.meshIndex === b.index);
    const slotTex = (texRes?.slots ?? []).filter((s) => s.hasMap).map((s) => ({
      slot: s.slot, state: s.state, textureId: s.textureId ?? null, label: s.label ?? null,
      method: s.method, byteShapeControl: s.byteShapeControl ?? null, referenceControl: s.referenceControl ?? null,
    }));
    meshes.push({
      name: b.name ?? '', block: b.index, dataBlock: b.dataRef,
      numVertices: g.numVertices, numTriangles: g.numTriangles,
      positions: base64Of(g.positions ?? new Float32Array(0)),
      normals: g.normals ? base64Of(g.normals) : null,
      uvs: (g.uvSets?.[0]) ? base64Of(g.uvSets[0]) : null,
      indices: g.indices ? base64Of(g.indices) : null,
      world: wf.elements ? Array.from(wf.elements) : null,
      material: matProp ? {
        ambient: matProp.fields?.ambient ?? null, diffuse: matProp.fields?.diffuse ?? null,
        specular: matProp.fields?.specular ?? null, emissive: matProp.fields?.emissive ?? null,
        alpha: matProp.fields?.materialAlpha ?? null,
      } : null,
      alphaProp: alphaProp ? { flags: alphaProp.fields?.propertyFlags ?? null, threshold: alphaProp.fields?.alphaThreshold ?? null } : null,
      texSlots: slotTex,
      skin: (ir.blocks.find((x) => x.type === 'NiSkinInstance' && (byIndex.get(x.fields?.dataRef) !== undefined))
        && false) ? null : null, // skins attached below via anim.skeletons
    });
  }
  const response = {
    runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
    id, name: entry.name, sizeBytes: entry.size, payloadSha256: sha256(payload),
    version: versionString,
    status: validation.ok ? 'OK' : 'LINK_ERRORS',
    validationErrors: validation.errors.slice(0, 16),
    blocks: blocksSlim,
    blockTypeCensus: ir.blockTypeCensus,
    numBlocks: r.blocks.length,
    meshes,
    bounds: {
      min: bounds.min ?? null,
      max: bounds.max ?? null,
      extents: bounds.extents ?? null,
      maxAxisExtent: (bounds.extents && Number.isFinite(bounds.min?.[0]))
        ? Math.max(bounds.extents[0], bounds.extents[1], bounds.extents[2]) : null,
    },
    animations: anim,
    textures: { state: tex.state, exactSlots: tex.exactSlots, mapSlots: tex.mapSlots, fallback: tex.fallback, meshes: tex.results },
    generatedAt: new Date().toISOString(),
  };
  const json = JSON.stringify(response);
  if (json.length > CONFIG.maxAssetJsonBytes) {
    throw Object.assign(new Error(`asset ${id} JSON ${json.length} B exceeds the ${CONFIG.maxAssetJsonBytes} B ceiling`), { statusCode: 413 });
  }
  const obj = { json, etag: `"a-${sha256(Buffer.from(json)).slice(0, 16)}"` };
  assetCache.set(id, obj);
  return obj;
}

// ---------------------------------------------------------------- http plumbing

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.wasm': 'application/wasm',
};

const STATIC_FILES = new Map([
  ['/', { file: 'compat/pcg935-viewer.html', mime: 'text/html; charset=utf-8' }],
  ['/index.html', { file: 'compat/pcg935-viewer.html', mime: 'text/html; charset=utf-8' }],
  ['/app.js', { file: 'compat/pcg935-viewer.js', mime: 'text/javascript; charset=utf-8' }],
  ['/app.css', { file: 'compat/pcg935-viewer.css', mime: 'text/css; charset=utf-8' }],
]);

function deny(res, status, code, message, rawUrl) {
  const body = JSON.stringify({ error: code, message, url: rawUrl }, null, 1) + '\n';
  res.writeHead(status, { 'content-type': 'application/json', 'content-length': Buffer.byteLength(body) });
  res.end(body);
}

function serveBytes(res, status, buf, mime, extra = {}) {
  res.writeHead(status, {
    'content-type': mime,
    'content-length': buf.length,
    'cache-control': 'no-store',
    ...extra,
  });
  res.end(buf);
}

function readJailed(root, sub) {
  if (sub.includes('..') || sub.includes('\\') || sub.includes('\0') || path.isAbsolute(sub)) return null;
  const abs = path.normalize(path.join(root, sub));
  if (!abs.startsWith(path.normalize(root))) return null;
  try { return fs.readFileSync(abs); } catch { return null; }
}

export function createApp({ wire, statusInfo }) {
  return async function handle(req, res) {
    const rawUrl = req.url;
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      deny(res, 405, 'METHOD_NOT_ALLOWED_READ_ONLY', `method ${req.method} refused: read-only loopback viewer API`, rawUrl);
      return;
    }
    if (rawUrl.length > CONFIG.requestLineLimit) {
      deny(res, 414, 'URL_TOO_LONG', `URL exceeds ${CONFIG.requestLineLimit} B bound`, rawUrl);
      return;
    }
    let urlPath;
    try {
      urlPath = decodeURIComponent(rawUrl.split('?')[0]);
    } catch {
      deny(res, 400, 'MALFORMED_URL', 'percent-decoding failed', rawUrl);
      return;
    }
    if (urlPath.includes('\0')) { deny(res, 400, 'NULL_BYTE_IN_URL', 'NUL byte refused', rawUrl); return; }
    if (urlPath.includes('\\')) { deny(res, 400, 'BACKSLASH_IN_URL', 'backslash refused', rawUrl); return; }

    // static allowlist
    const st = STATIC_FILES.get(urlPath);
    if (st) {
      const b = fs.readFileSync(path.join(CONFIG.repoRoot, st.file));
      serveBytes(res, 200, b, st.mime);
      return;
    }
    // three (jail-checked, version already verified at startup)
    if (urlPath.startsWith('/node_modules/three/')) {
      const sub = urlPath.slice('/node_modules/three/'.length);
      const b = readJailed(CONFIG.threeRoot, sub);
      if (!b) { deny(res, 404, 'THREE_FILE_NOT_FOUND', `three submodule "${sub}" not found (jail-checked allowlist)`, rawUrl); return; }
      serveBytes(res, 200, b, MIME[path.extname(sub).toLowerCase()] || 'application/octet-stream');
      return;
    }
    if (urlPath.startsWith('/node_modules/')) {
      deny(res, 403, 'ONLY_THREE_ALLOWED', 'only the pinned three package is routed', rawUrl);
      return;
    }

    if (urlPath === '/api/status') {
      const body = JSON.stringify(statusInfo(), null, 1);
      serveBytes(res, 200, Buffer.from(body + '\n'), 'application/json');
      return;
    }
    if (urlPath === '/api/catalog') {
      serveBytes(res, 200, catalogBuffer, 'application/json');
      return;
    }
    if (urlPath.startsWith('/api/asset/')) {
      const rest = urlPath.slice('/api/asset/'.length);
      if (!/^\d{1,7}\.json$/.test(rest) && !/^\d{1,7}$/.test(rest)) {
        deny(res, 400, 'MALFORMED_ASSET_ID', `asset id "${rest.slice(0, 24)}" must be numeric (1-7 digits)`, rawUrl);
        return;
      }
      const id = parseInt(rest.replace(/\.json$/, ''), 10);
      if (!entryById.has(id)) {
        deny(res, 404, 'ASSET_ID_NOT_IN_INDEX', `id ${id} is not a Models.bnt index entry (foreign IDs refused)`, rawUrl);
        return;
      }
      try {
        const obj = buildAssetResponse(id);
        if (!obj) { deny(res, 500, 'PARSE_FAILED', `id ${id} could not be parsed`, rawUrl); return; }
        serveBytes(res, 200, Buffer.from(obj.json), 'application/json', { etag: obj.etag });
      } catch (err) {
        const isSize = err?.statusCode === 413;
        const status = isSize ? 413 : 422;
        deny(res, status, isSize ? 'ASSET_TOO_LARGE' : 'PARSE_FAILED_TRUTHFUL',
          `id ${id}: ${String(err?.message ?? err).slice(0, 400)}`, rawUrl);
        assetCache.set(id, { json: null, etag: null, failed: true });
        return;
      }
      return;
    }
    if (urlPath.startsWith('/api/texture/')) {
      const rest = urlPath.slice('/api/texture/'.length);
      if (!/^\d{1,7}\.png$/.test(rest) && !/^\d{1,7}$/.test(rest)) {
        deny(res, 400, 'MALFORMED_TEXTURE_ID', `texture id "${rest.slice(0, 24)}" must be numeric`, rawUrl);
        return;
      }
      const id = parseInt(rest.replace(/\.png$/, ''), 10);
      const cached = textureCache.get(id);
      if (cached) {
        if (cached.png) serveBytes(res, 200, cached.png, 'image/png', { etag: cached.etag });
        else deny(res, cached.status, cached.code, cached.message, rawUrl);
        return;
      }
      const te = textureEntryById.get(id);
      if (!te) {
        const rec = { png: null, status: 404, code: 'TEXTURE_ID_NOT_IN_INDEX', message: `id ${id} is not a Textures.bnt entry` };
        textureCache.set(id, rec);
        deny(res, 404, rec.code, rec.message, rawUrl);
        return;
      }
      const payload = texturesBytes.subarray(te.offset, te.offset + te.size);
      try {
        const dec = decodeTexturePayload(payload);
        const png = encodePng(dec.width, dec.height, dec.rgba);
        const rec = { png, etag: `"t-${sha256(png).slice(0, 16)}"` };
        textureCache.set(id, rec);
        serveBytes(res, 200, png, 'image/png', { etag: rec.etag });
      } catch (err) {
        const unsupported = err?.state === 'UNSUPPORTED_FORMAT';
        const rec = { png: null, status: unsupported ? 415 : 422, code: unsupported ? 'TEXTURE_FORMAT_UNSUPPORTED' : 'TEXTURE_DECODE_FAILED', message: String(err?.message ?? err).slice(0, 200) };
        textureCache.set(id, rec);
        deny(res, rec.status, rec.code, rec.message, rawUrl);
        return;
      }
      return;
    }
    deny(res, 404, 'ROUTE_NOT_FOUND', `no route for ${urlPath.slice(0, 80)} (allowlist: /, /app.js, /app.css, /node_modules/three/*, /api/*)`, rawUrl);
  };
}

// ---------------------------------------------------------------- main

function statusInfo() {
  return {
    runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
    server: 'server-pcg935-viewer.mjs',
    modelsSha256: modelsSha,
    texturesSha256: texturesSha,
    catalogEntries: catalog.entries.length,
    catalogStats: catalog.stats,
    cache: { assets: assetCache.size(), textures: textureCache.size() },
    threeVersion: CONFIG.threePinnedVersion,
    uptimeMs: Math.round(process.uptime() * 1000),
    startedAt,
  };
}

const startedAt = new Date().toISOString();

async function main() {
  const probeFree = (port, host) => new Promise((resolve) => {
    const p = net.createServer();
    p.once('error', () => resolve(false));
    p.listen(port, host, () => p.close(() => resolve(true)));
  });
  if (!(await probeFree(CONFIG.port, CONFIG.host))) {
    fail(`port ${CONFIG.port} on ${CONFIG.host} is BUSY — refusing to start`);
  }
  const server = http.createServer(createApp({ wire: null, statusInfo }));
  server.listen(CONFIG.port, CONFIG.host, () => {
    console.log(`[server] LISTENING http://${CONFIG.host}:${CONFIG.port}/ (read-only loopback viewer)`);
    console.log(`[server] routes: / /app.js /app.css /node_modules/three/* /api/status /api/catalog /api/asset/<id> /api/texture/<id>`);
  });
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
if (isMain) main();
