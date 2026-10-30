// test_adapter.mjs — Wave B2 (job J4) executed test suite.
// Parent RUN_ID: PE2003_ROSETTA_GAMEBRYO_BRIDGE_CORRECTIONS_R1_20261030
//
// The oracle below is INDEPENDENT of the adapter under test: the formulas are
// transcribed from transform_check.py (SHA256 68FEB748...4FF), the J2
// ground-truth oracle, into JS. The adapter's own applyIR/matrices are never
// used to compute expected values.
//
// Usage:  node test_adapter.mjs [--adapter=./niTransformAdapter.mjs]
// Run 1 (REQUIRED negative control): --adapter=./mutant_wrong_transpose.mjs
//         -> MUST exit non-zero with failing gates.
// Run 2 (correct): default adapter -> MUST exit 0 with all gates PASS.
//
// SPEC_DEVIATION (recorded, J2 gate camera_eye_to_origin): the J2 gate text
// demands view X == camera right (R col2 = (0.5, 0, 0.866025), the mirror
// fix) but its numeric expected x for the world point (-4.964102) was
// computed with the MIRRORED X (norm(U x F) == -col2, as in
// transform_check.py correct_view_matrix). With X == col2 the correct value
// is dot(w-eye, col2) = +4.964102. We follow the normative X == col2 rule
// (stated twice in adapter_spec.handedness and the gate) and assert
// +4.964102; the -4.964102 value is separately asserted as the MIRRORED
// result (negative control for the mirror bug).

import { pathToFileURL } from 'node:url';
import process from 'node:process';

const args = process.argv.slice(2);
let adapterPath = './niTransformAdapter.mjs';
for (const a of args) {
  const m = /^--adapter=(.+)$/.exec(a);
  if (m) adapterPath = m[1];
}

const A = await import(pathToFileURL(adapterPath).href);

// ===========================================================================
// INDEPENDENT ORACLE (from transform_check.py — no adapter imports)
// ===========================================================================
const EPS = 1e-6;
const EPS5 = 1e-5;

const vadd = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
const vscale = (a, s) => a.map((x) => x * s);
const vdot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const vcross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
const vnorm = (a) => { const l = Math.sqrt(vdot(a, a)); return a.map((x) => x / l); };
const matmul = (P, Q) => {
  const o = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) {
    o[i][j] = P[i][0] * Q[0][j] + P[i][1] * Q[1][j] + P[i][2] * Q[2][j];
  }
  return o;
};
const matvec = (M, v) => [
  M[0][0] * v[0] + M[0][1] * v[1] + M[0][2] * v[2],
  M[1][0] * v[0] + M[1][1] * v[1] + M[1][2] * v[2],
  M[2][0] * v[0] + M[2][1] * v[1] + M[2][2] * v[2],
];
const cosd = (d) => Math.cos((d * Math.PI) / 180);
const sind = (d) => Math.sin((d * Math.PI) / 180);
const rotX = (deg) => [[1, 0, 0], [0, cosd(deg), -sind(deg)], [0, sind(deg), cosd(deg)]];
const rotY = (deg) => [[cosd(deg), 0, sind(deg)], [0, 1, 0], [-sind(deg), 0, cosd(deg)]];
const rotZ = (deg) => [[cosd(deg), -sind(deg), 0], [sind(deg), cosd(deg), 0], [0, 0, 1]];

// ground truth: p' = R (s p) + t  (Ni row-dot)
const truthApply = (R, s, t, p) => vadd(matvec(R, vscale(p, s)), t);

// oracle compose (parent o child, child first) — from transform_check.py
const oracleCompose = (Ps, PR, Pt, Cs, CR, Ct) => ({
  s: Ps * Cs, R: matmul(PR, CR), t: vadd(matvec(PR, vscale(Ct, Ps)), Pt),
});

