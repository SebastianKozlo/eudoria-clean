#!/usr/bin/env node
// PRIVATE probe: hex dump a region of a corpus payload.
import fs from 'node:fs';
import { Bnt2Archive } from '../../src/pesource/Bnt2Archive.js';
const name = process.argv[2];
const from = parseInt(process.argv[3], 10);
const len = parseInt(process.argv[4] ?? '96', 10);
const bytes = new Uint8Array(fs.readFileSync('D:\\Eudoria_Reconstruction\\pcg_install\\Data\\Models\\Models.bnt'));
const archive = new Bnt2Archive(bytes);
const { payload } = archive.readEntry(archive.entryByName(name));
for (let off = from; off < Math.min(from + len, payload.length); off += 16) {
  let hex = '', ascii = '';
  for (let i = 0; i < 16 && off + i < payload.length; i++) {
    const b = payload[off + i];
    hex += b.toString(16).padStart(2, '0') + ' ';
    ascii += (b >= 32 && b < 127) ? String.fromCharCode(b) : '.';
  }
  console.log(off.toString().padStart(6) + ': ' + hex.padEnd(48) + ' ' + ascii);
}
// also show the header + first blocks region: dump the blockTypeIndex from the header
const nl = payload.indexOf(0x0a);
const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
let p = nl + 1;
const version = dv.getUint32(p, true); p += 4;
const userVersion = dv.getUint32(p, true); p += 4;
const numBlocks = dv.getUint32(p, true); p += 4;
const numBlockTypes = dv.getUint16(p, true); p += 2;
const types = [];
for (let i = 0; i < numBlockTypes; i++) {
  const l = dv.getInt32(p, true); p += 4;
  types.push(String.fromCharCode(...payload.subarray(p, p + l))); p += l;
}
const idx = [];
for (let i = 0; i < numBlocks; i++) { idx.push(dv.getUint16(p, true)); p += 2; }
const numGroups = dv.getUint32(p, true); p += 4;
console.log(`\nheader: v=0x${version.toString(16)} user=${userVersion} blocks=${numBlocks} types=${types.join('|')}`);
console.log(`numGroups=${numGroups} dataStart=${p}`);
console.log('first 12 block types:', idx.slice(0, 12).map((i) => types[i]).join(', '));
if (process.argv[5]) {
  const [a, b] = process.argv[5].split('-').map(Number);
  console.log(`block types ${a}..${b}:`, idx.slice(a, b + 1).map((i, k) => `${a + k}=${types[i]}`).join(' '));
}
console.log('blocks 100-112 types:', idx.slice(100, 113).map((i) => types[i]).join(', '));
