#!/usr/bin/env node
// controlB_compare.mjs — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// Control B comparison runner: fixture NIF -> independent IR reader ->
// composed camera world translate vs the NATIVE expected value (captured by
// the original GB 1.2 SceneGraphPrinter in the phase-1 controls; see
// docs/audits/.../CONTROLS_B.json). Tolerance-based FULL-VECTOR comparison —
// never rendered similarity.
//
// Usage: node tools/pecompat/controlB_compare.mjs <fixture.nif> <x,y,z> [--tol 1e-4]
import { readFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { readNif10 } from '../../src/pecompat/PecNif10Reader.js';
import { buildAssetIR, composeWorldTransforms } from '../../src/pecompat/PecSceneIR.js';

const args = process.argv.slice(2);
const fixture = args[0];
const expectedVec = args[1];
let tol = 1e-4;
{
  const i = args.indexOf('--tol');
  if (i >= 0) tol = parseFloat(args[i + 1]);
}
if (!fixture || !expectedVec) {
  console.error('usage: node tools/pecompat/controlB_compare.mjs <fixture.nif> <x,y,z> [--tol 1e-4]');
  process.exit(2);
}
const expected = expectedVec.split(',').map((v) => parseFloat(v.trim()));
if (expected.length !== 3 || expected.some((v) => !Number.isFinite(v))) {
  console.error('expected vector must be x,y,z');
  process.exit(2);
}

const sha256 = (b) => createHash('sha256').update(b).digest('hex');

try {
  const bytes = new Uint8Array(await readFile(fixture));
  const r = readNif10(bytes, { sourceName: fixture.split(/[\\/]/).pop() });
  const ir = buildAssetIR(r, {
    assetId: 'CONTROL_B_FIXTURE',
    era: 'SYNTHETIC_CONTROL',
    build: 'GB_1_2_SOURCE_QUALIFIED_FIXTURE',
    container: 'synthetic-controlB',
    entryName: fixture,
    payloadSha256: sha256(bytes),
    sizeBytes: bytes.byteLength,
    adapterVersion: 'controlB-compare-v1',
  });
  const world = composeWorldTransforms(ir);
  const cam = r.blocks.find((b) => b.type === 'NiCamera');
  if (!cam) {
    console.log(JSON.stringify({ verdict: 'FAIL', error: 'no NiCamera probe block in fixture' }, null, 2));
    process.exit(1);
  }
  const w = world.get(cam.index);
  const diffs = w.translate.map((v, i) => Math.abs(v - expected[i]));
  const maxDiff = Math.max(...diffs);
  const out = {
    tool: 'tools/pecompat/controlB_compare.mjs',
    fixture,
    fixtureSha256: sha256(bytes),
    cameraBlock: cam.index,
    cameraName: cam.name,
    measuredQuantity: 'composed camera world translate (FILE_SCENE_SPACE; parentWorld*local to the file root)',
    independentSourceOfTruth: 'native GB 1.2 SceneGraphPrinter world bound center (phase-1 CONTROLS_B.json)',
    measured: w.translate,
    expected,
    perComponentDiff: diffs,
    tolerance: tol,
    maxDiff,
    verdict: maxDiff <= tol ? 'PASS' : 'FAIL',
  };
  console.log(JSON.stringify(out, null, 2));
  process.exit(out.verdict === 'PASS' ? 0 : 1);
} catch (e) {
  console.log(JSON.stringify({ verdict: 'FAIL', error: String(e && e.message ? e.message : e) }, null, 2));
  process.exit(1);
}
