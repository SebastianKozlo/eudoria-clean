#!/usr/bin/env node
// w1_f0_noise_control.mjs — W1-2: capture staging f0 TWICE in two fresh loads of
// the SAME staging stack (three 0.187.0 + fixes) to measure run-to-run noise of
// the f0 frame (open-loop async LOD/veg/streaming states). This is the honest
// denominator for the baseline-vs-staging pixel diff.
import { spawn } from 'node:child_process';
import { writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import net from 'node:net';
import path from 'node:path';
const BASE = 'http://127.0.0.1:8171';
const OUT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_WORLD_8163_TEXTURE_BIOME_PLAYER_GAME_ANIMATIONS_6H_R1_20261031\\W1_TERRAIN_MATERIALS\\W1-2\\staging';
const PROFILE_MARK = 'pec-w1-2-f0noise-8171';
const EDGE_CANDIDATES = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
function findFreePort() {
  const tryPort = (p) => new Promise((resolve) => { const s = net.createServer(); s.once('error', () => resolve(false)); s.listen(p, '127.0.0.1', () => s.close(() => resolve(true))); });
  return (async () => { for (let p = 21400; p < 21500; p++) { if (await tryPort(p)) return p; } throw new Error('no free CDP port'); })();
}
class Cdp {
  constructor(ws) { this.ws = ws; this.seq = 0; this.pending = new Map(); }
  static async connect(port) {
    for (let i = 0; i < 60; i++) {
      try { const r = await fetch(`http://127.0.0.1:${port}/json/list`); const page = (await r.json()).find((t) => t.type === 'page');
        if (page) { const ws = new WebSocket(page.webSocketDebuggerUrl); await new Promise((res, rej) => { ws.addEventListener('open', res); ws.addEventListener('error', rej); }); return new Cdp(ws); } } catch { }
      await sleep(250);
    }
    throw new Error('CDP page target not found');
  }
  send(method, params = {}) { return new Promise((resolve, reject) => { const id = ++this.seq; this.pending.set(id, { resolve, reject }); this.ws.send(JSON.stringify({ id, method, params })); setTimeout(() => { if (this.pending.has(id)) { this.pending.delete(id); reject(new Error(`timeout ${method}`)); } }, 90000); }); }
  handle(msg) { if (msg.id && this.pending.has(msg.id)) { const { resolve, reject } = this.pending.get(msg.id); this.pending.delete(msg.id); if (msg.error) reject(new Error(msg.error.message)); else resolve(msg.result); } }
  async evaluate(expression) { const r = await this.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true }); if (r.exceptionDetails) throw new Error(String(r.exceptionDetails.exception?.description).slice(0, 300)); return r.result.value; }
  async screenshot() { const r = await this.send('Page.captureScreenshot', { format: 'png' }); return Buffer.from(r.data, 'base64'); }
  close() { try { this.ws.close(); } catch { } }
}
async function launchBrowser() {
  const bin = EDGE_CANDIDATES.find((p) => existsSync(p)); if (!bin) throw new Error('no browser binary');
  const port = await findFreePort();
  const child = spawn(bin, ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${path.join(os.tmpdir(), 'opencode', `${PROFILE_MARK}-${Date.now()}`)}`,
    '--no-first-run', '--no-default-browser-check', '--disable-extensions', '--window-size=1280,720', 'about:blank'], { stdio: 'ignore', windowsHide: true });
  const cdp = await Cdp.connect(port);
  return { child, cdp };
}
async function captureF0(tag) {
  const b = await launchBrowser();
  const { cdp } = b;
  cdp.ws.addEventListener('message', (m) => cdp.handle(JSON.parse(m.data)));
  await cdp.send('Page.enable'); await cdp.send('Runtime.enable');
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 720, deviceScaleFactor: 1, mobile: false });
  await cdp.send('Page.navigate', { url: `${BASE}/world` });
  const t0 = Date.now();
  for (;;) { try { if (await cdp.evaluate(`document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY'`) &&
      (await cdp.evaluate(`(document.getElementById('scene-coherence')?.textContent ?? '').includes('GOTOWA')`))) break; } catch { }
    if (Date.now() - t0 > 180000) break; await sleep(300); }
  await sleep(500);
  const png = await cdp.screenshot();
  await writeFile(path.join(OUT, `staging_f0_${tag}.png`), png);
  const cam = await cdp.evaluate(`window.__peR2Debug.camera`);
  cdp.close(); try { process.kill(b.child.pid); } catch { }
  return { tag, cam };
}
const r1 = await captureF0('noise1');
const r2 = await captureF0('noise2');
await writeFile(path.join(OUT, '..', 'F0_NOISE_CONTROL.json'), JSON.stringify({ capturedAt: new Date().toISOString(), runs: [r1, r2] }, null, 1));
console.log('f0 noise pair captured', JSON.stringify([r1.cam, r2.cam]));
process.exit(0);
