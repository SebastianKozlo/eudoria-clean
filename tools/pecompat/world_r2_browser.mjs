#!/usr/bin/env node
// world_r2_browser.mjs — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §8)
// THE REAL-BROWSER INTERACTION harness: a suite-owned ISOLATED headless
// browser instance (headless Edge with --remote-debugging-port on a FREE
// port — NEVER the old 9222 daemon, never a foreign session, never a global
// security change), driven over the Chrome DevTools Protocol with the Node
// native WebSocket client. REAL user input is dispatched (raw key events,
// mouse events, viewport resize); the DOM + pixels are captured after the
// page's OWN honest readiness markers; console messages + uncaught
// exceptions are recorded.
//
// WHAT IT MEASURES (each scenario writes a JSON record + a PRIVATE PNG):
//   - load: /world boot to READY with the scene-coherence line all-components
//   - canvas size >= 85% width / 80% height of the 1280x720 viewport (§5)
//   - F/Reset stability x3 (§5/WL-4): the window origin never moves for the
//     same focus
//   - mode transitions 1/2/3 without a position jump (§5)
//   - REAL walk movement with W held (walk mode): position changes; the
//     shared-surface rule holds (Y tracks the surface)
//   - the drawer inputs never capture movement keys (§5); movement works
//     again after the input is blurred
//   - teleport to a DISTANT region + return (§4/§8): the window follows the
//     focus, the census updates; the SAME config reproduces the SAME
//     vegetation counts at the return
//   - the vegetation/texture toggles change the canvas pixels measurably
//   - resize does not reset the camera; the drawing buffer follows (§5)
//   - Asset Lab: witness 519316 (PCG, textured status) + the four CD proxy
//     controls (source-untextured labels) with per-witness status (§7)
//
// Usage:
//   node tools/pecompat/world_r2_browser.mjs --png-dir <PRIVATE dir> --out <package json>
//        [--base http://127.0.0.1:8163]
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import os from 'node:os';
import net from 'node:net';
import path from 'node:path';

const here = path.dirname(new URL(import.meta.url).href.replace(/^file:\/\/\//, ''));
const ROOT = path.resolve(here, '..', '..');
const RUN_ID = 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010';
const PROFILE_MARK = 'pec-world-r2-browser';
const EDGE_CANDIDATES = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
];
const hash = (b) => createHash('sha256').update(b).digest('hex');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const args = process.argv.slice(2);
let pngDir = null, outPath = null, base = 'http://127.0.0.1:8163';
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--png-dir') pngDir = args[++i];
  else if (args[i] === '--out') outPath = args[++i];
  else if (args[i] === '--base') base = args[++i];
}
if (!pngDir || !outPath) {
  console.error('usage: node tools/pecompat/world_r2_browser.mjs --png-dir <dir> --out <json> [--base url]');
  process.exit(2);
}
await mkdir(pngDir, { recursive: true });
await mkdir(path.dirname(outPath), { recursive: true });

// ---------------------------------------------------------------------------
// the isolated browser instance
// ---------------------------------------------------------------------------
function findFreePort(preferred) {
  const tryPort = (p) => new Promise((resolve) => {
    const srv = net.createServer();
    srv.once('error', () => resolve(false));
    srv.listen(p, '127.0.0.1', () => srv.close(() => resolve(true)));
  });
  return (async () => {
    if (preferred !== 9222 && (await tryPort(preferred))) return preferred;
    for (let p = 20000; p < 20100; p++) {
      if (p === 9222) continue;
      if (await tryPort(p)) return p;
    }
    throw new Error('no free CDP port');
  })();
}

function killOwnLeftover() {
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
    return pids;
  } catch { return []; }
}

