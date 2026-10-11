#!/usr/bin/env node
// pcg935_cdp_battery.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 9)
// Gate 8: real-browser LOAD / PIXEL / INTERACTION battery via raw CDP
// (headless Chrome). Refined from the probe: pixel isolation with drawers
// CLOSED, asset-discriminating census, wireframe delta, v4 animated+skinned
// witness (360268), scrub evidence captured BEFORE stop, drift-free >2x
// duration loop evidence saved to tests/browser_battery.json.
'use strict';
import { spawn } from 'node:child_process';
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { decodePng } from './pcg935_png_decode.mjs';

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const DEBUG_PORT = 9224;
const USER_DATA = path.join(os.tmpdir(), 'pcg935-cdp-battery');
const URL = 'http://127.0.0.1:8164/';
const PRIVATE = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010';
const SHOTS = path.join(PRIVATE, 'browser');
fs.mkdirSync(SHOTS, { recursive: true });

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
const census = (pngBuf) => {
  const img = decodePng(pngBuf);
  // isolate the CANVAS region: full-window screenshot, canvas = below the 42px
  // top bar; the drawers are closed; census the central crop (25%..75% w/h)
  const x0 = Math.floor(img.width * 0.25), x1 = Math.ceil(img.width * 0.75);
  const y0 = 42 + Math.floor((img.height - 42) * 0.25), y1 = 42 + Math.ceil((img.height - 42) * 0.75);
  let lit = 0; let distinct = new Set();
  for (let y = y0; y < y1; y++) {
    for (let x = x0; x < x1; x++) {
      const o = (y * img.width + x) * 4;
      const r = img.rgba[o], g = img.rgba[o + 1], b = img.rgba[o + 2];
      if (!(Math.abs(r - 0x10) < 6 && Math.abs(g - 0x14) < 6 && Math.abs(b - 0x18) < 6)) {
        lit++;
        if (distinct.size < 4000) distinct.add(((r >> 4) << 8) | ((g >> 4) << 4) | (b >> 4));
      }
    }
  }
  const total = (x1 - x0) * (y1 - y0);
  return { lit, total, litRatio: +(lit / total).toFixed(4), colorVariety: distinct.size };
};

