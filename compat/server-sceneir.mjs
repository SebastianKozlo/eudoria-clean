#!/usr/bin/env node
// server-sceneir.mjs -- PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// The app's bounded LOOPBACK server (contract §8 + PLAN §2/§3).
//
// DESIGN (path denial BY CONSTRUCTION):
//   - Binds 127.0.0.1 ONLY (loopback; the bind address is not configurable).
//   - PORT: env override, default 8140; VERIFIED FREE at bind (a busy port is
//     a LOUD failure -- this server never replaces or stops another process).
//   - Static surface = EXACT ALLOWLIST MAPS (the request URL never becomes a
//     filesystem path): the six compat app files, the four client-needed
//     src/pecompat modules, and the configured three-package private root.
//   - The ONLY data API is /api/sceneir/218757 -- the bounded, index-derived
//     SceneIR of model 218757, REGENERATED AT STARTUP from the pinned
//     Models.bnt through PecAssetAdapter (fail-closed: container + payload
//     SHA256 verified against the run pins; any mismatch exits non-zero and
//     NOTHING is served). No stale exported JSON exists in the product path;
//     the in-memory cache is keyed by the SceneIR cacheKey (asset SHA +
//     adapter/schema version).
//   - The whole BNT and arbitrary source trees are NOT exposed: no route can
//     reach them. /pcg/-style aliases are deliberately NOT replicated.
//   - Read-only: GET/HEAD only; other methods get 405.
//
// START:  node compat/server-sceneir.mjs           (env PORT, default 8140)
// STOP:   terminate the printed PID (Ctrl+C in the owning console, or
//         Stop-Process -Id <PID> / child.kill() from a harness).
// The startup line is:  sceneir server http://127.0.0.1:<PORT>/ pid=<PID>
//
// IMPORT-SAFE for tests: this module only starts the server when executed as
// the main script; importing { buildWireSceneIR, SCENEIR_WIRE_VERSION, ... }
// has no side effects.

'use strict';
import http from 'node:http';
import net from 'node:net';
import path from 'node:path';
import { promises as fsp } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

import { PecAssetAdapter, MODEL_218757_PINS } from '../src/pecompat/PecAssetAdapter.js';
import { fileSceneSpaceArtifact } from '../src/pecompat/PecSceneIR.js';
import { RENDER_ADAPTER_CHOICE } from '../src/pecompat/PecRenderConvert.js';
import { VIEWER_INSTANCE_WRAPPER_POLICY } from '../src/pecompat/PecInstanceBuilder.js';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url))); // repo root
const RUN_ID = 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009';
const SERVER_VERSION = 'sceneir-server-r1 (loopback, allowlist statics, regenerated SceneIR API)';

// ---- configured roots (the ONLY filesystem roots this server may read) ----
const CONFIG = {
  bind: '127.0.0.1',
  port: Number(process.env.PORT) || 8140,
  modelsBntPath: process.env.PECOMPAT_MODELS_BNT || MODEL_218757_PINS.modelsBntPath,
  threeRoot: process.env.PECOMPAT_THREE_ROOT ||
    'D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\node_modules\\three',
  threePinnedVersion: '0.185.0',
  modelId: MODEL_218757_PINS.modelId,
  logRequests: process.env.SCENEIR_LOG_REQUESTS === '1',
};

// EXACT static allowlists (request URL -> fixed repo file; no user-derived path).
const COMPAT_FILES = Object.freeze({
  'index.html': 'compat/index.html',
  'app.js': 'compat/app.js',
  'api.js': 'compat/api.js',
  'asset-mode.js': 'compat/asset-mode.js',
  'scene-mode.js': 'compat/scene-mode.js',
  'compat.css': 'compat/compat.css',
});
// The four client-needed modules. PecNif10Reader.js/PecAssetAdapter.js are the
// SERVER-SIDE extraction chain and are deliberately NOT publicly routed.
const PEC_MODULES = Object.freeze([
  'PecTransform.js', 'PecSceneIR.js', 'PecInstanceBuilder.js', 'PecRenderConvert.js',
]);

export const SCENEIR_WIRE_VERSION = 'pec-sceneir-wire-v1';

const MIME = {
  '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.html': 'text/html', '.json': 'application/json', '.css': 'text/css',
  '.map': 'application/json', '.txt': 'text/plain',
};

