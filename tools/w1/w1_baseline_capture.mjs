#!/usr/bin/env node
// w1_baseline_capture.mjs — PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031 / W1-1
// Baseline capture LIVE 8163 (READ-ONLY: no server restart, no Stop-Process, no BASE mutation).
// Isolated headless Edge + CDP on a FREE port (never the 9222 daemon), pattern: BASE
// tools/pecompat/world_r2_browser.mjs. Identical viewport 1280x720 DPR=1 for ALL frames.
// Frames: (a) ground close, (b) top-down tiles, (c) low horizon, (d) near/mid/far,
// (e) teleport far (evict) -> return home (same tiles). PNG + JSON metrics per frame.
// Plus: server-side material chain census over the ACTIVE 8x8 window (+after move).
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import os from 'node:os';
import net from 'node:net';
import path from 'node:path';

const here = path.dirname(new URL(import.meta.url).href.replace(/^file:\/\/\//, ''));
const BASE = 'http://127.0.0.1:8163';
const OUT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031\\W1_TERRAIN_MATERIALS\\baseline';
const PROFILE_MARK = 'pec-w1-baseline-8163';
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
    for (let p = 21000; p < 21100; p++) { if (p === 9222) continue; if (await tryPort(p)) return p; }
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
      setTimeout(() => { if (this.pending.has(id)) { this.pending.delete(id); reject(new Error(`CDP timeout: ${method}`)); } }, 60000);
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

// ---- per-frame capture: PNG + JSON metrics (identical viewport/DPR for ALL frames) ----
async function frame(cdp, name, notes) {
  const metrics = await cdp.evaluate(`(() => {
    const c = document.getElementById('view-canvas');
    const m = document.getElementById('pos-hud')?.textContent ?? '';
    const p = /X=([\\d.-]+) Y=([\\d.-]+) Z=([\\d.-]+)/.exec(m);
    const cen = document.getElementById('world-census')?.textContent ?? '';
    const ev = document.getElementById('world-evidence')?.textContent ?? '';
    const spl = /resolved (\\d+)\\/(\\d+) warstw, zdekodowane (\\d+), zastosowane (\\d+)/.exec(cen);
    const spl2 = /okno: resolved (\\d+)\\/(\\d+) \\| zdekodowane (\\d+) \\| zastosowane (\\d+)/.exec(ev);
    const dr = /draw calls (\\d+), tr\\u00f3jk\\u0105ty (\\d+), tekstury (\\d+), geometrie (\\d+)/.exec(cen);
    const fetches = /pobrania: (\\d+) \\| b\\u0142\\u0119dy: (\\d+)/.exec(cen);
    const matFetches = /fetch materia\\u0142\\u00f3w: (\\d+) \\(b\\u0142\\u0119dy (\\d+)\\) \\| fetch tekstur: (\\d+) \\(b\\u0142\\u0119dy (\\d+)\\)/.exec(cen);
    const cacheN = /cache klienta: (\\d+) kafli/.exec(cen);
    const texCache = /cache tekstur RGBA: (\\d+)/.exec(cen);
    const coh = (document.getElementById('scene-coherence')?.textContent ?? '').match(/\\u017c\\u0105dane okno (\\d+),(\\d+)/);
    const d = window.__peR2Debug;
    return {
      cam: d ? d.camera : null, posHud: p ? p.slice(1, 4).map(Number) : null,
      mode: d ? d.mode : null, windowOrigin: d ? d.windowOrigin : null,
      coherenceWindow: coh ? [ +coh[1], +coh[2] ] : null,
      loadStatus: document.getElementById('diagnostics')?.getAttribute('data-load-status'),
      coherenceText: (document.getElementById('scene-coherence')?.textContent ?? '').slice(0, 300),
      drawcalls: dr ? +dr[1] : null, triangles: dr ? +dr[2] : null,
      texturesMem: dr ? +dr[3] : null, geometriesMem: dr ? +dr[4] : null,
      fetches: fetches ? { count: +fetches[1], errors: +fetches[2] } : null,
      materialFetches: matFetches ? { materials: +matFetches[1], materialsErrors: +matFetches[2], textures: +matFetches[3], textureErrors: +matFetches[4] } : null,
      tileCacheSize: cacheN ? +cacheN[1] : null, rgbaCacheSize: texCache ? +texCache[1] : null,
      splatCensusLine: spl ? { resolved: +spl[1], layersTotal: +spl[2], decoded: +spl[3], applied: +spl[4] } : null,
      splatEvidenceLine: spl2 ? { resolved: +spl2[1], layersTotal: +spl2[2], decoded: +spl2[3], applied: +spl2[4] } : null,
      censusRaw: cen, dpr: window.devicePixelRatio, viewport: { w: innerWidth, h: innerHeight },
      buffer: c ? { w: c.width, h: c.height } : null,
      vegLine: (document.getElementById('world-veg')?.textContent ?? '').slice(0, 200),
    };
  })()`);
  const buf = await cdp.screenshot();
  const file = `${name}.png`;
  await writeFile(path.join(OUT, file), buf);
  const rec = { frame: name, notes, capturedAt: new Date().toISOString(), viewport: { w: 1280, h: 720, deviceScaleFactor: 1 }, ...metrics, png: { file, bytes: buf.length, sha256: hash(buf) } };
  await writeFile(path.join(OUT, `${name}.json`), JSON.stringify(rec, null, 1));
  return rec;
}

// ---- server-side material chain census for an 8x8 window (read-only GETs) ----
async function materialChainWindow(origin) {
  const perTile = [];
  let expected = 0, resolved = 0, missing = [];
  for (let ty = 0; ty < 8; ty++) {
    for (let tx = 0; tx < 8; tx++) {
      const gx = origin.gx + tx, gy = origin.gy + ty;
      try {
        const r = await fetch(`${BASE}/api/world/tile/${gx}/${gy}/materials`);
        if (!r.ok) { perTile.push({ gx, gy, http: r.status }); missing.push({ tile: `${gx}/${gy}`, reason: `HTTP ${r.status}` }); continue; }
        const j = await r.json();
        const mats = j.materials ?? [];
        expected += mats.length;
        for (const m of mats) {
          if (m.texture?.resolved === true) resolved++;
          else missing.push({ tile: `${gx}/${gy}`, id: m.id, name: m.name, reason: m.texture?.reason ?? 'UNRESOLVED binding' });
        }
        perTile.push({ gx, gy, layers: mats.length });
      } catch (e) { perTile.push({ gx, gy, error: String(e?.message ?? e) }); missing.push({ tile: `${gx}/${gy}`, reason: `FETCH_FAILED ${e?.message}` }); }
    }
  }
  return { origin, expected, resolved, missing, perTile };
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
async function key(cdp, code, down) {
  await cdp.send('Input.dispatchKeyEvent', { type: down ? 'rawKeyDown' : 'keyUp', key: code.startsWith('Key') ? code.slice(3).toLowerCase() : code, code, windowsVirtualKeyCode: 0 });
}
async function press(cdp, code) { await key(cdp, code, true); await sleep(80); await key(cdp, code, false); await sleep(150); }

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

const frames = [];
const chain = {};

// ---- load /world ----
await cdp.send('Page.navigate', { url: `${BASE}/world` });
const loadWait = await waitForExpr(cdp, `(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY')`);
const homeOrigin = await cdp.evaluate(`window.__peR2Debug.windowOrigin`);
frames.push(await frame(cdp, 'f0_world_ready', 'initial load, orbit default framing'));
chain.home = await materialChainWindow(homeOrigin);

// ---- (a) ground detail CLOSE: walk mode (eye 1.7m above surface), look down-forward ----
await press(cdp, 'Digit3'); // walk mode
await waitForExpr(cdp, `((document.getElementById('scene-coherence')?.textContent ?? '').includes('GOTOWA'))`, 90000);
await dragLook(cdp, 0, 180); // pitch look down
await sleep(400);
frames.push(await frame(cdp, 'fa_ground_close_walk', 'walk mode, eye on shared surface, look-down angle'));
await dragLook(cdp, 0, -180); // restore pitch

// ---- (b) top-down several tiles: orbit mode, drag-rotate to top-down + moderate zoom ----
await press(cdp, 'Digit1'); // orbit
await sleep(400);
await dragLook(cdp, 0, -220); // orbit drag up -> camera swings toward top-down
await wheelZoom(cdp, -4);    // zoom out a bit to see several tiles
frames.push(await frame(cdp, 'fb_topdown_tiles', 'orbit, camera high above target (top-down-ish), several tiles'));
// restore
await dragLook(cdp, 0, 220);

// ---- (c) low horizon angle: orbit drag to near-horizontal, low distance ----
await wheelZoom(cdp, 6); // zoom in close
await dragLook(cdp, 0, 120); // swing camera low near horizon
frames.push(await frame(cdp, 'fc_low_horizon', 'orbit, low camera angle near horizon'));
await dragLook(cdp, 0, -120);

// ---- (d) near/mid/far together: zoom far out ----
await wheelZoom(cdp, -18);
frames.push(await frame(cdp, 'fd_near_mid_far', 'orbit zoomed out: near window + mid LOD ring + far world'));
await wheelZoom(cdp, 14);

// ---- (e) movement -> evict -> return: teleport far, return, SAME tiles ----
const farHome = await cdp.evaluate(`(() => { document.getElementById('btn-drawer').click(); return true; })()`);
await sleep(300);
await cdp.evaluate(`(() => { const a = document.getElementById('tp-gx'), b = document.getElementById('tp-gy'); a.value = '180'; b.value = '40'; a.dispatchEvent(new Event('change', { bubbles: true })); document.getElementById('tp-go').click(); })()`);
await waitForExpr(cdp, `((document.getElementById('scene-coherence')?.textContent ?? '').includes('\\u017c\\u0105dane okno 176,36'))`, 90000);
await waitForExpr(cdp, `(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY')`, 120000);
frames.push(await frame(cdp, 'fe1_teleport_far', 'teleported to tile 180,40 (window 176,36) — far region'));
chain.far = await materialChainWindow({ gx: 176, gy: 36 });

// return home (same window as the baseline frames)
await cdp.evaluate(`(() => { const a = document.getElementById('tp-gx'), b = document.getElementById('tp-gy'); a.value = '${homeOrigin.gx + 4}'; b.value = '${homeOrigin.gy + 4}'; a.dispatchEvent(new Event('change', { bubbles: true })); document.getElementById('tp-go').click(); })()`);
await waitForExpr(cdp, `((document.getElementById('scene-coherence')?.textContent ?? '').match(/\\u017c\\u0105dane okno (\\d+),(\\d+)/)?.[1] === '${homeOrigin.gx}' || document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY')`, 90000);
await waitForExpr(cdp, `(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY')`, 120000);
await sleep(1500);
frames.push(await frame(cdp, 'fe2_return_home', 'returned to the home window — SAME tiles re-displayed after movement/evict cycle'));
chain.backHome = await materialChainWindow(homeOrigin);

const out = {
  run: 'PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031/W1-1',
  capturedAt: new Date().toISOString(), base: BASE,
  browser: { bin: browser.bin, cdpPort: browser.port, isolated: true, headless: 'new', profileMark: PROFILE_MARK },
  fixedCaptureConfig: { viewport: '1280x720', deviceScaleFactor: 1, dprExpected: 1 },
  loadWait, homeWindowOrigin: homeOrigin,
  frames, materialChain: chain,
  consoleTail: consoleLog.slice(-30), pageErrors,
};
await writeFile(path.join(OUT, '..', 'BASELINE_CAPTURE_SUMMARY.json'), JSON.stringify(out, null, 1));
await writeFile(path.join(OUT, '..', 'MATERIAL_CHAIN_COUNTS.json'), JSON.stringify({
  home: { origin: chain.home.origin, expected: chain.home.expected, resolved: chain.home.resolved, missing: chain.home.missing.length, missingDetail: chain.home.missing },
  far: { origin: chain.far.origin, expected: chain.far.expected, resolved: chain.far.resolved, missing: chain.far.missing.length, missingDetail: chain.far.missing },
  backHome: { origin: chain.backHome.origin, expected: chain.backHome.expected, resolved: chain.backHome.resolved, missing: chain.backHome.missing.length, missingDetail: chain.backHome.missing },
  perTile: { home: chain.home.perTile, far: chain.far.perTile },
}, null, 1));
console.log(JSON.stringify({ frames: frames.map((f) => ({ frame: f.frame, cam: f.cam, drawcalls: f.drawcalls, triangles: f.triangles, splat: f.splatCensusLine, coherenceWindow: f.coherenceWindow })), chain: { home: { o: chain.home.origin, exp: chain.home.expected, res: chain.home.resolved, miss: chain.home.missing.length }, far: { o: chain.far.origin, exp: chain.far.expected, res: chain.far.resolved, miss: chain.far.missing.length }, back: { exp: chain.backHome.expected, res: chain.backHome.resolved, miss: chain.backHome.missing.length } }, pageErrors: pageErrors.length }, null, 1));
cdp.close();
try { browser.child.kill(); } catch { /* gone */ }
killOwnLeftover();
process.exit(0);
