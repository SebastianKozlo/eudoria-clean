// av4_debug_walk.mjs — per-block walk trace for one file (diagnostic only).
'use strict';
import { promises as fs } from 'node:fs';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';
import { parseModel40 } from '../../src/pesource/NifModelReader40.js';

const MODELS = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const name = process.argv[2] ?? '41743.nif';
const mbuf = new Uint8Array(await fs.readFile(MODELS));
const ark = new ArkArchive(mbuf);
const e = ark.entries().find(e => e.name === name);
const p = ark.readEntry(e).payload;
try {
  const { extraction } = parseModel40(p, name);
  for (const b of extraction.blocks) {
    console.log(`#${b.index} ${b.type}${b.opaque ? ' [OPAQUE]' : ''} rtti=${b.rttiStart} end=${b.blockEnd} span=${b.blockEnd - b.rttiStart}`);
  }
  console.log('status', extraction.parseStatus, 'tail', extraction.fileTailBytesLen, 'topLevel', JSON.stringify(extraction.topLevelObjects));
} catch (err) {
  console.log('THREW:', err.message);
  let s = '';
  for (let i = 0; i < p.length; i++) {
    if (i % 16 === 0) s += '\n' + i.toString().padStart(4) + ': ';
    s += p[i].toString(16).padStart(2, '0') + ' ';
  }
  console.log(s);
}
