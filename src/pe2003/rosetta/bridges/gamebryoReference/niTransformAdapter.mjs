// niTransformAdapter.mjs
// PORTABLE_NI_TRANSFORM_ADAPTER — Wave B1 (job J4), parent RUN_ID:
//   PE2003_ROSETTA_GAMEBRYO_BRIDGE_CORRECTIONS_R1_20261030
// RESEARCH ONLY: pure CPU math, dependency-free, no SDK code copied.
// Conventions derived independently from point-math ground truth
// (transform_check.py truth_apply) and, for convention reference only,
// NiDX9Renderer.cpp (SHA256 62205FDB...C212F):
//   - GetD3DFromNi  (NiDX9Renderer.cpp:2801-2816): D3DMATRIX M with
//     M[i][j] = s*R[j][i] (rotation TRANSPOSED into upper 3x3),
//     translate in row 4 -> row-vector device reproduces p' = R(s p)+t.
//   - SetCameraData (NiDX9Renderer.cpp:2643-2658): view matrix places the
//     (Right, Up, Dir) basis in COLUMNS, row4 = -(basis . eye) -> B(v-e).
//   - Composition site (NiDX9Renderer.cpp:2948):
//         NiTransform kBoneMatrix = ppkBones[i]->GetWorldTransform() *
//                                   pkBoneData[i].m_kSkinToBone;
//     i.e. NiTransform operator* is parent o child, child applied FIRST
//     (also left-folded at :2958: kWorldFromSkinFromWorld * kBoneMatrix).
//
// NO silent handedness conversion, NO magic scale factors anywhere.

export const D3D_LH_TARGET = Object.freeze({
  id: 'd3d-lh',
  forward: '+Z (left-handed view space, D3DXLookAtLH convention)',
  vectorConvention: 'row-vector device: v\'_j = sum_i v_i M[i][j] (+ M[3][j], w=1)',
});

export const THREE_RH_TARGET = Object.freeze({
  id: 'three-rh',
  forward: '-Z (right-handed camera; THREE.Camera looks down local -Z)',
  vectorConvention: 'column-vector device: out_i = sum_j M[i][j] v_j (+ M[i][3], w=1)',
});

// ---------------------------------------------------------------------------
// IR validation
// ---------------------------------------------------------------------------

export class NiTransformIRError extends Error {
  constructor(msg, site) {
    super(`NiTransform IR rejected (${site}): ${msg}`);
    this.name = 'NiTransformIRError';
    this.site = site;
  }
}

function fin(x, site) {
  const n = Number(x);
  if (typeof x !== 'number' || !Number.isFinite(n)) {
    // rejects NaN, +Inf, -Inf and non-numbers; never emits a matrix
    throw new NiTransformIRError(`non-finite/non-number value ${String(x)}`, site);
  }
  return n;
}

/**
 * Validate + freeze a NiTransform IR.
 * Fields: scale (uniform finite float), rotate (3x3, Ni row order,
 * entry [i][j] = R_ij, convention p'_i = sum_j R_ij p_j), translate [x,y,z].
 * Application order FIXED: p' = R (s p) + t.
 * NaN / +/-Inf anywhere => NiTransformIRError thrown BEFORE any matrix build.
 */
export function makeIR(raw) {
  if (raw === null || typeof raw !== 'object') {
    throw new NiTransformIRError('IR must be an object', 'top');
  }
  const scale = fin(raw.scale, 'scale');
  if (!Array.isArray(raw.rotate) || raw.rotate.length !== 3) {
    throw new NiTransformIRError('rotate must be 3 rows', 'rotate');
  }
  const R = raw.rotate.map((row, i) => {
    if (!Array.isArray(row) || row.length !== 3) {
      throw new NiTransformIRError(`rotate row ${i} must have 3 entries`, `rotate[${i}]`);
    }
    return row.map((v, j) => fin(v, `rotate[${i}][${j}]`));
  });
  if (!Array.isArray(raw.translate) || raw.translate.length !== 3) {
    throw new NiTransformIRError('translate must have 3 components', 'translate');
  }
  const t = raw.translate.map((v, i) => fin(v, `translate[${i}]`));
  return Object.freeze({ scale, rotate: Object.freeze(R.map(Object.freeze)), translate: Object.freeze(t) });
}

