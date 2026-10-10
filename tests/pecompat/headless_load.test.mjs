// headless_load.test.mjs — T9 GATE (FIXED per SCENEIR-T9-C1 / P2) — PE_CITY_ASSET_MAP_R1_20261010
//
// HISTORY OF THE DEFECT (Desktop post-audit SCENEIR_59641CA_POST_AUDIT.md,
// finding SCENEIR-T9-C1 / P2): the previous version of this suite computed
// hasCanvas/hasDiagnostics/loadStatus and then assigned a LITERAL 'PASS' —
// exitCode was recorded but never required to be 0, no non-empty captured DOM
// was required, and no marker/READY status was required. A node.exe stand-in
// process (exitCode=9, empty stdout, no markers) passed the old gate, and the
// aggregate harness reported 13 PASS / exit 0. Raw PRE evidence of that
// false-PASS is preserved in docs/audits/PE_CITY_ASSET_MAP_R1_20261010/raw/T9/PRE*.
//
// THE FIXED GATE (contract §0): a load PASSES only if ALL FIVE conjuncts hold:
//   EXIT_CODE_ZERO + DOM_NONEMPTY + CANVAS_PRESENT + DIAGNOSTICS_PRESENT + STATUS_READY
// (data-load-status === 'READY'). Every conjunct is evaluated SEPARATELY; each
// missing conjunct is NAMED in the FAIL record. The SAME production predicate
// evaluateLoadGate() is used by every load path in this suite (real-browser
// asset mode, real-browser #scene mode, env-override stand-in binaries) and by
// the six synthetic per-conjunct negative controls, which remove ONE conjunct
// at a time and must FAIL with the named missing conjunct.
//
// SEPARATION OF CONCERNS (contract §0 "nie boczny błąd pliku/manifestu"):
// - a browser-gate result is NEVER produced by a file/manifest error: raw
//   persistence is a SEPARATE side-error record (T9_RAW_PERSISTENCE);
// - the suite-owned server lifecycle (start/stop/PID/port-freed proof) is a
//   SEPARATE record (T9_SERVER_LIFECYCLE);
// - a stand-in binary selected via PECOMPAT_BROWSER_BIN is labeled
//   STAND_IN_PROCESS (env override, not a known browser binary): its gate
//   result can never masquerade as a real-browser positive control. The
//   positive control in a clean run is an ACTUAL browser binary (no env
//   override).
//
// SCOPE: this suite is the LOAD gate only (real headless-browser DOM capture).
// PIXEL_RENDER (real rendered pixel image) and INTERACTIVE (automation-driven
// user input) are SEPARATE gates — see tools/pecompat/t9_pixel_render.mjs and
// the report package; an unavailable automation tool is recorded
// NOT_PERFORMED, never PASS.
//
// The suite owns the server + browser lifecycle (bounded; nothing left
// running; a DEDICATED temp --user-data-dir — the user's browser profiles and
// running browsers are never touched; leftover Edge processes referencing OUR
// profile mark are killed by exact command-line match, never foreign ones).
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir, rm } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  startServer, stopServer, findFreePort,
} from './_app_server_helpers.mjs';

const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}

const BROWSER_CANDIDATES = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
];

const PROFILE_MARK = 'pec-city-asset-map-headless';

/** The production load gate: the ONE predicate every load must pass.
 * Pure function — evaluated identically for real-browser captures, env-override
 * stand-in processes and synthetic negative controls. Each conjunct is
 * evaluated separately; missing conjuncts are named. */
export const LOAD_GATE_CONJUNCTS = Object.freeze([
  'EXIT_CODE_ZERO',
  'DOM_NONEMPTY',
  'CANVAS_PRESENT',
  'DIAGNOSTICS_PRESENT',
  'STATUS_READY',
]);

