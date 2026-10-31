// tools/av3/gates.mjs — AV-3 browser gates (headless Chrome + raw CDP, the
// proven av2/gates.mjs pattern). Per model (206264 KINEMATIC/EMBEDDED anchor,
// 103004 + 103005 with NiTextKeyExtraData textkeys):
//   KF1 model loads IR_READY with keyframeAnim closure-exact
//   KF2 clip list has a KF clip with >0 tracks; play it; activeTracks > 0;
//       mixer time advances after play
//   KF3 RIGID-SEGMENT MOTION: world position of an animated target node
//       changes between t=0, playback and seek (visible rigid movement)
//   KF4 seek works (time moves to a different value)
//   KF5 __AV_NAN_CHECK__ = 0 non-finite values in the animated subtree
//   KF6 zero page errors
'use strict';
import { spawn } from 'node:child_process';
import { promises as fs } from 'node:fs';

const BASE = process.env.AV_BASE_URL || 'http://127.0.0.1:8141';
const SCI = process.env.AV_SCI_DIR ||
  'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV3_ANIMATION';
const URL_PAGE = `${BASE}/compat/assets.html`;
const MODELS = [206264, 103004, 103005];

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const DEBUG_PORT = 8153;
const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  `--remote-debugging-port=${DEBUG_PORT}`, '--user-data-dir=C:/Users/User/AppData/Local/Temp/opencode/cdp_profile_av3',
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
for (let i = 0; i < 120; i++) {
  if (await ev('window.__AV_STATE__ && __AV_STATE__.doneIndex ? true : false')) break;
  await sleep(500);
}

const gates = { url: URL_PAGE, models: {} };
for (const id of MODELS) {
  const g = { id };
  await ev(`__AV_LOAD_MODEL__(${id})`);
  let st = null;
  for (let i = 0; i < 120; i++) {
    st = await ev('__AV_STATE__');
    if (st && st.currentId === id && (st.modelStatus === 'IR_READY' || String(st.modelStatus).startsWith('UNSUPPORTED') || st.modelStatus === 'LOAD_FAIL')) break;
    await sleep(500);
  }
  g.KF1 = { status: st?.modelStatus, parseStatus: st?.parseStatus, kf: st?.anim?.kf ?? null,
    pass: st?.modelStatus === 'IR_READY' && !!st?.anim?.kf && st.anim.kf.clips > 0 && st.anim.kf.closureAll === true };
  const info = await ev('__AV_KF_INFO__()');
  g.KF2 = { clips: info?.clips, tracks: info?.tracks, names: info?.names, durations: info?.durations,
    pass: info && info.clips > 0 && info.tracks > 0 };
  const kfIdx = info?.kfIdx?.[0] ?? -1;
  if (kfIdx >= 0) {
    // motion: node world position at t=0
    const tgt = info.anim.firstController.target;
    const p0 = await ev(`__AV_NODE_POS__(${tgt})`);
    await ev(`__AV_PLAY__(${kfIdx})`);
    await sleep(1800); // let the render loop drive the mixer
    const st2 = await ev('__AV_STATE__.anim');
    const pMid = await ev(`__AV_NODE_POS__(${tgt})`);
    await ev('__AV_SEEK__(0.5)');
    const st3 = await ev('__AV_STATE__.anim');
    const pSeek = await ev(`__AV_NODE_POS__(${tgt})`);
    const moved = (a, b) => a && b && (Math.abs(a[0] - b[0]) + Math.abs(a[1] - b[1]) + Math.abs(a[2] - b[2]) > 1e-6);
    g.KF2.play = { pass: st2?.activeTracks > 0 && st2?.time > 0, activeTracks: st2?.activeTracks, timeAfterPlay: st2?.time };
    g.KF3 = { pass: moved(p0, pMid) || moved(p0, pSeek), posT0: p0, posPlaying: pMid, posSeek: pSeek,
      note: 'rigid-segment motion: animated target node world position changes' };
    g.KF4 = { pass: st3?.time > 0 && Math.abs(st3.time - st2.time) > 1e-9, timeAfterSeek: st3?.time };
    const nan = await ev('__AV_NAN_CHECK__()');
    g.KF5 = { pass: nan && nan.naN === 0 && nan.checked > 0, ...nan };
    await shot(`g_kf_${id}`);
    await ev('__AV_PLAY__(-1)');
  } else {
    g.KF2.play = { pass: false, reason: 'no KF clip index' };
    g.KF3 = { pass: false }; g.KF4 = { pass: false }; g.KF5 = { pass: false };
  }
  g.pass = g.KF1.pass && g.KF2.pass && g.KF2.play.pass && g.KF3.pass && g.KF4.pass && g.KF5.pass;
  gates.models[id] = g;
  console.log(`KF ${id}`, JSON.stringify(g.pass), JSON.stringify({ tracks: g.KF2.tracks, active: g.KF2.play?.activeTracks, motion: g.KF3.pass, seek: g.KF4.pass, nan: g.KF5.naN }));
}

const exc = consoleMsgs.filter((c) => c.type === 'EXCEPTION' || c.type === 'error');
gates.KF6 = { pass: exc.length === 0, errorCount: exc.length, errors: exc.slice(0, 10) };
gates.ALL_PASS = Object.values(gates.models).every((m) => m.pass) && gates.KF6.pass;
gates.consoleMsgs = consoleMsgs.slice(0, 60);
await fs.writeFile(`${SCI}\\av3_browser_gates.json`, JSON.stringify(gates, null, 2));
console.log('ALL_PASS =', gates.ALL_PASS);
ws.close();
chrome.kill();
process.exit(gates.ALL_PASS ? 0 : 2);
