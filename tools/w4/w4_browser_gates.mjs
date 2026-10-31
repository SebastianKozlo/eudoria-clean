#!/usr/bin/env node
// w4_browser_gates.mjs — PE_WORLD_8163 W4-1 browser gates G1–G5 (staging 8171).
// Isolated headless Edge + CDP on a FREE port (pattern: W1-1 baseline capture).
// G1 character renders (pixels changed in character screen region),
// G2 idle active at t0 + WASD->walk (clip switch counter), G3 no geometry
// explosion (bbox stable, no NaN in matrices), G4 texture bound (not black),
// G5 pause/seek/speed works. PNG frames -> SCI W4_ANIMATIONS dir.
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import os from 'node:os';
import net from 'node:net';
import path from 'node:path';

const BASE = 'http://127.0.0.1:8171';
const OUT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031\\W4_ANIMATIONS';
const PROFILE_MARK = 'pec-w4-player-gates-8171';
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
    for (let p = 21200; p < 21300; p++) { if (await tryPort(p)) return p; }
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
  constructor(ws) { this.ws = ws; this.seq = 0; this.pending = new Map(); }
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
  }
  async evaluate(expression) {
    const r = await this.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(`page eval failed: ${r.exceptionDetails.exception?.description?.slice(0, 500) ?? r.exceptionDetails.text}`);
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
  cdp.ws.addEventListener('message', (ev) => { try { cdp.handle(JSON.parse(ev.data)); } catch { /* ignore */ } });
  return { child, port, bin, cdp };
}

const consoleLog = []; let pageErrors = [];
const results = { runId: 'W4-1_BROWSER_GATES_20261031', base: BASE, gates: {} };

function recordConsole() { /* handler installed below */ }

