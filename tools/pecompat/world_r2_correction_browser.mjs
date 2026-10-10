#!/usr/bin/env node
// world_r2_correction_browser.mjs — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010
// CORRECTION ROUND browser re-verify (P1-2; contract §8/§10 mandatory sequence
// "browser re-verify of the world page (veg coherence scenario: switch region
// while veg building)").
//
// THE SCENARIO (the QC-required production race, in the LIVE browser):
//   1. load /world with the DEFAULT config and wait for the page OWN
//      all-coherent marker (boot COMPLETE; the focus-follow streaming tick is
//      running);
//   2. WARM-UP: teleport to the distant target B=(200,200) through the REAL
//      teleport UI, wait for B coherent (its window tiles + textures cached),
//      then teleport home and wait coherent again;
//   3. THE RACE: apply veg config A (global profile 1, density 50 — 10 COLD
//      textured models) through the REAL drawer apply button; the apply
//      handler calls rebuildVegetation DIRECTLY (no terrain latency), so the
//      A build starts immediately (running.vegBusy === true);
//   4. WHILE the A build is in flight, apply veg config B (global profile 2)
//      through the REAL apply button — a NEWER CONFIG requested while the
//      rebuild is busy: the wrapper must STORE it (running.vegPending
//      non-null with B's request id — the direct LIVE proof of the P1-2 fix;
//      the b4dfae7 wrapper returned null and LOST it);
//   5. WHILE the builds are still in flight, SWITCH REGION: teleport to the
//      pre-warmed B through the REAL teleport UI (the focus moves; the
//      streaming tick follows) — the FINAL scene must commit the TELEPORT
//      window with the LAST config (global:2): the A and B censuses are
//      stale-guarded (never committed), the teleport request builds and
//      commits gen-gated, and the page reaches its OWN all-coherent marker
//      (the #scene-coherence "GOTOWA" line — the data-load-status READY
//      attribute is a ONE-SHOT latch, unusable for a post-boot scene);
//   6. PASS = the newer config was observed STORED while busy, the trace
//      shows stale-guarded census commits (A/B not committed, the teleport
//      request committed), the FINAL committed scene (terrain + textures +
//      vegetation) is the teleport window with the LAST config, and zero
//      page errors.
//
// MEASURED BUILD TIMES on this warm machine (honest): the trace records every
// wrapper event; cold builds here are 200-800 ms class (the QC's
// "long-running build" premise does not reproduce with real warm data — the
// race is engaged through the direct-call apply path instead, which starts
// the build without the ~1 s terrain-rebuild latency).
//
// Isolated instance discipline (as the original run): suite-owned headless
// Edge with --remote-debugging-port on a FREE port (NEVER 9222, never a
// foreign session); the process is killed at the end; the PNG is PRIVATE.
//
// Usage:
//   node tools/pecompat/world_r2_correction_browser.mjs --png-dir <PRIVATE dir> \
//        [--base http://127.0.0.1:8163] [--target-gx 200] [--target-gy 200]
// Writes the JSON record to docs/audits/<RUN_ID>/raw/CORRECTION/BROWSER_REVERIFY_VEG_COHERENCE.json
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
let pngDir = null, base = 'http://127.0.0.1:8163', targetGx = 200, targetGy = 200;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--png-dir') pngDir = args[++i];
  else if (args[i] === '--base') base = args[++i];
  else if (args[i] === '--target-gx') targetGx = parseInt(args[++i], 10);
  else if (args[i] === '--target-gy') targetGy = parseInt(args[++i], 10);
}
if (!pngDir) { console.error('usage: node tools/pecompat/world_r2_correction_browser.mjs --png-dir <dir> [--base url] [--target-gx N] [--target-gy N]'); process.exit(2); }
await mkdir(pngDir, { recursive: true });
await mkdir(path.join(ROOT, 'docs', 'audits', RUN_ID, 'raw', 'CORRECTION'), { recursive: true });

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
      `Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*${PROFILE_MARK}*' } | Select-Object ProcessId | ConvertTo-Json`,
    ], { encoding: 'utf8', timeout: 20000 });
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
    for (let i = 0; i < 60; i++) {
      try {
        const r = await fetch(`http://127.0.0.1:${port}/json/list`);
        const targets = await r.json();
        const page = targets.find((t) => t.type === 'page');
        if (page) {
          const ws = new WebSocket(page.webSocketDebuggerUrl);
          await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); });
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
      setTimeout(() => { if (this.pending.has(id)) { this.pending.delete(id); reject(new Error(`CDP timeout: ${method}`)); } }, 90000);
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

