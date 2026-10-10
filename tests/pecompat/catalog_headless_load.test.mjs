// catalog_headless_load.test.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W6)
// T9-STYLE REAL-BROWSER LOAD of /catalog through the FIXED 5-conjunct gate:
//   exitCode===0 AND DOM_NONEMPTY AND CANVAS_PRESENT AND DIAGNOSTICS_PRESENT
//   AND STATUS_READY (data-load-status==='READY').
// Every conjunct is evaluated SEPARATELY with per-conjunct records — the SAME
// production predicate evaluateLoadGate() the 218757 app loads use (IMPORTED
// from tests/pecompat/headless_load.test.mjs, NOT reimplemented — the gate
// semantics stay identical by construction).
//
// Loads:
//   1. /catalog            — the catalog table page (rows rendered, READY)
//   2. /catalog#model=193313 — the deep-linked PREVIEW page (wire fetched,
//      preview mounted, materials applied markers in the DOM, READY)
//
// REUSE LABELS: evaluateLoadGate + LOAD_GATE_CONJUNCTS imported UNCHANGED
// from the fixed T9 suite; the headless spawn pattern (headless Edge
// --headless=new --dump-dom with a DEDICATED temp profile, bounded timeout,
// profile-mark-scoped leftover cleanup, bounded flake retry max 3 attempts,
// all attempts recorded) follows headless_load.test.mjs with a SEPARATE
// profile mark. The server lifecycle is owned by this suite via
// _catalog_server_helpers.mjs.
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  startCatalogServer, stopCatalogServer, findFreePort,
} from './_catalog_server_helpers.mjs';
import { evaluateLoadGate, LOAD_GATE_CONJUNCTS } from './headless_load.test.mjs';

const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';
const PROFILE_MARK = 'pec-city-asset-map-catalog-headless';

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
    const p = process.env.PECOMPAT_BROWSER_BIN;
    if (existsSync(p)) {
      const base = path.basename(p).toLowerCase();
      const known = base === 'msedge.exe' || base === 'chrome.exe';
      return { path: p, provenance: 'PECOMPAT_BROWSER_BIN env override', envOverride: true, knownBrowserBinary: known, standIn: !known };
    }
    return { path: null, provenance: `PECOMPAT_BROWSER_BIN env override set to a MISSING path (${p})`, envOverride: true, knownBrowserBinary: false, standIn: true };
  }
  const found = BROWSER_CANDIDATES.find((p) => existsSync(p));
  return { path: found ?? null, provenance: found ? 'first existing default browser candidate' : 'no default browser candidate exists', envOverride: false, knownBrowserBinary: Boolean(found), standIn: false };
}

function killOwnLeftoverEdge() {
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
    for (const pid of pids) { try { process.kill(Number(pid)); } catch { /* already gone */ } }
    return pids;
  } catch { return []; }
}

function headlessDumpDom(browserBin, url, { timeoutMs = 90000 } = {}) {
  return new Promise((resolve, reject) => {
    const userDataDir = path.join(os.tmpdir(), 'opencode', `${PROFILE_MARK}-${Date.now()}`);
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
      killOwnLeftoverEdge();
      resolve({ domText: dom, stderr: stderr.slice(0, 2000), exitCode: null, elapsedMs: Date.now() - t0, userDataDir, timedOut: true });
    }, timeoutMs);
    child.once('exit', (code) => {
      clearTimeout(timer);
      killOwnLeftoverEdge();
      resolve({ domText: dom, stderr: stderr.slice(0, 2000), exitCode: code, elapsedMs: Date.now() - t0, userDataDir, timedOut: false });
    });
  });
}

