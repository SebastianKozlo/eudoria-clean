#!/usr/bin/env node
// pcg935_census_types.mjs — block-type census across ALL v4 files (PRIVATE).
import fs from 'node:fs';
import path from 'node:path';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif41Corpus } from '../../src/pecompat/PecNif41Reader.js';

const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const dv = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
const entries = archive.entries().filter((e) => {
  const p = bytes.subarray(e.offset, e.offset + 64);
  const nl = p.indexOf(0x0a);
  if (nl < 4 || nl + 8 > p.length) return false;
  return dv.getUint32(e.offset + nl + 1, true) < 0x05000000;
});
console.log('v4 entries:', entries.length);
const typeCount = {};
const typeByFile = [];
let pass = 0;
for (const e of entries) {
  const payload = bytes.subarray(e.offset, e.offset + e.size);
  try {
    const r = readNif41Corpus(payload, { sourceName: e.name });
    pass++;
    const c = {};
    for (const b of r.blocks) {
      c[b.type] = (c[b.type] || 0) + 1;
      typeCount[b.type] = (typeCount[b.type] || 0) + 1;
    }
    typeByFile.push({ name: e.name, size: e.size, types: c });
  } catch (err) {
    typeByFile.push({ name: e.name, size: e.size, error: String(err.message).slice(0, 120) });
  }
}
console.log('pass:', pass, '/', entries.length);
const outDir = 'D:\\Eudoria_Reconstruction\\99_Audits\\PE_SCENEIR_PCG935_ALL_ASSETS_R1_20261010\\census';
fs.writeFileSync(path.join(outDir, 'v4_block_types.json'), JSON.stringify(typeByFile, null, 1));
console.log('TYPE TOTALS:');
for (const [t, n] of Object.entries(typeCount).sort((a, b) => b[1] - a[1])) console.log(' ', t, n);
