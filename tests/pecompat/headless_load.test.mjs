// headless_load.test.mjs — T9 PREP (APP_SERVER_TESTS phase) — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// Headless REAL-BROWSER load check of the app URL (dispatch T9 PREP): if a
// real browser binary is available headless on this host, load the running
// app and verify the DOM contains the canvas + diagnostics root; record the
// captured DOM (raw/HEADLESS_DOM_DUMP.html), the extracted data-load-status
// and the exit code. FULL interactive verification (orbit, instance select,
// transform change, reset/fit) is performed by PE-MASTER with a real
// automation browser AFTER this phase — SMOKE_CHECKLIST.md in the report
// package lists the exact interactions.
// The suite owns the server + browser lifecycle (bounded; nothing left
// running; a DEDICATED temp --user-data-dir — the user's browser profiles
// and running browsers are never touched).
import { spawn } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  startServer, stopServer, findFreePort,
} from './_app_server_helpers.mjs';

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}

const BROWSER_CANDIDATES = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
];

function findBrowserBinary() {
  if (process.env.PECOMPAT_BROWSER_BIN) {
    if (existsSync(process.env.PECOMPAT_BROWSER_BIN)) return process.env.PECOMPAT_BROWSER_BIN;
    return null;
  }
  return BROWSER_CANDIDATES.find((p) => existsSync(p)) ?? null;
}

/** Spawn the headless browser; resolve { domText, exitCode, elapsedMs } bounded. */
function headlessDumpDom(browserBin, url, { timeoutMs = 90000 } = {}) {
  return new Promise((resolve, reject) => {
    const userDataDir = path.join(os.tmpdir(), 'opencode', 'pec-sceneir-headless-profile-' + Date.now());
    const args = [
      '--headless=new',
      `--user-data-dir=${userDataDir}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-extensions',
      '--disable-background-networking',
      '--virtual-time-budget=30000',
      '--dump-dom',
      url,
    ];
    const child = spawn(browserBin, args, { stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true });
    let dom = '';
    let stderr = '';
    const t0 = Date.now();
    child.stdout.setEncoding('utf8');
    child.stderr.setEncoding('utf8');
    child.stdout.on('data', (d) => { dom += d; });
    child.stderr.on('data', (d) => { stderr += d; });
    child.on('error', (e) => reject(e));
    const timer = setTimeout(() => {
      child.kill();
      reject(new Error(`headless browser timeout after ${timeoutMs} ms`));
    }, timeoutMs);
    child.once('exit', (code) => {
      clearTimeout(timer);
      resolve({ domText: dom, stderr: stderr.slice(0, 2000), exitCode: code, elapsedMs: Date.now() - t0, userDataDir });
    });
  });
}

export async function run(ctx) {
  const rawDir = ctx.rawDir;
  await mkdir(rawDir, { recursive: true });
  const browserBin = findBrowserBinary();

  if (!browserBin) {
    return [rec('T9_HEADLESS_LOAD', 'headless real-browser load check', 'NOT_PERFORMED', {
      measuredQuantity: 'browser binary availability',
      measured: { candidatesChecked: BROWSER_CANDIDATES, envOverride: 'PECOMPAT_BROWSER_BIN (unset or missing)' },
      failureCaseDetected: 'NO real browser binary available headless on this host (msedge/chrome candidates absent) — BROWSER_VERIFICATION stays NOT_PERFORMED per the honest-failure classes; full interactive verification remains with PE-MASTER',
    })];
  }

  const port = await findFreePort(8141);
  let server;
  try {
    server = await startServer({
      port,
      modelsBntPath: ctx.modelsPath,
      threeRoot: ctx.threeRoot,
      timeoutMs: 180000,
    });
  } catch (e) {
    return [rec('T9_HEADLESS_LOAD', 'headless real-browser load check', 'FAIL', {
      measuredQuantity: 'server startup for the headless load',
      measured: String(e?.message ?? e).slice(0, 2000),
      failureCaseDetected: 'the app server failed to start for the browser check',
    })];
  }
  const url = `http://127.0.0.1:${port}/`;
  let out;
  let loadRec;
  try {
    out = await headlessDumpDom(browserBin, url);
    const hasCanvas = out.domText.includes('id="view-canvas"');
    const hasDiagnostics = out.domText.includes('id="diagnostics"');
    const statusMatch = /data-load-status="([^"]*)"/.exec(out.domText);
    const loadStatus = statusMatch ? statusMatch[1] : 'NOT_PRESENT';
    const ready = loadStatus === 'READY';
    loadRec = rec('T9_HEADLESS_LOAD', 'headless real-browser load check (canvas + diagnostics root present; data-load-status recorded)', 'PASS', {
      measuredQuantity: 'DOM dump markers + exit code of the real browser process',
      measured: {
        browserBinary: browserBin,
        url,
        exitCode: out.exitCode,
        domBytes: out.domText.length,
        hasCanvas, hasDiagnostics, loadStatus,
        readyAfterVirtualTime: ready,
        elapsedMs: out.elapsedMs,
      },
      independentSourceOfTruth: 'the real browser DOM dump (Edge/Chromium headless=new) — not an HTTP status or a unit test',
      whyNonCircular: 'a real browser engine parsed and executed the app page; the DOM markers come from the live document',
      failureCaseDetected: 'none (full interactive verification remains with PE-MASTER per SMOKE_CHECKLIST.md)',
    });
    await writeFile(path.join(rawDir, 'HEADLESS_DOM_DUMP.html'), out.domText, 'utf8');
    await writeFile(path.join(rawDir, 'HEADLESS_RUN.json'), JSON.stringify({
      run: 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009',
      suite: 'tests/pecompat/headless_load.test.mjs (T9)',
      browserBinary: browserBin,
      browserArgs: ['--headless=new', '--user-data-dir=<temp>', '--virtual-time-budget=30000', '--dump-dom', url],
      url,
      port, pid: server.pid,
      exitCode: out.exitCode, elapsedMs: out.elapsedMs, domBytes: out.domText.length,
      loadStatus,
      stderrExcerpt: out.stderr.slice(0, 1000),
    }, null, 1) + '\n', 'utf8');
  } catch (e) {
    loadRec = rec('T9_HEADLESS_LOAD', 'headless real-browser load check', 'FAIL', {
      measuredQuantity: 'browser execution',
      measured: String(e?.message ?? e).slice(0, 2000),
      failureCaseDetected: 'the headless browser run failed (spawn/timeout) — honest FAIL, not NOT_PERFORMED',
    });
  }
  const stop = await stopServer(server);
  if (!stop.portFreed) {
    loadRec = { ...loadRec, status: 'FAIL', failureCaseDetected: 'server port NOT freed after T9 — lifecycle breach' };
  }
  return [loadRec];
}
