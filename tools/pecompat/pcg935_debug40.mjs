#!/usr/bin/env node
// PRIVATE probe: parse the single 4.0.0.2 file (52555.nif).
import fs from 'node:fs';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif41Corpus } from '../../src/pecompat/PecNif41Reader.js';

const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const { payload } = archive.readEntry(archive.entryByName('52555.nif'));
const trace = [];
try {
  const r = readNif41Corpus(payload, { sourceName: '52555.nif', debugTrace: trace });
  console.log('OK blocks', r.blocks.length, 'eof', r.closure.eofExact, 'tail', r.closure.tailBytes);
  const c = {};
  for (const b of r.blocks) c[b.type] = (c[b.type] || 0) + 1;
  console.log('types', JSON.stringify(c));
  for (const d of r.closure.decisions) console.log('decision:', JSON.stringify(d));
} catch (e) {
  console.log('FAIL:', e.message.slice(0, 240));
  const oks = trace.filter((t) => !t.err);
  const maxIdx = oks.length ? Math.max(...oks.map((t) => t.blockIndex)) : -1;
  console.log('deepest OK chain (by block):');
  for (const t of oks.filter((t) => t.blockIndex <= (maxIdx > 4 ? 4 : maxIdx))) {
    console.log('  blk', t.blockIndex, t.type, t.start + '-' + t.end);
  }
  const errs = trace.filter((t) => t.err);
  console.log('ERRS:', errs.length);
  for (const t of errs.slice(0, 8)) console.log('  blk', t.blockIndex, JSON.stringify(t.type).slice(0, 30), '@' + t.start, String(t.err).slice(0, 80));
  const allIdx = [...new Set(trace.map((t) => t.blockIndex))].sort((a, b) => a - b);
  console.log('blocks attempted (ok or err):', allIdx.join(','));
  for (const idx of allIdx) {
    if (idx < 30) continue;
    const rows = trace.filter((t) => t.blockIndex === idx).slice(0, 4);
    for (const t of rows) {
      if (t.err) console.log('  blk', idx, 'ERR @' + t.start, JSON.stringify(String(t.err).slice(0, 100)));
      else console.log('  blk', idx, 'OK', t.type, t.start + '-' + t.end);
    }
  }
}
