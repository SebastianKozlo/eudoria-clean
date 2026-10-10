#!/usr/bin/env node
// server-catalog.mjs -- PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W5, contract §5)
// THE /catalog bounded LOOPBACK server.
//
// DESIGN (path denial BY CONSTRUCTION — EXTENDS the proven
// compat/server-sceneir.mjs design of the predecessor SceneIR run; REUSE
// LABEL: same deny()/serveBytes() shape, same exact-allowlist static maps,
// same jailed three-subtree reader, same verified-free-port + fail-closed
// startup pattern, same GET/HEAD-only surface. NOT a fork: the sceneir server
// stays byte-identical and untouched; this server serves ONLY the catalog
// app + the bounded catalog APIs):
//   - Binds 127.0.0.1 ONLY (loopback; the bind address is not configurable).
//   - PORT: env PECATALOG_PORT || env PORT || default 8161. Port 8140 is
//     REFUSED EXPLICITLY (the foreign standing reference server owns it and
//     is NEVER touched or replaced). A busy port is a LOUD failure.
//   - Static surface = EXACT ALLOWLIST MAPS (the request URL never becomes a
//     filesystem path): the catalog app files, the shared compat stylesheet,
//     the two client-needed src/pecompat modules, and the configured
//     three-package private root (jailed subtree).
//   - Data APIs (all index-derived, metadata-only):
//       GET /api/catalog/status  — identity/coverage/cache snapshot
//       GET /api/catalog/rows    — sorted/filtered/searched rows (paged)
//       GET /api/catalog/model/CD_2003/<id> — the bounded PREVIEW WIRE for
//         exactly the FOUR pinned primaries (lazy build + identity-keyed
//         cache). Any other id: DENIED_EXPLICIT with the honest decode state
//         of that entry (CATALOG_ONLY / VERSION_GATED / FAILED — no fake
//         preview). PCG_9_3_5 has NO preview route in this app by design.
//   - The containers and arbitrary source trees are NOT exposed: no route can
//     reach them. No whole-corpus static route exists BY CONSTRUCTION.
//   - Read-only: GET/HEAD only; other methods get 405.
//
// START:  node compat/server-catalog.mjs          (env PECATALOG_PORT, default 8161)
// STOP:   terminate the printed PID (Ctrl+C in the owning console, or
//         Stop-Process -Id <PID> / child.kill() from a harness).
// The startup line is:  catalog server http://127.0.0.1:<PORT>/ pid=<PID>
//
// IMPORT-SAFE for tests: this module only starts the server when executed as
// the main script; importing { createCatalogApp, buildStatusInfo, ... } has no
// side effects.

'use strict';
import http from 'node:http';
import net from 'node:net';
import path from 'node:path';
import { promises as fsp } from 'node:fs';
import { fileURLToPath } from 'node:url';

import {
  buildCatalogData, sortRows, filterRows, buildPrimaryWire,
  CATALOG_PINS, PRIMARY_IDS, PRIMARY_PINS, SORT_RULE_LABEL, CATALOG_DATA_VERSION,
} from '../tools/pecompat/catalog_data.mjs';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url))); // repo root
const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';
const SERVER_VERSION = 'catalog-server-r1 (loopback, allowlist statics, regenerated catalog API; extends the sceneir server design)';

// ---- configured roots (the ONLY filesystem roots this server may read) ----
const FOREIGN_REFERENCE_PORT = 8140; // the standing sceneir reference server — NEVER bound over
const CONFIG = {
  bind: '127.0.0.1',
  port: Number(process.env.PECATALOG_PORT) || Number(process.env.PORT) || 8161,
  threeRoot: process.env.PECOMPAT_THREE_ROOT ||
    'D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\node_modules\\three',
  threePinnedVersion: '0.185.0',
  logRequests: process.env.CATALOG_LOG_REQUESTS === '1',
};

const PRIV_DEFAULT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_CITY_ASSET_MAP_R1_20261010';

// EXACT static allowlists (request URL -> fixed repo file; no user-derived path).
const CATALOG_FILES = Object.freeze({
  'index.html': 'compat/catalog.html',
  'catalog-app.js': 'compat/catalog-app.js',
  'catalog-table.js': 'compat/catalog-table.js',
  'catalog-preview.js': 'compat/catalog-preview.js',
  'catalog.css': 'compat/catalog.css',
  'compat.css': 'compat/compat.css',
});
// The two client-needed src/pecompat modules (client-side composition +
// transform helpers — the same reuse as the sceneir app). The extraction
// chain (ArkArchive/Bnt2Archive/nif41_deep/catalog_data) is SERVER-SIDE and
// deliberately NOT publicly routed.
const PEC_MODULES = Object.freeze(['PecTransform.js', 'PecSceneIR.js']);