const pageErrors = [];
const browser = await launchBrowser();
const { cdp } = browser;
cdp.ws.addEventListener('message', (ev) => {
  let msg; try { msg = JSON.parse(ev.data); } catch { return; }
  if (msg.method === 'Runtime.exceptionThrown') {
    pageErrors.push(String(msg.params.exceptionDetails?.text ?? '') + ' ' + String(msg.params.exceptionDetails?.exception?.description ?? '').slice(0, 500));
  }
  cdp.handle(msg);
});
await cdp.send('Page.enable');
await cdp.send('Runtime.enable');
await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });

const record = {
  scenario: 'CORRECTION_REVERIFY_VEG_COHERENCE (P1-2): the LIVE browser requests a NEWER CONFIG (a second veg-apply) and then SWITCHES REGION (teleport) while vegetation rebuilds are in flight. The wrapper must STORE the newer request (running.vegPending observed while busy), stale-guard the superseded censuses (never committed), commit the LAST request census gen-gated, and reach the page all-coherent marker with the teleport window + the LAST config',
  measuredAt: new Date().toISOString(),
  base,
  url: `${base}/world`,
  configA: { mode: 'global', profile: 1, density: 50, whyCold: 'profile 1 — 14 records / 10 DISTINCT original models, never fetched by this page before the apply' },
  configB: { mode: 'global', profile: 2, density: 50, whyNewer: 'profile 2 — 11 records / 8 DISTINCT original models; the NEWER config requested while the A build is in flight' },
  teleport: { tile: { gx: targetGx, gy: targetGy }, window: { gx: Math.min(Math.max(targetGx - 4, 0), 212), gy: Math.min(Math.max(targetGy - 4, 0), 228) }, whyWarm: 'pre-visited in the warm-up (tiles + textures cached)' },
  homeTile: { gx: 54, gy: 115 },
  homeWindow: { gx: 50, gy: 111 },
  steps: [],
};