// oracle D3D row-vector device apply: v'_j = sum_i v_i M[i][j] + M[3][j]
const deviceApply = (M, p) => [
  p[0] * M[0][0] + p[1] * M[1][0] + p[2] * M[2][0] + M[3][0],
  p[0] * M[0][1] + p[1] * M[1][1] + p[2] * M[2][1] + M[3][1],
  p[0] * M[0][2] + p[1] * M[1][2] + p[2] * M[2][2] + M[3][2],
];

// oracle WRONG harness world layout (MatFromTransform): rows of R -> rows
const harnessWorldMatrix = (R, s, t) => {
  const M = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]];
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) M[i][j] = s * R[i][j];
  M[3] = [t[0], t[1], t[2], 1];
  return M;
};

// oracle camera basis — BOTH X variants, to pin the mirror bug
const oracleBasis = (R) => ({
  F: [R[0][0], R[1][0], R[2][0]],             // look = col0
  U: [R[0][1], R[1][1], R[2][1]],            // up   = col1
  right: [R[0][2], R[1][2], R[2][2]],         // camera right = col2 (engine kRight)
  harnessX: vnorm(vcross([R[0][1], R[1][1], R[2][1]], [R[0][0], R[1][0], R[2][0]])), // norm(U x F)
});

// oracle WRONG harness view (basis-in-ROWS, mirrored X) — negative control
const harnessViewMatrix = (R, e) => {
  const b = oracleBasis(R);
  const M = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]];
  M[0] = [b.harnessX[0], b.harnessX[1], b.harnessX[2], 0];
  const Y = vnorm(vcross(b.F, b.harnessX));
  M[1] = [Y[0], Y[1], Y[2], 0];
  M[2] = [b.F[0], b.F[1], b.F[2], 0];
  M[3] = [-vdot(b.harnessX, e), -vdot(Y, e), -vdot(b.F, e), 1];
  return M;
};

const close = (a, b, eps) => a.every((x, i) => Math.abs(x - b[i]) <= eps);
const maxdiff = (a, b) => Math.max(...a.map((x, i) => Math.abs(x - b[i])));
const r6 = (v) => v.map((x) => Math.round(x * 1e6) / 1e6);

// ===========================================================================
// harness
// ===========================================================================
const results = [];
let failures = 0;
async function gate(name, fn) {
  try {
    const detail = await fn(); // sync or async fns both fine
    if (detail === Symbol.for('SKIPPED')) return; // already recorded by fn
    results.push({ gate: name, status: 'PASS', detail });
    console.log(`GATE ${name}: PASS  ${detail ?? ''}`);
  } catch (e) {
    failures++;
    results.push({ gate: name, status: 'FAIL', error: String(e.message ?? e) });
    console.log(`GATE ${name}: FAIL  ${e.message ?? e}`);
  }
}
function expect(cond, msg) { if (!cond) throw new Error(msg); }

// adapter world pipeline under test: D3D device apply of adapter matrix
const d3dWorldApply = (ir, p) => A.d3dDeviceApply(A.niToD3DWorld(ir), p);
const threeWorldApply = (ir, p) => A.threeElementsApply(A.niToThreeWorld(ir).columnMajorElements, p);

// ---------------------------------------------------------------------------
// G1 identity
// ---------------------------------------------------------------------------
await gate('identity', () => {
  const p = [3.0, -4.0, 5.5];
  const id = A.makeIR({ scale: 1.0, rotate: [[1, 0, 0], [0, 1, 0], [0, 0, 1]], translate: [0, 0, 0] });
  const d = d3dWorldApply(id, p);
  const th = threeWorldApply(id, p);
  expect(close(d, p, EPS), `d3d path ${d} != ${p}`);
  expect(close(th, p, EPS), `three path ${th} != ${p}`);
  return `p=${p} -> d3d ${r6(d)} three ${r6(th)}`;
});