export async function run(ctx) {
  const rawDir = ctx.rawDir;
  await mkdir(rawDir, { recursive: true });
  const records = [];

  const bin = findBrowserBinary();
  if (!bin.path) {
    for (const id of ['CAT_T9_LOAD_CATALOG', 'CAT_T9_LOAD_PREVIEW']) {
      records.push(rec(id, 'real headless-browser load of /catalog', 'NOT_PERFORMED', {
        resultClass: 'REAL_BROWSER_HEADLESS_DOM (not executed)',
        measuredQuantity: 'browser binary availability',
        measured: { candidatesChecked: BROWSER_CANDIDATES, provenance: bin.provenance },
        failureCaseDetected: 'NO browser binary available headless on this host — honest NOT_PERFORMED; BROWSER_VERIFICATION stays NOT_PERFORMED for this gate',
      }));
    }
    return records;
  }

  const port = await findFreePort(8161);
  let server;
  try {
    server = await startCatalogServer({ port, timeoutMs: 180000 });
  } catch (e) {
    records.push(rec('CAT_T9_SERVER_STARTUP', 'suite-owned catalog server startup (SIDE-ERROR class — never conflated with the browser gate records)', 'FAIL', {
      measuredQuantity: 'server startup for the headless loads',
      measured: String(e?.message ?? e).slice(0, 2000),
      failureCaseDetected: 'the catalog server failed to start — the browser loads could NOT run (fail-closed; not a browser conjunct result)',
    }));
    for (const id of ['CAT_T9_LOAD_CATALOG', 'CAT_T9_LOAD_PREVIEW']) {
      records.push(rec(id, 'real headless-browser load of /catalog', 'NOT_PERFORMED', {
        resultClass: 'REAL_BROWSER_HEADLESS_DOM (not executed)',
        measuredQuantity: 'server availability',
        measured: { serverStartupFailed: true },
        failureCaseDetected: 'server startup failed — load not attempted (honest NOT_PERFORMED, not a conjunct FAIL)',
      }));
    }
    return records;
  }

  const urls = [
    ['CAT_T9_LOAD_CATALOG', 'catalog table page (both eras, rows rendered)', `http://127.0.0.1:${port}/catalog`, 'CATALOG_DOM_DUMP_TABLE.html'],
    ['CAT_T9_LOAD_PREVIEW', 'preview deep link #model=193313 (wire fetched, preview mounted)', `http://127.0.0.1:${port}/catalog#model=193313`, 'CATALOG_DOM_DUMP_PREVIEW.html'],
  ];

  const MAX_ATTEMPTS = 3;
  const loadRuns = [];
  for (const [id, modeName, url, dumpFile] of urls) {
    const attempts = [];
    let best = null;
    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
      let out = null;
      let execError = null;
      try {
        out = await headlessDumpDom(bin.path, url);
      } catch (e) { execError = e; }
      const gate = evaluateLoadGate({
        exitCode: out ? out.exitCode : undefined,
        domText: out ? out.domText : '',
      });
      const a = { attempt, out, gate, execError, passed: gate.passed && !execError && !(out && out.timedOut) };
      attempts.push(a);
      if (a.passed) { best = a; break; }
      if (!best) best = a;
    }
    const final = attempts.find((a) => a.passed) ?? attempts[0];
    loadRuns.push({ id, modeName, url, dumpFile, final, attempts });
    const gate = final.gate;
    const out = final.out;
    const pass = final.passed;
    // page-specific content markers (beyond the 5 conjuncts — honest extras):
    const dom = out?.domText ?? '';
    const extra = id === 'CAT_T9_LOAD_CATALOG'
      ? { catalogTable: /id="catalog-table"/.test(dom), eraBadges: /era-CD_2003/.test(dom), unknownBadge: /unknown-badge/.test(dom) || /UNKNOWN/.test(dom) }
      : { previewTitle: /preview:/i.test(dom), untexturedDiag: /UNTEXTURED_PROXY_MESH/.test(dom), materialsApplied: /APPLIED \(material preview\)/.test(dom), boundsDiag: /maxAxisExtent/.test(dom) };
    const extraOk = Object.values(extra).every(Boolean);
    records.push(rec(id, `real headless-browser load — ${modeName} — 5-conjunct gate (per-conjunct records) + page content markers`, (pass && extraOk) ? 'PASS' : 'FAIL', {
      resultClass: bin.standIn
        ? 'STAND_IN_PROCESS (env override; NOT a real-browser positive control)'
        : 'REAL_BROWSER_HEADLESS_DOM',
      measuredQuantity: 'captured DOM markers + browser exit code through the production evaluateLoadGate (imported from the fixed T9 suite) + page content markers',
      measured: {
        browserBinary: bin.path,
        knownBrowserBinary: bin.knownBrowserBinary,
        url,
        attemptCount: attempts.length,
        conjuncts: gate.conjuncts,          // PER-CONJUNCT RECORDS (separate)
        missingConjuncts: gate.missing,
        loadStatus: gate.loadStatus,
        domBytes: gate.domBytes,
        exitCode: gate.exitCode,
        elapsedMs: out ? out.elapsedMs : null,
        timedOut: out ? out.timedOut : null,
        pageContentMarkers: extra,
      },
      missingConjuncts: gate.missing,
      independentSourceOfTruth: 'the real browser DOM dump (Edge headless=new) — not an HTTP status or a unit test',
      whyNonCircular: 'a real browser engine parsed and executed the catalog page; the markers come from the live document',
      failureCaseDetected: final.execError
        ? `browser execution error (fail-closed): ${String(final.execError.message ?? final.execError).slice(0, 400)}`
        : (gate.passed
          ? (extraOk ? 'none — all five conjuncts hold and the page content markers are present' : 'gate conjuncts hold but page content markers missing (page defect or premature capture)')
          : `MISSING CONJUNCT(S): ${gate.missing.join(', ')}`),
    }));
  }

  // raw persistence (SEPARATE side-error record)
  let persistError = null;
  const persisted = [];
  try {
    for (const r of loadRuns) {
      const file = path.join(rawDir, r.dumpFile);
      const domText = r.final.out ? r.final.out.domText : '(no capture)';
      await writeFile(file, domText, 'utf8');
      persisted.push({ file: r.dumpFile, bytes: domText.length });
    }
    await writeFile(path.join(rawDir, 'CATALOG_HEADLESS_RUN.json'), JSON.stringify({
      run: RUN_ID,
      suite: 'tests/pecompat/catalog_headless_load.test.mjs',
      gate: 'evaluateLoadGate imported from tests/pecompat/headless_load.test.mjs (the FIXED T9 5-conjunct gate — identical semantics)',
      conjuncts: LOAD_GATE_CONJUNCTS,
      browserBinary: bin.path,
      standInBinary: bin.standIn,
      port,
      pid: server.pid,
      loads: loadRuns.map((r) => ({
        id: r.id, url: r.url, attemptCount: r.attempts.length,
        exitCode: r.final.gate.exitCode, domBytes: r.final.gate.domBytes,
        loadStatus: r.final.gate.loadStatus, conjuncts: r.final.gate.conjuncts,
        missingConjuncts: r.final.gate.missing,
        timedOut: r.final.out ? r.final.out.timedOut : null,
        allAttempts: r.attempts.map((a) => ({
          attempt: a.attempt, exitCode: a.gate.exitCode, domBytes: a.gate.domBytes,
          loadStatus: a.gate.loadStatus, missingConjuncts: a.gate.missing, timedOut: a.out ? a.out.timedOut : null,
        })),
      })),
    }, null, 1) + '\n', 'utf8');
    persisted.push({ file: 'CATALOG_HEADLESS_RUN.json' });
    for (const r of loadRuns) {
      for (const a of r.attempts) {
        if (a.out && a.out.userDataDir) await rm(a.out.userDataDir, { recursive: true, force: true }).catch(() => {});
      }
    }
  } catch (e) { persistError = e; }
  records.push(rec('CAT_T9_RAW_PERSISTENCE', 'raw capture persistence (SIDE-ERROR class — the browser-gate statuses above were computed independently of this record)', persistError ? 'FAIL' : 'PASS', {
    measuredQuantity: 'writeFile of the DOM dumps + CATALOG_HEADLESS_RUN.json',
    measured: persistError ? String(persistError.message ?? persistError).slice(0, 1000) : { persisted },
    failureCaseDetected: persistError ? 'raw persistence failed (side error)' : 'none',
  }));

  // server lifecycle (SEPARATE record)
  const stop = await stopCatalogServer(server);
  records.push(rec('CAT_T9_SERVER_LIFECYCLE', `suite-owned bounded catalog server lifecycle (pid ${server.pid}, port ${port}; stop + port-freed proof)`, stop.portFreed ? 'PASS' : 'FAIL', {
    measuredQuantity: 'start/stop/PID/lifetime/port-freed proof',
    measured: {
      pid: server.pid, port, lifetimeMs: stop.lifetimeMs,
      killed: stop.killed, exitCode: stop.exitCode, signal: stop.signal,
      portFreed: stop.portFreed, freedAfterMs: stop.freedAfterMs,
    },
    failureCaseDetected: stop.portFreed ? 'none — server stopped, port freed' : 'port NOT freed (LIFECYCLE BREACH)',
  }));

  return records;
}
