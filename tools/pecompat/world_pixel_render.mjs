#!/usr/bin/env node
// world_pixel_render.mjs — PIXEL_RENDER gate of Etap C + ETAP D TOGGLE GATE +
// ETAP E VEGETATION TOGGLE GATE — PE_WORLD_LAUNCHER_R1_20261010.
//
// SEPARATION (contract §0/§8): LOAD (tests/pecompat/world_headless_load.test.mjs)
// and INTERACTION (automation-driven input — NOT_PERFORMED while the
// automation daemon is down) are SEPARATE gates. THIS tool captures REAL
// RENDERED PIXEL IMAGES of /launcher and /world via headless Edge
// --screenshot and verifies each PNG is non-trivial with the OWN bounded PNG
// check (tools/pecompat/png_nontrivial.mjs — node:zlib only; reused from the
// catalog pixel tool, NOT reimplemented). HONEST LABEL: a pixel-content
// heuristic (not a semantic render check); a DOM-READY page with a FAILED
// WebGL context would still produce a solid-color canvas region, which the
// canvas-region thresholds catch.
//
// ETAP D (contract §8 materials gate): the world is captured TWICE — with
// the terrain-texture toggle ON (#textures=1, the original-texture splat)
// and OFF (#textures=0, the height-palette preview) — and the two canvas
// regions are compared pixel-by-pixel (own bounded decoder, decodePngRaw):
// the toggle must CHANGE PIXELS measurably (differing-pixel fraction and
// mean abs delta over the canvas region), else the REAL-toggle gate FAILS.
//
// ETAP E (contract §8 vegetation gate): the world is captured TWICE more —
// with the vegetation toggle ON (#veg=1, the deterministic RECONSTRUCTION_
// PREVIEW instances from the original models) and OFF (#veg=0) — and the
// SAME comparison runs: the vegetation must CHANGE PIXELS measurably.
// A toggle that changes nothing is a defect — never PASS-by-default.
//
// The PNGs are written to PRIVATE OUTPUT ONLY (never the repo — no
// proprietary rendered payloads in Git, also not base64/JSON-encoded). The
// record written to --raw-out contains METADATA ONLY (path, size, SHA256,
// pixel statistics, PIDs/ports/lifetimes).
//
// CAPTURE METHOD (Etap E correction, measured): the OLD --screenshot +
// --virtual-time-budget capture starves the compositor — with virtual time
// the rAF frames run back-to-back without PRESENTING, so the captured frame
// was stale (measured: the vegetation InstancedMeshes and the splat terrain
// rendered in the live WebGL buffer — proven by an in-page toDataURL probe —
// but the compositor capture showed them absent/near-black; the phase-3/4
// captures carried the same defect for the splat). THE FIX: a CDP
// (Chrome DevTools Protocol) capture — headless Edge with
// --remote-debugging-port on a suite-owned free port, the page polled via
// Runtime.evaluate until the HONEST per-kind readiness marker is present in
// the DOM (the launcher's data-load-status=READY; the world's
// world-veg panel census line — 'instancje okna' after the awaited Etap E
// vegetation build, or the explicit WYŁĄCZONA line for #veg=0), then a real
// settle wait (presented frames at real vsync) and Page.captureScreenshot.
// If the CDP client cannot start (no global WebSocket), the tool falls back
// to the OLD method with a LOUD method label (never a silent downgrade).
//
// Usage:
//   node tools/pecompat/world_pixel_render.mjs --out-dir <PRIVATE png dir>
//        [--raw-out <report raw json>] [--terrain <terrain.bnt>] [--port <preferred>]
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { existsSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  startWorldServer, stopWorldServer, findFreePort,
} from '../../tests/pecompat/_world_server_helpers.mjs';
import { analyzePng, decodePngRaw } from './png_nontrivial.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const RUN_ID = 'PE_WORLD_LAUNCHER_R1_20261010';
const PROFILE_MARK = 'pec-world-launcher-pixel';
const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