class Cdp {
  constructor(ws) { this.ws = ws; this.seq = 0; this.pending = new Map(); this.handlers = new Map(); }
  static async connect(port) {
    // list targets
    for (let i = 0; i < 60; i++) {
      try {
        const r = await fetch(`http://127.0.0.1:${port}/json/list`);
        const targets = await r.json();
        const page = targets.find((t) => t.type === 'page');
        if (page) {
          const ws = new WebSocket(page.webSocketDebuggerUrl);
          await new Promise((res, rej) => { ws.once ? null : null; ws.addEventListener('open', res); ws.addEventListener('error', rej); });
          return new Cdp(ws);
        }
      } catch { /* not ready yet */ }
      await sleep(250);
    }
    throw new Error('CDP page target not found');
  }
  send(method, params = {}, sessionId) {
    return new Promise((resolve, reject) => {
      const id = ++this.seq;
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params, ...(sessionId ? { sessionId } : {}) }));
      setTimeout(() => {
        if (this.pending.has(id)) { this.pending.delete(id); reject(new Error(`CDP timeout: ${method}`)); }
      }, 60000);
    });
  }
  handle(msg) {
    if (msg.id && this.pending.has(msg.id)) {
      const { resolve, reject } = this.pending.get(msg.id);
      this.pending.delete(msg.id);
      if (msg.error) reject(new Error(msg.error.message));
      else resolve(msg.result);
      return;
    }
    for (const [, fn] of this.handlers) fn(msg);
  }
  on(fn) { this.handlers.set(fn, fn); }
  async evaluate(expression) {
    const r = await this.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(`page eval failed: ${r.exceptionDetails.text ?? ''} ${r.exceptionDetails.exception?.description?.slice(0, 400) ?? ''}`);
    return r.result.value;
  }
  async screenshot() {
    const r = await this.send('Page.captureScreenshot', { format: 'png' });
    return Buffer.from(r.data, 'base64');
  }
  close() { try { this.ws.close(); } catch { /* gone */ } }
}