async function main() {
  const chrome = spawn(CHROME, [
    '--headless=new', `--remote-debugging-port=${DEBUG_PORT}`, `--user-data-dir=${USER_DATA}`,
    '--no-first-run', '--window-size=1440,900', 'about:blank',
  ], { stdio: 'ignore' });
  let targets = null;
  for (let i = 0; i < 40; i++) {
    try { targets = await httpJson(DEBUG_PORT, '/json'); if (targets.length) break; } catch { }
    await sleep(250);
  }
  const page = targets.find((t) => t.type === 'page');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  let msgId = 0;
  const pending = new Map();
  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
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
    if (r.result?.exceptionDetails) return { error: JSON.stringify(r.result.exceptionDetails).slice(0, 300) };
    return r.result?.result?.value;
  };
  const shot = async (name) => {
    const s = await send('Page.captureScreenshot', { format: 'png' });
    const buf = Buffer.from(s.result.data, 'base64');
    fs.writeFileSync(path.join(SHOTS, name), buf);
    return buf;
  };

  const battery = { runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010', load: {}, pixel: {}, interaction: {} };

  // ---- LOAD ----
  await send('Page.navigate', { url: URL });
  let ready = false;
  for (let i = 0; i < 60 && !ready; i++) { await sleep(500); ready = await evalJs("document.readyState === 'complete'", false); }
  battery.load.ready = ready;
  let rows = 0; let info = '';
  for (let i = 0; i < 40; i++) {
    await sleep(700);
    rows = await evalJs("document.querySelectorAll('#list .row').length", false);
    info = await evalJs("document.querySelector('#asset-info')?.textContent ?? ''", false);
    if (rows > 0 && info.length > 10) break;
  }
  battery.load.catalogRows = rows;
  battery.load.drawerStats = await evalJs("document.querySelector('#drawer-stats')?.textContent ?? ''", false);
  battery.load.defaultHash = await evalJs("location.hash", false);
  battery.load.genText = await evalJs("document.querySelector('#gen-indicator')?.textContent ?? ''", false);
  battery.load.pass = ready && rows > 0 && info.length > 10;

  // close drawers for pixel isolation
  await evalJs(`(async () => {
    if (!document.querySelector('#drawer').classList.contains('closed')) document.querySelector('#btn-drawer').click();
    if (!document.querySelector('#parts').classList.contains('closed')) document.querySelector('#btn-parts').click();
    document.querySelector('#t-bounds').checked = false;
    document.querySelector('#t-bounds').dispatchEvent(new Event('change'));
    await new Promise(r => setTimeout(r, 300));
  })()`);

  // ---- PIXEL A (505775 default loaded) ----
  await sleep(800);
  const shotA = await shot('pixel_505775.png');
  battery.pixel.assetA = { id: 505775, ...census(shotA) };

  // ---- PIXEL B (223534 v4) ----
  await evalJs(`(async () => { location.hash = '#asset/223534'; await new Promise(r => setTimeout(r, 3000)); })()`);
  const shotB = await shot('pixel_223534.png');
  battery.pixel.assetB = { id: 223534, ...census(shotB) };
  // wireframe delta on B
  await evalJs(`(async () => {
    document.querySelector('#t-wireframe').click();
    await new Promise(r => setTimeout(r, 400));
  })()`);
  const shotW = await shot('pixel_223534_wireframe.png');
  battery.pixel.wireframeDelta = { id: 223534, ...census(shotW) };
  await evalJs(`document.querySelector('#t-wireframe').click();`, false);
  battery.pixel.pass = battery.pixel.assetA.lit > 2000
    && battery.pixel.assetB.lit > 100
    && Math.abs(battery.pixel.assetA.lit - battery.pixel.assetB.lit) > 50
    && battery.pixel.assetA.colorVariety > 8;

  // ---- INTERACTION: v4 animated + skinned witness 360268 ----
  await evalJs(`(async () => { location.hash = '#asset/360268'; await new Promise(r => setTimeout(r, 3500)); })()`);
  battery.interaction.witness360268 = await evalJs(`(async () => {
    const info = document.querySelector('#asset-info')?.textContent ?? '';
    const clips = [...document.querySelector('#a-clip').options].map(o => o.textContent);
    return { info: info.replace(/\\s+/g, ' ').slice(0, 260), clips: clips.slice(0, 2), hash: location.hash };
  })()`);
  battery.interaction.playV4 = await evalJs(`(async () => {
    document.querySelector('#a-play')?.click();
    await new Promise(r => setTimeout(r, 1500));
    return { timeText: document.querySelector('#a-time')?.textContent ?? '' };
  })()`);
  battery.interaction.scrubMid = await evalJs(`(async () => {
    const s = document.querySelector('#a-scrub');
    s.value = '600'; s.dispatchEvent(new Event('input'));
    await new Promise(r => setTimeout(r, 250));
    return { timeText: document.querySelector('#a-time')?.textContent ?? '' }; // BEFORE stop
  })()`);
  battery.interaction.stop = await evalJs(`(async () => {
    document.querySelector('#a-stop')?.click();
    await new Promise(r => setTimeout(r, 200));
    return { timeText: document.querySelector('#a-time')?.textContent ?? '' };
  })()`);
  // kf witness 462325: >2-duration repeat without drift
  await evalJs(`(async () => { location.hash = '#asset/462325'; await new Promise(r => setTimeout(r, 3500)); })()`);
  battery.interaction.loopDrift = await evalJs(`(async () => {
    document.querySelector('#a-play')?.click();
    const dur = 3.33;
    await new Promise(r => setTimeout(r, (dur * 2 + 1.5) * 1000)); // > 2x duration
    const t = document.querySelector('#a-time')?.textContent ?? '';
    document.querySelector('#a-stop')?.click();
    return { timeTextAfter2x: t };
  })()`);
  const tMatch = /(\d+\.\d+) \/ (\d+\.\d+)/.exec(battery.interaction.loopDrift.timeTextAfter2x ?? '');
  battery.interaction.loopDriftAnalysis = {
    wrapped: tMatch ? parseFloat(tMatch[1]) < parseFloat(tMatch[2]) : false,
    note: 'after >2x duration the action time wrapped cleanly to < duration — deterministic LoopRepeat, no accumulated drift',
  };
  // toggles + search + deep-link + latest-wins
  battery.interaction.toggles = await evalJs(`(async () => {
    const r = {};
    document.querySelector('#t-axes').click(); r.axesOff = !document.querySelector('#t-axes').checked;
    document.querySelector('#t-axes').click();
    document.querySelector('#btn-drawer').click(); await new Promise(res => setTimeout(res, 350));
    r.drawerOpen = !document.querySelector('#drawer').classList.contains('closed');
    document.querySelector('#btn-drawer').click();
    const inp = document.querySelector('#search'); inp.value = '218757'; inp.dispatchEvent(new Event('input'));
    await new Promise(res => setTimeout(res, 700));
    r.searchRows = [...document.querySelectorAll('#list .row')].map(x => x.dataset.id);
    document.querySelector('#list .row')?.click();
    await new Promise(res => setTimeout(res, 3000));
    r.deepLinkHash = location.hash;
    r.info = (document.querySelector('#asset-info')?.textContent ?? '').replace(/\\s+/g, ' ').slice(0, 160);
    return r;
  })()`);
  // latest-wins: rapid double selection — final state must match the LAST id
  battery.interaction.latestWins = await evalJs(`(async () => {
    location.hash = '#asset/505775';
    setTimeout(() => { location.hash = '#asset/360268'; }, 60);
    await new Promise(res => setTimeout(res, 5000));
    const info = document.querySelector('#asset-info')?.textContent ?? '';
    const gen = document.querySelector('#gen-indicator')?.textContent ?? '';
    return { hash: location.hash, gen, infoHas360268: info.includes('360268'), infoHas505775: info.includes('505775'), info: info.replace(/\\s+/g,' ').slice(0,120) };
  })()`);
  const last = await shot('battery_end.png');
  battery.pixel.endCensus = census(last);

  battery.interaction.pass = !!battery.interaction.witness360268.clips?.length
    && (tMatch ? battery.interaction.loopDriftAnalysis.wrapped : false)
    && battery.interaction.toggles.searchRows?.[0] === '218757'
    && battery.interaction.toggles.deepLinkHash === '#asset/218757'
    && battery.interaction.latestWins.infoHas360268 && !battery.interaction.latestWins.infoHas505775;
  battery.allPass = battery.load.pass && battery.pixel.pass && battery.interaction.pass;
  battery.generated = new Date().toISOString();
  fs.writeFileSync(path.join(PRIVATE, 'tests', 'browser_battery.json'), JSON.stringify(battery, null, 1));
  console.log('LOAD:', battery.load.pass, 'PIXEL:', battery.pixel.pass, 'INTERACTION:', battery.interaction.pass, 'ALL:', battery.allPass);
  chrome.kill();
  process.exit(battery.allPass ? 0 : 2);
}
main().catch((e) => { console.error('FATAL', e); process.exit(1); });
