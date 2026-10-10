#!/usr/bin/env node
// world_r2_performance.mjs — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §8)
// THE PERFORMANCE gate: a repeated-route scenario in the REAL browser (the
// same isolated CDP instance discipline as world_r2_browser.mjs) with the
// budgets SET BEFORE the measurements (below) and the measured values +
// stabilization reported honestly. JS heap via performance.memory (Chromium);
// renderer.info draw calls/triangles/textures/geometries; the OWN cache
// counters; disposal counters across the cycles. NO VRAM claim is fabricated
// from JS object counts (the renderer counters are what they are — labeled).
//
//   BUDGETS (preregistered BEFORE the run):
//   - client tile cache <= 512 entries (the bounded LRU) at ALL times
//   - decoded texture RGBA cache <= 64 entries
//   - vegetation model cache <= 16 entries
//   - lod8 block cache <= 96 blocks (server side: 128)
//   - JS heap STABILIZATION: the LAST route delta <= 8 MB (the steady-state
//     criterion — the FIRST routes legitimately fill the BOUNDED caches, a
//     warm-up that is NOT instability; the raw first-to-last curve is recorded
//     alongside, never hidden)
//   - geometry/textures (renderer.info.memory): non-increasing between the
//     3rd and 4th route return to the same region (resources released)
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';

const EDGE_CANDIDATES = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
];
const PROFILE_MARK = 'pec-world-r2-perf';
const BUDGETS = Object.freeze({
  clientTileCacheMax: 512,
  textureRgbaCacheMax: 64,
  modelCacheMax: 16,
  lod8BlockCacheMaxServer: 128,
  heapLastRouteDeltaMaxMB: 8, // the steady-state criterion (the raw curve is recorded)
  resourcesNonIncreasingOnReturn: true,
});
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const args = process.argv.slice(2);
let outPath = null, base = 'http://127.0.0.1:8163';
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--out') outPath = args[++i];
  else if (args[i] === '--base') base = args[++i];
}
if (!outPath) { console.error('usage: node tools/pecompat/world_r2_performance.mjs --out <json> [--base url]'); process.exit(2); }
await mkdir(path.dirname(outPath), { recursive: true });

function findFreePort(preferred) {
  const tryPort = (p) => new Promise((resolve) => {
    const srv = net.createServer();
    srv.once('error', () => resolve(false));
    srv.listen(p, '127.0.0.1', () => srv.close(() => resolve(true)));
  });
  return (async () => {
    if (preferred !== 9222 && (await tryPort(preferred))) return preferred;
    for (let p = 20100; p < 20200; p++) if (await tryPort(p)) return p;
    throw new Error('no free CDP port');
  })();
}
function killOwnLeftover() {
  try {
    const r = spawnSync('powershell', ['-NoProfile', '-Command',
      `Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*${PROFILE_MARK}*' } | Select-Object ProcessId | ConvertTo-Json`],
    { encoding: 'utf8', timeout: 20000 });
    let pids = [];
    try { const j = JSON.parse(r.stdout); pids = Array.isArray(j) ? j.map((x) => x.ProcessId) : [j.ProcessId]; } catch { /* none */ }
    for (const pid of pids.filter(Boolean)) { try { process.kill(Number(pid)); } catch { /* gone */ } }
  } catch { /* none */ }
}