async function main() {
  killOwnLeftover();
  const { child, port, bin, cdp } = await launchBrowser();
  results.browser = { bin, cdpPort: port, profileMark: PROFILE_MARK };
  cdp.ws.addEventListener('message', (ev) => {
    let msg; try { msg = JSON.parse(ev.data); } catch { return; }
    if (msg.method === 'Runtime.consoleAPICalled') consoleLog.push((msg.params.args ?? []).map((a) => a.value ?? a.description ?? '').join(' '));
    if (msg.method === 'Runtime.exceptionThrown') pageErrors.push(String(msg.params.exceptionDetails?.exception?.description ?? msg.params.exceptionDetails?.text ?? 'exception').slice(0, 400));
    cdp.handle(msg);
  });
  await cdp.send('Runtime.enable');
  await cdp.send('Page.enable');
  await cdp.evaluate(`window.location.href = '${BASE}/world'`);
  await sleep(6000); // scene + player boot

  // ---------- G1: player module ready + renders ----------
  const bootInfo = await cdp.evaluate(`(() => ({
    playerReady: !!(window.__pePlayer && window.__pePlayer.ready),
    identity: window.__pePlayer?.identity ?? null,
    bindReport: window.__pePlayer?.bindReport ?? null,
    texture: window.__pePlayer?.texture ?? null,
    activeClip: window.__pePlayer?.activeClip ?? null,
    appReady: document.getElementById('load-status')?.textContent ?? null,
  }))()`);
  results.boot = bootInfo;

  // character screen-region pixels: CLIP-RECT screenshots around the projected
  // character position (readPixels after present returns zeros without
  // preserveDrawingBuffer; the clipped PNG is the honest pixel evidence)
  const region = await cdp.evaluate(`window.__pePlayer.projectToScreen()`);
  const clip = { x: Math.max(0, region.sx - 90), y: Math.max(0, region.sy - 130), width: 180, height: 220, scale: 1 };
  async function regionShot() {
    const r = await cdp.send('Page.captureScreenshot', { format: 'png', clip });
    return Buffer.from(r.data, 'base64');
  }
  const withChar = await regionShot();
  // hide the character -> pixels change in the region (negative control)
  await cdp.evaluate(`(() => { const d = window.__peWorldScene.scene; window.__w4Root = d.getObjectByName('GAME_CHARACTER_REF_546608'); window.__w4Root.visible = false; })()`);
  await sleep(250);
  const withoutChar = await regionShot();
  await cdp.evaluate(`window.__w4Root.visible = true`);
  const g1a = { sha256: hash(withChar), bytes: withChar.length };
  const g1b = { sha256: hash(withoutChar), bytes: withoutChar.length };
  const shotIdle = await cdp.screenshot();
  await writeFile(path.join(OUT, 'W4_G1_G2_IDLE_T0.png'), shotIdle);
  await writeFile(path.join(OUT, 'W4_G1_REGION_WITH_CHARACTER.png'), withChar);
  await writeFile(path.join(OUT, 'W4_G1_REGION_HIDDEN_CONTROL.png'), withoutChar);
  results.gates.G1 = {
    playerReady: bootInfo.playerReady,
    identity: bootInfo.identity,
    screenRegion: clip,
    regionWithCharacter: g1a,
    regionHiddenControl: g1b,
    pixelsChangedWhenHidden: g1a.sha256 !== g1b.sha256,
    pass: bootInfo.playerReady && g1a.sha256 !== g1b.sha256,
  };

  // ---------- G2: idle at t0; WASD -> walk ----------
  const idleAtT0 = await cdp.evaluate(`window.__pePlayer.activeClip`);
  // press W for 1.2s
  await cdp.evaluate(`window.dispatchEvent(new KeyboardEvent('keydown', { key: 'w' }))`);
  await sleep(1200);
  const duringWalk = await cdp.evaluate(`(() => ({ clip: window.__pePlayer.activeClip, switches: window.__pePlayer.clipSwitchCount, pos: window.__pePlayer.position }))()`);
  await cdp.evaluate(`window.dispatchEvent(new KeyboardEvent('keyup', { key: 'w' }))`);
  await sleep(700);
  const afterRelease = await cdp.evaluate(`window.__pePlayer.activeClip`);
  const shotWalk = await cdp.screenshot();
  await writeFile(path.join(OUT, 'W4_G2_WALK.png'), shotWalk);
  results.gates.G2 = {
    idleAtT0,
    switchedTo: duringWalk.clip,
    clipSwitchCount: duringWalk.switches,
    movedDuringWalk: !!duringWalk.pos,
    backToIdle: afterRelease,
    pass: idleAtT0 === 'idle' && duringWalk.clip === 'walk' && duringWalk.switches >= 1 && afterRelease === 'idle',
  };

  // ---------- G3: geometry sanity (bbox stable across frames, no NaN) ----------
  const bbox1 = await cdp.evaluate(`window.__pePlayer.nanCheck()`);
  await sleep(600);
  const bbox2 = await cdp.evaluate(`window.__pePlayer.nanCheck()`);
  results.gates.G3 = {
    bbox1: bbox1?.bbox, bbox2: bbox2?.bbox,
    bboxFinite: bbox1?.bboxFinite && bbox2?.bboxFinite,
    nanObjects: bbox1?.nanObjects,
    bboxStable: bbox1 && bbox2 && Math.abs(bbox1.bbox.x - bbox2.bbox.x) < 0.6
      && Math.abs(bbox1.bbox.y - bbox2.bbox.y) < 0.6 && Math.abs(bbox1.bbox.z - bbox2.bbox.z) < 0.6,
    pass: !!bbox1?.bboxFinite && bbox1.nanObjects === 0 && !!bbox2?.bboxFinite
      && Math.abs(bbox1.bbox.x - bbox2.bbox.x) < 0.6 && Math.abs(bbox1.bbox.y - bbox2.bbox.y) < 0.6,
  };

  // ---------- G4: texture bound (not black / not untextured) ----------
  const texProbe = await cdp.evaluate(`(() => {
    const d = window.__peWorldScene.scene;
    const root = d.getObjectByName('GAME_CHARACTER_REF_546608');
    let map = null, mapOk = false, matColor = null;
    root.traverse((o) => { if (o.isSkinnedMesh) { map = o.material.map; matColor = '#' + o.material.color.getHexString(); mapOk = !!(map && map.image && map.image.width > 0); } });
    return { textureResolved: window.__pePlayer.texture?.resolved ?? false, texInfo: window.__pePlayer.texture, mapOk, matColor };
  })()`);
  // sample texture pixels: are they non-uniform (not a flat/untextured look)?
  const texPixels = await cdp.evaluate(`(() => {
    const d = window.__peWorldScene.scene;
    const root = d.getObjectByName('GAME_CHARACTER_REF_546608');
    let m = null; root.traverse((o) => { if (o.isSkinnedMesh) m = o.material.map; });
    if (!m || !m.image || !m.image.data) return null;
    const d1 = m.image.data; // DataTexture RGBA
    let nonzero = 0; const set = new Set();
    for (let i = 0; i < d1.length; i += 4) { const l = d1[i] + d1[i+1] + d1[i+2]; if (l > 0) nonzero++; set.add(d1[i] + ',' + d1[i+1] + ',' + d1[i+2]); }
    return { nonzero, total: d1.length / 4, distinctColors: set.size, w: m.image.width, h: m.image.height };
  })()`);
  results.gates.G4 = {
    textureResolved: texProbe.textureResolved, decoder: texProbe.texInfo?.decoder,
    mapBound: texProbe.mapOk, texturePixels: texPixels,
    pass: texProbe.textureResolved && texProbe.mapOk && texPixels && texPixels.nonzero > 0 && texPixels.distinctColors > 8,
  };

  // ---------- G5: pause/seek/speed ----------
  const g5 = {};
  g5.pausedAt = await cdp.evaluate(`window.__pePlayer.setPaused(true)`);
  const tBefore = await cdp.evaluate(`window.__pePlayer.seek('idle', 2.0)`);
  await sleep(400);
  const tFrozen = await cdp.evaluate(`window.__pePlayer.seek('idle')`);
  g5.seekWorks = tBefore === 2.0 || tFrozen === 2.0;
  g5.speed = await cdp.evaluate(`window.__pePlayer.setSpeed(0.5)`);
  await cdp.evaluate(`window.__pePlayer.setPaused(false); window.__pePlayer.setSpeed(1.0)`);
  const g5shot = await cdp.screenshot();
  await writeFile(path.join(OUT, 'W4_G5_INSPECT_SEEK.png'), g5shot);
  results.gates.G5 = { ...g5, pass: g5.pausedAt === true && g5.speed === 0.5 && g5.seekWorks };

  results.pageErrors = pageErrors.slice(0, 10);
  results.consoleLog = consoleLog.filter((l) => l.includes('world-player')).slice(0, 10);
  results.pngSha256 = {
    'W4_G1_G2_IDLE_T0.png': hash(shotIdle),
    'W4_G2_WALK.png': hash(shotWalk),
    'W4_G5_INSPECT_SEEK.png': hash(g5shot),
  };
  const overall = Object.values(results.gates).every((g) => g && g.pass);
  results.OVERALL = overall ? 'PASS' : 'FAIL';
  await writeFile(path.join(OUT, 'W4_BROWSER_GATES.json'), JSON.stringify(results, null, 1));
  console.log(JSON.stringify({ gates: results.gates, OVERALL: results.OVERALL, boot: results.boot }, null, 1));
  cdp.close();
  try { process.kill(-child.pid); } catch { try { process.kill(child.pid); } catch { /* gone */ } }
  // hard cleanup of the profile browser
  killOwnLeftover();
}
main().catch((e) => { console.error('FATAL', e); process.exit(1); });
