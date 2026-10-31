// av4_probe.mjs — AV-4 LAYOUT DIFF evidence (read-only): sample NIF 4.0.0.0 /
// 4.0.0.2 members of Models.ark, dump header + first bytes so the 4.0 layout
// is OBSERVED from bytes, cross-checked against the gb12 SDK NiStream canon.
'use strict';
import { promises as fs } from 'node:fs';
import { ArkArchive } from '../../src/pesource/ArkArchive.js';

const MODELS = 'D:\\Eudoria_Reconstruction\\01_Original_Files\\ARK\\Models.ark';
const mbuf = new Uint8Array(await fs.readFile(MODELS));
const ark = new ArkArchive(mbuf);

const v400 = [], v402 = [], other = new Map();
for (const e of ark.entries()) {
  const { payload } = ark.readEntry(e);
  const nl = payload.indexOf(0x0a);
  if (nl < 0 || payload.length < nl + 9) continue;
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const ver = dv.getUint32(nl + 1, true);
  if (ver === 0x04000000) v400.push(e);
  else if (ver === 0x04000002) v402.push(e);
  else other.set(ver, (other.get(ver) ?? 0) + 1);
}
console.log('v400 count', v400.length, 'v402 count', v402.length, 'other', JSON.stringify([...other]));

function hexAt(p, off, len) {
  const { payload } = ark.readEntry(p);
  let s = '';
  for (let i = 0; i < len; i++) s += payload[off + i].toString(16).padStart(2, '0') + ' ';
  return s;
}
function header(p) {
  const { payload } = ark.readEntry(p);
  const nl = payload.indexOf(0x0a);
  const dv = new DataView(payload.buffer, payload.byteOffset, payload.byteLength);
  const text = String.fromCharCode(...payload.subarray(0, nl));
  const ver = dv.getUint32(nl + 1, true);
  const num = dv.getUint32(nl + 5, true);
  return { text, ver: '0x' + ver.toString(16), num, size: payload.length, tail: payload.length - (nl + 9) };
}
// small+large samples each
for (const [label, arr] of [['4.0.0.0', v400], ['4.0.0.2', v402]]) {
  arr.sort((a, b) => a.size - b.size);
  const picks = [arr[0], arr[1], arr[2], arr[Math.floor(arr.length / 2)], arr[arr.length - 1], arr[arr.length - 2]];
  for (const p of picks) {
    const h = header(p);
    console.log(`\n${label} ${p.name} size=${h.size} hdr="${h.text}" numBlocks=${h.num}`);
    // header is: text\n + ver(4) + num(4); blocks start at nl+9
    const { payload } = ark.readEntry(p);
    const nl = payload.indexOf(0x0a);
    const start = nl + 9;
    console.log('  block0 @' + start + ':', hexAt(p, start, 48));
    console.log('  tail(64):', hexAt(p, payload.length - 64, 64));
  }
}