// ---------------------------------------------------------------------------
// G2 rotY90_scale1.5 — canonical wrong-transpose counterexample
// ---------------------------------------------------------------------------
await gate('rotY90_scale1.5', () => {
  const R = rotY(90), s = 1.5, t = [50, 0, 20], p = [1, 0, 0];
  const ir = A.makeIR({ scale: s, rotate: R, translate: t });
  const gt = truthApply(R, s, t, p); // (50, 0, 18.5)
  const d = d3dWorldApply(ir, p);
  const th = threeWorldApply(ir, p);
  expect(close(gt, [50, 0, 18.5], EPS), `oracle self-check failed: ${gt}`);
  expect(close(d, gt, EPS), `d3d ${d} != ground truth ${gt}`);
  expect(close(th, gt, EPS), `three ${th} != ground truth ${gt}`);
  // oracle wrong-transpose yields (50,0,21.5) — the value a mutant produces
  const wrong = deviceApply(harnessWorldMatrix(R, s, t), p);
  expect(close(wrong, [50, 0, 21.5], EPS), `oracle harness-layout self-check: ${wrong}`);
  return `p=(1,0,0) -> ${r6(d)} (wrong-transpose would give ${r6(wrong)})`;
});

// ---------------------------------------------------------------------------
// G3 non-commuting pair, BOTH orders
// ---------------------------------------------------------------------------
await gate('noncommuting_pair', () => {
  const p = [1, 2, 3];
  const Rz = rotZ(90), Rx = rotX(90);
  // order 1: A=Rz90/tA first, then B=Rx90/tB  (compose B o A)
  const BA = oracleCompose(1.0, Rx, [0, 2, 0], 1.0, Rz, [1, 0, 0]);
  const gt1 = truthApply(BA.R, BA.s, BA.t, p);
  expect(close(gt1, [-1, -1, 1], EPS), `oracle gt1 ${gt1}`);
  const ir1 = A.compose(A.makeIR({ scale: 1, rotate: Rx, translate: [0, 2, 0] }),
                        A.makeIR({ scale: 1, rotate: Rz, translate: [1, 0, 0] }));
  const d1 = d3dWorldApply(ir1, p);
  expect(close(d1, gt1, EPS), `d3d order1 ${d1} != ${gt1}`);
  const th1 = threeWorldApply(ir1, p);
  expect(close(th1, gt1, EPS), `three order1 ${th1} != ${gt1}`);
  // order 2: B first, then A (compose A o B) — MUST differ from order 1
  const AB = oracleCompose(1.0, Rz, [1, 0, 0], 1.0, Rx, [0, 2, 0]);
  const gt2 = truthApply(AB.R, AB.s, AB.t, p);
  expect(close(gt2, [2, 1, 2], EPS), `oracle gt2 ${gt2}`);
  expect(!close(gt1, gt2, EPS), `orders must be distinct: ${gt1} vs ${gt2}`);
  const ir2 = A.compose(A.makeIR({ scale: 1, rotate: Rz, translate: [1, 0, 0] }),
                        A.makeIR({ scale: 1, rotate: Rx, translate: [0, 2, 0] }));
  const d2 = d3dWorldApply(ir2, p);
  expect(close(d2, gt2, EPS), `d3d order2 ${d2} != ${gt2}`);
  const th2 = threeWorldApply(ir2, p);
  expect(close(th2, gt2, EPS), `three order2 ${th2} != ${gt2}`);
  return `AB=${r6(d2)} BA=${r6(d1)} (distinct, both == oracle ground truth)`;
});

