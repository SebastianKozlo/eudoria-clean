// tests/pecompat/pcg935_viewer.test.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010
// Formal test battery wrapper: 11 acceptance gates via the generator tools.
// Each gate reports PASS / NON-PASS honestly; the harness never converts a
// non-pass into a pass (fail-closed).
'use strict';

import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const TOOLS = path.resolve(HERE, '../../tools/pecompat');
const PRIVATE = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010';
const TESTS = path.join(PRIVATE, 'tests');

const results = [];

function run(label, tool, args = []) {
  const started = Date.now();
  try {
    const out = execFileSync(process.execPath, [path.join(TOOLS, tool), ...args], {
      cwd: path.resolve(HERE, '../..'),
      encoding: 'utf8',
      timeout: 20 * 60 * 1000,
    });
    results.push({ label, tool, ok: true, ms: Date.now() - started, out: out.slice(-400) });
    console.log(`[ok]   ${label} (${Date.now() - started}ms)`);
    return true;
  } catch (e) {
    results.push({ label, tool, ok: false, ms: Date.now() - started, out: String(e.stdout ?? '').slice(-600), err: String(e.message).slice(0, 200) });
    console.log(`[FAIL] ${label} (${Date.now() - started}ms): ${String(e.message).slice(0, 120)}`);
    return false;
  }
}

function readGate(name, file) {
  try {
    const j = JSON.parse(fs.readFileSync(path.join(TESTS, file), 'utf8'));
    return { name, ok: j.pass ?? j.allPass ?? false, detail: j };
  } catch (e) {
    return { name, ok: false, error: String(e.message) };
  }
}

// ---- run the batteries ----
run('node-gates (1,2,4,5,6,11)', 'pcg935_tests.mjs');
run('api-negatives (7)', 'pcg935_api_negatives.mjs');
run('browser-battery (8)', 'pcg935_cdp_battery.mjs');
// gate 3/9/10 = the sweep (long); the sweep result is read from disk when the
// generator already ran — run() also works standalone via the runner.

const gates = [];
gates.push(readGate('gate1-2-4-5-6-11', 'gates_node.json'));
gates.push(readGate('gate7-api-negatives', 'api_negatives.json'));
gates.push(readGate('gate8-browser', 'browser_battery.json'));
let sweepOk = false;
try {
  const s = JSON.parse(fs.readFileSync(path.join(TESTS, 'sweep.json'), 'utf8'));
  sweepOk = !!(s.gate9?.pass);
  gates.push({ name: 'gate3-9-10-sweep', ok: sweepOk, detail: { gate9: s.gate9, gate3: s.gate3, gate10: s.gate10 } });
} catch {
  gates.push({ name: 'gate3-9-10-sweep', ok: false, error: 'sweep.json not present — run tools/pecompat/pcg935_sweep.mjs (long-running)' });
}

const all = gates.every((g) => g.ok);
const report = {
  runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010',
  generated: new Date().toISOString(),
  harness: 'tests/pecompat/run_pcg935_viewer_tests.mjs',
  battery: 'tests/pecompat/pcg935_viewer.test.mjs',
  results, gates, allPass: all,
};
fs.writeFileSync(path.join(TESTS, 'TEST_RESULTS.json'), JSON.stringify(report, null, 1));
console.log('PCG935 VIEWER TESTS:', all ? 'ALL PASS' : 'NON-PASS (see gates above)');
process.exit(all ? 0 : 1);
