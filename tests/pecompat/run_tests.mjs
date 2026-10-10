#!/usr/bin/env node
// run_tests.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// Zero-dependency Node harness for the preregistered test classes (repo
// style: each control prints MEASURED_QUANTITY / INDEPENDENT_SOURCE_OF_TRUTH /
// WHY_NON_CIRCULAR / FAILURE_CASE_DETECTED). Aggregates PASS/FAIL/
// NOT_PERFORMED; exits 1 on any FAIL.
//
// Usage:
//   node tests/pecompat/run_tests.mjs [--models <Models.bnt>] [--tol 1e-4]
//        [--json-out <path>] [--artifact-out <path>] [--repo-root <path>]
//
// Without --models, the pinned-container tests report
// NOT_PERFORMED_CONTAINER_UNAVAILABLE LOUDLY (never silently skipped).
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { writeFile } from 'node:fs/promises';

const here = path.dirname(fileURLToPath(import.meta.url));

const args = process.argv.slice(2);
const ctx = {
  modelsPath: null,
  tol: 1e-4,
  jsonOut: null,
  artifactOutPath: null,
  repoRoot: path.resolve(here, '..', '..'),
};
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--models') ctx.modelsPath = args[++i];
  else if (args[i] === '--tol') ctx.tol = parseFloat(args[++i]);
  else if (args[i] === '--json-out') ctx.jsonOut = args[++i];
  else if (args[i] === '--artifact-out') ctx.artifactOutPath = args[++i];
  else if (args[i] === '--repo-root') ctx.repoRoot = args[++i];
}

const suites = [
  ['transform_composition.test.mjs', (await import('./transform_composition.test.mjs')).run],
  ['instance_separation.test.mjs', (await import('./instance_separation.test.mjs')).run],
  ['invalid_links.test.mjs', (await import('./invalid_links.test.mjs')).run],
  ['missing_texture.test.mjs', (await import('./missing_texture.test.mjs')).run],
  ['model_218757.test.mjs', (await import('./model_218757.test.mjs')).run],
  ['witness_457485_regression.test.mjs', (await import('./witness_457485_regression.test.mjs')).run],
];

const all = [];
let pass = 0, fail = 0, notPerformed = 0;
const t0 = Date.now();

console.log('== PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009 — tests/pecompat ==');
console.log(`run: node tests/pecompat/run_tests.mjs --models "${ctx.modelsPath ?? '(none — pinned-container tests will report NOT_PERFORMED)'}" --tol ${ctx.tol}`);

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
      console.log(`  MEASURED: ${JSON.stringify(r.measured ?? null, null, 2)}`);
      console.log(`  EXPECTED: ${JSON.stringify(r.expected ?? null, null, 2)}`);
    }
  }
}

const summary = {
  run: 'PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009',
  phase: 'IR_ADAPTER_UNIT_TESTS',
  harness: 'tests/pecompat/run_tests.mjs',
  ctx: { modelsPath: ctx.modelsPath, tol: ctx.tol, repoRoot: ctx.repoRoot },
  totals: { pass, fail, notPerformed, total: all.length },
  elapsedMs: Date.now() - t0,
  tests: all,
};

console.log(`\n== SUMMARY: ${pass} PASS / ${fail} FAIL / ${notPerformed} NOT_PERFORMED (total ${all.length}) ==`);
if (ctx.jsonOut) {
  await writeFile(ctx.jsonOut, JSON.stringify(summary, null, 1) + '\n', 'utf8');
  console.log(`machine summary -> ${ctx.jsonOut}`);
}
process.exit(fail > 0 ? 1 : 0);
