// QC11 — REAL headless-browser /catalog load through the FIXED 5-conjunct gate
// + one PIXEL screenshot spot-check (PNG -> PRIVATE_OUTPUT only; metadata here).
import { spawn } from 'node:child_process';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import fs from 'node:fs';
import { createHash } from 'node:crypto';
import { writeFileSync } from 'node:fs';
import { resolve, join } from 'node:path';
// the PRODUCTION gate predicate (fixed per SCENEIR-T9-C1) — imported, not reimplemented:
import { evaluateLoadGate } from '../../../../tests/pecompat/headless_load.test.mjs';

const PKG = resolve(process.argv[2]);
const PRIV = process.argv[3];
const PORT = Number(process.argv[4] || 8197);
const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const res = { qcStep: 'QC11_REAL_BROWSER_CATALOG_LOAD', port: PORT };

function checkPortFree(port) {
  return new Promise((resolveP, reject) => {
    const probe = net.createServer();
    probe.once('error', (e) => reject(e));
    probe.listen(port, '127.0.0.1', () => probe.close(() => resolveP(true)));
  });
}
// start server
await checkPortFree(PORT);
const child = spawn(process.execPath, ['compat/server-catalog.mjs'], {
  env: { ...process.env, PECATALOG_PORT: String(PORT) }, cwd: process.cwd(), stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true,
});
let srvOut = ''; child.stdout.setEncoding('utf8'); child.stdout.on('data', (d) => { srvOut += d; });
const dl = Date.now() + 120000;
while (Date.now() < dl && !new RegExp(`catalog server http://127\\.0\\.0\\.1:${PORT}/ pid=\\d+`).test(srvOut)) await new Promise((r) => setTimeout(r, 200));
res.serverStartupLine = (new RegExp(`catalog server http://127\\.0\\.0\\.1:${PORT}/ pid=\\d+`).exec(srvOut) || [null])[0];
res.serverPid = child.pid;

// headless DOM capture (bounded 90 s)
async function dumpDom(url) {
  return new Promise((resolveP) => {
    const profile = path.join(os.tmpdir(), 'opencode', `pec-qc-catalog-${Date.now()}`);
    const args = ['--headless=new', `--user-data-dir=${profile}`, '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--disable-background-networking', '--virtual-time-budget=30000', '--dump-dom', url];
    const c = spawn(EDGE, args, { stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true });
    let dom = ''; c.stdout.setEncoding('utf8'); c.stdout.on('data', (d) => { dom += d; });
    const t0 = Date.now();
    const timer = setTimeout(() => { c.kill(); resolveP({ domText: dom, exitCode: null, elapsedMs: Date.now() - t0, timedOut: true }); }, 90000);
    c.once('exit', (code) => { clearTimeout(timer); resolveP({ domText: dom, exitCode: code, elapsedMs: Date.now() - t0, timedOut: false }); });
  });
}
const load = await dumpDom(`http://127.0.0.1:${PORT}/catalog`);
const gate = evaluateLoadGate({ exitCode: load.exitCode, domText: load.domText });
res.tableLoad = {
  exitCode: load.exitCode, domBytes: gate.domBytes, timedOut: load.timedOut,
  conjuncts: gate.conjuncts, missing: gate.missing, loadStatus: gate.loadStatus,
  gatePassed: gate.passed,
  domExcerptHasRows: load.domText.includes('CD_2003') && load.domText.includes('PCG_9_3_5')
};

// pixel screenshot -> PRIVATE_OUTPUT only
const shotPath = join(PRIV, 'PIXEL_RENDER_CATALOG', 'QC_FRESH_CATALOG_TABLE.png');
await new Promise((resolveP) => {
  const profile = path.join(os.tmpdir(), 'opencode', `pec-qc-catalog-shot-${Date.now()}`);
  const args = ['--headless=new', `--user-data-dir=${profile}`, '--no-first-run', '--window-size=1280,800', '--virtual-time-budget=30000', `--screenshot=${shotPath}`, `http://127.0.0.1:${PORT}/catalog`];
  const c = spawn(EDGE, args, { stdio: 'ignore', windowsHide: true });
  // poll for file write + size stability; kill after stability (measured Edge quirk: may not exit)
  const t0 = Date.now(); let lastSize = -1, stable = 0;
  const iv = setInterval(() => {
    try { const st = fs.statSync(shotPath); if (st.size === lastSize && st.size > 0) { stable++; if (stable >= 3) { clearInterval(iv); c.kill(); resolveP({ bytes: st.size, waitedMs: Date.now() - t0 }); } else lastSize = st.size; } else { lastSize = st.size; stable = 0; } } catch { /* not yet */ }
    if (Date.now() - t0 > 90000) { clearInterval(iv); c.kill(); resolveP({ bytes: fs.existsSync(shotPath) ? fs.statSync(shotPath).size : 0, waitedMs: Date.now() - t0, timedOut: true }); }
  }, 500);
});
const shotBytes = fs.readFileSync(shotPath);
res.pixelScreenshot = {
  path: shotPath, bytes: shotBytes.length, sha256: createHash('sha256').update(shotBytes).digest('hex'),
  signature: shotBytes.subarray(1, 4).toString('latin1') === 'PNG' ? 'PNG' : 'NOT_PNG'
};

// stop server + port freed
const stopT0 = Date.now();
child.kill();
let stopped = false;
await Promise.race([new Promise((r) => child.once('exit', () => { stopped = true; r(); })), new Promise((r) => setTimeout(r, 10000))]);
let freed = false, freedAfterMs = null;
const fdl = Date.now() + 15000;
while (Date.now() < fdl) { try { await checkPortFree(PORT); freed = true; freedAfterMs = Date.now() - stopT0; break; } catch { await new Promise((r) => setTimeout(r, 250)); } }
res.lifecycle = { stopped, portFreed: freed, freedAfterMs };

writeFileSync(join(PKG, '00_CONTROL_INTERNAL_QC', 'QC11_BROWSER_LOAD.json'), JSON.stringify(res, null, 1));
console.log(JSON.stringify({ startup: res.serverStartupLine, gatePassed: res.tableLoad.gatePassed, conjuncts: res.tableLoad.conjuncts, loadStatus: res.tableLoad.loadStatus, domBytes: res.tableLoad.domBytes, domHasBothEras: res.tableLoad.domExcerptHasRows, screenshot: res.pixelScreenshot, lifecycle: res.lifecycle }, null, 1));
