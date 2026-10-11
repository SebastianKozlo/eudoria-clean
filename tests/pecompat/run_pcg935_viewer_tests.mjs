#!/usr/bin/env node
// tests/pecompat/run_pcg935_viewer_tests.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010
// Test runner: executes the formal battery (fast gates) and optionally the
// long sweep with --sweep. Exit code 0 only when everything passes.
'use strict';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const doSweep = args.includes('--sweep');

// 1) the long sweep first if requested (gates 3/9/10)
if (doSweep) {
  console.log('[runner] running the long coverage sweep (gate 3/9/10)…');
  execFileSync(process.execPath, ['--expose-gc', path.resolve(HERE, '../../tools/pecompat/pcg935_sweep.mjs')], {
    cwd: path.resolve(HERE, '../..'), stdio: 'inherit', timeout: 40 * 60 * 1000,
  });
}

// 2) the formal battery
const r = execFileSync(process.execPath, [path.join(HERE, 'pcg935_viewer.test.mjs')], {
  cwd: path.resolve(HERE, '../..'), stdio: 'inherit', timeout: 30 * 60 * 1000,
});
process.exit(r === null ? 0 : 0);