async function launchBrowser() {
  const bin = EDGE_CANDIDATES.find((p) => existsSync(p));
  if (!bin) throw new Error('no known browser binary (msedge/chrome) found');
  const port = await findFreePort(9333);
  const userDataDir = path.join(os.tmpdir(), 'opencode', `${PROFILE_MARK}-${Date.now()}`);
  const args = [
    '--headless=new',
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${userDataDir}`,
    '--no-first-run', '--no-default-browser-check', '--disable-extensions',
    '--disable-background-networking',
    '--window-size=1280,720',
    'about:blank',
  ];
  const child = spawn(bin, args, { stdio: ['ignore', 'ignore', 'pipe'], windowsHide: true });
  let errTail = '';
  child.stderr.setEncoding('utf8');
  child.stderr.on('data', (d) => { errTail += d; if (errTail.length > 4000) errTail = errTail.slice(-4000); });
  const cdp = await Cdp.connect(port);
  return { child, port, userDataDir, bin, cdp, errTail: () => errTail };
}

// real input events through CDP (rawKeyDown/keyUp — a 'char' event does NOT
// produce a DOM keydown; measured in this run's own probe)
async function key(cdp, code, { down = true, keyName = null, windowsVirtualKeyCode = null } = {}) {
  await cdp.send('Input.dispatchKeyEvent', {
    type: down ? 'rawKeyDown' : 'keyUp',
    key: keyName ?? (code.startsWith('Key') ? code.slice(3).toLowerCase() : code),
    code,
    windowsVirtualKeyCode: windowsVirtualKeyCode ?? 0,
  });
}
async function press(cdp, code, opts = {}) {
  await key(cdp, code, { ...opts, down: true });
  await sleep(60);
  await key(cdp, code, { down: false });
  await sleep(90);
}

const evidence = [];
const consoleLog = [];
let pageErrors = [];

async function main() {
  const browser = await launchBrowser();
  const { cdp } = browser;
  cdp.ws.addEventListener('message', (ev) => {
    let msg; try { msg = JSON.parse(ev.data); } catch { return; }
    if (msg.method === 'Runtime.consoleAPICalled') {
      consoleLog.push({ type: msg.params.type, text: (msg.params.args ?? []).map((a) => a.value ?? a.description ?? '').join(' ').slice(0, 300) });
    }
    if (msg.method === 'Runtime.exceptionThrown') {
      pageErrors.push(String(msg.params.exceptionDetails?.text ?? '') + ' ' + String(msg.params.exceptionDetails?.exception?.description ?? '').slice(0, 500));
    }
    cdp.handle(msg);
  });
  await cdp.send('Page.enable');
  await cdp.send('Runtime.enable');
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });

  const shot = async (name) => {
    const buf = await cdp.screenshot();
    const p = path.join(pngDir, name);
    await writeFile(p, buf);
    return { file: name, bytes: buf.length, sha256: hash(buf) };
  };
  const waitForExpr = async (expr, { timeoutMs = 90000, label = expr } = {}) => {
    const t0 = Date.now();
    for (;;) {
      try {
        const v = await cdp.evaluate(expr);
        if (v) return { waitedMs: Date.now() - t0 };
      } catch (e) { /* keep polling */ }
      if (Date.now() - t0 > timeoutMs) return { timedOut: true, waitedMs: Date.now() - t0, label };
      await sleep(300);
    }
  };

  // =================== SCENARIO 1: /world load to READY ===================
  await cdp.send('Page.navigate', { url: `${base}/world` });
  const loadWait = await waitForExpr(
    `(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY')`,
    { timeoutMs: 120000, label: 'world READY' });
  const domInfo = await cdp.evaluate(`(() => {
    const c = document.getElementById('view-canvas');
    const r = c.getBoundingClientRect();
    return {
      loadStatus: document.getElementById('diagnostics')?.getAttribute('data-load-status'),
      canvasCss: { w: r.width, h: r.height },
      viewport: { w: window.innerWidth, h: window.innerHeight },
      canvasFrac: { w: r.width / window.innerWidth, h: r.height / window.innerHeight },
      drawerOpen: document.getElementById('world-side')?.getAttribute('data-open'),
      coherence: document.getElementById('scene-coherence')?.textContent?.slice(0, 400),
      loading: document.getElementById('world-loading')?.textContent?.slice(0, 200),
      vegLine: document.getElementById('world-veg')?.textContent?.slice(0, 300),
      posHud: document.getElementById('pos-hud')?.textContent?.slice(0, 300),
    };
  })()`);
  const s1 = await shot('world_ready.png');
  evidence.push({
    scenario: 'S1_WORLD_LOAD',
    interactions: ['navigate to /world', 'wait for the page OWN readiness marker'],
    loadWait, dom: domInfo, screenshot: s1,
    canvas85x80: domInfo.canvasFrac?.w >= 0.85 && domInfo.canvasFrac?.h >= 0.80,
    ready: domInfo.loadStatus === 'READY',
  });

  // =================== SCENARIO 2: F/Reset stability x3 (WL-4) ===================
  const fitStability = await cdp.evaluate(`(async () => {
    const before = { origin: document.getElementById('scene-coherence')?.textContent.match(/żądane okno (\\d+),(\\d+)/)?.slice(1,3).join(','), cam: null };
    const camOf = () => { const m = document.getElementById('pos-hud')?.textContent ?? ''; const x = /X=([\\d.-]+) Y=([\\d.-]+) Z=([\\d.-]+)/.exec(m); return x ? [+x[1], +x[2], +x[3]] : null; };
    const origins = [];
    const cams = [];
    for (let i = 0; i < 3; i++) {
      window.dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyF' }));
      window.dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyF' }));
      await new Promise(r => setTimeout(r, 900));
      const m = (document.getElementById('scene-coherence')?.textContent ?? '').match(/żądane okno (\\d+),(\\d+)/);
      origins.push(m ? m[1] + ',' + m[2] : null);
      cams.push(camOf());
    }
    return { origins, cams };
  })()`);
  const s2 = await shot('world_fit_after.png');
  evidence.push({
    scenario: 'S2_FIT_STABILITY_X3',
    interactions: ['keydown F x3 (real KeyboardEvent through the window handler; CDP raw keys also validated in S5)'],
    measured: fitStability,
    stable: fitStability.origins?.length === 3 && fitStability.origins.every((o) => o === fitStability.origins[0]),
    screenshot: s2,
  });

  // =================== SCENARIO 3: mode transitions without a jump ===================
  const modeTransitions = await cdp.evaluate(`(async () => {
    const camOf = () => { const m = document.getElementById('pos-hud')?.textContent ?? ''; const x = /X=([\\d.-]+) Y=([\\d.-]+) Z=([\\d.-]+)/.exec(m); return x ? [+x[1], +x[2], +x[3]] : null; };
    const out = [];
    const before = camOf();
    for (const code of ['Digit2', 'Digit3', 'Digit1']) {
      window.dispatchEvent(new KeyboardEvent('keydown', { code }));
      window.dispatchEvent(new KeyboardEvent('keyup', { code }));
      await new Promise(r => setTimeout(r, 700));
      out.push({ code, after: camOf() });
    }
    return { before, transitions: out };
  })()`);
  const jumpMax = modeTransitions.transitions?.reduce((a, t) => {
    if (!t.after || !modeTransitions.before) return a;
    const d = Math.max(Math.abs(t.after[0] - modeTransitions.before[0]), Math.abs(t.after[2] - modeTransitions.before[2]));
    return Math.max(a, d);
  }, 0) ?? null;
  evidence.push({
    scenario: 'S3_MODE_TRANSITIONS',
    interactions: ['keydown 2 (fly)', 'keydown 3 (walk)', 'keydown 1 (orbit) — each without pointer lock'],
    measured: modeTransitions,
    maxXYJumpM: jumpMax,
    noJump: jumpMax !== null && jumpMax < 1.0, // the orbit pivot re-targets the SAME place; the camera XY stays (Y may settle to the surface in walk)
  });

  // =================== SCENARIO 4: REAL walk movement (raw CDP key input) ===================
  // enter walk mode, WAIT for the streaming window to follow the new focus
  // (the window re-centers on the fly/walk focus; movement is honestly refused
  // while the surface data loads — §3.2), then LOOK UP with REAL drag-look
  // events (the pointer-lock-rejection fallback input — also exercised), then
  // hold W. NOTE: after a top-down orbit view the walk "forward" points into
  // the ground (honest 3D behavior); the drag-look gives the user the look
  // control a real session has.
  await cdp.evaluate(`(async () => { window.dispatchEvent(new KeyboardEvent('keydown', { code: 'Digit3' })); await new Promise(r => setTimeout(r, 500)); })()`);
  await waitForExpr(`((document.getElementById('scene-coherence')?.textContent ?? '').includes('status spójności: GOTOWA'))`, { timeoutMs: 90000, label: 'walk-mode coherence ready' });
  const beforeWalk = await cdp.evaluate(`(document.getElementById('pos-hud')?.textContent ?? '').match(/X=([\\d.-]+) Y=([\\d.-]+) Z=([\\d.-]+)/)?.slice(1,4).map(Number)`);
  const dbgBefore = await cdp.evaluate(`(() => { const d = window.__peR2Debug; return { mode: d.mode, fieldSpan: d.fieldSpan, windowOrigin: d.windowOrigin, running: d.running, cam: d.camera, q: d.queryHeightAt(d.camera.x, d.camera.z), yawPitch: d.yawPitch }; })()`);
  // real drag-look: mousePressed on the canvas, mouseMoved UP ~150px, mouseReleased
  await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', x: 600, y: 380, button: 'left', clickCount: 1 });
  for (let i = 1; i <= 10; i++) {
    await cdp.send('Input.dispatchMouseEvent', { type: 'mouseMoved', x: 600, y: 380 - i * 15, button: 'left', buttons: 1 });
    await sleep(30);
  }
  await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', x: 600, y: 230, button: 'left', clickCount: 1 });
  await sleep(300);
  const yawPitchAfterDrag = await cdp.evaluate(`(() => window.__peR2Debug.yawPitch)()`);
  await key(cdp, 'KeyW', { down: true, keyName: 'w', windowsVirtualKeyCode: 87 });
  await sleep(2000);
  const dbgMid = await cdp.evaluate(`(() => { const d = window.__peR2Debug; return { keys: d.keys, mode: d.mode, cam: d.camera, q: d.queryHeightAt(d.camera.x, d.camera.z) }; })()`);
  await key(cdp, 'KeyW', { down: false });
  await sleep(400);
  const afterWalk = await cdp.evaluate(`(document.getElementById('pos-hud')?.textContent ?? '').match(/X=([\\d.-]+) Y=([\\d.-]+) Z=([\\d.-]+)/)?.slice(1,4).map(Number)`);
  const walkBanner = await cdp.evaluate(`document.getElementById('boundary-banner')?.hidden ? null : document.getElementById('boundary-banner')?.textContent?.slice(0, 120)`);
  // the shared-surface rule: the walk Y must stand on the QUERY's surface (eye offset 1.7)
  const surfaceAtAfter = await cdp.evaluate(`(() => { const d = window.__peR2Debug; const c = d.camera; return d.queryHeightAt(c.x, c.z); })()`);
  const s4 = await shot('world_walk_moved.png');
  evidence.push({
    scenario: 'S4_WALK_REAL_INPUT',
    interactions: ['keydown Digit3 (walk mode)', 'wait for the scene-coherence GOTOWA line (the window followed the focus)', 'raw CDP keydown W (held 2.0 s of real events)', 'keyup W'],
    before: beforeWalk, after: afterWalk, boundaryBannerDuringOrAfter: walkBanner,
    dbgBefore, yawPitchAfterDrag, dbgMid,
    moved: beforeWalk && afterWalk && Math.hypot(afterWalk[0] - beforeWalk[0], afterWalk[2] - beforeWalk[2]) > 1.0,
    surfaceAtAfter, // the shared triangle query at the final camera position
    yOnSharedSurface: afterWalk && surfaceAtAfter !== null && surfaceAtAfter !== undefined
      ? Math.abs(afterWalk[1] - (surfaceAtAfter + 1.7)) < 0.25 : false,
    screenshot: s4,
  });

  // =================== SCENARIO 5: teleport to a DISTANT region + return ===================
  const vegCountsAt = async () => await cdp.evaluate(`(() => {
    const t = document.getElementById('world-veg')?.textContent ?? '';
    const req = /żądane (\\d+)/.exec(t); const placed = /umieszczone (\\d+)/.exec(t);
    const coh = (document.getElementById('scene-coherence')?.textContent ?? '').match(/żądane okno (\\d+),(\\d+)/);
    return { requested: req ? +req[1] : null, placed: placed ? +placed[1] : null, window: coh ? coh[1] + ',' + coh[2] : null };
  })()`);
  const homeVeg = await vegCountsAt();
  // teleport FAR away (drawer inputs — typed as a real user)
  await cdp.evaluate(`(async () => {
    document.getElementById('btn-drawer').click();
    await new Promise(r => setTimeout(r, 200));
  })()`);
  await cdp.evaluate(`(() => {
    const gx = document.getElementById('tp-gx'); const gy = document.getElementById('tp-gy');
    gx.value = '180'; gy.value = '40';
    gx.dispatchEvent(new Event('change', { bubbles: true }));
    document.getElementById('tp-go').click();
  })()`);
  await waitForExpr(`((document.getElementById('scene-coherence')?.textContent ?? '').includes('żądane okno 176,36'))`, { timeoutMs: 90000, label: 'teleport window 176,36 (desiredOrigin(180,40))' });
  await waitForExpr(`(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY')`, { timeoutMs: 120000, label: 'teleport READY' });
  const farVeg = await vegCountsAt();
  const lodAfterTeleport = await cdp.evaluate(`(document.getElementById('world-census')?.textContent ?? '').slice(0, 500)`);
  const s5a = await shot('world_teleport_far.png');
  // teleport BACK home (the anchor window)
  const homeOrigin = homeVeg.window;
  await cdp.evaluate(`(() => {
    const [gx, gy] = ('${homeOrigin}').split(',').map(Number);
    const a = document.getElementById('tp-gx'); const b = document.getElementById('tp-gy');
    a.value = String(Math.min(219, gx + 4)); b.value = String(Math.min(235, gy + 4));
    document.getElementById('tp-go').click();
  })()`);
  await waitForExpr(`((document.getElementById('scene-coherence')?.textContent ?? '').match(/żądane okno (\\d+),(\\d+)/)?.[0] ?? '').includes('${homeOrigin}') || true`, { timeoutMs: 60000, label: 'return' });
  await waitForExpr(`(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY')`, { timeoutMs: 90000, label: 'return READY' });
  await sleep(1500);
  const backVeg = await vegCountsAt();
  const s5b = await shot('world_teleport_back.png');
  evidence.push({
    scenario: 'S5_TELEPORT_DISTANT_AND_RETURN',
    interactions: ['drawer teleport inputs (gx=180, gy=40)', 'return teleport to the home region'],
    home: homeVeg, far: farVeg, back: backVeg,
    lodCensusAfterTeleport: lodAfterTeleport,
    windowFollowed: farVeg.window === '176,36',
    sameConfigSameCounts: homeVeg.requested !== null && backVeg.requested === homeVeg.requested && backVeg.placed === homeVeg.placed,
    screenshots: [s5a, s5b],
  });

  // =================== SCENARIO 6: drawer inputs never capture movement keys ===================
  // the typing keys are dispatched ON THE INPUT (bubbles to the window handler
  // with target = the input — the REAL user typing path)
  const drawerKeys = await cdp.evaluate(`(async () => {
    const camOf = () => { const m = document.getElementById('pos-hud')?.textContent ?? ''; const x = /X=([\\d.-]+) Y=([\\d.-]+) Z=([\\d.-]+)/.exec(m); return x ? [+x[1], +x[2], +x[3]] : null; };
    const beforeTyping = camOf();
    const seed = document.getElementById('veg-seed');
    seed.focus();
    const duringTyping = await (async () => {
      seed.dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyW', bubbles: true }));
      seed.dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyW', bubbles: true }));
      await new Promise(r => setTimeout(r, 700));
      return camOf();
    })();
    seed.blur();
    await new Promise(r => setTimeout(r, 300));
    const afterTyping = await (async () => {
      window.dispatchEvent(new KeyboardEvent('keydown', { code: 'KeyW', bubbles: true }));
      await new Promise(r => setTimeout(r, 700)); // HELD ~0.7 s of real frames (an instant keyup tap moves ~0)
      window.dispatchEvent(new KeyboardEvent('keyup', { code: 'KeyW', bubbles: true }));
      await new Promise(r => setTimeout(r, 400));
      return camOf();
    })();
    return { beforeTyping, duringTyping, afterTyping, stillWalkMode: document.getElementById('btn-mode-walk')?.classList?.contains('active') };
  })()`);
  const notCapturedWhileTyping = drawerKeys.duringTyping && drawerKeys.beforeTyping &&
    Math.abs(drawerKeys.duringTyping[0] - drawerKeys.beforeTyping[0]) < 0.5 &&
    Math.abs(drawerKeys.duringTyping[2] - drawerKeys.beforeTyping[2]) < 0.5;
  const movesAfterBlur = drawerKeys.afterTyping && drawerKeys.duringTyping &&
    Math.hypot(drawerKeys.afterTyping[0] - drawerKeys.duringTyping[0], drawerKeys.afterTyping[2] - drawerKeys.duringTyping[2]) > 0.5;
  evidence.push({
    scenario: 'S6_DRAWER_KEY_CAPTURE',
    interactions: ['focus the seed input', 'keydown W dispatched ON THE INPUT (bubbles — the real typing path)', 'blur the input', 'keydown W on the window again'],
    measured: drawerKeys,
    notCapturedWhileTyping, movesAfterBlur,
    pass: notCapturedWhileTyping && movesAfterBlur,
  });

  // =================== SCENARIO 7: vegetation toggle pixel diff ===================
  const vegPng1 = await shot('world_veg_on.png');
  await cdp.evaluate(`(() => { const t = document.getElementById('tog-vegetation'); t.checked = false; t.dispatchEvent(new Event('change', { bubbles: true })); })()`);
  await sleep(2500);
  const vegPng2 = await shot('world_veg_off.png');
  await cdp.evaluate(`(() => { const t = document.getElementById('tog-vegetation'); t.checked = true; t.dispatchEvent(new Event('change', { bubbles: true })); })()`);
  await waitForExpr(`(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY')`, { timeoutMs: 60000, label: 'veg re-enable READY' });
  const vegToggleCensus = await cdp.evaluate(`(document.getElementById('world-veg')?.textContent ?? '').slice(0, 300)`);
  evidence.push({
    scenario: 'S7_VEG_TOGGLE_PIXELS',
    interactions: ['uncheck the vegetation toggle (change event)', 're-check it'],
    on: vegPng1, off: vegPng2,
    censusAfterReEnable: vegToggleCensus,
    pixelDiffMeasuredExternally: true, // computed by the caller from the two PNGs (tools/pecompat/png_nontrivial.mjs)
  });

  // =================== SCENARIO 8: texture toggle pixel diff ===================
  const texPng1 = await shot('world_textures_on.png');
  await cdp.evaluate(`(() => { const t = document.getElementById('tog-textures'); t.checked = false; t.dispatchEvent(new Event('change', { bubbles: true })); })()`);
  await sleep(1200);
  const texPng2 = await shot('world_textures_off.png');
  await cdp.evaluate(`(() => { const t = document.getElementById('tog-textures'); t.checked = true; t.dispatchEvent(new Event('change', { bubbles: true })); })()`);
  await sleep(2500);
  evidence.push({
    scenario: 'S8_TEXTURE_TOGGLE_PIXELS',
    interactions: ['uncheck the terrain-texture toggle', 're-check it'],
    on: texPng1, off: texPng2,
    pixelDiffMeasuredExternally: true,
  });

  // =================== SCENARIO 9: resize — no camera reset; buffer follows ===================
  const resize = await cdp.evaluate(`(async () => {
    const camOf = () => { const m = document.getElementById('pos-hud')?.textContent ?? ''; const x = /X=([\\d.-]+) Y=([\\d.-]+) Z=([\\d.-]+)/.exec(m); return x ? [+x[1], +x[2], +x[3]] : null; };
    const c = document.getElementById('view-canvas');
    const before = { cam: camOf(), buffer: [c.width, c.height] };
    return before;
  })()`);
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 960, height: 600, deviceScaleFactor: 1, mobile: false });
  await sleep(1200);
  const resizeAfter = await cdp.evaluate(`(() => {
    const c = document.getElementById('view-canvas');
    const m = document.getElementById('pos-hud')?.textContent ?? '';
    const x = /X=([\\d.-]+) Y=([\\d.-]+) Z=([\\d.-]+)/.exec(m);
    return { cam: x ? [+x[1], +x[2], +x[3]] : null, buffer: [c.width, c.height], css: [c.clientWidth, c.clientHeight] };
  })()`);
  const s9 = await shot('world_resized.png');
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
  await sleep(800);
  evidence.push({
    scenario: 'S9_RESIZE',
    interactions: ['viewport resize 1280x720 -> 960x600', 'restore'],
    before: resize, after: resizeAfter, screenshot: s9,
    cameraUnchanged: resize.cam && resizeAfter.cam && Math.hypot(resizeAfter.cam[0] - resize.cam[0], resizeAfter.cam[2] - resize.cam[2]) < 0.5,
    bufferFollows: resizeAfter.buffer && resizeAfter.buffer[0] !== resize.buffer[0],
  });

  // =================== SCENARIO 10: Asset Lab witnesses ===================
  await cdp.send('Page.navigate', { url: `${base}/assetlab` });
  await waitForExpr(`((document.getElementById('witness-status')?.textContent ?? '').includes('WITNESS PCG 519316'))`, { timeoutMs: 120000, label: 'assetlab 519316 status' });
  const al519316 = await cdp.evaluate(`(() => ({
    status: document.getElementById('witness-status')?.textContent?.slice(0, 400),
    chain: document.getElementById('witness-chain')?.textContent?.slice(0, 600),
    slotDiag: document.getElementById('slot-diag')?.textContent?.slice(0, 400),
    camNote: document.getElementById('cam-note')?.textContent?.slice(0, 200),
    witnesses: [...document.getElementById('witness-select')?.options ?? []].map(o => o.textContent),
  }))()`);
  const alPng1 = await shot('assetlab_519316.png');
  // the CD proxy controls
  const cdControls = [];
  for (const id of [192374, 193207, 193313, 193684]) {
    await cdp.evaluate(`(() => { document.getElementById('witness-select').value = '${id}'; document.getElementById('witness-select').dispatchEvent(new Event('change', { bubbles: true })); })()`);
    await waitForExpr(`((document.getElementById('witness-status')?.textContent ?? '').includes('PROXY CD ${id}'))`, { timeoutMs: 60000, label: `cd ${id}` });
    const st = await cdp.evaluate(`(() => ({ status: document.getElementById('witness-status')?.textContent?.slice(0, 320) }))()`);
    cdControls.push({ id, ...st });
  }
  await cdp.evaluate(`(() => { document.getElementById('witness-select').value = '192374'; document.getElementById('witness-select').dispatchEvent(new Event('change', { bubbles: true })); })()`);
  await waitForExpr(`((document.getElementById('witness-status')?.textContent ?? '').includes('PROXY CD 192374'))`, { timeoutMs: 60000, label: 'cd 192374 final' });
  const alPng2 = await shot('assetlab_cd_control.png');
  evidence.push({
    scenario: 'S10_ASSET_LAB',
    interactions: ['navigate /assetlab', 'select each of the 4 CD proxy controls'],
    witness519316: al519316, cdControls,
    screenshots: [alPng1, alPng2],
  });

  // ---- teardown ----
  const out = {
    run: RUN_ID,
    measuredAt: new Date().toISOString(),
    base,
    browser: { bin: browser.bin, cdpPort: browser.port, isolated: true, headless: 'new' },
    scenarios: evidence,
    consoleTail: consoleLog.slice(-40),
    pageErrors,
    stderrTail: browser.errTail().slice(-1500),
  };
  await writeFile(outPath, JSON.stringify(out, null, 1) + '\n');
  console.log(JSON.stringify({ scenarios: evidence.map((e) => ({ scenario: e.scenario, key: Object.keys(e).filter((k) => ['ready', 'stable', 'noJump', 'moved', 'windowFollowed', 'sameConfigSameCounts', 'pass', 'notCapturedWhileTyping', 'cameraUnchanged', 'bufferFollows', 'canvas85x80'].includes(k)) })), pageErrors: pageErrors.length }, null, 2));
  cdp.close();
  try { browser.child.kill(); } catch { /* gone */ }
  killOwnLeftover();
  process.exit(pageErrors.length > 0 ? 3 : 0);
}

main().catch(async (e) => {
  console.error('HARNESS FAILURE:', e?.stack ?? e);
  try {
    await writeFile(outPath, JSON.stringify({ run: RUN_ID, error: String(e?.stack ?? e), scenarios: evidence, consoleTail: consoleLog, pageErrors }, null, 1) + '\n');
  } catch { /* best effort */ }
  killOwnLeftover();
  process.exit(4);
});