// ---------------------------------------------------------------------------
// G4 parent+child composition vs step-by-step ground truth
// ---------------------------------------------------------------------------
await gate('parent_child_composition', () => {
  const P = { s: 2.0, R: rotY(90), t: [10, 0, -5] };
  const C = { s: 1.5, R: rotZ(90), t: [1, 2, 3] };
  const p = [0.5, -1.0, 2.0];
  const gtStep = truthApply(P.R, P.s, P.t, truthApply(C.R, C.s, C.t, p));
  const oc = oracleCompose(P.s, P.R, P.t, C.s, C.R, C.t);
  const gtOne = truthApply(oc.R, oc.s, oc.t, p);
  expect(close(gtStep, gtOne, 1e-9), `oracle compose consistency: ${gtStep} vs ${gtOne}`);
  expect(close(gtStep, [22.0, 5.5, -10.0], EPS5), `oracle ground truth ${gtStep}`);
  const Pir = A.makeIR({ scale: P.s, rotate: P.R, translate: P.t });
  const Cir = A.makeIR({ scale: C.s, rotate: C.R, translate: C.t });
  const composed = A.compose(Pir, Cir);
  // composed apply == step-by-step, both device paths, eps 1e-5 (scale 2*1.5)
  const d = d3dWorldApply(composed, p);
  const th = threeWorldApply(composed, p);
  expect(close(d, gtStep, EPS5), `d3d composed ${d} != step-by-step ${gtStep}`);
  expect(close(th, gtStep, EPS5), `three composed ${th} != step-by-step ${gtStep}`);
  // adapter compose fields == oracle compose fields (s=3.0, t=(16,4,-7) pinned)
  expect(Math.abs(composed.scale - 3.0) < EPS, `composed scale ${composed.scale} != 3.0`);
  expect(close(composed.translate, [16, 4, -7], EPS), `composed t ${composed.translate} != (16,4,-7)`);
  // adapter(P).apply(adapter(C).apply(p)) == same
  const step = d3dWorldApply(Pir, d3dWorldApply(Cir, p));
  expect(close(step, gtStep, EPS5), `adapter step-by-step ${step} != ${gtStep}`);
  return `composed=${r6(d)} == step-by-step=${r6(gtStep)} (s=3.0, t=(16,4,-7))`;
});

