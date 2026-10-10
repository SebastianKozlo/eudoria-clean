#!/usr/bin/env node
// world_r2_collect_test_results.mjs — gathers ALL battery summaries + the
// browser/countercheck artifacts into the package TEST_RESULTS.json.
import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).href.replace(/^file:\/\/\//, '')), '..', '..');
const PKG = path.join(ROOT, 'docs/audits/PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010');
const read = async (p) => JSON.parse(await readFile(path.join(PKG, p), 'utf8'));

const world = await read('raw/WORLD/WORLD_TESTS_SUMMARY_R2.json');
const unit = await read('raw/UNIT/UNIT_TESTS_SUMMARY_R2.json');
const app = await read('raw/APP/APP_TESTS_SUMMARY_R2.json');
const catalog = await read('raw/CATALOG/CATALOG_TESTS_SUMMARY_R2.json');
const pre = await read('PRE_COUNTERCHECKS.json');
const post = await read('POST_COUNTERCHECKS.json');
const browser = await read('raw/BROWSER/INTERACTION_SCENARIOS.json');
const pixels = await read('raw/BROWSER/PIXEL_DIFFS.json');
const perf = JSON.parse(await readFile(path.join(PKG, 'raw/PERFORMANCE_MEASURED.json'), 'utf8'));

const allTotals = [world, unit, app, catalog].reduce((a, b) => ({
  pass: a.pass + b.totals.pass, fail: a.fail + b.totals.fail,
  notPerformed: a.notPerformed + b.totals.notPerformed, total: a.total + b.totals.total,
}), { pass: 0, fail: 0, notPerformed: 0, total: 0 });

const out = {
  run: 'PE_WORLD_CONTINUOUS_ROSETTA_R2_20261010',
  collectedAt: new Date().toISOString(),
  batteries: {
    world: { harness: 'node tests/pecompat/run_world_tests.mjs', totals: world.totals, suites: [...new Set(world.tests.map((t) => t.suite))] },
    unit: { harness: 'node tests/pecompat/run_tests.mjs --models <pinned Models.bnt>', totals: unit.totals },
    app: { harness: 'node tests/pecompat/run_app_tests.mjs --models <pinned Models.bnt>', totals: app.totals },
    catalog: { harness: 'node tests/pecompat/run_catalog_tests.mjs --models ... --models-ark ... --textures-bnt ...', totals: catalog.totals },
  },
  totalsAcrossBatteries: allTotals,
  counterchecks: {
    pre: { findings: Object.keys(pre.findings), summary: 'all WL-1..WL-5 REPRODUCED on the BASE production functions (see PRE_COUNTERCHECKS.json)' },
    post: {
      WL_1_latestRequest: post.findings.WL_1,
      WL_2_height: { instances: post.findings.WL_2.instances, sharedQueryNullNoSurface: post.findings.WL_2.sharedQueryNullNoSurface, maxDifferenceVsRenderedTriangle: post.findings.WL_2.maxDifferenceVsRenderedTriangle, y0FallbackInProductionApply: post.findings.WL_2.y0FallbackInProductionApply },
      WL_3_movement: post.findings.WL_3,
      WL_4_fit: post.findings.WL_4.steps ? { steps: post.findings.WL_4.steps.length, stable: post.findings.WL_4.focusStable } : post.findings.WL_4,
      WL_5_selection: { capSelection: post.findings.WL_5.capSelection, coincidentGroups: post.findings.WL_5.coincidentRecords.duplicateGroups, density: post.findings.WL_5.densityRounding },
      WL_6_records: 'LITERAL_ORIGINAL_BASE_GATE_COMPLIANCE=FAIL preserved; see R1_RECORD_SUPERSESSION.md',
    },
  },
  browserInteraction: {
    pageErrors: browser.pageErrors.length,
    scenarios: browser.scenarios.map((s) => ({ scenario: s.scenario, ready: s.ready, canvas85x80: s.canvas85x80, stable: s.stable, noJump: s.noJump, moved: s.moved, yOnSharedSurface: s.yOnSharedSurface, windowFollowed: s.windowFollowed, sameConfigSameCounts: s.sameConfigSameCounts, drawerKeyCapture: s.pass, resizeOk: s.cameraUnchanged && s.bufferFollows })),
    pixelDiffs: { vegToggle: pixels.diffs.vegToggle, textureToggle: pixels.diffs.textureToggle, teleportFarVsHome: pixels.diffs.teleportFarVsHome },
  },
  performance: { verdict: perf.verdict, checks: perf.checks, budgets: perf.budgetsSetBefore, heap: perf.heap, routeTimings: perf.routeTimings },
};
await writeFile(path.join(PKG, 'TEST_RESULTS.json'), JSON.stringify(out, null, 1) + '\n');
console.log(JSON.stringify({ totalsAcrossBatteries: allTotals, perf: perf.verdict }, null, 1));
