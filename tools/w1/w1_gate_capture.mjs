#!/usr/bin/env node
// w1_gate_capture.mjs — PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031 / W1-2
// Staging gate on NEW_WORK server :8171 (three 0.187.0 exact pin + W1-2 product fixes).
// READ-ONLY vs BASE/LIVE 8163. Isolated headless Edge + CDP on a FREE port.
// Gates:
//   GATE_REVISION:  THREE.REVISION === '187' on /world
//   GATE_PANEL:     after teleport, census panel "origin okna" == requested window (fix a)
//   GATE_LRU:       return to a cached window -> terrain tile re-fetch delta == 0 (fix b)
//   FRAMES:         f0/fa/fb/fc/fd (+fe1/fe2, +fb2 corrected top-down root-cause proof)
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import os from 'node:os';
import net from 'node:net';
import path from 'node:path';

const here = path.dirname(new URL(import.meta.url).href.replace(/^file:\/\/\//, ''));
const BASE = 'http://127.0.0.1:8171';
const OUT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031\\W1_TERRAIN_MATERIALS\\W1-2\\staging';
const PROFILE_MARK = 'pec-w1-2-gate-8171';
const EDGE_CANDIDATES = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
];
const hash = (b) => createHash('sha256').update(b).digest('hex');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
await mkdir(OUT, { recursive: true });

function findFreePort() {
  const tryPort = (p) => new Promise((resolve) => {
    const srv = net.createServer();
    srv.once('error', () => resolve(false));
    srv.listen(p, '127.0.0.1', () => srv.close(() => resolve(true)));
  });
  return (async () => {
    for (let p = 21200; p < 21300; p++) { if (p === 9222) continue; if (await tryPort(p)) return p; }
    throw new Error('no free CDP port');
  })();
}
function killOwnLeftover() {
  try {
    const r = spawnSync('powershell', ['-NoProfile', '-Command',
      `Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*${PROFILE_MARK}*' } | Select-Object ProcessId | ConvertTo-Json`],
    { encoding: 'utf8', timeout: 20000 });
    let pids = [];
    try { const j = JSON.parse(r.stdout); if (Array.isArray(j)) pids = j.map((x) => x.ProcessId).filter(Boolean); else if (j && j.ProcessId) pids = [j.ProcessId]; } catch { /* none */ }
    for (const pid of pids) { try { process.kill(Number(pid)); } catch { /* gone */ } }
  } catch { /* none */ }
}
class Cdp {
  constructor(ws) { this.ws = ws; this.seq = 0; this.pending = new Map(); this.handlers = new Map(); }
  static async connect(port) {
    for (let i = 0; i < 60; i++) {
      try {
        const r = await fetch(`http://127.0.0.1:${port}/json/list`);
        const page = (await r.json()).find((t) => t.type === 'page');
        if (page) {
          const ws = new WebSocket(page.webSocketDebuggerUrl);
          await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
          return new Cdp(ws);
        }
      } catch { /* not ready */ }
      await sleep(250);
    }
    throw new Error('CDP page target not found');
  }
  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = ++this.seq; this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
      setTimeout(() => { if (this.pending.has(id)) { this.pending.delete(id); reject(new Error(`CDP timeout: ${method}`)); } }, 90000);
    });
  }
  handle(msg) {
    if (msg.id && this.pending.has(msg.id)) {
      const { resolve, reject } = this.pending.get(msg.id); this.pending.delete(msg.id);
      if (msg.error) reject(new Error(msg.error.message)); else resolve(msg.result);
      return;
    }
    for (const [, fn] of this.handlers) fn(msg);
  }
  async evaluate(expression) {
    const r = await this.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(`page eval failed: ${r.exceptionDetails.exception?.description?.slice(0, 400) ?? r.exceptionDetails.text}`);
    return r.result.value;
  }
  async screenshot() { const r = await this.send('Page.captureScreenshot', { format: 'png' }); return Buffer.from(r.data, 'base64'); }
  close() { try { this.ws.close(); } catch { /* gone */ } }
}
async function launchBrowser() {
  const bin = EDGE_CANDIDATES.find((p) => existsSync(p));
  if (!bin) throw new Error('no browser binary found');
  const port = await findFreePort();
  const userDataDir = path.join(os.tmpdir(), 'opencode', `${PROFILE_MARK}-${Date.now()}`);
  const child = spawn(bin, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${userDataDir}`,
    '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--disable-background-networking',
    '--window-size=1280,720', 'about:blank'], { stdio: ['ignore', 'ignore', 'ignore'], windowsHide: true });
  const cdp = await Cdp.connect(port);
  return { child, port, bin, cdp };
}

const consoleLog = []; let pageErrors = [];

async function counters(cdp) {
  return cdp.evaluate(`(() => {
    const cen = document.getElementById('world-census')?.textContent ?? '';
    const ev  = document.getElementById('world-evidence')?.textContent ?? '';
    const fetches = /pobrania: (\\d+) \\| b\\u0142\\u0119dy: (\\d+)/.exec(cen);
    const mats = /fetch materia\\u0142\\u00f3w: (\\d+) \\(b\\u0142\\u0119dy (\\d+)\\) \\| fetch tekstur: (\\d+)/.exec(cen);
    const origin = /origin okna: (\\d+),(\\d+)/.exec(cen);
    const spl = /resolved (\\d+)\\/(\\d+) warstw, zdekodowane (\\d+), zastosowane (\\d+)/.exec(cen);
    const spl2 = /okno: resolved (\\d+)\\/(\\d+)/.exec(ev);
    return {
      windowOrigin: window.__peR2Debug.windowOrigin,
      panelOrigin: origin ? [Number(origin[1]), Number(origin[2])] : null,
      evidenceWindowResolved: spl2 ? Number(spl2[1]) : null,
      terrainFetches: fetches ? Number(fetches[1]) : null,
      fetchErrors: fetches ? Number(fetches[2]) : null,
      materialFetches: mats ? Number(mats[1]) : null,
      textureFetches: mats ? Number(mats[3]) : null,
      censusSplatResolved: spl ? Number(spl[1]) : null,
      coherence: document.getElementById('scene-coherence')?.textContent ?? '',
      loadStatus: document.getElementById('diagnostics')?.getAttribute('data-load-status'),
      cam: window.__peR2Debug.camera,
      mode: window.__peR2Debug.mode,
    };
  })()`);
}

async function frame(cdp, name, notes) {
  const m = await counters(cdp);
  const png = await cdp.screenshot();
  const file = `staging_${name}.png`;
  await writeFile(path.join(OUT, file), png);
  const cohFirstLine = (m.coherence.split('\n')[0] ?? '');
  const reqWin = /\\u017c\\u0105dane okno (\\d+),(\\d+)/.exec(cohFirstLine);
  const terWin = /teren (\\d+),(\\d+)/.exec(cohFirstLine);
  return {
    frame: name, notes, png: { file, bytes: png.length, sha256: hash(png) },
    cam: m.cam, mode: m.mode, loadStatus: m.loadStatus,
    windowOrigin: m.windowOrigin, panelOrigin: m.panelOrigin,
    requestedWindow: reqWin ? [Number(reqWin[1]), Number(reqWin[2])] : null,
    terrainCoherenceWindow: terWin ? [Number(terWin[1]), Number(terWin[2])] : null,
    evidenceWindowResolved: m.evidenceWindowResolved,
    censusSplatResolved: m.censusSplatResolved,
    terrainFetches: m.terrainFetches, fetchErrors: m.fetchErrors,
    materialFetches: m.materialFetches, textureFetches: m.textureFetches,
    coherenceFirstLine: cohFirstLine.slice(0, 160),
  };
}

async function waitForExpr(cdp, expr, timeoutMs = 120000) {
  const t0 = Date.now();
  for (;;) {
    try { if (await cdp.evaluate(expr)) return { waitedMs: Date.now() - t0 }; } catch { /* poll */ }
    if (Date.now() - t0 > timeoutMs) return { timedOut: true, waitedMs: Date.now() - t0 };
    await sleep(300);
  }
}
async function dragLook(cdp, dx, dy) {
  await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: 640, y: 360, button: 'left', clickCount: 1 });
  const steps = 10;
  for (let i = 1; i <= steps; i++) {
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: 640 + Math.round(dx * i / steps), y: 360 + Math.round(dy * i / steps), button: 'left', buttons: 1 });
    await sleep(25);
  }
  await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: 640 + dx, y: 360 + dy, button: 'left', clickCount: 1 });
  await sleep(300);
}
async function wheelZoom(cdp, clicks) {
  for (let i = 0; i < Math.abs(clicks); i++) {
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseWheel', x: 640, y: 360, deltaX: 0, deltaY: clicks > 0 ? 120 : -120 });
    await sleep(60);
  }
  await sleep(400);
}
async function key(cdp, code, down) { await cdp.send('Input.dispatchKeyEvent', { type: down ? 'rawKeyDown' : 'keyUp', key: code.startsWith('Key') ? code.slice(3).toLowerCase() : code, code, windowsVirtualKeyCode: 0 }); }
async function press(cdp, code) { await key(cdp, code, true); await sleep(80); await key(cdp, code, false); await sleep(150); }
async function teleport(cdp, gx, gy) {
  await cdp.evaluate(`(() => { document.getElementById('btn-drawer').click(); return true; })()`);
  await sleep(300);
  await cdp.evaluate(`(() => { const a = document.getElementById('tp-gx'), b = document.getElementById('tp-gy'); a.value = '${gx}'; b.value = '${gy}'; a.dispatchEvent(new Event('change', { bubbles: true })); document.getElementById('tp-go').click(); })()`);
}

const browser = await launchBrowser();
const { cdp } = browser;
cdp.ws.addEventListener('message', (ev) => {
  let msg; try { msg = JSON.parse(ev.data); } catch { return; }
  if (msg.method === 'Runtime.consoleAPICalled') consoleLog.push({ type: msg.params.type, text: (msg.params.args ?? []).map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 200) });
  if (msg.method === 'Runtime.exceptionThrown') pageErrors.push(String(msg.params.exceptionDetails?.exception?.description ?? msg.params.exceptionDetails?.text ?? '').slice(0, 400));
  cdp.handle(msg);
});
await cdp.send('Page.enable');
await cdp.send('Runtime.enable');
await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });

const gates = {};
const frames = [];

// ---- load /world ----
await cdp.send('Page.navigate', { url: `${BASE}/world` });
await waitForExpr(cdp, `(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY')`);
const homeOrigin = await cdp.evaluate(`window.__peR2Debug.windowOrigin`);

// GATE_REVISION — world-app.js is a module (no window.THREE), so the proof is
// the SERVED three build REVISION constant (the exact bytes the page imports).
// r187 splits the build: three.module.js re-exports from three.core.js, where
// the REVISION literal lives; check BOTH served files.
const revision = await cdp.evaluate(`(async () => {
  const grab = async (u) => { try { const t = await fetch(u).then(r => r.text()); const m = /REVISION\\s*=\\s*'(\\d+)'/.exec(t); return m ? m[1] : null; } catch { return null; } };
  return (await grab('/node_modules/three/build/three.core.js')) ?? (await grab('/node_modules/three/build/three.module.js'));
})()`);
const revisionScene = await cdp.evaluate(`fetch('/compat/world-app.js').then(r => r.ok)`);
gates.GATE_REVISION = { expected: '187', actual: revision, importMapReachable: revisionScene, pass: revision === '187' };

// wait for full coherence (textures+veg of the same request) like the baseline did
await waitForExpr(cdp, `((document.getElementById('scene-coherence')?.textContent ?? '').includes('GOTOWA'))`, 180000);
frames.push(await frame(cdp, 'f0_world_ready', 'initial load, orbit default framing (same as W1-1 baseline)'));

// ---- (a) ground close: walk, look down ----
await press(cdp, 'Digit3');
await waitForExpr(cdp, `((document.getElementById('scene-coherence')?.textContent ?? '').includes('GOTOWA'))`, 90000);
await dragLook(cdp, 0, 180);
await sleep(400);
frames.push(await frame(cdp, 'fa_ground_close_walk', 'walk mode, eye on shared surface, look-down angle'));
await dragLook(cdp, 0, -180);

// ---- (b) THE SAME top-down attempt as W1-1 (root-cause frame; expected FLAT background) ----
await press(cdp, 'Digit1');
await sleep(400);
await dragLook(cdp, 0, -220);
await wheelZoom(cdp, -4);
frames.push(await frame(cdp, 'fb_topdown_tiles', 'IDENTICAL choreography to W1-1 fb (expected: still flat — root cause is the tool drag direction, not the product)'));
// fb2: the CORRECTED top-down (drag DOWN = camera toward top-down in OrbitControls semantics)
await dragLook(cdp, 0, 220); // restore
await dragLook(cdp, 0, 220); // swing the camera up above the target (correct direction)
await sleep(300);
frames.push(await frame(cdp, 'fb2_topdown_corrected', 'CORRECTED top-down drag direction (+220): what the terrain actually looks like from above — root-cause proof'));
await dragLook(cdp, 0, -220); // restore

// ---- (c) low horizon ----
await wheelZoom(cdp, 6);
await dragLook(cdp, 0, 120);
frames.push(await frame(cdp, 'fc_low_horizon', 'orbit, low camera angle near horizon'));
await dragLook(cdp, 0, -120);

// ---- (d) near/mid/far ----
await wheelZoom(cdp, -18);
frames.push(await frame(cdp, 'fd_near_mid_far', 'orbit zoomed out: near window + mid LOD ring + far world'));
await wheelZoom(cdp, 14);

// ---- (e) teleport far -> GATE_PANEL ----
const beforeFar = await counters(cdp);
await teleport(cdp, 180, 40);
await waitForExpr(cdp, `(window.__peR2Debug.windowOrigin && window.__peR2Debug.windowOrigin.gx === 176 && window.__peR2Debug.windowOrigin.gy === 36)`, 180000);
await waitForExpr(cdp, `((document.getElementById('scene-coherence')?.textContent ?? '').includes('GOTOWA'))`, 180000);
await sleep(600); // let the census/evidence panels tick at least once past the rebuild
const fe1 = await frame(cdp, 'fe1_teleport_far', 'teleported to tile 180,40 (window 176,36)');
frames.push(fe1);
gates.GATE_PANEL = {
  requested: [176, 36],
  stateWindowOrigin: fe1.windowOrigin,
  panelOrigin: fe1.panelOrigin,
  pass: fe1.windowOrigin && fe1.windowOrigin.gx === 176 && fe1.windowOrigin.gy === 36
     && Array.isArray(fe1.panelOrigin) && fe1.panelOrigin[0] === 176 && fe1.panelOrigin[1] === 36,
};

// ---- return home -> GATE_LRU ----
const beforeReturn = await counters(cdp);
await teleport(cdp, homeOrigin.gx + 4, homeOrigin.gy + 4);
await waitForExpr(cdp, `(window.__peR2Debug.windowOrigin && window.__peR2Debug.windowOrigin.gx === ${homeOrigin.gx} && window.__peR2Debug.windowOrigin.gy === ${homeOrigin.gy})`, 180000);
await waitForExpr(cdp, `((document.getElementById('scene-coherence')?.textContent ?? '').includes('GOTOWA'))`, 180000);
await sleep(600);
const fe2 = await frame(cdp, 'fe2_return_home', 'returned to the home window — SAME tiles (LRU gate)');
frames.push(fe2);
const afterReturn = await counters(cdp);
await sleep(2000); // idle stability: NO further terrain fetches may appear
const afterReturnStable = await counters(cdp);
// fetches between beforeReturn and afterReturn must all belong to the RETURN
// rebuild, and with the fix every home-window tile comes from the LRU.
gates.GATE_LRU = {
  homeWindow: homeOrigin,
  terrainFetchesBeforeReturn: beforeReturn.terrainFetches,
  terrainFetchesAfterReturn: afterReturn.terrainFetches,
  terrainRefetchDelta: afterReturn.terrainFetches - beforeReturn.terrainFetches,
  materialFetchesDelta: afterReturn.materialFetches - beforeReturn.materialFetches,
  textureFetchesDelta: afterReturn.textureFetches - beforeReturn.textureFetches,
  stateWindowOrigin: fe2.windowOrigin,
  panelOrigin: fe2.panelOrigin,
  historicalNegativeControl: 'W1-1 LIVE 8163 (pre-fix): the same return-home refetched ~100 tiles (fe1->fe2 fetches 232->332, identityOf wiped by boot status refresh)',
// the LRU delta is measured from the point the FAR window had FULLY settled:
// fetches between beforeReturn and afterReturn must all belong to the RETURN
// rebuild, and with the fix every home-window tile comes from the LRU.
  terrainRefetchDeltaStable: afterReturnStable.terrainFetches - beforeReturn.terrainFetches,
  pass: fe2.windowOrigin && fe2.windowOrigin.gx === homeOrigin.gx && fe2.windowOrigin.gy === homeOrigin.gy
     && (afterReturn.terrainFetches - beforeReturn.terrainFetches) === 0,
};
gates.GATE_PANEL_HOME = {
  requested: [homeOrigin.gx, homeOrigin.gy],
  panelOrigin: fe2.panelOrigin,
  evidenceWindowResolved: fe2.evidenceWindowResolved,
  censusSplatResolved: fe2.censusSplatResolved,
  pass: Array.isArray(fe2.panelOrigin) && fe2.panelOrigin[0] === homeOrigin.gx && fe2.panelOrigin[1] === homeOrigin.gy,
};
// evidence vs census coherence (the fix-a symptom was 583 vs 959 from different windows)
gates.GATE_EVIDENCE_CENSUS_COHERENT = {
  evidenceWindowResolved: fe2.evidenceWindowResolved,
  censusSplatResolved: fe2.censusSplatResolved,
  note: 'fix-a symptom was evidence showing an OLD window (583/583) while census showed the current one (959/959); both must now agree within one 400ms tick',
  pass: fe2.evidenceWindowResolved === fe2.censusSplatResolved,
};

const out = {
  run: 'PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031/W1-2',
  capturedAt: new Date().toISOString(), base: BASE,
  browser: { bin: browser.bin, cdpPort: browser.port, isolated: true, headless: 'new', profileMark: PROFILE_MARK },
  fixedCaptureConfig: { viewport: '1280x720', deviceScaleFactor: 1 },
  homeWindowOrigin: homeOrigin,
  threeRevision: revision,
  gates, frames,
  beforeFar, beforeReturn, afterReturn,
  consoleTail: consoleLog.slice(-30), pageErrors,
};
await writeFile(path.join(OUT, '..', 'GATE_RESULTS.json'), JSON.stringify(out, null, 1));
console.log('GATE_REVISION pass=', gates.GATE_REVISION.pass, 'rev=', revision);
console.log('GATE_PANEL pass=', gates.GATE_PANEL.pass, JSON.stringify(gates.GATE_PANEL));
console.log('GATE_LRU pass=', gates.GATE_LRU.pass, JSON.stringify({ delta: gates.GATE_LRU.terrainRefetchDelta }));
console.log('GATE_PANEL_HOME pass=', gates.GATE_PANEL_HOME.pass, JSON.stringify(gates.GATE_PANEL_HOME));
console.log('GATE_EVIDENCE_CENSUS_COHERENT pass=', gates.GATE_EVIDENCE_CENSUS_COHERENT.pass);
console.log('pageErrors=', pageErrors.length);
cdp.close();
setTimeout(() => { try { process.kill(browser.child.pid); } catch { /* gone */ } process.exit(0); }, 800);