// ---------------------------------------------------------------------------
// G5 camera eye -> view origin (+ mirror fix + wrong-transpose view control)
// ---------------------------------------------------------------------------
await gate('camera_eye_to_origin', () => {
  const camR = matmul(rotY(30), rotZ(20));
  const eye = [10.0, 5.0, -3.0];
  const cam = A.makeIR({ scale: 1.0, rotate: camR, translate: eye });
  const b = oracleBasis(camR);
  // mirror-fix self-checks (oracle): harness X == -right(col2)
  expect(close(b.harnessX, vscale(b.right, -1), 1e-9),
    `oracle: norm(U x F) must equal -col2: ${b.harnessX} vs ${vscale(b.right, -1)}`);
  expect(close(b.right, [0.5, 0.0, 0.866025], 1e-6), `oracle right(col2) ${b.right}`);
  // adapter X must be the camera's OWN right (col2), NOT U x F
  const ab = A.cameraBasis(cam);
  expect(close(ab.X, b.right, 1e-9), `adapter view X ${ab.X} != camera right(col2) ${b.right}`);
  expect(!close(ab.X, b.harnessX, 1e-9), `adapter view X must NOT be norm(U x F)`);
  // convention parameter required
  let threw = false;
  try { A.cameraViewD3D(cam, {}); } catch (e) { threw = /convention/i.test(e.message); }
  expect(threw, 'cameraViewD3D without convention must throw MissingConventionError');
  threw = false;
  try { A.cameraViewThree(cam, {}); } catch (e) { threw = /convention/i.test(e.message); }
  expect(threw, 'cameraViewThree without convention must throw MissingConventionError');
  // D3D view: eye -> origin exactly
  const V = A.cameraViewD3D(cam, { convention: 'd3d-lh' });
  const vEye = deviceApply(V, eye);
  expect(close(vEye, [0, 0, 0], EPS), `d3d view(eye) ${vEye} != origin`);
  // world point w: (dot(w-e,X), dot(w-e,Y), dot(w-e,F)) with X = col2
  // SPEC_DEVIATION: J2 numeric x=-4.964102 used the mirrored X; with X=col2
  // the correct x is +4.964102 (see file header).
  const w = [13.0, 2.0, 1.0];
  const vW = deviceApply(V, w);
  const expectX = vdot(vadd(w, vscale(eye, -1)), b.right);   // +4.964102
  const expectY = vdot(vadd(w, vscale(eye, -1)), b.U);       // -3.023632
  const expectF = vdot(vadd(w, vscale(eye, -1)), b.F);       // -0.464053
  expect(Math.abs(expectX - 4.964102) < 1e-5, `oracle expectX ${expectX}`);
  expect(Math.abs(expectY - (-3.023632)) < 1e-5, `oracle expectY ${expectY}`);
  expect(Math.abs(expectF - (-0.464053)) < 1e-5, `oracle expectF ${expectF}`);
  expect(close(vW, [expectX, expectY, expectF], EPS), `d3d view(w) ${vW} != (${expectX},${expectY},${expectF})`);
  // mirrored X would give -4.964102 — the mirror bug, separately caught
  const mirroredX = vdot(vadd(w, vscale(eye, -1)), b.harnessX);
  expect(Math.abs(mirroredX - (-4.964102)) < 1e-5 && !close([mirroredX], [expectX], 1e-3),
    'mirror negative control: U x F basis must give -4.964102 != adapter x');
  // harness wrong-transpose view FAILS to map eye to origin (|v| ~ 18.98)
  const HV = harnessViewMatrix(camR, eye);
  const hvEye = deviceApply(HV, eye);
  expect(!close(hvEye, [0, 0, 0], EPS), 'harness wrong-transpose view must NOT map eye to origin');
  const hvNorm = Math.hypot(...hvEye);
  expect(hvNorm > 1.0, `harness wrong-transpose |view(eye)| = ${hvNorm} must be > 1`);
  expect(Math.abs(hvNorm - 18.977673634) < 1e-4, `harness |view(eye)| ${hvNorm} != 18.977674 (J2 pin)`);
  // Three.js RH view: eye -> origin; z = -F.(w-e) (+0.464053); explicit reorientation
  const VT = A.cameraViewThree(cam, { convention: 'three-rh' });
  const tEye = A.threeElementsApply(VT.columnMajorElements, eye);
  expect(close(tEye, [0, 0, 0], EPS), `three view(eye) ${tEye} != origin`);
  const tW = A.threeElementsApply(VT.columnMajorElements, w);
  expect(close(tW, [expectX, expectY, -expectF], EPS),
    `three view(w) ${tW} != (${expectX},${expectY},${-expectF})`);
  expect(VT.reorientation.declared === true &&
    JSON.stringify([...VT.reorientation.matrix]) === JSON.stringify([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1]),
    'three view must declare explicit diag(1,1,-1) LH->RH reorientation');
  return `eye->(0,0,0) both conventions; w->(${r6(vW)}) d3d / z=${r6(tW)[2]} three; ` +
    `harness mutant |view(eye)|=${hvNorm.toFixed(6)} (FAILS, as required)`;
});

// ---------------------------------------------------------------------------
// G6 NaN/Inf rejection — 13 singly-poisoned sites x {NaN, +Inf, -Inf}
// ---------------------------------------------------------------------------
await gate('nan_inf_rejection', () => {
  const good = { scale: 1.5, rotate: [[0, 0, 1], [0, 1, 0], [-1, 0, 0]], translate: [50, 0, 20] };
  const poisons = [NaN, Infinity, -Infinity];
  let rejections = 0, misses = [];
  const sites = [
    ['scale', (v) => ({ ...good, scale: v })],
    ...[0, 1, 2].flatMap((i) => [0, 1, 2].map((j) =>
      [`rotate[${i}][${j}]`, (v) => {
        const R = good.rotate.map((r) => [...r]); R[i][j] = v; return { ...good, rotate: R };
      }])),
    ...[0, 1, 2].map((i) => [`translate[${i}]`, (v) => {
      const t = [...good.translate]; t[i] = v; return { ...good, translate: t };
    }]),
  ];
  expect(sites.length === 13, `expected 13 poison sites, got ${sites.length}`);
  for (const [site, mut] of sites) {
    for (const poison of poisons) {
      let rejected = false;
      try { A.makeIR(mut(poison)); } catch (e) { rejected = e instanceof Error; }
      if (rejected) rejections++; else misses.push(`${site}=${poison}`);
      // matrix builders must also reject raw (non-IR) poisoned objects
      let rejectedD3 = false, rejectedTh = false;
      try { A.niToD3DWorld(mut(poison)); } catch { rejectedD3 = true; }
      try { A.niToThreeWorld(mut(poison)); } catch { rejectedTh = true; }
      if (!rejectedD3) misses.push(`niToD3DWorld accepted ${site}=${poison}`);
      if (!rejectedTh) misses.push(`niToThreeWorld accepted ${site}=${poison}`);
    }
  }
  expect(misses.length === 0, `non-rejected poisons: ${misses.join('; ')}`);
  return `${rejections}/39 makeIR rejections + 39/39 builder rejections across 13 sites x 3 poisons`;
});

