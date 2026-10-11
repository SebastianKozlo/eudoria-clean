#!/usr/bin/env node
// pcg935_batch41.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 3)
// FULL NIF 4.1.0.12 batch: all 757 v4 entries through PecNif41Reader.
'use strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif41Corpus } from '../../src/pecompat/PecNif41Reader.js';
import { buildAssetIR, validateSceneGraph, composeWorldTransforms, computeSceneBounds } from '../../src/pecompat/PecSceneIR.js';

const PRIVATE_ROOT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010';
const OUT_DIR = path.join(PRIVATE_ROOT, 'batch41');
const CHECKPOINT = path.join(OUT_DIR, 'checkpoint.jsonl');
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex');

const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const entries = archive.entries().filter((e) => {
  const p = bytes.subarray(e.offset, e.offset + 64);
  const nl = p.indexOf(0x0a);
  if (nl < 4 || nl + 8 > p.length) return false;
  const dv = new DataView(p.buffer, p.byteOffset, p.byteLength);
  return dv.getUint32(nl + 1, true) === 0x0401000C;
});
console.log('[batch41] entries:', entries.length);
fs.mkdirSync(OUT_DIR, { recursive: true });
let doneSet = new Set();
if (fs.existsSync(CHECKPOINT)) {
  for (const ln of fs.readFileSync(CHECKPOINT, 'utf8').split('\n')) {
    if (!ln) continue;
    try { doneSet.add(JSON.parse(ln).name); } catch { }
  }
  console.log('[batch41] resuming:', doneSet.size);
}
const out = fs.createWriteStream(CHECKPOINT, { flags: 'a' });
let pass = 0; let fail = 0;
const failFamilies = {};
const t0 = Date.now();
for (const e of entries) {
  if (doneSet.has(e.name)) continue;
  const payload = bytes.subarray(e.offset, e.offset + e.size);
  const row = { name: e.name, size: e.size, sha: sha256(payload).slice(0, 16) };
  const tf = Date.now();
  try {
    const r = readNif41Corpus(payload, { sourceName: e.name });
    const ir = buildAssetIR(r, {
      assetId: parseInt(e.name, 10), era: 'PCG_9_3_5', build: 'PCG_9_3_5_Models_bnt_entry',
      container: 'Models/Models.bnt', entryName: e.name, payloadSha256: sha256(payload),
      sizeBytes: e.size, adapterVersion: 'batch41', physicalSource: 'Models.bnt',
    });
    const validation = validateSceneGraph(ir);
    const world = composeWorldTransforms(ir);
    const bounds = computeSceneBounds(ir, world);
    let tris = 0, verts = 0, meshes = 0;
    for (const b of ir.blocks) if (b.type === 'NiTriShape') {
      const g = ir.blocks.find((x) => x.index === b.dataRef)?.geometry;
      meshes++;
      if (g) { tris += g.numTriangles ?? 0; verts += g.numVertices ?? 0; }
    }
    const typeC = ir.blockTypeCensus;
    row.status = validation.ok ? 'PASS' : 'PASS_LINKS_INVALID';
    row.blocks = r.blocks.length;
    row.meshes = meshes; row.tris = tris; row.verts = verts;
    row.kf = typeC['NiKeyframeController'] ?? 0;
    row.tk = typeC['NiTextKeyExtraData'] ?? 0;
    row.skin = typeC['NiSkinInstance'] ?? 0;
    row.attempts = r.closure.attempts;
    row.extent = Number.isFinite(bounds.min[0]) ? Math.max(bounds.extents[0], bounds.extents[1], bounds.extents[2]) : null;
    row.errors = validation.errors.length;
    row.tail = r.closure.tailBytes;
    pass++;
  } catch (err) {
    row.status = 'FAIL';
    row.error = String(err.message).slice(0, 300);
    const fam = row.error.split(']')[1]?.split('(')[0]?.trim().slice(0, 40) ?? 'OTHER';
    failFamilies[fam] = (failFamilies[fam] ?? 0) + 1;
    fail++;
  }
  out.write(JSON.stringify(row) + '\n');
  const dt = Date.now() - tf;
  if (dt > 3000) console.log(`[slow] ${e.name} ${dt}ms`);
  if ((pass + fail) % 200 === 0) console.log(`[batch41] ${pass + fail}/${entries.length} pass=${pass} fail=${fail}`);
}
out.end();
console.log(`[batch41] DONE pass=${pass} fail=${fail} elapsed=${Date.now() - t0}ms`);
console.log('[batch41] fail families:', JSON.stringify(failFamilies));
