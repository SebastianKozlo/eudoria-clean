#!/usr/bin/env node
// run_world_tests.mjs — WORLD_TESTS harness — PE_WORLD_LAUNCHER_R1_20261010, ETAP C + ETAP D
// Runs the world gate battery (contract §4 + §5 + §8):
//   WORLD_TERRAIN   — terrain gates through the PRODUCTION modules +
//                     independent byte-level reads (offset 64 vs 52, 1024
//                     heights, sentinel/NODATA, reverse order, hash witness,
//                     bounds/calibration-once, CAM identity)
//   WORLD_T7 (api)  — world server positives + denial subset + no
//                     whole-container route + overview/climates/gaps honesty
//   WORLD_MAT (Etap D) — the materials gates: mask@56 vs wrong-52 negative,
//                     raw weights bit-exact through the wire, malformed/RLE
//                     controlled failures, the id@+16 -> "<id>.dat" chain
//                     resolve + texture wire bit-exact, era refusal + CAM-C3
//                     cache mutants, the unresolved-binding diagnostic, the
//                     UV/flip pattern+real control, and the REAL window
//                     through the pure splat builder
//   WORLD_VEG (Etap E) — the vegetation gates: 25.vcl strict UNSUPPORTED,
//                     the measured default profile justification, the
//                     untouched byte-locked core + arithmetic control,
//                     repeat-seed determinism, streaming-order invariance,
//                     edge ownership, the 5000 cap, the model import chain
//                     (bit-exact wire + the witness + the support census),
//                     CAM-C3 model-cache mutants, the headless THREE
//                     resource-discipline census
//   WORLD_T9 (headless) — real-browser LOAD of /launcher and /world through
//                     the FIXED 5-conjunct gate
// REUSE LABEL: the harness follows tests/pecompat/run_catalog_tests.mjs
// (nonzero exit on ANY FAIL; NOT_PERFORMED counted separately, never PASS).
// The catalog/app/unit batteries are UNTOUCHED and run separately as the
// regression battery.
//
// Usage:
//   node tests/pecompat/run_world_tests.mjs [--terrain <terrain.bnt>]
//        [--textures <Textures.bnt>] [--raw-dir <dir>] [--json-out <path>]
// P3a FIX (correction round 2026-10-10): the DEFAULT raw dir is a NEUTRAL
// temp directory (os.tmpdir()), NOT a docs/audits package — an accidental
// flagless invocation can no longer write into the HISTORICAL READ_ONLY
// packages (PE_WORLD_LAUNCHER_R1_20261010 was the old default and was
// dirtied by exactly such an invocation in the original run). Writing into
// any docs/audits package now requires an EXPLICIT --raw-dir.
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { writeFile } from 'node:fs/promises';

const here = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(here, '..', '..');
const RUN_ID = 'PE_WORLD_LAUNCHER_R1_20261010'; // the battery lineage label ONLY — never a write path (see the P3a fix above)

const args = process.argv.slice(2);
const ctx = {
  terrainPath: null,
  texturesPath: null,
  rawDir: path.join(os.tmpdir(), 'pecompat-tests-raw', 'WORLD'),
  jsonOut: null,
};
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--terrain') ctx.terrainPath = args[++i];
  else if (args[i] === '--textures') ctx.texturesPath = args[++i];
  else if (args[i] === '--raw-dir') ctx.rawDir = args[++i];
  else if (args[i] === '--json-out') ctx.jsonOut = args[++i];
}

const suites = [
  ['world_terrain.test.mjs', (await import('./world_terrain.test.mjs')).run],
  ['world_server.test.mjs', (await import('./world_server.test.mjs')).run],
  ['world_materials.test.mjs', (await import('./world_materials.test.mjs')).run],
  ['world_vegetation.test.mjs', (await import('./world_vegetation.test.mjs')).run],
  ['world_headless_load.test.mjs', (await import('./world_headless_load.test.mjs')).run],
  ['world_r2_gates.test.mjs', (await import('./world_r2_gates.test.mjs')).run],
];

const all = [];
let pass = 0, fail = 0, notPerformed = 0;
const t0 = Date.now();

console.log(`== ${RUN_ID} — WORLD_TESTS (Etap C gate battery; harness pattern from run_catalog_tests.mjs) ==`);
console.log(`run: node tests/pecompat/run_world_tests.mjs --terrain "${ctx.terrainPath ?? '(default pin)'}" --raw-dir "${ctx.rawDir}"`);

for (const [file, run] of suites) {
  console.log(`\n---- ${file} ----`);
  let records = [];
  try {
    records = await run(ctx);
  } catch (e) {
    records = [{
      id: `${file}:CRASH`, name: file, status: 'FAIL',
      measuredQuantity: 'suite execution',
      measured: String(e?.stack ?? e),
      failureCaseDetected: 'suite crashed',
    }];
  }
  for (const r of records) {
    all.push({ suite: file, ...r });
    if (r.status === 'PASS') pass++;
    else if (r.status === 'NOT_PERFORMED') notPerformed++;
    else fail++;
    const badge = r.status === 'PASS' ? '[PASS]' : r.status === 'NOT_PERFORMED' ? '[NOT_PERFORMED]' : '[FAIL]';
    console.log(`${badge} ${r.id} — ${r.name}`);
    console.log(`  MEASURED_QUANTITY: ${r.measuredQuantity ?? '(see measured)'}`);
    if (r.independentSourceOfTruth) console.log(`  INDEPENDENT_SOURCE_OF_TRUTH: ${r.independentSourceOfTruth}`);
    if (r.whyNonCircular) console.log(`  WHY_NON_CIRCULAR: ${r.whyNonCircular}`);
    console.log(`  FAILURE_CASE_DETECTED: ${r.failureCaseDetected ?? 'n/a'}`);
    if (r.status !== 'PASS') {
      console.log(`  MEASURED: ${JSON.stringify(r.measured ?? null, null, 2).slice(0, 3000)}`);
    }
  }
}

const summary = {
  run: RUN_ID,
  phase: 'ETAP_C_AND_D',
  harnessInheritedFrom: 'tests/pecompat/run_catalog_tests.mjs (pattern; the catalog/app/unit batteries stay separate)',
  harness: 'tests/pecompat/run_world_tests.mjs',
  ctx: { terrainPath: ctx.terrainPath, texturesPath: ctx.texturesPath, rawDir: ctx.rawDir },
  totals: { pass, fail, notPerformed, total: all.length },
  elapsedMs: Date.now() - t0,
  serverLeftRunning: false,
  note: 'the T7/T9 suites start and stop their own bounded world server; the port-freed proof is asserted in each lifecycle record; the foreign standing servers (8140/8161) are never touched; 8162 is the documented default world port (dev server may hold it — suites use a free port)',
  tests: all,
};

console.log(`\n== SUMMARY: ${pass} PASS / ${fail} FAIL / ${notPerformed} NOT_PERFORMED (total ${all.length}) ==`);
if (ctx.jsonOut) {
  await writeFile(ctx.jsonOut, JSON.stringify(summary, null, 1) + '\n', 'utf8');
  console.log(`machine summary -> ${ctx.jsonOut}`);
}
process.exit(fail > 0 ? 1 : 0);