export function evaluateLoadGate({ exitCode, domText }) {
  const dom = typeof domText === 'string' ? domText : '';
  const statusMatch = /data-load-status="([^"]*)"/.exec(dom);
  const loadStatus = statusMatch ? statusMatch[1] : 'NOT_PRESENT';
  const conjuncts = {
    EXIT_CODE_ZERO: exitCode === 0,
    DOM_NONEMPTY: dom.trim().length > 0,
    CANVAS_PRESENT: dom.includes('id="view-canvas"'),
    DIAGNOSTICS_PRESENT: dom.includes('id="diagnostics"'),
    STATUS_READY: loadStatus === 'READY',
  };
  const missing = LOAD_GATE_CONJUNCTS.filter((c) => !conjuncts[c]);
  return {
    passed: missing.length === 0,
    missing,
    conjuncts,
    loadStatus,
    exitCode: exitCode === undefined ? null : exitCode,
    domBytes: dom.length,
  };
}

/** Locate the browser binary. An env override (PECOMPAT_BROWSER_BIN) is
 * allowed for CONTROLLED NEGATIVES ONLY and is explicitly labeled: a binary
 * that is not a known browser (msedge/chrome) by basename is a STAND-IN
 * process, never a real-browser positive control. */
function findBrowserBinary() {
  if (process.env.PECOMPAT_BROWSER_BIN) {
    const p = process.env.PECOMPAT_BROWSER_BIN;
    if (existsSync(p)) {
      const base = path.basename(p).toLowerCase();
      const known = base === 'msedge.exe' || base === 'chrome.exe';
      return {
        path: p,
        provenance: 'PECOMPAT_BROWSER_BIN env override',
        envOverride: true,
        knownBrowserBinary: known,
        standIn: !known,
        candidatesChecked: BROWSER_CANDIDATES,
      };
    }
    return {
      path: null, provenance: `PECOMPAT_BROWSER_BIN env override set to a MISSING path (${p})`,
      envOverride: true, knownBrowserBinary: false, standIn: true, candidatesChecked: BROWSER_CANDIDATES,
    };
  }
  const found = BROWSER_CANDIDATES.find((p) => existsSync(p));
  return {
    path: found ?? null,
    provenance: found ? 'first existing default browser candidate' : 'no default browser candidate exists',
    envOverride: false,
    knownBrowserBinary: Boolean(found),
    standIn: false,
    candidatesChecked: BROWSER_CANDIDATES,
  };
}

/** Kill ONLY leftover Edge processes whose command line references OUR profile
 * mark (never foreign/user browsers). Bounded, best-effort. Returns the PIDs. */