try {
  const dbg = (expr) => cdp.evaluate(expr);
  const teleportUi = async (gx, gy) => cdp.evaluate(`(() => {
    const a = document.getElementById('tp-gx'); const b = document.getElementById('tp-gy');
    a.value = '${gx}'; b.value = '${gy}';
    document.getElementById('tp-go').click(); // the REAL teleport button (a human's region switch)
    const d = window.__peR2Debug;
    return { sceneId: d.running.sceneId, vegBusy: d.running.vegBusy, windowOrigin: d.windowOrigin };
  })()`);
  const applyConfigUi = async (profile) => cdp.evaluate(`(() => {
    const sel = document.getElementById('veg-profile'); sel.value = '${profile}';
    sel.dispatchEvent(new Event('change'));
    document.getElementById('veg-apply').click(); // the REAL apply button — its handler calls rebuildVegetation DIRECTLY (no terrain latency) with a forceNew request id
    const d = window.__peR2Debug;
    return { sceneId: d.running.sceneId, vegBusy: d.running.vegBusy, vegPending: d.running.vegPending, windowOrigin: d.windowOrigin };
  })()`);
  // the page OWN all-coherent marker, WINDOW-AWARE: the coherence text only
  // re-renders on census-panel updates, so a stale GOTOWA line of the
  // PREVIOUS window can persist right after a teleport — the wait must
  // require the CURRENT window origin to be the expected one AND the line
  // to be GOTOWA for it (the data-load-status READY attribute is a ONE-SHOT
  // latch — unusable for a post-boot scene)
  const waitCoherentFor = async (win, timeoutMs) => {
    const t = Date.now();
    for (;;) {
      const s = await cdp.evaluate(`(() => { const d = window.__peR2Debug; const c = document.getElementById('scene-coherence')?.textContent ?? ''; return d ? { gotowa: c.includes('GOTOWA (wszystkie komponenty'), line: c.split('\\n')[0], identity: c.split('\\n')[2] ?? '', win: d.windowOrigin, vegBusy: d.running.vegBusy } : { gotowa: false, line: '(page loading — __peR2Debug not yet defined)', identity: '', win: null, vegBusy: null }; })()`);
      if (s.gotowa && s.win && s.win.gx === win.gx && s.win.gy === win.gy) return { coherent: true, waitedMs: Date.now() - t, at: s };
      if (Date.now() - t > timeoutMs) return { coherent: false, waitedMs: Date.now() - t, at: s };
      await sleep(250);
    }
  };

  // ---- 1. load the world page; wait for the boot scene to be all-coherent ----
  await cdp.send('Page.navigate', { url: record.url });
  const bootCoherent = await waitCoherentFor(record.homeWindow, 150000);
  record.boot = bootCoherent;
  record.steps.push({ step: 'boot-to-coherent', ok: bootCoherent.coherent, at: bootCoherent.at });

  // ---- 2. WARM-UP: teleport to the target (wait ITS window coherent — tiles
  //      + textures cached for the later region switch), then home ----
  const warmOut = await teleportUi(targetGx, targetGy);
  const warmTargetCoherent = await waitCoherentFor(record.teleport.window, 150000);
  record.warmupTarget = { click: warmOut, coherent: warmTargetCoherent };
  const warmHome = await teleportUi(record.homeTile.gx, record.homeTile.gy);
  const warmHomeCoherent = await waitCoherentFor(record.homeWindow, 150000);
  record.warmupHome = { click: warmHome, coherent: warmHomeCoherent };
  record.steps.push({ step: 'warm-up (teleport target + home)', ok: warmTargetCoherent.coherent && warmHomeCoherent.coherent, warmTargetWin: warmTargetCoherent.at.win });

  // ---- 3. THE RACE, config A: apply global profile 1 through the REAL apply
  //      button — the handler's DIRECT rebuildVegetation call starts the A
  //      build immediately (no terrain-rebuild latency) ----
  const applyA = await applyConfigUi(1);
  record.applyA = applyA;
  let aBusyMs = null;
  const tA = Date.now();
  for (;;) {
    const v = await dbg(`window.__peR2Debug.running.vegBusy`);
    if (v === true) { aBusyMs = Date.now() - tA; break; }
    if (Date.now() - tA > 20000) break;
    await sleep(20);
  }
  record.applyAVegBusyAfterMs = aBusyMs;
  record.steps.push({ step: 'config A applied (global profile 1; build in flight)', ok: aBusyMs !== null, vegBusyAfterMs: aBusyMs });

  // ---- 4. THE RACE, config B: WHILE the A build is in flight, apply global
  //      profile 2 — the NEWER CONFIG must be STORED at the busy wrapper ----
  const applyB = await applyConfigUi(2);
  record.applyB = applyB;
  // observe the STORED newer request (running.vegPending) — the direct LIVE
  // proof; poll fast (the store window equals the A build's remaining time)
  let midRace = null;
  const t2 = Date.now();
  for (;;) {
    const v = await dbg(`(() => { const r = window.__peR2Debug.running; return { vegBusy: r.vegBusy, vegPending: r.vegPending, sceneId: r.sceneId, runningOrigin: r.runningOrigin, busy: r.busy }; })()`);
    if (v.vegPending) { midRace = { ...v, observedAfterMs: Date.now() - t2 }; break; } // the newer request is STORED at the busy wrapper
    if (v.vegBusy === false && Date.now() - t2 > 3000) { midRace = { ...v, observedAfterMs: Date.now() - t2 }; break; } // the wrapper drained before we sampled — race missed (honest)
    if (Date.now() - t2 > 20000) { midRace = { ...v, observedAfterMs: Date.now() - t2 }; break; }
    await sleep(20);
  }
  record.midRace = midRace;
  record.steps.push({ step: 'config B applied while A building — observe the stored newer request (vegPending while busy)', ok: !!(midRace && midRace.vegPending) });

  // ---- 5. THE RACE, region switch: WHILE the builds are still in flight,
  //      teleport to the PRE-WARMED target through the REAL teleport UI ----
  const tpClick = await teleportUi(targetGx, targetGy);
  record.teleportClick = { ...tpClick, vegBusyAtClick: tpClick.vegBusy };
  record.steps.push({ step: 'region switch (teleport) while veg building', ok: true, vegBusyAtClick: tpClick.vegBusy });

  // ---- 6. wait for the page OWN all-coherent marker for the TELEPORT window ----
  const finalCoherent = await waitCoherentFor(record.teleport.window, 180000);
  record.finalCoherent = finalCoherent;

  // ---- 7. the FINAL committed state (incl. the full wrapper trace) ----
  const fin = await cdp.evaluate(`(() => {
    const d = window.__peR2Debug;
    return {
      loadStatus: document.getElementById('diagnostics')?.getAttribute('data-load-status'),
      windowOrigin: d.windowOrigin,
      running: d.running,
      coherence: document.getElementById('scene-coherence')?.textContent,
      vegPanel: document.getElementById('world-veg')?.textContent?.slice(0, 600),
      censusPanel: document.getElementById('world-census')?.textContent?.slice(0, 900),
    };
  })()`);
  record.final = fin;

  const shot = await cdp.screenshot();
  const pngPath = path.join(pngDir, 'correction_veg_coherence_reverify.png');
  await writeFile(pngPath, shot);
  record.screenshot = { file: path.basename(pngPath), bytes: shot.length, sha256: hash(shot) };

  // ---- 8. the honest PASS predicate ----
  const wantWin = record.teleport.window;
  const trace = fin.running.vegTrace ?? [];
  const idT = tpClick.sceneId; // teleportTo -> requestScene is SYNCHRONOUS: the teleport click's capture IS its post-bump request id
  // HONEST NOTE on the apply-button captures: the veg-apply click handler is
  // async (it awaits veg.setConfig BEFORE its requestScene) — the click-time
  // sceneId readout therefore predates the handler's id bump; the config
  // requests' true ids live in the wrapper TRACE (request-stored-pending /
  // drain-run runRequestId), not in the click captures.
  const storedPendingEvents = trace.filter((e) => e.event === 'request-stored-pending (busy)');
  const configStoredWhileBusy = storedPendingEvents.some((e) => e.origin.gx === record.homeWindow.gx && e.origin.gy === record.homeWindow.gy);
  const teleportStoredWhileBusy = storedPendingEvents.some((e) => e.origin.gx === wantWin.gx && e.origin.gy === wantWin.gy);
  const staleSkips = trace.filter((e) => e.event === 'census-not-committed (stale or aborted)');
  const lastCommitted = trace.filter((e) => e.event === 'census-committed (current scene)').pop() ?? null;
  const committedIsLastRequest = !!(lastCommitted && lastCommitted.runRequestId === idT && lastCommitted.censusOrigin.gx === wantWin.gx && lastCommitted.censusOrigin.gy === wantWin.gy);
  const coherenceAllTarget = fin.coherence && fin.coherence.includes(`teren ${wantWin.gx},${wantWin.gy}`)
    && fin.coherence.includes(`tekstury ${wantWin.gx},${wantWin.gy}`)
    && fin.coherence.includes(`roślinność ${wantWin.gx},${wantWin.gy}`) && fin.coherence.includes('GOTOWA');
  const lastConfigCommitted = fin.coherence && fin.coherence.includes('global:2'); // the committed census carries the LAST config (profile 2)
  record.pass = {
    bootCoherent: bootCoherent.coherent,
    warmupCoherent: warmTargetCoherent.coherent && warmHomeCoherent.coherent,
    aBuildInFlightAtB: !!(midRace && midRace.vegBusy === true),
    newerConfigStoredWhileBusy: !!(midRace && midRace.vegPending && midRace.vegPending.origin.gx === record.homeWindow.gx && midRace.vegPending.origin.gy === record.homeWindow.gy) && configStoredWhileBusy,
    regionSwitchStoredWhileBusy: teleportStoredWhileBusy,
    staleGuardedCensuses: staleSkips.length >= 2,
    committedCensusIsLastRequest: committedIsLastRequest,
    finalSceneCoherentForTeleport: finalCoherent.coherent && finalCoherent.at.win.gx === wantWin.gx && finalCoherent.at.win.gy === wantWin.gy,
    coherenceAllTarget,
    lastConfigCommitted,
    vegDrainedAfter: fin.running.vegBusy === false && fin.running.vegPending === null,
    noPageErrors: pageErrors.length === 0,
  };
  record.verdict = Object.values(record.pass).every(Boolean) ? 'REVERIFY_PASS' : 'REVERIFY_FAIL (honest record)';
  record.pageErrors = pageErrors;
} catch (e) {
  record.verdict = 'REVERIFY_ERROR (honest record)';
  record.error = String(e?.stack ?? e);
  record.pageErrors = pageErrors;
} finally {
  const outPath = path.join(ROOT, 'docs', 'audits', RUN_ID, 'raw', 'CORRECTION', 'BROWSER_REVERIFY_VEG_COHERENCE.json');
  await writeFile(outPath, JSON.stringify(record, null, 1) + '\n');
  console.log(JSON.stringify({ verdict: record.verdict, pass: record.pass ?? null, midRace: record.midRace ?? null, applyBSceneId: record.applyB?.sceneId ?? null, finalCoherent: record.finalCoherent?.coherent ?? null, finalWindow: record.final?.windowOrigin ?? null, coherenceFirst200: (record.final?.coherence ?? '').slice(0, 200), pageErrors: pageErrors.length }, null, 2));
  cdp.close();
  try { browser.child.kill(); } catch { /* gone */ }
  killOwnLeftover();
  process.exit(record.verdict === 'REVERIFY_PASS' ? 0 : 1);
}
