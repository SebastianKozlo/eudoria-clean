#!/usr/bin/env node
// PRIVATE probe: run PecNif10CorpusReader against a set of real corpus payloads.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10Corpus } from '../../src/pecompat/PecNif10CorpusReader.js';

const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const sha256 = (b) => crypto.createHash('sha256').update(b).digest('hex');

const targets = process.argv.slice(2).length ? process.argv.slice(2) : [
  '218757.nif', '505775.nif', '505813.nif', '524447.nif', '460075.nif', '421380.nif', '508854.nif', '417906.nif', '505007.nif',
];
for (const name of targets) {
  const entry = archive.entryByName(name);
  if (!entry) { console.log(name, 'NOT FOUND'); continue; }
  const { payload } = archive.readEntry(entry);
  const t0 = Date.now();
  try {
    const r = readNif10Corpus(payload, { sourceName: name });
    const census = {};
    for (const b of r.blocks) census[b.type] = (census[b.type] ?? 0) + 1;
    const kf = census['NiKeyframeController'] ?? 0;
    const tk = census['NiTextKeyExtraData'] ?? 0;
    const skins = census['NiSkinInstance'] ?? 0;
    console.log(`${name} OK ${Date.now() - t0}ms blocks=${r.blocks.length} kf=${kf} tk=${tk} skin=${skins} types=${Object.keys(census).length} attempts=${r.closure.attempts} decisions=${r.closure.decisions.length}`);
  } catch (e) {
    console.log(`${name} FAIL ${Date.now() - t0}ms: ${e.message.slice(0, 220)}`);
  }
}