// ---------------------------------------------------------------------------
// buildWireSceneIR -- the bounded wire payload of the regenerated SceneIR.
// Serves: identity/provenance, per-block TRS + links, geometry arrays (plain
// JSON arrays; regenerated at runtime from the pinned container, loopback
// only, NEVER committed as a fixture), fingerprints, bounded diagnostics.
// NO raw opaque bytes (only boundaries), no SDK/NIF payloads.
// ---------------------------------------------------------------------------
export function buildWireSceneIR(loadedModel) {
  const { ir, worldTransforms, meshFingerprints, provenance, validation, sceneBounds } = loadedModel;
  const blocks = ir.blocks.map((b) => {
    const rec = {
      index: b.index,
      type: b.type,
      name: b.name,
      decodeStatus: b.decodeStatus,
      byteRange: [b.byteStart, b.byteEnd],
      localTrs: b.localTrs
        ? { translate: [...b.localTrs.translate], rotate: b.localTrs.rotate.map((r) => [...r]), scale: b.localTrs.scale }
        : null,
      children: b.children ?? null,
      propertyRefs: b.propertyRefs ?? null,
      extraDataRefs: b.extraDataRefs ?? null,
      dataRef: b.dataRef ?? null,
      geometry: null,
      opaqueBoundary: b.opaque
        ? { extStart: b.opaque.extStart, extEnd: b.opaque.extEnd, extLength: b.opaque.extLength, boundaryMethod: b.opaque.boundaryMethod }
        : null,
    };
    if (b.geometry) {
      const g = b.geometry;
      rec.geometry = {
        positions: Array.from(g.positions ?? []),
        normals: g.normals ? Array.from(g.normals) : null,
        colors: g.colors ? Array.from(g.colors) : null,
        uvSets: (g.uvSets ?? []).map((set) => Array.from(set)),
        indices: Array.from(g.indices ?? []),
        numVertices: g.numVertices,
        numTriangles: g.numTriangles,
        vertexPositionsF32leSha256: g.vertexPositionsF32leSha256 ?? null,
        triangleIndicesU16leSha256: g.triangleIndicesU16leSha256 ?? null,
        vertexByteRange: g.vertexRange ? [g.vertexRange.start, g.vertexRange.end] : null,
        indexByteRange: g.indexRange ? [g.indexRange.start, g.indexRange.end] : null,
      };
    }
    return rec;
  });
  return {
    wireVersion: SCENEIR_WIRE_VERSION,
    run: RUN_ID,
    serverVersion: SERVER_VERSION,
    cacheKey: ir.cacheKey,
    wireContract:
      'regenerated at server startup from the pinned Models.bnt through PecAssetAdapter ' +
      '(fail-closed SHA); geometry arrays are runtime loopback-only data, never a committed fixture',
    provenance,
    pins: {
      modelId: MODEL_218757_PINS.modelId,
      payloadSha256: MODEL_218757_PINS.payloadSha256,
      containerSha256: MODEL_218757_PINS.modelsBntSha256,
    },
    asset: {
      assetId: ir.asset.assetId,
      era: ir.asset.era,
      build: ir.asset.build,
      container: ir.asset.container,
      entryName: ir.asset.entryName,
      payloadSha256: ir.asset.payloadSha256,
      sizeBytes: ir.asset.sizeBytes,
      nifVersion: ir.asset.nifVersion,
      numBlocks: ir.asset.numBlocks,
      closure: {
        eofExact: ir.asset.closure.eofExact,
        numBlocksDecoded: ir.asset.closure.numBlocksDecoded,
        topObjects: ir.asset.closure.topObjects,
        decisions: ir.asset.closure.decisions,
      },
    },
    blockTypeCensus: ir.blockTypeCensus,
    decodeCensus: ir.decodeCensus,
    roots: ir.roots,
    blocks,
    meshAssociations: ir.meshAssociations,
    meshFingerprints,
    textureBindings: ir.diagnostics.textureBindings,
    diagnosticsNotes: ir.diagnostics.notes,
    sceneBounds_FILE_SCENE_SPACE: sceneBounds,
    // phase-2 bounded artifact (transforms + names only): shipped for the
    // client's INDEPENDENT composition cross-check (fail-closed on mismatch).
    fileSceneSpaceTransforms: fileSceneSpaceArtifact(ir, worldTransforms).blocks,
    validation: {
      ok: validation.ok,
      errorCount: validation.errors.length,
      warnings: validation.warnings,
    },
    renderAdapterChoice: RENDER_ADAPTER_CHOICE,
    policyLabels: {
      viewerInstanceWrapper: VIEWER_INSTANCE_WRAPPER_POLICY,
      authorPlacedLab:
        'AUTHOR_PLACED_LAB -- authored laboratory coordinates. NOT historical Eudoria positions. ' +
        'HISTORICAL_WORLD_INSTANCE = NOT_ESTABLISHED; WORLD_XYZ_RECOVERED = NO.',
      units: 'PE_AXES_AND_UNITS = UNVERIFIED_FROM_ENGINE; the render conversion is a RENDER_ADAPTER_CHOICE / PE_UNITS_NOT_CONFIRMED applied exactly once.',
    },
  };
}

