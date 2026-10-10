// world_headless_load.test.mjs — PE_WORLD_LAUNCHER_R1_20261010, ETAP C
// T9-STYLE REAL-BROWSER LOAD of /launcher and /world through the FIXED
// 5-conjunct gate (evaluateLoadGate imported from tests/pecompat/
// headless_load.test.mjs — the SAME production predicate, NOT reimplemented).
// REUSE LABEL: the suite shape follows tests/pecompat/catalog_headless_load.
// test.mjs (phase 4) — separate suite-owned server, DEDICATED temp Edge
// profile, bounded timeout, leftover-Edge cleanup by exact profile-mark
// match, per-conjunct records + page content markers.
//
// SEPARATION (contract §0): LOAD (this suite) vs PIXEL_RENDER
// (tools/pecompat/world_pixel_render.mjs — real rendered pixel image, private
// output only) vs INTERACTION (automation-driven user input — honest
// NOT_PERFORMED while the automation daemon is down; never PASS-by-default).
//
// PREREGISTERED EXPECTATIONS:
//   - both pages PASS all five conjuncts (exit 0, non-empty DOM, the
//     view-canvas marker, the diagnostics marker, data-load-status READY);
//   - /launcher dump contains: era PCG_9_3_5 markers, the entry button
//     label EXACTLY „Uruchom podgląd świata”, the coverage denominator
//     '51 920', and the honest era/label texts;
//   - /world dump contains: the 64-tile active-window census line
//     ('kafle aktywne (okno 8×8): 64 / limit 64'), the adapter-units position
//     line prefix, and NO position readout CLAIMING 'oryginalne XYZ' (the
//     honest negation labels are REQUIRED by the contract and are not
//     readout claims — marker refined after the first run measured the
//     negation label tripping a substring check);
//   - the gate negatives (STATUS_ERROR / NO_CANVAS) FAIL the same gate
//     (imported production predicate already proven by the 6-negative suite
//     in the app battery; two spot negatives re-prove the predicate here).
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { evaluateLoadGate } from './headless_load.test.mjs';
import {
  startWorldServer, stopWorldServer, findFreePort, rawRequestFull, parseJsonOrNone,
} from './_world_server_helpers.mjs';

const PROFILE_MARK = 'pec-world-launcher-headless';
const BROWSER_CANDIDATES = [
  'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe',
  'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
];

