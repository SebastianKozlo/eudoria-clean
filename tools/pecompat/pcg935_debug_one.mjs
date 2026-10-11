#!/usr/bin/env node
// PRIVATE probe: debug one failing file with block trace.
import fs from 'node:fs';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
import { readNif10Corpus } from '../../src/pecompat/PecNif10CorpusReader.js';

const name = process.argv[2];
const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const entry = archive.entryByName(name);
const { payload } = archive.readEntry(entry);
const trace = [];
let maxBlock = -1;
try {
  const r = readNif10Corpus(payload, { sourceName: name, debugTrace: trace });
  console.log('OK', r.blocks.length);
} catch (e) {
  console.log('FAIL:', e.message.slice(0, 300));
  const errs = trace.filter((t) => t.err);
  console.log('PARSE-ERR ENTRIES:', errs.length);
  for (const t of errs.slice(-12)) console.log('  blk', t.blockIndex, t.type, '@', t.start, '->', t.err);
  const pfail = trace.filter((t) => t.preambleFail);
  console.log('PREAMBLE-FAIL ENTRIES:', pfail.length);
  for (const t of pfail.slice(-8)) console.log('  blk', t.blockIndex, t.type, '@', t.start, 'preamble=0x' + t.preamble.toString(16));
  // reconstruct the DEEPEST chain: walk backwards keeping monotonically increasing blockIndex
  const oks = trace.filter((t) => !t.err && !t.preambleFail);
  console.log('TOTAL TRACE:', trace.length, 'OK ENTRIES:', oks.length);
  // chronological entries around the transition into the failing block:
  let seen158 = 0;
  console.log('TRACE WINDOW (from 5 entries before the first blk-158 OK):');
  let startIdx = trace.findIndex((t) => t.blockIndex === 158 && !t.err && !t.preambleFail);
  for (let i = Math.max(0, startIdx - 4); i < Math.min(startIdx + 12, trace.length); i++) {
    const t = trace[i];
    const tag = t.err ? 'ERR' : (t.preambleFail ? 'PFAIL' : 'OK');
    console.log(`  [${i}] blk ${t.blockIndex} ${t.type} @${t.start}${t.end ? '-' + t.end : ''} ${tag}${t.err ? ' ' + t.err.slice(0, 90) : ''}`);
  }
  void seen158;
  const byIdx = {};
  for (const t of oks) (byIdx[t.blockIndex] ??= []).push(t);
  const idxs = Object.keys(byIdx).map(Number).sort((a, b) => a - b);
  console.log('OK-BY-BLOCKINDEX:', idxs.map((i) => `${i}:${byIdx[i].length}`).join(' '));
  // For the deepest block index reached, show its attempts:
  const maxIdx = idxs[idxs.length - 1];
  if (maxIdx != null) {
    console.log('DEEPEST BLOCK', maxIdx, 'ATTEMPTS:');
    for (const t of byIdx[maxIdx]) console.log('  ', `${t.start}-${t.end}`);
  }
  const chain = [];
  let want = Infinity;
  for (let i = oks.length - 1; i >= 0 && chain.length < 20; i--) {
    if (oks[i].blockIndex < want) { chain.unshift(oks[i]); want = oks[i].blockIndex; }
  }
  console.log('DEEPEST CHAIN (tail):');
  for (const t of chain) console.log('  blk', t.blockIndex, t.type, `${t.start}-${t.end}`);
  console.log('FIRST 8 OK ENTRIES:');
  for (const t of oks.slice(0, 8)) console.log('  blk', t.blockIndex, t.type, `${t.start}-${t.end}`);
}