const MIME = {
  '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.html': 'text/html', '.json': 'application/json', '.css': 'text/css',
  '.map': 'application/json', '.txt': 'text/plain',
};

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

/** Jail-checked read inside the configured three package root (REUSE: the
 * sceneir server's proven readThreeSub design). Returns {bytes} |
 * {denyStatus, denyError, denyMessage} — never an escape. */
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

/** Parse the /api/catalog/rows querystring (era/status/q/sort/page/pageSize).
 * Unknown filter values -> null (caller maps to a 400 DENIED_EXPLICIT). */
function parseRowsQuery(rawUrl) {
  const qs = rawUrl.split('?')[1] ?? '';
  const out = {};
  for (const pair of qs.split('&')) {
    if (!pair) continue;
    const eq = pair.indexOf('=');
    const k = eq < 0 ? pair : pair.slice(0, eq);
    const v = eq < 0 ? '' : pair.slice(eq + 1);
    out[decodeURIComponent(k)] = decodeURIComponent(v);
  }
  return out;
}

/** createCatalogApp — the request handler (exported for tests).
 * state = { data, statusInfo, wireCache } */
export function createCatalogApp(state) {
  const { data, statusInfo, wireCache } = state;
  const logRequests = CONFIG.logRequests;
  return async function handle(req, res) {
    if (logRequests) {
      res.on('finish', () => console.log(`[req] ${req.method} ${req.url} -> ${res.statusCode}`));
    }
    const rawUrl = req.url;
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
    if (urlPath === '/' || urlPath === '/catalog' || urlPath === '/catalog/'
        || urlPath === '/catalog/index.html' || urlPath === '/index.html') {
      const b = await readRepoFile(CATALOG_FILES['index.html']);
      serveBytes(res, 200, b, 'text/html');
      return;
    }
    if (urlPath.startsWith('/compat/')) {
      const key = urlPath.slice('/compat/'.length);
      const rel = CATALOG_FILES[key];
      if (!rel) {
        deny(res, 404, 'STATIC_FILE_NOT_ALLOWEDLISTED',
          `"${key}" is not in the catalog allowlist (fixed file set: ${Object.keys(CATALOG_FILES).join(', ')})`, rawUrl);
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
          `"${name}" is not in the client module allowlist (${PEC_MODULES.join(', ')}); the server-side extraction chain (ArkArchive/Bnt2Archive/nif41_deep/catalog_data) is not publicly routed`, rawUrl);
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

    // ---- bounded catalog APIs ----
    if (urlPath === '/api/catalog/status') {
      const body = Buffer.from(JSON.stringify(statusInfo(), null, 1) + '\n');
      serveBytes(res, 200, body, 'application/json');
      return;
    }
    if (urlPath === '/api/catalog/rows') {
      let q;
      try {
        q = parseRowsQuery(rawUrl);
      } catch {
        deny(res, 400, 'MALFORMED_QUERY', 'query parsing failed', rawUrl);
        return;
      }
      const era = q.era ?? 'ALL';
      const status = q.status ?? 'ALL';
      const search = q.q ?? '';
      const sort = q.sort ?? 'size';
      const page = Math.max(1, parseInt(q.page ?? '1', 10) || 1);
      const pageSize = Math.min(500, Math.max(1, parseInt(q.pageSize ?? '100', 10) || 100));
      let rows;
      try {
        rows = filterRows(data.rows, { era, status, q: search });
      } catch (e) {
        deny(res, 400, 'DENIED_EXPLICIT', String(e?.message ?? e), rawUrl);
        return;
      }
      let sorted;
      try {
        sorted = sortRows(rows, { metric: sort });
      } catch (e) {
        deny(res, 400, 'DENIED_EXPLICIT', `unknown sort metric "${sort}" (allowed: size, extent, triangles, vertices, shapes)`, rawUrl);
        return;
      }
      const total = sorted.length;
      const pageCount = Math.max(1, Math.ceil(total / pageSize));
      const slice = sorted.slice((page - 1) * pageSize, (page - 1) * pageSize + pageSize);
      const body = Buffer.from(JSON.stringify({
        ok: true,
        sortRule: SORT_RULE_LABEL,
        sort, era, status, q: search, page, pageSize, pageCount, total,
        coverage: data.coverage,
        rows: slice,
      }) + '\n');
      serveBytes(res, 200, body, 'application/json');
      return;
    }
    if (urlPath.startsWith('/api/catalog/model/')) {
      const rest = urlPath.slice('/api/catalog/model/'.length).replace(/\.json$/, '');
      const parts = rest.split('/');
      const [era, idRaw] = parts;
      if (parts.length !== 2 || era !== 'CD_2003' || !/^\d+$/.test(idRaw)) {
        deny(res, 404, 'UNKNOWN_ASSET_ROUTE',
          `the model route serves ONLY /api/catalog/model/CD_2003/<primary-id> (the four pinned primaries); got "${rest}"`, rawUrl);
        return;
      }
      const id = idRaw;
      if (!PRIMARY_IDS.includes(id)) {
        // honest decode state of the requested entry (no fake preview)
        const row = data.rows.find((r) => r.era === 'CD_2003' && r.id === Number(id))
          ?? data.rows.find((r) => r.entryName === `${id}.nif` && r.era === 'CD_2003');
        deny(res, 404, 'PREVIEW_NOT_ESTABLISHED',
          `no safe import established for CD_2003 ${id}.nif in this run — preview is available ONLY for the four pinned primaries (${PRIMARY_IDS.join(', ')}). Honest state: ${row ? row.decodeCoverage : 'entry not found in the CD_2003 catalog'} (${row ? row.decodeReason : 'the entry does not exist in the regenerated index'}). CATALOG_ONLY/UNSUPPORTED/VERSION_GATED states are shown, never faked.`, rawUrl);
        return;
      }
      const cacheKey = `catalog-wire-v1|CD_2003|${PRIMARY_PINS[id].sha256}`;
      let wire = wireCache.get(cacheKey);
      if (!wire) {
        const primary = data.primaries[id];
        wire = buildPrimaryWire(primary, id);
        wireCache.set(cacheKey, wire); // identity-keyed lazy cache (era+container+entry+payload+reader+wire version)
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
      'no route matches; this server exposes ONLY the catalog app allowlist, the pinned three package subtree, /api/catalog/status, /api/catalog/rows and /api/catalog/model/CD_2003/<primary-id> -- arbitrary filesystem paths and the SceneIR API are not servable BY CONSTRUCTION (the 218757 SceneIR app is served by its own server)', rawUrl);
  };
}

// ---------------------------------------------------------------------------
// startup (main guard — importing this module has no side effects)
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

export function buildStatusInfo(data, { threeVersion, startedAt, elapsed }) {
  return () => ({
    ok: true,
    run: RUN_ID,
    serverVersion: SERVER_VERSION,
    readOnly: true,
    bind: CONFIG.bind,
    port: CONFIG.port,
    pid: process.pid,
    startedAt,
    dataVersion: CATALOG_DATA_VERSION,
    three: { version: threeVersion, root: CONFIG.threeRoot, pin: CONFIG.threePinnedVersion },
    containers: {
      'CD_2003_Models_ark': {
        path: CATALOG_PINS.modelsArk.path, sizeBytes: CATALOG_PINS.modelsArk.sizeBytes,
        sha256: CATALOG_PINS.modelsArk.sha256, pin: 'MATCH (verified fail-closed at startup)',
        entries: data.containers.CD_2003_Models_ark.entries,
        crc32Verified: data.containers.CD_2003_Models_ark.crc32Verified,
        crc32Mismatch: data.containers.CD_2003_Models_ark.crc32Mismatch,
      },
      'PCG_9_3_5_Models_bnt': {
        path: CATALOG_PINS.modelsBnt.path, sizeBytes: CATALOG_PINS.modelsBnt.sizeBytes,
        sha256: CATALOG_PINS.modelsBnt.sha256,
        pin: 'MATCH (REQUIRED pin — contract §1 — verified fail-closed at load)',
        entries: data.containers.PCG_9_3_5_Models_bnt.entries,
        crc32Verified: data.containers.PCG_9_3_5_Models_bnt.crc32Verified,
        crc32Mismatch: data.containers.PCG_9_3_5_Models_bnt.crc32Mismatch,
      },
    },
    textureContainers: {
      note: 'NOT loaded by this server (bounded startup): texture coverage comes from the identity-keyed phase-3 measured cache (era + container SHA + entry + payload SHA); the Textures containers are pinned in the report package INPUT_IDENTITIES.json',
    },
    coverage: data.coverage,
    overlapSameNameBothEras: data.overlap,
    primaries: {
      ids: PRIMARY_IDS,
      previewable: PRIMARY_IDS.length,
      decodeCoverage: 'DECODED_FULL_CLOSURE (live decode at startup via the phase-3 bounded NIF-4.1 reader)',
    },
    cache: data.cache,
    sortRule: SORT_RULE_LABEL,
    elapsedMs: elapsed,
    note: 'loopback-only; static surface = fixed allowlists + the pinned three package; data APIs = index-derived catalog metadata + the four primary preview wires (lazy, identity-keyed); no arbitrary filesystem path endpoint, no whole-corpus route',
  });
}

async function main() {
  const t0 = Date.now();
  if (CONFIG.port === FOREIGN_REFERENCE_PORT) {
    console.error(`[server-catalog] PORT ${FOREIGN_REFERENCE_PORT} REFUSED — that port belongs to the foreign standing reference server (never touched, never replaced). Set PECATALOG_PORT=<other>.`);
    process.exit(1);
  }
  // 1. three retention pin (configured private root, version-verified).
  const threeVersion = await verifyThreePin().catch((e) => {
    console.error(`[server-catalog] THREE PIN FAILURE: ${e.message} -- LOUD FAIL (refusing to start)`);
    process.exit(1);
  });

  // 2. REGENERATE the catalog data from the pinned originals (fail-closed
  //    container identity incl. the REQUIRED Models.bnt pin).
  let data;
  try {
    data = await buildCatalogData({
      batchStatePath: process.env.PECATALOG_BATCH_STATE ?? `${PRIV_DEFAULT}\\PHASE2_EXTENT\\PCG935_NIF10_BATCH_STATE.jsonl`,
      nameEdgesPath: process.env.PECATALOG_NAME_EDGES ?? `${PRIV_DEFAULT}\\PHASE3_PCG935_BATCH\\PCG935_NAME_EDGES.jsonl`,
    });
  } catch (e) {
    console.error(`[server-catalog] CATALOG REGENERATION FAILED_FAIL_CLOSED: ${e.message}`);
    console.error('[server-catalog] NOTHING IS SERVED. A pinned container identity did not verify.');
    process.exit(1);
  }
  // after the build the raw container buffers are no longer referenced —
  // only rows + the four pin-verified primary payloads remain (GC reclaims
  // the ~520 MB of container bytes; the server stays light).
  const wireCache = new Map();

  // 3. verified-free-port binding (never replaces another process).
  try {
    await checkPortFree(CONFIG.port, CONFIG.bind);
  } catch (e) {
    console.error(`[server-catalog] PORT ${CONFIG.port} ON ${CONFIG.bind} IS BUSY (${e.code}) -- LOUD FAIL (this server never replaces a running process; set PECATALOG_PORT=<other>)`);
    process.exit(1);
  }

  const startedAt = new Date().toISOString();
  const statusInfo = buildStatusInfo(data, { threeVersion, startedAt, elapsed: Date.now() - t0 });
  const state = { data, statusInfo, wireCache };
  const server = http.createServer(createCatalogApp(state));
  server.on('error', (e) => {
    console.error(`[server-catalog] BIND ERROR on ${CONFIG.bind}:${CONFIG.port}: ${e.message} -- LOUD FAIL`);
    process.exit(1);
  });
  server.listen(CONFIG.port, CONFIG.bind, () => {
    const startupMs = Date.now() - t0;
    console.log(`catalog server http://127.0.0.1:${CONFIG.port}/ pid=${process.pid}`);
    console.log(`[server-catalog] ready in ${startupMs} ms — catalog regenerated from the pinned originals (fail-closed SHAs; rows ${data.coverage.totalRows} = CD_2003 ${data.coverage.byEra.CD_2003} + PCG_9_3_5 ${data.coverage.byEra.PCG_9_3_5})`);
    console.log(`[server-catalog] coverage: extent measured ${data.coverage.sceneExtent.measured}/${data.coverage.totalRows}; decode ${JSON.stringify(data.coverage.byDecodeCoverage)}`);
    console.log(`[server-catalog] same-name-both-eras census: ${data.overlap.count} names (era-separated by construction)`);
    console.log(`[server-catalog] four primaries DECODED_FULL_CLOSURE + previewable; three ${threeVersion} from the configured private root; STOP = terminate pid ${process.pid}`);
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
    console.error(`[server-catalog] UNEXPECTED STARTUP FAILURE: ${e?.stack ?? e}`);
    process.exit(1);
  });
}
