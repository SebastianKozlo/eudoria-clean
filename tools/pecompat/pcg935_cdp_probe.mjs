#!/usr/bin/env node
// pcg935_cdp_probe.mjs — PRIVATE: real-browser LOAD/PIXEL/INTERACTION probe for
// the 8164 viewer via raw CDP (headless Chrome + built-in WebSocket; no deps).
// Usage: node tools/pecompat/pcg935_cdp_probe.mjs [steps...]
'use strict';
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const DEBUG_PORT = 9223;
const USER_DATA = path.join(os.tmpdir(), 'pcg935-cdp-profile');
const URL = process.env.PCG935_URL || 'http://127.0.0.1:8164/';

function httpJson(port, pathname) {
  return new Promise((resolve, reject) => {
    http.get({ host: '127.0.0.1', port, path: pathname }, (res) => {
      let data = '';
      res.on('data', (c) => { data += c; });
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(e); } });
    }).on('error', reject);
  });
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  const chrome = spawn(CHROME, [
    '--headless=new', `--remote-debugging-port=${DEBUG_PORT}`, `--user-data-dir=${USER_DATA}`,
    '--no-first-run', '--no-default-browser-check', '--window-size=1440,900', '--disable-gpu-sandbox',
    'about:blank',
  ], { stdio: 'ignore' });
  console.log('[cdp] chrome pid', chrome.pid);
  let targets = null;
  for (let i = 0; i < 40; i++) {
    try { targets = await httpJson(DEBUG_PORT, '/json'); if (targets.length) break; } catch { }
    await sleep(250);
  }
  if (!targets) { console.log('[cdp] FATAL: no CDP targets'); chrome.kill(); process.exit(1); }
  const page = targets.find((t) => t.type === 'page');
  const wsUrl = page.webSocketDebuggerUrl;
  const ws = new WebSocket(wsUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  let msgId = 0;
  const pending = new Map();
  const events = [];
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
    else events.push(msg);
  };
  const send = (method, params = {}) => new Promise((resolve) => {
    const id = ++msgId;
    pending.set(id, resolve);
    ws.send(JSON.stringify({ id, method, params }));
  });
  await send('Page.enable');
  await send('Runtime.enable');
  const evalJs = async (expression, awaitPromise = true) => {
    const r = await send('Runtime.evaluate', { expression, awaitPromise, returnByValue: true });
    if (r.result?.exceptionDetails) return { error: JSON.stringify(r.result.exceptionDetails).slice(0, 400) };
    return r.result?.result?.value;
  };

  // ---- LOAD ----
  const nav = await send('Page.navigate', { url: URL });
  let loaded = false;
  for (let i = 0; i < 120 && !loaded; i++) {
    await sleep(250);
    loaded = await evalJs("document.readyState === 'complete'", false);
  }
  console.log('[LOAD] readyState complete:', loaded);
  // wait for catalog render + default asset selection
  let catalogRows = 0; let assetInfo = ''; let genText = '';
  for (let i = 0; i < 60; i++) {
    await sleep(500);
    catalogRows = await evalJs("document.querySelectorAll('#list .row').length", false);
    assetInfo = await evalJs("document.querySelector('#asset-info')?.textContent ?? ''", false);
    genText = await evalJs("document.querySelector('#gen-indicator')?.textContent ?? ''", false);
    if (catalogRows > 0 && !assetInfo.includes('loading') && assetInfo.length > 10) break;
  }
  console.log(`[LOAD] catalogRows=${catalogRows} gen="${genText}" assetInfo="${String(assetInfo).replace(/\s+/g, ' ').slice(0, 220)}"`);
  const drawerStats = await evalJs("document.querySelector('#drawer-stats')?.textContent ?? ''", false);
  console.log(`[LOAD] drawerStats="${String(drawerStats).slice(0, 160)}"`);
  const hash = await evalJs("location.hash", false);
  console.log(`[LOAD] hash="${hash}"`);

  // ---- PIXEL (screenshot + non-background pixel census) ----
  await sleep(1200);
  const shot1 = await send('Page.captureScreenshot', { format: 'png' });
  const png1 = Buffer.from(shot1.result.data, 'base64');
  fs.writeFileSync('D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010\\browser\\load_default.png', png1);
  console.log(`[PIXEL] screenshot1 saved ${png1.length} B`);
  // count non-background pixels via canvas readback INSIDE the page (GPU canvas)
  const pixCensus = await evalJs(`(async () => {
    const c = document.querySelector('#c');
    const gl = c.getContext('webgl2') || c.getContext('webgl');
    if (!gl) return { error: 'no webgl context' };
    const w = gl.drawingBufferWidth, h = gl.drawingBufferHeight;
    const px = new Uint8Array(w * h * 4);
    gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px);
    let lit = 0, dark = 0;
    for (let i = 0; i < px.length; i += 4) {
      const r = px[i], g = px[i+1], b = px[i+2];
      const isBg = Math.abs(r-0x10)<6 && Math.abs(g-0x14)<6 && Math.abs(b-0x18)<6;
      if (!isBg) { lit++; if (r+g+b < 60) dark++; }
    }
    return { w, h, lit, dark, total: w*h };
  })()`);
  console.log('[PIXEL]', JSON.stringify(pixCensus));

  // ---- INTERACTION: toggles + animation witness (462325 = kf+textkey) ----
  const sel = await evalJs(`(async () => {
    // deep-link to the animated witness
    location.hash = '#asset/462325';
    await new Promise(r => setTimeout(r, 4000));
    const info = document.querySelector('#asset-info')?.textContent ?? '';
    const rows = document.querySelectorAll('#list .row').length;
    return { hash: location.hash, info: info.replace(/\\s+/g,' ').slice(0,240), rows };
  })()`);
  console.log('[INTERACTION] select 462325 ->', JSON.stringify(sel));
  const animUi = await evalJs(`(async () => {
    const anim = document.querySelector('#anim');
    const clips = document.querySelector('#a-clip');
    const options = clips ? [...clips.options].map(o => o.textContent) : [];
    return { open: !anim.classList.contains('closed'), options: options.slice(0,3) };
  })()`);
  console.log('[INTERACTION] anim drawer:', JSON.stringify(animUi));
  const play = await evalJs(`(async () => {
    document.querySelector('#a-play')?.click();
    await new Promise(r => setTimeout(r, 2600));
    const t = document.querySelector('#a-time')?.textContent ?? '';
    return { timeText: t };
  })()`);
  console.log('[INTERACTION] play 2.6s ->', JSON.stringify(play));
  const play2 = await evalJs(`(async () => {
    // >2-duration repeat without drift: let it run beyond 2x duration
    await new Promise(r => setTimeout(r, 4200));
    const t = document.querySelector('#a-time')?.textContent ?? '';
    return { timeText: t };
  })()`);
  console.log('[INTERACTION] extended play (>2x duration) ->', JSON.stringify(play2));
  const scrub = await evalJs(`(async () => {
    const s = document.querySelector('#a-scrub');
    s.value = '500'; s.dispatchEvent(new Event('input'));
    await new Promise(r => setTimeout(r, 200));
    const t = document.querySelector('#a-time')?.textContent ?? '';
    document.querySelector('#a-stop')?.click();
    return { timeText: t };
  })()`);
  console.log('[INTERACTION] scrub mid ->', JSON.stringify(scrub));
  const toggles = await evalJs(`(async () => {
    const results = {};
    document.querySelector('#t-wireframe').click();
    await new Promise(r => setTimeout(r, 300));
    results.wireframe = document.querySelector('#t-wireframe').checked;
    document.querySelector('#t-wireframe').click();
    document.querySelector('#btn-drawer').click();
    await new Promise(r => setTimeout(r, 400));
    results.drawerOpen = !document.querySelector('#drawer').classList.contains('closed');
    document.querySelector('#btn-parts').click();
    await new Promise(r => setTimeout(r, 400));
    results.partsOpen = !document.querySelector('#parts').classList.contains('closed');
    document.querySelector('#btn-drawer').click();
    document.querySelector('#btn-parts').click();
    results.search = 'skip';
    return results;
  })()`);
  console.log('[INTERACTION] toggles ->', JSON.stringify(toggles));
  // search + filter
  const search = await evalJs(`(async () => {
    const inp = document.querySelector('#search');
    inp.value = '223534'; inp.dispatchEvent(new Event('input'));
    await new Promise(r => setTimeout(r, 600));
    const rows = [...document.querySelectorAll('#list .row')].map(r => r.dataset.id);
    return { rows: rows.slice(0, 5) };
  })()`);
  console.log('[INTERACTION] search 223534 ->', JSON.stringify(search));
  const clickRow = await evalJs(`(async () => {
    const row = document.querySelector('#list .row');
    row?.click();
    await new Promise(r => setTimeout(r, 3000));
    return { hash: location.hash, info: (document.querySelector('#asset-info')?.textContent ?? '').replace(/\\s+/g,' ').slice(0, 200) };
  })()`);
  console.log('[INTERACTION] row click ->', JSON.stringify(clickRow));
  const shot2 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010\\browser\\interaction_end.png', Buffer.from(shot2.result.data, 'base64'));
  console.log('[PIXEL] screenshot2 saved');

  chrome.kill();
  process.exit(0);
}
main().catch((e) => { console.error('FATAL', e); process.exit(1); });