function rec(id, name, status, extra = {}) {
  return { id, name, status, ...extra };
}

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

  // ---- gate predicate spot-negatives (imported production gate) ----
  const GOOD = { exitCode: 0, domText: '<canvas id="view-canvas"></canvas><div id="diagnostics"></div><div data-load-status="READY"></div>' };
  const NEG = [
    ['WORLD_T9_GATE_NEG_STATUS_ERROR', { exitCode: 0, domText: GOOD.domText.replace('data-load-status="READY"', 'data-load-status="ERROR"') }, ['STATUS_READY']],
    ['WORLD_T9_GATE_NEG_NO_CANVAS', { exitCode: 0, domText: GOOD.domText.replace('<canvas id="view-canvas"></canvas>', '') }, ['CANVAS_PRESENT']],
  ];
  let negOk = true;
  const negMeasured = [];
  for (const [id, input, expected] of NEG) {
    const gate = evaluateLoadGate(input);
    const ok = gate.passed === false && expected.every((m) => gate.missing.includes(m));
    if (!ok) negOk = false;
    negMeasured.push({ id, gateResult: gate.passed, missing: gate.missing, expected, ok });
  }
  records.push(rec('WORLD_T9_GATE_PREDICATIVE_NEGATIVES',
    'the imported FIXED gate rejects defective captures (spot negatives through the same production evaluateLoadGate)',
    negOk ? 'PASS' : 'FAIL', {
      resultClass: 'SYNTHETIC_GATE_NEGATIVE_CONTROL (defective input through the imported production gate)',
      measuredQuantity: 'evaluateLoadGate verdicts',
      measured: negMeasured,
    }));

  // ---- browser availability ----
  const browserPath = BROWSER_CANDIDATES.find((p) => existsSync(p)) ?? null;
  const port = ctx.worldPort ?? (await findFreePort(8162));
  const serverRec = await startWorldServer({ port });

  try {
    if (!browserPath) {
      for (const id of ['WORLD_T9_LOAD_LAUNCHER', 'WORLD_T9_LOAD_WORLD']) {
        records.push(rec(id, 'real headless-browser load', 'NOT_PERFORMED', {
          resultClass: 'REAL_BROWSER_HEADLESS_DOM (not executed)',
          measuredQuantity: 'browser binary availability',
          measured: { candidatesChecked: BROWSER_CANDIDATES },
          failureCaseDetected: 'NO browser binary available headless on this host — honest NOT_PERFORMED; BROWSER_VERIFICATION stays NOT_PERFORMED for the load gates',
        }));
      }
      return records;
    }

    const loads = [
      ['WORLD_T9_LOAD_LAUNCHER', 'launcher page (5 panels, overview from the real index, entry button)', `http://127.0.0.1:${port}/launcher`, 'WORLD_DOM_DUMP_LAUNCHER.html', 'launcher'],
      ['WORLD_T9_LOAD_WORLD', 'world view (terrain from original u16 samples, 64-tile window, vegetation ON)', `http://127.0.0.1:${port}/world#tile=53,114&profile=0&seed=0&density=50&veg=1`, 'WORLD_DOM_DUMP_WORLD.html', 'world'],
    ];
    for (const [id, modeName, url, dumpName, kind] of loads) {
      const out = await headlessDumpDom(browserPath, url);
      const gate = evaluateLoadGate({ exitCode: out.exitCode, domText: out.domText });
      // page content markers (beyond the 5 conjuncts — honest extras)
      let extra = {};
      let extraOk = false;
      if (kind === 'launcher') {
        const hasEntry = out.domText.includes('Uruchom podgląd świata');
        const hasEra = out.domText.includes('PCG_9_3_5');
        const hasDenominator = out.domText.includes('51 920') || out.domText.includes('51920');
        const hasReady = gate.conjuncts.STATUS_READY;
        const hasCoverage = out.domText.includes('pokrycie:');
        extra = { entryButtonLabelExact: hasEntry, eraLabel: hasEra, denominator: hasDenominator, coverageLine: hasCoverage };
        extraOk = hasEntry && hasEra && hasDenominator && hasReady && hasCoverage;
      } else {
        const hasCensus = out.domText.includes('kafle aktywne (okno 8×8): 64 / limit 64');
        const hasPos = out.domText.includes('pozycja (jednostki adaptera');
        // contract §7: the POSITION READOUT must not be labeled "oryginalne
        // XYZ" — the honest NEGATION labels ("NIE „oryginalne XYZ”") are
        // required and stay; the marker targets the readout claim only.
        const noOriginalXyzPositionClaim = !/pozycja \(oryginalne/i.test(out.domText)
          && !/pozycja: oryginalne/i.test(out.domText);
        const hasRawU16 = out.domText.includes('surowe u16=');
        // ETAP E vegetation markers (contract §6.7/§8): the DOM census carries
        // the R2 status-vocabulary counts (requested/selected/placed/limited —
        // the fair-cap census) + the VEGETATION_MODE label + the profile-mode/
        // seed labels + the p3-shown-separately line.
        const vegCensus = /ro\u015blinno\u015b\u0107: \u017c\u0105dane \d+ \/ wybrane \d+ \/ umieszczone \d+ \/ ograniczone \d+/.test(out.domText);
        const vegMode = out.domText.includes('VEGETATION_MODE = RECONSTRUCTION_PREVIEW');
        const vegProfileSeed = out.domText.includes('Tryb profilu:') && out.domText.includes('LAB_SEED');
        const vegP3Separate = /p3 = 0/.test(out.domText);
        const vegThreeWay = out.domText.includes('ORIGINAL_CLIMATE_RECORDS') && out.domText.includes('RECOVERED_RNG_ARITHMETIC') && out.domText.includes('INSTANCE_DISTRIBUTION');
        extra = { activeWindow64: hasCensus, adapterUnitsPosition: hasPos, noOriginalXyzPositionClaim, rawU16Readout: hasRawU16, vegetationCensus: vegCensus, vegetationMode: vegMode, vegetationProfileSeed: vegProfileSeed, vegetationP3Separate: vegP3Separate, vegetationThreeWaySeparation: vegThreeWay };
        extraOk = hasCensus && hasPos && noOriginalXyzPositionClaim && hasRawU16 && vegCensus && vegMode && vegProfileSeed && vegP3Separate && vegThreeWay;
      }
      await writeFile(path.join(rawDir, dumpName), out.domText, 'utf8');
      records.push(rec(id, `real headless-browser load — ${modeName} — 5-conjunct gate (per-conjunct records) + page content markers`,
        (gate.passed && extraOk) ? 'PASS' : 'FAIL', {
          resultClass: 'REAL_BROWSER_HEADLESS_DOM (Edge headless=new, dedicated temp profile)',
          measuredQuantity: 'captured DOM markers + browser exit code through the production evaluateLoadGate + page content markers',
          measured: {
            url, exitCode: out.exitCode, elapsedMs: out.elapsedMs, domBytes: out.domText.length,
            gate: { passed: gate.passed, missing: gate.missing, conjuncts: gate.conjuncts, loadStatus: gate.loadStatus },
            pageContentMarkers: extra,
            stderrExcerpt: out.stderr.slice(0, 400),
          },
          independentSourceOfTruth: 'the real browser DOM dump (Edge headless=new) — not an HTTP status or a unit test',
          whyNonCircular: 'the dump is what the browser actually rendered/executed at capture time; markers are page-behavior facts (census line, adapter-units labels), not static HTML echoes',
          failureCaseDetected: gate.passed && extraOk ? 'none — all five conjuncts hold and the page content markers are present'
            : (gate.passed ? 'gate conjuncts hold but page content markers missing (page defect or premature capture)' : `gate missing: ${gate.missing.join('+')}`),
          rawDump: dumpName,
        }));
    }
  } finally {
    const stop = await stopWorldServer(serverRec);
    records.push(rec('WORLD_T9_SERVER_LIFECYCLE',
      `suite-owned world server lifecycle (pid ${serverRec.pid}, port ${port}; stop + port-freed proof)`,
      stop.portFreed ? 'PASS' : 'FAIL', {
        measuredQuantity: 'startup line + stop result + port-freed proof',
        measured: { startupLine: serverRec.startupLine, pid: serverRec.pid, port, stop },
        failureCaseDetected: stop.portFreed ? 'none — the suite cleaned up its OWN process only' : 'PORT NOT FREED after stop',
      }));
  }
  return records;
}
