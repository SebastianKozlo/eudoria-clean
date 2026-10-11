#!/usr/bin/env node
// PRIVATE probe: for every PASSED file with a NiVertexMorphExtraData block,
// record {vertexCount N, extLength L} and find the L(N, W) relation.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10Corpus } from '../../src/pecompat/PecNif10CorpusReader.js';

const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const targets = process.argv.slice(2);
let count = 0;
for (const e of archive.entries()) {
  if (targets.length && !targets.includes(e.name)) continue;
  const p = bytes.subarray(e.offset, e.offset + 32);
  const nl = p.indexOf(0x0a);
  if (nl < 4) continue;
  const dv = new DataView(p.buffer, p.byteOffset, p.byteLength);
  if (dv.getUint32(nl + 1, true) !== 0x0A010000) continue;
  const payload = bytes.subarray(e.offset, e.offset + e.size);
  try {
    const r = readNif10Corpus(payload, { sourceName: e.name });
    for (const b of r.blocks) {
      if (b.type !== 'NiVertexMorphExtraData') continue;
      const N = b.fields.vertexCount;
      const L = b.fields.opaque.extLength;
      // candidate formulas
      const perRec = (L - (L % N || 0)) / N;
      console.log(`${e.name} blk=${b.index} N=${N} L=${L} L/N=${(L / N).toFixed(2)} (L-2)/N=${((L - 2) / N).toFixed(2)} (L-6)/N=${((L - 6) / N).toFixed(2)} tag=${b.fields.tag}`);
      if (++count > 25) process.exit(0);
    }
  } catch { /* skip failing files */ }
}
