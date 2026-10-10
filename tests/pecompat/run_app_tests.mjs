#!/usr/bin/env node
// run_app_tests.mjs — APP_SERVER_TESTS harness — base PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009,
// T9 gate fix + run relabel PE_CITY_ASSET_MAP_R1_20261010 (worktree pe-city-asset-map-r1).
// Runs the app/server gates: T7 (API + path denial against a RUNNING server),
// T8 (app-integration through the app's own builder path) and T9 (headless
// real-browser load through the FIXED 5-conjunct gate — see
// tests/pecompat/headless_load.test.mjs for the SCENEIR-T9-C1 defect history).
// The T7/T9 suites own their bounded server lifecycle (start/stop/PID/
// port-freed proof; NOTHING is left running at the end). The phase-2 unit
// harness (run_tests.mjs) and its verified artifacts are untouched.
//
// Harness exit code: ANY FAIL record (suite crash, gate failure, side error)
// produces a NONZERO harness exit (fail > 0 -> exit 1); NOT_PERFORMED records
// do NOT fail the harness but are counted separately and can never be
// reported as PASS.
//
// Usage:
//   node tests/pecompat/run_app_tests.mjs [--models <Models.bnt>]
//        [--raw-dir <dir>] [--json-out <path>] [--three-root <three pkg dir>]
// Without --models, T8 reports NOT_PERFORMED_CONTAINER_UNAVAILABLE loudly
// (T7 also fails closed — the server refuses to serve without the pinned
// container; that refusal is itself a recorded fail-closed behavior).
// The DEFAULT raw dir is THIS run's report package (never the historical
// READ_ONLY package of the predecessor run).
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { writeFile } from 'node:fs/promises';

const here = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(here, '..', '..');
const RUN_ID = 'PE_CITY_ASSET_MAP_R1_20261010';

const args = process.argv.slice(2);
const ctx = {
  modelsPath: null,
  threeRoot: null,
  rawDir: path.join(REPO_ROOT, 'docs', 'audits', RUN_ID, 'raw'),
  jsonOut: null,
};
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--models') ctx.modelsPath = args[++i];
  else if (args[i] === '--three-root') ctx.threeRoot = args[++i];
  else if (args[i] === '--raw-dir') ctx.rawDir = args[++i];
  else if (args[i] === '--json-out') ctx.jsonOut = args[++i];
}

const suites = [
  ['api_path_denial.test.mjs', (await import('./api_path_denial.test.mjs')).run],
  ['app_integration.test.mjs', (await import('./app_integration.test.mjs')).run],
  ['headless_load.test.mjs', (await import('./headless_load.test.mjs')).run],
];

const all = [];
let pass = 0, fail = 0, notPerformed = 0;
const t0 = Date.now();

console.log(`== ${RUN_ID} — APP_SERVER_TESTS (T7/T8/T9 fixed gate; harness inherited from PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009) ==`);
console.log(`run: node tests/pecompat/run_app_tests.mjs --models "${ctx.modelsPath ?? '(none)'}" --raw-dir "${ctx.rawDir}"`);

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
  harnessInheritedFrom: 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009',
  phase: 'APP_SERVER_TESTS',
  harness: 'tests/pecompat/run_app_tests.mjs',
  ctx: { modelsPath: ctx.modelsPath, rawDir: ctx.rawDir, threeRoot: ctx.threeRoot },
  totals: { pass, fail, notPerformed, total: all.length },
  elapsedMs: Date.now() - t0,
  serverLeftRunning: false,
  note: 'T7/T9 suites start and stop their own bounded server processes; the port-freed proof is asserted inside each lifecycle record',
  tests: all,
};

console.log(`\n== SUMMARY: ${pass} PASS / ${fail} FAIL / ${notPerformed} NOT_PERFORMED (total ${all.length}) ==`);
if (ctx.jsonOut) {
  await writeFile(ctx.jsonOut, JSON.stringify(summary, null, 1) + '\n', 'utf8');
  console.log(`machine summary -> ${ctx.jsonOut}`);
}
process.exit(fail > 0 ? 1 : 0);