function revalidate(ir) {
  // Defensive re-validation at every consumer: a raw object that skipped
  // makeIR (or was tampered with) is rejected the same way.
  return makeIR(ir);
}

// ---------------------------------------------------------------------------
// CPU point application (ground truth inside the adapter; the TEST suite
// uses its own independent oracle, never this function)
// ---------------------------------------------------------------------------

/** p' = R (s p) + t  (Ni row-dot: p'_i = sum_j R_ij (s p_j) + t_i) */
export function applyIR(ir, p) {
  const x = revalidate(ir);
  const [px, py, pz] = p;
  const R = x.rotate, s = x.scale, t = x.translate;
  return [
    R[0][0] * s * px + R[0][1] * s * py + R[0][2] * s * pz + t[0],
    R[1][0] * s * px + R[1][1] * s * py + R[1][2] * s * pz + t[1],
    R[2][0] * s * px + R[2][1] * s * py + R[2][2] * s * pz + t[2],
  ];
}

// ---------------------------------------------------------------------------
// D3D world matrix (corrected GetD3DFromNi equivalent)
// ---------------------------------------------------------------------------

/**
 * 4x4 D3DMATRIX in row-vector layout consumed by fixed-function
 * SetTransform: M[i][j] = s * R[j][i] for i,j in 0..2 (rotation TRANSPOSED
 * into the upper 3x3), M[3][0..2] = t (translate row 4), M[0..2][3] = 0,
 * M[3][3] = 1. Device semantics v'_j = sum_i v_i M[i][j] + M[3][j]
 * reproduce p' = R(s p) + t exactly.
 * Returns nested row-major array M[row][col].
 */
export function niToD3DWorld(ir) {
  const x = revalidate(ir);
  const R = x.rotate, s = x.scale, t = x.translate;
  const M = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 1],
  ];
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      M[i][j] = s * R[j][i]; // TRANSPOSED (GetD3DFromNi layout)
    }
  }
  M[3][0] = t[0]; M[3][1] = t[1]; M[3][2] = t[2];
  return M;
}

/** D3D fixed-function row-vector device semantics:
 *  v'_j = sum_i v_i M[i][j] + M[3][j] (homogeneous w=1). */
export function d3dDeviceApply(M, p) {
  const [px, py, pz] = p;
  return [
    px * M[0][0] + py * M[1][0] + pz * M[2][0] + M[3][0],
    px * M[0][1] + py * M[1][1] + pz * M[2][1] + M[3][1],
    px * M[0][2] + py * M[1][2] + pz * M[2][2] + M[3][2],
  ];
}

// ---------------------------------------------------------------------------
// Three.js world representation (column-vector device, NO transpose path)
// ---------------------------------------------------------------------------

/**
 * Three.js-compatible representation of the SAME world transform.
 * Because THREE.Matrix4 multiplies COLUMN vectors (out = M v), the logical
 * matrix rows carry R directly — NO transpose in this path. Layout:
 *   logical row-major:  [ s*R00 s*R01 s*R02 tx ] etc., last row (0,0,0,1).
 * Returned object:
 *   setArguments       — 16 row-major arguments for THREE.Matrix4().set()
 *                        (set(n11,n12,n13,n14, n21,...) is row-major).
 *   columnMajorElements — 16 elements in THREE's internal column-major
 *                        storage order, valid for THREE.Matrix4().fromArray().
 *   mapping note: new THREE.Matrix4().set(...setArguments) and
 *                 new THREE.Matrix4().fromArray(columnMajorElements) are
 *                 equivalent; M.applyMatrix4 / Vector3.applyMatrix4 then
 *                 reproduces p' = R(s p)+t. This is the same logical matrix
 *                 as Matrix4.compose(pos, quat_from_R, scalar) would give
 *                 for a pure rotation quaternion, but is built from the Ni
 *                 row-dot rotation directly, without quaternion conversion.
 */
