#!/usr/bin/env node
// world_r2_pixel_diff.mjs — PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010 (contract §8)
// The PIXEL gates for the browser-interaction captures: the vegetation and
// terrain-texture toggles must change the canvas-region pixels MEASURABLY
// (the R1 TOGGLE_THRESHOLDS discipline — a no-op toggle FAILS, never
// PASS-by-default), and every capture must be non-trivial.
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import { analyzePng, decodePngRaw } from './png_nontrivial.mjs';

const args = process.argv.slice(2);
let pngDir = null, outPath = null;
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--png-dir') pngDir = args[++i];
  else if (args[i] === '--out') outPath = args[++i];
}
if (!pngDir || !outPath) {
  console.error('usage: node tools/pecompat/world_r2_pixel_diff.mjs --png-dir <dir> --out <json>');
  process.exit(2);
}
await mkdir(path.dirname(outPath), { recursive: true });

const THRESHOLDS = Object.freeze({
  minBytes: 10000,
  fullUniqueColorsMin: 50,
  fullMostCommonFractionMax: 0.995,
  fullLumaStdDevMin: 1.0,
  toggle: { minDifferingFraction: 0.02, perPixelDiff: 8 },
});
// the full-canvas region of the R2 world layout (the canvas IS the main screen)
const REGIONS = { full: [0, 0, 1280, 720], canvas: [0, 0, 1160, 700] };
// the VISIBLE 3D canvas region when the „Szczegóły” drawer is open (the drawer
// covers the right ~520px; the action bar the top ~60px; the HUD the bottom
// ~70px — the identical chrome is excluded from the TOGGLE denominators)
const VISIBLE_CANVAS = [0, 70, 750, 650];

const diffPair = (a, b, region = null) => {
  const da = decodePngRaw(a), db = decodePngRaw(b);
  if (!da?.decodeOk || !db?.decodeOk || da.width !== db.width || da.height !== db.height || da.channels !== db.channels) {
    return { comparable: false, reason: 'dimension/raw mismatch', a: da?.decodeOk, b: db?.decodeOk };
  }
  // the honest region of interest: identical UI chrome (the open drawer, the
  // action bar, the HUD readouts) is EXCLUDED from the denominator — the R1
  // pixel-tool CANVAS_REGIONS discipline; a toggle that only changes the 3D
  // canvas is measured there, not diluted by fixed chrome
  const [rx0, ry0, rx1, ry1] = region ?? [0, 0, da.width, da.height];
  let differing = 0, total = 0, sumAbs = 0;
  const step = 4; // sample every 4th pixel (bounded measurement; documented)
  const pa = da.img, pb = db.img, ch = da.channels;
  for (let y = ry0; y < Math.min(ry1, da.height); y += step) {
    const rowA = y * da.width * ch, rowB = y * db.width * ch;
    for (let x = rx0; x < Math.min(rx1, da.width); x += step) {
      const i = rowA + x * ch, j = rowB + x * ch;
      const dr = Math.abs(pa[i] - pb[j]), dg = Math.abs(pa[i + 1] - pb[j + 1]), dbb = Math.abs(pa[i + 2] - pb[j + 2]);
      const luma = Math.abs((pa[i] * 0.299 + pa[i + 1] * 0.587 + pa[i + 2] * 0.114) - (pb[j] * 0.299 + pb[j + 1] * 0.587 + pb[j + 2] * 0.114));
      total++;
      if (luma >= THRESHOLDS.toggle.perPixelDiff || Math.max(dr, dg, dbb) >= THRESHOLDS.toggle.perPixelDiff) {
        differing++; sumAbs += (dr + dg + dbb) / 3;
      }
    }
  }
  const fraction = total ? differing / total : 0;
  return {
    comparable: true, region: region ?? 'full', sampledPixels: total, differing,
    differingFraction: fraction,
    meanAbsDeltaOverDiffering: differing ? sumAbs / differing : 0,
    threshold: THRESHOLDS.toggle,
    passes: fraction >= THRESHOLDS.toggle.minDifferingFraction,
  };
};

const result = { run: 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010', measuredAt: new Date().toISOString(), thresholds: THRESHOLDS, captures: {}, diffs: {} };
const files = ['world_ready.png', 'world_walk_moved.png', 'world_teleport_far.png', 'world_teleport_back.png', 'world_veg_on.png', 'world_veg_off.png', 'world_textures_on.png', 'world_textures_off.png', 'world_resized.png', 'assetlab_519316.png', 'assetlab_cd_control.png'];
for (const f of files) {
  try {
    const buf = await readFile(path.join(pngDir, f));
    const a = analyzePng(buf, { regions: REGIONS });
    const full = a.stats?.full ?? {};
    result.captures[f] = {
      bytes: buf.length,
      nontrivial: buf.length >= THRESHOLDS.minBytes && (full.uniqueColors ?? 0) >= THRESHOLDS.fullUniqueColorsMin &&
        (full.mostCommonColorFraction ?? 1) <= THRESHOLDS.fullMostCommonFractionMax && (full.lumaStdDev ?? 0) >= THRESHOLDS.fullLumaStdDevMin,
      full: { uniqueColors: full.uniqueColors, mostCommonColorFraction: full.mostCommonColorFraction, lumaStdDev: full.lumaStdDev },
    };
  } catch (e) {
    result.captures[f] = { missing: true, error: String(e?.message ?? e).slice(0, 200) };
  }
}
const pairs = [
  ['vegToggle', 'world_veg_on.png', 'world_veg_off.png', VISIBLE_CANVAS],
  ['textureToggle', 'world_textures_on.png', 'world_textures_off.png', VISIBLE_CANVAS],
  ['teleportFarVsHome', 'world_ready.png', 'world_teleport_far.png', null],
];
for (const [name, fa, fb, region] of pairs) {
  try {
    const a = await readFile(path.join(pngDir, fa));
    const b = await readFile(path.join(pngDir, fb));
    result.diffs[name] = { a: fa, b: fb, ...diffPair(a, b, region) };
  } catch (e) {
    result.diffs[name] = { a: fa, b: fb, missing: true, error: String(e?.message ?? e).slice(0, 200) };
  }
}
await writeFile(outPath, JSON.stringify(result, null, 1) + '\n');
console.log(JSON.stringify({
  captures: Object.fromEntries(Object.entries(result.captures).map(([k, v]) => [k, v.nontrivial ?? 'missing'])),
  diffs: Object.fromEntries(Object.entries(result.diffs).map(([k, v]) => [k, v.comparable ? { fraction: v.differingFraction, passes: v.passes } : 'not-comparable'])),
}, null, 2));
process.exit(0);
