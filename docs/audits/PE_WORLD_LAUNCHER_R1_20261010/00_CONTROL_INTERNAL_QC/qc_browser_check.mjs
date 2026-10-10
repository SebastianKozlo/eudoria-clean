// qc_browser_check.mjs â€” PE_WORLD_LAUNCHER_R1_20261010 â€” FRESH INTERNAL QC (pe-master-auditor)
// MY OWN headless-browser LOAD of /launcher + /world against the STANDING run
// server 127.0.0.1:8162 (the final code), evaluated through the FIXED
// production 5-conjunct gate (evaluateLoadGate imported from the app suite â€”
// the same predicate the run's T9 gates use), plus MY OWN CDP pixel capture
// (PNG -> PRIVATE OUTPUT ONLY) with a non-triviality check.
import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { writeFile, mkdir } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { evaluateLoadGate } from '../../../../tests/pecompat/headless_load.test.mjs';
import { analyzePng } from '../../../../tools/pecompat/png_nontrivial.mjs';

const BASE = 'http://127.0.0.1:8162';
const PROFILE_MARK = 'pec-auditor-qc-browser';
const OUT_DIR = path.dirname(fileURLToPath(import.meta.url));
const PRIVATE_PNG_DIR = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_WORLD_LAUNCHER_R1_20261010\\BROWSER_QC_R1';
const BROWSERS = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
];
const browserBin = BROWSERS.find((p) => existsSync(p));
const results = { browserBin, loads: [], pixel: null, interaction: null };

function killLeftover() {
  try {
    const r = spawnSync('powershell', ['-NoProfile', '-Command',
      `Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*${PROFILE_MARK}*' } | Select-Object ProcessId | ConvertTo-Json`],
      { encoding: 'utf8', timeout: 20000 });
    let pids = [];
    try {
      const j = JSON.parse(r.stdout);
      if (Array.isArray(j)) pids = j.map((x) => x.ProcessId).filter(Boolean);
      else if (j && j.ProcessId) pids = [j.ProcessId];
    } catch { /* none */ }
    for (const pid of pids) { try { process.kill(Number(pid)); } catch { /* gone */ } }
  } catch { /* none */ }
}
import { spawnSync } from 'node:child_process';

function dumpDom(url, timeoutMs = 90000) {
  return new Promise((resolve) => {
    const userDataDir = path.join(os.tmpdir(), 'opencode', `${PROFILE_MARK}-${Date.now()}`);
    const args = ['--headless=new', `--user-data-dir=${userDataDir}`, '--no-first-run',
      '--no-default-browser-check', '--disable-extensions', '--disable-background-networking',
      '--virtual-time-budget=30000', '--dump-dom', url];
    const child = spawn(browserBin, args, { stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true });
    let dom = '', stderr = '';
    child.stdout.setEncoding('utf8'); child.stderr.setEncoding('utf8');
    child.stdout.on('data', (d) => { dom += d; });
    child.stderr.on('data', (d) => { stderr += d; });
    const t0 = Date.now();
    const timer = setTimeout(() => { child.kill(); killLeftover();
      resolve({ domText: dom, stderr, exitCode: null, elapsedMs: Date.now() - t0, timedOut: true }); }, timeoutMs);
    child.once('exit', (code) => { clearTimeout(timer); killLeftover();
      resolve({ domText: dom, stderr, exitCode: code, elapsedMs: Date.now() - t0, timedOut: false }); });
  });
}

