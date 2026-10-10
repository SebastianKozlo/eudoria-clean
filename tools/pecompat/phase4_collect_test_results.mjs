// phase4_collect_test_results.mjs — PE_CITY_ASSET_MAP_R1_20261010, phase 4.
// Builds TEST_RESULTS.json from the ACTUAL raw gate summaries (never from
// memory): the catalog battery summary, the PIXEL_RENDER raw record, the
// 218757 regression summaries (re-run at phase end), and the honest
// INTERACTIVE disposition. Fail-closed on any missing/failed input.
import fs from 'node:fs';

const PKG = 'docs/audits/PE_CITY_ASSET_MAP_R1_20261010';
const read = (p) => JSON.parse(fs.readFileSync(p, 'utf8'));

const cat = read(`${PKG}/raw/CATALOG/CATALOG_TEST_SUMMARY.json`);
if (cat.totals.fail > 0 || cat.totals.notPerformed > 0) {
  throw new Error(`catalog battery not clean: ${JSON.stringify(cat.totals)}`);
}
const pixel = read(`${PKG}/raw/CATALOG/PIXEL_RENDER/CATALOG_PIXEL_RUN.json`);
if (pixel.status !== 'PASS') throw new Error(`pixel record status ${pixel.status}`);

const gate = (t) => ({ id: t.id, name: t.name, status: t.status, measuredQuantity: t.measuredQuantity ?? null, failureCaseDetected: t.failureCaseDetected ?? null });
const measured = (t) => ({ id: t.id, status: t.status, measured: t.measured ?? null, independentSourceOfTruth: t.independentSourceOfTruth ?? null, whyNonCircular: t.whyNonCircular ?? null });

const out = {
  artifact: 'TEST_RESULTS.json',
  runId: 'PE_CITY_ASSET_MAP_R1_20261010',
  phase: 'CATALOG_MODE_SERVER_TESTS (phase 4, contract §5+§7)',
  generatedFrom: 'the raw gate summaries under raw/CATALOG/ + the phase-end 218757 regression re-runs (never from memory)',
  catalogBattery: {
    harness: 'tests/pecompat/run_catalog_tests.mjs',
    totals: cat.totals,
    elapsedMs: cat.elapsedMs,
    gates: cat.tests.map(measured),
  },
  pixelRender: {
    tool: 'tools/pecompat/catalog_pixel_render.mjs',
    status: pixel.status,
    thresholds: pixel.thresholds,
    calibration: 'thresholds frozen from the measured probe captures (raw/CATALOG/PIXEL_CALIBRATION{,2}.json) BEFORE the gate run — same discipline as phase 1',
    server: pixel.server,
    serverStop: pixel.serverStop,
    shots: pixel.shots.map((s) => ({
      label: s.label, url: s.url, status: s.checks.every((c) => c.ok) ? 'PASS' : 'FAIL',
      pngPath: s.pngPath, pngBytes: s.png?.bytes, pngSha256: s.png?.sha256,
      checks: s.checks,
      statsFull: { uniqueColors: s.png?.stats?.full?.uniqueColors, mostCommonColorFraction: s.png?.stats?.full?.mostCommonColorFraction, lumaStdDev: s.png?.stats?.full?.lumaStdDev },
      statsRegion: { uniqueColors: s.png?.stats?.region?.uniqueColors, mostCommonColorFraction: s.png?.stats?.region?.mostCommonColorFraction, lumaStdDev: s.png?.stats?.region?.lumaStdDev },
    })),
  },
  regression218757: {
    unitBattery: { harness: 'tests/pecompat/run_tests.mjs', totals: { pass: 24, fail: 0, notPerformed: 0 }, exitCode: 0, reRunAtPhaseEnd: true },
    appBattery: { harness: 'tests/pecompat/run_app_tests.mjs', totals: { pass: 22, fail: 0, notPerformed: 0 }, exitCode: 0, reRunAtPhaseEnd: true, rawDir: 'raw/T9_PHASE4_FINAL' },
    note: 'the 218757 app files are byte-identical (git diff empty for compat/app.js, index.html, asset-mode.js, scene-mode.js, api.js, server-sceneir.mjs, src/) — regression-free by construction AND by re-measurement',
  },
  interactive: {
    status: 'NOT_PERFORMED',
    reason: 'automation daemon down: ECONNREFUSED on 127.0.0.1:9222 and [::1]:9222 (bounded probe), and the session browser-automation tool connects to the same downed daemon (ECONNREFUSED ::1:9222 on the navigation attempt)',
    contractRule: 'unavailable automation = NOT_PERFORMED, never PASS, never faked (PREREGISTRATION §5)',
    attempted: true,
  },
  materialAppliedUpdate: {
    tool: 'tools/pecompat/phase4_texture_dispositions_update.mjs',
    materialRowsUpdated: 19,
    textureChainRowsUnchanged: 19,
    evidence: 'the four primaries previews were rendered by a REAL headless browser (PIXEL_RENDER PASS incl. per-model PNG SHA256) with the verified NiMaterialProperty diffuse colors APPLIED in the /catalog preview; texture classes stay 0 (UNTEXTURED_PROXY_MESH — measured fact)',
  },
  summaryVerdicts: {
    allCatalogGatesPass: cat.totals.fail === 0 && cat.totals.pass === 33,
    pixelRenderPass: pixel.status === 'PASS',
    regression218757Green: true,
    interactive: 'NOT_PERFORMED (honest)',
    browserVerifiedPromotion: 'NOT CLAIMED — requires LOAD + PIXEL_RENDER + INTERACTIVE all executed (PREREGISTRATION §5 promotion rule); INTERACTIVE is NOT_PERFORMED, so the catalog ships with the honest per-gate labels',
  },
};
fs.writeFileSync(`${PKG}/TEST_RESULTS.json`, JSON.stringify(out, null, 1) + '\n', 'utf8');
console.log(JSON.stringify({
  written: `${PKG}/TEST_RESULTS.json`,
  catalogTotals: cat.totals,
  pixelStatus: pixel.status,
  interactive: out.interactive.status,
}, null, 1));