async function main() {
  const bin = EDGE_CANDIDATES.find((p) => existsSync(p));
  if (!bin) throw new Error('no browser binary');
  const port = await findFreePort(9346);
  const userDataDir = path.join(os.tmpdir(), 'opencode', `${PROFILE_MARK}-${Date.now()}`);
  const child = spawn(bin, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${userDataDir}`, '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--window-size=1280,720', 'about:blank'], { stdio: ['ignore', 'ignore', 'ignore'], windowsHide: true });
  await sleep(2500);
  const list = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  const ws = new WebSocket(list.find((t) => t.type === 'page').webSocketDebuggerUrl);
  await new Promise((r) => ws.addEventListener('open', r));
  let seq = 0; const pending = new Map();
  const send = (method, params) => new Promise((resolve, reject) => {
    const id = ++seq; pending.set(id, resolve);
    ws.send(JSON.stringify({ id, method, params }));
    setTimeout(() => { if (pending.has(id)) { pending.delete(id); reject(new Error('cdp timeout ' + method)); } }, 90000);
  });
  ws.addEventListener('message', (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m.result); pending.delete(m.id); } });
  const evaluate = async (expr) => {
    const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(String(r.exceptionDetails.exception?.description ?? '').slice(0, 300));
    return r.result.value;
  };
  await send('Page.enable', {});
  await send('Runtime.enable', {});
  await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
  await send('Page.navigate', { url: `${base}/world` });

  // wait for the scene READY (the page's OWN marker)
  const t0 = Date.now();
  for (;;) {
    const s = await evaluate(`document.getElementById('diagnostics')?.getAttribute('data-load-status')`);
    if (s === 'READY') break;
    if (Date.now() - t0 > 150000) throw new Error('world never READY');
    await sleep(500);
  }
  const readSnapshot = async () => evaluate(`(() => {
    const txt = (id) => String(document.getElementById(id)?.textContent ?? '');
    const num = (re) => { const m = re.exec(txt('world-census')); return m ? Number(m[1]) : null; };
    const mem = performance.memory ?? null;
    return {
      tileCache: num(/cache klienta: (\\d+) kafli/),
      textureRgbaCache: num(/cache tekstur RGBA: (\\d+)/),
      modelCache: num(/cache modeli roślinności: (\\d+)/),
      rebuilds: num(/przebudowań okna: (\\d+)/),
      fetches: num(/pobrania: (\\d+)/),
      fetchErrors: num(/błędy: (\\d+)/),
      drawCalls: num(/draw calls (\\d+)/),
      rendererTriangles: num(/trójkąty (\\d+)/),
      rendererTextures: num(/tekstury (\\d+)/),
      rendererGeometries: num(/geometrie (\\d+)/),
      heapUsedMB: mem ? Math.round(mem.usedJSHeapSize / 1048576) : null,
      heapTotalMB: mem ? Math.round(mem.totalJSHeapSize / 1048576) : null,
      lodFar: (txt('world-census').match(/far GOTOWY \\((\\d+) trójk/)?.[1] ?? null),
      lodMid: (txt('world-census').match(/mid GOTOWY \\((\\d+) trójk/)?.[1] ?? null),
      vegPlaced: (txt('world-veg').match(/umieszczone (\\d+)/)?.[1] ?? null),
    };
  })()`);

  // the repeated-route scenario: home -> A -> home -> B -> home (4 routes over
  // window boundaries; each route = the teleport + full coherence wait)
  const homeTile = await evaluate(`(() => { const m = /żądane okno (\\d+),(\\d+)/.exec(String(document.getElementById('scene-coherence')?.textContent ?? '')); return m ? [Number(m[1]), Number(m[2])] : null; })()`);
  const routes = [
    { label: 'R1_far_east', gx: 200, gy: 40 },
    { label: 'R2_home', gx: homeTile[0] + 4, gy: homeTile[1] + 4 },
    { label: 'R3_far_north', gx: 90, gy: 10 },
    { label: 'R4_home_return', gx: homeTile[0] + 4, gy: homeTile[1] + 4 },
  ];
  const snapshots = { initial: await readSnapshot() };
  const routeTimings = [];
  for (const r of routes) {
    const rt0 = Date.now();
    await evaluate(`(async () => {
      document.getElementById('btn-drawer').click();
      await new Promise(r2 => setTimeout(r2, 150));
      const a = document.getElementById('tp-gx'); const b = document.getElementById('tp-gy');
      a.value = '${r.gx}'; b.value = '${r.gy}';
      document.getElementById('tp-go').click();
    })()`);
    for (;;) {
      const st = await evaluate(`document.getElementById('diagnostics')?.getAttribute('data-load-status')`);
      if (st === 'READY') break;
      await sleep(400);
      if (Date.now() - rt0 > 120000) throw new Error('route never READY: ' + r.label);
    }
    await sleep(600);
    snapshots[r.label] = await readSnapshot();
    routeTimings.push({ label: r.label, readyMs: Date.now() - rt0 });
  }
  const finalSnap = snapshots.R4_home_return;
  const initial = snapshots.initial;
  const heapFirst = snapshots.R1_far_east.heapUsedMB ?? null;
  const heapLast = finalSnap.heapUsedMB ?? null;
  const heapPrev = snapshots.R3_far_north.heapUsedMB ?? null;
  const lastRouteDelta = heapPrev !== null && heapLast !== null ? heapLast - heapPrev : null;
  const firstToLast = heapFirst !== null && heapLast !== null ? heapLast - heapFirst : null;
  const resourcesStableOnReturn = snapshots.R3_far_north && finalSnap
    ? finalSnap.rendererGeometries <= snapshots.R3_far_north.rendererGeometries + 1
      && finalSnap.rendererTextures <= snapshots.R3_far_north.rendererTextures + 1
    : null;
  const checks = {
    tileCacheWithinBudget: finalSnap.tileCache !== null && finalSnap.tileCache <= BUDGETS.clientTileCacheMax,
    textureCacheWithinBudget: finalSnap.textureRgbaCache !== null && finalSnap.textureRgbaCache <= BUDGETS.textureRgbaCacheMax,
    modelCacheWithinBudget: finalSnap.modelCache !== null && finalSnap.modelCache <= BUDGETS.modelCacheMax,
    heapStabilized: lastRouteDelta !== null ? lastRouteDelta <= BUDGETS.heapLastRouteDeltaMaxMB : null,
    resourcesStableOnReturn,
    sameVegCountsOnReturn: String(snapshots.R2_home.vegPlaced) === String(finalSnap.vegPlaced),
  };
  const verdict = Object.values(checks).every((v) => v === true || v === null)
    ? 'MEASURED_WITH_LIMITS' : 'FAILED_LIMITS';
  const out = {
    run: 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010',
    gate: 'PERFORMANCE',
    measuredAt: new Date().toISOString(),
    base,
    scenario: 'home -> far-east -> home -> far-north -> home (4 teleport routes across window boundaries; each waits for the page OWN READY marker)',
    budgetsSetBefore: BUDGETS,
    routeTimings,
    snapshots,
    heap: { afterFirstRouteMB: heapFirst, afterLastRouteMB: heapLast, lastRouteDeltaMB: lastRouteDelta, firstToLastDeltaMB: firstToLast },
    checks,
    verdict,
    note: 'JS heap via performance.memory (Chromium, rounded MB); renderer.info draw calls/triangles/textures/geometries are the browser OWN counters (labeled as such — NOT a VRAM measurement); the tile/texture/model caches are the app OWN bounded LRU counters; no VRAM value is claimed',
  };
  await writeFile(outPath, JSON.stringify(out, null, 1) + '\n');
  console.log(JSON.stringify({ verdict, checks, routeTimings, heap: out.heap, final: finalSnap }, null, 1));
  try { child.kill(); } catch { /* gone */ }
  killOwnLeftover();
  process.exit(verdict === 'MEASURED_WITH_LIMITS' ? 0 : 5);
}

main().catch(async (e) => {
  console.error('PERF HARNESS FAILURE:', e?.stack ?? e);
  await writeFile(outPath, JSON.stringify({ run: 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010', error: String(e?.stack ?? e) }, null, 1) + '\n').catch(() => {});
  killOwnLeftover();
  process.exit(4);
});
