// t9_pixel_render.mjs — PIXEL_RENDER gate of the T9 fix validation — PE_CITY_ASSET_MAP_R1_20261010.
//
// SEPARATION (contract §0): LOAD (real-browser DOM capture) is
// tests/pecompat/headless_load.test.mjs; INTERACTIVE (automation-driven user
// input) is a SEPARATE gate recorded NOT_PERFORMED when no automation tool is
// available. THIS tool captures a REAL RENDERED PIXEL IMAGE of the app's
// asset mode (model 218757) via headless Edge --screenshot and verifies the
// PNG is non-trivial with an OWN bounded PNG check (tools/pecompat/
// png_nontrivial.mjs — node:zlib only, no new dependency): signature+IHDR+
// IDAT inflate+scanline unfilter+per-region unique-color census+luminance
// statistics. HONEST LABEL: a pixel-content heuristic (not a semantic render
// check); a DOM-READY page with a FAILED WebGL context would still produce a
// solid-color canvas region, which the canvas-region thresholds below catch.
//
// The PNG is written to PRIVATE OUTPUT ONLY (never the report package/repo —
// no proprietary rendered payloads in Git, also not base64/JSON-encoded). The
// record written to --raw-out contains METADATA ONLY (path, size, SHA256,
// pixel statistics, PIDs/ports/lifetimes).
//
// Known host quirk (measured in the phase probe): headless Edge --screenshot
// WRITES the file but the process may not exit on its own; this tool polls
// for the file, waits for size stability, then kills the child and ONLY
// those Edge processes whose command line carries OUR profile mark (never
// foreign/user browsers).
//
// Usage:
//   node tools/pecompat/t9_pixel_render.mjs --out <PRIVATE png path>
//        [--raw-out <report raw json>] [--models <Models.bnt>]
//        [--three-root <three pkg dir>] [--port <preferred port>]
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir, rm } from 'node:fs/promises';
import { existsSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { startServer, stopServer, findFreePort } from '../../tests/pecompat/_app_server_helpers.mjs';
import { analyzePng } from './png_nontrivial.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';
const PROFILE_MARK = 'pec-city-asset-map-pixel';
const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

// Canvas viewport region in the 1280x800 capture (below the header, left of
// the side panel) — where the WebGL canvas actually renders.
const CANVAS_REGION = [10, 80, 900, 790];

// Frozen non-triviality thresholds (calibrated on the phase probe capture:
// full: 805 unique colors / 0.468 most-common / lumaStdDev 44.5;
// canvasRegion: 671 / 0.735 / 33.2; a blank single-color page scores 1-3
// unique colors, most-common 1.0, lumaStdDev 0).
const THRESHOLDS = Object.freeze({
  minBytes: 10000,
  fullUniqueColorsMin: 50,
  fullMostCommonFractionMax: 0.995,
  fullLumaStdDevMin: 1.0,
  canvasUniqueColorsMin: 20,
  canvasMostCommonFractionMax: 0.99,
});

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }

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

  // poll for the file + size stability (Edge writes it but may hang after)
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
  const pngPath = opt('--out');
  const rawOut = opt('--raw-out');
  const modelsPath = opt('--models') ?? 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt';
  const threeRoot = opt('--three-root') ?? 'D:\\Eudoria_Reconstruction\\12_WebGame\\eudoria-clean\\node_modules\\three';
  const preferredPort = Number(opt('--port') ?? 8160);

  if (!pngPath) { console.error('missing --out <png path>'); process.exit(2); }
  await mkdir(path.dirname(pngPath), { recursive: true });
  if (rawOut) await mkdir(path.dirname(rawOut), { recursive: true });

  const port = await findFreePort(preferredPort); // bind/close probe; NEVER 8140 (foreign reference)
  const record = {
    run: RUN_ID,
    gate: 'PIXEL_RENDER (T9 separation: LOAD is headless_load.test.mjs; INTERACTIVE is a separate gate)',
    browserBinary: EDGE,
    url: `http://127.0.0.1:${port}/`,
    canvasRegion: CANVAS_REGION,
    thresholds: THRESHOLDS,
    pngPath, // PRIVATE OUTPUT ONLY — never committed
  };

  let server;
  try {
    server = await startServer({ port, modelsBntPath: modelsPath, threeRoot, timeoutMs: 180000 });
  } catch (e) {
    record.status = 'FAIL';
    record.error = `server startup failed: ${String(e?.message ?? e).slice(0, 800)}`;
    if (rawOut) await writeFile(rawOut, JSON.stringify(record, null, 1) + '\n', 'utf8');
    console.log(JSON.stringify(record, null, 1));
    process.exit(1);
  }
  record.server = { pid: server.pid, port, startedAtMs: server.startedAtMs };

  const shot = await runEdgeScreenshot(record.url, pngPath);
  record.browserRun = {
    processExitedOnItsOwn: shot.processExitedOnItsOwn,
    exitInfo: shot.exitInfo,
    killedByTool: shot.killedByTool,
    leftoverEdgePidsKilled: shot.leftoverEdgePidsKilled,
    fileSeenMs: shot.fileSeenMs,
    totalMs: shot.totalMs,
    stderrExcerpt: shot.stderrExcerpt,
    note: 'host quirk (measured): headless Edge --screenshot writes the file then may not exit; the tool waits for size stability and kills the child + ONLY profile-mark-matching Edge leftovers',
  };

  // non-triviality check (own bounded PNG analysis)
  const checks = [];
  let decode;
  if (shot.finalSize > 0) {
    const buf = (await import('node:fs')).readFileSync(pngPath);
    decode = analyzePng(buf, { regions: { canvasRegion: CANVAS_REGION } });
    record.png = {
      bytes: buf.length,
      sha256: createHash('sha256').update(buf).digest('hex'),
      dimensions: decode.dimensions,
      colorType: decode.colorType,
      decodeOk: decode.decodeOk,
      decodeError: decode.error ?? null,
      stats: decode.stats,
    };
    checks.push(['png_file_min_bytes', buf.length >= THRESHOLDS.minBytes, `${buf.length} >= ${THRESHOLDS.minBytes}`]);
    checks.push(['png_decode_ok', decode.decodeOk === true, String(decode.decodeOk)]);
    if (decode.decodeOk) {
      const full = decode.stats.full;
      const canvas = decode.stats.canvasRegion;
      checks.push(['full_unique_colors', full.uniqueColors >= THRESHOLDS.fullUniqueColorsMin, `${full.uniqueColors} >= ${THRESHOLDS.fullUniqueColorsMin}`]);
      checks.push(['full_most_common_fraction', full.mostCommonColorFraction < THRESHOLDS.fullMostCommonFractionMax, `${full.mostCommonColorFraction} < ${THRESHOLDS.fullMostCommonFractionMax}`]);
      checks.push(['full_luma_stddev', full.lumaStdDev >= THRESHOLDS.fullLumaStdDevMin, `${full.lumaStdDev} >= ${THRESHOLDS.fullLumaStdDevMin}`]);
      checks.push(['canvas_region_unique_colors', canvas.uniqueColors >= THRESHOLDS.canvasUniqueColorsMin, `${canvas.uniqueColors} >= ${THRESHOLDS.canvasUniqueColorsMin}`]);
      checks.push(['canvas_region_most_common_fraction', canvas.mostCommonColorFraction < THRESHOLDS.canvasMostCommonFractionMax, `${canvas.mostCommonColorFraction} < ${THRESHOLDS.canvasMostCommonFractionMax}`]);
    }
  } else {
    checks.push(['png_file_created', false, 'the screenshot file was NOT created']);
  }
  record.checks = checks.map(([name, ok, detail]) => ({ name, ok, detail }));
  record.gateResult = checks.every(([, ok]) => ok) ? 'PASS' : 'FAIL';

  // stop the suite-owned server (port-freed proof)
  const stop = await stopServer(server);
  record.serverStop = {
    killed: stop.killed, exitCode: stop.exitCode, signal: stop.signal,
    lifetimeMs: stop.lifetimeMs, portFreed: stop.portFreed, freedAfterMs: stop.freedAfterMs,
  };
  record.status = record.gateResult === 'PASS' && stop.portFreed ? 'PASS' : 'FAIL';

  // best-effort temp profile cleanup
  await rm(shot.userDataDir, { recursive: true, force: true }).catch(() => {});

  if (rawOut) await writeFile(rawOut, JSON.stringify(record, null, 1) + '\n', 'utf8');
  console.log(JSON.stringify({
    status: record.status, gateResult: record.gateResult, pngPath, pngBytes: record.png?.bytes,
    server: record.server, serverStop: record.serverStop,
    checks: record.checks, stats: decode?.stats,
  }, null, 1));
  process.exit(record.status === 'PASS' ? 0 : 1);
}

main().catch((e) => { console.error('PIXEL_TOOL_CRASH', e); process.exit(3); });
