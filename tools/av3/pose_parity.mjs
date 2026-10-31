// tools/av3/pose_parity.mjs — AV-3 objective pose check (no eyes needed):
// replicate the client KF-hierarchy math (wrapper Rx(-90°)·0.01 + raw-NIF
// node locals) in node, then verify EVERY shape's bind world position equals
// the AV-2 static path value A·t_world·U (worldTRS from the reader's
// engine-validated composeTRS). If the rotation convention were wrong
// (R vs R^T), child translations would NOT match. 206264 + 103004.
'use strict';
import { promises as fs } from 'node:fs';
import * as THREE from 'three';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { parseModel41 } from '../../src/pesource/NifModelReader41.js';

const PIN = 128742137;
const buf = await fs.readFile('D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark');
if (buf.length !== PIN) throw new Error('FAIL-CLOSED pin');
const ark = new ArkArchive(new Uint8Array(buf));
const SCI = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_ISO_ASSET_VIEWER_R1_20261031\\AV3_ANIMATION';
const UNIT = 0.01;

const out = {};
for (const id of [206264, 103004]) {
  const { payload } = ark.readEntry(ark.entryById(id));
  const { extraction, renderModel } = parseModel41(payload, `${id}.nif`);
  const byIndex = new Map(extraction.blocks.map(b => [b.index, b]));
  const childOf = new Map();
  for (const b of extraction.blocks) if (b.type === 'NiNode' && b.fields) for (const c of b.fields.children) if (c >= 0) childOf.set(c, b.index);

  // client-identical hierarchy build
  const wrapper = new THREE.Group(); wrapper.matrixAutoUpdate = false;
  const wm = new THREE.Matrix4().makeRotationX(-Math.PI / 2); wm.scale(new THREE.Vector3(UNIT, UNIT, UNIT));
  wrapper.matrix.copy(wm); wrapper.matrixWorld.copy(wm);
  const objs = new Map();
  for (const n of renderModel.shapes.map(s => s.shapeIndex)) { /* shapes below */ }
  const nodesAll = extraction.blocks.filter(b => (b.type === 'NiNode' || b.type === 'NiTriShape') && b.fields);
  for (const n of nodesAll) {
    const o = new THREE.Object3D(); o.name = `n${n.index}`;
    const R = n.fields.rotation.map(r => r.map(h => {
      const u = new Uint32Array(1); const bb = new Uint8Array(u.buffer);
      for (let i = 0; i < 4; i++) bb[i] = parseInt(h.substr(i * 2, 2), 16);
      return new Float32Array(u.buffer)[0];
    }));
    const t = n.fields.translation.map(h => {
      const u = new Uint32Array(1); const bb = new Uint8Array(u.buffer);
      for (let i = 0; i < 4; i++) bb[i] = parseInt(h.substr(i * 2, 2), 16);
      return new Float32Array(u.buffer)[0];
    });
    const sh = (() => { const u = new Uint32Array(1); const bb = new Uint8Array(u.buffer);
      for (let i = 0; i < 4; i++) bb[i] = parseInt(n.fields.scale.substr(i * 2, 2), 16);
      return new Float32Array(u.buffer)[0]; })();
    o.position.fromArray(t);
    const m = new THREE.Matrix4().set(R[0][0], R[0][1], R[0][2], 0, R[1][0], R[1][1], R[1][2], 0, R[2][0], R[2][1], R[2][2], 0, 0, 0, 0, 1);
    o.quaternion.setFromRotationMatrix(m);
    o.scale.setScalar(sh);
    objs.set(n.index, o);
  }
  for (const n of nodesAll) {
    const o = objs.get(n.index);
    const p = childOf.has(n.index) && objs.has(childOf.get(n.index)) ? objs.get(childOf.get(n.index)) : wrapper;
    p.add(o);
  }
  wrapper.updateMatrixWorld(true);

  // compare EVERY shape node's world position with A·t_world·U (static path)
  let worst = 0, checked = 0, fails = 0;
  for (const s of renderModel.shapes) {
    const o = objs.get(s.shapeIndex); if (!o) continue;
    const wp = o.getWorldPosition(new THREE.Vector3());
    const exp = new THREE.Vector3(s.worldTRS.translation[0], s.worldTRS.translation[2], -s.worldTRS.translation[1]).multiplyScalar(UNIT);
    const d = wp.distanceTo(exp);
    checked++; if (d > worst) worst = d; if (d > 1e-4) fails++;
  }
  out[id] = { shapesChecked: checked, worstDeltaMeters: worst, failsOver1e_4: fails,
    pass: fails === 0 };
  console.log(id, JSON.stringify(out[id]));
}
out.pass = out[206264].pass && out[103004].pass;
await fs.writeFile(`${SCI}\\av3_pose_parity.json`, JSON.stringify(out, null, 2));
console.log('POSE_PARITY_PASS =', out.pass);
process.exit(out.pass ? 0 : 2);