export function niToThreeWorld(ir) {
  const x = revalidate(ir);
  const R = x.rotate, s = x.scale, t = x.translate;
  const L = [ // logical row-major 4x4 (column-vector device)
    [s * R[0][0], s * R[0][1], s * R[0][2], t[0]],
    [s * R[1][0], s * R[1][1], s * R[1][2], t[1]],
    [s * R[2][0], s * R[2][1], s * R[2][2], t[2]],
    [0, 0, 0, 1],
  ];
  const setArguments = L.flat(); // row-major for Matrix4.set()
  const columnMajorElements = []; // elements[col*4 + row] = L[row][col]
  for (let col = 0; col < 4; col++) {
    for (let row = 0; row < 4; row++) {
      columnMajorElements.push(L[row][col]);
    }
  }
  return Object.freeze({
    target: THREE_RH_TARGET,
    setArguments: Object.freeze(setArguments),
    columnMajorElements: Object.freeze(columnMajorElements),
  });
}

/** Apply a 16-element column-major element array (THREE storage order) as a
 *  column-vector device: out_i = sum_j el[col_j_start] ... — helper for
 *  consumers that do not have the three package. */
export function threeElementsApply(columnMajorElements, p) {
  const e = columnMajorElements;
  const [px, py, pz] = p;
  return [
    e[0] * px + e[4] * py + e[8] * pz + e[12],
    e[1] * px + e[5] * py + e[9] * pz + e[13],
    e[2] * px + e[6] * py + e[10] * pz + e[14],
  ];
}

// ---------------------------------------------------------------------------
// Composition (Ni/Gamebryo parent o child, child applied FIRST)
// ---------------------------------------------------------------------------

function mat3mul(A, B) {
  const out = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      out[i][j] = A[i][0] * B[0][j] + A[i][1] * B[1][j] + A[i][2] * B[2][j];
    }
  }
  return out;
}

/**
 * parent o child (child applied first):
 *   world = parent.rotate * (child.rotate * p * child.scale + child.translate)
 *           * parent.scale + parent.translate
 * Ni/Gamebryo NiTransform operator* semantics, based on the SDK composition
 * site NiDX9Renderer.cpp:2948
 *   NiTransform kBoneMatrix = ppkBones[i]->GetWorldTransform() *
 *                             pkBoneData[i].m_kSkinToBone;
 * (world-from-bone parent multiplied on the LEFT of skin-to-bone child;
 * left-folded again at :2958). Closed form (uniform scale):
 *   (P o C).s = P.s * C.s
 *   (P o C).R = P.R * C.R          (3x3 matrix product)
 *   (P o C).t = P.t + P.R (P.s * C.t)
 */
export function compose(parentIR, childIR) {
  const P = revalidate(parentIR);
  const C = revalidate(childIR);
  return makeIR({
    scale: P.scale * C.scale,
    rotate: mat3mul(P.rotate, C.rotate),
    translate: [
      P.translate[0] + P.scale * (P.rotate[0][0] * C.translate[0] + P.rotate[0][1] * C.translate[1] + P.rotate[0][2] * C.translate[2]),
      P.translate[1] + P.scale * (P.rotate[1][0] * C.translate[0] + P.rotate[1][1] * C.translate[1] + P.rotate[1][2] * C.translate[2]),
      P.translate[2] + P.scale * (P.rotate[2][0] * C.translate[0] + P.rotate[2][1] * C.translate[1] + P.rotate[2][2] * C.translate[2]),
    ],
  });
}

// ---------------------------------------------------------------------------
// Camera basis (NiCamera column convention, X-axis fix)
// ---------------------------------------------------------------------------

/**
 * NiCamera rotation column convention consumed AS-IS:
 *   F (look)  = R col0,  U (up) = R col1,  RIGHT = R col2.
 * X of the view basis is the camera's OWN right vector (col2) — NOT
 * norm(U x F), which equals -col2 for a proper RH rotation and would
 * mirror the view (the J2 camera_case mirror bug, fixed here).
 */