// ---------------------------------------------------------------------------
// G7 wrong-transpose mutation must fail (embedded oracle control; the real
// mutant run is a SEPARATE execution with --adapter=./mutant_wrong_transpose.mjs)
// ---------------------------------------------------------------------------
await gate('wrong_transpose_mutation_must_fail', () => {
  const R = rotY(90), s = 1.5, t = [50, 0, 20], p = [1, 0, 0];
  const gt = truthApply(R, s, t, p); // (50,0,18.5)
  const wrong = deviceApply(harnessWorldMatrix(R, s, t), p); // (50,0,21.5)
  const dev = maxdiff(wrong, gt);
  expect(dev > 1.0, `harness-layout deviation ${dev} must be > 1.0`);
  // same check via the noncommuting pair on p=(1,2,3), composed BA from G3
  const BA = oracleCompose(1.0, rotX(90), [0, 2, 0], 1.0, rotZ(90), [1, 0, 0]);
  const gt1 = truthApply(BA.R, BA.s, BA.t, [1, 2, 3]); // (-1,-1,1)
  const wrong1 = deviceApply(harnessWorldMatrix(BA.R, BA.s, BA.t), [1, 2, 3]);
  expect(maxdiff(wrong1, gt1) > 1.0, `harness-layout noncomm deviation must be > 1.0`);
  return `harness layout: Y90 dev=${dev} (assert >1.0), noncomm dev=${maxdiff(wrong1, gt1)} — ` +
    `separate mutant execution MUST exit non-zero`;
});