async function loadChecks() {
  // ---------- /launcher ----------
  const l = await dumpDom(`${BASE}/launcher`);
  const lGate = evaluateLoadGate({ exitCode: l.exitCode, domText: l.domText });
  const lMarkers = {
    entryButtonLabelExact: l.domText.includes('Uruchom podgl\u0105d \u015bwiata'),
    eraLabel: l.domText.includes('PCG_9_3_5'),
    denominator: l.domText.includes('51 920') || l.domText.includes('51920'),
    coverageLine: l.domText.includes('pokrycie:'),
    vegModeLabel: l.domText.includes('VEGETATION_MODE = RECONSTRUCTION_PREVIEW'),
    threeWaySeparation: l.domText.includes('ORIGINAL_CLIMATE_RECORDS') && l.domText.includes('INSTANCE_DISTRIBUTION'),
    unsupported25Visible: l.domText.includes('25') && /nieobsÅ‚ugiwane|UNSUPPORTED/i.test(l.domText),
    noOriginalXyzClaim: !/oryginalne\s+xyz\s*[:=]/i.test(l.domText),
  };
  results.loads.push({ url: `${BASE}/launcher`, exitCode: l.exitCode, elapsedMs: l.elapsedMs,
    domBytes: l.domText.length, gate: { passed: lGate.passed, missing: lGate.missing, conjuncts: lGate.conjuncts, loadStatus: lGate.loadStatus },
    markers: lMarkers, stderrExcerpt: l.stderr.slice(0, 300) });
  // ---------- /world (veg ON) ----------
  const w = await dumpDom(`${BASE}/world#tile=53,114&profile=0&seed=0&density=50&veg=1`);
  const wGate = evaluateLoadGate({ exitCode: w.exitCode, domText: w.domText });
  const wMarkers = {
    activeWindow64: w.domText.includes('kafle aktywne (okno 8\u00d78): 64 / limit 64'),
    adapterUnitsPosition: w.domText.includes('pozycja (jednostki adaptera'),
    noOriginalXyzPositionClaim: !/pozycja \(oryginalne/i.test(w.domText) && !/pozycja: oryginalne/i.test(w.domText),
    rawU16Readout: w.domText.includes('surowe u16='),
    vegetationCensus: /ro\u015blinno\u015b\u0107: \u017c\u0105dane \d+ \/ wyrenderowane \d+ \/ ograniczone \d+/.test(w.domText),
    vegetationMode: w.domText.includes('VEGETATION_MODE = RECONSTRUCTION_PREVIEW'),
    vegetationProfileSeed: w.domText.includes('Profil ro\u015blinno\u015bci:') && w.domText.includes('Seed podgl\u0105du (LAB_SEED):'),
    vegetationP3Separate: /p3 = 0/.test(w.domText),
    vegetationThreeWaySeparation: w.domText.includes('ORIGINAL_CLIMATE_RECORDS') && w.domText.includes('RECOVERED_RNG_ARITHMETIC') && w.domText.includes('INSTANCE_DISTRIBUTION'),
  };
  results.loads.push({ url: `${BASE}/world#tile=53,114&profile=0&seed=0&density=50&veg=1`, exitCode: w.exitCode, elapsedMs: w.elapsedMs,
    domBytes: w.domText.length, gate: { passed: wGate.passed, missing: wGate.missing, conjuncts: wGate.conjuncts, loadStatus: wGate.loadStatus },
    markers: wMarkers, stderrExcerpt: w.stderr.slice(0, 300) });
  await writeFile(path.join(OUT_DIR, 'raw', 'QC_BROWSER_LAUNCHER_DOM.html'), l.domText, 'utf8');
  await writeFile(path.join(OUT_DIR, 'raw', 'QC_BROWSER_WORLD_DOM.html'), w.domText, 'utf8');
}

// ---------- CDP pixel capture (launcher page; PRIVATE PNG only) ----------
async function freePort() {
  const net = await import('node:net');
  return new Promise((res) => {
    const s = net.createServer();
    s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); });
  });
}
async function cdpCapture(kind, url) {
  const dbgPort = await freePort();
  const userDataDir = path.join(os.tmpdir(), 'opencode', `${PROFILE_MARK}-cdp-${Date.now()}`);
  const args = ['--headless=new', `--remote-debugging-port=${dbgPort}`, `--user-data-dir=${userDataDir}`,
    '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--disable-background-networking',
    '--window-size=960,700', url];
  const child = spawn(browserBin, args, { stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true });
  let stderrAll = '';
  child.stderr.setEncoding('utf8'); child.stderr.on('data', (d) => { stderrAll += d; });
  try {
    // poll the /json list until ready
    let target = null;
    for (let i = 0; i < 60 && !target; i++) {
      await new Promise((r) => setTimeout(r, 500));
      try {
        const list = await (await fetch(`http://127.0.0.1:${dbgPort}/json`)).json();
        target = list.find((t) => t.type === 'page' && t.url.startsWith('http://127.0.0.1:8162')) ?? list.find((t) => t.type === 'page');
      } catch { /* not up yet */ }
    }
    if (!target) throw new Error('CDP /json target not found');
    const ws = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((res, rej) => { ws.onopen = res; ws.onerror = (e) => rej(new Error('ws error')); });
    let msgId = 0;
    const pending = new Map();
    ws.onmessage = (ev) => {
      const m = JSON.parse(ev.data);
      if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
    };
    const send = (method, params = {}) => new Promise((res) => {
      const id = ++msgId; pending.set(id, res); ws.send(JSON.stringify({ id, method, params }));
    });
    await send('Runtime.enable');
    // readiness poll on the page's OWN honest census markers (real-time, not virtual)
    let ready = false;
    for (let i = 0; i < 80 && !ready; i++) {
      await new Promise((r) => setTimeout(r, 500));
      const r = await send('Runtime.evaluate', { expression:
        kind === 'world'
          ? `document.body.innerText.includes('kafle aktywne') && /instancje okna/.test(document.body.innerText) ? 'READY' : 'WAIT'`
          : `document.querySelector('[data-load-status]')?.dataset.loadStatus === 'READY' ? 'READY' : 'WAIT'`,
        returnByValue: true });
      if (r.result?.result?.value === 'READY') ready = true;
    }
    await new Promise((r) => setTimeout(r, 3000)); // real-time settle (presented frames)
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    ws.close();
    const b64 = shot.result?.data;
    if (!b64) throw new Error('no screenshot data');
    return { png: Buffer.from(b64, 'base64'), ready, stderrAll: stderrAll.slice(0, 300) };
  } finally {
    try { child.kill(); } catch { /* gone */ }
    killLeftover();
  }
}

