// tools/av2/gates.mjs — AV-2 browser gates (isolated headless Chrome + raw CDP,
// tools/cdp_probe.js pattern). Runs the FULL G1-G5 sequence against the live
// AV-2 server on 127.0.0.1:8141 and writes evidence JSON + PNGs to the SCI dir.
// G1 page loads + index > 2000; G2 render 3 diverse models with honest
// bound/missing texture counters; G3 animation clip play + activeTracks > 0 +
// seek works; G4 zero page errors; G5 era label visible in UI.
'use strict';
import { spawn } from 'node:child_process';
import { promises as fs } from 'node:fs';

const BASE = process.env.AV_BASE_URL || 'http://127.0.0.1:8141';
const SCI = process.env.AV_SCI_DIR || 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV2_VIEWER';
const URL_PAGE = `${BASE}/compat/assets.html`;
// G2 trio: small textured (103241) / large untextured-honest (206264) /
// animated + textured (128816 — 3 NiUVControllers, 19/28 textures)
const G2_MODELS = [103241, 206264, 128816];

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const DEBUG_PORT = 8149;
const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  `--remote-debugging-port=${DEBUG_PORT}`, '--user-data-dir=C:/Users/User/AppData/Local/Temp/opencode/cdp_profile_av2',
  'about:blank',
], { stdio: 'ignore' });
console.log('chrome pid', chrome.pid);

async function getTarget() {
  for (let i = 0; i < 40; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
      const page = (await res.json()).find((t) => t.type === 'page');
      if (page) return page;
    } catch { /* retry */ }
    await new Promise((r) => setTimeout(r, 250));
  }
  throw new Error('no CDP page target');
}
const target = await getTarget();
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let msgId = 0;
const pending = new Map();
const consoleMsgs = [];
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
  else if (m.method === 'Runtime.consoleAPICalled') {
    consoleMsgs.push({ type: m.params.type, text: (m.params.args ?? []).map((a) => a.value ?? a.description).join(' ') });
  } else if (m.method === 'Runtime.exceptionThrown') {
    consoleMsgs.push({ type: 'EXCEPTION', text: JSON.stringify(m.params.exceptionDetails).slice(0, 500) });
  }
};
function send(method, params = {}) {
  return new Promise((resolve) => {
    const id = ++msgId;
    pending.set(id, resolve);
    ws.send(JSON.stringify({ id, method, params }));
  });
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function ev(expr) {
  const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
  if (r.result?.exceptionDetails) return { __exc: JSON.stringify(r.result.exceptionDetails).slice(0, 300) };
  return r.result?.result?.value;
}
async function shot(name) {
  const s = await send('Page.captureScreenshot', { format: 'png' });
  await fs.writeFile(`${SCI}\\${name}.png`, Buffer.from(s.result.data, 'base64'));
}

await send('Page.enable');
await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1280, height: 860, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: URL_PAGE });

const gates = { url: URL_PAGE, models: {} };
// G1: index ready + count > 2000
let ok = false;
for (let i = 0; i < 120; i++) {
  const st = await ev('window.__AV_STATE__ && __AV_STATE__.doneIndex ? __AV_STATE__ : null');
  if (st) { gates.indexCount = st.indexCount; ok = st.indexCount > 2000; break; }
  await sleep(500);
}
gates.G1 = { pass: ok, indexCount: gates.indexCount ?? null };
console.log('G1', JSON.stringify(gates.G1));

// G2: render the 3 models; per-model bound/missing + screenshot
for (const id of G2_MODELS) {
  await ev(`__AV_LOAD_MODEL__(${id})`);
  let st = null;
  for (let i = 0; i < 120; i++) {
    st = await ev('__AV_STATE__');
    if (st && st.currentId === id && (st.modelStatus === 'IR_READY' || String(st.modelStatus).startsWith('UNSUPPORTED') || st.modelStatus === 'LOAD_FAIL')) break;
    await sleep(500);
  }
  const m = {
    id, status: st?.modelStatus, parseStatus: st?.parseStatus,
    shapes: st?.shapesCount ?? null, vertices: st?.vertices, triangles: st?.triangles,
    texBound: st?.texBound, texMissing: st?.texMissing, texJoins: st?.texTotal,
  };
  gates.models[id] = m;
  await shot(`g2_model_${id}`);
}
gates.G2 = {
  pass: gates.models[103241]?.status === 'IR_READY' && gates.models[206264]?.status === 'IR_READY' && gates.models[128816]?.status === 'IR_READY'
    && gates.models[103241].texBound > 0,
  models: gates.models,
};
console.log('G2', JSON.stringify(gates.G2));

// G3: animation on 128816 (NiUVController): clip play, active tracks > 0,
// mixer.update advances time, seek works
await ev('__AV_PLAY__(0)');
await sleep(1500); // let the render loop run mixer.update
const a1 = await ev('__AV_STATE__.anim');
await ev('__AV_SEEK__(0.5)');
const seekT = await ev('__AV_STATE__.anim.time');
gates.G3 = {
  pass: a1 && a1.activeTracks > 0 && a1.time > 0 && Number(seekT) > 0,
  activeTracks: a1?.activeTracks, timeAfterPlay: a1?.time, timeAfterSeek: seekT, clips: a1?.clips,
};
await shot('g3_anim_128816');
console.log('G3', JSON.stringify(gates.G3));

// G4: zero page errors (console exceptions on the exercised path)
const exc = consoleMsgs.filter((c) => c.type === 'EXCEPTION' || c.type === 'error');
gates.G4 = { pass: exc.length === 0, errorCount: exc.length, errors: exc.slice(0, 10) };
console.log('G4', JSON.stringify(gates.G4));

// G5: era label visible in UI
const eraOk = await ev("document.body.innerText.includes('ISO_5_1_0_0')");
gates.G5 = { pass: !!eraOk };
console.log('G5', JSON.stringify(gates.G5));

gates.ALL_PASS = gates.G1.pass && gates.G2.pass && gates.G3.pass && gates.G4.pass && gates.G5.pass;
gates.consoleMsgs = consoleMsgs.slice(0, 60);
await fs.writeFile(`${SCI}\\av2_gates.json`, JSON.stringify(gates, null, 2));
console.log('ALL_PASS =', gates.ALL_PASS);
ws.close();
chrome.kill();
process.exit(gates.ALL_PASS ? 0 : 2);