// Canvas viewport regions in the 1280x800 capture:
//  - launcher: the map panel canvas (center column of the launcher grid)
//  - world: the WebGL terrain canvas (left of the 480px side panel)
const CANVAS_REGIONS = {
  launcher: [540, 130, 620, 480],
  world: [10, 110, 740, 540],
};
// Frozen non-triviality thresholds (same shape as the catalog pixel tool —
// calibrated on the prior phase captures; a blank single-color page scores
// 1-3 unique colors, most-common 1.0, lumaStdDev 0).
const THRESHOLDS = Object.freeze({
  minBytes: 10000,
  fullUniqueColorsMin: 50,
  fullMostCommonFractionMax: 0.995,
  fullLumaStdDevMin: 1.0,
  canvasUniqueColorsMin: 20,
  canvasMostCommonFractionMax: 0.99,
});
// ETAP D TOGGLE gate thresholds (preregistered BEFORE the captures): the
// terrain-texture toggle must change the canvas region pixels measurably —
// at least 2% of the sampled canvas pixels differing by >= 8 luma units
// (or >= 1 channel unit) with a mean abs channel delta >= 2.0. A
// no-op/deterministic-equal toggle FAILS (never PASS-by-default).
const TOGGLE_THRESHOLDS = Object.freeze({
  minDifferingFraction: 0.02,
  minMeanAbsDeltaOverDiffering: 2.0,
  perPixelDiff: 8, // luma units OR any-channel >= this counts as differing
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

async function runEdgeScreenshot(url, pngPath, { waitMs = 90000, kind = 'world' } = {}) {
  // ---- the CDP capture path (the Etap E correction; see the header) ----
  if (typeof WebSocket === 'function') {
    try {
      const result = await runEdgeScreenshotCdp(url, pngPath, { waitMs, kind });
      if (result) return result;
    } catch (e) {
      console.log(`[world_pixel_render] CDP capture failed (${String(e?.message ?? e)}) — falling back to the legacy --screenshot method (LOUD label)`);
    }
  } else {
    console.log('[world_pixel_render] no global WebSocket client — using the legacy --screenshot method (LOUD label)');
  }
  return runEdgeScreenshotLegacy(url, pngPath, { waitMs });
}

/** The readiness marker per page kind (the HONEST completion signals from
 * the page itself — the same census lines the DOM gates assert). For /world
 * the marker waits for the SETTLED streaming state: the window follow moves
 * the origin exactly once for this fixed anchor (53,114 -> the settled
 * 'origin okna: 53,114'), so requiring it prevents capturing a mid-rebuild
 * frame (measured: a boot-time-only marker caught the second window
 * rebuild's palette/splat swap in flight). The vegetation census line is
 * required in EVERY veg state ('żądane…' on, 'WYŁĄCZONA' off, …). */
function cdpReadinessExpression(kind) {
  if (kind === 'launcher') {
    return `(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY')`;
  }
  return `(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY') && ` +
    `String(document.getElementById('world-census')?.textContent || '').includes('origin okna: 53,114') && ` +
    `String(document.getElementById('world-census')?.textContent || '').includes('ro\u015blinno\u015b\u0107:')`;
}

async function runEdgeScreenshotCdp(url, pngPath, { waitMs = 90000, kind = 'world' } = {}) {
  const dbgPort = await findFreePort(9223);
  if (dbgPort === 9222) throw new Error('the automation-daemon port 9222 is NEVER used by this tool');
  const userDataDir = path.join(os.tmpdir(), 'opencode', `${PROFILE_MARK}-cdp-${Date.now()}`);
  const args = [
    '--headless=new',
    `--remote-debugging-port=${dbgPort}`,
    `--user-data-dir=${userDataDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-extensions',
    '--disable-background-networking',
    '--window-size=1280,800',
    url,
  ];
  const t0 = Date.now();
  const child = spawn(EDGE, args, { stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true });
  let stderr = '';
  child.stderr.setEncoding('utf8');
  child.stderr.on('data', (d) => { stderr += d; });
  let exited = null;
  child.once('exit', (code, signal) => { exited = { code, signal }; });

  const cleanup = () => {
    try { child.kill(); } catch { /* already gone */ }
    killOwnLeftoverEdge();
  };

  try {
    // find the page target over the DevTools HTTP endpoints
    const deadline = Date.now() + waitMs;
    let pageWsUrl = null;
    while (Date.now() < deadline && !pageWsUrl) {
      if (exited) throw new Error(`Edge exited early (code ${exited.code}) — stderr: ${stderr.slice(0, 400)}`);
      try {
        const r = await fetch(`http://127.0.0.1:${dbgPort}/json/list`);
        const targets = await r.json();
        const page = targets.find((t) => t.type === 'page' && (t.url.includes('/world') || t.url.includes('/launcher')));
        if (page) pageWsUrl = page.webSocketDebuggerUrl;
      } catch { /* endpoint not up yet */ }
      await sleep(300);
    }
    if (!pageWsUrl) throw new Error('the DevTools /json/list page target never appeared');

    // a minimal CDP client over the global WebSocket
    const ws = new WebSocket(pageWsUrl);
    await new Promise((resolve, reject) => {
      ws.addEventListener('open', resolve, { once: true });
      ws.addEventListener('error', (ev) => reject(new Error('CDP websocket error')), { once: true });
    });
    let msgId = 0;
    const pending = new Map();
    ws.addEventListener('message', (ev) => {
      let m = null;
      try { m = JSON.parse(ev.data); } catch { return; }
      if (m.id && pending.has(m.id)) {
        const { resolve, reject } = pending.get(m.id);
        pending.delete(m.id);
        if (m.error) reject(new Error(m.error.message));
        else resolve(m.result);
      }
    });
    const send = (method, params = {}) => new Promise((resolve, reject) => {
      const id = ++msgId;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
      setTimeout(() => {
        if (pending.has(id)) { pending.delete(id); reject(new Error(`CDP ${method} timeout`)); }
      }, 30000).unref?.();
    });
    await send('Page.enable');
    await send('Runtime.enable');

    // poll the HONEST readiness marker (the page's own census lines)
    const expr = cdpReadinessExpression(kind);
    let ready = false;
    let lastEval = null;
    while (Date.now() < deadline) {
      if (exited) throw new Error(`Edge exited during readiness polling (code ${exited.code}) — stderr: ${stderr.slice(0, 400)}`);
      try {
        const r = await send('Runtime.evaluate', { expression: expr, returnByValue: true });
        lastEval = r?.result?.value ?? null;
        if (lastEval === true) { ready = true; break; }
      } catch (e) { lastEval = String(e?.message ?? e); }
      await sleep(400);
    }
    if (!ready) throw new Error(`the page readiness marker never became true (last=${JSON.stringify(lastEval)})`);

    // the real-time settle: a few dozen PRESENTED frames at real vsync
    await sleep(3000);
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    await writeFile(pngPath, Buffer.from(shot.data, 'base64'));
    try { ws.close(); } catch { /* best effort */ }
    return {
      method: 'CDP (remote-debugging + Runtime.evaluate readiness poll + Page.captureScreenshot)',
      readinessExpression: expr,
      processExitedOnItsOwn: exited !== null,
      exitInfo: exited,
      killedByTool: exited === null,
      leftoverEdgePidsKilled: [],
      fileSeenMs: null,
      finalSize: statSync(pngPath).size,
      totalMs: Date.now() - t0,
      stderrExcerpt: stderr.slice(0, 600),
      userDataDir, dbgPort,
    };
  } finally {
    cleanup();
  }
}

