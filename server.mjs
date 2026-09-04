// server.mjs — static file server for the eudoria-clean runtime (ITER 019).
// Serves the repo root so that ES-module import maps can reference
// /node_modules/three/... directly. Read-only on originals: the runtime
// fetches original PE containers from ABSOLUTE paths exposed explicitly
// via /pcg/... aliases (see ALIASES) — never writes.
//
// Port 8130 (new; 8124/8126 belong to legacy eudoria-web servers).
'use strict';
import http from 'node:http';
import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const PORT = 8130;

// Explicit, era-labeled, read-only aliases into the original corpora.
// PCG_9_3_5 primary reference (ledger ENTRY #6): pcg_install.
const ALIASES = {
  '/pcg/': 'D:/Eudoria_Reconstruction/pcg_install/',
  '/jul/': 'C:/Entropia Universe/Data/',
};

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

server.listen(PORT, '127.0.0.1', () => {
  console.log(`eudoria-clean server http://127.0.0.1:${PORT}/ pid=${process.pid}`);
});
