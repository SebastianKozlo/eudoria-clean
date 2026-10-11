#!/usr/bin/env node
// PRIVATE probe: trace the morph block candidate loop inside a real file.
import fs from 'node:fs';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10Corpus } from '../../src/pecompat/PecNif10CorpusReader.js';

const name = process.argv[2] ?? '591842.nif';
const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const { payload } = archive.readEntry(archive.entryByName(name));
const trace = [];
try {
  const r = readNif10Corpus(payload, { sourceName: name, debugTrace: trace });
  console.log('OK', r.blocks.length);
  const morphs = r.blocks.filter((b) => b.type === 'NiVertexMorphExtraData');
  for (const m of morphs) console.log('MORPH blk', m.index, 'N=' + m.fields.vertexCount, 'ext=' + m.fields.opaque.extLength, 'method=' + m.fields.opaque.boundaryMethod);
} catch (e) {
  console.log('FAIL:', e.message.slice(0, 200));
  // Find all trace entries that are boundary-block decisions... they're not traced; show entries with type morph
  const morphEntries = trace.filter((t) => t.type === 'NiVertexMorphExtraData');
  console.log('morph trace entries:', morphEntries.length, morphEntries.slice(0, 5));
  // what's the last type that appears?
  const types = {};
  for (const t of trace) types[t.type] = (types[t.type] ?? 0) + 1;
  console.log('trace type census:', JSON.stringify(types));
}