async function pixelCheck() {
  await mkdir(PRIVATE_PNG_DIR, { recursive: true });
  const { png, ready, stderrAll } = await cdpCapture('launcher', `${BASE}/launcher`);
  const sha = createHash('sha256').update(png).digest('hex');
  const pngPath = path.join(PRIVATE_PNG_DIR, 'qc_pixel_launcher.png');
  await writeFile(pngPath, png);
  let stats = null;
  try { stats = await analyzePng(png); } catch (e) { stats = { error: String(e) }; }
  results.pixel = {
    kind: 'launcher', url: `${BASE}/launcher`, readinessMarkerSeen: ready,
    pngPath, bytes: png.byteLength, sha256: sha, stats,
  };
}

await loadChecks();
await pixelCheck();
// INTERACTION: the automation daemon (port 9222) check â€” expected DOWN
try {
  const net = await import('node:net');
  const daemonUp = await new Promise((res) => {
    const s = new net.Socket();
    s.setTimeout(1500);
    s.once('connect', () => { s.destroy(); res(true); });
    s.once('timeout', () => { s.destroy(); res(false); });
    s.once('error', () => res(false));
    s.connect(9222, '127.0.0.1');
  });
  results.interaction = { daemon9222Up: daemonUp, status: daemonUp ? 'PERFORMABLE' : 'NOT_PERFORMED (automation daemon DOWN â€” honest)' };
} catch (e) { results.interaction = { status: 'NOT_PERFORMED', error: String(e) }; }

await writeFile(path.join(OUT_DIR, 'raw', 'QC_BROWSER_CHECK.json'), JSON.stringify(results, null, 1), 'utf8');
console.log(JSON.stringify(results, null, 1));