// ---------------------------------------------------------------------------
// G8 three engine math cross-check (executed if three@0.185.0 importable;
// NOT a rendering/runtime engine claim — math classes only)
// ---------------------------------------------------------------------------
await gate('three_engine_math_crosscheck', async () => {
  let THREE;
  try {
    // Portable resolution (J6 fix): no hardcoded absolute private paths.
    // 1) bare specifier — resolves via the repo checkout's own node_modules
    try {
      THREE = await import('three');
    } catch {
      // 2) walk up from THIS module's own location to find node_modules/three
      const { fileURLToPath } = await import('node:url');
      const { dirname, join } = await import('node:path');
      const { existsSync } = await import('node:fs');
      let dir = dirname(fileURLToPath(import.meta.url));
      for (;;) {
        const cand = join(dir, 'node_modules', 'three', 'build', 'three.module.js');
        if (existsSync(cand)) { THREE = await import(pathToFileURL(cand).href); break; }
        const parent = dirname(dir);
        if (parent === dir) break; // reached filesystem root
        dir = parent;
      }
    }
    if (!THREE) {
      // honest degrade: skip with explicit label, never a fabricated pass
      throw new Error('THREE_MATH_CROSSCHECK_SKIPPED_NO_PACKAGE: three is not ' +
        'resolvable from this checkout (no node_modules/three on this module\'s ancestor chain)');
    }
  } catch (e) {
    results.push({ gate: 'three_engine_math_crosscheck', status: 'SKIPPED', reason: String(e.message ?? e) });
    console.log(`GATE three_engine_math_crosscheck: SKIPPED (${e.message ?? e}) — ` +
      `documented public layout already covered by G1-G5`);
    return Symbol.for('SKIPPED');
  }
  const R = rotY(90), s = 1.5, t = [50, 0, 20], p = [1, 0, 0];
  const gt = truthApply(R, s, t, p);
  const ir = A.makeIR({ scale: s, rotate: R, translate: t });
  const rep = A.niToThreeWorld(ir);
  // path 1: Matrix4.set(...setArguments) + Vector3.applyMatrix4
  const M1 = new THREE.Matrix4().set(...rep.setArguments);
  const out1 = new THREE.Vector3(...p).applyMatrix4(M1);
  // path 2: Matrix4.fromArray(columnMajorElements) + applyMatrix4
  const M2 = new THREE.Matrix4().fromArray([...rep.columnMajorElements]);
  const out2 = new THREE.Vector3(...p).applyMatrix4(M2);
  expect(close([out1.x, out1.y, out1.z], gt, EPS), `THREE.set path (${out1.x},${out1.y},${out1.z}) != ${gt}`);
  expect(close([out2.x, out2.y, out2.z], gt, EPS), `THREE.fromArray path != ${gt}`);
  // Matrix4.compose semantics cross-check (position/quaternion/scale).
  // NOTE: Quaternion.setFromRotationMatrix requires a full Matrix4 (it reads
  // te[0], te[4], te[8], te[12]...), so build the rotation as a Matrix4.
  const q = new THREE.Quaternion().setFromRotationMatrix(
    new THREE.Matrix4().set(R[0][0], R[0][1], R[0][2], 0,
                            R[1][0], R[1][1], R[1][2], 0,
                            R[2][0], R[2][1], R[2][2], 0,
                            0, 0, 0, 1));
  const M3 = new THREE.Matrix4().compose(new THREE.Vector3(...t), q, new THREE.Vector3(s, s, s));
  const out3 = new THREE.Vector3(...p).applyMatrix4(M3);
  expect(close([out3.x, out3.y, out3.z], gt, EPS5), `THREE.compose path != ${gt}`);
  // three view matrix: eye -> origin, RH -Z forward
  const camR = matmul(rotY(30), rotZ(20));
  const eye = [10.0, 5.0, -3.0];
  const cam = A.makeIR({ scale: 1.0, rotate: camR, translate: eye });
  const VT = A.cameraViewThree(cam, { convention: 'three-rh' });
  const MV = new THREE.Matrix4().fromArray([...VT.columnMajorElements]);
  const cv = new THREE.Vector3(...eye).applyMatrix4(MV);
  expect(close([cv.x, cv.y, cv.z], [0, 0, 0], EPS), `THREE view(eye) (${cv.x},${cv.y},${cv.z}) != origin`);
  const wv = new THREE.Vector3(13, 2, 1).applyMatrix4(MV);
  const b = oracleBasis(camR);
  expect(close([wv.x, wv.y, wv.z],
    [vdot(vadd([13, 2, 1], vscale(eye, -1)), b.right),
     vdot(vadd([13, 2, 1], vscale(eye, -1)), b.U),
     -vdot(vadd([13, 2, 1], vscale(eye, -1)), b.F)], EPS),
    `THREE view(w) (${wv.x},${wv.y},${wv.z}) != oracle`);
  return `three@${THREE.REVISION ?? '0.185.0'} math classes: set/fromArray/compose paths + view all match oracle (executed math cross-check, not runtime proof)`;
});

// ---------------------------------------------------------------------------
// summary + exit code
// ---------------------------------------------------------------------------
console.log('--- GATE MATRIX ---');
for (const r of results) {
  console.log(`${r.status === 'PASS' ? '[PASS]' : `[${r.status}]`} ${r.gate}`);
}
const skipped = results.filter((r) => r.status === 'SKIPPED').length;
if (failures === 0) {
  console.log(`ALL_GATES_PASS (${results.length - skipped} pass, ${skipped} skipped, 0 fail) ` +
    `adapter=${adapterPath}`);
  process.exit(0);
} else {
  console.log(`SUITE_FAIL: ${failures} gate(s) failed, adapter=${adapterPath}`);
  process.exit(1);
}
