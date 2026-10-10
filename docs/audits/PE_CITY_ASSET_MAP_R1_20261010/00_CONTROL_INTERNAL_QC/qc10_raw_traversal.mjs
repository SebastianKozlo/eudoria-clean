// QC10 — RAW-socket traversal probes (no URL normalization — exercises the
// server-side jail directly) + catalog.html marker presence check.
import net from 'node:net';
import { writeFileSync, readFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const PKG = resolve(process.argv[2]);
const PORT = Number(process.argv[3] || 8199);
const res = { qcStep: 'QC10_RAW_TRAVERSAL_PROBES', port: PORT, probes: [] };

function rawProbe(rawRequestLine, timeoutMs = 8000) {
  return new Promise((resolveP) => {
    const sock = net.connect({ host: '127.0.0.1', port: PORT }, () => {
      sock.write(rawRequestLine + ' HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n');
    });
    let data = '';
    sock.setEncoding('utf8');
    sock.on('data', (d) => { data += d; });
    const t = setTimeout(() => { sock.destroy(); resolveP({ status: null, body: data.slice(0, 500), timedOut: true }); }, timeoutMs);
    sock.on('close', () => { clearTimeout(t); resolveP({ status: data.split(' ')[1] ?? null, body: data.slice(0, 600), timedOut: false }); });
    sock.on('error', (e) => { clearTimeout(t); resolveP({ status: null, body: String(e), error: true }); });
  });
}

// start server
const { spawn } = await import('node:child_process');
const { checkPortFree } = await import('file://' + join(PKG, '..', '..', '..', 'tests', 'pecompat', '_app_server_helpers.mjs').replace(/\\/g, '/'));
try { await checkPortFree(PORT); } catch { res.fatal = 'port busy'; }
const child = spawn(process.execPath, ['compat/server-catalog.mjs'], {
  env: { ...process.env, PECATALOG_PORT: String(PORT) }, cwd: process.cwd(), stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true,
});
let stdout = ''; child.stdout.setEncoding('utf8'); child.stdout.on('data', (d) => { stdout += d; });
const dl = Date.now() + 120000;
while (Date.now() < dl && !/catalog server http:\/\/127\.0\.0\.1:\d+\/ pid=\d+/.test(stdout)) await new Promise((r) => setTimeout(r, 200));
res.serverUp = /catalog server http:\/\/127\.0\.0\.1:\d+\/ pid=\d+/.test(stdout);

// raw traversal probes — the client (net socket) cannot normalize these
const probes = [
  ['GET /compat/../package.json'],
  ['GET /compat/..%2Fpackage.json'],
  ['GET /node_modules/three/../server-catalog.mjs'],
  ['GET /node_modules/three/%2e%2e/package.json'],
  ['GET /%2e%2e/package.json'],
  ['GET /api/catalog/model/CD_2003/193313?x=1&sort=notametric'],
];
for (const [line] of probes) {
  const r = await rawProbe(line);
  let errorName = null;
  const m = /"error"\s*:\s*"([^"]+)"/.exec(r.body);
  if (m) errorName = m[1];
  res.probes.push({ request: line, status: r.status, error: errorName, refused: r.status !== null && Number(r.status) >= 400, excerpt: (m ? '' : r.body.slice(0, 200)) });
}

// stop
child.kill();
await new Promise((r) => setTimeout(r, 800));

// catalog.html markers (for the browser gate conjuncts)
const html = readFileSync(join(PKG, '..', '..', '..', 'compat', 'catalog.html'), 'utf8');
res.catalogHtmlMarkers = {
  hasViewCanvas: html.includes('id="view-canvas"'),
  hasDiagnostics: html.includes('id="diagnostics"'),
  hasDataLoadStatus: html.includes('data-load-status'),
  dataLoadStatusValues: [...html.matchAll(/data-load-status="([^"]*)"/g)].map((m) => m[1]).slice(0, 8),
  title: /<title>([^<]*)<\/title>/.exec(html)?.[1] ?? null
};

writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC', 'QC10_RAW_TRAVERSAL.json'), JSON.stringify(res, null, 1));
console.log(JSON.stringify({ serverUp: res.serverUp, probes: res.probes.map(p => `${p.request} -> ${p.status}/${p.error} refused=${p.refused}`), markers: res.catalogHtmlMarkers }, null, 1));