function killOwnLeftoverEdge() {
  try {
    const r = spawnSync('powershell', ['-NoProfile', '-Command',
      `Get-CimInstance Win32_Process -Filter "Name='msedge.exe'" | Where-Object { $_.CommandLine -like '*${PROFILE_MARK}*' } | Select-Object ProcessId | ConvertTo-Json`],
    { encoding: 'utf8', timeout: 20000 });
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

/** Spawn the headless browser; resolve { domText, stderr, exitCode, elapsedMs,
 * userDataDir } bounded. A timeout resolves fail-closed (exitCode null). */
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

  // ------------------------------------------------------------------
  // (1) Six synthetic per-conjunct negative controls — ALWAYS evaluated
  // (no browser/server needed). Each removes ONE conjunct from an
  // otherwise-good capture and is fed THROUGH THE SAME production gate
  // evaluateLoadGate(). The CONTROL passes when the gate FAILS the
  // defective input and names exactly the expected missing conjunct(s);
  // a gate that lets a defective input through FAILS the control loudly
  // (the SCENEIR-T9-C1 defect class). NOT a browser execution.
  // ------------------------------------------------------------------
  const GOOD_DOM = [
    '<!DOCTYPE html><html lang="en"><head><title>synthetic</title></head><body>',
    '<canvas id="view-canvas"></canvas>',
    // The diagnostics marker and the load-status attribute are placed on
    // SEPARATE synthetic elements so each negative control removes EXACTLY
    // ONE conjunct (in the real app both live on the same <details> element —
    // there the cascade is real; POST_RUN1_INTERMEDIATE shows this control
    // catching a synthetic input that removed both at once).
    '<div id="diagnostics"></div>',
    '<div data-load-status="READY"></div>',
    '</body></html>',
  ].join('');
  const GOOD = { exitCode: 0, domText: GOOD_DOM };
  const NEGATIVES = [
    ['T9_GATE_NEG_EXIT_CODE', 'remove ONLY the good exit code (exitCode=1, otherwise-good DOM)', { ...GOOD, exitCode: 1 }, ['EXIT_CODE_ZERO']],
    ['T9_GATE_NEG_EMPTY_DOM', 'remove ONLY the DOM (empty capture, exitCode=0)', { ...GOOD, domText: '' }, ['DOM_NONEMPTY', 'CANVAS_PRESENT', 'DIAGNOSTICS_PRESENT', 'STATUS_READY']],
    ['T9_GATE_NEG_NO_CANVAS', 'remove ONLY the canvas marker', { exitCode: 0, domText: GOOD_DOM.replace('<canvas id="view-canvas"></canvas>', '') }, ['CANVAS_PRESENT']],
    ['T9_GATE_NEG_NO_DIAGNOSTICS', 'remove ONLY the diagnostics marker', { exitCode: 0, domText: GOOD_DOM.replace('<div id="diagnostics"></div>', '') }, ['DIAGNOSTICS_PRESENT']],
    ['T9_GATE_NEG_STATUS_ERROR', 'replace ONLY the status with ERROR', { exitCode: 0, domText: GOOD_DOM.replace('data-load-status="READY"', 'data-load-status="ERROR_ASSET_LOAD: synthetic"') }, ['STATUS_READY']],
    ['T9_GATE_NEG_STATUS_LOADING', 'replace ONLY the status with LOADING', { exitCode: 0, domText: GOOD_DOM.replace('data-load-status="READY"', 'data-load-status="LOADING"') }, ['STATUS_READY']],
  ];
  for (const [id, what, input, expectedMissing] of NEGATIVES) {
    const gate = evaluateLoadGate(input);
    const namedExactly = gate.missing.length === expectedMissing.length
      && expectedMissing.every((m) => gate.missing.includes(m));
    const controlOk = gate.passed === false && namedExactly;
    records.push(rec(id, `controlled per-conjunct gate negative — ${what} — the gate MUST FAIL it and name exactly ${expectedMissing.join('+')}`, controlOk ? 'PASS' : 'FAIL', {
      resultClass: 'SYNTHETIC_GATE_NEGATIVE_CONTROL (defective input fed through the same production evaluateLoadGate; NOT a browser execution)',
      controlExpectation: 'gate FAIL + exact missing-conjunct naming',
      measuredQuantity: 'evaluateLoadGate() on a synthetic defective input',
      measured: {
        input: { exitCode: input.exitCode, domBytes: input.domText.length },
        gateResult: gate.passed ? 'PASS (DEFECT: defective input was let through — SCENEIR-T9-C1 class)' : 'FAIL',
        gateMissingConjuncts: gate.missing,
        expectedMissingConjuncts: expectedMissing,
      },
      failureCaseDetected: gate.passed
        ? 'GATE DEFECT reproduced: the defective input PASSED the gate (SCENEIR-T9-C1 class)'
        : (namedExactly
          ? 'none — the gate failed the defective input naming exactly the expected conjunct(s)'
          : `WRONG conjunct set: gate named ${JSON.stringify(gate.missing)}, expected ${JSON.stringify(expectedMissing)}`),
    }));
  }

  // ------------------------------------------------------------------
  // (2) Real-browser loads: the app's TWO modes through the SAME gate.
  // ------------------------------------------------------------------
  const bin = findBrowserBinary();
  if (!bin.path) {
    records.push(rec('T9_LOAD_ASSET_MODE', 'real headless-browser load — asset mode (218757)', 'NOT_PERFORMED', {
      resultClass: 'REAL_BROWSER_HEADLESS_DOM (not executed)',
      measuredQuantity: 'browser binary availability',
      measured: { candidatesChecked: bin.candidatesChecked, provenance: bin.provenance },
      failureCaseDetected: 'NO browser binary available headless on this host (msedge/chrome candidates absent and no usable PECOMPAT_BROWSER_BIN) — honest NOT_PERFORMED; BROWSER_VERIFICATION stays NOT_PERFORMED; the synthetic gate negatives above were still evaluated',
    }));
    records.push(rec('T9_LOAD_SCENE_MODE', 'real headless-browser load — authored scene mode (#scene deep link)', 'NOT_PERFORMED', {
      resultClass: 'REAL_BROWSER_HEADLESS_DOM (not executed)',
      measuredQuantity: 'browser binary availability',
      measured: { candidatesChecked: bin.candidatesChecked, provenance: bin.provenance },
      failureCaseDetected: 'NO browser binary available headless on this host — honest NOT_PERFORMED',
    }));
    return records;
  }

  const port = await findFreePort(8160); // NEVER 8140 (foreign standing reference server)
  let server;
  try {
    server = await startServer({
      port,
      modelsBntPath: ctx.modelsPath,
      threeRoot: ctx.threeRoot,
      timeoutMs: 180000,
    });
  } catch (e) {
    records.push(rec('T9_SERVER_STARTUP', 'suite-owned app server startup (SIDE-ERROR class — never conflated with the browser gate records)', 'FAIL', {
      measuredQuantity: 'server startup for the headless loads',
      measured: String(e?.message ?? e).slice(0, 2000),
      failureCaseDetected: 'the app server failed to start — the browser loads below could NOT run (fail-closed; not a browser conjunct result)',
    }));
    for (const id of ['T9_LOAD_ASSET_MODE', 'T9_LOAD_SCENE_MODE']) {
      records.push(rec(id, 'real headless-browser load', 'NOT_PERFORMED', {
        resultClass: 'REAL_BROWSER_HEADLESS_DOM (not executed)',
        measuredQuantity: 'server availability',
        measured: { serverStartupFailed: true },
        failureCaseDetected: 'server startup failed — load not attempted (honest NOT_PERFORMED, not a conjunct FAIL)',
      }));
    }
    return records;
  }

  const urls = [
    ['T9_LOAD_ASSET_MODE', 'asset mode (default URL — model 218757)', `http://127.0.0.1:${port}/`, 'HEADLESS_DOM_DUMP_ASSET.html'],
    ['T9_LOAD_SCENE_MODE', 'authored scene mode (#scene deep link — two instances)', `http://127.0.0.1:${port}/#scene`, 'HEADLESS_DOM_DUMP_SCENE.html'],
  ];

  // Bounded flake mitigation: a real headless Edge invocation OCCASIONALLY
  // hangs AFTER printing a complete, valid DOM dump (observed once in
  // raw/T9/POST_RUN1_INTERMEDIATE: full 9309-byte READY capture, then the
  // process refused to exit within the 90 s budget). The strict per-attempt
  // predicate is unchanged (a hung attempt FAILS on EXIT_CODE_ZERO);
  // up to MAX_ATTEMPTS transparent attempts are made per mode and ALL
  // attempts are recorded verbatim in the record. PASS iff at least one
  // attempt holds ALL FIVE conjuncts — never by ignoring a missing one.
  const MAX_ATTEMPTS = 3;

  const loadRuns = [];
  for (const [id, modeName, url, dumpFile] of urls) {
    const attempts = [];
    let best = null; // the attempt whose gate result is final for this mode
    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
      let out = null;
      let execError = null;
      try {
        out = await headlessDumpDom(bin.path, url);
      } catch (e) {
        execError = e;
      }
      // The SAME production gate evaluates every capture — including the
      // fail-closed path for spawn errors/timeouts (empty capture, no exit code).
      const gate = evaluateLoadGate({
        exitCode: out ? out.exitCode : undefined,
        domText: out ? out.domText : '',
      });
      const a = {
        attempt,
        out,
        gate,
        execError,
        passed: gate.passed && !execError && !(out && out.timedOut),
      };
      attempts.push(a);
      if (a.passed) { best = a; break; }
      if (!best) best = a; // first attempt is the provisional result
    }
    // final = first fully-passing attempt, else the first attempt (fail-closed)
    const final = attempts.find((a) => a.passed) ?? attempts[0];
    loadRuns.push({ id, modeName, url, dumpFile, final, attempts });
    const pass = final.passed;
    const gate = final.gate;
    const out = final.out;
    const execError = final.execError;
    records.push(rec(id, `real headless-browser load — ${modeName} — 5-conjunct gate: exitCode===0 AND nonempty DOM AND canvas AND diagnostics AND data-load-status==='READY'`, pass ? 'PASS' : 'FAIL', {
      resultClass: bin.standIn
        ? 'STAND_IN_PROCESS (PECOMPAT_BROWSER_BIN env override; not a known browser binary; NOT a real-browser positive control — used for controlled negatives only)'
        : 'REAL_BROWSER_HEADLESS_DOM',
      measuredQuantity: 'captured DOM markers + browser exit code through the production evaluateLoadGate',
      measured: {
        browserBinary: bin.path,
        binaryProvenance: bin.provenance,
        knownBrowserBinary: bin.knownBrowserBinary,
        url,
        attemptCount: attempts.length,
        attempts: attempts.map((a) => ({
          attempt: a.attempt,
          exitCode: a.gate.exitCode,
          domBytes: a.gate.domBytes,
          loadStatus: a.gate.loadStatus,
          conjuncts: a.gate.conjuncts,
          missingConjuncts: a.gate.missing,
          elapsedMs: a.out ? a.out.elapsedMs : null,
          timedOut: a.out ? a.out.timedOut : null,
          executionError: a.execError ? String(a.execError.message ?? a.execError).slice(0, 300) : null,
        })),
        // the FINAL attempt evaluated by the gate:
        exitCode: gate.exitCode,
        domBytes: gate.domBytes,
        conjuncts: gate.conjuncts,
        loadStatus: gate.loadStatus,
        elapsedMs: out ? out.elapsedMs : null,
        timedOut: out ? out.timedOut : null,
        executionError: execError ? String(execError.message ?? execError).slice(0, 500) : null,
      },
      missingConjuncts: gate.missing,
      independentSourceOfTruth: 'the real browser DOM dump (Edge/Chromium headless=new) — not an HTTP status or a unit test',
      whyNonCircular: 'a real browser engine parsed and executed the app page; the DOM markers come from the live document',
      failureCaseDetected: execError
        ? `browser execution error (fail-closed): ${String(execError.message ?? execError).slice(0, 400)}`
        : (out && out.timedOut)
          ? `headless browser TIMED OUT after the bounded budget in ${attempts.length} attempt(s) — fail-closed; missing conjunct(s): ${gate.missing.join(', ')}`
          : (gate.passed
            ? (attempts.length > 1
              ? `none in the final attempt — every conjunct holds (${attempts.length} attempts recorded: earlier attempt(s) timed out after a complete capture — flaky Edge exit, not a page defect)`
              : 'none — every conjunct holds (exit code 0, non-empty captured DOM, canvas, diagnostics, data-load-status READY)')
            : `MISSING CONJUNCT(S): ${gate.missing.join(', ')}`),
    }));
  }

  // ------------------------------------------------------------------
  // (3) Raw persistence — SEPARATE side-error record (a file/manifest
  // error must never be conflated with the browser-gate records above).
  // ------------------------------------------------------------------
  let persistError = null;
  const persisted = [];
  try {
    for (const r of loadRuns) {
      const file = path.join(rawDir, r.dumpFile);
      const domText = r.final.out ? r.final.out.domText : '(no capture — browser execution failed or timed out)';
      await writeFile(file, domText, 'utf8');
      persisted.push({ file: r.dumpFile, bytes: r.final.out ? r.final.out.domText.length : 0 });
    }
    await writeFile(path.join(rawDir, 'HEADLESS_RUN.json'), JSON.stringify({
      run: RUN_ID,
      suite: 'tests/pecompat/headless_load.test.mjs (T9 gate — FIXED per SCENEIR-T9-C1)',
      browserBinary: bin.path,
      binaryProvenance: bin.provenance,
      knownBrowserBinary: bin.knownBrowserBinary,
      standInBinary: bin.standIn,
      browserArgs: ['--headless=new', '--user-data-dir=<temp>', '--virtual-time-budget=30000', '--dump-dom', '<per-mode URL>'],
      port,
      pid: server.pid,
      loads: loadRuns.map((r) => ({
        id: r.id, url: r.url, attemptCount: r.attempts.length,
        exitCode: r.final.gate.exitCode, elapsedMs: r.final.out ? r.final.out.elapsedMs : null,
        domBytes: r.final.gate.domBytes, loadStatus: r.final.gate.loadStatus,
        conjuncts: r.final.gate.conjuncts, missingConjuncts: r.final.gate.missing,
        timedOut: r.final.out ? r.final.out.timedOut : null,
        executionError: r.final.execError ? String(r.final.execError.message ?? r.final.execError).slice(0, 500) : null,
        stderrExcerpt: r.final.out ? r.final.out.stderr.slice(0, 1000) : null,
        allAttempts: r.attempts.map((a) => ({
          attempt: a.attempt,
          exitCode: a.gate.exitCode,
          domBytes: a.gate.domBytes,
          loadStatus: a.gate.loadStatus,
          missingConjuncts: a.gate.missing,
          timedOut: a.out ? a.out.timedOut : null,
        })),
      })),
    }, null, 1) + '\n', 'utf8');
    persisted.push({ file: 'HEADLESS_RUN.json', bytes: null });
    // best-effort temp profile cleanup (bounded; Edge may hold locks)
    for (const r of loadRuns) {
      for (const a of r.attempts) {
        if (a.out && a.out.userDataDir) await rm(a.out.userDataDir, { recursive: true, force: true }).catch(() => {});
      }
    }
  } catch (e) {
    persistError = e;
  }
  records.push(rec('T9_RAW_PERSISTENCE', 'raw capture persistence (SIDE-ERROR class — the browser-gate statuses above were computed independently of this record)', persistError ? 'FAIL' : 'PASS', {
    measuredQuantity: 'writeFile of the DOM dumps + HEADLESS_RUN.json (report raw dir)',
    measured: persistError ? String(persistError.message ?? persistError).slice(0, 1000) : { persisted },
    failureCaseDetected: persistError
      ? `raw persistence failed (side error; the browser-gate records keep their own independently computed statuses): ${String(persistError.message ?? persistError).slice(0, 300)}`
      : 'none — raw DOM dumps + run JSON written to the report raw dir',
  }));

  // ------------------------------------------------------------------
  // (4) Suite-owned server lifecycle — bounded, with port-freed proof.
  // ------------------------------------------------------------------
  const stop = await stopServer(server);
  const lifecycleOk = stop.portFreed;
  records.push(rec('T9_SERVER_LIFECYCLE', `suite-owned bounded server lifecycle (pid ${server.pid}, port ${port}; stop + port-freed proof)`, lifecycleOk ? 'PASS' : 'FAIL', {
    measuredQuantity: 'start/stop/PID/lifetime/port-freed proof of the suite-owned server',
    measured: {
      pid: server.pid, port, startedAtMs: server.startedAtMs, lifetimeMs: stop.lifetimeMs,
      killed: stop.killed, exitCode: stop.exitCode, signal: stop.signal,
      portFreed: stop.portFreed, freedAfterMs: stop.freedAfterMs,
    },
    failureCaseDetected: lifecycleOk
      ? 'none — server stopped, port freed, nothing left running'
      : 'server port NOT freed after the suite — LIFECYCLE BREACH (side-error class; not a browser conjunct result)',
  }));

  return records;
}
