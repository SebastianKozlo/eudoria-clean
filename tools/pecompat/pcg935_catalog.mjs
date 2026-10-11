#!/usr/bin/env node
// pcg935_catalog.mjs — PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010 (Wave 4)
// Unified catalog: EVERY Models.bnt entry parsed through its version reader,
// composed bounds (FILE_SCENE_SPACE), extent ranking, texture/animation stats.
// Output: PRIVATE_OUTPUT_ROOT/catalog/catalog.json (resumable, keyed by entry).
'use strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10Corpus } from '../../src/pecompat/PecNif10CorpusReader.js';
import { readNif41Corpus } from '../../src/pecompat/PecNif41Reader.js';
import { buildAssetIR, validateSceneGraph, composeWorldTransforms, computeSceneBounds } from '../../src/pecompat/PecSceneIR.js';

const MODELS = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt';
const TEXTURES = 'D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Textures\\Textures.bnt';
const OUT_DIR = path.join('D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010', 'catalog');
const CHECKPOINT = path.join(OUT_DIR, 'checkpoint.jsonl');
const CATALOG = path.join(OUT_DIR, 'catalog.json');
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex');
fs.mkdirSync(OUT_DIR, { recursive: true });

const bytes = new Uint8Array(fs.readFileSync(MODELS));
const archive = new Bnt2Archive(bytes);
const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
const entries = archive.entries();
console.log('[catalog] entries:', entries.length);

// Texture index (for the reference control only — counts, no decode here).
const texBytes = new Uint8Array(fs.readFileSync(TEXTURES));
const texArchive = new Bnt2Archive(texBytes);
const texIds = new Set(texArchive.entries().map((e) => parseInt(String(e.name).replace(/\.dds$|\.tga$/i, ''), 10) || 0));
console.log('[catalog] texture entries:', texIds.size);

const headerVersion = (e) => {
  const p = bytes.subarray(e.offset, e.offset + 64);
  const nl = p.indexOf(0x0a);
  if (nl < 4 || nl + 8 > p.length) return 0;
  return dv.getUint32(e.offset + nl + 1, true);
};

let doneSet = new Set();
if (fs.existsSync(CHECKPOINT)) {
  for (const ln of fs.readFileSync(CHECKPOINT, 'utf8').split('\n')) {
    if (!ln) continue;
    try { doneSet.add(JSON.parse(ln).name); } catch { }
  }
  console.log('[catalog] resuming:', doneSet.size);
}
const out = fs.createWriteStream(CHECKPOINT, { flags: 'a' });
const t0 = Date.now();
let pass = 0; let fail = 0;
let unknownExtent = 0;
for (const e of entries) {
  if (doneSet.has(e.name)) continue;
  const payload = bytes.subarray(e.offset, e.offset + e.size);
  const id = parseInt(String(e.name).replace(/\.nif$/i, ''), 10);
  const version = headerVersion(e);
  const versionString = version >= 0x0a000000 ? '10.1.0.0' : (version === 0x04000002 ? '4.0.0.2' : '4.1.0.12');
  const row = { name: e.name, id, sizeBytes: e.size, sha: sha256(payload), version, versionString };
  const tf = Date.now();
  try {
    const r = version >= 0x0a000000
      ? readNif10Corpus(payload, { sourceName: e.name })
      : readNif41Corpus(payload, { sourceName: e.name });
    const ir = buildAssetIR(r, {
      assetId: id, era: 'PCG_9_3_5', build: 'PCG_9_3_5_Models_bnt_entry',
      container: 'Models/Models.bnt', entryName: e.name, payloadSha256: sha256(payload),
      sizeBytes: e.size, adapterVersion: 'pcg935-catalog-r1', physicalSource: 'Models.bnt',
    });
    const validation = validateSceneGraph(ir);
    const world = composeWorldTransforms(ir);
    const bounds = computeSceneBounds(ir, world);
    let tris = 0; let verts = 0; let meshes = 0;
    const typeC = ir.blockTypeCensus;
    for (const b of ir.blocks) {
      if (b.type === 'NiTriShape') {
        meshes++;
        // v10: geometry lives on the dataRef TARGET block (TriShapeData);
        // v4: buildAssetIR attaches .geometry the same way. Same lookup works.
        const g = ir.blocks.find((x) => x.index === b.dataRef)?.geometry;
        if (g) { tris += g.numTriangles ?? 0; verts += g.numVertices ?? 0; }
      }
    }
    // ArkTexture tails (RAW) for the texture chain; controls applied there.
    const arkTex = [];
    for (const b of ir.blocks) {
      if (b.type === 'NiArkTextureExtraData') {
        const list = b.fields?.entries ?? [];
        for (const t of list) arkTex.push({ meshRef: b.fields?.nextExtraDataRef ?? null, entryName: t.entryName, f1: t.f1, f2: t.f2, texPropRef: t.texturingPropertyRef, bytes9Hex: t.bytes9Hex });
      }
    }
    // NiSourceTexture file names (v10) + texprop slot sources
    const sourceTex = [];
    for (const b of ir.blocks) {
      if (b.type === 'NiSourceTexture' && b.fields?.fileName) sourceTex.push(b.fields.fileName);
    }
    const controllers = [];
    for (const b of ir.blocks) {
      if (/Controller$/.test(b.type) || b.type === 'NiTextKeyExtraData' || b.type === 'NiVertexMorphExtraData') {
        controllers.push(b.type);
      }
    }
    const extent = Number.isFinite(bounds.min?.[0]) && Number.isFinite(bounds.extents?.[0])
      ? Math.max(bounds.extents[0], bounds.extents[1], bounds.extents[2]) : null;
    if (extent == null) unknownExtent++;
    row.status = validation.ok ? 'PASS' : 'PASS_LINKS_INVALID';
    row.blocks = r.blocks.length;
    row.meshes = meshes; row.tris = tris; row.verts = verts;
    row.extent = extent;
    row.extents = bounds.extents ?? null;
    row.boundsMin = bounds.min ?? null;
    row.kf = typeC['NiKeyframeController'] ?? 0;
    row.tk = typeC['NiTextKeyExtraData'] ?? 0;
    row.skin = typeC['NiSkinInstance'] ?? 0;
    row.morph = typeC['NiVertexMorphExtraData'] ?? 0;
    row.psys = typeC['NiPSysData'] ?? 0;
    row.controllers = controllers.slice(0, 24);
    row.arkTexCount = arkTex.length;
    row.arkTexRefs = arkTex.slice(0, 8);
    row.sourceTexCount = sourceTex.length;
    row.sourceTexNames = sourceTex.slice(0, 8);
    row.errors = validation.errors.length;
    row.attempts = r.closure?.attempts ?? 0;
    pass++;
  } catch (err) {
    row.status = 'FAIL';
    row.error = String(err?.message ?? err).slice(0, 220);
    fail++;
  }
  out.write(JSON.stringify(row) + '\n');
  const dt = Date.now() - tf;
  if (dt > 5000) console.log(`[slow] ${e.name} ${dt}ms`);
  if ((pass + fail) % 500 === 0) console.log(`[catalog] ${pass + fail}/${entries.length} pass=${pass} fail=${fail} elapsed=${Date.now() - t0}ms`);
}
out.end();
console.log(`[catalog] parsed pass=${pass} fail=${fail} unknownExtent=${unknownExtent} elapsed=${Date.now() - t0}ms`);
