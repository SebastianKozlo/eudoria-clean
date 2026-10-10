#!/usr/bin/env node
// world_splat_per_color.mjs — U-19 per-color revalidation gate —
// PE_WORLD_LAUNCHER_R1_20261010 (the QC P2-1 correction round).
//
// THE DEFECT (U-19, QC-confirmed at code level): SPLAT_FRAG sampled the
// sampler2DArray with the NORMALIZED idx byte (texelFetch on an RGBA8
// texture returns byte/255 in [0,1]) instead of the LAYER NUMBER — every
// layer sampled array layer 0 and the textured terrain rendered near-black
// in headless GPU captures. THE FIX (compat/world-app.js): decode the slot
// byte EXACTLY in the shader (floor(b*255.0+0.5): byte k -> layer k, no
// off-by-one; byte 255 = the EMPTY slot, now also correctly excluded by the
// < 254.5 guard evaluated on the DECODED value).
//
// THIS GATE proves the fix per-color at REAL GPU pixels — the QC revalidation
// requirement ("per-color pixel comparison of #textures=1, not merely
// toggle-vs-palette change"):
//   1. the page (#textures=1&veg=0) renders through the REAL app + the REAL
//      server wire; a CDP capture (the Etap E corrected method: readiness poll
//      on the page's OWN census markers + Page.captureScreenshot after a
//      real-time settle) provides the rendered pixels.
//   2. the EXPECTED color of a pixel is recomputed INDEPENDENTLY in Node from
//      the SAME wire data the page consumed (tiles -> PETerrainRegion ->
//      buildGeometry; materials -> buildRegionSplatData (the PURE builder);
//      textures -> decodeTga2), replicating the EXACT shader math (cell
//      lookup, GLOBAL world uv /32 m, GL bilinear+repeat sampling, the
//      sequential RAW mask/255 lerp in slot order) at the ray-hit world
//      position of that pixel (the app's own deterministic boot camera pose;
//      cross-checked against the page's live position HUD + census lines).
//   3. GATES:
//      WORLD_U19_PER_COLOR_EXACT — the read capture pixel lies within the
//        expected color span (5 sub-pixel ray hits bound the MSAA/edge blend)
//        for EVERY valid sample (>=20 samples, >=8 distinct cells).
//      WORLD_U19_LAYER_MAPPING_CONTROL — every slot byte in the window's idx
//        textures indexes a REAL texture slot (0..N-1; 255=EMPTY only), and
//        the exact gate itself is the render-level proof that layer k maps to
//        texture layer k (the expected uses textureIds[slotByte] and matches
//        the GPU output).
//      WORLD_U19_PRE_FIX_BEHAVIOR_REJECTED — the NEGATIVE CONTROL: the
//        pre-fix expectation (every layer samples array layer 0 = the window's
//        FIRST texture) does NOT match the read pixels (mean channel delta
//        >= 10 over the DISCRIMINATING samples — cells whose fixed vs
//        pre-fix expectations differ by >= 15); every discriminating sample
//        is CLOSER to the fixed expectation than to the pre-fix one. A
//        still-broken shader FAILS this control (the read pixels would match
//        the pre-fix expectation instead).
//      WORLD_U19_HEADLESS_NOT_NEAR_BLACK — the capture's canvas-region color
//        census (unique colors, mean luma, std) vs the PRE-FIX capture
//        (--pre-fix-png, the same URL state #textures=1&veg=0 from the
//        Etap E private captures): the near-black profile is GONE.
//
// HONEST LIMITS (never claimed by this gate): this is a HEADLESS GPU
// verification of the rendered per-color output — it is NOT interactive
// verification (INTERACTION stays NOT_PERFORMED; the interactive appearance
// stays UNVERIFIED). The raw weights, the record-order lerp, the
// RENDER_RECONSTRUCTION preset labels and every data path are UNCHANGED
// (only the layer-coordinate decode inside SPLAT_FRAG changed).
//
// The PNG is written to PRIVATE OUTPUT ONLY (never the repo). The --raw-out
// record carries METADATA + the per-sample evidence table (no payload bytes).
//
// Usage:
//   node tools/pecompat/world_splat_per_color.mjs --out-dir <PRIVATE png dir>
//        [--raw-out <report raw json>] [--pre-fix-png <the pre-fix capture>]
//        [--port <preferred>]
import { spawn, spawnSync } from 'node:child_process';
import { writeFile, mkdir } from 'node:fs/promises';
import { existsSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import * as THREE from 'three';
import { PETerrainRegion, worldHeightMeters } from '../../src/peworld/PETerrainCore.js';
import { TerrainTile } from '../../src/pesource/TerrainTile.js';
import { makeProvenance } from '../../src/pesource/PEProvenance.js';
import { decodeTga2 } from '../../src/pesource/TgaDecoder.js';
import {
  buildRegionSplatData, REGION_CELLS, MAX_LAYERS_PER_CELL, EMPTY_SLOT_INDEX,
} from '../../compat/world-splat.js';
import {
  startWorldServer, stopWorldServer, findFreePort, rawRequestFull,
} from '../../tests/pecompat/_world_server_helpers.mjs';
import { analyzePng, decodePngRaw } from './png_nontrivial.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const RUN_ID = 'PE_WORLD_LAUNCHER_R1_20261010';
const PROFILE_MARK = 'pec-world-launcher-percolor';
const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

// The fixed gate anchor — the SAME #tile the PIXEL toggle gates use.
const ANCHOR = { gx: 53, gy: 114 };
const GRID_W = 220, GRID_H = 236;
const TILE_M = 64, WINDOW_T = 8;
const UV_REPEAT_M = 32;      // RENDER_RECONSTRUCTION preset (world-splat.js)
const MATERIAL_CELL_M = 4;   // 16x16 cells per 32x32-sample tile
const CANVAS_REGION = [10, 110, 740, 540]; // the pixel tool's world canvas region (same layout)

// Preregistered gate thresholds (set BEFORE the run; a still-broken shader or
// a wrong layer mapping FAILS them — never PASS-by-default).
const GATE_THRESHOLDS = Object.freeze({
  minValidSamples: 20,
  minDistinctCells: 8,
  minDiscriminatingSamples: 8,
  spanTolerance: 3,          // per-channel units outside the 5-hit expected span
  discriminatingExpectedGap: 15, // |expectedFixed - expectedPrefixed| >= 15 (max channel)
  prefixRejectedMeanDelta: 10,   // mean max-channel delta read vs PREFIX expectation
  notNearBlack: { minUniqueColors: 600, minLumaMeanGain: 10, minLumaStdDev: 8 },
});

function sleep(ms) { return new Promise((r) => setTimeout(r, ms)); }
const clampI = (v, lo, hi) => Math.min(Math.max(v, lo), hi);

/** The app's desiredOrigin math (world-app.js) — the SETTLED window follows the
 * camera after resetView; cross-checked against the page's census line. */
function desiredOrigin(camGx, camGy) {
  return {
    gx: Math.min(Math.max(camGx - (WINDOW_T >> 1), 0), GRID_W - WINDOW_T),
    gy: Math.min(Math.max(camGy - (WINDOW_T >> 1), 0), GRID_H - WINDOW_T),
  };
}

function tileName(gx, gy) { return gx.toString(16).padStart(4, '0') + gy.toString(16).padStart(4, '0') + '.tdf'; }

/** GL bilinear sampling with REPEAT wrap on a flipY=false IMAGE-order RGBA
 * buffer (the EXACT GPU semantics of texture(uMats, vec3(uv, layer)) with
 * LinearFilter + RepeatWrapping on the 256x256 DataArrayTexture layers). */
function bilinearRepeat(rgba, size, u, v) {
  const s = u * size - 0.5, t = v * size - 0.5;
  const x0 = Math.floor(s), y0 = Math.floor(t);
  const fx = s - x0, fy = t - y0;
  const wrap = (i) => ((i % size) + size) % size;
  const xa = wrap(x0), xb = wrap(x0 + 1), ya = wrap(y0), yb = wrap(y0 + 1);
  const at = (x, y, c) => rgba[(y * size + x) * 4 + c];
  const out = [0, 0, 0];
  for (let c = 0; c < 3; c++) {
    const top = at(xa, ya, c) + (at(xb, ya, c) - at(xa, ya, c)) * fx;
    const bot = at(xa, yb, c) + (at(xb, yb, c) - at(xa, yb, c)) * fx;
    out[c] = top + (bot - top) * fy;
  }
  return out;
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

/** The readiness marker (ASCII-safe matchers; the page's OWN census lines —
 * the settled origin + the SETTLED WINDOW's texture chain census, which only
 * appears after applyTexturesForWindow(origin) completes, + the vegetation
 * line). expectedChain is computed from THIS tool's independent build of the
 * SAME wire data — a cross-check that the page's applied splat IS the window
 * this gate validates. */
function cdpReadinessExpression(origin, expectedChain) {
  return `(document.getElementById('diagnostics')?.getAttribute('data-load-status') === 'READY') && ` +
    `String(document.getElementById('world-census')?.textContent || '').includes('origin okna: ${origin.gx},${origin.gy}') && ` +
    `String(document.getElementById('world-census')?.textContent || '').includes('ro\u015blinno\u015b\u0107:') && ` +
    `String(document.getElementById('world-census')?.textContent || '').includes(${JSON.stringify(expectedChain)})`;
}

/** CDP headless-Edge session against the suite server (the pixel tool's
 * corrected capture method, reused: remote-debugging on a suite-owned free
 * port — NEVER 9222; a Runtime.evaluate readiness poll + a real-time settle
 * + Page.captureScreenshot). Returns { png, info } where info carries the
 * measured canvas rect/dpr/buffer + the live census/pos-hud text. */
async function captureWorldPage({ port, url, origin, expectedChain, waitMs = 120000 }) {
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
  const child = spawn(EDGE, args, { stdio: ['ignore', 'pipe', 'pipe'], windowsHide: true });
  let stderr = '';
  child.stderr.setEncoding('utf8');
  child.stderr.on('data', (d) => { stderr += d; });
  let exited = null;
  child.once('exit', (code, signal) => { exited = { code, signal }; });
  const cleanup = () => { try { child.kill(); } catch { /* already gone */ } killOwnLeftoverEdge(); };

  try {
    const deadline = Date.now() + waitMs;
    let pageWsUrl = null;
    while (Date.now() < deadline && !pageWsUrl) {
      if (exited) throw new Error(`Edge exited early (code ${exited.code}) — stderr: ${stderr.slice(0, 400)}`);
      try {
        const r = await fetch(`http://127.0.0.1:${dbgPort}/json/list`);
        const targets = await r.json();
        const page = targets.find((t) => t.type === 'page' && t.url.includes('/world'));
        if (page) pageWsUrl = page.webSocketDebuggerUrl;
      } catch { /* endpoint not up yet */ }
      await sleep(300);
    }
    if (!pageWsUrl) throw new Error('the DevTools /json/list page target never appeared');

    const ws = new WebSocket(pageWsUrl);
    await new Promise((resolve, reject) => {
      ws.addEventListener('open', resolve, { once: true });
      ws.addEventListener('error', () => reject(new Error('CDP websocket error')), { once: true });
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

    const expr = cdpReadinessExpression(origin, expectedChain);
    let ready = false, lastEval = null;
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

    // the real-time settle (presented frames at real vsync)
    await sleep(3000);

    // measured page geometry + the live census/pos-hud text (cross-checks)
    const infoExpr = `JSON.stringify({
      rect: (() => { const r = document.getElementById('view-canvas').getBoundingClientRect(); return { left: r.left, top: r.top, width: r.width, height: r.height }; })(),
      dpr: window.devicePixelRatio,
      bufW: document.getElementById('view-canvas').width,
      bufH: document.getElementById('view-canvas').height,
      posHud: String(document.getElementById('pos-hud')?.textContent || ''),
      census: String(document.getElementById('world-census')?.textContent || ''),
      loadStatus: document.getElementById('diagnostics')?.getAttribute('data-load-status'),
    })`;
    const ir = await send('Runtime.evaluate', { expression: infoExpr, returnByValue: true });
    const info = JSON.parse(ir.result.value);

    const shot = await send('Page.captureScreenshot', { format: 'png' });
    const png = Buffer.from(shot.data, 'base64');
    try { ws.close(); } catch { /* best effort */ }
    return { png, info, readinessExpression: expr, userDataDir, dbgPort };
  } finally {
    cleanup();
  }
}

async function main() {
  const args = process.argv.slice(2);
  const opt = (name) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
  const outDir = opt('--out-dir');
  const rawOut = opt('--raw-out');
  const preFixPng = opt('--pre-fix-png');
  const preferredPort = Number(opt('--port') ?? 8162);
  if (!outDir) { console.error('[world_splat_per_color] --out-dir (PRIVATE output root) is required'); process.exit(2); }
  await mkdir(outDir, { recursive: true });
  if (rawOut) await mkdir(path.dirname(rawOut), { recursive: true });
  if (!existsSync(EDGE)) {
    const result = { run: RUN_ID, gate: 'U19_PER_COLOR', status: 'NOT_PERFORMED', reason: `Edge binary not found at ${EDGE} — honest NOT_PERFORMED (no browser, no fake capture)` };
    if (rawOut) await writeFile(rawOut, JSON.stringify(result, null, 1) + '\n', 'utf8');
    console.error(result.reason); process.exit(0);
  }

  const port = await findFreePort(preferredPort);
  const serverRec = await startWorldServer({ port });
  const t0 = Date.now();
  try {
    // ================= PHASE A: the independent expected-data build =================
    // The app's boot math (world-app.js): anchor -> spawn (patch center) ->
    // boot window -> resetView pose -> the settled window follows the camera.
    const spawn = { x: ANCHOR.gx * TILE_M + 128, z: ANCHOR.gy * TILE_M + 128 };
    const bootOrigin = desiredOrigin(ANCHOR.gx + 1, ANCHOR.gy + 1);
    const camPose = { x: spawn.x + 180, z: spawn.z + 180 }; // resetView (orbit)
    const settledOrigin = desiredOrigin(Math.floor(camPose.x / TILE_M), Math.floor(camPose.z / TILE_M));
    console.log(`[world_splat_per_color] anchor ${ANCHOR.gx},${ANCHOR.gy} -> boot window ${bootOrigin.gx},${bootOrigin.gy} -> settled window ${settledOrigin.gx},${settledOrigin.gy}`);

    // tiles of the SETTLED window -> PETerrainRegion -> buildGeometry (positions+indices)
    const tileRows = [];
    for (let dy = 0; dy < WINDOW_T; dy++) {
      const row = [];
      for (let dx = 0; dx < WINDOW_T; dx++) row.push(null);
      tileRows.push(row);
    }
    for (let gy = settledOrigin.gy; gy < settledOrigin.gy + WINDOW_T; gy++) {
      for (let gx = settledOrigin.gx; gx < settledOrigin.gx + WINDOW_T; gx++) {
        const r = await rawRequestFull(port, `/api/world/tile/${gx}/${gy}`);
        if (r.status !== 200 || r.body.length !== 2048) throw new Error(`tile wire ${gx},${gy}: HTTP ${r.status} ${r.body.length} B != 2048`);
        const heights = new Uint16Array(r.body.buffer.slice(r.body.byteOffset, r.body.byteOffset + 2048));
        const prov = makeProvenance({
          era: r.headers['x-pe-era'] ?? 'PCG_9_3_5',
          container: r.headers['x-pe-container'] ?? 'Terrain/terrain.bnt',
          entry: r.headers['x-pe-entry'] ?? tileName(gx, gy),
          physicalSource: r.headers['x-pe-physical-source'] ?? '',
          offset: Number(r.headers['x-pe-offset'] ?? '0'),
          decoderVersion: r.headers['x-pe-decoder-version'] ?? '',
          evidenceStatus: r.headers['x-pe-evidence-status'] ?? 'CONFIRMED',
          extra: { containerSha256: r.headers['x-pe-container-sha256'] ?? '', heightDataOffsetPayloadRelative: 64, rawUInt16NoNormalization: true },
        });
        tileRows[gy - settledOrigin.gy][gx - settledOrigin.gx] = new TerrainTile({ gridX: gx, gridY: gy, name: tileName(gx, gy), heights, provenance: prov });
      }
    }
    const region = new PETerrainRegion(tileRows);
    const regionGeo = region.buildGeometry();
    // groundAt(spawn) with the SETTLED window (the same world sample the boot
    // window read: local (160,160) of (50,111) == local (64,64) of (53,114))
    const spawnLocalVx = Math.floor((spawn.x - settledOrigin.gx * TILE_M) / 2);
    const spawnLocalVy = Math.floor((spawn.z - settledOrigin.gy * TILE_M) / 2);
    const g = worldHeightMeters(region.rawSample(spawnLocalVx, spawnLocalVy));
    const cameraPos = { x: camPose.x, y: g + 220, z: camPose.z };
    console.log(`[world_splat_per_color] groundAt(spawn)=${g.toFixed(3)} m -> camera (${cameraPos.x}, ${cameraPos.y.toFixed(1)}, ${cameraPos.z})`);

    // the materials grid of the SETTLED window -> the PURE splat builder
    const matGrid = [];
    for (let dy = 0; dy < WINDOW_T; dy++) {
      const row = [];
      for (let dx = 0; dx < WINDOW_T; dx++) row.push(null);
      matGrid.push(row);
    }
    for (let gy = settledOrigin.gy; gy < settledOrigin.gy + WINDOW_T; gy++) {
      for (let gx = settledOrigin.gx; gx < settledOrigin.gx + WINDOW_T; gx++) {
        const r = await rawRequestFull(port, `/api/world/tile/${gx}/${gy}/materials`);
        if (r.status !== 200) throw new Error(`materials wire ${gx},${gy}: HTTP ${r.status}`);
        matGrid[gy - settledOrigin.gy][gx - settledOrigin.gx] = JSON.parse(r.body.toString('utf8'));
      }
    }
    const splatData = buildRegionSplatData(matGrid);
    const textureIds = splatData.textureIds;
    const decodeFailures = [];
    const textureRgba = [];
    const textureMean = [];
    for (const id of textureIds) {
      const r = await rawRequestFull(port, `/api/world/texture/${id}`);
      if (r.status !== 200) throw new Error(`texture wire ${id}: HTTP ${r.status}`);
      let decoded = null;
      try { decoded = decodeTga2(new Uint8Array(r.body)); }
      catch (e) { decodeFailures.push({ id, error: String(e?.message ?? e) }); continue; }
      if (decoded.width !== 256 || decoded.height !== 256) { decodeFailures.push({ id, error: `${decoded.width}x${decoded.height} != 256x256` }); continue; }
      textureRgba.push(decoded.rgba);
      let sr = 0, sg = 0, sb = 0;
      for (let i = 0; i < 256 * 256; i++) { sr += decoded.rgba[i * 4]; sg += decoded.rgba[i * 4 + 1]; sb += decoded.rgba[i * 4 + 2]; }
      textureMean.push([Math.round(sr / 65536), Math.round(sg / 65536), Math.round(sb / 65536)]);
    }
    if (decodeFailures.length > 0) {
      throw new Error(`THIS gate requires every window texture to decode (the page skips failed ones -> the layer mapping could diverge): ${decodeFailures.length} failures — refusing honestly`);
    }
    // the page's own chain census for the SETTLED window (deterministic; the
    // readiness poll requires the page to show EXACTLY these numbers).
    const expectedChain = `resolved ${splatData.resolvedLayers}/${splatData.layersTotal} warstw, zdekodowane tekstury ${textureIds.length}, zastosowane warstwy ${splatData.appliedLayers}`;
    console.log(`[world_splat_per_color] splat build: layers ${splatData.layersTotal}, resolved ${splatData.resolvedLayers}, textures ${textureIds.length}, applied ${splatData.appliedLayers}, unresolved ${splatData.unresolved.length}, capped ${splatData.cappedCells}`);
    if (splatData.unresolved.length > 0) throw new Error(`unresolved bindings in the gate window (${splatData.unresolved.length}) — the page census cross-check would be ambiguous; refusing honestly`);

    // ================= PHASE B: the real browser render =================
    const url = `http://127.0.0.1:${port}/world#tile=${ANCHOR.gx},${ANCHOR.gy}&profile=0&seed=0&density=50&textures=1&veg=0`;
    const { png, info } = await captureWorldPage({ port, url, origin: settledOrigin, expectedChain });
    const pngPath = path.join(outDir, 'pixel_world-percolor.png');
    await writeFile(pngPath, png);
    const sha = createHash('sha256').update(png).digest('hex');
    console.log(`[world_splat_per_color] capture: ${png.length} B -> ${pngPath} (PRIVATE) sha ${sha.slice(0, 12)}…`);

    // ================= PHASE C: the cross-checks =================
    const crossChecks = { cameraPose: null, settledOrigin: null, dpr: null, chainCensus: null };
    const posM = /X=([0-9.]+) Y=([0-9.]+) Z=([0-9.]+)/.exec(info.posHud ?? '');
    if (!posM) throw new Error(`the position HUD did not parse: ${JSON.stringify((info.posHud ?? '').slice(0, 160))}`);
    const hudPos = { x: parseFloat(posM[1]), y: parseFloat(posM[2]), z: parseFloat(posM[3]) };
    const poseOk = Math.abs(hudPos.x - cameraPos.x) <= 0.06 && Math.abs(hudPos.y - cameraPos.y) <= 0.06 && Math.abs(hudPos.z - cameraPos.z) <= 0.06;
    crossChecks.cameraPose = { computed: { x: cameraPos.x, y: Math.round(cameraPos.y * 100) / 100, z: cameraPos.z }, hud: hudPos, match: poseOk };
    const orgM = /origin okna: (\d+),(\d+)/.exec(info.census ?? '');
    crossChecks.settledOrigin = { computed: settledOrigin, page: orgM ? { gx: Number(orgM[1]), gy: Number(orgM[2]) } : null, match: !!orgM && Number(orgM[1]) === settledOrigin.gx && Number(orgM[2]) === settledOrigin.gy };
    crossChecks.dpr = { dpr: info.dpr, buffer: [info.bufW, info.bufH], rect: info.rect, ok: info.dpr === 1 && info.bufW === Math.round(info.rect.width) && info.bufH === Math.round(info.rect.height) };
    crossChecks.chainCensus = { expected: expectedChain, pageLineContains: (info.census ?? '').includes(expectedChain) };
    if (!poseOk) throw new Error(`camera pose cross-check FAILED (computed ${JSON.stringify(cameraPos)} vs HUD ${JSON.stringify(hudPos)}) — refusing honestly`);
    if (!crossChecks.settledOrigin.match) throw new Error(`settled origin cross-check FAILED (computed ${JSON.stringify(settledOrigin)} vs page ${orgM?.[0]})`);
    if (!crossChecks.dpr.ok) throw new Error(`dpr/buffer cross-check FAILED (dpr ${info.dpr}, buffer ${info.bufW}x${info.bufH}, rect ${info.rect.width}x${info.rect.height}) — the pixel mapping would be wrong; refusing honestly`);
    if (!crossChecks.chainCensus.pageLineContains) throw new Error(`the page's applied-splat census does not show the independently computed chain (${expectedChain}) — the capture is NOT the validated window; refusing honestly`);
    console.log('[world_splat_per_color] cross-checks: camera pose MATCH, settled origin MATCH, dpr/buffer MATCH, chain census MATCH');

    // ================= PHASE D: the per-color comparison =================
    const cap = decodePngRaw(png);
    if (!cap.decodeOk) throw new Error(`capture decode failed: ${cap.error}`);
    const readPx = (col, row) => {
      const i = (row * cap.width + col) * cap.channels;
      return [cap.img[i], cap.img[i + 1], cap.img[i + 2]];
    };
    const rectLeft = Math.round(info.rect.left), rectTop = Math.round(info.rect.top);

    const camera = new THREE.PerspectiveCamera(60, info.rect.width / info.rect.height, 0.5, 30000);
    camera.position.set(cameraPos.x, cameraPos.y, cameraPos.z);
    camera.lookAt(new THREE.Vector3(spawn.x, g, spawn.z));
    camera.updateMatrixWorld();
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(regionGeo.positions, 3));
    geo.setIndex(new THREE.BufferAttribute(regionGeo.indices, 1));
    const mesh = new THREE.Mesh(geo, new THREE.MeshBasicMaterial());
    mesh.position.set(settledOrigin.gx * TILE_M, 0, settledOrigin.gy * TILE_M);
    mesh.updateMatrixWorld(true);
    const raycaster = new THREE.Raycaster();
    const castRayAt = (fx, fy) => { // fx/fy = buffer-pixel coordinates (float; the pixel center = px + 0.5)
      const ndc = new THREE.Vector2((2 * fx) / info.bufW - 1, 1 - (2 * fy) / info.bufH);
      raycaster.setFromCamera(ndc, camera);
      const hits = raycaster.intersectObject(mesh, false);
      return hits.length ? hits[0].point.clone() : null;
    };

    // the EXACT shader math on the independent build (fixed + pre-fix layer maps)
    const layerOfFixed = (slotByte) => textureRgba[slotByte];
    const layerOfPreFix = () => textureRgba[0]; // the defect: EVERY layer sampled array layer 0
    const shaderExpected = (p, layerOf) => {
      const u = p.x / UV_REPEAT_M, v = p.z / UV_REPEAT_M;
      const cx = clampI(Math.floor((p.x - settledOrigin.gx * TILE_M) / MATERIAL_CELL_M), 0, REGION_CELLS - 1);
      const cy = clampI(Math.floor((p.z - settledOrigin.gy * TILE_M) / MATERIAL_CELL_M), 0, REGION_CELLS - 1);
      const texel = (cy * REGION_CELLS + cx) * 4;
      let r = 0, g2 = 0, b = 0, any = false;
      const layers = [];
      for (let slot = 0; slot < MAX_LAYERS_PER_CELL; slot++) {
        const sb = splatData.idxTextures[slot >> 2][texel + (slot & 3)];
        const w = splatData.wTextures[slot >> 2][texel + (slot & 3)];
        if (w > 0 && sb !== EMPTY_SLOT_INDEX) {
          const c = bilinearRepeat(layerOf(sb), 256, u, v);
          const a = w / 255;
          r += (c[0] - r) * a; g2 += (c[1] - g2) * a; b += (c[2] - b) * a;
          any = true;
          layers.push({ slot, textureId: textureIds[sb], weight: w });
        }
      }
      return { rgb: any ? [r, g2, b] : null, any, cell: [cx, cy], layers };
    };
    const cellOf = (p) => [
      clampI(Math.floor((p.x - settledOrigin.gx * TILE_M) / MATERIAL_CELL_M), 0, REGION_CELLS - 1),
      clampI(Math.floor((p.z - settledOrigin.gy * TILE_M) / MATERIAL_CELL_M), 0, REGION_CELLS - 1),
    ];
    const maxChannelDelta = (a, b) => Math.max(Math.abs(a[0] - b[0]), Math.abs(a[1] - b[1]), Math.abs(a[2] - b[2]));

    // the structural layer-mapping control: every slot byte in the idx
    // textures is a REAL texture slot (0..N-1) or the EMPTY marker
    let badSlotBytes = 0, slotByteHist = new Map();
    for (const t of splatData.idxTextures) {
      for (let i = 0; i < t.length; i += 4) {
        for (let c = 0; c < 4; c++) {
          const sb = t[i + c];
          if (sb === EMPTY_SLOT_INDEX) continue;
          if (sb >= textureIds.length) badSlotBytes++;
          else slotByteHist.set(sb, (slotByteHist.get(sb) ?? 0) + 1);
        }
      }
    }
    const layerMappingControl = {
      textureSlots: textureIds.length,
      distinctSlotBytesUsed: [...slotByteHist.keys()].sort((a, b) => a - b),
      badSlotBytes, // >= 1 would ALSO sample out-of-range layers on the GPU
      ok: badSlotBytes === 0,
    };

    // candidate canvas pixels -> ray -> validity -> expected vs read
    const samples = [];
    const reject = { miss: 0, boxMiss: 0, cellChange: 0, border: 0, inactive: 0 };
    const pxMin = Math.round(info.rect.width * 0.12), pxMax = Math.round(info.rect.width * 0.88);
    const pyMin = Math.round(info.rect.height * 0.12), pyMax = Math.round(info.rect.height * 0.88);
    const timeBudgetMs = 120000;
    const collectStart = Date.now();
    outer:
    for (let py = pyMin; py <= pyMax; py += 36) {
      for (let px = pxMin; px <= pxMax; px += 40) {
        if (samples.length >= 36) break outer;
        if (Date.now() - collectStart > timeBudgetMs) { console.log('[world_splat_per_color] collect time budget reached — evaluating with the samples collected (honest count)'); break outer; }
        const p = castRayAt(px + 0.5, py + 0.5);
        if (!p) { reject.miss++; continue; }
        // 2-px box: the neighborhood must hit the SAME material cell (no cell-boundary AA blend)
        let cellChange = false, boxMiss = false;
        for (const [ox, oy] of [[2, 0], [-2, 0], [0, 2], [0, -2]]) {
          const q = castRayAt(px + 0.5 + ox, py + 0.5 + oy);
          if (!q) { boxMiss = true; break; }
          const cc = cellOf(q), c0 = cellOf(p);
          if (cc[0] !== c0[0] || cc[1] !== c0[1]) { cellChange = true; break; }
        }
        if (boxMiss) { reject.boxMiss++; continue; }
        if (cellChange) { reject.cellChange++; continue; }
        // away from the tile-bound overlay lines (every 64 m tile border)
        const mx = p.x % TILE_M, mz = p.z % TILE_M;
        if (mx < 2.5 || mx > TILE_M - 2.5 || mz < 2.5 || mz > TILE_M - 2.5) { reject.border++; continue; }
        const exp = shaderExpected(p, layerOfFixed);
        if (!exp.any) { reject.inactive++; continue; } // the honest void cell (no active layers)
        const expPre = shaderExpected(p, layerOfPreFix);
        // the 5-hit expected span (center + 4 sub-pixel diagonals) bounds the MSAA/edge blend
        const span = [[exp.rgb[0], exp.rgb[1], exp.rgb[2]], ];
        for (const [ox, oy] of [[0.3, 0.3], [0.3, -0.3], [-0.3, 0.3], [-0.3, -0.3]]) {
          const q = castRayAt(px + 0.5 + ox, py + 0.5 + oy);
          if (q) {
            const eq = shaderExpected(q, layerOfFixed);
            if (eq.any) span.push(eq.rgb);
          }
        }
        const spanMin = [Math.min(...span.map((c) => c[0])), Math.min(...span.map((c) => c[1])), Math.min(...span.map((c) => c[2]))];
        const spanMax = [Math.max(...span.map((c) => c[0])), Math.max(...span.map((c) => c[1])), Math.max(...span.map((c) => c[2]))];
        const read = readPx(rectLeft + px, rectTop + py);
        const inSpan = [0, 1, 2].every((c) => read[c] >= spanMin[c] - GATE_THRESHOLDS.spanTolerance && read[c] <= spanMax[c] + GATE_THRESHOLDS.spanTolerance);
        const dFixed = maxChannelDelta(read, exp.rgb);
        const dPre = maxChannelDelta(read, expPre.rgb);
        const discriminating = expPre.any && maxChannelDelta(exp.rgb, expPre.rgb) >= GATE_THRESHOLDS.discriminatingExpectedGap;
        samples.push({
          capturePixel: [rectLeft + px, rectTop + py],
          canvasPixel: [px, py],
          worldHit: { x: Math.round(p.x * 100) / 100, y: Math.round(p.y * 100) / 100, z: Math.round(p.z * 100) / 100 },
          cell: exp.cell,
          layers: exp.layers,
          expectedFixed: exp.rgb.map((v) => Math.round(v * 10) / 10),
          expectedSpan: { min: spanMin.map((v) => Math.round(v * 10) / 10), max: spanMax.map((v) => Math.round(v * 10) / 10) },
          expectedPreFix: expPre.rgb.map((v) => Math.round(v * 10) / 10),
          read,
          deltaFixed: dFixed, deltaPreFix: dPre,
          inSpan, discriminating,
        });
      }
    }
    const distinctCells = new Set(samples.map((s) => s.cell.join(','))).size;
    const discriminatingSamples = samples.filter((s) => s.discriminating);
    const exactOk = samples.length >= GATE_THRESHOLDS.minValidSamples
      && distinctCells >= GATE_THRESHOLDS.minDistinctCells
      && samples.every((s) => s.inSpan);
    const prefixMeanDelta = discriminatingSamples.length
      ? discriminatingSamples.reduce((a, s) => a + s.deltaPreFix, 0) / discriminatingSamples.length : 0;
    const prefixRejected = discriminatingSamples.length >= GATE_THRESHOLDS.minDiscriminatingSamples
      && prefixMeanDelta >= GATE_THRESHOLDS.prefixRejectedMeanDelta
      && discriminatingSamples.every((s) => s.deltaFixed < s.deltaPreFix);

    // the canvas-region census: post-fix vs pre-fix (the same #textures=1&veg=0 state)
    const postStats = await analyzePng(png, { regions: { canvasRegion: CANVAS_REGION } });
    let preFixStats = null, notNearBlack = null;
    if (preFixPng && existsSync(preFixPng)) {
      const { readFile } = await import('node:fs/promises');
      const preBuf = await readFile(preFixPng);
      const pre = await analyzePng(preBuf, { regions: { canvasRegion: CANVAS_REGION } });
      preFixStats = { path: preFixPng, bytes: statSync(preFixPng).size, sha256: createHash('sha256').update(preBuf).digest('hex'), canvasRegion: pre.stats.canvasRegion, full: pre.stats.full };
      const post = postStats.stats.canvasRegion;
      notNearBlack = {
        preFixCanvas: pre.stats.canvasRegion,
        postFixCanvas: post,
        uniqueColorsGain: post.uniqueColors - pre.stats.canvasRegion.uniqueColors,
        lumaMeanGain: Math.round((post.lumaMean - pre.stats.canvasRegion.lumaMean) * 100) / 100,
        ok: post.uniqueColors >= GATE_THRESHOLDS.notNearBlack.minUniqueColors
          && (post.lumaMean - pre.stats.canvasRegion.lumaMean) >= GATE_THRESHOLDS.notNearBlack.minLumaMeanGain
          && post.lumaStdDev >= GATE_THRESHOLDS.notNearBlack.minLumaStdDev,
      };
    } else {
      notNearBlack = { status: 'NOT_PERFORMED', reason: preFixPng ? `--pre-fix-png not found: ${preFixPng}` : 'no --pre-fix-png given (the pre/post census comparison is optional evidence; the exact per-color gate is the primary proof)' };
    }

    const gates = [
      {
        id: 'WORLD_U19_PER_COLOR_EXACT',
        name: 'the rendered #textures=1 terrain pixels match the INDEPENDENTLY recomputed shader output per sample (the ray-hit world position -> cell -> RAW-weight sequential lerp -> bilinear texture sample; the read capture pixel within the 5-hit expected span ± tolerance)',
        status: exactOk ? 'PASS' : 'FAIL',
        measured: {
          validSamples: samples.length, distinctCells, inSpan: samples.filter((s) => s.inSpan).length,
          maxDeltaFixed: samples.reduce((a, s) => Math.max(a, s.deltaFixed), 0),
          meanDeltaFixed: samples.length ? Math.round(samples.reduce((a, s) => a + s.deltaFixed, 0) / samples.length * 100) / 100 : null,
          rejected: reject,
          thresholds: GATE_THRESHOLDS,
          samples: samples.map((s) => ({ ...s, layers: s.layers.map((l) => ({ slot: l.slot, textureId: l.textureId, weight: l.weight })) })),
        },
        independentSourceOfTruth: 'the wire payloads (tiles + materials + textures) re-fetched through the same routes and rebuilt through the PRODUCTION modules (PETerrainRegion/buildRegionSplatData/decodeTga2) + the shader math reimplemented from the SPLAT_FRAG source',
        whyNonCircular: 'the expected color is computed by THIS tool from the original payloads without touching the page state; the read pixel is the page\u2019s REAL GPU output — agreement proves the layer mapping, disagreement localizes the defect',
        failureCaseDetected: exactOk ? null : `valid ${samples.length} (>= ${GATE_THRESHOLDS.minValidSamples} required), distinct cells ${distinctCells} (>= ${GATE_THRESHOLDS.minDistinctCells}), out-of-span ${samples.length - samples.filter((s) => s.inSpan).length}`,
      },
      {
        id: 'WORLD_U19_LAYER_MAPPING_CONTROL',
        name: 'structural: every slot byte in the window idx textures is a REAL texture slot (0..N-1; 255=EMPTY only) — layer k maps to texture slot k (the exact gate is the render-level proof)',
        status: layerMappingControl.ok ? 'PASS' : 'FAIL',
        measured: layerMappingControl,
        independentSourceOfTruth: 'the idx texture arrays from the pure builder over the served materials',
        whyNonCircular: 'an out-of-range slot byte would sample an out-of-range array layer (undefined/black on the GPU) and fail both this control and the exact gate',
        failureCaseDetected: layerMappingControl.ok ? null : `${layerMappingControl.badSlotBytes} slot bytes >= textureIds.length`,
      },
      {
        id: 'WORLD_U19_PRE_FIX_BEHAVIOR_REJECTED',
        name: 'negative control: the PRE-FIX expectation (every layer samples array layer 0 = the window FIRST texture) does NOT match the read pixels',
        status: prefixRejected ? 'PASS' : 'FAIL',
        measured: {
          discriminatingSamples: discriminatingSamples.length,
          meanDeltaPreFix: Math.round(prefixMeanDelta * 100) / 100,
          maxDeltaPreFix: discriminatingSamples.reduce((a, s) => Math.max(a, s.deltaPreFix), 0),
          everyDiscriminatingCloserToFixed: discriminatingSamples.every((s) => s.deltaFixed < s.deltaPreFix),
          thresholds: GATE_THRESHOLDS,
        },
        independentSourceOfTruth: 'the same shader math with the DEFECTIVE layer map (layer 0 for every slot) — the behavior the pre-fix shader produced',
        whyNonCircular: 'a still-broken shader renders the pre-fix expectation — the read pixels would MATCH it and this control FAILS (it can only pass when the fix is real)',
        failureCaseDetected: prefixRejected ? null : `discriminating ${discriminatingSamples.length}, meanDeltaPreFix ${prefixMeanDelta.toFixed(2)}`,
      },
      {
        id: 'WORLD_U19_HEADLESS_NOT_NEAR_BLACK',
        name: 'the headless #textures=1&veg=0 capture canvas-region census vs the PRE-FIX capture (the near-black profile is gone; real TGA-derived colors)',
        status: notNearBlack?.ok === true ? 'PASS' : notNearBlack?.status === 'NOT_PERFORMED' ? 'NOT_PERFORMED' : 'FAIL',
        measured: notNearBlack,
        independentSourceOfTruth: 'the bounded PNG census (tools/pecompat/png_nontrivial.mjs) over the canvas region of the two PRIVATE captures',
        whyNonCircular: 'the pre-fix capture is the Etap E private PNG (kept); the post-fix capture is this gate\u2019s — the census is computed, not asserted',
        failureCaseDetected: notNearBlack?.ok === true || notNearBlack?.status === 'NOT_PERFORMED' ? null : `post uniqueColors ${notNearBlack?.postFixCanvas?.uniqueColors}, lumaMeanGain ${notNearBlack?.lumaMeanGain}`,
      },
    ];
    const allOk = gates.every((x) => x.status === 'PASS' || x.status === 'NOT_PERFORMED');

    const result = {
      run: RUN_ID,
      gate: 'U19_PER_COLOR',
      phase: 'U19_SPLAT_LAYER_COORDINATE_FIX',
      status: allOk ? 'PASS' : 'FAIL',
      ok: allOk,
      fix: {
        defect: 'SPLAT_FRAG sampled texture(uMats, vec3(uv, i0.x)) with the NORMALIZED idx byte (RGBA8 texelFetch -> byte/255 in [0,1]) instead of the LAYER NUMBER — every layer sampled array layer 0 (near-black headless render)',
        fix: 'decode the slot byte EXACTLY in the shader: s = floor(i*255.0+0.5) — byte k -> array layer k (the idx bytes ARE the texture slot numbers; the DataArrayTexture is filled in textureIds order); the empty-slot guard (< 254.5) now evaluates the DECODED value (pre-fix it compared the normalized byte against 254.5 — always true)',
        location: 'compat/world-app.js SPLAT_FRAG (the decode block + the 16 layer-sampling lines)',
        unchanged: 'RAW weights bit-exact the served masks; the RECORD-ORDER sequential lerp; NO weight normalization; the RENDER_RECONSTRUCTION preset labels; every data path (tiles/materials/textures wire, PEFoliageCore, decoders) untouched',
      },
      honestLimits: 'HEADLESS GPU verification of the per-color output — NOT interactive verification (INTERACTION stays NOT_PERFORMED; the interactive appearance stays UNVERIFIED)',
      crossChecks,
      expectedData: {
        settledWindow: settledOrigin, spawn: { x: spawn.x, z: spawn.z },
        layersTotal: splatData.layersTotal, resolvedLayers: splatData.resolvedLayers,
        appliedLayers: splatData.appliedLayers, textureSlots: textureIds.length,
        textureIds, textureMeanColors: textureMean,
        activeLayersHist: splatData.activeLayersHist,
        chainCensusLine: expectedChain,
      },
      capture: {
        kind: 'world-percolor', url, bytes: png.length, sha256: sha,
        captureMethod: 'CDP (remote-debugging + Runtime.evaluate readiness poll incl. the page chain-census cross-check + Page.captureScreenshot after a real-time settle)',
        privatePngPath: pngPath,
        note: 'PNG in the PRIVATE OUTPUT ROOT only (no proprietary rendered payloads in the repo)',
      },
      preFixComparison: preFixStats,
      gates,
      thresholds: GATE_THRESHOLDS,
      server: { pid: serverRec.pid, port, startupLine: serverRec.startupLine },
      elapsedMs: Date.now() - t0,
    };
    if (rawOut) await writeFile(rawOut, JSON.stringify(result, null, 1) + '\n', 'utf8');
    for (const g of gates) console.log(`[world_splat_per_color] ${g.id}: ${g.status}`);
    console.log(`[world_splat_per_color] valid samples ${samples.length}, distinct cells ${distinctCells}, discriminating ${discriminatingSamples.length}, meanDeltaFixed ${(samples.reduce((a, s) => a + s.deltaFixed, 0) / Math.max(1, samples.length)).toFixed(2)}, meanDeltaPreFix ${prefixMeanDelta.toFixed(2)}`);
    console.log(`[world_splat_per_color] gate ${allOk ? 'PASS' : 'FAIL'} (server stop follows)`);
    process.exitCode = allOk ? 0 : 1;
  } finally {
    const stop = await stopWorldServer(serverRec);
    console.log(`[world_splat_per_color] server stopped (port freed: ${stop.portFreed})`);
  }
}

main().catch((e) => {
  console.error(`[world_splat_per_color] UNEXPECTED FAILURE: ${e?.stack ?? e}`);
  killOwnLeftoverEdge();
  process.exit(1);
});
