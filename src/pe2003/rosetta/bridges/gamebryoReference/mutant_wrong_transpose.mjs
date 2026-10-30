// mutant_wrong_transpose.mjs — DELIBERATE NEGATIVE CONTROL (DO NOT USE).
// Parent RUN_ID: PE2003_ROSETTA_GAMEBRYO_BRIDGE_CORRECTIONS_R1_20261030 (J4, Wave B2).
//
// This mutant reproduces the harness.cpp MatFromTransform bug class: it
// uploads R UNTRANSPOSED into the D3D row-vector world matrix
// (M[i][j] = s*R[i][j], the "harness layout"), so the device computes
// R^T (s p) + t instead of R (s p) + t.
//
// It is a targeted mutation: every export except niToD3DWorld is re-exported
// unchanged from the correct adapter; ONLY niToD3DWorld is mutated, so any
// test failure observed with this module is attributable to the missing
// transpose alone.
//
// REQUIRED BEHAVIOR: the test suite run against this mutant MUST FAIL
// (non-zero exit), specifically gates rotY90_scale1.5 (produces (50,0,21.5),
// deviation 3.0 from ground truth) and noncommuting_pair, per the J2 gate
// wrong_transpose_mutation_must_fail. A suite that passes with this mutant
// present is itself broken.
import * as correct from './niTransformAdapter.mjs';

export const {
  makeIR, applyIR, d3dDeviceApply, niToThreeWorld, threeElementsApply,
  compose, cameraBasis, cameraViewD3D, cameraViewThree,
  D3D_LH_TARGET, THREE_RH_TARGET,
  NiTransformIRError, MissingConventionError,
} = correct;

import { makeIR as _makeIR } from './niTransformAdapter.mjs';

/** MUTATED: harness layout — R copied UNTRANSPOSED (missing transpose). */
export function niToD3DWorld(ir) {
  const x = _makeIR(ir); // validation kept; only the LAYOUT is mutated
  const R = x.rotate, s = x.scale, t = x.translate;
  const M = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 1],
  ];
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      M[i][j] = s * R[i][j]; // MUTANT: no transpose (harness MatFromTransform)
    }
  }
  M[3][0] = t[0]; M[3][1] = t[1]; M[3][2] = t[2];
  return M;
}
