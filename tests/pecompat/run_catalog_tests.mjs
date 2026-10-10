#!/usr/bin/env node
// run_catalog_tests.mjs — CATALOG_TESTS harness — PE_CITY_ASSET_MAP_R1_20261010, phase 4 (W6).
// PE_WORLD_LAUNCHER_R1_20261010 Etap A: the battery gains the Focused QC A
// suite (catalog_cam_fixes.test.mjs — CAM-C1 fresh GLB comparison execution,
// CAM-C2 shared status model + 1572 baseline control, CAM-C3 three mutants +
// clean + no-envelope refusal through the REAL production build). The prior
// 33 gates are UNCHANGED (no assertion weakened).
// Runs the phase-4 /catalog gate battery (contract §7):
//   CAT_ARCHIVE_SAFETY   — bounded archive reads, CRC/tamper, truncation,
//                          wrong magic, duplicate-ID era separation, pin re-verify
//   CAT_BOUNDS_COUNTERCHECK — hierarchy->bounds independent countercheck
//   CAT_TEXTURE_GATES    — wrong-ID / wrong-era / missing-image controlled dispositions
//   CAT_UNKNOWN_SORT     — UNKNOWN sort/filter/badge correctness (never 0)
//   CAT_PREVIEW_MATH     — no-accidental-centering / no-double-conversion
//   CAM_C1/C2/C3         — Etap A focused QC (PE_WORLD_LAUNCHER_R1_20261010)
//   CAT_T7 (api_denial)  — catalog server positives + synthetic denial battery
//   CAT_T9 (headless)    — real-browser LOAD of /catalog through the FIXED gate
// REUSE LABEL: the harness follows tests/pecompat/run_app_tests.mjs (the
// app harness — nonzero exit on ANY FAIL; NOT_PERFORMED counted separately,
// never reported as PASS). The 218757 suites (run_tests.mjs / run_app_tests.mjs)
// are UNTOUCHED and run separately as the regression battery.
//
// Usage:
//   node tests/pecompat/run_catalog_tests.mjs --models <Models.bnt>
//        [--models-ark <Models.ark>] [--textures-bnt <Textures.bnt>]
//        [--textures-ark <Textures.ark>] [--batch-state <jsonl>]
//        [--name-edges <jsonl>] [--raw-dir <dir>] [--json-out <path>]
//        [--three-root <three pkg dir>]
// The DEFAULT raw dir is THIS run's report package (never a historical package).
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { writeFile } from 'node:fs/promises';

const here = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(here, '..', '..');
const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';
const PRIV_DEFAULT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_CITY_ASSET_MAP_R1_20261010';

const args = process.argv.slice(2);
const ctx = {
  modelsPath: null,
  modelsArkPath: null,
  texturesBntPath: null,
  texturesArkPath: null,
  batchStatePath: `${PRIV_DEFAULT}\\PHASE2_EXTENT\\PCG935_NIF10_BATCH_STATE.jsonl`,
  nameEdgesPath: `${PRIV_DEFAULT}\\PHASE3_PCG935_BATCH\\PCG935_NAME_EDGES.jsonl`,
  threeRoot: null,
  rawDir: path.join(REPO_ROOT, 'docs', 'audits', RUN_ID, 'raw', 'CATALOG'),
  jsonOut: null,
};
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--models') ctx.modelsPath = args[++i];
  else if (args[i] === '--models-ark') ctx.modelsArkPath = args[++i];
  else if (args[i] === '--textures-bnt') ctx.texturesBntPath = args[++i];
  else if (args[i] === '--textures-ark') ctx.texturesArkPath = args[++i];
  else if (args[i] === '--batch-state') ctx.batchStatePath = args[++i];
  else if (args[i] === '--name-edges') ctx.nameEdgesPath = args[++i];
  else if (args[i] === '--three-root') ctx.threeRoot = args[++i];
  else if (args[i] === '--raw-dir') ctx.rawDir = args[++i];
  else if (args[i] === '--json-out') ctx.jsonOut = args[++i];
}

const suites = [
  ['catalog_archive_safety.test.mjs', (await import('./catalog_archive_safety.test.mjs')).run],
  ['catalog_bounds_countercheck.test.mjs', (await import('./catalog_bounds_countercheck.test.mjs')).run],
  ['catalog_texture_gates.test.mjs', (await import('./catalog_texture_gates.test.mjs')).run],
  ['catalog_unknown_sort.test.mjs', (await import('./catalog_unknown_sort.test.mjs')).run],
  ['catalog_preview_math.test.mjs', (await import('./catalog_preview_math.test.mjs')).run],
  ['catalog_cam_fixes.test.mjs', (await import('./catalog_cam_fixes.test.mjs')).run],
  ['catalog_api_denial.test.mjs', (await import('./catalog_api_denial.test.mjs')).run],
  ['catalog_headless_load.test.mjs', (await import('./catalog_headless_load.test.mjs')).run],
];

const all = [];
let pass = 0, fail = 0, notPerformed = 0;
const t0 = Date.now();

console.log(`== ${RUN_ID} — CATALOG_TESTS (phase-4 /catalog gate battery; harness pattern from run_app_tests.mjs) ==`);
console.log(`run: node tests/pecompat/run_catalog_tests.mjs --models "${ctx.modelsPath ?? '(default pin)'}" --raw-dir "${ctx.rawDir}"`);

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
  harnessInheritedFrom: 'tests/pecompat/run_app_tests.mjs (pattern; the 218757 suites stay separate)',
  phase: 'CATALOG_MODE_SERVER_TESTS',
  harness: 'tests/pecompat/run_catalog_tests.mjs',
  ctx: {
    modelsPath: ctx.modelsPath, modelsArkPath: ctx.modelsArkPath,
    texturesBntPath: ctx.texturesBntPath, texturesArkPath: ctx.texturesArkPath,
    batchStatePath: ctx.batchStatePath, nameEdgesPath: ctx.nameEdgesPath,
    rawDir: ctx.rawDir,
  },
  totals: { pass, fail, notPerformed, total: all.length },
  elapsedMs: Date.now() - t0,
  serverLeftRunning: false,
  note: 'the T7/T9-style suites start and stop their own bounded catalog server; the port-freed proof is asserted in each lifecycle record; the foreign 8140 reference server is never touched',
  tests: all,
};

console.log(`\n== SUMMARY: ${pass} PASS / ${fail} FAIL / ${notPerformed} NOT_PERFORMED (total ${all.length}) ==`);
if (ctx.jsonOut) {
  await writeFile(ctx.jsonOut, JSON.stringify(summary, null, 1) + '\n', 'utf8');
  console.log(`machine summary -> ${ctx.jsonOut}`);
}
process.exit(fail > 0 ? 1 : 0);