// ---------------------------------------------------------------------------
// request handling
// ---------------------------------------------------------------------------
function deny(res, status, error, message, requestPath) {
  const body = JSON.stringify({ ok: false, error, message, requestPath: requestPath ?? null });
  res.writeHead(status, { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' });
  res.end(body);
  return body.length;
}

function serveBytes(res, status, bytes, contentType, extraHeaders = {}) {
  res.writeHead(status, {
    'Content-Type': contentType,
    'Cache-Control': 'no-store',
    'Content-Length': bytes.length,
    ...extraHeaders,
  });
  res.end(bytes);
}

async function readRepoFile(rel) {
  return fsp.readFile(path.join(ROOT, rel));
}

/** Jail-checked read inside the configured three package root. Returns
 *  {bytes} | {denyStatus, denyError, denyMessage} -- never an escape. */
async function readThreeSub(sub) {
  if (sub.includes('..') || sub.includes('\\') || sub.includes('\0') || sub.includes('%')) {
    return { denyStatus: 403, denyError: 'PATH_TRAVERSAL_BLOCKED', denyMessage: 'three-package route refuses traversal/encoded/absolute escape attempts (allowlist-jailed subtree)' };
  }
  const abs = path.normalize(path.join(CONFIG.threeRoot, sub));
  const rootWithSep = CONFIG.threeRoot.endsWith(path.sep) ? CONFIG.threeRoot : CONFIG.threeRoot + path.sep;
  if (abs !== CONFIG.threeRoot && !abs.startsWith(rootWithSep)) {
    return { denyStatus: 403, denyError: 'PATH_TRAVERSAL_BLOCKED', denyMessage: 'resolved path escaped the configured three package root' };
  }
  try {
    const st = await fsp.stat(abs);
    if (!st.isFile()) return { denyStatus: 404, denyError: 'NOT_A_FILE', denyMessage: 'the three-package route serves files only' };
    return { bytes: await fsp.readFile(abs) };
  } catch {
    return { denyStatus: 404, denyError: 'THREE_FILE_NOT_FOUND', denyMessage: 'no such file inside the configured three package root' };
  }
}

export function createApp({ wire, statusInfo }) {
  const logRequests = CONFIG.logRequests;
  return async function handle(req, res) {
    if (logRequests) {
      res.on('finish', () => console.log(`[req] ${req.method} ${req.url} -> ${res.statusCode}`));
    }
    const rawUrl = req.url;
    // read-only surface: GET/HEAD only.
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      deny(res, 405, 'METHOD_NOT_ALLOWED_READ_ONLY', `method ${req.method} refused: the server is a read-only loopback asset API`, rawUrl);
      return;
    }
    let urlPath;
    try {
      urlPath = decodeURIComponent(rawUrl.split('?')[0]);
    } catch {
      deny(res, 400, 'MALFORMED_URL', 'percent-decoding failed (malformed URL refused)', rawUrl);
      return;
    }
    if (urlPath.includes('\0')) {
      deny(res, 400, 'NULL_BYTE_IN_URL', 'NUL byte in URL refused', rawUrl);
      return;
    }
    if (urlPath.includes('\\')) {
      deny(res, 400, 'BACKSLASH_IN_URL', 'backslash in URL refused (no Windows path semantics in routes)', rawUrl);
      return;
    }

    // ---- static allowlists (exact map lookups; no fs path from the URL) ----
    if (urlPath === '/' || urlPath === '/index.html' || urlPath === '/compat/' || urlPath === '/compat/index.html') {
      const b = await readRepoFile(COMPAT_FILES['index.html']);
      serveBytes(res, 200, b, 'text/html');
      return;
    }
    if (urlPath.startsWith('/compat/')) {
      const key = urlPath.slice('/compat/'.length);
      const rel = COMPAT_FILES[key];
      if (!rel) {
        deny(res, 404, 'STATIC_FILE_NOT_ALLOWEDLISTED',
          `"${key}" is not in the compat allowlist (fixed file set: ${Object.keys(COMPAT_FILES).join(', ')})`, rawUrl);
        return;
      }
      const b = await readRepoFile(rel);
      serveBytes(res, 200, b, MIME[path.extname(rel)] || 'application/octet-stream');
      return;
    }
    if (urlPath.startsWith('/src/pecompat/')) {
      const name = urlPath.slice('/src/pecompat/'.length);
      if (!PEC_MODULES.includes(name)) {
        deny(res, 404, 'STATIC_FILE_NOT_ALLOWEDLISTED',
          `"${name}" is not in the client module allowlist (${PEC_MODULES.join(', ')}); the server-side extraction chain (PecNif10Reader/PecAssetAdapter) is not publicly routed`, rawUrl);
        return;
      }
      const b = await readRepoFile(path.join('src', 'pecompat', name));
      serveBytes(res, 200, b, 'text/javascript');
      return;
    }
    if (urlPath.startsWith('/node_modules/three/')) {
      const sub = urlPath.slice('/node_modules/three/'.length);
      const r = await readThreeSub(sub);
      if (r.bytes) {
        serveBytes(res, 200, r.bytes, MIME[path.extname(sub).toLowerCase()] || 'application/octet-stream');
      } else {
        deny(res, r.denyStatus, r.denyError, r.denyMessage, rawUrl);
      }
      return;
    }

    // ---- bounded data API ----
    if (urlPath === '/api/status') {
      const body = JSON.stringify(statusInfo(), null, 1);
      serveBytes(res, 200, Buffer.from(body + '\n'), 'application/json');
      return;
    }
    if (urlPath.startsWith('/api/sceneir/')) {
      const id = urlPath.slice('/api/sceneir/'.length).replace(/\.json$/, '');
      if (id !== String(CONFIG.modelId)) {
        deny(res, 404, 'UNKNOWN_ASSET_ID',
          `asset "${id}" is not served: this server exposes ONLY the bounded index-derived SceneIR of model ${CONFIG.modelId} (no whole-BNT or arbitrary-entry route exists)`, rawUrl);
        return;
      }
      const body = Buffer.from(JSON.stringify(wire) + '\n');
      serveBytes(res, 200, body, 'application/json', {
        'X-PE-Cache-Key': wire.cacheKey,
        'X-PE-Payload-Sha256': wire.provenance.payloadSha256,
        'X-PE-Container-Sha256': wire.provenance.containerSha256,
      });
      return;
    }

    deny(res, 404, 'ROUTE_NOT_FOUND',
      'no route matches; the server exposes ONLY the compat app allowlist, the pinned three package subtree, /api/status and /api/sceneir/218757 -- arbitrary filesystem paths are not servable BY CONSTRUCTION', rawUrl);
  };
}

// ---------------------------------------------------------------------------
// startup (main guard -- importing this module has no side effects)
// ---------------------------------------------------------------------------
async function verifyThreePin() {
  const pkgRaw = await fsp.readFile(path.join(CONFIG.threeRoot, 'package.json'), 'utf8');
  const pkg = JSON.parse(pkgRaw);
  if (pkg.version !== CONFIG.threePinnedVersion) {
    throw new Error(`three version ${pkg.version} != pinned ${CONFIG.threePinnedVersion} at ${CONFIG.threeRoot} -- REFUSING (retention pin)`);
  }
  return pkg.version;
}

function checkPortFree(port, host) {
  return new Promise((resolve, reject) => {
    const probe = net.createServer();
    probe.once('error', (err) => reject(err));
    probe.listen(port, host, () => probe.close(() => resolve(true)));
  });
}

async function main() {
  const t0 = Date.now();
  // 1. three retention pin (configured private root, version-verified).
  const threeVersion = await verifyThreePin().catch((e) => {
    console.error(`[server-sceneir] THREE PIN FAILURE: ${e.message} -- LOUD FAIL (refusing to start)`);
    process.exit(1);
  });

  // 2. REGENERATE the SceneIR from the pinned container (fail-closed SHA).
  const io = {
    readFile: async (p) => new Uint8Array(await fsp.readFile(p)),
    sha256: (b) => createHash('sha256').update(b).digest('hex'),
  };
  let wire;
  try {
    const adapter = new PecAssetAdapter(io, { modelsBntPath: CONFIG.modelsBntPath });
    const loaded = await adapter.loadModel(CONFIG.modelId);
    wire = buildWireSceneIR(loaded);
    // buildWireSceneIR itself never mutates; sanity: cacheKey must include the
    // payload SHA + adapter/schema version (contract §7 cache-key rule).
    if (!wire.cacheKey.includes(wire.provenance.payloadSha256)) {
      throw new Error('cacheKey does not include the payload SHA -- cache-key contract violated');
    }
  } catch (e) {
    console.error(`[server-sceneir] SCENEIR REGENERATION FAILED_FAIL_CLOSED: ${e.message}`);
    console.error('[server-sceneir] NOTHING IS SERVED. The pinned container/entry identity did not verify.');
    process.exit(1);
  }

  // 3. verified-free-port binding (never replaces another process).
  try {
    await checkPortFree(CONFIG.port, CONFIG.bind);
  } catch (e) {
    console.error(`[server-sceneir] PORT ${CONFIG.port} ON ${CONFIG.bind} IS BUSY (${e.code}) -- LOUD FAIL (this server never replaces a running process; set PORT=<other>)`);
    process.exit(1);
  }

  const startedAt = new Date().toISOString();
  const statusInfo = () => ({
    ok: true,
    run: RUN_ID,
    serverVersion: SERVER_VERSION,
    readOnly: true,
    bind: CONFIG.bind,
    port: CONFIG.port,
    pid: process.pid,
    startedAt,
    three: { version: threeVersion, root: CONFIG.threeRoot, pin: CONFIG.threePinnedVersion },
    sceneir: {
      modelId: CONFIG.modelId,
      cacheKey: wire.cacheKey,
      entryName: wire.provenance.entryName,
      payloadSha256: wire.provenance.payloadSha256,
      containerSha256: wire.provenance.containerSha256,
      adapterLoadElapsedMs: wire.provenance.elapsedMs,
      counts: {
        blocks: wire.blocks.length,
        meshes: wire.meshAssociations.length,
        supported: wire.decodeCensus.SUPPORTED,
        partiallyUnderstood: wire.decodeCensus.PARTIALLY_UNDERSTOOD,
        opaque: wire.decodeCensus.OPAQUE,
      },
    },
    note: 'loopback-only; static surface = fixed allowlists + the pinned three package; data API = the regenerated 218757 SceneIR only; no arbitrary filesystem path endpoint',
  });

  const server = http.createServer(createApp({ wire, statusInfo }));
  server.on('error', (e) => {
    console.error(`[server-sceneir] BIND ERROR on ${CONFIG.bind}:${CONFIG.port}: ${e.message} -- LOUD FAIL`);
    process.exit(1);
  });
  server.listen(CONFIG.port, CONFIG.bind, () => {
    const startupMs = Date.now() - t0;
    console.log(`sceneir server http://127.0.0.1:${CONFIG.port}/ pid=${process.pid}`);
    console.log(`[server-sceneir] ready in ${startupMs} ms -- model ${CONFIG.modelId} regenerated from the pinned container (fail-closed SHA verified; adapter load ${wire.provenance.elapsedMs} ms)`);
    console.log(`[server-sceneir] cacheKey=${wire.cacheKey}`);
    console.log(`[server-sceneir] payloadSha256=${wire.provenance.payloadSha256} containerSha256=${wire.provenance.containerSha256}`);
    console.log(`[server-sceneir] blocks=${wire.blocks.length} meshes=${wire.meshAssociations.length} supported=${wire.decodeCensus.SUPPORTED} partiallyUnderstood=${wire.decodeCensus.PARTIALLY_UNDERSTOOD} opaque=${wire.decodeCensus.OPAQUE}`);
    console.log(`[server-sceneir] three ${threeVersion} from the configured private root; static surface = allowlist maps; STOP = terminate pid ${process.pid}`);
  });
  const shutdown = () => {
    server.close(() => process.exit(0));
    setTimeout(() => process.exit(0), 3000).unref();
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (isMain) {
  main().catch((e) => {
    console.error(`[server-sceneir] UNEXPECTED STARTUP FAILURE: ${e?.stack ?? e}`);
    process.exit(1);
  });
}