async function runEdgeScreenshotLegacy(url, pngPath, { waitMs = 75000 } = {}) {
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
    method: 'LEGACY --screenshot + --virtual-time-budget=30000 (compositor capture — KNOWN to starve late-boot WebGL frames; see the header)',
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
  const preferredPort = Number(opt('--port') ?? 8162);
  if (!outDir) { console.error('[world_pixel_render] --out-dir (PRIVATE output root) is required'); process.exit(2); }
  await mkdir(outDir, { recursive: true });
  if (rawOut) await mkdir(path.dirname(rawOut), { recursive: true });

  if (!existsSync(EDGE)) {
    const result = {
      run: RUN_ID, gate: 'PIXEL_RENDER', ok: false, status: 'NOT_PERFORMED',
      reason: `Edge binary not found at ${EDGE} — honest NOT_PERFORMED (no browser, no fake capture)`,
      shots: [],
    };
    if (rawOut) await writeFile(rawOut, JSON.stringify(result, null, 1) + '\n', 'utf8');
    console.log(result.reason);
    process.exit(0);
  }

  const port = await findFreePort(preferredPort);
  const serverRec = await startWorldServer({ port });
  const shots = [];
  let allOk = true;
  try {
    const targets = [
      ['launcher', `http://127.0.0.1:${port}/launcher`],
      ['world-on', `http://127.0.0.1:${port}/world#tile=53,114&profile=0&seed=0&density=50&textures=1`],
      ['world-off', `http://127.0.0.1:${port}/world#tile=53,114&profile=0&seed=0&density=50&textures=0`],
      ['world-veg-on', `http://127.0.0.1:${port}/world#tile=53,114&profile=0&seed=0&density=50&textures=1&veg=1`],
      ['world-veg-off', `http://127.0.0.1:${port}/world#tile=53,114&profile=0&seed=0&density=50&textures=1&veg=0`],
    ];
    const pngByKind = {};
    for (const [kind, url] of targets) {
      const pngPath = path.join(outDir, `pixel_${kind}.png`);
      pngByKind[kind] = pngPath;
      const edge = await runEdgeScreenshot(url, pngPath, { kind });
      const { readFile } = await import('node:fs/promises');
      let stats = null, buf = null, sha = null;
      if (edge.finalSize > 0) {
        buf = await readFile(pngPath);
        sha = createHash('sha256').update(buf).digest('hex');
        stats = await analyzePng(buf, { regions: { canvasRegion: kind === 'launcher' ? CANVAS_REGIONS.launcher : CANVAS_REGIONS.world } });
      }
      const region = kind === 'launcher' ? CANVAS_REGIONS.launcher : CANVAS_REGIONS.world;
      const fullStats = stats?.stats?.full ?? null;
      const canvasStats = stats?.stats?.canvasRegion ?? null;
      const checks = {
        bytes: (edge.finalSize ?? 0) >= THRESHOLDS.minBytes,
        decodeOk: stats?.decodeOk === true,
        fullUniqueColors: (fullStats?.uniqueColors ?? 0) >= THRESHOLDS.fullUniqueColorsMin,
        fullMostCommon: (fullStats?.mostCommonColorFraction ?? 1) <= THRESHOLDS.fullMostCommonFractionMax,
        fullLumaStdDev: (fullStats?.lumaStdDev ?? 0) >= THRESHOLDS.fullLumaStdDevMin,
        canvasUniqueColors: (canvasStats?.uniqueColors ?? 0) >= THRESHOLDS.canvasUniqueColorsMin,
        canvasMostCommon: (canvasStats?.mostCommonColorFraction ?? 1) <= THRESHOLDS.canvasMostCommonFractionMax,
      };
      const ok = Object.values(checks).every(Boolean);
      if (!ok) allOk = false;
      shots.push({
        kind, url, pngPath, bytes: edge.finalSize, sha256: sha,
        captureMethod: edge.method ?? 'LEGACY (unlabeled)',
        pngStats: { full: fullStats, canvasRegion: canvasStats, dimensions: stats?.dimensions, decodeOk: stats?.decodeOk },
        canvasRegion: region, checks, ok,
        edge: { method: edge.method ?? 'LEGACY (unlabeled)', processExitedOnItsOwn: edge.processExitedOnItsOwn, exitInfo: edge.exitInfo, killedByTool: edge.killedByTool, leftoverEdgePidsKilled: edge.leftoverEdgePidsKilled, fileSeenMs: edge.fileSeenMs, totalMs: edge.totalMs, stderrExcerpt: edge.stderrExcerpt },
        thresholds: THRESHOLDS,
      });
      console.log(`[world_pixel_render] ${kind}: ${ok ? 'NON_TRIVIAL PASS' : 'FAIL'} — ${edge.finalSize} B, full uniqueColors ${fullStats?.uniqueColors}, canvas uniqueColors ${canvasStats?.uniqueColors} [${edge.method ?? 'LEGACY'}]`);
    }

    // ---- the toggle pixel-comparison (shared by the ETAP D and ETAP E gates) ----
    const { readFile: rf } = await import('node:fs/promises');
    const compareToggle = async (gateId, onKind, offKind, note) => {
      try {
        const onBuf = await rf(pngByKind[onKind]);
        const offBuf = await rf(pngByKind[offKind]);
        const dOn = decodePngRaw(onBuf);
        const dOff = decodePngRaw(offBuf);
        if (!(dOn.decodeOk && dOff.decodeOk && dOn.width === dOff.width && dOn.height === dOff.height && dOn.channels === dOff.channels)) {
          return { gate: gateId, status: 'FAIL', error: `decode on=${dOn.error ?? 'ok'} off=${dOff.error ?? 'ok'} (dims ${dOn.width}x${dOn.height}c${dOn.channels} vs ${dOff.width}x${dOff.height}c${dOff.channels})` };
        }
        const [x0, y0, x1, y1] = CANVAS_REGIONS.world;
        let samples = 0, differing = 0, sumAbs = 0, sumLumaOn = 0, sumLumaOff = 0;
        const step = Math.max(1, Math.floor(Math.sqrt(((x1 - x0) * (y1 - y0)) / 100000)));
        for (let y = y0; y < y1; y += step) {
          for (let x = x0; x < x1; x += step) {
            const i = (y * dOn.width + x) * dOn.channels;
            let diff = false, absSum = 0;
            for (let c = 0; c < 3; c++) {
              const d = Math.abs(dOn.img[i + c] - dOff.img[i + c]);
              absSum += d;
              if (d >= 1) diff = true;
            }
            const lumaOn = 0.2126 * dOn.img[i] + 0.7152 * dOn.img[i + 1] + 0.0722 * dOn.img[i + 2];
            const lumaOff = 0.2126 * dOff.img[i] + 0.7152 * dOff.img[i + 1] + 0.0722 * dOff.img[i + 2];
            if (Math.abs(lumaOn - lumaOff) >= TOGGLE_THRESHOLDS.perPixelDiff || absSum >= TOGGLE_THRESHOLDS.perPixelDiff) diff = true;
            samples++;
            if (diff) { differing++; sumAbs += absSum / 3; }
            sumLumaOn += lumaOn; sumLumaOff += lumaOff;
          }
        }
        const differingFraction = samples ? differing / samples : 0;
        const meanAbsDeltaOverDiffering = differing ? sumAbs / differing : 0;
        const meanLumaDelta = samples ? Math.abs(sumLumaOn - sumLumaOff) / samples : 0;
        const ok = differingFraction >= TOGGLE_THRESHOLDS.minDifferingFraction
          && meanAbsDeltaOverDiffering >= TOGGLE_THRESHOLDS.minMeanAbsDeltaOverDiffering;
        return {
          gate: gateId, status: ok ? 'PASS' : 'FAIL',
          region: CANVAS_REGIONS.world, samples, step,
          differingPixels: differing, differingFraction: Math.round(differingFraction * 10000) / 10000,
          meanAbsChannelDeltaOverDiffering: Math.round(meanAbsDeltaOverDiffering * 100) / 100,
          meanLumaDelta: Math.round(meanLumaDelta * 100) / 100,
          thresholds: TOGGLE_THRESHOLDS, note,
        };
      } catch (e) {
        return { gate: gateId, status: 'FAIL', error: String(e?.message ?? e) };
      }
    };

    // ETAP D: the terrain-texture toggle must CHANGE PIXELS
    const texGate = await compareToggle('ETAP_D_TEXTURE_TOGGLE_CHANGES_PIXELS', 'world-on', 'world-off',
      'the REAL terrain-texture toggle proof: #textures=1 (original-texture splat) vs #textures=0 (height-palette preview) — the canvas pixels must differ measurably; a no-op toggle FAILS');
    if (texGate.status !== 'PASS') allOk = false;
    console.log(`[world_pixel_render] ${texGate.gate}: ${texGate.status} — differing ${texGate.differingPixels ?? 'n/a'}/${texGate.samples ?? 'n/a'} (${((texGate.differingFraction ?? 0) * 100).toFixed(2)}%), meanAbsΔ ${(texGate.meanAbsChannelDeltaOverDiffering ?? 0).toFixed(2)}`);
    shots.push(texGate);

    // ETAP E: the vegetation toggle must CHANGE PIXELS (the reconstruction-
    // preview instances + the ORIGINAL models render on the terrain)
    const vegGate = await compareToggle('ETAP_E_VEGETATION_TOGGLE_CHANGES_PIXELS', 'world-veg-on', 'world-veg-off',
      'the REAL vegetation toggle proof: #veg=1 (deterministic RECONSTRUCTION_PREVIEW instances — original same-era models through the qualified importer, LAB_SEED-keyed distribution) vs #veg=0 — the canvas pixels must differ measurably; a no-op toggle FAILS');
    if (vegGate.status !== 'PASS') allOk = false;
    console.log(`[world_pixel_render] ${vegGate.gate}: ${vegGate.status} — differing ${vegGate.differingPixels ?? 'n/a'}/${vegGate.samples ?? 'n/a'} (${((vegGate.differingFraction ?? 0) * 100).toFixed(2)}%), meanAbsΔ ${(vegGate.meanAbsChannelDeltaOverDiffering ?? 0).toFixed(2)}`);
    shots.push(vegGate);
  } finally {
    const stop = await stopWorldServer(serverRec);
    const result = {
      run: RUN_ID,
      gate: 'PIXEL_RENDER',
      status: allOk ? 'PASS' : 'FAIL',
      ok: allOk,
      honestLabel: 'pixel-content heuristic (not a semantic render check); PNGs in PRIVATE OUTPUT ONLY (metadata here)',
      server: { pid: serverRec.pid, port, startupLine: serverRec.startupLine, stop: { exitCode: stop.exitCode, portFreed: stop.portFreed } },
      shots,
    };
    if (rawOut) await writeFile(rawOut, JSON.stringify(result, null, 1) + '\n', 'utf8');
    console.log(`[world_pixel_render] server stopped (port freed: ${stop.portFreed}); gate ${allOk ? 'PASS' : 'FAIL'}`);
    process.exit(allOk ? 0 : 1);
  }
}

main().catch((e) => {
  console.error(`[world_pixel_render] UNEXPECTED FAILURE: ${e?.stack ?? e}`);
  process.exit(1);
});
