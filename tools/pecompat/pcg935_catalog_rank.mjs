#!/usr/bin/env node
// pcg935_catalog_rank.mjs — final catalog emission from the parse checkpoint.
// Ranking: extent maxAxis DESC (largest->smallest), UNKNOWN last, stable
// tie-break id ASC. Alternate sort keys measured with coverage counts.
'use strict';
import fs from 'node:fs';
import path from 'node:path';

const OUT_DIR = path.join('D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010', 'catalog');
const rows = fs.readFileSync(path.join(OUT_DIR, 'checkpoint.jsonl'), 'utf8')
  .split('\n').filter(Boolean).map((l) => JSON.parse(l));
// Deduplicate (checkpoint appends are name-keyed; last row wins).
const byName = new Map();
for (const r of rows) byName.set(r.name, r);
const list = [...byName.values()];
console.log('[rank] unique entries:', list.length);

const ver = (r) => ({ '4838': '10.1.0.0', '757': '4.1.0.12', '1': '4.0.0.2' });
const diag = (r) => r.extents ? Math.hypot(r.extents[0], r.extents[1], r.extents[2]) : null;

const sorters = {
  extent: (a, b) => {
    if (a.extent == null && b.extent == null) return a.id - b.id;
    if (a.extent == null) return 1;
    if (b.extent == null) return -1;
    if (b.extent !== a.extent) return b.extent - a.extent;
    return a.id - b.id;
  },
  bytes: (a, b) => b.sizeBytes - a.sizeBytes || a.id - b.id,
  tris: (a, b) => (b.tris ?? 0) - (a.tris ?? 0) || a.id - b.id,
  verts: (a, b) => (b.verts ?? 0) - (a.verts ?? 0) || a.id - b.id,
  diagonal: (a, b) => {
    const da = diag(a); const db = diag(b);
    if (da == null && db == null) return a.id - b.id;
    if (da == null) return 1;
    if (db == null) return -1;
    return db - da || a.id - b.id;
  },
  vertical: (a, b) => {
    const va = a.extents ? a.extents[2] : null; const vb = b.extents ? b.extents[2] : null;
    if (va == null && vb == null) return a.id - b.id;
    if (va == null) return 1;
    if (vb == null) return -1;
    return vb - va || a.id - b.id;
  },
};
const extentOrder = [...list].sort(sorters.extent).map((r) => r.id);
const coverage = {
  extent: list.filter((r) => r.extent != null).length,
  bytes: list.length,
  tris: list.filter((r) => (r.tris ?? 0) > 0).length,
  verts: list.filter((r) => (r.verts ?? 0) > 0).length,
  diagonal: list.filter((r) => diag(r) != null).length,
  vertical: list.filter((r) => r.extents != null).length,
};
const slim = list.map((r) => ({
  id: r.id, name: r.name, v: r.versionString, size: r.sizeBytes, status: r.status,
  blocks: r.blocks ?? null, meshes: r.meshes ?? 0, tris: r.tris ?? 0, verts: r.verts ?? 0,
  extent: r.extent, ex: r.extents ?? null,
  kf: r.kf ?? 0, tk: r.tk ?? 0, skin: r.skin ?? 0, morph: r.morph ?? 0, psys: r.psys ?? 0,
  ctrl: r.controllers ?? [], arkTex: r.arkTexCount ?? 0, srcTex: r.sourceTexCount ?? 0,
  err: r.status === 'FAIL' ? r.error : undefined,
}));
const stats = {
  total: list.length, pass: list.filter((r) => r.status !== 'FAIL').length,
  fail: list.filter((r) => r.status === 'FAIL').length,
  byVersion: Object.fromEntries([...list.reduce((m, r) => m.set(r.versionString, (m.get(r.versionString) ?? 0) + 1), new Map())]),
  unknownExtent: list.filter((r) => r.extent == null).length,
  withMeshes: list.filter((r) => (r.meshes ?? 0) > 0).length,
  withKf: list.filter((r) => (r.kf ?? 0) > 0).length,
  withSkin: list.filter((r) => (r.skin ?? 0) > 0).length,
  withMorph: list.filter((r) => (r.morph ?? 0) > 0).length,
  withArkTex: list.filter((r) => (r.arkTexCount ?? 0) > 0).length,
  coverage,
};
const catalog = { runId: 'PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010', generated: new Date().toISOString(), rankingPolicy: 'extent maxAxis DESC, UNKNOWN last, tie-break id ASC', stats, extentOrder, entries: slim };
fs.writeFileSync(path.join(OUT_DIR, 'catalog.json'), JSON.stringify(catalog));
console.log('[rank] stats:', JSON.stringify(stats));
console.log('[rank] top-5 by extent:', extentOrder.slice(0, 5).join(','));
console.log('[rank] last-5:', extentOrder.slice(-5).join(','));
