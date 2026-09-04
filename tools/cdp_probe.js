// cdp_probe.js — raw CDP headless-Chrome probe for the clean runtime pages
// (Playwright MCP is known-flaky; the project's proven route is raw CDP —
// same route as the ITER 019 r185 calibration gate).
// Usage: node tools/cdp_probe.js <url> <waitForGlobal> <outJsonPath> [outPngPath]
'use strict';
import { spawn } from 'node:child_process';
import { promises as fs } from 'node:fs';

const [url, waitFor, outJson, outPng] = process.argv.slice(2);
if (!url || !waitFor || !outJson) throw new Error('usage: node cdp_probe.js <url> <waitForGlobal> <outJson> [outPng]');

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const DEBUG_PORT = 8133;

const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
  `--remote-debugging-port=${DEBUG_PORT}`, '--user-data-dir=C:/Users/User/AppData/Local/Temp/opencode/cdp_profile',
  'about:blank',
], { stdio: 'ignore' });
console.log('chrome pid', chrome.pid);

async function getTarget() {
  for (let i = 0; i < 40; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
      const list = await res.json();
      const page = list.find((t) => t.type === 'page');
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
    consoleMsgs.push({ type: 'EXCEPTION', text: JSON.stringify(m.params.exceptionDetails) });
  }
};

function send(method, params = {}) {
  return new Promise((resolve) => {
    const id = ++msgId;
    pending.set(id, resolve);
    ws.send(JSON.stringify({ id, method, params }));
  });
}

await send('Page.enable');
await send('Runtime.enable');
await send('Emulation.setDeviceMetricsOverride', { width: 1100, height: 820, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url });
// poll for the result global (up to 120 s — 1.1GB of fetch+decode happens)
let result = null;
for (let i = 0; i < 480; i++) {
  const r = await send('Runtime.evaluate', { expression: `typeof window.${waitFor} !== 'undefined' ? window.${waitFor} : undefined`, returnByValue: true, awaitPromise: false });
  if (r.result?.result?.value) { result = r.result.result.value; break; }
  await new Promise((res) => setTimeout(res, 250));
}
if (!result) {
  // dump what the page said before failing
  console.log('RESULT GLOBAL NOT READY. Console tail:');
  for (const c of consoleMsgs.slice(-15)) console.log(`  [${c.type}] ${c.text}`);
  throw new Error(`window.${waitFor} not available in time`);
}

let pngB64 = null;
if (outPng) {
  const shot = await send('Page.captureScreenshot', { format: 'png' });
  pngB64 = shot.result.data;
  await fs.writeFile(outPng, Buffer.from(pngB64, 'base64'));
}

await fs.writeFile(outJson, JSON.stringify({
  url, waitFor, result, consoleMsgs: consoleMsgs.slice(0, 80),
}, null, 2));
console.log(`probe OK — result written to ${outJson}${outPng ? ', screenshot to ' + outPng : ''}`);
ws.close();
chrome.kill();
process.exit(0);
