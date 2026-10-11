#!/usr/bin/env node
// pcg935_batch10.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 2)
// FULL-CORPUS NIF 10.1.0.0 batch: every 10.1 entry from the physical index
// through PecNif10CorpusReader with closure + status per row. Resumable.
'use strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10Corpus, PEC_NIF10_CORPUS_READER_VERSION } from '../../src/pecompat/PecNif10CorpusReader.js';
import { buildAssetIR, validateSceneGraph, composeWorldTransforms, computeSceneBounds } from '../../src/pecompat/PecSceneIR.js';

const PRIVATE_ROOT = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010';
const OUT_DIR = path.join(PRIVATE_ROOT, 'batch10');
const CHECKPOINT = path.join(OUT_DIR, 'checkpoint.jsonl');
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex');

const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const entries = archive.entries().filter((e) => {
  const p = bytes.subarray(e.offset, e.offset + 64);
  const nl = p.indexOf(0x0a);
  if (nl < 4 || nl + 8 > p.length) return false;
  const dv = new DataView(p.buffer, p.byteOffset, p.byteLength);
  return dv.getUint32(nl + 1, true) === 0x0A010000;
});
console.log('[batch10] entries:', entries.length);
fs.mkdirSync(OUT_DIR, { recursive: true });

// resume support
let doneSet = new Set();
if (fs.existsSync(CHECKPOINT)) {
  for (const ln of fs.readFileSync(CHECKPOINT, 'utf8').split('\n')) {
    if (!ln) continue;
    try { doneSet.add(JSON.parse(ln).name); } catch { }
  }
  console.log('[batch10] resuming:', doneSet.size);
}
const out = fs.createWriteStream(CHECKPOINT, { flags: 'a' });
const VERBOSE = process.env.PCG935_VERBOSE === '1';
let pass = 0; let fail = 0;
const failFamilies = {};
const t0 = Date.now();
for (const e of entries) {
  if (doneSet.has(e.name)) continue;
  const payload = bytes.subarray(e.offset, e.offset + e.size);
  const row = { name: e.name, size: e.size, sha: sha256(payload).slice(0, 16) };
  const tf = Date.now();
  if (VERBOSE) console.log('[start]', e.name, e.size);
  try {
    const r = readNif10Corpus(payload, { sourceName: e.name });
    const ir = buildAssetIR(r, {
      assetId: parseInt(e.name, 10), era: 'PCG_9_3_5', build: 'PCG_9_3_5_Models_bnt_entry',
      container: 'Models/Models.bnt', entryName: e.name, payloadSha256: sha256(payload),
      sizeBytes: e.size, adapterVersion: 'batch10', physicalSource: 'Models.bnt',
    });
    const validation = validateSceneGraph(ir);
    const world = composeWorldTransforms(ir);
    const bounds = computeSceneBounds(ir, world);
    // stats
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
  if (dt > 3000 || VERBOSE) console.log(`[slow] ${e.name} ${dt}ms`);
  if ((pass + fail) % 500 === 0) console.log(`[batch10] ${pass + fail}/${entries.length} pass=${pass} fail=${fail} (${Math.round((pass + fail) / entries.length * 100)}%)`);
}
out.end();
console.log(`[batch10] DONE pass=${pass} fail=${fail} elapsed=${Date.now() - t0}ms`);
console.log('[batch10] fail families:', JSON.stringify(failFamilies));
