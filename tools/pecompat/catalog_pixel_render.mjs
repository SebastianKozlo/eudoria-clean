// catalog_pixel_render.mjs — PIXEL_RENDER gate, PE_CITY_ASSET_MAP_R1_20261010 phase 4 (W6).
//
// SEPARATION (PREREGISTRATION §5): LOAD is tests/pecompat/catalog_headless_load.test.mjs
// (DONE — 33 PASS incl. both /catalog loads); INTERACTIVE is a SEPARATE gate
// (automation attempt recorded honestly); THIS tool captures REAL RENDERED
// PIXEL IMAGES of the /catalog pages via headless Edge --screenshot:
//   1. /catalog                    — the catalog table page (both eras)
//   2. /catalog#model=<id>          — the FOUR primary model previews
//      (the material preview with NiMaterialProperty diffuse colors applied —
//      the evidence layer for the MATERIAL_APPLIED/BROWSER_OBSERVED
//      TEXTURE_LINK_DISPOSITIONS update: ONLY what the real render observed)
// and verifies each PNG is non-trivial with the OWN bounded PNG check
// (tools/pecompat/png_nontrivial.mjs — node:zlib only, no new dependency).
// HONEST LABEL: a pixel-content heuristic (not a semantic render check); a
// DOM-READY page with a FAILED WebGL context would still produce a solid-color
// canvas region, which the canvas-region thresholds catch.
//
// REUSE LABEL: the capture/lifecycle pattern is tools/pecompat/t9_pixel_render.mjs
// (the phase-1 PIXEL tool — headless Edge --screenshot, poll-file+size-stability
// for the measured host quirk (Edge writes the file but may not exit), profile-
// mark-scoped leftover cleanup, suite-owned bounded server) adapted to the
// CATALOG server; the PNG analysis is png_nontrivial.mjs imported UNCHANGED.
//
// CALIBRATION discipline (same as phase 1): run with --calibrate first, read
// the measured statistics, freeze the thresholds BELOW, then run the gate.
//
// Usage:
//   node tools/pecompat/catalog_pixel_render.mjs --out-dir <PRIVATE png dir>
//        [--raw-out <report raw json>] [--port <preferred port>] [--calibrate]
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir, rm } from 'node:fs/promises';
import { existsSync, statSync, readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import { startCatalogServer, stopCatalogServer, findFreePort } from '../../tests/pecompat/_catalog_server_helpers.mjs';
import { analyzePng } from './png_nontrivial.mjs';

const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';
const PROFILE_MARK = 'pec-city-asset-map-catalog-pixel';
const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

// Canvas viewport region in the 1280x800 capture (x0,y0,x1,y1 END coords —
// png_nontrivial regionStats expects end coordinates). The preview canvas
// lives in the right panel of the catalog grid, below the preview head.
const PREVIEW_CANVAS_REGION = [720, 200, 1260, 530];
// The catalog table region (left panel).
const TABLE_REGION = [10, 165, 610, 415];

// Frozen non-triviality thresholds (CALIBRATED on the phase-4 probe captures —
// measured: table full uniq 1096/mc 0.495, table region uniq 552/mc 0.637/lumaStd 34.6;
// previews full uniq 1240-1273/mc ~0.48, preview canvas region uniq 373-403/mc 0.92-0.925/
// lumaStd 10-20; the raw calibration records are in raw/CATALOG/PIXEL_CALIBRATION{,2}.json.
// A blank single-color page scores 1-3 unique colors, most-common ~1.0, lumaStdDev 0 —
// the thresholds catch it, including a DOM-READY page with a dead WebGL canvas.)
const THRESHOLDS = Object.freeze({
  minBytes: 20000,
  full: { uniqueColorsMin: 100, mostCommonFractionMax: 0.9, lumaStdDevMin: 5 },
  previewCanvas: { uniqueColorsMin: 100, mostCommonFractionMax: 0.97 },
  tableRegion: { uniqueColorsMin: 200, mostCommonFractionMax: 0.9 },
});

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

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

async function runEdgeScreenshot(url, pngPath, { waitMs = 75000 } = {}) {
  const userDataDir = path.join(os.tmpdir(), 'opencode', `${PROFILE_MARK}-${Date.now()}`);
  const args = [
    '--headless=new',
    `--user-data-dir=${userDataDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-extensions',
    '--disable-background-networking',
    '--window-size=1280,800',
    '--virtual-time-budget=30000',
    `--screenshot=${pngPath}`,
    url,
  ];
  const t0 = Date.now();
  const child = spawn(EDGE, args, { stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true });
  let stderr = '';
  child.stderr.setEncoding('utf8');
  child.stderr.on('data', (d) => { stderr += d; });

  let stablePolls = 0;
  let lastSize = -1;
  let fileSeenMs = null;
  const deadline = Date.now() + waitMs;
  let exitInfo = null;
  let exited = false;
  child.once('exit', (code, signal) => { exited = true; exitInfo = { code, signal }; });

  while (Date.now() < deadline) {
    await sleep(1500);
    if (existsSync(pngPath)) {
      const size = statSync(pngPath).size;
      if (fileSeenMs === null) fileSeenMs = Date.now() - t0;
      if (size === lastSize && size > 0) stablePolls++;
      else stablePolls = 0;
      lastSize = size;
      if (stablePolls >= 2) break;
    }
    if (exited) break;
  }
  const processKilledByUs = !exited;
  if (!exited) {
    child.kill();
    await sleep(500);
  }
  const leftover = killOwnLeftoverEdge();
  return {
    processExitedOnItsOwn: exited,
    exitInfo,
    killedByTool: processKilledByUs,
    leftoverEdgePidsKilled: leftover,
    fileSeenMs,
    finalSize: existsSync(pngPath) ? statSync(pngPath).size : 0,
    totalMs: Date.now() - t0,
    stderrExcerpt: stderr.slice(0, 1500),
    userDataDir,
  };
}

async function main() {
  const args = process.argv.slice(2);
  const opt = (name) => {
    const i = args.indexOf(name);
    return i >= 0 ? args[i + 1] : undefined;
  };
  const outDir = opt('--out-dir');
  const rawOut = opt('--raw-out');
  const preferredPort = Number(opt('--port') ?? 8161);
  const calibrate = args.includes('--calibrate');
  if (!outDir) { console.error('missing --out-dir <png dir>'); process.exit(2); }
  await mkdir(outDir, { recursive: true });
  if (rawOut) await mkdir(path.dirname(rawOut), { recursive: true });

  const port = await findFreePort(preferredPort); // bind/close probe; NEVER 8140
  const SHOTS = [
    ['CATALOG_TABLE', `http://127.0.0.1:${port}/catalog`, 'CATALOG_PIXEL_TABLE.png', TABLE_REGION, 'tableRegion'],
    ['PREVIEW_193313', `http://127.0.0.1:${port}/catalog#model=193313`, 'CATALOG_PIXEL_PREVIEW_193313.png', PREVIEW_CANVAS_REGION, 'previewCanvas'],
    ['PREVIEW_192374', `http://127.0.0.1:${port}/catalog#model=192374`, 'CATALOG_PIXEL_PREVIEW_192374.png', PREVIEW_CANVAS_REGION, 'previewCanvas'],
    ['PREVIEW_193684', `http://127.0.0.1:${port}/catalog#model=193684`, 'CATALOG_PIXEL_PREVIEW_193684.png', PREVIEW_CANVAS_REGION, 'previewCanvas'],
    ['PREVIEW_193207', `http://127.0.0.1:${port}/catalog#model=193207`, 'CATALOG_PIXEL_PREVIEW_193207.png', PREVIEW_CANVAS_REGION, 'previewCanvas'],
  ];

  const record = {
    run: RUN_ID,
    gate: 'CATALOG PIXEL_RENDER (LOAD gate already executed in catalog_headless_load.test.mjs; INTERACTIVE is a separate gate)',
    browserBinary: EDGE,
    calibrate,
    thresholds: THRESHOLDS,
    outDir, // PRIVATE OUTPUT ONLY — never committed
    shots: [],
  };

  let server;
  try {
    server = await startCatalogServer({ port, timeoutMs: 180000 });
  } catch (e) {
    record.status = 'FAIL';
    record.error = `catalog server startup failed: ${String(e?.message ?? e).slice(0, 800)}`;
    if (rawOut) await writeFile(rawOut, JSON.stringify(record, null, 1) + '\n', 'utf8');
    console.log(JSON.stringify(record, null, 1));
    process.exit(1);
  }
  record.server = { pid: server.pid, port, startedAtMs: server.startedAtMs, startupLine: server.startupLine };

  let allOk = true;
  for (const [label, url, fileName, region, regionKey] of SHOTS) {
    const pngPath = path.join(outDir, fileName);
    const shot = await runEdgeScreenshot(url, pngPath);
    const entry = { label, url, pngPath, browserRun: { ...shot, userDataDir: undefined }, png: null, checks: [] };
    if (shot.finalSize > 0) {
      const buf = readFileSync(pngPath);
      const decode = analyzePng(buf, { regions: { region } });
      entry.png = {
        bytes: buf.length,
        sha256: createHash('sha256').update(buf).digest('hex'),
        dimensions: decode.dimensions,
        decodeOk: decode.decodeOk,
        stats: decode.stats,
      };
      const T = THRESHOLDS;
      const full = decode.stats.full;
      const reg = decode.stats.region;
      if (calibrate) {
        entry.checks = [
          ['calibration_only', true, `full: uniqueColors=${full.uniqueColors} mostCommon=${full.mostCommonColorFraction} lumaStdDev=${full.lumaStdDev}; region(${regionKey}): uniqueColors=${reg.uniqueColors} mostCommon=${reg.mostCommonColorFraction} lumaStdDev=${reg.lumaStdDev}`],
        ];
      } else {
        const checks = [
          ['png_file_min_bytes', buf.length >= T.minBytes, `${buf.length} >= ${T.minBytes}`],
          ['png_decode_ok', decode.decodeOk === true, String(decode.decodeOk)],
          ['full_unique_colors', full.uniqueColors >= T.full.uniqueColorsMin, `${full.uniqueColors} >= ${T.full.uniqueColorsMin}`],
          ['full_most_common_fraction', full.mostCommonColorFraction < T.full.mostCommonFractionMax, `${full.mostCommonColorFraction} < ${T.full.mostCommonFractionMax}`],
          ['full_luma_stddev', full.lumaStdDev >= T.full.lumaStdDevMin, `${full.lumaStdDev} >= ${T.full.lumaStdDevMin}`],
        ];
        const rt = T[regionKey];
        checks.push(['region_unique_colors', reg.uniqueColors >= rt.uniqueColorsMin, `${reg.uniqueColors} >= ${rt.uniqueColorsMin} (${regionKey})`]);
        checks.push(['region_most_common_fraction', reg.mostCommonColorFraction < rt.mostCommonFractionMax, `${reg.mostCommonColorFraction} < ${rt.mostCommonFractionMax} (${regionKey})`]);
        entry.checks = checks.map(([name, okv, detail]) => ({ name, ok: okv, detail }));
        if (!checks.every(([, okv]) => okv)) allOk = false;
      }
    } else {
      entry.checks = [{ name: 'png_file_created', ok: false, detail: 'the screenshot file was NOT created' }];
      allOk = false;
    }
    record.shots.push(entry);
    await rm(shot.userDataDir, { recursive: true, force: true }).catch(() => {});
  }

  const stop = await stopCatalogServer(server);
  record.serverStop = {
    killed: stop.killed, exitCode: stop.exitCode, signal: stop.signal,
    lifetimeMs: stop.lifetimeMs, portFreed: stop.portFreed, freedAfterMs: stop.freedAfterMs,
  };
  record.status = calibrate ? 'CALIBRATION' : (allOk && stop.portFreed ? 'PASS' : 'FAIL');

  if (rawOut) await writeFile(rawOut, JSON.stringify(record, null, 1) + '\n', 'utf8');
  console.log(JSON.stringify({
    status: record.status,
    calibrate,
    server: record.server,
    serverStop: record.serverStop,
    shots: record.shots.map((s) => ({
      label: s.label, url: s.url, pngBytes: s.png?.bytes, pngSha256: s.png?.sha256,
      dimensions: s.png?.dimensions, checks: s.checks,
      stats: { full: s.png?.stats?.full, region: s.png?.stats?.region },
    })),
  }, null, 1));
  process.exit(calibrate ? 0 : (record.status === 'PASS' ? 0 : 1));
}

main().catch((e) => { console.error('CATALOG_PIXEL_TOOL_CRASH', e); process.exit(3); });
