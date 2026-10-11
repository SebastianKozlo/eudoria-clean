#!/usr/bin/env node
// PRIVATE probe: debug one v4 file with trace.
import fs from 'node:fs';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif41Corpus } from '../../src/pecompat/PecNif41Reader.js';

const name = process.argv[2];
const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const { payload } = archive.readEntry(archive.entryByName(name));
const trace = [];
try {
  const r = readNif41Corpus(payload, { sourceName: name, debugTrace: trace });
  console.log('OK', r.blocks.length, 'blocks; tops', r.footer.topObjects, 'eof', r.closure.eofExact, 'tail', r.closure.tailBytes);
  for (const d of r.closure.decisions) console.log('  decision:', JSON.stringify(d));
} catch (e) {
  console.log('FAIL:', e.message.slice(0, 300));
  const errs = trace.filter((t) => t.err);
  console.log('TRACE ERRS:', errs.length);
  for (const t of errs.slice(-10)) console.log('  blk', t.blockIndex, t.type, '@', t.start, '->', String(t.err).slice(0, 110));
}
