// server.mjs — static file server for the eudoria-clean runtime (ITER 019).
// Serves the repo root so that ES-module import maps can reference
// /node_modules/three/... directly. Read-only on originals: the runtime
// fetches original PE containers from ABSOLUTE paths exposed explicitly
// via /pcg/... aliases (see ALIASES) — never writes.
//
// Port: env PORT override, default 8140 (W03 ISO_TERRAIN_VERTICAL_SLICE
// contract; 8141 fallback if occupied — chosen port is written to the lease).
// 8130/8132 were earlier ITER session servers; 8000/8124/8126 belong to
// legacy eudoria-web servers.
//
// W03: exact route '/iso/50.bnt' serves the RECOVERED PE 5.1.0.0 ISO
// (PC Gamer Nov2003) terrain container, read-only, SHA-pinned by the page.
// This is the ONLY /iso/... route (allowlist — no directory under /iso/).
'use strict';
import http from 'node:http';
import { promises as fs, writeFileSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const BASE_PORT = Number(process.env.PORT) || 8140;
const FALLBACK_PORT = 8141;

// W03 exact-file routes: URL -> absolute original path (READ-ONLY allowlist).
// Sanitized (PATH_INCIDENT root cause fix): no hardcoded private absolute
// paths. Routes are supplied via env SERVER_EXACT_ROUTES as a JSON object
// mapping URL path -> absolute file path (read-only, exact-file semantics,
// no directory traversal). Empty default when the env var is not set.
const EXACT_ROUTES = (() => {
  try {
    return JSON.parse(process.env.SERVER_EXACT_ROUTES || '{}');
  } catch (e) {
    console.error('SERVER_EXACT_ROUTES parse failed (using empty map):', e.message);
    return {};
  }
})();
// Server lease (pid/exe/start/port/stop) — env override, default local file.
// Sanitized: no hardcoded private absolute path (PATH_INCIDENT root cause).
const LEASE_PATH = process.env.SERVER_LEASE_PATH || process.env.LEASE_PATH ||
  './server_lease.json';

// Explicit, era-labeled, read-only aliases into the original corpora.
// Sanitized: supplied via env SERVER_ALIASES as a JSON object mapping
// URL prefix -> absolute directory path. Empty default when not set.
const ALIASES = (() => {
  try {
    return JSON.parse(process.env.SERVER_ALIASES || '{}');
  } catch (e) {
    console.error('SERVER_ALIASES parse failed (using empty map):', e.message);
    return {};
  }
})();

const MIME = {
  '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.html': 'text/html', '.json': 'application/json',
  '.css': 'text/css', '.txt': 'text/plain',
  '.bnt': 'application/octet-stream', '.dat': 'application/octet-stream',
  '.tdf': 'application/octet-stream', '.tga': 'application/octet-stream',
};

const server = http.createServer(async (req, res) => {
  try {
    let urlPath = decodeURIComponent(req.url.split('?')[0]);
    if (urlPath.endsWith('/')) urlPath += 'index.html';
    // W03 exact-file allowlist FIRST (no prefix semantics, no traversal).
    if (Object.prototype.hasOwnProperty.call(EXACT_ROUTES, urlPath)) {
      const data = await fs.readFile(EXACT_ROUTES[urlPath]);
      res.writeHead(200, {
        'Content-Type': 'application/octet-stream',
        'Cache-Control': 'no-store',
        'Content-Length': data.length,
      });
      res.end(data);
      return;
    }
    let fsPath = null;
    for (const [alias, target] of Object.entries(ALIASES)) {
      if (urlPath.startsWith(alias)) {
        fsPath = target + urlPath.slice(alias.length);
        break;
      }
    }
    if (!fsPath) {
      // serve from repo root; block path traversal
      const rel = path.normalize(urlPath).replace(/^([/\\]+)*/, '');
      const abs = path.join(ROOT, rel);
      if (!abs.startsWith(ROOT)) { res.writeHead(403); res.end('forbidden'); return; }
      fsPath = abs;
    }
    const data = await fs.readFile(fsPath);
    res.writeHead(200, {
      'Content-Type': MIME[path.extname(fsPath).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-store',
      'Content-Length': data.length,
    });
    res.end(data);
  } catch (err) {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end(`not found: ${req.url}`);
  }
});

server.on('error', (err) => {
  if (err.code === 'EADDRINUSE' && server.portAttempts === 0) {
    server.portAttempts = 1;
    server.listen(FALLBACK_PORT, '127.0.0.1');
  } else {
    console.error('server error:', err.message);
    process.exit(1);
  }
});

function writeLease(port) {
  const lease = {
    job: 'W03_ISO_TERRAIN_VERTICAL_SLICE',
    pid: process.pid,
    exe: process.execPath,
    startedUtc: new Date().toISOString(),
    port,
    bind: '127.0.0.1',
    command: 'node server.mjs',
    stop: `Stop-Process -Id ${process.pid}`,
    route: EXACT_ROUTES,
  };
  try {
    mkdirSync(path.dirname(LEASE_PATH), { recursive: true });
    writeFileSync(LEASE_PATH, JSON.stringify(lease, null, 2) + '\n');
    console.log(`lease written: ${LEASE_PATH}`);
  } catch (e) {
    console.error('lease write FAILED (non-fatal):', e.message);
  }
}

server.portAttempts = 0;
server.listen(BASE_PORT, '127.0.0.1', () => {
  const addr = server.address();
  writeLease(addr.port);
  console.log(`eudoria-clean server http://127.0.0.1:${addr.port}/ pid=${process.pid}`);
});
