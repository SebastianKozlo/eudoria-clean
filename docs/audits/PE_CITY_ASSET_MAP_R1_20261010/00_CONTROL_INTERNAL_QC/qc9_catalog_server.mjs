// QC9 — catalog server lifecycle + API surface + denial battery (pe-master-auditor fresh internal QC).
// My OWN bounded lifecycle (no executor helpers): spawn server-catalog.mjs on a FREE port
// (never 8140), verify startup regeneration + status coverage, rows paging, the four
// primary preview wire pins, issue 12 synthetic denial requests, stop, verify port freed.
import { spawn } from 'node:child_process';
import net from 'node:net';
import { writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';

const PKG = resolve(process.argv[2]);
const PORT = Number(process.argv[3] || 8188);
const res = { qcStep: 'QC9_CATALOG_SERVER', port: PORT, requests: [], denials: [], wireChecks: [], lifecycle: {} };

function checkPortFree(port) {
  return new Promise((resolveP, reject) => {
    const probe = net.createServer();
    probe.once('error', (e) => reject(e));
    probe.listen(port, '127.0.0.1', () => probe.close(() => resolveP(true)));
  });
}
async function get(path_, method = 'GET') {
  const r = await fetch(`http://127.0.0.1:${PORT}${path_}`, { method });
  const headers = {};
  r.headers.forEach((v, k) => { headers[k] = v; });
  let body = null;
  const text = await r.text();
  try { body = JSON.parse(text); } catch { body = text.slice(0, 400); }
  return { status: r.status, headers, body, bytes: text.length };
}

// start
await checkPortFree(PORT);
const child = spawn(process.execPath, ['compat/server-catalog.mjs'], {
  env: { ...process.env, PECATALOG_PORT: String(PORT) },
  cwd: process.cwd(), stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true,
});
let stdout = '', stderr = '';
child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8');
child.stdout.on('data', (d) => { stdout += d; });
child.stderr.on('data', (d) => { stderr += d; });
res.lifecycle.pid = child.pid;
const deadline = Date.now() + 120000;
let startupLine = null;
while (Date.now() < deadline) {
  const m = /catalog server http:\/\/127\.0\.0\.1:(\d+)\/ pid=(\d+)/.exec(stdout);
  if (m && Number(m[1]) === PORT) { startupLine = m[0]; break; }
  await new Promise((r) => setTimeout(r, 200));
}
res.lifecycle.startupLine = startupLine;
res.lifecycle.startupStdout = stdout.split(/\r?\n/).filter(Boolean).slice(0, 8);

// status
const st = await get('/api/catalog/status');
res.status = {
  httpStatus: st.status,
  coverage: st.body?.coverage ?? null,
  containers: st.body?.containers ? {
    modelsArk: { sha256: st.body.containers['CD_2003_Models_ark']?.sha256, entries: st.body.containers['CD_2003_Models_ark']?.entries, crcMismatch: st.body.containers['CD_2003_Models_ark']?.crc32Mismatch },
    modelsBnt: { sha256: st.body.containers['PCG_9_3_5_Models_bnt']?.sha256, entries: st.body.containers['PCG_9_3_5_Models_bnt']?.entries, crcMismatch: st.body.containers['PCG_9_3_5_Models_bnt']?.crc32Mismatch },
  } : null,
  three: st.body?.three ?? null,
  primaries: st.body?.primaries ?? null,
  overlapSameNameBothEras: st.body?.overlapSameNameBothEras?.count ?? st.body?.overlapSameNameBothEras ?? null,
  readOnly: st.body?.readOnly, bind: st.body?.bind, pid: st.body?.pid
};

// rows paging checks
const p1 = await get('/api/catalog/rows?page=1&pageSize=100');
const p2 = await get('/api/catalog/rows?page=2&pageSize=100');
const p81 = await get('/api/catalog/rows?page=81&pageSize=100');
const pBad = await get('/api/catalog/rows?page=1&pageSize=100&sort=bogus');
res.rowsApi = {
  p1: { status: p1.status, total: p1.body?.total, pageCount: p1.body?.pageCount, rowsReturned: p1.body?.rows?.length, firstRow: p1.body?.rows?.[0] ? { id: p1.body.rows[0].id, entryName: p1.body.rows[0].entryName, size: p1.body.rows[0].sizeBytes ?? p1.body.rows[0].uncompressedSizeBytes } : null, coverage: p1.body?.coverage ? { totalRows: p1.body.coverage.totalRows, byEra: p1.body.coverage.byEra } : null, sortRule: p1.body?.sortRule },
  p2_firstId: p2.body?.rows?.[0]?.entryName ?? p2.body?.rows?.[0]?.id ?? null, p2_rows: p2.body?.rows?.length,
  p81_rows: p81.body?.rows?.length, p81_expectedLastPageRows: p1.body?.total ? p1.body.total - 80 * 100 : null,
  lastRowId: p81.body?.rows?.slice(-1)[0]?.entryName ?? p81.body?.rows?.slice(-1)[0]?.id ?? null,
  badSort: { status: pBad.status, error: pBad.body?.error, message: (pBad.body?.message ?? '').slice(0, 120) }
};
// paging math: p1 first row = rank 1 (largest); page 81 has total-8000 rows
res.rowsApi.pagingMathOk = res.rowsApi.p1.pageCount === 81 && res.rowsApi.p81_rows === (res.rowsApi.p1.total - 8000);

// four primary wire pins
const expectedPins = {
  '192374': '08d80c67bb87caf6a1c00bf8c034e329484e25a6a588da411079bb6f682de8c1',
  '193207': '220f549b311563a1a6506cacefcebb8911ee4770cf72b85f2f635146c111adbb',
  '193313': '02fc860a840e9cdb948f04daff2691bb37baf9e0da8dbadc8f77773c517beef2',
  '193684': '4cc5f9203280c26fc2020bb6c432e2bcf4e5db4ec2f47be3df573e537660901f',
};
const containerSha = 'f660d055b4b9471b3b6e16b07f5368dbd6f2208dab6b51bb9bdb9942bd73ea62';
for (const id of ['192374', '193207', '193313', '193684']) {
  const w = await get(`/api/catalog/model/CD_2003/${id}`);
  const ok = w.status === 200 && w.headers['x-pe-payload-sha256'] === expectedPins[id] && w.headers['x-pe-container-sha256'] === containerSha;
  res.wireChecks.push({
    id, httpStatus: w.status,
    headerPayloadSha256: w.headers['x-pe-payload-sha256'],
    headerContainerSha256: w.headers['x-pe-container-sha256'],
    bodyPayloadSha256: w.body?.provenance?.payloadSha256 ?? null,
    bodyHasMeshes: Array.isArray(w.body?.meshes) || Array.isArray(w.body?.parts),
    pinOk: ok
  });
}

// 12 synthetic denials
const denials = [
  ['non-primary CD id', '/api/catalog/model/CD_2003/101411'],
  ['real non-previewable entry 65678', '/api/catalog/model/CD_2003/65678'],
  ['PCG id (no preview route by design)', '/api/catalog/model/PCG_9_3_5/218757'],
  ['malformed model route (3 parts)', '/api/catalog/model/CD_2003/193313/extra'],
  ['unallowlisted compat static (app.js)', '/compat/app.js'],
  ['server-side module not routed', '/src/pecompat/ArkArchive.js'],
  ['three traversal', '/node_modules/three/../package.json'],
  ['encoded traversal in compat', '/compat/%2e%2e/server-catalog.mjs'],
  ['backslash in URL', '/api%5c/secret'],
  ['unknown route (root)', '/api/sceneir/status'],
  ['bogus sort metric', '/api/catalog/rows?sort=bogus'],
  ['POST method', '/api/catalog/rows'],
];
for (const [name, path_] of denials) {
  const r = await get(path_, path_ === '/api/catalog/rows' && name === 'POST method' ? 'POST' : 'GET');
  res.denials.push({
    name, path: path_, method: path_ === '/api/catalog/rows' && name === 'POST method' ? 'POST' : 'GET',
    status: r.status, error: r.body?.error ?? null,
    refused: r.status >= 400,
    bodyIsJsonWithNamedError: typeof r.body === 'object' && r.body !== null && typeof r.body.error === 'string'
  });
}

// stop + port freed
const stopT0 = Date.now();
child.kill();
let exitInfo = null;
await Promise.race([
  new Promise((r2) => child.once('exit', (c, s) => { exitInfo = { code: c, signal: s }; r2(); })),
  new Promise((r2) => setTimeout(() => { exitInfo = { code: null, signal: 'TIMEOUT' }; r2(); }, 10000)),
]);
let portFreed = false, freedAfterMs = null;
const freeDeadline = Date.now() + 15000;
while (Date.now() < freeDeadline) {
  try { await checkPortFree(PORT); portFreed = true; freedAfterMs = Date.now() - stopT0; break; } catch { /* still bound */ }
  await new Promise((r2) => setTimeout(r2, 250));
}
res.lifecycle.stop = { exit: exitInfo, portFreed, freedAfterMs, stderrTail: stderr.slice(-400) };

writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC', 'QC9_CATALOG_SERVER.json'), JSON.stringify(res, null, 1));
console.log(JSON.stringify({
  startupLine: res.lifecycle.startupLine, pid: res.lifecycle.pid,
  statusCoverage: { totalRows: res.status.coverage?.totalRows, byEra: res.status.coverage?.byEra, extentMeasured: res.status.coverage?.sceneExtent?.measured, extentUnknown: res.status.coverage?.sceneExtent?.unknown, byDecodeCoverage: res.status.coverage?.byDecodeCoverage },
  rowsPagingOk: res.rowsApi.pagingMathOk, p1_firstRow: res.rowsApi.p1.firstRow,
  wireOk: res.wireChecks.every(w => w.pinOk),
  denialsRefused: res.denials.filter(d => d.refused && d.bodyIsJsonWithNamedError).length + '/' + res.denials.length,
  deniedErrors: res.denials.map(d => `${d.name}: ${d.status}/${d.error}`),
  stop: res.lifecycle.stop
}, null, 1));