export function cameraBasis(ir) {
  const x = revalidate(ir);
  const R = x.rotate;
  return {
    F: [R[0][0], R[1][0], R[2][0]],   // look  = col0
    U: [R[0][1], R[1][1], R[2][1]],   // up    = col1
    X: [R[0][2], R[1][2], R[2][2]],   // right = col2 (MIRROR FIX)
  };
}

export class MissingConventionError extends Error {
  constructor(fnName) {
    super(`${fnName}: a camera/view convention parameter is REQUIRED ` +
      `('d3d-lh' or 'three-rh'); handedness is never silently converted`);
    this.name = 'MissingConventionError';
  }
}

function requireConvention(convention, fnName) {
  if (convention === undefined || convention === null || convention === '') {
    throw new MissingConventionError(fnName);
  }
  if (convention !== 'd3d-lh' && convention !== 'three-rh') {
    throw new MissingConventionError(fnName +
      ` (unknown convention '${String(convention)}')`);
  }
}

// ---------------------------------------------------------------------------
// Camera view matrices (explicit, per-convention)
// ---------------------------------------------------------------------------

/**
 * D3D LH view matrix (row-vector device, basis-in-COLUMNS as the engine's
 * SetCameraData and D3DXLookAtLH do). Device computes v' = B(v - eye):
 *   M[i][0] = X_i, M[i][1] = Y_i, M[i][2] = F_i (i in 0..2),
 *   M[3] = ( -X.eye, -Y.eye, -F.eye, 1 ), M[0..2][3] = 0.
 * X = camera right (R col2) — the mirror fix; eye maps to exactly (0,0,0).
 * convention MUST be 'd3d-lh' (absent/other => MissingConventionError).
 */
export function cameraViewD3D(ir, { convention } = {}) {
  requireConvention(convention, 'cameraViewD3D');
  const b = cameraBasis(ir);
  const eye = revalidate(ir).translate;
  const dot = (a, c) => a[0] * c[0] + a[1] * c[1] + a[2] * c[2];
  const M = [
    [b.X[0], b.U[0], b.F[0], 0],
    [b.X[1], b.U[1], b.F[1], 0],
    [b.X[2], b.U[2], b.F[2], 0],
    [-dot(b.X, eye), -dot(b.U, eye), -dot(b.F, eye), 1],
  ];
  return M;
}

/**
 * Three.js RH camera view (column-vector device). The camera's view space is
 * right-handed with the camera looking down -Z (THREE_RH_TARGET). Built as
 * the D3D-style basis projection FOLLOWED BY an EXPLICIT, separately
 * declared LH->RH reorientation diag(1,1,-1) applied as its own step:
 *   x = X.(v - eye),  y = U.(v - eye),  z = -F.(v - eye)
 * No handedness change is ever folded into the rotate/transpose logic.
 * convention MUST be 'three-rh' (absent/other => MissingConventionError).
 */
export function cameraViewThree(ir, { convention } = {}) {
  requireConvention(convention, 'cameraViewThree');
  const b = cameraBasis(ir);
  const eye = revalidate(ir).translate;
  const dot = (a, c) => a[0] * c[0] + a[1] * c[1] + a[2] * c[2];
  const L = [ // logical row-major 4x4 (column-vector device)
    [b.X[0], b.X[1], b.X[2], -dot(b.X, eye)],
    [b.U[0], b.U[1], b.U[2], -dot(b.U, eye)],
    [-b.F[0], -b.F[1], -b.F[2], dot(b.F, eye)],
    [0, 0, 0, 1],
  ];
  const columnMajorElements = [];
  for (let col = 0; col < 4; col++) {
    for (let row = 0; row < 4; row++) {
      columnMajorElements.push(L[row][col]);
    }
  }
  return Object.freeze({
    target: THREE_RH_TARGET,
    reorientation: Object.freeze({
      declared: true,
      step: 'LH->RH change of basis applied as an EXPLICIT separate step',
      matrix: Object.freeze([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, -1]), // diag(1,1,-1)
    }),
    setArguments: Object.freeze(L.flat()),
    columnMajorElements: Object.freeze(columnMajorElements),
  });
}
