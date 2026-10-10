// PecTransform.js — PE_935_SCENEIR_MODEL_218757_BROWSER_R1_20261009
// The GB-contract transform math for the PE compatibility layer (src/pecompat).
//
// ENGINE CONTRACT IMPLEMENTED (architectural reference, re-implemented
// independently; NO SDK source is copied — see the run's SOURCE_IDENTITIES.json):
//   NiTransform.inl (Gb12_Source CoreLibs NiMain, SHA 92e8acf6...):
//     operator*(NiTransform):   res.scale    = m_fScale * xform.m_fScale
//                               res.rotate   = m_Rotate * xform.m_Rotate
//                               res.translate= m_Translate + m_fScale * (m_Rotate * xform.m_Translate)
//     operator*(NiPoint3):     (m_Rotate * kPoint) * m_fScale + m_Translate
//   NiAVObject_Win32.cpp (SHA 75e45268...): world = parentWorld * local; root
//     world == local when no parent.
//
// REUSE LABEL: the TRS representation (translation vec3 + row-major 3x3 rotate
// + scalar scale, with p' = (R*p)*s + t) follows the documented NIF/NiTransform
// convention used by the base repo's src/pesource/NifModelReader.js (the R61
// lineage). src/pesource/NifModelReader.js itself is NOT imported and NOT
// modified (457485 single-witness reader, stays untouched — witness regression
// preserved; see tests/pecompat/witness_457485_regression.test.mjs).
//
// This module is PURE: no THREE import, no I/O — Node-testable and
// browser-usable. NEVER flatten by summing positions: composition goes through
// the full rotate/scale/translate law above.

export const PEC_TRANSFORM_VERSION = 'pec-transform-v1';

// ---- 3x3 row-major rotation helpers (rows are basis images: p' = R*p) ----

export function identityMat3() {
  return [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
  ];
}

export function mulMat3(a, b) {
  const out = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      let s = 0;
      for (let k = 0; k < 3; k++) s += a[i][k] * b[k][j];
      out[i][j] = s;
    }
  }
  return out;
}

export function matVec3(m, v) {
  return [
    m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
    m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
    m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2],
  ];
}

// ---- TRS (translation, rotation, uniform scale) ----
// Shape: { translate: [x,y,z], rotate: [[r00..r02],[r10..r12],[r20..r22]] (row-major), scale: number }

export function identityTrs() {
  return { translate: [0, 0, 0], rotate: identityMat3(), scale: 1 };
}

export function isIdentityTrs(trs) {
  return (
    trs.translate[0] === 0 && trs.translate[1] === 0 && trs.translate[2] === 0 &&
    trs.scale === 1 &&
    trs.rotate[0][0] === 1 && trs.rotate[0][1] === 0 && trs.rotate[0][2] === 0 &&
    trs.rotate[1][0] === 0 && trs.rotate[1][1] === 1 && trs.rotate[1][2] === 0 &&
    trs.rotate[2][0] === 0 && trs.rotate[2][1] === 0 && trs.rotate[2][2] === 1
  );
}

export function makeTrs(translate, rotate, scale) {
  return {
    translate: [translate[0], translate[1], translate[2]],
    rotate: [
      [rotate[0][0], rotate[0][1], rotate[0][2]],
      [rotate[1][0], rotate[1][1], rotate[1][2]],
      [rotate[2][0], rotate[2][1], rotate[2][2]],
    ],
    scale,
  };
}

export function makeTranslationTrs(t) {
  return makeTrs(t, identityMat3(), 1);
}

export function makeScaleTrs(s) {
  return makeTrs([0, 0, 0], identityMat3(), s);
}

/** Rotation about +Z by `radians` (right-handed, p' = Rz*p).
 * Used by tests to mirror the source-qualified synthetic fixtures
 * (Rz90 maps (x,y,z) -> (-y,x,z)). */
export function makeRotationZTrs(radians) {
  const c = Math.cos(radians);
  const s = Math.sin(radians);
  return makeTrs([0, 0, 0], [[c, -s, 0], [s, c, 0], [0, 0, 1]], 1);
}

/**
 * composeTrs — THE GB contract: world = parentWorld * local.
 *   scale    = ps * ls
 *   rotate   = pr * lr
 *   translate = pt + ps * (pr * lt)
 * Never flattens by summing positions.
 */
export function composeTrs(parent, local) {
  return {
    translate: matVec3(parent.rotate, [
      local.translate[0] * parent.scale,
      local.translate[1] * parent.scale,
      local.translate[2] * parent.scale,
    ]).map((v, i) => v + parent.translate[i]),
    rotate: mulMat3(parent.rotate, local.rotate),
    scale: parent.scale * local.scale,
  };
}

/** Point application: (R * p) * s + t (NiTransform::operator*(NiPoint3)). */
export function applyTrsPoint(trs, p) {
  const r = matVec3(trs.rotate, [p[0], p[1], p[2]]);
  return [
    r[0] * trs.scale + trs.translate[0],
    r[1] * trs.scale + trs.translate[1],
    r[2] * trs.scale + trs.translate[2],
  ];
}

// ---- column-major 4x4 (THREE-compatible layout) ----
// THREE.Matrix4 stores elements column-major and transforms p as M*p.
// For p' = (R*p)*s + t the equivalent 4x4 has rows [R*s | t]:
//   row i = [R[i][0]*s, R[i][1]*s, R[i][2]*s, t[i]]
// Column-major flat layout: elements[4*c + r].
export function trsToColumnMajor4(trs) {
  const { rotate: R, translate: t, scale: s } = trs;
  return new Float64Array([
    R[0][0] * s, R[1][0] * s, R[2][0] * s, 0,
    R[0][1] * s, R[1][1] * s, R[2][1] * s, 0,
    R[0][2] * s, R[1][2] * s, R[2][2] * s, 0,
    t[0], t[1], t[2], 1,
  ]);
}

// ---- comparisons (tolerance per component; full matrices, never sums) ----

export function diffVec3(a, b) {
  return Math.max(Math.abs(a[0] - b[0]), Math.abs(a[1] - b[1]), Math.abs(a[2] - b[2]));
}

export function diffMat3(a, b) {
  let d = 0;
  for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) d = Math.max(d, Math.abs(a[i][j] - b[i][j]));
  return d;
}

export function compareTrs(a, b, tol) {
  const dt = diffVec3(a.translate, b.translate);
  const dr = diffMat3(a.rotate, b.rotate);
  const ds = Math.abs(a.scale - b.scale);
  return {
    ok: dt <= tol && dr <= tol && ds <= tol,
    maxTranslateDiff: dt,
    maxRotateDiff: dr,
    scaleDiff: ds,
    tolerance: tol,
  };
}

/** Deep structural equality (exact) — used to prove serialized TRS values stay
 * intact through render conversion and instance operations. */
export function trsDeepEqual(a, b) {
  if (a === b) return true;
  if (!a || !b) return false;
  if (a.scale !== b.scale) return false;
  for (let i = 0; i < 3; i++) {
    if (a.translate[i] !== b.translate[i]) return false;
    for (let j = 0; j < 3; j++) if (a.rotate[i][j] !== b.rotate[i][j]) return false;
  }
  return true;
}

export function cloneTrs(trs) {
  return makeTrs(trs.translate, trs.rotate, trs.scale);
}
